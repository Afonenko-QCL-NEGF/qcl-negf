module V843Selection

using LinearAlgebra: dot
using SHA: sha256
using TOML

const ROLES = ("u", "l", "e", "i")
const RANKS = (6, 7, 8, 9, 11)
const PERIOD_NM = 36.16
const TRANSLATION_LIMITS = (translation=0.1, translation_nearest=0.1, translation_two_pairs=0.005)

# Fixed before any candidate results. The archived identification has RMS 1.79
# meV, a 7.05 meV energy margin, and an e profile cosine of 0.807. The e
# support is clipped by the figure and is compared only on its visible domain.
const COMPARISON = (
    shift_samples=361,
    shape_margin=0.02,
    energy_margin_meV=3.0,
    energy_rms_meV=5.0,
    minimum_role_cosine=0.8,
    minimum_clipped_e_cosine=0.75,
    expanded_window_cosine=0.95,
    expanded_window_energy_max_meV=3.0,
)

function figure_profiles(path)
    entries = Dict(label => Tuple{Float64,Float64,Float64}[] for label in ROLES)
    rows = readlines(path)
    first(rows) == "state,point,z_nm,plotted_energy_eV,baseline_eV_estimate,relative_curve_height_eV_plot_units" ||
        error("Unexpected published Fig. 1 CSV schema")
    for row in rows[2:end]
        label, _, x, _, baseline, height = split(row, ',')
        push!(entries[label], (parse(Float64, x), max(0.0, parse(Float64, height)), 1000parse(Float64, baseline)))
    end
    return map(ROLES) do label
        points = sort!(entries[label]; by=first)
        x = first.(points)
        all(>(0), diff(x)) || error("Figure has repeated or unordered coordinates for role $label")
        baseline = only(unique(last.(points)))
        (; x, height=getindex.(points, 2), baseline)
    end
end

function trapezoid_weights(x)
    w = zeros(Float64, length(x))
    for k in 1:(length(x)-1)
        half = (x[k+1]-x[k])/2
        w[k] += half
        w[k+1] += half
    end
    return w
end

function interpolate(x, values, z)
    (first(x) <= z <= last(x)) || return 0.0
    i = searchsortedlast(x, z)
    i == length(x) && return values[i]
    β = (z-x[i])/(x[i+1]-x[i])
    return (1-β)*values[i] + β*values[i+1]
end

function weighted_cosine(values, reference, w)
    norm_product = sqrt(dot(w, abs2.(values))*dot(w, abs2.(reference)))
    return norm_product > 0 ? dot(w, values .* reference)/norm_product : 0.0
end

function candidate_data(candidate)
    x = Float64.(candidate["x_nm"])
    energy = Float64.(candidate["energies_meV"])
    profiles = [Float64.(p) for p in candidate["density_profiles"]]
    rank = candidate["rank"]
    length(x) >= 2 && all(isfinite, x) && all(>(0), diff(x)) ||
        error("Invalid candidate probability coordinates")
    length(energy) == length(profiles) == rank && all(isfinite, energy) && issorted(energy) ||
        error("Invalid candidate energy and rank")
    all(p -> length(p) == length(x) && all(v -> isfinite(v) && v >= 0, p), profiles) ||
        error("Invalid candidate probabilities")
    return (; x, energy, profiles)
end

