"""Independent FD benchmark for a real, translation-invariant Bloch snapshot POD."""
import csv
import json
from pathlib import Path
import tomllib

import numpy as np

HERE = Path(__file__).resolve().parent
BANDS = HERE.parent / "bands"
P = tomllib.loads((BANDS / "passport.toml").read_text())
NATIVE = tomllib.loads((BANDS / "native.toml").read_text())
K = 6.62607015e-34**2 / ((2*np.pi)**2 * 2 * 9.1093837139e-31 * 1.602176634e-22 * 1e-18)
TRAIN = 2*np.pi*np.arange(24)/24
HOLDOUT = 2*np.pi*(np.arange(211) + np.sqrt(3)/11)/211
CELLS = 2 * P["basis_half_window_periods"] + 1

def cell_blocks(case):
    widths = np.array(P["layer_width_nm"])
    lp, nz = widths.sum(), case["nz"]
    dz = lp/nz
    x = (np.arange(nz)+0.5)*dz
    layer = np.searchsorted(widths.cumsum(), x, side="right")+1
    barrier = np.isin(layer, P["barrier_layers_1based"])
    mass = np.where(barrier, P["barrier_mass_z_parallel_over_me"], P["well_mass_z_parallel_over_me"])
    edge = np.where(barrier, case["cbo_mev"], P["energy_zero_mev"])
    hops = 2*K/(mass+np.roll(mass,-1))/dz**2
    cell = np.diag(edge + hops + np.roll(hops,1)) - np.diag(hops[:-1],1) - np.diag(hops[:-1],-1)
    plus = np.zeros((nz,nz))
    plus[-1,0] = -hops[-1]
    end_delta = K/(mass[[0,-1]]*dz**2) - hops[-1]
    return lp, x, cell, plus, np.diag(x), np.diag(1/mass), end_delta


def bloch(h, t, phase, levels):
    energies, vectors = np.linalg.eigh(h + (phase*t) + (phase.conjugate()*t.T))
    return energies[:levels], vectors[:,:levels]


def pod(h, t):
    frames = [bloch(h,t,np.exp(1j*q),9)[1] for q in TRAIN]
    bases = {}
    for count in (3,4,5,6,7,8,9):
        snapshots = np.hstack([u[:,:count] for u in frames])
        real_snapshots = np.hstack([snapshots.real, snapshots.imag])/np.sqrt(len(TRAIN))
        basis, singular, _ = np.linalg.svd(real_snapshots, full_matrices=False)
        bases[count] = basis, singular
    return bases


def angle_bounded_basis(h, phi, maximum_angle):
    """Clip principal rotations from the lowest isolated-cell Ritz vectors."""
    anchor = np.linalg.eigh(h)[1][:,:phi.shape[1]]
    u, sigma, vh = np.linalg.svd(anchor.T @ phi)
    reference, endpoint = anchor @ u, phi @ vh.T
    angle = np.arccos(np.clip(sigma,0,1))
    limited = np.minimum(angle,maximum_angle)
    scale = np.divide(np.sin(limited),np.sin(angle),out=np.ones_like(angle),where=angle>1e-12)
    result = reference*(np.cos(limited)-scale*sigma)+endpoint*scale
    return np.linalg.qr(result)[0]


def seam_basis(h, nb):
    """Cell component modes with two static seam attachment modes."""
    interior = h[1:-1,1:-1]
    boundary_coupling = h[1:-1][:,[0,-1]]
    _, fixed_modes = np.linalg.eigh(interior)
    fixed_modes = fixed_modes[:,:nb-2]
    boundary_modes = -np.linalg.solve(interior,boundary_coupling)
    cell_modes = np.zeros((len(h),nb))
    cell_modes[1:-1,:nb-2] = fixed_modes
    cell_modes[1:-1,nb-2:] = boundary_modes
    cell_modes[0,nb-2] = cell_modes[-1,nb-1] = 1
    return np.linalg.qr(cell_modes)[0]


