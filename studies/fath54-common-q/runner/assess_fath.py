"""Reduce compact Runner evidence on common residuals and fixed physical cuts."""

import argparse
import json
from itertools import product
from pathlib import Path


def maximum_difference(a, b):
    return max(abs(x - y) for x, y in zip(a, b, strict=True))


def residual_match(a, b):
    return all(
        max(a["row"][key], b["row"][key]) <= 1.25 * min(a["row"][key], b["row"][key])
        for key in ("rK", "rSigma")
    )


def quadrature_error(record):
    uncertainty = record["observation"]["uncertainty"]
    return max(
        uncertainty["GL18_GL20_centered"],
        uncertainty["production_GL20_centered"],
    )


def compare_profiles(a, b):
    x, y = (row["observation"]["GL20"] for row in (a, b))
    return {
        "centered": maximum_difference(x["centered"], y["centered"]),
        "full": maximum_difference(x["profile"], y["profile"]),
        "jump_change": y["delta_segment"] - x["delta_segment"],
        "mean_change": y["mean"] - x["mean"],
        "quadrature": quadrature_error(a) + quadrature_error(b),
    }


def observation_map(records, name):
    return {
        row["step"]: row
        for row in records
        if row.get("observation") and row["name"] == name
    }


def choose_matched_triples(records, names):
    maps = tuple(observation_map(records, name) for name in names)
    same_step = set.intersection(*(set(maps_by_step) for maps_by_step in maps))
    matched = [
        tuple(maps_by_step[step] for maps_by_step in maps)
        for step in sorted(same_step)
        if step >= 16
    ]
    accepted = [
        triple for triple in matched
        if all(residual_match(a, b) for a, b in product(triple, repeat=2))
    ]
    if len(accepted) >= 2:
        return accepted, "same_depth"
    overlapping = [
        triple
        for triple in product(*(list(m.values()) for m in maps))
        if min(x["step"] for x in triple) >= 16
        and all(residual_match(a, b) for a, b in product(triple, repeat=2))
    ]
    overlapping.sort(key=lambda t: (
        max(x["row"]["rK"] for x in t),
        max(x["row"]["rSigma"] for x in t),
    ), reverse=True)
    if not overlapping:
        return [], None
    latest = overlapping[-1]
    preceding = [
        t for t in overlapping
        if all(a["step"] < b["step"] for a, b in zip(t, latest, strict=True))
    ]
    return [*preceding[-1:], latest], "shared_residuals"


def late_differences(records, names, matches):
    if not matches:
        return []
    output = []
    for index, group in enumerate(matches):
        nearby = matches[index-1] if index > 0 else matches[min(index+1, len(matches)-1)]
        contrasts = []
        for i in range(len(group)-1):
            a, b = group[i : i+2]
            current = compare_profiles(a, b)
            drift = None
            if len(matches) > 1:
                drift = sum(
                    maximum_difference(
                        x["observation"]["GL20"]["centered"],
                        y["observation"]["GL20"]["centered"],
                    )
                    for x, y in zip((a, b), nearby[i : i+2], strict=True)
                )
            other = []
            for name, row in zip(names[i : i+2], (a, b), strict=True):
                readings = observation_map(records, "history2_" + name)
                comparable = [value for value in readings.values() if residual_match(row, value)]
                if comparable:
                    candidate = min(
                        comparable,
                        key=lambda r: sum(
                            abs(r["row"][k] - row["row"][k]) / row["row"][k]
                            for k in ("rK", "rSigma")
                        ),
                    )
                    other.append(compare_profiles(row, candidate)["centered"])
            start = sum(other) if len(other) == 2 else None
            interval = None
            if drift is not None and start is not None:
                error = current["quadrature"] + drift + start
                interval = [max(0, current["centered"] - error), current["centered"] + error]
            tolerance = max(1.0, 0.01 * abs(a["observation"]["GL20"]["mean"]))
            contrasts.append(current | {
                "drift": drift, "initial_state": start, "interval": interval,
                "practical_tolerance": tolerance,
                "shape_stable_within_tolerance": interval is not None and interval[1] < tolerance,
            })
        r_k = [x["row"]["rK"] for x in group]
        r_sigma = [x["row"]["rSigma"] for x in group]
        output.append({
            "steps": [x["step"] for x in group], "rK": r_k, "rSigma": r_sigma,
            "rK_ratio": max(r_k) / max(min(r_k), 1e-300),
            "rSigma_ratio": max(r_sigma) / max(min(r_sigma), 1e-300),
            "contrasts": contrasts,
        })
    return output


