module ScientificPlanContracts
using Test
using YAML
using QCLNEGFRunner
using SHA
using Unitful

@testset "Field-authored study has one canonical bias in the point passport" begin
    mktempdir() do directory
        examples = normpath(joinpath(@__DIR__, "..", "..", "examples", "config"))
        configuration = YAML.load_file(joinpath(examples, "reference-2019-70k.yaml"))
        physical = configuration["physical"]
        delete!(physical, "voltage_per_period")
        physical["field_bias"] = "21 kV/cm"
        source_path = joinpath(directory, "field.yaml")
        YAML.write_file(source_path, configuration)
        source = load_run_configuration(source_path)
        period_m = ustrip(u"m", QCLNEGFRunner.period_length(source.physical))
        voltage = 2.1e6 * period_m

        study = YAML.load_file(joinpath(examples, "operator-algebra.yaml"))
        study["configuration"]["sources"] = [source_path]
        study["axes"]["voltages"] = Dict("values" => [voltage], "unit" => "V")
        definition = joinpath(directory, "study.yaml")
        YAML.write_file(definition, study)
        plan = resolve_scientific_plan(definition)
        frozen = scientific_plan_dict(plan)
        @test only(load_scientific_plan(frozen).points).voltage_per_period_V ≈ voltage
        passport = only(frozen["points"])["effective_inputs"]
        @test passport["field_V_per_m"] ≈ 2.1e6
        @test passport["period_length_m"] ≈ period_m

        workflow = QCLNEGFRunner.QCLScientificWorkflow
        point_configuration = workflow._point_resolved_raw(
            only(plan.executions).configuration, only(plan.points),
        )
        @test !haskey(point_configuration["physical"], "field_bias")
        point_path = joinpath(directory, "point.yaml")
        YAML.write_file(point_path, point_configuration)
        @test ustrip(u"V/m", load_run_configuration(point_path).physical.F_bias) ≈ 2.1e6
        point_configuration["physical"]["field_bias"] = "21 kV/cm"
        YAML.write_file(point_path, point_configuration)
        @test_throws QCLNEGFRunner.ConfigurationError load_run_configuration(point_path)
    end
end

