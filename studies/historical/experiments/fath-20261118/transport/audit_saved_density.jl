# Bounded memory post-processing of a native terminal state, with no SCBA or kernel build.
using HDF5, LinearAlgebra, SHA, TOML

boundary_profiles="--boundary-profiles" in ARGS
inputs=filter(!=("--boundary-profiles"),ARGS)
length(inputs) in (1,3) || error("Supply attempt alone, or attempt and Julia E,k witness indices")
attempt=abspath(inputs[1])
witness_indices=length(inputs)==3 ? (parse(Int,inputs[2]),parse(Int,inputs[3])) : nothing
summary=TOML.parsefile(joinpath(attempt,"summary.toml"))
case_root=haskey(summary,"source_case") ? dirname(attempt) : attempt
haskey(summary,"source_case") && basename(case_root)!=summary["source_case"] &&
    error("Checkpoint parent case differs from its recorded identity")
model=joinpath(case_root,"model.h5")
state=joinpath(attempt,"state.h5")
sha(path)=bytes2hex(open(sha256,path))
sha(model)==summary["model_sha256"] || error("Model SHA mismatch")
sha(state)==summary["state_sha256"] || error("State SHA mismatch")
BLAS.set_num_threads(1)
energy,tE,kaxis,tk,trusted,phi,center_x,center_w,mass= h5open(model,"r") do f
    read(f["schema"])=="fath-cbo149-model-v1" || error("Unexpected model schema")
    (read(f["energy_dimensionless"]),read(f["weight_energy"]),read(f["k_dimensionless"]),
     read(f["weight_k"]),isone.(read(f["trusted_energy"])),
     complex.(read(f["Phi_real"]),read(f["Phi_imag"])),
     read(f["position_dimensionless"]),read(f["weight_position"]),read(f["mass_axial"]))
end
Ne,Nk,Nb=length(energy),length(kaxis),size(phi,2)
Device=TOML.parsefile(joinpath(case_root,"device.toml"))
config=TOML.parsefile(joinpath(case_root,"input.toml"))
spin=Device["spin_degeneracy"]
L0=1e-8; E0=0.10
energy_meV=(1000*E0).*energy
isapprox(first(energy_meV),config["E_min_meV"]; rtol=1e-14) &&
    isapprox(last(energy_meV),config["E_max_meV"]; rtol=1e-14) ||
    error("Resolved energy units differ from the frozen input")
