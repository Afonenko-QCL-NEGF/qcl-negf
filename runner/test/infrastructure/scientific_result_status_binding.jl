module ScientificResultStatusBinding
include("../support/common.jl")

@testset "Completed scientific series points bind to their commits" begin
    Runner = QCLNEGFRunner
    Workflow = Runner.QCLScientificWorkflow
    status = Runner._point_scientific_status(:completed)
    point = Dict{String,Any}(
        "id"=>"p", "execution_id"=>"e", "attempt"=>1, "status"=>"completed",
        "scientific_status"=>status, "data"=>Dict("result_commit"=>"commit.json"),
    )
    fingerprint = repeat("a", 64)
    series = Dict(
        "schema"=>"qcl-negf-series-result-v4", "contract_set"=>Runner._RESULT_CONTRACT_SET,
        "plan_fingerprint"=>fingerprint, "points"=>[point],
    )
    commit = Dict(
        "schema"=>Runner.POINT_COMMIT_SCHEMA, "contract_set"=>Runner._RESULT_CONTRACT_SET,
        "identity"=>Dict(
            "point_id"=>"p", "execution_id"=>"e", "attempt"=>1, "plan_fingerprint"=>fingerprint,
        ),
        "scientific_status"=>copy(status),
    )
    mktempdir() do directory
        series_path = joinpath(directory, "series_result.json")
        commit_path = joinpath(directory, "commit.json")
        publish(path, value) = open(io -> Runner._light_json(io, value), path, "w")
        publish(series_path, series)
        publish(commit_path, commit)
        recovered, _ = Workflow._read_series(directory)
        @test only(recovered["points"])["scientific_status"] == status

        commit["identity"]["attempt"] = 2
        publish(commit_path, commit)
        @test_throws ArgumentError Workflow._read_series(directory)
        commit["identity"]["attempt"] = 1
        commit["scientific_status"]["physical_candidate"] = "passed"
        publish(commit_path, commit)
        @test_throws ArgumentError Workflow._read_series(directory)

        malformed = copy(point)
        malformed["status"] = "paused"
        malformed["scientific_status"] = Runner._point_scientific_status(:paused)
        malformed["scientific_accepted"] = false
        series["points"] = [malformed]
        publish(series_path, series)
        @test_throws ArgumentError Workflow._read_series(directory)
    end
end
end
