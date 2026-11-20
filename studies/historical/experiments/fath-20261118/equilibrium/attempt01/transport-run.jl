using QCLNEGF, Unitful, LinearAlgebra, HDF5, TOML, SHA
const N = QCLNEGF.QCLNumerics
const EXPECTED_HEAD = "e171caa60cce676c6c4238dd671e7c527f2bd977"
const EXPECTED_TREE = "742ed5a6fe82f1e5c63fc1a2290ed77f89ca6da8"
const EXPECTED_MANIFEST = "da0780fbe150c0e16e9fedf3566a1971095642f14f57f32524b52f430a4adb65"
const CHANNELS = [:LO,:acoustic,:impurity,:IFR,:alloy]
const RUN_STARTED = time()
const SQ_FLOOR = 1e-14

sha(path) = bytes2hex(open(sha256, path))
digest(x) = bytes2hex(sha256(reinterpret(UInt8,vec(x))))
showval(x::Symbol) = string(x)
showval(x::Union{Real,AbstractString}) = x
showval(x::Complex) = Dict("real"=>real(x),"imag"=>imag(x))
showval(x::Nothing) = "not_measured"
showval(x::AbstractArray) = ndims(x) == 1 ? showval.(x) :
    Dict("shape"=>collect(size(x)),"column_major_values"=>showval.(vec(x)))
showval(x::AbstractDict) = Dict(string(k)=>showval(v) for (k,v) in x)
showval(x) = Dict(string(f)=>showval(getfield(x,f)) for f in fieldnames(typeof(x)))

function write_toml(path, fields)
    open(path*".tmp","w") do io
        TOML.print(io,fields; sorted=true)
    end
    mv(path*".tmp",path; force=true)
end

function gate(c; runtime)
    core = dirname(dirname(pathof(QCLNEGF)))
    readchomp(`git -C $core rev-parse HEAD`) == EXPECTED_HEAD || error("Unexpected Core commit")
    readchomp(`git -C $core rev-parse $("HEAD^{tree}")`) == EXPECTED_TREE || error("Unexpected Core tree")
    isempty(readchomp(`git -C $core status --porcelain --untracked-files=no`)) || error("Tracked Core files changed")
    manifest = joinpath(dirname(Base.active_project()),"Manifest.toml")
    sha(manifest) == EXPECTED_MANIFEST || error("Manifest differs")
    VERSION == v"1.13.4" || error("Unexpected Julia version")
    c["voltage_mV"] in (52.0,54.0,56.0) || error("Outside planned Fath voltage")
    c["mode"] in ("fixed","poisson") || error("Invalid electronic/Hartree mode")
    BLAS.set_num_threads(1)
    if runtime
        Threads.nthreads(:default)==c["workers"] && BLAS.get_num_threads()==1 ||
            error("Thread count differs from launch policy")
        group = only(filter(x->startswith(x,"0::"),readlines("/proc/self/cgroup")))
        cg = joinpath("/sys/fs/cgroup",lstrip(split(group,':';limit=3)[3],'/'))
        for (name,value) in (("memory.max",c["memory_max_bytes"]),("memory.swap.max",0),
                ("memory.high",c["memory_high_bytes"]))
            strip(read(joinpath(cg,name),String)) == string(value) || error("OS resource invariant: "*name)
        end
        quota, period = split(strip(read(joinpath(cg,"cpu.max"),String)))
        parse(Int,quota) == parse(Int,period)*c["workers"] || error("OS CPU quota mismatch")
    end
    return Dict{String,Any}("core_path"=>core,"core_commit"=>EXPECTED_HEAD,"core_tree"=>EXPECTED_TREE,
        "manifest_sha256"=>sha(manifest),"manifest_path"=>manifest,"driver_sha256"=>sha(@__FILE__),
        "julia_version"=>string(VERSION))
end

