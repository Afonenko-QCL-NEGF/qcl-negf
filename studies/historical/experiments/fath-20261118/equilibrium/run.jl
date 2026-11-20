using HDF5, LinearAlgebra, QCLNEGF, SHA, TOML, Unitful

const N = QCLNEGF.QCLNumerics
const MAP_BUDGET = 256
const SAMPLE_MAPS = (48, 128, MAP_BUDGET)
const EXPECTED_CHANNELS = Set((:LO, :acoustic, :impurity, :IFR, :alloy))
const EXPECTED_HEAD = "e171caa60cce676c6c4238dd671e7c527f2bd977"
const EXPECTED_TREE = "742ed5a6fe82f1e5c63fc1a2290ed77f89ca6da8"
const EXPECTED_MANIFEST = "da0780fbe150c0e16e9fedf3566a1971095642f14f57f32524b52f430a4adb65"
const METRICS = (:ν, :J, :r_D, :r_A, :r_K, :r_Σ, :r_λ, :λ, :r_PSD, :r_caus,
                 :r_roundoff, :r_Jchange, :r_population, :raw_charge, :target_charge,
                 :normalized_charge)

function digest(path)
    return bytes2hex(open(sha256, path))
end

function ensure_environment()
    core = dirname(dirname(pathof(QCLNEGF)))
    readchomp(`git -C $core rev-parse HEAD`) == EXPECTED_HEAD || error("Core HEAD differs")
    readchomp(`git -C $core rev-parse $("HEAD^{tree}")`) == EXPECTED_TREE || error("Core tree differs")
    isempty(readchomp(`git -C $core status --porcelain --untracked-files=no`)) ||
        error("Core has modified tracked files")
    manifest = joinpath(dirname(Base.active_project()), "Manifest.toml")
    digest(manifest) == EXPECTED_MANIFEST || error("Manifest differs")
    VERSION == v"1.13.4" && Threads.nthreads(:default) == 1 || error("Unexpected Julia runtime")
    get(ENV, "OMP_NUM_THREADS", "") == "1" || error("OMP could oversubscribe")
    BLAS.set_num_threads(1)
    BLAS.get_num_threads() == 1 || error("BLAS could oversubscribe")
end

function write_toml(path, doc)
    open(path, "w") do output
        TOML.print(output, doc; sorted=true)
    end
end

function algorithms_for(mixing)
    return AlgorithmOptions(; kernel_build=:direct, embedding=:finite_chain, embedding_periods=4,
        mixing, anderson_history_depth=2, anderson_damping=1.0, anderson_regularization=1e-12,
        energy_shift=:sparse_plan, hilbert=:product_integration, elastic_retarded=:direct_green)
end

module FrozenTransport
include(joinpath(@__DIR__, "attempt01", "transport-run.jl"))
end

function main()
    ensure_environment()
    length(ARGS) == 2 || error("Expected output and hashed model")
    output, model_path = abspath.(ARGS)
    device = TOML.parsefile(model_path)
    numerical = NumericalParameters(; N_z=144, N_b=7, P_basis=3, E_min=-0.4u"eV",
        E_max=.56u"eV", N_E=1201, M_E=260u"meV", k_max=.6u"nm^-1", N_k=4,
        N_φ=12, qz_max=10u"nm^-1", N_qz=31, η_seed=0.5u"meV")
    algorithms = algorithms_for(:linear)
    models = PhysicalModelOptions(screening=:fixed, dispersion=:parabolic,
        electron_electron=ElectronElectronOptions(mode=:none), lo_population=:thermal)
    physical = FrozenTransport.device(device)
    physical.Tᴸ == 10u"K" && physical.Tᴸᴼ == 10u"K" || error("Incorrect Fath temperatures")
    p0 = build_configured_scattering_problem(; physical, numerical, scales=ScaleSystem(),
        scattering=ScatteringOptions(LO=true, acoustic=true, impurity=true, IFR=true, alloy=true),
        algorithms,
        kernel_options=ProductionKernelOptions(), physical_models=models).problem
    problem = retarget_problem(p0; V_period=0u"mV", energy_shift=:sparse_plan)
    iszero(problem.physical.F_bias) ||
        error("Incorrect Fath voltage")
    Set(problem.kernels.enabled) == EXPECTED_CHANNELS || error("Incorrect scattering channels")
    problem.models.electron_electron.mode === :none || error("e–e accidentally enabled")
    pbase = ProductionOptions(; algorithms, worker_count=1, parallel_backend=:threads,
        hilbert_columns=1, phase_timing=true, verify_fft_roundoff=true, memory_budget_bytes=600*2^20,
        physics_markers=SCBAPhysicsMarkerPolicy(cadence=16, max_spectral_blocks=32),
        progress_every_scba=1, checkpoint_every_scba=0,
        checkpoint_request=req->(req.stage === :scba && req.iteration in SAMPLE_MAPS))
    scba_options = SolverOptions(; α_Σ=.4, max_scba=MAP_BUDGET, max_poisson=1,
        convergence=ConvergencePolicy(; stagnation_window=0, stagnation_relative_improvement=0.0))
    write_toml(joinpath(output,"identity.toml"), Dict(
        "core"=>EXPECTED_HEAD, "tree"=>EXPECTED_TREE, "manifest_sha256"=>EXPECTED_MANIFEST,
        "biased_control_driver_sha256"=>"270912a8fd0aff3c03612883b24dae42f7a3eca51778194bd236edfb6bdb8099",
        "energy_range_meV"=>[-400.,560.], "k_max_nm_inverse"=>.6,
        "nphi"=>12, "nqz"=>31, "qz_max_nm_inverse"=>10.0, "p_basis"=>3,
        "embedding"=>"finite_chain", "embedding_periods"=>4, "seed_eta_meV"=>.5,
        "occupation_normalization"=>"paired_convex",
        "model_source_sha256"=>digest(model_path),
        "transport_driver_sha256"=>digest(joinpath(@__DIR__, "attempt01", "transport-run.jl")), "case"=>"Fath 10 K, E_C offset 149 meV",
        "potential_drop_mV"=>0.0, "lattice_temperature_K"=>10.0, "LO_temperature_K"=>10.0,
        "hartree"=>"fixed_zero", "electron_electron"=>"none",
        "channels"=>String.(collect(problem.kernels.enabled)), "shape_julia"=>[1201,4,7,7], "spatial_nodes"=>144,
        "alpha"=>.4, "max_scba_per_branch"=>MAP_BUDGET,
        "anderson_history_depth"=>2, "anderson_damping"=>1.,
        "anderson_regularization"=>1.e-12,
        "tolerances"=>Dict(String(f)=>getfield(scba_options.tolerances,f)
                           for f in fieldnames(SolverTolerances)),
        "scba_required_consecutive_passes"=>3, "min_scba_iteration"=>2))
    cache = build_production_cache(problem; options=pbase)
    run_branch(problem, cache, pbase, scba_options, :linear, output)

