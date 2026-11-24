function matched_at_marks(history, measured)
    candidates = []
    for a in sort!(collect(keys(measured[1]))), b in sort!(collect(keys(measured[2])))
        seven,eight = history[1][a],history[2][b]
        checkpoints_match(seven,eight) || continue
        fractions = (seven.rK/history[1][1].rK,seven.rSigma/history[1][1].rSigma,
            eight.rK/history[2][1].rK,eight.rSigma/history[2][1].rSigma)
        mismatch = abs(log(seven.rK/eight.rK)) + abs(log(seven.rSigma/eight.rSigma))
        push!(candidates,(;steps=(a,b),max_relative=maximum(fractions),mismatch))
    end
    sort!(candidates;by=x->(x.max_relative,x.mismatch,abs(x.steps[1]-x.steps[2]),x.steps))
    return [(;fraction,best=let at = findfirst(x->x.max_relative<=fraction,candidates)
        isnothing(at) ? nothing : candidates[at]
    end) for fraction in (1.0,0.5,0.25,0.1)]
end

function profile_contrast(seven,eight)
    a,b = seven.GL20,eight.GL20
    physical_tolerance = max(1.0,0.01abs(a.mean))
    numerical = max(seven.uncertainty.GL18_GL20_centered,seven.uncertainty.production_GL20_centered) +
        max(eight.uncertainty.GL18_GL20_centered,eight.uncertainty.production_GL20_centered)
    pair_max_centered = maximum(abs,b.centered.-a.centered)
    sa,sb = seven.fresh.contrasts.late7,eight.fresh.contrasts.late7
    lo = sb.collisions_A_cm2["LO"]-sa.collisions_A_cm2["LO"]
    projection = sb.projection_A_cm2-sa.projection_A_cm2
    compensation = sign(lo)!=sign(projection) && min(abs(lo),abs(projection))>max(0.1,numerical)
    return (;pair_max_centered,physical_tolerance,numerical,lo,projection,compensation,
        resolved=pair_max_centered-numerical>physical_tolerance,
        charge_difference_cm2=b.raw_charge-a.raw_charge,lambda_difference=b.raw_lambda-a.raw_lambda)
end

function measured_contrast(history, measured, step)
    earlier = step-8
    rate(arm,metric) = getproperty(history[arm][step],metric) /
        getproperty(history[arm][earlier],metric)
    plateau_metrics = [metric for metric in (:rK,:rSigma)
        if all(rate(arm,metric)>0.75 && getproperty(history[arm][step],metric)>1e-4 for arm in 1:2)]
    rates = [(;rank=arm+6,rK_factor=rate(arm,:rK),rSigma_factor=rate(arm,:rSigma),
        fixed_segment_reduction_A_cm2=abs(measured[arm][earlier].GL20.delta_segment)-
            abs(measured[arm][step].GL20.delta_segment)) for arm in 1:2]
    progress = all(r.rK_factor<=0.75 && r.rSigma_factor<=0.75 &&
        r.fixed_segment_reduction_A_cm2>0.1 for r in rates)
    common_steps = intersect(keys(measured[1]),keys(measured[2]))
    repeated = [(;at,contrast...) for at in sort!(collect(common_steps))
        if at>1 && checkpoints_match(history[1][at],history[2][at]) &&
            all(history[arm][at].rK < 0.5 * history[arm][1].rK &&
                history[arm][at].rSigma < 0.5 * history[arm][1].rSigma for arm in 1:2)
        for contrast in (profile_contrast(measured[1][at],measured[2][at]),)
        if contrast.resolved]
    compensated = filter(x->x.compensation,repeated)
    unitary_trigger = length(repeated)>=2 && last(repeated).at==step
    operator_trigger = length(compensated)>=2 && last(compensated).at==step &&
        sign(last(compensated).lo)==sign(compensated[end-1].lo)
    return (;step,earlier,rates,plateau=!isempty(plateau_metrics),plateau_metrics,
        advances_toward_stationarity=progress,matched=matched_at_marks(history,measured),
        operator_trigger,unitary_trigger,repeated,compensated)
end

