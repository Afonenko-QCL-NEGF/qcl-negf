# Static coordinate-operator and diagonal LO witnesses on the same K31 geometry.
# Usage: operator_witness.jl NIGHT_REPLAY F13 F25 NIGHT_EVIDENCE OUT K31_DRIVER RING
length(ARGS)==7 || error("expected NIGHT_REPLAY F13 F25 NIGHT_EVIDENCE OUT K31_DRIVER RING")
include(ARGS[1])

function announce(event)
    T.Runner._light_json(stderr,event)
    println(stderr)
    flush(stderr)
end

const Experiment = include(ARGS[6])
BLAS.set_num_threads(1)

function current_operator_errors(p, basis)
    q = basis.rotated
    modal = basis.modal
    old_w, new_w = p.geo.modes, q.geo.modes
    peak = 0.0
    peak_absolute = 0.0
    for (i,z) in enumerate(first(p.geo.monitor):(last(p.geo.monitor)-1))
        a,b = @views old_w[z,:],old_w[z+1,:]
        c,d = @views new_w[z,:],new_w[z+1,:]
        original = conj(a) * transpose(b)
        rotated = conj(c) * transpose(d)
        delta = rotated - modal' * original * modal
        peak = max(peak,norm(delta)/max(norm(original),floatmin(Float64)))
        peak_absolute = max(peak_absolute,maximum(abs,delta) * 2maximum(abs,@view(p.hops[i,:])))
    end
    return (;sections=length(p.geo.monitor)-1,radii=p.nk,maximum_frobenius_relative=peak,
        maximum_hopping_scaled_absolute=peak_absolute)
end

function witness(ring)
    fine = T.Runner._read_linked_checkpoint(ARGS[3])
    base = Experiment.load_arm(fine.problem,"K31")
    geometry = ENV["FATH_BDD"]
    spec = T.TOML.parsefile(joinpath(ARGS[3],"spec.toml"))
    # A minimal zero packet exercises the same rank construction. The static
    # h, W, Q and LO kernels do not depend on the occupation field.
    empty_source = zeros(Float64,base.p.r^2,2,1,1,1)
    expanded = Experiment.RankControl.expand(base.p,base.k,empty_source,ARGS[3],geometry,
        spec["source_model_sha"])
    problem = expanded.problem
    sites = T.Runner._read_linked_array(ARGS[3],"ifr_sites",Float64,
        size(problem.v.interface_probes,1),problem.nz)
    basis = Experiment.rotate_problem(problem,sites)
    current = current_operator_errors(problem,basis)
    current.maximum_frobenius_relative < 2e-12 ||
        error("the physical current operator did not transform covariantly")
    device = T.TOML.parsefile(joinpath(ENV["FATH_APP"],"studies","fath-v843","fath-device.toml"))
    lo = Experiment.lo_diagonal_control(problem,sites,ring,device["LO_energy_meV"]/100)
    return (;stage="static_K31_Q25_operator",current,lo,ring_nm_inverse=base.k[ring]/10,
        source_geometry_sha256=T.file_sha(geometry),
        scientific_application=readchomp(`git -C $(ENV["FATH_APP"]) rev-parse HEAD`),
        runtime=T.Runner._runtime_toolchain_provenance())
end

destination = ARGS[5]
ispath(destination) && error("output already exists: $destination")
T.radial_write(destination,witness(parse(Int,ARGS[7])))
