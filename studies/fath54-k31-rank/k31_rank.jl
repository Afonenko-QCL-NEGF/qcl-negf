# Continuation loaded by the published local replay driver after map 48.
module K31RankExperiment
const T = Main.T
const LT = Main.LT
const announce = Main.announce
const coarse_path, fine_path, archived_path = ARGS[2:4]
using LinearAlgebra

module K31Radial
const T = Main.T
const LT = Main.LT
const announce = Main.announce
const coarse_path, fine_path, archived_path = ARGS[2:4]
using LinearAlgebra
const prior = joinpath(dirname(@__DIR__), "fath54-local-radial")
include(joinpath(prior, "refinement.jl"))
include(joinpath(prior, "observe_direct.jl"))
end

using .K31Radial: RankControl, direct_observation, observed_row, arm_image,
    load_arm, radial_coordinates, transfer_arm, fixed_cuts

const K31_STEPS = (1, 4, 8, 12, 16, 24)
const K31_ALPHA = 0.35
const K31_RESIDUAL_RATIO = 1.25

function append_row(path, kind, payload)
    open(path,"a") do io
        T.Runner._light_json(io,(;kind,payload...))
        println(io)
    end
end

function section_jump(cuts, profile, positions=fixed_cuts)
    a,b = (argmin(abs.(cuts .- z)) for z in positions)
    return profile[b]-profile[a]
end

function fresh_row(p, image, cuts)
    r = T.linked_metrics(image.summary,T.widths_at(cuts))
    j = r.current_profile_A_cm2
    return (;r...,centered_A_cm2=j .- r.spatial.mean_internal_A_cm2,
        oriented_seams_A_cm2=j[[1,end]],
        fixed_segment_A_cm2=section_jump(cuts,j),
        second_segment_A_cm2=section_jump(cuts,j,RankControl.FATH_LATE8_CUTS_NM),
        input=T.input_stage(image.summary))
end

function checkpoints_match(x, y)
    factor(a,b) = max(a,b)/max(min(a,b),floatmin(Float64))
    return max(factor(x.rK,y.rK),factor(x.rSigma,y.rSigma)) <= K31_RESIDUAL_RATIO
end

