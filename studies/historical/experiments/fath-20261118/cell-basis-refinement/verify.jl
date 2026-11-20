using LinearAlgebra, SHA, TOML, Unitful
import QCLNEGF
include("RefinedCellBasis.jl")

const Q = QCLNEGF
const N = Q.QCLNumerics
const PASSPORT = TOML.parsefile(joinpath(@__DIR__, "passport.toml"))
const CHANNELS = [:LO,:acoustic,:impurity,:IFR,:alloy]

function fath_physical(d)
    layers = map(eachindex(d["material_order"])) do i
        kind = d["material_order"][i]
        barrier = kind == "AlGaAs"
        mass = d[barrier ? "barrier_mass_over_me" : "well_mass_over_me"]
        Q.Layer(d=d["thickness_nm"][i]*u"nm", material=Symbol(kind),
            x_Al=barrier ? d["barrier_x_Al"] : 0.0, Eᶜ=(barrier ? d["CBO_meV"] : 0.0)*u"meV",
            mᶻᵣ=mass, m_parallelᵣ=mass,
            εᵣ=d[barrier ? "barrier_permittivity" : "well_permittivity"],
            doped=i==d["doped_segment_index"])
    end
    return Q.PhysicalParameters(
        layers,d["sheet_donors_m_minus_2"]*u"m^-2",d["ionized_fraction"],0u"V/m",
        d["z_reference_nm"]*u"nm",d["energy_reference_eV"]*u"eV",
        d["lattice_temperature_K"]*u"K",d["LO_temperature_K"]*u"K",
        d["epsilon_static"],d["epsilon_optical"],d["LO_energy_meV"]*u"meV",
        d["q_impurity_nm_inverse"]*u"nm^-1",d["q_LO_nm_inverse"]*u"nm^-1",
        d["IFR_height_nm"]*u"nm",d["IFR_correlation_length_nm"]*u"nm",
        d["acoustic_deformation_eV"]*u"eV",d["mass_density_kg_m3"]*u"kg/m^3",
        d["sound_speed_m_s"]*u"m/s",d["alloy_disorder_eV"]*u"eV",d["alloy_volume_m3"]*u"m^3",
        d["spin_degeneracy"],d["interface_positions_nm"].*u"nm",
    )
end

function relative_error(a, b)
    return maximum(abs, a-b)/max(maximum(abs, b), eps(Float64))
end

function matrix_check(p)
    nz = p.numerical.N_z
    phi = p.basis.Φ
    E = p.profiles.Eᶜ
    mass = p.profiles.mᶻᵣ
    dx = only(unique(p.grids.wˣ))
    h = Q.build_bdd_hamiltonian(repeat(E, 7), repeat(mass, 7), dx, Q.QCLReferenceOperators._C̄(p.scales))
    centre, right = (3nz+1:4nz), (4nz+1:5nz)
    expected = [
        phi' * h[centre,centre] * phi,
        phi' * h[centre,right] * phi,
        phi' * h[right,centre] * phi,
        phi' * Diagonal(p.grids.x) * phi,
        phi' * Diagonal(1 ./ p.profiles.m_parallelᵣ) * phi,
    ]
    actual = [p.basis.H₀, p.basis.T₊, p.basis.T₋, p.basis.Z, p.basis.M⁻¹]
    matrix_errors = Dict(key => relative_error(a,b) for
        (key,a,b) in zip(["H0","Tplus","Tminus","Z","M_inverse"],actual,expected))
    @assert maximum(values(matrix_errors)) < 1e-12
    return matrix_errors
end

function kernel_check(p)
    literal = Q.build_kernels(p.physical,p.numerical,p.scattering,p.scales,p.grids,p.profiles,p.basis)
    @assert Set(p.kernels.enabled) == Set(literal.enabled) == Set(CHANNELS)
    relative_errors = Dict(string(key)=>
        relative_error(p.kernels.K[key]*p.kernels.qᴷ[key],literal.K[key]*literal.qᴷ[key])
        for key in CHANNELS)
    relative_errors["LO_form_factor"] = relative_error(p.kernels.Fᴸᴼ,literal.Fᴸᴼ)
    @assert maximum(values(relative_errors)) < 1e-12
    return relative_errors
end

