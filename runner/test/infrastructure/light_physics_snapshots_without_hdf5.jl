module NativePhysicsArtifactContracts
include("../support/common.jl")
using HDF5, SHA
include("../support/native_physics_fixture.jl")

@testset "Scientific status records the measured axes" begin
    status = QCLNEGFRunner._point_scientific_status
    assessment = Dict{String,Any}(
        "iterative_converged"=>true,
        "stationary_candidate_accepted"=>true,
        "discretization_verified"=>"not_measured",
        "metrics"=>Dict(
            "fixed_point"=>Dict("category"=>"nonlinear_fixed_point", "status"=>"pass"),
            "charge"=>Dict("category"=>"physical_and_algebraic", "status"=>"pass"),
        ),
    )
    result = status(:completed; assessment)
    @test result["process"] == "completed"
    @test result["iterative_convergence"] == result["physical_candidate"] == "passed"
    @test result["discretization"] == result["campaign_verdict"] == result["operator"] == "unknown"

    assessment["stationary_candidate_accepted"] = false
    assessment["metrics"]["charge"]["status"] = "not_measured"
    @test status(:completed; assessment)["physical_candidate"] == "unknown"
    assessment["metrics"]["charge"]["status"] = "fail"
    @test status(:completed; assessment)["physical_candidate"] == "failed"
end

