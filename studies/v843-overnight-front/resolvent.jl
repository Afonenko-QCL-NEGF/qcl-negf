using LinearAlgebra, SHA, TOML, Unitful
using QCLNEGF
import QCLNEGFRunner

# A(E) = -Im <v|(E+iη-H)^-1|v>/π, in 1/eV for unit-norm v.
# The coordinate calculation uses a tridiagonal factorization at each E;
# the Galerkin calculation uses one small Hermitian eigensolve per k.
function responses(diag_h, off_h, U, probes, energies, eta)
    n = length(diag_h)
    length(off_h) == n-1 || error("bad tridiagonal dimensions")
    H = SymTridiagonal(diag_h, off_h)
    projected = Hermitian(U' * (H * U))
    eig = eigen(projected)
    coeff = eig.vectors' * (U' * probes)
    weights = abs2.(coeff)
    direct = zeros(length(energies), size(probes, 2))
    reduced = similar(direct)
    blas_threads = BLAS.get_num_threads()
    try
        BLAS.set_num_threads(1)
        Threads.@threads :dynamic for i in eachindex(energies)
            E = energies[i]
            z = complex(E, eta)
            T = Tridiagonal(complex.(-off_h), z .- diag_h, complex.(-off_h))
            solved = T \ probes
            for j in axes(probes, 2)
                direct[i,j] = -imag(dot(view(probes,:,j), view(solved,:,j))) / π
                reduced[i,j] = sum(weights[:,j] .* (eta ./ ((E .- eig.values).^2 .+ eta^2))) / π
            end
        end
    finally
        BLAS.set_num_threads(blas_threads)
    end
    return direct, reduced
end

function selftest()
    d = [-0.03, 0.02, 0.08]; o = [-0.01, -0.015]
    U = Matrix{Float64}(I, 3, 3); P = U[:,1:2]
    a, b = responses(d, o, U, P, range(-0.1, 0.12; length=21), 0.003)
    @assert maximum(abs.(a-b)) < 1e-10
    @assert minimum(a) >= 0
    println("selftest passed: complete-basis response and positivity")
end

