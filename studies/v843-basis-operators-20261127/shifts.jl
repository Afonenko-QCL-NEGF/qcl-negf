module V843ShiftAudit

using LinearAlgebra
using QCLNEGF
using Unitful

const NUM = QCLNEGF.QCLNumerics
const REF = QCLNEGF.QCLReferenceOperators
const E_MIN = -650.0
const E_MAX = 1000.0
const PEAK_SIGMA = 20.0
const PEAK_CENTER = 175.0
const PEAK_EDGE = 980.0
const RULE_NODES = (
    -0.9602898564975363, -0.7966664774136267, -0.5255324099163290, -0.1834346424956498,
    0.1834346424956498, 0.5255324099163290, 0.7966664774136267, 0.9602898564975363,
)
const RULE_WEIGHTS = (
    0.1012285362903763, 0.2223810344533745, 0.3137066458778873, 0.3626837833783620,
    0.3626837833783620, 0.3137066458778873, 0.2223810344533745, 0.1012285362903763,
)

function integral(f, a, b)
    b > a || return 0.0
    intervals = ceil(Int, (b - a) / PEAK_SIGMA)
    Δ = (b-a) / intervals
    half = Δ/2
    result = 0.0
    for j in 1:intervals
        center = a + (j-0.5)*Δ
        result += half * sum(w*f(center + half*x) for (x,w) in zip(RULE_NODES,RULE_WEIGHTS))
    end
    return result
end

function shifted_action(operator, energy, edges, weights, δ, scheme, name, f, safe)
    cell = scheme === :finite_volume_piecewise_constant
    if cell
        source = [integral(f, edges[i], edges[i+1]) / (edges[i+1]-edges[i]) for i in eachindex(energy)]
        exact = [integral(f, max(E_MIN,edges[i]+δ), min(E_MAX,edges[i+1]+δ)) /
                 (edges[i+1]-edges[i]) for i in eachindex(energy)]
    else
        source = f.(energy)
        exact = [E_MIN <= e+δ <= E_MAX ? f(e+δ) : 0.0 for e in energy]
    end
    action = operator * source
    row = Dict{String,Any}(
        "field"=>name, "signed_shift_meV"=>δ, "interior_nodes"=>count(safe),
    )
    for (region, mask) in (("interior",safe), ("edge",.!safe), ("all",trues(length(safe))))
        errors = view(action,mask) - view(exact,mask)
        w = view(weights,mask)
        absolute = sqrt(dot(w, abs2.(errors)))
        reference = sqrt(dot(w, abs2.(view(exact,mask))))
        row[region] = Dict{String,Any}("absolute_weighted_l2"=>absolute, "reference_weighted_l2"=>reference,
                           "relative_defined"=>!iszero(reference))
        iszero(reference) || (row[region]["relative_weighted_l2"] = absolute/reference)
    end
    continuum_input = integral(f, E_MIN, E_MAX)
    retained = integral(f, max(E_MIN,E_MIN+δ), min(E_MAX,E_MAX+δ))
    row["exact_escaped_weight_meV"] = continuum_input-retained
    row["discrete_escaped_weight_meV"] = dot(weights,source)-dot(weights,action)
    row["retained_weight_error_meV"] = dot(weights,action)-retained
    return row
end

