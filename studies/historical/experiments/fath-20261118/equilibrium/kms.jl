using HDF5, LinearAlgebra, QCLNEGF, SHA, TOML, Unitful

const HERE = @__DIR__
const RUN = joinpath(HERE, "attempt01")
const N = QCLNEGF.QCLNumerics

module FrozenTransport
include(joinpath(@__DIR__, "attempt01", "transport-run.jl"))
end

function fermi_pair(energy, μ, kT)
    x = (energy .- μ)./kT
    u = exp.(-abs.(x))
    return ifelse.(x .>= 0, u./(1 .+ u), 1 ./(1 .+ u)),
           ifelse.(x .>= 0, 1 ./(1 .+ u), u./(1 .+ u))
end

function prepare()
    BLAS.set_num_threads(1)
    @assert VERSION == v"1.13.4" && Threads.nthreads(:default) == 1 && BLAS.get_num_threads() == 1
    root_core = dirname(dirname(pathof(QCLNEGF)))
    @assert readchomp(`git -C $root_core rev-parse HEAD`) == "e171caa60cce676c6c4238dd671e7c527f2bd977"
    @assert isempty(readchomp(`git -C $root_core status --porcelain --untracked-files=no`))
    src = joinpath(RUN, "device.toml")
    @assert bytes2hex(open(sha256, src)) == "4e4314af4696465084b48fc7e22cd0310c03889256f19abaa2500ee6a923d502"
    cfg = TOML.parsefile(src)
    numerical = NumericalParameters(; N_z=144, N_b=7, P_basis=3, E_min=-0.4u"eV",
        E_max=.56u"eV", N_E=1201, M_E=260u"meV", k_max=.6u"nm^-1", N_k=4,
        N_φ=12, qz_max=10u"nm^-1", N_qz=31, η_seed=0.5u"meV")
    algorithms = AlgorithmOptions(; kernel_build=:direct, embedding=:finite_chain,
        embedding_periods=4, mixing=:linear, anderson_history_depth=2,
        anderson_damping=1.0, anderson_regularization=1e-12,
        energy_shift=:sparse_plan, hilbert=:product_integration, elastic_retarded=:direct_green)
    models = PhysicalModelOptions(screening=:fixed, dispersion=:parabolic,
        electron_electron=ElectronElectronOptions(mode=:none), lo_population=:thermal)
    physical = FrozenTransport.device(cfg)
    p = build_configured_scattering_problem(; physical, numerical, scales=ScaleSystem(),
        scattering=ScatteringOptions(LO=true, acoustic=true, impurity=true, IFR=true, alloy=true),
        algorithms, kernel_options=ProductionKernelOptions(), physical_models=models).problem
    p = retarget_problem(p; V_period=0u"mV", energy_shift=:sparse_plan)
    opts = ProductionOptions(; algorithms, worker_count=1, parallel_backend=:threads,
        hilbert_columns=1, verify_fft_roundoff=true, memory_budget_bytes=600*2^20)
    return p, opts, build_production_cache(p; options=opts)
end

function terminal_A(p)
    path = joinpath(RUN, "linear", "fdt-state.h5")
    terminal = TOML.parsefile(joinpath(RUN, "linear", "execution.toml"))
    hash = bytes2hex(open(sha256, path))
    @assert hash == terminal["fdt_state_sha256"]
    result = h5open(path, "r") do input
        @assert read(input["schema"]) == "fath-equilibrium-FDT-terminal-v1"
        @assert read(input["map"]) == 256
        @assert read(input["energy_dimensionless"]) == p.grids.ε
        @assert read(input["energy_weight"]) == p.grids.wᴱ
        @assert read(input["radial_weight"]) == p.grids.wᵏ
        @assert all(iszero, read(input["hartree_dimensionless"]))
        return complex.(read(input["A_real"]), read(input["A_imag"]))
    end
    return result, hash
end

