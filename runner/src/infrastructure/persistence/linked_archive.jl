using TOML
using QCLNEGF.LinkedTransport: COLLISION_CHANNELS, LinkedProblem, LocalCollisionKernels

_linked_file_digest(path) = open(io->bytes2hex(sha256(io)),path)

function _linked_manifest(directory)
    path = joinpath(directory,"files.sha256")
    isfile(path) || return nothing
    bytes = read(path)
    digest = bytes2hex(sha256(bytes))
    expected = Dict{String,String}()
    for line in eachline(IOBuffer(bytes))
        isempty(strip(line)) && continue
        record = match(r"^([0-9a-fA-F]{64}) [ *](.+)$",line)
        isnothing(record) && error("Malformed SHA-256 entry in $path")
        filename = normpath(record.captures[2])
        haskey(expected,filename) && error("Duplicate SHA-256 entry for $filename in $path")
        expected[filename] = lowercase(record.captures[1])
    end
    return (;expected,digest)
end

function _verify_linked_asset(manifest, filename, digest)
    isnothing(manifest) && return nothing
    get(manifest.expected,filename,nothing) == digest ||
        error("SHA-256 mismatch or absent manifest entry for $filename")
    return nothing
end

function _linked_input_id(spec_digest, assets)
    pairs = [filename * " " * assets[filename] for filename in sort!(collect(keys(assets)))]
    return bytes2hex(sha256(join(["qcl-negf-linked-input/v1"; "spec.toml " * spec_digest; pairs], '\n')))
end

function _read_linked_array(directory, name, ::Type{T}, dims...) where T
    path = joinpath(directory,name*".bin")
    filesize(path) == prod(dims)*sizeof(T) || error("Wrong size for $path")
    return open(io->read!(io,Array{T}(undef,dims...)),path)
end

