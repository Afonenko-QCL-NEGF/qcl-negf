module V843Transport

using LinearAlgebra
using QCLNEGF
using QCLNEGFRunner
using SHA: sha256
using TOML
using Unitful

include(joinpath(@__DIR__, "..", "fath-v843", "controls", "v843-input", "dupont", "dupont_device.jl"))

const CASES = Dict(
    "PILOT"=>(17,32,1),
    "T17A32"=>(17,32,128), "T17A128"=>(17,128,128),
    "T33A32"=>(33,32,128), "T33A128"=>(33,128,128),
)
const MAP_REAL_FIELDS = (:J, :raw_charge, :r_K, :r_Σ, :r_λ)
const USABLE_STATUSES = (:converged, :max_iterations, :stagnated, :approximate, :research_continue)

digest(path) = bytes2hex(open(sha256,path))

function iteration_record(row)
    result = Dict{String,Any}()
    unavailable = String[]
    for field in fieldnames(typeof(row))
        value = getfield(row,field)
        value isa Real || continue
        if isfinite(value)
            result[string(field)] = value
        else
            push!(unavailable,string(field))
        end
    end
    haskey(result,"J") && (result["J_A_cm2"] = result["J"]/1e4)
    isempty(unavailable) || (result["nonfinite_or_unavailable_scalar_fields"] = unavailable)
    return result
end

function validation_rejection(err, frames)
    err isa ErrorException || return false
    # In the pinned publication, this is the error returned by
    # DupontDevice.prepare when Core's full validate_problem report fails.
    return any(frame -> (frame.func === :prepare || startswith(String(frame.func),"#prepare#")) &&
                       endswith(String(frame.file), "dupont_device.jl") &&
                       frame.line == 149, frames)
end

function usable_terminal_map(static_passed, native_status, quality, history)
    return static_passed && native_status in USABLE_STATUSES && quality !== :invalid &&
        !isempty(history) && all(key -> isfinite(getfield(last(history),key)), MAP_REAL_FIELDS)
end

function check_selected_geometry(record)
    record["schema"] == "v843-basis-selection-v1" &&
        record["field_kV_cm"] == 21 && record["spatial_nodes"] == 144 ||
        error("SELECT input has an incompatible scientific identity")
    rank, p_basis = record["rank"], record["p_basis"]
    rank in (6,7,8,9,11) && p_basis in 3:5 &&
        record["window_periods"] == 2p_basis+1 ||
        error("SELECT input contains an inadmissible geometry")
    return (; rank, p_basis)
end

function check_pilot_identity(pilot, selected, select_hash)
    pilot["schema"] == "v843-basis-operator-transport-v1" &&
        pilot["task"] == "PILOT" && pilot["select_sha256"] == select_hash ||
        error("PILOT receipt came from a different SELECT revision")
    if pilot["status"] == "admitted"
        geometry = pilot["built_geometry"]
        manifest = joinpath(dirname(Base.active_project()),"Manifest.toml")
        pilot["driver_sha256"] == digest(@__FILE__) &&
            pilot["device_sha256"] == digest(DupontDevice.DEFAULT_DEVICE) &&
            pilot["manifest_sha256"] == digest(manifest) &&
            geometry["rank"] == selected.rank && geometry["p_basis"] == selected.p_basis &&
            geometry["spatial_nodes"] == 144 && geometry["window_periods"] == 2selected.p_basis+1 &&
            pilot["field_kV_cm"] == 21 && pilot["radial_nodes"] == 17 &&
            pilot["angular_nodes"] == 32 && pilot["completed_iterations"] == 1 &&
            pilot["static_validation_passed"] && pilot["pilot_gate_passed"] && pilot["qualified"] ||
            error("PILOT receipt does not describe the selected one-map science input")
    end
    return nothing
end

