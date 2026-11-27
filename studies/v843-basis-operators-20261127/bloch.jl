if !isdefined(@__MODULE__, :V843BasisDiagnostics)
    include(joinpath(@__DIR__, "basis.jl"))
end

module V843BlochDiagnostics

using LinearAlgebra
using ..V843BasisDiagnostics: inputs, operator

const TRACKED_BANDS = 11
const GAP_TOLERANCE_MEV = 0.01
const PROJECTOR_GROUP_MEV = 0.10
const PHASE_TOLERANCE = π/1024
const MAX_REFINEMENTS = 8

function sample!(samples, phases, cell, forward, energy_meV)
    missing = unique(filter(phase -> !haskey(samples, phase), phases))
    new_samples = Vector{Tuple{Vector{Float64},Matrix{ComplexF64}}}(undef, length(missing))
    Threads.@threads for j in eachindex(missing)
        phase_factor = cis(missing[j])
        coupled = cell + phase_factor * forward + conj(phase_factor) * forward'
        result = eigen(Hermitian(coupled), 1:(TRACKED_BANDS + 1))
        new_samples[j] = (energy_meV .* result.values, result.vectors)
    end
    for (phase, sample) in zip(missing, new_samples)
        samples[phase] = sample
    end
    return nothing
end

direct_gap7(samples, phase) = samples[phase][1][8] - samples[phase][1][7]

function refine_minimum!(samples, cell, forward, energy_meV; max_refinements)
    refinements = Dict{String,Any}[]
    stable = false
    consecutive = 0
    for iteration in 0:max_refinements
        phases = sort!(collect(keys(samples)))
        gaps = [direct_gap7(samples, phase) for phase in phases]
        best, i = findmin(gaps)
        neighbors = Float64[]
        if i > 1
            push!(neighbors, phases[i]-phases[i-1])
        end
        if i < length(phases)
            push!(neighbors, phases[i+1]-phases[i])
        end
        bracket_step = maximum(neighbors)
        row = Dict{String,Any}("refinement"=>iteration, "gap_meV"=>best, "phase_rad"=>phases[i],
            "max_neighbor_step_rad"=>bracket_step, "phase_count"=>length(phases))
        if !isempty(refinements)
            delta = abs(best - last(refinements)["gap_meV"])
            row["gap_change_meV"] = delta
            consecutive = delta <= GAP_TOLERANCE_MEV ? consecutive + 1 : 0
        end
        push!(refinements, row)
        if consecutive >= 2 && bracket_step <= PHASE_TOLERANCE
            stable = true
            break
        end
        iteration == max_refinements && break

        additions = Float64[]
        # Refine each sampled local minimum within the predetermined ambiguity
        # band of the best gap. The ±π endpoints are the same Bloch boundary.
        for j in eachindex(phases)
            jm = j == 1 ? length(phases)-1 : j-1
            jp = j == length(phases) ? 2 : j+1
            gaps[j] <= min(gaps[jm],gaps[jp]) + 1e-10 || continue
            gaps[j] <= best + PROJECTOR_GROUP_MEV || continue
            j > 1 && push!(additions, (phases[j-1]+phases[j])/2)
            j < length(phases) && push!(additions, (phases[j]+phases[j+1])/2)
        end
        isempty(additions) && error("Gap refinement lost the sampled minimum")
        sample!(samples, additions, cell, forward, energy_meV)
    end
    return refinements, stable
end

function overlap_assignment(scores)
    # Exact maximum-weight assignment for the 11 tracked modes.
    count = size(scores,1)
    states = 1 << count
    totals = fill(-Inf, states)
    last_column = zeros(Int, states)
    totals[1] = 0.0
    for mask in 0:(states-2)
        row = count_ones(mask)+1
        for column in 1:count
            bit = 1 << (column-1)
            iszero(mask & bit) || continue
            index = (mask | bit) + 1
            score = totals[mask+1] + scores[row,column]
            if score > totals[index]
                totals[index] = score
                last_column[index] = column
            end
        end
    end
    order = zeros(Int, count)
    mask = states-1
    for row in count:-1:1
        column = last_column[mask+1]
        order[row] = column
        mask ⊻= 1 << (column-1)
    end
    return order
end

