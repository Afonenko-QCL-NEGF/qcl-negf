include("../fath-v843/profile_experiment.jl")
include("../fath-v843/controls/v843-input/method/pinned/conservative_shifts.jl")
include("lo_measure.jl")

function equilibrium_fixture(step, omega, beta)
    energy = collect(range(-3step,3step;length=7))
    weights = [step/2;fill(step,5);step/2]
    base = campaign_conservative_shift_pair(energy,weights,omega)
    alternate = hat_shift_pair(energy,weights,omega)
    green = zeros(1,2,length(energy),2)
    for (k,spectrum) in enumerate(([1.,4.,2.,3.,5.,2.,1.],[2.,1.,3.,7.,6.,3.,2.]))
        f = 1 ./ (1 .+exp.(beta.*(energy.-0.02)))
        green[1,1,:,k] .= spectrum.*f
        green[1,2,:,k] .= spectrum.*(1 .-f)
    end
    ifr_sites = zeros(0,1)
    covariance = reshape(ComplexF64[0.8,0.2,0.2,1.3],1,1,2,2)
    function measure(pair)
        v = LT.LocalCollisionKernels(ones(1,1),[0.31,0.69],zeros(1),zeros(1),ifr_sites,
            zeros(2,2),covariance,zeros(1,1,2,2),pair.plus,pair.minus,inv(expm1(beta*omega)))
        return (;shift=shift_metrics(energy,weights,pair.plus,pair.minus,omega),
            balance=lo_events(green,v,ifr_sites,energy,weights,omega))
    end
    return (;step_meV=100step,equilibrium_beta=beta,base=measure(base),alternate=measure(alternate))
end

function main()
    length(ARGS)==1 || error("Usage: lo_control.jl FIXTURE_JSON")
    output = only(ARGS)
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    aligned = equilibrium_fixture(FATH_LO,FATH_LO,7.)
    off_grid = equilibrium_fixture(0.125,FATH_LO,7.)
    exact = aligned.base.balance
    @assert exact.stationwise_collision_l1_relative < 2e-15
    @assert isapprox(exact.emission.events,exact.absorption.events;rtol=2e-15)
    @assert isapprox(exact.emission_loss_meV_per_event,36.7;atol=2e-13)
    @assert isapprox(exact.absorption_gain_meV_per_event,36.7;atol=2e-13)
    for record in (aligned.base,aligned.alternate,off_grid.base,off_grid.alternate)
        @assert record.balance.emission.number_relative < 5e-14
        @assert record.balance.absorption.number_relative < 5e-14
        @assert record.shift.maximum_row_overfill < 5e-14
    end
    open(output,"w") do io
        Runner._light_json(io,(;aligned,off_grid,
            core=Runner._linked_package_identity(Runner.QCLNEGF),
            runner=Runner._linked_package_identity(Runner),runtime=Runner._runtime_toolchain_provenance()))
        println(io)
    end
end

abspath(PROGRAM_FILE)==abspath(@__FILE__) && main()
