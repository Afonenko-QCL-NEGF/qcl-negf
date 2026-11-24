# This entry point receives the F13 map-48 input from replay.jl in the same process.
function run_refinement(p, seed, cuts, workers, replay)
    work = dirname(output)
    attempt = 1
    while true
        path = joinpath(work, attempt==1 ? "trajectory.jsonl" : "trajectory-$(attempt).jsonl")
        ispath(path) && error("trajectory output already exists: $path")
        try
            experiment = include(joinpath(@__DIR__,"k31_rank.jl"))
            execute = Base.invokelatest(getproperty,experiment,:run_k31_rank)
            Base.invokelatest(execute,
                p,seed,cuts,workers,replay,path)
            return
        catch err
            err isa InterruptException && rethrow()
            open(joinpath(work,"campaign.errors"),"a") do io
                showerror(io,err,catch_backtrace())
                println(io)
            end
            announce((;phase="continuation_failed",attempt,error=sprint(showerror,err)))
        end
        # Preserve F13 in RAM during repairs. Each retry starts its own evidence file.
        retry = joinpath(work,"retry-$(attempt+1)")
        while !isfile(retry)
            sleep(5)
        end
        rm(retry)
        attempt += 1
        GC.gc()
    end
end
