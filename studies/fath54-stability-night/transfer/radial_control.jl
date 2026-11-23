module FathRadialControl

const STUDY = joinpath(get(ENV, "FATH_APP", joinpath(@__DIR__, "..", "..",
    "fath54-validation-20261121", "source", "app")), "studies", "fath-v843")
include(joinpath(STUDY, "v843_radial.jl"))

relerr(a, b) = norm(a-b)/max(norm(b), floatmin(Float64))
file_sha(path) = bytes2hex(open(sha256,path))
packed_sha(x) = bytes2hex(sha256(reinterpret(UInt8,vec(x))))

function pair_reciprocity(cov, w)
    n, d = 0.0, 0.0
    @views for j in eachindex(w), i in eachindex(w)
        a = selectdim(selectdim(cov, ndims(cov), j), ndims(cov)-1, i)
        b = selectdim(selectdim(cov, ndims(cov), i), ndims(cov)-1, j)
        n += w[i]*w[j]*sum(abs2, a .- conj.(b))
        d += w[i]*w[j]*sum(abs2, a)
    end
    return sqrt(n/max(d, floatmin(Float64)))
end

function radial_setup(p, cuts, coarse_archive, fine_archive)
    # This sealed packet supplies geometry and rebuilt pair kernels only.
    fine = Runner._read_linked_checkpoint(fine_archive)
    f = fine.problem
    fine.current_midpoints == cuts || error("inconsistent physical current cuts")
    (p.ne,p.nk,p.r,p.nb)==(481,13,21,7) && (f.ne,f.nk,f.r,f.nb)==(481,25,21,7) ||
        error("unexpected Fath E481 K13/K25 Q21 pair")
    srcspec = TOML.parsefile(joinpath(coarse_archive,"spec.toml"))
    dstspec = TOML.parsefile(joinpath(fine_archive,"spec.toml"))
    for key in ("device","stage_source","source_model_sha","source_fresh_sha","causal_reference_sha",
            "voltage","physical_T_K","LO_temp_K","energy_step_meV","energy_phase_meV","channels")
        srcspec[key] == dstspec[key] || error("physical packet parameter changed: $key")
    end
    srcspec["voltage"] == 0.54 && srcspec["physical_T_K"] == 10.0 ||
        error("expected frozen Fath 54 mV / 10 K")
    k = Runner._read_linked_array(coarse_archive,"k",Float64,p.nk)
    kf = Runner._read_linked_array(fine_archive,"k",Float64,f.nk)
    common = 1:2:f.nk
    k == kf[common] || error("radial nodes are not exactly nested")
    edges(k) = [first(k); (k[1:end-1] .+ k[2:end])./2; last(k)].^2
    for (radial, weights) in ((k,p.wk),(kf,f.wk))
        isapprox(diff(edges(radial))./(4π), weights; rtol=2e-13) ||
            error("archive weights do not match the physical annular measure")
    end
    for (name,a,b) in (
            (:energy,p.en,f.en),(:energy_weights,p.we,f.we),(:frame,p.v.coordinate_frame,f.v.coordinate_frame),
            (:modes,p.geo.modes,f.geo.modes),(:offsets,p.geo.offsets,f.geo.offsets),
            (:voltage,p.geo.voltage,f.geo.voltage),(:reach,p.geo.reach,f.geo.reach),
            (:hop,p.hops,f.hops[:,common]),(:H,p.h,f.h[:,:,common]),
            (:acoustic,p.v.acoustic,f.v.acoustic),(:alloy,p.v.alloy,f.v.alloy),
            (:IFR_probes,p.v.interface_probes,f.v.interface_probes),
            (:LO_plus,p.v.lo_plus,f.v.lo_plus),(:LO_minus,p.v.lo_minus,f.v.lo_minus),
            (:Bose,p.v.bose,f.v.bose),(:anchor,p.const_by_channel,f.const_by_channel[:,:,common,:]),
            (:spin,p.spin_degeneracy,f.spin_degeneracy),(:current_scale,p.current_scale,f.current_scale),
            (:density_scale,p.density_scale,f.density_scale),(:target,p.target_dimless,f.target_dimless))
        a == b || error("inconsistent physical asset: $name")
    end
    kernels = Dict(string(name)=>relerr(a,b) for (name,a,b) in (
        (:IFR, f.v.interface_pair[common,common], p.v.interface_pair),
        (:LO, f.v.lo_covariance[:,:,common,common], p.v.lo_covariance),
        (:impurity, f.v.impurity_covariance[:,:,common,common], p.v.impurity_covariance)))
    maximum(values(kernels)) < 2e-12 || error("a reconstructed kernel changed a common pair: $kernels")
    reciprocal = map((p,f)) do q
        (; IFR=pair_reciprocity(q.v.interface_pair,q.wk),
            LO=pair_reciprocity(q.v.lo_covariance,q.wk),
            impurity=pair_reciprocity(q.v.impurity_covariance,q.wk))
    end
    p_to_f = annular_transfer(k,kf,p.wk,f.wk)
    f_to_p = annular_transfer(kf,k,f.wk,p.wk)
    relerr(f.wk .* p_to_f, (p.wk .* f_to_p)') < 2e-13 ||
        error("restriction and prolongation are not weighted adjoints")
    p_to_f[common,:] == Matrix{Float64}(I,p.nk,p.nk) ||
        error("shared radial source components are not preserved")
    affine = copy(f.const_by_channel)
    retained = copy(f.const_by_channel)
    @views for i in 2:2:f.nk-1
        left = i ÷ 2
        radius_fraction = (kf[i]^2-k[left]^2)/(k[left+1]^2-k[left]^2)
        affine[:,:,i,:] .= (1-radius_fraction).*p.const_by_channel[:,:,left,:] .+
            radius_fraction.*p.const_by_channel[:,:,left+1,:]
        fill!(retained[:,:,i,:],0.)
        for j in 1:p.nk
            retained[:,:,i,:] .+= p_to_f[i,j].*p.const_by_channel[:,:,j,:]
        end
    end
    relerr(affine,f.const_by_channel) < 2e-13 ||
        error("refined radial anchor does not reproduce the archived affine continuation")
    anchor_overlap_relative_difference = relerr(retained,f.const_by_channel)
    anchor_overlap_maximum_difference_meV = 100maximum(abs,retained.-f.const_by_channel)
    return (; p,f,k,kf,common,p_to_f,f_to_p,fine_identity=fine.identity,
        kernel_common_relative=kernels,kernel_reciprocity_coarse_and_fine=reciprocal,
        anchor_overlap_relative_difference,anchor_overlap_maximum_difference_meV,
        archive_spec_sha256=file_sha(joinpath(coarse_archive,"spec.toml")))
end

function apply_radial(t, x)
    out = zeros(Float64,size(x,1),2,size(x,3),size(t,1),size(x,5))
    @views for channel in axes(x,5), i in axes(t,1), j in axes(t,2)
        weight = t[i,j]
        iszero(weight) && continue
        if isone(weight)
            copyto!(out[:,:,:,i,channel],x[:,:,:,j,channel])
        else
            out[:,:,:,i,channel] .+= weight .* x[:,:,:,j,channel]
        end
    end
    return out
end

function radial_integral(x,w,c)
    integrated = zeros(size(x,1),2,size(x,3))
    @views for k in eachindex(w)
        integrated .+= w[k].*x[:,:,:,k,c]
    end
    return integrated
end

function input_transfer_checks(pair, coarse, fine)
    channels = [relerr(radial_integral(fine,pair.f.wk,c),radial_integral(coarse,pair.p.wk,c))
        for c in axes(coarse,5)]
    @views all(isequal(fine[:,:,:,pair.common[i],:],coarse[:,:,:,i,:]) for i in eachindex(pair.common)) ||
        error("a common source component changed during prolongation")
    maximum(channels) < 2e-13 || error("prolongation failed integral conservation")
    return (; relative_integral_by_channel=channels, shared_component_maximum=0.)
end

function packed_difference(p, a, b, radial)
    fro = LT.pack_fro_weights(p.r)
    results = Dict{String,Any}()
    for (channel,name) in enumerate(LT.COLLISION_CHANNELS), part in 1:2
        n,d = zeros(p.ne,p.nk),zeros(p.ne,p.nk)
        @inbounds for k in 1:p.nk, e in 1:p.ne, i in eachindex(fro)
            x,y = a[i,part,e,k,channel], b[i,part,e,k,channel]
            w = p.weights[e,k]*fro[i]
            n[e,k] += w*abs2(x-y)
            d[e,k] += w*abs2(y)
        end
        peak = argmax(n)
        total = sum(n)
        label = string(name,part==1 ? "_L" : "_G")
        results[label] = (;relative=sqrt(total/max(sum(d),floatmin(Float64))),
            squared_weighted_difference=total, peak_E_meV=100*p.en[peak[1]],
            peak_k_nm_inverse=radial[peak[2]]/10,
            peak_squared_defect_fraction=n[peak]/max(total,floatmin(Float64)),
            squared_defect_fraction_by_ring=vec(sum(n;dims=1))./max(total,floatmin(Float64)))
    end
    return results
end

widths_at(cuts) = (cuts[3:end] .- cuts[1:end-2])./2

function radial_observe(p, source, cuts, workers; high_order=true)
    rule = if high_order
        independent_energy_rule
    else
        (problem, total, anchor, ring) -> begin
            layout = LT.CausalGeometry(problem.en,LT.tapered_support(problem.en),
                Matrix(anchor),problem.geo.voltage,maximum(abs,problem.geo.offsets))
            causal = LT.CausalRing(layout,LT.unpack_ring(total,problem.r))
            poles = LT.scan_poles(causal,problem.geo,@view(problem.h[:,:,ring]);subdivisions=2)
            LT.resonance_rule(causal,poles,18)
        end
    end
    return spatial_balance(p,source,widths_at(cuts);workers,current_cuts=cuts,energy_rule=rule)
end

function map_radial(p, seed, workers)
    image = LT.linked_fresh_map(p,seed; projector=LT.project_linked_economical,
        selected_rows=true,projection_for_collision=true,workers)
    return (; image.source, image.summary)
end

function input_stage(summary)
    observation = summary["projected_input"]
    return (;raw_lambda=observation["raw_lambda"],raw_sheet_cm2=observation["raw_sheet_cm2"],
        raw_holes_cm2=observation["raw_holes_cm2"],
        maximum_spectral_defect=maximum(observation["spectral_weight_relative_by_ring"]),
        normalization=summary["input_pair_projection"])
end

function observed_delta(a,b)
    delta = a.current_A_cm2.-b.current_A_cm2
    band_delta = a.central_bands.fraction.-b.central_bands.fraction
    return (; profile_A_cm2=delta, maximum_profile_A_cm2=maximum(abs,delta),
        mean_A_cm2=a.current.mean_internal_A_cm2-b.current.mean_internal_A_cm2,
        raw_lambda=a.raw_lambda-b.raw_lambda, raw_sheet_cm2=a.raw_sheet_cm2-b.raw_sheet_cm2,
        band_fraction=band_delta, maximum_band_fraction=maximum(abs,band_delta),
        maximum_particle_exchange_A_cm2=maximum(abs(a.particle_exchange_A_cm2[key]-
            b.particle_exchange_A_cm2[key]) for key in keys(a.particle_exchange_A_cm2)))
end

function radial_write(path, report)
    temporary = path*".tmp"
    open(temporary, "w") do io
        Runner._light_json(io,report)
        println(io)
    end
    mv(temporary,path;force=true)
end

function note(label)
    println(stderr, "radial control: ", label)
    flush(stderr)
end

function radial_control_impl(p, seed, image, cuts, workers; coarse_archive, fine_archive,
        output, coarse_iteration, baseline_observed=nothing)
    ispath(output) && error("output already exists: $output")
    pair = radial_setup(p,cuts,coarse_archive,fine_archive)
    GC.gc(false)
    f = pair.f
    fine_seed = apply_radial(pair.p_to_f,seed)
    input_checks = input_transfer_checks(pair,seed,fine_seed)
    fields_sha256 = (;coarse_input=packed_sha(seed),coarse_image=packed_sha(image.source),
        prolonged_input=packed_sha(fine_seed))
    radial_write(output,(;stage="validated_input",coarse_iteration,input_checks,fields_sha256,
        fine_identity=pair.fine_identity,kernel_common_relative=pair.kernel_common_relative,
        kernel_reciprocity=pair.kernel_reciprocity_coarse_and_fine))
    note("input, all common pairs and overlap transport verified")

    coarse_input = radial_observe(p,seed,cuts,workers)
    cell_charge = coarse_input.raw_ring_sheet_cm2 ./ p.wk
    prolonged_cell_charge = pair.p_to_f * cell_charge
    prolonged_raw_charge = dot(prolonged_cell_charge,f.wk)
    relative_charge_conservation = abs(prolonged_raw_charge/coarse_input.raw_sheet_cm2-1)
    relative_charge_conservation < 2e-13 || error("conservative transfer changed integrated density")
    fine_input = radial_observe(f,fine_seed,cuts,workers)
    coarse_band_rings = permutedims(hcat(coarse_input.central_bands.fraction_by_ring_and_band...))
    prolonged_band_rings = f.wk .* (pair.p_to_f * (coarse_band_rings ./ p.wk))
    transferred_band_fraction = vec(sum(prolonged_band_rings;dims=1))
    maximum(abs,transferred_band_fraction.-coarse_input.central_bands.fraction) < 2e-13 ||
        error("conservative transfer changed integrated band fractions")
    charge_transfer = (;coarse_cm2=coarse_input.raw_sheet_cm2,
        conservatively_transferred_cm2=prolonged_raw_charge, relative_charge_conservation,
        re_solved_refined_cm2=fine_input.raw_sheet_cm2,
        re_solved_charge_relative=fine_input.raw_sheet_cm2/coarse_input.raw_sheet_cm2-1,
        prolonged_ring_sheet_cm2=prolonged_cell_charge.*f.wk,transferred_band_fraction)
    coarse_observed = isnothing(baseline_observed) ? radial_observe(p,image.source,cuts,workers) : baseline_observed
    note("independent input charge and coarse image observed")

    fine_image = map_radial(f,fine_seed,workers)
    fine_metrics = linked_metrics(fine_image.summary,widths_at(cuts))
    coarse_metrics = linked_metrics(image.summary,widths_at(cuts))
    native_inputs = (;coarse=input_stage(image.summary),fine=input_stage(fine_image.summary))
    radial_write(output,(;stage="fresh_pair",coarse_iteration,input_checks,charge_transfer,fields_sha256,native_inputs,
        fine_identity=pair.fine_identity,kernel_common_relative=pair.kernel_common_relative,
        kernel_reciprocity=pair.kernel_reciprocity_coarse_and_fine,coarse_metrics,fine_metrics,
        native_collision_balances=(;coarse=image.summary["fresh_channel_balance"],
            fine=fine_image.summary["fresh_channel_balance"])))
    note("refined fresh map computed")

    prolong_image = apply_radial(pair.p_to_f,image.source)
    commutator = packed_difference(f,fine_image.source,prolong_image,pair.kf)
    p_f_coarse = radial_observe(f,prolong_image,cuts,workers)
    fine_observed = radial_observe(f,fine_image.source,cuts,workers)
    delta = observed_delta(fine_observed,p_f_coarse)
    coarse_to_common = observed_delta(p_f_coarse,coarse_observed)
    prolong_image = nothing
    restrict_image = apply_radial(pair.f_to_p,fine_image.source)
    restriction = packed_difference(p,restrict_image,image.source,pair.k)
    restricted_observed = radial_observe(p,restrict_image,cuts,workers)
    inverse_delta = observed_delta(restricted_observed,coarse_observed)
    roundtrip_source = apply_radial(pair.f_to_p*pair.p_to_f,image.source)
    restriction_smoothing = packed_difference(p,roundtrip_source,image.source,pair.k)
    restricted_commutator = packed_difference(p,restrict_image,roundtrip_source,pair.k)
    roundtrip_source = nothing
    restrict_image = nothing
    note("common-grid and back-restriction observations computed")
    report = (;schema="qcl-negf-fath-radial-commutator/v1",stage="completed",
        coarse_iteration,cuts_nm=cuts,
        coarse_archive_spec_sha256=pair.archive_spec_sha256,
        source_sha256=file_sha(@__FILE__),protocol_sha256=file_sha(joinpath(@__DIR__,"protocol.md")),
        fine_identity=pair.fine_identity,
        coarse_k_nm_inverse=pair.k./10,fine_k_nm_inverse=pair.kf./10,
        coarse_radial_weights=p.wk,fine_radial_weights=f.wk,
        prolongation=[collect(row) for row in eachrow(pair.p_to_f)],
        restriction=[collect(row) for row in eachrow(pair.f_to_p)],
        kernel_common_relative=pair.kernel_common_relative,
        kernel_reciprocity_coarse_and_fine=pair.kernel_reciprocity_coarse_and_fine,
        pair.anchor_overlap_relative_difference,pair.anchor_overlap_maximum_difference_meV,
        input_checks,charge_transfer,fields_sha256,native_inputs,coarse_metrics,fine_metrics,commutator,
        restriction_difference=restriction,restriction_smoothing,restricted_commutator,
        observations=(;coarse_input,fine_input,coarse_observed,
            prolong_after_coarse_map=p_f_coarse, fine_after_prolong_map=fine_observed,
            restriction_after_fine_map=restricted_observed),
        native_collision_balances=(;coarse=image.summary["fresh_channel_balance"],
            fine=fine_image.summary["fresh_channel_balance"]),
        fine_common_difference=delta, coarse_to_common_difference=coarse_to_common,
        restricted_to_coarse_difference=inverse_delta)
    radial_write(output,report)
    control = (;pair, fine_seed, fine_image, fine_observed, report)
    if isfile(output*".decompose")
        maybe_radial_mechanism(output*".mechanism.json",control,seed,image,cuts,workers)
    end
    return control
end

function maybe_radial_mechanism(output, control, seed, image, cuts, workers)
    (;pair,fine_seed,fine_image,fine_observed,report) = control
    intermediate = report.observations.prolong_after_coarse_map
    tolerance = max(intermediate.current.target_tolerance_A_cm2,
        fine_observed.current.target_tolerance_A_cm2)
    if report.fine_common_difference.maximum_profile_A_cm2 <= tolerance
        radial_write(output,(;stage="not_triggered",profile_tolerance_A_cm2=tolerance,
            measured_maximum_difference_A_cm2=report.fine_common_difference.maximum_profile_A_cm2))
        return
    end
    try
        script = joinpath(@__DIR__,"radial_mechanism.jl")
        isdefined(@__MODULE__,:radial_mechanism) || Base.include(@__MODULE__,script)
        prolong_image = apply_radial(pair.p_to_f,image.source)
        result = Base.invokelatest(radial_mechanism,pair,seed,image,fine_seed,fine_image,
            prolong_image,cuts,workers,report.commutator,intermediate,fine_observed)
        radial_write(output,(;stage="completed",profile_tolerance_A_cm2=tolerance,
            mechanism_source_sha256=file_sha(script),result...))
        note("large commutator decomposed on the common radial grid")
    catch err
        radial_failure(output,err)
    end
end


function radial_continue_impl(control, cuts, workers; maps, output)
    maps>=1 || throw(ArgumentError("the fine continuation needs at least one fresh map"))
    ispath(output) && error("output already exists: $output")
    f = control.pair.f
    state = control.fine_seed
    image = control.fine_image
    history = NamedTuple[]
    confirmation = 0
    alpha = 0.35
    for step in 1:maps
        if step > 1
            @. state = (1-alpha)*state + alpha*image.source
            image = map_radial(f,state,workers)
        end
        row = linked_metrics(image.summary,widths_at(cuts))
        confirmation = strictly_qualified(row) ? confirmation+1 : 0
        push!(history,(; fine_step=step,
            nominal_iteration=control.report.coarse_iteration+step-1,
            row..., input=input_stage(image.summary), strict_confirmations=confirmation, collision_balance=image.summary["fresh_channel_balance"]))
        spatial = row.spatial
        note("fine step $step/$maps: rK=$(row.rK) rSigma=$(row.rSigma) raw_lambda=$(row.raw_lambda) "*
            "spectral=$(row.maximum_spectral_defect) J=$(spatial.mean_internal_A_cm2) "*
            "max_dev=$(spatial.max_deviation_from_mean_A_cm2)")
        radial_write(output,(;stage="running",start_iteration=control.report.coarse_iteration,
            alpha,cuts_nm=cuts,history))
        confirmation>=3 && break
    end
    row = last(history)
    observed = length(history)==1 ? control.fine_observed : radial_observe(f,image.source,cuts,workers)
    phase = radial_observe(f,image.source,cuts,workers;high_order=false)
    lagged = spatial_balance(f,state,widths_at(cuts);collision_sources=image.source,workers,
        energy_rule=independent_energy_rule,current_cuts=cuts,
        coefficients=(row.fermionic_pair.a,row.fermionic_pair.c))
    phase_delta = observed_delta(phase,observed)
    independent_current_difference_A_cm2 = maximum(abs,observed.current_A_cm2.-row.current_profile_A_cm2)
    accepted = independent_current_difference_A_cm2 <= observed.current.target_tolerance_A_cm2 &&
        observed.current.max_deviation_from_mean_A_cm2 <= observed.current.target_tolerance_A_cm2 &&
        lagged.weighted_rK_Q<1e-8
    report = (;schema="qcl-negf-fath-radial-continuation/v1", stage="completed",
        start_iteration=control.report.coarse_iteration, requested_fine_maps=maps, alpha,cuts_nm=cuts,
        history,observed,lagged,phase_delta,independent_current_difference_A_cm2,
        stationary=confirmation>=3 && accepted)
    radial_write(output,report)
    return report
end


function radial_failure(output, err)
    err isa InterruptException && throw(err)
    note(sprint(showerror,err,catch_backtrace()))
    failure = (;stage="failed",error=sprint(showerror,err))
    radial_write(isfile(output) ? output*".error.json" : output,failure)
    return nothing
end

function radial_control(p, seed, image, cuts, workers; output, options...)
    ispath(output) && error("output already exists: $output")
    try
        return radial_control_impl(p,seed,image,cuts,workers;output,options...)
    catch err
        return radial_failure(output,err)
    end
end

function continue_fine(control, cuts, workers; maps, output)
    isnothing(control) && return nothing
    ispath(output) && error("output already exists: $output")
    try
        target_file = output * ".target"
        target = isfile(target_file) ? parse(Int,strip(read(target_file,String))) : maps
        target >= maps || throw(ArgumentError("fine target cannot shorten the requested comparison"))
        return radial_continue_impl(control,cuts,workers;maps=target,output)
    catch err
        return radial_failure(output,err)
    end
end

end # module
