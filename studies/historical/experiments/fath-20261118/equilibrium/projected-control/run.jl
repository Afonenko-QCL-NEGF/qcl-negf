using LinearAlgebra, QCLNEGF, SHA, TOML, Unitful

const PROCESS_START = time()
const HERE = @__DIR__
const N = QCLNEGF.QCLNumerics
const PROJECTED_LIMIT = 552
const STOCK_LIMIT = 48
const RETARDED_SOFT_SECONDS = 1540
const CHANNELS = (:LO,:acoustic,:impurity,:IFR,:alloy,:embedding,:embedding_plus,:embedding_minus)
const ALPHA = 0.4

module Setup
include(joinpath(@__DIR__, "..", "kms.jl"))
end

sha(path) = bytes2hex(open(sha256, path))
function save_toml(path, record)
    open(path, "w") do f
        TOML.print(f, record; sorted=true)
    end
end

"""Fit the scalar chemical potential using A, grid measures and donor charge."""
function fdt_green(problem, gr, a, conditions, scales)
    energies, we, wk = problem.grids.ε, problem.grids.wᴱ, problem.grids.wᵏ
    ne, nk, nb, _ = size(a)
    weight = zeros(ne)
    for m in 1:nk, e in 1:ne, b in 1:nb
        weight[e] += we[e]*wk[m]*real(a[e,m,b,b])
    end
    weight .*= problem.physical.g_s/(2π)
    @assert all(isfinite, weight) && minimum(weight) >= -1e-12*maximum(abs,weight)
    target = N._scaled_physics(problem.physical, problem.scales).Nᴰ²ᴰ
    @assert 0 < target < sum(weight)
    kT = (1.380649e-23 / 1.602176634e-19) * 10 / problem.scales.E₀_eV
    lo, hi = first(energies)-128kT, last(energies)+128kT
    for _ in 1:75
        mid = lo+(hi-lo)/2
        f, _ = Setup.fermi_pair(energies, mid, kT)
        if dot(weight,f) < target
            lo = mid
        else
            hi = mid
        end
    end
    μ = lo+(hi-lo)/2
    f, holes = Setup.fermi_pair(energies, μ, kT)
    renormalization = abs(dot(weight,f)/target-1)
    @assert renormalization < 1e-12
    green = GreenState(gr, im.*f.*a, -im.*holes.*a, a, conditions, scales)
    return green, 1000*problem.scales.E₀_eV*μ, renormalization
end

function projected_candidate(p, g, h, cache, opts)
    local_fields = N._scattering_candidate_production(p,g,cache,opts)
    embedding, plus, minus = N._embedding_self_energy_selected(p,g,cache,opts;
                                                               scattering=local_fields,h)
    retarded = Dict(name=>family.Σᴿ for (name,family) in local_fields)
    retarded[:embedding] = embedding.Σᴿ
    retarded[:embedding_plus] = plus.Σᴿ
    retarded[:embedding_minus] = minus.Σᴿ
    return (; local_fields, embedding, plus, minus, retarded)
end

function projected_loop(p,h,cache,opts,output)
    seed,_ = N._seed_green_production(p,h,opts)
    g, μ, n_error = fdt_green(p,seed.Gᴿ,seed.A,seed.condition_number,seed.dyson_scale)
    seed = nothing
    accepted = nothing
    streak = 0
    last_r = Inf
    path = joinpath(output,"projected.csv")
    return open(path,"w") do io
        println(io,"map,rR_max_family,rR_total,limiting_R_family,mu_meV,charge_relative,phase_seconds,elapsed_seconds")
        for i in 1:PROJECTED_LIMIT
            start = time()
            if i > 1
                total = copy(accepted[:embedding])
                for name in p.kernels.enabled
                    total .+= accepted[name]
                end
                gr, kd, ds = N._retarded_green_production(p.grids.ε, h, total; η=0.0, options=opts)
                a = im.*(gr.-permutedims(conj.(gr),(1,2,4,3)))
                g, μ, n_error = fdt_green(p,gr,a,kd,ds)
            end
            candidate = projected_candidate(p,g,h,cache,opts)
            if i == 1
                last_r, total_residual, limiting = Inf, Inf, "seed"
                accepted = Dict(key=>copy(matrix) for (key,matrix) in candidate.retarded)
            else
                differences = [norm(candidate.retarded[x].-accepted[x])/(norm(candidate.retarded[x])+1e-14)
                               for x in CHANNELS]
                last_r, limiting_index = findmax(differences)
                limiting = String(CHANNELS[limiting_index])
                fresh_total = copy(candidate.retarded[:embedding])
                for name in p.kernels.enabled
                    fresh_total .+= candidate.retarded[name]
                end
                total_residual = norm(fresh_total.-total)/(norm(fresh_total)+1e-14)
                all(isfinite, (last_r,total_residual,μ)) || error("Non-finite projected map")
                streak = last_r < 1e-8 && total_residual < 1e-8 ? streak+1 : 0
            end
            println(io,join((i,last_r,total_residual,limiting,μ,n_error,time()-start,time()-PROCESS_START),','))
            flush(io)
            if i==1 || i%16==0 || streak>=3
                println("projected map ",i," rR=",last_r," rtotal=",total_residual," μ(meV)=",μ)
                flush(stdout)
            end
            reason = streak>=3 ? "retarded_three_passes" :
                     i==PROJECTED_LIMIT ? "projected_map_budget" :
                     time()-PROCESS_START >= RETARDED_SOFT_SECONDS ? "wall_reserve" : nothing
            if reason !== nothing
                initial = SCBAResult(g,candidate.local_fields,candidate.embedding,candidate.plus,
                    candidate.minus,SCBAIteration[],false,:warm_initial_guess,:unresolved,nothing)
                return initial, Dict("maps"=>i,"reason"=>reason,"rR_max_family"=>last_r,
                    "rR_total"=>total_residual,"mu_meV"=>μ,"strict_R_streak"=>streak,
                    "projected_elapsed_seconds"=>time()-PROCESS_START)
            end
            if i>1
                for (name,r) in accepted
                    fresh = candidate.retarded[name]
                    r .= (1-ALPHA).*r .+ ALPHA.*fresh
                end
            end
        end
        error("Projected loop exited without a handoff")
    end
