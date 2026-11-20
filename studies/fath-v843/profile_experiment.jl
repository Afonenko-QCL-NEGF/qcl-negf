using LinearAlgebra
using SHA
using QCLNEGFRunner
import QCLNEGF.LinkedTransport as LT

include("spatial_balance.jl")
using .SpatialBalance

const Runner = QCLNEGFRunner

function independent_energy_rule(p, total, anchor, ring)
    layout = LT.CausalGeometry(p.en, LT.tapered_support(p.en),
        Matrix(anchor), p.geo.voltage, maximum(abs, p.geo.offsets))
    source = LT.CausalRing(layout, LT.unpack_ring(total, p.r))
    h = @view p.h[:, :, ring]
    poles = LT.scan_poles(source, p.geo, h; subdivisions=3)
    return LT.resonance_rule(source, poles, 20)
end

function rotated_modes(p)
    dimensions = size(p.h, 1)
    unitary = Matrix{ComplexF64}(I, dimensions, dimensions)
    angle = π/7
    phase = cis(π/5)
    for block in p.geo.block_ranges
        length(block) >= 2 || continue
        a, b = first(block), first(block)+1
        unitary[[a,b], [a,b]] .= [cos(angle) sin(angle)*phase;
                                 -sin(angle)*conj(phase) cos(angle)]
    end
    rotated_h = similar(p.h)
    for k in 1:p.nk
        rotated_h[:, :, k] .= unitary' * p.h[:, :, k] * unitary
    end
    return LT.LinkedProblem(p.en, p.we, p.wk, p.geo.modes*unitary, p.nb,
        p.geo.offsets, p.geo.voltage, p.geo.reach, rotated_h, p.hops, p.const_by_channel,
        p.v; spin_degeneracy=p.spin_degeneracy, current_scale=p.current_scale,
        density_scale=p.density_scale, target_dimless=p.target_dimless)
end

function run_experiment(directory, workers, check_rotated)
    saved = Runner._read_linked_checkpoint(directory)
    p = saved.problem
    k = Runner._read_linked_array(directory, "k", Float64, p.nk)
    first(k) == 0 || throw(ArgumentError("transverse-energy reference requires k=0"))
    radial_grid_sha256 = bytes2hex(sha256(reinterpret(UInt8, k)))
    cuts = saved.current_midpoints
    widths = (cuts[3:end] .- cuts[1:end-2])./2
    fresh = LT.linked_fresh_map(p, saved.seed;
        projector=LT.project_linked_economical, order=18, subdivisions=2,
        selected_rows=true, projection_for_collision=false, workers)
    println(stderr, "fresh linked map complete")
    nodal = spatial_balance(p, fresh.source, widths; workers)
    projected = fresh.summary["projected_fresh"]
    archived_nodal = fresh.summary["fresh"]["raw_profile_A_cm2"]
    maxdiff(a,b) = maximum(abs.(a .- b))
    nodal_agreement = maxdiff(archived_nodal, nodal.current_A_cm2)
    nodal_agreement <= max(1e-8, 1e-10maximum(abs, archived_nodal)) ||
        error("independent nodal profile differs from the solver observation")
    resolved = spatial_balance(p, fresh.source, widths; workers, energy_rule=independent_energy_rule)
    println(stderr, "independent resolved profile complete")
    lagged = spatial_balance(p, saved.seed, widths;
        collision_sources=fresh.source, workers, energy_rule=independent_energy_rule)
    println(stderr, "lagged balance complete")
    unitary = if check_rotated
        rotated = spatial_balance(rotated_modes(p), fresh.source, widths; workers)
        (; profile_A_cm2=maxdiff(nodal.current_A_cm2,rotated.current_A_cm2),
           channel_max_A_cm2=Dict(name=>maxdiff(curve, rotated.collision_cumulative_A_cm2[name])
               for (name,curve) in nodal.collision_cumulative_A_cm2),
           raw_charge_cm2=abs(nodal.raw_sheet_cm2-rotated.raw_sheet_cm2),
           central_band_population_max=maxdiff(nodal.central_bands.fraction,rotated.central_bands.fraction),
           equivalent_temperature_K=abs(nodal.equivalent_temperature_K-rotated.equivalent_temperature_K))
    else
        nothing
    end
    voltage_V = 0.1p.geo.voltage
    field_power_W_m2 = resolved.current.mean_internal_A_cm2 * voltage_V * 1e4
    return (;
        schema="qcl-negf-linked-spatial-balance/v1",
        identity=saved.identity,
        provenance=(;core=Runner._linked_package_identity(Runner.QCLNEGF),
            runner=Runner._linked_package_identity(Runner),
            runtime=Runner._runtime_toolchain_provenance(),
            source_sha256=Dict(basename(path)=>bytes2hex(open(sha256,path))
                for path in (@__FILE__,joinpath(@__DIR__,"spatial_balance.jl"))),
            radial_grid_sha256),
        current_midpoints_nm=cuts,
        radial_grid_dimensionless=k,
        configuration=(;workers, mode_count=size(p.h,1), reach=p.geo.reach, voltage_V,
            reference_projection="GL9/13/18 by pole distance, selected rows, subdivisions=2",
            independent_projection="GL20, full solve, subdivisions=3",
            collision_measure="normalized nodal",
            spin=p.spin_degeneracy),
        measured=(;nodal, resolved, lagged, unitary, field_power_W_m2,
            nodal_agreement_A_cm2=nodal_agreement,
            independent_vs_production_A_cm2=maxdiff(resolved.current_A_cm2,projected["raw_profile_A_cm2"])),
        reference=fresh.summary,
        stationary=false,
    )
end

if abspath(PROGRAM_FILE)==abspath(@__FILE__)
    length(ARGS) in (3,4) || error("Usage: profile_experiment.jl ARCHIVE OUTPUT WORKERS [compare-unitary]")
    input, output, worker_argument = ARGS[1:3]
    isfile(output) && error("output already exists: $output")
    check_rotated = length(ARGS)==4 && ARGS[4]=="compare-unitary"
    length(ARGS)==4 && !check_rotated && error("unknown argument $(ARGS[4])")
    BLAS.set_num_threads(1)
    result = run_experiment(input,parse(Int,worker_argument),check_rotated)
    open(output, "w") do io
        Runner._light_json(io, result)
        println(io)
    end
end
