include("../fath-v843/v843_radial.jl")
include("../fath-v843/controls/v843-input/dupont/v843_linked_input.jl")

const V843 = V843LinkedInput

function refine_radial(builder, rings)
    old = builder.grids
    radii = collect(range(first(old.κ),last(old.κ);length=rings))
    edges = [first(radii); (radii[1:end-1] .+ radii[2:end])./2; last(radii)]
    weights = diff(edges.^2)./(4π)
    grids = Runner.QCLNEGF.QCLDomain.ModelGrids(old.x,old.wˣ,old.ε,old.wᴱ,
        old.trusted_energy,radii,weights,old.qᶻ,old.wᑫᶻ,old.φ)
    device = V843.DupontDevice.physical_inputs(21.0)
    cov = V843.V843TailVertices.assemble(device.physical,builder.profiles,grids,builder.scales,device.ifr)
    geometry = builder.geometry
    h = [geometry.Hamiltonian+k^2*geometry.transverse for k in radii]
    return merge(builder,(;grids,cov,nominal_chain_H_by_k=h))
end

function v843_measure(p, source, cuts, workers)
    widths = (cuts[3:end] .- cuts[1:end-2])./2
    image = LT.linked_fresh_map(p,source;projector=LT.project_linked_economical,
        selected_rows=true,projection_for_collision=true,workers)
    observation = spatial_balance(p,image.source,widths;
        workers,energy_rule=independent_energy_rule,current_cuts=cuts)
    fractions = observation.central_bands.fraction
    return (;summary=image.summary,observation,extractor_over_upper=fractions[1]/fractions[3],
        observer_max_difference_A_cm2=maximum(abs.(observation.current_A_cm2 .-
            image.summary["projected_fresh"]["raw_profile_A_cm2"])))
end

function main()
    length(ARGS)==5 || error("Usage: v843_refine.jl ARCHIVE GEOMETRY RINGS WORKERS OUTPUT")
    archive,geometry,rings_arg,workers_arg,output = ARGS
    rings,workers = parse(Int,rings_arg),parse(Int,workers_arg)
    rings in (5,9,17) || error("use a registered nested radial axis")
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    input = Runner._read_linked_checkpoint(archive)
    p = input.problem
    p.nk==5 && isapprox(1000p.geo.voltage/(last(input.current_midpoints)-first(input.current_midpoints)),21.0) ||
        error("expected the common V843 21 kV/cm archive with five rings")
    old_k = Runner._read_linked_array(archive,"k",Float64,p.nk)
    builder = V843.new_input(21.0;Nk=9,geometry_file=geometry)
    builder.hdf_geometry_sha256==input.identity["source_geometry_model_sha256"] ||
        error("unexpected V843 geometry")
    TOML.parsefile(joinpath(archive,"spec.toml"))["device_sha256"]==builder.source_device_sha256 ||
        error("unexpected V843 device")
    if rings==17
        builder = refine_radial(builder,rings)
    end
    mapped = rings==5 ? (;linked=p,mapped_source=input.seed,transfer=Matrix{Float64}(I,5,5),new_k=old_k) :
        expand_rings(input,old_k,builder)
    if rings==17
        # The 9-ring checks ensure that refinement preserves its existing vertices too.
        nine = V843.new_input(21.0;Nk=9,geometry_file=geometry)
        nested = [argmin(abs.(mapped.new_k .- k)) for k in nine.grids.κ]
        mapped.new_k[nested] ≈ nine.grids.κ || error("nine-ring grid not nested")
        for (old,new) in ((nine.cov.ifr_pair,builder.cov.ifr_pair[nested,nested]),
                (nine.cov.lo,view(builder.cov.lo,:,:,nested,nested)),
                (nine.cov.impurity,view(builder.cov.impurity,:,:,nested,nested)))
            isapprox(old,new;rtol=2e-12) || error("a vertex changed on the nine-ring grid")
        end
    end
    println(stderr,"checkpoint verified and $rings-ring problem constructed in RAM")
    flush(stderr)
    result = v843_measure(mapped.linked,mapped.mapped_source,input.current_midpoints,workers)
    report = (;schema="qcl-negf-v843-common-seed-radial/v1",input.identity,
        core=Runner._linked_package_identity(Runner.QCLNEGF),
        runner=Runner._linked_package_identity(Runner),runtime=Runner._runtime_toolchain_provenance(),
        source_sha256=bytes2hex(open(sha256,@__FILE__)),rings,workers,
        geometry_sha256=builder.hdf_geometry_sha256,device_sha256=builder.source_device_sha256,
        radial_nodes=mapped.new_k,radial_weights=mapped.linked.wk,
        transfer=[collect(row) for row in eachrow(mapped.transfer)],
        cuts_nm=input.current_midpoints,result...)
    open(output,"w") do io
        Runner._light_json(io,report)
        println(io)
    end
end

abspath(PROGRAM_FILE)==abspath(@__FILE__) && main()
