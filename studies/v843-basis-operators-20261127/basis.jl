module V843BasisDiagnostics

using LinearAlgebra
using QCLNEGF
using Unitful

include(joinpath(@__DIR__, "..", "fath-v843", "controls", "v843-input", "dupont", "dupont_device.jl"))
const N = QCLNEGF.QCLNumerics
const REFERENCE = QCLNEGF.QCLReferenceOperators
const RANKS = (6, 7, 8, 9, 11)
const NEAR_GROUP_MEV = 2.0

function inputs(nz, half_window; field=21.0)
    device = DupontDevice.physical_inputs(field)
    numerical = NumericalParameters(N_z=nz, N_b=7, P_basis=half_window,
        E_min=-650u"meV", E_max=1000u"meV", N_E=239, M_E=390u"meV",
        k_max=0.6u"nm^-1", N_k=17, N_φ=32, qz_max=10u"nm^-1", N_qz=161, η_seed=0.5u"meV")
    scale = ScaleSystem()
    grid = build_grids(device.physical, numerical, scale)
    profiles = DupontDevice.sheet_profiles(device.physical, numerical, scale, grid, device.donor_center)
    return (; device.physical, numerical, scale, grid, profiles)
end

function operator(data, periods; boundary=:dirichlet)
    dz = first(data.grid.wˣ)
    Ec = repeat(data.profiles.Eᶜ, periods)
    mass = repeat(data.profiles.mᶻᵣ, periods)
    return build_bdd_hamiltonian(Ec, mass, dz, REFERENCE._C̄(data.scale); boundary)
end

matrix_rows(a) = [collect(row) for row in eachrow(a)]

