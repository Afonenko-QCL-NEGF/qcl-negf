using LinearAlgebra
using QCLNEGFRunner
using SHA
import QCLNEGF.LinkedTransport as LT

include("spatial_balance.jl")
include("direct_impurity.jl")
include("direct_ifr.jl")
using .DirectImpurity
using .DirectIFR

const IMP = findfirst(==(:impurity), LT.COLLISION_CHANNELS)
const IFR = findfirst(==(:IFR), LT.COLLISION_CHANNELS)
const ARMS = ("baseline_PV", "matched_PV", "direct_RLG")
const Runner = QCLNEGFRunner
const COEFFICIENTS = ("a", "c")

function hermitian_parts!(output, frozen, direct, arm)
    if arm == "baseline_PV"
        output .= frozen
    else
        output .= direct
        if arm == "matched_PV"
            for side in axes(output,4)
                @views r, old_r = output[:,:,1,side], frozen[:,:,1,side]
                r .+= (old_r .+ old_r' .- r .- r')./2
            end
        end
    end
    return output
end

function ring_test(p,k,energies,measures,seed_total,seed_channel,fresh_other,fresh_channel,
        anchor,anchor_other,table,coefficients,channel)
    a,c = coefficients
    ne = length(energies)
    geo = p.geo
    base = LT.centered_basis(geo)
    center = @view geo.modes[(first(geo.monitor)+1):(last(geo.monitor)-1),:]
    nmodes = size(geo.modes,2)
    dual = Hermitian(geo.metric) \ Matrix{ComplexF64}(I,nmodes,nmodes)
    center_metric = center' * center
    schur = zeros(3,3,length(ARMS))
    schur_norm = zero(schur)
    rk_fit = zeros(length(ARMS))
    rk_norm = 0.0
    rs_fit,rs_norm = zeros(3,length(ARMS)),zeros(3,length(ARMS))
    current = zeros(p.nz+1,length(ARMS))
    sheet = zeros(length(ARMS))
    moment = zero(sheet)
    spectral = zeros(ComplexF64,p.r,p.r,length(ARMS))
    mechanism = zeros(ComplexF64,nmodes,nmodes,3)
    local_channel = zeros(ComplexF64,nmodes,nmodes,length(ARMS))
    old_balance = zero(local_channel)
    all_parts = zeros(ComplexF64,p.r,p.r,3,length(geo.offsets))
    selected_source = similar(all_parts)
    old = LT.TailWorkspace(geo)
    ws = LT.TailWorkspace(geo)
    center_side = div(length(geo.offsets),2)+1
    @views dual_htrans = dual * (p.h[:,:,k]-p.h[:,:,1])
    @views for start in 1:128:ne
        indices = start:min(start+127,ne)
        rows = LT.CausalRows(p.en,LT.shifted_queries(p.geo,energies[indices]))
        previous = LT.sample_packed_ring(rows,seed_total[:,:,:,k],anchor[:,:,k])
        other = LT.sample_packed_ring(rows,fresh_other[:,:,:,k],anchor_other[:,:,k])
        frozen = LT.sample_packed_ring(rows,fresh_channel[:,:,:,k],p.const_by_channel[:,:,k,channel])
        old_channel = LT.sample_packed_ring(rows,seed_channel[:,:,:,k],p.const_by_channel[:,:,k,channel])
        for (i,node) in enumerate(indices)
            e = energies[node]
            weight = measures[node] * p.wk[k] * p.spin_degeneracy/(2π)
            LT.sample_node!(old,geo,e,p.h[:,:,k],p.hops[:,k],previous[:,:,:,i,:])
            old_r, old_l = old.mode_green[:,:,1],old.mode_green[:,:,2]
            local_l, local_g = old.local_green[:,:,2], old.local_green[:,:,3]
            normalized_lesser = a.*local_l .- c.*local_g
            rk_norm += weight*sum(abs2,normalized_lesser)
            response = base * old_r
            old_cavity = LT.boundary_parts(old,geo)
            direct = table.fields[:,:,:,table.location[node,:],k]
            for (j,arm) in enumerate(ARMS)
                hermitian_parts!(selected_source,frozen[:,:,:,i,:],direct,arm)
                all_parts .= other[:,:,:,i,:] .+ selected_source
                LT.sample_node!(ws,geo,e,p.h[:,:,k],p.hops[:,k],all_parts)
                r,l = ws.mode_green[:,:,1], ws.mode_green[:,:,2]
                current[:,j] .+= weight .* ws.bond_profile[:,1]
                sheet[j] += weight*imag(tr(ws.local_green[:,:,2]))
                moment[j] += weight*imag(sum((dual_htrans * l) .* transpose(center_metric)))
                rl = ws.local_green[:,:,1]
                spectral[:,:,j] .+= (im*measures[node]/(2π)) .* (rl .- rl')
                new_lesser = response * ws.mode_source[:,:,2] * response'
                rk_fit[j] += weight*sum(abs2,new_lesser-normalized_lesser)
                cavity = LT.boundary_parts(ws,geo)
                for t in 1:3, n in 1:3
                    candidate = cavity[:,:,n,t]
                    schur[n,t,j] += weight*sum(abs2,candidate-old_cavity[:,:,n,t])
                    schur_norm[n,t,j] += weight*sum(abs2,candidate)
                end
                for n in 1:3
                    candidate = selected_source[:,:,n,center_side]
                    rs_fit[n,j] += weight*sum(abs2,candidate-old_channel[:,:,n,i,center_side])
                    rs_norm[n,j] += weight*sum(abs2,candidate)
                end
                SpatialBalance.local_source!(mechanism,geo.bases,selected_source)
                sig_r,sig_l = mechanism[:,:,1],mechanism[:,:,2]
                y = -(dual*sig_r)*l + r*(sig_l*dual)
                SpatialBalance.add_hermitian_part!(local_channel[:,:,j],y,weight)
                y_old = -(dual*sig_r)*old_l + old_r*(sig_l*dual)
                SpatialBalance.add_hermitian_part!(old_balance[:,:,j],y_old,weight)
            end
        end
    end
    return (; current, sheet, moment, schur, schur_norm, rk_fit, rk_norm, rs_fit, rs_norm,
        local_channel, old_balance, spectral)
end

function prepared_arms(p,seed,fresh,channel=IMP)
    anchor = dropdims(sum(p.const_by_channel; dims=4); dims=4)
    anchor_other = anchor .- @view p.const_by_channel[:,:,:,channel]
    seed_total = dropdims(sum(seed; dims=5); dims=5)
    all_fresh = dropdims(sum(fresh; dims=5); dims=5)
    fresh_channel = @view fresh[:,:,:,:,channel]
    fresh_other = all_fresh .- fresh_channel
    seed_channel = @view seed[:,:,:,:,channel]
    return (;seed_total,seed_channel,fresh_other,fresh_channel,anchor,anchor_other,channel)
end

function raw_arms(p,preparation,energies,weights,table,coefficients;workers)
    (;seed_total,seed_channel,fresh_other,fresh_channel,anchor,anchor_other,channel) = preparation
    rings = Vector{Any}(undef,p.nk)
    LT.N._production_worker_ranges!(p.nk,min(workers,p.nk)) do _,lo,hi
        for k in lo:hi
            rings[k] = ring_test(p,k,energies,weights,seed_total,seed_channel,fresh_other,
                fresh_channel,anchor,anchor_other,table,coefficients,channel)
        end
    end
    return rings
end

function formatted_arms(p,rings,cuts;full_window)
    center = @view p.geo.modes[(first(p.geo.monitor)+1):(last(p.geo.monitor)-1),:]
    widths = (cuts[3:end] .- cuts[1:end-2])./2
    gather(name) = sum(getproperty(row,name) for row in rings)
    mode_source = gather(:local_channel)
    lagged_source = gather(:old_balance)
    current = p.current_scale .* gather(:current)
    curr_source(a,j) = [0.; cumsum(p.current_scale .* SpatialBalance.diagonal_in_coordinates(a[:,:,j],center))]
    sheet = gather(:sheet)
    temp = 100 .* gather(:moment) ./ sheet ./ 0.08617333262145
    rK = sqrt.(gather(:rk_fit) ./ max(gather(:rk_norm), 1e-300))
    r_imp = sqrt.(gather(:rs_fit) ./ max.(gather(:rs_norm), 1e-300))
    r_bound = sqrt.(gather(:schur) ./ max.(gather(:schur_norm), 1e-300))
    absolute = sqrt.(gather(:schur))
    bound_groups = ("left","right","mixed")
    completeness = LT.spectral_completeness(p.geo)
    return Dict(arm=>(;profile_A_cm2=current[:,j],
        profile_statistics=SpatialBalance.current_metrics(current[:,j],widths),
        selected_channel_cumulative_in_fresh_A_cm2=curr_source(mode_source,j),
        selected_channel_cumulative_on_previous_A_cm2=curr_source(lagged_source,j),
        raw_sheet_cm2=sheet[j]*p.density_scale,
        raw_lambda=sheet[j]/p.target_dimless,
        equivalent_temperature_K=temp[j],
        weighted_rK=rK[j],
        weighted_selected_channel_RLG=r_imp[:,j],
        weighted_boundary_RLG=Dict(side=>r_bound[:,i,j] for (i,side) in enumerate(bound_groups)),
        absolute_weighted_boundary_RLG=Dict(side=>absolute[:,i,j] for (i,side) in enumerate(bound_groups)),
        spectral_defect_by_ring=full_window ?
            [norm(x.spectral[:,:,j]-completeness)/norm(completeness) for x in rings] : nothing)
        for (j,arm) in enumerate(ARMS))
end

function integrated_arms(p,seed,fresh,energies,weights,cuts,table,coefficients;
        workers,full_window=true,channel=IMP)
    preparation = prepared_arms(p,seed,fresh,channel)
    rings = raw_arms(p,preparation,energies,weights,table,coefficients;workers)
    return formatted_arms(p,rings,cuts;full_window)
end

function fixed_window_rule(lo,hi,n,order)
    lo<hi && n>0 || throw(ArgumentError("nonpositive window or panel count"))
    nodes,weights = Float64[],Float64[]
    panels = range(lo,hi;length=n+1)
    rule = LT.gauss_rule(order)
    for (a,b) in zip(panels[1:end-1],panels[2:end])
        e,w = LT.integrate_panel(a,b,nothing,rule;grading=false)
        append!(nodes,e)
        append!(weights,w)
    end
    return nodes,weights
end

elastic_operator(channel)=channel==IFR ? direct_ifr : direct_impurity

function window_compare(p,seed,fresh,cuts,coefficients,window,workers,channel)
    lo,hi = window ./ 100
    minimum(p.en) <= lo < hi <= maximum(p.en) ||
        throw(ArgumentError("selected window lies outside the central energy grid"))
    n = max(1,ceil(Int,(hi-lo)/0.001))
    nearby = map(((n,10),(2n,16))) do (count,order)
        e,w = fixed_window_rule(lo,hi,count,order)
        source = elastic_operator(channel)(p,seed,LT.shifted_queries(p.geo,e),coefficients...;workers)
        return integrated_arms(p,seed,fresh,e,w,cuts,source,coefficients;workers,full_window=false,channel)
    end
    return (;
        window_meV=window,coarse=(panels=n,order=10),fine=(panels=2n,order=16),
        fine_arms=nearby[2],
        quadrature_change_A_cm2=Dict(name=>maximum(abs.(nearby[1][name].profile_A_cm2 .-
            nearby[2][name].profile_A_cm2)) for name in ARMS),
        interpretation="integrated contribution of the stated energy window",
    )
end

function run_elastic_experiment(path,workers,windows,channel)
    return run_elastic_on(Runner._read_linked_checkpoint(path),workers,windows,channel)
end

function run_elastic_on(saved,workers,windows,channel)
    p = saved.problem
    solver = LT.linked_fresh_map(p,saved.seed;projector=LT.project_linked_economical,
        projection_for_collision=false,selected_rows=true,workers)
    pair = solver.summary["input_pair_projection"]
    a,c = (pair[n] for n in COEFFICIENTS)
    table = elastic_operator(channel)(p,saved.seed,LT.shifted_queries(p.geo,p.en),a,c;workers)
    println(stderr,"direct convolution and all translated inputs complete")
    arms = integrated_arms(p,saved.seed,solver.source,p.en,p.we,saved.current_midpoints,table,(a,c);workers,channel)
    reference = solver.summary["fresh"]["raw_profile_A_cm2"]
    reproduced = maximum(abs.(reference .- arms["baseline_PV"].profile_A_cm2))
    reproduced < max(1e-6,1e-10maximum(abs,reference)) ||
        error("paired solver does not reproduce the canonical nodal profile: $reproduced")
    selected=String(LT.COLLISION_CHANNELS[channel])
    return (;schema="qcl-negf-linked-direct-elastic-nodal/v1",identity=saved.identity,channel=selected,
        provenance=(;core=Runner._linked_package_identity(Runner.QCLNEGF),
            runner=Runner._linked_package_identity(Runner),runtime=Runner._runtime_toolchain_provenance(),
            sources=Dict(name=>bytes2hex(open(sha256,joinpath(@__DIR__,name)))
                for name in ("spatial_balance.jl","direct_impurity.jl","direct_ifr.jl","impurity_experiment.jl"))),
        current_midpoints_nm=saved.current_midpoints,external_temperature_K=saved.identity["temperature_K"],
        fixed_normalization=(;a,c),num_unique_queries=length(table.queries),
        translated_energy_merge_error_scaled=table.maximum_merge_error,
        canonical_profile_reproduction_A_cm2=reproduced,arms,
        continuous_windows=[window_compare(p,saved.seed,solver.source,saved.current_midpoints,
            (a,c),window,workers,channel) for window in windows],
        canonical_other_channels_RLG=Dict(key=>value for (key,value) in
            solver.summary["weighted_rSigma_channels_RLG"] if key!=selected),
        notes="nodal common measure; matched_PV is a diagnostic control, not a causal continuation")
end

if abspath(PROGRAM_FILE)==abspath(@__FILE__)
    length(ARGS)>=3 ||
        error("Usage: impurity_experiment.jl ARCHIVE OUTPUT WORKERS [IFR] [Emin:Emax ... in meV]")
    input, output, worker_argument = ARGS[1:3]
    channel=length(ARGS)>=4 && ARGS[4]=="IFR" ? IFR : IMP
    windows = [parse.(Float64,split(token,":")) for token in ARGS[(channel==IFR ? 5 : 4):end]]
    all(x->length(x)==2,windows) || error("use one lower and upper energy per window")
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    report=run_elastic_experiment(input,parse(Int,worker_argument),windows,channel)
    open(output,"w") do io
        Runner._light_json(io,report)
        println(io)
    end
end
