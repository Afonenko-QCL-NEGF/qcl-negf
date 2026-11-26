energy_edges(nodes) = [first(nodes); (nodes[1:end-1] .+ nodes[2:end])./2; last(nodes)]

function cell_lo_pair(energy, weights, omega)
    edges = energy_edges(energy)
    lower, upper = edges[1:end-1], edges[2:end]
    overlap = max.(0.0,min.(upper .+ omega,transpose(upper)) .-
        max.(lower .+ omega,transpose(lower)))
    plus = RC.sparse(overlap ./ weights)
    minus = RC.sparse(transpose(overlap) ./ weights)
    maximum(sum(plus;dims=2))<=1+2e-12 && maximum(sum(minus;dims=2))<=1+2e-12 ||
        error("translated LO overlap exceeds its energy-cell measure")
    return (;plus,minus)
end

function energy_refinement(problem, source, requested, divisions)
    new_nodes = Float64[]
    for (lo,hi) in requested
        for shift in (0., -0.367, 0.367, -problem.geo.voltage, problem.geo.voltage)
            append!(new_nodes, range(lo+shift,hi+shift,length=divisions+1))
        end
    end
    sort!(new_nodes)
    energy = copy(problem.en)
    for x in new_nodes
        first(energy)<x<last(energy) || continue
        i = searchsortedfirst(energy,x)
        min(abs(energy[i-1]-x),abs(energy[i]-x)) > 2e-13 &&
            insert!(energy,i,x)
    end
    edges = energy_edges(energy)
    weights = diff(edges)
    transfer = T.cell_transfer(energy_edges(problem.en),edges,problem.we,weights)
    old_shifts = cell_lo_pair(problem.en,problem.we,0.367)
    old_error = max(T.relerr(old_shifts.plus,problem.v.lo_plus),
        T.relerr(old_shifts.minus,problem.v.lo_minus))
    old_error<2e-12 || error("energy refinement changes the archived LO rule")
    shifts = cell_lo_pair(energy,weights,0.367)
    # Momentum and physical vertices are unchanged, but both directions of the
    # energy-shift pair are recomputed on the new measure.
    kernels = RC.lo_kernel(problem.v,physical_sites(problem),shifts.plus,shifts.minus)
    refined = LT.LinkedProblem(energy,weights,problem.wk,problem.geo.modes,problem.nb,
        problem.geo.offsets,problem.geo.voltage,problem.geo.reach,problem.h,problem.hops,
        problem.const_by_channel,kernels;spin_degeneracy=problem.spin_degeneracy,
        current_scale=problem.current_scale,density_scale=problem.density_scale,
        target_dimless=problem.target_dimless)
    axes_to = (problem.r^2,2,length(energy),problem.nk,length(LT.COLLISION_CHANNELS))
    mapped = zeros(axes_to)
    @views for e in eachindex(energy), j in findall(>(0),transfer[e,:])
        mapped[:,:,e,:,:] .+= transfer[e,j].*source[:,:,j,:,:]
    end
    report = (;energy_meV=100 .* energy,weights,shift_error=refined.shift_error,old_error,
        shift_before=RC.shift_metrics(problem.en,problem.we,problem.v.lo_plus,problem.v.lo_minus,0.367),
        shift_after=RC.shift_metrics(energy,weights,shifts.plus,shifts.minus,0.367),
        source_integral_error=measure_error(source,mapped,problem.we,weights,3))
    return (;problem=refined,source=mapped,report)
end

physical_sites(problem) = T.Runner._read_linked_array(fine_path,"ifr_sites",Float64,
    size(problem.v.interface_probes,1),problem.nz)

function measure_error(source, mapped, old_weights, new_weights, axis)
    function integrated(field, w, c)
        channel = selectdim(field,5,c)
        shape = ntuple(i->i==axis ? length(w) : 1, ndims(channel))
        return sum(channel .* reshape(w,shape);dims=axis)
    end
    errors = [T.relerr(integrated(source,old_weights,c),integrated(mapped,new_weights,c))
        for c in axes(source,5)]
    maximum(errors)<2e-12 || error("source integral changed on transfer")
    return errors
