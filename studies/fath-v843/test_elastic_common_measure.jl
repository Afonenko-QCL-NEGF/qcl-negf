using Test
include("direct_continuum.jl")
let
    energy=[-2.0,-0.5,0.5,2.0]
    we=[0.75,1.25,1.25,0.75]
    wk=[1.0]
    rank=2
    q=Matrix{ComplexF64}(I,rank,rank)
    modes=Matrix{ComplexF64}(I,3rank,3rank)
    h=Matrix(SymTridiagonal(fill(0.0,3rank),fill(-0.15,3rank-1)))
    shift=Matrix{Float64}(I,length(energy),length(energy))
    probes=[1.0 0.0;0.35 0.65]
    kernels=LT.LocalCollisionKernels(q,wk,fill(0.01,rank),zeros(rank),probes,fill(0.021,1,1),
        zeros(ComplexF64,rank,rank,1,1),fill(0.013,rank,rank,1,1),shift,shift,0.0)
    anchor=zeros(ComplexF64,rank,rank,1,5)
    p=LT.LinkedProblem(energy,we,wk,modes,rank,[-1,0,1],0.15,1,
        reshape(h,3rank,3rank,1),fill(-0.15,rank+1,1),anchor,kernels;
        spin_degeneracy=2,current_scale=1.0,density_scale=1.0,target_dimless=0.1)
    seed=zeros(rank^2,2,length(energy),1,5)
    seed[1:rank,1,:,1,2].=[0.07,0.12]
    seed[1:rank,2,:,1,2].=[0.05,0.08]
    result=LT.linked_fresh_map(p,seed;projector=nothing)
    a,c=(result.summary["input_pair_projection"][x] for x in COEFFICIENTS)
    cuts=[0.,1.,2.]
    for channel in (IMP,IFR)
        construct=elastic_operator(channel)
        table=construct(p,seed,LT.shifted_queries(p.geo,p.en),a,c;workers=1)
        arms=integrated_arms(p,seed,result.source,p.en,p.we,cuts,table,(a,c);workers=1,channel)
        control=arms["baseline_PV"]
        @test control.profile_A_cm2 ≈ result.summary["fresh"]["raw_profile_A_cm2"] atol=1e-12
        @test control.weighted_rK ≈ result.summary["weighted_rK"] atol=1e-12
        @test control.weighted_boundary_RLG["left"] ≈ result.summary["weighted_rSigma_boundaries_RLG"]["left"] atol=1e-12
        @test arms["matched_PV"].weighted_rK ≈ arms["direct_RLG"].weighted_rK atol=1e-12
        for j in eachindex(energy)
            center=table.location[j,2]
            ret,les,gr=(table.fields[:,:,i,center,1] for i in 1:3)
            for (i,sigma) in enumerate((-im*les,im*gr))
                packed=zeros(rank^2)
                LT.pack_hermitian!(packed,sigma)
                @test packed ≈ result.source[:,i,j,1,channel] atol=1e-12
            end
            @test norm((ret-ret')-(gr-les)) < 1e-13
        end
        preparation=prepared_arms(p,seed,result.source,channel)
        chunks=map((1:2,3:4)) do index
            table=construct(p,seed,LT.shifted_queries(p.geo,energy[index]),a,c;workers=1)
            return raw_arms(p,preparation,energy[index],we[index],table,(a,c);workers=1)
        end
        combined=formatted_arms(p,map(add_raw,chunks... ),cuts;full_window=true)
        @test combined["direct_RLG"].profile_A_cm2 ≈ arms["direct_RLG"].profile_A_cm2 atol=1e-12
        @test combined["direct_RLG"].spectral_defect_by_ring ≈ arms["direct_RLG"].spectral_defect_by_ring atol=1e-12
    end
    pset=array_breakpoints(p,prepared_arms(p,seed,result.source),(-0.9,1.4),1,1)
    nodes,weights=shared_measure(pset,3)
    @test sum(weights) ≈ 4.0 atol=1e-12
    @test all(>(0),weights)
    @test length(canonical_on_shared_measure(p,prepared_arms(p,seed,result.source),nodes,weights,1)["raw_profile_A_cm2"]) == 3
    println("Elastic L/G retained for both kernels, common measure and streamed accumulation passed.")
end
