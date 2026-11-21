using LinearAlgebra

BLAS.set_num_threads(1)

# meV nm², from CODATA ℏ²/(2m₀).
const K0 = 38.09982116
const LAYERS = [4.30, 8.90, 2.46, 8.15, 4.10, 16.00]
const PERIOD = sum(LAYERS)
const RANGES = (
    [(-16.0, 0.0)],
    [(4.30, 13.20), (15.66, 23.81)],
    [(27.91, PERIOD)],
)

function hamiltonian(z, spacing, ranges, offset, mw, mb, gradient, potential)
    in_well = [any(lo <= pos < hi for (lo, hi) in ranges) for pos in z]
    mass = ifelse.(in_well, mw, mb)
    edge = ifelse.(in_well, 0.0, offset) .- gradient .* z .+ potential
    links = (2K0 / spacing^2) ./ (mass[1:end-1] + mass[2:end])
    diag = edge + vcat(0.0, links) + vcat(links, 0.0)
    diag[1] += 2K0 / (mass[1] * spacing^2)
    diag[end] += 2K0 / (mass[end] * spacing^2)
    return SymTridiagonal(diag, -links), edge
end

function orthogonalize(states)
    overlap = eigen(Symmetric(states' * states))
    inverse_sqrt = overlap.vectors * Diagonal(1 ./ sqrt.(overlap.values)) * overlap.vectors'
    return states * inverse_sqrt
end

function overlap_projection(full_h, states)
    orthonormal = orthogonalize(states)
    return Symmetric(orthonormal' * (full_h * orthonormal))
end

function flux_coupling(z, spacing, left_state, right_state, mb, cut)
    idx = searchsortedlast(z, cut)
    # Discrete Wronskian at the link that straddles the cut. Eigenvectors have
    # Euclidean norm one, so each carries a factor sqrt(spacing).
    wronskian = left_state[idx] * right_state[idx + 1] -
               left_state[idx + 1] * right_state[idx]
    return abs(K0 / (mb * spacing^2) * wronskian)
end

function paired_levels(full_h, states)
    solved = eigen(full_h, 1:6)
    pair_weights = vec(sum(abs2, orthogonalize(states)' * solved.vectors; dims=1))
    idx = sort(sortperm(pair_weights; rev=true)[1:2])
    return solved.values[idx], minimum(pair_weights[idx]), idx
end

function solve(;
    field=12.2, cbo=149.0, mw=0.067, mb=0.07945, scale=1.0,
    step=0.01, padding=18.0, hartree=(_ -> 0.0),
)
    spacing = step * scale
    left = (-16.0 - padding) * scale
    right = (PERIOD + padding) * scale
    n = round(Int, (right - left) / spacing)
    z = [left + (i - 0.5) * spacing for i in 1:n]
    ranges = [map(x -> scale .* x, group) for group in RANGES]
    potential = hartree.(z)
    gradient = field / 10
    operators = [
        hamiltonian(z, spacing, group, cbo, mw, mb, gradient, potential)[1]
        for group in ranges
    ]
    modes = [eigen(h, 1:2) for h in operators]
    g, l, u, e = modes[1].values[1], modes[2].values..., modes[3].values[2]
    states = hcat(modes[1].vectors[:, 1], modes[2].vectors, modes[3].vectors[:, 2])
    full_h, edge = hamiltonian(z, spacing, vcat(ranges...), cbo, mw, mb, gradient, potential)
    full_projected = overlap_projection(full_h, states)
    injection_h = hamiltonian(z, spacing, vcat(ranges[1:2]...), cbo, mw, mb, gradient, potential)[1]
    extraction_h = hamiltonian(z, spacing, vcat(ranges[2:3]...), cbo, mw, mb, gradient, potential)[1]
    injection_states = states[:, [1, 3]]
    extraction_states = states[:, [2, 4]]
    injection_h2 = overlap_projection(injection_h, injection_states)
    extraction_h2 = overlap_projection(extraction_h, extraction_states)
    injection_levels, inj_weight, i_idx = paired_levels(injection_h, injection_states)
    extraction_levels, ext_weight, e_idx = paired_levels(extraction_h, extraction_states)
    gu = abs(full_projected[1, 3])
    le = abs(full_projected[2, 4])
    zu_l = abs(dot(states[:, 3], z .* states[:, 2]))
    oscillator = mw * (u-l) * zu_l^2 / K0
    gu_flux = [flux_coupling(z, spacing, states[:, 1], states[:, 3], mb, x * scale)
               for x in (0.43, 2.15, 3.87)]
    le_flux = [flux_coupling(z, spacing, states[:, 2], states[:, 4], mb, x * scale)
               for x in (24.22, 25.86, 27.50)]
    inj_pair_gap = injection_levels[2] - injection_levels[1]
    ext_pair_gap = extraction_levels[2] - extraction_levels[1]
    measures = (;
        field, cbo, mw, mb, scale, step, padding, g, l, u, e, doublet=u-l,
        omega_gu=gu, omega_le=le, two_gu=2gu, two_le=2le, oscillator, zu_l,
        detuning_gu=g-u, detuning_le=l-e,
        lowdin_gu_pair=abs(injection_h2[1, 2]), lowdin_le_pair=abs(extraction_h2[1, 2]),
        lowdin_detuning_gu=full_projected[1, 1]-full_projected[3, 3],
        lowdin_detuning_le=full_projected[2, 2]-full_projected[4, 4],
        flux_gu=gu_flux[2], flux_le=le_flux[2],
        flux_gu_range=maximum(gu_flux)-minimum(gu_flux),
        flux_le_range=maximum(le_flux)-minimum(le_flux),
        inj_pair_gap, ext_pair_gap, inj_weight, ext_weight,
        inj_first_index=i_idx[1], ext_first_index=e_idx[1],
        phonon_gap=modes[3].values[2]-modes[3].values[1],
        g_next=modes[3].values[1],
    )
    return measures, (z, edge, hcat(states, modes[3].vectors[:, 1]), full_projected)
end

# Frozen electrostatic sensitivity, with energies in meV and lengths in nm.
function donor_hartree(electron_slabs)
    period = PERIOD
    e = 1.602176634e-19
    eps0 = 8.8541878188e-12
    amplitude = e * 3e14 / (12.9 * eps0) * 1e-6 # electron energy gradient, meV/nm
    ks = 2pi .* (1:100) ./ period
    function slab_modes(center, width)
        return sinc.((1:100) .* width ./ period) .* cis.(-ks .* center)
    end
    donor = slab_modes(35.91, 5.0)
    electron = sum(weight .* slab_modes(center, width) for (weight, center, width) in electron_slabs)
    voltage_modes = -2amplitude .* (donor - electron) ./ (period .* ks.^2)
    return z -> sum(real, voltage_modes .* cis.(ks .* z))
end

function print_csv(io, cases)
    header = true
    for (name, options) in cases
        info, _ = solve(; options...)
        if header
            println(io, join(("case", keys(info)...), ','))
            header = false
        end
        println(io, join((name, values(info)...), ','))
    end
end

function main()
    cases = [
        ("base", (;)),
        ("unaligned-dz-0.020", (; step=0.02)),
        ("dz-0.005", (; step=0.005)),
        ("dz-0.0025", (; step=0.0025)),
        ("padding-12", (; padding=12.0)),
        ("padding-28", (; padding=28.0)),
        ("cbo-130", (; cbo=130.0)),
        ("cbo-140", (; cbo=140.0)),
        ("cbo-160", (; cbo=160.0)),
        ("mb-0.075", (; mb=0.075)),
        ("mb-0.067", (; mb=0.067)),
        ("scale-0.995", (; scale=0.995)),
        ("scale-1.005", (; scale=1.005)),
        ("field-12.15", (; field=12.15)),
        ("field-12.25", (; field=12.25)),
        ("54mV-per-period", (; field=540 / PERIOD)),
    ]
    open("sensitivity.csv", "w") do io
        print_csv(io, cases)
    end
    open("field-scan.csv", "w") do io
        print_csv(io, [("field-$(f)", (; field=f)) for f in 10.8:0.02:13.7])
    end
    info, data = solve(step=0.005)
    z, edge, states, lowdin_h = data
    open("profiles.csv", "w") do io
        println(io, "z_nm,Ec_meV,g_nm^-1,l_nm^-1,u_nm^-1,e_nm^-1,gprime_nm^-1")
        for index in 1:10:length(z)
            println(io, join((z[index], edge[index], (states[index, :] .^ 2 ./ info.step)...), ','))
        end
    end
    open("projected-H.csv", "w") do io
        println(io, "g,l,u,e")
        for row in eachrow(lowdin_h)
            println(io, join(row, ','))
        end
    end
    phonon_density = donor_hartree([(1.0,35.91,16.0)])
    laser_density = donor_hartree([(8.90/17.05,8.75,8.90), (8.15/17.05,19.735,8.15)])
    open("additional-sensitivity.csv", "w") do io
        print_csv(io, [
            ("cbo-120-nextnano-only", (; cbo=120.0)),
            ("cbo-135-flores-albo-only", (; cbo=135.0)),
            ("frozen-H-phonon", (; hartree=phonon_density)),
            ("frozen-H-laser-double-well", (; hartree=laser_density)),
        ])
    end
    for (name, hartree) in (("phonon", phonon_density), ("laser", laser_density))
        vs = hartree.(0.0:0.01:PERIOD)
        println("Frozen Hartree peak-to-peak ", name, " ", maximum(vs)-minimum(vs), " meV")
    end
    println("Julia ", VERSION, " threads ", Threads.nthreads(), " BLAS ", BLAS.get_num_threads())
    println(info)
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