function policies(c, out)
    algorithms = AlgorithmOptions(
        kernel_build=:direct, embedding=:finite_chain, embedding_periods=c["embedding_periods"],
        mixing=Symbol(c["mixing"]), energy_shift=:sparse_plan, hilbert=:product_integration,
        elastic_retarded=:direct_green, occupation_normalization=:paired_convex,
        anderson_history_depth=get(c,"anderson_history_depth",5),
        anderson_regularization=get(c,"anderson_regularization",1e-12),
        anderson_damping=get(c,"anderson_damping",1.0),
    )
    po = ProductionOptions(algorithms=algorithms, worker_count=c["workers"], hilbert_columns=1,
        parallel_backend=:threads, verify_fft_roundoff=true, phase_timing=true,
        memory_budget_bytes=c["memory_max_bytes"]-c["reserve_bytes"],
        checkpoint_every_scba=0, checkpoint_every_outer=0, progress_every_scba=1,
        physics_markers=SCBAPhysicsMarkerPolicy(cadence=c["marker_cadence"],max_spectral_blocks=64),
        checkpoint_request=req->req.stage===:scba,
        event_sink=out===nothing ? nothing :
            event->open(io->println(io,repr(event)),joinpath(out,"phases.log"),"a"))
    n = NumericalParameters(N_z=c["Nz"],N_b=c["Nb"],P_basis=c["P_basis"],
        E_min=c["E_min_meV"]*u"meV",E_max=c["E_max_meV"]*u"meV",N_E=c["NE"],
        M_E=c["trust_margin_meV"]*u"meV",k_max=c["k_max_nm_inverse"]*u"nm^-1",N_k=c["Nk"],
        N_φ=c["Nphi"],qz_max=c["qz_max_nm_inverse"]*u"nm^-1",N_qz=c["Nqz"],
        η_seed=c["seed_eta_meV"]*u"meV")
    n.M_E ≥ (c["voltage_mV"]*c["embedding_periods"]+36.7)*u"meV" ||
        error("Trust margin does not cover four bias shifts and one LO shift")
    so = SolverOptions(α_Σ=c["alpha_sigma"],α_P=get(c,"alpha_poisson",0.2),
        max_scba=c["max_scba"],max_poisson=c["max_poisson"],
        convergence=ConvergencePolicy(stagnation_window=0,stagnation_relative_improvement=0.0,
            minimum_scba_iterations=2,required_consecutive_scba_passes=3))
    return algorithms,po,n,so
end

function device(d)
    d["identity"]=="fathololoumi-2012-cbo149-reconstruction-v1" || error("Unsupported device")
    d["enabled_scattering"] == string.(CHANNELS) || error("Five required local mechanisms")
    d["electron_electron"]=="none" && d["photon_field"]=="dark" || error("Fath case is dark, with EE off")
    d["CBO_meV"]==149.0 && d["lattice_temperature_K"]==d["LO_temperature_K"]==10.0 ||
        error("This campaign is the 149 meV / 10 K reconstruction")
    layers = Layer[]
    for (i,(kind,thickness)) in enumerate(zip(d["material_order"],d["thickness_nm"]))
        barrier = kind == "AlGaAs"
        mass = barrier ? d["barrier_mass_over_me"] : d["well_mass_over_me"]
        push!(layers, Layer(d=thickness*u"nm",material=Symbol(kind),
            x_Al=barrier ? d["barrier_x_Al"] : 0.0,Eᶜ=(barrier ? d["CBO_meV"] : 0.0)*u"meV",
            mᶻᵣ=mass,m_parallelᵣ=mass,εᵣ=d[barrier ? "barrier_permittivity" : "well_permittivity"],
            doped=(i==d["doped_segment_index"])))
    end
    isapprox(sum(d["thickness_nm"]),d["period_nm"]; rtol=1e-14) || error("Period thickness")
    bounds=cumsum([0.0;d["thickness_nm"]])
    si=d["doped_segment_index"]
    isapprox(bounds[si:si+1], d["donor_interval_nm"]; rtol=1e-14) || error("Donor placement")
    interfaces = [bounds[i] for i in eachindex(layers) if when_jump(layers,i)]
    isapprox(interfaces,d["interface_positions_nm"]; rtol=1e-14) || error("IFR positions")
    return PhysicalParameters(
        layers,d["sheet_donors_m_minus_2"]*u"m^-2",d["ionized_fraction"],0.0u"V/m",
        d["z_reference_nm"]*u"nm",d["energy_reference_eV"]*u"eV",
        d["lattice_temperature_K"]*u"K",d["LO_temperature_K"]*u"K",
        d["epsilon_static"],d["epsilon_optical"],d["LO_energy_meV"]*u"meV",
        d["q_impurity_nm_inverse"]*u"nm^-1",d["q_LO_nm_inverse"]*u"nm^-1",
        d["IFR_height_nm"]*u"nm",d["IFR_correlation_length_nm"]*u"nm",
        d["acoustic_deformation_eV"]*u"eV",d["mass_density_kg_m3"]*u"kg/m^3",
        d["sound_speed_m_s"]*u"m/s",d["alloy_disorder_eV"]*u"eV",d["alloy_volume_m3"]*u"m^3",
        d["spin_degeneracy"],d["interface_positions_nm"].*u"nm")