function shifted_shape_comparisons(Φwin, energies, rank, nz, periods, central)
    first_rows = 1:(size(Φwin, 1) - nz)
    second_rows = (nz + 1):size(Φwin, 1)
    results = Dict{String,Any}[]
    for pair in 1:(periods - 1)
        a = ((pair - 1) * rank + 1):(pair * rank)
        b = (pair * rank + 1):((pair + 1) * rank)
        first = @view Φwin[first_rows, a]
        second = @view Φwin[second_rows, b]
        retained_a = vec(sum(abs2, first; dims=1))
        retained_b = vec(sum(abs2, second; dims=1))
        # The finite-coordinate window is cropped before normalizing each column.
        A = first ./ sqrt.(transpose(retained_a))
        B = second ./ sqrt.(transpose(retained_b))
        overlap = A' * B
        groups = Dict{String,Any}[]
        start = 1
        for finish in 1:rank
            near = finish < rank && min(abs(energies[a[finish + 1]] - energies[a[finish]]),
                                         abs(energies[b[finish + 1]] - energies[b[finish]])) <= NEAR_GROUP_MEV
            near && continue
            if finish > start
                ix = start:finish
                Ua = qr(A[:, ix]).Q[:, 1:length(ix)]
                Ub = qr(B[:, ix]).Q[:, 1:length(ix)]
                push!(groups, Dict("modes"=>collect(ix), "projector_overlap_singular_values"=>svdvals(Ua' * Ub)))
            end
            start = finish + 1
        end
        Ua = qr(A).Q[:, 1:rank]
        Ub = qr(B).Q[:, 1:rank]
        push!(results, Dict(
            "left_period"=>pair - central, "right_period"=>pair + 1 - central,
            "left_retained_norm_squared"=>retained_a, "right_retained_norm_squared"=>retained_b,
            "overlap_real"=>matrix_rows(real.(overlap)), "overlap_imag"=>matrix_rows(imag.(overlap)),
            "projector_overlap_singular_values"=>svdvals(Ua' * Ub), "near_groups"=>groups,
        ))
    end
    return results
end

function evaluate_rank(data, Hwin, diagonalization, rescale, half_window, rank)
    nz = data.numerical.N_z
    period_count = 2half_window + 1
    central = half_window + 1
    nsub = rank * period_count
    xnm = 1e9 * data.scale.L₀_m
    emeV = 1e3 * data.scale.E₀_eV
    dz = first(data.grid.wˣ)
    physical = N._scaled_physics(data.physical, data.scale)

    # Same contiguous low-energy spectral subspace and PzP as Core.
    C = ComplexF64.(diagonalization.vectors[:, 1:nsub])
    x = [(g - 0.5) * dz for g in 1:size(Hwin, 1)]
    Z = C' * (reshape(x, :, 1) .* C)
    local_diag = eigen(Hermitian((Z + Z') / 2))
    order = sortperm(local_diag.values)
    centers = local_diag.values[order]
    Φwin = C * local_diag.vectors[:, order]
    REFERENCE._phase_fix!(Φwin)
    center_table = reshape(centers, rank, period_count)
    displacements = diff(center_table; dims=2) .- physical.Lp
    distance = abs.(displacements) ./ physical.Lp
    trans, worst = findmax(distance)
    central_nearest = maximum(distance[:, central])
    central_two = maximum(distance[:, central:(central + 1)])
    edges = maximum(distance[:, [1, end]])
    HΦ = Hwin * Φwin
    mode_energies = emeV .* [real(dot(view(Φwin, :, j), view(HΦ, :, j))) for j in 1:nsub]
    eigenvalues = diagonalization.values[1:nsub] .* rescale
    residual = Hwin * C - C .* transpose(eigenvalues)
    hnorm = maximum(abs, diagonalization.values) * rescale
    eigen_residual = maximum(norm(view(residual, :, j)) /
        (hnorm + abs(eigenvalues[j])) for j in 1:nsub)
    rows = (half_window*nz + 1):(central*nz)
    cols = (half_window*rank + 1):(central*rank)
    B = Matrix(Φwin[rows, cols])
    metric = B' * B
    overlap = eigen(Hermitian((metric + metric') / 2))
    smin, smax = extrema(overlap.values)
    result = Dict{String,Any}(
        "rank"=>rank, "p_basis"=>half_window, "translation"=>trans, "translation_nearest"=>central_nearest,
        "translation_two_pairs"=>central_two, "edge_pairs_translation"=>edges,
        "translation_per_pair"=>vec(maximum(distance; dims=1)),
        "worst_mode"=>worst[1], "worst_left_period"=>worst[2]-central,
        "worst_right_period"=>worst[2]+1-central, "worst_signed_displacement_nm"=>xnm*displacements[worst],
        "centers_nm_by_period"=>[xnm .* collect(c) for c in eachcol(center_table)],
        "localized_energy_meV_by_period"=>[collect(c) for c in eachcol(reshape(mode_energies, rank, period_count))],
        "window_spectrum_meV"=>emeV .* eigenvalues, "window_eigen_residual"=>eigen_residual,
        "neighbor_shapes"=>shifted_shape_comparisons(Φwin, mode_energies, rank, nz, period_count, central),
        "cell_metric_eigenvalues"=>collect(overlap.values),
        "static_pass"=>false, "status"=>"inconclusive",
    )
    if smin <= 0 || smin <= 100eps(Float64)*smax || smax/smin > 1e8
        result["reason"] = "Cell overlap is singular or ill-conditioned under the Core rule"
        return result
    end

    # Lowdin and biased central Hamiltonian match Core project_hamiltonians at k=0, U_H=0.
    inverse_sqrt = overlap.vectors * Diagonal(1 ./ sqrt.(overlap.values)) * overlap.vectors'
    Φ = ComplexF64.(B * inverse_sqrt)
    REFERENCE._phase_fix!(Φ)
    hcell = Matrix(Hwin[rows, rows])
    h0 = Φ' * hcell * Φ
    position = Φ' * Diagonal(data.grid.x) * Φ
    h_f = h0 - physical.F * (position - physical.z₀ * I)
    biased = eigen(Hermitian((h_f + h_f') / 2))
    ψ = Φ * biased.vectors
    REFERENCE._phase_fix!(ψ)
    maximum(abs, imag.(ψ)) <= 1e-9 || error("real BDD problem produced non-real central orbitals beyond roundoff")
    result["x_nm"] = data.grid.x .* xnm
    result["wavefunctions"] = [real.(collect(col)) for col in eachcol(ψ)]
    result["density_profiles"] = [abs2.(collect(col)) ./ (dz*xnm) for col in eachcol(ψ)]
    result["energies_meV"] = emeV .* biased.values
    result["orthogonality"] = norm(Φ' * Φ - I)
    result["static_pass"] = trans <= N._PZP_TRANSLATION_LIMIT &&
        central_nearest <= N._PZP_TRANSLATION_LIMIT && central_two <= N._PZP_TWO_PAIR_LIMIT &&
        result["orthogonality"] <= N._STRUCTURAL_VALIDATION_LIMITS[:basis_orthogonality] &&
        eigen_residual <= N._STRUCTURAL_VALIDATION_LIMITS[:basis_eigen]
    result["status"] = "measured"
    return result
end

function run(task, args)
    half_windows = Dict("B7"=>3, "B9"=>4, "B11"=>5)
    half_window = half_windows[task]
    fixture = args == ["fixture"]
    isempty(args) || fixture || error("basis arguments must be empty or fixture")
    nz = fixture ? 24 : 144
    BLAS.set_num_threads(parse(Int,get(ENV,"QCL_SLOT_CPUS","1")))
    data = inputs(nz, half_window)
    periods = 2half_window + 1
    H = operator(data, periods)
    rescale = maximum(abs, diag(H))
    diagonalization = eigen(Hermitian(H / rescale))
    ranks = fixture ? (7,) : RANKS
    candidates = [evaluate_rank(data, H, diagonalization, rescale, half_window, rank) for rank in ranks]
    result = Dict{String,Any}("task"=>task, "status"=>"measured", "spatial_nodes"=>nz,
        "window_periods"=>periods, "p_basis"=>half_window, "field_kV_cm"=>21.0, "fixture"=>fixture,
        "near_group_threshold_meV"=>NEAR_GROUP_MEV, "blas_threads"=>BLAS.get_num_threads(),
        "period_nm"=>1e9*data.scale.L₀_m*N._scaled_physics(data.physical,data.scale).Lp, "candidates"=>candidates,
        "probability_units"=>"nm^-1", "wavefunction_metric"=>"unit Euclidean norm per central-cell state")
    if task == "B7" && !fixture
        value = only(filter(x -> x["rank"] == 7, candidates))["translation"]
        result["baseline_published_rounded"] = 0.162285
        result["baseline_reproduced"] = round(value; digits=6) == 0.162285
        if !result["baseline_reproduced"]
            result["status"] = "inconclusive"
            result["reason"] = "Published six-digit baseline did not reproduce"
        end
    end
    return result
end

end # module

run_basis(task::String, args::Vector{String}) = V843BasisDiagnostics.run(task, args)
