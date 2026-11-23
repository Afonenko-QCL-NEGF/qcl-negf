#!/usr/bin/env python3
"""Build concise reproducible evidence from the nightly run directory."""
import argparse
import csv
import json
import math
from pathlib import Path

from summarize import load, metrics


def write_json(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def profile_diff(left, right):
    delta = [a-b for a, b in zip(left["current_profile_A_cm2"],
                                right["current_profile_A_cm2"], strict=True)]
    mean_offset = left["spatial"]["mean_internal_A_cm2"]-right["spatial"]["mean_internal_A_cm2"]
    return {
        "offset_of_means_A_cm2": mean_offset,
        "max_absolute_A_cm2": max(abs(x) for x in delta),
        "max_centered_A_cm2": max(abs(x-mean_offset) for x in delta),
    }


def matched(left, right):
    """Use only the late history, minimizing the largest log-residual mismatch."""
    eligible_left = [row for row in left if row["step"] >= 40]
    eligible_right = [row for row in right if row["step"] >= 40]
    if not eligible_left or not eligible_right:
        return None
    def key(pair):
        a,b = pair
        mismatch = max(abs(math.log(max(1e-300, a[name])/max(1e-300, b[name])))
                       for name in ("rK", "rSigma"))
        qualified = mismatch <= math.log(1.25)
        if qualified:
            return 0, max(a["rK"],b["rK"]), mismatch
        return 1, mismatch, max(a["rK"],b["rK"])
    return min(((a,b) for a in eligible_left for b in eligible_right), key=key)


def residual_match(a,b):
    ratios = {name:max(a[name],b[name])/max(1e-300,min(a[name],b[name]))
              for name in ("rK","rSigma")}
    return {"ratios":ratios,"within_ratio_1p25":max(ratios.values())<=1.25,
            "same_mixing":a.get("arm","picard035")==b.get("arm","picard035")}


def balance_row(row):
    if row is None:
        return None
    result = row["result"]
    lag = result["lagged"]
    obs = result["observed"]
    fixed = lag["contrasts"]["late7"]
    cuts = result["cut_coordinates_nm"]
    lo = result.get("lo_localization")
    if lo and "split" in lo:
        lo = dict(lo, split={"rings": [
            {name:ring[name] for name in ("ring","radial_weight","maximum_closure_error_A_cm2","contrasts")}
            for ring in lo["split"]["rings"]]})
    i,j = cuts.index(fixed["from_nm"]), cuts.index(fixed["to_nm"])
    biggest = max(range(len(cuts)-1),
                  key=lambda k:abs(lag["current_A_cm2"][k+1]-lag["current_A_cm2"][k]))
    return {
        "step": row["step"],
        "arm": row["arm"],
        "independent_rK_Q": lag["weighted_rK_Q"],
        "independent_current_error_A_cm2": result["independent_profile_difference_A_cm2"],
        "lagged_current": lag["current"],
        "closure_A_cm2": lag["maximum_closure_error_A_cm2"],
        "projected_divergence_error_A_cm2": lag["largest_projected_flux_divergence_disagreement_A_cm2"],
        "contrasts": lag["contrasts"],
        "particle_exchange_A_cm2": lag["particle_exchange_A_cm2"],
        "projected_crossings_delta_A_cm2": {name: curve[j]-curve[i]
            for name,curve in lag["projected_crossings_A_cm2"].items()},
        "strongest_cell_center_nm": (cuts[biggest]+cuts[biggest+1])/2,
        "strongest_cell_delta_A_cm2": lag["current_A_cm2"][biggest+1]-lag["current_A_cm2"][biggest],
        "lo_localization": lo,
        "fresh_current": obs["current"],
        "fresh_raw_lambda": obs["raw_lambda"],
        "fresh_bands": {key:obs["central_bands"][key] for key in ("reference_energy_meV", "sheet_cm2",
                                                                 "fraction", "total_sheet_over_physical_sheet")},
    }


def remove_histories(report):
    """Keep scalar compatibility checks and all current profiles, omit per-ring energy tables."""
    result = dict(report)
    for name in ("observations",):
        if name in result:
            result[name] = {case: {key: value for key, value in obs.items()
                                   if key in ("current_A_cm2", "current", "raw_lambda", "raw_sheet_cm2", "raw_ring_sheet_cm2",
                                              "central_bands", "particle_exchange_A_cm2")}
                            for case, obs in result[name].items()}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    records, tracks, cuts, chosen = {}, {}, None, {}
    scalar_rows = []
    for label in ("primary7", "expanded8"):
        rows = load(args.runs/(label+".jsonl"))
        if not rows:
            continue
        config = rows[0]
        if cuts is None:
            cuts = config["cuts"]
        if cuts != config["cuts"]:
            raise ValueError(f"{label} changed physical cuts")
        maps = [row for row in rows if row["kind"] == "map"]
        trial = [row for row in rows if row["kind"] == "comparison"]
        balance = [row for row in rows if row["kind"] == "balance"]
        tracks[label] = maps
        selected = {1, 8, 24, 40, 48, 56, 64, 72, 80, 96}
        if maps:
            selected.add(maps[-1]["step"])
        chosen[label] = [row for row in maps if row["step"] in selected]
        records[label] = {
            "configuration": {key: value for key, value in config.items() if key != "cuts"},
            "selected": [metrics(row, cuts) for row in chosen[label]],
            "balances": [balance_row(row) for row in balance],
            "comparison": [metrics(row,cuts) for row in trial],
        }
        for row in (maps + trial):
            scalar_rows.append({"run":label, "kind":row["kind"], **metrics(row,cuts)})
        if trial and maps:
            effect = []
            for alternate in trial:
                accelerated = next((r for r in maps if r["step"] == alternate["step"]
                                    and r["arm"] == "picard100"), None)
                if accelerated is not None:
                    effect.append({"step":alternate["step"], "standard":metrics(alternate,cuts),
                                   "full":metrics(accelerated,cuts),
                                   "profile":profile_diff(accelerated,alternate)})
            records[label]["paired_solver_comparison"] = effect

    radial = args.runs/"primary7.jsonl.radial.json"
    if radial.exists():
        records["radial"] = remove_histories(json.loads(radial.read_text()))
    for suffix in ("radial.json.mechanism.json", "radial.json.error.json", "fine.jsonl.error.json"):
        additional = args.runs/("primary7.jsonl." + suffix)
        if additional.exists():
            records[suffix] = json.loads(additional.read_text())
    fine = args.runs/"primary7.jsonl.fine.jsonl"
    fine_history = []
    if fine.exists():
        data = json.loads(fine.read_text())
        fine_history = data.get("history",[])
        records["radial_continuation"] = {"stage": data.get("stage"), "error":data.get("error")}
    if fine_history:
        rows = [dict(row,step=row["nominal_iteration"]) for row in fine_history]
        for row in rows:
            scalar_rows.append({"run":"radial25","kind":"map",**metrics(row,cuts)})
        records["radial_continuation"] = {key: data.get(key) for key in (
            "stage","stationary","independent_current_difference_A_cm2","phase_delta")}
        records["radial_continuation"]["last"] = metrics(rows[-1],cuts)
        if "observed" in data:
            records["radial_continuation"]["last_observation"] = {
                k:data["observed"][k] for k in ("current","raw_lambda","central_bands")}
            records["radial_continuation"]["last_rK_Q"] = data["lagged"]["weighted_rK_Q"]
        primary_full = load(args.runs/"primary7.jsonl")
        standard = [r for r in primary_full if r.get("arm")=="picard035"
                    and r["kind"] in ("map","comparison")]
        at = next((r for r in standard if r["step"] == rows[-1]["step"]), None)
        if at is not None:
            records["radial_continuation"]["same_count"] = {
                "coarse":metrics(at,cuts),"fine":metrics(rows[-1],cuts),
                "profile":profile_diff(rows[-1],at), "residual_match":residual_match(rows[-1],at)}
        pool = [row for row in standard if row["step"] >= 16]
        if pool:
            coarse = min(pool,key=lambda row:max(residual_match(row,rows[-1])["ratios"].values()))
            records["radial_continuation"]["similar_residuals"] = {
                "coarse":metrics(coarse,cuts),"fine":metrics(rows[-1],cuts),
                "profile":profile_diff(rows[-1],coarse),
                "residual_match":residual_match(rows[-1],coarse)}

    node = args.runs/"node-replay.json"
    if node.exists():
        records["node_omission"] = json.loads(node.read_text())
        for arm in records["node_omission"].get("results",{}).values():
            if "observation_GL20" in arm:
                obs = arm["observation_GL20"]
                arm["observation_GL20"] = {name:obs[name] for name in (
                    "current_A_cm2","current","raw_lambda","raw_sheet_cm2","central_bands","particle_exchange_A_cm2")}

    if "primary7" in tracks and "expanded8" in tracks:
        choice = matched(tracks["primary7"], tracks["expanded8"])
        if choice:
            a,b = choice
            records["matched_rank"] = {"base":metrics(a,cuts), "expanded":metrics(b,cuts),
                                       "expanded_minus_base":profile_diff(b,a), "residual_match":residual_match(a,b)}
        a = next((r for r in tracks["primary7"] if r["step"]==48), None)
        b = next((r for r in tracks["expanded8"] if r["step"]==48), None)
        if a and b:
            records["rank_at_48"] = {"base":metrics(a,cuts),"expanded":metrics(b,cuts),
                                      "expanded_minus_base":profile_diff(b,a), "residual_match":residual_match(a,b)}

    if scalar_rows:
        with (args.out/"fresh-maps.csv").open("w", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=list(scalar_rows[0]))
            writer.writeheader()
            writer.writerows(scalar_rows)
    if cuts:
        profiles = {"z_nm":cuts}
        for label, rows in chosen.items():
            for row in rows:
                profiles[f'{label}_{row["step"]}'] = row["current_profile_A_cm2"]
        if fine_history:
            profiles["radial25_last"] = fine_history[-1]["current_profile_A_cm2"]
        with (args.out/"profiles.csv").open("w",newline="") as out:
            writer = csv.writer(out)
            writer.writerow(profiles)
            writer.writerows(zip(*profiles.values(),strict=True))
    write_json(args.out/"measurements.json",records)


if __name__ == "__main__":
    main()
