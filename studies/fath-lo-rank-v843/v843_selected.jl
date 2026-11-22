include("v843_refine.jl")

# These are exactly the projected input and collision stages of linked_fresh_map.
# During replay, the discarded nodal and fresh observations do not feed the seed.
function replay_source!(p, seed, workers, maps)
    fresh = similar(seed)
    normalized = zeros(p.r^2,2,p.ne,p.nk)
    anchor = dropdims(sum(p.const_by_channel;dims=4);dims=4)
    for iteration in 1:maps
        total = dropdims(sum(seed;dims=5);dims=5)
        projected = LT.projected_image(p,total,anchor,:input_projected;
            projector=LT.project_linked_economical,selected_rows=true,order=18,
            subdivisions=2,grading=true,workers,observe=_->nothing)
        LT.prepare_occupation!(normalized,projected,p)
        LT.scatter_packed!(fresh,normalized,p.v)
        seed .= (1-0.35) .* seed .+ 0.35 .* fresh
        println(stderr,"replayed V843 input update $iteration of $maps")
        flush(stderr)
    end
    return seed
end

function selected_radial()
    length(ARGS)==5 || error("Usage: v843_selected.jl ARCHIVE GEOMETRY UPDATES WORKERS OUTPUT_DIRECTORY")
    archive,geometry,updates_arg,workers_arg,output = ARGS
    updates,workers = parse(Int,updates_arg),parse(Int,workers_arg)
    updates in (0,47) || error("use the zero-update control or the published 48th map")
    isdir(output) || error("output directory must already exist")
    all(rings->!ispath(joinpath(output,"v843-selected-$rings.json")),(5,9,17)) ||
        error("refusing to overwrite an existing selected radial report")
    BLAS.set_num_threads(1)
    input = Runner._read_linked_checkpoint(archive)
    p = input.problem
    p.nk==5 && isapprox(1000p.geo.voltage/(last(input.current_midpoints)-first(input.current_midpoints)),21.0) ||
        error("expected the common V843 21 kV/cm archive with five rings")
    old_k=Runner._read_linked_array(archive,"k",Float64,p.nk)
    original=V843.new_input(21.0;Nk=9,geometry_file=geometry)
    original.hdf_geometry_sha256==input.identity["source_geometry_model_sha256"] ||
        error("unexpected V843 geometry")
    TOML.parsefile(joinpath(archive,"spec.toml"))["device_sha256"]==original.source_device_sha256 ||
        error("unexpected V843 device")
    published = updates==47 ? Runner.YAML.load_file(
        joinpath(@__DIR__,"../fath-v843/evidence/v843-f21.json")) : nothing
    if !isnothing(published)
        input.identity == published["identity"] || error("archive identity differs from the published run")
        published["selected_iteration"]==updates+1 && published["configuration"]["alpha"]==0.35 &&
            published["configuration"]["measure"]=="projected" ||
            error("published replay conditions differ")
    end
    replay_source!(p,input.seed,workers,updates)
    seed_sha256=bytes2hex(sha256(reinterpret(UInt8,vec(input.seed))))
    for rings in (5,9,17)
        reference = if isnothing(published) || rings==17
            nothing
        elseif rings==5
            published["observed"]
        else
            published["paired_controls"]["radial"]["observation"]
        end
        run_radial_condition(input,original,old_k,updates,workers,output,seed_sha256,rings;reference)
        GC.gc()
    end
end

function run_radial_condition(input, original, old_k, updates, workers, output, seed_sha256, rings; reference)
    p = input.problem
    builder = rings==17 ? refine_radial(original,17) : original
    mapped = rings==5 ? (;linked=p,mapped_source=input.seed,transfer=Matrix{Float64}(I,5,5),new_k=old_k) :
        expand_rings(input,old_k,builder)
    if rings==17
        nested = [argmin(abs.(mapped.new_k.-k)) for k in original.grids.κ]
        mapped.new_k[nested] ≈ original.grids.κ || error("nine-ring grid not nested")
        for (old,new) in ((original.cov.ifr_pair,builder.cov.ifr_pair[nested,nested]),
                (original.cov.lo,view(builder.cov.lo,:,:,nested,nested)),
                (original.cov.impurity,view(builder.cov.impurity,:,:,nested,nested)),
                (original.nominal_chain_H_by_k,builder.nominal_chain_H_by_k[nested]))
            @assert isapprox(old,new;rtol=2e-12)
        end
    end
    println(stderr,"starting selected V843 map at $rings rings")
    flush(stderr)
    result=v843_measure(mapped.linked,mapped.mapped_source,input.current_midpoints,workers)
    report=(;schema="qcl-negf-v843-selected-radial/v1",input.identity,seed_sha256,updates,
        core=Runner._linked_package_identity(Runner.QCLNEGF),
        runner=Runner._linked_package_identity(Runner),runtime=Runner._runtime_toolchain_provenance(),
        source_sha256=Dict(file=>bytes2hex(open(sha256,joinpath(@__DIR__,file)))
            for file in ("v843_selected.jl","v843_refine.jl")),
        rings,workers,geometry_sha256=builder.hdf_geometry_sha256,device_sha256=builder.source_device_sha256,
        radial_nodes=mapped.new_k,radial_weights=mapped.linked.wk,
        transfer=[collect(row) for row in eachrow(mapped.transfer)],cuts_nm=input.current_midpoints,result...)
    open(joinpath(output,"v843-selected-$rings.json"),"w") do io
        Runner._light_json(io,report)
        println(io)
    end
    if !isnothing(reference)
        prior = reference["central_bands"]["fraction"]
        profile_difference = maximum(abs.(result.observation.current_A_cm2.-reference["current_A_cm2"]))
        temperature_difference = abs(result.observation.equivalent_temperature_K-reference["equivalent_temperature_K"])
        ratio_difference = abs(result.extractor_over_upper-prior[1]/prior[3])
        profile_difference <= 1e-4 && temperature_difference <= 1e-6 && ratio_difference <= 1e-7 ||
            error("replayed $rings-ring map disagrees with the published reference")
        println(stderr,"reproduced published $rings-ring profile: difference ",profile_difference," A/cm²")
        flush(stderr)
    end
end

abspath(PROGRAM_FILE)==abspath(@__FILE__) && selected_radial()
