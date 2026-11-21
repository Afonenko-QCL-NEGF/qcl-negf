module V843LinkedInput

using HDF5
using LinearAlgebra
using QCLNEGF
using SHA
using TOML
using Unitful

include(joinpath(@__DIR__,"dupont_device.jl"))
include(joinpath(@__DIR__,"v843_tail_vertices.jl"))
include(joinpath(@__DIR__,"../method/pinned/conservative_shifts.jl"))

const NUM = QCLNEGF.QCLNumerics
const REF = QCLNEGF.QCLReferenceOperators
const ROOT = @__DIR__
const V843_GEOMETRY = joinpath(ROOT,"tail-geometry.h5")

complex_field(group, key) = complex.(read(group[key*"_real"]),read(group[key*"_imag"]))
sha(path) = bytes2hex(open(sha256,path))

function new_input(field; NE=121, Nk=5, geometry_file=V843_GEOMETRY)
    field in (21.0,12.5) || throw(ArgumentError("Linked geometry is frozen at two fields"))
    Nk in (5,9) || throw(ArgumentError("Use one of the two registered radial axes"))
    group = field == 21.0 ? "field_75.936" : "field_45.2"
    geometry = h5open(geometry_file,"r") do file
        g = file[group]
        return (
            W=complex_field(g,"modes"), Q=complex_field(g,"local_span"),
            S=complex_field(g,"model_overlap"), expected_metric=complex_field(g,"local_spectral_target"),
            Hamiltonian=complex_field(g,"projected_H0"), transverse=complex_field(g,"projected_transverse_H"),
            offsets=Int.(read(g["period_offsets"])), drop=only(read(g["field_drop_solver_units"])),
            x=read(g["z_dimensionless"]), wx=read(g["weight_z"]), donor=read(g["donor_dimensionless"]),
        )
    end
    scales = ScaleSystem()
    device = DupontDevice.physical_inputs(field)
    p = device.physical
    n = NumericalParameters(
        N_z=length(geometry.x),N_b=size(geometry.Q,2),P_basis=4,
        E_min=-0.65u"eV",E_max=1.0u"eV",N_E=NE,M_E=0.39u"eV",
        k_max=0.60u"nm^-1",N_k=Nk,N_φ=32,qz_max=10.0u"nm^-1",N_qz=161,η_seed=0.5u"meV",
    )
    grids = build_grids(p,n,scales)
    profiles = DupontDevice.sheet_profiles(p,n,scales,grids,device.donor_center)
    @assert isapprox(geometry.x,grids.x;rtol=1e-13)
    @assert isapprox(geometry.wx,grids.wˣ;rtol=1e-13)
    @assert isapprox(geometry.donor,profiles.Nᴰ;rtol=1e-13)
    @assert isapprox(geometry.drop,NUM._scaled_physics(p,scales).Eᵖ;rtol=1e-13)
    @assert isapprox(geometry.S,geometry.W'*geometry.W;rtol=1e-12)
    cov = V843TailVertices.assemble(p,profiles,grids,scales,device.ifr)
    Δω = scaled_value(p.ħωᴸᴼ,scales,:energy)
    phonon_shifts = campaign_conservative_shift_pair(grids.ε,grids.wᴱ,Δω)
    m = profiles.mᶻᵣ
    factor = REF._C̄(scales)/only(unique(grids.wˣ))^2
    hops = -2factor ./ (m[1:end-1]+m[2:end])
    seam = -2factor / (m[1]+m[end])
    physical_hop = [seam;hops;seam]
    h = [geometry.Hamiltonian+κ^2*geometry.transverse for κ in grids.κ]
    data = (;
        geometry,grids,profiles,scales,physical=p,phonon_shifts,cov,
        nominal_chain_H_by_k=h,physical_hop,block_width=size(geometry.W,2)÷length(geometry.offsets),
        hdf_geometry_sha256=sha(geometry_file), source_device_sha256=sha(DupontDevice.DEFAULT_DEVICE),
    )
    return data
end

end
