"""Compare equal-size, equal-map-budget cold basis experiments."""
import csv
import json
from pathlib import Path
import statistics
import tomllib

root = Path(__file__).resolve().parent


def load(name):
    attempt = root / name
    def toml(key):
        return tomllib.loads((attempt / key).read_text())
    with (attempt / "history.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    summary = toml("summary.toml")
    assert summary["execution"] == "complete"
    return {
        "path": name, "input": toml("input.toml"), "summary": summary,
        "row": rows, "basis": toml("identity.toml")["effective_basis_localization"],
        "resolved": toml("resolved.toml"), "observables": toml("terminal-observables.toml"),
        "execution": json.loads((attempt / "execution.json").read_text()),
    }


control, trial = load("compact54-pzp7"), load("compact54-bloch7")
control_args, trial_args = control["input"], trial["input"]
keys = set(control_args) | set(trial_args)
assert all(control_args[k] == trial_args[k]
           for k in keys if k != "name" and not k.startswith("basis_"))
assert control["summary"]["device_sha256"] == trial["summary"]["device_sha256"]
assert control["basis"] == "pzp" and trial["basis"] == "bounded_bloch_snapshot_pod"
assert control["summary"]["model_identity"] != trial["summary"]["model_identity"]
assert len(control["row"]) == len(trial["row"]) == 64
for case in (control, trial):
    assert case["execution"]["exit_code"] == 0
    assert case["resolved"]["spectral_window"]["local_spectrum_covered"]
    assert case["resolved"]["scattering_channels"] == control["resolved"]["scattering_channels"]


def summarize(case):
    rows = case["row"]
    metrics = ["r_Σ", "r_K", "r_λ", "r_PSD", "r_caus", "r_roundoff"]
    return {
        "model_identity": case["summary"]["model_identity"], "basis": case["basis"],
        "status": case["summary"]["status"], "quality": case["summary"]["quality"],
        "strict_rows": sum(row["strict_row"] == "true" for row in rows),
        "late_median": {key: statistics.median(float(row[key]) for row in rows[-8:]) for key in metrics},
        "last": {key: float(rows[-1][key]) for key in metrics},
        "terminal_current": {key: case["observables"][key] for key in (
            "J_plus_out_A_cm2", "J_minus_out_A_cm2", "boundary_continuity_relative",
            "bond_J_average_A_cm2", "bond_J_min_A_cm2", "bond_J_max_A_cm2")},
        "elapsed_seconds": case["execution"]["elapsed_seconds"],
        "peak_GiB": int(case["execution"]["cgroup"]["memory.peak"])/1024**3,
    }


print(json.dumps({"diagnostic_only": True, "control": summarize(control), "alternate": summarize(trial)},
                 ensure_ascii=False, indent=2))
