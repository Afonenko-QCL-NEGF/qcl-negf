using LinearAlgebra
using QCLNEGF
using QCLNEGFRunner
using SHA
using TOML
using Unitful
using YAML

const Runner = QCLNEGFRunner
const Ref = QCLNEGF.QCLReferenceOperators
const LT = QCLNEGF.LinkedTransport
const APP = normpath(joinpath(@__DIR__, "..", ".."))
const HISTORICAL = "d76b588c1af2ef5d3a4b09b67d0094a9a809db11"
const BDD_SOURCE = "studies/fath-lo-rank-v843/fath_factorial.jl"
const BOSCO_SOURCE = "studies/fath54-common-q/runner/bosco_vertices.jl"
const BOSCO_DRIVER = "studies/fath54-common-q/runner/bosco.jl"
const BOSCO_SELECTION = "studies/fath54-common-q/runner/followup.jl"
const FATH_REPLAY = "studies/fath54-common-q/evidence/f13-replay.json"
const FATH_DEVICE = "studies/fath-v843/fath-device.toml"
const BOSCO_DEVICE = "runner/examples/config/reference-2019-70k.yaml"

historical(path) = read(`git -C $APP show $HISTORICAL:$path`, String)
sha(x) = bytes2hex(sha256(x))
file_sha(path) = bytes2hex(open(sha256, path))
relative(a, b) = norm(a-b) / norm(b)

function package_source(package)
    root = pkgdir(package)
    command = `git -C $root rev-parse --verify HEAD`
    head = readchomp(pipeline(ignorestatus(command); stderr=devnull))
    paths = ["Project.toml"]
    for subdir in ("src", "ext", "schema")
        directory = joinpath(root, subdir)
        isdir(directory) || continue
        for (dir, _, files) in walkdir(directory), file in files
            push!(paths, replace(relpath(joinpath(dir, file), root), '\\'=>'/'))
        end
    end
    records = [path * "\0" * file_sha(joinpath(root, path)) * "\n" for path in sort!(paths)]
    return (;version=string(Base.pkgversion(package)), git_head=isempty(head) ? nothing : head,
        source_tree_sha256=sha(join(records)))
end

function check_geometry(physical, numerical, scales; period_nm, voltage_V, temperature_K,
                        sheet_cm2, donor_interval_nm)
    grids = build_grids(physical, numerical, scales)
    profiles = build_profiles(physical, numerical, scales, grids)
    period = ustrip(u"nm", QCLNEGF.QCLDomain.period_length(physical))
    field = ustrip(u"V/m", physical.F_bias)
    voltage = field * period * 1e-9
    @assert isapprox(period, period_nm; atol=1e-12)
    @assert isapprox(voltage, voltage_V; atol=1e-14)
    @assert ustrip(u"K", physical.Tᴸ) == ustrip(u"K", physical.Tᴸᴼ) == temperature_K
    density_scale = 1 / (scales.L₀_m^2 * 1e4)
    measured_sheet = dot(grids.wˣ, profiles.Nᴰ) * density_scale
    @assert isapprox(measured_sheet, sheet_cm2; rtol=2e-14)
    z_nm = grids.x .* (1e9 * scales.L₀_m)
    donors = findall(>(0), profiles.Nᴰ)
    first_donor, last_donor = donor_interval_nm
    @assert donors == findall(z -> first_donor <= z < last_donor, z_nm)
    drange = ustrip(u"nm^-1", numerical.k_max)
    @assert all(>(0), grids.wᵏ)
    @assert isapprox(sum(grids.wᵏ)/(1e9*scales.L₀_m)^2, drange^2/(4π); rtol=2e-14)
    energy_span_eV = sum(grids.wᴱ) * scales.E₀_eV
    @assert isapprox(energy_span_eV, ustrip(u"eV", numerical.E_max-numerical.E_min); rtol=2e-14)
    cuts_nm = collect(range(0, period; length=numerical.N_z+1))
    passport = (; period_nm=period, voltage_per_period_V=voltage, field_V_per_m=field,
        lattice_temperature_K=temperature_K, lo_temperature_K=temperature_K,
        donor_interval_nm, donors_selected_cells=length(donors), donor_sheet_cm2=measured_sheet,
        position_nodes=length(z_nm), cuts=length(cuts_nm), dz_nm=period/length(z_nm),
        energy_nodes=length(grids.ε), energy_min_max_eV=collect(extrema(grids.ε .* scales.E₀_eV)),
        energy_weight_sum_eV=energy_span_eV, radial_nodes=length(grids.κ),
        radial_max_nm_inverse=drange, radial_measure_nm_minus_2=sum(grids.wᵏ)/(1e9*scales.L₀_m)^2,
        angular_nodes=length(grids.φ), qz_nodes=length(grids.qᶻ))
    return (; physical, numerical, scales, grids, profiles, cuts_nm, passport)
