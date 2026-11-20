"""Same piecewise-linear frozen SigmaR, interval-resolved Dyson quadrature at k=0.6."""
import csv
import json
import numpy as np

from spectral_refinement import HERE, E0_MEV, E_MIN, E_MAX, LO, I, adjoint, hdf_arrays, interp, resolver, integrate_region


def crossing_candidates(energy, h, sigma):
    omega = energy[:,None,None]*I/E0_MEV-h-(sigma+adjoint(sigma))/2
    candidates = []
    ill_conditioned = 0
    for i,(left,right) in enumerate(zip(omega[:-1],omega[1:],strict=True)):
        change = right-left
        if np.linalg.cond(change)>1e12:
            ill_conditioned += 1
            continue
        x = np.linalg.eigvals(np.linalg.solve(change,-left))
        for root in x:
            if abs(root.imag)>1e-8 or root.real<0.0 or root.real>=1.0:
                continue
            x0 = root.real
            values,vectors = np.linalg.eigh(left+x0*change)
            index = np.argmin(abs(values))
            if abs(values[index])>1e-8:
                continue
            v = vectors[:,index]
            e = energy[i]+x0*(energy[i+1]-energy[i])
            gamma = 1j*((1-x0)*(sigma[i]-adjoint(sigma[i])) +
                        x0*(sigma[i+1]-adjoint(sigma[i+1])))
            g = float((v.conj()@gamma@v).real*E0_MEV)
            slope = float((v.conj()@change@v).real*E0_MEV/(energy[i+1]-energy[i]))
            width = g/abs(slope) if abs(slope)>1e-13 else np.nan
            candidates.append((e,g,slope,width,v))
    return sorted(candidates,key=lambda x:x[0]),ill_conditioned


def adaptive_integral(edges, order, energy, h, sigma, eta):
    x,w=np.polynomial.legendre.leggauss(order)
    mid=(edges[1:]+edges[:-1])/2
    half=np.diff(edges)/2
    nodes=(mid[:,None]+half[:,None]*x).ravel()
    weights=(half[:,None]*w).ravel()
    sp=interp(energy,sigma[:,None,:,:],nodes)
    d,gr,a=resolver(nodes,h[None,:,:],sp,eta)
    integral=np.einsum("e,eab->ab",weights/(2*np.pi*E0_MEV),a[:,0])
    return ((integral+adjoint(integral))/2,
            np.linalg.svd(d,compute_uv=False)[..., -1].min()*E0_MEV)


def main():
    energy,kgrid,hk,sigma,reference,record=hdf_arrays()
    idx=int(np.argmax(kgrid))
    assert abs(kgrid[idx]-.6)<1e-12
    h,sigma=hk[idx],sigma[:,idx]
    crossings,skipped=crossing_candidates(energy,h,sigma)
    extra=[E_MIN+LO,E_MAX-LO,E_MAX-10]
    for centre,_,_,width,_ in crossings:
        extra.append(centre)
        if np.isfinite(width) and width>1e-10:
            extra.extend(x for multiplier in (0.04,0.25,1,4,16,64)
                         for sign in (-1,1)
                         if E_MIN<(x:=centre+sign*multiplier*width)<E_MAX)
    raw_edges=np.sort(np.r_[energy,extra])
    edges=raw_edges[np.r_[True,np.diff(raw_edges)>1e-9]]
    edges[-1] = E_MAX
    configs=[(8,0.),(16,0.),(32,0.),(16,1e-6),(16,1e-4)]
    results=[]
    for order,eta in configs:
        integration,min_s=adaptive_integral(edges,order,energy,h,sigma,eta)
        eig,vec=np.linalg.eigh(integration)
        results.append(dict(order=order,eta_meV=eta,r_sum=float(np.linalg.norm(integration-I)/np.sqrt(7)),
           trace=float(np.trace(integration).real),min_eigenvalue=float(eig[0]),
           max_eigenvalue=float(eig[-1]),lowest_sampled_dyson_singular_meV=float(min_s),
           spectral_matrix_change_vs_previous=None if not results else
               float(np.linalg.norm(integration-previous)/np.sqrt(7))))
        previous=integration
        if order==32:
            weakest=vec[:,0]
    edge={}
    for name,lo,hi in (("lower_36_7",E_MIN,E_MIN+LO),("upper_36_7",E_MAX-LO,E_MAX),
                       ("upper_10",E_MAX-10,E_MAX)):
        piv=np.r_[lo,edges[(edges>lo)&(edges<hi)],hi]
        part,_=adaptive_integral(piv,32,energy,h,sigma,0.)
        edge[name]={"trace":float(np.trace(part).real),
                    "weak_mode_weight":float((weakest.conj()@part@weakest).real)}
    narrow_indices=[j for j,(_,_,_,w,_) in enumerate(crossings) if 0 < w < 0.01]
    regular_e = np.linspace(E_MIN,E_MAX,9601)
    regular_s = interp(energy,sigma[:,None,:,:],regular_e)
    _,_,regular_a = resolver(regular_e,h[None,:,:],regular_s,0.)
    narrow_areas=[]
    for j in narrow_indices:
        centre,_,slope,width,_ = crossings[j]
        lower=max(E_MIN,centre-16*width,
                  (centre+crossings[j-1][0])/2 if j else E_MIN)
        upper=min(E_MAX,centre+16*width,
                  (centre+crossings[j+1][0])/2 if j+1<len(crossings) else E_MAX)
        piv=np.r_[lower,edges[(edges>lower)&(edges<upper)],upper]
        part,_=adaptive_integral(piv,32,energy,h,sigma,0.)
        coarse=integrate_region(regular_a,regular_e,lower,upper)[0]
        narrow_areas.append(dict(centre_meV=centre,region_meV=[lower,upper],
                                 isolated_scalar_weight_estimate=1/abs(slope),
                                 adaptive_weak_mode_weight=float((weakest.conj()@part@weakest).real),
                                 aligned_0_1_weak_mode_weight=float((weakest.conj()@coarse@weakest).real)))
    rows=[dict(omega_crossing_meV=e,gamma_along_vector_meV=g,
               omega_slope=s,local_FWHM_estimate_meV=w,
               squared_overlap_missing_mode=abs(np.vdot(weakest,v))**2)
          for e,g,s,w,v in crossings]
    with (HERE/"pole_candidates.csv").open("w",newline="") as f:
        assert rows
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result=dict(source_state_sha256=record["state_sha256"],k_nm_inverse=float(kgrid[idx]),
                omega_crossings=len(rows),ill_conditioned_affine_intervals=skipped,
                integration_panels=len(edges)-1,results=results,edge_areas=edge,
                narrow_peak_windows=narrow_areas,
                exact_real_poles="No delta masses inserted; diag linewidths and finite sampled resolvent only.",
                exterior="Unknown SigmaR outside archived interval, no extrapolation.")
    (HERE/"adaptive_poles.json").write_text(json.dumps(result,indent=2)+"\n")


if __name__=="__main__":
    main()
