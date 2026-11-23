const radial_study = @__DIR__
const build_dir = dirname(dirname(radial_study))
const static_builder = get(ENV,"FATH_ARCHIVED_REGRID",joinpath(dirname(fine_path),"regrid.py"))
const python = get(ENV,"FATH_KERNEL_PYTHON",joinpath(homedir(),".cache","codex-runtimes",
    "codex-primary-runtime","dependencies","python","bin","python3.12"))
const fixed_cuts = (33.84729166666667,39.640972222222224)
const target_charge_tolerance = 3e8
const population_tolerance = 0.005

radial_coordinates(path,n) = T.Runner._read_linked_array(path,"k",Float64,n)
cell_edges(k) = [first(k); (k[1:end-1] .+ k[2:end])./2; last(k)].^2
center_j(profile,mean) = profile .- mean

function load_arm(base, marker)
    n = marker == "K27" ? 27 : 31
    nz, r, modes, channels = base.nz, base.r, size(base.h,1), length(LT.COLLISION_CHANNELS)
    command = `$python $(joinpath(radial_study,"physical_kernels.py")) $fine_path $static_builder $marker`
    command = addenv(command,"OPENBLAS_NUM_THREADS"=>"1","OMP_NUM_THREADS"=>"1","PYTHONDONTWRITEBYTECODE"=>"1")
    k,w,h,hop,anchor,ifr,lo,impurity = open(command,"r") do io
        k = read!(io,Vector{Float64}(undef,n))
        w = read!(io,similar(k))
        h = read!(io,Array{ComplexF64}(undef,modes,modes,n))
        hop = read!(io,Matrix{Float64}(undef,nz+1,n))
        anchor = read!(io,Array{ComplexF64}(undef,r,r,n,channels))
        ifr = Matrix{Float64}(undef,n,n)
        lo = Array{ComplexF64}(undef,nz,nz,n,n)
        impurity = Array{Float64}(undef,nz,nz,n,n)
        for out in 1:n
            read!(io,@view(ifr[:,out]))
            read!(io,@view(lo[:,:,:,out]))
            read!(io,@view(impurity[:,:,:,out]))
        end
        eof(io) || error("physical constructor returned extra data")
        return k,w,h,hop,anchor,ifr,lo,impurity
    end
    v = base.v
    sites = T.Runner._read_linked_array(fine_path,"ifr_sites",Float64,size(v.interface_probes,1),nz)
    for (name,kernel) in ((:IFR,ifr),(:LO,lo),(:impurity,impurity))
        reciprocal = T.pair_reciprocity(kernel,w)
        reciprocal < 2e-12 || error("$marker $name lost reciprocity: $reciprocal")
    end
    contracted = LT.LocalCollisionKernels(v.coordinate_frame,w,v.acoustic,v.alloy,
        sites,ifr,lo,impurity,v.lo_plus,v.lo_minus,v.bose)
    p = LT.LinkedProblem(base.en,base.we,w,base.geo.modes,base.nb,base.geo.offsets,
        base.geo.voltage,base.geo.reach,h,hop,anchor,contracted;
        spin_degeneracy=base.spin_degeneracy,current_scale=base.current_scale,
        density_scale=base.density_scale,target_dimless=base.target_dimless)
    return (;p,k)
end

function common_operators(old,new)
    i = searchsortedfirst.(Ref(new.k),old.k)
    new.k[i] == old.k || error("the two radial levels lost exact nesting")
    p,q = old.p,new.p
    common = Dict(string(name)=>T.relerr(original,rebuilt) for (name,original,rebuilt) in (
        (:H,p.h,q.h[:,:,i]),(:hop,p.hops,q.hops[:,i]),
        (:anchor,p.const_by_channel,q.const_by_channel[:,:,i,:]),
        (:IFR,p.v.interface_pair,q.v.interface_pair[i,i]),
        (:LO,p.v.lo_covariance,q.v.lo_covariance[:,:,i,i]),
        (:impurity,p.v.impurity_covariance,q.v.impurity_covariance[:,:,i,i])))
    maximum(values(common)) < 2e-12 || error("nested shared operators changed: $common")
    return common