end

function fath_geometry()
    device = TOML.parse(historical(FATH_DEVICE))
    isbarrier(i) = device["material_order"][i] == "AlGaAs"
    layers = map(eachindex(device["material_order"])) do i
        prefix = isbarrier(i) ? "barrier" : "well"
        mass = device[prefix * "_mass_over_me"]
        Layer(d=device["thickness_nm"][i]*u"nm", material=Symbol(device["material_order"][i]),
            x_Al=isbarrier(i) ? device["barrier_x_Al"] : 0.0,
            Eᶜ=(isbarrier(i) ? device["CBO_meV"] : 0.0)*u"meV", mᶻᵣ=mass,
            m_parallelᵣ=mass, εᵣ=device[prefix * "_permittivity"],
            doped=i==device["doped_segment_index"])
    end
    p = PhysicalParameters(layers, device["sheet_donors_m_minus_2"]*u"m^-2",
        device["ionized_fraction"], 54u"mV"/(device["period_nm"]*u"nm"),
        device["z_reference_nm"]*u"nm", device["energy_reference_eV"]*u"eV",
        device["lattice_temperature_K"]*u"K", device["LO_temperature_K"]*u"K",
        device["epsilon_static"], device["epsilon_optical"], device["LO_energy_meV"]*u"meV",
        device["q_impurity_nm_inverse"]*u"nm^-1", device["q_LO_nm_inverse"]*u"nm^-1",
        device["IFR_height_nm"]*u"nm", device["IFR_correlation_length_nm"]*u"nm",
        device["acoustic_deformation_eV"]*u"eV", device["mass_density_kg_m3"]*u"kg/m^3",
        device["sound_speed_m_s"]*u"m/s", device["alloy_disorder_eV"]*u"eV",
        device["alloy_volume_m3"]*u"m^3", device["spin_degeneracy"],
        device["interface_positions_nm"] .* u"nm")
    # The published compact sources identify the spatial, energy and radial axes.
    # The default auxiliary grid entries here are never used as F13 evidence.
    n = NumericalParameters(N_z=144, N_b=7, P_basis=3, E_min=-400u"meV", E_max=560u"meV",
        N_E=481, M_E=80u"meV", k_max=0.6u"nm^-1", N_k=13, N_φ=32,
        qz_max=10u"nm^-1", N_qz=161, η_seed=0.5u"meV")
    g = check_geometry(p, n, ScaleSystem(); period_nm=43.91, voltage_V=0.054,
        temperature_K=10.0, sheet_cm2=3e10, donor_interval_nm=device["donor_interval_nm"])
    replay = YAML.load(historical(FATH_REPLAY))
    cut_error_nm = maximum(abs, g.cuts_nm - replay["cuts_nm"])
    @assert cut_error_nm <= 5e-13
    input = replay["replay"]
    metrics = input["metrics"]
    profile = metrics["current_profile_A_cm2"]
    @assert length(profile) == length(g.cuts_nm) == 145
    midpoint_weights = (g.cuts_nm[3:end] - g.cuts_nm[1:end-2]) ./ 2
    interior = profile[2:end-1]
    mean_current = dot(interior, midpoint_weights)/sum(midpoint_weights)
    maxdev = maximum(abs, profile .- mean_current)
    @assert isapprox(mean_current, metrics["spatial"]["mean_internal_A_cm2"]; atol=2e-11)
    @assert isapprox(maxdev, metrics["spatial"]["max_deviation_from_mean_A_cm2"]; atol=2e-11)
    @assert isapprox(collect(extrema(profile)), metrics["spatial"]["full_range_A_cm2"]; atol=2e-11)
    tol = max(1.0, 0.01abs(mean_current))
    @assert metrics["rK"] > 1e-8 && metrics["rSigma"] > 1e-8
    @assert abs(metrics["raw_lambda"]-1) > 1e-8 && maxdev > tol
    geometry_keys = (:period_nm, :voltage_per_period_V, :field_V_per_m, :lattice_temperature_K,
        :lo_temperature_K, :donor_interval_nm, :donors_selected_cells, :donor_sheet_cm2,
        :position_nodes, :cuts, :dz_nm, :energy_nodes, :energy_min_max_eV, :energy_weight_sum_eV,
        :radial_nodes, :radial_max_nm_inverse, :radial_measure_nm_minus_2)
    return (; geometry=NamedTuple{geometry_keys}(Tuple(getfield(g.passport,k) for k in geometry_keys)), cut_error_nm,
        historical_profile_arithmetic=(; mean_A_cm2=mean_current, max_deviation_A_cm2=maxdev,
            range_A_cm2=collect(extrema(profile)), tolerance_A_cm2=tol,
            input_sha256=input["input_sha"], fresh_image_sha256=input["image_sha"],
            input_lambda=input["native_input"]["raw_lambda"], fresh_lambda=metrics["raw_lambda"],
            rK=metrics["rK"], rSigma=metrics["rSigma"], stationarity="failed"),
        fresh_dyson_map="unknown")
