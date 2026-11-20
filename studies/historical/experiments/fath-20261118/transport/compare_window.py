"""Compare the 64-map native experiments after extending the upper energy limit."""
import csv
import json
import math
from pathlib import Path
import statistics
import tomllib

root = Path(__file__).resolve().parent


def retrieve(name):
    out = root / name
    def parse(file):
        return tomllib.loads((out / file).read_text())
    rows = list(csv.DictReader((out / "history.csv").read_text().splitlines()))
    assert [(int(row["outer"]), int(row["ν"])) for row in rows] == [(0, i) for i in range(1, 65)]
    s = parse("summary.toml")
    assert s["execution"] == "complete"
    return {"rows": rows, "obs": parse("terminal-observables.toml"),
            "summary": s, "args": parse("input.toml"),
            "audit": parse("independent-density-audit.toml"),
            "markers": parse("terminal-markers.toml")}


old, new = retrieve("compact54-pzp7"), retrieve("compact54-pzp7-wide-upper")
assert old["summary"]["device_sha256"] == new["summary"]["device_sha256"]
assert all(old["args"][k] == v for k, v in new["args"].items()
           if k not in ("E_max_meV", "NE", "name"))
assert old["args"]["NE"] == 2401 and new["args"]["NE"] == 3151
a, b = [case["audit"]["energy_meV"] for case in (old, new)]
assert math.isclose(a[-1], 560) and math.isclose(b[-1], 860)
assert all(abs(x-y) < 1e-10 for x, y in zip(a,b))
active = [i for i, value in enumerate(a) if -100.0-1e-10 <= value <= 80.0+1e-10]


def brief(case):
    keys = ("r_Σ", "r_K", "r_λ")
    audit = case["audit"]
    energy = audit["energy_meV"]
    coverage = {}
    for field in ("occupied_energy_bin_integral_dimensionless", "spectral_trace_bin_integral_dimensionless"):
        values = audit[field]
        total = math.fsum(values)
        coverage[field] = {
            "whole_grid_sum": total,
            "uppermost_252_7meV_fraction": math.fsum(v for e, v in zip(energy, values)
                                                    if e > energy[-1]-252.7)/total,
            "common_slice_307_3_to_560_fraction": math.fsum(v for e, v in zip(energy, values)
                                                           if 307.3 < e <= 560.0+1e-10)/total,
            "above_560_meV_fraction": math.fsum(v for e, v in zip(energy, values)
                                               if e > 560.0+1e-10)/total,
        }
    max_channel = max((row for row in case["markers"]["channels"] if row["channel"] != "total"),
                      key=lambda row: row["residual_relative"])
    return {
        "status": case["summary"]["status"],
        "strict_rows": sum(row["strict_row"] == "true" for row in case["rows"]),
        "last": {key: float(case["rows"][-1][key]) for key in keys},
        "late_median": {key: statistics.median(float(row[key]) for row in case["rows"][-8:]) for key in keys},
        "largest_fresh_component": max_channel,
        "terminal_observables": {key: case["obs"][key] for key in (
            "J_plus_out_A_cm2", "J_minus_out_A_cm2", "boundary_continuity_relative",
            "bond_J_average_A_cm2", "bond_J_min_A_cm2", "bond_J_max_A_cm2")},
        "full_spectral_sum_residual": audit["r_sum_max_unweighted_per_k"],
        "energy_support_diagnostics": coverage,
    }


shape = {}
for field in ("occupied_energy_bin_integral_dimensionless", "spectral_trace_bin_integral_dimensionless"):
    x, y = [case["audit"][field] for case in (old,new)]
    scale = math.fsum(x[i] for i in active)
    shape[field] = {"old_active_mass": scale,
                    "new_active_mass": math.fsum(y[i] for i in active),
                    "active_relative_L1_using_control": math.fsum(abs(x[i]-y[i]) for i in active)/scale}
print(json.dumps({"cold_equal_maps": 64, "diagnostic_only": True,
                  "control": brief(old), "upper_expanded": brief(new),
                  "common_active_interval_meV": [-100,80], "active_shapes": shape}, ensure_ascii=False, indent=2))
