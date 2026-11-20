"""Predeclared static refinement of the CBO149 Fath single-cell basis."""
import csv
import json
from pathlib import Path
import sys
import tomllib

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"cell-basis"))
from holdout import K, NATIVE, cell_blocks, projected_window, squared_subspace_overlap

P = tomllib.loads((HERE/"passport.toml").read_text())
TRAIN = 2*np.pi*np.arange(P["zero_field_training_phase_count"])/P["zero_field_training_phase_count"]
TEST = 2*np.pi*(np.arange(P["holdout_phase_count"])+np.sqrt(5)/13)/P["holdout_phase_count"]
FIELD = P["bias_mv"]
ETA = P["seed_broadening_mev"]
EMIN = P["energy_min_mev"]
MARGIN = P["trust_margin_mev"]
KMAX = P["momentum_max_inverse_nm"]
NCELL = P["finite_compare_cells"]
NSPEC = P["finite_cavity_cells"]


def ortho(matrix):
    q, r = np.linalg.qr(matrix)
    assert min(abs(np.diag(r))) > 1e-10
    return q


def snapshot_modes(h, t, bands):
    shots = np.hstack([np.linalg.eigh(h + phase*t + phase.conjugate()*t.T)[1][:,:bands]
                       for phase in np.exp(1j*TRAIN)])
    u, ss, _ = np.linalg.svd(np.hstack((shots.real,shots.imag)),full_matrices=False)
    assert ss[11] > 1e-10
    return u


def space(variant, h, u_pod, u_cell):
    method, n = variant["method"], variant["rank"]
    if method == "shifted_seam_attachment":
        sub = h[1:-1,1:-1]
        e, u = np.linalg.eigh(sub)
        q = u[:,n-2:]
        # Fixed-interface modes carry the first n-2 poles explicitly. The
        # two residual seam modes interpolate the interior Green response.
        ends = -q @ ((q.T @ h[1:-1][:,[0,-1]]) / (e[n-2:,None]-variant["shift_mev"]))
        phi = np.zeros((len(h),n))
        phi[1:-1,:n-2] = u[:,:n-2]
        phi[1:-1,n-2:] = ends
        phi[0,n-2] = phi[-1,n-1] = 1
        return ortho(phi)
    pod = u_pod[variant["train_bands"]]
    if method == "pod":
        return pod[:,:n]
    assert method == "cell_augmented_pod"
    core = pod[:,:variant["retained_pod_modes"]]
    # Keep the POD core intact. Add the lowest cell block Ritz eigenvectors
    # in its orthogonal complement, with the bare isolated-cell energies.
    candidate = u_cell - core@(core.T@u_cell)
    extra, singular, _ = np.linalg.svd(candidate,full_matrices=False)
    extra = extra[:,singular > 1e-8]
    _, modes = np.linalg.eigh(extra.T@h@extra)
    # Use a pool of the first 18 isolated-cell modes before minimization.
    return ortho(np.hstack((core,extra@modes[:,:n-core.shape[1]])))


