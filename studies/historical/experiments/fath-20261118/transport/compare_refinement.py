"""Compare all recomputed cold energy grids at a common iteration and momentum grid."""
import csv
from hashlib import sha256
import json
import math
from pathlib import Path
import statistics
import tomllib

root = Path(__file__).resolve().parent
identities = {0.4: "compact54-pzp7", 0.2: "compact54-pzp7-de020", 0.1: "compact54-pzp7-de010"}
metrics = ("r_Σ", "r_K", "r_λ", "r_PSD", "r_caus", "r_roundoff", "r_Jchange", "r_population")
cold_config = tomllib.loads((root / identities[0.4] / "input.toml").read_text())
active_k = 0.375


def load(step, name):
    attempt = root / name
    def read(file):
        return tomllib.loads((attempt / file).read_text())
    args = read("input.toml")
    assert {k: v for k, v in args.items() if k not in ("name", "NE", "hard_seconds")} == {
        k: v for k, v in cold_config.items() if k not in ("name", "NE", "hard_seconds")
    }
    assert (args["E_max_meV"]-args["E_min_meV"])/(args["NE"]-1) == step
    with (attempt / "history.csv").open() as stream:
        history = list(csv.DictReader(stream))
    assert [(int(row["outer"]), int(row["ν"])) for row in history] == [(0, n) for n in range(1, 65)]
    summary = read("summary.toml")
    audit = read("energy-refinement-audit.toml")
    markers = read("terminal-markers.toml")
    identity, resolved = read("identity.toml"), read("resolved.toml")
    assert sha256((attempt / "run.jl").read_bytes()).hexdigest() == identity["driver_sha256"]
    assert sha256((attempt / "input.toml").read_bytes()).hexdigest() == identity["case_sha256"]
    assert audit["state_sha256"] == summary["state_sha256"] and audit["model_sha256"] == summary["model_sha256"]
    m = min(range(args["Nk"]), key=lambda i: abs(audit["k_nm_inverse"][i]-active_k))
    assert math.isclose(audit["k_nm_inverse"][m],active_k,rel_tol=1e-13)
    flux = audit["boundary_flux_profiles"]
    return {"step": step, "id": name, "r": history, "summary": summary, "a": audit, "m": m,
            "J_E": flux["signed_integrated_A_cm2_by_energy"], "J_k": flux["signed_integrated_A_cm2_by_k"],
            "identity": identity, "resolved": resolved, "markers": markers,
            "execution": json.loads((attempt / "execution.json").read_text())}


cases = [load(step, name) for step, name in identities.items()]
assert len({case["summary"]["model_identity"] for case in cases}) == 3
assert len({case["summary"]["device_sha256"] for case in cases}) == 1
assert all(case["a"]["k_nm_inverse"] == cases[0]["a"]["k_nm_inverse"] for case in cases)
for key in ("algorithm", "strict_thresholds", "core_commit", "core_tree", "manifest_sha256"):
    assert all(case["identity"][key] == cases[0]["identity"][key] for case in cases)
for key in ("basis_sha256", "scattering_channels", "electron_electron", "dark"):
    assert all(case["resolved"][key] == cases[0]["resolved"][key] for case in cases)
assert all(case["execution"]["exit_code"] == 0 for case in cases)


def binned_flux(nodal_mass, step):
    """Distribute each nodal interior weight half to either adjacent physical bin boundary."""
    binsize = round(4.0/step)
    last = len(nodal_mass)-1
    assert last % binsize == 0
    return [
        math.fsum(nodal_mass[left+1:right])
        + nodal_mass[left] * (1.0 if left == 0 else 0.5)
        + nodal_mass[right] * (1.0 if right == last else 0.5)
        for left, right in zip(range(0,last,binsize), range(binsize,last+1,binsize))
    ]


def diff_ratio(x, y):
    return math.fsum(abs(a-b) for a, b in zip(x,y)) / math.fsum(abs(a) for a in x)