end
when_jump(layers,i) = layers[mod1(i-1,length(layers))].Eᶜ != layers[i].Eᶜ

function preflight(c, d, n, po)
    scales = ScaleSystem()
    p = device(d)
    grids = build_grids(p,n,scales)
    profiles = build_profiles(p,n,scales,grids)
    estimated = estimate_production_memory(n,5;dense_mechanism_count=5,
        options=po,worker_capacity=c["workers"],energy_nodes=grids.ε)
    estimated.peak_bytes <= po.memory_budget_bytes || error("Estimated RAM plus 3 GiB reserve exceeds cap")
    counts = [count(==(i),profiles.layer_index) for i in eachindex(p.layers)]
    Nbar = N._scaled_physics(p,scales).Nᴰ²ᴰ
    isapprox(dot(grids.wˣ,profiles.Nᴰ),Nbar; rtol=1e-13) || error("Integrated donors disagree")
    return p,scales,Dict("estimated_peak_bytes"=>estimated.peak_bytes,"planned_budget_bytes"=>po.memory_budget_bytes,
        "field_bytes"=>16*n.N_E*n.N_k*n.N_b^2,"spatial_layer_cell_counts"=>counts,
        "discrete_doped_thickness_nm"=>sum(grids.wˣ[i] for i in findall(>(0),profiles.Nᴰ))*scales.L₀_m*1e9,
        "integrated_donor_sheet_m_minus_2"=>Nbar/scales.L₀_m^2,
        "trust_energy_bounds_meV"=>[1000*scales.E₀_eV*f(grids.ε[grids.trusted_energy]) for f in (first,last)])
end

function write_complex(parent,name,array)
    parent[name*"_real"] = real.(array)
    parent[name*"_imag"] = imag.(array)
end

function save_model(path,p,c,digest_device)
    g,b,x=p.grids,p.basis,p.profiles
    fingerprints=Dict("device_sha256"=>digest_device,"energy"=>digest(g.ε),"momentum"=>digest(g.κ),
        "energy_weights"=>digest(g.wᴱ),"k_weights"=>digest(g.wᵏ),"basis"=>digest(b.Φ),
        "H_zero"=>digest(b.H₀),"T_plus"=>digest(b.T₊),"T_minus"=>digest(b.T₋),
        "conduction"=>digest(x.Eᶜ),"layer_index"=>digest(x.layer_index),"donor"=>digest(x.Nᴰ),
        "case_voltage_mV"=>string(c["voltage_mV"]),
        "per_mechanism_kernel_sha256"=>Dict(string(name)=>digest(p.kernels.K[name]) for name in CHANNELS))
    h5open(path,"w") do f
        f["schema"]="fath-cbo149-model-v1"
        f["fingerprints_toml"]=sprint(io->TOML.print(io,fingerprints;sorted=true))
        f["energy_dimensionless"]=g.ε; f["weight_energy"]=g.wᴱ
        f["k_dimensionless"]=g.κ; f["weight_k"]=g.wᵏ
        f["position_dimensionless"]=g.x; f["weight_position"]=g.wˣ
        f["trusted_energy"]=UInt8.(g.trusted_energy)
        f["layer_index"]=x.layer_index; f["E_conduction_dimensionless"]=x.Eᶜ
        f["donor_dimensionless"]=x.Nᴰ; f["mass_axial"]=x.mᶻᵣ; f["mass_lateral"]=x.m_parallelᵣ
        f["alloy_fraction"]=x.x_Al; f["permittivity"]=x.εᵣ
        for (name,field) in (("Phi",b.Φ),("H0",b.H₀),("Tplus",b.T₊),("Tminus",b.T₋))
            write_complex(f,name,field)
        end
    end
    return fingerprints
