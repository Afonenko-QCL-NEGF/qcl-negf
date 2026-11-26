using Unitful

const Runner = T.Runner
const CoreNUM = Runner.QCLNEGF.QCLNumerics
const CoreDomain = Runner.QCLNEGF.QCLDomain
include("bosco_vertices.jl")
const source_work = dirname(dirname(dirname(coarse_path)))
const calibration = joinpath(source_work,"dupont","linked-adaptive-v3-seal","method","pinned",
    "causal_operator.jl")
include(calibration)

function bosco_configuration(reference, overrides, scheme)
    # The published device uses the original layer sequence and fixed screening.
    # The five-channel procedure uses the same documented alloy coefficients as Fath.
    configuration = Dict(
        "run"=>Dict("name"=>"bosco2019-200k-56mV", "classification"=>"study"),
        "physical"=>Dict("lattice_temperature"=>"200 K","lo_temperature"=>"200 K",
            "alloy_potential"=>"0.60 eV","primitive_cell_volume"=>"4.5168e-29 m^3"),
        "physical_models"=>Dict("screening"=>"fixed","dispersion"=>"parabolic",
            "lo_population"=>"thermal","electron_electron"=>Dict("mode"=>"none")),
        "numerical"=>Dict("spatial_nodes"=>scheme.nz,"basis_states"=>scheme.base_modes,
            "basis_periods"=>3,"energy_min"=>"$(scheme.Emin) eV","energy_max"=>"$(scheme.Emax) eV",
            "energy_nodes"=>scheme.ne,"momentum_max"=>"0.60 nm^-1","momentum_nodes"=>scheme.nk,
            "angular_nodes"=>scheme.angular,"longitudinal_momentum_nodes"=>scheme.nqz),
        "scattering"=>Dict("alloy_disorder"=>true),
        "algorithms"=>Dict("energy_shift"=>"conservative_pair","hilbert"=>"fft"),
        "execution"=>Dict("strategy"=>"manual","solver_backend"=>"production",
            "julia_threads"=>Threads.nthreads(),"blas_threads"=>1,"fail_on_thread_mismatch"=>true),
        "production"=>Dict("checkpoint_every_outer"=>0,"checkpoint_every_scba"=>0,
            "energy_chunk"=>32,"worker_count"=>Threads.nthreads()),
        "output"=>Dict("resume"=>false,"intermediate_checkpoints"=>false,
            "save_full_state"=>false,"debug_hdf5"=>false,"live_visualization"=>false),
        "study"=>Dict("temperatures"=>["200 K"],"voltages_per_period"=>["56 mV"],
            "calculate_optical_response"=>false))
    Runner.YAML.write_file(overrides,configuration)
    return Runner.load_run_configuration([reference,overrides])
end

function bosco_coordinates(p)
    g, m = p.grids, p.profiles
    return (;axial=m.mᶻᵣ,lateral=m.m_parallelᵣ,material=m.Eᶜ,position=g.x,step=only(unique(g.wˣ)))
end

