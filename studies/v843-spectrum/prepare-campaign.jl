using QCLNEGFRunner
using TOML
using YAML

length(ARGS) == 1 || error("Usage: prepare-campaign.jl FROZEN_PLAN")
rule = TOML.parsefile(joinpath(@__DIR__, "admission.toml"))
study = YAML.load_file(joinpath(@__DIR__, "b7.yaml"); dicttype = Dict{String,Any})
study["id"] = "dupont-v843-basis-admission"
study["name"] = "V843 finite-window basis candidates"

function basis_variant(window, rank)
    overrides = Dict{String,Any}()
    controlled_paths = String[]
    baseline = rule["baseline"]
    for (name, value, original) in (
        ("basis_periods", (window - 1) ÷ 2, (baseline["window"] - 1) ÷ 2),
        ("basis_states", rank, baseline["rank"]),
    )
        value == original && continue
        overrides[name] = value
        push!(controlled_paths, "numerical.$name")
    end
    return Dict(
        "id" => "b$(window)-r$(rank)",
        "method_id" => "configured",
        "overrides" => Dict("numerical" => overrides),
        "controlled_paths" => controlled_paths,
        "comparison_kind" => "representation",
    )
end

study["variants"] = [basis_variant(window, rank) for window in rule["windows"]
                     for rank in rule["ranks"]]
plan = resolve_scientific_plan(study; base_directory = @__DIR__,
    maximum_solver_runs = length(study["variants"]))
length(plan.executions) == length(plan.points) == length(study["variants"]) ||
    error("each registered candidate must resolve to one independent point")
!ispath(ARGS[1]) || error("frozen plan already exists")
open(ARGS[1], "w") do io
    write_scientific_plan(io, plan)
end
