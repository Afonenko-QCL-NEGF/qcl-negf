include("continuation.jl")

function projected_holdout(archive, workers)
    data = Runner._read_linked_checkpoint(archive)
    p, cuts = data.problem, data.current_midpoints
    widths = (cuts[3:end] .- cuts[1:end-2])./2
    fresh = LT.linked_fresh_map(p,data.seed; projector=LT.project_linked_economical,
        selected_rows=true,projection_for_collision=true,workers)
    println(stderr,"projected fresh holdout map complete")
    flush(stderr)
    observation=spatial_balance(p,fresh.source,widths;workers,
        energy_rule=independent_energy_rule,current_cuts=cuts)
    projected=linked_metrics(fresh.summary,widths)
    difference=maximum(abs.(observation.current_A_cm2.-projected.current_profile_A_cm2))
    return (;
        schema="qcl-negf-linked-projected-holdout/v1",identity=data.identity,
        current_midpoints_nm=cuts,
        core=Runner._linked_package_identity(Runner.QCLNEGF),
        runner=Runner._linked_package_identity(Runner),
        runtime=Runner._runtime_toolchain_provenance(),
        sources=Dict(name=>bytes2hex(open(sha256,joinpath(@__DIR__,name)))
            for name in ("spatial_balance.jl","profile_experiment.jl","continuation.jl","projected_holdout.jl")),
        production=projected,observation,
        independent_current_difference_A_cm2=difference,stationary=false,
    )
end

if abspath(PROGRAM_FILE)==abspath(@__FILE__)
    length(ARGS)==3 || error("Usage: projected_holdout.jl ARCHIVE OUTPUT WORKERS")
    archive,output,workers=ARGS
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    report=projected_holdout(archive,parse(Int,workers))
    open(output,"w") do io
        Runner._light_json(io,report)
        println(io)
    end
end
