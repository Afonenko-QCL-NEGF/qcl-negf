# Run inside the pinned, already installed Julia Runner project.
const v843_studies = abspath(ARGS[1])
const v843_reference = joinpath(v843_studies, "fath-v843", "evidence", "v843-f21.json")
const v843_comparison = joinpath(v843_studies, "fath-v843", "evidence", "v843-comparison.json")
include(joinpath(v843_studies, "fath-v843", "continuation.jl"))
using TOML

const v843_identity = "e53da1d48e986cc181cf0ccd4c682578283ac24994e2afdf7d39cdd6f7c0e01d"
const v843_bands = (extractor=1, lower_lasing=2, upper_lasing=3, injector=4)
const v843_channels = (:LO, :acoustic, :impurity, :IFR, :alloy)

function diagnostic_log(path, kind, payload)
    open(path, "a") do io
        Runner._light_json(io, (;kind, payload...))
        println(io)
    end
end

v843_sha(x::AbstractArray) = bytes2hex(sha256(reinterpret(UInt8, vec(x))))
v843_sha(path::AbstractString) = bytes2hex(open(sha256, path))

function v843_checked_input(archive)
    saved = Runner._read_linked_checkpoint(archive)
    p = saved.problem
    spec = TOML.parsefile(joinpath(archive, "spec.toml"))
    cuts = saved.current_midpoints
    saved.identity["id"] == v843_identity || error("unexpected V843 sealed source")
    (p.ne, p.nk, p.r, p.nb, p.geo.reach, length(cuts), spec["physical_T_K"], spec["LO_temp_K"]) ==
        (239, 5, 28, 11, 8, 145, 50.0, 50.0) ||
        error("V843 diagnostic expects the frozen 21 kV/cm E239 K5 Q28 packet")
    isapprox(last(cuts)-first(cuts), 36.16; atol=1e-10) &&
        isapprox(1000p.geo.voltage/(last(cuts)-first(cuts)), 21.0; atol=1e-10) ||
        error("wrong V843 physical bias or period")
    LT.COLLISION_CHANNELS == v843_channels || error("unexpected collision channel ordering")
    return saved
end

function v843_reference_data(saved)
    evidence = Runner.YAML.load_file(v843_reference; dicttype=Dict{String,Any})
    evidence["identity"]["id"] == saved.identity["id"] &&
        evidence["selected_iteration"] == 48 &&
        evidence["current_midpoints_nm"] == saved.current_midpoints ||
        error("V843 published trajectory and sealed packet are out of sync")
    comparison = Runner.YAML.load_file(v843_comparison; dicttype=Dict{String,Any})
    fixed_field = only(filter(x -> x["field_kV_cm"]==21.0, comparison["cases"]))
    row = evidence["history"][48]
    obs = evidence["observed"]
    sheet = obs["central_bands"]["sheet_cm2"]
    trajectory = [(;rK=row["rK"], rSigma=row["rSigma"]) for row in evidence["history"]]
    return (;
        old_trajectory=(;selected_iteration=48, stationary=evidence["stationary"],
            trajectory, rK=row["rK"], rSigma=row["rSigma"], raw_lambda=row["raw_lambda"],
            mean_A_cm2=obs["current"]["mean_internal_A_cm2"],
            deviation_A_cm2=obs["current"]["max_deviation_from_mean_A_cm2"],
            J_A_cm2=obs["current_A_cm2"],
            extractor_cm2=sheet[v843_bands.extractor], upper_lasing_cm2=sheet[v843_bands.upper_lasing],
            extractor_over_upper=sheet[v843_bands.extractor]/sheet[v843_bands.upper_lasing]),
        published=fixed_field["published"],
        NEGF50_envelope_A_cm2=fixed_field["published_negf_digitization_envelope_A_cm2"],
        DM50_extractor_over_upper=0.60,
        files=(;v843_f21_sha256=v843_sha(v843_reference),
            v843_comparison_sha256=v843_sha(v843_comparison),
            jonasson_subbands_sha256=v843_sha(joinpath(v843_studies, "fath-v843",
                "v843-published-subband-moments.csv"))))
end

function v843_map(p, seed, workers)
    function progress(record)
        if hasproperty(record,:k)
            println(stderr, "V843 ", record.stage, " ring ", record.k)
            flush(stderr)
        end
    end
    return LT.linked_fresh_map(p, seed; projector=LT.project_linked_economical,
        selected_rows=true, projection_for_collision=true, workers, observe=progress)
end