function same_input_control(pair, images, cuts, workers, path, branch_step)
    comparisons = NamedTuple[]
    for (problem,input,image) in zip(pair.problems,pair.seeds,images)
        common_input_sha = T.packed_sha(input)
        common_image_sha = T.packed_sha(image.source)
        input_row = fresh_row(problem,image,cuts)
        endpoints = NamedTuple[]
        for alpha in (K31_ALPHA,1.0)
            state = copy(input)
            k31_update!(state,image,alpha)
            for forward_step in 1:4
                start = time_ns()
                trial = arm_image(problem,state,cuts,workers)
                row = fresh_row(problem,trial,cuts)
                append_row(path,"update_control",(;branch_step,forward_step,rank=problem.nb,
                    alpha,common_input_sha,common_image_sha,row,seconds=(time_ns()-start)*1e-9))
                forward_step==4 && push!(endpoints,(;alpha,row.rK,row.rSigma,row.fixed_segment_A_cm2))
                k31_update!(state,trial,alpha)
            end
        end
        mixed,pure = endpoints
        pure_improves = pure.rK <= 0.75 * min(mixed.rK,input_row.rK) &&
            pure.rSigma <= 0.75 * min(mixed.rSigma,input_row.rSigma) &&
            abs(pure.fixed_segment_A_cm2) < abs(input_row.fixed_segment_A_cm2)-0.1
        push!(comparisons,(;rank=problem.nb,mixed,pure,pure_improves))
        GC.gc()
    end
    adopt_pure = all(c.pure_improves for c in comparisons)
    return (;branch_step,comparisons,adopt_pure)
end

function modal_pieces(frame, operator, shared, added)
    common = @view frame[:,shared]
    extra = @view frame[:,added]
    a = common * operator[shared,shared] * common'
    b = extra * operator[added,added] * extra'
    cross = common * operator[shared,added] * extra' +
        extra * operator[added,shared] * common'
    return (;common=a,added=b,cross)
end

function cut_pair_terms(h, lesser, cuts, monitor, nz)
    function at(index)
        face = first(monitor)+index-1
        values = zeros(3)
        for j in (face+1):size(h,1), i in 1:face
            part = j==i+1 ? 1 : (fld(i-1,nz)==fld(j-1,nz) ? 2 : 3)
            values[part] += 2real(h[i,j]*lesser[j,i])
        end
        return values
    end
    a,b = (argmin(abs.(cuts.-z)) for z in fixed_cuts)
    return at(b)-at(a)
end

