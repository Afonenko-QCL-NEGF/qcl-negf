# V843 native fixed-potential diagnostic; launch through the Julia Runner project.
using QCLNEGFRunner
using LinearAlgebra
using TOML
using SHA
using Unitful
const CoreNUM = QCLNEGFRunner.QCLNEGF.QCLNumerics
using QCLNEGF
include(joinpath(@__DIR__, "..", "fath-v843", "controls", "v843-input", "dupont", "dupont_device.jl"))

const USAGE = "usage: julia --startup-file=no --project=runner --threads=N studies/cluster-eight-20261126/v843_native.jl FIELD_KV_CM K OUTDIR [MAX_SCBA] [MEMORY_GIB] [NPHI]; or --describe"

function describe(field, k, maps, memory, nphi)
    return Dict{String,Any}(
        "schema"=>"qcl-v843-native-fixed-u-diagnostic-v1", "field_kV_cm"=>field,
        "voltage_mV_per_period"=>3.616field, "radial_nodes"=>k,
        "temperature_K"=>50.0, "hartree"=>"fixed U_H=0; no Poisson loop",
        "method"=>"native production SCBA; finite-chain embedding; linear mixing; direct elastic retarded; paired convex occupation; product integration; nodal-linear energy shifts",
        "interpretation"=>"new native diagnostic; not equivalent to archived linked solver; finite iterations do not establish stationarity or grid convergence",
        "energy_min_meV"=>-650.0, "energy_max_meV"=>1000.0, "energy_nodes"=>239,
        "energy_trust_margin_meV"=>390.0, "spatial_nodes"=>144, "basis_states"=>7,
        "basis_periods"=>3, "basis"=>"pzp", "angular_nodes"=>nphi,
        "qz_nodes"=>161, "k_max_nm_inverse"=>0.6, "qz_max_nm_inverse"=>10.0,
        "seed_eta_meV"=>0.5, "embedding_periods"=>4, "alpha_sigma"=>0.2,
        "max_scba"=>maps, "memory_budget_GiB"=>memory,
        "channels"=>["LO", "acoustic", "impurity", "IFR", "alloy"],
        "light"=>"dark", "electron_electron_collisions"=>"none",
        "screening"=>"density_temperature", "ifr_correlation"=>"exponential",
        "cold_start"=>true, "workers"=>Threads.nthreads(:default), "blas_threads"=>1)
end

function atomic_toml(path, data)
    tmp = path * ".tmp"
    open(tmp,"w") do io
        TOML.print(io,data;sorted=true)
    end
    mv(tmp,path;force=true)
end

function main(args)
    if args == ["--describe"]
        TOML.print(stdout,describe(21.0,9,128,8.0,32);sorted=true)
        return
    end
    3 <= length(args) <= 6 || error(USAGE)
    field = parse(Float64,args[1]); k = parse(Int,args[2]); out = abspath(args[3])
    maps = length(args)>=4 ? parse(Int,args[4]) : 128
    memory = length(args)>=5 ? parse(Float64,args[5]) : 8.0
    nphi = length(args)>=6 ? parse(Int,args[6]) : 32
    nphi in (32,128) || error("NPHI must be 32 or 128")
    field in (12.5,21.0) || error("field must be 12.5 or 21 kV/cm")
    k in (9,17,33) || error("K must be 9, 17 or 33")
    maps > 0 && isfinite(memory) && memory > 0 || error("positive iteration count and memory budget required")
    ispath(out) && error("output path already exists")
    BLAS.set_num_threads(1)
    algorithms = AlgorithmOptions(kernel_build=:direct,embedding=:finite_chain,embedding_periods=4,
        mixing=:linear,energy_shift=:sparse_plan,hilbert=:product_integration,
        elastic_retarded=:direct_green,occupation_normalization=:paired_convex)
    po = ProductionOptions(algorithms=algorithms,worker_count=Threads.nthreads(:default),
        parallel_backend=:threads,memory_budget_bytes=round(Int,memory*1024^3),
        checkpoint_every_scba=0,checkpoint_every_outer=0)
    n = NumericalParameters(N_z=144,N_b=7,P_basis=3,E_min=-650u"meV",E_max=1000u"meV",
        N_E=239,M_E=390u"meV",k_max=0.6u"nm^-1",N_k=k,N_φ=nphi,
        qz_max=10u"nm^-1",N_qz=161,η_seed=0.5u"meV")
    so = SolverOptions(α_Σ=0.2,max_scba=maps,max_poisson=1,
        convergence=ConvergencePolicy(stagnation_window=0,stagnation_relative_improvement=0.0,
            minimum_scba_iterations=2,required_consecutive_scba_passes=3))
    mkdir(out)
    record = describe(field,k,maps,memory,nphi)
    record["status"] = "building"
    record["device_sha256"] = bytes2hex(open(sha256,DupontDevice.DEFAULT_DEVICE))
    record["driver_sha256"] = bytes2hex(open(sha256,@__FILE__))
    record["julia_version"] = string(VERSION)
    record["core"] = QCLNEGFRunner._linked_package_identity(QCLNEGF)
    record["runner"] = QCLNEGFRunner._linked_package_identity(QCLNEGFRunner)
    manifest = joinpath(dirname(Base.active_project()), "Manifest.toml")
    record["manifest_sha256"] = bytes2hex(open(sha256, manifest))
    record["completed_iterations"] = 0
    atomic_toml(joinpath(out,"summary.toml"),record)
    try
        built = DupontDevice.prepare(field,n,po)
        p = built.problem
        record["memory_estimate_peak_bytes"] = built.estimate.peak_bytes
        record["status"] = "running"
        atomic_toml(joinpath(out,"summary.toml"),record)
        rows = Dict{String,Any}[]
        observer = row -> begin
            d = Dict{String,Any}(string(f)=>getfield(row,f) for f in fieldnames(typeof(row))
                if fieldtype(typeof(row),f)<:Real)
            d["J_A_cm2"] = row.J/1e4
            push!(rows,d)
            if length(rows) % 8 == 0
                record["completed_iterations"] = length(rows)
                record["iterations"] = rows
                atomic_toml(joinpath(out,"summary.toml"),record)
            end
        end
        result = solve_scba_production(p,zeros(n.N_z);options=so,production_options=po,
            history_observer=observer)
        record["status"] = string(result.status)
        record["quality"] = string(result.quality)
        record["scba_converged"] = result.converged
        record["stationarity"] = "not established by native SCBA convergence alone"
        record["completed_iterations"] = length(rows)
        record["iterations"] = rows
        if !isempty(rows)
            record["last_iteration"] = last(rows)
        end
        density = CoreNUM._electron_density_bar(p,result.green.Gˡ)
        record["density_z_cm_minus_3"] = density ./ (p.scales.L₀_m^3*1e6)
        record["density_z_nm"] = p.grids.x .* (p.scales.L₀_m*1e9)
        record["density_note"] = "density of returned Green state; inspect convergence and iterate provenance before interpretation"
        atomic_toml(joinpath(out,"summary.toml"),record)
    catch err
        record["status"] = "failed"
        record["error"] = sprint(showerror,err)
        atomic_toml(joinpath(out,"summary.toml"),record)
        rethrow()
    end
end
main(ARGS)
