"""Compare native finite-window PzP choices against common Bloch and biased FD operators."""

import json
import sys
import tomllib

import numpy as np

from compare import HERE, NATIVE, K, MASS, MATERIAL, WIDTHS, PERIOD, BASIS_WINDOW, PERIOD_COUNT
from compare import fd_blocks, floquet, open_window, write_csv

BLOCH_COUNT = 4
FIELD = 54.0
OVERLAP_TARGET = 0.95
ENERGY_TARGET_MEV = 0.10


def basis_gate(basis):
    limit_by_diagnostic = {
        "r_orth": 1e-12, "r_eigen": 1e-12, "r_translation": 0.10,
        "r_translation_nearest": 0.10,
        "r_translation_two_pairs": 0.005 if basis["basis_half_window"] >= 3 else 0.10,
    }
    return [name for name, limit in limit_by_diagnostic.items() if basis[name] > limit]


def biased_pair(weights):
    """Find the two Ritz eigenvectors maximizing the smaller principal cosine squared."""
    left, right = np.triu_indices(weights.shape[1], k=1)
    column_norm2 = np.sum(abs(weights)**2, axis=0)
    trace = column_norm2[left] + column_norm2[right]
    det2 = abs(weights[0, left]*weights[1, right] - weights[0, right]*weights[1, left])**2
    discriminant = np.sqrt(np.maximum(0, trace**2 - 4*det2))
    least = (trace-discriminant)/2
    is_best = int(np.lexsort((-trace, -least))[0])
    return np.array([left[is_best], right[is_best]]), float(least[is_best]), float((trace[is_best]+discriminant[is_best])/2)


def compare(source):
    nz = source["nz"]
    cbo = source["cbo_mev"]
    dx = PERIOD/nz
    coord = (np.arange(nz)+0.5)*dx
    layer = np.searchsorted(WIDTHS.cumsum(), coord, side="right")
    mass = MASS[layer]
    cell, plus, seam = fd_blocks(np.where(MATERIAL, cbo, 0)[layer], mass, dx)
    fdbloch = np.array([vals[:BLOCH_COUNT] for vals, _ in floquet(cell, plus, plus.T)])
    ends = np.zeros((2, nz, nz))
    ends[0, 0, 0] = ends[1, -1, -1] = 1
    delta = K/(mass[[0, -1]]*dx**2) - seam
    e, wave = open_window(cell, plus, plus.T, np.diag(coord), FIELD, delta, ends)
    central = slice(BASIS_WINDOW*nz, (BASIS_WINDOW+1)*nz)
    central_probability = np.sum(abs(wave[central])**2, axis=0)
    targets = np.flatnonzero((central_probability >= 0.85) & (e > 0) & (e < 20))
    assert len(targets) == 2, (cbo, nz, targets)
    reference = wave[:, targets]
    split = e[targets[1]]-e[targets[0]]
    rows = []
    escale, zscale = NATIVE["scales"]["energy_mev"], NATIVE["scales"]["length_nm"]
    for b in source["records"]:
        nb, half_window = b["nb"], b["basis_half_window"]
        row = dict(nz=nz, nb=nb, p_basis=half_window)
        if "error" in b:
            row.update(e171_pass=False, failed_basis_gate=None, e171_error=b["error"])
            rows.append(row)
            continue
        failed = basis_gate(b)
        h, t, tm, h54 = [escale*np.asarray(b[key]) for key in ("h0", "tplus", "tminus", "h54")]
        z = zscale*np.asarray(b["position"])
        phi = np.asarray(b["phi"])
        expected = [phi.T @ matrix @ phi for matrix in (cell, plus, plus.T, np.diag(coord))]
        difference = max(np.max(abs(a-r)) for a,r in zip((h,t,tm,z), expected, strict=True))
        h54_error = np.max(abs(h54 - (h-FIELD/PERIOD*z)))
        assert max(difference,h54_error) < 1e-8
        ebloch = np.array([vals[:BLOCH_COUNT] for vals, _ in floquet(h, t, tm)])
        bloch_error = np.max(abs(ebloch-fdbloch), axis=0)
        end_projectors = [np.outer(phi[index], phi[index]) for index in (0, -1)]
        eb, w = open_window(h54, t, tm, np.zeros_like(z), FIELD, delta, end_projectors)
        embedded = np.kron(np.eye(PERIOD_COUNT), phi)
        weights = reference.T @ embedded @ w
        pair, sq_low, sq_high = biased_pair(weights)
        assert -1e-12 <= sq_low <= sq_high <= 1+1e-12
        t_coverage = np.linalg.svd(weights, compute_uv=False)**2
        ep = eb[pair]
        pair_errors = ep - e[targets]
        row.update(e171_pass=not failed, failed_basis_gate=failed, e171_error=None,
                   r_translation=b["r_translation"], r_translation_nearest=b["r_translation_nearest"],
                   r_translation_two_pairs=b["r_translation_two_pairs"],
                   overlap_matrix_min_eig=b["overlap_min"],
                   fd_reference_pair_mev=e[targets].tolist(),
                   fd_reference_pair_idx=(targets+1).tolist(),
                   fd_central_probability=central_probability[targets].tolist(),
                   fd_reference_split_mev=float(split),
                   pzp_pair_mev=ep.tolist(), pair_indices_1based=(pair+1).tolist(),
                   pair_signed_errors_mev=pair_errors.tolist(), pair_split_mev=float(np.diff(ep).item()),
                   pair_split_abs_error_mev=abs(float(np.diff(ep).item())-split),
                   pair_principal_lo_sq=sq_low, pair_principal_hi_sq=sq_high,
                   full_pzp_subspace_principal_min_sq=float(t_coverage[-1]),
                   bloch_1_4_error_mev=bloch_error.tolist(), bloch_1_4_peak_mev=float(np.max(bloch_error)),
                   native_projection_check_peak_mev_or_nm=max(float(difference), float(h54_error)),
                   standalone_scientific_targets_pass=(
                       not failed and sq_low>=OVERLAP_TARGET and max(abs(pair_errors))<=ENERGY_TARGET_MEV
                       and abs(float(np.diff(ep).item())-split)<=ENERGY_TARGET_MEV
                       and np.max(bloch_error)<=ENERGY_TARGET_MEV))
        rows.append(row)
    return rows