def sections(records, names):
    results = []
    for name in names:
        maps = observation_map(records, name)
        if not maps:
            continue
        row = maps[max(maps)]
        observed = row["observation"]["GL20"]
        summary = row["row"]
        results.append({
            "name": name, "step": row["step"], "W": row["W"], "Q": row["Q"],
            "rK": summary["rK"], "rSigma": summary["rSigma"],
            "spectral": summary["maximum_spectral_defect"], "lambda": observed["raw_lambda"],
            "charge": observed["raw_charge"], "mean": observed["mean"],
            "max_deviation": observed["max_deviation"], "seams": observed["oriented_seams"],
            "jump": observed["delta_segment"], "fractions": observed["mode_fractions"],
            "fresh_balance": row["observation"]["fresh"]["contrasts"],
            "lagged_balance": row["observation"]["lagged"]["contrasts"],
        })
    return results


def coordinate_contrasts(records):
    analyses = {}
    for original, shared in (("W7_Q21", "W7_common"), ("W8_Q25", "W8_common")):
        a, b = (observation_map(records, name) for name in (original, shared))
        if not b:
            continue
        analyses[original] = [
            {"step": step, "comparable": residual_match(a[step], b[step])}
            | compare_profiles(a[step], b[step])
            for step in sorted(a.keys() & b.keys())
        ]
    arms = [observation_map(records, name) for name in
            ("W7_Q21", "W7_common", "W8_common", "W8_Q25")]
    decomposition = []
    for step in sorted(set.intersection(*(set(arm) for arm in arms))):
        maps = [arm[step] for arm in arms]
        profiles = [record["observation"]["GL20"]["centered"] for record in maps]
        levels = [record["observation"]["GL20"]["delta_segment"] for record in maps]
        closure = max(abs((v1 - v0) + (v2 - v1) + (v3 - v2) - (v3 - v0))
                      for v0, v1, v2, v3 in zip(*profiles, strict=True))
        decomposition.append({
            "step": step,
            "all_residuals_comparable": all(residual_match(a, b) for a, b in product(maps, repeat=2)),
            "section_contributions": [b-a for a, b in zip(levels, levels[1:])],
            "total": levels[-1]-levels[0],
            "centered_profile_closure": closure,
        })
    return {"fixed_rank": analyses, "signed_path": decomposition}


def assess(all_rows):
    records = [row for row in all_rows if row["kind"] == "map"]
    configuration = next(row for row in all_rows if row["kind"] == "configuration")
    available = ["W7_Q21", "W8_Q25", "W7_common", "W8_common", "W9_common"]
    names = (
        available[-3:]
        if configuration["ninth_admitted"]
        else ["W7_common", "W8_common" if observation_map(records, "W8_common") else "W8_Q25"]
    )
    matches, method = choose_matched_triples(records, names)
    differences = late_differences(records, names, matches)
    two = differences[-2:]
    narrowed = len(names) == 3 and len(two) == 2 and all(
        all(c["interval"] is not None for c in m["contrasts"])
        and m["contrasts"][1]["interval"][1] < m["contrasts"][0]["interval"][0]
        for m in two
    )
    return {
        "comparable": method,
        "ranks": names,
        "contrasts": differences,
        "resolved_decrease": narrowed,
        "latest_sections": sections(records, available),
        "coordinate_controls": [r for r in all_rows if r["kind"] == "coordinate_control"],
        "coordinate_contrasts": coordinate_contrasts(records),
        "grid_contrasts": [r for r in all_rows if r["kind"] == "grid_contrast"],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trajectory", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    with args.trajectory.open() as handle:
        rows = [json.loads(line) for line in handle]
    result = json.dumps(assess(rows), indent=2, allow_nan=False)
    if args.out:
        args.out.write_text(result + "\n")
    else:
        print(result)


if __name__ == "__main__":
    main()