function audit_pair(nodes, label, displacement, scales)
    lower=scaled_value(E_MIN*u"meV",scales,:energy)
    upper=scaled_value(E_MAX*u"meV",scales,:energy)
    scaled_delta=scaled_value(displacement,scales,:energy)
    scaled_energy=collect(range(lower,upper;length=nodes))
    Δ=(upper-lower)/(nodes-1)
    scaled_weights=fill(Δ,nodes)
    scaled_weights[[1,end]] ./= 2
    to_meV=1000scales.E₀_eV
    energy=scaled_energy .* to_meV
    energy[[1,end]] .= (E_MIN,E_MAX)
    weights=scaled_weights .* to_meV
    δ=scaled_delta*to_meV
    edges=vcat(first(energy),(energy[1:end-1]+energy[2:end])/2,last(energy))
    safe=BitVector(E_MIN+δ+Δ*to_meV <= e <= E_MAX-δ-Δ*to_meV for e in energy)
    funcs=(("constant", x -> 1.0), ("central_gaussian", x -> exp(-0.5*((x-PEAK_CENTER)/PEAK_SIGMA)^2)),
           ("edge_gaussian", x -> exp(-0.5*((x-PEAK_EDGE)/PEAK_SIGMA)^2)))
    fv=REF.build_conservative_shift_pair(scaled_energy,scaled_weights,scaled_delta)
    node_plus=NUM.build_shift_plan(scaled_energy,scaled_delta)
    node_minus=NUM.build_shift_plan(scaled_energy,-scaled_delta)
    schemes=((:nodal_linear,node_plus,node_minus),
             (:finite_volume_piecewise_constant,fv.plus,fv.minus))
    return Dict(
        "energy_nodes"=>nodes,"shift_pair"=>label,"shift_meV"=>δ,
        "schemes"=>map(schemes) do (scheme,plus,minus)
            report=NUM._shift_pair_validation(plus,minus,scaled_energy,scaled_weights,scaled_delta,scheme)
            actions=Dict{String,Any}[]
            # Both dense matrices use the same zero continuation as the sparse neighbor plan.
            matrices=scheme === :nodal_linear ?
                (REF.build_shift_matrix(scaled_energy,scaled_delta),REF.build_shift_matrix(scaled_energy,-scaled_delta)) :
                (plus,minus)
            for (matrix,signed_shift) in zip(matrices,(δ,-δ)), (name,f) in funcs
                push!(actions,shifted_action(matrix,energy,edges,weights,signed_shift,scheme,name,f,safe))
            end
            Dict("scheme"=>string(scheme),"core_metrics"=>Dict(string(k)=>v for (k,v) in pairs(report)),
                 "actions"=>actions)
        end |> collect,
    )
end

function run_shift(task::String,args::Vector{String})
    task=="SHIFT" && isempty(args) || error("Usage: SHIFT")
    BLAS.set_num_threads(1)
    scales=ScaleSystem()
    delays=(("LO",36.7u"meV"),("field_12p5",45.20u"meV"),("field_21",75.936u"meV"))
    combinations=[(n,label,δ) for n in (239,477,953) for (label,δ) in delays]
    rows=Vector{Dict{String,Any}}(undef,length(combinations))
    Threads.@threads for j in eachindex(combinations)
        rows[j]=audit_pair(combinations[j]...,scales)
    end
    group=Dict(row["shift_pair"]=>first(row["schemes"])["core_metrics"]["quadrature_adjoint"]
               for row in rows if row["energy_nodes"]==239)
    short=max(group["LO"],group["field_12p5"])
    working=max(group["LO"],group["field_21"])
    expected=(0.03287979746107182,0.033167906340332426)
    matches=[isapprox(x,y;rtol=0.0,atol=5e-14) for (x,y) in zip((short,working),expected)]
    fv_pass=all(last(row["schemes"])["core_metrics"]["quadrature_adjoint"] <= 1e-14 for row in rows)
    return Dict(
        "status"=>(all(matches) && fv_pass ? "measured" : "inconclusive"),
        "energy_min_meV"=>E_MIN,"energy_max_meV"=>E_MAX,
        "central_gaussian_center_meV"=>PEAK_CENTER,"edge_gaussian_center_meV"=>PEAK_EDGE,
        "gaussian_sigma_meV"=>PEAK_SIGMA,"control_peak_height"=>1.0,
        "interior_definition"=>"At least one energy spacing plus absolute shift from each window edge.",
        "quadrature_reference"=>"Cell averages evaluated by independent composited eight-point Gauss-Legendre; node control uses exact point values; zero continuation.",
        "error_norm"=>"Energy weights are trapezoidal widths in meV for both sampled and cell-average fields.",
        "E239_field_LO_maxima"=>[short,working],"E239_baseline_matches"=>matches,
        "finite_volume_adjoint_pass"=>fv_pass,"rows"=>rows,
    )
end

end

run_shift(task::String,args::Vector{String}) = V843ShiftAudit.run_shift(task,args)
