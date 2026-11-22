include("fath_factorial.jl")

function holdout_main()
    length(ARGS)==4 || error("Usage: fath_rank_holdout.jl F25 NATIVE_BDD WORKERS OUTPUT")
    archive,geometry,workers_arg,output=ARGS
    workers=parse(Int,workers_arg)
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    input=Runner._read_linked_checkpoint(archive)
    p=input.problem
    p.nk==25 && p.ne==959 && p.geo.voltage≈0.54 && input.identity["temperature_K"]==10.0 ||
        error("expected the archived F25 holdout at 54 mV and 10 K")
    original=Runner.YAML.load_file(joinpath(@__DIR__,"../fath-v843/evidence/fath-F25-projected.json"))
    input.identity==original["identity"] && input.current_midpoints==original["current_midpoints_nm"] ||
        error("the holdout baseline uses different physical conditions")
    spec=TOML.parsefile(joinpath(archive,"spec.toml"))
    ifr_sites=Runner._read_linked_array(archive,"ifr_sites",Float64,spec["n_interfaces"],p.nz)
    radial=Runner._read_linked_array(archive,"k",Float64,p.nk)
    coordinates=coordinate_data(geometry,input.identity["source_geometry_model_sha256"],p)
    expanded=expand_modes(p,coordinates,radial)
    embedding=expanded.q'*p.v.coordinate_frame
    lifted=lift_source(input.seed,embedding)
    r=size(expanded.q,2)
    anchors=Array{ComplexF64}(undef,r,r,p.nk,length(LT.COLLISION_CHANNELS))
    for channel in axes(anchors,4), k in axes(anchors,3)
        anchors[:,:,k,channel]=embedding*p.const_by_channel[:,:,k,channel]*embedding'
    end
    v=lo_kernel(p.v,ifr_sites,p.v.lo_plus,p.v.lo_minus;q=expanded.q)
    candidate=rebuild(p,v;modes=expanded.modes,nb=expanded.nb,h=expanded.h,anchor=anchors)
    common_bases_error = maximum(norm(embedding'*b[:,expanded.common]-old)/norm(old)
        for (b,old) in zip(candidate.geo.bases,p.geo.bases))
    @assert common_bases_error < 2e-13
    println(stderr,"held-out F25 geometry and rank verified")
    flush(stderr)
    image=LT.linked_fresh_map(candidate,lifted.source;projector=LT.project_linked_economical,
        selected_rows=true,projection_for_collision=true,workers)
    cuts=input.current_midpoints
    widths=(cuts[3:end] .- cuts[1:end-2])./2
    new=linked_metrics(image.summary,widths)
    println(stderr,"held-out F25 fresh map complete: rK=",new.rK,
        " spatial deviation=",new.spatial.max_deviation_from_mean_A_cm2)
    flush(stderr)
    observed=spatial_balance(candidate,image.source,widths;
        workers,energy_rule=independent_energy_rule,current_cuts=cuts)
    old=original["observation"]
    old_profile=old["current_A_cm2"]
    raw_difference=observed.current_A_cm2.-old_profile
    mean_difference=observed.current.mean_internal_A_cm2-old["current"]["mean_internal_A_cm2"]
    report=(;schema="qcl-negf-fath-rank-holdout/v1",input.identity,workers,
        core=Runner._linked_package_identity(Runner.QCLNEGF),
        runner=Runner._linked_package_identity(Runner),runtime=Runner._runtime_toolchain_provenance(),
        source_sha256=bytes2hex(open(sha256,@__FILE__)),
        rank=(;nb=candidate.nb,r,expanded.metric_error,expanded.h_error,
            lift_roundtrip_maximum=lifted.roundtrip_maximum,common_bases_error),
        cuts_nm=cuts,original=original["production"],candidate=new,observed,
        maximum_profile_difference_A_cm2=maximum(abs,raw_difference),
        mean_difference_A_cm2=mean_difference,
        maximum_centered_difference_A_cm2=maximum(abs,raw_difference.-mean_difference),
        maximum_LO_cumulative_difference_A_cm2=maximum(abs,observed.collision_cumulative_A_cm2["LO"].-
            old["collision_cumulative_A_cm2"]["LO"]),
        maximum_projection_cumulative_difference_A_cm2=maximum(abs,observed.spatial_projection_gap_A_cm2.-
            old["spatial_projection_gap_A_cm2"]),
        independent_profile_difference_A_cm2=maximum(abs,observed.current_A_cm2.-new.current_profile_A_cm2))
    open(output,"w") do io
        Runner._light_json(io,report)
        println(io)
    end
end

abspath(PROGRAM_FILE)==abspath(@__FILE__) && holdout_main()
