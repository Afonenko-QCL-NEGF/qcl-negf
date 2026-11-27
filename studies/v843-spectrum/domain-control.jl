using LinearAlgebra
using QCLNEGF
import QCLNEGFRunner
using QCLNEGFRunner: load_scientific_plan
using SHA
using TOML
using Unitful

function rank11_observation_control(p, n, s, localization)
    grids = build_grids(p, n, s)
    profiles = build_profiles(p, n, s, grids)
    length_unit_nm = s.L₀_m * 1e9
    basis = QCLNEGF.build_multiperiod_reference_basis(p, n, s, grids, profiles; localization)
    z_nm = basis.coordinates .* length_unit_nm
    rows = basis.central_rows
    metric = basis.weights .* length_unit_nm
    W = basis.envelopes[:, basis.central_columns] ./ sqrt(length_unit_nm)
    field_V_per_nm = ustrip(u"V/nm", p.F_bias)
    reference_energy = ustrip(u"eV", p.E_ref)
    # The uncut basis uses a zero-field window; bias is applied to H only
    # after choosing the representation. The same H and W feed both solves.
    H = basis.real_space_hamiltonian .* s.E₀_eV +
        Diagonal(reference_energy .- field_V_per_nm .* (z_nm .- ustrip(u"nm", p.z₀)))

    full = projected_spectrum(H, W, metric)
    cropped = projected_spectrum(H, W, metric; observation_rows = rows)
    restricted = projected_spectrum(H, W, metric; solve_rows = rows)
    full.energies_eV == cropped.energies_eV || error("observing one period changed solve energies")
    control = Dict{String,Any}()
    if localization === :pzp_tails
        cell = localized_cell_spectrum(p, n, s, grids, profiles)
        cutoff_error_eV = maximum(abs, restricted.energies_eV - cell.energies_eV)
        cutoff_error_eV <= 1e-10 || error("restricted solve differs from public cell solver")
        control["restricted_vs_cell_max_energy_difference_eV"] = cutoff_error_eV
    end
    @assert sum(abs2.(W) .* metric; dims = 1) ≈ ones(1, n.N_b)
    merge!(control, Dict(
        "schema" => "v843-new-rank11-domains-v1",
        "status" => "measured",
        "historical_w11_reproduction" => false,
        "spatial_nodes_per_period" => n.N_z,
        "rank" => n.N_b,
        "hamiltonian_periods" => basis.periods,
        "localization" => String(basis.localization),
        "boundary" => String(basis.boundary),
        "observed_periods" => 1,
        "z_nm" => z_nm[rows],
        "metric_nm" => cropped.metric,
        "energy_reference_eV" => reference_energy,
        "whole_window_observed_in_cell" => observation(cropped),
        "both_operator_and_basis_restricted_to_cell" => observation(restricted),
    ))
    return control
end

function observation(spectrum)
    densities = abs2.(spectrum.amplitudes)
    return Dict(
        "energies_eV" => spectrum.energies_eV,
        "density_nm_inverse" => collect.(eachcol(densities)),
        "retained_probability" => vec(sum(spectrum.metric .* densities; dims = 1)),
    )
end

function main()
    length(ARGS) == 3 || error("Usage: domain-control.jl FROZEN_PLAN b11-pzp|w11-wannier-proxy OUTPUT_TOML")
    plan = load_scientific_plan(ARGS[1])
    request = ARGS[2]
    variant, localization, half_window = if request == "b11-pzp"
        ("b11-r11", :pzp_tails, 5)
    elseif request == "w11-wannier-proxy"
        ("b9-r11", :bloch_wannier, 4)
    else
        error("unknown domain-control input")
    end
    execution = only(filter(e -> e.variant_id == variant, plan.executions))
    execution.operation === :structure_spectrum ||
        error("domain control requires the frozen structure_spectrum operation")
    point = only(filter(p -> p.execution_id == execution.id, plan.points))
    workflow = QCLNEGFRunner.QCLScientificWorkflow
    configuration = execution.configuration
    raw = workflow._point_resolved_raw(configuration, point)
    resolved = QCLNEGFRunner._resolve_configuration(raw, configuration.provenance)
    p, n, s = resolved.physical, resolved.numerical, resolved.scales
    @assert n.N_z == 144 && n.P_basis == half_window && n.N_b == 11
    @assert ustrip(u"kV/cm", p.F_bias) ≈ 21.0
    @assert point.temperature_K == point.lo_temperature_K == 50.0

    report = rank11_observation_control(p, n, s, localization)
    report["configuration_source_plan_fingerprint"] = plan.fingerprint
    report["configuration_source_execution_id"] = execution.id
    report["configuration_source_point_id"] = point.id
    report["voltage_per_period_V"] = point.voltage_per_period_V
    report["temperature_K"] = point.temperature_K
    report["lo_temperature_K"] = point.lo_temperature_K
    report["driver_sha256"] = bytes2hex(open(sha256, @__FILE__))
    report["case"] = request
    !ispath(ARGS[3]) || error("domain-control output already exists")
    open(ARGS[3], "w") do io
        TOML.print(io, report)
    end
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
