include("profile_experiment.jl")

function linked_metrics(summary, widths)
    adaptive = summary["projected_fresh"]
    profile = adaptive["raw_profile_A_cm2"]
    physical = SpatialBalance.current_metrics(profile,widths)
    rS = summary["weighted_rSigma_channels_RLG"]
    cavities = summary["weighted_rSigma_boundaries_RLG"]
    raw_spectral = adaptive["spectral_weight_relative_by_ring"]
    return (;
        rK=summary["weighted_rK"],
        rSigma=max(maximum(maximum,values(rS)),maximum(maximum,values(cavities))),
        rSigma_by_channel=rS,
        rSigma_boundary=cavities,
        raw_lambda=adaptive["raw_lambda"],
        raw_sheet_cm2=adaptive["raw_sheet_cm2"],
        spectral_defect_by_ring=raw_spectral,
        maximum_spectral_defect=maximum(raw_spectral),
        spatial=physical,
        current_profile_A_cm2=profile,
        fermionic_pair=(a=summary["input_pair_projection"]["a"],
            c=summary["input_pair_projection"]["c"]),
    )
end

function strictly_qualified(row)
    return max(row.rK,row.rSigma,abs(row.raw_lambda-1)) < 1e-8 &&
        row.maximum_spectral_defect < 1e-3 &&
        row.spatial.max_deviation_from_mean_A_cm2 <= row.spatial.target_tolerance_A_cm2
end

function run_continuation(directory,maps,alpha,measure,workers)
    maps >= 1 || throw(ArgumentError("requested map count must be positive"))
    0 < alpha <= 1 || throw(ArgumentError("fresh-source fraction must be in (0,1]"))
    measure in ("projected","normalized-nodal") || throw(ArgumentError("unknown collision measure"))
    data = Runner._read_linked_checkpoint(directory)
    (;problem,seed,current_midpoints) = data
    widths = (current_midpoints[3:end] .- current_midpoints[1:end-2])./2
    history = NamedTuple[]
    confirmations = 0
    fresh_source = nothing
    best_score = Inf
    for iteration in 1:maps
        start = time_ns()
        image = LT.linked_fresh_map(problem, seed;
            projector=LT.project_linked_economical, selected_rows=true,
            projection_for_collision=measure=="projected", workers)
        row = linked_metrics(image.summary,widths)
        confirmations = strictly_qualified(row) ? confirmations+1 : 0
        push!(history,(;iteration,row...,strict_confirmations=confirmations,
            elapsed_s=(time_ns()-start)*1e-9))
        Runner._light_json(stderr, (;iteration,row.rK,row.rSigma,row.raw_lambda,
            row.maximum_spectral_defect,J_A_cm2=row.spatial.mean_internal_A_cm2,
            J_deviation_A_cm2=row.spatial.max_deviation_from_mean_A_cm2,confirmations))
        println(stderr)
        flush(stderr)
        score = max(row.rK,row.rSigma,abs(row.raw_lambda-1),
            row.spatial.max_deviation_from_mean_A_cm2 / max(abs(row.spatial.mean_internal_A_cm2),1.0))
        if score < best_score || confirmations>=3
            best_score = score
            fresh_source = (;iteration,source=image.source)
        end
        confirmations>=3 && break
        # A convex combination of the two L/G pairs keeps both kinetic sources
        # positive and leaves the retarded convention and anchors unchanged.
        seed .= (1-alpha) .* seed .+ alpha .* image.source
    end
    observed = spatial_balance(problem,fresh_source.source,widths;
        workers,energy_rule=independent_energy_rule)
    row = history[fresh_source.iteration]
    quadrature_difference = maximum(abs.(row.current_profile_A_cm2 .- observed.current_A_cm2))
    independent_accepted = quadrature_difference <= observed.current.target_tolerance_A_cm2 &&
        observed.current.max_deviation_from_mean_A_cm2 <= observed.current.target_tolerance_A_cm2
    return (;
        schema="qcl-negf-linked-continuation/v1",
        identity=data.identity,
        core=Runner._linked_package_identity(Runner.QCLNEGF),
        runner=Runner._linked_package_identity(Runner),
        runtime=Runner._runtime_toolchain_provenance(),
        sources=Dict(name=>bytes2hex(open(sha256,joinpath(@__DIR__,name)))
            for name in ("spatial_balance.jl","profile_experiment.jl","continuation.jl")),
        configuration=(;maps,alpha,measure,workers,energy_projection="GL9/13/18 subsplit 2",
            independent="GL20 subsplit 3"),
        current_midpoints_nm=current_midpoints,history,
        selected_iteration=fresh_source.iteration,
        independent_current_difference_A_cm2=quadrature_difference,
        observed,
        stationary=confirmations>=3 && independent_accepted,
    )
end

if abspath(PROGRAM_FILE)==abspath(@__FILE__)
    length(ARGS)==6 ||
        error("Usage: continuation.jl ARCHIVE OUTPUT MAPS ALPHA projected|normalized-nodal WORKERS")
    input,output,maps_arg,alpha_arg,measure,workers_arg=ARGS
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    report=run_continuation(input,parse(Int,maps_arg),parse(Float64,alpha_arg),measure,parse(Int,workers_arg))
    open(output,"w") do io
        Runner._light_json(io,report)
        println(io)
    end
end
