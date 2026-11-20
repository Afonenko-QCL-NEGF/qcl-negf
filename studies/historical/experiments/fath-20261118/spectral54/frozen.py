"""Replay one fixed-k retarded slab from each native Fath-54 state."""
import argparse
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
E0_MEV, L0_NM = 100.0, 10.0
HBAR, ME, E_CHARGE = 1.054571817e-34, 9.1093837139e-31, 1.602176634e-19
CBAR = HBAR**2/(2*ME*(E0_MEV*1e-3*E_CHARGE)*(L0_NM*1e-9)**2)
NB, NE, NK, NZ = 7, 4801, 25, 144
I = np.eye(NB)
FAMILIES = ("LO","acoustic","impurity","IFR","alloy","embedding")
CASES = ("native54-03","native54-long-alpha02/checkpoint-0256")
CORE = "e171caa60cce676c6c4238dd671e7c527f2bd977"


def adj(a):
    return a.swapaxes(-2,-1).conj()


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream,"sha256").hexdigest()


def scalar_hdf(file, dataset):
    log = subprocess.check_output(["h5dump","-y","-w","0","-d",dataset,file],text=True)
    return re.search(r'DATA\s*\{\s*"([^"]+)"',log).group(1)


def read_inputs(base, label):
    case = base / label.split("/")[0]
    run = base / label
    model, state = case/"model.h5",run/"state.h5"
    record = tomllib.loads((run/"summary.toml").read_text())
    input_case = tomllib.loads((case/"input.toml").read_text())
    device = tomllib.loads((case/"device.toml").read_text())
    assert input_case["mode"]=="fixed" and input_case["voltage_mV"]==54 and device["CBO_meV"]==149
    assert device["electron_electron"]=="none" and device["photon_field"]=="dark"
    assert sha(model)==record["model_sha256"]
    assert scalar_hdf(state,"/schema")=="fath-cbo149-aligned-state-v1"
    assert scalar_hdf(state,"/model_identity")==record["model_identity"]
    if (case/"identity.toml").is_file():
        assert tomllib.loads((case/"identity.toml").read_text())["core_commit"]==CORE
    audit = tomllib.loads((run/"independent-density-audit.toml").read_text())
    assert audit["state_sha256"]==record["state_sha256"] and audit["model_sha256"]==record["model_sha256"]
    assert audit["k_at_max_r_sum_nm_inverse"]==0.375
    read_digest = hashlib.sha256()
    with tempfile.TemporaryDirectory(prefix="fath54-spectral-slab-") as tmp:
        buffer = Path(tmp)/"slab.bin"
        def data(file, name, shape, k_idx=None):
            command = ["h5dump","-b","LE","-o",buffer,"-d","/"+name]
            if k_idx is not None:
                command += ["-s",f"0,0,{k_idx},0","-c",f"{NB},{NB},1,{NE}"]
            log = subprocess.check_output([*command,file],text=True)
            header = re.search(r"DATASPACE\s+SIMPLE\s*\{\s*\(\s*([\d,\s]+)",log)
            source_shape = tuple(map(int,header.group(1).split(",")))
            expected_shape = (NB,NB,NK,NE) if k_idx is not None else shape
            assert source_shape == expected_shape, (name, source_shape)
            raw = buffer.read_bytes()
            if k_idx is not None:
                read_digest.update(name.encode()+b"\0"+raw)
            a = np.frombuffer(raw,dtype="<f8").reshape(shape)
            assert np.isfinite(a).all()
            return a
        def complex_data(file, name, shape, k_idx=None):
            return data(file,name+"_real",shape,k_idx)+1j*data(file,name+"_imag",shape,k_idx)
        energies = E0_MEV*data(model,"energy_dimensionless",(NE,))
        w = data(model,"weight_energy",(NE,))
        k_axis = data(model,"k_dimensionless",(NK,))
        kidx = int(np.argmin(abs(k_axis/L0_NM-.375)))
        assert abs(k_axis[kidx]/L0_NM-.375)<1e-14
        assert energies[0]==-400 and abs(energies[-1]-560)<1e-12
        assert np.allclose(np.diff(energies),.20,atol=2e-12,rtol=0)
        assert np.max(abs(data(state,"hartree",(NZ,))))==0
        phi = complex_data(model,"Phi",(NB,NZ)).T
        m = data(model,"mass_lateral",(NZ,))
        z = data(model,"position_dimensionless",(NZ,))
        h0 = complex_data(model,"H0",(NB,NB)).T
        lp = device["period_nm"]/L0_NM
        zshift = z-device["z_reference_nm"]/L0_NM
        h = h0 + phi.conj().T @ (phi*(CBAR*k_axis[kidx]**2/m-54/E0_MEV/lp*zshift)[:,None])
        assert np.linalg.norm(h-adj(h))<1e-12
        def slab(group):
            raw = complex_data(state,group,(NB,NB,1,NE),k_idx=kidx)
            return np.ascontiguousarray(raw[:,:,0,:].transpose(2,1,0))
        sigma = sum((slab(f"selfenergy/{name}/R") for name in FAMILIES),
                    start=np.zeros((NE,NB,NB),complex))
        original_g, original_a = slab("green/GR"),slab("green/A")
    return energies,w,h,sigma,original_g,original_a,dict(
        source_case=label,source_map_count=record["last_row"]["ν"],source_status=record["status"],
        source_recorded_full_state_sha256=record["state_sha256"],model_sha256=record["model_sha256"],
        model_identity=record["model_identity"],chosen_k_nm_inverse=float(k_axis[kidx]/L0_NM),
        source_k_index_1based=kidx+1,native_audit_r_sum=audit["r_sum_max_unweighted_per_k"],
        native_audit_occupied_sheet_outside_trust=audit["occupied_sheet_outside_trust"],
        native_audit_spectral_trace_outside_trust=audit["spectral_trace_outside_trust"],
        slab_content_sha256=read_digest.hexdigest())