end

function bosco_configuration()
    source = historical(BOSCO_DEVICE)
    mktempdir() do directory
        reference = joinpath(directory, "reference.yaml")
        overrides = joinpath(directory, "point.yaml")
        write(reference, source)
        # These are the shared pre-refinement settings of the published Bosco driver.
        YAML.write_file(overrides, Dict(
            "run"=>Dict("name"=>"bosco2019-200k-56mV-base-control", "classification"=>"study"),
            "physical"=>Dict("lattice_temperature"=>"200 K", "lo_temperature"=>"200 K",
                "alloy_potential"=>"0.60 eV", "primitive_cell_volume"=>"4.5168e-29 m^3"),
            "physical_models"=>Dict("screening"=>"fixed", "dispersion"=>"parabolic",
                "lo_population"=>"thermal", "electron_electron"=>Dict("mode"=>"none")),
            "numerical"=>Dict("spatial_nodes"=>98, "basis_states"=>5, "basis_periods"=>3,
                "energy_min"=>"-0.4 eV", "energy_max"=>"0.56 eV", "energy_nodes"=>481,
                "momentum_nodes"=>31, "angular_nodes"=>32, "longitudinal_momentum_nodes"=>641),
            "scattering"=>Dict("alloy_disorder"=>true),
            "algorithms"=>Dict("energy_shift"=>"conservative_pair", "hilbert"=>"fft"),
            "study"=>Dict("temperatures"=>["200 K"], "voltages_per_period"=>["56 mV"],
                "calculate_optical_response"=>false)))
        return Runner.load_run_configuration([reference, overrides])
    end
end

function weighted_reciprocity(a, w)
    # Compare covariances before the radial measure with the pair norm w_in*w_out.
    slices = CartesianIndices(size(a)[1:ndims(a)-2])
    d2 = 0.0
    n2 = 0.0
    for j in eachindex(w), i in eachindex(w), site in slices
        x = a[site, i, j]
        d2 += w[i]*w[j]*abs2(x)
        n2 += w[i]*w[j]*abs2(x - conj(a[site, j, i]))
    end
    d2 > 0 || error("cannot qualify an empty covariance")
    return sqrt(n2 / d2)
end

