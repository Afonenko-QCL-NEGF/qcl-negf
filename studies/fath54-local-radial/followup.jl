function transfer_path(p,seed,old_k,base,k25,fine,cuts,workers,ring_charge)
    first = transfer_arm(p,old_k,seed,base,k25,ring_charge)
    P = T.annular_transfer(k25,fine.k,base.wk,fine.p.wk)
    mapped = T.apply_radial(P,first.mapped)
    direct = T.apply_radial(T.annular_transfer(old_k,fine.k,p.wk,fine.p.wk),seed)
    field_change = T.packed_difference(fine.p,mapped,direct,fine.k)
    direct = nothing
    input = observed_row(observe_refinement(fine.p,mapped,cuts,workers),cuts)
    image = arm_image(fine.p,mapped,cuts,workers)
    measurements = measure_arm(fine.p,image,cuts,workers;independent_input=input)
    return (;field_change,measurements,source_sha=T.packed_sha(mapped))
end

function fine_rule(p,total,anchor,k)
    layout = LT.CausalGeometry(p.en,LT.tapered_support(p.en),Matrix(anchor),
        p.geo.voltage,maximum(abs,p.geo.offsets))
    causal = LT.CausalRing(layout,LT.unpack_ring(total,p.r))
    poles = LT.scan_poles(causal,p.geo,@view(p.h[:,:,k]);subdivisions=5)
    return LT.resonance_rule(causal,poles,28)
end

function spectral_ring(p,source,k,energy_rule,indices)
    total = dropdims(sum(@view(source[:,:,:,k,:]);dims=4);dims=4)
    anchor = dropdims(sum(@view(p.const_by_channel[:,:,k,:]);dims=3);dims=3)
    rule = energy_rule(p,total,anchor,k)
    ws = LT.TailWorkspace(p.geo)
    number = zeros(p.ne-1)
    mean_current = zeros(p.ne-1)
    segment_current = zeros(p.ne-1)
    radial = p.wk[k]*p.spin_degeneracy/(2π)
    for start in 1:128:length(rule.points)
        window = start:min(start+127,length(rule.points))
        points = @view rule.points[window]
        plan = LT.CausalRows(p.en,LT.shifted_queries(p.geo,points))
        packed = LT.sample_packed_ring(plan,total,anchor)
        for (i,E) in enumerate(points)
            e = clamp(searchsortedlast(p.en,E),1,p.ne-1)
            weight = radial*rule.weights[window[i]]
            @views LT.sample_node!(ws,p.geo,E,p.h[:,:,k],p.hops[:,k],packed[:,:,:,i,:])
            @views number[e] += weight*imag(tr(ws.local_green[:,:,2]))*p.density_scale
            profile = @view ws.bond_profile[:,1]
            mean_current[e] += weight*dot(profile[2:end-1],indices.widths)/sum(indices.widths)*p.current_scale
            segment_current[e] += weight*(profile[indices.right]-profile[indices.left])*p.current_scale
        end
    end
    return (;ring=k,number,mean_current,segment_current)
end

function window_charge_difference(baseline,retained)
    a,b = baseline.report,retained.report
    P = T.annular_transfer(baseline.arm.k,retained.arm.k,a.w,b.w)
    rebinned(stage) = let old = getproperty(a.measurements,stage), new = getproperty(b.measurements,stage)
        new.raw_charge_by_ring .- b.w .* (P * (old.raw_charge_by_ring ./ a.w))
    end
    candidates = findall(k->1.5-1e-14<=k<=2.0+1e-14,retained.arm.k)
    return (;P,input=rebinned(:independent_input),fresh=rebinned(:observed),candidates)
end