function v843_observation(p, image, cuts, workers, reference)
    widths = (cuts[3:end] .- cuts[1:end-2])./2
    measured = spatial_balance(p, image.source, widths;
        energy_rule=independent_energy_rule, current_cuts=cuts, workers)
    bands = measured.central_bands
    sheet = bands.sheet_cm2
    e, u = v843_bands.extractor, v843_bands.upper_lasing
    isapprox(bands.reference_energy_meV[e], -26.298857420548234; atol=1e-6) &&
        isapprox(bands.reference_energy_meV[u], 15.14935021640365; atol=1e-6) ||
        error("V843 physical band assignment fingerprint changed")
    native = linked_metrics(image.summary, widths)
    profile = measured.current_A_cm2
    mean_A_cm2 = measured.current.mean_internal_A_cm2
    return (;
        J_A_cm2=profile, centered_J_A_cm2=profile.-mean_A_cm2, mean_A_cm2,
        maximum_deviation_A_cm2=measured.current.max_deviation_from_mean_A_cm2,
        current_tolerance_A_cm2=measured.current.target_tolerance_A_cm2,
        outward_seams_A_cm2=measured.current.outward_A_cm2,
        independent_current_difference_A_cm2=maximum(abs,profile.-native.current_profile_A_cm2),
        raw_sheet_cm2=measured.raw_sheet_cm2, raw_lambda=measured.raw_lambda,
        extractor=(;energy_meV=bands.reference_energy_meV[e], sheet_cm2=sheet[e],
            fraction=bands.fraction[e]),
        upper_lasing=(;energy_meV=bands.reference_energy_meV[u], sheet_cm2=sheet[u],
            fraction=bands.fraction[u]),
        extractor_over_upper=sheet[e]/sheet[u],
        temperature_K=measured.equivalent_temperature_K,
        kinetic_remainder_A_cm2=measured.kinetic_remainder_A_cm2,
        spatial_projection_gap_A_cm2=measured.spatial_projection_gap_A_cm2,
        collision_cumulative_A_cm2=measured.collision_cumulative_A_cm2,
        coherent_projected_A_cm2=measured.coherent_projected_A_cm2,
        balance_closure_A_cm2=measured.maximum_closure_error_A_cm2,
        maximum_exact_dyson_residual=measured.maximum_exact_dyson_residual,
        difference_from_published_A_cm2=Dict(key => mean_A_cm2-value["current_A_cm2"]
            for (key,value) in reference.published),
        difference_from_DM50_extractor_over_upper=sheet[e]/sheet[u]-reference.DM50_extractor_over_upper)
end

function v843_record_map(path, label, step, source, image, widths, confirmations)
    row = linked_metrics(image.summary, widths)
    confirmations = strictly_qualified(row) ? confirmations+1 : 0
    input_sha, fresh_sha = v843_sha(source), v843_sha(image.source)
    diagnostic_log(path,"map",(;label, step, row, confirmations, input_sha, fresh_sha,
        channel_balance=image.summary["fresh_channel_balance"], peak_rss_bytes=Int(Sys.maxrss())))
    println(stderr, "V843 $label fresh map $step rK=$(row.rK) rΣ=$(row.rSigma)")
    flush(stderr)
    return (;row, confirmations, input_sha, fresh_sha)
end

function v843_convex!(seed, image, alpha)
    seed .= (1-alpha) .* seed .+ alpha .* image.source
    return nothing
end

function v843_mixing_branch(p, source, image, cuts, widths, workers, path, maps, reference, alpha)
    label = alpha==1.0 ? "picard100" : "picard035"
    seed = copy(source)
    v843_convex!(seed, image, alpha)
    confirmations = 0
    for step in 1:maps
        candidate = v843_map(p, seed, workers)
        record = v843_record_map(path, label, step, seed, candidate, widths, confirmations)
        confirmations = record.confirmations
        if step==maps
            observation = v843_observation(p, candidate, cuts, workers, reference)
            confirmed = confirmations>=3 &&
                observation.maximum_deviation_A_cm2<=observation.current_tolerance_A_cm2 &&
                observation.independent_current_difference_A_cm2<=observation.current_tolerance_A_cm2
            diagnostic_log(path, "GL20", (;label, step, record.input_sha, record.fresh_sha, observation))
            return (;label, alpha, step, record.row, confirmations, confirmed, observation)
        end
        v843_convex!(seed, candidate, alpha)
    end
end

