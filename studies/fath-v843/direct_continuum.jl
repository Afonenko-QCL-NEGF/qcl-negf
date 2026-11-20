include("impurity_experiment.jl")
using TOML

function packed_control(path,saved,digest)
    summary=TOML.parsefile(joinpath(path,"summary.toml"))
    summary["input_spec_sha256"]==saved.identity["input_spec_sha256"] ||
        error("frozen output refers to a different seed or device")
    fresh=Runner._read_linked_array(path,"fresh_source_LG_packed",Float64,size(saved.seed)...)
    bytes2hex(sha256(reinterpret(UInt8,vec(fresh))))==digest ||
        error("frozen source differs from the accepted archived reference")
    return (;summary,fresh)
end

function array_breakpoints(p,preparation,occupied_window,subdivisions,workers)
    (;seed_total,fresh_other,fresh_channel,anchor)=preparation
    fresh_total=fresh_other+fresh_channel
    pins=Vector{Vector{Float64}}(undef,p.nk)
    extent=extrema(p.en)
    support=LT.tapered_support(p.en)
    LT.N._production_worker_ranges!(p.nk,min(workers,p.nk)) do _,lo,hi
        @views for k in lo:hi
            geometry=LT.CausalGeometry(p.en,support,Matrix(anchor[:,:,k]),
                p.geo.voltage,maximum(abs,p.geo.offsets))
            scan(field)=LT.scan_poles(LT.CausalRing(geometry,LT.unpack_ring(field,p.r)),
                p.geo,p.h[:,:,k];subdivisions)
            before,after=scan(seed_total[:,:,:,k]),scan(fresh_total[:,:,:,k])
            nodes=copy(after.points)
            for pole in after.poles
                width=max(pole.width,1e-10)
                append!(nodes,pole.energy .+ width.*[-5,0,5])
            end
            for pole in before.poles, offset in p.geo.offsets
                incoming=pole.energy-offset*p.geo.voltage
                if first(occupied_window)<=incoming<=last(occupied_window)
                    width=max(pole.width,1e-10)
                    append!(nodes,incoming .+ width.*[-5,0,5])
                end
            end
            pins[k]=filter(x->first(extent)<=x<=last(extent),nodes)
        end
    end
    values=sort!([first(extent);vcat(pins...);last(extent)])
    knots=Float64[first(values)]
    tolerance=64eps(Float64)*max(1.0,maximum(abs,extent))
    for x in values[2:end]
        x-last(knots)>tolerance && push!(knots,x)
    end
    knots[end]=last(extent)
    return knots
end

function shared_measure(knots,order)
    rule=LT.gauss_rule(order)
    weights=Float64[]
    energies=Float64[]
    for (lo,hi) in zip(knots[1:end-1],knots[2:end])
        e,w=LT.integrate_panel(lo,hi,nothing,rule;grading=false)
        append!(energies,e)
        append!(weights,w)
    end
    isapprox(sum(weights),last(knots)-first(knots);rtol=2e-13) &&
        all(>(0),weights) || error("shared positive energy measure lost its mass")
    return energies,weights
end

function add_raw(a,b)
    return NamedTuple{keys(a)}(map(+,values(a),values(b)))
end

function canonical_on_shared_measure(p,preparation,energies,weights,workers)
    cell=clamp.(searchsortedlast.(Ref(p.en),energies),1,p.ne-1)
    rule=(points=energies,weights=weights,cell=cell)
    function shared_projector(ring,tail,h,hops,radial;sampler,kwargs...)
        result=LT.integrate_linked(ring,tail,h,hops,rule,radial;sampler,project=true)
        return (;result,poles=(poles=(),),rule)
    end
    return LT.projected_image(p,preparation.fresh_other+preparation.fresh_channel,
        preparation.anchor,:common_preflight;projector=shared_projector,selected_rows=true,
        order=2,subdivisions=1,grading=false,workers,observe=_->nothing).raw
end

