# Rotations keep both the periodwise modal span and the coordinate span fixed.
function fixed_rotation(rank)
    u = Matrix{ComplexF64}(I,rank,rank)
    i,j = 1,rank
    c,s = cos(0.37),sin(0.37)*cis(0.61)
    u[i,i] = u[j,j] = c
    u[i,j],u[j,i] = s,-conj(s)
    return u
end

function rotate_problem(p, sites)
    coord = fixed_rotation(p.r)
    modal = zeros(ComplexF64,size(p.geo.metric))
    for block in p.geo.block_ranges
        modal[block,block] .= fixed_rotation(length(block))
    end
    v = p.v
    kernel = RankControl.lo_kernel(v,sites,v.lo_plus,v.lo_minus;q=v.coordinate_frame*coord)
    h = similar(p.h)
    anchors = similar(p.const_by_channel)
    for k in 1:p.nk
        @views h[:,:,k] .= modal' * p.h[:,:,k] * modal
        for c in eachindex(LT.COLLISION_CHANNELS)
            @views anchors[:,:,k,c] .= coord' * p.const_by_channel[:,:,k,c] * coord
        end
    end
    rotated = RankControl.rebuild(p,kernel;modes=p.geo.modes*modal,h,anchor=anchors)
    return (;rotated,coord,modal)
end