function project_vertices(g, basis, cov)
    picks = [1, cld(length(g.grids.κ), 2), length(g.grids.κ)]
    p, s, grid = g.physical, g.scales, g.grids
    slim = QCLNEGF.QCLDomain.ModelGrids(grid.x, grid.wˣ, grid.ε, grid.wᴱ, grid.trusted_energy,
        grid.κ[picks], grid.wᵏ[picks], grid.qᶻ, grid.wᑫᶻ, grid.φ)
    density(ψ) = hcat((conj.(ψ[:,a]).*ψ[:,b] for b in axes(ψ,2) for a in axes(ψ,2))...)
    d = density(basis.Φ)
    ifr_density = density(cov.interfaces * basis.Φ)
    oracle = (
        LO=first(Ref.lo_phonon_kernel(p, s, slim, basis)),
        acoustic=Ref.acoustic_kernel(p, s, slim, basis),
        impurity=Ref.impurity_kernel(p, s, slim, g.profiles, basis; angular=:legacy_uniform),
        IFR=Ref.interface_roughness_kernel(p, s, slim, basis),
        alloy=Ref.alloy_kernel(p, s, slim, g.profiles, basis),
    )
    return map(((1,1),(1,3),(2,2))) do (i,j)
        outgoing, incoming = picks[i], picks[j]
        compare = (
            LO=transpose(d)*cov.lo[:,:,incoming,outgoing]*d,
            acoustic=transpose(d)*(cov.acoustic.*d),
            impurity=transpose(d)*cov.impurity[:,:,incoming,outgoing]*d,
            IFR=cov.ifr_pair[incoming,outgoing]*(transpose(ifr_density)*ifr_density),
            alloy=transpose(d)*(cov.alloy.*d),
        )
        channels = Dict{String,Float64}()
        for name in keys(oracle)
            n = g.numerical.N_b
            direct = reshape(getproperty(oracle, name)[i,j,:,:,:,:], n^2, n^2)
            channels[string(name)] = relative(getproperty(compare, name), direct)
        end
        @assert maximum(values(channels)) < 2e-11
        (; outgoing_nm_inverse=grid.κ[outgoing]/(1e9*s.L₀_m),
           incoming_nm_inverse=grid.κ[incoming]/(1e9*s.L₀_m), relative_frobenius=channels)
    end
end

# Coefficient and boundary stencil from fath_factorial.jl bdd_chain, with the
# published 0.1 eV, 10 nm base scaling. The linked chain has no corner hop.
const BDD_CBAR = (1.054571817e-34)^2/(2*9.1093837139e-31*0.1*1.602176634e-19*(1e-8)^2)
function chain(g, cells, bias; periodic_ends)
    nz = g.numerical.N_z
    dz = first(g.grids.wˣ)
    pos = (first(cells)*nz):((last(cells)+1)*nz-1)
    site(i) = mod(i, nz)+1
    axial = g.profiles.mᶻᵣ
    face(i) = -2BDD_CBAR/(dz^2*(axial[site(i)]+axial[site(i+1)]))
    faces = face.((first(pos)-1):last(pos))
    if !periodic_ends
        faces[1] = -BDD_CBAR/(dz^2*axial[1])
        faces[end] = -BDD_CBAR/(dz^2*axial[end])
    end
    site_ids = site.(pos)
    z = g.grids.x[site_ids] + (nz*dz).*fld.(pos, nz)
    diagonal = g.profiles.Eᶜ[site_ids] - bias .* z ./ (nz*dz) - faces[1:end-1] - faces[2:end]
    return (;z, h=SymTridiagonal(diagonal, faces[2:end-1]), radial=BDD_CBAR ./ g.profiles.m_parallelᵣ[site_ids])
end

