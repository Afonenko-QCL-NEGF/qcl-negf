using HDF5, LinearAlgebra, QCLNEGF, SHA, Statistics, TOML, Unitful

const PROCESS_START = time()
const HERE = @__DIR__
const N = QCLNEGF.QCLNumerics
const PROJECTED_LIMIT = 1200
const STOCK_LIMIT = 128
const RETARDED_SOFT_SECONDS = 1700
const STOCK_SOFT_SECONDS = 2040
const RETARDED_TARGET = 1e-10
const CHANNELS = (:LO,:acoustic,:impurity,:IFR,:alloy,:embedding,:embedding_plus,:embedding_minus)
const ALPHA = 0.4

module Setup
include(joinpath(@__DIR__, "..", "..", "kms.jl"))
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

function source_state(p, output)
    parent = joinpath(HERE,"..","attempt01")
    summary = TOML.parsefile(joinpath(parent,"summary.toml"))
    @assert summary["stock_maps"] == 48 && summary["stock_status"] == "max_iterations"
    path, model = joinpath(parent,"state.h5"), joinpath(parent,"model.h5")
    @assert sha(path) == summary["state_sha256"] ==
        "d6df731827b57e7b48565069080494a6363a3abd41aad885eb096ba053bdce15"
    @assert sha(model) == summary["model_sha256"] ==
        "0a8eca5877b4c3770fc706922a9fb8562db734f92fbbbea98d74e514cd66d77e"
    complex_field(f,name) = complex.(read(f[name*"_real"]),read(f[name*"_imag"]))
    h5open(model,"r") do f
        @assert isequal(read(f["energy_dimensionless"]),p.grids.ε)
        @assert isequal(read(f["weight_energy"]),p.grids.wᴱ)
        @assert isequal(read(f["weight_k"]),p.grids.wᵏ)
        @assert isequal(read(f["k_dimensionless"]),p.grids.κ)
        @assert isapprox(complex_field(f,"H0"),p.basis.H₀;rtol=1e-13)
        @assert isapprox(complex_field(f,"Phi"),p.basis.Φ;rtol=1e-13)
        @assert isapprox(complex_field(f,"Tplus"),p.basis.T₊;rtol=1e-13)
        fprint = TOML.parse(read(f["fingerprints_toml"]))
        for name in p.kernels.enabled
            @assert Setup.FrozenTransport.digest(p.kernels.K[name]) ==
                fprint["per_mechanism_kernel_sha256"][String(name)]
        end
    end
    cp(model,joinpath(output,"model.h5"))
    archived, greendata = h5open(path,"r") do f
        @assert read(f["schema"]) == "fath-cbo149-aligned-state-v1"
        @assert read(f["model_identity"]) == summary["model_sha256"]
        @assert all(iszero,read(f["hartree"]))
        stage = Dict(name=>complex_field(f,"selfenergy/$(String(name))/R") for name in CHANNELS)
        g = (gr=complex_field(f,"green/GR"), a=complex_field(f,"green/A"))
        return stage,g
    end
    return archived, greendata, summary["model_sha256"], summary["state_sha256"]
end

function write_projected(path,p,i,g,old,candidate,record,model_hash,source_hash)
    wc = Setup.FrozenTransport.write_complex
    h5open(path*".tmp","w") do f
        f["schema"] = "fath-equilibrium-projected-aligned-v1"
        f["model_identity"] = model_hash
        f["source_stock_sha256"] = source_hash
        f["map"] = i
        f["hartree"] = zeros(p.numerical.N_z)
        f["parameters_toml"] = sprint(io->TOML.print(io,record;sorted=true))
        green = create_group(f,"green")
        for (name,field) in (("GR",g.Gᴿ),("A",g.A),("GL",g.Gˡ),("GG",g.Gᵍ))
            wc(green,name,field)
        end
        green["condition_number"] = g.condition_number
        green["dyson_scale"] = g.dyson_scale
        rested = create_group(f,"accepted_R")
        for name in CHANNELS
            wc(rested,String(name),old[name])
        end
        fresh = create_group(f,"fresh")
        families = copy(candidate.local_fields)
        families[:embedding] = candidate.embedding
        families[:embedding_plus] = candidate.plus
        families[:embedding_minus] = candidate.minus
        for name in CHANNELS
            out = create_group(fresh,String(name))
            family = families[name]
            wc(out,"R",family.Σᴿ); wc(out,"L",family.Σˡ); wc(out,"G",family.Σᵍ)
        end
    end
    mv(path*".tmp",path)
    save_toml(path*".toml",merge(record,Dict("sha256"=>sha(path))))
end