function lo_operator_control(p, image, cuts, workers)
    RC = RankControl
    lo = only(findall(==(:LO),LT.COLLISION_CHANNELS))
    shared = vcat([collect(first(range):(last(range)-1)) for range in p.geo.block_ranges]...)
    added = last.(p.geo.block_ranges)
    energy_rule = RC.independent_energy_rule
    dual = Matrix(inv(Hermitian(p.geo.metric)))
    center = @view p.geo.modes[(first(p.geo.monitor)+1):(last(p.geo.monitor)-1),:]
    center_metric = center' * center
    state_total = dropdims(sum(image.source;dims=5);dims=5)
    anchor = dropdims(sum(p.const_by_channel;dims=4);dims=4)
    output = Vector{Any}(undef,p.nk)
    a,b = (argmin(abs.(cuts.-z)) for z in fixed_cuts)
    LT.N._production_worker_ranges!(p.nk,min(workers,p.nk)) do _,first_ring,last_ring
        for k in first_ring:last_ring
            r = RC.SpatialBalance.ring_balance(p,state_total,anchor,image.source,
                dual,center_metric,false,energy_rule,nothing,k)
            local_lo = modal_pieces(center[a:b-1,:],r.contributions[lo],shared,added)
            lo_partition = Dict(name=>p.current_scale*real(tr(x)) for (name,x) in pairs(local_lo))
            local_projection = p.current_scale * (r.current[b]-r.current[a])
            lhs = modal_pieces(p.geo.modes,dual*p.h[:,:,k]*dual,shared,added)
            rhs = modal_pieces(p.geo.modes,im .* r.occupation,shared,added)
            hamiltonian = Dict("$(key_h)_$(key_g)"=>p.current_scale.*
                cut_pair_terms(h,g,cuts,p.geo.monitor,p.nz)
                for (key_h,h) in pairs(lhs) for (key_g,g) in pairs(rhs))
            lo_total = p.current_scale * sum(RC.SpatialBalance.diagonal_in_coordinates(
                r.contributions[lo],center)[a:b-1])
            flux = vec(sum(hcat(values(hamiltonian)...);dims=2))
            full_flux = p.current_scale .* cut_pair_terms(sum(values(lhs)),sum(values(rhs)),
                cuts,p.geo.monitor,p.nz)
            output[k] = (;k,lo_total,lo_partition,hamiltonian,flux,
                lo_partition_error=abs(sum(values(lo_partition))-lo_total),
                flux_partition_error=maximum(abs,flux.-full_flux),
                projection=local_projection-sum(flux))
        end
    end
    chosen = sort!(sortperm(abs.([r.lo_total for r in output]);rev=true)[1:2])
    fresh_lo = @view image.source[:,:,:,:,lo]
    lo_constant = @view p.const_by_channel[:,:,:,lo]
    # The first columns of Q25 are the archived Q21. Restrict the LO source
    # (including its causal anchor) with P21 while holding full-rank G fixed.
    restricted = zeros(Float64,size(fresh_lo))
    restricted_constant = zeros(ComplexF64,size(lo_constant))
    oldq = 1:21
    mat = zeros(ComplexF64,p.r,p.r)
    for k in chosen
        @views restricted_constant[oldq,oldq,k] .= lo_constant[oldq,oldq,k]
        for e in 1:p.ne, c in 1:2
            @views LT.unpack_hermitian!(mat,fresh_lo[:,c,e,k])
            mat[22:end,:] .= 0
            mat[:,22:end] .= 0
            @views LT.pack_hermitian!(restricted[:,c,e,k],mat)
        end
    end
    control = map(chosen) do k
        full = RC.split_lo_ring(p,state_total,anchor,fresh_lo,lo_constant,dual,center,cuts,energy_rule,k)
        projected_lo = RC.split_lo_ring(p,state_total,anchor,restricted,restricted_constant,
            dual,center,cuts,energy_rule,k)
        independent_error = full.contrasts.late7.total_A_cm2-output[k].lo_total
        maximum(abs,(independent_error,full.maximum_closure_error_A_cm2,
            projected_lo.maximum_closure_error_A_cm2)) < 1e-7 ||
            error("independent LO split did not close at ring $k")
        return (;k,full,projected_lo,independent_error,
            delta=full.contrasts.late7.total_A_cm2-projected_lo.contrasts.late7.total_A_cm2)
    end
    maximum(max(r.lo_partition_error,r.flux_partition_error) for r in output) < 1e-7 ||
        error("modal decomposition did not reproduce the spatial balance")
    return (;green_source="synchronized_fresh",common_G_source_sha=T.packed_sha(image.source),
        by_ring=output,control)
end

function independently_stationary(observation)
    gl20 = observation.GL20
    tolerance = max(1.0,0.01abs(gl20.mean))
    return gl20.max_deviation<=tolerance && observation.lagged.weighted_rK_Q<1e-8 &&
        observation.uncertainty.production_GL20_profile<=tolerance
end

function verify_second_history(pair,cuts,workers,path,alpha)
    second_path = get(ENV,"FATH_SECOND_HISTORY",
        joinpath(dirname(coarse_path),"linked-E481x13-norm-alpha020-step0002"))
    other = T.Runner._read_linked_checkpoint(second_path)
    other.current_midpoints==cuts || error("independent archive cuts changed")
    old_k = radial_coordinates(second_path,other.problem.nk)
    stages = pair.problems
    direct = T.apply_radial(T.annular_transfer(old_k,pair.stage.k,other.problem.wk,stages[1].wk),other.seed)
    embedding = stages[2].v.coordinate_frame' * stages[1].v.coordinate_frame
    other_seeds = (direct,RankControl.lift_source(direct,embedding).source)
    return map(stages,other_seeds) do problem,state
        confirmations = 0
        for step in 1:96
            image = arm_image(problem,state,cuts,workers)
            row = fresh_row(problem,image,cuts)
            confirmations = T.strictly_qualified(row) ? confirmations+1 : 0
            append_row(path,"second_history",(;rank=problem.nb,step,row,
                strict_confirmations=confirmations,archive_seed_sha=other.identity["input_seed_sha256"]))
            if confirmations>=3 || step==96
                observation = observe_k31(problem,state,image,row,cuts,workers)
                append_row(path,"second_history_GL20",(;rank=problem.nb,step,observation))
                independent = independently_stationary(observation)
                if (independent && confirmations>=3) || step==96
                    GC.gc(false)
                    return (;rank=problem.nb,step,confirmations,independent,observation)
                end
            end
            k31_update!(state,image,alpha)
        end
    end
end
