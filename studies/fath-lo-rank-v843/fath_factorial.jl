include("../fath-v843/continuation.jl")
using HDF5, TOML
include("lo_measure.jl")

function rebuild(p,v; modes=p.geo.modes, nb=p.nb, h=p.h, anchor=p.const_by_channel)
    return LT.LinkedProblem(p.en,p.we,p.wk,modes,nb,p.geo.offsets,p.geo.voltage,p.geo.reach,
        h,p.hops,anchor,v;spin_degeneracy=p.spin_degeneracy,current_scale=p.current_scale,
        density_scale=p.density_scale,target_dimless=p.target_dimless)
end

function coordinate_data(path, expected_sha, p)
    bytes2hex(open(sha256,path))==expected_sha || error("unexpected Fath native BDD input")
    return h5open(path,"r") do archive
        axial, lateral, material, position, widths =
            (read(archive[n]) for n in ("mass_axial","mass_lateral","E_conduction_dimensionless",
                "position_dimensionless","weight_position"))
        all(length(v)==p.nz for v in (axial,lateral,material,position,widths)) ||
            throw(DimensionMismatch("coordinate model axes differ from the packed input"))
        (;axial,lateral,material,position,step=only(unique(widths)))
    end
end

const BDD_CBAR = (1.054571817e-34)^2/(2*9.1093837139e-31*0.1*1.602176634e-19*(1e-8)^2)

function bdd_chain(coordinates, cells, bias; periodic_ends)
    (;axial,lateral,material,position,step) = coordinates
    nz = length(axial)
    span = (first(cells)*nz):(last(cells)*nz+nz-1)
    site(i) = mod(i,nz)+1
    sites = site.(span)
    face(i) = -2BDD_CBAR/(step^2*(axial[site(i)]+axial[site(i+1)]))
    faces = face.((first(span)-1):last(span))
    if !periodic_ends
        faces[1] = -BDD_CBAR/(step^2*axial[1])
        faces[end] = -BDD_CBAR/(step^2*axial[end])
    end
    z = position[sites] .+ (nz*step .* fld.(span,nz))
    diagonal = material[sites] .- bias.*z./(nz*step) .- faces[1:end-1] .- faces[2:end]
    return (;z,diagonal,off_diagonal=faces[2:end-1],radial=BDD_CBAR ./ lateral[sites])
end