function whole_profile(directory,reference,digest,order,subdivisions,workers;baseline_only=false)
    saved=Runner._read_linked_checkpoint(directory)
    p=saved.problem
    controlled=packed_control(reference,saved,digest)
    coefficients=Tuple(controlled.summary["input_pair_projection"][key] for key in COEFFICIENTS)
    prepared=prepared_arms(p,saved.seed,controlled.fresh)
    provenance=(;core=Runner._linked_package_identity(Runner.QCLNEGF),
        runner=Runner._linked_package_identity(Runner),runtime=Runner._runtime_toolchain_provenance(),
        sources=Dict(name=>bytes2hex(open(sha256,joinpath(@__DIR__,name)))
            for name in ("spatial_balance.jl","direct_impurity.jl","direct_ifr.jl","impurity_experiment.jl","direct_continuum.jl")))
    # On the accepted archive 99.98% of the occupied quadrature mass lies
    # between these conservative limits. All three arms also integrate the
    # whole outer region; only the additional shifted pole panel knots differ.
    occupied_window=(-0.90,1.40)
    knots=array_breakpoints(p,prepared,occupied_window,subdivisions,workers)
    energies,weights=shared_measure(knots,order)
    println(stderr,"whole window with $(length(knots)-1) common panels and $(length(energies)) samples")
    flush(stderr)
    canonical=canonical_on_shared_measure(p,prepared,energies,weights,workers)
    current_reference=controlled.summary["projected_fresh"]["raw_profile_A_cm2"]
    difference=maximum(abs.(canonical["raw_profile_A_cm2"] .- current_reference))
    spectral=maximum(canonical["spectral_weight_relative_by_ring"])
    tolerance=max(1.0,0.01abs(sum(current_reference)/length(current_reference)))
    preflight=(;baseline_maximum_current_difference_A_cm2=difference,
        maximum_spectral_defect=spectral,canonical,
        admitted=difference<=tolerance && spectral<1e-3)
    println(stderr,"common baseline preflight: difference $difference A/cm², spectral defect $spectral")
    flush(stderr)
    if baseline_only || !preflight.admitted
        return (;schema="qcl-negf-linked-direct-continuum-preflight/v1",
            identity=saved.identity,source_digest=digest,provenance,order,subdivisions,
            shared_samples=length(energies),preflight)
    end
    accumulator=nothing
    unique_queries_in_tiles=0
    for start in 1:96:length(energies)
        block=start:min(start+95,length(energies))
        nodes=@view energies[block]
        measure=@view weights[block]
        table=DirectImpurity.direct_convolution(p,prepared.seed_total,prepared.anchor,
            LT.shifted_queries(p.geo,nodes),coefficients...;workers)
        values=raw_arms(p,prepared,nodes,measure,table,coefficients;workers)
        unique_queries_in_tiles+=length(table.queries)
        accumulator=isnothing(accumulator) ? values : map(add_raw,accumulator,values)
        if last(block)%1920==0 || last(block)==length(energies)
            println(stderr,"completed $(last(block)) of $(length(energies)) points")
            flush(stderr)
        end
    end
    arms=formatted_arms(p,accumulator,saved.current_midpoints;full_window=true)
    baseline=arms["baseline_PV"].profile_A_cm2
    return (;
        schema="qcl-negf-linked-direct-continuum/v1",identity=saved.identity,provenance,
        canonical_fresh_source_sha256=digest,current_midpoints_nm=saved.current_midpoints,
        order,subdivisions,shared_panels=length(knots)-1,shared_samples=length(energies),
        unique_translated_queries_counted_per_tile=unique_queries_in_tiles,workers,
        energy_interval_meV=100 .* [first(knots),last(knots)],
        more_panel_knots_in_meV=100 .* collect(occupied_window),
        baseline_maximum_current_difference_A_cm2=maximum(abs.(baseline.-current_reference)),
        preflight,
        fixed_normalization=NamedTuple{(:a,:c)}(coefficients),arms,
    )
end

if abspath(PROGRAM_FILE)==abspath(@__FILE__)
    length(ARGS) in (7,8) ||
        error("Usage: direct_continuum.jl ARCHIVE FROZEN_RUN FRESH_SHA256 OUTPUT ORDER SUBDIVISIONS WORKERS [preflight]")
    input,reference,digest,output,order,subdivisions,workers=ARGS[1:7]
    length(ARGS)==8 && ARGS[8]!="preflight" && error("unknown optional argument")
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    report=whole_profile(input,reference,digest,parse.(Int,(order,subdivisions,workers))...;
        baseline_only=length(ARGS)==8)
    open(output,"w") do io
        Runner._light_json(io,report)
        println(io)
    end
end
