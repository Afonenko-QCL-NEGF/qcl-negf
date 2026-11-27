module ProductionObservationAndOuterRestart
include("../support/common.jl")
include("../support/native_physics_fixture.jl")

const Runner = QCLNEGFRunner

@testset "Compact observation and exact outer-boundary continuation" begin
    fixture = native_physics_fixture(; energy_nodes = 65)
    options = SolverOptions(
        max_scba = 4,
        max_poisson = 2,
        convergence = ConvergencePolicy(
            mode = :research_continue,
            required_consecutive_scba_passes = 99,
            # This storage fixture exercises two bounded outer steps.
            trend = ResearchTrendPolicy(window = 2, promising_threshold = 1e6),
        ),
    )
    production_options = ProductionOptions(
        worker_count = 1,
        progress_every_scba = 0,
        progress_every_outer = 0,
        checkpoint_request = context -> context.stage === :outer ? :state_and_analysis : :none,
    )
    solve_point(; kwargs...) = solve_production(fixture.problem; options, production_options, kwargs...)
    reference = solve_point()
    @test length(reference.outer_history) == options.max_poisson
    @test length(reference.scba.history) == options.max_scba
    @test isfinite(last(reference.scba.history).raw_charge)
    raw_scba(result) = [
        (row.ν, row.r_D, row.r_K, row.r_Σ, row.r_λ, row.raw_charge)
        for row in result.scba.history
    ]
    raw_outer(result) = [
        (row.μ, row.r_P, row.r_U, row.r_n, row.r_neutral, row.r_J, row.density)
        for row in result.outer_history
    ]
    function check_same(result)
        @test result.status === reference.status
        @test result.converged == reference.converged
        @test result.Uᴴ == reference.Uᴴ
        @test result.n == reference.n
        @test result.scba.green.Gˡ == reference.scba.green.Gˡ
        @test result.observables[:bond_current] == reference.observables[:bond_current]
        @test isequal(raw_scba(result), raw_scba(reference))
        @test isequal(raw_outer(result), raw_outer(reference))
        candidate = Runner.QCLNEGF.fresh_scba_map(result.problem, result.Uᴴ, result.scba; production_options)
        expected = Runner.QCLNEGF.fresh_scba_map(
            reference.problem, reference.Uᴴ, reference.scba; production_options,
        )
        @test candidate.embedding.Σˡ == expected.embedding.Σˡ
        @test candidate.embedding.Σᴿ == expected.embedding.Σᴿ
    end
    mktempdir() do directory
        seen = Symbol[]
        snapshots = Int[]
        function observer(measurement)
            @test measurement isa Runner.QCLNEGF.ProductionObservation
            push!(seen, measurement.stage)
            fill!(measurement.z_nm, NaN)
            fill!(measurement.hartree_eV, NaN)
            fill!(measurement.density_per_m3, NaN)
        end
        function history(kind, outer, row, grid)
            @test grid isa Runner.QCLNEGF.SolverHistoryGrid
            fill!(grid.energy_eV, NaN)
            if kind === :outer
                fill!(row.density, NaN)
                fill!(row.populations, NaN)
            elseif row.witness !== nothing
                empty!(row.witness.matrices)
            end
        end
        function snapshot(state, analysis)
            state.status === :running || return
            @test analysis
            outer = length(state.outer_history)
            push!(snapshots, outer)
            file = joinpath(directory, "outer-$outer.h5")
            save_checkpoint(file, state; include_kernels = false)
        end
        result = solve_point(; observation_sink = observer, history_observer = history, checkpoint_sink = snapshot)
        @test seen == [:outer, :outer, :terminal]
        @test snapshots == [1, 2]
        check_same(result)
        for outer in 1:options.max_poisson
            file = joinpath(directory, "outer-$outer.h5")
            recovered = load_production_restart(
                file, fixture.problem; algorithms = production_options.algorithms, solver_options = options,
            )
            @test recovered.resume_outer && !recovered.resume_scba
            @test length(recovered.outer_history) == outer
            @test recovered.poisson_streak == 0
            check_same(solve_point(;
                initial_Uᴴ = recovered.Uᴴ,
                initial_scba = recovered.scba,
                initial_outer_history = recovered.outer_history,
                initial_warnings = recovered.warnings,
                resume_outer = recovered.resume_outer,
                initial_poisson_streak = recovered.poisson_streak,
                consume_initial = true,
            ))
        end
        terminal_path = joinpath(directory, "returned.h5")
        save_checkpoint(terminal_path, reference; include_kernels = false)
        returned = load_production_restart(terminal_path, fixture.problem)
        @test returned.completed && !returned.resume_outer && !returned.resume_scba
        reused = Runner._completed_restart_solution(fixture.problem, options, returned)
        @test reused.scba.status == reference.scba.status
        @test reused.scba.quality == reference.scba.quality
        @test reused.report.messages == reference.report.messages
        @test reused.report.passed == reference.report.passed
        @test isequal(reused.report.metrics, reference.report.metrics)
        @test isequal(reused.observables[:charge_constraint], reference.observables[:charge_constraint])
        check_same(reused)
    end
end
end
