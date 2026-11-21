include("impurity_experiment.jl")
using HDF5

function shift_voltage(saved,model,voltage_mV)
    p=saved.problem
    expected=saved.identity["source_geometry_model_sha256"]
    bytes2hex(open(sha256,model))==expected || error("coordinate model identity differs")
    positions,widths=h5open(model,"r") do archive
        read(archive["position_dimensionless"]),read(archive["weight_position"])
    end
    length(positions)==length(widths)==p.nz || error("coordinate model axes differ")
    period=sum(widths)
    relative_position=vcat([positions./period .+ cell for cell in p.geo.offsets]...)
    W=p.geo.modes
    potential=W' * Diagonal(relative_position) * W
    voltage=voltage_mV/100
    h=cat([p.h[:,:,k] .- (voltage-p.geo.voltage).*potential for k in 1:p.nk]...;dims=3)
    changed=LT.LinkedProblem(p.en,p.we,p.wk,W,p.nb,p.geo.offsets,voltage,p.geo.reach,
        h,p.hops,p.const_by_channel,p.v;spin_degeneracy=p.spin_degeneracy,
        current_scale=p.current_scale,density_scale=p.density_scale,target_dimless=p.target_dimless)
    h_digest=bytes2hex(sha256(reinterpret(UInt8,vec(h))))
    identity=merge(saved.identity,Dict("parent_input_id"=>saved.identity["id"],
        "id"=>bytes2hex(sha256(saved.identity["id"]*":"*repr(voltage_mV)*":"*h_digest)),
        "rebias_hamiltonian_sha256"=>h_digest,"rebias_voltage_mV"=>voltage_mV))
    return merge(saved,(;problem=changed,identity))
end

if abspath(PROGRAM_FILE)==abspath(@__FILE__)
    length(ARGS)==5 ||
        error("Usage: nearby_resonance.jl ARCHIVE NATIVE_MODEL.h5 OUTPUT VOLTAGE_MV WORKERS")
    archive,model,output,voltage_mV,threads=ARGS
    ispath(output) && error("output already exists: $output")
    BLAS.set_num_threads(1)
    starting=Runner._read_linked_checkpoint(archive)
    changed=shift_voltage(starting,model,parse(Float64,voltage_mV))
    report=run_elastic_on(changed,parse(Int,threads),[[25.0,26.0],[26.0,27.0]],IMP)
    physical_control=(;nominal_voltage_mV=100starting.problem.geo.voltage,
        linked_regions="unchanged coordinate and scattering vertices; potential and all translated energies shifted",
        seed="nominal continuation source as initial guess",schema="qcl-negf-fath-nearby-resonance/v1",
        rebias_source_sha256=bytes2hex(open(sha256,@__FILE__)),report)
    open(output,"w") do io
        Runner._light_json(io,physical_control)
        println(io)
    end
end
