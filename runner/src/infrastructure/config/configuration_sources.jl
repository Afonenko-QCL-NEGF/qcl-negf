"""Собирает один канонический файл конфигурации запуска."""
function _collect_contract_source!(
    source::AbstractString,
    manifests::Vector{String},
    files::Vector{String},
    schema::Dict{String,Any},
)
    isfile(source) || _configuration_error(
        source,
        "configuration source must be a canonical YAML/JSON file",
    )
    canonical=realpath(source)
    basename(canonical)=="manifest.yaml" && _configuration_error(
        source,
        "paired manifest/profile configurations are not supported",
    )
    lowercase(splitext(canonical)[2]) in (".yaml", ".yml", ".json") ||
        _configuration_error(source, "configuration source must use .yaml, .yml, or .json")
    push!(files, canonical)
    return files
end

"""
    validate_configuration_source(sources...;
        schema_path=default_configuration_schema())

Объединяет источники конфигурации в указанном порядке. Каждый источник
представляет собой отдельный документ YAML или JSON. Паспорт модели
предшествует численным настройкам и явным переопределениям. Более поздние
значения заменяют более ранние в тех же конечных узлах.
"""
function validate_configuration_source(
    source::AbstractString,
    additional_sources::AbstractString...;
    schema_path::AbstractString = default_configuration_schema(),
)
    return _validate_configuration_sources((source, additional_sources...); schema_path)
end

function _validate_configuration_sources(
    sources_input;
    schema_path::AbstractString = default_configuration_schema(),
    expected_sha256 = Dict{String,String}(),
    receipts = nothing,
)
    schema = _load_configuration_schema(schema_path)
    manifests = String[]
    files = String[]
    for item in sources_input
        _collect_contract_source!(item, manifests, files, schema)
    end
    isempty(files) &&
        _configuration_error(source, "resolved configuration contains no files")

    merged = Dict{String,Any}()
    sources = Dict{String,Vector{String}}()
    for file in files
        bytes = read(file)
        expected = get(expected_sha256, file, nothing)
        if expected !== nothing || receipts !== nothing
            digest = bytes2hex(sha256(bytes))
            expected === nothing || digest == expected ||
                throw(ArgumentError("device source does not match its catalog: $(basename(file))"))
            receipts === nothing || push!(receipts, Dict("name" => basename(file), "sha256" => digest))
        end
        _deep_merge!(merged, _parse_yaml_mapping(bytes, file), sources, file)
    end
    _validate_schema_node(merged, schema, schema)
    schema_id = String(get(schema, "\$id", basename(schema_path)))
    provenance = ConfigurationProvenance(manifests, files, sources)
    return ValidatedConfigurationDocument(
        merged,
        provenance,
        schema_id,
        realpath(schema_path),
    )
end

function validate_configuration_source(
    sources::AbstractVector{<:AbstractString};
    schema_path::AbstractString = default_configuration_schema(),
)
    isempty(sources) &&
        _configuration_error("sources", "at least one configuration source is required")
    return validate_configuration_source(first(sources), sources[2:end]...; schema_path)
end

"""
    load_configuration_source(sources...; schema_path=...)

Загружает конфигурацию и возвращает `ResolvedRunConfiguration`. Сначала
проверяет объединённый документ по схеме, затем преобразует данные в
строго типизированные объекты решателя.
"""
function load_configuration_source(
    source::AbstractString,
    additional_sources::AbstractString...;
    schema_path::AbstractString = default_configuration_schema(),
)
    document = validate_configuration_source(source, additional_sources...; schema_path)
    return _resolve_configuration(document.data, document.provenance)
end

function load_configuration_source(
    sources::AbstractVector{<:AbstractString};
    schema_path::AbstractString = default_configuration_schema(),
)
    document = validate_configuration_source(sources; schema_path)
    return _resolve_configuration(document.data, document.provenance)
end
