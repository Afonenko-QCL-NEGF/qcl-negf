using LinearAlgebra, TOML, Unitful
import QCLNEGF as Q

BLAS.set_num_threads(1)
@assert Threads.nthreads() == BLAS.get_num_threads() == 1
passport = TOML.parsefile(joinpath(@__DIR__,"passport.toml"))
core = dirname(dirname(pathof(Q)))
@assert readchomp(`git -C $core rev-parse HEAD`) == passport["core_commit"]
@assert readchomp(`git -C $core rev-parse $("HEAD^{tree}")`) == passport["core_tree"]
@assert isempty(readchomp(`git -C $core status --porcelain --untracked-files=no`))
alg = Q.AlgorithmOptions(kernel_build=:direct, energy_shift=:sparse_plan, hilbert=:product_integration,
    elastic_retarded=:direct_green, embedding=:finite_chain, embedding_periods=4,
    occupation_normalization=:paired_convex)
function memory_row(label, nz, nb, ne, nk, upper; workers=12)
    opts = Q.ProductionOptions(algorithms=alg,worker_count=workers,hilbert_columns=1,
        parallel_backend=:threads,verify_fft_roundoff=true,memory_budget_bytes=15*1024^3)
    n = Q.NumericalParameters(
        N_z=nz,N_b=nb,P_basis=3,N_E=ne,N_k=nk,N_φ=32,N_qz=81,
        E_min=-400u"meV",E_max=upper*u"meV",M_E=260u"meV",
        k_max=0.60u"nm^-1",qz_max=10u"nm^-1",η_seed=0.5u"meV",
    )
    ε = collect(range(-4.0,upper/100;length=ne))
    planned = Q.estimate_production_memory(n,5;dense_mechanism_count=5,
        options=opts,worker_capacity=workers,energy_nodes=ε)
    expected = Q.estimate_production_memory(n,5;dense_mechanism_count=3,
        options=opts,worker_capacity=workers,energy_nodes=ε)
    return Dict("name"=>label,"nz"=>nz,"nb"=>nb,"ne"=>ne,"nk"=>nk,"upper_mev"=>upper,
        "delta_mev"=>(upper+400)/(ne-1),"workers"=>workers,"preflight_peak_gib"=>planned.peak_bytes/1024^3,
        "expected_dense3_peak_gib"=>expected.peak_bytes/1024^3,
        "within_15gib_campaign_budget"=>planned.peak_bytes<=opts.memory_budget_bytes,
        "expected_kernel_flops_per_candidate_dense3"=>expected.kernel_flops_per_candidate,
        "field_gib"=>16*ne*nk*nb^2/1024^3)
end

rows = [memory_row("native-pzp7-original",144,7,4801,25,560),
        memory_row("native-pzp7-pair",144,7,2401,17,560)]
for nk in (13,17)
    push!(rows,memory_row("pod7-r9-compact-grid",192,9,4001,nk,4200))
    push!(rows,memory_row("pod7-r9-resolved-grid",192,9,11001,nk,4000))
    push!(rows,memory_row("pod8-r10-resolved-grid",192,10,13001,nk,4800))
    push!(rows,memory_row("pod5-core7-cell-r9-resolved-grid",192,9,9501,nk,3400))
    push!(rows,memory_row("pod7-core9-cell-r12-resolved-grid",192,12,11126,nk,4050))
end
for workers in (8,12), nk in (9,13,17)
    push!(rows,memory_row("pod7-r9-Nz144-E4000",144,9,11001,nk,4000;workers))
end
for row in rows
    row["flops_vs_original_native"] = row["expected_kernel_flops_per_candidate_dense3"]/
        rows[1]["expected_kernel_flops_per_candidate_dense3"]
    row["flops_vs_compact_native_pair"] = row["expected_kernel_flops_per_candidate_dense3"]/
        rows[2]["expected_kernel_flops_per_candidate_dense3"]
end
open(io->TOML.print(io,Dict("core_commit"=>passport["core_commit"],
    "e171_preflight_only"=>true,"rows"=>rows);sorted=true),
    joinpath(@__DIR__,"preflight.toml"),"w")