function record_drive_settings(task, selected, k, angles, iterations, budget, select_hash)
    manifest = joinpath(dirname(Base.active_project()),"Manifest.toml")
    device = TOML.parsefile(DupontDevice.DEFAULT_DEVICE)
    return Dict{String,Any}(
        "schema"=>"v843-basis-operator-transport-v1", "task"=>task,
        "field_kV_cm"=>21.0, "temperature_K"=>device["lattice_temperature_K"],
        "voltage_mV_per_period"=>0.1*21*device["period_nm"], "hartree"=>"fixed U_H=0",
        "energy_min_meV"=>-650.0, "energy_max_meV"=>1000.0, "energy_nodes"=>239,
        "energy_trust_margin_meV"=>390.0, "radial_nodes"=>k, "angular_nodes"=>angles,
        "k_max_nm_inverse"=>0.6, "qz_nodes"=>161, "qz_max_nm_inverse"=>10.0,
        "requested_geometry"=>Dict("rank"=>selected.rank,"spatial_nodes"=>144,
            "p_basis"=>selected.p_basis,"window_periods"=>2selected.p_basis+1,"localization"=>"pzp"),
        "basis_states"=>selected.rank, "basis_periods"=>selected.p_basis, "basis"=>"pzp",
        "spatial_nodes"=>144, "max_scba"=>iterations, "alpha_sigma"=>0.2,
        "seed_eta_meV"=>0.5, "embedding_periods"=>4,
        "method"=>"native production SCBA; finite-chain embedding; linear mixing; direct elastic retarded; paired convex occupation; product integration; nodal-linear energy shifts",
        "channels"=>["LO","acoustic","impurity","IFR","alloy"], "light"=>"dark",
        "electron_electron_collisions"=>"none", "screening"=>"density_temperature",
        "ifr_correlation"=>"exponential", "cold_start"=>true,
        "memory_budget_GiB"=>budget, "workers"=>Threads.nthreads(:default), "blas_threads"=>BLAS.get_num_threads(),
        "julia_version"=>string(VERSION), "driver_sha256"=>digest(@__FILE__),
        "device_sha256"=>digest(DupontDevice.DEFAULT_DEVICE), "manifest_sha256"=>digest(manifest),
        "core"=>QCLNEGFRunner._linked_package_identity(QCLNEGF),
        "runner"=>QCLNEGFRunner._linked_package_identity(QCLNEGFRunner),
        "select_sha256"=>select_hash, "completed_iterations"=>0, "scba_converged"=>false,
        "charge_unit"=>"Core dimensionless sheet charge before current-iteration normalization",
    )
end

function built_geometry(problem)
    numerical = problem.numerical
    n_cells, rank = size(problem.basis.Φ)
    window_modes = length(problem.basis.window_eigenvalues)
    window_periods, remaining_modes = divrem(window_modes,rank)
    iszero(remaining_modes) && isodd(window_periods) &&
        length(problem.basis.centres) == rank || error("Inconsistent constructed PzP basis")
    return Dict(
        "rank"=>rank, "numerical_rank"=>numerical.N_b, "spatial_nodes"=>n_cells,
        "p_basis"=>(window_periods-1)÷2, "numerical_p_basis"=>numerical.P_basis,
        "window_periods"=>window_periods, "computed_window_eigenvalue_count"=>window_modes,
        "localization"=>string(problem.basis.localization),
    )
end

