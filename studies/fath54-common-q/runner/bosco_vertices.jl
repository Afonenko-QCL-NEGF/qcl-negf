module BoscoVertices

using LinearAlgebra
using QCLNEGF
using Unitful

const NUM = QCLNEGF.QCLNumerics

"""
    assemble(physical, profiles, grids, scales, correlation; enabled)

Coordinate covariances before the radial measure, in the V843 convention.
`enabled` must be an explicit collection of symbols selected from
`:LO, :acoustic, :impurity, :IFR, :alloy`. The output is compatible with
`LinkedTransport.LocalCollisionKernels`; its LO and impurity axes are
`(z,z′,incoming k,outgoing k)` and interface rows are physical site probes.

The angular rule is Core's equally weighted periodic `grids.φ` rule and the
LO qz sum uses the actual `grids.wᑫᶻ` trapezoid weights. As in V843 this
constructor uses a uniform cell-centred position grid and equal interface
jump magnitudes; it fails closed for unsupported geometry. The Gaussian IFR
shape matches Core reference; exponential IFR is the separate V843/Fath
model and must be explicitly selected. Impurities sum over every positive
weighted donor cell, extending the V843 sheet implementation without a
change of microscopic kernel. Output contains zero arrays for disabled
channels; enabled alloy requires both physical alloy parameters.

This is a coordinate representation of the same formulas, not proof of
numerical equivalence: compare projected vertices with Core and V843 for
identical physical inputs before scientific use. No adaptive angular or qz
quadrature is silently substituted.
"""
function assemble(physical, profiles, grids, scales, correlation; enabled)
    valid = Set((:LO, :acoustic, :impurity, :IFR, :alloy))
    selected = Set(Symbol.(collect(enabled)))
    issubset(selected,valid) || throw(ArgumentError("unknown collision channel"))
    active(channel) = channel in selected
    correlation in (:gaussian,:exponential) || throw(ArgumentError("unknown interface spectrum"))
    x = grids.x
    nz, nk = length(x), length(grids.κ)
    nz > 1 && nk > 0 || throw(ArgumentError("empty coordinate or momentum grid"))
    length(grids.wˣ)==nz && length(profiles.Nᴰ)==nz && length(profiles.x_Al)==nz ||
        throw(DimensionMismatch("spatial arrays differ"))
    dx = first(grids.wˣ)
    dx > 0 && all(w -> isapprox(w,dx;rtol=1e-13,atol=0),grids.wˣ) &&
        all(isapprox.(diff(x),dx;rtol=1e-13,atol=1e-14)) ||
        throw(ArgumentError("V843 coordinate representation requires uniform cells"))
    nφ = length(grids.φ)
    nφ > 0 && all(isapprox(grids.φ[i],2π*(i-1)/nφ;rtol=1e-13,atol=1e-14) for i in 1:nφ) ||
        throw(ArgumentError("expected Core periodic uniform angular rule"))
    length(grids.qᶻ)==length(grids.wᑫᶻ) && all(>(0),grids.wᑫᶻ) ||
        throw(ArgumentError("invalid qz quadrature weights"))
    all(>=(0),profiles.Nᴰ) || throw(ArgumentError("negative donor density"))
    all(>(0),grids.wᵏ) || throw(ArgumentError("nonpositive radial weights"))

    e, ε0, kB = 1.602176634e-19, 8.8541878128e-12, 1.380649e-23
    L0, E0 = scales.L₀_m, scales.E₀_J
    mechanism_scale = E0^2*L0^3*dx
    acoustic = zeros(Float64,nz)
    alloy = zeros(Float64,nz)
    if active(:acoustic)
        Ξ = ustrip(u"J",uconvert(u"J",physical.Ξ))
        ρ = ustrip(u"kg/m^3",physical.ρ_m)
        sound = ustrip(u"m/s",physical.v_s)
        acoustic .= Ξ^2*(kB*ustrip(u"K",physical.Tᴸ))/(ρ*sound^2*mechanism_scale)
    end
    if active(:alloy)
        isnothing(physical.ΔV_alloy) && throw(ArgumentError("alloy enabled but ΔV_alloy is missing"))
        isnothing(physical.Ω₀) && throw(ArgumentError("alloy enabled but Ω₀ is missing"))
        ΔV = ustrip(u"J",uconvert(u"J",physical.ΔV_alloy))
        Ω = ustrip(u"m^3",physical.Ω₀)
        alloy .= Ω*ΔV^2/mechanism_scale .* profiles.x_Al .* (1 .- profiles.x_Al)
    end

    interfaces = zeros(Float64,length(physical.interfaces),nz)
    ifr_pair = zeros(Float64,nk,nk)
    roughness_strength = 0.0
    λ = scaled_value(physical.Λᴵᶠᴿ,scales,:length)
    if active(:IFR)
        isempty(physical.interfaces) && throw(ArgumentError("IFR enabled without interfaces"))
        for (j,interface) in pairs(physical.interfaces)
            z = scaled_value(interface,scales,:length)
            if iszero(z)
                interfaces[j,1] = 1.0
            else
                right = searchsortedfirst(x,z)
                1 < right <= nz || throw(ArgumentError("interface outside interpolation support"))
                a = (z-x[right-1])/(x[right]-x[right-1])
                interfaces[j,right-1],interfaces[j,right] = 1-a,a
            end
        end
        jumps = [abs(ustrip(u"J",NUM._band_jump(physical,z))) for z in physical.interfaces]
        all(isapprox(j,first(jumps);rtol=1e-12,atol=0) for j in jumps) ||
            throw(ArgumentError("V843 representation requires equal interface jump magnitudes"))
        r = scaled_value(physical.Δᴵᶠᴿ,scales,:length)
        roughness_strength = π*(r*λ*first(jumps)/(E0*dx))^2
    end

    lo = zeros(ComplexF64,nz,nz,nk,nk)
    impurity = zeros(Float64,nz,nz,nk,nk)
    phonon_j = ustrip(u"J",uconvert(u"J",physical.ħωᴸᴼ))
    bose = active(:LO) ? inv(expm1(phonon_j/(kB*ustrip(u"K",physical.Tᴸᴼ)))) : 0.0
    lo_prefactor = e^2*phonon_j/(2ε0)*(1/physical.ε_∞ - 1/physical.ε_s)
    qlo2 = scaled_value(physical.qᴸᴼ_s,scales,:wavenumber)^2
    qz_prefactors = grids.wᑫᶻ .* (lo_prefactor/(2π*E0^2*L0))
    phases = cis.(x * transpose(grids.qᶻ))
    donor = grids.wˣ .* profiles.Nᴰ ./ L0^2
    donor_nodes = findall(>(0),donor)
    distances = abs.(x .- transpose(x[donor_nodes]))
    impurity_prefactor = e^2/(2ε0*physical.ε_s*E0)
    qs = scaled_value(physical.q_s,scales,:wavenumber)
    angular = cos.(grids.φ)
    qz2 = grids.qᶻ.^2
    for (kout,k) in pairs(grids.κ), (kin,kp) in pairs(grids.κ)
        q2 = max.(0.0,k^2 + kp^2 .- 2k*kp .* angular)
        if active(:IFR)
            shape = correlation === :exponential ? 2 .* (1 .+ λ^2 .* q2).^(-1.5) :
                exp.(-λ^2/4 .* q2)
            ifr_pair[kin,kout] = roughness_strength * sum(shape) / nφ
        end
        if active(:LO)
            lo_weight = vec(sum(1 ./ (qz2 .+ qlo2 .+ transpose(q2));dims=2)) .* (qz_prefactors / nφ)
            @views lo[:,:,kin,kout] .= (phases .* transpose(lo_weight)) * phases'
        end
        if active(:impurity)
            impurity_matrix = @view impurity[:,:,kin,kout]
            for q in sqrt.(q2)
                scale = impurity_prefactor/(q+qs)/sqrt(nφ)
                factors = exp.(-q .* distances) .* transpose(scale .* sqrt.(donor[donor_nodes]))
                mul!(impurity_matrix,factors,transpose(factors),1.0,1.0)
            end
        end
    end
    return (;weights_k=grids.wᵏ,acoustic,alloy,interfaces,ifr_pair,lo,impurity,bose)
end

end
