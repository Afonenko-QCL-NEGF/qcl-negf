using QCLNEGF.LinkedTransport: linked_fresh_map, project_linked, project_linked_economical

const _LINKED_USAGE =
    "run-linked INPUT OUTPUT [--projector resonance|distance] [--solve full|selected] " *
    "[--collision-measure projected|normalized-nodal] [--order N] [--subdivisions N] " *
    "[--workers N] [--reference ARCHIVE ...]"

function _linked_options(arguments)
    supported = ("--projector","--solve","--collision-measure","--order","--subdivisions","--workers")
    iseven(length(arguments)) || throw(ArgumentError(_LINKED_USAGE))
    options = Dict{String,String}()
    references = String[]
    for index in 1:2:length(arguments)
        key,value = arguments[index],arguments[index+1]
        if key == "--reference"
            push!(references,value)
        else
            key in supported || throw(ArgumentError("unknown run-linked option $key"))
            haskey(options,key) && throw(ArgumentError("duplicate run-linked option $key"))
            options[key] = value
        end
    end
    projector = get(options,"--projector","resonance")
    solver = get(options,"--solve","full")
    measure = get(options,"--collision-measure","projected")
    projector in ("resonance","distance") || throw(ArgumentError("invalid linked projector $projector"))
    solver in ("full","selected") || throw(ArgumentError("invalid linked solve $solver"))
    measure in ("projected","normalized-nodal") || throw(ArgumentError("invalid linked collision measure $measure"))
    default_order,default_subdivisions = projector == "distance" ? (18,2) : (12,1)
    order = parse(Int,get(options,"--order",string(default_order)))
    subdivisions = parse(Int,get(options,"--subdivisions",string(default_subdivisions)))
    workers = parse(Int,get(options,"--workers",string(Threads.nthreads(:default))))
    order >= 2 && subdivisions >= 1 && workers >= 1 ||
        throw(ArgumentError("linked order must be at least two, with positive subdivisions and worker count"))
    projector == "distance" && order != 18 &&
        throw(ArgumentError("the distance-tiered GL9/13/18 projector uses order 18 near the poles"))
    return (;projector,solver,measure,order,subdivisions,workers,references)
end

function _linked_current_state(checkpoint, projected)
    p = checkpoint.problem
    isnothing(projected.seam_lesser) && error("Linked projection did not retain both lesser seam moments")
    energy_moment = zeros(Float64,p.r^2,p.nk)
    @views for k in 1:p.nk, e in 1:p.ne
        energy_moment[:,k] .+= p.we[e].*projected.occupation[:,1,e,k]
    end
    q = p.v.coordinate_frame
    return (;
        schema="qcl-negf-linked-current-state/v1",
        current_midpoints_nm=checkpoint.current_midpoints,
        coordinate_frame_real=[real.(row) for row in eachrow(q)],
        coordinate_frame_imag=[imag.(row) for row in eachrow(q)],
        packed_lesser_energy_moment_by_ring=collect(eachcol(energy_moment)),
        seam_real_lesser_energy_moment_by_ring=collect(eachcol(projected.seam_lesser)),
        hopping_by_ring=collect(eachcol(p.hops)),
        radial_weights=p.wk,
        spin_degeneracy=p.spin_degeneracy,
        current_scale_A_cm2=p.current_scale,
    )
end

function _execute_linked_run(directory, options)
    start = time_ns()
    former_blas_threads = BLAS.get_num_threads()
    BLAS.set_num_threads(1)
    try
        event = Dict{String,Any}(
            "schema"=>"qcl-negf-linked-run/v1",
            "input"=>Dict{String,Any}("directory"=>abspath(directory)),
            "core"=>_package_source_identity(QCLNEGF),
            "runner"=>_package_source_identity(@__MODULE__),
            "environment"=>_runtime_toolchain_provenance(),
            "mode"=>Dict(
                "projector"=>options.projector,"solve"=>options.solver,"collision_measure"=>options.measure,
                "order"=>options.order,"subdivisions"=>options.subdivisions,"requested_workers"=>options.workers,
            ),
            "archive_comparisons"=>[], "metrics"=>nothing, "state"=>nothing, "error"=>nothing,
        )
        try
            checkpoint = _read_linked_checkpoint(directory)
            merge!(event["input"],checkpoint.identity)
            workers = min(options.workers,Threads.nthreads(:default),checkpoint.problem.nk)
            event["mode"]["workers"] = workers
            projector = options.projector == "distance" ? project_linked_economical : project_linked
            result = linked_fresh_map(checkpoint.problem,checkpoint.seed;
                projector, selected_rows=options.solver=="selected",
                projection_for_collision=options.measure=="projected",
                options.order, options.subdivisions, workers)
            event["metrics"] = result.summary
            event["state"] = _linked_current_state(checkpoint,result.projected)
            # Archive comparisons consume the fresh packed LG directly in memory.
            comparison = [ _linked_compare_archive(path,result,checkpoint.problem,checkpoint.identity)
                for path in options.references ]
            event["archive_comparisons"] = comparison
            passed = all(report["transfer_gate_passed"] for report in comparison)
            event["status"] = passed ? "completed" : "reference_mismatch"
            event["exit_code"] = passed ? 0 : 1
        catch problem
            event["status"] = problem isa InterruptException ? "cancelled" : "failed"
            event["exit_code"] = problem isa InterruptException ? 130 : 1
            event["error"] = sprint(showerror,problem)
        end
        event["elapsed_seconds"] = (time_ns()-start)*1e-9
        event["peak_rss_bytes"] = Int(Sys.maxrss())
        return event
    finally
        BLAS.set_num_threads(former_blas_threads)
    end
end

function _write_linked_event(path, event)
    event["result_size_bytes"] = 0
    payload = ""
    # The size includes the result's own size field and terminal newline.
    while true
        payload = sprint(io->_light_json(io,event)) * "\n"
        ncodeunits(payload) == event["result_size_bytes"] && break
        event["result_size_bytes"] = ncodeunits(payload)
    end
    target = abspath(path)
    mkpath(dirname(target))
    temporary,stream = mktemp(dirname(target))
    try
        write(stream,payload)
        close(stream)
        chmod(temporary,0o640)
        hardlink(temporary,target)
    finally
        isopen(stream) && close(stream)
        rm(temporary;force=true)
    end
    return target
end

function _run_linked_cli(arguments)
    if arguments == ["--help"]
        println(_LINKED_USAGE)
        return 0
    end
    length(arguments) >= 2 || throw(ArgumentError(_LINKED_USAGE))
    input,output = arguments[1:2]
    (ispath(output) || islink(output)) && throw(ArgumentError("linked output already exists: $output"))
    event = _execute_linked_run(input,_linked_options(arguments[3:end]))
    path = _write_linked_event(output,event)
    isnothing(event["error"]) || println(stderr,event["error"])
    println(path)
    return event["exit_code"]
end