def window(lp, x, h, t, delta, volts):
    diag = np.tile(np.diag(h), CELLS)
    diag -= volts/lp * (x[None,:]+lp*(np.arange(CELLS)-CELLS//2)[:,None]).ravel()
    diag[0] += delta[0]
    diag[-1] += delta[1]
    off = np.tile(np.r_[np.diag(h,1), t[-1,0]], CELLS)[:-1]
    energies, vectors = np.linalg.eigh(np.diag(diag)+np.diag(off,1)+np.diag(off,-1))
    count = np.searchsorted(energies, 300)
    return energies[:count], vectors[:,:count]


def projected_window(nb, vh, vt, vz, lp, voltage, phi, delta):
    shift = np.arange(CELLS)-CELLS//2
    across = np.eye(CELLS,k=1)
    h = (np.kron(np.eye(CELLS),vh-voltage/lp*vz) -
         np.diag(np.repeat(shift*voltage,nb)) +
         np.kron(across,vt)+np.kron(across.T,vt.T))
    h[:nb,:nb] += delta[0]*np.outer(phi[0],phi[0])
    h[-nb:,-nb:] += delta[1]*np.outer(phi[-1],phi[-1])
    return np.linalg.eigh(h)


def squared_subspace_overlap(q, r):
    return float(np.min(np.linalg.svd(q.conj().T @ r, compute_uv=False))**2)


def score_bloch(phi, h, t, full_holdout):
    nb = phi.shape[1]
    vh, vt = phi.T@h@phi, phi.T@t@phi
    error, rank_overlap, subspace, coverage = [], [], [], []
    for (ef, uf), q in zip(full_holdout, HOLDOUT, strict=True):
        er, ur = bloch(vh,vt,np.exp(1j*q),nb)
        psi = phi@ur
        error.append(er-ef[:nb])
        rank_overlap.append(abs(np.sum(uf[:,:nb].conj()*psi,axis=0))**2)
        subspace.append([squared_subspace_overlap(uf[:,:k],psi[:,:k]) for k in (3,4,5)])
        coverage.append([squared_subspace_overlap(uf[:,:k],phi) for k in (3,4,5)])
    assert np.min(error) >= -1e-7
    return dict(max_abs_error_mev=np.max(np.abs(error),axis=0).tolist(),
                min_squared_rank_overlap=np.min(rank_overlap,axis=0).tolist(),
                lowest_3_4_5_min_squared_ritz_principal_overlap=np.min(subspace,axis=0).tolist(),
                lowest_3_4_5_min_squared_projection_principal_overlap=np.min(coverage,axis=0).tolist())


def score_window(phi, h, t, z, lp, delta, volt, full):
    nb = phi.shape[1]
    energy, wave = full
    ranked, reduced = projected_window(nb, phi.T@h@phi, phi.T@t@phi, phi.T@z@phi, lp, volt, phi, delta)
    embedding = np.kron(np.eye(CELLS),phi)
    embedded = embedding @ reduced
    i = CELLS//2*len(h)
    central_weight = np.sum(np.abs(wave[i:i+len(h)])**2,axis=0)
    def match(upper_bound):
        index = np.flatnonzero((central_weight>=0.10)&(energy>=-100)&(energy<=upper_bound))
        overlaps = abs(wave[:,index].T @ embedded)**2
        rows, cols = np.arange(len(index)), np.argmax(overlaps,axis=1)
        errors = ranked[cols]-energy[index[rows]]
        return dict(max_abs_matched_error_mev=float(max(abs(errors))),
                    min_matched_squared_overlap=float(min(overlaps[rows,cols])),
                    distinct_dominant_matches=int(len(set(cols))),
                    min_projection_weight=float(min(overlaps.sum(axis=1))),
                    matches=[dict(full_index=int(j+1),fd_mev=float(energy[j]),
                                  ritz_mev=float(ranked[c]),error_mev=float(e),
                                  squared_overlap=float(overlaps[r,c]))
                             for r,c,j,e in zip(rows,cols,index[rows],errors,strict=True)])
    count = CELLS*4
    shifts = ranked[:count]-energy[:count]
    assert min(shifts) >= -1e-7
    return dict(lowest_four_per_cell_max_rank_error_mev=float(max(abs(shifts))),
                lowest_four_per_cell_min_squared_ritz_principal_overlap=squared_subspace_overlap(wave[:,:count],embedded[:,:count]),
                lowest_four_per_cell_min_squared_projection_principal_overlap=squared_subspace_overlap(wave[:,:count],embedding),
                central_to_80_mev=match(80),central_to_170_mev=match(170))


def write_summary(results):
    rows = []
    for geometry in results:
        for case in geometry["cases"]:
            zero = case["finite"]["0.0"]
            biased = case["finite"]["54.0"]
            active = biased["central_to_80_mev"]
            broad = biased["central_to_170_mev"]
            bloch = case["bloch"]
            rows.append(dict(
                barrier_mev=geometry["cbo_mev"],nz=geometry["nz"],nb=case["nb"],
                method=case["method"],train_bands=case.get("train_bands"),
                max_principal_angle_rad=case.get("max_principal_angle_rad"),
                bloch_low4_max_error_mev=max(bloch["max_abs_error_mev"][:4]),
                bloch_low4_min_squared_ritz_principal_overlap=bloch["lowest_3_4_5_min_squared_ritz_principal_overlap"][1],
                bloch_last_band_max_error_mev=bloch["max_abs_error_mev"][-1],
                zero_field_lowest_28_ranked_max_error_mev=zero["lowest_four_per_cell_max_rank_error_mev"],
                zero_field_lowest_28_min_squared_ritz_principal_overlap=zero["lowest_four_per_cell_min_squared_ritz_principal_overlap"],
                tilted_lowest_28_ranked_max_error_mev=biased["lowest_four_per_cell_max_rank_error_mev"],
                tilted_active_max_paired_error_mev=active["max_abs_matched_error_mev"],
                tilted_active_min_squared_overlap=active["min_matched_squared_overlap"],
                tilted_active_distinct_dominant_matches=active["distinct_dominant_matches"],
                tilted_active_candidate_count=len(active["matches"]),
                tilted_broad_max_paired_error_mev=broad["max_abs_matched_error_mev"],
                tilted_broad_min_squared_overlap=broad["min_matched_squared_overlap"],
            ))
    with (HERE/"summary.csv").open("w", newline="") as output:
        writer = csv.DictWriter(output,fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    results = []
    for case in NATIVE["cases"]:
        lp, x, h, t, z, mass_inv, delta = cell_blocks(case)
        bases = pod(h,t)
        full_holdout = [bloch(h,t,np.exp(1j*q),9) for q in HOLDOUT]
        finite = {v:window(lp,x,h,t,delta,v) for v in P["voltage_mv_per_period"]}
        cases = []
        def evaluate(label, phi, **extra):
            b = score_bloch(phi,h,t,full_holdout)
            f = {str(v):score_window(phi,h,t,z,lp,delta,v,full) for v,full in finite.items()}
            cases.append(dict(method=label,nb=phi.shape[1],bloch=b,finite=f,**extra))
        for pzp in case["basis"]:
            evaluate("pzp",np.asarray(pzp["phi"]))
        for count, (basis,singular) in bases.items():
            for nb in P["modes"]:
                evaluate("bloch_pod",basis[:,:nb],train_bands=count,
                         orthogonality=float(np.linalg.norm(basis[:,:nb].T@basis[:,:nb]-np.eye(nb))),
                         discarded_snapshot_fraction=float(sum(singular[nb:]**2)/sum(singular**2)))
        for nb in P["modes"]:
            evaluate("bounded_bloch_pod",angle_bounded_basis(h,bases[5][0][:,:nb],0.25),
                     train_bands=5,max_principal_angle_rad=0.25)
            evaluate("seam_attachment",seam_basis(h,nb))
        results.append(dict(cbo_mev=case["cbo_mev"],nz=case["nz"],cases=cases))
    result = dict(core_commit=P["core_commit"],periods=CELLS,train_phase_count=len(TRAIN),
                  holdout_phase_count=len(HOLDOUT),holdout_phase_offset=float(np.sqrt(3)/11),
                  central_selection_min_weight=0.10,central_selection_min_energy_mev=-100,
                  numpy_version=np.__version__,results=results)
    julia_path = HERE/"verification.toml"
    if julia_path.exists():
        native_pod = tomllib.loads(julia_path.read_text())
        case = next(c for c in NATIVE["cases"] if (c["cbo_mev"],c["nz"])==(149,144))
        lp,x,h,t,z,m,delta = cell_blocks(case)
        julia_basis = np.asarray(native_pod["phi"])
        python_basis = angle_bounded_basis(h,pod(h,t)[5][0][:,:7],0.25)
        projector_error = np.linalg.norm(julia_basis@julia_basis.T-python_basis@python_basis.T,ord=2)
        assert projector_error < 1e-9
        full_holdout = [bloch(h,t,np.exp(1j*q),9) for q in HOLDOUT]
        independent_fd_54mv = window(lp,x,h,t,delta,54.0)
        result["julia_implementation_holdout"] = dict(
            subspace_projector_norm_error=float(projector_error),
            bloch=score_bloch(julia_basis,h,t,full_holdout),
            finite_54mv=score_window(julia_basis,h,t,z,lp,delta,54.0,independent_fd_54mv),
        )
    (HERE/"holdout.json").write_text(json.dumps(result,indent=2)+"\n")
    write_summary(results)


if __name__ == "__main__":
    main()