function main()
    BLAS.set_num_threads(1)
    @assert BLAS.get_num_threads() == Threads.nthreads() == 1
    core = dirname(dirname(pathof(Q)))
    @assert readchomp(`git -C $core rev-parse HEAD`) == PASSPORT["core_commit"]
    @assert readchomp(`git -C $core rev-parse $("HEAD^{tree}")`) == PASSPORT["core_tree"]
    @assert isempty(readchomp(`git -C $core status --porcelain --untracked-files=no`))
    device_path = joinpath(@__DIR__, "../transport/device.toml")
    device = TOML.parsefile(device_path)
    sc = Q.ScaleSystem()
    phys = fath_physical(device)
    n = Q.NumericalParameters(
        N_z=144, N_b=9, P_basis=3, E_min=-400u"meV", E_max=4000u"meV", N_E=121,
        M_E=260u"meV", k_max=0.60u"nm^-1", N_k=2, N_φ=4,
        qz_max=10u"nm^-1", N_qz=5, η_seed=0.5u"meV",
    )
    alg = Q.AlgorithmOptions(kernel_build=:direct, energy_shift=:sparse_plan,
        hilbert=:product_integration, elastic_retarded=:direct_green, embedding=:finite_chain,
        embedding_periods=4, occupation_normalization=:paired_convex)
    scattering = Q.ScatteringOptions(LO=true,acoustic=true,impurity=true,IFR=true,alloy=true)
    models = Q.PhysicalModelOptions(screening=:fixed,dispersion=:parabolic,
        electron_electron=Q.ElectronElectronOptions(mode=:none),lo_population=:thermal)
    made = RefinedCellBasis.build_problem(; physical=phys,numerical=n,scales=sc,scattering,
        algorithms=alg,kernel_options=Q.ProductionKernelOptions(),physical_models=models)
    p = made.problem
    aimed = Q.retarget_problem(p; V_period=54u"mV", energy_shift=:sparse_plan)
    voltage = ustrip(u"mV",aimed.physical.F_bias*Q.period_length(aimed.physical))
    @assert voltage ≈ 54
    @assert aimed.basis === p.basis && aimed.kernels.K === p.kernels.K && aimed.kernels.Fᴸᴼ === p.kernels.Fᴸᴼ
    biased_report = Q.validate_problem(aimed)
    @assert biased_report.passed
    @assert p.basis.localization === :bloch_snapshot_pod
    @assert !haskey(biased_report.metrics,:translation)
    @assert isnan(p.basis.r_translation)
    @assert length(p.basis.window_eigenvalues) == n.N_b
    h = Q.project_hamiltonians(aimed,zeros(n.N_z))
    options = Q.ProductionOptions(algorithms=alg,worker_count=1,hilbert_columns=1)
    cache = Q.build_production_cache(aimed; options)
    @assert cache.source_kernel_arrays === aimed.kernels.K
    seed, chemical_potential = N._seed_green_production(aimed,h,options)
    populations = Q.state_populations(aimed,seed.Gˡ)
    target_error = abs(sum(populations.p)-1)
    @assert target_error < 1e-12
    spectral=Q.QCLReferenceOperators.spectral_window_diagnostic(aimed,h)
    result = Dict(
        "core_commit"=>PASSPORT["core_commit"],"core_tree"=>PASSPORT["core_tree"],
        "julia_version"=>string(VERSION),
        "device_sha256"=>bytes2hex(open(sha256,device_path)),
        "adapter_sha256"=>bytes2hex(open(sha256,joinpath(@__DIR__,"RefinedCellBasis.jl"))),
        "basis_provenance"=>made.training.provenance,
        "basis_method"=>string(p.basis.localization),"train_bands"=>made.training.train_bands,
        "train_phase_count"=>made.training.phase_count,
        "n_z"=>n.N_z,"n_b"=>n.N_b,"n_e"=>n.N_E,"n_k"=>n.N_k,
        "n_phi"=>n.N_φ,"n_qz"=>n.N_qz,"bias_mv"=>voltage,
        "native_structural_pass_zero_and_54mv"=>true,
        "reuses_identical_basis_and_kernels_after_retarget"=>true,
        "training_eigensolve_scaled_max_residual"=>p.basis.r_eigen,
        "basis_orthogonality_frobenius_residual"=>p.basis.r_orth,
        "matrix_projection_max_relative_error" => matrix_check(p),
        "native_exact_parallel_vs_native_literal_max_relative_error"=>kernel_check(aimed),
        "production_cache_reuses_kernel_arrays"=>true,
        "native_seed_chemical_potential_mev"=>chemical_potential*sc.E₀_eV*1e3,
        "native_seed_donor_relative_error"=>target_error,
        "spectral_window"=>Dict(string(k)=>(v isa Symbol ? string(v) : v) for (k,v) in pairs(spectral)),
        "energy_unit_mev"=>sc.E₀_eV*1e3,"scba_iterations"=>0,
        "phi"=>[collect(real(row)) for row in eachrow(p.basis.Φ)],
    )
    path = joinpath(@__DIR__,"verification.toml")
    open(io->TOML.print(io,result;sorted=true),path*".tmp","w")
    mv(path*".tmp",path;force=true)
    delete!(result,"phi")
    result["full_verification_sha256"] = bytes2hex(open(sha256,path))
    compact_path = joinpath(@__DIR__,"verification-summary.toml")
    open(io->TOML.print(io,result;sorted=true),compact_path*".tmp","w")
    mv(compact_path*".tmp",compact_path;force=true)
end

main()
