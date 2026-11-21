using SparseArrays: sparse

"""Sparse storage of the Core's weighted finite-volume shift pair."""
function campaign_conservative_shift_pair(axis, weights, displacement)
    n = length(axis)
    n ≥ 2 && length(weights) == n || throw(DimensionMismatch("energy nodes and weights differ"))
    all(isfinite, axis) && all(>(0), diff(axis)) && isfinite(displacement) ||
        throw(ArgumentError("invalid energy axis or displacement"))
    edges = vcat(first(axis), (axis[1:end-1] + axis[2:end]) / 2, last(axis))
    widths = diff(edges)
    tolerance = 32eps(Float64) * max(maximum(abs, axis), last(axis) - first(axis))
    all(isfinite, weights) && all(>(0), weights) &&
        all(abs.(weights - widths) .≤ tolerance .+ 32eps(Float64) .* widths) ||
        throw(ArgumentError("weights must equal the trapezoidal cell widths"))

    destinations = Int[]
    sources = Int[]
    overlaps = Float64[]
    first_source = 1
    for destination in eachindex(axis)
        left_edge = edges[destination] + displacement
        right_edge = edges[destination+1] + displacement
        while first_source ≤ n && edges[first_source+1] ≤ left_edge
            first_source += 1
        end
        source = first_source
        while source ≤ n && edges[source] < right_edge
            overlap = min(edges[source+1], right_edge) - max(edges[source], left_edge)
            if overlap > 0
                push!(destinations, destination)
                push!(sources, source)
                push!(overlaps, overlap)
            end
            source += 1
        end
    end

    plus_coefficients = overlaps ./ weights[destinations]
    minus_coefficients = overlaps ./ weights[sources]
    plus = sparse(destinations, sources, plus_coefficients, n, n)
    minus = sparse(sources, destinations, minus_coefficients, n, n)
    return (; plus, minus)
end

"""Attach weighted conservative shifts to an already retargeted Core problem."""
function campaign_conservative_problem(core, problem)
    axis, weights = problem.grids.ε, problem.grids.wᴱ
    scales = core._scaled_physics(problem.physical, problem.scales)
    field = campaign_conservative_shift_pair(axis, weights, scales.Eᵖ)
    lo = campaign_conservative_shift_pair(axis, weights, scales.ħωᴸᴼ)
    return core.NEGFProblem(
        problem.physical, problem.numerical, problem.scattering, problem.scales,
        problem.grids, problem.profiles, problem.basis, problem.kernels,
        field.plus, field.minus, lo.plus, lo.minus,
        :finite_volume_piecewise_constant, problem.models,
    )
end
