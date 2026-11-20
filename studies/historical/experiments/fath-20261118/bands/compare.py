"""Independent scalar BDD continuum and FD benchmark of the pinned e171 PzP export."""

import csv
import json
from pathlib import Path
import tomllib

import numpy as np

HERE = Path(__file__).resolve().parent
P = tomllib.loads((HERE / "passport.toml").read_text())
NATIVE = tomllib.loads((HERE / "native.toml").read_text())
K = 1.054571817e-34**2 / (2 * 9.1093837139e-31 * 1.602176634e-22 * 1e-18)
WIDTHS = np.array(P["layer_width_nm"])
PERIOD = round(sum(WIDTHS), 12)
PHASES = np.arange(15) * np.pi / 14
BASIS_WINDOW = P["basis_half_window_periods"]
PERIOD_COUNT = 2 * BASIS_WINDOW + 1
MATERIAL = np.isin(np.arange(1, len(WIDTHS) + 1), P["barrier_layers_1based"])
DONOR = np.isin(np.arange(1, len(WIDTHS) + 1), P["donor_layers_1based"])
MASS = np.where(MATERIAL, P["barrier_mass_z_parallel_over_me"], P["well_mass_z_parallel_over_me"])
BLOCH_BANDS = 9
LIMITS = {"orthogonality": 1e-12, "eigen": 1e-12, "translation": 0.1,
          "translation_nearest": 0.1, "translation_two_pairs": 5e-3}


def continuum_trace(energy, width, edges):
    """The state is (psi, psi'/m_rel), continuous at every interface."""
    m11, m12, m21, m22 = 1.0, 0.0, 0.0, 1.0
    for w, mass, edge in zip(width, MASS, edges, strict=True):
        q2 = mass * (energy - edge) / K
        q = np.sqrt(q2 + 0j)
        c = np.cos(w * q).real
        s = w * np.sinc(w * q / np.pi).real
        a, b = mass * s, -q2 / mass * s
        m11, m12, m21, m22 = (c*m11 + a*m21, c*m12 + a*m22, b*m11 + c*m21, b*m12 + c*m22)
    return m11 + m22


def continuum(width, edges):
    spectra = []
    for step in (0.025, 0.0125):
        grid = np.linspace(0, 350, round(350 / step) + 1)
        discriminant = continuum_trace(grid, width, edges)
        phase_rows = []
        for phase in PHASES:
            target = 2 * np.cos(phase)
            residual = discriminant - target
            roots = list(grid[residual == 0.0])
            for index in np.flatnonzero(residual[:-1] * residual[1:] < 0):
                lo, hi = grid[index:index + 2]
                sign = residual[index] > 0
                for _ in range(39):
                    mid = (lo + hi) / 2
                    if (continuum_trace(mid, width, edges) > target) == sign:
                        lo = mid
                    else:
                        hi = mid
                roots.append((lo + hi) / 2)
            assert len(roots) >= BLOCH_BANDS, (width, phase, roots)
            phase_rows.append(sorted(roots)[:BLOCH_BANDS])
        spectra.append(np.array(phase_rows))
    error = np.max(abs(spectra[0] - spectra[1]))
    assert error < 1e-9
    return spectra[1], float(error)


def fd_blocks(edge, mass, dz):
    hop = 2*K / (mass + np.roll(mass, -1)) / dz**2
    cell = np.diag(edge + hop + np.roll(hop, 1)) - np.diag(hop[:-1], 1) - np.diag(hop[:-1], -1)
    plus = np.zeros_like(cell)
    plus[-1, 0] = -hop[-1]
    return cell, plus, hop[-1]


def floquet(cell, plus, minus):
    return [np.linalg.eigh(cell + np.exp(1j*q)*plus + np.exp(-1j*q)*minus) for q in PHASES]


def open_window(cell, plus, minus, position, voltage, edge_hop_delta, edge_projectors):
    """Seven cells, hard ends with the same e171 Dirichlet diagonal convention."""
    n = len(cell)
    hops = np.eye(PERIOD_COUNT, k=1)
    shifts = np.arange(-BASIS_WINDOW, BASIS_WINDOW+1) * voltage
    h = np.kron(np.eye(PERIOD_COUNT), cell - voltage/PERIOD*position)
    h -= np.diag(np.repeat(shifts, n))
    h += np.kron(hops, plus) + np.kron(hops.T, minus)
    h[:n, :n] += edge_hop_delta[0] * edge_projectors[0]
    h[-n:, -n:] += edge_hop_delta[1] * edge_projectors[1]
    return np.linalg.eigh(h)


def max_by_band(values):
    return np.max(abs(values), axis=0).tolist()


