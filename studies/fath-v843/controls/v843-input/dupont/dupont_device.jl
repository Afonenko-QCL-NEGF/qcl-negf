module DupontDevice

using LinearAlgebra: dot
using QCLNEGF
using TOML
using Unitful

const Numerics = QCLNEGF.QCLNumerics
const DEFAULT_DEVICE = joinpath(@__DIR__, "device.toml")

function physical_inputs(field_kV_cm::Real; device=DEFAULT_DEVICE)
    input = TOML.parsefile(device)
    widths = input["layer_thickness_nm"]
    edges = cumsum([0.0; widths])
    @assert length(widths) == 8
    @assert isapprox(last(edges), input["period_nm"]; rtol=1e-14)
    @assert isapprox(widths[1] / 2, input["donor_center_nm"]; rtol=1e-14)
    layers = Layer[]
    for (i, width) in pairs(widths)
        barrier = isodd(i)
        mass = input[barrier ? "barrier_mass_over_me" : "well_mass_over_me"]
        push!(layers, Layer(
            d=width*u"nm",
            material=barrier ? :AlGaAs : :GaAs,
            x_Al=barrier ? input["barrier_x_al"] : 0.0,
            Eᶜ=(barrier ? input["barrier_offset_meV"] : 0.0)*u"meV",
            mᶻᵣ=mass,
            m_parallelᵣ=mass,
            εᵣ=input["epsilon_static"],
            doped=i==1,
        ))
    end
    # The positive placeholders for q are replaced by the thermodynamic closure.
    @assert input["screening_model"] == "density_temperature"
    @assert input["electron_electron_collisions"] == "none"
    @assert input["photon_field"] == "dark"
    physical = PhysicalParameters(
        layers, input["sheet_donors_m_minus_2"]*u"m^-2", input["ionized_fraction"],
        field_kV_cm*u"kV/cm", 0.0u"nm", 0.0u"eV",
        input["lattice_temperature_K"]*u"K", input["lo_temperature_K"]*u"K",
        input["epsilon_static"], input["epsilon_optical"], input["lo_energy_meV"]*u"meV",
        1.0u"nm^-1", 1.0u"nm^-1",
        input["ifr_height_nm"]*u"nm", input["ifr_correlation_length_nm"]*u"nm",
        input["acoustic_deformation_eV"]*u"eV", input["mass_density_kg_m3"]*u"kg/m^3",
        input["sound_speed_m_s"]*u"m/s", input["alloy_disorder_eV"]*u"eV",
        (input["lattice_constant_nm"]*u"nm")^3 / 4,
        input["spin_degeneracy"], [z*u"nm" for z in edges[1:end-1]],
    )
    models = PhysicalModelOptions(
        screening=:density_temperature,
        screening_temperature_K=input["screening_temperature_K"],
        screening_mass_ratio=input["screening_mass_over_me"],
        dispersion=:parabolic,
        electron_electron=ElectronElectronOptions(mode=:none),
        lo_population=:thermal,
    )
    return (
        physical=Numerics.resolve_physical_models(physical, models),
        models,
        donor_center=input["donor_center_nm"]*u"nm",
        ifr=Symbol(input["ifr_correlation"]),
    )
end

function sheet_profiles(physical, numerical, scales, grids, donor_center)
    base = build_profiles(physical, numerical, scales, grids)
    z = scaled_value(donor_center, scales, :length)
    target = Numerics._scaled_physics(physical, scales).Nᴰ²ᴰ
    right = searchsortedfirst(grids.x, z)
    1 < right <= length(grids.x) || throw(ArgumentError("Donor sheet lies outside the grid"))
    left = right - 1
    all(==(1), base.layer_index[left:right]) ||
        throw(ArgumentError("Donor sheet requires two centres in the injection barrier"))
    fraction_right = (z - grids.x[left]) / (grids.x[right] - grids.x[left])
    donor = zeros(length(grids.x))
    donor[left] = (1.0 - fraction_right) * target / grids.wˣ[left]
    donor[right] = fraction_right * target / grids.wˣ[right]
    isapprox(dot(grids.wˣ, donor), target; rtol=1e-14) || error("Donor sheet integral changed")
    centroid = dot(grids.x, grids.wˣ .* donor) / target
    isapprox(centroid, z; rtol=1e-14) || error("Donor sheet centroid shifted")
    return Numerics.MaterialProfiles(
        base.Eᶜ, base.mᶻᵣ, base.m_parallelᵣ, base.εᵣ,
        donor, base.x_Al, base.layer_index,
    )