end

function save_state(path,p,r,U,model_sha,stop)
    h5open(path*".tmp","w") do f
        f["schema"]="fath-cbo149-aligned-state-v1"
        f["model_identity"]=model_sha; f["hartree"]=U
        f["status"]=stop; f["converged"]=r.converged
        f["restart_contract_toml"]=sprint(io->TOML.print(io,r.restart_contract;sorted=true))
        g=HDF5.create_group(f,"green")
        for (name,field) in (("GR",r.green.Gᴿ),("GL",r.green.Gˡ),("GG",r.green.Gᵍ),("A",r.green.A))
            write_complex(g,name,field)
        end
        g["condition_number"]=r.green.condition_number
        g["dyson_scale"]=r.green.dyson_scale
        families=copy(r.scattering)
        merge!(families,Dict(:embedding=>r.embedding,:embedding_plus=>r.embedding_plus,
            :embedding_minus=>r.embedding_minus))
        se=HDF5.create_group(f,"selfenergy")
        for (name,family) in sort(collect(families);by=first)
            sub=HDF5.create_group(se,string(name))
            for (component,field) in (("R",family.Σᴿ),("L",family.Σˡ),("G",family.Σᵍ))
                write_complex(sub,component,field)
            end
        end
    end
    mv(path*".tmp",path)
end

function restore_state(attempt,p,model_sha,U)
    prior=TOML.parsefile(joinpath(attempt,"summary.toml"))
    statepath=joinpath(attempt,"state.h5")
    prior["model_identity"]==model_sha || error("Warm checkpoint model mismatch before field read")
    sha(statepath)==prior["state_sha256"] || error("Warm checkpoint hash mismatch")
    shape=(p.numerical.N_E,p.numerical.N_k,p.numerical.N_b,p.numerical.N_b)
    return h5open(statepath,"r") do f
        read(f["schema"])=="fath-cbo149-aligned-state-v1" || error("Warm checkpoint schema")
        read(f["model_identity"])==model_sha || error("Warm checkpoint identity")
        isequal(read(f["hartree"]),U) || error("Warm checkpoint Hartree mismatch")
        function readcomplex(group,name)
            size(group[name*"_real"])==size(group[name*"_imag"])==shape || error("Warm field shape")
            out=complex.(read(group[name*"_real"]),read(group[name*"_imag"]))
            all(isfinite,out) || error("Warm field non-finite")
            out
        end
        g=f["green"]
        green=GreenState((readcomplex(g,name) for name in ("GR","GL","GG","A"))...,
            read(g["condition_number"]),read(g["dyson_scale"]))
        family(name)=SelfEnergyFamily((readcomplex(f["selfenergy/"*string(name)],tag) for tag in ("R","L","G"))...)
        return SCBAResult(green,Dict(name=>family(name) for name in CHANNELS),family(:embedding),
            family(:embedding_plus),family(:embedding_minus),SCBAIteration[],false,:warm_initial_guess,
            :unresolved,TOML.parse(read(f["restart_contract_toml"])))
    end
end

