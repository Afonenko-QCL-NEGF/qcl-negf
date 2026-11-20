using HDF5, LinearAlgebra, QCLNEGF, SHA, TOML, Unitful

const HERE = @__DIR__
const PROCESS_START = time()
const N = QCLNEGF.QCLNumerics
const SAMPLES = (48,128,256)
const LOCALS = (:LO,:acoustic,:impurity,:IFR,:alloy)
const ZERO_STATE_SHA = "2a90e8b95b6fc349087449c5b12f31eddec202a15c9b7ca41a99c4df79100c74"
const ZERO_MODEL_SHA = "0a8eca5877b4c3770fc706922a9fb8562db734f92fbbbea98d74e514cd66d77e"
const DEVICE_SHA = "4e4314af4696465084b48fc7e22cd0310c03889256f19abaa2500ee6a923d502"
const MANIFEST_SHA = "da0780fbe150c0e16e9fedf3566a1971095642f14f57f32524b52f430a4adb65"

module Setup
include(joinpath(@__DIR__,"..","kms.jl"))
end

const Transport = Setup.FrozenTransport
sha(path) = bytes2hex(open(sha256,path))
function write_toml(path, record)
    open(path,"w") do f
        TOML.print(f,record;sorted=true)
    end
end

struct PilotStop <: Exception end

function transplanted_locals(p)
    zero = joinpath(HERE,"..","projected-control","continuation","attempt01")
    state, model = joinpath(zero,"state.h5"), joinpath(zero,"model.h5")
    summary = TOML.parsefile(joinpath(zero,"summary.toml"))
    @assert sha(state) == summary["state_sha256"] == ZERO_STATE_SHA
    @assert sha(model) == summary["model_sha256"] == ZERO_MODEL_SHA
    @assert summary["stock_maps"] == 128 && !summary["stock_converged"]
    shape = (1201,4,7,7)
    field(f,key) = complex.(read(f[key*"_real"]),read(f[key*"_imag"]))
    h5open(model,"r") do f
        g,b,x = p.grids,p.basis,p.profiles
        for (key,values) in (("energy_dimensionless",g.ε),("weight_energy",g.wᴱ),
                            ("k_dimensionless",g.κ),("weight_k",g.wᵏ),
                            ("position_dimensionless",g.x),("weight_position",g.wˣ),
                            ("layer_index",x.layer_index),("donor_dimensionless",x.Nᴰ),
                            ("E_conduction_dimensionless",x.Eᶜ),
                            ("mass_axial",x.mᶻᵣ),("mass_lateral",x.m_parallelᵣ))
            @assert isequal(read(f[key]),values) key
        end
        for (key,values) in (("H0",b.H₀),("Phi",b.Φ),("Tplus",b.T₊),("Tminus",b.T₋))
            @assert isapprox(field(f,key),values;rtol=1e-13) key
        end
        fingerprints = TOML.parse(read(f["fingerprints_toml"]))
        @assert fingerprints["device_sha256"] == DEVICE_SHA
        @assert parse(Float64,fingerprints["case_voltage_mV"]) == 0.
        for name in LOCALS
            @assert Transport.digest(p.kernels.K[name]) ==
                fingerprints["per_mechanism_kernel_sha256"][String(name)]
        end
    end
    return h5open(state,"r") do f
        @assert read(f["schema"]) == "fath-cbo149-aligned-state-v1"
        @assert read(f["model_identity"]) == ZERO_MODEL_SHA
        @assert all(iszero,read(f["hartree"]))
        families = Dict{Symbol,SelfEnergyFamily}()
        for name in LOCALS
            parts = [field(f,"selfenergy/$(String(name))/$component") for component in ("R","L","G")]
            @assert all(x->size(x)==shape && all(isfinite,x), parts)
            families[name] = SelfEnergyFamily(parts...)
        end
        families
    end
end

function build_seed(p,cache,opts,u,locals)
    # finite_chain only uses size(dummy.Gᴿ), and none of these placeholder values.
    z = zeros(ComplexF64,1201,4,7,7)
    dummy = GreenState(z,z,z,z,ones(1201,4),ones(1201,4))
    h = project_hamiltonians(p,u)
    plan = N._cavity_production_plan(p,h,opts)
    embedding, plus, minus = N._embedding_self_energy_selected(p,dummy,cache,opts;
        scattering=locals,h,cavity_plan=plan)
    green, raw_lambda, _ = N._current_green_production(p,h,locals,embedding,opts)
    initial = SCBAResult(green,locals,embedding,plus,minus,SCBAIteration[],false,
        :warm_initial_guess,:unresolved)
    return initial,raw_lambda
end

