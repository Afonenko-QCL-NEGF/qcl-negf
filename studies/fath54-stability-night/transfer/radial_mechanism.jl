# Included in FathRadialControl. Keep the production collision map in Core.
function normalized_radial_occupation(p, source, workers)
    total = dropdims(sum(source;dims=5);dims=5)
    anchor = dropdims(sum(p.const_by_channel;dims=4);dims=4)
    projected = LT.projected_image(p,total,anchor,:input_projected;
        projector=LT.project_linked_economical,selected_rows=true,order=18,
        subdivisions=2,grading=true,workers,observe=_->nothing)
    occupation = similar(projected.occupation)
    normalization = LT.prepare_occupation!(occupation,projected,p)
    return (;occupation,normalization)
end

function normalize_replay(occupation, summary)
    for key in ("a","c","physical_sheet_cm2")
        isapprox(occupation.normalization[key],summary["input_pair_projection"][key];rtol=2e-13,atol=2e-15) ||
            error("occupation replay changed the normalization: $key")
    end
end

function prolong_occupation(pair, coarse)
    n = reshape(coarse.occupation,pair.p.r^2,2,pair.p.ne,pair.p.nk,1)
    transported = dropdims(apply_radial(pair.p_to_f,n);dims=5)
    function integrated_charge(g,p)
        return sum(p.weights[e,k]*sum(@view(g[1:p.r,1,e,k])) for e in 1:p.ne,k in 1:p.nk)
    end
    charge_coarse = integrated_charge(coarse.occupation,pair.p)
    charge_transfer = integrated_charge(transported,pair.f)
    relative = abs(charge_transfer/charge_coarse-1)
    relative < 2e-13 || error("normalized occupation transfer changed integrated charge")
    return (;transported,relative_charge=relative)
end

function pair_factor(v, channel, kin, kout, incoming, outgoing)
    if channel==:LO || channel==:impurity
        covariance = channel==:LO ? v.lo_covariance : v.impurity_covariance
        a = @view covariance[:,:,kin,kout]
        return real(dot(outgoing,a.*incoming))
    end
    if channel==:IFR
        return v.interface_pair[kin,kout]*dot(incoming,outgoing)
    end
    strength = channel==:acoustic ? v.acoustic : v.alloy
    return dot(strength .* real.(diag(incoming)),real.(diag(outgoing)))
end