function terminal_observables(p,r,U)
    g=r.green
    J0=ustrip(u"A/m^2",p.scales.J₀)
    Iplus=J0*N._production_boundary_flux_bar(p,r.embedding_plus,g)
    Iminus=J0*N._production_boundary_flux_bar(p,r.embedding_minus,g)
    Hgrid=build_bdd_hamiltonian(p.profiles,p.grids,p.scales)
    Pbar=N._sheet_density_matrix_bar(p,g.Gˡ)
    density_projected=p.basis.Φ*(im.*Pbar)*p.basis.Φ'
    z_nm=1e9*p.scales.L₀_m.*p.grids.x
    bonds=[J0*2real(Hgrid[i,i+1]*density_projected[i+1,i]) for i in 1:length(z_nm)-1]
    collisions=Dict(name=>N._channel_collision_marker(p,g,name,:mixed,r.scattering[name])
        for name in CHANNELS)
    plus=N._channel_collision_marker(p,g,:embedding_plus,:mixed,r.embedding_plus)
    minus=N._channel_collision_marker(p,g,:embedding_minus,:mixed,r.embedding_minus)
    particle=sum(x.particle_signed for x in values(collisions))+plus.particle_signed+minus.particle_signed
    particle_scale=sum(x.particle_absolute for x in values(collisions))+plus.particle_absolute+minus.particle_absolute
    power_unit=p.scales.E₀_J*p.scales.E₀_eV/(ustrip(u"eV*s",CODATA.ħₑᵥ)*p.scales.L₀_m^2)
    Psc=sum(x.energy_signed for x in values(collisions))*power_unit
    Pfield=Iplus*ustrip(u"V",p.physical.F_bias*period_length(p.physical))
    power_scale=sum(abs(x.energy_signed) for x in values(collisions))*power_unit+abs(Pfield)
    return Dict(
        "J_plus_out_A_cm2"=>Iplus/1e4,"J_minus_out_A_cm2"=>Iminus/1e4,
        "sum_boundary_J_A_cm2"=>(Iplus+Iminus)/1e4,
        "boundary_continuity_relative"=>abs(Iplus+Iminus)/max(abs(Iplus),abs(Iminus),1e-12*J0),
        "bond_J_A_cm2"=>bonds./1e4,"bond_J_average_A_cm2"=>sum(bonds)/length(bonds)/1e4,
        "bond_J_min_A_cm2"=>minimum(bonds)/1e4,"bond_J_max_A_cm2"=>maximum(bonds)/1e4,
        "bond_midpoint_nm"=>(z_nm[1:end-1].+z_nm[2:end])./2,
        "sheet_density_m_minus_2"=>showval(Pbar./p.scales.L₀_m^2),
        "sheet_trace_m_minus_2"=>real(tr(Pbar))/p.scales.L₀_m^2,
        "mixed_collisions"=>showval(collisions),"signed_particle_relative"=>abs(particle)/(particle_scale+SQ_FLOOR),
        "mixed_Psc_W_m2"=>Psc,"Pfield_W_m2"=>Pfield,
        "mixed_power_balance_relative"=>abs(Psc+Pfield)/(power_scale+SQ_FLOOR),
        "Hartree_energy_meV"=>1000*p.scales.E₀_eV.*U)
end

struct AlignedStop <: Exception
    state::SCBAResult
end

const ROW_FIELDS=[f for f in fieldnames(SCBAIteration) if fieldtype(SCBAIteration,f)<:Real]
row_values(row)=Dict(string(f)=>getfield(row,f) for f in ROW_FIELDS)

function write_row(io,row,so,out,outer=0)
    assessment=N.scba_convergence_assessment(row,so.tolerances,so.convergence)
    values=(outer,[getfield(row,f) for f in ROW_FIELDS]...,
        assessment.passed,assessment.limiting_metric,assessment.limiting_ratio)
    println(io,join(string.(values),','))
    flush(io)
    if row.physical_markers!==nothing
        write_toml(joinpath(out,"marker-$(outer)-$(lpad(row.ν,4,'0')).toml"),showval(row.physical_markers))
    end
    if row.ν==1 || row.ν%8==0
        println("SCBA outer=",outer," row=",row.ν," J(A/cm2)=",row.J/1e4,
            " rSigma=",row.r_Σ," rK=",row.r_K," rLambda=",row.r_λ," rPSD=",row.r_PSD)
        flush(stdout)
    end
