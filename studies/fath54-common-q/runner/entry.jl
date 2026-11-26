function run_refinement(p, seed, cuts, workers, replay)
    work = dirname(output)
    campaign = nothing
    scheme = nothing
    successful_trajectory = nothing
    for attempt in Iterators.countfrom(1)
        path = joinpath(work, attempt == 1 ? "trajectory.jsonl" : "trajectory-$(attempt).jsonl")
        ispath(path) && error("trajectory output already exists: $path")
        try
            campaign = include(joinpath(@__DIR__, "rank_scan.jl"))
            execute = Base.invokelatest(getproperty, campaign, :run)
            scheme = Base.invokelatest(execute, p, seed, cuts, workers, replay, path)
            successful_trajectory = path
            break
        catch err
            err isa InterruptException && rethrow()
            open(joinpath(work, "runner.errors"), "a") do io
                showerror(io, err, catch_backtrace())
                println(io)
            end
            announce((;phase="continuation_failed", attempt, error=sprint(showerror,err)))
        end
        retry = joinpath(work, "retry-$(attempt+1)")
        while !isfile(retry)
            sleep(5)
        end
        rm(retry)
        GC.gc()
    end
    GC.gc()
    source = joinpath(@__DIR__,"bosco.jl")
    bosco_out = joinpath(work,"bosco")
    for attempt in Iterators.countfrom(1)
        try
            Base.include(campaign,source)
            solve = Base.invokelatest(getproperty,campaign,:run_bosco)
            Base.invokelatest(solve,work,scheme)
            break
        catch err
            err isa InterruptException && rethrow()
            open(joinpath(work,"bosco.errors"),"a") do io
                showerror(io,err,catch_backtrace())
                println(io)
            end
            announce((;phase="bosco_attempt_failed",attempt,error=sprint(showerror,err)))
        end
        retry = joinpath(work,"bosco-retry-$(attempt+1)")
        while !isfile(retry)
            sleep(5)
        end
        rm(retry)
        if isdir(bosco_out)
            mv(bosco_out,joinpath(work,"bosco-attempt-$attempt"))
        end
        GC.gc()
    end
    announce((;phase="all_numerical_maps_complete",work))
    collector = joinpath(@__DIR__,"collect_results.py")
    Base.run(`python3 $collector $successful_trajectory`)
    announce((;phase="compact_evidence_ready",evidence=joinpath(work,"evidence")))
end
