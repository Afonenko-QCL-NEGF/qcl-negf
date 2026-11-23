include(ARGS[1])
Base.include(T, joinpath(dirname(ARGS[1]), "radial_mechanism.jl"))
const coarse_path, fine_path, archived_path, output, continuation = ARGS[2:6]
const workers = Threads.nthreads()
BLAS.set_num_threads(1)

function announce(event)
    T.Runner._light_json(stderr, event)
    println(stderr)
    flush(stderr)
end

function run()
    archived = T.Runner.YAML.load_file(archived_path; dicttype=Dict{String,Any})
    # Accept either the original nightly branch or the published evidence bundle.
    archived = get(archived,"radial",archived)
    initial = T.Runner._read_linked_checkpoint(coarse_path)
    p, cuts = initial.problem, initial.current_midpoints
    cuts == archived["cuts_nm"] || error("physical section mismatch")
    T.file_sha(joinpath(coarse_path,"spec.toml")) == archived["coarse_archive_spec_sha256"] ||
        error("F13 specification mismatch")
    seed = Base.invokelatest(replay_source!,p,initial.seed,workers,announce)
    replay = checked_replay(p,seed,cuts,workers,archived)
    T.radial_write(output,(;stage="coarse_replayed",cuts_nm=cuts,replay))
    (replay.input_matches && replay.image_matches) || replay.numerical_match ||
        error("map 48 reproduction failed")
    announce((;phase="coarse_replayed",replay.input_matches,replay.image_matches,replay.delta))
    while get(ENV,"FATH_HOLD_REPLAY","")=="1" && !isfile(continuation * ".ready")
        sleep(5)
    end
    include(continuation)
    Base.invokelatest(run_refinement,p,seed,cuts,workers,replay)
end

abspath(PROGRAM_FILE)==abspath(@__FILE__) && run()
