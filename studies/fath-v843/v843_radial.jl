include("continuation.jl")
using TOML

function cell_transfer(old_edges, new_edges, old_weights, new_weights)
    isapprox(first(old_edges),first(new_edges);atol=2e-14) &&
        isapprox(last(old_edges),last(new_edges);rtol=2e-13) ||
        throw(ArgumentError("the two cell measures cover different domains"))
    transfer = [max(0.0,min(old_edges[j+1],new_edges[i+1])-max(old_edges[j],new_edges[i])) /
        (new_edges[i+1]-new_edges[i]) for i in eachindex(new_weights), j in eachindex(old_weights)]
    isapprox(vec(sum(transfer;dims=2)),ones(length(new_weights));rtol=2e-13) &&
        isapprox(transfer'*new_weights,old_weights;rtol=2e-13) ||
        error("positive cell projection did not preserve the measure")
    return transfer
end

function annular_transfer(old, new, old_weights, new_weights)
    boundaries(k) = [first(k); (k[1:end-1] .+ k[2:end])./2; last(k)].^2
    return cell_transfer(boundaries(old),boundaries(new),old_weights,new_weights)
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

function coarsen_energy(saved, previous, coarse)
    fine,other=saved.problem,coarse.problem
    for key in ("W.bin","Q.bin","H.bin","hop.bin","weights_k.bin","anchor_by_channel.bin",
        "acoustic.bin","alloy.bin","ifr_sites.bin","ifr_pair.bin","lo_covariance.bin","impurity_covariance.bin")
        saved.identity["asset_sha256"][key]==coarse.identity["asset_sha256"][key] ||
            error("energy control changes the physical asset $key")
    end
    fine.geo.voltage==other.geo.voltage && fine.geo.offsets==other.geo.offsets &&
        fine.geo.reach==other.geo.reach && fine.target_dimless==other.target_dimless &&
        fine.v.bose==other.v.bose && fine.spin_degeneracy==other.spin_degeneracy &&
        extrema(fine.en)==extrema(other.en) || error("energy control changed the physical problem")
    edges(weights) = [0.; cumsum(weights)]
    transfer = cell_transfer(edges(fine.we),edges(other.we),fine.we,other.we)
    new_source = fill!(similar(coarse.seed),0)
    @views for j in 1:fine.ne,i in 1:other.ne
        weight = transfer[i,j]
        iszero(weight) && continue
        new_source[:,:,i,:,:] .+= weight .* previous[:,:,j,:,:]
    end
    return new_source
end

function compare_grid(p, previous, baseline, cuts, measure, workers)
    widths=(cuts[3:end] .- cuts[1:end-2])./2
    sample=LT.linked_fresh_map(p,previous;projector=LT.project_linked_economical,
        selected_rows=true,projection_for_collision=measure=="projected",workers)
    observation=spatial_balance(p,sample.source,widths;
        workers,energy_rule=independent_energy_rule,current_cuts=cuts)
    return (;summary=sample.summary,observation,
        profile_max_difference_A_cm2=maximum(abs.(observation.current_A_cm2.-baseline.current_A_cm2)),
        mean_difference_A_cm2=observation.current.mean_internal_A_cm2-baseline.current.mean_internal_A_cm2)
end

function run_v843(directory,coarse_directory,input_builder,builder_path,geometry_path,maps,alpha,measure,workers)
    function selected_controls(saved, previous, baseline)
        p=saved.problem
        old_k=Runner._read_linked_array(directory,"k",Float64,p.nk)
        cuts=saved.current_midpoints
        field=1000p.geo.voltage/(last(cuts)-first(cuts))
        expected_field=isapprox(field,21.0) ? 21.0 : 12.5
        isapprox(field,expected_field) || error("archive field is neither V843 target field")
        builder=input_builder.new_input(expected_field;NE=121,Nk=9,geometry_file=geometry_path)
        builder.hdf_geometry_sha256==saved.identity["source_geometry_model_sha256"] ||
            error("refined radial builder has a different archived geometry identity")
        spec=TOML.parsefile(joinpath(directory,"spec.toml"))
        spec["device_sha256"]==builder.source_device_sha256 ||
            error("refined radial builder has a different physical device")
        coarse=Runner._read_linked_checkpoint(coarse_directory)
        coarse.current_midpoints==cuts || error("energy control uses different physical current cuts")
        lower_resolution=coarsen_energy(saved,previous,coarse)
        energy=compare_grid(coarse.problem,lower_resolution,baseline,cuts,measure,workers)
        println(stderr,"matched E$(coarse.problem.ne) energy control complete")
        flush(stderr)
        refined=expand_rings((;problem=p,seed=previous),old_k,builder)
        radial=compare_grid(refined.linked,refined.mapped_source,baseline,cuts,measure,workers)
        println(stderr,"matched radial $(p.nk)→$(refined.linked.nk) control complete")
        flush(stderr)
        return (;
            definition="both controls branch from the same previous source of the selected unmixed primary image",
            old_k,new_k=refined.new_k,old_energy_count=p.ne,new_energy_count=coarse.problem.ne,
            radial_transfer=[collect(row) for row in eachrow(refined.transfer)],
            geometry_sha256=builder.hdf_geometry_sha256,device_sha256=builder.source_device_sha256,
            coarse_input_identity=coarse.identity,
            builder_source_sha256=bytes2hex(open(sha256,builder_path)),
            radial_source_sha256=bytes2hex(open(sha256,@__FILE__)),
            energy,radial,
        )
    end
    return run_continuation(directory,maps,alpha,measure,workers;selected_control=selected_controls)
end

if abspath(PROGRAM_FILE)==abspath(@__FILE__)
    length(ARGS)==9 ||
        error("Usage: v843_radial.jl ARCHIVE COARSE_ARCHIVE BUILDER GEOMETRY OUTPUT MAPS ALPHA MEASURE WORKERS")
    archive,coarse,builder,geometry,output,maps,alpha,measure,workers=ARGS
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    include(abspath(builder))
    report=run_v843(archive,coarse,V843LinkedInput,builder,geometry,parse(Int,maps),
        parse(Float64,alpha),measure,parse(Int,workers))
    open(output,"w") do io
        Runner._light_json(io,report)
        println(io)
    end
end
