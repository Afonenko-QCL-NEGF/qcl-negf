using SparseArrays

const FATH_LO = 0.367

# Integrate the product of two piecewise linear hats on their shared shifted
# support. Two Gauss points on each interval integrate the product exactly.
function hat_shift_pair(energy, weights, omega)
    lower = max(first(energy),first(energy)-omega)
    upper = min(last(energy),last(energy)-omega)
    knots = sort!(unique([lower; filter(x->lower<x<upper,energy);
        filter(x->lower<x<upper,energy.-omega); upper]))
    transport = spzeros(length(energy),length(energy))
    for (a,b) in zip(knots[1:end-1],knots[2:end])
        midpoint, radius = (a+b)/2, (b-a)/2
        for direction in (-1,1)
            x = midpoint+direction*radius/sqrt(3)
            i = clamp(searchsortedlast(energy,x),1,length(energy)-1)
            j = clamp(searchsortedlast(energy,x+omega),1,length(energy)-1)
            u = clamp((x-energy[i])/(energy[i+1]-energy[i]),0,1)
            v = clamp((x+omega-energy[j])/(energy[j+1]-energy[j]),0,1)
            for (ii,c) in ((i,1-u),(i+1,u)), (jj,d) in ((j,1-v),(j+1,v))
                transport[ii,jj] += radius*c*d
            end
        end
    end
    plus = spdiagm(1 ./ weights)*transport
    minus = spdiagm(1 ./ weights)*transpose(transport)
    return (;plus,minus)
end

function lo_kernel(v, ifr_sites, plus, minus; q=v.coordinate_frame, bose=v.bose)
    return LT.LocalCollisionKernels(q,v.weights_k,v.acoustic,v.alloy,ifr_sites,v.interface_pair,
        v.lo_covariance,v.impurity_covariance,plus,minus,bose)
end

function shift_metrics(energy, weights, plus, minus, omega)
    mass = weights.*plus
    row,column,value = findnz(mass)
    defects = 100 .* (energy[column] .- energy[row] .- omega)
    return (;adjoint_relative=norm(mass-(weights.*minus)')/norm(mass),
        minimum_transfer=min(minimum(plus),minimum(minus)),
        maximum_row_overfill=max(0,maximum(sum(plus;dims=2))-1,maximum(sum(minus;dims=2))-1),
        missing_plus_measure=dot(weights,1 .-vec(sum(plus;dims=2))),
        missing_minus_measure=dot(weights,1 .-vec(sum(minus;dims=2))),
        maximum_node_shift_error_meV=maximum(abs,defects),
        rms_node_shift_error_meV=sqrt(dot(value,defects.^2)/sum(value)))
end

# Directional calls use the same scatter_packed! branch that A calls. Splitting
# by Bose coefficient uses zero absorption first, then swaps the shift pair.
function lo_events(green, v, ifr_sites, energy, weights, omega; basis=v.coordinate_frame)
    r = size(basis,2)
    ne,nk = length(energy),length(v.weights_k)
    dest = zeros(r^2,2,ne,nk,length(LT.COLLISION_CHANNELS))
    trace_weights = LT.pack_fro_weights(r)
    function directional(plus,minus,bose_factor)
        kernel = lo_kernel(v,ifr_sites,plus,minus;q=basis,bose=0)
        LT.scatter_packed!(dest,green,kernel)
        gain, loss = zeros(ne,nk),zeros(ne,nk)
        @views for k in 1:nk, e in 1:ne
            w = bose_factor*weights[e]*v.weights_k[k]
            gain[e,k] = w*dot(trace_weights .* dest[:,1,e,k,1],green[:,2,e,k])
            loss[e,k] = w*dot(trace_weights .* dest[:,2,e,k,1],green[:,1,e,k])
        end
        return (;gain,loss)
    end
    emission = directional(v.lo_plus,v.lo_minus,1+v.bose)
    absorption = directional(v.lo_minus,v.lo_plus,v.bose)
    LT.scatter_packed!(dest,green,v)
    combined = zeros(ne,nk)
    @views for k in 1:nk, e in 1:ne
        combined[e,k] = weights[e]*v.weights_k[k] *
            (dot(trace_weights .* dest[:,1,e,k,1],green[:,2,e,k]) -
             dot(trace_weights .* dest[:,2,e,k,1],green[:,1,e,k]))
    end
    function summarize(x)
        gain,loss = sum(x.gain),sum(x.loss)
        return (;gain,loss,number_relative=abs(gain-loss)/max(abs(gain)+abs(loss),floatmin(Float64)),
            electron_power_meV=100dot(energy,vec(sum(x.gain.-x.loss;dims=2))),
            events=(gain+loss)/2)
    end
    em,absorption_report = summarize(emission),summarize(absorption)
    net = em.events-absorption_report.events
    power = em.electron_power_meV+absorption_report.electron_power_meV
    net_spectrum = emission.gain.-emission.loss.+absorption.gain.-absorption.loss
    total_events = em.events+absorption_report.events
    combined_relative = sum(abs,combined.-net_spectrum)/max(total_events,floatmin(Float64))
    @assert combined_relative < 2e-13
    missing_above = 1 .-vec(sum(v.lo_plus;dims=2))
    missing_below = 1 .-vec(sum(v.lo_minus;dims=2))
    function clipped_weight(missing,kind)
        @views return sum(weights[e]*v.weights_k[k]*max(0,missing[e])*sum(green[1:r,kind,e,k])
            for e in 1:ne,k in 1:nk)
    end
    return (;emission=em,absorption=absorption_report,net_events=net,electron_power_meV=power,
        combined_operator_relative=combined_relative,
        occupied_weight_with_target_below_window=clipped_weight(missing_below,1),
        occupied_weight_with_target_above_window=clipped_weight(missing_above,1),
        empty_weight_with_source_below_window=clipped_weight(missing_below,2),
        empty_weight_with_source_above_window=clipped_weight(missing_above,2),
        electron_loss_meV_per_net_event=abs(net)<=256eps(Float64)*total_events ? nothing : -power/net,
        emission_loss_meV_per_event=iszero(em.events) ? nothing : -em.electron_power_meV/em.events,
        absorption_gain_meV_per_event=iszero(absorption_report.events) ? nothing :
            absorption_report.electron_power_meV/absorption_report.events,
        energy_minus_expected_meV=power+100omega*net,
        stationwise_collision_l1_relative=sum(abs,net_spectrum)/(em.gain+em.loss+
            absorption_report.gain+absorption_report.loss),
        energy_spectrum=vec(sum(net_spectrum;dims=2)))
end