def r_sum(integral):
    return float(np.linalg.norm(integral-I)/np.sqrt(NB))


def a_of(d):
    g = np.linalg.inv(d)
    return 1j*(g-adj(g))


def trap_refined(pieces, energy, subdivisions, phase):
    count = (len(energy)-1)*subdivisions
    if phase == "aligned":
        target = np.linspace(energy[0],energy[-1],count+1)
    else:
        target = np.r_[energy[0],energy[0]+(np.arange(count)+.5)*((energy[-1]-energy[0])/count),energy[-1]]
    k = np.clip(np.searchsorted(energy,target,side="right")-1,0,len(energy)-2)
    vals = np.clip((target-energy[k])/(energy[k+1]-energy[k]),0,1)
    w = np.r_[np.diff(target)[0]/2,(target[2:]-target[:-2])/2,np.diff(target)[-1]/2]/(2*np.pi*E0_MEV)
    total = np.zeros((NB,NB),complex)
    for start in range(0,len(k),2048):
        s = slice(start,start+2048)
        block = pieces[k[s]] + vals[s,None,None]*(pieces[k[s]+1]-pieces[k[s]])
        total += np.einsum("i,iab->ab",w[s],a_of(block))
    return total


def integrate_matrix_pencil(d, g, energy):
    # For C=D0^-1(D1-D0), integrate (I+t C)^-1 D0^-1 exactly
    # with the scalar function log(1+lambda)/lambda on the principal branch.
    pencil = g[:-1] @ (d[1:]-d[:-1])
    eig, vec = np.linalg.eig(pencil)
    val = np.divide(np.log1p(eig),eig,out=np.ones_like(eig),where=abs(eig)>1e-15)
    mean_g = (vec*val[:,None,:]) @ (np.linalg.inv(vec)@g[:-1])
    piece = 1j*(mean_g-adj(mean_g))*np.diff(energy)[:,None,None]/(2*np.pi*E0_MEV)
    return piece,eig,float(np.max(np.linalg.cond(vec)))


