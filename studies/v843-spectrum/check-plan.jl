using QCLNEGFRunner
using Test

@testset "V843 B7 authors freeze the same declared problem" begin
    path = joinpath(@__DIR__, "b7.yaml")
    yaml_plan = resolve_scientific_plan(path)
    config_sources = ["../../runner/examples/config/reference-2019-70k.yaml"]
    execution = only(yaml_plan.executions)
    # Construct the author document in Julia. Geometry comes from the same
    # published V843 input, supplied here as the resolved physical map.
    definition = Dict(
        "schema" => "qcl-negf-study-v2",
        "id" => "dupont-v843-b7",
        "name" => "Julia-authored V843 static spectrum",
        "purpose" => "diagnostic",
        "operation" => "structure_spectrum",
        "configuration" => Dict(
            "sources" => config_sources,
            "overrides" => Dict(
                "physical" => execution.configuration.raw["physical"],
                "numerical" => execution.configuration.raw["numerical"],
            ),
        ),
        "axes" => Dict(
            "temperatures" => Dict("values" => [50], "unit" => "K"),
            "voltages" => Dict("values" => [75.936], "unit" => "mV"),
        ),
        "outputs" => Dict("projections" => false, "intermediate_history" => 1),
    )
    julia_plan = resolve_scientific_plan(definition; base_directory = @__DIR__)
    yaml_frozen = scientific_plan_dict(yaml_plan)
    julia_frozen = scientific_plan_dict(julia_plan)
    @test julia_frozen["scientific_fingerprint"] == yaml_frozen["scientific_fingerprint"]
    passport = only(yaml_frozen["points"])["effective_inputs"]
    @test passport["field_V_per_m"] ≈ 2.1e6
    @test passport["period_length_m"] ≈ 36.16e-9
    @test only(yaml_plan.points).voltage_per_period_V ≈ 0.075936
    @test execution.operation === :structure_spectrum
    @test execution.configuration.numerical.N_b == 7
    @test execution.configuration.numerical.P_basis == 3
end
