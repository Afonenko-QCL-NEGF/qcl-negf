# Read only the compact terminal sheet density matrices and model inputs.
# The optional intermediate checkpoint reads only Gless, a k slab at a time.
using HDF5, LinearAlgebra, SHA, TOML
import QCLNEGF as Q

const HERE = @__DIR__
const PLAN = TOML.parsefile(joinpath(HERE,"sources.toml"))
const TRANSPORT = isempty(ARGS) ? joinpath(HERE,"..","transport") : only(ARGS)

sha(path) = bytes2hex(open(sha256,path))

function compact_matrix(field)
    values = [complex(v["real"],v["imag"]) for v in field["column_major_values"]]
    return reshape(values,Tuple(field["shape"]))
end

function checkpoint_matrix(path,summary,g,spin,scale,nb)
    return h5open(path,"r") do f
        read(f["schema"]) == "fath-cbo149-aligned-state-v1" || error("Unexpected checkpoint schema")
        read(f["model_identity"]) == summary["model_identity"] || error("Wrong checkpoint identity")
        maximum(abs,read(f["hartree"])) == 0 || error("Expected fixed zero Hartree input")
        realGL,imagGL = f["green/GL_real"],f["green/GL_imag"]
        expected = (length(g.wᴱ),length(g.wᵏ),nb,nb)
        size(realGL) == size(imagGL) == expected || error("Wrong checkpoint Gless shape")
        p = zeros(ComplexF64,nb,nb)
        for k in eachindex(g.wᵏ)
            re,im = realGL[:,k,:,:],imagGL[:,k,:,:]
            prefactor = spin*g.wᵏ[k]/(2π*scale.L₀_m^2)
            @views for b in 1:nb, a in 1:nb
                p[a,b] += prefactor*complex(dot(g.wᴱ,im[:,a,b]),-dot(g.wᴱ,re[:,a,b]))
            end
        end
        return p
    end
end

function read_model(path)
    return h5open(path,"r") do f
        read(f["schema"]) == "fath-cbo149-model-v1" || error("Unexpected saved model schema")
        get(key) = read(f[key])
        g = Q.ModelGrids(get("position_dimensionless"),get("weight_position"),
            get("energy_dimensionless"),get("weight_energy"),BitVector(isone.(get("trusted_energy"))),
            get("k_dimensionless"),get("weight_k"),Float64[],Float64[],Float64[])
        p = Q.MaterialProfiles(get("E_conduction_dimensionless"),get("mass_axial"),
            get("mass_lateral"),get("permittivity"),get("donor_dimensionless"),
            get("alloy_fraction"),Int.(get("layer_index")))
        return g,p,complex.(get("Phi_real"),get("Phi_imag"))
    end
end