function projected_loop(p,h,cache,opts,output,accepted,archived,model_hash,source_hash)
    streak = 0
    interval = Float64[]
    previous_median = Inf
    unproductive = 0
    path = joinpath(output,"projected.csv")
    return open(path,"w") do io
        println(io,"map,rR_max_family,rR_total,limiting_R_family,mu_meV,charge_relative,phase_seconds,elapsed_seconds")
        for i in 1:PROJECTED_LIMIT
            start = time()
            total = copy(accepted[:embedding])
            for name in p.kernels.enabled
                total .+= accepted[name]
            end
            gr,kd,ds = N._retarded_green_production(p.grids.ε,h,total;η=0.0,options=opts)
            a = im.*(gr.-permutedims(conj.(gr),(1,2,4,3)))
            if i == 1
                recon = norm(gr.-archived.gr)/norm(archived.gr)
                reconA = norm(a.-archived.a)/norm(archived.a)
                @assert recon < 1e-11 && reconA < 1e-11
                save_toml(joinpath(output,"source-replay.toml"),Dict(
                    "stock_state_sha256"=>source_hash,"stock_retarded_relative"=>recon,
                    "stock_A_relative"=>reconA,"kind"=>"native Dyson replay before FDT reprojection"))
            end
            g,μ,n_error = fdt_green(p,gr,a,kd,ds)
            candidate = projected_candidate(p,g,h,cache,opts)
            distances = [norm(candidate.retarded[x].-accepted[x])/(norm(candidate.retarded[x])+1e-14)
                         for x in CHANNELS]
            last_r, limiting_index = findmax(distances)
            limiting = String(CHANNELS[limiting_index])
            fresh_total = copy(candidate.retarded[:embedding])
            for name in p.kernels.enabled
                fresh_total .+= candidate.retarded[name]
            end
            total_residual = norm(fresh_total.-total)/(norm(fresh_total)+1e-14)
            all(isfinite,(last_r,total_residual,μ)) || error("Non-finite projected map")
            streak = last_r < RETARDED_TARGET && total_residual < RETARDED_TARGET ? streak+1 : 0
            push!(interval,last_r)
            if i%128==0
                current = median(interval)
                unproductive = current >= 0.95*previous_median && streak == 0 ? unproductive+1 : 0
                previous_median = current
                empty!(interval)
            end
            println(io,join((i,last_r,total_residual,limiting,μ,n_error,time()-start,time()-PROCESS_START),','))
            flush(io)
            if i==1 || i%32==0 || streak>=3
                println("projected map ",i," rR=",last_r," rtotal=",total_residual," μ(meV)=",μ,
                        " 3-pass streak ",streak)
                flush(stdout)
            end
            reason = streak>=3 ? "retarded_three_passes" :
                     unproductive>=2 ? "two_blocks_plateau" :
                     i==PROJECTED_LIMIT ? "projected_map_budget" :
                     time()-PROCESS_START >= RETARDED_SOFT_SECONDS ? "wall_reserve" : nothing
            record = Dict("maps"=>i,"reason"=>something(reason,"periodic_checkpoint"),
                "rR_max_family"=>last_r,"rR_total"=>total_residual,"mu_meV"=>μ,"strict_R_streak"=>streak,
                "projected_elapsed_seconds"=>time()-PROCESS_START,"alpha"=>ALPHA,
                "projected_threshold"=>RETARDED_TARGET,"unproductive_128_map_blocks"=>unproductive)
            if i%256==0 || reason!==nothing
                name = reason == "retarded_three_passes" ? "projected-handoff.h5" : "projected-$(i).h5"
                write_projected(joinpath(output,name),p,i,g,accepted,candidate,record,model_hash,source_hash)
                record["checkpoint"] = name
            end
            if reason !== nothing
                initial = SCBAResult(g,candidate.local_fields,candidate.embedding,candidate.plus,
                    candidate.minus,SCBAIteration[],false,:warm_initial_guess,:unresolved,nothing)
                return initial,record
            end
            for (name,r) in accepted
                fresh = candidate.retarded[name]
                r .= (1-ALPHA).*r .+ ALPHA.*fresh
            end
        end
        error("Projected loop exited without final state")
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
            if time()-PROCESS_START>STOCK_SOFT_SECONDS
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
    accepted, archived, model_hash, source_hash = source_state(p,output)
    initial,handoff = projected_loop(p,h,cache,opts,output,accepted,archived,model_hash,source_hash)
    save_toml(joinpath(output,"handoff.toml"),handoff)
    if handoff["reason"]=="retarded_three_passes"
        accepted = archived = nothing
        GC.gc()
        stock(p,h,cache,opts,initial,output,model_hash,handoff)
    else
        save_toml(joinpath(output,"summary.toml"),Dict(
            "handoff"=>handoff,"stock_status"=>"not_started","stock_maps"=>0,
            "total_fresh_maps"=>handoff["maps"],"model_sha256"=>model_hash))
    end
end

main()
