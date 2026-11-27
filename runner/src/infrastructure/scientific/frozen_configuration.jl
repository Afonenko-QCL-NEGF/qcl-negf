# The author parser applies defaults. Store the resulting values under the
# same public keys so that execution can verify and hydrate a complete plan.
function _freeze_configuration(config::ResolvedRunConfiguration)
    data = deepcopy(config.raw)
    _freeze_quantities!(data["physical"], (
        "position_origin" => "m", "reference_energy" => "eV",
        "lattice_temperature" => "K", "lo_temperature" => "K",
        "voltage_per_period" => "V", "field_bias" => "V/m",
        "donor_sheet_density" => "m^-2", "lo_phonon_energy" => "eV",
        "impurity_screening_wavenumber" => "m^-1", "lo_screening_wavenumber" => "m^-1",
        "interface_roughness_height" => "m", "interface_correlation_length" => "m",
        "acoustic_deformation_potential" => "eV", "mass_density" => "kg/m^3",
        "sound_velocity" => "m/s", "alloy_potential" => "eV", "primitive_cell_volume" => "m^3",
    ))
    for layer in data["physical"]["layers"]
        _freeze_quantities!(layer, ("thickness" => "m", "conduction_band_edge" => "eV"))
    end
    data["physical"]["interfaces"] = [
        _frozen_quantity(value, "m", "physical.interfaces")
        for value in data["physical"]["interfaces"]
    ]
    _freeze_quantities!(data["numerical"], (
        "energy_min" => "eV", "energy_max" => "eV", "energy_trust_margin" => "eV",
        "momentum_max" => "m^-1", "longitudinal_momentum_max" => "m^-1",
        "seed_broadening" => "eV",
    ))
    _freeze_quantities!(data["scales"], ("energy" => "eV", "length" => "m"))
    _freeze_quantities!(data["study"], ("photon_energy_min" => "eV", "photon_energy_max" => "eV"))
    for (field, unit) in ("voltages_per_period" => "V", "temperatures" => "K")
        data["study"][field] = [
            _frozen_quantity(value, unit, field) for value in data["study"][field]
        ]
    end

    convergence = config.solver.convergence
    convergence_data = data["solver"]["convergence"]
    convergence_data["mode"] = String(convergence.mode)
    convergence_data["trend"] = _frozen_fields(convergence.trend)
    diagnostic = convergence.diagnostic_quality
    merge!(convergence_data["diagnostic_quality"], Dict(
        "target_fixed_point" => diagnostic.target_fixed_point_threshold,
        "coarse_wait_iterations" => diagnostic.coarse_wait_iterations,
        "strict_attempt_iterations" => diagnostic.strict_attempt_iterations,
        "observables" => diagnostic.observable_threshold,
        "positivity" => diagnostic.positivity_threshold,
        "causality" => diagnostic.causality_threshold,
        "outer_threshold" => diagnostic.outer_threshold,
    ))
    data["production"]["physics_markers"] = _frozen_fields(config.production.physics_markers)
    data["kernel_construction"]["impurity_angular_tolerance"] =
        config.kernels.impurity_angular_tolerance
    for field in (:occupation_normalization, :embedding, :embedding_periods)
        data["algorithms"][String(field)] = _frozen_scalar(getproperty(config.algorithms, field))
    end
    for field in (:debug_hdf5, :light_max_space_points, :light_max_energy_points,
                  :light_max_momentum_points, :light_max_snapshots, :intermediate_checkpoints)
        data["output"][String(field)] = getproperty(config.output, field)
    end
    models = config.physical_models
    model_data = get!(data, "physical_models", Dict{String,Any}())
    for field in fieldnames(typeof(models))
        field === :electron_electron && continue
        model_data[String(field)] = _frozen_scalar(getproperty(models, field))
    end
    ee_data = get!(model_data, "electron_electron", Dict{String,Any}())
    for field in (:mode, :screening_dimension, :include_exchange)
        ee_data[String(field)] = _frozen_scalar(getproperty(models.electron_electron, field))
    end
    data["domain_adaptation"] = _frozen_fields(config.domain_adaptation)
    return data
end

_frozen_scalar(value) = value isa Symbol ? String(value) : value
_frozen_fields(value) = Dict{String,Any}(
    String(field) => _frozen_scalar(getfield(value, field)) for field in fieldnames(typeof(value))
)

function _frozen_quantity(value, unit, field)
    quantity = _untyped_quantity(value, field)
    return string(ustrip(Unitful.uparse(unit), quantity), " ", unit)
end

function _freeze_quantities!(data, fields)
    for (field, unit) in fields
        value = get(data, field, nothing)
        value === nothing || (data[field] = _frozen_quantity(value, unit, field))
    end
end
