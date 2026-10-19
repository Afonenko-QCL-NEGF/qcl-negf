# RV04 blind source notes

Before candidate/fixes read; S=e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1, Core C=3108150dd1b6b1377470b384b15c26e272fe5c5d, Runner J=0c53c6d0f68e0b25fce79388db831da6fc3ae856. N=6 from card; source-only, no imports/tests.

1. J `configured_execution.jl::planned_solver_runs/_check_solver_run_budget/execute_configured_run` owns study dispatch and precreation invocation budget. Output retargeting deepcopies raw/provenance, preserves scientific parameters.
2. J `QCLNEGFRunner.jl` imports Core, owns HDF5/YAML/Downloads; `core_api.jl` imports many Core public/private numerical bindings. Broad impact surface is a coupling observation, LOC alone no defect. C top includes domain/reference/optimized/physics, not Runner persistence.
3. J `production_solver_adapter.jl::solve_production` wraps Core solve with optional file checkpoint sink. Core owns solve state, Runner owns `_atomic_checkpoint`; dynamic callback edge must be shown, not presumed effect-free.
4. J coordinator `PointExecutionContext/save_checkpoint!` adapts repository/codec; `execute_point!(AbstractPointRunner)` dispatches to composition `QCLProductionPointRunner`. Numerical callbacks and payload filesystem writes remain Runner effects.
5. J `coordinator.jl::run_sweep!` initialize/provenance/status→point runner→write result→verify artifacts/digest→terminal status ordering makes persistence explicit.
6. `run_sweep!` catch classifies interruption vs failure, loads verified latest checkpoint, writes status, rethrows interruption/fail_fast. Recovery owner is Runner; not a Core scientific continuation proof.

Negative: putting persistence in Core would invert this dependency and hide file effects; common numerical helper shared with oracle can create correlated error, not measured here. M12 selected dependency map only; exact SCC/whole-repo forbidden-edge count and M13 numeric CFG unmeasured. Targeted test source catalogue from test filenames identifies runtime repository/checkpoint/sweep coverage but no execution; candidate must avoid stronger count/coverage claims. No independently established blocking implementation defect in this bounded trace.