function compare_figure(candidate, reference)
    data = candidate_data(candidate)
    n = length(data.energy)
    assignments = [(u,l,e,i) for u in 1:n for l in 1:n for e in 1:n for i in 1:n
                   if length(Set((u,l,e,i))) == 4]
    energy_residuals = map(assignments) do ids
        delta = [data.energy[ids[j]] - reference[j].baseline for j in eachindex(ROLES)]
        offset = sum(delta)/length(delta)
        (; offset, rms=sqrt(sum(abs2, delta .- offset)/length(delta)))
    end
    best_shape = fill(-Inf, length(assignments))
    shifts = zeros(length(assignments))
    components = zeros(4, length(assignments))
    weights = map(p -> trapezoid_weights(p.x), reference)
    for shift in range(-PERIOD_NM, 0; length=COMPARISON.shift_samples)
        scores = [
            weighted_cosine(
                [interpolate(data.x, data.profiles[mode], z-shift) for z in reference[role].x],
                reference[role].height, weights[role],
            ) for role in eachindex(ROLES), mode in 1:n
        ]
        for (index, ids) in enumerate(assignments)
            score = sum(scores[j, ids[j]] for j in eachindex(ROLES))/length(ROLES)
            if score > best_shape[index]
                best_shape[index] = score
                shifts[index] = shift
                for role in eachindex(ROLES)
                    components[role,index] = scores[role,ids[role]]
                end
            end
        end
    end
    by_shape = sortperm(best_shape; rev=true)
    by_energy = sortperm(getproperty.(energy_residuals, :rms))
    winner = first(by_shape)
    ids = assignments[winner]
    shape_margin = best_shape[winner] - best_shape[by_shape[2]]
    energy_margin = energy_residuals[by_energy[2]].rms - energy_residuals[first(by_energy)].rms
    reason = String[]
    winner == first(by_energy) || push!(reason, "shape_and_relative_energy_match_different_roles")
    shape_margin >= COMPARISON.shape_margin || push!(reason, "shape_margin_below_threshold")
    energy_margin >= COMPARISON.energy_margin_meV || push!(reason, "energy_margin_below_threshold")
    energy_residuals[winner].rms <= COMPARISON.energy_rms_meV || push!(reason, "energy_rms_above_threshold")
    minimum_cosine = (COMPARISON.minimum_role_cosine, COMPARISON.minimum_role_cosine,
                     COMPARISON.minimum_clipped_e_cosine, COMPARISON.minimum_role_cosine)
    all(components[j,winner] >= minimum_cosine[j] for j in eachindex(ROLES)) ||
        push!(reason, "role_cosine_below_threshold")
    return Dict(
        "admitted"=>isempty(reason), "reasons"=>reason,
        "role_indices"=>Dict(zip(ROLES, ids)),
        "energy_best_role_indices"=>Dict(zip(ROLES, assignments[first(by_energy)])),
        "common_shift_nm"=>shifts[winner], "mean_cosine"=>best_shape[winner],
        "role_cosines"=>Dict(zip(ROLES, components[:,winner])),
        "shape_margin"=>shape_margin, "energy_margin_meV"=>energy_margin,
        "energy_offset_model_minus_article_meV"=>energy_residuals[winner].offset,
        "energy_rms_meV"=>energy_residuals[winner].rms,
        "role_energies_meV"=>Dict(zip(ROLES, data.energy[collect(ids)])),
    )
end

function confirm_expansion(small, large, first_fit, second_fit)
    a, b = candidate_data(small), candidate_data(large)
    ids_a = first_fit["role_indices"]
    ids_b = second_fit["role_indices"]
    common = filter(x -> first(b.x) <= x <= last(b.x), a.x)
    length(common) >= 2 || error("No common physical grid for adjacent basis windows")
    w = trapezoid_weights(common)
    cosines = Dict(role => weighted_cosine(
        [interpolate(a.x, a.profiles[ids_a[role]], z) for z in common],
        [interpolate(b.x, b.profiles[ids_b[role]], z) for z in common], w,
    ) for role in ROLES)
    e_a = first_fit["role_energies_meV"]
    e_b = second_fit["role_energies_meV"]
    drift = maximum(abs((e_a[role]-e_a[anchor])-(e_b[role]-e_b[anchor]))
                    for role in ROLES for anchor in ROLES)
    admitted = minimum(values(cosines)) >= COMPARISON.expanded_window_cosine &&
               drift <= COMPARISON.expanded_window_energy_max_meV
    return Dict("admitted"=>admitted, "rank"=>small["rank"],
                "smaller_p_basis"=>small["p_basis"], "larger_p_basis"=>large["p_basis"],
                "role_cosines"=>cosines, "relative_energy_max_change_meV"=>drift)
end

function read_basis_candidate_results(parent)
    candidates = Dict{Tuple{Int,Int},Dict{String,Any}}()
    baseline_reproduced = false
    for window in (7,9,11)
        report = TOML.parsefile(joinpath(parent, "B$window.toml"))
        p_basis = (window-1)÷2
        if window == 7
            baseline = get(report, "baseline_reproduced", nothing)
            baseline isa Bool || error("Missing explicit B7 baseline verdict")
            baseline_reproduced = baseline
        end
        report["field_kV_cm"] == 21 && report["spatial_nodes"] == 144 &&
            report["window_periods"] == window && report["p_basis"] == p_basis ||
            error("Basis direction has mismatched scientific input")
        for candidate in report["candidates"]
            rank = candidate["rank"]
            candidate["p_basis"] == p_basis && rank in RANKS ||
                error("Basis candidate geometry differs from the frozen matrix")
            id = (rank,p_basis)
            haskey(candidates,id) && error("Duplicate basis candidate")
            candidates[id] = candidate
        end
    end
    length(candidates) == 3length(RANKS) || error("Incomplete basis candidate matrix")
    return (; candidates, baseline_reproduced)
end

