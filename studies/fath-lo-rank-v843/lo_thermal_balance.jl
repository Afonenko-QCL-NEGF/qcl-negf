include("fath_factorial.jl")
include("../fath-v843/controls/v843-input/method/pinned/conservative_shifts.jl")

function discrete_thermal_pair(energy, weights, plus, minus, bose, temperature)
    rows,cols,value = findnz(plus)
    jumps = energy[cols].-energy[rows]
    all(>(0),jumps) || error("LO emission paths must descend in nodal energy")
    beta = 100/(0.08617333262145*temperature)
    # The existing emission pairs are kept. Their reverse uses the Boltzmann
    # ratio evaluated at the actual difference of the two electronic nodes.
    absorption_plus = sparse(rows,cols,(1+bose).*value.*exp.(-beta.*jumps),size(plus)...)
    absorption_minus = spdiagm(1 ./ weights)*transpose(weights.*absorption_plus)
    thermal_l = (1+bose).*plus + absorption_minus
    thermal_g = (1+bose).*minus + absorption_plus
    return (;transfer=(thermal_l,thermal_g),
        maximum_absorption_pair_weight=maximum(absorption_plus),
        relative_absorption_change=norm(absorption_plus-bose.*plus)/norm(bose.*plus))
end

function scalar_equilibrium(thermal_temperature)
    step = 0.02
    energy = collect(-50:50).*step
    weights = [step/2;fill(step,length(energy)-2);step/2]
    pair = campaign_conservative_shift_pair(energy,weights,FATH_LO)
    x = 100 .* (energy.-0.02)./(0.08617333262145*thermal_temperature)
    normalizer = 1 .+ exp.(-abs.(x))
    f = exp.(-max.(x,0.0))./normalizer
    hole = exp.(min.(x,0.0))./normalizer
    green = zeros(1,2,length(energy),2)
    for (ring,center) in enumerate((-0.15,0.21))
        spectrum = 0.1 .+ exp.(-((energy.-center)./0.33).^2)
        green[1,1,:,ring] .= spectrum.*f
        green[1,2,:,ring] .= spectrum.*hole
    end
    bose = inv(expm1(100FATH_LO/(0.08617333262145*thermal_temperature)))
    v = LT.LocalCollisionKernels(ones(1,1),[0.31,0.69],zeros(1),zeros(1),zeros(0,1),
        zeros(2,2),reshape(ComplexF64[0.8,0.2,0.2,1.3],1,1,2,2),zeros(1,1,2,2),
        pair.plus,pair.minus,bose)
    correction = discrete_thermal_pair(energy,weights,pair.plus,pair.minus,bose,thermal_temperature)
    dest = zeros(1,2,length(energy),2,length(LT.COLLISION_CHANNELS))
    function equilibrium_collision(transfer)
        LT.scatter_packed!(dest,green,v;lo_occupation_transfer=transfer)
        gain = weights.*(@view(dest[1,1,:,:,1]).*@view(green[1,2,:,:])).*v.weights_k'
        loss = weights.*(@view(dest[1,2,:,:,1]).*@view(green[1,1,:,:])).*v.weights_k'
        return (;local_relative=sum(abs,gain-loss)/sum(gain+loss),
            particle_number_relative=abs(sum(gain)-sum(loss))/sum(gain+loss),
            energy_meV_per_total_event=100dot(energy,vec(sum(gain-loss;dims=2)))/sum(gain+loss))
    end
    plain, thermal = equilibrium_collision(nothing), equilibrium_collision(correction.transfer)
    @assert thermal.local_relative < 2e-13
    @assert thermal.particle_number_relative < 2e-13
    return (;temperature_K=thermal_temperature,plain,thermal,correction.relative_absorption_change)
end

function balance_main()
    length(ARGS) in (1,3) || error("Usage: lo_thermal_balance.jl [ARCHIVE WORKERS] OUTPUT")
    output=last(ARGS)
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    temperature=10.0
    fixture=scalar_equilibrium(temperature)
    physical = if length(ARGS)==1
        nothing
    else
        archive,workers_arg=ARGS[1:2]
        workers=parse(Int,workers_arg)
        input=Runner._read_linked_checkpoint(archive)
        p=input.problem
        input.identity["temperature_K"]==temperature && p.geo.voltage≈0.54 ||
            error("expected Fath at 54 mV and 10 K")
        correction=discrete_thermal_pair(p.en,p.we,p.v.lo_plus,p.v.lo_minus,p.v.bose,temperature)
        widths=(input.current_midpoints[3:end] .- input.current_midpoints[1:end-2])./2
        image=LT.linked_fresh_map(p,input.seed;projector=LT.project_linked_economical,
            selected_rows=true,projection_for_collision=true,workers,
            lo_occupation_transfer=correction.transfer)
        println(stderr,"thermal-balance Fath map complete")
        flush(stderr)
        comparison=linked_metrics(image.summary,widths)
        observation=spatial_balance(p,image.source,widths;workers,
            energy_rule=independent_energy_rule,current_cuts=input.current_midpoints)
        (;input.identity,workers,fixture,
            correction.relative_absorption_change,correction.maximum_absorption_pair_weight,
            summary=image.summary,comparison,observation,current_cuts_nm=input.current_midpoints,
            observer_max_difference_A_cm2=maximum(abs.(observation.current_A_cm2.-
                comparison.current_profile_A_cm2)))
    end
    open(output,"w") do io
        Runner._light_json(io,(;schema="qcl-negf-lo-thermal-balance/v1",fixture,physical,
            core=Runner._linked_package_identity(Runner.QCLNEGF),
            runner=Runner._linked_package_identity(Runner),runtime=Runner._runtime_toolchain_provenance()))
        println(io)
    end
end

abspath(PROGRAM_FILE)==abspath(@__FILE__) && balance_main()
