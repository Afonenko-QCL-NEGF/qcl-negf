module CommonQCampaign

using LinearAlgebra
using Dates

const archive = ENV["FATH_RANK_STUDIES"]
const R = include(joinpath(archive, "fath54-k31-rank", "k31_rank.jl"))
const RC = R.RankControl
const T = R.T
const LT = R.LT
const coarse_path, fine_path = ARGS[2:3]
const marks = (1, 4, 8, 12, 16, 24, 32, 40, 48)
const rank_limit = 32
const alpha = 0.35
const geometry = ENV["FATH_BDD"]
const workdir = @__DIR__
include("probes.jl")
include("local_grids.jl")

function strictly_stationary(result)
    T.strictly_qualified(result.row) || return false
    independent = result.observation
    R.independently_stationary(independent) || return false
    gl20 = independent.GL20
    return maximum(abs,gl20.oriented_seams.-gl20.mean) <= max(1.0,0.01abs(gl20.mean))
end

function projected_common_q(problem, common)
    embedding = common.v.coordinate_frame' * problem.v.coordinate_frame
    sites = T.Runner._read_linked_array(fine_path, "ifr_sites", Float64,
        size(common.v.interface_probes, 1), common.nz)
    kernels = RC.lo_kernel(problem.v, sites, problem.v.lo_plus, problem.v.lo_minus;
        q=common.v.coordinate_frame)
    projected = RC.rebuild(problem, kernels; anchor=common.const_by_channel)
    anchor_error = maximum(T.relerr(embedding' * projected.const_by_channel[:,:,k,c] * embedding,
        problem.const_by_channel[:,:,k,c]) for k in 1:problem.nk, c in eachindex(LT.COLLISION_CHANNELS))
    vertex_error = maximum(T.relerr(embedding' * a, b)
        for (a,b) in zip(projected.geo.bases, problem.geo.bases))
    frame_error = T.relerr(common.v.coordinate_frame * embedding, problem.v.coordinate_frame)
    overlap_error = norm(embedding' * embedding - I)
    maximum((anchor_error, vertex_error, frame_error, overlap_error)) < 2e-12 ||
        error("fixed W changed its restriction when promoted to common Q")
    return projected, (;anchor_error, vertex_error, frame_error, overlap_error)
end

function check_added_mode(problem, coordinates, radius)
    offsets = problem.geo.offsets
    center = findfirst(iszero, offsets)
    index = last(problem.geo.block_ranges[center])
    added = problem.geo.modes[:,index]
    components = reshape(added, problem.nz, :)
    weights = vec(sum(abs2, components; dims=1))
    norm_error = abs(sum(weights) - 1)
    deviations = [(;offset=offsets[i], norm=norm(problem.geo.modes[:,last(columns)]),
        shift_error=maximum(norm(components[:,j] - problem.geo.modes[
            (l-1)*problem.nz+1:l*problem.nz,last(columns)])
            for j in eachindex(offsets) for l in eachindex(offsets) if offsets[l]==offsets[j]+offsets[i]))
        for (i,columns) in enumerate(problem.geo.block_ranges)]

    zero = RC.bdd_chain(coordinates, offsets, 0; periodic_ends=false)
    lower = length(offsets) * (problem.nb-1) + 1
    upper = length(offsets) * problem.nb
    band = eigen(SymTridiagonal(zero.diagonal, zero.off_diagonal), lower:upper)
    zero_field_band_weight = sum(abs2, band.vectors' * added)
    tail = -3:3
    narrow = RC.bdd_chain(coordinates, tail, 0; periodic_ends=false)
    tight_band = eigen(SymTridiagonal(narrow.diagonal, narrow.off_diagonal),
        (length(tail)*(problem.nb-1)+1):(length(tail)*problem.nb))
    wide_span = (100first(band.values), 100last(band.values))
    narrow_span = (100first(tight_band.values), 100last(tight_band.values))

    k_samples = unique([1, argmin(abs.(radius .- 1.6875)), length(radius)])
    spectra = map(k_samples) do k
        chain = RC.bdd_chain(coordinates, offsets, problem.geo.voltage; periodic_ends=false)
        fd = SymTridiagonal(chain.diagonal + radius[k]^2 * chain.radial, chain.off_diagonal)
        reference = eigen(fd)
        projection = abs2.(reference.vectors' * added)
        active = first(problem.en) .<= reference.values .<= last(problem.en)
        margins = 0.02
        edge = active .& ((reference.values .< first(problem.en) + margins) .|
            (reference.values .> last(problem.en) - margins))
        projected = eigen(Hermitian(problem.h[:,:,k]), Hermitian(problem.geo.metric))
        coefficients = abs2.(projected.vectors' * problem.geo.metric[:,index])
        dominant = argmax(projection)
        reduced = argmax(coefficients)
        return (;k_nm_inverse=radius[k]/10, fd_centroid_meV=100dot(reference.values,projection),
            fd_dominant_meV=100reference.values[dominant], fd_dominant_weight=projection[dominant],
            projected_dominant_meV=100projected.values[reduced], projected_dominant_weight=coefficients[reduced],
            window_weight=sum(projection[active]), edge_weight=sum(projection[edge]),
            below_weight=sum(projection[reference.values .< first(problem.en)]),
            above_weight=sum(projection[reference.values .> last(problem.en)]))
    end
    gram_condition = cond(problem.geo.metric)
    accepted = norm_error < 2e-12 && maximum(x.shift_error for x in deviations) < 2e-12 &&
        gram_condition < 100 && weights[center] >= 0.5 && zero_field_band_weight >= 0.90 &&
        all(s.window_weight >= 0.95 && s.edge_weight <= 0.05 for s in spectra)
    return (;accepted, norm_error, deviations, offsets, weights, gram_condition,
        zero_field_band_weight, wide_span, narrow_span, spectra,
        energy_window_meV=100 .* [first(problem.en), last(problem.en)])
end

function wide_tail_candidate(problem, grid, data)
    wide = -4:4
    local_tail = -3:3
    chain = RC.bdd_chain(data,wide,0;periodic_ends=false)
    low = length(wide)*problem.nb+1
    high = length(wide)*(problem.nb+1)
    band = eigen(SymTridiagonal(chain.diagonal,chain.off_diagonal),low:high)
    localization = eigen(Symmetric(band.vectors'*(chain.z .* band.vectors)))
    central = band.vectors*localization.vectors[:,div(length(wide),2)+1]
    chunks = reshape(central,problem.nz,length(wide))
    discarded = sum(abs2,chunks[:,[1,end]])
    retained = chunks[:,2:end-1]
    retained ./= norm(retained)

    old_count, new_count = problem.nb, problem.nb+1
    geo = problem.geo
    old_ids = Int[]
    modes = zeros(ComplexF64,size(geo.modes,1),length(geo.offsets)*new_count)
    for (period,columns) in enumerate(geo.block_ranges)
        target = ((period-1)*new_count+1):((period-1)*new_count+old_count)
        append!(old_ids,target)
        modes[:,target] .= geo.modes[:,columns]
        for (i,delta) in enumerate(local_tail)
            cell = period+delta
            1<=cell<=length(geo.offsets) || continue
            modes[(cell-1)*problem.nz+1:cell*problem.nz,last(target)+1] .= retained[:,i]
        end
    end
    q = problem.v.coordinate_frame
    residual = retained-q*(q'*retained)
    decomposition = svd(residual)
    count_added = count(>(1e-10),decomposition.S)
    count_added>0 || error("wide-tail candidate has no new local component")
    new_dirs = decomposition.U[:,1:count_added]
    new_dirs -= q*(q'*new_dirs)
    common_q = hcat(q,Matrix(qr(new_dirs).Q)[:,1:count_added])
    chain = RC.bdd_chain(data,geo.offsets,geo.voltage;periodic_ends=true)
    h = cat((modes'*SymTridiagonal(chain.diagonal+k^2*chain.radial,chain.off_diagonal)*modes
        for k in grid)...;dims=3)
    h_error = T.relerr(h[old_ids,old_ids,:],problem.h)
    metric_error = T.relerr((modes'*modes)[old_ids,old_ids],geo.metric)
    max(h_error,metric_error)<2e-12 || error("wide-tail candidate changed old modes")
    embedding = common_q' * q
    rank = size(common_q,2)
    anchors = zeros(ComplexF64,rank,rank,problem.nk,length(LT.COLLISION_CHANNELS))
    for k in 1:problem.nk, c in eachindex(LT.COLLISION_CHANNELS)
        anchors[:,:,k,c] .= embedding*problem.const_by_channel[:,:,k,c]*embedding'
    end
    v = problem.v
    kernels = RC.lo_kernel(v,physical_sites(problem),v.lo_plus,v.lo_minus;q=common_q)
    candidate = RC.rebuild(problem,kernels;modes,nb=new_count,h,anchor=anchors)
    return (;problem=candidate,discarded,h_error,metric_error)
end

function qualify_ninth(eight, grid, source, data, sha, path)
    for method in ("seven_period_band","nine_period_band_truncated")
        try
            constructed = method=="seven_period_band" ?
                RC.expand(eight,grid,source,fine_path,geometry,sha) :
                wide_tail_candidate(eight,grid,data)
            problem = constructed.problem
            audit = R.audit_expansion(eight,problem)
            static_data = check_added_mode(problem,data,grid)
            lost = method=="seven_period_band" ? 0.0 : constructed.discarded
            accepted = static_data.accepted && lost <= 0.005
            R.append_row(path,"ninth_mode",(;method,accepted,static_data,audit,lost,
                constructed.metric_error,constructed.h_error))
            accepted && return problem
        catch err
            err isa InterruptException && rethrow()
            R.append_row(path,"ninth_mode_error",(;method,error=sprint(showerror,err)))
        end
    end
    return nothing
end

function close_coordinate_frame(problem)
    frame = problem.v.coordinate_frame
    geo = problem.geo
    # The chain columns are laid out by period; concatenate their physical
    # period slices explicitly so every boundary copy is audited.
    physical_blocks = hcat((view(geo.modes,(j-1)*problem.nz+1:j*problem.nz,:)
        for j in eachindex(geo.offsets))...)
    residual = physical_blocks-frame*(frame'*physical_blocks)
    decomp = svd(residual)
    admitted = count(>(1e-10),decomp.S)
    chosen = problem
    if admitted>0
        directions = decomp.U[:,1:admitted]
        directions -= frame*(frame'*directions)
        q = hcat(frame,Matrix(qr(directions).Q)[:,1:admitted])
        embedding = q'*frame
        rank = size(q,2)
        anchors = zeros(ComplexF64,rank,rank,problem.nk,length(LT.COLLISION_CHANNELS))
        for k in 1:problem.nk, c in eachindex(LT.COLLISION_CHANNELS)
            anchors[:,:,k,c] .= embedding*problem.const_by_channel[:,:,k,c]*embedding'
        end
        v = problem.v
        new_kernels = RC.lo_kernel(v,physical_sites(problem),v.lo_plus,v.lo_minus;q)
        chosen = RC.rebuild(problem,new_kernels;anchor=anchors)
        R.audit_expansion(problem,chosen)
    end
    Q = chosen.v.coordinate_frame
    err = maximum(svdvals(physical_blocks-Q*(Q'*physical_blocks)))
    err <= 2e-10 || error("common coordinate frame does not cover local modes: $err")
    return chosen,(;admitted,singular_values_before=decomp.S,max_singular_tail=err)
end

function setup(pair, path)
    seven, eight = pair.problems
    grid = pair.stage.k
    sha = T.TOML.parsefile(joinpath(fine_path, "spec.toml"))["source_model_sha"]
    data = RC.coordinate_data(geometry, sha, seven)
    nine = qualify_ninth(eight,grid,pair.seeds[2],data,sha,path)
    admitted = !isnothing(nine)
    common,closure = close_coordinate_frame(admitted ? nine : eight)
    w7, check7 = projected_common_q(seven, common)
    w8, check8 = projected_common_q(eight, common)
    seed7 = RC.lift_source(pair.seeds[1], common.v.coordinate_frame' * seven.v.coordinate_frame)
    unchanged_eight = !admitted && common.r==eight.r
    staged = unchanged_eight ? nothing :
        RC.lift_source(pair.seeds[2],common.v.coordinate_frame' * eight.v.coordinate_frame)
    want = unchanged_eight ? pair.seeds[2] : staged.source
    embedding_dual_error = T.relerr(seed7.source, want)
    embedding_dual_error < 2e-12 || error("direct and staged source embeddings differ")
    R.append_row(path, "configuration", (;pair.evidence..., common_Q=common.r,
        ninth_admitted=admitted, closure, check7, check8, embedding_dual_error,
        direct_source_roundtrip=seed7.roundtrip_maximum,
        shared_seed_sha=T.packed_sha(seed7.source), marks, rank_limit, alpha, grid,
        julia_threads=Threads.nthreads(), blas_threads=BLAS.get_num_threads()))
    if admitted
        return ["W7_Q21", "W8_Q25", "W7_common", "W8_common", "W9_common"],
            [seven, eight, w7, w8, common], [pair.seeds..., seed7.source, want, want]
    end
    if unchanged_eight
        return ["W7_Q21", "W8_Q25", "W7_common"], [seven, eight, w7],
            [pair.seeds..., seed7.source]
    end
    return ["W7_Q21", "W8_Q25", "W7_common", "W8_common"], [seven, eight, w7, w8],
        [pair.seeds..., seed7.source, want]
end

function nodal_audit(image)
    fields = ("kinetic_PSD_min_relative", "Dyson_max_relative",
        "charge_metric_max_relative", "spectral_identity_max_relative",
        "coupled_cavity_max_relative")
    return Dict(stage=>Dict(x=>image.summary[stage][x] for x in fields)
        for stage in ("input","fresh"))
end

function observed_map(problem, seed, name, step, cuts, workers, path; baseline=nothing)
    T0 = time_ns()
    image = R.arm_image(problem, seed, cuts, workers)
    row = R.fresh_row(problem, image, cuts)
    observation = step in marks || T.strictly_qualified(row) ?
        R.observe_k31(problem, seed, image, row, cuts, workers; baseline) : nothing
    R.append_row(path, "map", (;name, step, W=problem.nb, Q=problem.r, row, observation,
        seconds=(time_ns()-T0)*1e-9,maxrss_bytes=Int(Sys.maxrss()),
        nodal=nodal_audit(image),channel_balance=image.summary["fresh_channel_balance"]))
    return (;image, row, observation)
end

function extend_unmatched!(names,problems,states,latest,confirmations,passed,cuts,workers,path)
    common = findall(n->endswith(n,"_common") ||
        (length(names)==3 && n=="W8_Q25"),names)
    comparable() = all(R.checkpoints_match(latest[i].row,latest[j].row)
        for i in common for j in common)
    comparable() && return
    step = rank_limit
    while step<48 && !comparable() && !all(passed[common])
        starting = [(latest[i].row.rK,latest[i].row.rSigma) for i in common]
        for i in common
            passed[i] && continue
            image = R.arm_image(problems[i],states[i],cuts,workers)
            R.k31_update!(states[i],image,alpha)
        end
        stop = step+8
        R.append_row(path,"extend_for_matched_residuals",(;from=step,to=stop,names=names[common],starting))
        for mark in step+1:stop
            for i in common
                passed[i] && continue
                measurement = observed_map(problems[i],states[i],names[i],mark,cuts,workers,path)
                confirmations[i] = strictly_stationary(measurement) ? confirmations[i]+1 : 0
                latest[i] = (;measurement.row,measurement.observation)
                passed[i] = confirmations[i]>=3
                if mark<stop && !passed[i]
                    R.k31_update!(states[i],measurement.image,alpha)
                end
                measurement = nothing
                GC.gc(false)
            end
        end
        step = stop
    end
end

function continuation(pair, cuts, workers, path)
    base = observed_map(pair.problems[1],pair.seeds[1],"W7_Q21",1,cuts,workers,path;
        baseline=pair.stage)
    names, problems, seed_inputs = setup(pair, path)
    count = length(names)
    active = trues(count)
    confirmations = zeros(Int, count)
    passed = falses(count)
    states = copy(seed_inputs)
    if count==5
        # The two promoted higher ranks share their input until updates begin.
        states[5] = copy(states[5])
    end
    latest = Vector{Any}(undef, count)
    for step in 1:rank_limit
        for i in eachindex(names)
            active[i] && !passed[i] || continue
            reuse = step==1 && i==1
            result = reuse ? base : observed_map(problems[i],states[i],names[i],step,cuts,workers,path)
            reuse && (base = nothing)
            confirmations[i] = strictly_stationary(result) ?
                confirmations[i] + 1 : 0
            latest[i] = (;result.row, result.observation)
            passed[i] = confirmations[i]>=3
            if step < rank_limit && !passed[i]
                R.k31_update!(states[i], result.image, alpha)
            end
            result = nothing
            GC.gc(false)
        end
        if step == 1
            for (native,promoted) in (count >= 4 ? ((1,3),(2,4)) : ((1,3),))
                a,b = latest[native].observation,latest[promoted].observation
                contrast = R.profile_contrast(a,b)
                comparable = R.checkpoints_match(latest[native].row,latest[promoted].row)
                detectable = contrast.pair_max_centered > contrast.numerical
                active[native] = !comparable || detectable
                R.append_row(path, "coordinate_control", (;step, native=names[native], promoted=names[promoted],
                    contrast, comparable, detectable, continues=active[native]))
            end
        end
        all(passed[active]) && break
    end
    extend_unmatched!(names,problems,states,latest,confirmations,passed,cuts,workers,path)
    R.append_row(path, "rank_block_complete", (;names, active, confirmations))
    return (;names, problems, states, latest, active, confirmations)
end

function run(p, seed, cuts, workers, replay, path)
    replay.input_matches && replay.image_matches || error("expected bitwise map 48 reproduction")
    pair = R.make_k31_pair(p, seed, cuts, workers)
    result = continuation(pair, cuts, workers, path)
    work = dirname(path)
    followup = joinpath(work, "followup.jl")
    for attempt in Iterators.countfrom(1)
        Main.announce((;phase="rank_block_complete", waiting_for=followup, attempt))
        ready = followup * ".ready-$attempt"
        while !isfile(ready)
            sleep(5)
        end
        try
            execute = include(followup)
            scheme = Base.invokelatest(execute, result, pair, cuts, workers, path)
            scheme_file = joinpath(work,"selected-bosco-scheme.json")
            open(scheme_file,"w") do io
                T.Runner._light_json(io,(;scheme...,chosen_at=string(Dates.now(Dates.UTC)),
                    app_revision=readchomp(`git -C $(ENV["FATH_APP"]) rev-parse HEAD`),
                    core_revision="c2f45cae21c3e2e4257805ea9c30f9c1d80a7515",
                    driver_sha=T.file_sha(joinpath(workdir,"bosco.jl"))))
                println(io)
            end
            return scheme
        catch err
            err isa InterruptException && rethrow()
            open(joinpath(work,"followup.errors"),"a") do io
                showerror(io,err,catch_backtrace())
                println(io)
            end
            Main.announce((;phase="followup_failed", attempt, error=sprint(showerror,err)))
        end
    end
end

end
