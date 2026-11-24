# Diagnose the relative bond-current trigger on the exact sealed V843 input.
length(ARGS)==3 || error("expected PUBLISHED_STUDIES ARCHIVE OUTPUT")
const v843_studies, archive, output = ARGS
include(joinpath(v843_studies,"fath-v843","continuation.jl"))
include("v843_unitary_adapter.jl")
BLAS.set_num_threads(1)

function current_samples(p, basis, source, rotated)
    q = basis.rotated
    old_ws,new_ws = LT.TailWorkspace(p.geo),LT.TailWorkspace(q.geo)
    indices = unique(round.(Int,range(1,p.ne;length=9)))
    rings = unique(round.(Int,range(1,p.nk;length=5)))
    energies = p.en[indices]
    plan = LT.CausalRows(p.en,LT.shifted_queries(p.geo,energies))
    worst = nothing
    maximum_reference = 0.0
    maximum_absolute = 0.0
    for ring in rings
        function samples(problem,state)
            s = dropdims(sum(@view(state[:,:,:,ring,:]);dims=4);dims=4)
            a = dropdims(sum(@view(problem.const_by_channel[:,:,ring,:]);dims=3);dims=3)
            return LT.sample_packed_ring(plan,s,a)
        end
        old,new = samples(p,source),samples(q,rotated)
        for (i,E) in enumerate(energies)
            @views LT.sample_node!(old_ws,p.geo,E,p.h[:,:,ring],p.hops[:,ring],old[:,:,:,i,:])
            @views LT.sample_node!(new_ws,q.geo,E,q.h[:,:,ring],q.hops[:,ring],new[:,:,:,i,:])
            reference = norm(old_ws.bond_profile)
            absolute = norm(new_ws.bond_profile-old_ws.bond_profile)
            relative = absolute/max(reference,floatmin(Float64))
            maximum_reference = max(reference,maximum_reference)
            maximum_absolute = max(absolute,maximum_absolute)
            if isnothing(worst) || relative>worst.relative
                worst = (;ring,index=indices[i],energy_meV=100E,relative,absolute,reference)
            end
        end
    end
    return (;worst,maximum_reference,maximum_absolute,
        max_absolute_over_global_reference=maximum_absolute/maximum_reference)
end

function direct_section_error(p, basis)
    q,u = basis.rotated,basis.modal
    old,rot = p.geo.modes,q.geo.modes
    peak = 0.0
    for z in first(p.geo.monitor):(last(p.geo.monitor)-1)
        a,b = @views old[z,:],old[z+1,:]
        c,d = @views rot[z,:],rot[z+1,:]
        expected = u' * (conj(a) * transpose(b)) * u
        peak = max(peak,T.relerr(conj(c)*transpose(d),expected))
    end
    return peak
end

function section_witness()
    saved = Runner._read_linked_checkpoint(archive)
    p = saved.problem
    sites = Runner._read_linked_array(archive,"ifr_sites",Float64,size(p.v.interface_probes,1),p.nz)
    basis = rotate_problem(p,sites)
    source = RankControl.lift_source(saved.seed,basis.coord').source
    probes = current_samples(p,basis,saved.seed,source)
    return (;input_sha=bytes2hex(sha256(reinterpret(UInt8,vec(saved.seed)))),
        section_operator_error=direct_section_error(p,basis),sections=p.nz+1,probes)
end

ispath(output) && error("output already exists: $output")
T.radial_write(output,section_witness())