function spectral_check(baseline,retained,cuts,levels,label)
    arm,mapped,image = retained.arm,retained.mapped,retained.image
    # Choose the four largest changes of radial charge density, with K25
    # observations transported to the same cells before taking the difference.
    coarse = levels["K25"]
    destination = levels[label]
    diagnostic = window_charge_difference(baseline,retained)
    P,charge,fresh = diagnostic.P,diagnostic.input,diagnostic.fresh
    selected = sort(diagnostic.candidates;by=k->max(abs(charge[k]),abs(fresh[k])),rev=true)[1:4]
    jleft,jright = [argmin(abs.(cuts .- edge)) for edge in fixed_cuts]
    indices = (;widths=T.widths_at(cuts),left=jleft,right=jright)
    base_indices = findall(j -> any(i -> P[i,j]>0,selected),eachindex(coarse.w))
    function evaluate(source, reference_source, ref)
        baseline_by_ring = Dict(j => spectral_ring(baseline.arm.p,reference_source,j,
            T.independent_energy_rule,indices) for j in base_indices)
        return map(selected) do ring
            standard = spectral_ring(arm.p,source,ring,T.independent_energy_rule,indices)
            finer = spectral_ring(arm.p,source,ring,fine_rule,indices)
            total = sum(standard.number)
            isapprox(total,ref.raw_charge_by_ring[ring];rtol=2e-8,atol=2.) ||
                error("spectral binning does not reproduce the independent charge")
            function delta_in_measure(field)
                delta = copy(getproperty(standard,field))
                for j in base_indices
                    delta .-= (arm.p.wk[ring]*P[ring,j]/coarse.w[j]) .* getproperty(baseline_by_ring[j],field)
                end
                return delta
            end
            delta_vs_K25 = (;number=delta_in_measure(:number),mean_current=delta_in_measure(:mean_current),
                segment_current=delta_in_measure(:segment_current))
            totals(x) = (;number=sum(x.number),mean_current=sum(x.mean_current),
                segment_current=sum(x.segment_current))
            (;radius_nm_inverse=arm.k[ring]/10,standard=totals(standard),finer=totals(finer),delta_vs_K25,
                high_order_charge_delta_cm2=sum(finer.number)-total,
                high_order_current_delta_A_cm2=sum(finer.mean_current)-sum(standard.mean_current),
                high_order_segment_delta_A_cm2=sum(finer.segment_current)-sum(standard.segment_current))
        end
    end
    return (;energy_edges_meV=100arm.p.en,selected,charge_rebinned_difference_by_ring=charge,
        fresh_rebinned_difference_by_ring=fresh,
        input=evaluate(mapped,baseline.mapped,destination.measurements.independent_input),
        fresh=evaluate(image.source,baseline.image.source,destination.measurements.observed))
end

module RankControl
include(joinpath(ENV["FATH_APP"],"studies","fath-lo-rank-v843","fath_factorial.jl"))
include(joinpath(dirname(dirname(ARGS[1])),"balance","observe_balance.jl"))