@testset "Scientific plan freeze, shared inclusions and explicit repeats" begin
    base=normpath(joinpath(@__DIR__, "..", "fixtures", "research-inputs", "model", "reference-2019-70k.yaml"))
    mktempdir() do directory
        function write_definition(name, value)
            written_path=joinpath(directory, name*".yaml")
            YAML.write_file(written_path, value)
            return written_path
        end
        study=Dict{String,Any}(
            "schema"=>"qcl-negf-study-v2",
            "kind"=>"study",
            "id"=>"test-study",
            "operation"=>"operator_algebra",
            "configuration"=>Dict("sources"=>[base]),
            "axes"=>Dict(
                "temperatures"=>Dict("values"=>[70], "unit"=>"K"),
                "voltages"=>Dict("values"=>[50, 56], "unit"=>"mV"),
            ),
        )
        study_path=write_definition("study", study)
        meta=Dict{String,Any}(
            "schema"=>"qcl-negf-study-v2",
            "kind"=>"meta",
            "id"=>"test-meta",
            "includes"=>["study.yaml", "study.yaml"],
        )
        path=write_definition("meta", meta)
        plan=resolve_scientific_plan(path)
        @test length(plan.points)==2
        @test length(plan.executions)==2
        @test length(plan.inclusions)==3
        @test plan.inclusions[2].id!=plan.inclusions[3].id
        @test plan.inclusions[2].execution_ids==plan.inclusions[3].execution_ids
        @test all(p->p.temperature_K==70 && p.predecessor_id===nothing, plan.points)
        @test plan.executions[1].configuration.solver.max_scba==2000
        @test plan.executions[1].configuration.solver.convergence.mode===:research_continue
        frozen=scientific_plan_dict(plan)
        renamed=deepcopy(frozen)
        renamed["name"]="Different display title"
        renamed["executions"][1]["label"]="Translated label"
        @test QCLNEGFRunner.QCLScientificWorkflow._scientific_fingerprint(renamed)==frozen["scientific_fingerprint"]
        @test QCLNEGFRunner.QCLScientificWorkflow._plan_fingerprint(renamed)!=frozen["fingerprint"]
        study["axes"]["voltages"]["values"]=[64]
        write_definition("study", study)
        loaded=load_scientific_plan(frozen)
        @test length(loaded.points)==2
        @test [p.voltage_per_period_V for p in loaded.points]≈[0.050, 0.056]
        altered=deepcopy(frozen)
        altered["points"][1]["voltage_per_period_V"]=0.9
        @test_throws ArgumentError load_scientific_plan(altered)
        @test_throws ArgumentError resolve_scientific_plan(path; maximum_solver_runs = 0)
        study["axes"]["voltages"]["values"]=[50, 56]
        study["policies"]=Dict(
            "voltage"=>Dict("mode"=>"strict", "invalid_predecessor"=>"cold_start"),
        )
        write_definition("study", study)
        continuation=resolve_scientific_plan(study_path)
        @test continuation.points[2].predecessor_id==continuation.points[1].id
        @test continuation.points[2].initialization===:predecessor
        @test_throws ArgumentError resolve_scientific_plan(
            study_path;
            maximum_solver_runs = 1,
        )
        study["repetitions"]=2
        write_definition("study", study)
        @test_throws ArgumentError resolve_scientific_plan(study_path)
        study["purpose"]="reproducibility"
        write_definition("study", study)
        repeats=resolve_scientific_plan(path)
        @test length(repeats.executions)==4
        @test length(repeats.points)==8
        @test length(unique(p.id for p in repeats.points))==8
        meta["includes"]=["meta.yaml"]
        write_definition("meta", meta)
        error=try
            resolve_scientific_plan(path)
            nothing
        catch caught
            caught
        end
        @test error isa ArgumentError
        @test occursin("cycle", sprint(showerror, error))
        meta["includes"]=["missing.yaml"]
        write_definition("meta", meta)
        @test_throws ArgumentError resolve_scientific_plan(path)
        study["axes"]["temperatures"]["values"]=[200]
        write_definition("study", study)
        @test all(p->p.temperature_K==200, resolve_scientific_plan(study_path).points)
        study["axes"]["temperatures"]["question"]="explicit temperature dependence"
        write_definition("study", study)
        @test all(p->p.temperature_K==200, resolve_scientific_plan(study_path).points)
        missing_axes = deepcopy(study)
        delete!(missing_axes, "axes")
        write_definition("missing-axes", missing_axes)
        @test_throws ArgumentError resolve_scientific_plan(joinpath(directory, "missing-axes.yaml"))
        for field in ("admission", "campaign")
            unsupported = deepcopy(study)
            unsupported[field] = Dict("stage_id" => "hidden-policy")
            write_definition("unsupported", unsupported)
            @test_throws ArgumentError resolve_scientific_plan(joinpath(directory, "unsupported.yaml"))
        end
        external_policy = deepcopy(frozen)
        external_policy["campaign"] = Dict("maximum_active_executions" => 2)
        external_policy["scientific_fingerprint"] = QCLNEGFRunner.QCLScientificWorkflow._scientific_fingerprint(external_policy)
        external_policy["fingerprint"] = QCLNEGFRunner.QCLScientificWorkflow._plan_fingerprint(external_policy)
        @test_throws ArgumentError load_scientific_plan(external_policy)
    end
end

