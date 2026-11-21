include("profile_experiment.jl")
using TOML

function annular_transfer(old, new, old_weights, new_weights)
    boundaries(k) = [first(k); (k[1:end-1] .+ k[2:end])./2; last(k)].^2
    a,b = boundaries(old),boundaries(new)
    first(a)==first(b) && last(a)==last(b) ||
        throw(ArgumentError("radial refinement changed the physical domain"))
    transfer = [max(0.0,min(a[j+1],b[i+1])-max(a[j],b[i]))/(b[i+1]-b[i])
        for i in eachindex(new), j in eachindex(old)]
    isapprox(vec(sum(transfer;dims=2)),ones(length(new));rtol=2e-13) &&
        isapprox(transfer'*new_weights,old_weights;rtol=2e-13) ||
        error("annular projection did not preserve the radial measure")
    return transfer
end

function expand_rings(old, old_k, builder)
    (;problem,seed) = old
    layout, cov, grids = builder.geometry,builder.cov,builder.grids
    isequal(layout.W,problem.geo.modes) && isequal(layout.Q,problem.v.coordinate_frame) &&
        layout.offsets==problem.geo.offsets && layout.drop==problem.geo.voltage ||
        error("the refined radial builder returned different coordinate geometry")
    new_k, new_weights = grids.κ,grids.wᵏ
    new_h = cat(builder.nominal_chain_H_by_k...;dims=3)
    candidate_h = [argmin(abs.(new_k .- radius)) for radius in old_k]
    new_k[candidate_h] ≈ old_k || error("the old radii are not nested")
    vertices = problem.v
    checks = (
        H=(problem.h, new_h[:,:,candidate_h]),
        hops=(problem.hops, repeat(builder.physical_hop,1,problem.nk)),
        acoustic=(vertices.acoustic, cov.acoustic),
        alloy=(vertices.alloy, cov.alloy),
        bose=(vertices.bose, cov.bose),
        interface_probes=(vertices.interface_probes, cov.interfaces*layout.Q),
        interface_pair=(vertices.interface_pair, cov.ifr_pair[candidate_h,candidate_h]),
        impurity=(vertices.impurity_covariance, @view cov.impurity[:,:,candidate_h,candidate_h]),
        LO=(vertices.lo_covariance, @view cov.lo[:,:,candidate_h,candidate_h]),
    )
    for (name,(original,refined)) in pairs(checks)
        isapprox(original,refined;rtol=2e-12) ||
            error("the radial builder changed $name at common nodes")
    end
    transfer = annular_transfer(old_k,new_k,problem.wk,new_weights)
    r, ne, nk = problem.r,problem.ne,length(new_k)
    mapped_source = zeros(r^2,2,ne,nk,length(LT.COLLISION_CHANNELS))
    mapped_anchor = zeros(ComplexF64,r,r,nk,length(LT.COLLISION_CHANNELS))
    @views for j in eachindex(old_k), i in eachindex(new_k)
        weight=transfer[i,j]
        iszero(weight) && continue
        mapped_source[:,:,:,i,:] .+= weight .* seed[:,:,:,j,:]
        mapped_anchor[:,:,i,:] .+= weight .* problem.const_by_channel[:,:,j,:]
    end
    kernels=LT.LocalCollisionKernels(layout.Q,new_weights,cov.acoustic,cov.alloy,
        cov.interfaces,cov.ifr_pair,cov.lo,cov.impurity,problem.v.lo_plus,problem.v.lo_minus,cov.bose)
    linked=LT.LinkedProblem(problem.en,problem.we,new_weights,layout.W,problem.nb,
        layout.offsets,layout.drop,problem.geo.reach,new_h,
        repeat(builder.physical_hop,1,nk),mapped_anchor,kernels;
        spin_degeneracy=problem.spin_degeneracy,current_scale=problem.current_scale,
        density_scale=problem.density_scale,target_dimless=problem.target_dimless)
    return (;linked,mapped_source,transfer,new_k)
end

function run_radial_control(directory,input_builder,builder_path,geometry_path,measure,workers)
    measure in ("projected","normalized-nodal") || throw(ArgumentError("unknown collision measure"))
    original=Runner._read_linked_checkpoint(directory)
    p=original.problem
    old_k=Runner._read_linked_array(directory,"k",Float64,p.nk)
    cuts=original.current_midpoints
    field=1000p.geo.voltage/(last(cuts)-first(cuts))
    expected_field=isapprox(field,21.0) ? 21.0 : 12.5
    isapprox(field,expected_field) || error("archive field is neither V843 target field")
    archive_builder=input_builder.new_input(expected_field;
        NE=121,Nk=9,geometry_file=geometry_path)
    archive_builder.hdf_geometry_sha256==original.identity["source_geometry_model_sha256"] ||
        error("refined radial builder has a different archived geometry identity")
    spec=TOML.parsefile(joinpath(directory,"spec.toml"))
    archive_builder.source_device_sha256==spec["device_sha256"] ||
        error("refined radial builder has a different physical device")
    revised=expand_rings(original,old_k,archive_builder)
    widths=(cuts[3:end] .- cuts[1:end-2])./2
    rows = map(((p,original.seed),(revised.linked,revised.mapped_source))) do (q,seed)
        sample=LT.linked_fresh_map(q,seed;projector=LT.project_linked_economical,
            selected_rows=true,projection_for_collision=measure=="projected",workers)
        observation=spatial_balance(q,sample.source,widths;
            workers,energy_rule=independent_energy_rule,current_cuts=cuts)
        return (;summary=sample.summary,observation)
    end
    return (;schema="qcl-negf-v843-radial-control/v1",identity=original.identity,
        provenance=(;core=Runner._linked_package_identity(Runner.QCLNEGF),
            runner=Runner._linked_package_identity(Runner),
            sources=Dict(name=>bytes2hex(open(sha256,joinpath(@__DIR__,name)))
                for name in ("spatial_balance.jl","profile_experiment.jl","v843_radial.jl"))),
        runtime=Runner._runtime_toolchain_provenance(),
        physics_builder_source_sha256=bytes2hex(open(sha256,builder_path)),
        old_radial_grid_sha256=bytes2hex(open(sha256,joinpath(directory,"k.bin"))),
        geometry_sha256=archive_builder.hdf_geometry_sha256,
        device_sha256=archive_builder.source_device_sha256,
        current_midpoints_nm=cuts, measure, old_k, new_k=revised.new_k,
        projected_radial_transfer=[collect(row) for row in eachrow(revised.transfer)],
        old=rows[1], refined=rows[2],
        profile_max_difference_A_cm2=maximum(abs.(rows[1].observation.current_A_cm2 .-
            rows[2].observation.current_A_cm2)))
end

if abspath(PROGRAM_FILE)==abspath(@__FILE__)
    length(ARGS)==6 ||
        error("Usage: v843_radial.jl ARCHIVE BUILDER.jl GEOMETRY.h5 OUTPUT MEASURE WORKERS")
    archive,builder,geometry,output,measure,worker_argument=ARGS
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    include(abspath(builder))
    report=run_radial_control(archive,V843LinkedInput,builder,geometry,measure,parse(Int,worker_argument))
    open(output,"w") do io
        Runner._light_json(io,report)
        println(io)
    end
end