function expand(p,k,seed,archive,geometry_path,geometry_sha)
    data = coordinate_data(geometry_path,geometry_sha,p)
    x = expand_modes(p,data,k)
    embedding = x.q' * p.v.coordinate_frame
    lifted = lift_source(seed,embedding)
    sites = Runner._read_linked_array(archive,"ifr_sites",Float64,size(p.v.interface_probes,1),p.nz)
    kernel = lo_kernel(p.v,sites,p.v.lo_plus,p.v.lo_minus;q=x.q)
    anchors = cat([embedding * p.const_by_channel[:,:,j,c] * embedding'
        for j in 1:p.nk, c in eachindex(LT.COLLISION_CHANNELS)]...;dims=3)
    anchors = reshape(anchors,size(x.q,2),size(x.q,2),p.nk,:)
    expanded = rebuild(p,kernel;modes=x.modes,nb=x.nb,h=x.h,anchor=anchors)
    common_error = maximum(norm(embedding' * b[:,x.common] - old) / norm(old)
        for (b,old) in zip(expanded.geo.bases,p.geo.bases))
    common_error < 2e-13 || error("rank control did not retain the common basis")
    return (;problem=expanded,lifted.source,x.metric_error,x.h_error,common_error,lifted.roundtrip_maximum)
end
end

function rank_control(retained,cuts,workers)
    arm, mapped = retained.arm, retained.mapped
    geometry = get(ENV,"FATH_BDD",joinpath(build_dir,"fath54-20261120","work","05-iterator","runs","causal-native-512","model.h5"))
    spec = T.TOML.parsefile(joinpath(fine_path,"spec.toml"))
    expanded = RankControl.expand(arm.p,arm.k,mapped,fine_path,geometry,spec["source_model_sha"])
    problems = (arm.p,expanded.problem)
    states = [mapped,expanded.source]
    images = [retained.image,arm_image(expanded.problem,expanded.source,cuts,workers)]
    widths = T.widths_at(cuts)
    factor(x,y) = max(x,y)/max(min(x,y),1e-300)
    native = map(im->T.linked_metrics(im.summary,widths),images)
    ratios() = (;rK=factor(native[1].rK,native[2].rK),
        rSigma=factor(native[1].rSigma,native[2].rSigma))
    history = [(;step=1,ratios=ratios(),rows=copy(native))]
    step = 1
    while maximum(values(ratios()))>1.25 && step<4
        step += 1
        for i in eachindex(states)
            # Guard the common initial F13 transfer retained by the caller.
            states[i] = 0.65 .* states[i] .+ 0.35 .* images[i].source
            images[i] = arm_image(problems[i],states[i],cuts,workers)
            native[i] = T.linked_metrics(images[i].summary,widths)
        end
        push!(history,(;step,ratios=ratios(),rows=copy(native)))
    end
    obs = [RankControl.observe_balance(problems[i],states[i],images[i],cuts,workers;lo_control=false)
        for i in eachindex(states)]
    seven,eight = [(;native=native[i],independent=obs[i]) for i in eachindex(obs)]
    factors = (;ratios()...,rK_Q=factor(seven.independent.lagged.weighted_rK_Q,
        eight.independent.lagged.weighted_rK_Q))
    return (;seven,eight,stage="matched_grid_rank",step,history,
        comparable_residuals=max(factors.rK,factors.rSigma)<=1.25,factors,
        expansion=(;expanded.metric_error,expanded.h_error,expanded.common_error,expanded.roundtrip_maximum))
end

function second_history(p,base,k25,fine,cuts,workers)
    second_path = get(ENV,"FATH_SECOND_HISTORY",joinpath(dirname(coarse_path),"linked-E481x13-norm-alpha020-step0002"))
    x = T.Runner._read_linked_checkpoint(second_path)
    x.current_midpoints==cuts || error("second history has different physical cuts")
    k = radial_coordinates(second_path,x.problem.nk)
    T.radial_setup(x.problem,cuts,second_path,fine_path)
    observations = T.radial_observe(x.problem,x.seed,cuts,workers)
    q = observations.raw_ring_sheet_cm2
    coarse_i = level_control(x.problem,x.seed,k,(;p=base,k=k25),cuts,workers,q)
    fine_i = level_control(x.problem,x.seed,k,fine,cuts,workers,q)
    return (;coarse=coarse_i,fine=fine_i,comparison=compare_arms(coarse_i,fine_i),
        initial_input_sha=x.identity["input_seed_sha256"])
end

function measured_reversal(x,y,a,b)
    sign(x) != sign(y) && abs(x)>a.error && abs(y)>b.error &&
        (abs(x)-a.error>a.tol || abs(y)-b.error>b.tol)
end

function classify_primary(differences)
    first,second = differences["K25_to_K27"],differences["K27_to_K31"]
    has_reversal(field) = let a=getproperty(first,field), b=getproperty(second,field)
        measured_reversal(a.value,b.value,a,b)
    end
    centered_reversal = any(measured_reversal(x,y,first.centered,second.centered)
        for (x,y) in zip(first.delta_centered,second.delta_centered))
    reversals = (;mean=has_reversal(:mean),centered=centered_reversal,
        input_charge=has_reversal(:input_charge),fresh_charge=has_reversal(:raw_charge))
    primary_defect = any(values(differences)) do comparison
        any(getproperty(comparison,field).status!="within" for field in (:input_charge,:raw_charge,:profile))
    end
    return (;primary_defect,reversals,unstable=primary_defect || any(values(reversals)))
end

function run_followup(p,seed,old_k,base,k25,archive_K25,retained,cuts,workers,ring_charge,levels,differences,save)
    fine = retained.arm
    path = transfer_path(p,seed,old_k,base,k25,fine,cuts,workers,ring_charge)
    path_difference = compare_arms(levels["K31"],path)
    followup = (;path,path_difference)
    save("transfer_path";followup)
    diagnosis = classify_primary(differences)
    baseline = levels["K25"].measurements
    final = levels["K31"].measurements
    window = differences["K27_to_K31"].delta_segment
    attenuated = abs(baseline.observed.delta_segment)-abs(final.observed.delta_segment) >
        window.tol + baseline.uncertainty.delta_segment + final.uncertainty.delta_segment
    substantial = abs(final.observed.delta_segment)>window.tol ||
        final.observed.max_deviation>window.tol
    charge_window = window_charge_difference(archive_K25,retained)
    local_feature = any(i->max(abs(charge_window.input[i]),abs(charge_window.fresh[i])) >
        0.1target_charge_tolerance,charge_window.candidates)
    followup = merge(followup,(;diagnosis,attenuated,substantial,local_feature))
    if local_feature && !diagnosis.unstable
        loc = spectral_check(archive_K25,retained,cuts,levels,"K31")
        followup = merge(followup,(;localization_K31=loc))
        save("energy_localization";followup)
    end
    GC.gc()
    followup = if diagnosis.unstable
        shifted = load_arm(base,"K31_shift")
        retained_shift = level_control(p,seed,old_k,shifted,cuts,workers,ring_charge;retain=true)
        levels["K31_shift"] = retained_shift.report
        differences["K31_to_shift"] = compare_arms(levels["K31"],levels["K31_shift"])
        save("shifted";followup)
        loc = spectral_check(archive_K25,retained,cuts,levels,"K31")
        save("energy_localization";followup=merge(followup,(;localization_K31=loc)))
        loc_shift = spectral_check(archive_K25,retained_shift,cuts,levels,"K31_shift")
        merge(followup,(;choice="shifted_nodes",localization_K31=loc,localization_shifted=loc_shift))
    elseif attenuated || !substantial
        merge(followup,(;choice="second_history",second_history=second_history(p,base,k25,fine,cuts,workers)))
    else
        merge(followup,(;choice="rank",rank=rank_control(retained,cuts,workers)))
    end
    save("completed";followup)
end
