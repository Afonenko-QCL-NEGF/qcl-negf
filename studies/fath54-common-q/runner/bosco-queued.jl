length(ARGS)==5 || error("Expected the archived observer, three archive inputs, and campaign directory")
include(ARGS[1])
Base.include(T,joinpath(dirname(ARGS[1]),"radial_mechanism.jl"))

function announce(event)
    T.Runner._light_json(stderr,event)
    println(stderr)
    flush(stderr)
end

const campaign = include(joinpath(@__DIR__,"rank_scan.jl"))
Base.include(campaign,joinpath(@__DIR__,"bosco.jl"))
const work = ARGS[5]
const selected = T.Runner.YAML.load_file(joinpath(work,"selected-bosco-scheme.json");
    dicttype=Dict{String,Any})
const scheme = (;(Symbol(key)=>value for (key,value) in selected)...)
Threads.nthreads(:default)==12 || error("Bosco queue requires twelve Julia worker threads")
BLAS.set_num_threads(1)
announce((;phase="bosco_queue_started",julia_threads=Threads.nthreads(),blas_threads=BLAS.get_num_threads(),
    gc_threads=Threads.ngcthreads()))
Base.invokelatest(campaign.solve_bosco,work,scheme)
