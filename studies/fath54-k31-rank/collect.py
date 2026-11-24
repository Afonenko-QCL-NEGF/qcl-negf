"""Audit compact Fath K31 measurements and export current profiles."""

import argparse
import csv
import json
import math
import re
from pathlib import Path


CHANNELS = ("LO", "acoustic", "impurity", "IFR", "alloy")
CROSSINGS = ("nearest_bond", "longer_within_period", "longer_between_periods")
RSS = re.compile(r'("maxrss_bytes":)0x([0-9a-f]+)(?=[,}])')


def canonical_lines(path):
    """Translate the Runner's UInt display for the memory counter into JSON."""
    data = path.read_text()
    # A running process can be appending its next record. The record becomes
    # available to the auditor only after its newline has been flushed.
    return [RSS.sub(lambda m: m[1] + str(int(m[2], 16)), line)
            for line in data.split("\n")[:-1]]


def widths(cuts):
    return [(b - a) / 2 for a, b in zip(cuts, cuts[2:])]


def weighted_mean(profile, measure):
    return math.fsum(j * w for j, w in zip(profile[1:-1], measure, strict=True)) / math.fsum(measure)


def check_balance(balance, size, tolerance=1e-8):
    current = balance["current_A_cm2"]
    projected = balance["projected_current_A_cm2"]
    crossings = balance["projected_crossings_A_cm2"]
    channels = balance["collision_cumulative_A_cm2"]
    kinetic = balance["kinetic_remainder_A_cm2"]
    gap = balance["spatial_projection_gap_A_cm2"]
    assert set(channels) == set(CHANNELS)
    assert set(crossings) == set(CROSSINGS)
    for curve in (current, projected, kinetic, gap, *channels.values(), *crossings.values()):
        assert len(curve) == size and all(math.isfinite(value) for value in curve)
    assert max(abs(projected[i] - math.fsum(crossings[k][i] for k in CROSSINGS))
               for i in range(size)) < tolerance
    assert max(abs(current[i] - current[0] - projected[i] + projected[0] - gap[i])
               for i in range(size)) < tolerance
    closure = [
        current[i] - current[i-1] - (kinetic[i] - kinetic[i-1]) - (gap[i] - gap[i-1])
        - math.fsum(channels[k][i] - channels[k][i-1] for k in CHANNELS)
        for i in range(1, size)
    ]
    error = max(map(abs, closure))
    assert math.isclose(error, balance["maximum_closure_error_A_cm2"], abs_tol=tolerance)
    return error


def compare(seven, eight, seven_map, eight_map):
    a, b = [m["GL20"] for m in (seven, eight)]
    ratios = {
        key: max(seven_map[key], eight_map[key]) / min(seven_map[key], eight_map[key])
        for key in ("rK", "rSigma")
    }
    lambda_difference = b["raw_lambda"] - a["raw_lambda"]
    charge_difference = b["raw_charge"] - a["raw_charge"]
    uncertainties = [m["uncertainty"] for m in (seven, eight)]
    uncertainty = math.fsum(max(u["GL18_GL20_centered"], u["production_GL20_centered"])
                            for u in uncertainties)
    difference = max(abs(y - x) for x, y in zip(a["centered"], b["centered"], strict=True))
    return dict(
        ratios=ratios,
        within_ratio_1p25=max(ratios.values()) <= 1.25,
        mean_difference_A_cm2=b["mean"] - a["mean"],
        max_centered_difference_A_cm2=difference,
        centered_numerical_uncertainty_A_cm2=uncertainty,
        fixed_jump_difference_A_cm2=b["delta_segment"] - a["delta_segment"],
        charge_difference_cm2=charge_difference,
        lambda_difference=lambda_difference,
        possible_normalization_effect=abs(charge_difference) > 3e8 or abs(lambda_difference) > 0.01,
        contrasts={stage: {f"Q{rank}": obs[stage]["contrasts"]
                           for rank, obs in ((21, seven), (25, eight))}
                   for stage in ("fresh", "lagged")},
    )


