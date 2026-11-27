#!/usr/bin/env julia
# Independent, reduced coordinate-space diagnostic; no transport state required.
using QCLNEGF, Unitful, LinearAlgebra, TOML, SHA
include(joinpath(@__DIR__, "..", "fath-v843", "controls", "v843-input", "dupont", "dupont_device.jl"))
const DEVICE = DupontDevice.DEFAULT_DEVICE
const NS = (64,128,256,512,1024,2048,4096)
const BASE_WIDTH = 2pi/64
const FORWARD_WIDTH = pi/64 # independent narrower angular sector

# Three unique elements of the covariance restricted to the two coordinate nodes.
# Returns full, forward sector (trapezoidal endpoints) and its complement.
function integrate_pair(k, kp, qs, pref, distances, donor; counts=NS, width=BASE_WIDTH)
    nmax = maximum(counts)
    all(nmax % n == 0 && n % 64 == 0 for n in counts) || error("incompatible nested angles")
    full = zeros(3,length(counts)); sector = similar(full); fill!(sector,0)
    for r in 0:nmax-1
        angle = 2pi*r/nmax
        # Stable at equal rings and phi=0, without subtractive cancellation.
        q = sqrt((k-kp)^2 + 4k*kp*sin(angle/2)^2)
        scale = (pref/(q+qs))^2
        v1 = 0.0; v2 = 0.0; v3 = 0.0
        for s in eachindex(donor)
            a,b = distances[1,s],distances[2,s]
            ea=exp(-q*a); eb=exp(-q*b); d=donor[s]*scale
            v1 += d*ea*ea; v2 += d*ea*eb; v3 += d*eb*eb
        end
        for (j,n) in pairs(counts)
            r % (nmax ÷ n) == 0 || continue
            m = r ÷ (nmax ÷ n)
            # Fraction of the angular cell around this periodic sample inside
            # the sector. At aligned endpoints this is trapezoidal half weight;
            # for N=64 and pi/64 it gives the sole phi=0 sample full weight.
            edge = width*n/(2pi)
            sw = clamp(edge + 0.5 - min(m,n-m), 0.0, 1.0)
            full[1,j] += v1/n; full[2,j] += v2/n; full[3,j] += v3/n
            sector[1,j] += sw*v1/n; sector[2,j] += sw*v2/n; sector[3,j] += sw*v3/n
        end
    end
    return full,sector,full-sector
end

# Frobenius norm of the Schur product C .* P, P=I/2 or ones(2,2)/2.
norm2(v, coherent) = (v[1]^2 + v[3]^2 + (coherent ? 2v[2]^2 : 0.0))/4
function fixtures()
    # q=0 constant integrand: periodic quadrature and both sector endpoints.
    f,s,r = integrate_pair(0.,0.,1.,1.,zeros(2,1),[1.]; counts=(64,128))
    @assert maximum(abs.(f .- 1)) < 1e-13
    @assert maximum(abs.(s .- 1/32)) < 1e-13
    @assert maximum(abs.(f .- s .- r)) < 1e-14
    fn,sn,rn = integrate_pair(0.,0.,1.,1.,zeros(2,1),[1.]; counts=(64,128), width=FORWARD_WIDTH)
    @assert maximum(abs.(fn .- 1)) < 1e-13
    @assert maximum(abs.(sn .- 1/64)) < 1e-13
    @assert maximum(abs.(fn .- sn .- rn)) < 1e-14
    @assert all(sn .< s)
    # Nonconstant equal-ring peak: nested reference differences and partition.
    f2,s2,r2 = integrate_pair(2.,2.,0.1,1.,[0.0; 1.0;;],[1.]; counts=(64,128,2048,4096), width=FORWARD_WIDTH)
    @assert maximum(abs.(f2 .- s2 .- r2)) < 1e-12
    @assert f2[1,1] > f2[1,end] && s2[1,end] > 0 && r2[1,end] > 0
    @assert abs(f2[1,3]-f2[1,4]) < abs(f2[1,1]-f2[1,4])
    @assert norm2([1.,1.,1.],true) > norm2([1.,1.,1.],false)
    @assert sqrt((2.0 - 2.0)^2+4*2*2*sin(0/2)^2)==0
