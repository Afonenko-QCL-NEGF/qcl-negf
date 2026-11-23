# Include after studies/fath-lo-rank-v843/fath_factorial.jl.
# SpatialBalance.ring_balance supplies the common GL20 Dyson reconstruction.

const FATH_LATE7_CUTS_NM = (33.84729166666667,39.640972222222224)
const FATH_LATE8_CUTS_NM = (34.45715277777778,39.031111111111116)
include(joinpath(@__DIR__, "lo_cut_split.jl"))

function projected_crossings(frame, h, lesser, monitor, nz)
    coordinate_h = frame * h * frame'
    coordinate_lesser = frame * lesser * frame'
    # Every pair (i,j) contributes to the consecutive faces i through j-1.
    # The columns split the nearest bond, longer in-period, and interperiod links.
    first_cut, last_cut = first(monitor), last(monitor)-1
    changes = zeros(length(monitor), 3)
    for j in (first_cut+1):size(frame, 1)
        for i in 1:min(j-1, last_cut)
            a, b = max(i, first_cut), min(j-1, last_cut)
            part = j == i+1 ? 1 : (fld(i-1, nz) == fld(j-1, nz) ? 2 : 3)
            value = 2real(coordinate_h[i,j] * coordinate_lesser[j,i])
            changes[a-first_cut+1,part] += value
            changes[b-first_cut+2,part] -= value
        end
    end
    return cumsum(changes; dims=1)[1:end-1, :]
end

function fixed_cut_balance(cuts, current, kinetic, gap, collisions)
    cut_index(z) = argmin(abs.(cuts .- z))
    minimum_index, maximum_index = argmin(current), argmax(current)
    steepest = argmax(abs.(diff(current)))
    function contrast(a, b)
        difference(curve) = curve[b] - curve[a]
        collisional = Dict(channel=>difference(curve) for (channel,curve) in collisions)
        collision_sum = sum(values(collisional))
        delta, lag, projection = difference(current), difference(kinetic), difference(gap)
        return (;from_nm=cuts[a], to_nm=cuts[b], delta_J_A_cm2=delta,
            J_from_A_cm2=current[a], J_to_A_cm2=current[b],
            source_lag_A_cm2=lag, projection_A_cm2=projection,
            collisions_A_cm2=collisional, collision_sum_A_cm2=collision_sum,
            closure_A_cm2=delta-lag-projection-collision_sum)
    end
    return (;
        late7=contrast(cut_index.(FATH_LATE7_CUTS_NM)...),
        late8=contrast(cut_index.(FATH_LATE8_CUTS_NM)...),
        extrema=contrast(minimum_index,maximum_index),
        seams=contrast(firstindex(cuts),lastindex(cuts)),
        largest_cell_jump=contrast(steepest,steepest+1),
    )
end

function localize_lo(p, seed, image, cuts, results, center, fixed, energy_rule)
    lo_total = fixed.collisions_A_cm2["LO"]
    threshold_J, threshold_fraction = 5.0, 0.5
    triggered = abs(fixed.delta_J_A_cm2) > threshold_J &&
        abs(lo_total) > threshold_fraction * abs(fixed.delta_J_A_cm2)
    criterion = (;threshold_current_A_cm2=threshold_J, threshold_fraction,
        fixed.from_nm, fixed.to_nm, fixed.delta_J_A_cm2, lo_total_A_cm2=lo_total)
    triggered || return (;triggered, criterion)

    lo = only(findall(==(:LO),LT.COLLISION_CHANNELS))
    a,b = (argmin(abs.(cuts .- z)) for z in FATH_LATE7_CUTS_NM)
    by_ring = [p.current_scale * sum(@view SpatialBalance.diagonal_in_coordinates(
        x.balance.contributions[lo],center)[a:b-1]) for x in results]
    chosen = sortperm(abs.(by_ring); rev=true)[1:min(2,p.nk)]
    selected_native = sum(by_ring[chosen])
    split = lo_cut_split(p,seed,image,cuts,chosen; energy_rule)
    selected_control = sum(x.contrasts.late7.total_A_cm2 for x in split.rings)
    selected = [(;ring=k, radial_weight=p.wk[k],
        raw_sheet_cm2=p.density_scale*results[k].balance.radial_number,
        native_lo_A_cm2=by_ring[k]) for k in chosen]
    return (;triggered, criterion, selected, native_lo_by_ring_A_cm2=by_ring,
        native_lo_all_rings_A_cm2=lo_total,
        native_lo_selected_rings_A_cm2=selected_native,
        native_lo_other_rings_A_cm2=lo_total-selected_native,
        selected_lo_fraction=selected_native/lo_total,
        selected_signed_lo_rerun_A_cm2=selected_control,
        native_ring_sum_error_A_cm2=sum(by_ring)-lo_total,
        selected_reconstruction_error_A_cm2=selected_control-selected_native,
        split)
