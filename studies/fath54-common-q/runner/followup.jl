function second_seed(result, pair, cuts)
    archive_path = joinpath(dirname(coarse_path),"linked-E481x13-norm-alpha020-step0002")
    other = T.Runner._read_linked_checkpoint(archive_path)
    other.current_midpoints==cuts || error("independent archive cuts changed")
    old_k = R.radial_coordinates(archive_path,other.problem.nk)
    first = result.problems[1]
    direct = T.apply_radial(T.annular_transfer(old_k,pair.stage.k,other.problem.wk,first.wk),other.seed)
    common = result.problems[end]
    common.geo.offsets == other.problem.geo.offsets || error("second history has different offsets")
    promoted = RC.lift_source(direct,common.v.coordinate_frame' * other.problem.v.coordinate_frame)
    return (;source=promoted.source, fingerprint=other.identity["input_seed_sha256"],
        roundtrip=promoted.roundtrip_maximum)
end

function other_history(result, pair, cuts, workers, path)
    indices = findall(n->endswith(n,"_common") ||
        (length(result.names)==3 && n=="W8_Q25"),result.names)
    initial = second_seed(result,pair,cuts)
    R.append_row(path,"second_input",(;initial.fingerprint,initial.roundtrip))
    for arm in indices
        state = copy(initial.source)
        problem,name = result.problems[arm], result.names[arm]
        matched = Int[]
        confirmations = 0
        terminal = 0
        for step in 1:48
            measured = observed_map(problem,state,"history2_"*name,step,cuts,workers,path)
            terminal = step
            confirmations = strictly_stationary(measured) ? confirmations+1 : 0
            if !isnothing(measured.observation) &&
                R.checkpoints_match(result.latest[arm].row,measured.row)
                push!(matched,step)
            end
            if confirmations>=3 || (step>=32 && !isempty(matched))
                break
            end
            R.k31_update!(state,measured.image,alpha)
            GC.gc(false)
        end
        R.append_row(path,"second_input_outcome",(;name,matched,confirmations,terminal))
    end
end

function diff_metrics(x, y)
    return (;full=maximum(abs,x.profile.-y.profile),
        centered=maximum(abs,x.centered.-y.centered),
        mean=y.mean-x.mean, segment=y.delta_segment-x.delta_segment,
        charge=y.raw_charge-x.raw_charge, seams=y.oriented_seams.-x.oriented_seams)
end

function controlled_refinement(baseline, input, name, cuts, workers, path, make_grid; levels=1:2)
    control = observed_map(baseline,input,name*"_base",1,cuts,workers,path)
    reference = control.observation.GL20
    fixed = R.observed_row(R.direct_observation(baseline,input,cuts,workers),cuts)
    for level in levels
        trial = make_grid(level)
        problem, state = trial.problem, trial.source
        mapped = R.observed_row(R.direct_observation(problem,state,cuts,workers),cuts)
        R.append_row(path,"grid_transfer",(;name,level,trial.report,
            fixed=diff_metrics(fixed,mapped),base=fixed,mapped))
        for step in 1:8
            tag = name * "_refined" * string(level)
            measurement = observed_map(problem,state,tag,step,cuts,workers,path)
            if !isnothing(measurement.observation)
                compare = R.checkpoints_match(control.row,measurement.row)
                changes = diff_metrics(reference,measurement.observation.GL20)
                R.append_row(path,"grid_contrast",(;name,level,step,compare,changes,
                    target=max(1.0,0.01abs(reference.mean))))
                # Compare the first image as well as a continued fresh image.
                step>1 && compare && break
            end
            R.k31_update!(state,measurement.image,alpha)
            GC.gc(false)
        end
    end
end

function select_probe(probes)
    energy = map(probes.energy) do x
        a,b = x.phases
        standard = x.standard.J
        evaluations = (a.J,b.J)
        differences = map(y->max(abs(y.segment-standard.segment),
            maximum(abs,y.centered.-standard.centered)),evaluations)
        spread = max(abs(a.J.segment-b.J.segment),maximum(abs,a.J.centered.-b.J.centered))
        contribution = max(abs(standard.segment),maximum(abs,standard.centered))
        return (;x.candidate,x.k_nm_inverse,contribution,
            score=min(contribution, min(differences...)), spread,
            narrowest_meV=isempty(x.poles) ? nothing : 200minimum(p->p.width,x.poles))
    end
    radial = map(probes.radial) do x
        a,b,c = x.phases
        diffs = map(y->max(abs(y.J.segment-a.J.segment),
            maximum(abs,y.J.centered.-a.J.centered)),(b,c))
        spread = max(abs(b.J.segment-c.J.segment),maximum(abs,b.J.centered.-c.J.centered))
        contribution = max(abs(a.J.segment),maximum(abs,a.J.centered))
        return (;x.k_nm_inverse,contribution,score=min(contribution,min(diffs...)),spread)
    end
    qualified = filter(x->x.candidate!="control10",energy)
    by_energy = isempty(qualified) ? nothing : last(sort(qualified;by=x->(x.score>x.spread,x.score,x.contribution)))
    by_radial = last(sort(radial;by=x->(x.score>x.spread,x.score,x.contribution)))
    return (;energy,radial,by_energy,by_radial)
end

function probe_then_test(result, pair, cuts, workers, path)
    grid = pair.stage.k
    candidates = findall(n->endswith(n,"_common") ||
        (length(result.names)==3 && n=="W8_Q25"),result.names)
    # Choose the smallest observed maximum flattening error at the
    # last matched point; if the residuals fail the two-metric rule, preserve
    # that fact and choose the smallest maximum residual for diagnosis.
    controlled = all(R.checkpoints_match(result.latest[i].row,result.latest[j].row)
        for i in candidates for j in candidates)
    index = argmin(candidates) do i
        x = result.latest[i]
        controlled ? x.observation.GL20.max_deviation : max(x.row.rK,x.row.rSigma)
    end
    problem, state, name = result.problems[index], result.states[index], result.names[index]
    choice = (;name,index,controlled,rK=result.latest[index].row.rK,rSigma=result.latest[index].row.rSigma)
    R.append_row(path,"probe_stage",(;choice,input_sha=T.packed_sha(state)))
    image = R.arm_image(problem,state,cuts,workers)
    repeated = R.fresh_row(problem,image,cuts)
    R.checkpoints_match(repeated,result.latest[index].row) ||
        error("held probe state did not reproduce the selected fresh residuals")
    probes = probe_windows(problem,image.source,grid,cuts)
    lagged = probe_windows(problem,state,grid,cuts)
    scores = select_probe(probes)
    R.append_row(path,"local_probes",(;choice,probes,lagged,scores,fresh_sha=T.packed_sha(image.source)))
    e, k = scores.by_energy, scores.by_radial
    e_detected = !isnothing(e) && e.score>e.spread
    k_detected = k.score>k.spread
    if !e_detected && !k_detected
        R.append_row(path,"registered_local_refinement",(;choice,branch="unresolved",scores))
        return choice
    end
    use_radial = k_detected && (!e_detected || k.score>e.score)
    decision = (;choice,branch=use_radial ? "radial" : "energy",
        selected=use_radial ? k : e,
        width=use_radial ? nothing : e.narrowest_meV)
    R.append_row(path,"registered_local_refinement",decision)
    if use_radial
        center = grid[argmin(abs.(grid.-10k.k_nm_inverse))]
        schemes = ((0.5,),(0.25,0.5,0.75),(0.20,0.45,0.70))
        controlled_refinement(problem,state,"local_K",cuts,workers,path,
            level -> radial_refinement(problem,state,grid,center,schemes[level]);levels=1:3)
    else
        selected = only(filter(w->w.name==e.candidate,ENERGY_WINDOWS))
        lo,hi = selected.e ./ 100
        poles = filter(x -> x.candidate==e.candidate && x.k_nm_inverse==e.k_nm_inverse, probes.energy)
        local_intervals = [(lo,hi)]
        for ring in poles, pole in ring.poles
            width = max(pole.width,0.00002)
            push!(local_intervals,(max(lo,pole.energy-3width),min(hi,pole.energy+3width)))
        end
        controlled_refinement(problem,state,"local_E",cuts,workers,path,
            level -> energy_refinement(problem,state,local_intervals,level==1 ? 4 : 8))
    end
    return choice
end

function scheme_from_fath(result, choice, path)
    rows = open(path) do io
        [T.Runner.YAML.load(line;dicttype=Dict{String,Any}) for line in eachline(io)]
    end
    eligible = findall(n->endswith(n,"_common") ||
        (length(result.names)==3 && n=="W8_Q25"),result.names)
    groups = Dict(i=>filter(r->r["kind"]=="map" && r["name"]==result.names[i] &&
        !isnothing(r["observation"]),rows) for i in eligible)
    second = Dict(i=>filter(r->r["kind"]=="second_input_outcome" &&
        r["name"]==result.names[i],rows) for i in eligible)
    gl(s) = s.observation.GL20
    candidates = map(eligible) do i
        a = result.latest[i]
        second_entry = only(second[i])
        i == choice.index || !choice.controlled || R.checkpoints_match(a.row,result.latest[choice.index].row) ||
            error("selection candidate lost residual comparability")
        earlier = groups[i][max(1,end-1)]["observation"]["GL20"]
        late = maximum(abs,gl(a).profile.-earlier["profile"])
        history = filter(r->r["kind"]=="map" && r["name"]=="history2_"*result.names[i] &&
            r["step"] in second_entry["matched"],rows)
        memory = isempty(history) ? nothing :
            maximum(abs,gl(a).centered.-last(history)["observation"]["GL20"]["centered"])
        uq = max(a.observation.uncertainty.production_GL20_profile,
            a.observation.uncertainty.GL18_GL20_profile)
        tolerance = max(1.0,0.01abs(gl(a).mean))
        score = max(gl(a).max_deviation,maximum(abs,gl(a).oriented_seams.-gl(a).mean))
        other_at_terminal = findlast(r -> r["kind"]=="map" &&
            r["name"]=="history2_"*result.names[i] && r["step"]==second_entry["terminal"],rows)
        replay_profile = isnothing(other_at_terminal) ? nothing : rows[other_at_terminal]["observation"]
        terminal_distance = isnothing(replay_profile) ? nothing :
            maximum(abs,gl(a).profile.-replay_profile["GL20"]["profile"])
        strict = result.confirmations[i]>=3 && second_entry["confirmations"]>=3 &&
            !isnothing(terminal_distance) && terminal_distance<=tolerance
        adjacent = [maximum(abs,gl(a).centered.-gl(result.latest[j]).centered) for j in eligible
            if abs(result.problems[i].nb-result.problems[j].nb)==1 &&
            R.checkpoints_match(a.row,result.latest[j].row)]
        rank_sensitivity = isempty(adjacent) ? nothing : maximum(adjacent)
        return (;i,name=result.names[i],strict,late,memory,uq,tolerance,score,
            terminal_distance,rank_sensitivity,
            residual=max(a.row.rK,a.row.rSigma),rK=a.row.rK,rSigma=a.row.rSigma,
            raw_lambda=gl(a).raw_lambda,spectral=a.row.maximum_spectral_defect)
    end
    pool = any(c.strict for c in candidates) ? filter(c->c.strict,candidates) : candidates
    choice.controlled || (pool = filter(c->c.i==choice.index || c.strict,pool))
    chosen_priority(c) = c.strict && !isnothing(c.rank_sensitivity) ? c.rank_sensitivity : c.score
    best = first(sort(pool;by=c->(isnothing(c.memory),chosen_priority(c),c.residual)))
    equivalent = filter(pool) do c
        c.i==best.i && return true
        (isnothing(c.memory) || isnothing(best.memory)) && return false
        return chosen_priority(c)-chosen_priority(best) <= c.uq+best.uq+c.late+best.late+c.memory+best.memory
    end
    chosen = first(sort(equivalent;by=c->result.problems[c.i].nb))
    native = result.problems[chosen.i]
    refinement = "base"
    level_names = ("local_K","local_E")
    for test in level_names
        comparisons = [r for r in rows if r["kind"]=="grid_contrast" && r["name"]==test &&
            r["step"]>1 && r["compare"]]
        levels = Set(r["level"] for r in comparisons)
        required_levels = test=="local_K" ? (1,2,3) : (1,2)
        length(levels)==length(required_levels) && chosen.i==choice.index || continue
        endpoint_by_level = map(required_levels) do l
            last([r for r in comparisons if r["level"]==l])
        end
        endpoints = map(endpoint_by_level) do r
            label = test*"_refined"*string(r["level"])
            measure = last(filter(x -> x["kind"]=="map" && x["name"]==label &&
                x["step"]==r["step"],rows))["observation"]["GL20"]
            score = max(measure["max_deviation"],maximum(abs,measure["oriented_seams"].-measure["mean"]))
            return (;score,centered=measure["centered"])
        end
        improvement = chosen.score - max((x.score for x in endpoints)...)
        grid_disagreement = maximum(maximum(abs,a.centered.-b.centered) for a in endpoints for b in endpoints)
        threshold = isnothing(chosen.memory) ? nothing :
            chosen.tolerance+chosen.uq+chosen.late+chosen.memory+grid_disagreement
        accepted = !isnothing(threshold) && improvement>threshold
        accepted && (refinement = test)
        R.append_row(path,"fath_grid_selection",(;test,improvement,threshold,grid_disagreement,accepted))
    end
    R.append_row(path,"fath_scheme_selection",(;chosen,candidates,choice,refinement,
        rule="strict and second-history agreement, then worst section or seam, resolving with late and start variation"))
    return (;identifier="linked_five_channel_"*chosen.name*"_"*refinement,
        Fath_W=native.nb,Fath_Q=native.r,refinement,
        base_modes=5,nb=5+native.nb-7,nz=98,
        Emin=-0.4,Emax=0.56,ne=native.ne,nk=31,angular=32,nqz=641,
        diagnostics=(;chosen,choice))
end

function observed_lo_control(result,cuts,workers,path)
    arms = findall(n->endswith(n,"_common") ||
        (length(result.names)==3 && n=="W8_Q25"),result.names)
    sort!(arms;by=i->result.problems[i].nb)
    for (a,b) in zip(arms,arms[2:end])
        x,y = result.latest[a],result.latest[b]
        R.checkpoints_match(x.row,y.row) || continue
        delta = R.profile_contrast(x.observation,y.observation)
        delta.resolved && delta.compensation || continue
        higher = result.problems[b]
        image = R.arm_image(higher,result.states[b],cuts,workers)
        R.append_row(path,"registered_LO_source_control",(;lower=result.names[a],upper=result.names[b],
            contrast=delta,source_sha=T.packed_sha(image.source),
            condition="LO and projection oppose in resolved centered contrast; compare full and Q21-restricted LO at fixed fresh G"))
        observed = R.lo_operator_control(higher,image,cuts,workers)
        R.append_row(path,"synchronized_LO_source_control",(;rank=higher.nb,observed))
        return
    end
end

function late_work(result, pair, cuts, workers, path)
    choice = probe_then_test(result,pair,cuts,workers,path)
    observed_lo_control(result,cuts,workers,path)
    other_history(result,pair,cuts,workers,path)
    R.append_row(path,"fath_data_complete",(;choice))
    Main.announce((;phase="fath_data_complete",path))
    scheme = scheme_from_fath(result,choice,path)
    return scheme
end

late_work