"""
Read a sealed legacy linked-map checkpoint into arrays for the in-memory Core
map. Keep archive identity and device labels with the Runner.
"""
function _read_linked_checkpoint(directory)
    Base.ENDIAN_BOM == 0x04030201 || error("The packed archive requires a little-endian host")
    manifest = _linked_manifest(directory)
    spec_path = joinpath(directory,"spec.toml")
    spec_bytes = read(spec_path)
    spec_digest = bytes2hex(sha256(spec_bytes))
    _verify_linked_asset(manifest,"spec.toml",spec_digest)
    spec = TOML.parse(String(spec_bytes))
    Tuple(Symbol.(spec["channels"])) == COLLISION_CHANNELS ||
        error("Channel order differs from the packed archive format")
    ne,nk,r,nb,nz,m,nfaces = (spec[key] for key in
        ("ne","nk","r","nb","nz","n_modes","n_interfaces"))
    offsets = spec["periods"]
    asset_digests = Dict{String,String}()
    function field(name,T,dims...)
        values = _read_linked_array(directory,name,T,dims...)
        filename = name*".bin"
        digest = bytes2hex(sha256(reinterpret(UInt8,vec(values))))
        _verify_linked_asset(manifest,filename,digest)
        asset_digests[filename] = digest
        return values
    end
    energy = field("energy",Float64,ne)
    we = field("weights_E",Float64,ne)
    wk = field("weights_k",Float64,nk)
    q = field("Q",ComplexF64,nz,r)
    modes = field("W",ComplexF64,nz*length(offsets),m)
    h = field("H",ComplexF64,m,m,nk)
    hops = field("hop",Float64,nz+1,nk)
    anchor = field("anchor_by_channel",ComplexF64,r,r,nk,length(COLLISION_CHANNELS))
    kernels = LocalCollisionKernels(q,wk,field("acoustic",Float64,nz),field("alloy",Float64,nz),
        field("ifr_sites",Float64,nfaces,nz),field("ifr_pair",Float64,nk,nk),
        field("lo_covariance",ComplexF64,nz,nz,nk,nk),
        field("impurity_covariance",Float64,nz,nz,nk,nk),
        field("LO_plus",Float64,ne,ne),field("LO_minus",Float64,ne,ne),spec["bose"])
    problem = LinkedProblem(energy,we,wk,modes,nb,offsets,spec["voltage"],spec["reach"],
        h,hops,anchor,kernels;spin_degeneracy=spec["g_s"],current_scale=spec["J0"],
        density_scale=spec["density_scale"],target_dimless=spec["target_dimless"])
    seed = field("seed_packed_LG",Float64,r^2,2,ne,nk,length(COLLISION_CHANNELS))
    seed_digest = asset_digests["seed_packed_LG.bin"]
    expected_digest = get(get(spec,"restart",Dict()),"new_seed_sha256",seed_digest)
    seed_digest == expected_digest || error("Packed seed SHA-256 differs from the checkpoint")
    current_midpoints = Float64.(spec["coordinates_of_current_midpoints_nm"])
    length(current_midpoints) == nz+1 && all(isfinite,current_midpoints) &&
        issorted(current_midpoints) ||
        throw(ArgumentError("Archive current cut coordinates do not match the linked geometry"))
    identity = Dict{String,Any}("device"=>spec["device"],"temperature_K"=>spec["physical_T_K"],
        "input_spec_sha256"=>spec_digest,"input_seed_sha256"=>seed_digest,
        "source_geometry_model_sha256"=>spec["source_model_sha"],
        "id"=>_linked_input_id(spec_digest,asset_digests),"asset_sha256"=>asset_digests)
    local_source = spec["source_fresh_sha"]
    if occursin(r"^[0-9a-fA-F]{64}$",local_source)
        identity["input_local_archive_sha256"] = lowercase(local_source)
    else
        identity["input_local_source"] = local_source
    end
    if !isnothing(manifest)
        identity["input_manifest_sha256"] = manifest.digest
    end
    restart_path = joinpath(directory,"restart.json")
    if isfile(restart_path)
        restart_bytes = read(restart_path)
        identity["input_restart_sha256"] = bytes2hex(sha256(restart_bytes))
        restart = YAML.load(String(restart_bytes))
        get(restart,"next_spec_sha256",spec_digest) == spec_digest ||
            error("Specification SHA-256 differs from the archived restart")
        get(restart,"next_seed_sha256",seed_digest) == seed_digest ||
            error("Packed seed SHA-256 differs from the archived restart")
    end
    return (;problem,seed,identity,current_midpoints)
end

function _linked_packed_reference_errors(reference_file, source, problem)
    r,ne,nk = problem.r,problem.ne,problem.nk
    filesize(reference_file) == sizeof(Float64)*length(source) ||
        error("Packed reference length differs from the candidate")
    packed = Array{Float64}(undef,r^2,2,ne)
    frobenius_weights = [ones(r); fill(2.0,r^2-r)]
    errors = Dict{String,Vector{Float64}}()
    open(reference_file,"r") do io
        for (c,channel) in enumerate(COLLISION_CHANNELS)
            diff,base = zeros(2),zeros(2)
            for k in 1:nk
                read!(io,packed)
                @inbounds for e in 1:ne, part in 1:2, i in 1:r^2
                    reference = packed[i,part,e]
                    w = problem.weights[e,k]*frobenius_weights[i]
                    diff[part] += w*abs2(source[i,part,e,k,c]-reference)
                    base[part] += w*abs2(reference)
                end
            end
            errors[String(channel)] = sqrt.(diff./max.(base,1e-300))
        end
    end
    return errors
end