def check_controls(records, maps, observations):
    results = {}
    updates = {}
    second_maps = {}
    second_observations = {}
    for r in records:
        kind = r["kind"]
        if kind == "update_control":
            key = r["branch_step"], r["rank"], r["alpha"]
            updates.setdefault(key, []).append(r)
        elif kind == "update_assessment":
            step = r["branch_step"]
            for arm in r["comparisons"]:
                rank = arm["rank"]
                mixed, pure = (updates[step, rank, a] for a in (0.35, 1.0))
                for rows in (mixed, pure):
                    assert [x["forward_step"] for x in rows] == list(range(1, 5))
                    assert all(x["common_input_sha"] == observations[rank, step]["input_sha"] and
                               x["common_image_sha"] == observations[rank, step]["fresh_sha"]
                               for x in rows)
                base = maps[rank, step]
                m, p = mixed[-1]["row"], pure[-1]["row"]
                adopted = (all(p[k] <= 0.75 * min(m[k], base[k]) for k in ("rK", "rSigma")) and
                           abs(p["fixed_segment_A_cm2"]) < abs(base["fixed_segment_A_cm2"]) - 0.1)
                assert adopted == arm["pure_improves"]
            assert r["adopt_pure"] == all(x["pure_improves"] for x in r["comparisons"])
            results["update"] = r
        elif kind == "unitary_control":
            result = r["result"]
            ref = observations[8, r["step"]]
            assert result["input_sha"] == ref["input_sha"] and result["image_sha"] == ref["fresh_sha"]
            assert result["passes"] == (result["first_difference"] is None)
            results["unitary"] = {"step": r["step"], "passes": result["passes"],
                                  "first_difference": result["first_difference"],
                                  "delta": result["delta"]}
        elif kind == "LO_operator_control":
            result = r["result"]
            assert result["common_G_source_sha"] == observations[8, r["step"]]["fresh_sha"]
            for ring in result["control"]:
                full, projected = ring["full"], ring["projected_lo"]
                assert abs(ring["independent_error"]) < 1e-7
                assert max(full["maximum_closure_error_A_cm2"],
                           projected["maximum_closure_error_A_cm2"]) < 1e-7
                assert math.isclose(ring["delta"], full["contrasts"]["late7"]["total_A_cm2"]
                                    - projected["contrasts"]["late7"]["total_A_cm2"], abs_tol=1e-9)
            results["LO_operator"] = {"step": r["step"], "rings": [x["k"] for x in result["control"]]}
        elif kind == "LO_golden_rule":
            result = r["result"]
            for width in result["rates"]:
                e, a = width["emission"], width["absorption"]
                assert min(e["observed"], e["reference"], a["observed"], a["reference"]) >= 0
                assert math.isclose(a["observed"]/e["observed"], width["observed_detailed_ratio"])
                assert math.isclose(a["reference"]/e["reference"], result["expected_bose_ratio"])
            results["LO_golden_rule"] = {"step": r["step"], "ring": result["ring"],
                                         "rates": result["rates"]}
        elif kind == "second_history":
            second_maps[r["rank"], r["step"]] = r
        elif kind == "second_history_GL20":
            second_observations[r["rank"], r["step"]] = r["observation"]
            for stage in ("fresh", "lagged"):
                check_balance(r["observation"][stage], 145)
        elif kind == "completed" and r["reason"] == "primary_three_fresh_confirmations":
            for arm in r["agreement"]:
                rank, step = arm["rank"], arm["second_step"]
                assert arm["confirmations"] == second_maps[rank, step]["strict_confirmations"]
                repeat = second_observations[rank, step]
                a, b = [m["GL20"]["profile"] for m in (observations[rank, r["step"]], repeat)]
                assert math.isclose(arm["difference"], max(abs(x-y) for x, y in zip(a, b, strict=True)))
            assert r["reproduced"] == all(x["reproduced"] for x in r["agreement"])
            results["independent_history"] = r["agreement"]
    return results