function window_pair_events(f, occupation, channel, eout, kout; part=1)
    v = f.v
    q = v.coordinate_frame
    s = v.interface_probes
    kdim = size(f.h,3)
    function coordinate_density(part,e,k)
        g = zeros(ComplexF64,f.r,f.r)
        LT.unpack_hermitian!(g,@view occupation[:,part,e,k])
        if channel==:IFR
            return real.(diag(s*g*s'))
        end
        return q*g*q'
    end
    paired_part = 3-part
    receiver = coordinate_density(paired_part,eout,kout)
    pairs = NamedTuple[]
    directions = if channel==:LO
        forward, backward = part==1 ? (v.lo_plus,v.lo_minus) : (v.lo_minus,v.lo_plus)
        ((name="emission",matrix=forward,reverse=backward,bose=1+v.bose),
            (name="absorption",matrix=backward,reverse=forward,bose=v.bose))
    else
        ((name="elastic",matrix=nothing,reverse=nothing,bose=1.),)
    end
    for direction in directions
        if channel==:LO
            energy_donors = findall(>(0),direction.matrix[eout,:])
            missing_forward = max(0.,1-sum(direction.matrix[eout,:]))
            missing_reverse = max(0.,1-sum(direction.reverse[:,eout].*f.we./f.we[eout]))
        else
            energy_donors = [eout]
            missing_forward = missing_reverse = 0.
        end
        events = NamedTuple[]
        for ein in energy_donors, kin in 1:kdim
            donor = coordinate_density(part,ein,kin)
            forward_weight = f.we[eout]*f.wk[kout]*f.wk[kin]*direction.bose
            reverse_weight = f.we[ein]*f.wk[kout]*f.wk[kin]*direction.bose
            if channel==:LO
                forward_weight *= direction.matrix[eout,ein]
                reverse_weight *= direction.reverse[ein,eout]
            end
            gain = forward_weight*pair_factor(v,channel,kin,kout,donor,receiver)
            loss = reverse_weight*pair_factor(v,channel,kout,kin,receiver,donor)
            push!(events,(;ein,kin,gain,loss))
        end
        paired_error = sum(x->abs(x.gain-x.loss),events;init=0.) /
            max(sum(x->abs(x.gain)+abs(x.loss),events;init=0.),floatmin(Float64))
        aggregate_gain = sum(x->x.gain,events;init=0.)
        aggregate_loss = sum(x->x.loss,events;init=0.)
        total_magnitude = sum(x->abs(x.gain),events;init=0.)
        top = first(sort!(events;by=x->abs(x.gain),rev=true),min(5,length(events)))
        dominant = [(;energy_meV=100*f.en[x.ein],ring=x.kin,
            gain_fraction=abs(x.gain)/max(total_magnitude,floatmin(Float64))) for x in top]
        push!(pairs,(;direction=direction.name,missing_forward,missing_reverse,paired_error,
            aggregate_gain,aggregate_loss,dominant))
    end
    return pairs
end

function verify_window_events(f, state, occupation, channel, e, k, part)
    pairs = window_pair_events(f,occupation,channel,e,k;part)
    index = findfirst(==(channel),LT.COLLISION_CHANNELS)
    fro = LT.pack_fro_weights(f.r)
    source = @view state[:,part,e,k,index]
    bath = @view occupation[:,3-part,e,k]
    expected = f.we[e]*f.wk[k]*dot(fro.*source,bath)
    reconstructed = sum(x->x.aggregate_gain,pairs)
    relative = abs(reconstructed-expected)/max(abs(expected),abs(reconstructed),floatmin(Float64))
    relative < 2e-12 || error("paired $channel replay disagrees with production source: $relative")
    return (; relative_production_replay=relative,pairs)
end

function radial_mechanism(pair, seed, coarse_image, fine_seed, fine_image, prolong_image,
        cuts, workers, commutator, coarse_prolong_observed, fine_observed)
    coarse = normalized_radial_occupation(pair.p,seed,workers)
    fine = normalized_radial_occupation(pair.f,fine_seed,workers)
    normalize_replay(coarse,coarse_image.summary)
    normalize_replay(fine,fine_image.summary)
    transported = prolong_occupation(pair,coarse)
    alternate = similar(prolong_image)
    LT.scatter_packed!(alternate,transported.transported,pair.f.v)
    balance = LT.local_collision_balance(pair.f,transported.transported,alternate)
    collision_operator_effect = packed_difference(pair.f,alternate,prolong_image,pair.kf)
    input_response_effect = packed_difference(pair.f,fine_image.source,alternate,pair.kf)
    alternate_observed = radial_observe(pair.f,alternate,cuts,workers)
    operator_current = observed_delta(alternate_observed,coarse_prolong_observed)
    input_current = observed_delta(fine_observed,alternate_observed)
    closure = maximum(abs,(operator_current.profile_A_cm2 .+ input_current.profile_A_cm2) .-
        (fine_observed.current_A_cm2.-coarse_prolong_observed.current_A_cm2))
    peak_by_part = Dict{String,Any}()
    for (part,suffix) in enumerate(("_L","_G"))
        names = filter(key->endswith(key,suffix),collect(keys(commutator)))
        name = argmax(n->commutator[n].squared_weighted_difference,names)
        location = commutator[name]
        channel = Symbol(chop(name;tail=2))
        e = argmin(abs.(100 .* pair.f.en .- location.peak_E_meV))
        k = argmin(abs.(pair.kf./10 .- location.peak_k_nm_inverse))
        pair_measurements = try
            (;fine_occupation_pairs=verify_window_events(pair.f,fine_image.source,
                fine.occupation,channel,e,k,part),
              transferred_occupation_pairs=verify_window_events(pair.f,alternate,
                transported.transported,channel,e,k,part))
        catch err
            err isa InterruptException && rethrow()
            (;paired_replay_error=sprint(showerror,err))
        end
        peak_by_part[suffix] = (;channel,energy_meV=location.peak_E_meV,
            k_nm_inverse=location.peak_k_nm_inverse,pair_measurements...)
    end
    return (;schema="qcl-negf-fath-radial-mechanism/v1",
        normalized_occupation_charge_conservation_relative=transported.relative_charge,
        balance_for_transferred_occupation=balance,collision_operator_effect,input_response_effect,
        alternate_observed,operator_current,input_current,
        maximum_current_telescope_error_A_cm2=closure, peak_by_part)
end
