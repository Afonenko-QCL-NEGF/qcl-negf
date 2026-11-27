"""Хранит скалярную историю в закрытых типизированных сегментах. Каждая принятая итерация записывается один раз."""
mutable struct ScientificHistoryRecorder
    directory::String
    identity::Dict{String,Any}
    scba_count::Base.RefValue{Int}
    outer_count::Base.RefValue{Int}
    scba::Vector{Tuple{Int,Int,SCBAIteration}}
    outer::Vector{Tuple{Int,OuterIteration}}
    segment::Int
    problem_id::String
    segments::Vector{Dict{String,Any}}
    published_scba::Int
    published_outer::Int
    flush_interval_ns::UInt64
    last_flush_ns::UInt64
    clock_ns::Function
    grid::Union{Nothing,SolverHistoryGrid}
end

function ScientificHistoryRecorder(
    directory,
    identity,
    scba_count,
    outer_count;
    flush_interval_seconds::Real = 30,
    clock_ns::Function = time_ns,
)
    isfinite(flush_interval_seconds) && flush_interval_seconds>0 || throw(
        ArgumentError("scientific history flush interval must be finite and positive"),
    )
    root=joinpath(directory, "history")
    mkpath(root)
    return ScientificHistoryRecorder(
        root,
        identity,
        scba_count,
        outer_count,
        Tuple{Int,Int,SCBAIteration}[],
        Tuple{Int,OuterIteration}[],
        0,
        "",
        Dict{String,Any}[],
        0,
        0,
        round(UInt64, flush_interval_seconds*1e9),
        UInt64(clock_ns()),
        clock_ns,
        nothing,
    )
end

function record_scientific_history!(
    recorder::ScientificHistoryRecorder,
    kind,
    outer,
    row,
    grid::SolverHistoryGrid,
)
    # A domain rebuild starts a new segment; metadata identifies the actual grid.
    previous = recorder.grid
    if previous === nothing ||
       previous.energy_eV != grid.energy_eV ||
       previous.momentum_per_nm != grid.momentum_per_nm ||
       previous.spatial_nodes != grid.spatial_nodes ||
       previous.energy_scale_eV != grid.energy_scale_eV ||
       previous.length_scale_m != grid.length_scale_m
        previous === nothing || flush_scientific_history!(recorder)
        recorder.problem_id = bytes2hex(sha256(sprint(
            _light_json,
            (; grid.energy_eV, grid.momentum_per_nm, grid.spatial_nodes,
               grid.energy_scale_eV, grid.length_scale_m),
        )))
        recorder.grid = grid
    end
    if kind===:scba
        recorder.scba_count[]+=1
        push!(recorder.scba, (recorder.scba_count[], outer, row))
    else
        recorder.outer_count[]+=1
        push!(recorder.outer, (recorder.outer_count[], row))
    end
    # Presentation follows durable closed scalar segments. Its cadence does not
    # request expensive matrix checkpoints or alter solver iteration limits.
    if length(recorder.scba)+length(recorder.outer)>=1000 ||
       UInt64(recorder.clock_ns())-recorder.last_flush_ns>=recorder.flush_interval_ns
        flush_scientific_history!(recorder)
    end
    return nothing
end

record_scientific_history!(recorder, kind, outer, row, problem::NEGFProblem) =
    record_scientific_history!(recorder, kind, outer, row, SolverHistoryGrid(problem))

