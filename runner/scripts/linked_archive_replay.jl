#!/usr/bin/env julia
# Compatibility entry point for the two archived replay recipes.
using QCLNEGFRunner
using TOML

length(ARGS) >= 2 ||
    error("usage: linked_archive_replay.jl {fath-x9|v3} INPUT_CHECKPOINT [REFERENCE_RUN ...]")
options = if ARGS[1] == "fath-x9"
    ["--projector","distance","--solve","selected","--collision-measure","normalized-nodal"]
elseif ARGS[1] == "v3"
    String[]
else
    throw(ArgumentError("Unknown linked replay recipe $(ARGS[1])"))
end
append!(options,Iterators.flatten(("--reference",path) for path in ARGS[3:end]))
event = QCLNEGFRunner._execute_linked_run(ARGS[2],QCLNEGFRunner._linked_options(options))
if event["state"] === nothing
    TOML.print(stdout,Dict("exit_code"=>event["exit_code"],"error"=>event["error"]);sorted=true)
else
    summary = merge(event["metrics"],event["input"],Dict(
        "projection_recipe"=>ARGS[1],
        "threads"=>event["environment"]["julia_threads"],
        "BLAS_threads"=>event["environment"]["blas_threads"],
        "peak_rss_bytes"=>event["peak_rss_bytes"],
        "archive_comparisons"=>event["archive_comparisons"]))
    TOML.print(stdout,summary;sorted=true)
end
exit(event["exit_code"])
