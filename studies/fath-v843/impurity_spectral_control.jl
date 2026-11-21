include("direct_continuum.jl")

function candidate_inverse(p, prepared, energies, coefficients, rings, workers)
    inverse = [Vector{Matrix{ComplexF64}}(undef,length(energies)) for _ in rings]
    for start in 1:96:length(energies)
        block = start:min(start+95,length(energies))
        nodes = @view energies[block]
        queries = LT.shifted_queries(p.geo,nodes)
        elastic = DirectImpurity.direct_convolution(p,prepared.seed_total,prepared.anchor,
            queries,coefficients...;workers)
        causality = LT.CausalRows(p.en,queries)
        for (i,k) in enumerate(rings)
            ws = LT.TailWorkspace(p.geo)
            fixed = LT.sample_packed_ring(causality,@view(prepared.fresh_other[:,:,:,k]),
                @view(prepared.anchor_other[:,:,k]))
            @views for (j,e) in enumerate(nodes)
                ws.triplets .= fixed[:,:,:,j,:] .+ elastic.fields[:,:,:,elastic.location[j,:],k]
                LT.assemble_sources!(ws,p.geo,ws.triplets)
                inverse[i][block[j]] = e.*p.geo.metric .- p.h[:,:,k] .- ws.mode_source[:,:,1]
            end
        end
    end
    return inverse
end

function candidate_poles(p, prepared, coefficients, rings, points, workers)
    sampled = candidate_inverse(p,prepared,points,coefficients,rings,workers)
    initial = [LT.crossings(ds,points) for ds in sampled]
    brackets = [(;ring=i,interval) for (i,x) in enumerate(initial) for interval in x]
    isempty(brackets) && error("no crossings in the exact direct inverse")
    for step in 1:20
        locations = [(x.interval.lo+x.interval.hi)/2 for x in brackets]
        sampled = candidate_inverse(p,prepared,locations,coefficients,rings,workers)
        brackets = map(enumerate(brackets)) do (j,x)
            r = x.interval
            e = locations[j]
            f = eigvals(LT.hermitian_part(sampled[x.ring][j]))[r.eigindex]
            next = signbit(f)==signbit(r.f_lo) ? LT.Crossing(r.eigindex,e,r.hi,f,r.f_hi) :
                LT.Crossing(r.eigindex,r.lo,e,r.f_lo,f)
            return (;x.ring,interval=next)
        end
        if step%5==0
            println(stderr,"candidate pole bisection $step/20 on $(length(brackets)) intervals")
            flush(stderr)
        end
    end
    locations = map(brackets) do x
        r = x.interval
        e = (r.f_hi*r.lo-r.f_lo*r.hi)/(r.f_hi-r.f_lo)
        return isfinite(e) ? clamp(e,r.lo,r.hi) : (r.lo+r.hi)/2
    end
    sampled = candidate_inverse(p,prepared,locations,coefficients,rings,workers)
    return map(enumerate(brackets)) do (j,x)
        D = sampled[x.ring][j]
        r = x.interval
        modes = eigen(LT.hermitian_part(D))
        v = @view modes.vectors[:,r.eigindex]
        slope = (r.f_hi-r.f_lo)/(r.hi-r.lo)
        width = abs(imag(dot(v,D*v)))/max(abs(slope),1e-15)
        (;ring=rings[x.ring],energy=locations[j],width,residual=abs(modes.values[r.eigindex]))
    end
end

function reference_poles(p, prepared, selected_rings, workers)
    support = LT.tapered_support(p.en)
    reference = Vector{Any}(undef,p.nk)
    LT.N._production_worker_ranges!(p.nk,min(workers,p.nk)) do _,lo,hi
        @views for k in lo:hi
            layout=LT.CausalGeometry(p.en,support,Matrix(prepared.anchor[:,:,k]),
                p.geo.voltage,maximum(abs,p.geo.offsets))
            old=LT.CausalRing(layout,LT.unpack_ring(prepared.seed_total[:,:,:,k],p.r))
            frozen=prepared.fresh_other[:,:,:,k]+prepared.fresh_channel[:,:,:,k]
            canonical=LT.CausalRing(layout,LT.unpack_ring(frozen,p.r))
            old_scan=LT.scan_poles(old,p.geo,p.h[:,:,k];subdivisions=1)
            translated = [(;energy=x.energy-j*p.geo.voltage,width=x.width)
                for x in old_scan.poles for j in p.geo.offsets
                if -0.90 <= x.energy-j*p.geo.voltage <= 1.40]
            fresh = if k in selected_rings
                [(;x.energy,x.width) for x in LT.scan_poles(canonical,p.geo,p.h[:,:,k];subdivisions=1).poles]
            else
                NamedTuple{(:energy,:width),Tuple{Float64,Float64}}[]
            end
            reference[k] = (;translated, fresh)
        end
    end
    return [vcat([x.translated for x in reference]...); vcat([x.fresh for x in reference]...)]
end

