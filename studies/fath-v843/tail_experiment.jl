include("profile_experiment.jl")
using HDF5
using TOML

function coordinates_from_archive(path, spec_sha, p)
    digest = bytes2hex(open(sha256,path))
    digest == spec_sha || throw(ArgumentError("coordinate model digest differs from the packed input"))
    return h5open(path,"r") do archive
        axial_mass, transverse_mass, material, position, widths =
            (read(archive[n]) for n in ("mass_axial","mass_lateral","E_conduction_dimensionless",
                "position_dimensionless","weight_position"))
        all(length(v)==p.nz for v in (axial_mass,transverse_mass,material,position,widths)) ||
            throw(DimensionMismatch("coordinate model axes differ from the packed input"))
        return (; axial_mass,transverse_mass,material,position,step=only(unique(widths)))
    end
end

function coordinate_hamiltonian(p, coordinates, radial_grid)
    (;axial_mass,transverse_mass,material,position,step) = coordinates
    cbar = (1.054571817e-34)^2/(2*9.1093837139e-31*0.1*1.602176634e-19*(1e-8)^2)
    periods = p.geo.offsets
    span = (first(periods)*p.nz):(last(periods)*p.nz+p.nz-1)
    physical_index(i) = mod(i,p.nz)+1
    at_cell = physical_index.(span)
    length_period = p.nz*step
    z = position[at_cell] .+ (length_period .* fld.(span,p.nz))
    full_faces = [-2cbar / (step^2*(axial_mass[physical_index(i)]+axial_mass[physical_index(i+1)]))
        for i in (first(span)-1):last(span)]
    diagonal = material[at_cell] .- p.geo.voltage.*z./length_period .-
        full_faces[1:end-1] .- full_faces[2:end]
    return [SymTridiagonal(diagonal .+ cbar*k^2 ./ transverse_mass[at_cell],full_faces[2:end-1])
        for k in radial_grid]
end

function shorter_tails(p, radial, model)
    full_modes = p.geo.modes
    coordinates = coordinate_hamiltonian(p,model,radial)
    verification_error = maximum(norm(full_modes' * h * full_modes - p.h[:,:,k])/
        max(norm(p.h[:,:,k]),1e-300) for (k,h) in enumerate(coordinates))
    verification_error <= 2e-12 ||
        error("coordinate BDD projection failed to reproduce the original H: $verification_error")
    frame = copy(full_modes)
    @views for block in eachindex(p.geo.block_ranges), cell in eachindex(p.geo.offsets)
        distance = abs(block-cell)
        sites = ((cell-1)*p.nz+1):(cell*p.nz)
        distance > 3 && norm(frame[sites,p.geo.block_ranges[block]])>1e-12 &&
            error("original mode tails exceed three translated periods")
        distance > 2 && fill!(frame[sites,p.geo.block_ranges[block]],0)
    end
    h = cat([frame' * part * frame for part in coordinates]...;dims=3)
    variant = LT.LinkedProblem(p.en,p.we,p.wk,frame,p.nb,p.geo.offsets,p.geo.voltage,5,
        h,p.hops,p.const_by_channel,p.v;spin_degeneracy=p.spin_degeneracy,current_scale=p.current_scale,
        density_scale=p.density_scale,target_dimless=p.target_dimless)
    return (;variant, verification_error, removed_mode_norm=norm(full_modes-frame)/norm(full_modes))
end

function paired_tail_rule(full, short, total, anchor, ring)
    layout = LT.CausalGeometry(full.en,LT.tapered_support(full.en),
        Matrix(anchor),full.geo.voltage,maximum(abs,full.geo.offsets))
    kernel = LT.CausalRing(layout,LT.unpack_ring(total,full.r))
    a = LT.scan_poles(kernel,full.geo,@view(full.h[:,:,ring]);subdivisions=3)
    b = LT.scan_poles(kernel,short.geo,@view(short.h[:,:,ring]);subdivisions=3)
    grid = sort!(unique([a.points;b.points]))
    poles = sort!(unique([a.poles;b.poles]);by=x->x.energy)
    return LT.resonance_rule(kernel,(points=grid,poles=poles),20)
end

function frozen_fresh_source(directory,saved,expected_digest)
    summary = TOML.parsefile(joinpath(directory,"summary.toml"))
    summary["input_spec_sha256"]==saved.identity["input_spec_sha256"] ||
        error("frozen output refers to a different seed or device")
    source = Runner._read_linked_array(directory,"fresh_source_LG_packed",Float64,size(saved.seed)...)
    bytes2hex(sha256(reinterpret(UInt8,vec(source))))==expected_digest ||
        error("frozen fresh source differs from the accepted archived reference")
    return source
end

function compare_tails(directory,path,reference,digest,workers)
    saved=Runner._read_linked_checkpoint(directory)
    p=saved.problem
    radial=Runner._read_linked_array(directory,"k",Float64,p.nk)
    model=coordinates_from_archive(path,saved.identity["source_geometry_model_sha256"],p)
    restricted=shorter_tails(p,radial,model)
    source=frozen_fresh_source(reference,saved,digest)
    cuts=saved.current_midpoints
    widths=(cuts[3:end] .- cuts[1:end-2])./2
    rule=(_,total,anchor,ring)->paired_tail_rule(p,restricted.variant,total,anchor,ring)
    full=spatial_balance(p,source,widths;workers,energy_rule=rule,current_cuts=cuts)
    short=spatial_balance(restricted.variant,source,widths;workers,energy_rule=rule,current_cuts=cuts)
    return (;
        schema="qcl-negf-linked-tail-comparison/v1",identity=saved.identity,
        runtime=Runner._runtime_toolchain_provenance(),
        frozen_fresh_source_sha256=digest,
        sources=Dict(name=>bytes2hex(open(sha256,joinpath(@__DIR__,name)))
            for name in ("spatial_balance.jl","profile_experiment.jl","tail_experiment.jl")),
        same_physical_axis_nm=cuts,
        selected_radius_in_periods=[2,3],mode_count=size(p.h,1),
        current_maximum_change_A_cm2=maximum(abs.(full.current_A_cm2 .- short.current_A_cm2)),
        restricted.removed_mode_norm,reconstructed_H_relative=restricted.verification_error,
        full,short,
    )
end

if abspath(PROGRAM_FILE)==abspath(@__FILE__)
    length(ARGS)==6 ||
        error("Usage: tail_experiment.jl ARCHIVE NATIVE_MODEL.h5 FROZEN_RUN FRESH_SHA256 OUTPUT WORKERS")
    input,model,reference,digest,output,worker_argument=ARGS
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    report=compare_tails(input,model,reference,digest,parse(Int,worker_argument))
    open(output,"w") do io
        Runner._light_json(io,report)
        println(io)
    end
end
