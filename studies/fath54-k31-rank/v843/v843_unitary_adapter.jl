module V843RankControl
include(joinpath(Main.v843_studies,"fath-lo-rank-v843","fath_factorial.jl"))
end

include(joinpath(v843_studies, "fath54-stability-night", "transfer", "radial_control.jl"))
const RankControl = V843RankControl
const T = FathRadialControl
const v843_representation_driver = joinpath(v843_studies,"fath54-k31-rank","representation.jl")
include(v843_representation_driver)

function v843_covariant_cavities(p, original, rotated, modal)
    central = p.geo.center_modes
    overlap = modal[central,central]
    errors = zeros(3,3)
    norms = zeros(3,3)
    for k in 1:p.nk, e in 1:p.ne, side in 1:3, part in 1:3
        @views expected = overlap' * original[:,:,part,side,e,k] * overlap
        @views actual = rotated[:,:,part,side,e,k]
        w = p.weights[e,k]
        errors[part,side] += w * sum(abs2, actual.-expected)
        norms[part,side] += w * sum(abs2, expected)
    end
    return [collect(col) for col in eachcol(sqrt.(errors ./ max.(norms,floatmin(Float64))))]
end

function v843_run_unitary(saved, archive, cuts, widths, workers, path, reference)
    p, source = saved.problem,saved.seed
    sites = Runner._read_linked_array(archive,"ifr_sites",Float64,size(p.v.interface_probes,1),p.nz)
    basis = rotate_problem(p,sites)
    q = basis.rotated
    transformed = RankControl.lift_source(source,basis.coord')
    invariant_operators = (;modal=norm(basis.modal'*basis.modal-I),
        coordinate=norm(basis.coord'*basis.coord-I),
        metric=T.relerr(q.geo.metric,basis.modal'*p.geo.metric*basis.modal),
        ifr_probe=T.relerr(q.v.interface_probes,p.v.interface_probes*basis.coord),
        same_measures=p.en==q.en && p.we==q.we && p.wk==q.wk && p.hops==q.hops,
        source_roundtrip_maximum=transformed.roundtrip_maximum)
    input_probe = probe_covariance(p,basis,source,transformed.source;by_channel=true)
    diagnostic_log(path,"unitary_input_probe",(;invariant_operators,input_probe,
        same_W_rank=p.nb,same_Q_rank=p.r,representation_sha256=v843_sha(v843_representation_driver)))
    base = v843_map(p,source,workers)
    record_a = v843_record_map(path,"native_W_Q",1,source,base,widths,0)
    observation_a = v843_observation(p,base,cuts,workers,reference)
    diagnostic_log(path,"GL20",(;label="native_W_Q",step=1,record_a.input_sha,record_a.fresh_sha,
        observation=observation_a))
    modified = v843_map(q,transformed.source,workers)
    record_b = v843_record_map(path,"unitarily_rotated_W_Q",1,transformed.source,modified,widths,0)
    observation_b = v843_observation(q,modified,cuts,workers,reference)
    diagnostic_log(path,"GL20",(;label="unitarily_rotated_W_Q",step=1,record_b.input_sha,record_b.fresh_sha,
        observation=observation_b))
    emitted_original_frame = RankControl.lift_source(modified.source,basis.coord)
    radii = Runner._read_linked_array(archive,"k",Float64,p.nk)
    emitted_LG = T.packed_difference(p,emitted_original_frame.source,base.source,radii)
    emitted_RLG = probe_covariance(p,basis,base.source,modified.source;by_channel=true)
    cavity_RLG = v843_covariant_cavities(p,base.fresh.cavities,modified.fresh.cavities,basis.modal)
    contrast = v843_pair_contrast((;record_a.row,observation=observation_a),
        (;record_b.row,observation=observation_b))
    native_profile = maximum(abs,record_a.row.current_profile_A_cm2.-record_b.row.current_profile_A_cm2)
    bands_relative = max(abs(contrast.extractor_sheet_delta_cm2)/observation_a.extractor.sheet_cm2,
        abs(contrast.upper_lasing_sheet_delta_cm2)/observation_a.upper_lasing.sheet_cm2)
    closure_difference = maximum(maximum(abs,observation_a.collision_cumulative_A_cm2[k].-
        observation_b.collision_cumulative_A_cm2[k]) for k in keys(observation_a.collision_cumulative_A_cm2))
    basis_error = max(invariant_operators.modal,invariant_operators.coordinate,
        invariant_operators.metric,invariant_operators.ifr_probe)
    input_error = max(input_probe.mode_RLG,input_probe.local_RLG,input_probe.bond_current,
        input_probe.per_channel_RLG_maximum)
    emitted_LG_error = maximum(x.relative for x in values(emitted_LG))
    emitted_RLG_error = max(emitted_RLG.mode_RLG,emitted_RLG.local_RLG,emitted_RLG.bond_current,
        emitted_RLG.per_channel_RLG_maximum)
    first_difference = if !invariant_operators.same_measures || basis_error >= 2e-12
        "basis_metric_or_interface"
    elseif input_error >= 1e-6
        "input_causal_Dyson_or_current"
    elseif emitted_LG_error >= 1e-7
        "fresh_packed_collision"
    elseif emitted_RLG_error >= 1e-6 || maximum(maximum,cavity_RLG) >= 1e-7
        "fresh_causal_Dyson_or_boundary"
    elseif max(native_profile,contrast.maximum_absolute_profile_delta_A_cm2,closure_difference) >= 1e-5 ||
            bands_relative >= 1e-7
        "fresh_observable"
    else
        nothing
    end
    return (;mode="unitary", base_input_sha=record_a.input_sha, rotated_input_sha=record_b.input_sha,
        emitted_LG, emitted_RLG, cavity_RLG, contrast, native_profile, bands_relative, closure_difference,
        first_difference, passes=isnothing(first_difference), stationary_confirmations=0,
        note="one fresh map in each representation; no trajectory stationarity test")
end