function probe_covariance(p,basis,source,rotated_source; by_channel=false)
    q,coord,modal = basis.rotated,basis.coord,basis.modal
    old_ws,new_ws = LT.TailWorkspace(p.geo),LT.TailWorkspace(q.geo)
    max_green, max_local, max_current, max_sources = 0.0,0.0,0.0,0.0
    sample_indices = unique(round.(Int,range(1,p.ne;length=9)))
    sample_rings = unique(round.(Int,range(1,p.nk;length=5)))
    energies = p.en[sample_indices]
    plan = LT.CausalRows(p.en,LT.shifted_queries(p.geo,energies))
    for k in sample_rings
        if by_channel
            for c in eachindex(LT.COLLISION_CHANNELS)
                sigma = @views LT.sample_packed_ring(plan,source[:,:,:,k,c],p.const_by_channel[:,:,k,c])
                after = @views LT.sample_packed_ring(plan,rotated_source[:,:,:,k,c],q.const_by_channel[:,:,k,c])
                for e in axes(sigma,4), period in axes(sigma,5), part in 1:3
                    max_sources = max(max_sources,@views T.relerr(after[:,:,part,e,period],
                        coord' * sigma[:,:,part,e,period] * coord))
                end
            end
        end
        s = dropdims(sum(@view(source[:,:,:,k,:]);dims=4);dims=4)
        t = dropdims(sum(@view(rotated_source[:,:,:,k,:]);dims=4);dims=4)
        a = dropdims(sum(@view(p.const_by_channel[:,:,k,:]);dims=3);dims=3)
        b = dropdims(sum(@view(q.const_by_channel[:,:,k,:]);dims=3);dims=3)
        input = LT.sample_packed_ring(plan,s,a)
        output = LT.sample_packed_ring(plan,t,b)
        for (i,E) in enumerate(energies)
            @views LT.sample_node!(old_ws,p.geo,E,p.h[:,:,k],p.hops[:,k],input[:,:,:,i,:])
            @views LT.sample_node!(new_ws,q.geo,E,q.h[:,:,k],q.hops[:,k],output[:,:,:,i,:])
            for part in 1:3
                @views max_green = max(max_green,T.relerr(new_ws.mode_green[:,:,part],
                    modal' * old_ws.mode_green[:,:,part] * modal))
                @views max_local = max(max_local,T.relerr(new_ws.local_green[:,:,part],
                    coord' * old_ws.local_green[:,:,part] * coord))
            end
            max_current = max(max_current,T.relerr(new_ws.bond_profile,old_ws.bond_profile))
        end
    end
    return (;mode_RLG=max_green,local_RLG=max_local,bond_current=max_current,
        per_channel_RLG_maximum=max_sources,sample_indices,sample_rings)
end

function unitary_control(p, state, image, cuts, workers, radii, sites)
    basis = rotate_problem(p,sites)
    q = basis.rotated
    transformed = RankControl.lift_source(state,basis.coord').source
    algebra = (;modal=norm(basis.modal'*basis.modal-I),coordinate=norm(basis.coord'*basis.coord-I),
        metric=T.relerr(q.geo.metric,basis.modal'*p.geo.metric*basis.modal),
        ifr_probe=T.relerr(q.v.interface_probes,p.v.interface_probes*basis.coord))
    mapped_input = probe_covariance(p,basis,state,transformed;by_channel=true)
    rotated_map = arm_image(q,transformed,cuts,workers)
    unmapped = RankControl.lift_source(rotated_map.source,basis.coord).source
    emitted_LG = T.packed_difference(p,unmapped,image.source,radii)
    emitted_RLG = probe_covariance(p,basis,image.source,rotated_map.source;by_channel=true)
    base = fresh_row(p,image,cuts)
    trial = fresh_row(q,rotated_map,cuts)
    independent = observed_row(direct_observation(q,rotated_map.source,cuts,workers),cuts)
    ref = observed_row(direct_observation(p,image.source,cuts,workers),cuts)
    delta = (;rK=trial.rK-base.rK,rSigma=trial.rSigma-base.rSigma,
        raw_lambda=trial.raw_lambda-base.raw_lambda,
        native_profile=maximum(abs,trial.current_profile_A_cm2.-base.current_profile_A_cm2),
        independent_profile=maximum(abs,independent.profile.-ref.profile))
    # Pointwise comparisons at very small tails are reported as well as integrated norms.
    structural = maximum(values(algebra))<2e-12
    collision_covariant = maximum(r.relative for r in values(emitted_LG))<1e-7
    observation_covariant = max(delta.independent_profile,delta.native_profile)<1e-5
    first_difference = if !structural
        "basis_metric_or_interface"
    elseif mapped_input.per_channel_RLG_maximum>=1e-6
        "input_causal_channel"
    elseif max(mapped_input.mode_RLG,mapped_input.local_RLG)>=1e-6
        "input_Dyson_green_function"
    elseif mapped_input.bond_current>=1e-6
        "input_current_operator"
    elseif !collision_covariant
        "fresh_collision"
    elseif !observation_covariant
        "fresh_current"
    else
        nothing
    end
    return (;input_sha=T.packed_sha(state),image_sha=T.packed_sha(image.source),
        same_modal_rank=p.nb,same_coordinate_rank=p.r,algebra,mapped_input,emitted_LG,emitted_RLG,
        base,trial,delta,first_difference,passes=isnothing(first_difference))
end

function overlapping_states(p,k,omega)
    cols = p.geo.center_modes
    modes = eigen(Hermitian(p.h[cols,cols,k]),Hermitian(p.geo.metric[cols,cols]))
    transitions = [(i,j) for i in 1:(p.nb-1) for j in (i+1):p.nb]
    best = argmin([abs(modes.values[b]-modes.values[a]-omega) for (a,b) in transitions])
    low,high = transitions[best]
    frame = LT.centered_basis(p.geo)[:,cols]
    normalize(v) = v/norm(v)
    return (;low,high,energies=modes.values[[low,high]],
        low_q=normalize(frame*modes.vectors[:,low]),high_q=normalize(frame*modes.vectors[:,high]))
end

function lo_diagonal_control(p,sites,ring,omega)
    v = p.v
    sel = ring:ring
    selected = overlapping_states(p,ring,omega)
    lower = sum(selected.energies)/2-omega/2
    upper = lower+omega
    step = minimum(diff(p.en))
    widths = step .* (0.5,1.0,2.0,4.0)
    min(lower-first(p.en),last(p.en)-upper)>8maximum(widths) ||
        error("the diagonal LO fixture is too close to the finite energy edge")
    subset(plus,minus) = LT.LocalCollisionKernels(v.coordinate_frame,p.wk[sel],v.acoustic,v.alloy,
        sites,v.interface_pair[sel,sel],@view(v.lo_covariance[:,:,sel,sel]),
        @view(v.impurity_covariance[:,:,sel,sel]),plus,minus,0.)
    emit = subset(v.lo_plus,v.lo_minus)
    absorb = subset(v.lo_minus,v.lo_plus)
    occupation = zeros(Float64,p.r^2,2,p.ne,1)
    destination = zeros(Float64,p.r^2,2,p.ne,1,length(LT.COLLISION_CHANNELS))
    unpacked = zeros(ComplexF64,p.r,p.r)
    packed = zeros(Float64,p.r^2)
    lo = only(findall(==(:LO),LT.COLLISION_CHANNELS))
    physical_covariance = @view v.lo_covariance[:,:,ring,ring]
    function matrix_element(a,b)
        difference = conj.(v.coordinate_frame*a).*(v.coordinate_frame*b)
        return real(dot(difference,physical_covariance*difference))
    end
    function measure(kernel,initial,final,Ei,Ef,bose,sigma)
        gaussian(E) = exp.(-((p.en .- E)./sigma).^2 ./2)./(sqrt(2π)*sigma)
        initial_profile,final_profile = gaussian(Ei),gaussian(Ef)
        LT.pack_hermitian!(packed,initial*initial')
        @views occupation[:,1,:,1] .= packed .* reshape(initial_profile,1,:)
        LT.scatter_packed!(destination,occupation,kernel)
        sampled = 0.
        for e in 1:p.ne
            @views LT.unpack_hermitian!(unpacked,destination[:,1,e,1,lo])
            sampled += p.we[e]*final_profile[e]*real(dot(final,unpacked*final))
        end
        observed = bose*p.wk[ring]*sampled
        M = matrix_element(initial,final)
        reference = bose*p.wk[ring]^2*M/(2sqrt(π)*sigma)
        return (;observed,reference,matrix_element=M,
            relative=abs(observed-reference)/max(abs(reference),floatmin(Float64)),
            input_energy_integral=dot(initial_profile,p.we),output_energy_integral=dot(final_profile,p.we))
    end
    rates = map(widths) do sigma
        emission = measure(emit,selected.high_q,selected.low_q,upper,lower,1+v.bose,sigma)
        absorption = measure(absorb,selected.low_q,selected.high_q,lower,upper,v.bose,sigma)
        return (;sigma_meV=100sigma,emission,absorption,
            observed_detailed_ratio=absorption.observed/emission.observed)
    end
    return (;ring,phonon_meV=100omega,levels=(selected.low,selected.high),
        bare_energies_meV=100selected.energies,shell_centers_meV=100 .* (lower,upper),
        expected_bose_ratio=v.bose/(1+v.bose),rates)
end