end

function run_branch(problem, cache, pbase, scba_options, branch, output)
    result_dir = mkdir(joinpath(output, String(branch)))
    rows = mkdir(joinpath(result_dir, "rows"))
    observer = row -> begin
        selected = Dict{String,Any}(String(name)=>getfield(row, name) for name in METRICS)
        assessment = scba_convergence_assessment(row, scba_options.tolerances, scba_options.convergence)
        selected["strict_pass"] = assessment.passed
        selected["failed"] = String.(assessment.failed_metrics)
        write_toml(joinpath(rows,lpad(row.ν,3,'0')*".toml"), selected)
    end
    options = N.with_production_options(pbase; algorithms=algorithms_for(branch))
    start = time_ns()
    result = solve_scba_production(problem, zeros(problem.numerical.N_z);
        options=scba_options, production_options=options, cache, history_observer=observer,
        iteration_callback=record_aligned->write_flux(problem, record_aligned, result_dir))
    isempty(result.history) && error("No aligned SCBA map available")
    write_flux(problem, result, result_dir)
    path = joinpath(result_dir, "fdt-state.h5")
    write_fdt_state(path, problem, result)
    write_toml(joinpath(result_dir,"execution.toml"), Dict("maps"=>length(result.history),
        "fdt_state_sha256"=>digest(path), "state_scope"=>"aligned terminal A/GL/GG for offline FDT",
        "status"=>String(result.status), "quality"=>String(result.quality),
        "converged"=>result.converged, "seconds"=>(time_ns()-start)*1e-9))
end

# Read-only telemetry from the same normalized Green state used in that row.
function write_flux(problem, result, dir)
    row = last(result.history)
    unit = ustrip(u"A/m^2", problem.scales.J₀)/1e4
    jplus = unit*N._production_boundary_flux_bar(problem, result.embedding_plus, result.green)
    jminus = unit*N._production_boundary_flux_bar(problem, result.embedding_minus, result.green)
    jrow = row.J/1e4
    isapprox(jplus, jrow; atol=1e-15, rtol=1e-13) || error("Plus current is not aligned")
    write_toml(joinpath(dir,"flux-$(lpad(row.ν,3,'0')).toml"), Dict(
        "map"=>row.ν, "J_left_out_A_cm2"=>jminus, "J_right_out_A_cm2"=>jplus,
        "sum_out_A_cm2"=>jplus+jminus, "history_right_out_A_cm2"=>jrow,
    ))
end

function write_fdt_state(path, problem, result)
    g = result.green
    h5open(path*".tmp", "w") do output
        output["schema"] = "fath-equilibrium-FDT-terminal-v1"
        output["map"] = last(result.history).ν
        output["hartree_dimensionless"] = zeros(problem.numerical.N_z)
        output["energy_scale_eV"] = problem.scales.E₀_eV
        output["length_scale_m"] = problem.scales.L₀_m
        output["temperature_K"] = ustrip(u"K",problem.physical.Tᴸ)
        output["spin_degeneracy"] = problem.physical.g_s
        output["target_number_dimensionless"] = last(result.history).target_charge
        output["energy_dimensionless"] = problem.grids.ε
        output["energy_weight"] = problem.grids.wᴱ
        output["radial_weight"] = problem.grids.wᵏ
        output["k_dimensionless"] = problem.grids.κ
        for (name,field) in (("A",g.A),("GL",g.Gˡ),("GG",g.Gᵍ))
            FrozenTransport.write_complex(output,name,field)
        end
    end
    mv(path*".tmp",path)
end

main()
