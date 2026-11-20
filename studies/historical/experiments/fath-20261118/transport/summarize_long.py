"""Build the completed long-run audit with signed current and separate residual scales."""
import csv
import json
import math
from pathlib import Path
import tomllib

root = Path(__file__).resolve().parent / "native54-long-alpha02"


def toml(path):
    return tomllib.loads(path.read_text())


def measurement(case, markers):
    row = case["last_row"]
    top = max((channel for channel in markers["channels"] if channel["channel"] != "total"),
              key=lambda channel: channel["residual_relative"])
    assert math.isclose(top["residual_relative"], row["r_Σ"], rel_tol=1e-9)
    residual, denominator = top["residual_absolute"], top["residual_scale"]
    assert math.isclose(residual/(denominator+1e-14), row["r_Σ"], rel_tol=1e-9)
    result = {
        "local_map": row["ν"], "sequence_map_without_replay_duplicates": 142 + row["ν"],
        "state_sha256": case["state_sha256"],
        "leading_channel": top["channel"], "component": top["component"],
        "unweighted_absolute_F_dimensionless": residual,
        "unweighted_fresh_F_dimensionless": denominator,
        "unweighted_absolute_F_meV": residual*100.0,
        "unweighted_fresh_F_meV": denominator*100.0,
        "rSigma": row["r_Σ"], "rK": row["r_K"], "rLambda": row["r_λ"],
        "rPSD": row["r_PSD"], "Jplus_A_cm2": row["J"]/1e4,
    }
    return result


history = list(csv.DictReader((root / "history.csv").read_text().splitlines()))
assert [int(row["ν"]) for row in history] == list(range(1, len(history)+1))
primary = toml(root / "summary.toml")
assert primary["execution"] == "complete"
audit = toml(root / "independent-density-audit.toml")
assert audit["state_sha256"] == primary["state_sha256"]
obs = toml(root / "terminal-observables.toml")
observations = []
for index in (128, 256, 512):
    folder = root / f"checkpoint-{index:04d}"
    if not (folder / "summary.toml").is_file():
        continue
    snapshot = toml(folder / "summary.toml")
    assert snapshot["model_identity"] == primary["model_identity"]
    v = measurement(snapshot, toml(folder / "markers.toml"))
    if (folder / "independent-density-audit.toml").is_file():
        data = toml(folder / "independent-density-audit.toml")
        assert data["state_sha256"] == snapshot["state_sha256"]
        v["independent_spectral_sum_F_max"] = data["r_sum_max_unweighted_per_k"]
        v["independent_internal_mean_A_cm2"] = data["independent_bond_J_mean_A_cm2"]
    observations.append(v)
observations.append(measurement(primary,toml(root / "terminal-markers.toml")))
execution = json.loads((root / "execution.json").read_text())
thresholds = {"r_Σ": 1e-8, "r_K": 1e-8, "r_λ": 1e-8, "r_PSD": 1e-10,
              "r_Jchange": 1e-4, "r_population": 1e-4}
jplus, jminus = obs["J_plus_out_A_cm2"], obs["J_minus_out_A_cm2"]
assert math.isclose(jplus, audit["boundary_flux_profiles"]["integrated_A_cm2"][0], rel_tol=1e-10)
assert math.isclose(jminus, audit["boundary_flux_profiles"]["integrated_A_cm2"][1], rel_tol=1e-10)
print(json.dumps({
    "model_identity": primary["model_identity"], "status": primary["status"],
    "scientific_acceptance": primary["scientific_acceptance"],
    "strict_rows": sum(row["strict_row"] == "true" for row in history),
    "local_maps": len(history),
    "per_gate_pass_count": {key: sum(float(row[key]) < rate for row in history)
                            for key, rate in thresholds.items()},
    "checkpoints_and_terminal": observations,
    "terminal_currents": {"Jplus_A_cm2": jplus, "Jminus_out_A_cm2": jminus,
                          "minus_Jminus_out_A_cm2": -jminus,
                          "absolute_boundary_imbalance_A_cm2": abs(jplus+jminus),
                          "boundary_imbalance_relative": obs["boundary_continuity_relative"],
                          "absolute_last_step_Jplus_change_A_cm2":
                              abs(float(history[-1]["J"])-float(history[-2]["J"]))/1e4,
                          "internal_profile_mean_A_cm2": obs["bond_J_average_A_cm2"],
                          "internal_profile_minmax_A_cm2":
                              [obs["bond_J_min_A_cm2"],obs["bond_J_max_A_cm2"]]},
    "terminal_k_E_audit": {"r_sum_max": audit["r_sum_max_unweighted_per_k"],
                            "k_where_r_sum_max": audit["k_at_max_r_sum_nm_inverse"],
                            "occupied_fraction_outside_trust": audit["occupied_sheet_outside_trust"],
                            "occupied_fraction_near_k_max": audit["occupied_sheet_above_95pct_kmax"],
                            "bond_compare_max_error_A_cm2": audit["independent_bond_J_max_error_A_cm2"]},
    "wall_seconds": execution["elapsed_seconds"],
    "peak_GiB": int(execution["cgroup"]["memory.peak"])/1024**3,
    "output_GiB": execution["output_bytes"]/1024**3,
}, ensure_ascii=False, indent=2))