function accumulate_metrics!(output, variant, family, ses, f, h, energy, μ, kT, Ω, we, wk)
    e0 = 100.0
    sn, sp = -im .* ses.Σˡ, im .* ses.Σᵍ
    covariance = f .* sp
    complement = h .* sn
    gamma = sn .+ sp
    r_enclosure = ses.Σᴿ === nothing ? nothing : im .* (
        ses.Σᴿ .- permutedims(conj.(ses.Σᴿ), (1,2,4,3)))
    masks = (
        ("all", trues(length(energy))),
        ("fermi_5kT", abs.(energy .- μ) .<= 5*kT),
        ("lo_full_support", (energy .- Ω .>= first(energy) - 1e-11) .&
                            (energy .+ Ω .<= last(energy) + 1e-11)),
        ("lo_lower_clip", energy .- Ω .< first(energy) - 1e-11),
        ("lo_upper_clip", energy .+ Ω .> last(energy) + 1e-11),
    )
    for (segment, mask) in masks
        e = findall(mask)
        @assert !isempty(e)
        w = we[e] .* transpose(wk)
        wn(x) = sqrt(sum(abs2.(x[e,:,:,:]) .* w))
        absolute = wn(complement .- covariance)
        scale = hypot(wn(complement), wn(covariance))
        rhs = r_enclosure === nothing ? gamma : r_enclosure
        lg_norm = wn(gamma)
        lesser_defect = wn(sn .- f .* rhs)
        greater_defect = wn(sp .- h .* rhs)
        gamma_closure = r_enclosure === nothing ? NaN : wn(r_enclosure .- gamma)/max(lg_norm, floatmin(Float64))
        push!(output, (variant, family, segment, length(e), e0*energy[first(e)], e0*energy[last(e)],
                       e0*absolute, e0*scale, (scale == 0 ? NaN : absolute/scale),
                       e0*lesser_defect, e0*greater_defect, e0*lg_norm, gamma_closure))
    end
end

function phonon_parts(kernel_action, shifted_n_p, shifted_n_m, shifted_h_p, shifted_h_m, nlo)
    sin = (nlo+1).*kernel_action(shifted_n_p) .+ nlo.*kernel_action(shifted_n_m)
    sout = (nlo+1).*kernel_action(shifted_h_m) .+ nlo.*kernel_action(shifted_h_p)
    return (Σˡ = im.*sin, Σᵍ = -im.*sout)
end

function near_grid(A, energy, Ω)
    n = length(energy)
    e = collect(range(first(energy); step=Ω/46, length=n))
    out = similar(A)
    for (i, target) in enumerate(e)
        j = min(n-1,searchsortedlast(energy,target))
        @assert j >= 1
        w = (target-energy[j])/(energy[j+1]-energy[j])
        @views out[i,:,:,:] .= (1-w).*A[j,:,:,:] .+ w.*A[j+1,:,:,:]
    end
    return e, out
end

function integer_shift(X, delta)
    out = zero(X)
    n = size(X,1)
    if delta > 0
        @views out[1:n-delta,:,:,:] .= X[1+delta:n,:,:,:]
    else
        d = -delta
        @views out[1+d:n,:,:,:] .= X[1:n-d,:,:,:]
    end
    return out
end