function close_groups(previous_energy, current_energy, previous_vectors, current_vectors)
    labels = collect(eachindex(previous_energy))
    for j in eachindex(labels), i in 1:(j-1)
        close = min(abs(previous_energy[i]-previous_energy[j]),
                    abs(current_energy[i]-current_energy[j])) <= PROJECTOR_GROUP_MEV
        close || continue
        old, replacement = labels[j], labels[i]
        replace!(labels, old=>replacement)
    end
    groups = Dict{String,Any}[]
    for label in unique(labels)
        ix = findall(==(label), labels)
        length(ix) >= 2 || continue
        s = svdvals(previous_vectors[:,ix]' * current_vectors[:,ix])
        push!(groups, Dict("tracked_indices"=>ix, "projector_overlap_singular_values"=>s,
            "projector_distance"=>sqrt(max(0.0, 1-minimum(s)^2))))
    end
    return groups
end

function connect_bands(samples, phases)
    order = collect(1:TRACKED_BANDS)
    indices = [copy(order)]
    links = Dict{String,Any}[]
    for i in 2:length(phases)
        old_energy, old_vectors = samples[phases[i-1]]
        new_energy, new_vectors = samples[phases[i]]
        left = old_vectors[:,order]
        right = new_vectors[:,1:TRACKED_BANDS]
        scores = abs2.(left' * right)
        new_order = overlap_assignment(scores)
        push!(indices, new_order)
        push!(links, Dict("phase_from_rad"=>phases[i-1], "phase_to_rad"=>phases[i],
            "mode_overlap_squared"=>[scores[j,new_order[j]] for j in eachindex(order)],
            "near_groups"=>close_groups(old_energy[order],new_energy[new_order],left,right[:,new_order])))
        order = new_order
    end
    return indices, links
end

function grid_sweep(nz; fixture=false)
    data = inputs(nz, 1; field=0.0)
    # The diagonal block includes both harmonic face masses from the three-cell
    # BDD construction. The off-diagonal block carries the periodic seam.
    H = operator(data, 3)
    central = (nz+1):(2nz)
    right = (2nz+1):(3nz)
    cell = ComplexF64.(H[central,central])
    forward = ComplexF64.(H[central,right])
    phases0 = collect(range(-π,π; length=fixture ? 9 : 65))
    samples = Dict{Float64,Tuple{Vector{Float64},Matrix{ComplexF64}}}()
    energy_meV = 1e3*data.scale.E₀_eV
    sample!(samples, phases0, cell, forward, energy_meV)
    refinements, stable = refine_minimum!(samples, cell, forward, energy_meV;
        max_refinements=fixture ? 3 : MAX_REFINEMENTS)
    phases = sort!(collect(keys(samples)))
    energies = [samples[phase][1][1:TRACKED_BANDS] for phase in phases]
    order, links = connect_bands(samples, phases)
    endpoint_error = maximum(abs, energies[1] .- energies[end])
    periodic_oracle = energy_meV .* eigvals(Symmetric(operator(data,1; boundary=:periodic)), 1:TRACKED_BANDS)
    periodic_oracle_error = maximum(abs, periodic_oracle .- samples[0.0][1][1:TRACKED_BANDS])
    reverse_phase_error = maximum(maximum(abs, samples[phase][1] .- samples[reflected][1])
        for (phase, reflected) in zip(phases0, reverse(phases0)))
    return Dict(
        "spatial_nodes"=>nz, "initial_phase_count"=>length(phases0), "phases_rad"=>phases,
        "energies_meV"=>energies, "connected_energies_meV"=>[energies[i][order[i]] for i in eachindex(energies)],
        "connected_sorted_indices"=>order, "adjacent_phase_links"=>links,
        "minimum_gap_meV"=>last(refinements)["gap_meV"], "minimum_gap_phase_rad"=>last(refinements)["phase_rad"],
        "min_gap_stable"=>stable, "refinements"=>refinements,
        "guard_band_11_12_min_gap_meV"=>minimum(samples[phase][1][12]-samples[phase][1][11] for phase in phases),
        "periodic_endpoint_error_meV"=>endpoint_error, "initial_reverse_phase_error_meV"=>reverse_phase_error,
        "periodic_oracle_error_meV"=>periodic_oracle_error,
    )
end

function run(task, args)
    task == "BLOCH" || error("expected BLOCH")
    fixture = args == ["fixture"]
    grids = if fixture
        [24]
    elseif isempty(args)
        [144,288]
    elseif args == ["144"] || args == ["288"]
        [parse(Int, only(args))]
    else
        error("BLOCH arguments must be empty, 144, 288 or fixture")
    end
    BLAS.set_num_threads(1)
    results = [grid_sweep(nz; fixture) for nz in grids]
    return Dict("task"=>task, "status"=>all(x->x["min_gap_stable"],results) ? "measured" : "inconclusive",
        "fixture"=>fixture, "field_kV_cm"=>0.0, "grids"=>results, "tracked_bands"=>TRACKED_BANDS,
        "phase_gap_threshold_meV"=>GAP_TOLERANCE_MEV, "phase_bracket_tolerance_rad"=>Float64(PHASE_TOLERANCE),
        "near_group_threshold_meV"=>PROJECTOR_GROUP_MEV, "blas_threads"=>BLAS.get_num_threads(),
        "julia_threads"=>Threads.nthreads(), "gap_definition"=>"direct eigenvalue gap E8-E7 at equal phase")
end

end # module

run_bloch(task::String, args::Vector{String}) = V843BlochDiagnostics.run(task,args)
