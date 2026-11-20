"""Evaluate the target POD7/rank9 window at each requested radial grid."""
import json

import numpy as np

from refine import HERE, NATIVE, EMIN, ETA, MARGIN, K, TEST, FIELD, NSPEC
from refine import cell_blocks, cavity, nodal_deficit, tail_deficits
from refine import e171_frobenius, snapshot_modes

E_MAX = 4000.0
NE = 11001
DELTA = (E_MAX-EMIN)/(NE-1)


def main():
    rows, scales = [], []
    for nz in (144,192):
        case = next(c for c in NATIVE["cases"] if (c["cbo_mev"],c["nz"])==(149,nz))
        lp,x,h,t,z,m,_ = cell_blocks(case)
        basis = snapshot_modes(h,t,7)[:,:9]
        # A physical energy-scale reference: take the exact first four and
        # first nine FD bands at the largest k (the transverse term is PSD),
        # before adding the finite-chain field span and trust reserve.
        hk = h+K*0.60**2*m
        full_Bloch = np.array([np.linalg.eigvalsh(hk+q*t+q.conjugate()*t.T)[:9]
                              for q in np.exp(1j*TEST)])
        upper_scales = {str(n):float(max(full_Bloch[:,n-1])) for n in (4,9)}
        scales.append(dict(nz=nz,exact_fd_bloch_max_by_rank_mev=upper_scales,
            energy_scale_with_field_span_and_margin_mev={
                n:ep+FIELD*(NSPEC//2)+MARGIN for n,ep in upper_scales.items()}))
        for nk in (9,13,17):
            spectra = [cavity(basis,h,t,z,m,lp,k) for k in np.linspace(0,0.60,nk)]
            # Isolate the lower and upper continuous omissions in the full matrix.
            lower = max(e171_frobenius(v,0.5+np.arctan((e-EMIN)/ETA)/np.pi) for e,_,v,_,_ in spectra)
            upper = max(e171_frobenius(v,0.5+np.arctan((E_MAX-e)/ETA)/np.pi) for e,_,v,_,_ in spectra)
            per_k = [nodal_deficit([row],E_MAX,NE) for row in spectra]
            rows.append(dict(nz=nz,nk=nk,analytic_both_edges_r_sum=tail_deficits(spectra,E_MAX)[0],
                             analytic_lower_edge_only_r_sum=lower,analytic_upper_edge_only_r_sum=upper,
                             discrete_r_sum=max(per_k),worst_k_inverse_nm=0.60*np.argmax(per_k).item()/(nk-1),
                             trusted_window_analytic_r_sum=tail_deficits(spectra,E_MAX-MARGIN,EMIN+MARGIN)[0],
                             lowest_cavity_pole_mev=float(min(x[0][0] for x in spectra)),
                             highest_cavity_pole_mev=float(max(x[0][-1] for x in spectra))))
    summary = dict(rank=9,method="pod7-r9",eta_mev=ETA,ne=NE,energy_mev=[EMIN,E_MAX],
                   energy_step_mev=DELTA,eta_to_energy_step=ETA/DELTA,
                   infinite_uniform_line_max_comb_alias=2/np.expm1(2*np.pi*ETA/DELTA),
                   rows=rows,fd_bloch_energy_scale=scales)
    (HERE/"resolved_grid.json").write_text(json.dumps(summary,indent=2)+"\n")

if __name__ == "__main__":
    main()
