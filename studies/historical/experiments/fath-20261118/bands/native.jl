using LinearAlgebra, TOML, Unitful
import QCLNEGF
using QCLNEGF: Layer, PhysicalParameters, NumericalParameters, ScaleSystem
using QCLNEGF: build_basis, build_grids, build_profiles, project_hamiltonians

const HERE = @__DIR__
const INPUT = TOML.parsefile(joinpath(HERE, "passport.toml"))
BLAS.set_num_threads(1)
@assert Threads.nthreads() == 1 && BLAS.get_num_threads() == 1
const PACKAGE = dirname(dirname(pathof(QCLNEGF)))
@assert readchomp(`git -C $PACKAGE rev-parse HEAD`) == INPUT["core_commit"]
@assert readchomp(`git -C $PACKAGE rev-parse $("HEAD^{tree}")`) == INPUT["core_tree"]
@assert isempty(readchomp(`git -C $PACKAGE status --short`))

function make_physical(cbo, voltage=0.0)
    barriers = INPUT["barrier_layers_1based"]
    layers = map(eachindex(INPUT["layer_width_nm"])) do i
        barrier = i in barriers
        mass = INPUT[barrier ? "barrier_mass_z_parallel_over_me" : "well_mass_z_parallel_over_me"]
        Layer(
            d=INPUT["layer_width_nm"][i]*u"nm", material=barrier ? :AlGaAs : :GaAs,
            x_Al=barrier ? INPUT["al_mole_fraction_barrier"] : 0.0,
            Eᶜ=(barrier ? cbo : 0.0)*u"meV",
            mᶻᵣ=mass, m_parallelᵣ=mass, εᵣ=12.9, doped=i in INPUT["donor_layers_1based"],
        )
    end
    # The dielectric/acoustic/LO/screening/IFR values below only satisfy the
    # constructor. This driver never builds a kernel or uses Poisson.
    return PhysicalParameters(
        layers, INPUT["donor_sheet_cm2"]*u"cm^-2", INPUT["ionized_fraction"],
        (voltage / sum(INPUT["layer_width_nm"]))*u"mV/nm", INPUT["position_zero_nm"]*u"nm", INPUT["energy_zero_mev"]*u"meV",
        INPUT["lattice_temperature_k"]*u"K", INPUT["lo_bath_temperature_k"]*u"K",
        12.9, 10.89, 36.7u"meV", 0.2u"nm^-1", 0.2u"nm^-1", 0.12u"nm",
        10.0u"nm", 7.0u"eV", 5317u"kg/m^3", 5240u"m/s",
        nothing, nothing, 2, INPUT["interface_nm"].*u"nm",
    )
end

function make_numerical(nz, nb, half_window=INPUT["basis_half_window_periods"])
    # The non-spatial grid arguments are constructor placeholders.
    return NumericalParameters(
        N_z=nz, N_b=nb, P_basis=half_window,
        E_min=-0.3u"eV", E_max=0.9u"eV", N_E=3, M_E=0.08u"eV",
        k_max=0.6u"nm^-1", N_k=2, N_φ=4, qz_max=10.0u"nm^-1",
        N_qz=3, η_seed=1.25u"meV",
    )
end

function real_rows(a)
    @assert maximum(abs, imag.(a)) < 1e-12
    return [collect(real.(row)) for row in eachrow(a)]
end

function basis_record(cbo, nz, nb, half_window, p0, grids, profiles, scales)
    n = make_numerical(nz, nb, half_window)
    b = build_basis(p0, n, scales, grids, profiles; localization=:pzp)
    p54 = make_physical(cbo, 54)
    projected = project_hamiltonians(b, grids, profiles, p54, scales, zeros(nz))
    return Dict(
        "nb" => nb, "basis_half_window" => half_window,
        "h0" => real_rows(b.H₀), "h54" => real_rows(projected[1,:,:]),
        "tplus" => real_rows(b.T₊), "tminus" => real_rows(b.T₋),
        "position" => real_rows(b.Z), "phi" => real_rows(b.Φ),
        "centre" => b.centres, "spread" => b.spreads,
        "overlap_min" => minimum(b.overlap_eigenvalues),
        "r_orth" => b.r_orth, "r_eigen" => b.r_eigen,
        "r_translation" => b.r_translation,
        "r_translation_nearest" => b.r_translation_nearest,
        "r_translation_two_pairs" => b.r_translation_two_pairs,
    )
end

function main()
    started = time()
    scales = ScaleSystem()
    result = Dict{String,Any}(
        "julia_version" => string(VERSION), "blas_threads" => BLAS.get_num_threads(),
        "julia_threads" => Threads.nthreads(), "scales" => Dict(
            "length_nm" => scales.L₀_m * 1e9, "energy_mev" => scales.E₀_eV * 1e3,
        ),
        "cases" => [],
    )
    for cbo in INPUT["barrier_mev"], nz in INPUT["spatial_nodes"]
        p = make_physical(cbo)
        n = make_numerical(nz, first(INPUT["modes"]))
        grids = build_grids(p, n, scales)
        profiles = build_profiles(p, n, scales, grids)
        case = Dict{String,Any}(
            "cbo_mev" => cbo, "nz" => nz,
            "coordinate" => grids.x, "weight" => grids.wˣ,
            "potential" => profiles.Eᶜ, "mass_z" => profiles.mᶻᵣ,
            "mass_parallel" => profiles.m_parallelᵣ, "layer_index" => profiles.layer_index,
            "donor_profile" => profiles.Nᴰ, "basis" => [],
        )
        for nb in INPUT["modes"]
            push!(case["basis"], basis_record(
                cbo, nz, nb, INPUT["basis_half_window_periods"], p, grids, profiles, scales,
            ))
        end
        push!(result["cases"], case)
    end
    result["elapsed_seconds"] = time() - started
    open(joinpath(HERE, "native.toml"), "w") do io
        TOML.print(io, result; sorted=true)
    end
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