end

function transfer_arm(old,old_k,source,new,new_k,ring_charge)
    P = T.annular_transfer(old_k,new_k,old.wk,new.wk)
    R = T.annular_transfer(new_k,old_k,new.wk,old.wk)
    adjoint_error = T.relerr(new.wk .* P,(old.wk .* R)')
    adjoint_error < 2e-13 || error("annular restriction lost weighted adjoint")
    mapped = T.apply_radial(P,source)
    integrals = [T.relerr(T.radial_integral(mapped,new.wk,c),T.radial_integral(source,old.wk,c))
                 for c in axes(source,5)]
    maximum(integrals) < 2e-13 || error("packed annular transfer did not conserve its measure")
    common = searchsortedfirst.(Ref(new_k),old_k)
    new_k[common] == old_k || error("source radii are not nested")
    weighted_charge = new.wk .* (P * (ring_charge ./ old.wk))
    isapprox(sum(weighted_charge),sum(ring_charge);rtol=2e-13) || error("density transfer lost charge")
    roundtrip = T.apply_radial(R*P,source)
    smoothing = T.packed_difference(old,roundtrip,source,old_k)
    return (;mapped,report=(;conservative_integral_error_by_channel=integrals,
        weighted_adjoint_error=adjoint_error,density_transferred_cm2=sum(weighted_charge),
        density_transferred_by_ring_cm2=weighted_charge,
        shared_rows_changed=count(i->P[common[i],i]!=1,eachindex(common)),roundtrip=smoothing,
        overlap=[collect(row) for row in eachrow(P)]))
end

function observed_row(observ,cuts)
    profile = observ.current_A_cm2
    mean = observ.current.mean_internal_A_cm2
    indices = [argmin(abs.(cuts .- edge)) for edge in fixed_cuts]
    return (;raw_charge=observ.raw_sheet_cm2,raw_lambda=observ.raw_lambda,
        raw_charge_by_ring=observ.raw_ring_sheet_cm2,profile,mean,
        centered=center_j(profile,mean),max_deviation=observ.current.max_deviation_from_mean_A_cm2,
        oriented_seams=profile[[1,end]],outward_seams=observ.current.outward_A_cm2,
        delta_segment=profile[indices[2]]-profile[indices[1]],mode_fractions=observ.central_bands.fraction,
        mode_fractions_by_ring=observ.central_bands.fraction_by_ring_and_band,
        band_energies_meV=observ.central_bands.reference_energy_meV,
        closure=observ.maximum_closure_error_A_cm2)
end

function arm_image(p,seed,cuts,workers)
    start = time_ns()
    image = T.map_radial(p,seed,workers)
    summary = image.summary
    native = T.linked_metrics(summary,T.widths_at(cuts))
    announce((;stage="fresh_map",nk=p.nk,nb=p.nb,native.raw_sheet_cm2,native.rK,native.rSigma,
        mean=native.spatial.mean_internal_A_cm2,deviation=native.spatial.max_deviation_from_mean_A_cm2,
        seconds=(time_ns()-start)*1e-9))
    return image
end

observe_refinement(p,source,cuts,workers;high_order=true) =
    T.radial_observe(p,source,cuts,workers;high_order)

function measure_arm(p, image, cuts,workers; independent_input)
    summary = image.summary
    native = T.linked_metrics(summary,T.widths_at(cuts))
    native_in = T.input_stage(summary)
    observed = observed_row(observe_refinement(p,image.source,cuts,workers),cuts)
    announce((;stage="GL20_fresh",nk=p.nk,nb=p.nb,observed.mean,observed.raw_charge))
    native_mean = native.spatial.mean_internal_A_cm2
    native_profile = native.current_profile_A_cm2
    i,j = [argmin(abs.(cuts .- edge)) for edge in fixed_cuts]
    lower = observe_refinement(p,image.source,cuts,workers;high_order=false)
    mode_uncertainty = abs.(observed.mode_fractions.-lower.central_bands.fraction)
    uncertainty = (;profile=maximum(abs,observed.profile.-native_profile),
        centered=maximum(abs,observed.centered.-center_j(native_profile,native_mean)),
        mean=abs(observed.mean-native_mean),delta_segment=abs(observed.delta_segment-(native_profile[j]-native_profile[i])),
        raw_charge=abs(observed.raw_charge-native.raw_sheet_cm2),
        input_charge=abs(independent_input.raw_charge-native_in.raw_sheet_cm2),mode_fractions=mode_uncertainty)
    return (;native,native_in,native_input_rings=summary["projected_input"]["per_ring_raw_sheet_cm2"],
        native_fresh_rings=summary["projected_fresh"]["per_ring_raw_sheet_cm2"],
        pole_count_input=summary["projected_input"]["pole_count_by_ring"],
        pole_count_fresh=summary["projected_fresh"]["pole_count_by_ring"],
        independent_input,observed,uncertainty)
end

function level_control(p,seed,old_k,arm,cuts,workers,ring_charge;retain=false)
    new,k = arm.p,arm.k
    transferred = transfer_arm(p,old_k,seed,new,k,ring_charge)
    measured_input = observed_row(observe_refinement(new,transferred.mapped,cuts,workers),cuts)
    announce((;stage="GL20_input",nk=new.nk,nb=new.nb,measured_input.raw_charge))
    image = arm_image(new,transferred.mapped,cuts,workers)
    measurements = measure_arm(new,image,cuts,workers;independent_input=measured_input)
    reciprocity = (;IFR=T.pair_reciprocity(new.v.interface_pair,new.wk),
        LO=T.pair_reciprocity(new.v.lo_covariance,new.wk),
        impurity=T.pair_reciprocity(new.v.impurity_covariance,new.wk))
    report = (;k_nm_inverse=k./10,w=new.wk,cells_u=cell_edges(k),weight_sum=sum(new.wk),reciprocity,
        transfer=transferred.report,input_sha=T.packed_sha(transferred.mapped),
        fresh_sha=T.packed_sha(image.source),measurements)
    return retain ? (;report,mapped=transferred.mapped,image,arm) : report
end

function compare_arms(old,new)
    a,b = old.measurements,new.measurements
    Jtol = max(1.0,0.01abs(a.observed.mean))
    band(value,error,tol) = (;value,error,tol,
        lower=max(0.,abs(value)-error),upper=abs(value)+error,
        status=error>0.2tol ? "observer_resolution" :
            abs(value)+error<=tol ? "within" : abs(value)-error>tol ? "above" : "overlaps")
    estimate(field,value,tol) = band(value,getproperty(a.uncertainty,field)+getproperty(b.uncertainty,field),tol)
    profile = b.observed.profile-a.observed.profile
    centered = b.observed.centered-a.observed.centered
    modes = b.observed.mode_fractions-a.observed.mode_fractions
    return (;input_charge=estimate(:input_charge,b.independent_input.raw_charge-a.independent_input.raw_charge,target_charge_tolerance),
        raw_charge=estimate(:raw_charge,b.observed.raw_charge-a.observed.raw_charge,target_charge_tolerance),
        mean=estimate(:mean,b.observed.mean-a.observed.mean,Jtol),
        profile=estimate(:profile,maximum(abs,profile),Jtol),
        centered=estimate(:centered,maximum(abs,centered),Jtol),
        delta_segment=estimate(:delta_segment,b.observed.delta_segment-a.observed.delta_segment,Jtol),
        mode_fractions=[band(value,a.uncertainty.mode_fractions[i]+b.uncertainty.mode_fractions[i],
            population_tolerance) for (i,value) in enumerate(modes)],
        delta_profile=profile,delta_centered=centered)
end

function run_refinement_stages(p, seed, cuts, workers, replay)
    archived = T.Runner.YAML.load_file(archived_path;dicttype=Dict{String,Any})
    archived = get(archived,"radial",archived)
    coarse_observed = archived["observations"]["coarse_input"]
    ring_charge = Float64.(coarse_observed["raw_ring_sheet_cm2"])
    if !(replay.input_matches && replay.image_matches)
        reproduced = T.radial_observe(p,seed,cuts,workers)
        ring_charge = reproduced.raw_ring_sheet_cm2
    end
    old_k = radial_coordinates(coarse_path,p.nk)
    pair = T.radial_setup(p,cuts,coarse_path,fine_path)
    base = pair.f
    pair.fine_identity["id"] == archived["fine_identity"]["id"] || error("K25 packet mismatch")
    levels = Dict{String,Any}()
    differences = Dict{String,Any}()
    shared_operators = Dict{String,Any}()
    metadata = (;fine_input_identity=pair.fine_identity,revision=readchomp(`git -C $(ENV["FATH_APP"]) rev-parse HEAD`),
        core=T.Runner._linked_package_identity(T.Runner.QCLNEGF),workers,
        conditions_sha256=T.file_sha(joinpath(@__DIR__,"protocol.md")),replay)
    save(stage;followup=nothing) = T.radial_write(output,(;stage,metadata,cuts_nm=cuts,
        levels,differences,shared_operators,followup))
    retained = nothing
    baseline = nothing
    previous_arm = nothing
    for label in ("K25","K27","K31")
        arm = label=="K25" ? (;p=base,k=pair.kf) : load_arm(base,label)
        announce((;phase="start",level=label,threads=workers))
        if previous_arm !== nothing
            before = label == "K27" ? "K25" : "K27"
            shared_operators[before * "_to_" * label] = common_operators(previous_arm,arm)
        end
        previous_arm = arm
        if label == "K25"
            baseline = level_control(p,seed,old_k,arm,cuts,workers,ring_charge;retain=true)
            levels[label] = baseline.report
        elseif label == "K31"
            retained = level_control(p,seed,old_k,arm,cuts,workers,ring_charge;retain=true)
            levels[label] = retained.report
        else
            levels[label] = level_control(p,seed,old_k,arm,cuts,workers,ring_charge)
        end
        if label == "K25"
            candidate = levels[label].measurements
            obs = archived["observations"]["fine_after_prolong_map"]
            maximum(abs,candidate.observed.profile.-obs["current_A_cm2"]) < 1e-5 ||
                error("K25 does not reproduce the archived independent current")
            abs(candidate.native_in.raw_sheet_cm2-archived["native_inputs"]["fine"]["raw_sheet_cm2"]) < 100 ||
                error("K25 does not reproduce the archived raw input charge")
        else
            previous = label=="K27" ? "K25" : "K27"
            pair_key = previous * "_to_" * label
            differences[pair_key] = compare_arms(levels[previous],levels[label])
            announce((;phase=pair_key,input_charge=differences[pair_key].input_charge,
                profile=differences[pair_key].profile,centered=differences[pair_key].centered))
        end
        save(label)
        announce((;phase="finished",level=label))
        GC.gc()
    end
    run_followup(p,seed,old_k,base,pair.kf,baseline,retained,cuts,workers,ring_charge,levels,differences,save)
end

include("followup.jl")

function run_refinement(p, seed, cuts, workers, replay)
    while true
        try
            Base.invokelatest(run_refinement_stages, p, seed, cuts, workers, replay)
            return
        catch err
            err isa InterruptException && rethrow()
            open(output * ".error","a") do io
                showerror(io,err,catch_backtrace())
                println(io)
            end
            announce((;phase="awaiting_repair",error=sprint(showerror,err)))
            while !isfile(continuation * ".retry")
                sleep(5)
            end
            rm(continuation * ".retry")
            include(continuation)
        end
    end
end