function audit_expansion(seven, eight)
    a,b = seven.v,eight.v
    common = [first(range):(first(range)+seven.nb-1) for range in eight.geo.block_ranges]
    shared_modes = vcat(collect.(common)...)
    embedding = b.coordinate_frame' * a.coordinate_frame
    orthogonality = norm(embedding' * embedding-I)
    frame_error = T.relerr(b.coordinate_frame*embedding,a.coordinate_frame)
    prefix_frame_error = T.relerr(b.coordinate_frame[:,1:seven.r],a.coordinate_frame)
    common_mode_error = T.relerr(eight.geo.modes[:,shared_modes],seven.geo.modes)
    anchors = [T.relerr(embedding' * eight.const_by_channel[:,:,k,c] * embedding,
        seven.const_by_channel[:,:,k,c]) for k in 1:seven.nk, c in eachindex(LT.COLLISION_CHANNELS)]
    anchor_error = maximum(anchors)
    max(frame_error,prefix_frame_error,orthogonality,common_mode_error,anchor_error) < 2e-12 ||
        error("extended frame, modes or causal anchor changed their restriction")
    seven.en == eight.en && seven.we == eight.we && seven.wk == eight.wk &&
        seven.hops == eight.hops && seven.geo.offsets == eight.geo.offsets &&
        seven.geo.voltage == eight.geo.voltage && seven.geo.reach == eight.geo.reach &&
        seven.spin_degeneracy == eight.spin_degeneracy && seven.current_scale == eight.current_scale &&
        seven.density_scale == eight.density_scale && seven.target_dimless == eight.target_dimless ||
        error("different physical measures")
    common_physics = (:acoustic,:alloy,:interface_pair,:lo_covariance,:impurity_covariance,
        :lo_plus,:lo_minus,:bose)
    all(getproperty(a,key)==getproperty(b,key) for key in common_physics) ||
        error("a physical channel changed")
    return (;orthogonality,frame_error,prefix_frame_error,common_mode_error,anchor_error,
        shared_modes,coordinate_channel_data_equal=common_physics,
        kernel_channels=LT.COLLISION_CHANNELS)
end

function check_baseline(stage, before, image, observed)
    refs = T.Runner.YAML.load_file(joinpath(K31Radial.prior,"evidence","measurements.json");
        dicttype=Dict{String,Any})
    ref = refs["levels"]["K31"]
    stage.p.wk == ref["w"] && stage.k./10 == ref["k_nm_inverse"] ||
        error("the primary K31 measure changed")
    expected = ref["measurements"]["observed"]
    checks = (;transfer_matches=T.packed_sha(before)==ref["input_sha"],
        image_matches=T.packed_sha(image.source)==ref["fresh_sha"],
        mean=observed.mean-expected["mean"],max_deviation=observed.max_deviation-expected["max_deviation"],
        fixed_segment=observed.delta_segment-expected["delta_segment"],
        maximum_profile=maximum(abs,observed.profile.-expected["profile"]))
    checks.transfer_matches && checks.image_matches && checks.maximum_profile<1e-5 ||
        error("primary K31 map 1 did not reproduce the archived baseline: $(checks)")
    return checks
end

function observe_k31(p, before, image, row, cuts, workers; baseline=nothing)
    gl20 = observed_row(direct_observation(p,image.source,cuts,workers),cuts)
    check = isnothing(baseline) ? nothing : check_baseline(baseline,before,image,gl20)
    !isnothing(check) && announce((;phase="baseline_K31",check))
    gl18 = observed_row(direct_observation(p,image.source,cuts,workers;high_order=false),cuts)
    lagged = RankControl.observe_balance(p,before,image,cuts,workers;
        fresh_profile=false,lo_control=false).lagged
    fresh_all = RankControl.observe_balance(p,image.source,image,cuts,workers;
        fresh_profile=false,lo_control=false).lagged
    # The independent kinetic residual with the input pair coefficients belongs to
    # the lagged equation only. On the fresh state its synchronized remainder is
    # checked by the signed spatial closure instead.
    fresh = Base.structdiff(fresh_all,(;weighted_rK_Q=nothing))
    uncertainty = (;production_GL20_profile=maximum(abs,row.current_profile_A_cm2.-gl20.profile),
        production_GL20_centered=maximum(abs,row.centered_A_cm2.-gl20.centered),
        GL18_GL20_profile=maximum(abs,gl18.profile.-gl20.profile),
        GL18_GL20_centered=maximum(abs,gl18.centered.-gl20.centered),
        GL18_GL20_charge=abs(gl18.raw_charge-gl20.raw_charge),
        production_GL20_charge=abs(row.raw_sheet_cm2-gl20.raw_charge),
        GL18_GL20_mode_fractions=abs.(gl18.mode_fractions.-gl20.mode_fractions),
        independent_accumulation=maximum(abs,fresh.current_A_cm2.-gl20.profile),
        lagged_production_GL20_profile=maximum(abs,lagged.current_A_cm2.-
            image.summary["projected_input"]["raw_profile_A_cm2"]))
    return (;GL20=gl20,GL18=gl18,uncertainty,fresh,lagged,baseline=check,
        input_sha=T.packed_sha(before),fresh_sha=T.packed_sha(image.source))
end

function k31_update!(seed, image, alpha)
    seed .= (1-alpha) .* seed .+ alpha .* image.source
    return nothing
end

function make_k31_pair(p, seed, cuts, workers)
    archives = T.radial_setup(p,cuts,coarse_path,fine_path)
    stage = load_arm(archives.f,"K31")
    old_k = radial_coordinates(coarse_path,p.nk)
    archive = T.Runner.YAML.load_file(archived_path;dicttype=Dict{String,Any})
    archive = get(archive,"radial",archive)
    charge = Float64.(archive["observations"]["coarse_input"]["raw_ring_sheet_cm2"])
    transferred = transfer_arm(p,old_k,seed,stage.p,stage.k,charge)
    spec = T.TOML.parsefile(joinpath(fine_path,"spec.toml"))
    expanded = RankControl.expand(stage.p,stage.k,transferred.mapped,fine_path,
        ENV["FATH_BDD"],spec["source_model_sha"])
    base,ext = stage.p,expanded.problem
    (base.ne,base.nk,base.nb,base.r,ext.ne,ext.nk,ext.nb,ext.r,length(cuts)) ==
        (481,31,7,21,481,31,8,25,145) || error("unexpected pair dimensions")
    verify = audit_expansion(base,ext)
    evidence = (;radii_nm_inverse=stage.k./10,weights=base.wk,cuts,
        coarse_K13=archive["coarse_metrics"],coarse_K13_GL20=archive["observations"]["coarse_observed"],
        transfer=transferred.report,
        source_hashes=(;seven=T.packed_sha(transferred.mapped),eight=T.packed_sha(expanded.source)),
        expansion=(;expanded.metric_error,expanded.h_error,expanded.common_error,
            expanded.roundtrip_maximum,verify))
    return (;stage,problems=(base,ext),seeds=(transferred.mapped,expanded.source),evidence)
end

include("controls.jl")
include("representation.jl")

function run_k31_rank(p, seed, cuts, workers, replay, path)
    replay.input_matches && replay.image_matches || error("expected bitwise map 48 reproduction")
    pair = make_k31_pair(p,seed,cuts,workers)
    app = ENV["FATH_APP"]
    inputs = (;coarse_spec_sha256=T.file_sha(joinpath(coarse_path,"spec.toml")),
        fine_spec_sha256=T.file_sha(joinpath(fine_path,"spec.toml")),
        BDD_sha256=T.file_sha(ENV["FATH_BDD"]),
        replay_evidence_sha256=T.file_sha(archived_path),
        physical_builder_sha256=T.file_sha(K31Radial.static_builder),
        radial_builder_sha256=T.file_sha(joinpath(K31Radial.prior,"physical_kernels.py")),
        night_observer_sha256=T.file_sha(joinpath(dirname(dirname(ARGS[1])),
            "balance","observe_balance.jl")))
    append_row(path,"configuration",(;pair.evidence...,replay,workers,
        marks=K31_STEPS,alpha=K31_ALPHA,ratio=K31_RESIDUAL_RATIO,
        inputs,
        app_revision=readchomp(`git -C $app rev-parse HEAD`),
        core=T.Runner._linked_package_identity(T.Runner.QCLNEGF),
        runner=T.Runner._linked_package_identity(T.Runner),
        runtime=T.Runner._runtime_toolchain_provenance(),
        sources=Dict(name=>T.file_sha(joinpath(@__DIR__,name))
            for name in ("k31_rank.jl","controls.jl","representation.jl","protocol.md"))))
    announce((;phase="K31_pair_ready",pair.evidence.expansion))
    GC.gc()
    history = (NamedTuple[],NamedTuple[])
    measured = (Dict{Int,Any}(),Dict{Int,Any}())
    confirmations = zeros(Int,2)
    alpha = K31_ALPHA
    switched_step = 0
    plateau_checked = false
    operator_checked = false
    representation = nothing
    for step in Iterators.countfrom(1)
        images = map(eachindex(pair.problems)) do arm
            problem,state = pair.problems[arm],pair.seeds[arm]
            start = time_ns()
            image = arm_image(problem,state,cuts,workers)
            row = fresh_row(problem,image,cuts)
            push!(history[arm],row)
            confirmations[arm] = T.strictly_qualified(row) ? confirmations[arm]+1 : 0
            append_row(path,"map",(;rank=problem.nb,step,alpha,row,
                strict_confirmations=confirmations[arm],seconds=(time_ns()-start)*1e-9,
                maxrss_bytes=Sys.maxrss(),channel_balance=image.summary["fresh_channel_balance"]))
            return image
        end
        if step in K31_STEPS || (step>24 && step%8==0) || minimum(confirmations)>=3
            for arm in eachindex(pair.problems)
                problem,state = pair.problems[arm],pair.seeds[arm]
                image,row = images[arm],last(history[arm])
                observation = observe_k31(problem,state,image,row,cuts,workers;
                    baseline=(step==1 && arm==1) ? pair.stage : nothing)
                measured[arm][step] = observation
                append_row(path,"GL20",(;rank=problem.nb,step,observation))
                announce((;phase="K31_observed",rank=problem.nb,step,
                    delta_J_A_cm2=observation.GL20.delta_segment,observation.uncertainty))
            end
        end
        if minimum(confirmations)>=3 && all(independently_stationary(m[step]) for m in measured)
            second = verify_second_history(pair,cuts,workers,path,alpha)
            agreement = map(eachindex(second)) do arm
                a,b = measured[arm][step].GL20,second[arm].observation.GL20
                difference = maximum(abs,a.profile.-b.profile)
                tolerance = max(1.0,0.01abs(a.mean))
                return (;second[arm].rank,second_step=second[arm].step,second[arm].confirmations,
                    second[arm].independent,difference,tolerance,
                    reproduced=second[arm].confirmations>=3 && second[arm].independent &&
                        difference<=tolerance)
            end
            reproduced = all(result.reproduced for result in agreement)
            append_row(path,"completed",(;step,reason="primary_three_fresh_confirmations",
                confirmations,reproduced,agreement))
            return
        end
        if step>=24 && step%8==0
            past = measured_contrast(history,measured,step)
            append_row(path,"assessment",past)
            if past.unitary_trigger && isnothing(representation)
                ext = pair.problems[2]
                sites = T.Runner._read_linked_array(fine_path,"ifr_sites",Float64,
                    size(ext.v.interface_probes,1),ext.nz)
                representation = unitary_control(ext,pair.seeds[2],images[2],cuts,workers,pair.stage.k,sites)
                append_row(path,"unitary_control",(;step,result=representation))
            end
            if past.operator_trigger && !operator_checked
                result = lo_operator_control(pair.problems[2],images[2],cuts,workers)
                append_row(path,"LO_operator_control",(;step,result))
                operator_checked = true
                if !isnothing(representation) && representation.passes
                    ext = pair.problems[2]
                    sites = T.Runner._read_linked_array(fine_path,"ifr_sites",Float64,
                        size(ext.v.interface_probes,1),ext.nz)
                    ring = argmax([abs(x.lo_total) for x in result.by_ring])
                    device = T.TOML.parsefile(joinpath(app,"studies","fath-v843","fath-device.toml"))
                    omega = device["LO_energy_meV"] / 100
                    diagonal = lo_diagonal_control(ext,sites,ring,omega)
                    append_row(path,"LO_golden_rule",(;step,result=diagonal))
                end
            end
            if past.plateau && !plateau_checked
                assessment = same_input_control(pair,images,cuts,workers,path,step)
                append_row(path,"update_assessment",assessment)
                plateau_checked = true
                if assessment.adopt_pure
                    alpha = 1.0
                    switched_step = step
                end
            end
            if plateau_checked && step>switched_step && !past.advances_toward_stationarity
                append_row(path,"completed",(;step,reason="measured_high_residual_plateau",
                    confirmations,operator_checked,plateau_checked))
                return
            end
        end
        for arm in eachindex(pair.problems)
            k31_update!(pair.seeds[arm],images[arm],alpha)
        end
        GC.gc(false)
    end
end

end