def gauss_matrix_pencil(d, energy, order):
    frac, weights = np.polynomial.legendre.leggauss(order)
    result = np.zeros_like(d[:-1])
    for w,t in zip(weights,frac,strict=True):
        result += .5*w*a_of(d[:-1]+(.5+.5*t)*(d[1:]-d[:-1]))
    return result*np.diff(energy)[:,None,None]/(2*np.pi*E0_MEV)


def expectation(a,v):
    return np.einsum("a,...ab,b->...",v.conj(),a,v).real


def measure(base, label):
    e,w,h,sigma,old_g,old_a,record=read_inputs(base,label)
    d = e[:,None,None]/E0_MEV*I-h-sigma
    g = np.linalg.inv(d)
    a = 1j*(g-adj(g))
    gamma = 1j*(sigma-adj(sigma))
    rel = lambda x,y: float(np.linalg.norm(x-y)/np.linalg.norm(y))
    error_g,error_a = rel(g,old_g),rel(a,old_a)
    assert max(error_g,error_a)<1e-10, (error_g,error_a)
    closure = rel(a,g@gamma@adj(g))
    gamma_min = float(np.min(np.linalg.eigvalsh(gamma)))
    assert gamma_min >= -1e-12*np.max(np.linalg.norm(gamma,axis=(-2,-1)))
    original = np.einsum("i,iab->ab",w/(2*np.pi),old_a)
    assert abs(r_sum(original)-record["native_audit_r_sum"])<1e-11
    piece,pencil_eig,vec_cond = integrate_matrix_pencil(d,g,e)
    exact = np.sum(piece,axis=0)
    reference = gauss_matrix_pencil(d,e,24)
    gauss_total_error = float(np.linalg.norm(np.sum(reference,axis=0)-exact)/np.sqrt(NB))
    gauss_cell_error = float(np.max(np.linalg.norm(reference-piece,axis=(-2,-1))))
    # A node-wise Gauss check is independent of the pencil eigendecomposition
    # and its complex-log branch choice. If it fails, increase the order.
    assert max(gauss_total_error,gauss_cell_error)<1e-8, (gauss_total_error,gauss_cell_error)
    evals,evecs = np.linalg.eigh(exact)
    weak,strong = evecs[:,0],evecs[:,-1]
    he,hv = np.linalg.eigh(h)
    align_h = abs(hv.conj().T@weak)**2
    align_strong = abs(hv.conj().T@strong)**2
    exact_weak = expectation(piece,weak)
    weak_density = expectation(a,weak)/E0_MEV
    exact_strong = expectation(piece,strong)
    strong_density = expectation(a,strong)/E0_MEV
    lo_edge = (e[1:] <= -363.2+1e-10)
    hi_edge = (e[:-1] >= 523.2-1e-10)
    upper_trust = e[:-1] >= 300-1e-10
    lower_trust = e[1:] <= -140+1e-10
    # Local roots of the linearly interpolated Dyson pencil. Restrict the
    # real part to the segment itself. Imaginary part is a width proxy.
    with np.errstate(divide="ignore",invalid="ignore"):
        root = -1/pencil_eig
    valid = np.isfinite(root)&(root.real>=0)&(root.real<=1)
    pole_centres = e[:-1,None] + np.diff(e)[:,None]*root.real
    widths = abs(np.diff(e)[:,None]*root.imag)
    valid_index = np.argwhere(valid)
    widths_index = np.argsort(widths[valid])[:5]
    narrow = [dict(energy_mev=float(pole_centres[j,m]),halfwidth_proxy_mev=float(widths[j,m]),
                   segment_total_trace=float(np.trace(piece[j]).real),
                   segment_weak_modal_weight=float(exact_weak[j]))
              for j,m in valid_index[widths_index]]
    if narrow:
        narrowest = narrow[0]["halfwidth_proxy_mev"]
    else:
        narrowest = None
    midpoint = (e[:-1]+e[1:])/2
    coarse_piece = (a[:-1]+a[1:])*np.diff(e)[:,None,None]/(4*np.pi*E0_MEV)
    interval_delta = exact_strong-expectation(coarse_piece,strong)
    absolute_interval_error = np.linalg.norm(piece-coarse_piece,axis=(-2,-1))/np.sqrt(NB)
    miss = np.argsort(absolute_interval_error)[-5:][::-1]
    coarse_error = original-exact
    continuum_error = exact-I
    strong_cumulative = np.cumsum(exact_strong)
    i_cross = int(np.argmax(strong_cumulative>1))
    assert strong_cumulative[i_cross]>1
    sv = np.linalg.svd(d,compute_uv=False)[:,-1]
    c = np.cumsum(exact_weak)/sum(exact_weak)
    title = record["source_case"]
    rows = []
    def push(method,delta,intervals,total):
        val=np.linalg.eigvalsh(total)
        rows.append(dict(case=title,method=method,energy_step_mev=delta,energy_intervals=intervals,
            r_sum=r_sum(total),trace=float(np.trace(total).real),
            minimum_eigenvalue=val[0],maximum_eigenvalue=val[-1],
            norm_difference_from_analytic=float(np.linalg.norm(total-exact)/np.sqrt(NB)),
            weak_mode_integral=float(expectation(total,weak))))
    push("stored_e171_trapezoid",.20,NE-1,original)
    for subdiv in (1,2,4,8,16):
        for phase in ("aligned","half_offset"):
            method="trapezoid_"+phase
            push(method,.20/subdiv,(NE-1)*subdiv+(phase=="half_offset"),trap_refined(d,e,subdiv,phase))
    push("gauss_legendre_24",None,NE-1,np.sum(reference,axis=0))
    push("analytic_each_original_interval",None,NE-1,exact)
    return rows,dict(**record,GR_replay_fro_relative=error_g,A_replay_fro_relative=error_a,
        A_vs_GGammaGadj_replay_fro_relative=closure,gamma_min_eig_mev=gamma_min*E0_MEV,
        pencil_eigenvector_max_condition=vec_cond,gauss_exact_matrix_difference=gauss_total_error,
        gauss_exact_max_interval_fro_difference=gauss_cell_error,analytic_r_sum=r_sum(exact),
        analytic_integral_eigenvalues=evals.tolist(),
        coarse_integral_eigenvalues=np.linalg.eigvalsh(original).tolist(),
        analytic_normalized_excess_r_sum=float(np.linalg.norm(np.maximum(evals-1,0))/np.sqrt(NB)),
        analytic_normalized_deficit_r_sum=float(np.linalg.norm(np.maximum(1-evals,0))/np.sqrt(NB)),
        native_trapezoid_vs_analytic_matrix_difference=r_sum(I+coarse_error),
        coarse_r_sum_squared_cross_term=float(2*np.vdot(coarse_error,continuum_error).real/NB),
        fraction_r_sum_squared_in_strong_direction=float((1-evals[-1])**2/np.sum((1-evals)**2)),
        strong_mode_h_rank_weights=align_strong.tolist(),
        strong_mode_h_expectation_mev=float(align_strong@he*E0_MEV),
        strong_mode_low_wing_36p8_weight=float(exact_strong[lo_edge].sum()),
        strong_mode_high_wing_36p8_weight=float(exact_strong[hi_edge].sum()),
        strong_mode_upper_outside_trust_weight=float(exact_strong[upper_trust].sum()),
        strong_mode_low_endpoint_A_over_mev=float(strong_density[0]),
        strong_mode_high_endpoint_A_over_mev=float(strong_density[-1]),
        strong_mode_energy_at_max_node_mev=float(e[np.argmax(strong_density)]),
        strong_mode_energy_q05_q50_q95_mev=np.interp([.05,.50,.95],
            strong_cumulative/strong_cumulative[-1],midpoint).tolist(),
        strong_mode_first_cell_where_cumulative_exceeds_one_mev=float(e[i_cross+1]),
        strong_mode_integral_ending_at_300_mev=float(exact_strong[~upper_trust].sum()),
        strong_mode_native_trapezoid_integral=float(expectation(original,strong)),
        total_trace_low_wing_36p8=float(np.trace(np.sum(piece[lo_edge],axis=0)).real),
        total_trace_high_wing_36p8=float(np.trace(np.sum(piece[hi_edge],axis=0)).real),
        fraction_r_sum_squared_in_weak_direction=float((1-evals[0])**2/np.sum((1-evals)**2)),
        h_eigenvalues_mev=(he*E0_MEV).tolist(),weak_mode_h_rank_weights=align_h.tolist(),
        weak_mode_h_expectation_mev=float(align_h@he*E0_MEV),
        weak_mode_low_wing_36p8_weight=float(exact_weak[lo_edge].sum()),
        weak_mode_high_wing_36p8_weight=float(exact_weak[hi_edge].sum()),
        weak_mode_lower_outside_trust_weight=float(exact_weak[lower_trust].sum()),
        weak_mode_upper_outside_trust_weight=float(exact_weak[upper_trust].sum()),
        weak_mode_low_endpoint_A_over_mev=float(weak_density[0]),
        weak_mode_high_endpoint_A_over_mev=float(weak_density[-1]),
        weak_mode_energy_at_max_node_mev=float(e[np.argmax(weak_density)]),
        weak_mode_energy_q05_q50_q95_mev=np.interp([.05,.50,.95],c,midpoint).tolist(),
        minimum_node_singular_dyson_mev=float(min(sv)*E0_MEV),
        minimum_node_singular_dyson_at_mev=float(e[np.argmin(sv)]),
        narrowest_local_pencil_halfwidth_proxy_mev=narrowest,narrowest_poles=narrow,
        largest_coarse_matrix_interval_errors=[
            dict(center_mev=float(midpoint[j]),
                matrix_difference_div_sqrt_nb=float(absolute_interval_error[j]),
                strong_modal_analytic_minus_coarse=float(interval_delta[j]))
            for j in miss]), dict(h=h,sigma=sigma,integral=exact,leading_mode=strong)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transport",type=Path,default=HERE.parent/"transport")
    args = parser.parse_args()
    report, records, slabs = [], [], []
    for label in CASES:
        rows, result, slab = measure(args.transport,label)
        report.extend(rows)
        records.append(result)
        slabs.append(slab)
        print(label,rows[0]["r_sum"],result["analytic_r_sum"],flush=True)
    with (HERE/"quadrature.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(report[0]))
        writer.writeheader()
        writer.writerows(report)
    old,new = slabs
    comparison = dict(
        relative_total_sigmaR_change=float(np.linalg.norm(old["sigma"]-new["sigma"])/np.linalg.norm(old["sigma"])),
        normalized_integral_matrix_difference=float(np.linalg.norm(old["integral"]-new["integral"])/np.sqrt(NB)),
        leading_mode_squared_overlap=float(abs(np.vdot(old["leading_mode"],new["leading_mode"]))**2),
        projected_h_max_abs_difference=float(np.max(abs(old["h"]-new["h"]))),
    )
    capsule=dict(core_commit=CORE,energy_window_mev=[-400,560],retarded_working_eta_mev=0,
                 interpolation="convex segment interpolation of stored total SigmaR with pointwise PSD broadening to roundoff, no extrapolation",
                 scba_maps_completed=0,records=records,checkpoint_comparison=comparison)
    (HERE/"diagnostics.json").write_text(json.dumps(capsule,indent=2)+"\n")


if __name__=="__main__":
    main()