function protected_rules(p, poles, references, plain_points, order)
    extent = extrema(p.en)
    centers=[[(;x.energy,x.width) for x in poles]; references]
    sort!(centers;by=x->(x.energy,x.width))
    grouped = eltype(centers)[]
    for x in centers
        first(extent)<x.energy<last(extent) || continue
        if isempty(grouped) || x.energy-last(grouped).energy>1e-12
            push!(grouped,x)
        elseif x.width<last(grouped).width
            grouped[end]=x
        end
    end
    transform = LT.resonance_rule((;geometry=(;energy=p.en)),
        (;points=plain_points,poles=grouped),order)
    return (;points=transform.points,weights=transform.weights,pole_count=length(grouped))
end

function restricted_spectra(directory, reference, digest, output, workers)
    saved=Runner._read_linked_checkpoint(directory)
    p=saved.problem
    old=packed_control(reference,saved,digest)
    prepared=prepared_arms(p,saved.seed,old.fresh)
    coefficients=Tuple(old.summary["input_pair_projection"][key] for key in COEFFICIENTS)
    rings=collect(1:3)
    geometry=LT.CausalGeometry(p.en,LT.tapered_support(p.en),Matrix(prepared.anchor[:,:,1]),
        p.geo.voltage,maximum(abs,p.geo.offsets))
    adapted=LT.CausalRing(geometry,LT.unpack_ring(@view(prepared.seed_total[:,:,:,1]),p.r))
    initial=LT.translated_knots(adapted,2)
    references=reference_poles(p,prepared,rings,workers)
    # Bracket direct roots on both sides of the incoming narrow poles as well
    # as on the nominal shifted cells. The final rule then uses all roots.
    search_nodes = copy(initial)
    for x in references, σ in (-3,0,3)
        node=x.energy+σ*max(x.width,1e-10)
        first(initial)<node<last(initial) && push!(search_nodes,node)
    end
    sort!(unique!(search_nodes))
    poles=candidate_poles(p,prepared,coefficients,rings,search_nodes,workers)
    rule=protected_rules(p,poles,references,initial,9)
    println(stderr,"$(length(poles)) exact direct crossings, $(rule.pole_count) common protected poles, $(length(rule.points)) samples")
    flush(stderr)
    accumulated=nothing
    for start in 1:96:length(rule.points)
        chunk=start:min(start+95,length(rule.points))
        energies=@view rule.points[chunk]
        weights=@view rule.weights[chunk]
        table=DirectImpurity.direct_convolution(p,prepared.seed_total,prepared.anchor,
            LT.shifted_queries(p.geo,energies),coefficients...;workers)
        observed=map(rings) do k
            ring_test(p,k,energies,weights,prepared.seed_total,prepared.seed_channel,
                prepared.fresh_other,prepared.fresh_channel,prepared.anchor,prepared.anchor_other,
                table,coefficients,IMP)
        end
        accumulated=isnothing(accumulated) ? observed : map(add_raw,accumulated,observed)
        if last(chunk)%1920==0 || last(chunk)==length(rule.points)
            println(stderr,"integrated $(last(chunk)) of $(length(rule.points)) points")
            flush(stderr)
        end
    end
    closure=formatted_arms(p,accumulated,saved.current_midpoints;full_window=true)
    ring_diagnostics=map(zip(rings,accumulated)) do (index,witness)
        metrics=formatted_arms(p,[witness],saved.current_midpoints;full_window=true)
        return (;index, arms=Dict(key=>(;spectral_defect=only(x.spectral_defect_by_ring),
            x.weighted_rK,x.raw_sheet_cm2,x.profile_statistics) for (key,x) in metrics))
    end
    maximum_residual=maximum(x.residual for x in poles)
    report=(;schema="qcl-negf-fath-impurity-spectral-control/v1",identity=saved.identity,
        reference_digest=digest,rings,current_midpoints_nm=saved.current_midpoints,
        exact_crossings=length(poles),maximum_residual,protected_poles=rule.pole_count,
        quadrature_samples=length(rule.points),partial_ring_sums=closure,ring_diagnostics,
        provenance=(;core=Runner._linked_package_identity(Runner.QCLNEGF),
            runner=Runner._linked_package_identity(Runner),
            sources=Dict(name=>bytes2hex(open(sha256,joinpath(@__DIR__,name)))
                for name in ("spatial_balance.jl","direct_impurity.jl","direct_ifr.jl",
                    "impurity_experiment.jl","direct_continuum.jl","impurity_spectral_control.jl"))))
    open(output,"w") do io
        Runner._light_json(io,report)
        println(io)
    end
end

if abspath(PROGRAM_FILE)==abspath(@__FILE__)
    length(ARGS)==5 || error("Usage: impurity_spectral_control.jl ARCHIVE FROZEN_RUN FRESH_SHA256 OUTPUT WORKERS")
    input,reference,digest,output,workers=ARGS
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    restricted_spectra(input,reference,digest,output,parse(Int,workers))
end
