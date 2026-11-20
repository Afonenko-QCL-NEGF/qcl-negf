"""Frozen-SigmaR spectral quadrature probe, with no fresh SCBA maps."""
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import tomllib

import numpy as np

HERE = Path(__file__).resolve().parent
RUN = HERE / "attempt01"
STATE, MODEL = RUN/"state.h5", RUN/"model.h5"
E0_MEV, L0_NM = 100.0, 10.0
HBAR, ME, E_CHARGE = 1.054571817e-34, 9.1093837139e-31, 1.602176634e-19
CBAR = HBAR**2/(2*ME*(E0_MEV*1e-3*E_CHARGE)*(L0_NM*1e-9)**2)
MODE = 7
E_MIN, E_MAX = -400., 560.
LO = 36.7
I = np.eye(MODE)
STEPS = (0.8,0.4,0.2,0.1)


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream,"sha256").hexdigest()


def hdf_arrays():
    record = tomllib.loads((RUN/"summary.toml").read_text())
    assert sha(STATE)==record["state_sha256"] and sha(MODEL)==record["model_sha256"]
    with tempfile.TemporaryDirectory(prefix="fath-frozen-spec-") as d:
        buffer = Path(d)/"field.bin"
        def data(file, name, shape):
            text = subprocess.check_output(["h5dump","-b","LE","-o",buffer,"-d","/"+name,file],text=True)
            match = re.search(r"DATASPACE\s+SIMPLE\s*\{\s*\(\s*([\d,\s]+)",text)
            assert match is not None and tuple(map(int,match.group(1).split(",")))==shape, name
            a = np.fromfile(buffer,dtype="<f8").reshape(shape)
            assert np.isfinite(a).all()
            return a
        def z(file, name, shape):
            return data(file,name+"_real",shape) + 1j*data(file,name+"_imag",shape)
        def field(name):
            return np.ascontiguousarray(z(STATE,name,(7,7,4,1201)).transpose(3,2,1,0))
        energies = E0_MEV*data(MODEL,"energy_dimensionless",(1201,))
        k = data(MODEL,"k_dimensionless",(4,))
        dz = data(STATE,"hartree",(144,))
        assert np.all(dz==0), "Hartree field differs from fixed-zero experiment"
        h0 = z(MODEL,"H0",(7,7)).T
        phi = z(MODEL,"Phi",(7,144)).T
        mass = data(MODEL,"mass_lateral",(144,))
        inverse = phi.T.conj()@(phi/mass[:,None])
        hk = h0 + CBAR*k[:,None,None]**2*inverse
        families = ("LO","acoustic","impurity","IFR","alloy","embedding")
        sigma = sum((field("selfenergy/"+name+"/R") for name in families),
                    start=np.zeros((1201,4,7,7),complex))
        reference = field("green/GR")
    return energies,k/L0_NM,hk,sigma,reference,record


def adjoint(a):
    return a.swapaxes(-2,-1).conj()


def interp(source, data, target):
    assert target[0]>=source[0]-1e-12 and target[-1]<=source[-1]+1e-12
    idx = np.clip(np.searchsorted(source,target,side="right")-1,0,len(source)-2)
    frac = np.clip((target-source[idx])/(source[idx+1]-source[idx]),0,1)[:,None,None,None]
    return (1-frac)*data[idx]+frac*data[idx+1]


def trap(a, e):
    return np.trapezoid(a, x=e/E0_MEV, axis=0)/(2*np.pi)


def integrate_region(a, e, low, high):
    subset = np.r_[low,e[(e>low)&(e<high)],high]
    return trap(interp(e,a,subset),subset)


def resolver(energy, h, sigma, eta_mev):
    d = ((energy+1j*eta_mev)/E0_MEV)[:,None,None,None]*I-h-sigma
    g = np.linalg.inv(d)
    return d,g,1j*(g-adjoint(g))


def grid(step, phase):
    count = round((E_MAX-E_MIN)/step)
    if phase == "aligned":
        return np.linspace(E_MIN,E_MAX,count+1)
    return np.r_[E_MIN,E_MIN+(np.arange(count)+.5)*step,E_MAX]


