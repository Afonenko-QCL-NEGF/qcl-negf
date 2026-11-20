module Suite_T061
include("../support/common.jl")
include("../support/native_physics_fixture.jl")

@testset "Production convergence diagnostics are complete" begin
    events = SolverEvent[]
    production = ProductionOptions(event_sink = event -> begin
        push!(events, event)
        true
    end)
    fixture = native_physics_fixture(; energy_nodes = 17)
    options = SolverOptions(; max_scba = 1, max_poisson = 1)
    core = QCLNEGFRunner.QCLNEGF
    state = core.solve_scba_production(
        fixture.problem, fixture.Uᴴ; options, production_options = production,
    )
    row = only(state.history)
    event = only(filter(e -> e.action === :progress && e.stage === :scba, events))
    @test event.iteration == row.ν
    metrics = Dict(metric.name => metric.value for metric in event.metrics)
    assessment = core.scba_convergence_assessment(row, options.tolerances, options.convergence)
    @test metrics[:limiting_gate] == String(assessment.limiting_metric)
    @test metrics[:limiting_ratio] == assessment.limiting_ratio
    @test metrics[:failed_gate_count] == length(assessment.failed_metrics)
    @test haskey(metrics, :fixed_point_limiting_gate)
    @test haskey(metrics, :diagnostic_quality)
    @test haskey(metrics, :diagnostic_quality_streak)
    @test metrics[:psd_energy_index] == row.witness.energy_index
    @test metrics[:psd_momentum_index] == row.witness.momentum_index
    @test metrics[:psd_block_norm_scaled] == row.witness.block_norm
    for name in (
        :r_D, :r_A, :r_K, :r_Σ, :r_λ, :r_PSD, :r_caus, :r_roundoff,
        :r_Jchange, :r_population,
    )
        @test isequal(metrics[name], getfield(row, name))
    end
end

end # independent suite
