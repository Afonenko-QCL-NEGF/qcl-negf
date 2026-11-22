#!/usr/bin/env python3
"""Compare the paired Fath and V843 experiment reports at their common inputs."""
import argparse
import json
from pathlib import Path


def read(path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def profile_difference(a, b):
    return [y - x for x, y in zip(a, b, strict=True)]


def maximum_absolute(values):
    return max(map(abs, values))


def profile_summary(row, key):
    obs = row[key]
    return {
        "current": obs["current"],
        "raw_lambda": obs["raw_lambda"],
        "raw_sheet_cm2": obs["raw_sheet_cm2"],
        "temperature_K": obs["equivalent_temperature_K"],
    }


def shared_conditions(rows, fields):
    for field in fields:
        if any(row[field] != rows[0][field] for row in rows):
            raise ValueError(f"paired experiment differs in {field}")


def factorial(directory):
    arms = [read(directory / f"fath-A-{rank}-{lo}.json")
            for rank in ("base", "expanded") for lo in ("cell", "hat")]
    shared_conditions(arms, ("identity", "cut_coordinates_nm", "core", "runner", "maps", "action"))
    if any(row["maps"] != 1 for row in arms):
        raise ValueError("the registered factorial compares the first unmixed image")
    profiles = [row["observation"]["current_A_cm2"] for row in arms]
    means = [row["observation"]["current"]["mean_internal_A_cm2"] for row in arms]
    centered = [[j - mu for j in profile] for mu, profile in zip(means, profiles, strict=True)]
    midpoint = len(profiles[0]) // 2

    def contrasts(values):
        cell, hat, large_cell, large_hat = values
        shift = profile_difference(cell, hat)
        large_shift = profile_difference(large_cell, large_hat)
        grow_cell = profile_difference(cell, large_cell)
        grow_hat = profile_difference(hat, large_hat)
        return {
            "LO_at_baseline_rank": shift,
            "LO_at_expanded_rank": large_shift,
            "rank_at_cell_LO": grow_cell,
            "rank_at_hat_LO": grow_hat,
            "LO_average": [(a + b) / 2 for a, b in zip(shift, large_shift, strict=True)],
            "rank_average": [(a + b) / 2 for a, b in zip(grow_cell, grow_hat, strict=True)],
            "interaction": profile_difference(shift, large_shift),
        }

    def summarize(values):
        return {key: {"maximum_absolute": maximum_absolute(delta), "left": delta[0],
                      "center": delta[midpoint], "right": delta[-1], "profile": delta}
                for key, delta in contrasts(values).items()}

    result = {}
    for arm in arms:
        obs = arm["observation"]
        worst = max(range(len(obs["current_A_cm2"])), key=lambda i:
                    abs(obs["current_A_cm2"][i] - obs["current"]["mean_internal_A_cm2"]))
        result[f'{arm["rank_mode"]}-{arm["lo_mode"]}'] = {
            **profile_summary(arm, "observation"),
            "rK": arm["history"][0]["rK"],
            "rSigma": arm["history"][0]["rSigma"],
            "independent_rK_Q": arm["lagged"]["weighted_rK_Q"],
            "observer_difference_A_cm2": arm["independent_profile_difference_A_cm2"],
            "maximum_defect_cut_nm": arm["cut_coordinates_nm"][worst],
            "LO_cumulative_at_defect_A_cm2": obs["collision_cumulative_A_cm2"]["LO"][worst],
            "projection_cumulative_at_defect_A_cm2": obs["spatial_projection_gap_A_cm2"][worst],
            "kinetic_cumulative_at_defect_A_cm2": obs["kinetic_remainder_A_cm2"][worst],
            "lagged_kinetic_cumulative_at_defect_A_cm2":
                arm["lagged"]["kinetic_remainder_A_cm2"][worst],
        }
    quadrature = [arm["independent_profile_difference_A_cm2"] for arm in arms]
    return {
        "conditions": result,
        "cuts_nm": arms[0]["cut_coordinates_nm"],
        "effects_raw_profile_A_cm2": summarize(profiles),
        "effects_centered_profile_A_cm2": summarize(centered),
        "effects_LO_cumulative_A_cm2": summarize(
            [x["observation"]["collision_cumulative_A_cm2"]["LO"] for x in arms]),
        "effects_projection_cumulative_A_cm2": summarize(
            [x["observation"]["spatial_projection_gap_A_cm2"] for x in arms]),
        "observed_quadrature_effect_envelope_A_cm2": sum(quadrature),
    }


def v843(directory, reference):
    arms = [read(directory / f"v843-selected-{rings}.json") for rings in (5, 9, 17)]
    shared_conditions(arms, ("identity", "seed_sha256", "updates", "core", "runner", "cuts_nm"))
    if arms[0]["updates"] != 47:
        raise ValueError("the selected radial control must replay to the published source")
    saved = read(reference)
    comparisons = {}
    archived_arms = [saved["observed"], saved["paired_controls"]["radial"]["observation"]]
    for arm, archive in zip(arms[:2], archived_arms, strict=True):
        obs = arm["observation"]
        profile_difference_max = maximum_absolute(profile_difference(
            obs["current_A_cm2"], archive["current_A_cm2"]))
        ratio = archive["central_bands"]["fraction"][0] / archive["central_bands"]["fraction"][2]
        temperature_difference = abs(obs["equivalent_temperature_K"] - archive["equivalent_temperature_K"])
        ratio_difference = abs(arm["extractor_over_upper"] - ratio)
        if profile_difference_max > 1e-4 or temperature_difference > 1e-6 or ratio_difference > 1e-7:
            raise ValueError("the replay differs from the published common-source reference")
        comparisons[f'{arm["rings"]}_rings'] = {
            "profile_difference_A_cm2": profile_difference_max,
            "temperature_difference_K": temperature_difference,
            "extractor_over_upper_difference": ratio_difference,
        }
    result = {}
    for arm in arms:
        bands = arm["observation"]["central_bands"]
        fractions = bands["fraction"][:4]
        temperature = sum(n * t for n, t in zip(
            fractions, bands["equivalent_temperature_K"][:4], strict=True)) / sum(fractions)
        result[str(arm["rings"])] = {
            **profile_summary(arm, "observation"),
            "temperature_matched_four_bands_K": temperature,
            "matched_four_band_charge_fraction": sum(fractions),
            "projected_to_physical_charge_ratio": bands["total_sheet_over_physical_sheet"],
            "extractor_over_upper": arm["extractor_over_upper"],
            "observer_difference_A_cm2": arm["observer_max_difference_A_cm2"],
            "rK": arm["summary"]["weighted_rK"],
        }
    differences = {}
    for a, b in zip(arms[:-1], arms[1:], strict=True):
        m, n = a["observation"], b["observation"]
        differences[f'{a["rings"]}_to_{b["rings"]}'] = {
            "maximum_profile_change_A_cm2": maximum_absolute(
                profile_difference(m["current_A_cm2"], n["current_A_cm2"])),
            "mean_change_A_cm2": n["current"]["mean_internal_A_cm2"] - m["current"]["mean_internal_A_cm2"],
            "temperature_change_K": n["equivalent_temperature_K"] - m["equivalent_temperature_K"],
            "extractor_over_upper_change": b["extractor_over_upper"] - a["extractor_over_upper"],
        }
    return {"replay_verified": comparisons, "conditions": result, "radial_steps": differences}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", choices=("fath", "v843"))
    parser.add_argument("results", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    evidence = Path(__file__).resolve().parents[1] / "fath-v843" / "evidence"
    report = factorial(args.results) if args.experiment == "fath" else v843(
        args.results, evidence / "v843-f21.json")
    with args.output.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, indent=2, allow_nan=False)
        stream.write("\n")