def evaluate_rows(energies,k,h,sigma,reference):
    _, g, _ = resolver(energies,h,sigma,0.)
    error = float(np.linalg.norm(g-reference)/np.linalg.norm(reference))
    assert error < 1e-11, error
    gamma0 = 1j*(sigma-adjoint(sigma))
    min_eig = float(np.linalg.eigvalsh(gamma0).min())
    max_scale = float(np.max(np.linalg.norm(gamma0,axis=(-2,-1))))
    assert min_eig >= -1e-12*max_scale, (min_eig,max_scale)
    rows = []
    configs = [(d,phase,0.0) for d in STEPS for phase in ("aligned","half_offset")]
    configs += [(0.1,"aligned",r) for r in (1e-6,1e-4)]
    for step,phase,eta in configs:
        e = grid(step,phase)
        s = interp(energies,sigma,e)
        gamma = 1j*(s-adjoint(s))
        gamma_min_k = np.linalg.eigvalsh(gamma).min(axis=(0,2))
        d,g,a = resolver(e,h,s,eta)
        singular = np.linalg.svd(d,compute_uv=False)[...,-1]
        min_singular_idx = singular.argmin(axis=0)
        integral = trap(a,e)
        low = integrate_region(a,e,E_MIN,E_MIN+LO)
        high = integrate_region(a,e,E_MAX-LO,E_MAX)
        centre = integrate_region(a,e,E_MIN+LO,E_MAX-LO)
        last10 = integrate_region(a,e,E_MAX-10,E_MAX)
        assert np.max(abs(integral-low-high-centre))<1e-10
        resolution, modes = np.linalg.eigh(integral)
        detune = np.linalg.norm(integral-I,axis=(-2,-1))/np.sqrt(MODE)
        a_closure = np.linalg.norm(a-g@(gamma+2*eta/E0_MEV*I)@adjoint(g),axis=(-2,-1))
        for idx, momentum in enumerate(k):
            eigmin = min_singular_idx[idx]
            weak = modes[idx,:,0]
            expectation = lambda block: (weak.conj()@block@weak).real
            trace_e = np.trace(a[:,idx],axis1=-2,axis2=-1).real/E0_MEV
            rows.append(dict(
                dE_meV=step, phase=phase, eta_meV=eta, energy_nodes=len(e), k_nm_inverse=momentum,
                r_sum=detune[idx], trace=np.trace(integral[idx]).real,
                eigen_min=resolution[idx,0], eigen_max=resolution[idx,-1],
                low_wing_trace_36_7meV=np.trace(low[idx]).real,
                high_wing_trace_36_7meV=np.trace(high[idx]).real,
                interior_trace=np.trace(centre[idx]).real,
                weak_eigenvector_low_wing_weight=expectation(low[idx]),
                weak_eigenvector_high_wing_weight=expectation(high[idx]),
                weak_eigenvector_last_10meV_weight=expectation(last10[idx]),
                weak_eigenvector_endpoint_A_over_meV=expectation(a[-1,idx])/E0_MEV,
                upper_endpoint_trace_A_over_meV=trace_e[-1],
                min_eig_gamma_meV=E0_MEV*gamma_min_k[idx],
                min_singular_dyson_meV=E0_MEV*singular[eigmin,idx],
                energy_at_min_singular_meV=e[eigmin],
                peak_trace_A_over_meV=trace_e.max(),
                energy_at_peak_trace_A_meV=e[trace_e.argmax()],
                max_absolute_spectral_closure_solver_units=a_closure[:,idx].max(),
            ))
    return rows,error,min_eig*E0_MEV,max_scale*E0_MEV


def trend():
    with (RUN/"projected.csv").open() as source: rows = list(csv.DictReader(source))
    output = []
    for a,b in ((256,319),(320,383),(384,447),(448,511),(512,552)):
        observed=[r for r in rows if a<=int(r["map"])<=b]
        rr=np.array([float(r["rR_max_family"]) for r in observed])
        rt=np.array([float(r["rR_total"]) for r in observed])
        output.append({
            "first_map":a,"last_map":b,"max_family_median":float(np.median(rr)),
            "max_family_min_max":[float(rr.min()),float(rr.max())],
            "total_median":float(np.median(rt)),
            "elapsed_seconds_end":float(observed[-1]["elapsed_seconds"]),
        })
    observed=[r for r in rows if int(r["map"])>=256]
    x=[int(r["map"]) for r in observed]
    y=np.log([float(r["rR_max_family"]) for r in observed])
    slope,offset=np.polyfit(x,y,1)
    predicted=(np.log(1e-8)-offset)/slope
    return {"windows":output,"log_slope_per_map":float(slope),
            "descriptive_half_life_maps":float(-np.log(2)/slope),
            "unvalidated_log_extrapolation_map_at_1e_8":float(predicted)}


def main():
    energies,k,h,sigma,reference,record = hdf_arrays()
    rows,error,min_eig,max_scale = evaluate_rows(energies,k,h,sigma,reference)
    with (HERE/"spectral_refinement.csv").open("w",newline="") as out:
        writer=csv.DictWriter(out,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary={
        "source_state_sha256":record["state_sha256"],"source_model_sha256":record["model_sha256"],
        "energy_support_meV":[E_MIN,E_MAX],"coarse_GR_relative_reconstruction":error,
        "coarse_Gamma_min_eigenvalue_meV":min_eig,"coarse_Gamma_max_Frobenius_meV":max_scale,
        "edge_width_meV":LO,"electrostatics":"field zero and Hartree zero held fixed",
        "spectral_sum_by_step": {
            f"{d}/{p}":max(r["r_sum"] for r in rows if r["dE_meV"]==d and r["phase"]==p and r["eta_meV"]==0)
            for d in STEPS for p in ("aligned","half_offset")
        },
        "projected_trend":trend(),
    }
    (HERE/"spectral_refinement.json").write_text(json.dumps(summary,indent=2)+"\n")


if __name__=="__main__":
    main()
