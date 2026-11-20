"""Compare the frozen 16-map alpha branches using only their verified ledgers."""
import csv
import json
from pathlib import Path
import statistics
import sys
import tomllib

root = Path(__file__).resolve().parent
a, b = (root / name for name in sys.argv[1:]) if len(sys.argv) == 3 else (
    root / "warm-alpha02-probe", root / "warm-alpha04-probe"
)


def load(path):
    config = tomllib.loads((path / "input.toml").read_text())
    summary = tomllib.loads((path / "summary.toml").read_text())
    assert summary["execution"] == "complete"
    with (path / "history.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    assert [int(row["ν"]) for row in rows] == list(range(1, 17))
    return config, summary, rows


ca, sa, ra = load(a)
cb, sb, rb = load(b)
assert ca["alpha_sigma"] == 0.2 and cb["alpha_sigma"] == 0.4
assert {k: v for k, v in ca.items() if k not in ("alpha_sigma", "name")} == {
    k: v for k, v in cb.items() if k not in ("alpha_sigma", "name")
}
assert sa["model_identity"] == sb["model_identity"]
for metric in ("J", "λ", "r_Σ", "r_K", "r_λ"):
    assert ra[0][metric] == rb[0][metric], f"Different initial replay for {metric}"
keys = ("r_Σ", "r_K", "r_λ")
median_a = {key: statistics.median(float(row[key]) for row in ra[8:]) for key in keys}
median_b = {key: statistics.median(float(row[key]) for row in rb[8:]) for key in keys}
thresholds = tomllib.loads((a / "identity.toml").read_text())["strict_thresholds"]


def physical_failures(rows):
    return [(int(row["ν"]), name)
            for row in rows for name in ("r_PSD", "r_caus", "r_roundoff")
            if not 0 <= float(row[name]) < thresholds[name]]


failures_a, failures_b = physical_failures(ra), physical_failures(rb)
new_physical_failures = sorted(set(failures_b) - set(failures_a))
choose = (
    median_b["r_Σ"] < median_a["r_Σ"] and median_b["r_K"] < median_a["r_K"]
    and median_b["r_λ"] <= 1.10 * median_a["r_λ"] and not new_physical_failures
)
print(json.dumps({
    "warm_checkpoint_parent": ca["warm_attempt"], "model_identity": sa["model_identity"],
    "replay_exact_for_tested_scalars": True,
    "medians_control": median_a, "medians_alpha04": median_b,
    "alpha04_over_alpha02": {key: median_b[key]/median_a[key] for key in keys},
    "new_physical_failures_alpha04": new_physical_failures,
    "continue_alpha04_under_predeclared_rule": choose,
    "control_status": sa["status"], "alpha04_status": sb["status"],
}, indent=2, ensure_ascii=False))
