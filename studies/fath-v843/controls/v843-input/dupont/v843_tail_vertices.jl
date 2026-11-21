module V843TailVertices

using LinearAlgebra
using QCLNEGF
using Unitful

const NUM = QCLNEGF.QCLNumerics
const DOMAIN = QCLNEGF.QCLDomain
const REF = QCLNEGF.QCLReferenceOperators

"""Return the V843 coordinate form factors before radial weighting.

The covariance axes are z, z′, incoming radial ring, outgoing radial ring.
The independent-interface vectors use the right-side value at the period seam
and the same interior interpolation as Core.
"""
function assemble(physical, profiles, grids, scales, correlation)
    e = 1.602176634e-19
    ε0 = 8.8541878128e-12
    kB = 1.380649e-23
    L0 = scales.L₀_m
    E0 = scales.E₀_J
    x = grids.x
    dx = only(unique(grids.wˣ))
    Nz = length(x)
    Nk = length(grids.κ)
    mechanism_scale = E0^2*L0^3*dx

    kBT = kB * ustrip(u"K",physical.Tᴸ)
    Ξ = ustrip(u"J",uconvert(u"J",physical.Ξ))
    ρ = ustrip(u"kg/m^3",physical.ρ_m)
    sound = ustrip(u"m/s",physical.v_s)
    acoustic = fill(Ξ^2*kBT/(ρ*sound^2*mechanism_scale),Nz)

    ΔV = ustrip(u"J",uconvert(u"J",physical.ΔV_alloy))
    Ω = ustrip(u"m^3",physical.Ω₀)
    alloy = Ω*ΔV^2/mechanism_scale .* profiles.x_Al .* (1 .- profiles.x_Al)

    interfaces = zeros(Float64,length(physical.interfaces),Nz)
    for (j,interface) in pairs(physical.interfaces)
        z = scaled_value(interface,scales,:length)
        if iszero(z)
            interfaces[j,1] = 1.0
        else
            right = searchsortedfirst(x,z)
            if 1 < right <= length(x)
                a = (z-x[right-1]) / (x[right]-x[right-1])
                interfaces[j,right-1] = 1-a
                interfaces[j,right] = a
            else
                throw(ArgumentError("Interface outside cell interpolation support"))
            end
        end
    end
    barrier_jump = abs(ustrip(u"J",NUM._band_jump(physical,first(physical.interfaces))))
    all(isapprox.(abs.(ustrip.(u"J",NUM._band_jump.(Ref(physical),physical.interfaces))),
        barrier_jump;rtol=1e-12)) || error("V843 vertex assumes eight equal-magnitude jumps")
    r = scaled_value(physical.Δᴵᶠᴿ,scales,:length)
    λ = scaled_value(physical.Λᴵᶠᴿ,scales,:length)
    roughness_strength = π*(r*λ*barrier_jump/(E0*dx))^2

    phonon_j = ustrip(u"J",uconvert(u"J",physical.ħωᴸᴼ))
    lo_prefactor = e^2*phonon_j/(2ε0)*(1/physical.ε_∞ - 1/physical.ε_s)
    qlo2 = scaled_value(physical.qᴸᴼ_s,scales,:wavenumber)^2
    qz_prefactors = grids.wᑫᶻ .* (lo_prefactor/(2π*E0^2*L0))
    phases = cis.(x * transpose(grids.qᶻ))

    donor = grids.wˣ .* profiles.Nᴰ ./ L0^2
    active = findall(>(0),donor)
    length(active) in (1,2) || throw(ArgumentError("Expected centre delta sheet"))
    distances = abs.(x .- transpose(x[active]))
    impurity_prefactor = e^2/(2ε0*physical.ε_s*E0)
    qs = scaled_value(physical.q_s,scales,:wavenumber)

    ifr_pair = zeros(Float64,Nk,Nk)
    lo = zeros(ComplexF64,Nz,Nz,Nk,Nk)
    impurity = zeros(Float64,Nz,Nz,Nk,Nk)
    angular = cos.(grids.φ)
    nφ = length(angular)
    qz2 = grids.qᶻ.^2
    for (kout,k) in pairs(grids.κ), (kin,kp) in pairs(grids.κ)
        q2 = max.(0.0,k^2 + kp^2 .- 2k*kp .* angular)
        angular_shape = if correlation === :exponential
            2 .* (1 .+ λ^2 .* q2).^(-1.5)
        elseif correlation === :gaussian
            exp.(-λ^2/4 .* q2)
        else
            throw(ArgumentError("Unknown interface spectrum"))
        end
        ifr_pair[kin,kout] = roughness_strength * sum(angular_shape) / nφ
        lo_weight = vec(sum(1 ./ (qz2 .+ qlo2 .+ transpose(q2));dims=2)) .* (qz_prefactors / nφ)
        @views lo[:,:,kin,kout] .= (phases .* transpose(lo_weight)) * phases'
        impurity_matrix = @view impurity[:,:,kin,kout]
        for q in sqrt.(q2)
            scale = impurity_prefactor/(q+qs)/sqrt(nφ)
            factors = exp.(-q .* distances) .* transpose(scale .* sqrt.(donor[active]))
            mul!(impurity_matrix,factors,transpose(factors),1.0,1.0)
        end
    end
    bose = inv(expm1(phonon_j/(kB*ustrip(u"K",physical.Tᴸᴼ))))
    return (;weights_k=grids.wᵏ,acoustic,alloy,interfaces,ifr_pair,lo,impurity,bose)
end

end
