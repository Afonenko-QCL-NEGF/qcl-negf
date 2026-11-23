include("radial_control.jl")
const T = FathRadialControl
const LT = T.LT
using LinearAlgebra

const REPLAY_STEPS = 48
const ALPHA = 0.35
const NODES_NM_INVERSE = (suspect=0.175, control=0.275)

function source_map!(out, p, source, workers)
    normalized = T.normalized_radial_occupation(p,source,workers)
    LT.scatter_packed!(out,normalized.occupation,p.v)
    return normalized.normalization
end

function replay_source!(p, seed, workers, announce)
    fresh = similar(seed)
    for step in 1:REPLAY_STEPS-1
        start = time_ns()
        normalization = source_map!(fresh,p,seed,workers)
        if step==1
            full = T.map_radial(p,seed,workers)
            T.normalize_replay((;normalization),full.summary)
            short_sha,full_sha = T.packed_sha(fresh),T.packed_sha(full.source)
            source_only_bitwise = short_sha==full_sha
            announce((;step,short_sha,full_sha,source_only_bitwise))
            source_only_bitwise || error("source-only map #1 differs from the full Core map")
            full = nothing
            GC.gc(false)
        end
        seed .= (1-ALPHA) .* seed .+ ALPHA .* fresh
        announce((;step,elapsed_s=(time_ns()-start)*1e-9))
    end
    return seed
end

function checked_replay(p, seed, cuts, workers, archived)
    input_sha = T.packed_sha(seed)
    image = T.map_radial(p,seed,workers)
    image_sha = T.packed_sha(image.source)
    reference_hashes = archived["fields_sha256"]
    checks = (; input_matches=input_sha == reference_hashes["coarse_input"],
        image_matches=image_sha == reference_hashes["coarse_image"])
    metrics = T.linked_metrics(image.summary,T.widths_at(cuts))
    native_input = T.input_stage(image.summary)
    baseline = archived["coarse_metrics"]
    tolerance = (; rK=1e-8,rSigma=1e-8,raw_lambda=1e-9,input_raw_lambda=1e-9,
        maximum_profile_A_cm2=1e-5)
    delta = (; rK=metrics.rK-baseline["rK"],rSigma=metrics.rSigma-baseline["rSigma"],
        raw_lambda=metrics.raw_lambda-baseline["raw_lambda"],
        input_raw_lambda=native_input.raw_lambda-archived["native_inputs"]["coarse"]["raw_lambda"],
        maximum_profile_A_cm2=maximum(abs,metrics.current_profile_A_cm2.-baseline["current_profile_A_cm2"]))
    numerical_match = all(abs.(collect(values(delta))).<=collect(values(tolerance)))
    reported_replay = (; checks..., input_sha,image_sha,numerical_match,delta,tolerance,metrics,native_input)
    return reported_replay
end

function node_omission(pair, coarse_archive, radius)
    coarse, fine = pair.p,pair.f
    j = findfirst(x->isapprox(x/10,radius;atol=1e-14,rtol=0.),pair.kf)
    !isnothing(j) && !(j in pair.common) && 1<j<fine.nk ||
        error("omission must select exactly one additional interior ring")
    keep = filter(!=(j),collect(1:fine.nk))
    new_k = pair.kf[keep]
    edges = [first(new_k); (new_k[1:end-1] .+ new_k[2:end])./2; last(new_k)].^2
    new_w = diff(edges)./(4π)
    prolongation = T.annular_transfer(pair.k,new_k,coarse.wk,new_w)
    same_retained_rows = prolongation==pair.p_to_f[keep,:]
    same_retained_rows || error("remaining nodes changed their conservative prolongation")
    common = [searchsortedfirst(new_k,k) for k in pair.k]
    new_k[common]==pair.k || error("omission dropped a common node")
    v = fine.v
    nfaces = size(v.interface_probes,1)
    ifr_sites = T.Runner._read_linked_array(coarse_archive,"ifr_sites",Float64,nfaces,fine.nz)
    contracted = LT.LocalCollisionKernels(v.coordinate_frame,new_w,v.acoustic,v.alloy,
        ifr_sites,v.interface_pair[keep,keep],@view(v.lo_covariance[:,:,keep,keep]),
        @view(v.impurity_covariance[:,:,keep,keep]),v.lo_plus,v.lo_minus,v.bose)
    p = LT.LinkedProblem(fine.en,fine.we,new_w,fine.geo.modes,fine.nb,fine.geo.offsets,
        fine.geo.voltage,fine.geo.reach,fine.h[:,:,keep],fine.hops[:,keep],fine.const_by_channel[:,:,keep,:],
        contracted;spin_degeneracy=fine.spin_degeneracy,current_scale=fine.current_scale,
        density_scale=fine.density_scale,target_dimless=fine.target_dimless)
    return (; p=coarse,f=p,common,keep,omitted_index=j,
        omitted_radius_nm_inverse=radius,k=new_k,p_to_f=prolongation,same_retained_rows)