function flush_scientific_history!(recorder::ScientificHistoryRecorder)
    isempty(recorder.scba) && isempty(recorder.outer) && return nothing
    recorder.segment+=1
    destination=joinpath(
        recorder.directory,
        "segment-"*lpad(string(recorder.segment), 6, '0')*".h5",
    )
    temporary, io=mktemp(recorder.directory)
    close(io)
    try
        h5open(temporary, "w") do file
            metadata=create_group(file, "metadata")
            metadata["toolchain_json"] =
                sprint(_light_json, _runtime_toolchain_provenance())
            attributes(metadata)["schema"]="qcl-negf-scientific-history-v4"
            attributes(metadata)["schema_version"]=_CHECKPOINT_SCHEMA_VERSION
            attributes(metadata)["contract_set"]=_RESULT_CONTRACT_SET
            attributes(metadata)["artifact_role"]="science.history"
            attributes(metadata)["scba_rows"]=length(recorder.scba)
            attributes(metadata)["outer_rows"]=length(recorder.outer)
            attributes(metadata)["domain_identity"]=recorder.problem_id
            metadata["identity_json"]=sprint(_light_json, recorder.identity)
            for kind in (:scba, :outer)
                group=create_group(file, String(kind))
                rows=kind===:scba ? recorder.scba : recorder.outer
                group["sequence"]=Int64[first(item) for item in rows]
                if kind===:scba
                    group["outer_iteration"]=Int64[item[2] for item in rows]
                    group["iteration"]=Int64[last(item).ν for item in rows]
                    for field in fieldnames(SCBAIteration)[2:end]
                        fieldtype(SCBAIteration, field)<:Real || continue
                        _physical_dataset(
                            group,
                            String(field),
                            Float64[getfield(last(item), field) for item in rows];
                            units = field===:J ? "A/m^2" : "dimensionless",
                            axes = "iteration",
                            description = "Complete accepted SCBA $(field)",
                        )
                    end
                else
                    group["iteration"]=Int64[last(item).μ for item in rows]
                    for field in fieldnames(OuterIteration)[2:10]
                        _physical_dataset(
                            group,
                            String(field),
                            Float64[getfield(last(item), field) for item in rows];
                            units = field===:J ? "A/m^2" : "dimensionless",
                            axes = "iteration",
                            description = "Complete outer diagnostic $(field)",
                        )
                    end
                end
            end
            _write_psd_history!(
                file,
                SCBAIteration[last(item) for item in recorder.scba];
                grid = recorder.grid,
                sequences = Int64[first(item) for item in recorder.scba],
            )
            _write_physical_markers!(
                file,
                SCBAIteration[last(item) for item in recorder.scba];
                sequences = Int64[first(item) for item in recorder.scba],
            )
            _annotate_physics_tree!(file)
        end
        chmod(temporary, 0o640)
        _sync_artifact_file(temporary)
        mv(temporary, destination; force = false)
        _sync_artifact_directory(recorder.directory)
        scba_rows=length(recorder.scba)
        outer_rows=length(recorder.outer)
        push!(
            recorder.segments,
            Dict{String,Any}(
                "path"=>basename(destination),
                "sha256"=>bytes2hex(open(sha256, destination)),
                "bytes"=>filesize(destination),
                "scba_rows"=>scba_rows,
                "outer_rows"=>outer_rows,
            ),
        )
        recorder.published_scba+=scba_rows
        recorder.published_outer+=outer_rows
        pointer=joinpath(recorder.directory, "index.json")
        index=Dict(
            "schema"=>"qcl-negf-scientific-history-index-v2",
            "contract_set"=>_RESULT_CONTRACT_SET,
            "identity"=>recorder.identity,
            "generation"=>recorder.segment,
            "updated_unix"=>time(),
            "scba_rows"=>recorder.published_scba,
            "outer_rows"=>recorder.published_outer,
            "segments"=>recorder.segments,
        )
        _observability_atomic_text(pointer) do io
            _light_json(io, index)
            println(io)
        end
        _sync_artifact_file(pointer)
        _sync_artifact_directory(recorder.directory)
        recorder.last_flush_ns=UInt64(recorder.clock_ns())
        empty!(recorder.scba)
        empty!(recorder.outer)
    finally
        isfile(temporary) && rm(temporary; force = true)
    end
    return destination
end

scientific_history_sources(recorder::ScientificHistoryRecorder) =
    [joinpath(recorder.directory, segment["path"]) for segment in recorder.segments]

function _history_boundary(file)
    boundary = Dict{String,Int}()
    for kind in ("scba", "outer")
        sequence = file[kind * "/sequence"]
        rows = Int(read_attribute(file["metadata"], kind * "_rows"))
        rows == length(sequence) ||
            throw(ArgumentError("saved $kind history length differs from its metadata"))
        last_sequence = rows == 0 ? 0 : Int(sequence[rows])
        last_sequence == rows ||
            throw(ArgumentError("saved $kind history does not end at its declared sequence"))
        boundary[kind * "_sequence"] = last_sequence
    end
    return boundary