end

function observe_balance(p, seed, image, cuts, workers; fresh_profile=true,
        energy_rule=independent_energy_rule, lo_control=true)
    length(cuts) == p.nz+1 && all(>(0),diff(cuts)) ||
        throw(ArgumentError("physical cut coordinates do not match the BDD grid"))
    widths = (cuts[3:end] .- cuts[1:end-2])./2
    row = linked_metrics(image.summary,widths)
    pair = row.fermionic_pair
    coefficients = (pair.a,pair.c)
    modes = p.geo.modes
    dual = inv(Hermitian(p.geo.metric))
    center = @view modes[(first(p.geo.monitor)+1):(last(p.geo.monitor)-1),:]
    center_metric = center' * center
    state_total = dropdims(sum(seed; dims=5); dims=5)
    anchor = dropdims(sum(p.const_by_channel; dims=4); dims=4)
    results = Vector{Any}(undef,p.nk)
    LT.N._production_worker_ranges!(p.nk, min(workers, Threads.nthreads(:default), p.nk)) do _, lo, hi
        for k in lo:hi
            balance = SpatialBalance.ring_balance(p, state_total, anchor, image.source,
                dual, center_metric, false, energy_rule, coefficients, k)
            projected_h_mode = dual * (@view p.h[:,:,k]) * dual
            crossed = projected_crossings(modes, projected_h_mode, im .* balance.occupation,
                p.geo.monitor, p.nz)
            results[k] = (;balance,crossed)
        end
    end
    scale = p.current_scale
    prefix(a) = [0.0; cumsum(a)]
    anchored(a) = a .- first(a)
    lift(a) = scale .* SpatialBalance.diagonal_in_coordinates(a, center)
    lagged_current = scale .* sum(x.balance.current for x in results)
    lagged_raw_lambda = sum(x.balance.radial_number for x in results)/p.target_dimless
    crossed = scale .* sum(x.crossed for x in results)
    projected_current = vec(sum(crossed; dims=2))
    coherent = lift(sum(x.balance.coherent for x in results))
    kinetic = lift(sum(x.balance.kinetic for x in results))
    projected_gap = anchored(lagged_current - projected_current)
    collision = [lift(sum(x.balance.contributions[j] for x in results))
        for j in eachindex(LT.COLLISION_CHANNELS)]
    channel_names = string.(LT.COLLISION_CHANNELS)
    collision_cumulative = Dict(name=>prefix(a) for (name,a) in zip(channel_names, collision))
    closure = diff(projected_current) - kinetic - sum(collision)
    contrasts = fixed_cut_balance(cuts,lagged_current,prefix(kinetic),projected_gap,collision_cumulative)
    lagged = (;current_A_cm2=lagged_current,
        current=SpatialBalance.current_metrics(lagged_current,widths),
        raw_lambda=lagged_raw_lambda,
        projected_current_A_cm2=projected_current,
        projected_crossings_A_cm2=(;nearest_bond=crossed[:,1],
            longer_within_period=crossed[:,2], longer_between_periods=crossed[:,3]),
        spatial_projection_gap_A_cm2=projected_gap,
        kinetic_remainder_A_cm2=prefix(kinetic),
        collision_cumulative_A_cm2=collision_cumulative,
        particle_exchange_A_cm2=Dict(name=>scale*value
            for (name,value) in zip(channel_names,sum(x.balance.particle_exchange for x in results))),
        maximum_closure_error_A_cm2=maximum(abs,closure),
        largest_projected_flux_divergence_disagreement_A_cm2=maximum(abs,diff(projected_current)-coherent),
        weighted_rK_Q=sqrt(sum(x.balance.kinetic_difference for x in results) /
            max(sum(x.balance.kinetic_reference for x in results),1e-300)),
        contrasts)
    lo_localization = lo_control ? localize_lo(p,seed,image,cuts,results,center,contrasts.late7,energy_rule) : nothing
    if !fresh_profile
        return (;cut_coordinates_nm=cuts, lagged, lo_localization, observed=nothing,
            independent_profile_difference_A_cm2=nothing)
    end
    observed = spatial_balance(p,image.source,widths; workers,energy_rule,current_cuts=cuts)
    return (;cut_coordinates_nm=cuts,lagged,lo_localization,observed,
        independent_profile_difference_A_cm2=maximum(abs,observed.current_A_cm2-row.current_profile_A_cm2))
end