function expand_modes(p, coordinates, radial)
    mode_count = p.nb+1
    n_periods = length(p.geo.offsets)
    tail = -3:3
    isolated = bdd_chain(coordinates,tail,0;periodic_ends=false)
    upper_span = (length(tail)*p.nb+1):(length(tail)*mode_count)
    band = eigen(SymTridiagonal(isolated.diagonal,isolated.off_diagonal),upper_span)
    localized = eigen(Symmetric(band.vectors'*(isolated.z .* band.vectors)))
    extra = band.vectors*localized.vectors[:,div(length(tail),2)+1]

    modes = zeros(ComplexF64,n_periods*p.nz,n_periods*mode_count)
    common = Int[]
    for (period,columns) in enumerate(p.geo.block_ranges)
        first_new = (period-1)*mode_count+1
        target = first_new:(first_new+p.nb-1)
        append!(common,target)
        modes[:,target] = p.geo.modes[:,columns]
        for distance in tail
            cell = period+distance
            1<=cell<=n_periods || continue
            rows = ((cell-1)*p.nz+1):(cell*p.nz)
            source = ((distance-first(tail))*p.nz+1):((distance-first(tail)+1)*p.nz)
            modes[rows,first_new+p.nb] = extra[source]
        end
    end
    gram = modes'*modes
    metric_error = norm(gram[common,common]-p.geo.metric)/norm(p.geo.metric)
    @assert metric_error < 2e-13
    q = p.v.coordinate_frame
    tail_components = reshape(extra,p.nz,length(tail))
    residual = tail_components-q*(q'*tail_components)
    decomposition = svd(residual)
    rank_added = count(>(1e-10),decomposition.S)
    @assert rank_added>0
    extra_q = decomposition.U[:,1:rank_added]
    extra_q -= q*(q'*extra_q)
    extra_q = Matrix(qr(extra_q).Q)[:,1:rank_added]
    q_new = [q extra_q]
    chain = bdd_chain(coordinates,p.geo.offsets,p.geo.voltage;periodic_ends=true)
    h = cat([modes'*SymTridiagonal(chain.diagonal+k^2*chain.radial,chain.off_diagonal)*modes
        for k in radial]...;dims=3)
    h_error = norm(h[common,common,:]-p.h)/norm(p.h)
    @assert h_error < 2e-12
    return (;modes,nb=mode_count,q=q_new,h,common,rank_added,metric_error,h_error,
        eighth_band_range_meV=100 .* extrema(band.values),
        local_singular_values=decomposition.S,
        metric_condition=cond(gram),
        center_weight_added=norm(tail_components[:,4])^2)
end

function lift_source(packed,embedding)
    r_new,r_old = size(embedding)
    output = zeros(r_new^2,size(packed)[2:end]...)
    old = zeros(ComplexF64,r_old,r_old)
    new = zeros(ComplexF64,r_new,r_new)
    mid = zeros(ComplexF64,r_new,r_old)
    packed_shape = reshape(packed,r_old^2,:)
    output_shape = reshape(output,r_new^2,:)
    roundtrip_maximum = 0.
    @views for slice in axes(packed_shape,2)
        LT.unpack_hermitian!(old,packed_shape[:,slice])
        mul!(mid,embedding,old)
        mul!(new,mid,embedding')
        LT.pack_hermitian!(output_shape[:,slice],new)
        err = norm(embedding'*new*embedding-old)/max(norm(old),floatmin(Float64))
        roundtrip_maximum = max(roundtrip_maximum,err)
    end
    roundtrip_maximum < 5e-13 || error("packed state failed the shared-subspace round trip")
    return (;source=output,roundtrip_maximum)
end

function collision_input(p,seed,workers)
    total = dropdims(sum(seed;dims=5);dims=5)
    anchor = dropdims(sum(p.const_by_channel;dims=4);dims=4)
    projected = LT.projected_image(p,total,anchor,:input_projected;
        projector=LT.project_linked_economical,selected_rows=true,order=18,
        subdivisions=2,grading=true,workers,observe=_->nothing)
    occupation = similar(projected.occupation)
    normalization = LT.prepare_occupation!(occupation,projected,p)
    return (;occupation,normalization)
end

function analyze_fath(p,seed,cuts,maps,workers; channel_control)
    widths = (cuts[3:end] .- cuts[1:end-2])./2
    measured = nothing
    history = NamedTuple[]
    confirmations = 0
    for step in 1:maps
        start = time_ns()
        image = LT.linked_fresh_map(p,seed;projector=LT.project_linked_economical,
            selected_rows=true,projection_for_collision=true,workers)
        row = linked_metrics(image.summary,widths)
        confirmations = strictly_qualified(row) ? confirmations+1 : 0
        push!(history,(;step,row...,confirmations,elapsed_s=(time_ns()-start)*1e-9))
        println(stderr,"map $step of $maps: rK=",row.rK," spatial deviation=",row.spatial.max_deviation_from_mean_A_cm2)
        flush(stderr)
        if step==maps || confirmations>=3
            observation = spatial_balance(p,image.source,widths;
                workers,energy_rule=independent_energy_rule,current_cuts=cuts)
            pair = row.fermionic_pair
            lagged = spatial_balance(p,seed,widths;collision_sources=image.source,workers,
                energy_rule=independent_energy_rule,current_cuts=cuts,coefficients=(pair.a,pair.c))
            measured = (;observation,lagged,summary=image.summary,
                independent_profile_difference_A_cm2=maximum(abs.(observation.current_A_cm2.-
                    row.current_profile_A_cm2)))
            break
        end
        seed .= 0.65 .* seed .+ 0.35 .* image.source
    end
    stationary = confirmations>=3 && measured.independent_profile_difference_A_cm2 <=
        measured.observation.current.target_tolerance_A_cm2 &&
        measured.observation.current.max_deviation_from_mean_A_cm2 <=
        measured.observation.current.target_tolerance_A_cm2 && measured.lagged.weighted_rK_Q<1e-8
    return (;history,measured...,channel_control,stationary)
end

function main()
    length(ARGS)==8 || error("Usage: fath_factorial.jl ARCHIVE NATIVE_BDD base|expanded cell|hat MAPS WORKERS map|operator OUTPUT")
    archive,geometry,rank_mode,lo_mode,maps_arg,workers_arg,action,output = ARGS
    rank_mode in ("base","expanded") && lo_mode in ("cell","hat") &&
        action in ("map","operator") || error("unregistered experimental condition")
    maps,workers = parse(Int,maps_arg),parse(Int,workers_arg)
    maps>=1 && workers>=1 || error("positive map and worker counts required")
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    input = Runner._read_linked_checkpoint(archive)
    p = input.problem
    p.geo.voltage≈0.54 && input.identity["temperature_K"]==10.0 || error("expected Fath at 54 mV and 10 K")
    spec = TOML.parsefile(joinpath(archive,"spec.toml"))
    ifr_sites = Runner._read_linked_array(archive,"ifr_sites",Float64,spec["n_interfaces"],p.nz)
    pair = lo_mode=="cell" ? (;plus=p.v.lo_plus,minus=p.v.lo_minus) : hat_shift_pair(p.en,p.we,FATH_LO)
    changed = lo_kernel(p.v,ifr_sites,pair.plus,pair.minus)
    problem = rebuild(p,changed)
    source = input.seed
    rank = (;nb=p.nb,r=p.r)
    if rank_mode=="expanded"
        coordinates = coordinate_data(geometry,input.identity["source_geometry_model_sha256"],p)
        radial = Runner._read_linked_array(archive,"k",Float64,p.nk)
        expanded = expand_modes(p,coordinates,radial)
        v = lo_kernel(p.v,ifr_sites,pair.plus,pair.minus;q=expanded.q)
        embedding = expanded.q'*p.v.coordinate_frame
        lift = lift_source(input.seed,embedding)
        anchor = cat([embedding*p.const_by_channel[:,:,k,c]*embedding'
            for k in 1:p.nk, c in eachindex(LT.COLLISION_CHANNELS)]...;dims=3)
        anchors = reshape(anchor,size(expanded.q,2),size(expanded.q,2),p.nk,:)
        problem = rebuild(p,v;modes=expanded.modes,nb=expanded.nb,h=expanded.h,anchor=anchors)
        common_bases_error = maximum(norm(embedding'*b[:,expanded.common]-old)/norm(old)
            for (b,old) in zip(problem.geo.bases,p.geo.bases))
        @assert common_bases_error < 2e-13
        source = lift.source
        rank = (;nb=problem.nb,r=problem.r,expanded.rank_added,expanded.metric_error,
            expanded.h_error,expanded.eighth_band_range_meV,expanded.local_singular_values,
            expanded.metric_condition,expanded.center_weight_added,common_bases_error,
            source_roundtrip_maximum=lift.roundtrip_maximum)
    end
    println(stderr,"input and rank/LO condition verified in RAM: ",rank_mode," / ",lo_mode)
    flush(stderr)
    result = if action=="operator"
        projected = collision_input(problem,source,workers)
        alternate = hat_shift_pair(p.en,p.we,FATH_LO)
        alternate_kernel = lo_kernel(problem.v,ifr_sites,alternate.plus,alternate.minus)
        (;normalization=projected.normalization,
            event_balance=lo_events(projected.occupation,problem.v,ifr_sites,p.en,p.we,FATH_LO),
            alternate_on_same_occupation=lo_events(projected.occupation,alternate_kernel,ifr_sites,p.en,p.we,FATH_LO))
    else
        analyze_fath(problem,source,input.current_midpoints,maps,workers;channel_control=nothing)
    end
    report = (;schema="qcl-negf-fath-factorial/v1",input.identity,rank_mode,lo_mode,rank,maps,workers,action,
        core=Runner._linked_package_identity(Runner.QCLNEGF),
        runner=Runner._linked_package_identity(Runner),runtime=Runner._runtime_toolchain_provenance(),
        source_sha256=bytes2hex(open(sha256,@__FILE__)),
        lo_source_sha256=bytes2hex(open(sha256,joinpath(@__DIR__,"lo_measure.jl"))),
        cut_coordinates_nm=input.current_midpoints,
        lo_measure=shift_metrics(p.en,p.we,pair.plus,pair.minus,FATH_LO),result...)
    open(output,"w") do io
        Runner._light_json(io,report)
        println(io)
    end
end

abspath(PROGRAM_FILE)==abspath(@__FILE__) && main()
