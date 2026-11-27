module V843OperatorAudit

using LinearAlgebra
using QCLNEGF
using Unitful

include(joinpath(@__DIR__, "..", "fath-v843", "controls", "v843-input", "dupont", "dupont_device.jl"))

const ANGLES = (32,128,512)
const QZ = (161,321,641)
const RADIAL_SIGMA_NM = 0.20
const DENSITY_SIGMA_NM = 2.0
const ADAPTIVE_RTOL = (1e-7,1e-9)
const E_CHARGE = 1.602176634e-19
const EPS_VACUUM = 8.8541878128e-12
const IMP_NAMES = ("angles32","angles128","angles512","adaptive_coarse","adaptive_tight")
const LO_NAMES = ("angles32_qz161","angles128_qz161","angles512_qz161","exact_qz161","exact_qz321","exact_qz641")

function operator_grid(k; nz=144, nqz=161, nphi=32)
    scales = ScaleSystem()
    inputs = DupontDevice.physical_inputs(21.0)
    n = NumericalParameters(N_z=nz,N_b=7,P_basis=3,E_min=-650u"meV",E_max=1000u"meV",
        N_E=239,M_E=390u"meV",k_max=0.6u"nm^-1",N_k=k,N_φ=nphi,
        qz_max=10u"nm^-1",N_qz=nqz,η_seed=0.5u"meV")
    grids = build_grids(inputs.physical,n,scales)
    profiles = DupontDevice.sheet_profiles(inputs.physical,n,scales,grids,inputs.donor_center)
    return (;inputs,scales,n,grids,profiles)
end

# q² evaluated in its positive form to avoid subtracting nearly equal diagonals.
momentum(k,kp,φ) = hypot(k-kp, 2sqrt(k*kp)*sin(φ/2))

function impurity_integrand(k,kp,screen,dx,distances,angle)
    q = momentum(k,kp,angle)
    ratio = exp(-q*dx)
    amplitude = inv((q+screen)^2)
    result = Vector{Float64}(undef,distances)
    @inbounds for l in eachindex(result)
        result[l] = amplitude
        amplitude *= ratio
    end
    return result
end

function uniform_impurity(k,kp,screen,dx,distances,angles)
    integral = zeros(distances)
    for j in 0:(angles-1)
        integral .+= impurity_integrand(k,kp,screen,dx,distances,2π*j/angles)
    end
    return integral ./ angles
end

# Vector adaptive Simpson, independent of the periodic trapezoidal discretization.
# The shared component bound is the zero-distance integrand at minimum q.
function adaptive_impurity(k,kp,screen,dx,distances,rtol)
    integrand(φ) = impurity_integrand(k,kp,screen,dx,distances,φ)
    f0, fm, f1 = integrand(0.0), integrand(π/2), integrand(Float64(π))
    initial = (π/6) .* (f0 .+ 4 .* fm .+ f1)
    tolerance = π * rtol / (abs(k-kp)+screen)^2
    function refine(a,b,left,center,right,coarse,tol,depth)
        midpoint = (a+b)/2
        q1,q3 = integrand((a+midpoint)/2),integrand((midpoint+b)/2)
        first = ((b-a)/12) .* (left .+ 4 .* q1 .+ center)
        second = ((b-a)/12) .* (center .+ 4 .* q3 .+ right)
        improved = first .+ second
        delta = improved .- coarse
        if maximum(abs,delta) <= 15tol
            return improved .+ delta ./ 15
        end
        depth > 0 || error("Adaptive impurity quadrature exhausted refinement depth")
        return refine(a,midpoint,left,q1,center,first,tol/2,depth-1) .+
               refine(midpoint,b,center,q3,right,second,tol/2,depth-1)
    end
    return refine(0.0,Float64(π),f0,fm,f1,initial,tolerance,24) ./ π
end

function impurity_data(problem)
    (;inputs,scales,grids,profiles) = problem
    k = grids.κ
    dx = only(unique(grids.wˣ))
    donor = grids.wˣ .* profiles.Nᴰ ./ scales.L₀_m^2
    active = findall(>(0),donor)
    length(active) in (1,2) || error("Unexpected donor support")
    isapprox(sum(donor),ustrip(u"m^-2",inputs.physical.N_dop²ᴰ)*inputs.physical.f_ion;rtol=1e-12) ||
        error("Incorrect donor normalization")
    screen = scaled_value(inputs.physical.q_s,scales,:wavenumber)
    screen > 0 || error("Impurity screening must be positive")
    prefactor = E_CHARGE^2/(2EPS_VACUUM*inputs.physical.ε_s*scales.E₀_J)
    nz = length(grids.x)
    lookup = [abs(i-d)+abs(j-d)+1 for i in 1:nz,j in 1:nz,d in active]
    distances = maximum(lookup)
    pairs = [(i,j) for i in eachindex(k) for j in i:length(k)]
    values = Array{Float64}(undef,distances,length(k),length(k),length(IMP_NAMES))
    Threads.@threads for (i,j) in pairs
        kernels = (
            (uniform_impurity(k[i],k[j],screen,dx,distances,n) for n in ANGLES)...,
            (adaptive_impurity(k[i],k[j],screen,dx,distances,tol) for tol in ADAPTIVE_RTOL)...,
        )
        for (c,x) in enumerate(kernels)
            values[:,i,j,c] = x
            i == j || (values[:,j,i,c] = x)
        end
    end
    return (;values,lookup,amplitudes=prefactor^2 .* donor[active], pairs,screen,active,donor)