function run_transport(task::String, args::Vector{String})
    case = get(CASES, task, nothing)
    case !== nothing && isempty(args) || error("Unknown transport task or extra arguments")
    k, angles, maps = case
    parent = ENV["QCL_PARENT_RESULTS"]
    select_path = joinpath(parent,"SELECT.toml")
    selection = TOML.parsefile(select_path)
    select_hash = digest(select_path)
    if selection["status"] == "rejected"
        selection["qualified"] === false || error("Conflicting SELECT result")
        return Dict("schema"=>"v843-basis-operator-transport-v1", "task"=>task,
                    "status"=>"skipped", "qualified"=>false, "reason"=>"SELECT rejected the basis",
                    "select_sha256"=>select_hash, "radial_nodes"=>k, "angular_nodes"=>angles)
    end
    selection["status"] == "admitted" && selection["qualified"] === true ||
        error("Unexpected or incomplete SELECT status")
    selected = check_selected_geometry(selection)
    pilot_hash = nothing
    if task != "PILOT"
        pilot_path = joinpath(parent,"PILOT.toml")
        pilot = TOML.parsefile(pilot_path)
        pilot_hash = digest(pilot_path)
        check_pilot_identity(pilot,selected,select_hash)
        if pilot["status"] in ("rejected","skipped")
            pilot["qualified"] === false || error("Conflicting PILOT result")
            return Dict("schema"=>"v843-basis-operator-transport-v1", "task"=>task,
                        "status"=>"skipped", "reason"=>"PILOT did not admit four transport trajectories",
                        "select_sha256"=>select_hash, "pilot_sha256"=>pilot_hash,
                        "radial_nodes"=>k, "angular_nodes"=>angles)
        end
        pilot["status"] == "admitted" || error("Unexpected or incomplete PILOT status")
    end

    budget = parse(Float64,ENV["QCL_BUDGET_GIB"])
    isfinite(budget) && budget > 0 || error("A finite positive Condor memory budget is required")
    workers = Threads.nthreads(:default)
    BLAS.set_num_threads(1)
    report = record_drive_settings(task,selected,k,angles,maps,budget,select_hash)
    pilot_hash === nothing || (report["pilot_sha256"] = pilot_hash)

    # These are the frozen native diagnostic settings, with only rank and
    # P_basis selected by the static and literature gate.
    algorithms = AlgorithmOptions(kernel_build=:direct,embedding=:finite_chain,embedding_periods=4,
        mixing=:linear,energy_shift=:sparse_plan,hilbert=:product_integration,
        elastic_retarded=:direct_green,occupation_normalization=:paired_convex)
    production = ProductionOptions(algorithms=algorithms,worker_count=workers,
        parallel_backend=:threads,memory_budget_bytes=round(Int,budget*1024^3),
        checkpoint_every_scba=0,checkpoint_every_outer=0)
    numerical = NumericalParameters(N_z=144,N_b=selected.rank,P_basis=selected.p_basis,
        E_min=-650u"meV",E_max=1000u"meV",N_E=239,M_E=390u"meV",k_max=0.6u"nm^-1",
        N_k=k,N_φ=angles,qz_max=10u"nm^-1",N_qz=161,η_seed=0.5u"meV")
    solver = SolverOptions(α_Σ=0.2,max_scba=maps,max_poisson=1,
        convergence=ConvergencePolicy(stagnation_window=0,stagnation_relative_improvement=0.0,
            minimum_scba_iterations=2,required_consecutive_scba_passes=3))
    prepared = try
        DupontDevice.prepare(21.0,numerical,production)
    catch err
        validation_rejection(err, stacktrace(catch_backtrace())) || rethrow()
        report["status"] = "rejected"
        report["reason"] = "full Core validate_problem rejected the prepared model"
        report["static_validation_passed"] = false
        report["validation_messages"] = String.(split(sprint(showerror,err), '\n'))
        if task == "PILOT"
            report["pilot_gate_passed"] = false
            report["qualified"] = false
        end
        return report
    end
    problem = prepared.problem
    geometry = built_geometry(problem)
    requested = report["requested_geometry"]
    all(geometry[key] == expected for (key,expected) in requested) &&
        geometry["rank"] == geometry["numerical_rank"] &&
        geometry["p_basis"] == geometry["numerical_p_basis"] ||
        error("Constructed basis did not match selected geometry")
    report["built_geometry"] = geometry
    report["static_validation_passed"] = prepared.static.passed
    report["static_validation_metrics"] = Dict(string(key)=>value for (key,value) in prepared.static.metrics)
    report["validation_messages"] = prepared.static.messages
    report["memory_estimate_peak_bytes"] = prepared.estimate.peak_bytes

    rows = Dict{String,Any}[]
    result = solve_scba_production(problem,zeros(numerical.N_z);options=solver,production_options=production,
        history_observer=row -> push!(rows,iteration_record(row)))
    length(rows) == length(result.history) || error("SCBA observer missed terminal rows")
    report["native_status"] = string(result.status)
    report["quality"] = string(result.quality)
    report["completed_iterations"] = length(rows)
    report["iterations"] = rows
    report["scba_converged"] = result.converged
    report["stationarity"] = "not established by native SCBA convergence alone"
    if !isempty(rows)
        report["last_iteration"] = last(rows)
    end
    usable = usable_terminal_map(prepared.static.passed,result.status,result.quality,result.history)
    if task == "PILOT"
        passed = usable && length(rows) == 1 && last(rows)["ν"] == 1
        report["pilot_gate_passed"] = passed
        report["qualified"] = passed
        report["status"] = passed ? "admitted" : "rejected"
        report["reason"] = passed ? "one complete finite nonfatal SCBA map" :
            "pilot did not produce exactly one complete finite nonfatal SCBA map"
        return report
    end

    if !usable
        report["status"] = "rejected"
        report["reason"] = "SCBA did not return a usable finite terminal map"
        return report
    end
    numerics = QCLNEGF.QCLNumerics
    density = numerics._electron_density_bar(problem,result.green.Gˡ)
    density_cm3 = density ./ (problem.scales.L₀_m^3*1e6)
    if !all(isfinite,density_cm3)
        report["status"] = "rejected"
        report["reason"] = "SCBA returned a nonfinite density"
        return report
    end
    report["density_z_cm_minus_3"] = density_cm3
    report["density_z_nm"] = problem.grids.x .* (problem.scales.L₀_m*1e9)
    report["density_note"] = "electron density of returned Green state"
    terminal = last(result.history)
    residuals_qualified = all(0 <= getfield(terminal,k) <= 1e-8 for k in (:r_K,:r_Σ,:r_λ))
    consecutive = length(result.history) >= 8
    if consecutive
        tail = result.history[end-7:end]
        consecutive = all(isfinite(row.J) && isfinite(row.raw_charge) for row in tail) &&
                      all(==(1),diff(getproperty.(tail,:ν)))
        if consecutive
            currents = getproperty.(tail,:J) ./ 1e4
            report["last8_current_range_A_cm2"] = maximum(currents)-minimum(currents)
        end
    end
    report["terminal_residuals_admitted"] = residuals_qualified
    report["consecutive_last8_admitted"] = consecutive
    report["status"] = result.converged && residuals_qualified && consecutive ? "measured" : "inconclusive"
    return report
end

end # module

run_transport(task::String, args::Vector{String}) = V843Transport.run_transport(task,args)