function main()
    output = only(ARGS)
    @assert sha(joinpath(dirname(Base.active_project()),"Manifest.toml")) == MANIFEST_SHA
    p0, opts, cache0 = Setup.prepare()
    p = retarget_problem(p0; V_period=54u"mV",energy_shift=:sparse_plan)
    @assert Set(p.kernels.enabled)==Set(LOCALS)
    @assert p.models.electron_electron.mode===:none && p.models.lo_population===:thermal
    @assert p.physical.Tᴸ==p.physical.Tᴸᴼ==10u"K"
    @assert isapprox(p.physical.F_bias*sum(x.d for x in p.physical.layers),54u"mV")
    @assert p.W₊ᴱᵖ !== p0.W₊ᴱᵖ && p.W₋ᴱᵖ !== p0.W₋ᴱᵖ
    @assert p.W₊ᴸᴼ === p0.W₊ᴸᴼ && p.W₋ᴸᴼ === p0.W₋ᴸᴼ
    @assert p.basis === p0.basis && p.kernels.K === p0.kernels.K
    cache0 = nothing
    GC.gc()
    cache = build_production_cache(p;options=opts)
    scba = SolverOptions(; α_Σ=.4,max_scba=256,max_poisson=1,
        convergence=ConvergencePolicy(; stagnation_window=0, stagnation_relative_improvement=0.0))
    options = N.with_production_options(opts;
        physics_markers=SCBAPhysicsMarkerPolicy(cadence=16,max_spectral_blocks=32),
        progress_every_scba=1,phase_timing=true,checkpoint_request=req->req.stage===:scba)
    cold_root = joinpath(HERE,"..","..","method","alpha-extended","attempt01")
    cold_identity = TOML.parsefile(joinpath(cold_root,"identity.toml"))
    @assert cold_identity["potential_drop_mV"] == 54 && cold_identity["alpha"] == .4
    @assert cold_identity["manifest_sha256"] == MANIFEST_SHA
    @assert cold_identity["model_source_sha256"] == DEVICE_SHA
    @assert cold_identity["shape_julia"] == [1201,4,7,7] && cold_identity["spatial_nodes"] == 144
    @assert cold_identity["tolerances"] == Dict(String(x)=>getfield(scba.tolerances,x) for x in fieldnames(SolverTolerances))
    cold = Dict(i=>TOML.parsefile(joinpath(cold_root,"linear","rows",lpad(i,3,'0')*".toml")) for i in SAMPLES)
    model_path = joinpath(output,"model.h5")
    Transport.save_model(model_path,p,Dict("voltage_mV"=>54.0),DEVICE_SHA)
    model_sha = sha(model_path)
    u = zeros(144)
    seed_start = time()
    locals = transplanted_locals(p)
    initial, seed_lambda = build_seed(p,cache,opts,u,locals)
    seed_seconds = time()-seed_start
    unit = ustrip(u"A/m^2",p.scales.J₀)/10000
    write_toml(joinpath(output,"seed.toml"),Dict("source_state_sha256"=>ZERO_STATE_SHA,
        "source_model_sha256"=>ZERO_MODEL_SHA,"target_model_sha256"=>model_sha,
        "source_cold_maps"=>48,"source_projected_maps"=>1450,"source_unforced_from_projected_maps"=>176,
        "rebuild_seconds"=>seed_seconds,"native_raw_lambda"=>seed_lambda,"bias_mV"=>54,
        "seed_Jplus_A_cm2"=>unit*N._production_boundary_flux_bar(p,initial.embedding_plus,initial.green),
        "seed_Jminus_A_cm2"=>unit*N._production_boundary_flux_bar(p,initial.embedding_minus,initial.green),
        "seed_r_sum"=>N._spectral_sum_residual(p,initial.green),
        "target_history_reused"=>false,"target_FDT_projection"=>false))
    println("Target operating point and initial state built; native α=.4 only")
    flush(stdout)
    solving = time()
    terminal = joinpath(output,"state.h5")
    function summarize(result,reason)
        Transport.save_state(terminal,p,result,u,model_sha,reason)
        r = last(result.history)
        write_toml(joinpath(output,"summary.toml"),Dict("reason"=>reason,"state_sha256"=>sha(terminal),
            "model_sha256"=>model_sha,"maps"=>r.ν,"converged"=>result.converged,
            "stock_status"=>String(result.status),"solver_seconds"=>time()-solving,
            "runtime_seconds_before_exit"=>time()-PROCESS_START,
            "r_sum"=>N._spectral_sum_residual(p,result.green)))
    end
    open(joinpath(output,"rows.csv"),"w") do csv
        println(csv,"map,rSigma,rK,rLambda,rPSD,rJchange,rPopulation,rD,rA,rCaus,rRoundoff,Jplus_A_cm2,Jminus_A_cm2,Jnet_A_cm2,r_sum,strict,failed")
        record = function(aligned)
            r = last(aligned.history)
            gate = scba_convergence_assessment(r,scba.tolerances,scba.convergence)
            jp = unit*N._production_boundary_flux_bar(p,aligned.embedding_plus,aligned.green)
            jm = unit*N._production_boundary_flux_bar(p,aligned.embedding_minus,aligned.green)
            @assert isapprox(jp,r.J/1e4; rtol=1e-13,atol=1e-12)
            sum_res = N._spectral_sum_residual(p,aligned.green)
            values = (r.ν,r.r_Σ,r.r_K,r.r_λ,r.r_PSD,r.r_Jchange,r.r_population,r.r_D,
                r.r_A,r.r_caus,r.r_roundoff,jp,jm,jp+jm,sum_res,gate.passed,join(String.(gate.failed_metrics),'|'))
            println(csv,join(values,',')); flush(csv)
            if r.ν in SAMPLES
                ref = cold[r.ν]
                trial = max(r.r_Σ,r.r_K,r.r_λ)
                control = max(ref["r_Σ"],ref["r_K"],ref["r_λ"])
                println("Matched map $(r.ν): target max=$trial, cold max=$control")
                flush(stdout)
                if r.ν < 256 && !(trial < control)
                    summarize(aligned,"no_matched_improvement")
                    throw(PilotStop())
                end
            end
            if time()-PROCESS_START>510
                summarize(aligned,"wall_reserve")
                throw(PilotStop())
            end
        end
        try
            result = solve_scba_production(p,u;options=scba,production_options=options,cache,initial,
                consume_initial=true,resume_iterations=false,iteration_callback=record)
            summarize(result,String(result.status))
        catch ex
            ex isa PilotStop || rethrow()
        end
    end
end

main()