end

function qz_plan(problem, nodes)
    grids = nodes == length(problem.grids.qᶻ) ? problem.grids :
        operator_grid(length(problem.grids.κ);nz=length(problem.grids.x),nqz=nodes).grids
    (;inputs,scales) = problem
    e_lo = ustrip(u"J",uconvert(u"J",inputs.physical.ħωᴸᴼ))
    prefactor = E_CHARGE^2*e_lo/(2EPS_VACUUM) * (1/inputs.physical.ε_∞ - 1/inputs.physical.ε_s)
    weights = grids.wᑫᶻ .* (prefactor/(2π*scales.E₀_J^2*scales.L₀_m))
    distances = only(unique(grids.wˣ)) .* collect(0:(length(grids.x)-1))
    phases = cos.(distances * transpose(grids.qᶻ))
    return (;qz2=grids.qᶻ.^2,weights,phases)
end

function lo_diagonal(plan, k,kp, screen2, angle_count)
    scale = plan.qz2 .+ screen2
    if isnothing(angle_count)
        return plan.phases * (plan.weights ./ sqrt.((scale .+ (k-kp)^2) .* (scale .+ (k+kp)^2)))
    end
    average = zeros(length(scale))
    for j in 0:(angle_count-1)
        q2 = (k-kp)^2 + 4k*kp*sin(π*j/angle_count)^2
        average .+= 1.0 ./ (scale .+ q2)
    end
    return plan.phases * (plan.weights .* (average ./ angle_count))
end

function lo_data(problem)
    (;inputs,scales,grids) = problem
    k = grids.κ
    screen2 = scaled_value(inputs.physical.qᴸᴼ_s,scales,:wavenumber)^2
    screen2 > 0 || error("LO screening must be positive")
    plans = map(n -> qz_plan(problem,n),QZ)
    nz = length(grids.x)
    pairs = [(i,j) for i in eachindex(k) for j in i:length(k)]
    values = Array{Float64}(undef,nz,length(k),length(k),length(LO_NAMES))
    Threads.@threads for (i,j) in pairs
        kernels = (
            (lo_diagonal(first(plans),k[i],k[j],screen2,n) for n in ANGLES)...,
            (lo_diagonal(plan,k[i],k[j],screen2,nothing) for plan in plans)...,
        )
        for (c,x) in enumerate(kernels)
            values[:,i,j,c] = x
            i == j || (values[:,j,i,c] = x)
        end
    end
    lookup = reshape([abs(i-j)+1 for i in 1:nz,j in 1:nz],nz,nz,1)
    return (;values,lookup,amplitudes=[1.0],pairs,screen=sqrt(screen2))
end

function assign_matrix(data, radial)
    shape = size(data.lookup)
    result = zeros(shape[1],shape[2])
    for h in eachindex(data.amplitudes)
        lookup = view(data.lookup,:,:,h)
        @inbounds for j in eachindex(result)
            result[j] += data.amplitudes[h] * radial[lookup[j]]
        end
    end
    return result
end

function norms(errors, reference, coordinate_weights)
    weighted_norm(M) = sqrt(sum(abs2(M[i,j])*coordinate_weights[i]*coordinate_weights[j]
                               for i in axes(M,1),j in axes(M,2)))
    absolute, denominator = weighted_norm(errors),weighted_norm(reference)
    result = Dict{String,Any}("absolute_l2"=>absolute,"reference_l2"=>denominator,
                  "relative_defined"=>!iszero(denominator))
    iszero(denominator) || (result["relative_l2"] = absolute/denominator)
    return result
end

function coordinate_fields(problem)
    (;grids,inputs,scales)=problem
    w = grids.wˣ
    z_nm = grids.x .* (scales.L₀_m*1e9)
    donor_nm = ustrip(u"nm",inputs.donor_center)
    # |ψ|² has the prescribed density width; ψ carries twice the variance in its exponent.
    packet = exp.(-((z_nm .- donor_nm) ./ DENSITY_SIGMA_NM).^2 ./ 4)
    packet ./= sqrt(dot(w,abs2.(packet)))
    return (("diagonal", Matrix(Diagonal(fill(1/sum(w),length(w))))),
            ("gaussian_projector",packet*transpose(packet)))