function bloch_diagnostics(parent)
    grids = map((144,288)) do n
        report = TOML.parsefile(joinpath(parent, "BLOCH$n.toml"))
        grid = only(report["grids"])
        grid["spatial_nodes"] == n || error("Bloch field has mismatched spatial resolution")
        gap = grid["minimum_gap_meV"]
        phase = grid["minimum_gap_phase_rad"]
        if isfinite(gap) && isfinite(phase)
            return Dict("spatial_nodes"=>n, "minimum_gap_meV"=>gap,
                        "minimum_gap_phase_rad"=>phase, "stable"=>grid["min_gap_stable"])
        end
        return Dict("spatial_nodes"=>n, "status"=>"inconclusive", "reason"=>"nonfinite_gap_diagnostic")
    end
    return collect(grids)
end

function run_select(task::String, args::Vector{String})
    task == "SELECT" && isempty(args) || error("SELECT takes no positional inputs")
    parent = ENV["QCL_PARENT_RESULTS"]
    (; candidates, baseline_reproduced) = read_basis_candidate_results(parent)
    bloch = bloch_diagnostics(parent)
    fig = joinpath(@__DIR__, "..", "fath-v843", "controls", "fig1", "fig1_profiles.csv")
    reference = figure_profiles(fig)
    fits = Dict{Tuple{Int,Int},Dict}()
    rows = Dict{String,Any}[]
    for id in sort!(collect(keys(candidates)))
        candidate = candidates[id]
        row = Dict{String,Any}("rank"=>id[1], "p_basis"=>id[2], "window_periods"=>2id[2]+1)
        if candidate["status"] == "inconclusive"
            row["status"] = "inconclusive"
            row["reason"] = get(candidate, "reason", "basis extraction did not provide identifiable reference modes")
        elseif candidate["status"] == "measured"
            metrics = Dict(string(name)=>candidate[string(name)] for name in keys(TRANSLATION_LIMITS))
            translation_pass = all(isfinite(metrics[string(name)]) && 0 <= metrics[string(name)] <= limit
                                    for (name,limit) in pairs(TRANSLATION_LIMITS))
            reported_static_pass = candidate["static_pass"]
            reported_static_pass isa Bool || error("Missing explicit static gate for $id")
            reported_static_pass && !translation_pass && error("Inconsistent translation gate for $id")
            structural = translation_pass && reported_static_pass
            row["translation_metrics"] = metrics
            row["reported_static_pass"] = reported_static_pass
            row["status"] = structural ? "static_admitted" : "static_rejected"
            if structural
                fit = compare_figure(candidate, reference)
                row["figure_comparison"] = fit
                row["status"] = fit["admitted"] ? "figure_admitted" : "figure_rejected"
                fit["admitted"] && (fits[id] = fit)
            end
        else
            error("Unrecognized terminal basis status for $id")
        end
        push!(rows, row)
    end
    expansions = Dict[]
    for rank in RANKS, p_basis in (3,4)
        small, large = (rank,p_basis), (rank,p_basis+1)
        haskey(fits, small) && haskey(fits, large) || continue
        push!(expansions, confirm_expansion(candidates[small], candidates[large], fits[small], fits[large]))
    end
    compatible = filter(x -> baseline_reproduced && x["admitted"], expansions)
    input_hashes = Dict(name => bytes2hex(open(sha256, joinpath(parent, name * ".toml")))
                        for name in ("B7","B9","B11","BLOCH144","BLOCH288"))
    report = Dict{String,Any}(
        "schema"=>"v843-basis-selection-v1",
        "status"=>isempty(compatible) ? "rejected" : "admitted",
        "qualified"=>!isempty(compatible), "baseline_reproduced"=>baseline_reproduced,
        "field_kV_cm"=>21.0, "spatial_nodes"=>144, "candidates"=>rows,
        "expansion_checks"=>expansions, "bloch_zero_field_diagnostics"=>bloch,
        "figure_sha256"=>bytes2hex(open(sha256,fig)), "parent_sha256"=>input_hashes,
        "translation_limits"=>Dict(string(k)=>v for (k,v) in pairs(TRANSLATION_LIMITS)),
        "literature_thresholds"=>Dict(string(k)=>v for (k,v) in pairs(COMPARISON)),
        "selection_rule"=>"smallest qualified rank; prefer the larger window confirmed by its adjacent smaller window",
    )
    if isempty(compatible)
        report["reason"] = baseline_reproduced ?
            "no_static_and_figure_admitted_rank_stable_under_window_expansion" :
            "b7_archive_baseline_did_not_reproduce"
        return report
    end
    best = first(sort!(compatible; by=x -> (x["rank"],-x["larger_p_basis"])))
    rank, p_basis = best["rank"], best["larger_p_basis"]
    report["rank"] = rank
    report["p_basis"] = p_basis
    report["window_periods"] = 2p_basis+1
    report["selected_confirmation"] = best
    report["selected_figure_comparison"] = fits[(rank,p_basis)]
    return report
end

end # module

run_select(task::String, args::Vector{String}) = V843Selection.run_select(task, args)
