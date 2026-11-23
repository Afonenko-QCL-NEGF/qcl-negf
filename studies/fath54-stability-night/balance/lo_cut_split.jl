# Include after observe_balance.jl. Uses the same state and quadrature as the lagged balance.

function lo_split_terms!(balanced, gain_loss, dispersive, scratch, green_h, sigma_h,
        retarded, lesser, greater, sigma_r, sigma_l, sigma_g, dual)
    green_h .= (retarded .+ retarded') ./ 2
    sigma_h .= (sigma_r .+ sigma_r') ./ 2

    mul!(scratch, retarded, sigma_l)
    mul!(balanced, scratch, dual)
    mul!(scratch, sigma_r, lesser)
    mul!(balanced, dual, scratch, -1, 1)

    mul!(scratch, greater, sigma_l)
    mul!(scratch, lesser, sigma_g, -1, 1)
    mul!(gain_loss, scratch, dual, 0.5, 0)

    mul!(scratch, green_h, sigma_l)
    mul!(dispersive, scratch, dual)
    mul!(scratch, sigma_h, lesser)
    mul!(dispersive, dual, scratch, -1, 1)
    return nothing
end

function split_lo_ring(p, state_total, anchor, fresh_lo, lo_constant, dual, center,
        cuts, energy_rule, k)
    lo_fields = zeros(ComplexF64, size(p.h,1), size(p.h,2), 3)
    sigma_buffer = similar(LT.centered_basis(p.geo))
    ws = LT.TailWorkspace(p.geo)
    integrals = [zero(dual) for _ in 1:3]
    balanced, gain_loss, dispersive, scratch, green_h, sigma_h = (similar(dual) for _ in 1:6)
    radial = p.wk[k] * p.spin_degeneracy / (2π)
    rule = isnothing(energy_rule) ? (points=p.en, weights=p.we) :
        energy_rule(p, @view(state_total[:,:,:,k]), @view(anchor[:,:,k]), k)
    rule_points, measure = rule.points, rule.weights
    length(rule_points) == length(measure) && all(>(0),measure) &&
        isapprox(sum(measure), sum(p.we); rtol=2e-12, atol=1e-14) ||
        throw(ArgumentError("LO split energy rule must preserve the positive measure"))
    @views for start in 1:128:length(rule_points)
        indices = start:min(start+127,length(rule_points))
        points = rule_points[indices]
        plan = LT.CausalRows(p.en, LT.shifted_queries(p.geo, points))
        driving = LT.sample_packed_ring(plan, state_total[:,:,:,k], anchor[:,:,k])
        latest = LT.sample_packed_ring(plan, fresh_lo[:,:,:,k], lo_constant[:,:,k])
        for (i,energy) in enumerate(points)
            LT.sample_node!(ws, p.geo, energy, p.h[:,:,k], p.hops[:,k], driving[:,:,:,i,:])
            SpatialBalance.local_source!(lo_fields, p.geo.bases, latest[:,:,:,i,:], sigma_buffer)
            retarded, lesser, greater = ws.mode_green[:,:,1], ws.mode_green[:,:,2], ws.mode_green[:,:,3]
            sigma_r, sigma_l, sigma_g = lo_fields[:,:,1], lo_fields[:,:,2], lo_fields[:,:,3]
            lo_split_terms!(balanced, gain_loss, dispersive, scratch, green_h, sigma_h,
                retarded, lesser, greater, sigma_r, sigma_l, sigma_g, dual)
            weight = radial * measure[indices[i]]
            for (integral, term) in zip(integrals, (balanced,gain_loss,dispersive))
                SpatialBalance.add_hermitian_part!(integral, term, weight)
            end
        end
    end
    lifted = [p.current_scale .* SpatialBalance.diagonal_in_coordinates(x,center) for x in integrals]
    total, kinetic, dispersion = ([0.0; cumsum(x)] for x in lifted)
    function contrast(positions)
        a,b = (argmin(abs.(cuts .- z)) for z in positions)
        return (;from_nm=cuts[a], to_nm=cuts[b], total_A_cm2=total[b]-total[a],
            gain_loss_A_cm2=kinetic[b]-kinetic[a], dispersive_A_cm2=dispersion[b]-dispersion[a])
    end
    return (;ring=k, radial_weight=radial,
        total_A_cm2=total, gain_loss_A_cm2=kinetic, dispersive_A_cm2=dispersion,
        maximum_closure_error_A_cm2=maximum(abs,lifted[1]-lifted[2]-lifted[3]),
        contrasts=(;late7=contrast(FATH_LATE7_CUTS_NM),
            late8=contrast(FATH_LATE8_CUTS_NM),
            seams=contrast((first(cuts),last(cuts)))))
end

function lo_cut_split(p, seed, image, cuts, rings; energy_rule=independent_energy_rule)
    rings = sort!(unique(collect(Int,rings)))
    !isempty(rings) && all(k->1 <= k <= p.nk, rings) ||
        throw(ArgumentError("choose valid radial rings"))
    lo = only(findall(==(:LO),LT.COLLISION_CHANNELS))
    length(cuts) == p.nz+1 && all(>(0),diff(cuts)) ||
        throw(ArgumentError("physical cut coordinates do not match the BDD grid"))
    dual = Matrix(inv(Hermitian(p.geo.metric)))
    center = @view p.geo.modes[(first(p.geo.monitor)+1):(last(p.geo.monitor)-1),:]
    state_total = dropdims(sum(seed; dims=5); dims=5)
    anchor = dropdims(sum(p.const_by_channel; dims=4); dims=4)
    fresh_lo = @view image.source[:,:,:,:,lo]
    lo_constant = @view p.const_by_channel[:,:,:,lo]
    return (;cut_coordinates_nm=cuts,
        rings=[split_lo_ring(p,state_total,anchor,fresh_lo,lo_constant,dual,center,cuts,
            energy_rule,k) for k in rings])
end
