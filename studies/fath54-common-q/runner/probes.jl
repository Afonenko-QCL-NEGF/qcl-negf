const ENERGY_WINDOWS = (
    (name="positive40", e=(40.0,42.0), k=(0.168,0.170)),
    (name="negative13", e=(-14.0,-12.0), k=(0.187,0.200)),
    (name="narrow26", e=(25.6,27.0), k=(0.075,0.100)),
    (name="control10", e=(9.0,11.8), k=(0.075,0.100)),
)

function integrated_samples(problem, source, anchor, h, hops, points, weights, cuts)
    ws = LT.TailWorkspace(problem.geo)
    number, profiles = zeros(length(points)), zeros(length(cuts),length(points))
    for start in 1:96:length(points)
        batch = start:min(start+95,length(points))
        plan = LT.CausalRows(problem.en,LT.shifted_queries(problem.geo,points[batch]))
        packed = LT.sample_packed_ring(plan,source,anchor)
        for (i,j) in enumerate(batch)
            @views LT.sample_node!(ws,problem.geo,points[j],h,hops,packed[:,:,:,i,:])
            number[j] = imag(tr(ws.local_green[:,:,2]))*problem.density_scale
            profiles[:,j] .= ws.bond_profile[:,1] .* problem.current_scale
        end
    end
    weight = weights .* (problem.spin_degeneracy/(2π))
    return (;charge=dot(weight,number), profile=profiles*weight, number, profiles)
end

function ring_data(problem, source, radius, value)
    right = searchsortedfirst(radius,value)
    left = (right == 1 || radius[right] == value) ? right : right-1
    fraction = left == right ? 0.0 : (value^2-radius[left]^2)/(radius[right]^2-radius[left]^2)
    @views mix(array, axis) = (1-fraction).*selectdim(array,axis,left) .+
        fraction.*selectdim(array,axis,right)
    packed = dropdims(sum(mix(source,4);dims=4);dims=4)
    anchor = dropdims(sum(mix(problem.const_by_channel,3);dims=3);dims=3)
    return (;packed,anchor,h=mix(problem.h,3),hops=mix(problem.hops,2))
end

function energy_rule_at(problem, data; boundaries=Float64[])
    layout = LT.CausalGeometry(problem.en,LT.tapered_support(problem.en),Matrix(data.anchor),
        problem.geo.voltage,maximum(abs,problem.geo.offsets))
    causal = LT.CausalRing(layout,LT.unpack_ring(data.packed,problem.r))
    scan = LT.scan_poles(causal,problem.geo,data.h;subdivisions=5)
    scan = (;points=sort!(unique!([scan.points; boundaries])),scan.poles)
    rule = LT.resonance_rule(causal,scan,28)
    return (;rule,scan.poles)
end

function profile_metrics(profile, cuts)
    widths = T.widths_at(cuts)
    mean = dot(widths,profile[2:end-1])/sum(widths)
    return (;mean,centered=profile.-mean,
        segment=R.section_jump(cuts,profile),
        second_segment=R.section_jump(cuts,profile,RC.FATH_LATE8_CUTS_NM))
end

function energy_probe(problem, source, grid, cuts, window)
    rings = findall(k -> first(window.k)<=k/10<=last(window.k),grid)
    return map(rings) do k
        data = ring_data(problem,source,grid,grid[k])
        a,b = collect(window.e)./100
        scan = energy_rule_at(problem,data;boundaries=[a,b])
        native_panels = sort!(unique([a; filter(x->a<x<b,problem.en); b]))
        panel_edges = collect(range(a,b,length=65))
        panel_widths = diff(panel_edges)
        phases = map((0.25,0.75)) do phase
            points = panel_edges[1:end-1] .+ phase.*panel_widths
            sampled = integrated_samples(problem,data.packed,data.anchor,data.h,data.hops,
                points,panel_widths.*problem.wk[k],cuts)
            (;charge=sampled.charge,J=profile_metrics(sampled.profile,cuts),
                points_meV=100 .* points,charge_density=sampled.number,
                signed_jump_density=map(j -> R.section_jump(cuts,view(sampled.profiles,:,j)),
                    eachindex(points)))
        end
        edges = integrated_samples(problem,data.packed,data.anchor,data.h,data.hops,
            native_panels,zeros(length(native_panels)),cuts)
        in_window = findall(x->a<x<b,scan.rule.points)
        standard = integrated_samples(problem,data.packed,data.anchor,data.h,data.hops,
            scan.rule.points[in_window],scan.rule.weights[in_window].*problem.wk[k],cuts)
        return (;candidate=window.name,k_nm_inverse=grid[k]/10, phases,
            native_panel_edges_meV=100 .* native_panels,native_charge_density=edges.number,
            poles=filter(x->a<=x.energy<=b,scan.poles),
            standard=(;charge=standard.charge,J=profile_metrics(standard.profile,cuts),
                integrated_measure=sum(scan.rule.weights[in_window])))
    end
end

function radial_probe(problem, source, grid, cuts, center)
    k = argmin(abs.(grid.-center))
    k in 2:length(grid)-1 || error("interior radius required")
    a,b = ((grid[k-1]+grid[k])/2)^2,((grid[k]+grid[k+1])/2)^2
    phases = map((0.0,0.25,0.75)) do phase
        radius = iszero(phase) ? grid[k] : sqrt(a+phase*(b-a))
        data = ring_data(problem,source,grid,radius)
        nodes = energy_rule_at(problem,data)
        result = integrated_samples(problem,data.packed,data.anchor,data.h,data.hops,
            nodes.rule.points,nodes.rule.weights.*problem.wk[k],cuts)
        return (;phase,k_nm_inverse=radius/10,charge=result.charge,J=profile_metrics(result.profile,cuts))
    end
    return (;k_nm_inverse=grid[k]/10,annulus_measure=problem.wk[k],phases)
end

function probe_windows(problem, source, grid, cuts)
    energy = vcat((energy_probe(problem,source,grid,cuts,w) for w in ENERGY_WINDOWS)...)
    radial = [radial_probe(problem,source,grid,cuts,k) for k in (1.6875,1.9375,2.75)]
    return (;energy,radial)
end