function _linked_observations(reference, candidate)
    profile = candidate["raw_profile_A_cm2"]-reference["raw_profile_A_cm2"]
    seams = candidate["raw_outward_left_right_A_cm2"]-reference["raw_outward_left_right_A_cm2"]
    result = Dict{String,Any}(
        "relative_raw_charge"=>candidate["raw_sheet_cm2"]/reference["raw_sheet_cm2"]-1,
        "raw_lambda_reference_and_candidate"=>[reference["raw_lambda"],candidate["raw_lambda"]],
        "max_absolute_current_profile_A_cm2"=>maximum(abs,profile),
        "seams_difference_A_cm2"=>seams,
        "maximum_spectral_defect"=>[maximum(report["spectral_weight_relative_by_ring"])
            for report in (reference,candidate)])
    ring_charge = "per_ring_raw_sheet_cm2"
    if haskey(reference,ring_charge)
        result["ring_charge_difference_cm2"] = candidate[ring_charge]-reference[ring_charge]
        result["samples_reference_and_candidate"] = [sum(report["sample_count_by_ring"])
            for report in (reference,candidate)]
    end
    return result
end

function _linked_relative_difference(current, old)
    return maximum(abs.(current.-old)./max.(1.,abs.(old)))
end

function _linked_compare_archive(directory, result, problem, identity)
    summary = result.summary
    reference_file = joinpath(directory,"fresh_source_LG_packed.bin")
    summary_path = joinpath(directory,"summary.toml")
    reference = TOML.parsefile(summary_path)
    identity["input_spec_sha256"] == reference["input_spec_sha256"] ||
        error("Candidate and archive differ in input_spec_sha256")
    for key in ("collision_occupation","physical_radial_measure","physical_E_measure_meV")
        summary[key] == reference[key] || error("Candidate and archive differ in $key")
    end
    source_errors = _linked_packed_reference_errors(reference_file, result.source, problem)
    stage_comparisons = Dict(stage=>_linked_observations(reference[stage],summary[stage])
        for stage in ("input","fresh","projected_input","projected_fresh"))
    norm_old,norm_new = (x["input_pair_projection"] for x in (reference,summary))
    normalization = Dict(key=>norm_new[key]-norm_old[key] for key in
        ("a","c","physical_sheet_cm2","profile_A_cm2","outward_left_right_A_cm2"))
    rK_change = abs(summary["weighted_rK"]-reference["weighted_rK"])
    residual_differences = Dict(key=>Dict(part=>_linked_relative_difference(value,reference[key][part])
        for (part,value) in summary[key])
        for key in ("weighted_rSigma_channels_RLG","weighted_rSigma_boundaries_RLG",
            "fresh_channel_balance"))
    # The archived transfer gate uses resolved projections. Nodal and normalized
    # profiles are recorded separately because the raw nodal spectrum can be underresolved.
    gate = all(
        abs(arm["relative_raw_charge"]) <= 5e-9 &&
        arm["max_absolute_current_profile_A_cm2"] <= 1e-3 &&
        maximum(abs,arm["seams_difference_A_cm2"]) <= 1e-3 &&
        maximum(arm["maximum_spectral_defect"]) < 1e-3
        for (stage,arm) in stage_comparisons if startswith(stage,"projected"))
    gate &= maximum(maximum,values(source_errors)) <= 1e-7
    gate &= rK_change <= 1e-8 && abs(normalization["a"]) <= 1e-8 && abs(normalization["c"]) <= 1e-8
    return Dict(
        "archive"=>abspath(directory),"transfer_gate_passed"=>gate,
        "archive_summary_sha256"=>_linked_file_digest(summary_path),
        "archive_fresh_LG_sha256"=>_linked_file_digest(reference_file),
        "observations"=>stage_comparisons,"weighted_source_LG_relative"=>source_errors,
        "normalization_candidate_minus_reference"=>normalization,
        "normalization_relative_charge"=>norm_new["physical_sheet_cm2"]/norm_old["physical_sheet_cm2"]-1,
        "rK_reference_and_candidate"=>[reference["weighted_rK"],summary["weighted_rK"]],
        "scaled_residual_differences"=>residual_differences)
end
