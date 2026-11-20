module DirectImpurity

using LinearAlgebra
import QCLNEGF.LinkedTransport as LT

export direct_impurity

"""
Group translated energies that differ only by floating-point roundoff.
Return the actual energy used and its location for every original query.
"""
function common_queries(raw)
    !isempty(raw) && all(isfinite, raw) || throw(ArgumentError("nonfinite or empty translated energies"))
    queries = Float64[]
    location = similar(raw, Int)
    error = 0.0
    for i in sortperm(vec(raw))
        value = raw[i]
        if isempty(queries) || abs(value - last(queries)) > 32eps(Float64)*max(1.0,abs(value))
            push!(queries, value)
        end
        error = max(error, abs(value-last(queries)))
        location[i] = length(queries)
    end
    return (; queries, location, maximum_merge_error=error)
end

function lift!(target, buffer, q, field)
    mul!(buffer, q, field)
    mul!(target, buffer, q')
    return nothing
end

function direct_tile!(fields, p, energies, total, anchor, a, c)
    q, weights, covariance = p.v.coordinate_frame, p.wk, p.v.impurity_covariance
    work = LT.TailWorkspace(p.geo)
    plan = LT.CausalRows(p.en, LT.shifted_queries(p.geo, energies))
    sources = [LT.sample_packed_ring(plan, @view(total[:,:,:,kin]), @view(anchor[:,:,kin]))
        for kin in 1:p.nk]
    z_retarded = zeros(ComplexF64, p.nz, p.nz, p.nk, 1)
    z_lesser = similar(z_retarded)
    z_greater = similar(z_retarded)
    projected = zeros(ComplexF64, p.r, p.r)
    buffer = zeros(ComplexF64, p.nz, p.r)
    coordinate = zeros(ComplexF64, p.nz, p.nz)
    @views for (j,e) in enumerate(energies)
        for kin in 1:p.nk
            LT.sample_node!(work,p.geo,e,p.h[:,:,kin],p.hops[:,kin],sources[kin][:,:,:,j,:])
            ret, les, gr = (work.local_green[:,:,part] for part in 1:3)
            projected .= (ret .+ ret')./2
            lift!(z_retarded[:,:,kin,1],buffer,q,projected)
            # G< = iP and G> = -iQ. The pair projection preserves G> - G<.
            projected .= a .* les .- c .* gr
            lift!(z_lesser[:,:,kin,1],buffer,q,projected)
            projected .= (1-c) .* gr .- (1-a) .* les
            lift!(z_greater[:,:,kin,1],buffer,q,projected)
        end
        for kout in 1:p.nk
            for (part, lifted) in ((1,z_retarded),(2,z_lesser),(3,z_greater))
                LT.contract_spatial!(coordinate,lifted,covariance,weights,1,kout)
                mul!(buffer,coordinate,q)
                mul!(fields[:,:,part,j,kout],q',buffer)
            end
            ret, les, gr = (fields[:,:,part,j,kout] for part in 1:3)
            ret .= (ret .+ ret' .+ gr .- les)./2
        end
    end
    return nothing
end

"""
Apply the elastic impurity map to a single lagged Green state. At every
translated real energy R/L/G use one covariance, one spatial projector
and one radial measure. The width is computed from L/G to avoid subtracting
nearly equal retarded and advanced matrices in tails. The paired charge
coefficients affect L/G together and preserve the spectral jump.
"""
function direct_impurity(p, source, requested, a, c; workers=1, tile=12)
    size(source) == (p.r^2,2,p.ne,p.nk,length(LT.COLLISION_CHANNELS)) ||
        throw(DimensionMismatch("source must contain the five packed channels"))
    workers > 0 && tile > 0 || throw(ArgumentError("nonpositive worker count or energy tile"))
    0 <= a <= 1 && 0 <= c <= 1 || throw(ArgumentError("invalid charge pair coefficients"))
    layout = common_queries(requested)
    energies = layout.queries
    total = dropdims(sum(source; dims=5); dims=5)
    anchor = dropdims(sum(p.const_by_channel; dims=4); dims=4)
    fields = Array{ComplexF64}(undef,p.r,p.r,3,length(energies),p.nk)
    ranges = [lo:min(lo+tile-1,length(energies)) for lo in 1:tile:length(energies)]
    parallel = min(workers, Threads.nthreads(:default), length(ranges))
    LT.N._production_worker_ranges!(length(ranges),parallel) do _,lo,hi
        for i in lo:hi
            selected = ranges[i]
            @views direct_tile!(fields[:,:,:,selected,:],p,energies[selected],total,anchor,a,c)
        end
    end
    return (; layout...,fields)
end

end
