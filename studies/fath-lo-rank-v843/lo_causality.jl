include("fath_factorial.jl")

# Integrate the piecewise-linear width after subtracting the value at the
# pole. The interval(s) incident on the pole then have constant integrand.
function quadrature_pv(support, gamma, q, rule)
    result = zeros(size(gamma,1))
    interior = first(support)<q<last(support)
    at_q = if interior
        j = searchsortedlast(support,q)
        t = (q-support[j])/(support[j+1]-support[j])
        (1-t).*gamma[:,j] .+ t.*gamma[:,j+1]
    else
        zero(result)
    end
    for j in 1:(length(support)-1)
        lo,hi = support[j],support[j+1]
        a,b = view(gamma,:,j),view(gamma,:,j+1)
        radius = (hi-lo)/2
        if interior && lo<=q<=hi
            result .+= a.-b
        else
            for (node,w) in zip(rule.nodes,rule.weights)
                t = (node+1)/2
                x = lo+t*(hi-lo)
                result .+= (radius*w/(q-x)).*((1-t).*a .+ t.*b .- at_q)
            end
        end
    end
    if interior
        result .+= at_q.*log(abs((q-first(support))/(q-last(support))))
    end
    return result./(2π)
end

function check_triplet(r, l, g, direct, anchor)
    dispersive = (r+r')/2-anchor
    return (;
        jump_absolute=norm(r-r'-(g-l)),
        jump_relative_to_retarded_and_kinetic=norm(r-r'-(g-l))/
            max(norm(r)+norm(g)+norm(l),floatmin(Float64)),
        causal_relative=norm(dispersive-direct)/max(norm(dispersive)+norm(direct),1e-300),
        causal_absolute=norm(dispersive-direct),
        spectral_minimum=minimum(eigvals(Hermitian(im*(g-l)))),
        Kinetics_antihermitian_relative=max(norm(l+l'),norm(g+g'))/
            max(norm(l)+norm(g),1e-300))
end

function audit_ring(p, packed, k)
    anchor = p.const_by_channel[:,:,k,1]
    layout = LT.CausalGeometry(p.en,LT.tapered_support(p.en),anchor,p.geo.voltage,maximum(abs,p.geo.offsets))
    ring = LT.CausalRing(layout,LT.unpack_ring(packed,p.r))
    guard = zeros(p.r^2)
    gamma = hcat(guard,packed[:,1,:]+packed[:,2,:],guard)
    nodes = LT.gauss_rule(32)
    criteria = [first(p.en),last(p.en),p.en[div(p.ne,2)],p.en[div(p.ne,2)+1]+0.37*(p.en[2]-p.en[1])]
    points = sort!(unique([q+j*p.geo.voltage for q in criteria for j in (-2,0,2)]))
    fields = LT.source_triplets(ring,points)
    nodal = LT.sample_packed_ring(LT.CausalRows(p.en,reshape(points,:,1)),packed,anchor)
    return map(eachindex(points)) do i
        q = points[i]
        direct = zeros(ComplexF64,p.r,p.r)
        LT.unpack_hermitian!(direct,quadrature_pv(layout.support,gamma,q,nodes))
        r,l,g = (view(f,i,1,:,:) for f in (fields.Σᴿ,fields.Σˡ,fields.Σᵍ))
        nodal_triplet = (view(nodal,:,:,j,i,1) for j in 1:3)
        difference = [norm(x-y)/max(norm(x)+norm(y),1e-300) for (x,y) in zip((r,l,g),nodal_triplet)]
        return (;energy_meV=100q,nodal_continuous_RLG_relative=difference,
            check_triplet(r,l,g,direct,anchor)...)
    end
end

function causality_main()
    length(ARGS)==3 || error("Usage: lo_causality.jl ARCHIVE WORKERS OUTPUT")
    archive,worker_arg,output = ARGS
    workers = parse(Int,worker_arg)
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    input = Runner._read_linked_checkpoint(archive)
    p = input.problem
    p.geo.voltage≈0.54 && input.identity["temperature_K"]==10.0 || error("expected Fath at 54 mV and 10 K")
    projected = collision_input(p,input.seed,workers)
    local_channels = similar(input.seed)
    LT.scatter_packed!(local_channels,projected.occupation,p.v)
    checks=map(unique([1,cld(p.nk,2),p.nk])) do k
        (;ring_index=k,queries=audit_ring(p,view(local_channels,:,:,:,k,1),k))
    end
    open(output,"w") do io
        Runner._light_json(io,(;schema="qcl-negf-lo-causality/v1",input.identity,
            core=Runner._linked_package_identity(Runner.QCLNEGF),
            runner=Runner._linked_package_identity(Runner),runtime=Runner._runtime_toolchain_provenance(),
            normalization=projected.normalization,checks))
        println(io)
    end
end

abspath(PROGRAM_FILE)==abspath(@__FILE__) && causality_main()
