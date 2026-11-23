"""Independently audit compact Fath measurements and produce publication tables."""

import argparse
import csv
import json
import math
from pathlib import Path


def close(a, b, atol=1e-8, rtol=2e-12):
    if not math.isclose(a, b, abs_tol=atol, rel_tol=rtol):
        raise ValueError(f"{a:.17g} does not match {b:.17g}")


def csv_file(path, headings, rows):
    with path.open("w", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(headings)
        writer.writerows(rows)


def check_observation(row, cuts):
    j = row["profile"]
    if len(j) != 145 or not all(math.isfinite(x) for x in j):
        raise ValueError("incomplete or nonfinite current profile")
    w = [(c-a)/2 for a, c in zip(cuts[:-2], cuts[2:], strict=True)]
    mean = math.fsum(a*b for a, b in zip(j[1:-1], w, strict=True))/math.fsum(w)
    close(mean, row["mean"])
    for current, centered in zip(j, row["centered"], strict=True):
        close(current-mean, centered)
    close(max(abs(x-mean) for x in j), row["max_deviation"])
    close(-j[0], row["outward_seams"][0])
    close(j[-1], row["outward_seams"][1])
    i, k = [min(range(len(cuts)), key=lambda n: abs(cuts[n]-x))
            for x in (33.84729166666667, 39.640972222222224)]
    close(j[k]-j[i], row["delta_segment"])
    close(math.fsum(row["raw_charge_by_ring"]), row["raw_charge"], .01)
    close(row["raw_charge"] / 3e10, row["raw_lambda"])
    close(math.fsum(row["mode_fractions"]), 1)


def check_levels(data):
    cuts = data["cuts_nm"]
    if len(cuts) != 145 or cuts != sorted(set(cuts)):
        raise ValueError("physical cuts must be the same ordered 145 cuts")
    levels = data["levels"]
    for name in ("K25", "K27", "K31"):
        if len(levels[name]["w"]) != int(name[1:]):
            raise ValueError(f"wrong number of rings in {name}")
    coarse_axis = set(levels["K25"]["k_nm_inverse"])
    for name, grid in levels.items():
        w = grid["w"]
        if min(w) <= 0 or not coarse_axis.issubset(grid["k_nm_inverse"]):
            raise ValueError(f"negative weights or missing K25 ring in {name}")
        close(math.fsum(w), 9/math.pi)
        close(math.fsum(grid["transfer"]["density_transferred_by_ring_cm2"]),
              grid["transfer"]["density_transferred_cm2"], .01)
        for key in ("observed", "independent_input"):
            check_observation(grid["measurements"][key], cuts)
    if not set(levels["K27"]["k_nm_inverse"]).issubset(levels["K31"]["k_nm_inverse"]):
        raise ValueError("K31 dropped K27 nodes")
    for pair, comparison in data["differences"].items():
        old, new = pair.split("_to_")
        if new == "shift":
            new = "K31_shift"
        a, b = [levels[name]["measurements"]["observed"] for name in (old, new)]
        for field, curve in (("profile", "profile"), ("centered", "centered")):
            delta = [y-x for x, y in zip(a[curve], b[curve], strict=True)]
            close(max(map(abs, delta)), comparison[field]["value"])
        close(b["mean"]-a["mean"], comparison["mean"]["value"])
        close(b["raw_charge"]-a["raw_charge"], comparison["raw_charge"]["value"])
        close(b["delta_segment"]-a["delta_segment"], comparison["delta_segment"]["value"])
    return levels, cuts


def charge_contrasts(levels, differences):
    rows = []
    for pair in differences:
        left, right = pair.split("_to_")
        a, b = levels[left], levels["K31_shift" if right == "shift" else right]
        edges_a, edges_b = a["cells_u"], b["cells_u"]
        for stage in ("independent_input", "observed"):
            q_a = a["measurements"][stage]["raw_charge_by_ring"]
            q_b = b["measurements"][stage]["raw_charge_by_ring"]
            delta_cells = []
            in_window = 0.
            for i, (low, high) in enumerate(zip(edges_b[:-1], edges_b[1:], strict=True)):
                overlap = math.fsum(q_a[j]*max(0., min(high, y)-max(low, x))/(y-x)
                                    for j, (x, y) in enumerate(zip(edges_a[:-1], edges_a[1:], strict=True)))
                delta = q_b[i]-overlap
                delta_cells.append(delta)
                inside = max(0., min(4., high)-max(2.25, low))
                in_window += delta*inside/(high-low)
            total = math.fsum(delta_cells)
            close(total, math.fsum(q_b)-math.fsum(q_a), .02)
            rows.append(dict(pair=pair, stage=stage, total_cm2=total,
                             in_window_cm2=in_window, outside_window_cm2=total-in_window,
                             difference_by_destination_cell_cm2=delta_cells))
    return rows


def publish(data, out):
    if data["stage"] != "completed":
        raise ValueError("the follow-up has not completed")
    levels, cuts = check_levels(data)
    out.mkdir(parents=True, exist_ok=True)
    names = [n for n in ("K25","K27","K31","K31_shift") if n in levels]
    profiles = ["z_nm", "cut"] + [f"{name}_{key}_A_cm2" for name in names
                                    for key in ("profile", "centered")]
    csv_file(out/"profiles.csv", profiles, (
        [z, "left" if i == 0 else "right" if i == len(cuts)-1 else "interior"] +
        [levels[name]["measurements"]["observed"][key][i] for name in names
         for key in ("profile", "centered")] for i, z in enumerate(cuts)))
    radial_rows = []
    summary = []
    for name in names:
        grid = levels[name]
        values = grid["measurements"]
        before, fresh = values["independent_input"], values["observed"]
        coefficients = values["native_in"]["normalization"]
        summary.append([name, grid["transfer"]["density_transferred_cm2"], before["raw_charge"],
                        coefficients["a"], coefficients["c"], fresh["raw_charge"],
                        fresh["mean"], fresh["max_deviation"], fresh["delta_segment"],
                        values["native"]["rK"], values["native"]["rSigma"]])
        for i, k in enumerate(grid["k_nm_inverse"]):
            radial_rows.append([name, k, grid["w"][i], grid["cells_u"][i]/100,
                                grid["cells_u"][i+1]/100,
                                grid["transfer"]["density_transferred_by_ring_cm2"][i],
                                before["raw_charge_by_ring"][i], fresh["raw_charge_by_ring"][i]])
    csv_file(out/"levels.csv", ["level", "transferred_charge_cm-2", "dyson_input_charge_cm-2",
             "occupation_a", "hole_c", "fresh_charge_cm-2", "mean_current_A_cm2",
             "maximum_deviation_A_cm2", "segment_delta_A_cm2", "rK", "rSigma"], summary)
    csv_file(out/"radial-charge.csv", ["level", "k_nm-1", "weight", "u_left_nm-2", "u_right_nm-2",
             "transferred_charge_cm-2", "dyson_input_charge_cm-2", "fresh_charge_cm-2"], radial_rows)
    (out/"charge-contrasts.json").write_text(json.dumps(charge_contrasts(levels,data["differences"]),
                                    indent=2, allow_nan=False)+"\n", encoding="utf-8")
    followup = data["followup"].copy()
    for name in ("localization_K31", "localization_shifted"):
        if name in followup:
            filename = name.replace("_", "-")+".json"
            (out/filename).write_text(json.dumps(followup.pop(name),ensure_ascii=False,
                separators=(",", ":"),allow_nan=False)+"\n",encoding="utf-8")
            followup[name] = filename
    data = dict(data,followup=followup)
    (out/"measurements.json").write_text(json.dumps(data, ensure_ascii=False,
            separators=(",", ":"), allow_nan=False)+"\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("measurement", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    publish(json.loads(args.measurement.read_text()), args.output)
