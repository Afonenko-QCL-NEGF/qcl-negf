include(joinpath(@__DIR__, "native.jl"))
using QCLNEGF: AlgorithmOptions, ProductionOptions, estimate_production_memory


# Calculate a size estimate only. This reproduces the frozen
# declared 4801-energy / 25-momentum-node diagnostic choices, with Nb varied.
function memory_estimate()
    algorithms = AlgorithmOptions(kernel_build=:direct, embedding=:finite_chain,
        embedding_periods=4, mixing=:linear, energy_shift=:sparse_plan,
        hilbert=:product_integration, elastic_retarded=:direct_green)
    opts = ProductionOptions(algorithms=algorithms, worker_count=12, hilbert_columns=1,
        parallel_backend=:threads, verify_fft_roundoff=true, phase_timing=true,
        memory_budget_bytes=15*1024^3, checkpoint_every_scba=0,
        checkpoint_every_outer=0, progress_every_scba=1)
    rows = []
    scales = ScaleSystem()
    p = make_physical(149, 54)
    for nb in (5, 7, 9, 12, 16)
        n = NumericalParameters(N_z=144, N_b=nb, P_basis=3,
            E_min=-0.4u"eV", E_max=0.56u"eV", N_E=4801, M_E=0.26u"eV",
            k_max=0.6u"nm^-1", N_k=25, N_φ=32, qz_max=10u"nm^-1",
            N_qz=81, η_seed=0.5u"meV")
        grids = build_grids(p, n, scales)
        estimate = estimate_production_memory(n, 5; dense_mechanism_count=5, options=opts,
            worker_capacity=12, energy_nodes=grids.ε)
        push!(rows, Dict("nb"=>nb, "peak_bytes"=>estimate.peak_bytes,
                        "field_bytes"=>16*n.N_E*n.N_k*n.N_b^2))
    end
    return rows
end

function scan()
    length(ARGS) >= 1 || error("usage: scan_native.jl scan|refine [Nb:P_basis ...]")
    mode = first(ARGS)
    if mode == "scan"
        @assert length(ARGS) == 1
        nz = 144
        pairs = [(nb, half_window) for half_window in 1:5 for nb in 5:16]
    elseif mode == "refine"
        nz = 192
        pairs = [Tuple(parse.(Int, split(arg, ':'))) for arg in ARGS[2:end]]
        @assert !isempty(pairs)
    else
        error("unsupported scan mode")
    end
    cbo = 149.0
    p = make_physical(cbo)
    s = ScaleSystem()
    n = make_numerical(nz, 7)
    grids = build_grids(p, n, s)
    profiles = build_profiles(p, n, s, grids)
    records = []
    started = time()
    for (nb, half_window) in pairs
        row = try
            basis_record(cbo, nz, nb, half_window, p, grids, profiles, s)
        catch err
            err isa ArgumentError || rethrow()
            Dict(
                "nb" => nb, "basis_half_window" => half_window,
                "error" => sprint(showerror, err),
            )
        end
        push!(records, row)
    end
    output = Dict(
        "core_commit" => INPUT["core_commit"], "cbo_mev" => cbo, "nz" => nz,
        "julia_threads" => Threads.nthreads(), "blas_threads" => BLAS.get_num_threads(),
        "elapsed_seconds" => time() - started, "records" => records,
    )
    if mode == "refine"
        output["transport_memory_size_only"] = memory_estimate()
    end
    open(joinpath(HERE, "native_$mode.toml"), "w") do file
        TOML.print(file, output; sorted=true)
    end
end

scan()