end

function native_comparison(row, baseline, cuts)
    profile = row.current_profile_A_cm2 .- baseline["current_profile_A_cm2"]
    mean = row.spatial.mean_internal_A_cm2-baseline["spatial"]["mean_internal_A_cm2"]
    imax = argmax(abs.(profile))
    return (; maximum_profile_A_cm2=abs(profile[imax]),position_nm=cuts[imax],mean_A_cm2=mean,
        maximum_centered_A_cm2=maximum(abs,profile.-mean),
        rK=row.rK-baseline["rK"],rSigma=row.rSigma-baseline["rSigma"],
        raw_lambda=row.raw_lambda-baseline["raw_lambda"],profile_A_cm2=profile)
end

function independent_comparison(observed, baseline, cuts)
    profile = observed.current_A_cm2.-baseline["current_A_cm2"]
    mean = observed.current.mean_internal_A_cm2-baseline["current"]["mean_internal_A_cm2"]
    band_fraction = observed.central_bands.fraction.-baseline["central_bands"]["fraction"]
    imax = argmax(abs.(profile))
    return (; maximum_profile_A_cm2=abs(profile[imax]),position_nm=cuts[imax],mean_A_cm2=mean,
        maximum_centered_A_cm2=maximum(abs,profile.-mean),profile_A_cm2=profile,
        raw_sheet_cm2=observed.raw_sheet_cm2-baseline["raw_sheet_cm2"],
        band_fraction,maximum_band_fraction=maximum(abs,band_fraction))
end

function measure_omission(pair, coarse_seed, cuts, workers, archived, coarse_path, radius)
    arm = node_omission(pair,coarse_path,radius)
    prolonged = T.apply_radial(arm.p_to_f,coarse_seed)
    input_checks = T.input_transfer_checks(arm,coarse_seed,prolonged)
    source_sha = T.packed_sha(prolonged)
    image = T.map_radial(arm.f,prolonged,workers)
    metrics = T.linked_metrics(image.summary,T.widths_at(cuts))
    native_input = T.input_stage(image.summary)
    fresh_native = image.summary["projected_fresh"]
    K25_input = archived["observations"]["fine_input"]
    K13_input = archived["observations"]["coarse_input"]
    K25_q_by_ring = Float64.(K25_input["raw_ring_sheet_cm2"])
    predicted_ring_charge = K25_q_by_ring[arm.keep] .* arm.f.wk ./ pair.f.wk[arm.keep]
    projected_input = image.summary["projected_input"]
    native_ring_charge = projected_input["per_ring_raw_sheet_cm2"]
    changed = findall(i->abs(arm.f.wk[i]-pair.f.wk[arm.keep[i]])>1e-14,eachindex(arm.keep))
    input_charge = (; predicted_sheet_cm2=sum(predicted_ring_charge),
        production_sheet_cm2=native_input.raw_sheet_cm2,
        production_minus_prediction_cm2=native_input.raw_sheet_cm2-sum(predicted_ring_charge),
        production_minus_K13_GL20_cm2=native_input.raw_sheet_cm2-K13_input["raw_sheet_cm2"],
        production_minus_K25_GL20_cm2=native_input.raw_sheet_cm2-K25_input["raw_sheet_cm2"],
        removed_K25_weight=pair.f.wk[arm.omitted_index],
        removed_K25_raw_ring_sheet_cm2=K25_q_by_ring[arm.omitted_index],
        native_ring_charge,predicted_ring_charge,
        reweighted=[(;k_nm_inverse=arm.k[i]/10,
            K25_weight=pair.f.wk[arm.keep[i]],new_weight=arm.f.wk[i],
            K25_GL20_sheet_cm2=K25_q_by_ring[arm.keep[i]],
            native_sheet_cm2=native_ring_charge[i]) for i in changed])
    report = (; arm.omitted_radius_nm_inverse,retained_k_nm_inverse=arm.k./10,
        measure=sum(arm.f.wk),arm.same_retained_rows,prolonged_input_sha256=source_sha,
        fresh_source_sha256=T.packed_sha(image.source),input_checks,input_charge,metrics,native_input,
        input_raw_profile_A_cm2=projected_input["raw_profile_A_cm2"],
        fresh_raw_ring_sheet_cm2=fresh_native["per_ring_raw_sheet_cm2"],
        collision_balance=image.summary["fresh_channel_balance"],
        relative_to_K13=native_comparison(metrics,archived["coarse_metrics"],cuts),
        relative_to_K25=native_comparison(metrics,archived["fine_metrics"],cuts))
    return (; report,p=arm.f,source=image.source)
end

