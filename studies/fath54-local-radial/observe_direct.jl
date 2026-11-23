# The same independent Dyson reconstruction as SpatialBalance.ring_balance,
# omitting collision integrals when observing charge, current and occupation only.
function direct_rule(p,total,anchor,k;high_order)
    high_order && return T.independent_energy_rule(p,total,anchor,k)
    geometry = LT.CausalGeometry(p.en,LT.tapered_support(p.en),
        Matrix(anchor),p.geo.voltage,maximum(abs,p.geo.offsets))
    causal = LT.CausalRing(geometry,LT.unpack_ring(total,p.r))
    poles = LT.scan_poles(causal,p.geo,@view(p.h[:,:,k]);subdivisions=2)
    return LT.resonance_rule(causal,poles,18)
end

function direct_ring(p,total,anchor,k,covectors;high_order)
    rule = direct_rule(p,total,anchor,k;high_order)
    all(>(0),rule.weights) && isapprox(sum(rule.weights),sum(p.we);rtol=2e-12) ||
        error("independent energy measure changed")
    workspace = LT.TailWorkspace(p.geo)
    number = 0.
    current = zeros(p.nz+1)
    occupation = zeros(ComplexF64,size(p.h,1),size(p.h,2))
    radial = p.wk[k]*p.spin_degeneracy/(2π)
    for start in 1:128:length(rule.points)
        window = start:min(start+127,length(rule.points))
        points = @view rule.points[window]
        plan = LT.CausalRows(p.en,LT.shifted_queries(p.geo,points))
        packed = LT.sample_packed_ring(plan,total,anchor)
        for (i,E) in enumerate(points)
            weight = radial*rule.weights[window[i]]
            @views LT.sample_node!(workspace,p.geo,E,p.h[:,:,k],p.hops[:,k],packed[:,:,:,i,:])
            @views current .+= weight .* workspace.bond_profile[:,1]
            @views number += weight * imag(tr(workspace.local_green[:,:,2]))
            @views occupation .-= im * weight .* workspace.mode_green[:,:,2]
        end
    end
    return (;current,number,bands=real.(diag(covectors' * occupation * covectors)))
end

function direct_observation(p,source,cuts,workers;high_order=true)
    bands = p.geo.center_modes
    metric = Hermitian(p.geo.metric[bands,bands])
    eigenvectors = eigen(Hermitian(p.h[bands,bands,1]),metric)
    covectors = p.geo.metric[:,bands] * eigenvectors.vectors
    total = dropdims(sum(source;dims=5);dims=5)
    anchor = dropdims(sum(p.const_by_channel;dims=4);dims=4)
    results = Vector{Any}(undef,p.nk)
    LT.N._production_worker_ranges!(p.nk,min(workers,p.nk)) do _,lo,hi
        for k in lo:hi
            @views results[k] = direct_ring(p,total[:,:,:,k],anchor[:,:,k],k,covectors;high_order)
        end
    end
    current_A_cm2 = p.current_scale .* sum(r.current for r in results)
    current = T.SpatialBalance.current_metrics(current_A_cm2,T.widths_at(cuts))
    number = sum(r.number for r in results)
    band_number = sum(r.bands for r in results)
    band_total = sum(band_number)
    central_bands = (;reference_energy_meV=100eigenvectors.values,fraction=band_number./band_total,
        fraction_by_ring_and_band=[r.bands./band_total for r in results])
    return (;current,current_A_cm2,raw_sheet_cm2=number*p.density_scale,
        raw_lambda=number/p.target_dimless,raw_ring_sheet_cm2=[r.number*p.density_scale for r in results],
        central_bands,maximum_closure_error_A_cm2=nothing)
end