function bosco_seed(g, basis)
    rank = g.numerical.N_b
    nz = g.numerical.N_z
    tail, offsets = -3:3, -4:4
    zero_bias = chain(g, tail, 0.0; periodic_ends=false)
    core_tridiagonal = build_bdd_hamiltonian(repeat(g.profiles.Eᶜ, length(tail)),
        repeat(g.profiles.mᶻᵣ, length(tail)), first(g.grids.wˣ), BDD_CBAR)
    @assert relative(zero_bias.h, core_tridiagonal) < 2e-14
    subspace = eigen(zero_bias.h, 1:length(tail)*rank).vectors
    position = eigen(Symmetric(subspace'*(zero_bias.z.*subspace)))
    columns = (3rank+1):(4rank)
    templates = subspace*position.vectors[:,columns]
    for col in eachcol(templates)
        col[argmax(abs.(col))] < 0 && (col .*= -1)
    end
    modes = zeros(ComplexF64, length(offsets)*nz, length(offsets)*rank)
    for (j, _) in enumerate(offsets), (t, shift) in enumerate(tail)
        i = j+shift
        1 <= i <= length(offsets) || continue
        modes[(i-1)*nz+1:i*nz,(j-1)*rank+1:j*rank] = templates[(t-1)*nz+1:t*nz,:]
    end
    q_base = basis.Φ
    sliced = reshape(templates, nz, :)
    added = svd(sliced - q_base*(q_base'*sliced))
    nd = count(>(1e-10), added.S)
    extension = added.U[:,1:nd]
    extension -= q_base*(q_base'*extension)
    q = hcat(q_base, Matrix(qr(extension).Q)[:,1:nd])
    coverage_error = relative(q*(q'*sliced), sliced)
    @assert coverage_error <= 2e-10
    @assert norm(q'*q-I) < 2e-12
    geo = LT.TailGeometry(modes, q, rank, collect(offsets), 0.56, 7)
    metric_condition = cond(geo.metric)
    @assert metric_condition < 100
    linked = chain(g, offsets, 0.56; periodic_ends=true)
    en, radial = g.grids.ε, g.grids.κ
    center = LT.centered_basis(geo)
    spectra = map(radial) do k
        h = modes'*(linked.h + Diagonal(k^2 .* linked.radial))*modes
        # Keep the projected Lorentzian representation factored by poles and
        # modal weights. No packed collision source or causal anchor is needed.
        spec = eigen(Hermitian(h), Hermitian(geo.metric))
        coefficients = center*spec.vectors
        (;values=spec.values, central_weights=vec(sum(abs2,coefficients;dims=1)))
    end
    η = ustrip(u"eV", g.numerical.η_seed)/g.scales.E₀_eV
    θ = 8.617333262145e-5 * g.passport.lattice_temperature_K / g.scales.E₀_eV
    fermi(x) = inv(1+exp(clamp(x, -700., 700.)))
    spectral_trace = [dot(s.central_weights, 2η ./ ((e .- s.values).^2 .+ η^2))
        for e in en, s in spectra]
    # The published seed uses spin/(2π) times the radial and energy weights.
    weights = (g.physical.g_s/(2π)) .* (g.grids.wᴱ * transpose(g.grids.wᵏ))
    sheet(μ) = sum(weights .* spectral_trace .* fermi.((en .- μ)./θ))
    target = dot(g.grids.wˣ, g.profiles.Nᴰ)
    lo, hi = first(en)-10θ, last(en)+10θ
    @assert sheet(lo) < target < sheet(hi)
    for _ in 1:80
        mid = (lo+hi)/2
        if sheet(mid) < target
            lo = mid
        else
            hi = mid
        end
    end
    μ = (lo+hi)/2
    raw_sheet = sheet(μ)
    @assert isapprox(raw_sheet, target; rtol=5e-12)
    # Cross-check the reduction by performing the separable weighted sum by ring.
    check = sum(eachindex(spectra)) do k
        ring = spectra[k]
        shell = sum(pairs(ring.values)) do (j, pole)
            line_shape = 2η ./ ((en .- pole).^2 .+ η^2)
            ring.central_weights[j]*dot(weights[:,k], line_shape .* fermi.((en .- μ)./θ))
        end
        shell
    end
    @assert isapprox(check, raw_sheet; rtol=5e-13)
    density_scale = 1/(g.scales.L₀_m^2*1e4)
    return (;label="unrefined W5 control", periods=length(offsets), rank, collision_coordinate_rank=size(q,2),
        coverage_error, metric_condition, broadening_meV=η*1e3*g.scales.E₀_eV,
        chemical_potential_meV=μ*1e3*g.scales.E₀_eV, raw_sheet_cm2=raw_sheet*density_scale,
        relative_charge_error=abs(raw_sheet-target)/target,
        independent_sum_difference_cm2=abs(raw_sheet-check)*density_scale,
        pole_range_meV=1e3*g.scales.E₀_eV .* [first(spectra[1].values),last(spectra[end].values)])
end

function bosco_geometry_and_vertices(assemble)
    c = bosco_configuration()
    g = check_geometry(c.physical, c.numerical, c.scales; period_nm=29.61, voltage_V=0.056,
        temperature_K=200.0, sheet_cm2=4.5e10, donor_interval_nm=[21.55,24.45])
    basis = build_basis(g.physical, g.numerical, g.scales, g.grids, g.profiles; localization=:pzp)
    seed = bosco_seed(g, basis)
    println(stderr, "Bosco geometry and W5 base seed checked")
    cov = assemble(g.physical, g.profiles, g.grids, g.scales, :gaussian; enabled=LT.COLLISION_CHANNELS)
    @assert cov.weights_k == g.grids.wᵏ
    reciprocity = (;LO=weighted_reciprocity(cov.lo,cov.weights_k),
        impurity=weighted_reciprocity(cov.impurity,cov.weights_k),
        IFR=weighted_reciprocity(cov.ifr_pair,cov.weights_k))
    @assert maximum(values(reciprocity)) < 2e-12
    @assert weighted_reciprocity([1.0 0.5; 0.75 1.0], [0.2,0.8]) > 2e-12
    local_channels = (;acoustic_range=collect(extrema(cov.acoustic)), alloy_range=collect(extrema(cov.alloy)))
    @assert all(isfinite,cov.acoustic) && all(isfinite,cov.alloy)
    @assert minimum(cov.acoustic) > 0 && minimum(cov.alloy) == 0 < maximum(cov.alloy)
    println(stderr, "Bosco radial reciprocity checked")
    projected_comparison = project_vertices(g, basis, cov)
    println(stderr, "Bosco five direct projections checked")
    return (; geometry=g.passport, cold_seed=seed, LO_bose_occupation=cov.bose,
        radial_pair_reciprocity=reciprocity, diagonal_local_channels=local_channels,
        five_channel_projected_comparison=projected_comparison,
        selected_scheme="unknown", fresh_dyson_map="unknown")
end

function write_result(output, assemble)
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    core = package_source(QCLNEGF)
    runner = package_source(Runner)
    fath = fath_geometry()
    println(stderr, "Fath geometry and published profile checked")
    bosco = bosco_geometry_and_vertices(assemble)
    core == package_source(QCLNEGF) &&
        runner == package_source(Runner) || error("loaded source changed during controls")
    evidence = (;schema="qcl-negf-initial-state-controls/v1",
        provenance=(;historical_source_revision=HISTORICAL,
            historical_file_sha256=Dict(path=>sha(historical(path)) for path in
                (BDD_SOURCE,BOSCO_SOURCE,BOSCO_DRIVER,BOSCO_SELECTION,BOSCO_DEVICE,FATH_DEVICE,FATH_REPLAY)),
            control_sha256=file_sha(@__FILE__), toolchain=Runner._runtime_toolchain_provenance(),
            core, runner),
        fath, bosco)
    open(output,"w") do io
        Runner._light_json(io,evidence)
        println(io)
    end
end

if abspath(PROGRAM_FILE)==abspath(@__FILE__)
    length(ARGS)==1 || error("Usage: controls.jl NEW_OUTPUT_JSON")
    include_string(Main, historical(BOSCO_SOURCE), BOSCO_SOURCE)
    Base.invokelatest() do
        write_result(only(ARGS), BoscoVertices.assemble)
    end
end