@testset "Frozen plan captures defaults, units, implementation, and separate temperatures" begin
    examples = normpath(joinpath(@__DIR__, "..", "..", "examples", "config"))
    original = YAML.load_file(joinpath(examples, "reference-2019-70k.yaml"))
    definition = YAML.load_file(joinpath(examples, "operator-algebra.yaml"))
    workflow = QCLNEGFRunner.QCLScientificWorkflow
    function rehash!(frozen)
        frozen["scientific_fingerprint"] = workflow._scientific_fingerprint(frozen)
        frozen["fingerprint"] = workflow._plan_fingerprint(frozen)
        return frozen
    end
    mktempdir() do directory
        source = joinpath(directory, "initial.yaml")
        definition["configuration"]["sources"] = [source]
        original["physical"]["interface_roughness_height"] = "1 nm"
        original["physical"]["ionization_fraction"] = 1
        original["physical"]["lo_temperature"] = "200 K"
        YAML.write_file(source, original)
        first = scientific_plan_dict(resolve_scientific_plan(definition; base_directory=directory))
        values = only(first["executions"])["resolved_configuration"]
        @test values["algorithms"]["embedding"] == "full_cell_resolvent"
        @test values["kernel_construction"]["impurity_angular_tolerance"] > 0
        @test values["solver"]["convergence"]["trend"]["window"] > 0
        @test only(first["points"])["effective_inputs"]["lo_temperature_K"] == 200
        @test only(first["points"])["effective_inputs"]["axes_applied"] === false
        @test only(first["points"])["effective_inputs"]["axis_source"] == "fixed_operator_fixture"
        @test length(first["implementation"]["core"]["source_tree_sha256"]) == 64

        relocated = mkpath(joinpath(directory, "relocated"))
        source_changed = joinpath(relocated, "initial.yaml")
        original["physical"]["interface_roughness_height"] = "10 Å"
        original["physical"]["ionization_fraction"] = 1.0
        original["run"]["name"] = "another run"
        original["output"]["directory"] = "elsewhere"
        original["production"]["worker_count"] = 2
        YAML.write_file(source_changed, original)
        definition["configuration"]["sources"] = [source_changed]
        equivalent = scientific_plan_dict(resolve_scientific_plan(definition; base_directory=directory))
        @test equivalent["scientific_fingerprint"] == first["scientific_fingerprint"]
        diff = compare_scientific_plans(first, equivalent)
        @test isempty(diff["science"]) && isempty(diff["implementation"])
        @test !diff["same_frozen_plan"]

        definition["configuration"]["overrides"] = Dict("numerical" => Dict("basis_states" => 8))
        altered = scientific_plan_dict(resolve_scientific_plan(definition; base_directory=directory))
        @test only(compare_scientific_plans(first, altered)["science"])["path"] ==
              "/executions/1/inputs/numerical/basis_states"

        delete!(definition["configuration"], "overrides")
        definition["axes"]["temperatures"]["values"] = [70, 160]
        definition["axes"]["lo_temperatures"] = Dict("unit" => "K", "values" => [70])
        fixed_lo = scientific_plan_dict(resolve_scientific_plan(definition; base_directory=directory))
        @test [point["lo_temperature_K"] for point in fixed_lo["points"]] == [70, 70]
        delete!(definition["axes"], "lo_temperatures")
        definition["axes"]["temperatures"]["values"] = [70]
        original["physical"]["field_bias"] = "21 kV/cm"
        delete!(original["physical"], "voltage_per_period")
        YAML.write_file(source_changed, original)
        field = scientific_plan_dict(resolve_scientific_plan(definition; base_directory=directory))
        @test field["scientific_fingerprint"] == first["scientific_fingerprint"]

        changes = Dict("numerical" => Dict("basis_states" => 8, "angular_nodes" => 48))
        definition["variants"] = [Dict(
            "id" => "changed", "overrides" => changes, "controlled_paths" => ["numerical"],
        )]
        @test_throws ArgumentError resolve_scientific_plan(definition; base_directory=directory)
        definition["variants"][1]["controlled_paths"] = ["numerical.basis_states"]
        @test_throws ArgumentError resolve_scientific_plan(definition; base_directory=directory)

        rm(source)
        rm(source_changed)
        @test scientific_plan_dict(load_scientific_plan(first)) == first

        incomplete = deepcopy(first)
        delete!(only(incomplete["executions"])["resolved_configuration"]["algorithms"], "embedding")
        @test_throws ArgumentError load_scientific_plan(rehash!(incomplete))

        foreign = deepcopy(first)
        foreign["implementation"]["core"]["source_tree_sha256"] = repeat("0", 64)
        rehash!(foreign)
        @test isempty(compare_scientific_plans(first, foreign)["science"])
        @test length(compare_scientific_plans(first, foreign)["implementation"]) == 1
        @test_throws ArgumentError load_scientific_plan(foreign)

        v2 = deepcopy(first)
        v2["schema"] = "qcl-negf-scientific-plan-v2"
        @test_throws ArgumentError load_scientific_plan(rehash!(v2))
    end
end

@testset "Short device and method names bind verified author inputs" begin
    examples = normpath(joinpath(@__DIR__, "..", "..", "examples", "config"))
    definition = YAML.load_file(joinpath(examples, "operator-algebra.yaml"))
    mktempdir() do directory
        source = joinpath(directory, "initial.yaml")
        cp(joinpath(examples, "reference-2019-70k.yaml"), source)
        digest = bytes2hex(open(sha256, source))
        catalog = Dict(
            "schema" => "qcl-negf-device-catalog-v1",
            "devices" => Dict("example" => [Dict("path"=>"initial.yaml", "sha256"=>digest)]),
        )
        catalog_path = joinpath(directory, "catalog.yaml")
        YAML.write_file(catalog_path, catalog)
        definition["configuration"] = Dict("device"=>"example", "catalog"=>"catalog.yaml")
        definition["variants"] = [Dict("id"=>"first", "method_id"=>"operator_algebra")]
        plan = scientific_plan_dict(resolve_scientific_plan(definition; base_directory=directory))
        execution = only(plan["executions"])
        @test execution["author_inputs"] == [Dict("name"=>"initial.yaml", "sha256"=>digest)]
        @test execution["method_id"] == "operator_algebra"
        definition["variants"][1]["method_id"] = "missing-method"
        @test_throws ArgumentError resolve_scientific_plan(definition; base_directory=directory)
        definition["variants"][1]["method_id"] = "operator_algebra"
        open(io->println(io, "# changed"), source, "a")
        @test_throws ArgumentError resolve_scientific_plan(definition; base_directory=directory)
        rm(source)
        rm(catalog_path)
        @test scientific_plan_dict(load_scientific_plan(plan)) == plan
    end
