module DirectIFR

using LinearAlgebra
import QCLNEGF.LinkedTransport as LT
using ..DirectImpurity: common_queries

export direct_ifr

function incorporate!(result,interface,green,buffer)
    mul!(buffer,interface,green)
    for r in axes(interface,1)
        @views result[r]=dot(interface[r,:],buffer[r,:])
    end
    return nothing
end

function ifr_tile!(result,p,energies,source,anchor,a,c)
    work=LT.TailWorkspace(p.geo)
    plan=LT.CausalRows(p.en,LT.shifted_queries(p.geo,energies))
    sources=[LT.sample_packed_ring(plan,@view(source[:,:,:,kin]),@view(anchor[:,:,kin]))
        for kin in 1:p.nk]
    interface=p.v.interface_probes
    kernel=p.v.interface_pair
    buffer=similar(interface)
    field=zeros(ComplexF64,p.r,p.r)
    projected=zeros(ComplexF64,size(interface,1),p.nk,3)
    strength=zeros(ComplexF64,size(interface,1))
    @views for (j,e) in enumerate(energies)
        for k in 1:p.nk
            LT.sample_node!(work,p.geo,e,p.h[:,:,k],p.hops[:,k],sources[k][:,:,:,j,:])
            ret,les,gr=(work.local_green[:,:,part] for part in 1:3)
            field .= (ret.+ret')./2
            incorporate!(projected[:,k,1],interface,field,buffer)
            field .= a.*les .- c.*gr
            incorporate!(projected[:,k,2],interface,field,buffer)
            field .= (1-c).*gr .- (1-a).*les
            incorporate!(projected[:,k,3],interface,field,buffer)
        end
        for kout in 1:p.nk
            for part in 1:3
                fill!(strength,0)
                for kin in 1:p.nk
                    strength .+= (p.wk[kin]*kernel[kin,kout]) .* projected[:,kin,part]
                end
                buffer .= strength .* interface
                mul!(result[:,:,part,j,kout],interface',buffer)
            end
            ret,les,gr=(result[:,:,part,j,kout] for part in 1:3)
            ret .= (ret.+ret'.+gr.-les)./2
        end
    end
    return nothing
end

function direct_ifr(p,seed,queries,a,c;workers=1)
    size(seed)==(p.r^2,2,p.ne,p.nk,length(LT.COLLISION_CHANNELS)) ||
        throw(DimensionMismatch("source must contain the five packed channels"))
    workers>0 && 0<=a<=1 && 0<=c<=1 || throw(ArgumentError("invalid IFR workers or charge coefficient"))
    layout=common_queries(queries)
    source=dropdims(sum(seed;dims=5);dims=5)
    anchor=dropdims(sum(p.const_by_channel;dims=4);dims=4)
    fields=Array{ComplexF64}(undef,p.r,p.r,3,length(layout.queries),p.nk)
    ranges=[lo:min(lo+11,length(layout.queries)) for lo in 1:12:length(layout.queries)]
    parallel=min(workers,Threads.nthreads(:default),length(ranges))
    LT.N._production_worker_ranges!(length(ranges),parallel) do _,lo,hi
        for i in lo:hi
            selected=ranges[i]
            @views ifr_tile!(fields[:,:,:,selected,:],p,layout.queries[selected],source,anchor,a,c)
        end
    end
    return (;layout...,fields)
end

end
