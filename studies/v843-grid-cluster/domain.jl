# Paired observation-domain control for a single frozen V843 spectrum plan.
# The common helper builds H and W once and applies both domain choices to them.
include(joinpath(@__DIR__, "..", "v843-spectrum", "domain-control.jl"))

function grid_domain_main()
    length(ARGS) == 3 || error("Usage: domain.jl PLAN b11-pzp|w11-wannier-proxy OUTPUT")
    plan_path, preset, output = ARGS
    half_window, localization = if preset == "b11-pzp"
        (5, :pzp_tails)
    elseif preset == "w11-wannier-proxy"
        (4, :bloch_wannier)
    else
        error("unknown domain preset")
    end
    !ispath(output) || error("domain output already exists")
    source_sha = bytes2hex(open(sha256, plan_path))
    plan = load_scientific_plan(plan_path) # validates plan and scientific fingerprints
    bytes2hex(open(sha256, plan_path)) == source_sha || error("plan changed while loading")
    execution = only(plan.executions)
    point = only(plan.points)
    execution.operation === :structure_spectrum || error("expected structure_spectrum")
    point.execution_id == execution.id && execution.point_ids == [point.id] || error("point/execution mismatch")
    execution.author_device == "dupont-v843" || error("unexpected device")
    sources = Dict(
        "reference-2019-70k.yaml" => joinpath(@__DIR__, "..", "..", "runner", "examples", "config", "reference-2019-70k.yaml"),
        "dupont-v843.yaml" => joinpath(@__DIR__, "..", "v843-spectrum", "dupont-v843.yaml"),
    )
    length(execution.author_inputs) == length(sources) || error("unexpected author inputs")
    author_hashes = Dict(input["name"] => input["sha256"] for input in execution.author_inputs)
    length(author_hashes) == length(sources) && Set(keys(author_hashes)) == Set(keys(sources)) ||
        error("unexpected or duplicate author input names")
    for (name, path) in sources
        bytes2hex(open(sha256, path)) == author_hashes[name] || error("author source SHA mismatch: $name")
    end
    workflow = QCLNEGFRunner.QCLScientificWorkflow
    configuration = execution.configuration
    raw = workflow._point_resolved_raw(configuration, point)
    resolved = QCLNEGFRunner._resolve_configuration(raw, configuration.provenance)
    p, n, s = resolved.physical, resolved.numerical, resolved.scales
    n.N_z in (96, 144, 216, 288) || error("unexpected spatial grid")
    n.P_basis == half_window && n.N_b == 11 || error("preset and basis disagree")
    expected_id = "b$(2half_window + 1)-r11-z$(n.N_z)"
    plan.root_definition_id == expected_id && execution.definition_id == expected_id || error("unexpected plan identity")
    thickness_nm = [ustrip(u"nm", layer.d) for layer in p.layers]
    all(isapprox.(thickness_nm, [4.4, 6.25, 1.09, 6.65, 2.28, 8.48, 0.91, 6.1]; atol=1e-9, rtol=0)) || error("unexpected V843 geometry")
    isapprox(ustrip(u"kV/cm", p.F_bias), 21.0; atol=1e-9, rtol=0) || error("unexpected field")
    isapprox(point.voltage_per_period_V, 0.075936; atol=1e-10, rtol=0) || error("unexpected voltage")
    point.temperature_K == point.lo_temperature_K == 50.0 || error("unexpected temperature")
    report = rank11_observation_control(p, n, s, localization)
    report["configuration_source_plan_fingerprint"] = plan.fingerprint
    report["configuration_source_plan_sha256"] = source_sha
    report["configuration_source_execution_id"] = execution.id
    report["configuration_source_point_id"] = point.id
    report["voltage_per_period_V"] = point.voltage_per_period_V
    report["temperature_K"] = point.temperature_K
    report["lo_temperature_K"] = point.lo_temperature_K
    report["driver_sha256"] = bytes2hex(open(sha256, @__FILE__))
    report["helper_sha256"] = bytes2hex(open(sha256, joinpath(@__DIR__, "..", "v843-spectrum", "domain-control.jl")))
    report["case"] = preset
    open(output, "w") do io
        TOML.print(io, report)
    end
end

grid_domain_main()