end

function radial_refinement(problem, source, radius, center, phases)
    ring = argmin(abs.(radius.-center))
    radius[ring] == center || error("refinement center must use an existing radius")
    increments = [sqrt(a^2+t*(b^2-a^2)) for (a,b) in
        ((radius[ring-1],center),(center,radius[ring+1])) for t in phases]
    grid = sort!([radius; increments])
    nk = length(grid)
    nz = problem.nz
    script = joinpath(@__DIR__,"radial_vertices.py")
    python = ENV["FATH_KERNEL_PYTHON"]
    builder = ENV["FATH_ARCHIVED_REGRID"]
    wk,ifr,lo,imp = open(`$python $script $builder $geometry $grid`,"r") do io
        wk = read!(io,zeros(nk))
        ifr = zeros(nk,nk)
        lo = zeros(ComplexF64,nz,nz,nk,nk)
        imp = zeros(nz,nz,nk,nk)
        @views for k in 1:nk
            read!(io,ifr[:,k])
            read!(io,lo[:,:,:,k])
            read!(io,imp[:,:,:,k])
        end
        eof(io) || error("trailing bytes in static vertex stream")
        return wk,ifr,lo,imp
    end
    isapprox(sum(wk),sum(problem.wk);rtol=2e-13) || error("radial mass changed")
    shared = searchsortedfirst.(Ref(grid),radius)
    grid[shared] == radius || error("old radii no longer nested")
    common = (;IFR=T.relerr(ifr[shared,shared],problem.v.interface_pair),
        LO=T.relerr(lo[:,:,shared,shared],problem.v.lo_covariance),
        impurity=T.relerr(imp[:,:,shared,shared],problem.v.impurity_covariance))
    reciprocal = map(v->T.pair_reciprocity(v,wk),(ifr,lo,imp))
    maximum((values(common)...,reciprocal...)) < 2e-12 ||
        error("radial vertex changed shared physical blocks or reciprocity")
    v = problem.v
    kernels = LT.LocalCollisionKernels(v.coordinate_frame,wk,v.acoustic,v.alloy,
        physical_sites(problem),ifr,lo,imp,v.lo_plus,v.lo_minus,v.bose)
    data = RC.coordinate_data(geometry,
        T.TOML.parsefile(joinpath(fine_path,"spec.toml"))["source_model_sha"],problem)
    chain = RC.bdd_chain(data,problem.geo.offsets,problem.geo.voltage;periodic_ends=true)
    modes = problem.geo.modes
    h = cat((modes'*SymTridiagonal(chain.diagonal+k^2*chain.radial,chain.off_diagonal)*modes
        for k in grid)...;dims=3)
    h_error = T.relerr(h[:,:,shared],problem.h)
    h_error<2e-12 || error("refined Hamiltonian changed original blocks")
    h[:,:,shared] .= problem.h
    all(==(problem.hops[:,1]),eachcol(problem.hops)) || error("k-dependent physical hopping")
    hops = repeat(problem.hops[:,1:1],1,nk)
    transfer = T.annular_transfer(radius,grid,problem.wk,wk)
    newer_anchor = zeros(ComplexF64,problem.r,problem.r,nk,length(LT.COLLISION_CHANNELS))
    @views for k in 1:nk, j in findall(>(0),transfer[k,:])
        newer_anchor[:,:,k,:] .+= transfer[k,j].*problem.const_by_channel[:,:,j,:]
    end
    refined = LT.LinkedProblem(problem.en,problem.we,wk,modes,problem.nb,
        problem.geo.offsets,problem.geo.voltage,problem.geo.reach,h,hops,newer_anchor,kernels;
        spin_degeneracy=problem.spin_degeneracy,current_scale=problem.current_scale,
        density_scale=problem.density_scale,target_dimless=problem.target_dimless)
    mapped = T.apply_radial(transfer,source)
    return (;problem=refined,source=mapped,report=(;grid,weights=wk,common,reciprocal,h_error,
        source_integral_error=measure_error(source,mapped,problem.wk,wk,4)))
end