end
function main(args)
    length(args)==4 || error("Usage: julia --project=runner impurity.jl NZ NK BASE|FORWARD OUTPUT.toml")
    nz,nk = parse.(Int,args[1:2]); mode=args[3]
    nz in (216,288,384) || error("NZ must be 216, 288 or 384")
    nk in (9,17,33,65) || error("NK must be 9, 17, 33 or 65")
    mode in ("BASE","FORWARD") || error("mode must be BASE or FORWARD")
    fixtures()
    BLAS.set_num_threads(1)
    width = mode == "BASE" ? BASE_WIDTH : FORWARD_WIDTH
    scales=ScaleSystem(); device=DupontDevice.physical_inputs(21.0); p=device.physical
    n=NumericalParameters(N_z=nz,N_b=11,P_basis=4,E_min=-0.65u"eV",E_max=1.0u"eV",N_E=121,M_E=0.39u"eV",k_max=0.60u"nm^-1",N_k=nk,N_φ=64,qz_max=10.0u"nm^-1",N_qz=161,η_seed=0.5u"meV")
    g=build_grids(p,n,scales); profile=DupontDevice.sheet_profiles(p,n,scales,g,device.donor_center)
    @assert all(>(0),g.wᵏ)
    @assert maximum(abs.(g.φ .- [2pi*r/64 for r in 0:63])) < 1e-14
    donor=g.wˣ .* profile.Nᴰ ./ scales.L₀_m^2
    active=findall(>(0),donor)
    length(active) in (1,2) || error("expected the discretized centre sheet")
    # Closest nodes to two fixed physical locations, one at donor and one at half period.
    targets=[scaled_value(device.donor_center,scales,:length), (first(g.x)-g.wˣ[1]/2 + nz*g.wˣ[1]/2)]
    picks=[argmin(abs.(g.x .- z)) for z in targets]
    length(unique(picks))==2 || error("probe points coincide")
    distances=abs.(g.x[picks] .- transpose(g.x[active]))
    qs=scaled_value(p.q_s,scales,:wavenumber)
    pref=(1.602176634e-19)^2/(2*8.8541878128e-12*p.ε_s*scales.E₀_J)
    sums=zeros(3,2,length(NS),2); worst=zeros(3,2,length(NS)); worstpair=zeros(Int,3,2,length(NS),2)
    pairerrors=zeros(3,2,length(NS)-1,nk,nk)
    pairnum=zeros(3,2,length(NS)-1,nk,nk); pairden=similar(pairnum)
    peaks=zeros(3,nk,nk); ratios=zeros(nk,nk)
    # Each input ring owns its output slots; no shared accumulation in threads.
    Threads.@threads for i in 1:nk
      for j in 1:nk
        full,sec,rest=integrate_pair(g.κ[i],g.κ[j],qs,pref,distances,donor[active]; width)
        pieces=(full,sec,rest)
        for (part,mat) in pairs(pieces), coherent in 0:1, a in 1:length(NS)-1
            d=mat[:,a]-mat[:,end]; ref=mat[:,end]
            err=norm2(d,coherent==1); den=norm2(ref,coherent==1)
            pairnum[part,coherent+1,a,i,j]=err
            pairden[part,coherent+1,a,i,j]=den
            # Relative pair error normalized by full reference to remain meaningful
            # for a small rest or sector. Outputs retain the aggregate sector norm too.
            denom=norm2(full[:,end],coherent==1)
            rel=sqrt(err/denom)
            pairerrors[part,coherent+1,a,i,j]=rel

        end
        # Actual integrand at forward angle, versus its 4096-point average.
        q=abs(g.κ[i]-g.κ[j]); val=sum(donor[active].*exp.(-2q.*distances[1,:]))*(pref/(q+qs))^2
        ratio=val/full[1,end]
        ratios[i,j]=ratio; peaks[:,i,j].=[val,full[1,end],q]
      end
    end
    # Fixed i,j order makes aggregation independent of thread scheduling.
    peak=zeros(3); peakpair=(0,0); peakratio=0.0
    for i in 1:nk, j in 1:nk
        weight=g.wᵏ[i]*g.wᵏ[j]
        for part in 1:3, ci in 1:2, a in 1:length(NS)-1
            sums[part,ci,a,1]+=weight*pairnum[part,ci,a,i,j]
            sums[part,ci,a,2]+=weight*pairden[part,ci,a,i,j]
            rel=pairerrors[part,ci,a,i,j]
            if rel>worst[part,ci,a]
                worst[part,ci,a]=rel; worstpair[part,ci,a,:].=[i,j]
            end
        end
        if ratios[i,j]>peakratio
            peakratio=ratios[i,j]; peakpair=(i,j); peak=peaks[:,i,j]
        end
    end
    results=Dict{String,Any}()
    for (part,label) in enumerate(("full","forward","rest")), (ci,probe) in enumerate(("diagonal","coherent"))
        entries=Dict{String,Any}()
        for a in 1:length(NS)-1
            den=sums[part,ci,a,2]
            entries[string(NS[a])]=Dict("weighted_relative_frobenius_error"=>sqrt(sums[part,ci,a,1]/den),"worst_pair_error_over_full_reference"=>worst[part,ci,a],"worst_pair_1based"=>vec(worstpair[part,ci,a,:]),"pair_error_rows_incoming_columns_outgoing"=>[collect(pairerrors[part,ci,a,i,:]) for i in 1:nk])
        end
        # Both aggregate and every pair must meet 1%; reference convergence must meet 0.1%.
        stable=entries["2048"]["weighted_relative_frobenius_error"]<=0.001 && entries["2048"]["worst_pair_error_over_full_reference"]<=0.001
        eligible=[a for a in NS[1:5] if entries[string(a)]["weighted_relative_frobenius_error"]<=0.01 && entries[string(a)]["worst_pair_error_over_full_reference"]<=0.01]
        results[label*"_"*probe]=Dict("reference_2048_vs_4096_stable_0_1_percent"=>stable,"minimum_candidate_at_1_percent"=>(stable && !isempty(eligible) ? first(eligible) : 0),"reference_weighted_norm"=>sqrt(sums[part,ci,1,2]),"reference_norm_over_full"=>sqrt(sums[part,ci,1,2]/sums[1,ci,1,2]),"comparisons"=>entries)
    end
    out=Dict{String,Any}("schema"=>"v843-impurity-angle-coordinate-diagnostic/1","mode"=>mode,"field_kV_cm"=>21.0,"temperature_K"=>50.0,"julia_threads"=>Threads.nthreads(),"blas_threads"=>BLAS.get_num_threads(),"nz"=>nz,"nk"=>nk,"n_basis_placeholder"=>11,"radial_nodes"=>g.κ,"radial_weights"=>g.wᵏ,"screening_dimensionless"=>qs,"donor_indices_1based"=>active,"donor_weight_dimensionless"=>donor[active],"probe_indices_1based"=>picks,"probe_x_dimensionless"=>g.x[picks],"probe_x_nm"=>g.x[picks].*scales.L₀_m.*1e9,"angular_half_width_radians"=>width,"angular_convention"=>"2pi*r/N, r=0,...,N-1; sector |wrapped phi| <= angular_half_width_radians; weight is fraction of sample cell inside sector (half at aligned boundaries; the N=64 FORWARD sector is the whole cell around zero)", "method"=>"Two selected coordinate nodes; covariance restricted to 2x2, Schur-multiplied by PSD matrices I/2 and ones/2. Weighted Frobenius over all ordered radial pairs with product w_k[i]*w_k[j]. Sector and rest are absolute angular contributions. Per-pair error uses the full-reference norm. A 2048-vs-4096 difference is an empirical uncertainty estimate, not a rigorous bound. Minimum 0 means unresolved or none passes. No retained-Q fields, energy dependence, signed collision balance, or transport gate; not DAG154 admission or global Q30 norm.","reference"=>"4096 uniform periodic angles; empirical uncertainty is 2048 versus 4096", "peak"=>Dict("pair_1based"=>collect(peakpair),"q_forward"=>peak[3],"integrand_at_zero"=>peak[1],"full_average"=>peak[2],"zero_over_average"=>peakratio),"results"=>results,"device_sha256"=>bytes2hex(sha256(read(DEVICE))),"script_sha256"=>bytes2hex(sha256(read(@__FILE__))))
    open(args[4],"w") do io; TOML.print(io,out;sorted=true); end
end
if abspath(PROGRAM_FILE) == @__FILE__
    main(ARGS)
end