end

function weighted_action(data, incoming, weights, output, variant)
    reduced = view(data.values,:,incoming,output,variant) * weights
    return assign_matrix(data,reduced)
end

function ring_comparison(data, problem, reference, variant; coarse=nothing)
    (;grids,scales) = problem
    radial_to_nm = 1e-9/scales.L₀_m
    radial_gaussian = exp.(-(grids.κ .* (radial_to_nm/RADIAL_SIGMA_NM)).^2)
    fine_weights = grids.wᵏ .* radial_gaussian
    out = isnothing(coarse) ? collect(eachindex(grids.κ)) : collect(1:2:length(grids.κ))
    coarse_weights = isnothing(coarse) ? Float64[] : coarse.grids.wᵏ .* radial_gaussian[out]
    if !isnothing(coarse)
        # Compare actual nested abscissae and use each grid's own positive measure.
        maximum(abs,coarse.grids.κ .- grids.κ[out]) < 2eps(maximum(grids.κ)) ||
            error("K17 and K33 must share the same outgoing radii")
    end
    return map(coordinate_fields(problem)) do (name,input)
        results=Vector{Dict{String,Any}}(undef,length(out))
        Threads.@threads for j in eachindex(out)
            i = out[j]
            ref = weighted_action(data,eachindex(grids.κ),fine_weights,i,reference) .* input
            actual = if isnothing(coarse)
                weighted_action(data,eachindex(grids.κ),fine_weights,i,variant) .* input
            else
                weighted_action(data,out,coarse_weights,i,variant) .* input
            end
            delta = actual-ref
            measure = grids.wˣ
            results[j] = merge(norms(delta,ref,measure),Dict(
                "k_nm_inverse"=>grids.κ[i]*radial_to_nm,
                "coarse_or_variant_trace"=>dot(measure,diag(actual)),
                "reference_trace"=>dot(measure,diag(ref)),
                "signed_trace_error"=>dot(measure,diag(delta)),
            ))
        end
        weights = isnothing(coarse) ? grids.wᵏ : coarse.grids.wᵏ
        absolute = sqrt(dot(weights, [row["absolute_l2"]^2 for row in results]))
        denominator = sqrt(dot(weights,[row["reference_l2"]^2 for row in results]))
        action = Dict{String,Any}("absolute_l2"=>absolute,"reference_l2"=>denominator,"relative_defined"=>!iszero(denominator))
        iszero(denominator) || (action["relative_l2"] = absolute/denominator)
        signed = dot(weights,[row["signed_trace_error"] for row in results])
        unsigned = dot(weights,[abs(row["signed_trace_error"]) for row in results])
        if !isnothing(coarse)
            fine_traces = Vector{Float64}(undef,length(grids.κ))
            Threads.@threads for i in eachindex(fine_traces)
                fine = weighted_action(data,eachindex(grids.κ),fine_weights,i,reference)
                fine_traces[i] = dot(grids.wˣ,diag(fine).*diag(input))
            end
            action["whole_grid_fine_trace"] = dot(grids.wᵏ,fine_traces)
            action["whole_grid_coarse_trace"] = dot(weights,[row["coarse_or_variant_trace"] for row in results])
            action["whole_grid_trace_difference"] = action["whole_grid_coarse_trace"]-action["whole_grid_fine_trace"]
        end
        Dict("field"=>name,"ring_weighted_action"=>action,"ring_weighted_signed_trace_error"=>signed,
             "ring_weighted_absolute_trace_error"=>unsigned,"outgoing_rings"=>results)
    end |> collect
end

