#!/usr/bin/env julia
# Independent uniform cell-centred BDD assembly. This is not a Core API test.
using LinearAlgebra
using TOML
using SHA

const HBAR2_2M0_eV_nm2 = 0.0380998211615486
const DEVICE = normpath(joinpath(@__DIR__, "..", "fath-v843", "controls", "v843-input", "dupont", "device.toml"))

"""Assemble a full N-cell ring explicitly, including the twisted seam."""
function ring_matrix(v, mass, dz, nperiod, phase)
    nz = length(v)
    n = nperiod * nz
    h = zeros(ComplexF64, n, n)
    for a in 1:n
        i = mod1(a, nz)
        h[a, a] += v[i]
        b = mod1(a + 1, n)
        j = mod1(a + 1, nz)
        t = HBAR2_2M0_eV_nm2 * (2 / (mass[i] + mass[j])) / dz^2
        h[a, a] += t
        h[b, b] += t
        seam = a == n ? cis(phase) : 1.0 + 0im
        h[a, b] -= t * seam
        h[b, a] -= t * conj(seam)
    end
    Hermitian(h)
end

"""Independently assemble the primitive cell with Bloch boundary phase theta."""
function primitive_matrix(v, mass, dz, theta)
    nz = length(v)
    h = zeros(ComplexF64, nz, nz)
    for i in 1:nz
        left = mod1(i - 1, nz)
        right = mod1(i + 1, nz)
        tl = HBAR2_2M0_eV_nm2 * (2 / (mass[left] + mass[i])) / dz^2
        tr = HBAR2_2M0_eV_nm2 * (2 / (mass[i] + mass[right])) / dz^2
        h[i, i] = v[i] + tl + tr
        h[i, right] = -tr * (i == nz ? cis(theta) : 1.0)
        h[i, left] = -tl * (i == 1 ? cis(-theta) : 1.0)
    end
    Hermitian(h)
end

function spectra(v, mass, dz, nperiod, phase)
    ring = eigvals(ring_matrix(v, mass, dz, nperiod, phase))
    phases = [(phase + 2pi*m) / nperiod for m in 0:nperiod-1]
    primitive = sort!(reduce(vcat, [eigvals(primitive_matrix(v, mass, dz, t)) for t in phases]))
    return ring, primitive, phases
end

function main(args)
    length(args) == 3 || error("Usage: julia floquet.jl N_PERIODS NZ OUTPUT.toml")
    nperiod, nz = parse.(Int, args[1:2])
    nperiod in (7, 9, 11) || error("N_PERIODS must be 7, 9 or 11")
    nz in (144, 288) || error("NZ must be 144 or 288")
    # Tiny uniform fixture checks dispersion and boundary phases, not V843.
    fixture_v, fixture_m, fixture_nz, fixture_n = fill(0.1, 4), fill(0.067, 4), 4, 3
    fixture_dz = 0.5
    fixture_t = HBAR2_2M0_eV_nm2 / (fixture_m[1] * fixture_dz^2)
    for phi in (0.0, pi)
        observed, primitive, _ = spectra(fixture_v, fixture_m, fixture_dz, fixture_n, phi)
        exact = sort!([0.1 + 2fixture_t * (1 - cos((phi + 2pi*m) / (fixture_n * fixture_nz))) for m in 0:fixture_n*fixture_nz-1])
        maximum(abs.(observed .- exact)) < 1e-10 || error("Uniform ring fixture failed")
        maximum(abs.(observed .- primitive)) < 1e-10 || error("Bloch fixture failed")
    end

    d = TOML.parsefile(DEVICE)
    widths = Float64.(d["layer_thickness_nm"])
    length(widths) == 8 || error("Expected eight V843 layers")
    period = Float64(d["period_nm"])
    edges = cumsum([0.0; widths])
    isapprox(edges[end], period; rtol=1e-14) || error("Layer widths do not sum to period")
    dz = period / nz
    # Same cell-centred material sampling for both representations.
    layer = [min(searchsortedlast(edges, (i-0.5)*dz), 8) for i in 1:nz]
    v = [isodd(i) ? Float64(d["barrier_offset_meV"])/1000 : 0.0 for i in layer]
    mass = [Float64(d[isodd(i) ? "barrier_mass_over_me" : "well_mass_over_me"]) for i in layer]
    out = Dict{String, Any}(
        "schema" => "v843-independent-bdd-floquet/1", "n_periods" => nperiod,
        "nodes_per_period" => nz, "period_nm" => period, "dz_nm" => dz,
        "device_sha256" => bytes2hex(sha256(read(DEVICE))),
        "script_sha256" => bytes2hex(sha256(read(@__FILE__))),
        "description" => "Independent cell-centred BDD, zero field, fixed equal dz weights. Not Core assembly or a transport validation.",
        "hbar2_over_2m0_eV_nm2" => HBAR2_2M0_eV_nm2,
        "interface_link" => "2/(m_left+m_right), matching Core face_inverse_mass",
        "layer_node_counts" => [count(==(i), layer) for i in 1:8],
        "boundary_phase_results" => Dict{String,Any}())
    for (name, phi) in (("periodic", 0.0), ("antiperiodic", pi))
        a, b, phases = spectra(v, mass, dz, nperiod, phi)
        delta = abs.(a .- b)
        out["boundary_phase_results"][name] = Dict(
            "phase_radians" => Float64(phi), "bloch_phases_radians" => phases,
            "count" => length(a), "max_abs_difference_meV" => 1000maximum(delta),
            "rms_difference_meV" => 1000sqrt(sum(abs2, delta)/length(delta)),
            "ring_spectrum_eV" => a, "primitive_union_spectrum_eV" => b)
    end
    open(args[3], "w") do io
        TOML.print(io, out; sorted=true)
    end
end

if abspath(PROGRAM_FILE) == abspath(@__FILE__)
    main(ARGS)
end