function main()
    @assert length(ARGS)==1
    μ = parse(Float64, only(ARGS))/100
    p, opts, cache = prepare()
    A, a_hash = terminal_A(p)
    energy, we, wk = p.grids.ε, p.grids.wᴱ, p.grids.wᵏ
    kT, Ω = (1.380649e-23/1.602176634e-19)*10/.1, 36.7/100
    f, empty = fermi_pair(energy, μ, kT)
    gl, gg = im.*(f.*A), -im.*(empty.*A)
    # Finite-window causal Cauchy transform of the measured A. No archived Re GR
    # was retained. The exact input spectral part is still A at each grid point.
    gr, _ = N._retarded_self_energy_selected(gl, gg, p, cache, opts)
    spectral_gr = im.*(gr.-permutedims(conj.(gr),(1,2,4,3)))
    @assert norm(spectral_gr.-A)/norm(A) < 1e-12
    g = GreenState(gr, gl, gg, A, zeros(length(energy),length(wk)), zeros(length(energy),length(wk)))
    stock = N._scattering_candidate_production(p, g, cache, opts)
    h = project_hamiltonians(p, zeros(144))
    stock_cavities = N._embedding_self_energy_selected(p, g, cache, opts; scattering=stock, h)
    nlo = N._thermal_lo_occupation(p.physical)
    fd_shift(direction, field) = N._selected_energy_shift(p, cache, direction, field, opts)
    action(field) = N._selected_static_contraction(p, cache, :LO, field, p.kernels.qᴷ[:LO], opts)
    a_p, a_m = fd_shift(:plus_lo,A), fd_shift(:minus_lo,A)
    f_p, hp = fermi_pair(energy .+ Ω, μ, kT)
    f_m, hm = fermi_pair(energy .- Ω, μ, kT)
    factored = phonon_parts(action, f_p.*a_p, f_m.*a_m, hp.*a_p, hm.*a_m, nlo)
    factored_R, _ = N._retarded_self_energy_selected(factored.Σˡ, factored.Σᵍ, p, cache, opts)
    modified = copy(stock)
    modified[:LO] = SelfEnergyFamily(factored_R, factored.Σˡ, factored.Σᵍ)
    factored_cavities = N._embedding_self_energy_selected(p, g, cache, opts; scattering=modified, h)
    e_near, a_near = near_grid(A, energy, Ω)
    fn, hn = fermi_pair(e_near, μ, kT)
    an, ap = fn.*a_near, hn.*a_near
    integer = phonon_parts(action, integer_shift(an,46), integer_shift(an,-46),
                           integer_shift(ap,46), integer_shift(ap,-46), nlo)
    wn = fill(Ω/46,length(e_near))
    wn[[1,end]] ./= 2
    rows = []
    for (name,family) in sort(collect(stock);by=first)
        accumulate_metrics!(rows, "native", String(name), family, f, empty, energy, μ, kT, Ω, we, wk)
    end
    for (name,family) in zip(("embedding_total","embedding_plus","embedding_minus"), stock_cavities)
        accumulate_metrics!(rows, "native", name, family, f, empty, energy, μ, kT, Ω, we, wk)
    end
    accumulate_metrics!(rows, "factorized_f", "LO", modified[:LO], f, empty, energy, μ, kT, Ω, we, wk)
    for (name,family) in zip(("embedding_total","embedding_plus","embedding_minus"), factored_cavities)
        accumulate_metrics!(rows, "factorized_f", name, family, f, empty, energy, μ, kT, Ω, we, wk)
    end
    accumulate_metrics!(rows, "commensurate_LO", "LO", (;Σᴿ=nothing, integer...), fn, hn,
                        e_near, μ, kT, Ω, wn, wk)
    open(joinpath(HERE,"kms.csv"),"w") do output
        println(output,"variant,family,segment,NE,Emin_meV,Emax_meV,KMS_weighted_abs_meV,KMS_weighted_scale_meV,KMS_relative,Sn_minus_fGammaR_abs_meV,Sp_minus_hGammaR_abs_meV,GammaLG_scale_meV,GammaR_vs_GammaLG_relative")
        for row in rows
            println(output,join(row,","))
        end
    end
    open(joinpath(HERE,"kms-identity.toml"),"w") do output
        TOML.print(output, Dict(
            "state_sha256"=>a_hash, "source_map"=>256, "mu_meV"=>100μ,
            "energy_step_meV"=>100*(energy[2]-energy[1]), "thermal_LO_occupation"=>nlo,
            "near_grid_meV"=>100.0.*[first(e_near),last(e_near)],
            "near_grid_step_meV"=>100Ω/46, "relative_change_LO_retarded"=>norm(factored_R.-stock[:LO].Σᴿ)/norm(stock[:LO].Σᴿ),
            "constructed_GR"=>"finite-window Hilbert(A) and archived spectral part A; terminal real GR unavailable",
        ); sorted=true)
    end
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