function run_node_replay(coarse_path, fine_path, archived_path, output, workers, control_gl20)
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    Base.include(T,joinpath(@__DIR__,"radial_mechanism.jl"))
    archived = T.Runner.YAML.load_file(archived_path; dicttype=Dict{String,Any})
    archived["stage"]=="completed" && archived["coarse_iteration"]==REPLAY_STEPS ||
        error("expected the completed matched radial branch on map #48")
    cfg = (;schema="qcl-negf-fath-radial-node-omission/v1",replay_steps=REPLAY_STEPS,alpha=ALPHA,workers,
        control_gl20,NODES_NM_INVERSE,source_sha256=T.file_sha(@__FILE__),
        replayed_core=T.Runner._linked_package_identity(T.Runner.QCLNEGF),
        replayed_runner=T.Runner._linked_package_identity(T.Runner),
        app_revision=readchomp(Cmd(["git","-C",dirname(dirname(T.STUDY)),"rev-parse","HEAD"])),
        accepted_C_report_sha256=T.file_sha(archived_path))
    initial = T.Runner._read_linked_checkpoint(coarse_path)
    p, cuts = initial.problem, initial.current_midpoints
    cuts == archived["cuts_nm"] || error("map-48 replay changed the observation cuts")
    T.file_sha(joinpath(coarse_path,"spec.toml")) == archived["coarse_archive_spec_sha256"] ||
        error("coarse archive does not match the previous C result")
    T.radial_write(output,(;stage="replay",cfg,cuts_nm=cuts,identity=initial.identity))
    function announce(event)
        T.Runner._light_json(stderr,event)
        println(stderr)
        flush(stderr)
    end
    seed = Base.invokelatest(replay_source!,p,initial.seed,workers,announce)
    replay = checked_replay(p,seed,cuts,workers,archived)
    equivalent = replay.input_matches && replay.image_matches
    comparison_label = if equivalent
        "bitwise_replay"
    elseif replay.numerical_match
        "numerically_matched_replay"
    else
        "replay_mismatch"
    end
    T.radial_write(output,(;stage="coarse_replayed",cfg,cuts_nm=cuts,replay,comparison_label))
    equivalent || replay.numerical_match || error("replayed map #48 did not reproduce the archived C arm")
    announce((;phase="coarse_replayed",replay.input_matches,replay.image_matches,replay.delta))
    pair = T.radial_setup(p,cuts,coarse_path,fine_path)
    pair.fine_identity["id"] == archived["fine_identity"]["id"] ||
        error("fine archive does not match the previous C result")
    GC.gc(false)
    results = Dict{String,Any}()
    arms = map(keys(NODES_NM_INVERSE)) do label
        radius = getproperty(NODES_NM_INVERSE,label)
        arm = measure_omission(pair,seed,cuts,workers,archived,coarse_path,radius)
        results[string(label)] = arm.report
        T.radial_write(output,(;stage="native_arms",cfg,cuts_nm=cuts,replay,comparison_label,results))
        announce((;phase=String(label),omitted_radius_nm_inverse=radius,
            observed_input_cm2=arm.report.native_input.raw_sheet_cm2,
            arm.report.metrics.rK,arm.report.metrics.rSigma,
            profile=arm.report.metrics.spatial))
        GC.gc(false)
        return arm
    end
    for (i,(label,arm)) in enumerate(zip(keys(NODES_NM_INVERSE),arms))
        i>1 && !control_gl20 && break
        observed = T.radial_observe(arm.p,arm.source,cuts,workers)
        contrast = (; relative_to_K13=independent_comparison(observed,
                archived["observations"]["coarse_observed"],cuts),
            relative_to_K25=independent_comparison(observed,
                archived["observations"]["fine_after_prolong_map"],cuts),
            max_native_difference_A_cm2=maximum(abs,observed.current_A_cm2.-arm.report.metrics.current_profile_A_cm2))
        results[string(label)] = merge(arm.report,(;observation_GL20=observed,contrast_GL20=contrast))
        T.radial_write(output,(;stage="independent_observation",cfg,cuts_nm=cuts,replay,comparison_label,results))
        announce((;phase="GL20",arm=String(label),contrast.max_native_difference_A_cm2))
        GC.gc(false)
    end
    T.radial_write(output,(;stage="completed",cfg,cuts_nm=cuts,replay,comparison_label,results))
end

if abspath(PROGRAM_FILE)==abspath(@__FILE__)
    length(ARGS) in (5,6) ||
        error("Usage: radial_node_replay.jl COARSE_ARCHIVE FINE_ARCHIVE ACCEPTED_C_JSON OUTPUT WORKERS [skip-control-GL20]")
    length(ARGS)==5 || ARGS[6]=="skip-control-GL20" || error("unexpected control observer option")
    run_node_replay(ARGS[1:4]...,parse(Int,ARGS[5]),length(ARGS)==5)
end
