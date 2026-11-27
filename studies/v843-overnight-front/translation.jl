# Full-window PzP translation diagnostic; no transport or private HOP reconstruction.
using LinearAlgebra, QCLNEGF, Unitful, TOML, SHA
include(joinpath(@__DIR__, "../fath-v843/controls/v843-input/dupont/dupont_device.jl"))
const NUM = QCLNEGF.QCLNumerics
const REF = QCLNEGF.QCLReferenceOperators

function translate_zero(W, n, direction)
    out = zero(W)
    if direction == 1
        out[n+1:end, :] .= W[1:end-n, :]
    else
        out[1:end-n, :] .= W[n+1:end, :]
    end
    out
end

# All overlaps use the same full-window Euclidean metric (Core's transform
# incorporates sqrt(dx)); whitening reports the effect of clipping separately.
function orthonormalize(A)
    f = eigen(Hermitian(A' * A))
    minimum(f.values) > 1e-12 || error("translated/restricted frame lost rank")
    A * f.vectors * Diagonal(1 ./ sqrt.(f.values)) * f.vectors', f.values
end

function main()
    length(ARGS) == 4 || error("Usage: julia --project=runner translation.jl B RANK NZ OUTPUT.toml")
    B, rank, nz = parse.(Int, ARGS[1:3])
    isodd(B) && B >= 3 || error("B must be odd and at least 3")
    1 <= rank <= nz || error("RANK must be between 1 and NZ")
    !ispath(ARGS[4]) || error("output already exists")
    manifest_path = normpath(joinpath(@__DIR__, "../../runner/Manifest.toml"))
    core_record = only(TOML.parsefile(manifest_path)["deps"]["QCLNEGF"])
    core_record["repo-rev"] == "0eba158d21148e0cb3f8c4dae31195aad1f2a43d" || error("Core manifest revision differs")
    core_basis_path = joinpath(dirname(pathof(QCLNEGF)), "numerics/reference/basis.jl")
    core_basis_sha = bytes2hex(open(sha256, core_basis_path))
    core_basis_sha == "423b8e6716afd47a188de53e0633d3cbd9da8001db842c82e2f8a53ef013f350" || error("loaded Core basis source differs")
    inputs = DupontDevice.physical_inputs(21.0)
    p, s = inputs.physical, ScaleSystem()
    n = NumericalParameters(N_z=nz, N_b=rank, P_basis=(B-1)÷2,
        E_min=-0.65u"eV", E_max=1.0u"eV", N_E=121, M_E=0.39u"eV",
        k_max=0.6u"nm^-1", N_k=17, N_φ=32, qz_max=10.0u"nm^-1",
        N_qz=161, η_seed=0.5u"meV")
    grids = build_grids(p,n,s)
    profiles = DupontDevice.sheet_profiles(p,n,s,grids,inputs.donor_center)
    basis = QCLNEGF.build_multiperiod_reference_basis(p,n,s,grids,profiles; localization=:pzp_tails)
    W = basis.transform[:, basis.central_columns]
    z_nm = basis.coordinates .* (s.L₀_m * 1e9)
    field = ustrip(u"V/nm",p.F_bias)
    drop = 0.075936
    @assert isapprox(field * 36.16,drop; atol=1e-12)
    # H in eV: Core's BDD kinetic + conduction band, actual linear field,
    # and parabolic k-dependent kinetic energy with layer-dependent mass.
    h0 = basis.real_space_hamiltonian .* s.E₀_eV +
        Diagonal(ustrip(u"eV",p.E_ref) .- field .* (z_nm .- ustrip(u"nm",p.z₀)))
    kin = REF._C̄(s) * s.E₀_eV * (s.L₀_m * 1e9)^2 ./ repeat(profiles.m_parallelᵣ,B)
    ks = collect(range(0.0,0.6; length=17))
    output = Dict{String,Any}(
        "schema"=>"v843-full-window-translation-v1", "periods"=>B, "rank"=>rank,
        "nodes_per_period"=>nz, "field_kV_cm"=>21.0, "drop_eV"=>drop,
        "k_nm_inverse"=>ks, "localization"=>"pzp_tails", "boundary"=>"dirichlet",
        "metric"=>"Core transform Euclidean metric on the same full window; translated tails zero-filled",
        "interpretation"=>"Independent neighboring PzP columns versus translated central columns. No claim of reproducing private HOP.",
        "core_subspace_residual"=>basis.subspace_residual,
        "core_required_revision"=>core_record["repo-rev"],
        "core_manifest_tree_sha1"=>core_record["git-tree-sha1"],
        "core_basis_sha256"=>core_basis_sha,
        "runner_manifest_sha256"=>bytes2hex(open(sha256,manifest_path)),
        "julia_version"=>string(VERSION),
        "operator_scope"=>"Hartree zero; parabolic transverse dispersion; no scattering or transport",
        "energy_zero"=>"E_ref=0 eV, potential -F*(z-z0); pzp_tails real_space_hamiltonian is zero-field",
        "donor_profile"=>"sheet profile; no effect on this zero-Hartree Hamiltonian",
        "driver_sha256"=>bytes2hex(open(sha256,@__FILE__)),
        "device_sha256"=>bytes2hex(open(sha256,DupontDevice.DEFAULT_DEVICE)),
        "pairs"=>Dict{String,Any}())
    for d in (-1,1)
        cols = (first(basis.central_columns)+d*rank):(last(basis.central_columns)+d*rank)
        V = basis.transform[:,cols]
        T = translate_zero(W,nz,d)
        Q, gram = orthonormalize(T)
        S = svd(Q' * V)
        # Rotate V into the Q gauge by the polar factor of Q'V.
        Va = V * S.V * S.U'
        vals = Vector{Dict{String,Any}}()
        for k in ks
            H = h0 + Diagonal(k^2 .* kin)
            hc, ht, hv = W' * H * W, Q' * H * Q, Va' * H * Va
            delta = hv - ht
            # Compare covariance against the field-shifted central H.
            covariance = ht - (hc - d*drop*I)
            push!(vals, Dict("k_nm_inverse"=>k,
                "translated_energies_eV"=>eigvals(Hermitian(ht)),
                "neighbor_energies_eV"=>eigvals(Hermitian(hv)),
                "central_energies_eV"=>eigvals(Hermitian(hc)),
                "paired_H_residual_eV_frobenius"=>norm(delta),
                "paired_H_relative_residual"=>norm(delta)/max(norm(ht),eps()),
                "translation_covariance_residual_eV_frobenius"=>norm(covariance),
                "translation_covariance_relative_residual"=>norm(covariance)/max(norm(hc),eps())))
        end
        output["pairs"][d == -1 ? "minus" : "plus"] = Dict(
            "direction_periods"=>d, "retained_gram_eigenvalues"=>gram,
            "lost_probability_per_column"=>vec(1 .- sum(abs2,T;dims=1)),
            "principal_singular_values"=>S.S,
            "absolute_overlap_frobenius"=>norm(Q' * V),
            "absolute_overlap_rows"=>[collect(row) for row in eachrow(abs.(Q' * V))],
            "k_results"=>vals)
    end
    open(ARGS[4],"w") do io
        TOML.print(io,output)
    end
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