def fd_chain(h, t, z, m, lp, n, k, end_delta=None):
    cell = h-FIELD/lp*z+K*k*k*m
    diagonal = np.tile(np.diag(cell),n)-np.repeat(FIELD*(np.arange(n)-n//2),len(h))
    if end_delta is not None:
        diagonal[[0,-1]] += end_delta
    off = np.tile(np.r_[np.diag(h,1),t[-1,0]],n)[:-1]
    return np.linalg.eigh(np.diag(diagonal)+np.diag(off,1)+np.diag(off,-1))


def best_pair(reference, approximate):
    weights = reference.T@approximate
    left,right = np.triu_indices(weights.shape[1],1)
    norms = np.sum(weights**2,axis=0)
    trace = norms[left]+norms[right]
    determinant = (weights[0,left]*weights[1,right]-weights[1,left]*weights[0,right])**2
    least = 0.5*(trace-np.sqrt(np.maximum(0,trace**2-4*determinant)))
    ix = int(np.lexsort((-trace,-least))[0])
    return np.array([left[ix],right[ix]]), float(least[ix])


def static_metrics(phi,h,t,z,lp,delta,full_seven,low_bloch):
    nb = phi.shape[1]
    cell,tplus,position = [phi.T@op@phi for op in (h,t,z)]
    e, waves = full_seven
    mid = (NCELL//2)*len(h)
    local = np.sum(waves[mid:mid+len(h)]**2,axis=0)
    p = np.flatnonzero((e > 0)&(e < 20)&(local >= 0.85))
    assert len(p) == 2
    er,reduced = projected_window(nb,cell,tplus,position,lp,FIELD,phi,delta)
    embedded = np.kron(np.eye(NCELL),phi)
    approx = embedded@reduced
    pair, overlap = best_pair(waves[:,p],approx)
    differences = er[pair]-e[p]
    gap_error = abs(np.diff(er[pair])[0]-np.diff(e[p])[0])
    raw = np.array([np.linalg.eigvalsh(cell + q*tplus + q.conjugate()*tplus.T)[:4]
                    for q in np.exp(1j*TEST)])
    bloch = np.max(abs(raw-low_bloch),axis=0)
    active = np.flatnonzero((e >= -100)&(e <= 80)&(local >= .1))
    overlap_active = abs(waves[:,active].T@approx)**2
    matched = np.argmax(overlap_active,axis=1)
    orth = np.linalg.norm(phi.T@phi-np.eye(nb))
    energy_max = max(max(abs(differences)),gap_error,max(bloch))
    mask = overlap >= .95 and orth <= 1e-12
    return dict(orthogonality_fro=orth, first_four_bloch_errors_mev=bloch.tolist(),
                first_four_bloch_peak_mev=float(max(bloch)),
                fd_pair_mev=e[p].tolist(),ritz_pair_mev=er[pair].tolist(),pair_error_mev=differences.tolist(),
                splitting_error_mev=float(gap_error),pair_principal_sq=overlap,
                pair_projection_min_principal_sq=squared_subspace_overlap(waves[:,p],embedded),
                broader_active_peak_mev=float(max(abs(er[matched]-e[active]))),
                broader_active_min_sq=float(min(overlap_active[np.arange(len(active)),matched])),
                broader_active_distinct_matches=len(set(matched)),broader_active_count=len(active),
                energy_gate_peak_mev=float(energy_max),static_05_pass=bool(mask and energy_max < .5),
                original_01_pass=bool(mask and energy_max <= .1))


def cavity(phi, h, t, z, m, lp, k):
    hp,tplus = [phi.T@a@phi for a in (h-FIELD/lp*z+K*k*k*m,t)]
    nb = phi.shape[1]
    upper = np.eye(NSPEC,k=1)
    shifts = np.repeat(FIELD*(np.arange(NSPEC)-NSPEC//2),nb)
    matrix = np.kron(np.eye(NSPEC),hp)+np.kron(upper,tplus)+np.kron(upper.T,tplus.T)-np.diag(shifts)
    e,v = np.linalg.eigh(matrix)
    central = v[NSPEC//2*nb:(NSPEC//2+1)*nb]
    return e,v,central,np.linalg.eigvalsh(hp)[-1],np.linalg.norm(tplus,ord=2)


def integrated_density(v,mass):
    return (v * mass) @ v.T


def tail_weight(e,low,high):
    return 1-(np.arctan((high-e)/ETA)-np.arctan((low-e)/ETA))/np.pi


def e171_frobenius(v,weight):
    n = len(v)
    return float(np.linalg.norm(integrated_density(v,weight)-np.eye(n))/np.sqrt(n))


def tail_deficits(spectrum,upper, lower=EMIN):
    out = []
    for e,_,v,_,_ in spectrum:
        lost = tail_weight(e,lower,upper)
        d = integrated_density(v,lost)
        eig = np.linalg.eigvalsh(d)
        out.append((float(np.linalg.norm(d)/np.sqrt(len(v))),float(np.trace(d)/len(v)),float(eig[-1])))
    return tuple(float(x) for x in np.max(out,axis=0))


def nodal_deficit(spectrum, upper, ne):
    energy = np.linspace(EMIN,upper,ne)
    weights = np.full(ne,(upper-EMIN)/(ne-1))
    weights[[0,-1]] *= 0.5
    out = []
    for e,_,v,_,_ in spectrum:
        lorentz = ETA/(np.pi*((energy[:,None]-e[None,:])**2+ETA**2))
        out.append(e171_frobenius(v,weights @ lorentz))
    return max(out)


def tail_cutoff(spectrum):
    # Analytic full-matrix deficit is decreasing as the upper window grows.
    lo,hi = 0.0,max(x[0][-1] for x in spectrum)+2000
    assert tail_deficits(spectrum,hi)[0] < P["spectral_sum_frobenius_limit"]
    for _ in range(34):
        mid=(lo+hi)/2
        if tail_deficits(spectrum,mid)[0] >= P["spectral_sum_frobenius_limit"]: lo=mid
        else: hi=mid
    return hi


def upper_poles(phi, h, t, m):
    # Find the worst excess of the highest Ritz band on an independent,
    # regularly spaced subgrid over three radial momenta.
    out = []
    embed_cell = phi.T
    ht = phi.T@t@phi
    n = phi.shape[1]
    for k in (0.0,0.30,0.60):
        hk = h+K*k*k*m
        reduced = phi.T@hk@phi
        for q in np.exp(1j*TEST[::8]):
            e,u = np.linalg.eigh(hk+q*t+q.conjugate()*t.T)
            ep,up = np.linalg.eigh(reduced+q*ht+q.conjugate()*ht.T)
            weights = abs((embed_cell@u).conj().T@up[:,-1])**2
            ix = int(np.argmax(weights))
            out.append(dict(k=k,phase_rad=float(np.angle(q)),ritz_top_mev=float(ep[-1]),
                exact_same_rank_mev=float(e[n-1]),same_rank_error_mev=float(ep[-1]-e[n-1]),
                strongest_exact_rank_1based=ix+1,strongest_exact_mev=float(e[ix]),
                strongest_squared_overlap=float(weights[ix]),
                overlap_within_20mev=float(weights[abs(e-ep[-1])<=20].sum()),
                expectation_error_mev=float(abs(weights@e-ep[-1]))))
    return max(out,key=lambda x:x["same_rank_error_mev"])


def compare_full_fd_cavity(phi,spectrum,exact_cavities, cutoff):
    nb = phi.shape[1]
    embed = np.kron(np.eye(NSPEC),phi)
    res = []
    for k,full,model in zip((0.0,0.30,0.60),exact_cavities,spectrum,strict=True):
        e,u = full
        er,w,central,_,_ = model
        cs = slice(NSPEC//2*len(phi),(NSPEC//2+1)*len(phi))
        v = phi.T@u[cs]
        exact_loss = integrated_density(v,tail_weight(e,EMIN,cutoff))
        model_loss = integrated_density(central,tail_weight(er,EMIN,cutoff))
        peaks = []
        # A weakly central edge copy of a Ritz direction is not a transport pole.
        central_weights = np.sum(central**2,axis=0)
        high = np.flatnonzero(central_weights>=0.10)[-2:]
        for ix in high:
            overlap = abs(u.T @ (embed@w[:,ix]))**2
            peak = int(np.argmax(overlap))
            peaks.append(dict(ritz_mev=float(er[ix]),ritz_central_weight=float(central_weights[ix]),
                exact_strongest_mev=float(e[peak]),exact_strongest_rank_1based=peak+1,
                exact_strongest_overlap=float(overlap[peak]),
                exact_fidelity_in_20mev=float(overlap[abs(e-er[ix])<=20].sum())))
        res.append(dict(k=k,window_upper_mev=cutoff,ritz_high=peaks,
            model_central_tail_trace_fraction=float(np.trace(model_loss)/nb),
            exact_fd_projected_tail_trace_fraction=float(np.trace(exact_loss)/nb),
            projected_fd_closure_error=float(np.linalg.norm(v@v.T-np.eye(nb))/np.sqrt(nb))))
    return res


def spectral_metrics(phi,h,t,z,m,lp, exact_cavities):
    spectra = {nk:[cavity(phi,h,t,z,m,lp,k) for k in np.linspace(0,KMAX,nk)]
               for nk in P["momentum_nodes"]}
    emax = max(tail_cutoff(s) for s in spectra.values())
    local_max = max(row[3] for row in spectra[17])
    coupling = max(row[4] for row in spectra[17])
    choices = []
    for upper in P["candidate_energy_max_mev"]:
        for ne in P["candidate_energy_nodes"]:
            metrics = {str(nk):nodal_deficit(spec,upper,ne) for nk,spec in spectra.items()}
            worst = max(metrics.values())
            exact = max(tail_deficits(sp,upper)[0] for sp in spectra.values())
            choices.append(dict(upper_mev=upper,ne=ne,delta_mev=(upper-EMIN)/(ne-1),
                analytic_matrix_deficit=exact,trapezoid_matrix_deficit=worst,
                trapezoid_by_nk=metrics,trusted_upper_mev=upper-MARGIN,
                trusted_trace_deficit=max(tail_deficits(sp,upper-MARGIN,EMIN+MARGIN)[1] for sp in spectra.values()),
                trusted_worst_orbital_deficit=max(tail_deficits(sp,upper-MARGIN,EMIN+MARGIN)[2] for sp in spectra.values()),
                both_sum_gates_pass=bool(worst<=.001 and exact<=.001)))
    # A registered window plus a deliberately resolved step gives a resource
    # reference, separate from the compact-grid admission. The integer grid
    # size is determined from the analytic cutoff rather than nudging nodes.
    design_upper = float(np.ceil((emax+MARGIN)/50)*50)
    resolution_design = []
    for step in (.50,.40,.35):
        ne = int(np.ceil((design_upper-EMIN)/step))+1
        resolution_design.append(dict(upper_mev=design_upper,ne=ne,
            delta_mev=(design_upper-EMIN)/(ne-1),
            trapezoid_matrix_deficit=max(nodal_deficit(s,design_upper,ne) for s in spectra.values())))
    return dict(local_max_mev=float(local_max),coupling_norm_mev=float(coupling),
        exact_cavity_max_mev=float(max(row[0][-1] for row in spectra[17])),
        analytic_min_upper_mev=emax,coarse_grid_options=choices,resolution_reference=resolution_design,
        full_FD_cavity=compare_full_fd_cavity(phi,spectra[17][::8],exact_cavities,860.0),
        worst_high_bloch=upper_poles(phi,h,t,m))


def main():
    result = dict(candidates=[],numerical_passers=[])
    for nz in P["spatial_nodes"]:
        ref = next(c for c in NATIVE["cases"] if (c["cbo_mev"],c["nz"])==(P["barrier_mev"],nz))
        lp,x,h,t,z,m,delta = cell_blocks(ref)
        exact_bloch = np.array([np.linalg.eigvalsh(h+q*t+q.conjugate()*t.T)[:4] for q in np.exp(1j*TEST)])
        finite = fd_chain(h,t,z,m,lp,NCELL,0.0,delta)
        u_cell = np.linalg.eigh(h)[1][:,:18]
        u_pod = {n:snapshot_modes(h,t,n) for n in sorted({v["train_bands"] for v in P["variant"] if "train_bands" in v})}
        exact_cavities = [fd_chain(h,t,z,m,lp,NSPEC,k) for k in (0.0,0.30,0.60)]
        for variant in P["variant"]:
            basis = space(variant,h,u_pod,u_cell)
            row = dict(nz=nz,**variant,**static_metrics(basis,h,t,z,lp,delta,finite,exact_bloch))
            print(nz,variant["name"],round(row["energy_gate_peak_mev"],4),round(row["pair_principal_sq"],5),row["static_05_pass"],flush=True)
            if row["static_05_pass"]:
                row["spectral_window"] = spectral_metrics(basis,h,t,z,m,lp,exact_cavities)
            result["candidates"].append(row)
    for v in P["variant"]:
        rows=[r for r in result["candidates"] if r["name"]==v["name"]]
        if all(r["static_05_pass"] for r in rows):
            assert all("spectral_window" in r for r in rows)
            common_windows = [set((x["upper_mev"],x["ne"]) for x in r["spectral_window"]["coarse_grid_options"]
                                  if x["both_sum_gates_pass"]) for r in rows]
            result["numerical_passers"].append(dict(name=v["name"],rank=v["rank"],
                common_compact_grid_passes=sorted(set.intersection(*common_windows))))
    (HERE/"results.json").write_text(json.dumps(result,indent=2)+"\n")
    fields = ("nz","name","method","rank","first_four_bloch_peak_mev","pair_error_mev",
              "splitting_error_mev","pair_principal_sq","broader_active_peak_mev","broader_active_min_sq",
              "static_05_pass","original_01_pass")
    with (HERE/"summary.csv").open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore")
        writer.writeheader()
        writer.writerows(result["candidates"])

if __name__=="__main__":
    main()