end

function stock(p,h,cache,opts,initial,output,model_hash,handoff)
    scba = SolverOptions(; α_Σ=ALPHA, max_scba=STOCK_LIMIT, max_poisson=1,
        convergence=ConvergencePolicy(; stagnation_window=0, stagnation_relative_improvement=0.0))
    options = N.with_production_options(opts;
        physics_markers=SCBAPhysicsMarkerPolicy(cadence=16,max_spectral_blocks=32),
        progress_every_scba=1, phase_timing=true, checkpoint_request=req->req.stage === :scba)
    u = zeros(p.numerical.N_z)
    unit = ustrip(u"A/m^2",p.scales.J₀)/1e4
    run_record = Dict{String,Any}("handoff"=>handoff,"stock_alpha"=>ALPHA,
        "native_r_sum_tolerance"=>scba.tolerances.r_sum,"model_sha256"=>model_hash)
    written = Ref(false)
    save(path,result,reason) = Setup.FrozenTransport.save_state(path,p,result,u,model_hash,reason)
    primary = joinpath(output,"state.h5")
    open(joinpath(output,"stock.csv"),"w") do csv
        println(csv,"stock_map,total_fresh_maps,rSigma,rK,rLambda,lambda,rPSD,rD,rA,rCaus,rRoundoff,rJchange,rPopulation,Jplus_A_cm2,Jminus_A_cm2,Jnet_A_cm2,r_sum,strict,failed")
        record = aligned -> begin
            r = last(aligned.history)
            gate = scba_convergence_assessment(r,scba.tolerances,scba.convergence)
            jp = unit*N._production_boundary_flux_bar(p,aligned.embedding_plus,aligned.green)
            jm = unit*N._production_boundary_flux_bar(p,aligned.embedding_minus,aligned.green)
            @assert isapprox(jp,r.J/1e4; rtol=1e-13,atol=1e-15)
            spectral_sum = N._spectral_sum_residual(p,aligned.green)
            values = (r.ν,r.ν+handoff["maps"],r.r_Σ,r.r_K,r.r_λ,r.λ,r.r_PSD,
                r.r_D,r.r_A,r.r_caus,r.r_roundoff,r.r_Jchange,r.r_population,jp,jm,jp+jm,spectral_sum,
                gate.passed,join(String.(gate.failed_metrics),'|'))
            println(csv,join(values,',')); flush(csv)
            if r.ν==1 || r.ν%8==0 || gate.passed
                println("stock map ",r.ν," rΣ=",r.r_Σ," rK=",r.r_K," rλ=",r.r_λ,
                        " J±=",jp,"/",jm," r_sum=",spectral_sum," strict=",gate.passed)
                flush(stdout)
            end
            if time()-PROCESS_START>1730
                save(primary,aligned,"wall_reserve")
                written[] = true
                run_record["stock_status"] = "wall_reserve"
                run_record["stock_maps"] = r.ν
                run_record["state_sha256"] = sha(primary)
                run_record["stock_converged"] = false
                save_toml(joinpath(output,"summary.toml"),run_record)
                error("Stock time reserve reached; aligned checkpoint saved")
            end
        end
        result = try
            solve_scba_production(p,u; options=scba, production_options=options,
                cache, initial, consume_initial=true, resume_iterations=false, iteration_callback=record)
        catch
            written[] || save_toml(joinpath(output,"summary.toml"),merge(run_record,Dict("stock_status"=>"exception")))
            rethrow()
        end
        @assert !isempty(result.history)
        save(primary,result,String(result.status))
        run_record["stock_status"] = String(result.status)
        run_record["stock_maps"] = length(result.history)
        run_record["stock_converged"] = result.converged
        run_record["total_fresh_maps"] = handoff["maps"]+length(result.history)
        run_record["state_sha256"] = sha(primary)
        run_record["wall_seconds_at_save"] = time()-PROCESS_START
        run_record["r_sum_terminal"] = N._spectral_sum_residual(p,result.green)
        save_toml(joinpath(output,"summary.toml"),run_record)
    end
end

function main()
    @assert length(ARGS)==1
    output = only(ARGS)
    @assert isdir(output)
    @assert sha(joinpath(dirname(Base.active_project()),"Manifest.toml")) ==
        "da0780fbe150c0e16e9fedf3566a1971095642f14f57f32524b52f430a4adb65"
    p, opts, cache = Setup.prepare()
    @assert iszero(p.physical.F_bias)
    @assert Set(p.kernels.enabled) == Set(CHANNELS[1:5])
    @assert p.models.lo_population === :thermal && p.models.electron_electron.mode === :none
    h = project_hamiltonians(p,zeros(144))
    model_path = joinpath(output,"model.h5")
    passport = joinpath(HERE,"..","attempt01","device.toml")
    Setup.FrozenTransport.save_model(model_path,p,Dict("voltage_mV"=>0.0,"embedding_periods"=>4),sha(passport))
    model_hash = sha(model_path)
    initial,handoff = projected_loop(p,h,cache,opts,output)
    save_toml(joinpath(output,"handoff.toml"),handoff)
    GC.gc()
    stock(p,h,cache,opts,initial,output,model_hash,handoff)
end

main()