function main(args)
    args == ["--selftest"] && return selftest()
    length(args) == 7 || error("usage: resolvent.jl WINDOW RANK NZ ETA_MEV NK NE OUTPUT.toml")
    window, rank, nz = parse.(Int, args[1:3])
    eta = parse(Float64, args[4]) / 1000
    nk, ne = parse.(Int, args[5:6]); output = args[7]
    window >= 3 && isodd(window) && 1 <= rank < nz && eta > 0 && nk >= 2 && ne >= 3 || error("invalid parameters")
    !ispath(output) || error("output exists")
    # Set JULIA_NUM_THREADS to the local Runner CPU allocation before starting.
    # Dense basis/eigen stages use that allocation, never an implicit BLAS default.
    BLAS.set_num_threads(Threads.nthreads())
    BLAS.get_num_threads() <= Threads.nthreads() || error("BLAS exceeds Julia CPU allocation")
    study = normpath(joinpath(@__DIR__, "..", "v843-spectrum", "b7.yaml"))
    manifest_path = normpath(joinpath(@__DIR__, "..", "..", "runner", "Manifest.toml"))
    core_record = only(TOML.parsefile(manifest_path)["deps"]["QCLNEGF"])
    core_record["repo-rev"] == "0eba158d21148e0cb3f8c4dae31195aad1f2a43d" || error("Core manifest revision differs")
    core_basis = joinpath(dirname(pathof(QCLNEGF)), "numerics", "reference", "basis.jl")
    core_basis_sha = bytes2hex(open(sha256, core_basis))
    core_basis_sha == "423b8e6716afd47a188de53e0633d3cbd9da8001db842c82e2f8a53ef013f350" || error("loaded Core basis source differs")
    plan = QCLNEGFRunner.resolve_scientific_plan(study; maximum_solver_runs=1)
    execution, point = only(plan.executions), only(plan.points)
    workflow = QCLNEGFRunner.QCLScientificWorkflow
    raw = workflow._point_resolved_raw(execution.configuration, point)
    c = QCLNEGFRunner._resolve_configuration(raw, execution.configuration.provenance)
    p, s = c.physical, c.scales
    fields = Dict(name => getfield(c.numerical, name) for name in fieldnames(NumericalParameters))
    fields[:N_z] = nz; fields[:N_b] = rank; fields[:P_basis] = (window-1) ÷ 2
    n = NumericalParameters(; fields...)
    @assert isapprox(ustrip(u"kV/cm", p.F_bias), 21.0)
    @assert point.temperature_K == point.lo_temperature_K == 50.0
    grids = build_grids(p, n, s); profiles = build_profiles(p, n, s, grids)
    basis = QCLNEGF.build_multiperiod_reference_basis(p, n, s, grids, profiles; localization=:pzp_tails)
    U = basis.transform
    @assert norm(U' * U - I) < 1e-9
    z_nm = basis.coordinates .* (s.L₀_m * 1e9)
    central = U[:, basis.central_columns]
    # Identical physical probe for different windows and retained ranks; the
    # density has sigma=2 nm, centred at the middle of the central period.
    centre_nm = (first(z_nm[basis.central_rows]) + last(z_nm[basis.central_rows])) / 2
    sigma_nm = 2.0
    gaussian = exp.(-((z_nm .- centre_nm).^2) ./ (4sigma_nm^2))
    gaussian ./= norm(gaussian)
    probes = hcat(central, gaussian)
    projected_norms = vec(sum(abs2, U' * probes; dims=1))
    H0 = basis.real_space_hamiltonian .* s.E₀_eV
    d0 = real.(diag(H0)) .+ ustrip(u"eV", p.E_ref) .- ustrip(u"V/nm", p.F_bias) .* (z_nm .- ustrip(u"nm", p.z₀))
    off = real.(diag(H0,1))
    # Fail closed if the assumed Dirichlet BDD structure changes.
    tridiag = SymTridiagonal(real.(diag(H0)), off)
    norm(H0-tridiag) <= 1e-12 * max(norm(H0), 1.0) || error("BDD is not real symmetric tridiagonal")
    invmass = repeat(1 ./ profiles.m_parallelᵣ, window)
    energies = collect(range(-0.060, 0.120; length=ne))
    ks = collect(range(0.0, 0.6; length=nk))
    cases = Dict{String,Any}[]
    for k in ks
        transverse = QCLNEGF._C̄(s) * (k*s.L₀_m*1e9)^2 * s.E₀_eV
        direct, reduced = responses(d0 .+ transverse .* invmass, off, U, probes, energies, eta)
        delta = reduced-direct
        push!(cases, Dict("k_nm_inverse"=>k,
            "relative_l2"=>norm(delta)/max(norm(direct), eps()),
            "maximum_absolute_per_eV"=>maximum(abs,delta),
            "probes"=>[Dict("column"=>j, "kind"=>j <= rank ? "central_pzp" : "fixed_gaussian",
                            "projected_weight"=>projected_norms[j],
                            "coordinate_per_eV"=>direct[:,j],
                            "galerkin_per_eV"=>reduced[:,j]) for j in 1:(rank+1)]))
    end
    report = Dict("schema"=>"v843-finite-window-resolvent-v1", "status"=>"finite-window-diagnostic",
        "scope"=>"Dirichlet BDD, Hartree zero, parabolic transverse dispersion; no scattering, transport or stationary state",
        "normalization"=>"A=-Im(v' G^R v)/pi per eV; same unit-normalized physical probe in both solves; Galerkin projection is not renormalized",
        "gaussian"=>Dict("density_sigma_nm"=>sigma_nm, "centre_nm"=>centre_nm,
                         "centre_definition"=>"midpoint of first and last central-period grid nodes"),
        "energy_zero"=>"E_ref=0 eV with -F*(z-z0), as domain-control.jl", "eta_meV"=>eta*1000,
        "window_periods"=>window, "rank_per_period"=>rank, "nodes_per_period"=>nz,
        "energy_eV"=>energies, "cases"=>cases, "source_plan_fingerprint"=>plan.fingerprint,
        "core_required_revision"=>"0eba158d21148e0cb3f8c4dae31195aad1f2a43d",
        "core_manifest_tree_sha1"=>core_record["git-tree-sha1"], "core_basis_sha256"=>core_basis_sha,
        "runner_manifest_sha256"=>bytes2hex(open(sha256, manifest_path)),
        "driver_sha256"=>bytes2hex(open(sha256, @__FILE__)),
        "julia_version"=>string(VERSION), "central_probe_orthogonality_error"=>norm(central' * central-I),
        "gaussian_norm"=>norm(gaussian),
        "julia_threads"=>Threads.nthreads(), "blas_threads_basis_and_projected_eigen"=>BLAS.get_num_threads(),
        "parallel_policy"=>"k sequential; independent energy rows dynamically threaded with BLAS=1; original BLAS restored for each k eigensolve",
        "basis_orthogonality_error"=>norm(U' * U-I))
    open(output, "w") do io; TOML.print(io, report); end
end

if abspath(PROGRAM_FILE) == @__FILE__
    main(ARGS)
end