def bounds(values):
    return list(zip(values.min(axis=0).tolist(), values.max(axis=0).tolist(), strict=True))


def write_csv(name, rows):
    with (HERE / name).open("w", newline="") as s:
        writer = csv.DictWriter(s, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def analyze_geometry(case, nominal, nominal_error, bloch_rows, finite_rows, spectrum_rows):
    cbo, nz = case["cbo_mev"], case["nz"]
    dx_scale = NATIVE["scales"]["length_nm"]
    energy_scale = NATIVE["scales"]["energy_mev"]
    edges = np.where(MATERIAL, cbo, P["energy_zero_mev"])
    dz = PERIOD / nz
    z = (np.arange(nz) + 0.5) * dz
    layer = np.searchsorted(WIDTHS.cumsum(), z, side="right")
    counts = np.bincount(layer, minlength=len(WIDTHS))
    assert np.all(counts > 0)
    stepped_width = counts * dz
    ec, mass = edges[layer], MASS[layer]
    np.testing.assert_allclose(case["coordinate"], z / dx_scale, atol=1e-12, rtol=0)
    np.testing.assert_allclose(case["weight"], dz / dx_scale, atol=1e-12, rtol=0)
    np.testing.assert_array_equal(case["layer_index"], layer+1)
    np.testing.assert_allclose(case["potential"], ec / energy_scale, atol=1e-14, rtol=0)
    np.testing.assert_array_equal(case["mass_z"], mass)
    np.testing.assert_array_equal(case["mass_parallel"], mass)
    density = np.asarray(case["donor_profile"]) / (dx_scale * 1e-7)**3
    target = P["donor_sheet_cm2"] * P["ionized_fraction"]
    sheet = density.sum() * dz * 1e-7
    np.testing.assert_array_equal(density > 0, DONOR[layer])
    assert abs(sheet / target - 1) < 1e-12
    stepped, stepped_error = continuum(stepped_width, edges)
    cell, plus, seam_hop = fd_blocks(ec, mass, dz)
    full = floquet(cell, plus, plus.T)
    full_bloch = np.array([e[:BLOCH_BANDS] for e, _ in full])
    edge_delta = K / (mass[[0, -1]] * dz**2) - seam_hop
    edge_projectors = np.zeros((2, nz, nz))
    edge_projectors[0, 0, 0] = edge_projectors[1, -1, -1] = 1
    voltages = P["voltage_mv_per_period"]
    all_z = (z[None, :] + np.arange(-BASIS_WINDOW, BASIS_WINDOW+1)[:, None] * PERIOD).ravel()
    central = slice(BASIS_WINDOW*nz, (BASIS_WINDOW+1)*nz)

    finite = {}
    for v in voltages:
        e, wave = open_window(cell, plus, plus.T, np.diag(z), v, edge_delta, edge_projectors)
        central_probability = np.sum(abs(wave[central])**2, axis=0)
        probability_by_well = np.array([
            np.sum(abs(wave[central][(layer >= lo) & (layer <= hi)])**2, axis=0)
            for lo, hi in [(1, 1), (3, 3), (5, 7)]
        ])
        centres = all_z @ (wave**2)
        # Store all low central-weight candidates useful for the biased active region.
        candidates = np.flatnonzero((central_probability >= 0.10) & (e >= -100) & (e <= 170))
        finite[v] = e, wave, candidates
        for j in candidates:
            spectrum_rows.append(dict(
                cbo_mev=cbo, nz=nz, voltage_mv=v, fd_index_1based=j+1, fd_mev=e[j],
                centre_nm=centres[j], central_probability=central_probability[j],
                central_well_1=probability_by_well[0, j], central_well_2=probability_by_well[1, j],
                central_well_3=probability_by_well[2, j],
            ))
    case_summary = dict(
        cbo_mev=cbo, nz=nz, dz_nm=dz, layer_counts=counts.tolist(), layer_width_effective_nm=stepped_width.tolist(),
        donor_density_cm3_max=float(density.max()), donor_sheet_cm2=float(sheet),
        continuum_refinement_max_mev=[nominal_error, stepped_error],
        nominal_range_mev=bounds(nominal), fd_range_mev=bounds(full_bloch),
        geometry_max_abs_mev=max_by_band(stepped - nominal),
        fd_truncation_max_abs_mev=max_by_band(full_bloch - stepped),
        fd_total_max_abs_mev=max_by_band(full_bloch - nominal),
        modes=[],
    )
    for b in case["basis"]:
        nb = b["nb"]
        phi = np.array(b["phi"])
        h, t, tminus = [energy_scale*np.array(b[key]) for key in ("h0", "tplus", "tminus")]
        position = dx_scale*np.array(b["position"])
        matrices = [h, t, tminus, position]
        exact = [phi.T @ op @ phi for op in (cell, plus, plus.T, np.diag(z))]
        matrix_errors = [float(np.max(abs(x-y))) for x, y in zip(matrices, exact, strict=True)]
        h54 = energy_scale*np.array(b["h54"])
        h54_error = float(np.max(abs(h54-(h-54/PERIOD*position))))
        assert max(*matrix_errors, h54_error) < 1e-8
        pzp = floquet(h, t, tminus)
        pzp_energies = np.array([e for e, _ in pzp])
        shifts = pzp_energies - full_bloch[:, :nb]
        assert np.min(shifts) >= -1e-8
        overlaps = np.array([
            abs(np.sum(u[:, :nb].conj() * (phi @ w), axis=0))**2
            for (_, u), (_, w) in zip(full, pzp, strict=True)
        ])
        for iq, (q, row) in enumerate(zip(PHASES, pzp_energies, strict=True)):
            for j, energy in enumerate(row):
                bloch_rows.append(dict(cbo_mev=cbo, nz=nz, nb=nb, phase_over_pi=q/np.pi,
                    band_1based=j+1, nominal_mev=nominal[iq, j], stepped_mev=stepped[iq, j],
                    fd_mev=full_bloch[iq, j], pzp_mev=energy, rank_matched_overlap=overlaps[iq, j]))
        diagnostics = {key: float(b[f"r_{key}"] if key != "orthogonality" else b["r_orth"])
                       for key in LIMITS}
        case_summary["modes"].append(dict(nb=nb, pzp_bloch_max_abs_error_mev=max_by_band(shifts),
            pzp_vs_nominal_bloch_max_abs_error_mev=max_by_band(pzp_energies-nominal[:, :nb]),
            pzp_bloch_range_mev=bounds(pzp_energies), rank_matched_overlap_min=overlaps.min(axis=0).tolist(),
            native_static_basis_pass=all(diagnostics[key] <= limit for key, limit in LIMITS.items()),
            native_basis_diagnostics=diagnostics, native_overlap_eigenvalue_min=b["overlap_min"],
            matrix_reconstruction_max_abs_H0_Tplus_Tminus_mev_Z_nm=matrix_errors,
            actual_h54_vs_independent_projection_mev=h54_error,
        ))

        end_projectors = [np.outer(phi[index], phi[index]) for index in (0, -1)]
        embed = np.kron(np.eye(PERIOD_COUNT), phi)
        for v, (e, wave, candidates) in finite.items():
            central_h = h54 if v == 54 else h
            ep, modes = open_window(central_h, t, tminus, np.zeros_like(position), v,
                                    edge_delta, end_projectors)
            overlap = abs(wave[:, candidates].T @ embed @ modes)**2
            coverage = overlap.sum(axis=1)
            winners = overlap.argmax(axis=1)
            for row, j in enumerate(candidates):
                i = winners[row]
                finite_rows.append(dict(cbo_mev=cbo, nz=nz, nb=nb, voltage_mv=v,
                    fd_index_1based=j+1, fd_mev=e[j], pzp_index_1based=i+1, pzp_mev=ep[i],
                    shift_mev=ep[i]-e[j], max_squared_overlap=overlap[row, i],
                    subspace_weight=coverage[row], unique_dominant_match=int(np.count_nonzero(winners == i) == 1)))
    return case_summary


def main():
    bloch_rows, finite_rows, spectrum_rows = [], [], []
    nominal = {cbo: continuum(WIDTHS, np.where(MATERIAL, cbo, P["energy_zero_mev"]))
               for cbo in P["barrier_mev"]}
    results = []
    for case in NATIVE["cases"]:
        results.append(analyze_geometry(case, *nominal[case["cbo_mev"]],
                                        bloch_rows, finite_rows, spectrum_rows))
    write_csv("bloch.csv", bloch_rows)
    write_csv("finite_fd.csv", spectrum_rows)
    write_csv("finite_pzp.csv", finite_rows)
    summary = {
        "core_commit": P["core_commit"], "period_nm": PERIOD, "phase_count": len(PHASES),
        "scales": NATIVE["scales"], "continuum_root_search_steps_mev": [0.025, 0.0125],
        "continuum_search_window_mev": [0, 350], "k_parallel_inverse_nm": 0,
        "finite_periods": PERIOD_COUNT, "finite_potential": "-V_period*z/Lp, central cell [0,Lp)",
        "finite_boundary": "Dirichlet ends, matched projected real-space end diagonals",
        "finite_report_selection": "full FD energy in [-100,170] meV and central-cell probability >=0.10",
        "basis_static_e171_limits": LIMITS,
        "cases": results,
    }
    (HERE / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")


if __name__ == "__main__":
    main()
