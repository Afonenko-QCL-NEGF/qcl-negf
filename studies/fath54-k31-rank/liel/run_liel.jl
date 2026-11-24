using LinearAlgebra
using QCLNEGFRunner
using SHA
using Unitful

const Runner = QCLNEGFRunner
const WELL_NM = ((5.2,15.5),(17.2,27.95),(31.55,40.35),(44.30,61.50))
const PERIOD_NM = 61.50
const TARGET_SHEET_PER_CM2 = 5.16e10

file_sha(path) = bytes2hex(open(sha256,path))

function json_line(io, record)
    Runner._light_json(io, record)
    println(io)
    flush(io)
end

function well_masks(z_nm)
    return [findall(z->a<=z<b,z_nm) for (a,b) in WELL_NM]
end

function state_diagnostics(solution)
    p = solution.problem
    scales, grids = p.scales, p.grids
    z_nm = grids.x .* (1e9 * scales.L₀_m)
    wells = well_masks(z_nm)
    h = Runner.project_hamiltonians(p,solution.Uᴴ)
    decomposition = eigen(Hermitian(Matrix(view(h,1,:,:))))
    transform = decomposition.vectors
    wavefields = p.basis.χ * transform
    measure = grids.wˣ
    energies_meV = decomposition.values .* (1e3 * scales.E₀_eV) .+
        ustrip(u"meV",p.physical.E_ref)
    sheet = solution.status==:snapshot ?
        Runner.sheet_density_matrix(p,solution.scba.green.Gˡ) :
        solution.observables[:sheet_density_matrix]
    rho = ustrip.(u"m^-2",sheet)
    populations = real.(diag(transform' * rho * transform)) .* 1e-4
    weights = [measure .* abs2.(view(wavefields,:,i)) for i in eachindex(energies_meV)]
    well_fraction = [[sum(weight[sites])/sum(weight) for sites in wells] for weight in weights]
    centroids_nm = [dot(z_nm,weight)/sum(weight) for weight in weights]

    pairs = NamedTuple[]
    for upper in eachindex(energies_meV), lower in eachindex(energies_meV)
        separation = energies_meV[upper]-energies_meV[lower]
        9.0<=separation<=18.0 || continue
        upper_left = well_fraction[upper][1]
        lower_middle = sum(well_fraction[lower][2:3])
        min(upper_left,lower_middle)>=0.35 || continue
        dipole_nm = abs(dot(view(wavefields,:,lower),
            (measure .* z_nm) .* view(wavefields,:,upper)))
        dipole_nm>0 || continue
        score = dipole_nm^2 * upper_left * lower_middle
        inversion_per_cm2 = populations[upper]-populations[lower]
        push!(pairs,(;upper,lower,separation,dipole_nm,score,inversion_per_cm2))
    end
    sort!(pairs;by=x->(-x.score,x.upper,x.lower))
    plausible = isempty(pairs) ? pairs : filter(x->x.score>=0.9*first(pairs).score,pairs)
    injectors = findall(f->f[4]>=0.5,well_fraction)
    injector = isempty(injectors) ? nothing : first(injectors)
    candidates_same_sign = !isempty(plausible) &&
        all(sign(x.inversion_per_cm2)==sign(first(plausible).inversion_per_cm2) for x in plausible)
    return (;energies_meV,populations_per_cm2=populations,well_fraction,centroids_nm,
        injector,injector_alignment_meV=isempty(pairs) || isnothing(injector) ? nothing :
            energies_meV[injector]+50.0-energies_meV[first(pairs).upper],
        pairs,plausible,candidates_same_sign)
end

function write_density(path, dens, energy_measure_meV, space_measure_nm)
    energy_meV = dens.energy_eV .* 1000
    z_nm = dens.z_m .* 1e9
    density = dens.n_per_eV_m3 .* 1e-30
    native_sheet_nm2 = dot(energy_measure_meV,density*space_measure_nm)
    binned_sheet_nm2 = 0.0
    open(path,"w") do io
        println(io,"energy_meV,z_nm,energy_weight_meV,z_weight_nm,n_per_meV_nm3")
        for a in 1:4:length(energy_meV), b in 1:2:length(z_nm)
            ei = a:min(a+3,length(energy_meV))
            zi = b:min(b+1,length(z_nm))
            we,wz = energy_measure_meV[ei],space_measure_nm[zi]
            ewidth,zwidth = sum(we),sum(wz)
            sheet = dot(we,density[ei,zi]*wz)
            println(io,join((dot(we,energy_meV[ei])/ewidth,dot(wz,z_nm[zi])/zwidth,
                ewidth,zwidth,sheet/(ewidth*zwidth)),','))
            binned_sheet_nm2 += sheet
        end
    end
    error_per_cm2 = abs(native_sheet_nm2-binned_sheet_nm2)*1e14
    error_per_cm2 <= 1e-10*TARGET_SHEET_PER_CM2 || error("density bin charge mismatch")
    spatial_density = vec(transpose(energy_measure_meV)*density)
    by_well = [dot(spatial_density[sites],space_measure_nm[sites])*1e14
        for sites in well_masks(z_nm)]
    return (;native_sheet_per_cm2=native_sheet_nm2*1e14,
        binned_sheet_per_cm2=binned_sheet_nm2*1e14,error_per_cm2,native_wells_per_cm2=by_well,
        minimum_density=minimum(density),maximum_density=maximum(density))
end

function diagnostics_record(solution,outer,snapshot_count)
    latest = isempty(solution.scba.history) ? nothing : last(solution.scba.history)
    return (;outer,snapshot_count,status=solution.status,quality=Runner.solution_quality(solution),
        converged=solution.converged,scba_status=solution.scba.status,
        scba_count=length(solution.scba.history),
        last_fresh=isnothing(latest) ? nothing :
            (;map=latest.ν,rK=latest.r_K,rSigma=latest.r_Σ,raw_lambda=latest.λ),
        physical_metrics=Runner._solution_report_metrics(solution),
        failed_criteria=solution.report.messages,
        raw_modes=state_diagnostics(solution))
end

function run_liel(reference,point,output; overrides=String[])
    ispath(output) && error("output must be a new directory")
    configuration = Runner.load_run_configuration([reference,point,overrides...])
    cfg = configuration
    cfg.execution.strategy==:manual && cfg.execution.solver_backend==:production ||
        error("explicit local production configuration required")
    !cfg.output.save_full_state && !cfg.output.intermediate_checkpoints &&
        !cfg.output.resume || error("in-memory solve required")
    !cfg.study.calculate_optical_response || error("dark transport required")
    Runner.configure_execution!(cfg)
    mkpath(output)
    open(joinpath(output,"history.jsonl"),"w") do io
        json_line(io,(;kind="configuration",reference_sha256=file_sha(reference),
            point_sha256=file_sha(point),driver_sha256=file_sha(@__FILE__),
            overrides_sha256=file_sha.(overrides),
            core=Runner._linked_package_identity(Runner.QCLNEGF),
            runner=Runner._linked_package_identity(Runner),
            runtime=Runner._runtime_toolchain_provenance()))
        configured = Runner.build_configured_problem(cfg)
        p = configured.problem
        sheet_target = ustrip(u"m^-2",p.physical.N_dop²ᴰ)*1e-4
        field_kV_cm = ustrip(u"V/m",p.physical.F_bias)*1e-5
        isapprox(sheet_target,TARGET_SHEET_PER_CM2;rtol=1e-12) &&
            isapprox(field_kV_cm,0.050/61.50e-9*1e-5;rtol=1e-12) &&
            ustrip(u"K",p.physical.Tᴸ)==77 && ustrip(u"K",p.physical.Tᴸᴼ)==77 ||
            error("wrong coordinate point")
        json_line(io,(;kind="problem",field_kV_cm,sheet_target,
            shape=(p.numerical.N_z,p.numerical.N_E,p.numerical.N_k,p.numerical.N_b),
            enabled_channels=p.kernels.enabled))
        println(stderr,"LiEL2014: local problem built")
        flush(stderr)
        function track(stage,outer,row,problem)
            if stage==:scba
                json_line(io,(;kind="scba",outer,map=row.ν,rK=row.r_K,rSigma=row.r_Σ,
                    raw_lambda=row.λ,rDyson=row.r_D,rSpectralIdentity=row.r_A,
                    rPositivity=row.r_PSD,rCausality=row.r_caus,J_A_cm2=row.J/1e4))
                if row.ν==1 || row.ν%8==0
                    println(stderr,"LiEL2014 outer ",outer," map ",row.ν,
                        " rK=",row.r_K," rSigma=",row.r_Σ)
                    flush(stderr)
                end
            else
                json_line(io,(;kind="poisson",outer,rHartree=row.r_U,rPoisson=row.r_P,
                    rContinuity=row.r_J,rDensity=row.r_n,rNeutral=row.r_neutral,
                    J_A_cm2=row.J/1e4))
            end
        end
        snapshot_count = 0
        function observe(solution)
            if solution.status==:snapshot
                snapshot_count += 1
                json_line(io,(;kind="outer_projection",
                    diagnostics_record(solution,length(solution.outer_history),snapshot_count)...))
            end
        end
        seconds_start = time_ns()
        solution = Runner.solve_production(p;options=cfg.solver,production_options=cfg.production,
            checkpoint_path=nothing,history_observer=track,state_observer=observe)
        report = diagnostics_record(solution,length(solution.outer_history),snapshot_count)
        dens = Runner.spatial_energy_density(p,solution.scba.green.Gˡ)
        energy_measure = p.grids.wᴱ .* (1e3*p.scales.E₀_eV)
        space_measure = p.grids.wˣ .* (1e9*p.scales.L₀_m)
        charge = write_density(joinpath(output,"density.csv"),dens,energy_measure,space_measure)
        sheet_check = sum(report.raw_modes.populations_per_cm2)-charge.native_sheet_per_cm2
        abs(sheet_check) <= 1e-8 * TARGET_SHEET_PER_CM2 ||
            error("coordinate and modal sheet densities disagree")
        current = ustrip(u"A/m^2",solution.observables[:electron_flow_current])/1e4
        jz = ustrip.(u"A/m^2",solution.observables[:bond_current])./1e4
        z_nm = dens.z_m .* 1e9
        centered = (z_nm[1:end-1].+z_nm[2:end])./2
        final = (;kind="final",report...,density=charge,sheet_projection_error_per_cm2=sheet_check,
            boundary_J_A_cm2=current,interior_J_A_cm2=sum(jz)/length(jz),
            max_interior_deviation_A_cm2=maximum(abs,jz.-sum(jz)/length(jz)),
            sections=(;z_nm=centered,J_A_cm2=jz),
            hartree_max_abs_meV=maximum(abs,solution.Uᴴ)*p.scales.E₀_eV*1e3,
            maxrss_bytes=Int(Sys.maxrss()),elapsed_seconds=(time_ns()-seconds_start)*1e-9)
        json_line(io,final)
        open(joinpath(output,"summary.json"),"w") do result
            json_line(result,final)
        end
    end
end

length(ARGS)>=3 || error("usage: run_liel.jl REFERENCE_CONFIG POINT_CONFIG OUTPUT_DIR [OVERRIDE...]")
run_liel(ARGS[1:3]...;overrides=ARGS[4:end])
