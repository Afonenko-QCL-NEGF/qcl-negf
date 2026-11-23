#!/usr/bin/env python3
"""Reproduce the fixed-cut audit from the published pre-campaign JSON files."""

import argparse
import csv
import hashlib
import json
import math
import tomllib
from pathlib import Path


CASES = (
    ("7-x9-first", "fath-lo-rank-v843/evidence/fath-A-base-cell.json"),
    ("8-x9-first", "fath-lo-rank-v843/evidence/fath-A-expanded-cell.json"),
    ("7-x9", "fath-v843/evidence/fath-F13-positive-long.json"),
    ("8-x9", "fath-lo-rank-v843/evidence/fath-D-expanded-cell.json"),
    ("7-second", "fath-lo-rank-v843/evidence/fath-D-second-seed.json"),
)
FIXED_NM = {
    "late7": (33.84729166666667, 39.640972222222224),
    "late8": (34.45715277777778, 39.031111111111116),
}


def cut_index(cuts, z):
    index = min(range(len(cuts)), key=lambda i: abs(cuts[i] - z))
    if not math.isclose(cuts[index], z, abs_tol=1e-10):
        raise ValueError(f"No physical cut at {z} nm")
    return index


def partition(cuts, profile, a, b):
    def delta(curve):
        return curve[b] - curve[a]

    current = profile["current_A_cm2"]
    change = delta(current)
    remainder = delta(profile["kinetic_remainder_A_cm2"])
    projection = delta(profile["spatial_projection_gap_A_cm2"])
    collisions = {
        channel: delta(curve)
        for channel, curve in profile["collision_cumulative_A_cm2"].items()
    }
    collisions_sum = math.fsum(collisions.values())
    return {
        "from_nm": cuts[a],
        "to_nm": cuts[b],
        "J_from_A_cm2": current[a],
        "J_to_A_cm2": current[b],
        "delta_J_A_cm2": change,
        "lag_A_cm2": remainder,
        "projection_A_cm2": projection,
        "collisions_A_cm2": collisions,
        "collisions_sum_A_cm2": collisions_sum,
        "closure_A_cm2": change - remainder - projection - collisions_sum,
    }


def balance(cuts, profile, cut_pairs):
    current = profile["current_A_cm2"]
    own_extrema = current.index(min(current)), current.index(max(current))
    differences = [b - a for a, b in zip(current, current[1:])]
    strongest = max(range(len(differences)), key=lambda i: abs(differences[i]))
    return {
        "current": profile["current"],
        "maximum_closure_error_A_cm2": profile["maximum_closure_error_A_cm2"],
        "weighted_rK_Q": profile["weighted_rK_Q"],
        "particle_exchange_A_cm2": profile["particle_exchange_A_cm2"],
        "cut_balances": {
            tag: partition(cuts, profile, a, b)
            for tag, (a, b) in (
                *cut_pairs.items(),
                ("extrema", own_extrema),
                ("seams", (0, len(cuts) - 1)),
                ("largest_cell_jump", (strongest, strongest + 1)),
            )
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("studies", type=Path, help="directory with the two published studies")
    parser.add_argument("output", type=Path, help="output directory for the compact audit")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    device = tomllib.loads((args.studies / "fath-v843/fath-device.toml").read_text())
    records = {
        "material_interfaces_nm": device["interface_positions_nm"],
        "donor_interval_nm": device["donor_interval_nm"],
        "cases": {},
    }
    rows = []
    for label, relative_path in CASES:
        contents = (args.studies / relative_path).read_bytes()
        archive = json.loads(contents)
        cuts = archive.get("current_midpoints_nm", archive.get("cut_coordinates_nm"))
        cut_pairs = {
            tag: tuple(cut_index(cuts, z) for z in ends)
            for tag, ends in FIXED_NM.items()
        }
        selected = archive.get("selected_iteration", len(archive["history"]))
        fresh = archive.get("observation", archive.get("observed"))
        records["cases"][label] = {
            "input": relative_path,
            "sha256": hashlib.sha256(contents).hexdigest(),
            "selected_map": selected,
            "fresh_state": balance(cuts, fresh, cut_pairs),
            "lagged_pair": balance(cuts, archive["lagged"], cut_pairs),
        }
        for row in archive["history"]:
            profile = row["current_profile_A_cm2"]
            spatial = row["spatial"]
            rows.append(
                {
                    "case": label,
                    "map": row.get("step", row.get("iteration")),
                    "rK": row["rK"],
                    "max_rSigma": row["rSigma"],
                    "raw_charge_ratio": row["raw_lambda"],
                    "max_spectral_defect": row["maximum_spectral_defect"],
                    "Jmean_A_cm2": spatial["mean_internal_A_cm2"],
                    "Jmax_deviation_A_cm2": spatial["max_deviation_from_mean_A_cm2"],
                    "Jmin_nm": cuts[profile.index(min(profile))],
                    "Jmax_nm": cuts[profile.index(max(profile))],
                    **{tag + "_delta_A_cm2": profile[b] - profile[a] for tag, (a, b) in cut_pairs.items()},
                }
            )
    with (args.output / "archive-balance.json").open("w") as stream:
        json.dump(records, stream, indent=2, allow_nan=False)
        stream.write("\n")
    with (args.output / "archive-trajectories.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
