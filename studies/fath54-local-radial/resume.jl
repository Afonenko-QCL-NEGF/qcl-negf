include("refinement.jl")
include("observe_direct.jl")

observe_refinement(p,source,cuts,workers;high_order=true) =
    direct_observation(p,source,cuts,workers;high_order)

# Compact measurements from a completed level can be reloaded without fields.
function named_evidence(x)
    x isa AbstractDict && return (;(Symbol(k)=>named_evidence(v) for (k,v) in x)...)
    x isa AbstractVector && return map(named_evidence,x)
    return x
end

function resumed_stages(p,seed,cuts,workers,replay)
    r = T.Runner.YAML.load_file(ENV["FATH_RESUME_EVIDENCE"];dicttype=Dict{String,Any})
    r["stage"]=="K27" && r["cuts_nm"]==cuts &&
        r["metadata"]["replay"]["input_sha"]==replay.input_sha &&
        r["metadata"]["replay"]["image_sha"]==replay.image_sha &&
        replay.input_matches && replay.image_matches || error("incompatible recovery evidence")
    old_k = radial_coordinates(coarse_path,p.nk)
    pair = T.radial_setup(p,cuts,coarse_path,fine_path)
    base = pair.f
    pair.fine_identity["id"]==r["metadata"]["fine_input_identity"]["id"] ||
        error("recovery loaded a different K25 packet")
    archived = T.Runner.YAML.load_file(archived_path;dicttype=Dict{String,Any})
    archived = get(archived,"radial",archived)
    q = Float64.(archived["observations"]["coarse_input"]["raw_ring_sheet_cm2"])
    levels = Dict{String,Any}(k=>named_evidence(v) for (k,v) in r["levels"])
    differences = Dict{String,Any}(k=>named_evidence(v) for (k,v) in r["differences"])
    shared_operators = Dict{String,Any}(r["shared_operators"])
    function save(stage;followup=nothing)
        metadata = merge(named_evidence(r["metadata"]),(;replay,
            recovered_from_stage="K27",recovery_workers=workers,direct_observer_crosscheck_K25=observer_crosscheck))
        T.radial_write(output,(;stage,metadata,cuts_nm=cuts,levels,differences,shared_operators,followup))
    end

    # Recreate the K25 fields solely as the reference for the spectral localization.
    # The measurements of the two completed arms are loaded from compact evidence.
    a = levels["K25"]
    input = T.apply_radial(pair.p_to_f,seed)
    T.packed_sha(input)==a.input_sha || error("recovered K25 transfer is different")
    image = arm_image(base,input,cuts,workers)
    T.packed_sha(image.source)==a.fresh_sha || error("recovered K25 fresh source is different")
    measured = observed_row(direct_observation(base,image.source,cuts,workers),cuts)
    ref = a.measurements.observed
    observer_crosscheck = (;max_profile_A_cm2=maximum(abs,measured.profile.-ref.profile),
        raw_charge_cm2=measured.raw_charge-ref.raw_charge,
        max_ring_charge_cm2=maximum(abs,measured.raw_charge_by_ring.-ref.raw_charge_by_ring),
        max_mode_fraction=maximum(abs,measured.mode_fractions.-ref.mode_fractions))
    observer_crosscheck.max_profile_A_cm2 < 1e-6 &&
        abs(observer_crosscheck.raw_charge_cm2)<100 &&
        observer_crosscheck.max_ring_charge_cm2<100 &&
        observer_crosscheck.max_mode_fraction<1e-9 ||
        error("direct independent observer did not reproduce K25")
    announce((;phase="recovered_K25",observer_crosscheck))
    baseline = (;report=a,mapped=input,image,arm=(;p=base,k=pair.kf))
    k27 = load_arm(base,"K27")
    fine = load_arm(base,"K31")
    shared_operators["K27_to_K31"] = common_operators(k27,fine)
    k27 = nothing
    GC.gc()
    retained = level_control(p,seed,old_k,fine,cuts,workers,q;retain=true)
    levels["K31"] = retained.report
    differences["K27_to_K31"] = compare_arms(levels["K27"],retained.report)
    save("K31")
    announce((;phase="finished",level="K31"))
    GC.gc()
    run_followup(p,seed,old_k,base,pair.kf,baseline,retained,cuts,workers,q,levels,differences,save)
end

run_refinement_stages(p,seed,cuts,workers,replay) = resumed_stages(p,seed,cuts,workers,replay)