def audit(path, emit):
    lines = canonical_lines(path)
    records = [json.loads(line) for line in lines]
    config = records[0]
    assert config["kind"] == "configuration"
    assert config["replay"]["input_matches"] and config["replay"]["image_matches"]
    cuts = config["cuts"]
    assert len(cuts) == 145 and all(b > a for a, b in zip(cuts, cuts[1:]))
    measure = widths(cuts)
    maps, observations, closures = {}, {}, {}
    for record in records[1:]:
        kind = record["kind"]
        if kind == "map":
            key = record["rank"], record["step"]
            assert key not in maps
            row = record["row"]
            profile = row["current_profile_A_cm2"]
            mean = weighted_mean(profile, measure)
            assert len(profile) == len(cuts)
            assert math.isclose(mean, row["spatial"]["mean_internal_A_cm2"], abs_tol=1e-9)
            assert math.isclose(max(abs(j - mean) for j in profile),
                                row["spatial"]["max_deviation_from_mean_A_cm2"], abs_tol=1e-9)
            assert all(math.isclose(j - mean, centered, abs_tol=1e-9)
                       for j, centered in zip(profile, row["centered_A_cm2"], strict=True))
            assert row["oriented_seams_A_cm2"] == [profile[0], profile[-1]]
            maps[key] = row
        elif kind == "GL20":
            rank, step = record["rank"], record["step"]
            observation = record["observation"]
            observations[rank, step] = observation
            closures[f"{rank}/{step}"] = {stage: check_balance(observation[stage], len(cuts))
                                         for stage in ("fresh", "lagged")}
            assert observation["uncertainty"]["independent_accumulation"] < 1e-6
    stages = sorted({step for rank, step in observations if (15-rank, step) in observations})
    same_steps = {step: compare(observations[7, step], observations[8, step],
                                maps[7, step], maps[8, step]) for step in stages}
    selected = {}
    assessment = next((r for r in reversed(records) if r["kind"] == "assessment"), None)
    if assessment is not None:
        for tier in assessment["matched"]:
            best = tier["best"]
            if best is not None:
                a, b = best["steps"]
                selected[tier["fraction"]] = dict(
                    best=best,
                    **compare(observations[7, a], observations[8, b], maps[7, a], maps[8, b]),
                )
    completion = next((r for r in reversed(records) if r["kind"] == "completed"), None)
    if completion is not None:
        assert all((rank, completion["step"]) in observations for rank in (7, 8))
        for rank in (7, 8):
            assert [step for rr, step in maps if rr == rank] == list(range(1, completion["step"]+1))
    result = dict(depth={rank: max((n for r, n in maps if r == rank), default=0) for rank in (7, 8)},
                  maximum_checked_closure_A_cm2=max((v for c in closures.values() for v in c.values()),
                                                   default=None),
                  closures=closures, selected=selected, same_steps=same_steps, completion=completion,
                  controls=check_controls(records, maps, observations))
    if emit:
        emit.mkdir(parents=True, exist_ok=True)
        (emit / "trajectory.jsonl").write_text("\n".join(lines)+"\n")
        (emit / "comparisons.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
        with (emit / "profiles.csv").open("w", newline="") as file:
            csv_out = csv.writer(file, lineterminator="\n")
            csv_out.writerow(("rank", "fresh_map", "section_nm", "J_native_A_cm2",
                              "centered_native_A_cm2", "J_GL20_A_cm2", "centered_GL20_A_cm2"))
            for (rank, step), row in maps.items():
                obs = observations.get((rank, step), {}).get("GL20")
                curves = [row["current_profile_A_cm2"], row["centered_A_cm2"]]
                curves.extend((obs["profile"], obs["centered"]) if obs else [[None] * len(cuts)] * 2)
                csv_out.writerows((rank, step, *cell) for cell in zip(cuts, *curves, strict=True))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trajectory", type=Path)
    parser.add_argument("--emit", type=Path)
    args = parser.parse_args()
    summary = audit(args.trajectory, args.emit)
    print(json.dumps({key: summary[key] for key in
                      ("depth", "maximum_checked_closure_A_cm2", "completion")}, indent=2))
