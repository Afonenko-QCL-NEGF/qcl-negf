"""Summarize one transport attempt with an explicit solver/physics status split."""
import argparse
import collections
import csv
from pathlib import Path
import json
import math
import re
import statistics
import tomllib

parser = argparse.ArgumentParser()
parser.add_argument("attempt", type=Path)
args = parser.parse_args()
root = args.attempt


def optional_file(name, load):
    path = root / name
    return load(path.read_text()) if path.exists() else None


def scalar(key, row):
    value = float(row[key])
    return value if math.isfinite(value) else str(value)


history = optional_file("history.csv", lambda data: list(csv.DictReader(data.splitlines()))) or []
columns = ("ν", "outer", "J", "r_Σ", "r_K", "r_λ", "r_D", "r_A", "r_PSD", "r_caus",
           "r_roundoff", "r_Jchange", "r_population", "limiting_ratio")
summary = optional_file("summary.toml", tomllib.loads)
observables = optional_file("terminal-observables.toml", tomllib.loads)
marks = optional_file("terminal-markers.toml", tomllib.loads)
execution = optional_file("execution.json", json.loads)
out = {
    "attempt": root.name, "status": summary["status"] if summary and "status" in summary else "unresolved",
    "quality": summary.get("quality") if summary else None,
    "scientific_acceptance": summary.get("scientific_acceptance", False) if summary else False,
    "maps_recorded": len(history), "strict_rows": sum(row["strict_row"] == "true" for row in history),
    "identity": optional_file("identity.toml", tomllib.loads),
    "resolved": optional_file("resolved.toml", tomllib.loads),
}
if summary and summary.get("error"):
    out["exception"] = summary["error"].splitlines()[0]
if history:
    out["first"] = {key: scalar(key, history[0]) for key in columns}
    out["last"] = {key: scalar(key, history[-1]) for key in columns}
    out["last"]["limiting_metric"] = history[-1]["limiting_metric"]
    out["last"]["J_plus_A_cm2"] = float(history[-1]["J"]) / 1e4
    out["best_each_independently"] = {}
    for key in ("r_Σ", "r_K", "r_λ", "r_Jchange", "r_population"):
        valid = [row for row in history if math.isfinite(float(row[key]))]
        if not valid:
            continue
        best = min(valid, key=lambda row: float(row[key]))
        out["best_each_independently"][key] = {"row": int(best["ν"]), "value": float(best[key])}
    if len(history) >= 16:
        recent = history[-16:]
        out["last_16_scalar_span"] = {
            key: [min(float(row[key]) for row in recent), max(float(row[key]) for row in recent)]
            for key in ("J", "r_Σ", "r_K", "r_λ")
        }
if observables:
    keys = ("J_plus_out_A_cm2", "J_minus_out_A_cm2", "boundary_continuity_relative",
            "bond_J_average_A_cm2", "bond_J_min_A_cm2", "bond_J_max_A_cm2",
            "sheet_trace_m_minus_2", "signed_particle_relative", "mixed_power_balance_relative")
    out["terminal_observables"] = {key: observables[key] for key in keys}
if marks:
    ordered = sorted(marks["channels"], key=lambda row: row["residual_relative"], reverse=True)
    out["largest_fresh_channels"] = [row for row in ordered if row["channel"] != "total"][:6]
    for key in ("sampled_gamma_over_dE_q10", "sampled_gamma_over_dE_q50", "sampled_gamma_over_dE_q90",
                "sampled_spectral_weight_underresolved", "lo_boundary_occupied_fraction",
                "lo_boundary_spectral_fraction", "field_boundary_occupied_fraction",
                "field_boundary_spectral_fraction"):
        value = marks.get(key)
        if value is not None:
            out[key] = value if math.isfinite(value) else str(value)
if execution:
    out["elapsed_seconds"] = execution["elapsed_seconds"]
    out["output_bytes"] = execution["output_bytes"]
    out["exit_code"] = execution["exit_code"]
    out["memory_peak_GiB"] = int(execution["cgroup"]["memory.peak"]) / 1024**3
    out["memory_events"] = execution["cgroup"]["memory.events"]
pattern = re.compile(
    r'^SolverEvent\(:phase_end, :scba, "([^"]+)", :completed, (\d+), .*?'
    r'SolverMetric\(:duration_seconds, ([0-9.eE+-]+), "s"\)'
)
if (root / "phases.log").is_file():
    times = collections.defaultdict(list)
    with (root / "phases.log").open() as stream:
        for line in stream:
            if match := pattern.search(line):
                label, index, elapsed = match.groups()
                if int(index) > 3:
                    times[label].append(float(elapsed))
    out["phase_median_after_warmup_seconds"] = {
        label: statistics.median(samples) for label, samples in sorted(times.items())
    }
print(json.dumps(out, ensure_ascii=False, indent=2, allow_nan=False))