function localized_templates(data, count)
    tail = -3:3
    d = RC.bdd_chain(data,tail,0;periodic_ends=false)
    fd = SymTridiagonal(d.diagonal,d.off_diagonal)
    subspace = eigen(fd,1:length(tail)*count)
    pzp = eigen(Symmetric(subspace.vectors'*(d.z .* subspace.vectors)))
    select = 3count+1:4count
    templates = subspace.vectors*pzp.vectors[:,select]
    for column in eachcol(templates)
        column[argmax(abs.(column))]<0 && (column .*= -1)
    end
    return templates
end

function bosco_transport_geometry(p, nb)
    data = bosco_coordinates(p)
    nz, base = length(data.position), p.numerical.N_b
    tail = -3:3
    offsets = -4:4
    voltage = 0.56
    templates = localized_templates(data,base)
    fd = RC.bdd_chain(data,tail,0;periodic_ends=false)
    base_chain = SymTridiagonal(fd.diagonal,fd.off_diagonal)
    for count in base+1:nb
        band = eigen(base_chain,(length(tail)*(count-1)+1):(length(tail)*count))
        localization = eigen(Symmetric(band.vectors'*(fd.z .* band.vectors)))
        mode = band.vectors*localization.vectors[:,4]
        mode[argmax(abs.(mode))]<0 && (mode .*= -1)
        templates = hcat(templates,mode)
    end
    modes = zeros(ComplexF64,length(offsets)*nz,length(offsets)*nb)
    for j in eachindex(offsets), u in eachindex(tail)
        i = j+tail[u]
        1<=i<=length(offsets) || continue
        rows = (i-1)*nz+1:i*nz
        cols = (j-1)*nb+1:j*nb
        local_rows = (u-1)*nz+1:u*nz
        modes[rows,cols] .= templates[local_rows,:]
    end
    # Keep the reference Phi as a subspace so the calibrated cold-seed real
    # part can be embedded and restricted without changing its matrix elements.
    q_base = p.basis.Φ
    slices = reshape(templates,nz,length(tail)*nb)
    decomp = svd(slices-q_base*(q_base'*slices))
    added = count(>(1e-10),decomp.S)
    extension = decomp.U[:,1:added]
    extension -= q_base*(q_base'*extension)
    q = hcat(q_base,Matrix(qr(extension).Q)[:,1:added])
    projection = norm(slices-q*(q'*slices))/norm(slices)
    projection <= 2e-10 || error("Bosco Q misses local mode components")
    gram_condition = cond(modes'*modes)
    gram_condition < 100 || error("Bosco translated basis is ill-conditioned")
    return (;data,voltage,offsets,modes,q,templates,projection,gram_condition,nb)
end

function bosco_anchor(p, configuration, Q)
    n = p.numerical.N_b
    h = Runner.project_hamiltonians(p, zeros(length(p.grids.x)))
    options = configuration.production
    cache = Runner.build_production_cache(p;options)
    green,μ = CoreNUM._seed_green_production(p,h,options)
    frozen = CoreNUM._scattering_candidate_production(p,green,cache,options)
    reference = FathCausalOperator.fath_causal_reference(p.grids.ε,p.grids.κ,frozen;anchor_meV=5.8)
    embedding = Q' * p.basis.Φ
    r = size(Q,2)
    result = zeros(ComplexF64,r,r,length(p.grids.κ),length(LT.COLLISION_CHANNELS))
    errors = zeros(length(LT.COLLISION_CHANNELS))
    for (c,channel) in enumerate(LT.COLLISION_CHANNELS), k in eachindex(p.grids.κ)
        original = reshape(reference.constants[channel][k,:,:],n,n)
        result[:,:,k,c] .= embedding*original*embedding'
        actual = embedding' * result[:,:,k,c] * embedding
        errors[c] = max(errors[c],T.relerr(original,actual))
    end
    maximum(errors)<2e-12 || error("Bosco cold-seed anchor lost the native restriction")
    return (;result,μ,errors)
end

function fermi_seed(problem, thermal_energy, η)
    R0 = problem.r
    energies, coefficients = [], []
    center_basis = LT.centered_basis(problem.geo)
    for k in 1:problem.nk
        spectrum = eigen(Hermitian(problem.h[:,:,k]),Hermitian(problem.geo.metric))
        push!(energies,spectrum.values)
        push!(coefficients,center_basis*spectrum.vectors)
    end
    weights = [sum(abs2,v;dims=1) |> vec for v in coefficients]
    logistic(x) = inv(1+exp(clamp(x,-700.,700.)))
    function sheet(μ)
        return sum(problem.weights[e,k]*logistic((x-μ)/thermal_energy)*
            sum(weights[k].*(2η./((x.-energies[k]).^2 .+ η^2)))
            for (e,x) in enumerate(problem.en), k in 1:problem.nk)
    end
    target = problem.target_dimless
    lo,hi = first(problem.en)-10thermal_energy,last(problem.en)+10thermal_energy
    sheet(lo)<target<sheet(hi) || error("Bosco seed charge not bracketed")
    for _ in 1:80
        μ = (lo+hi)/2
        if sheet(μ)<target
            lo = μ
        else
            hi = μ
        end
    end
    chemical_potential = (lo+hi)/2
    raw_sheet = sheet(chemical_potential)
    isapprox(raw_sheet,target;rtol=5e-12) || error("Bosco cold-seed charge mismatch")
    occ = zeros(R0^2,2,problem.ne,problem.nk)
    @views for (e,x) in enumerate(problem.en), k in 1:problem.nk
        spectral = coefficients[k] * Diagonal(2η./((x .- energies[k]).^2 .+ η^2)) * coefficients[k]'
        spectral .= (spectral+spectral')/2
        f = logistic((x-chemical_potential)/thermal_energy)
        LT.pack_hermitian!(occ[:,1,e,k],f .* spectral)
        LT.pack_hermitian!(occ[:,2,e,k],(1-f) .* spectral)
    end
    seed = zeros(R0^2,2,problem.ne,problem.nk,length(LT.COLLISION_CHANNELS))
    LT.scatter_packed!(seed,occ,problem.v)
    return (;seed,chemical_potential,raw_sheet)
end

function replace_axes(grid; energy=grid.ε, radius=grid.κ)
    wE, wk = diff(energy_edges(energy)),diff(energy_edges(radius).^2)./(4π)
    trusted = BitVector(first(energy)+0.8 .<= energy .<= last(energy)-0.8)
    return CoreDomain.ModelGrids(grid.x,grid.wˣ,energy,wE,trusted,radius,wk,grid.qᶻ,grid.wᑫᶻ,grid.φ)
end

function bosco_grid(p, layout, scheme)
    grid = p.grids
    branch = scheme.refinement
    branch=="base" && return grid
    m = layout.modes
    cells = layout.offsets
    chain = RC.bdd_chain(layout.data,cells,layout.voltage;periodic_ends=true)
    h0 = m'*SymTridiagonal(chain.diagonal,chain.off_diagonal)*m
    gram = m'*m
    modes = eigen(Hermitian(h0),Hermitian(gram))
    center = div(length(cells),2)*length(grid.x)
    sites = (center+1):(center+length(grid.x))
    occupancy_weight = vec(sum(abs2,(m*modes.vectors)[sites,:];dims=1))
    refs = filter(j->occupancy_weight[j]>=0.20 && -0.5<modes.values[j]<1.0,
        eachindex(occupancy_weight))
    isempty(refs) && error("Bosco physical pole selection found no central-band reference")
    if branch=="local_K"
        thermal = 8.617333262145e-5*200/p.scales.E₀_eV
        radial_mass = 0.067
        turning = sqrt(thermal*radial_mass/RC.BDD_CBAR)
        k = clamp(argmin(abs.(grid.κ.-turning)),2,length(grid.κ)-1)
        radius = copy(grid.κ)
        for (u,v) in ((radius[k-1],radius[k]),(radius[k],radius[k+1])), f in (0.25,0.5,0.75)
            push!(radius,sqrt(u^2+f*(v^2-u^2)))
        end
        return replace_axes(grid;radius=sort!(radius))
    end
    energy = copy(grid.ε)
    bounds = extrema(grid.ε)
    for j in refs, shift in (0.,0.367,-0.367,0.56,-0.56)
        for e in range(modes.values[j]+shift-0.01,modes.values[j]+shift+0.01,length=9)
            first(bounds)<e<last(bounds) || continue
            all(x->abs(x-e)>2e-13,energy) && push!(energy,e)
        end
    end
    return replace_axes(grid;energy=sort!(energy))
end

function verify_bosco_vertices(p, grid, cov)
    # Independently integrate the coordinate arrays in native Phi on a subset.
    picks = unique([1,cld(length(grid.κ),2),length(grid.κ)])
    slim = replace_axes(grid; radius=grid.κ[picks])
    basis = p.basis
    physical, s = p.physical,p.scales
    Φ = basis.Φ
    n = size(Φ,2)
    density(ψ) = hcat((conj.(ψ[:,a]).*ψ[:,b] for b in 1:n for a in 1:n)...)
    D = density(Φ)
    IFD = density(cov.interfaces*Φ)
    refs = (
        LO=first(CoreNUM.lo_phonon_kernel(physical,s,slim,basis)),
        acoustic=CoreNUM.acoustic_kernel(physical,s,slim,basis),
        impurity=CoreNUM.impurity_kernel(physical,s,slim,p.profiles,basis;angular=:legacy_uniform),
        IFR=CoreNUM.interface_roughness_kernel(physical,s,slim,basis),
        alloy=CoreNUM.alloy_kernel(physical,s,slim,p.profiles,basis),
    )
    pairs_to_check = ((1,1),(1,length(picks)),(2,2))
    comparison = map(pairs_to_check) do (m,mp)
        kin,kout = picks[mp],picks[m]
        values = (
            LO=transpose(D)*cov.lo[:,:,kin,kout]*D,
            acoustic=transpose(D)*(cov.acoustic.*D),
            impurity=transpose(D)*cov.impurity[:,:,kin,kout]*D,
            IFR=cov.ifr_pair[kin,kout].*(transpose(IFD)*IFD),
            alloy=transpose(D)*(cov.alloy.*D),
        )
        channels = Dict{String,Any}()
        for name in keys(refs)
            a = getproperty(values,name)
            r = reshape(getproperty(refs,name)[m,mp,:,:,:,:],n^2,n^2)
            channels[string(name)] = (;relative=T.relerr(a,r),absolute=maximum(abs,a.-r))
        end
        return (;outgoing=grid.κ[kout]/10,incoming=grid.κ[kin]/10,channels)
    end
    maximum(channel.relative for point in comparison for channel in values(point.channels))<2e-11 ||
        error("Bosco vertices differ from Core on common physical pairs: $comparison")
    return comparison
end

function anchor_on_grid(original, old, destination)
    old==destination && return original
    anchor = similar(original,size(original,1),size(original,2),length(destination),size(original,4))
    for (i,k) in enumerate(destination)
        right = searchsortedfirst(old,k)
        left = right==1 || old[right]==k ? right : right-1
        f = right==left ? 0. : (k^2-old[left]^2)/(old[right]^2-old[left]^2)
        @views anchor[:,:,i,:] .= (1-f).*original[:,:,left,:] .+ f.*original[:,:,right,:]
    end
    return anchor
end

function make_bosco_problem(p, scheme, configuration)
    layout = bosco_transport_geometry(p,scheme.nb)
    grid = bosco_grid(p,layout,scheme)
    Q = layout.q
    cov = BoscoVertices.assemble(p.physical,p.profiles,grid,p.scales,:gaussian;
        enabled=LT.COLLISION_CHANNELS)
    vertex_control = verify_bosco_vertices(p,grid,cov)
    w = grid.wᵏ
    reciprocity = map(a->T.pair_reciprocity(a,w),(cov.ifr_pair,cov.lo,cov.impurity))
    maximum(reciprocity)<2e-12 || error("Bosco kernels lost radial reciprocity")
    shifts = cell_lo_pair(grid.ε,grid.wᴱ,0.367)
    kernels = LT.LocalCollisionKernels(Q,w,cov.acoustic,cov.alloy,cov.interfaces,
        cov.ifr_pair,cov.lo,cov.impurity,shifts.plus,shifts.minus,cov.bose)
    chain = RC.bdd_chain(layout.data,layout.offsets,layout.voltage;periodic_ends=true)
    modes = layout.modes
    h = cat((modes'*SymTridiagonal(chain.diagonal+k^2*chain.radial,chain.off_diagonal)*modes
        for k in grid.κ)...;dims=3)
    nz = length(grid.x)
    mid = div(length(layout.offsets),2)
    hops = repeat(chain.off_diagonal[mid*nz:(mid+1)*nz],1,length(grid.κ))
    anchor = bosco_anchor(p,configuration,Q)
    anchors = anchor_on_grid(anchor.result,p.grids.κ,grid.κ)
    density_scale = 1/(p.scales.L₀_m^2*1e4)
    target = dot(grid.wˣ,p.profiles.Nᴰ)
    abs(target*density_scale-4.5e10) < 1e-3 || error("Bosco donor sheet does not match passport")
    jscale = ustrip(u"A/m^2",p.scales.J₀)/1e4
    problem = LT.LinkedProblem(grid.ε,grid.wᴱ,w,modes,layout.nb,collect(layout.offsets),layout.voltage,7,
        h,hops,anchors,kernels;spin_degeneracy=2.,current_scale=jscale,density_scale,
        target_dimless=target)
    seed = fermi_seed(problem,8.617333262145e-5*200/p.scales.E₀_eV,0.0005/p.scales.E₀_eV)
    cuts = collect(range(0,length(grid.x)*layout.data.step*1e9*p.scales.L₀_m,length=nz+1))
    spacing = grid.wˣ .* (1e9*p.scales.L₀_m)
    audit = (;layout.projection,layout.gram_condition,reciprocity,vertex_control,anchor=anchor.errors,
        energy_meV=100 .* grid.ε,k_nm_inverse=grid.κ./10,grid.wᴱ,grid.wᵏ,
        native_chemical_potential_meV=100anchor.μ,seed_chemical_potential_meV=100seed.chemical_potential,
        seed_sheet_cm2=seed.raw_sheet*density_scale,donor_sheet_cm2=target*density_scale,
        dims=(problem.ne,problem.nk,problem.nb,problem.r),LO_bose=cov.bose)
    return (;problem,seed=seed.seed,cuts,spacing,audit)
end

function density_regions(x, energy, n, wz, wE)
    definitions = (
        (name="injector", z=(10.,25.), E=(-30.,0.)),
        (name="upper", z=(0.,8.), E=(20.,55.)),
        (name="lower", z=(15.,26.), E=(0.,30.)),
    )
    return map(definitions) do region
        regions = [begin
            zz = findall(p -> first(region.z)<=p-3.26+dz<last(region.z),x)
            ee = findall(p -> first(region.E)<=p+56*3.26/29.61+dE<last(region.E),energy)
            weights = wz[zz].*n[zz,ee].*transpose(wE[ee])
            sheet = sum(weights)
            zcenter = iszero(sheet) ? nothing : dot(x[zz].-3.26.+dz,vec(sum(weights;dims=2)))/sheet
            ecenter = iszero(sheet) ? nothing :
                dot(energy[ee].+56*3.26/29.61+dE,vec(sum(weights;dims=1)))/sheet
            (;dz,dE,sheet_cm2=sheet*1e14,zcenter_fig_nm=zcenter,ecenter_fig_meV=ecenter)
        end for dz in (0.,-0.3,0.3) for dE in (0.,-3.,3.)]
        return (;region.name,regions)
    end
end

function bosco_local_modes(problem, cuts)
    idx = problem.geo.center_modes
    eigenstates = eigen(Hermitian(problem.h[idx,idx,1]),Hermitian(problem.geo.metric[idx,idx]))
    columns = problem.geo.modes[:,idx] * eigenstates.vectors
    mid = div(length(problem.geo.offsets),2)*problem.nz
    z = (cuts[1:end-1].+cuts[2:end])./2
    well1 = findall(p->3.26<=p<11.25,z)
    well2 = findall(p->13.15<=p<29.61,z)
    return map(eachindex(eigenstates.values)) do j
        local_weights = abs2.(columns[mid+1:mid+problem.nz,j])
        central = sum(local_weights)
        return (;index=j,energy_meV=100eigenstates.values[j],central_weight=central,
            well_weights=(sum(local_weights[well1]),sum(local_weights[well2])),
            centroid_nm=central==0 ? nothing : dot(z,local_weights)/central)
    end
end

function bosco_density(output, problem, occupation, native)
    n = zeros(problem.nz,problem.ne)
    rho = zeros(ComplexF64,problem.r,problem.r)
    work = zeros(ComplexF64,problem.nz,problem.r)
    site = problem.v.coordinate_frame
    for e in 1:problem.ne, k in 1:problem.nk
        @views LT.unpack_hermitian!(rho,occupation[:,1,e,k])
        mul!(work,site,rho)
        for z in 1:problem.nz
            n[z,e] += problem.wk[k] * real(dot(view(site,z,:),view(work,z,:)))
        end
    end
    n .*= problem.spin_degeneracy/(2π)*problem.density_scale/1e14
    rawnm = sum(n*problem.we)
    x = native.grids.x .* (1e9*native.scales.L₀_m)
    wz = native.grids.wˣ .* (1e9*native.scales.L₀_m)
    n ./= 100 .* wz
    open(output,"w") do io
        println(io,"energy_meV,z_nm,energy_weight_meV,z_weight_nm,n_per_meV_nm3")
        for e in eachindex(problem.en), z in eachindex(x)
            println(io,join((100problem.en[e],x[z],100problem.we[e],wz[z],n[z,e]),','))
        end
    end
    wells = ((3.26,11.25),(13.15,29.61))
    integrated = n * (100 .* problem.we)
    well_sheets = [sum(wz[j]*integrated[j] for j in findall(z -> a<=z<b,x))*1e14 for (a,b) in wells]
    regions = density_regions(x,100 .* problem.en,n,wz,100 .* problem.we)
    return (;sheet_cm2=rawnm*1e14,min_density=minimum(n),well_sheets,regions)
end

function bosco_row(problem,image,cuts)
    row = T.linked_metrics(image.summary,T.widths_at(cuts))
    j = row.current_profile_A_cm2
    return (;row...,oriented_seams=j[[1,end]])
end

function solve_bosco(work,scheme)
    out = joinpath(work,"bosco")
    ispath(out) && error("Bosco run directory already exists")
    mkdir(out)
    reference = joinpath(ENV["FATH_APP"],"runner","examples","config","reference-2019-70k.yaml")
    override = joinpath(out,"point.yaml")
    configuration = bosco_configuration(reference,override,scheme)
    native = Runner.build_configured_problem(configuration).problem
    physical = native.physical
    ustrip(u"K",physical.Tᴸ)==200 && ustrip(u"K",physical.Tᴸᴼ)==200 &&
        isapprox(ustrip(u"V/m",physical.F_bias),0.056/29.61e-9;rtol=1e-12) &&
        native.scales.L₀_m==1e-8 && native.scales.E₀_eV==0.1 ||
        error("Bosco point does not match the dimensional passport")
    configuration.output.intermediate_checkpoints == false &&
        configuration.output.save_full_state == false && configuration.output.resume == false ||
        error("Bosco point requires an in-memory trajectory")
    built = make_bosco_problem(native,scheme,configuration)
    problem,cuts,state = built.problem,built.cuts,built.seed
    path = joinpath(out,"trajectory.jsonl")
    R.append_row(path,"configuration",(;scheme,built.audit,reference_sha=T.file_sha(reference),
        override_sha=T.file_sha(override),init_sha=T.packed_sha(state),cuts,
        local_modes=bosco_local_modes(problem,cuts)))
    confirmations = 0
    last_measurement = nothing
    previous = nothing
    history = NamedTuple[]
    for step in Iterators.countfrom(1)
        image = LT.linked_fresh_map(problem,state;projector=LT.project_linked_economical,
            selected_rows=true,projection_for_collision=true,workers=Threads.nthreads())
        row = bosco_row(problem,image,cuts)
        jmean = row.spatial.mean_internal_A_cm2
        tolerance = max(1.0,0.01abs(jmean))
        pass = T.strictly_qualified(row) && maximum(abs,row.oriented_seams.-jmean)<=tolerance
        confirmations = pass ? confirmations+1 : 0
        push!(history,(;row.rK,row.rSigma,mean=jmean))
        prior = history[max(1,end-8)]
        plateau = step>=96 && step%8==0 &&
            row.rK>=0.75prior.rK && row.rSigma>=0.75prior.rSigma &&
            abs(jmean-prior.mean)<=tolerance
        final = confirmations>=3 || plateau
        R.append_row(path,"map",(;step,row,confirmations,plateau,nodal=nodal_audit(image)))
        if final || step in (1,8,16,24,32) || step%16==0
            observed = R.direct_observation(problem,image.source,cuts,Threads.nthreads())
            check = maximum(abs,observed.current_A_cm2.-row.current_profile_A_cm2)
            profile = observed.current_A_cm2
            jmean = observed.current.mean_internal_A_cm2
            previous,last_measurement = last_measurement,(;step,jmean,profile)
            R.append_row(path,"independent",(;step,observed,quadrature_error=check))
            if final
                density = bosco_density(joinpath(out,"density.csv"),problem,image.projected.occupation,native)
                charge_error = density.sheet_cm2-observed.raw_sheet_cm2
                native_density_error = density.sheet_cm2-row.raw_sheet_cm2
                abs(native_density_error)<=1e-8*problem.target_dimless*problem.density_scale ||
                    error("Bosco projected density did not reproduce projected raw charge")
                synced = RC.observe_balance(problem,image.source,image,cuts,Threads.nthreads();
                    fresh_profile=false,lo_control=false).lagged
                R.append_row(path,"signed_balance",(;step,synced))
                independent_flat = observed.current.max_deviation_from_mean_A_cm2<=tolerance &&
                    maximum(abs,profile[[1,end]].-jmean)<=tolerance
                drift = isnothing(previous) ? nothing : maximum(abs,profile.-previous.profile)
                R.append_row(path,"finished",(;step,confirmations,plateau,density,charge_error,native_density_error,late_drift=drift,
                    late_interval=isnothing(previous) ? nothing : (previous.step,step),
                    quadrature_error=check,mean_A_cm2=jmean,
                    reference_difference_A_cm2=jmean-3603.55,
                    reference_line_halfwidth_A_cm2=9.2624,
                    reference_adjacent_vertex_range_A_cm2=(3568.187,3603.55),
                    strict=confirmations>=3 && independent_flat && check<=tolerance))
                return
            end
        end
        R.k31_update!(state,image,alpha)
        GC.gc(false)
    end
end

function run_bosco(work,scheme)
    if isfile(joinpath(work,"bosco-queue-14.ready"))
        launcher = joinpath(@__DIR__,"bosco-queued.jl")
        project = joinpath(ENV["FATH_APP"],"runner")
        inputs = ARGS[1:4]
        julia = joinpath(Sys.BINDIR,"julia")
        # The Fath process waits while the sole numerical worker runs Bosco.
        GC.gc()
        try
            return Base.run(`$julia --compiled-modules=existing --startup-file=no --project=$project --threads=12,0 --gcthreads=1,0 --heap-size-hint=16G $launcher $inputs $work`)
        catch err
            err isa ProcessFailedException && !ispath(joinpath(work,"bosco")) || rethrow()
            Main.announce((;phase="bosco_queue_bootstrap_failed",fallback="existing Runner",
                error=sprint(showerror,err)))
        end
    end
    return solve_bosco(work,scheme)
end