end

@testset "Offline derivative and analytic campaign ledger" begin
    voltage=[0.0, 0.3, 0.9, 1.4]
    derivative=differential_conductance(voltage, voltage .^ 2)
    @test derivative[2:3]≈2voltage[2:3]
    @test_throws ArgumentError differential_conductance([1.0, 1.0], [2.0, 3.0])
    @test_throws ArgumentError differential_conductance([1.0, 2.0], [NaN, 3.0])
    for operation in (:operator_algebra, :operator_metrics, :operator_representation)
        ledger=QCLNEGFRunner.QCLScientificWorkflow.run_operator_diagnostics(operation)
        @test !isempty(ledger)
        @test all(row["passed"] for row in ledger)
    end
end


@testset "Attempt history survives repeated resumes and explicit operator reruns" begin
    fixture=normpath(joinpath(@__DIR__, "..", "fixtures", "research-inputs", "studies", "operator-a.yaml"))
    plan=resolve_scientific_plan(fixture)
    mktempdir() do directory
        snapshots=String[]
        for attempt = 1:3
            result=execute_scientific_plan(plan, directory; resume = false)
            @test only(result["points"])["attempt"]==attempt
            snapshot=joinpath(directory, only(result["points"])["data"]["operator_checks"])
            push!(snapshots, snapshot)
            @test isfile(snapshot)
            resumed=execute_scientific_plan(plan, directory; resume = true)
            @test only(resumed["points"])["attempt"]==attempt
            stored=YAML.load_file(
                joinpath(directory, "series_result.json");
                dicttype = Dict{String,Any},
            )
            @test [point["attempt"] for point in stored["attempt_history"]]==collect(1:attempt)
        end
        @test length(unique(snapshots))==3
        @test all(isfile, snapshots)
        # A crash after publication may leave only the durable history indexed.
        stored=YAML.load_file(
            joinpath(directory, "series_result.json");
            dicttype = Dict{String,Any},
        )
        stored["points"]=Any[]
        stored["available_point_count"]=0
        stored["status"]="running"
        open(joinpath(directory, "series_result.json"), "w") do io
            write_scientific_result(io, stored)
        end
        recovered=execute_scientific_plan(plan, directory; resume = false)
        @test only(recovered["points"])["attempt"]==4
        @test all(isfile, snapshots)
        orphan=joinpath(
            directory,
            "executions",
            only(plan.executions).id,
            only(plan.points).id,
            "attempt-5",
            "operator_checks.json",
        )
        mkpath(dirname(orphan))
        write(orphan, "interrupted attempt evidence")
        recovered=execute_scientific_plan(plan, directory; resume = false)
        @test only(recovered["points"])["attempt"]==6
        @test read(orphan, String)=="interrupted attempt evidence"
        @test all(isfile, snapshots)
        # Existing files and valid hashes cannot authorize a pre-v3 cached result.
        point=only(recovered["points"])
        commit_path=joinpath(directory, point["data"]["result_commit"])
        commit=YAML.load_file(commit_path; dicttype = Dict{String,Any})
        artifact=only(commit["artifacts"])
        payload_path=joinpath(dirname(commit_path), artifact["path"])
        payload=YAML.load_file(payload_path; dicttype = Dict{String,Any})
        payload["schema"]="qcl-negf-operator-diagnostics-v2"
        payload["schema_version"]="2.0"
        open(payload_path, "w") do io
            QCLNEGFRunner._light_json(io, payload)
        end
        artifact["schema"]=payload["schema"]
        artifact["bytes"]=filesize(payload_path)
        artifact["sha256"]=bytes2hex(open(sha256, payload_path))
        open(commit_path, "w") do io
            QCLNEGFRunner._light_json(io, commit)
        end
        @test_throws ArgumentError execute_scientific_plan(plan, directory; resume = true)
    end
end

end # module ScientificPlanContracts
