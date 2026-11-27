using LinearAlgebra, TOML, SHA
import Pkg

function publish(path, data)
    temp = path * ".tmp"
    open(temp, "w") do io
        TOML.print(io, data; sorted=true)
    end
    mv(temp, path; force=true)
end

function runtime(task)
    allocation = parse(Int, ENV["QCL_SLOT_CPUS"])
    info = Dict{String,Any}(
        "allocated_cpus" => allocation, "julia_threads" => Threads.nthreads(:default),
        "blas_threads" => BLAS.get_num_threads(), "visible_cpus" => Sys.CPU_THREADS,
        "julia_version" => string(VERSION), "op_sys" => Sys.iswindows() ? "WINDOWS" : "LINUX",
        "manifest_sha256" => bytes2hex(open(sha256, joinpath(dirname(Base.active_project()), "Manifest.toml"))),
    )
    if Sys.islinux() && isfile("/proc/self/status")
        for line in eachline("/proc/self/status")
            if startswith(line, "Cpus_allowed_list:")
                info["allowed_cpu_list"] = strip(split(line, ':'; limit=2)[2])
            end
        end
    elseif haskey(ENV, "QCL_AFFINITY_CPUS")
        info["affinity_cpus"] = parse(Int, ENV["QCL_AFFINITY_CPUS"])
    end
    machine_ad = get(ENV, "_CONDOR_MACHINE_AD", "")
    if isfile(machine_ad)
        for line in eachline(machine_ad)
            captured = match(r"^(Cpus|QCLWorkerId|Machine|Name)\s*=\s*(.+)$", line)
            isnothing(captured) && continue
            key, value = captured.captures
            if key == "Cpus"
                cpu_count = tryparse(Int, value)
                isnothing(cpu_count) || (info["condor_slot_cpus"] = cpu_count)
            else
                info["slot_" * lowercase(key)] = strip(value, '"')
            end
        end
    end
    return info
end

const task = first(ARGS)
const inputs = ARGS[2:end]
const output = get(ENV, "QCL_RESULT", "summary.toml")
VERSION == v"1.13.4" || error("Expected Julia 1.13.4")
if Sys.iswindows()
    setup_start = time_ns()
    manifest = joinpath(dirname(Base.active_project()), "Manifest.toml")
    digest = open(sha256, manifest)
    Pkg.instantiate(; allow_autoprecomp=false)
    open(sha256, manifest) == digest || error("Pkg changed the frozen Manifest.toml")
    const setup_seconds = (time_ns() - setup_start) / 1e9
else
    const setup_seconds = 0.0
end
BLAS.set_num_threads(1)
if task == "PROBE"
    @eval using QCLNEGF, QCLNEGFRunner
end
started = time_ns()
out = try
    if task == "PROBE"
        pkgversion(QCLNEGFRunner) == pkgversion(QCLNEGF) == v"0.2.0" || error("Unexpected package versions")
        observed = Threads.nthreads(:default)
        @assert observed == parse(Int, ENV["QCL_SLOT_CPUS"])
        @assert sum(fetch.([Threads.@spawn(i*i) for i in 1:10])) == 385
        Dict("status" => "measured", "operator" => "thread_and_transfer_probe",
             "runner_version" => string(pkgversion(QCLNEGFRunner)), "core_version" => string(pkgversion(QCLNEGF)))
    elseif task in ("B7", "B9", "B11")
        include("basis.jl")
        Base.invokelatest(run_basis, task, inputs)
    elseif task == "BLOCH"
        include("bloch.jl")
        Base.invokelatest(run_bloch, task, inputs)
    elseif task in ("IMP17", "IMP33", "LO")
        include("operators.jl")
        Base.invokelatest(run_operators, task, inputs)
    elseif task == "SHIFT"
        include("shifts.jl")
        Base.invokelatest(run_shift, task, inputs)
    elseif task == "SELECT"
        include("select.jl")
        Base.invokelatest(run_select, task, inputs)
    elseif task == "PILOT" || startswith(task, "T")
        include("transport.jl")
        Base.invokelatest(run_transport, task, inputs)
    else
        error("Unknown task: " * task)
    end
catch err
    publish(output, Dict("task" => task, "status" => "technical_error",
                         "error_type" => string(typeof(err)), "runtime" => runtime(task)))
    rethrow()
end
info = runtime(task)
info["setup_seconds"] = setup_seconds
info["compute_seconds"] = (time_ns() - started) / 1e9
info["peak_memory_mib"] = Sys.maxrss() / 1024^2
result = Dict{String,Any}(string(key)=>value for (key,value) in pairs(out))
result["task"] = task
result["runtime"] = info
publish(output, result)