@testset "Native physics, immutable commits and explicit scientific capabilities" begin
    solution=native_physics_fixture()
    original=copy(solution.scba.green.Gˡ)
    identity=Dict{String,Any}(
        "point_id"=>"point-1",
        "execution_id"=>"execution-1",
        "attempt"=>1,
        "plan_fingerprint"=>"fixture",
    )
    mktempdir() do directory
        first_commit=QCLNEGFRunner.commit_point_artifacts(
            directory,
            solution;
            identity,
            algorithms = AlgorithmOptions(),
        )
        first_bytes=read(first_commit)
        manifest=QCLNEGFRunner.verify_point_artifacts(first_commit)
        @test Set(a["role"] for a in manifest["artifacts"])==Set([
            "physics.full",
            "physics.analysis",
            "recovery",
        ])
        @test manifest["scientific_status"]["discretization"] == "unknown"
        @test manifest["scientific_status"]["campaign_verdict"] == "unknown"
        @test !manifest["presentation_ready"]
        wrong_status = deepcopy(manifest)
        wrong_status["scientific_status"]["campaign_verdict"] = "accepted"
        invalid_path = joinpath(dirname(first_commit), "invalid_status.json")
        open(invalid_path, "w") do io
            QCLNEGFRunner._light_json(io, wrong_status)
        end
        @test_throws ArgumentError QCLNEGFRunner.verify_point_artifacts(invalid_path)
        analysis=joinpath(dirname(first_commit), "analysis.h5")
        HDF5.h5open(analysis, "r") do file
            @test read_attribute(file["metadata"], "schema")=="qcl-negf-physics-analysis-v4"
            @test read_attribute(file["metadata"], "native_grid")
            @test QCLNEGFRunner.YAML.load(read(file["metadata/scientific_status_json"])) ==
                  manifest["scientific_status"]
            @test length(read(file["axes/energy_eV"]))==513
            @test QCLNEGFRunner._read_array(file["observables"], "spatial_energy_density")==spatial_energy_density(
                solution.problem,
                solution.scba.green.Gˡ,
            ).n_per_eV_m3
            @test read(file["observables/density_per_m3"])==solution.n ./
                                                            solution.problem.scales.L₀_m^3
            @test read_attribute(
                file["observables/spatial_energy_density"],
                "logical_axis_order",
            )=="E,z"
            @test read_attribute(file["observables/spatial_energy_density"], "units")=="m^-3/eV"
            @test QCLNEGFRunner.YAML.load(
                String(
                    read_attribute(
                        file["observables/spatial_energy_density"],
                        "axis_coordinate_paths_json",
                    ),
                ),
            )==["/axes/energy_eV", "/axes/z_nm"]
            @test read_attribute(
                file["basis/effective_wavefunctions/real"],
                "logical_axis_order",
            )=="z,state"
            @test read_attribute(file["basis/effective_wavefunctions/real"], "units")=="nm^-1/2"
            density = file["observables/spatial_energy_density"]
            energy = file["axes/energy_eV"]
            try
                @test HDF5.API.h5ds_is_attached(density, energy, UInt32(0)) > 0
            finally
                close(energy)
                close(density)
            end
            @test HDF5.API.h5ds_is_attached(
                file["observables/spatial_energy_density"].id,
                file["axes/z_nm"].id,
                UInt32(1),
            )>0
            @test QCLNEGFRunner._read_complex(file["basis"], "localized_wavefunctions")≈solution.problem.basis.χ ./
                                                                                    sqrt(
                solution.problem.scales.L₀_m*1e9,
            )
            warnings=QCLNEGFRunner.YAML.load(String(read(file["diagnostics/warnings_json"])))
            @test only(warnings)["code"]=="NATIVE_FIXTURE"
            @test !haskey(file, "state_dimensionless/GR")
            @test read(file["observables/potential_total_eV"])≈read(
                file["observables/potential_structure_eV"],
            )+read(file["observables/potential_external_eV"])+read(
                file["observables/potential_hartree_eV"],
            )
        end
        HDF5.h5open(joinpath(dirname(first_commit), "physics.h5"), "r") do file
            @test QCLNEGFRunner._read_complex(file["state_dimensionless"], "GL")==original
            @test read_attribute(file["metadata"], "artifact_role")=="physics.full"
            @test haskey(file, "algorithm_state")
        end
        resumed=load_production_restart(
            joinpath(dirname(first_commit), "physics.h5"),
            solution.problem,
        )
        @test resumed.scba.green.Gˡ==original
        second_commit=QCLNEGFRunner.commit_point_artifacts(
            directory,
            solution;
            identity,
            algorithms = AlgorithmOptions(),
            analysis = false,
        )
        @test read(first_commit)==first_bytes
        @test first_commit!=second_commit
        @test QCLNEGFRunner.verify_point_artifacts(second_commit)["science_parent_commit"]["sha256"]==bytes2hex(
            sha256(first_bytes),
        )
        @test !any(
            endswith(name, ".csv") || name=="data.json" for
            (_, _, names) in walkdir(directory) for name in names
        )
        @test length(render_saved_snapshot(analysis, joinpath(directory, "figures")))>=6
        for damage in (:legacy_version, :legacy_schema, :missing_markers, :missing_packed)
            incompatible=joinpath(directory, string(damage)*".h5")
            cp(analysis, incompatible)
            HDF5.h5open(incompatible, "r+") do file
                if damage==:legacy_version
                    HDF5.delete_attribute(file["metadata"], "schema_version")
                    HDF5.attributes(file["metadata"])["schema_version"]="2.0"
                elseif damage==:legacy_schema
                    HDF5.delete_attribute(file["metadata"], "schema")
                    HDF5.attributes(file["metadata"])["schema"]="qcl-negf-physics-analysis-v2"
                elseif damage==:missing_markers
                    HDF5.delete_object(file["diagnostics"], "physical_markers")
                else
                    HDF5.delete_object(file["diagnostics/psd_history"], "selected_blocks")
                end
            end
            output=joinpath(directory, "rejected-"*string(damage))
            @test_throws ArgumentError render_saved_snapshot(incompatible, output)
            @test isempty(readdir(output))
        end
        write(analysis, "corrupt")
        @test_throws ArgumentError QCLNEGFRunner.verify_point_artifacts(first_commit)
    end
    @test solution.scba.green.Gˡ==original
end

@testset "Monotonic recovery deadline does not modify scientific acceptance" begin
    clock=QCLNEGFRunner.CheckpointDeadline(UInt64(1))
    @test !QCLNEGFRunner.checkpoint_due(clock, UInt64(1_799_000_000_001))
    @test QCLNEGFRunner.checkpoint_due(clock, UInt64(1_800_000_000_001))
    @test QCLNEGFRunner.checkpoint_due(clock, UInt64(1_900_000_000_001))
    QCLNEGFRunner.checkpoint_completed!(clock)
    @test !QCLNEGFRunner.checkpoint_due(clock)
    @test QCLNEGFRunner.checkpoint_policy(clock)["interval_seconds"]==1800.0
end
end
