include("lo_control.jl")

function equilibrium_grid(step)
    radius = ceil(Int,1/step)
    energy = collect(-radius:radius).*step
    length(energy)>2 || error("empty thermal control")
    weights = [step/2;fill(step,length(energy)-2);step/2]
    beta = 100/(0.08617333262145*10)
    x = beta.*(energy.-0.02)
    occ = exp.(-max.(x,0.0))./(1 .+exp.(-abs.(x)))
    empty = exp.(min.(x,0.0))./(1 .+exp.(-abs.(x)))
    green=zeros(1,2,length(energy),2)
    for (ring,center) in enumerate((-0.15,0.21))
        spectrum=0.1 .+ exp.(-((energy.-center)./0.33).^2)
        green[1,1,:,ring] .= spectrum.*occ
        green[1,2,:,ring] .= spectrum.*empty
    end
    sites=zeros(0,1)
    covariance=reshape(ComplexF64[0.8,0.2,0.2,1.3],1,1,2,2)
    function evaluate(pair)
        v=LT.LocalCollisionKernels(ones(1,1),[0.31,0.69],zeros(1),zeros(1),sites,
            zeros(2,2),covariance,zeros(1,1,2,2),pair.plus,pair.minus,inv(expm1(beta*FATH_LO)))
        x=lo_events(green,v,sites,energy,weights,FATH_LO)
        return (;x.emission,x.absorption,x.net_events,
            x.stationwise_collision_l1_relative,x.combined_operator_relative,
            x.emission_loss_meV_per_event,x.absorption_gain_meV_per_event,
            normalized_equilibrium_energy_error_meV=x.electron_power_meV/(x.emission.events+x.absorption.events))
    end
    return (;step_meV=100step,
        cell=evaluate(campaign_conservative_shift_pair(energy,weights,FATH_LO)),
        hat=evaluate(hat_shift_pair(energy,weights,FATH_LO)))
end

function thermal_main()
    length(ARGS)==1 || error("Usage: lo_thermal_grid.jl OUTPUT")
    output=only(ARGS)
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    rows=map(equilibrium_grid,[0.02,0.01,0.005,FATH_LO/18,0.001])
    @assert rows[4].cell.stationwise_collision_l1_relative < 3e-12
    @assert rows[5].cell.stationwise_collision_l1_relative < 3e-12
    open(output,"w") do io
        Runner._light_json(io,(;temperature_K=10.0,rows,
            core=Runner._linked_package_identity(Runner.QCLNEGF),
            runner=Runner._linked_package_identity(Runner),runtime=Runner._runtime_toolchain_provenance()))
        println(io)
    end
end

abspath(PROGRAM_FILE)==abspath(@__FILE__) && thermal_main()