charge,hbar,me=1.602176634e-19,1.054571817e-34,9.1093837139e-31
current_unit=charge^2*E0/(hbar*L0^2)
Hopping=-2*hbar^2/(2me*E0*charge*L0^2)./(mass[1:end-1].+mass[2:end])./center_w[1]^2
P=zeros(ComplexF64,Nb,Nb)
per_k_spectral_residual=zeros(Nk)
matrix_sum_spectra=zeros(Nb,Nk)
spectral_energy=zeros(Ne)
occupied_energy=zeros(Ne)
occupied_momentum=zeros(Nk)
signed_boundary_energy=zeros(2,Ne)
signed_boundary_k=zeros(2,Nk)
witness=Dict{String,Any}()
h5open(state,"r") do f
    read(f["schema"])=="fath-cbo149-aligned-state-v1" || error("Unexpected state schema")
    read(f["model_identity"])==summary["model_identity"] || error("Canonical model identity mismatch")
    g=f["green"]
    for name in ("A_real","A_imag","GL_real","GL_imag")
        size(g[name])==(Ne,Nk,Nb,Nb) || error("Wrong field shape: $name")
    end
    for k in 1:Nk
        aa=complex.(g["A_real"][:,k,:,:],g["A_imag"][:,k,:,:])
        ll=complex.(g["GL_real"][:,k,:,:],g["GL_imag"][:,k,:,:])
        integral=zeros(ComplexF64,Nb,Nb)
        for e in 1:Ne
            Aw=tE[e]/(2π)
            Lw=spin*tk[k]*Aw
            @inbounds for b in 1:Nb,a in 1:Nb
                integral[a,b]+=Aw*aa[e,a,b]
                P[a,b]+=(-im*Lw)*ll[e,a,b]
            end
            @inbounds for a in 1:Nb
                spectral_energy[e]+=tk[k]*Aw*real(aa[e,a,a])
                value=Lw*imag(ll[e,a,a])
                occupied_energy[e]+=value
                occupied_momentum[k]+=value
            end
        end
        per_k_spectral_residual[k]=norm(integral-I)/sqrt(Nb)
        matrix_sum_spectra[:,k]=eigvals(Hermitian((integral+integral')/2))
        if boundary_profiles
            gg=complex.(g["GG_real"][:,k,:,:],g["GG_imag"][:,k,:,:])
            for (side,label) in enumerate(("embedding_plus","embedding_minus"))
                boundary=f["selfenergy/"*label]
                slab(name)=complex.(boundary[name*"_real"][:,k,:,:],boundary[name*"_imag"][:,k,:,:])
                sg,sl=slab("G"),slab("L")
                prefactor=current_unit*spin*tk[k]/(2π*1e4)
                @inbounds for e in 1:Ne
                    trace=0.0
                    for b in 1:Nb,a in 1:Nb
                        trace+=real(sg[e,a,b]*ll[e,b,a]-sl[e,a,b]*gg[e,b,a])
                    end
                    flux=prefactor*tE[e]*trace
                    signed_boundary_energy[side,e]+=flux
                    signed_boundary_k[side,k]+=flux
                end
            end
        end
    end
    if witness_indices!==nothing
        e,k=witness_indices
        block(group,name)=complex.(group[name*"_real"][e,k,:,:],group[name*"_imag"][e,k,:,:])
        A=block(g,"A")
        GR=block(g,"GR")
        Γ=zeros(ComplexF64,Nb,Nb)
        channels=("LO","acoustic","impurity","IFR","alloy","embedding")
        for name in channels
            family=f["selfenergy/"*name]
            Γ .+= im.*(block(family,"G").-block(family,"L"))
        end
        witness["E_index_julia"]=e
        witness["k_index_julia"]=k
        witness["energy_meV"]=energy_meV[e]
        witness["k_nm_inverse"]=kaxis[k]/(L0*1e9)
        witness["raw_A_minimum_hermitian_eigenvalue_dimensionless"]=eigmin(Hermitian((A+A')/2))
        witness["block_frobenius_A_dimensionless"]=norm(A)
        witness["using_GR_minus_GA_absolute_error"]=norm(A-im.*(GR-GR'))
        witness["using_GRGammaGA_absolute_error"]=norm(A-GR*Γ*GR')
    end
end
fraction(values,mask)=sum(values[mask])/sum(values)
e_span=last(energy)-first(energy)
tail_e=(energy.<first(energy)+0.05e_span) .| (energy.>last(energy)-0.05e_span)
tail_k=kaxis.>0.95last(kaxis)
proj=phi*(im.*P)*phi'
J=[2current_unit*real(Hopping[i]*proj[i+1,i])/1e4 for i in eachindex(Hopping)]
isapprox(real(tr(P)),summary["last_row"]["normalized_charge"]; rtol=1e-11) ||
    error("Density quadrature and measured charge differ")
result=Dict("state_sha256"=>summary["state_sha256"],"model_sha256"=>summary["model_sha256"],
    "independent_bond_J_profile_A_cm2"=>J,
    "independent_bond_J_mean_A_cm2"=>sum(J)/length(J),
    "independent_bond_J_min_A_cm2"=>minimum(J),"independent_bond_J_max_A_cm2"=>maximum(J),
    "r_sum_max_unweighted_per_k"=>maximum(per_k_spectral_residual),
    "k_at_max_r_sum_nm_inverse"=>kaxis[argmax(per_k_spectral_residual)]/(L0*1e9),
    "full_window_spectral_residual_per_k"=>per_k_spectral_residual,
    "spectral_sum_eigenvalues_per_k"=>[collect(col) for col in eachcol(matrix_sum_spectra)],
    "spectral_sum_excess_F_over_sqrtNb_per_k"=>[
        norm(max.(col.-1,0))/sqrt(Nb) for col in eachcol(matrix_sum_spectra)],
    "spectral_sum_deficit_F_over_sqrtNb_per_k"=>[
        norm(max.(1 .-col,0))/sqrt(Nb) for col in eachcol(matrix_sum_spectra)],
    "k_nm_inverse"=>kaxis./(L0*1e9),
    "occupied_sheet_each_radial_bin_m_minus_2"=>occupied_momentum./L0^2,
    "spectral_trace_outside_trust"=>fraction(spectral_energy,.!trusted),
    "occupied_sheet_outside_trust"=>fraction(occupied_energy,.!trusted),
    "occupied_sheet_in_outer_5pct_energy_each_side"=>fraction(occupied_energy,tail_e),
    "occupied_sheet_above_95pct_kmax"=>fraction(occupied_momentum,tail_k),
    "donor_sheet_integral_fraction_from_Gless"=>real(tr(P))/L0^2/Device["sheet_donors_m_minus_2"],
    "occupied_energy_bin_integral_dimensionless"=>occupied_energy,
    "spectral_trace_bin_integral_dimensionless"=>spectral_energy,
    "energy_meV"=>energy_meV)
terminal_path=joinpath(attempt,"terminal-observables.toml")
if isfile(terminal_path)
    terminal=TOML.parsefile(terminal_path)
    oracle_error=maximum(abs.(J-terminal["bond_J_A_cm2"]))
    oracle_error<1e-8*max(1.0,maximum(abs,J)) || error("Saved current profile mismatch")
    result["independent_bond_J_max_error_A_cm2"]=oracle_error
end
if boundary_profiles
    plus_from_slabs,minus_from_slabs=vec(sum(signed_boundary_k;dims=2))
    target=summary["last_row"]["J"]/1e4
    isapprox(plus_from_slabs,target;rtol=1e-8,atol=1e-9) ||
        error("Slab-integrated plus current does not match the native row")
    if isfile(terminal_path)
        terminal=TOML.parsefile(terminal_path)
        isapprox(minus_from_slabs,terminal["J_minus_out_A_cm2"];rtol=1e-8,atol=1e-9) ||
            error("Slab-integrated minus current differs from the recorded current")
    end
    result["boundary_flux_profiles"]=Dict("side_order"=>["plus_out","minus_out"],
        "signed_integrated_A_cm2_by_k"=>[collect(row) for row in eachrow(signed_boundary_k)],
        "signed_integrated_A_cm2_by_energy"=>[collect(row) for row in eachrow(signed_boundary_energy)],
        "integrated_A_cm2"=>[plus_from_slabs,minus_from_slabs])
end
isempty(witness) || (result["terminal_spectral_witness_from_state"]=witness)
TOML.print(stdout,result;sorted=true)
