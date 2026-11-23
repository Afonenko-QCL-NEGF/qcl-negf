#!/usr/bin/env python3
"""Compact comparison of freshly evaluated map and independent-observer records."""
import argparse
import csv
import json
from pathlib import Path


def load(path):
    if not path.exists():
        return []
    rows = []
    for line in path.read_text().splitlines(keepends=True):
        if line.endswith("\n"):
            rows.append(json.loads(line))
    return rows


def metrics(row, cuts):
    spatial = row["spatial"]
    profile = row["current_profile_A_cm2"]
    i0 = min(range(len(cuts)), key=lambda i: abs(cuts[i] - 33.84729166666667))
    i1 = min(range(len(cuts)), key=lambda i: abs(cuts[i] - 39.640972222222224))
    lo, hi = spatial["full_range_A_cm2"]
    return {
        "step": row.get("step", row.get("fine_step")),
        "arm": row.get("arm", "K25-picard035"),
        "rK": row["rK"],
        "rSigma": row["rSigma"],
        "raw_lambda_minus_one": row["raw_lambda"] - 1.0,
        "max_spectral_defect": row["maximum_spectral_defect"],
        "J_mean_A_cm2": spatial["mean_internal_A_cm2"],
        "J_min_A_cm2": lo,
        "J_max_A_cm2": hi,
        "J_deviation_A_cm2": spatial["max_deviation_from_mean_A_cm2"],
        "J_fixed_delta_A_cm2": profile[i1] - profile[i0],
        "J_left_out_A_cm2": spatial["outward_A_cm2"][0],
        "J_right_out_A_cm2": spatial["outward_A_cm2"][1],
        "strict_confirmations": row.get("confirmations", row.get("strict_confirmations")),
        "elapsed_s": row.get("elapsed_s"),
    }


def select(rows):
    if not rows:
        return []
    steps = {1, 8, 24, 40, 48, 56, 64, 72, 80, 96, rows[-1]["step"]}
    return [row for row in rows if row["step"] in steps]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", type=Path)
    parser.add_argument("--csv", type=Path)
    args = parser.parse_args()
    traces = []
    for label in ("primary7", "expanded8"):
        all_rows = load(args.runs / (label + ".jsonl"))
        if not all_rows:
            continue
        cuts = all_rows[0]["cuts"]
        maps = [metrics(row, cuts) for row in all_rows if row["kind"] == "map"]
        compare = [metrics(row, cuts) for row in all_rows if row["kind"] == "comparison"]
        balance = [row for row in all_rows if row["kind"] == "balance"]
        for row in select(maps):
            border = row["J_deviation_A_cm2"]
            print(label, row["step"], row["arm"], f'rK={row["rK"]:.6g}',
                  f'rSigma={row["rSigma"]:.6g}', f'dlambda={row["raw_lambda_minus_one"]:.4g}',
                  f'J={row["J_mean_A_cm2"]:.6g}', f'dev={border:.6g}',
                  f'delta={row["J_fixed_delta_A_cm2"]:.6g}')
        for row in balance:
            result = row["result"]
            fixed = result["lagged"]["contrasts"]["late7"]
            print(label, "balance", row["step"],
                  f'rK_Q={result["lagged"]["weighted_rK_Q"]:.6g}',
                  f'independent dJ={result["independent_profile_difference_A_cm2"]:.6g}',
                  f'delta={fixed["delta_J_A_cm2"]:.6g}', f'lag={fixed["source_lag_A_cm2"]:.6g}',
                  f'projection={fixed["projection_A_cm2"]:.6g}',
                  f'collision={fixed["collision_sum_A_cm2"]:.6g}')
        traces.extend({"arm_id": label, **row} for row in (maps + compare))
    fine_path = args.runs / "primary7.jsonl.fine.jsonl"
    if fine_path.exists():
        fine = json.loads(fine_path.read_text())
        for row in fine.get("history", []):
            trace = metrics(row, fine["cuts_nm"])
            traces.append({"arm_id": "radial25", **trace})
            print("radial25", trace["step"], f'rK={trace["rK"]:.6g}',
                  f'dev={trace["J_deviation_A_cm2"]:.6g}', fine["stage"])
    if args.csv and traces:
        with args.csv.open("w", newline="") as output:
            writer = csv.DictWriter(output, fieldnames=list(traces[0]))
            writer.writeheader()
            writer.writerows(traces)


if __name__ == "__main__":
    main()