function v843_pair_contrast(a, b)
    factor(a,b) = max(a,b)/max(min(a,b),floatmin(Float64))
    ratio_rK,ratio_rSigma = factor(a.row.rK,b.row.rK),factor(a.row.rSigma,b.row.rSigma)
    x,y = a.observation,b.observation
    return (;ratio_rK, ratio_rSigma, matched_residuals=max(ratio_rK,ratio_rSigma)<=1.25,
        mean_delta_A_cm2=y.mean_A_cm2-x.mean_A_cm2,
        maximum_absolute_profile_delta_A_cm2=maximum(abs,y.J_A_cm2.-x.J_A_cm2),
        maximum_centered_profile_delta_A_cm2=maximum(abs,y.centered_J_A_cm2.-x.centered_J_A_cm2),
        numerical_quadrature_difference_bound_A_cm2=
            x.independent_current_difference_A_cm2+y.independent_current_difference_A_cm2,
        raw_lambda_delta=y.raw_lambda-x.raw_lambda,
        extractor_sheet_delta_cm2=y.extractor.sheet_cm2-x.extractor.sheet_cm2,
        upper_lasing_sheet_delta_cm2=y.upper_lasing.sheet_cm2-x.upper_lasing.sheet_cm2,
        extractor_over_upper_delta=y.extractor_over_upper-x.extractor_over_upper)
end

function v843_run_mixing(saved, cuts, widths, workers, path, maps, reference)
    p,seed = saved.problem,saved.seed
    image = v843_map(p,seed,workers)
    shared = v843_record_map(path,"shared_branch_input",0,seed,image,widths,0)
    observation = v843_observation(p,image,cuts,workers,reference)
    diagnostic_log(path,"GL20",(;label="shared_branch_input",step=0,shared.input_sha,
        shared.fresh_sha,observation))
    mixed = v843_mixing_branch(p,seed,image,cuts,widths,workers,path,maps,reference,0.35)
    GC.gc()
    pure = v843_mixing_branch(p,seed,image,cuts,widths,workers,path,maps,reference,1.0)
    return (;mode="mixing", shared.input_sha, shared.fresh_sha, branch_maps=maps,
        mixed=(;mixed.confirmations,mixed.confirmed), pure=(;pure.confirmations,pure.confirmed),
        contrast=v843_pair_contrast(mixed,pure))
end

function v843_main()
    length(ARGS) in (5,6) ||
        error("Usage: v843_diagnostic.jl STUDIES SEALED_INPUT mixing|unitary WORKERS JSONL [BRANCH_MAPS]")
    _,archive,mode,workers_arg,path = ARGS[1:5]
    mode in ("mixing","unitary") || error("unknown V843 diagnostic mode")
    maps = length(ARGS)==6 ? parse(Int,ARGS[6]) : 4
    (mode=="mixing" && 1<=maps<=8) || (mode=="unitary" && length(ARGS)==5) ||
        error("choose 1–8 fresh maps per mixing branch; unitary uses one map per representation")
    workers = parse(Int,workers_arg)
    1<=workers<=min(Threads.nthreads(),5) || error("choose up to five V843 radial workers")
    ispath(path) && error("output already exists: $path")
    BLAS.set_num_threads(1)
    saved = v843_checked_input(archive)
    reference = v843_reference_data(saved)
    cuts = saved.current_midpoints
    widths = (cuts[3:end] .- cuts[1:end-2])./2
    p = saved.problem
    diagnostic_log(path,"configuration",(;schema="qcl-negf-v843-common-input-diagnostic/v1", mode,
        identity=saved.identity, input_stage="sealed early source of the archived continuation",
        input_sha=v843_sha(saved.seed), cuts, radial_weights=p.wk, energy_weights=p.we,
        radial_nodes=Runner._read_linked_array(archive,"k",Float64,p.nk),
        hartree="fixed zero", lattice_K=50.0, LO_bath_K=50.0, field_kV_cm=21.0,
        bias_meV_per_period=100p.geo.voltage, workers, reference,
        core=Runner._linked_package_identity(Runner.QCLNEGF),
        runner=Runner._linked_package_identity(Runner),
        runtime=Runner._runtime_toolchain_provenance(),
        driver_sha256=v843_sha(@__FILE__)))
    result = if mode=="mixing"
        v843_run_mixing(saved,cuts,widths,workers,path,maps,reference)
    else
        v843_run_unitary(saved,archive,cuts,widths,workers,path,reference)
    end
    diagnostic_log(path,"completed",result)
end

if abspath(PROGRAM_FILE)==abspath(@__FILE__)
    if length(ARGS)>=3 && ARGS[3]=="unitary"
        include("v843_unitary_adapter.jl")
    end
    v843_main()
end
