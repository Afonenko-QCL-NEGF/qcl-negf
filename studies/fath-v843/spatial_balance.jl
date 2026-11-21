module SpatialBalance

using LinearAlgebra
import QCLNEGF.LinkedTransport as LT

export spatial_balance

function diagonal_in_coordinates(op, frame)
    return vec(real.(sum((frame * op) .* conj.(frame); dims = 2)))
end

function add_hermitian_part!(destination, value, weight)
    destination .+= weight .* (value .+ value')
    return nothing
end

function local_source!(scratch, basis, source, buffer)
    fill!(scratch, 0)
    @views for field in 1:3, (side, q) in enumerate(basis)
        mul!(buffer, source[:, :, field, side], q)
        mul!(scratch[:, :, field], q', buffer, 1, 1)
    end
    return scratch
end

local_source!(scratch,basis,source) = local_source!(scratch,basis,source,similar(first(basis)))

function trace_product(a,b)
    sum = zero(eltype(a))
    @inbounds for j in axes(a,2), i in axes(a,1)
        sum += a[i,j]*b[j,i]
    end
    return sum
end

function current_metrics(profile, widths)
    interior = @view profile[2:end-1]
    mean_current = dot(interior, widths) / sum(widths)
    return (;
        mean_internal_A_cm2 = mean_current,
        full_range_A_cm2 = [minimum(profile), maximum(profile)],
        max_deviation_from_mean_A_cm2 = maximum(abs.(profile .- mean_current)),
        max_deviation_from_left_A_cm2 = maximum(abs.(profile .- first(profile))),
        target_tolerance_A_cm2 = max(1.0, 0.01abs(mean_current)),
        outward_A_cm2 = [-first(profile), last(profile)],
    )
end

function ring_balance(p, state_total, anchor, collision_sources, dual, center_metric,
        synchronized, energy_rule, coefficients, k)
    modes = size(p.h, 1)
    workspace = LT.TailWorkspace(p.geo)
    source = zeros(ComplexF64, modes, modes, 3)
    vertex_buffer = similar(LT.centered_basis(p.geo))
    hpart = zeros(ComplexF64, modes, modes)
    node_residual = similar(hpart)
    gain_greater, gain_lesser = similar(hpart), similar(hpart)
    product, raw_term = similar(hpart), similar(hpart)
    sum_lesser = similar(hpart)
    qframe = LT.centered_basis(p.geo)
    q_ret = similar(qframe)
    q_product = similar(qframe)
    q_image = zeros(ComplexF64,p.r,p.r)
    previous_pair = similar(q_image)
    kinetic_difference = 0.0
    kinetic_reference = 0.0
    contributions = [zeros(ComplexF64, modes, modes) for _ in LT.COLLISION_CHANNELS]
    energy_contributions = [zero(c) for c in contributions]
    coherent = zeros(ComplexF64, modes, modes)
    kinetic = zeros(ComplexF64, modes, modes)
    energy_coherent = zero(coherent)
    energy_kinetic = zero(kinetic)
    occupation = zeros(ComplexF64, modes, modes)
    current = zeros(p.nz+1)
    energy_current = zero(current)
    particle_exchange = zeros(length(contributions))
    electron_power = zeros(length(contributions))
    radial_number = 0.0
    max_dyson_residual = 0.0
    max_coherent_ratio = 0.0
    rule = isnothing(energy_rule) ? (points=p.en, weights=p.we) :
        energy_rule(p, @view(state_total[:, :, :, k]), @view(anchor[:, :, k]), k)
    energies, measure = rule.points, rule.weights
    length(energies) == length(measure) && all(>(0), measure) &&
        isapprox(sum(measure), sum(p.we); rtol=2e-12, atol=1e-14) ||
        throw(ArgumentError("energy measure changed across the independent profile"))
    dual_h = dual * @view(p.h[:, :, k])
    gain_measure = center_metric * dual
    radial = p.wk[k] * p.spin_degeneracy / (2π)
    for start in 1:128:length(energies)
        window = start:min(start+127, length(energies))
        points = @view energies[window]
        local_plan = LT.CausalRows(p.en, LT.shifted_queries(p.geo, points))
        @views image_source = LT.sample_packed_ring(local_plan, state_total[:, :, :, k], anchor[:, :, k])
        @views kernels = [LT.sample_packed_ring(local_plan, collision_sources[:, :, :, k, j],
            p.const_by_channel[:, :, k, j]) for j in eachindex(contributions)]
        for (i,node_energy) in enumerate(points)
            weight = radial * measure[window[i]]
            energy_weight = node_energy*weight
            @views LT.sample_node!(workspace, p.geo, node_energy, p.h[:, :, k],
                p.hops[:, k], image_source[:, :, :, i, :])
            @views retarded, lesser, greater = (workspace.mode_green[:, :, j] for j in 1:3)
            current .+= weight .* @view(workspace.bond_profile[:, 1])
            energy_current .+= energy_weight .* @view(workspace.bond_profile[:, 1])
            radial_number += weight * imag(tr(@view workspace.local_green[:, :, 2]))
            occupation .-= im * weight .* lesser
            mul!(hpart, dual_h, lesser)
            add_hermitian_part!(coherent, hpart, weight)
            add_hermitian_part!(energy_coherent, hpart, energy_weight)
            node_residual .= hpart .+ hpart'
            coherent_magnitude = norm(node_residual)
            mul!(gain_greater, greater, gain_measure)
            mul!(gain_lesser, lesser, gain_measure)
            fill!(sum_lesser,0)
            for j in eachindex(contributions)
                local_source!(source, p.geo.bases, @view(kernels[j][:, :, :, i, :]), vertex_buffer)
                @views sr, sl, sg = (source[:, :, n] for n in 1:3)
                gain = real(trace_product(sl,gain_greater) - trace_product(sg,gain_lesser))
                particle_exchange[j] += weight * gain
                electron_power[j] += node_energy * weight * gain
                mul!(product,sl,dual)
                mul!(raw_term,retarded,product)
                mul!(product,sr,lesser)
                mul!(raw_term,dual,product,-1,1)
                add_hermitian_part!(contributions[j], raw_term, weight)
                add_hermitian_part!(energy_contributions[j], raw_term, energy_weight)
                node_residual .-= raw_term .+ raw_term'
                isnothing(coefficients) || (sum_lesser .+= sl)
            end
            if !isnothing(coefficients)
                a,c = coefficients
                @views previous_pair .= a.*workspace.local_green[:,:,2] .- c.*workspace.local_green[:,:,3]
                mul!(q_ret,qframe,retarded)
                mul!(q_product,q_ret,sum_lesser)
                mul!(q_image,q_product,q_ret')
                q_image .-= previous_pair
                kinetic_difference += weight*sum(abs2,q_image)
                kinetic_reference += weight*sum(abs2,previous_pair)
            end
            kinetic .+= weight .* node_residual
            energy_kinetic .+= energy_weight .* node_residual
            residual = norm(node_residual)
            max_coherent_ratio = max(max_coherent_ratio, residual / max(coherent_magnitude, 1e-14))
            if synchronized
                max_dyson_residual = max(max_dyson_residual, residual / max(norm(lesser)*norm(dual_h), 1e-14))
            end
        end
    end
    transverse_operator = dual * (@view(p.h[:, :, k]) - @view(p.h[:, :, 1]))
    transverse_energy = real(sum((transverse_operator * occupation) .* transpose(center_metric)))
    return (;current, coherent, kinetic, occupation, contributions, particle_exchange, electron_power,
        energy_current, energy_coherent, energy_kinetic, energy_contributions,
        radial_number, transverse_energy, max_dyson_residual, max_coherent_ratio,
        kinetic_difference,kinetic_reference)
end

"""
Reconstruct the physical two seams and interior faces from an unmixed linked
Dyson image. `state_sources` determine that image. Distinct `collision_sources`
expose the kinetic remainder of the lagged equation at the same Green state.
All terms use one positive energy and radial quadrature.
"""
function spatial_balance(problem, state_sources, widths;
        collision_sources = state_sources, energy_rule = nothing, workers = 1,
        progress = (_)->nothing, coefficients = nothing, current_cuts = nothing)
    p = problem
    length(widths) == p.nz-1 && all(>(0), widths) ||
        throw(ArgumentError("weights must match the positive interior face widths"))
    dimensions = (p.r^2, 2, p.ne, p.nk, length(LT.COLLISION_CHANNELS))
    size(state_sources) == size(collision_sources) == dimensions || throw(DimensionMismatch("packed source axes differ"))
    modes = size(p.h, 1)
    dual = Hermitian(p.geo.metric) \ Matrix{ComplexF64}(I, modes, modes)
    center = p.geo.modes[(first(p.geo.monitor)+1):(last(p.geo.monitor)-1), :]
    center_metric = center' * center
    columns = p.geo.center_modes
    central_metric = Hermitian(p.geo.metric[columns, columns])
    bands = eigen(Hermitian(p.h[columns, columns, 1]), central_metric)
    band_covectors = p.geo.metric[:, columns] * bands.vectors
    state_total = dropdims(sum(state_sources; dims=5); dims=5)
    anchor = dropdims(sum(p.const_by_channel; dims=4); dims=4)
    synchronized = collision_sources === state_sources
    workers > 0 || throw(ArgumentError("worker count must be positive"))
    ring_results = Vector{Any}(undef, p.nk)
    LT.N._production_worker_ranges!(p.nk, min(workers, Threads.nthreads(:default), p.nk)) do _, lo, hi
        for k in lo:hi
            balance = ring_balance(p, state_total, anchor, collision_sources, dual,
                center_metric, synchronized, energy_rule, coefficients, k)
            lateral_h = p.h[columns, columns, k] - p.h[columns, columns, 1]
            band_energy_meV = 100 .* real.(diag(bands.vectors' * lateral_h * bands.vectors))
            band_number = real.(diag(band_covectors' * balance.occupation * band_covectors))
            ring_results[k] = (;balance..., band_number, band_energy_meV)
            progress((; ring = k, rings = p.nk))
        end
    end
    scale = p.current_scale
    physical_profile = scale .* sum(x.current for x in ring_results)
    h = scale .* diagonal_in_coordinates(sum(x.coherent for x in ring_results), center)
    collision = [scale .* diagonal_in_coordinates(sum(x.contributions[j] for x in ring_results), center)
        for j in eachindex(LT.COLLISION_CHANNELS)]
    kinetic = scale .* diagonal_in_coordinates(sum(x.kinetic for x in ring_results), center)
    stencil_gap = diff(physical_profile) - h
    lifted_closure = diff(physical_profile) - stencil_gap - kinetic - sum(collision)
    energy_scale=1e3scale  # E₀/e = 0.1 V and A/cm² → A/m².
    energy_flux=energy_scale .* sum(x.energy_current for x in ring_results)
    energy_h=energy_scale .* diagonal_in_coordinates(sum(x.energy_coherent for x in ring_results),center)
    energy_kinetic=energy_scale .* diagonal_in_coordinates(sum(x.energy_kinetic for x in ring_results),center)
    energy_gap=diff(energy_flux) - energy_h
    energy_collisions=[energy_scale .* diagonal_in_coordinates(
        sum(x.energy_contributions[j] for x in ring_results),center) for j in eachindex(collision)]
    energy_closure=diff(energy_flux)-energy_gap-energy_kinetic-sum(energy_collisions)
    local_energy = if isnothing(current_cuts)
        nothing
    else
        cuts = current_cuts
        length(cuts)==p.nz+1 && all(>(0),diff(cuts)) ||
            throw(ArgumentError("physical cut coordinates do not match energy flux"))
        cell_fraction = (cuts .- first(cuts)) ./ (last(cuts)-first(cuts))
        potential_shift = 0.1p.geo.voltage .* cell_fraction
        avg_faces(x) = (x[1:end-1] .+ x[2:end])./2
        local_flux = energy_flux .+ 1e4 .* potential_shift .* physical_profile
        field_work = 1e4dot(diff(potential_shift),avg_faces(physical_profile))
        offset_work = 1e4dot(avg_faces(potential_shift),diff(physical_profile))
        (;outward_W_m2=[-first(local_flux),last(local_flux)],
            field_work_W_m2=field_work,
            offset_times_number_exchange_W_m2=offset_work,
            net_relative_energy_minus_absolute_flux_and_work_W_m2=
                last(local_flux)-first(local_flux)-(last(energy_flux)-first(energy_flux))-field_work-offset_work)
    end
    prefix(v) = [0.0; cumsum(v)]
    radial_number = [x.radial_number for x in ring_results]
    sheet_number = sum(radial_number)
    transverse_energy_meV = 100sum(x.transverse_energy for x in ring_results)/sheet_number
    band_number = sum(x.band_number for x in ring_results)
    band_moment = sum(x.band_number .* x.band_energy_meV for x in ring_results)
    band_fraction = band_number ./ sum(band_number)
    band_temperature = [n > 0 ? e / n / 0.08617333262145 : nothing
        for (n,e) in zip(band_number, band_moment)]
    return (;
        current_A_cm2 = physical_profile,
        coherent_projected_A_cm2 = first(physical_profile) .+ prefix(h),
        kinetic_remainder_A_cm2 = prefix(kinetic),
        spatial_projection_gap_A_cm2 = prefix(stencil_gap),
        collision_cumulative_A_cm2 = Dict(string(n)=>prefix(v) for (n,v) in zip(LT.COLLISION_CHANNELS, collision)),
        maximum_closure_error_A_cm2 = maximum(abs.(lifted_closure)),
        maximum_exact_dyson_residual = synchronized ? maximum(x.max_dyson_residual for x in ring_results) : nothing,
        maximum_mode_balance_relative_to_coherent = maximum(x.max_coherent_ratio for x in ring_results),
        weighted_rK_Q = isnothing(coefficients) ? nothing :
            sqrt(sum(x.kinetic_difference for x in ring_results) /
                max(sum(x.kinetic_reference for x in ring_results),1e-300)),
        current = current_metrics(physical_profile, widths),
        raw_sheet_cm2 = sheet_number * p.density_scale,
        raw_ring_sheet_cm2 = radial_number .* p.density_scale,
        raw_lambda = sheet_number/p.target_dimless,
        transverse_energy_meV,
        equivalent_temperature_K = transverse_energy_meV / 0.08617333262145,
        central_bands = (;
            reference_energy_meV = 100 .* bands.values,
            sheet_cm2 = band_number .* p.density_scale,
            fraction = band_fraction,
            equivalent_temperature_K = band_temperature,
            population_weighted_temperature_K = sum(band_moment) / sum(band_number) / 0.08617333262145,
            total_sheet_over_physical_sheet = sum(band_number) / sheet_number,
            fraction_by_ring_and_band = [x.band_number ./ sum(band_number) for x in ring_results],
            kinetic_energy_meV_by_ring = [x.band_energy_meV for x in ring_results],
        ),
        particle_exchange_A_cm2 = Dict(string(n)=>scale*x for (n,x) in zip(LT.COLLISION_CHANNELS,
            sum(r.particle_exchange for r in ring_results))),
        carrier_power_W_m2 = Dict(string(n)=>1e3scale*x for (n,x) in zip(LT.COLLISION_CHANNELS,
            sum(r.electron_power for r in ring_results))),
        spectral_energy_budget = (;
            absolute_outward_W_m2=[-first(energy_flux),last(energy_flux)],
            absolute_flux_difference_W_m2=last(energy_flux)-first(energy_flux),
            projected_collision_power_W_m2=Dict(string(n)=>sum(v)
                for (n,v) in zip(LT.COLLISION_CHANNELS,energy_collisions)),
            projection_gap_W_m2=sum(energy_gap),
            kinetic_remainder_W_m2=sum(energy_kinetic),
            maximum_closure_error_W_m2=maximum(abs,energy_closure),
            relative_to_local_potential=local_energy,
        ),
    )
end

end