end

function accepted_seed_guard(c)
    if c["mode"]=="poisson" || c["voltage_mV"]!=54.0 || get(c,"refinement_of_central",false)
        prior=TOML.parsefile(joinpath(c["accepted_central_attempt"],"summary.toml"))
        prior["voltage_mV"]==54.0 && prior["inner_strictly_converged"]===true ||
            error("Central fixed-Hartree admission is still pending")
    end
end

function run(c,d,out,dfile; runtime=true)
    identity=gate(c; runtime)
    runtime && accepted_seed_guard(c)
    algorithms,po,n,so=policies(c,out)
    physical,scales,estimates=preflight(c,d,n,po)
    if !runtime
        TOML.print(stdout,estimates; sorted=true)
        return
    end
    merge!(identity,estimates)
    identity["device_sha256"]=sha(dfile)
    identity["case_sha256"]=sha(joinpath(out,"input.toml"))
    identity["algorithm"]=showval(algorithms)
    identity["strict_thresholds"]=showval(so.tolerances)
    write_toml(joinpath(out,"identity.toml"),identity)
    summary=Dict{String,Any}("execution"=>"started","scientific_acceptance"=>false,
        "mode"=>c["mode"],"voltage_mV"=>c["voltage_mV"],"device_sha256"=>sha(dfile),
        "process_start_epoch"=>RUN_STARTED)
    try
        models=PhysicalModelOptions(screening=:fixed,dispersion=:parabolic,
            electron_electron=ElectronElectronOptions(mode=:none),lo_population=:thermal)
        built=build_configured_scattering_problem(; physical,numerical=n,scales,
            scattering=ScatteringOptions(LO=true,acoustic=true,impurity=true,IFR=true,alloy=true),
            algorithms,kernel_options=ProductionKernelOptions(),physical_models=models)
        p0=built.problem
        p=retarget_problem(p0;V_period=c["voltage_mV"]*u"mV",energy_shift=:sparse_plan)
        Set(p.kernels.enabled)==Set(CHANNELS) && p.models.electron_electron.mode===:none ||
            error("Unexpected scattering model")
        p.basis===p0.basis && p.kernels.K===p0.kernels.K || error("Bias changed basis/kernel")
        physical_args=p.physical
        voltage=ustrip(u"mV",physical_args.F_bias*period_length(physical_args))
        isapprox(voltage,c["voltage_mV"];rtol=1e-13) || error("Bias units differ")
        U=zeros(n.N_z)
        modelpath=joinpath(out,"model.h5")
        fingerprints=save_model(modelpath,p,c,sha(dfile))
        model_sha=sha(modelpath)
        model_identity=bytes2hex(sha256(sprint(io->TOML.print(io,fingerprints;sorted=true))))
        summary["model_sha256"]=model_sha
        summary["model_identity"]=model_identity
        resolved=Dict{String,Any}(
            "voltage_mV"=>voltage,"field_kV_cm"=>ustrip(u"kV/cm",physical_args.F_bias),
            "period_nm"=>ustrip(u"nm",period_length(physical_args)),
            "q_impurity_nm_inverse"=>ustrip(u"nm^-1",physical_args.q_s),
            "q_LO_nm_inverse"=>ustrip(u"nm^-1",physical_args.qᴸᴼ_s),
            "scattering_channels"=>string.(p.kernels.enabled),"electron_electron"=>"none","dark"=>true,
            "spectral_window"=>showval(QCLNEGF.QCLReferenceOperators.spectral_window_diagnostic(p,project_hamiltonians(p,U))),
            "basis_sha256"=>fingerprints["basis"])
        write_toml(joinpath(out,"resolved.toml"),resolved)
        cache=build_production_cache(p;options=po)
        initial=haskey(c,"warm_attempt") ? restore_state(c["warm_attempt"],p,model_identity,U) : nothing
        elapsed_limit=parse(Float64,ENV["TRANSPORT_SOFT_SECONDS"])
        stop="solver_return"
        result=open(joinpath(out,"history.csv"),"w") do io
            println(io,join(["outer";string.(ROW_FIELDS);"strict_row";"limiting_metric";"limiting_ratio"],','))
            flush(io)
            if c["mode"]=="fixed"
                try
                    solve_scba_production(p,U;options=so,production_options=po,cache,
                        initial,consume_initial=initial!==nothing,
                        history_observer=row->write_row(io,row,so,out),
                        iteration_callback=state->begin
                            time()-RUN_STARTED >= elapsed_limit && throw(AlignedStop(state))
                        end)
                catch ex
                    ex isa AlignedStop || rethrow()
                    stop="soft_time_budget"
                    ex.state
                end
            else
                solve_production(p;options=so,production_options=po,cache,initial_Uᴴ=U,
                    initial_scba=initial,consume_initial=initial!==nothing,
                    history_observer=(which,μ,row,problem)->
                        which===:scba ? write_row(io,row,so,out,μ) :
                        write_toml(joinpath(out,"poisson-$μ.toml"),showval(row)))
            end
        end
        scba=result isa NEGFSolution ? result.scba : result
        result isa NEGFSolution && (U=result.Uᴴ)
        if !isempty(scba.history)
            row=last(scba.history)
            summary["last_row"]=row_values(row)
            summary["fresh_maps_completed"]=length(scba.history)
            summary["last_assessment"]=showval(N.scba_convergence_assessment(row,so.tolerances,so.convergence))
            if row.physical_markers!==nothing
                write_toml(joinpath(out,"terminal-markers.toml"),showval(row.physical_markers))
            end
            if row.witness!==nothing
                write_toml(joinpath(out,"terminal-witness.toml"),showval(row.witness))
            end
        end
        summary["execution"]="complete"
        summary["status"]=stop=="solver_return" ? string(result.status) : stop
        summary["quality"]=string(scba.quality)
        summary["inner_strictly_converged"]=scba.converged
        summary["poisson_scientifically_accepted"]=result isa NEGFSolution && result.converged && result.report.passed
        summary["scientific_acceptance"]=summary["poisson_scientifically_accepted"]
        if result isa NEGFSolution
            write_toml(joinpath(out,"final-validation.toml"),showval(result.report))
        end
        write_toml(joinpath(out,"summary.toml"),summary)
        terminal=terminal_observables(p,scba,U)
        write_toml(joinpath(out,"terminal-observables.toml"),terminal)
        summary["terminal_current_plus_A_cm2"]=terminal["J_plus_out_A_cm2"]
        summary["terminal_bond_mean_A_cm2"]=terminal["bond_J_average_A_cm2"]
        summary["terminal_boundary_continuity_relative"]=terminal["boundary_continuity_relative"]
        if scba.quality!==:invalid && scba.restart_contract!==nothing && !isempty(scba.history)
            path=joinpath(out,"state.h5")
            save_state(path,p,scba,U,model_identity,summary["status"])
            summary["state_sha256"]=sha(path)
        end
    catch ex
        summary["execution"]="error"
        summary["error"]=sprint(showerror,ex,catch_backtrace())
        rethrow()
    finally
        summary["elapsed_seconds"]=time()-RUN_STARTED
        write_toml(joinpath(out,"summary.toml"),summary)
    end
end

if abspath(PROGRAM_FILE)==(@__FILE__)
    if length(ARGS)==2 && ARGS[1]=="--plan"
        input=abspath(ARGS[2])
        dfile=joinpath(dirname(input),"device.toml")
        run(TOML.parsefile(input),TOML.parsefile(dfile),nothing,dfile;runtime=false)
    else
        length(ARGS)==2 || error("Usage: run.jl --plan INPUT or run.jl INPUT OUT")
        input=abspath(ARGS[1])
        out=abspath(ARGS[2])
        dfile=joinpath(dirname(input),"device.toml")
        run(TOML.parsefile(input),TOML.parsefile(dfile),out,dfile)
    end
end