function covariance_comparison(data,problem,reference,variant)
    categories = ("diagonal","neighbor","remote")
    counts=zeros(Int,3)
    worst=zeros(3)
    absolute_squared=zeros(3)
    reference_squared=zeros(3)
    pair_norms=Vector{Tuple{Float64,Float64}}(undef,length(data.pairs))
    Threads.@threads for k in eachindex(data.pairs)
        i,j=data.pairs[k]
        ref = assign_matrix(data,view(data.values,:,i,j,reference))
        pred = assign_matrix(data,view(data.values,:,i,j,variant))
        stat = norms(pred-ref,ref,problem.grids.wˣ)
        pair_norms[k] = (stat["absolute_l2"],stat["reference_l2"])
    end
    for (k,(i,j)) in enumerate(data.pairs)
        category = min(3,j-i+1)
        multiplicity = i == j ? 1 : 2
        weight = multiplicity*problem.grids.wᵏ[i]*problem.grids.wᵏ[j]
        a,b = pair_norms[k]
        counts[category] += multiplicity
        absolute_squared[category] += weight*a^2
        reference_squared[category] += weight*b^2
        iszero(b) || (worst[category] = max(worst[category],a/b))
    end
    return map(eachindex(categories)) do i
        result=Dict("pair_class"=>categories[i],"ordered_pairs"=>counts[i],
                    "radially_weighted_absolute_l2"=>sqrt(absolute_squared[i]),
                    "radially_weighted_reference_l2"=>sqrt(reference_squared[i]))
        if reference_squared[i] > 0
            result["radially_weighted_relative_l2"]=sqrt(absolute_squared[i]/reference_squared[i])
            result["max_relative_l2"]=worst[i]
        end
        result
    end |> collect
end

function comparison(data,problem,reference,variant,name)
    return Dict("rule"=>name,"covariance"=>covariance_comparison(data,problem,reference,variant),
                "fields"=>ring_comparison(data,problem,reference,variant))
end

function summarize_impurity(k)
    problem = operator_grid(k)
    data = impurity_data(problem)
    variants = [comparison(data,problem,5,v,IMP_NAMES[v]) for v in 1:4]
    scales = problem.scales
    indices = findall(isapprox(0.30;atol=1e-12,rtol=0.0),
                      problem.grids.κ .* (1e-9/scales.L₀_m))
    i = only(indices)
    scalar = collect(data.values[1,i,i,:])
    out=Dict(
        "radial_nodes"=>k,"reference_rule"=>"independent adaptive Simpson over [0,π], tightened",
        "adaptive_scaled_relative_targets"=>collect(ADAPTIVE_RTOL),
        "nominal_screen_nm_inverse"=>data.screen*1e-9/scales.L₀_m,
        "donor_grid_cells"=>data.active,"donor_sheets_m_minus_2"=>data.donor[data.active],
        "diagonal_k0p30_zero_distance"=>Dict(
            "rules"=>collect(IMP_NAMES),"values_before_donor_and_prefactor"=>scalar,
            "relative_errors"=>abs.(scalar ./ last(scalar) .- 1),
        ),
        "comparisons"=>variants,
    )
    if k==33
        out["shared_K17_K33"] = ring_comparison(data,problem,5,5;coarse=operator_grid(17))
    end
    return out
end

function summarize_lo(k)
    problem = operator_grid(k)
    data = lo_data(problem)
    angles = [comparison(data,problem,4,v,LO_NAMES[v]) for v in 1:3]
    qz = [comparison(data,problem,6,v,LO_NAMES[v]) for v in 4:5]
    return Dict(
        "radial_nodes"=>k,"screen_nm_inverse"=>data.screen*1e-9/problem.scales.L₀_m,
        "qz_max_nm_inverse"=>10.0,
        "angular_reference_rule"=>LO_NAMES[4],"longitudinal_reference_rule"=>LO_NAMES[6],
        "angular_comparisons"=>angles,"longitudinal_comparisons"=>qz,
    )
end

function run_operators(task::String,args::Vector{String})
    BLAS.set_num_threads(1)
    grids = if task in ("IMP17","IMP33") && isempty(args)
        [summarize_impurity(parse(Int,task[4:end]))]
    elseif task=="LO" && (isempty(args) || args==["17"] || args==["33"])
        map(summarize_lo,isempty(args) ? [17,33] : parse.(Int,args))
    else
        error("Usage: IMP17, IMP33 or LO [17|33]")
    end
    return Dict(
        "status"=>"measured","coordinate_cells"=>144,"k_max_nm_inverse"=>0.60,
        "model_field_kV_cm"=>21.0,"temperature_K"=>50.0,
        "radial_test_sigma_nm_inverse"=>RADIAL_SIGMA_NM,
        "gaussian_density_sigma_nm"=>DENSITY_SIGMA_NM,
        "coordinate_action"=>"Hadamard product of coordinate covariance with each unit-trace test matrix, summed over incoming Core ring weights times radial test profile",
        "matrix_norm"=>"Weighted Frobenius L2: sqrt(sum(w_z[i]*w_z[j]*abs2(M[i,j]))); signed trace uses one coordinate weight; Core nondimensional units",
        "radial_measure"=>"Positive annular Core weights ∫κ dκ/(2π), including half-width endpoint cells",
        "scalar_pair_classes"=>"Diagonal, nearest radial index, all other pairs. Off-diagonal pairs counted twice.",
        "grids"=>grids,
    )
end

end

run_operators(task::String,args::Vector{String}) = V843OperatorAudit.run_operators(task,args)
