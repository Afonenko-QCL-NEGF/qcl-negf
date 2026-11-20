"""Spectral measure of the noninteracting 54 mV, nine-cell cavity reference."""
import json
import sys

import numpy as np

from holdout import HERE, NATIVE, P, K, angle_bounded_basis, cell_blocks, pod, window

FIELD = 54.0
E_MIN, E_MAX = -400.0, 560.0
MARGIN = 260.0
ETA = 0.5
TEMPERATURE_ENERGY = P["lattice_temperature_k"] * 1.380649e-23 / 1.602176634e-22
DONOR_PER_NM2 = P["donor_sheet_cm2"] * P["ionized_fraction"] * 1e-14
NK = 17
KMAX = 0.60
K_NODES = np.linspace(0, KMAX, NK)
K_FACES = np.r_[0, (K_NODES[1:]+K_NODES[:-1])/2, KMAX]
K_WEIGHTS = np.diff(K_FACES**2)/(4*np.pi)
CELLS = 9
SHIFT = np.arange(CELLS)-CELLS//2


def estimate(basis, cell, hopping, z, inv_mass, active_density, lp):
    n = basis.shape[1]
    h = basis.T @ (cell-FIELD/lp*z) @ basis
    t = basis.T @ hopping @ basis
    m = basis.T @ inv_mass @ basis
    reduced_active = basis.T @ active_density @ basis
    p = np.diag(np.ones(CELLS-1),1)
    shifted_coupling = np.kron(p,t)+np.kron(p.T,t.T)-np.diag(np.repeat(FIELD*SHIFT,n))
    eig = []
    maximum_local = -np.inf
    for k in K_NODES:
        hk = h+K*k*k*m
        maximum_local = max(maximum_local,np.linalg.eigvalsh(hk)[-1])
        e, full_u = np.linalg.eigh(np.kron(np.eye(CELLS),hk)+shifted_coupling)
        u = full_u[(CELLS//2)*n:(CELLS//2+1)*n]
        total = np.sum(u*u,axis=0)
        active = np.sum(u*(reduced_active@u),axis=0)
        eig.append((e,total,active,u))
    energies, trace, active, _ = [np.array(row) for row in zip(*eig)]
    trace *= K_WEIGHTS[:,None]
    active *= K_WEIGHTS[:,None]
    norm_t, norm_a = trace.sum(),active.sum()
    def tails(low,high):
        lower = 0.5+np.arctan((low-energies)/ETA)/np.pi
        upper = 0.5+np.arctan((energies-high)/ETA)/np.pi
        average_lost_upper_matrix = sum(w*((u*f)@u.T) for w, f, (_,_,_,u)
                                        in zip(K_WEIGHTS,upper,eig)) / sum(K_WEIGHTS)
        return dict(total_lower_fraction=float((lower*trace).sum()/norm_t),
                    total_upper_fraction=float((upper*trace).sum()/norm_t),
                    active_lower_fraction=float((lower*active).sum()/norm_a),
                    active_upper_fraction=float((upper*active).sum()/norm_a),
                    worst_single_orbital_upper_fraction=float(np.linalg.eigvalsh(average_lost_upper_matrix)[-1]))
    def occupied(mu):
        fermi = np.exp(-np.logaddexp(0.0,(energies-mu)/TEMPERATURE_ENERGY))
        return trace*fermi
    mu_min, mu_max = np.min(energies)-100, np.max(energies)+100
    for _ in range(60):
        mu = (mu_min+mu_max)/2
        if 2*occupied(mu).sum() < DONOR_PER_NM2:
            mu_min = mu
        else:
            mu_max = mu
    occupation = occupied(mu)
    k0 = eig[0]
    local0 = np.linalg.eigvalsh(h)
    return dict(active_reference_weight_retained=float(np.trace(reduced_active)/np.trace(active_density)),
                maximum_local_pole_mev=float(maximum_local),
                k0_local_poles_mev=local0.tolist(),
                coupling_norm_mev=float(np.linalg.norm(t,ord=2)),
                conservative_maximum_local_plus_twice_coupling_norm_mev=float(maximum_local+2*np.linalg.norm(t,ord=2)),
                exact_finite_cavity_maximum_pole_mev=float(np.max(energies)),
                above_sampled_pole_count_on_k_grid=int(np.count_nonzero(energies>E_MAX)),
                central_weighted_total_k0_spectral_mass_above_sampled_uncorrected=float(k0[1][k0[0]>E_MAX].sum()),
                sampled=tails(E_MIN,E_MAX),trusted=tails(E_MIN+MARGIN,E_MAX-MARGIN),
                thermal_reference_chemical_potential_mev=float(mu),
                thermal_reference_upper_sampled_occupancy_fraction=float(occupation[energies>E_MAX].sum()/occupation.sum()),
                thermal_reference_upper_trusted_occupancy_fraction=float(occupation[energies>E_MAX-MARGIN].sum()/occupation.sum()))


def main():
    case = next(c for c in NATIVE["cases"] if c["cbo_mev"]==149 and c["nz"]==144)
    lp,x,h,t,z,m,delta = cell_blocks(case)
    e, waves = window(lp,x,h,t,delta,FIELD)
    i = P["basis_half_window_periods"]*len(h)
    central = waves[i:i+len(h)]
    selected = (np.sum(central**2,axis=0)>=0.10)&(e>=-100)&(e<=80)
    active = central[:,selected]@central[:,selected].T
    report = dict(energy_window_mev=[E_MIN,E_MAX],trusted_window_mev=[E_MIN+MARGIN,E_MAX-MARGIN],
                  voltage_mv=FIELD,n_k=NK,max_k_inverse_nm=KMAX,broadening_mev=ETA,
                  thermal_reference_temperature_k=P["lattice_temperature_k"],
                  active_reference="Central restriction of full FD7 modes in [-100,80] meV with central weight >=0.10",
                  spectral_reference="Exact finite nine-cell cavity with projected kinetic operator, k; constant Lorentzian 0.5 meV",
                  equilibrium_occupancy_reference="10 K Fermi occupation of discrete poles; common mu from central sheet weight and donor target",
                  candidates={})
    for trial in case["basis"]:
        if trial["nb"] in (7,9):
            report["candidates"][f"pzp{trial['nb']}"] = estimate(np.asarray(trial["phi"]),h,t,z,m,active,lp)
    for trains,(u,_) in pod(h,t).items():
        if trains in (5,6,7,8):
            for rank in (7,9):
                report["candidates"][f"pod{trains}_rank{rank}"] = estimate(u[:,:rank],h,t,z,m,active,lp)
    bounded=angle_bounded_basis(h,pod(h,t)[5][0][:,:7],0.25)
    report["candidates"]["bounded_pod5_rank7_0p25rad"]=estimate(bounded,h,t,z,m,active,lp)
    for file in sys.argv[1:]:
        from pathlib import Path
        path=Path(file)
        report["candidates"][path.stem]=estimate(np.loadtxt(path),h,t,z,m,active,lp)
    (HERE/"window_weight.json").write_text(json.dumps(report,indent=2)+"\n")

if __name__=="__main__":
    main()