function process_case(source, scale, csv, metadata)
    label = source["case"]
    attempt = joinpath(TRANSPORT,label)
    device = TOML.parsefile(joinpath(attempt,"device.toml"))
    config = TOML.parsefile(joinpath(attempt,"input.toml"))
    device["CBO_meV"] == 149.0 && device["electron_electron"] == "none" ||
        error("Wrong transport model")
    config["voltage_mV"] == PLAN["voltage_mV"] && config["mode"] == "fixed" ||
        error("Wrong transport mode")
    checkpoint = get(source,"checkpoint",nothing)
    state_dir = checkpoint === nothing ? attempt : joinpath(attempt,checkpoint)
    case_id = checkpoint === nothing ? label : label*"/"*checkpoint
    summary = TOML.parsefile(joinpath(state_dir,"summary.toml"))
    model = joinpath(attempt,"model.h5")
    sha(model) == summary["model_sha256"] || error("Model hash mismatch")
    grids,profiles,phi = read_model(model)
    target_sheet_m2 = device["sheet_donors_m_minus_2"]*device["ionized_fraction"]
    @assert isapprox(dot(grids.wˣ,profiles.Nᴰ)/scale.L₀_m^2,target_sheet_m2;rtol=1e-14)
    if checkpoint === nothing
        terminal_path = joinpath(attempt,"terminal-observables.toml")
        terminal = TOML.parsefile(terminal_path)
        maximum(abs,terminal["Hartree_energy_meV"]) == 0 || error("Expected zero Hartree input")
        density_matrix = compact_matrix(terminal["sheet_density_m_minus_2"])
        @assert isapprox(real(tr(density_matrix)),terminal["sheet_trace_m_minus_2"];rtol=1e-14)
        source_hash = sha(terminal_path)
        extraction = "terminal-observables sheet density matrix"
    else
        density_matrix = checkpoint_matrix(joinpath(state_dir,"state.h5"),summary,grids,
            device["spin_degeneracy"],scale,size(phi,2))
        source_hash = summary["state_sha256"]
        extraction = "streamed checkpoint Gless only; state SHA as recorded"
    end
    volume_scale = scale.L₀_m^3
    density = real.(diag(phi*density_matrix*phi')) .* scale.L₀_m^2 ./ grids.wˣ
    @assert isapprox(dot(grids.wˣ,density)/scale.L₀_m^2,real(tr(density_matrix));rtol=1e-14)
    U,ζ,rP,neutrality = Q.solve_periodic_poisson(profiles,grids,scale,density)
    L = Q.build_poisson_matrix(profiles,grids)
    rhs = scale.λ_P*(density-profiles.Nᴰ)
    rhs_zero_mean = rhs .- sum(rhs)/length(rhs)
    r_compatible = norm(L*U-rhs_zero_mean)/norm(rhs_zero_mean)
    @assert r_compatible < 1e-11
    escale = scale.E₀_eV*1000
    for j in eachindex(U)
        println(csv,join((case_id,j,grids.x[j]*scale.L₀_m*1e9,grids.wˣ[j]*scale.L₀_m*1e9,
            profiles.εᵣ[j],profiles.Nᴰ[j]/volume_scale,density[j]/volume_scale,escale*U[j]),','))
    end
    metadata[case_id] = Dict("source_kind"=>extraction,"source_sha256"=>source_hash,
        "recorded_state_sha256"=>summary["state_sha256"],"model_sha256"=>summary["model_sha256"],
        "model_identity"=>summary["model_identity"],"status"=>summary["status"],
        "source_maps"=>get(summary,"fresh_maps_completed",summary["last_row"]["ν"]),
        "source_scientific_acceptance"=>summary["scientific_acceptance"],
        "target_donor_m_minus_2"=>target_sheet_m2,"sheet_density_matrix_trace_m_minus_2"=>real(tr(density_matrix)),
        "sheet_density_matrix_antihermitian_relative"=>norm(density_matrix-density_matrix')/norm(density_matrix),
        "native_r_P_raw"=>rP,"native_r_P_compatible"=>r_compatible,
        "native_neutrality_relative"=>neutrality,"native_bordered_zeta"=>ζ)
end

function main()
    BLAS.set_num_threads(1)
    @assert Threads.nthreads() == BLAS.get_num_threads() == 1
    core = dirname(dirname(pathof(Q)))
    @assert readchomp(`git -C $core rev-parse HEAD`) == PLAN["core_commit"]
    @assert readchomp(`git -C $core rev-parse $("HEAD^{tree}")`) == PLAN["core_tree"]
    @assert isempty(readchomp(`git -C $core status --porcelain --untracked-files=no`))
    scales = Q.ScaleSystem()
    records = Dict{String,Any}()
    density_path = joinpath(HERE,"density-input.csv")
    open(density_path*".tmp","w") do io
        println(io,"case,node,z_nm,weight_nm,epsilon_r,donor_m3,electron_m3,native_U_meV")
        for source in PLAN["source"]
            process_case(source,scales,io,records)
        end
    end
    mv(density_path*".tmp",density_path;force=true)
    output = Dict("core_commit"=>PLAN["core_commit"],"core_tree"=>PLAN["core_tree"],
        "julia_version"=>string(VERSION),"cell_bias_mV"=>PLAN["voltage_mV"],
        "E0_eV"=>scales.E₀_eV,"L0_m"=>scales.L₀_m,"lambda_P"=>scales.λ_P,
        "density_csv_sha256"=>sha(density_path),"cases"=>records)
    open(io->TOML.print(io,output;sorted=true),joinpath(HERE,"density-sources.toml"),"w")
end

main()