def main():
    mode = sys.argv[1]
    assert mode in ("scan", "refine")
    source = tomllib.loads((HERE / f"native_{mode}.toml").read_text())
    rows = compare(source)
    accepted = [row for row in rows if row["e171_pass"]]
    order = lambda r: (-r["pair_principal_lo_sq"], r["pair_split_abs_error_mev"], r["bloch_1_4_peak_mev"])
    accepted.sort(key=order)
    evidence = {
        "fd_window_periods": PERIOD_COUNT, "fd_voltage_mv": FIELD, "target_pair_definition":
        "full FD states with central probability >=0.85 and E strictly between 0 and 20 meV at CBO149",
        "native_basis_anchor": {"nb": 7, "p_basis": 3},
        "sorting": ["descending smaller principal squared cosine", "ascending splitting error",
                    "ascending peak Bloch error"],
        "proposed_spectral_goals": {"pair_principal_low_squared_min": OVERLAP_TARGET,
                                    "energy_and_gap_error_mev_max": ENERGY_TARGET_MEV},
        "ranked_static_pass": [{"nb":r["nb"],"p_basis":r["p_basis"]} for r in accepted],
        "count": len(rows), "static_pass_count": len(accepted),
        "all_targets_pass_count": sum(row.get("standalone_scientific_targets_pass", False) for row in rows),
        "cases": sorted(rows, key=lambda row: (0, *order(row)) if row["e171_pass"] else (1, row["p_basis"], row["nb"])),
    }
    fields = [
        "nz", "nb", "p_basis", "e171_pass", "failed_basis_gate", "e171_error", "r_translation",
        "r_translation_nearest", "r_translation_two_pairs", "pair_principal_lo_sq",
        "pair_principal_hi_sq", "full_pzp_subspace_principal_min_sq", "pair_split_abs_error_mev",
        "pair_split_mev", "fd_reference_split_mev", "bloch_1_4_peak_mev", "bloch_1_4_error_mev",
        "pzp_pair_mev", "fd_reference_pair_mev", "pair_signed_errors_mev",
        "standalone_scientific_targets_pass",
    ]
    (HERE / f"basis_{mode}.json").write_text(json.dumps(evidence, indent=2) + "\n")
    write_csv(f"basis_{mode}.csv", [{key: row.get(key, "") for key in fields} for row in evidence["cases"]])


if __name__ == "__main__":
    main()