end

"""Возвращает только историю, включённую в уже проверенное поколение контрольной точки."""
function scientific_history_prefix(commit_path, commit)
    boundary = get(commit, "history_boundary", nothing)
    boundary === nothing && return (paths = String[], scba = 0, outer = 0)
    history = only(item for item in commit["artifacts"] if item["role"] == "science.history")
    return (
        paths = [joinpath(dirname(commit_path), history["path"])],
        scba = Int(boundary["scba_sequence"]),
        outer = Int(boundary["outer_sequence"]),
    )
end

"""Собирает проверенный префикс и закрытые сегменты текущей попытки с исходными идентификаторами."""
function consolidate_scientific_history(destination, paths)
    isempty(paths) && throw(
        ArgumentError(
            "native v4 consolidation requires at least one closed history segment",
        ),
    )
    tables=Dict("scba"=>Dict{String,Any}(), "outer"=>Dict{String,Any}())
    sources=Any[]
    for path in paths
        h5open(path, "r") do file
            _require_native_metadata(file, "qcl-negf-scientific-history-v4")
            _require_native_scba_tables(file)
            metadata=file["metadata"]
            if haskey(metadata, "source_segments_json")
                prior = YAML.load(String(read(metadata["source_segments_json"])))
                prior isa AbstractVector ||
                    throw(ArgumentError("consolidated history does not identify its source segments"))
                append!(sources, prior)
            else
                push!(sources, Dict(
                    "sha256"=>bytes2hex(open(sha256, path)),
                    "identity"=>YAML.load(
                        String(read(metadata["identity_json"]));
                        dicttype = Dict{String,Any},
                    ),
                    "domain_identity"=>String(read_attribute(metadata, "domain_identity")),
                    "scba_rows"=>Int(read_attribute(metadata, "scba_rows")),
                    "scba_sequence_first"=>(
                        length(file["scba/sequence"])==0 ? nothing :
                        Int(file["scba/sequence"][1])
                    ),
                    "scba_sequence_last"=>(
                        length(file["scba/sequence"])==0 ? nothing :
                        Int(file["scba/sequence"][length(file["scba/sequence"])])
                    ),
                    "outer_rows"=>Int(read_attribute(metadata, "outer_rows")),
                ))
            end
            for kind in ("scba", "outer"), name in keys(file[kind])
                values=read(file[kind][name])
                append!(get!(tables[kind], name, eltype(values)[]), values)
            end
        end
    end
    h5open(destination, "w") do file
        metadata=create_group(file, "metadata")
        metadata["toolchain_json"] = sprint(_light_json, _runtime_toolchain_provenance())
        attributes(metadata)["schema"]="qcl-negf-scientific-history-v4"
        attributes(metadata)["schema_version"]=_CHECKPOINT_SCHEMA_VERSION
        attributes(metadata)["contract_set"]=_RESULT_CONTRACT_SET
        attributes(metadata)["artifact_role"]="science.history"
        attributes(metadata)["representation"]="committed history prefix and closed segments of the current attempt"
        metadata["source_segments_json"]=sprint(_light_json, sources)
        for kind in ("scba", "outer")
            table=tables[kind]
            group=create_group(file, kind)
            sequence=get(table, "sequence", Int64[])
            order=sortperm(sequence)
            sequence[order] == collect(1:length(sequence)) ||
                throw(ArgumentError("scientific history sequence must be contiguous and point-local"))
            attributes(metadata)[kind*"_rows"]=length(sequence)
            for (name, values) in table
                _physical_dataset(
                    group,
                    name,
                    values[order];
                    units = name=="J" ? "A/m^2" : "dimensionless",
                    axes = "iteration",
                    description = "Complete $(kind) $(name), ordered by the point sequence",
                )
            end
        end
        _consolidate_psd_history!(file, paths)
        _consolidate_physical_markers!(file, paths)
        _annotate_physics_tree!(file)
    end
    return destination
end
