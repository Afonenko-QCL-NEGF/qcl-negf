length(ARGS) == 7 ||
    error("Usage: night.jl APP ARCHIVE BDD base|expanded WORKERS MAPS OUTPUT")
app, archive, geometry, rank_mode, workers_arg, maps_arg, output = ARGS
include(joinpath(app,"studies/fath-lo-rank-v843/fath_factorial.jl"))

function night_map(p, seed, workers)
    return LT.linked_fresh_map(p, seed; projector=LT.project_linked_economical,
        selected_rows=true, projection_for_collision=true, workers)
end

function record(io, kind, payload)
    Runner._light_json(io, (;kind, payload...))
    println(io)
    flush(io)
end

function conditions(input, archive, geometry, rank_mode)
    p = input.problem
    p.geo.voltage ≈ 0.54 && input.identity["temperature_K"] == 10.0 ||
        error("expected Fath at 54 mV and 10 K")
    spec = TOML.parsefile(joinpath(archive, "spec.toml"))
    sites = Runner._read_linked_array(archive, "ifr_sites", Float64, spec["n_interfaces"], p.nz)
    pair = (; plus=p.v.lo_plus, minus=p.v.lo_minus)
    if rank_mode == "base"
        kernel = lo_kernel(p.v, sites, pair.plus, pair.minus)
        return rebuild(p, kernel), input.seed, (;p.nb, p.r)
    end
    rank_mode == "expanded" || error("unknown rank")
    coordinates = coordinate_data(geometry, input.identity["source_geometry_model_sha256"], p)
    radial = Runner._read_linked_array(archive, "k", Float64, p.nk)
    expanded = expand_modes(p, coordinates, radial)
    embedding = expanded.q' * p.v.coordinate_frame
    lifted = lift_source(input.seed, embedding)
    kernel = lo_kernel(p.v, sites, pair.plus, pair.minus; q=expanded.q)
    anchors = cat([embedding * p.const_by_channel[:,:,k,c] * embedding'
        for k in 1:p.nk, c in eachindex(LT.COLLISION_CHANNELS)]...; dims=3)
    anchors = reshape(anchors, size(expanded.q,2), size(expanded.q,2), p.nk, :)
    problem = rebuild(p, kernel; modes=expanded.modes, nb=expanded.nb, h=expanded.h, anchor=anchors)
    common_error = maximum(norm(embedding' * b[:,expanded.common] - old) / norm(old)
        for (b,old) in zip(problem.geo.bases,p.geo.bases))
    common_error < 2e-13 || error("expanded bases failed common-component check")
    return problem, lifted.source, (;problem.nb, problem.r, expanded.metric_error,
        expanded.h_error, common_error, lifted.roundtrip_maximum)
end

function observe_at(io, p, seed, image, cuts, workers, step, arm, balance_file)
    isfile(balance_file) || return
    if !isdefined(Main, :observe_balance)
        Base.include(Main, balance_file)
    end
    result = Base.invokelatest(observe_balance, p, seed, image, cuts, workers)
    record(io, "balance", (;step, arm, result))
end

function radial_at(io, p, seed, image, cuts, workers, step, output)
    script = get(ENV, "FATH_RADIAL_SCRIPT", "")
    isfile(script) || return
    Base.include(Main, script)
    result = Base.invokelatest(FathRadialControl.radial_control, p, seed, image, cuts, workers;
        coarse_archive=archive, fine_archive=ENV["FATH_FINE_ARCHIVE"],
        output=output * ".radial.json", coarse_iteration=step)
    record(io, "radial", (;step, file=basename(output) * ".radial.json"))
    if isdefined(FathRadialControl, :continue_fine)
        Base.invokelatest(FathRadialControl.continue_fine, result, cuts, workers;
            maps=parse(Int,get(ENV,"FATH_FINE_MAPS","8")), output=output * ".fine.jsonl")
    end
end

function control(output, directive)
    path = output * "." * directive
    return isfile(path)
end

function main()
    BLAS.set_num_threads(1)
    workers, maps = parse(Int,workers_arg), parse(Int,maps_arg)
    balance_file = get(ENV, "FATH_BALANCE_SCRIPT", "")
    ispath(output) && error("output already exists: " * output)
    cuts, identity, p, seed, rank = let data = Runner._read_linked_checkpoint(archive)
        problem, initial, rank_data = conditions(data, archive, geometry, rank_mode)
        data.current_midpoints, data.identity, problem, initial, rank_data
    end
    GC.gc()
    widths = (cuts[3:end] .- cuts[1:end-2]) ./ 2
    observe_steps = parse.(Int, split(get(ENV, "FATH_BALANCE_STEPS", "48,72,96"),','))
    radial_step = parse(Int, get(ENV, "FATH_RADIAL_STEP", "0"))
    confirmations = 0
    arm = "picard035"
    alpha = 0.35
    open(output, "w") do io
        record(io, "configuration", (;identity, rank, workers, rank_mode, cuts,
            app_revision=readchomp(`git -C $app rev-parse HEAD`),
            core=Runner._linked_package_identity(Runner.QCLNEGF),
            runner=Runner._linked_package_identity(Runner),
            runtime=Runner._runtime_toolchain_provenance(),
            driver_sha256=bytes2hex(open(sha256,@__FILE__))))
        for step in 1:maps
            start = time_ns()
            image = night_map(p, seed, workers)
            row = linked_metrics(image.summary, widths)
            confirmations = strictly_qualified(row) ? confirmations + 1 : 0
            elapsed_s = (time_ns()-start)*1e-9
            record(io, "map", (;step, arm, row..., confirmations, elapsed_s,
                channel_balance=image.summary["fresh_channel_balance"]))
            println(stderr, "map $step ($arm): rK=$(row.rK), rSigma=$(row.rSigma), raw_lambda=$(row.raw_lambda), J deviation=$(row.spatial.max_deviation_from_mean_A_cm2)")
            flush(stderr)
            if step in observe_steps || step == maps || confirmations >= 3 || control(output, "stop")
                observe_at(io, p, seed, image, cuts, workers, step, arm, balance_file)
            end
            if rank_mode == "base" && step == radial_step
                radial_at(io, p, seed, image, cuts, workers, step, output)
            end
            (confirmations >= 3 || control(output, "stop")) && break
            if arm == "picard035" && control(output, "compare")
                # Both methods branch from exactly this input. The first map is shared.
                comparison_seed = copy(seed)
                comparison_seed .= 0.65 .* comparison_seed .+ 0.35 .* image.source
                seed .= image.source
                image = nothing
                alpha = 1.0
                arm = "picard100"
                for comparison_step in 1:8
                    trial = night_map(p, comparison_seed, workers)
                    metrics = linked_metrics(trial.summary, widths)
                    record(io, "comparison", (;step=step+comparison_step,
                        arm="picard035", branch_step=step, metrics...))
                    comparison_seed .= 0.65 .* comparison_seed .+ 0.35 .* trial.source
                    control(output, "stop") && break
                end
            else
                seed .= (1-alpha) .* seed .+ alpha .* image.source
            end
        end
    end
end

main()