def summarize(case):
    audit, m = case["a"], case["m"]
    history, terminal = case["r"], case["summary"]
    eig = audit["spectral_sum_eigenvalues_per_k"][m]
    max_index = max(range(len(audit["k_nm_inverse"])),
                    key=lambda i: audit["full_window_spectral_residual_per_k"][i])
    j_bins = [binned_flux(series,case["step"]) for series in case["J_E"]]
    base_bins = [binned_flux(series,cases[0]["step"]) for series in cases[0]["J_E"]]
    tot = audit["boundary_flux_profiles"]["integrated_A_cm2"]
    assert all(math.isclose(math.fsum(bins), current, rel_tol=1e-10, abs_tol=1e-9)
               for bins,current in zip(j_bins,tot))
    assert all(math.isclose(math.fsum(bins), current, rel_tol=1e-10, abs_tol=1e-9)
               for bins,current in zip(case["J_k"],tot))
    assert math.isclose(tot[0],terminal["last_row"]["J"]/1e4,rel_tol=1e-10)
    markers = case["markers"]
    return {
        "case": case["id"], "status": terminal["status"], "device_sha256": terminal["device_sha256"],
        "state_sha256": terminal["state_sha256"], "model_sha256": terminal["model_sha256"],
        "dE_meV": case["step"], "strict_rows": sum(row["strict_row"] == "true" for row in history),
        "last": {key: float(history[-1][key]) for key in metrics},
        "maximal_r_PSD": max(float(row["r_PSD"]) for row in history),
        "medians_last_eight": {key: statistics.median(float(row[key]) for row in history[-8:]) for key in metrics},
        "worst_k_nm_inverse": audit["k_nm_inverse"][max_index],
        "r_sum_max": audit["r_sum_max_unweighted_per_k"],
        "fixed_k_0_375": {
            "W_eigenvalues": eig, "W_trace": math.fsum(eig),
            "r_sum": audit["full_window_spectral_residual_per_k"][m],
            "excess": audit["spectral_sum_excess_F_over_sqrtNb_per_k"][m],
            "deficit": audit["spectral_sum_deficit_F_over_sqrtNb_per_k"][m],
            "Q_radial_bin_m_minus_2": audit["occupied_sheet_each_radial_bin_m_minus_2"][m],
            "signed_boundary_flux_bin_A_cm2": [side[m] for side in case["J_k"]],
        },
        "measured_shift_edge_fractions": {name: markers[name] for name in (
            "field_boundary_occupied_fraction","field_boundary_spectral_fraction",
            "lo_boundary_occupied_fraction","lo_boundary_spectral_fraction")},
        "occupied_outside_trust_and_k_edge": [
            audit["occupied_sheet_outside_trust"], audit["occupied_sheet_above_95pct_kmax"]],
        "J_plus_out_A_cm2": tot[0], "J_minus_out_A_cm2": tot[1],
        "J_boundary_continuity_relative": terminal["terminal_boundary_continuity_relative"],
        "internal_profile_mean_A_cm2": audit["independent_bond_J_mean_A_cm2"],
        "internal_profile_minmax_A_cm2": [audit["independent_bond_J_min_A_cm2"],audit["independent_bond_J_max_A_cm2"]],
        "boundary_integrated_signed_e_bins_A_cm2_4meV": j_bins,
        "boundary_integrated_signed_k_bins_A_cm2": case["J_k"],
        "boundary_E_binned_L1_against_control": [diff_ratio(x,y) for x,y in zip(base_bins,j_bins)],
        "boundary_E_active_binned_L1_against_control": [
            diff_ratio(x[75:120],y[75:120]) for x,y in zip(base_bins,j_bins)],
        "boundary_k_binned_L1_against_control": [diff_ratio(x,y) for x,y in zip(cases[0]["J_k"],case["J_k"])],
        "elapsed_seconds": case["execution"]["elapsed_seconds"],
        "peak_memory_GiB": int(case["execution"]["cgroup"]["memory.peak"])/1024**3,
    }


results = [summarize(case) for case in cases]
print(json.dumps({"matched_completed_maps": 64,
                  "strict_validation": all(result["strict_rows"] > 0 and result["r_sum_max"] <= 0.001
                                           for result in results),
                  "geometry": "Fathololoumi reconstruction CBO149, all five local kernels, no e-e",
                  "basis_sha256": cases[0]["resolved"]["basis_sha256"],
                  "core_commit": cases[0]["identity"]["core_commit"],
                  "manifest_sha256": cases[0]["identity"]["manifest_sha256"],
                  "selected_k_nm_inverse": active_k, "common_E_bin_width_meV": 4.0,
                  "active_E_meV": [-100.0,80.0], "common_k_nm_inverse": cases[0]["a"]["k_nm_inverse"],
                  "results": results}, ensure_ascii=False, indent=2))