end

function ifr_kernels(kernels, physical, scales, grids, correlation)
    correlation == :gaussian && return kernels
    correlation == :exponential || throw(ArgumentError("Unsupported IFR correlation"))
    first(grids.κ) == 0 || error("IFR covariance extraction requires the exact k=0 ring")
    λ = scaled_value(physical.Λᴵᶠᴿ, scales, :length)
    normalized = kernels.K[:IFR]
    raw_k0 = kernels.qᴷ[:IFR] .* view(normalized, 1, 1, :, :, :, :)
    raw = similar(normalized)
    for (j, kp) in pairs(grids.κ), (i, k) in pairs(grids.κ)
        # Ratio to the Gaussian q=0 spectrum. Spatial overlaps and RMS
        # displacement are kept, and the exponential q=0 spectrum is doubled.
        weight = sum(grids.φ) do angle
            q2 = max(0.0, k^2 + kp^2 - 2k*kp*cos(angle))
            return 2.0 * (1.0 + λ^2*q2)^(-1.5)
        end / length(grids.φ)
        @views raw[i, j, :, :, :, :] .= weight .* raw_k0
    end
    replacement = Numerics._normalize_production_kernels(Dict(:IFR => raw), kernels.Fᴸᴼ)
    return Numerics.KernelSet(
        merge(kernels.K, replacement.K), merge(kernels.qᴷ, replacement.qᴷ),
        kernels.Fᴸᴼ, kernels.enabled,
    )
end

"""Prepare the V843 problem. Building physical inputs and kernels runs no transport."""
function prepare(
    field_kV_cm::Real, numerical::NumericalParameters, options::ProductionOptions;
    device=DEFAULT_DEVICE, scales=ScaleSystem(),
    kernel_options=ProductionKernelOptions(), grids=nothing, basis_builder=nothing,
)
    inputs = physical_inputs(field_kV_cm; device)
    (; physical, models) = inputs
    scattering = ScatteringOptions(LO=true, acoustic=true, impurity=true, IFR=true, alloy=true)
    grids = isnothing(grids) ? build_grids(physical, numerical, scales) : grids
    estimate = Numerics._preflight_production_memory(
        numerical, scattering, options; energy_nodes=grids.ε,
    )
    profiles = sheet_profiles(physical, numerical, scales, grids, inputs.donor_center)
    basis = if isnothing(basis_builder)
        build_basis(physical, numerical, scales, grids, profiles; localization=:pzp)
    else
        basis_builder(physical, numerical, scales, grids, profiles)
    end
    plan = Numerics.scattering_numerical_plan(
        options.algorithms, kernel_options; solver_backend=:production,
    )
    context = Numerics.ScatteringAssemblyContext(
        physical, numerical, scales, grids, profiles, basis,
    )
    assembled = Numerics.assemble_scattering_kernels(
        context, Numerics.scattering_models(physical, scattering), plan,
    )
    kernels = ifr_kernels(assembled.kernels, physical, scales, grids, inputs.ifr)
    sp = Numerics._scaled_physics(physical, scales)
    shifts = map((sp.Eᵖ, -sp.Eᵖ, sp.ħωᴸᴼ, -sp.ħωᴸᴼ)) do displacement
        Numerics.build_shift_plan(grids.ε, displacement)
    end
    problem = NEGFProblem(
        physical, numerical, scattering, scales, grids, profiles, basis,
        kernels, shifts..., :nodal_linear, models,
    )
    report = validate_problem(problem)
    report.passed || error(join(report.messages, "\n"))
    return (; problem, static=report, assembled.diagnostics, estimate)
end

end
