#!/usr/bin/env python3
"""Assemble the V843 evidence table without interpolating the solver runs."""

import argparse
from bisect import bisect_right
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MATCHED = {"upper_lasing": 3, "lower_lasing": 2, "extractor": 1, "injector": 4}


def read(path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def resolved(path, selection=None):
    document = read(path)
    if "measured" in document:
        metrics = document["measured"]
        return metrics["resolved"], metrics["independent_vs_production_A_cm2"], document["stationary"]
    if "observed" in document:
        return (document["observed"], document["independent_current_difference_A_cm2"],
                document["stationary"])
    if selection in ("old", "refined"):
        selected = document[selection]
        observation = selected["observation"]
        production = selected["summary"]["projected_fresh"]["raw_profile_A_cm2"]
        difference = max(abs(a - b) for a, b in zip(production, observation["current_A_cm2"], strict=True))
        return observation, difference, False
    raise ValueError(f"{path.name}: unsupported result or radial selection")


def digitization_segment(curve, field, dx, dy):
    points = sorted(curve)
    axis = [x for x, _ in points]

    def at(x):
        i = bisect_right(axis, x) - 1
        x0, y0 = points[i]
        x1, y1 = points[i + 1]
        return y0 + (x - x0) * (y1 - y0) / (x1 - x0)

    lo, hi = field - dx, field + dx
    ordinates = [at(lo), at(hi), *(y for x, y in points if lo <= x <= hi)]
    return [min(ordinates) - dy, max(ordinates) + dy]


def published_current(field):
    with (ROOT / "v843-published-points.csv").open(newline="", encoding="utf-8") as stream:
        rows = [r for r in csv.DictReader(stream) if float(r["field_kV_cm"]) == field]
    curves = {}
    with (ROOT / "jonasson-figure-2.csv").open(newline="", encoding="utf-8") as stream:
        for r in csv.DictReader(stream):
            curves.setdefault(r["series"], []).append(
                (float(r["field_kV_cm"]), float(r["current_A_cm2"])))
    raster = "NEGF50_original_raster"
    with (ROOT / "dupont-figure-9-NEGF50-raster.csv").open(newline="", encoding="utf-8") as stream:
        curves[raster] = [(float(r["field_kV_cm"]), float(r["current_A_cm2"]))
                          for r in csv.DictReader(stream)]
    result = {}
    for r in rows:
        if not r["current_A_cm2"]:
            continue
        name = r["series"]
        dx, dy = (0.06, 10.0) if name == raster else (0.02, 5.0)
        result[name] = {
            "current_A_cm2": float(r["current_A_cm2"]),
            "interpolation_bracket_kV_cm": [float(r["field_left_kV_cm"]),
                                           float(r["field_right_kV_cm"])],
            "digitization_range_A_cm2": digitization_segment(curves[name], field, dx, dy),
            "status": r["status"],
        }
    return result


def compare_temperature(observation):
    bands = observation["central_bands"]
    rows = {}
    with (ROOT / "v843-published-subband-moments.csv").open(newline="", encoding="utf-8") as stream:
        for r in csv.DictReader(stream):
            name, kind = r["subband"], r["observable"]
            if name in MATCHED:
                rows.setdefault(name, {})[kind] = float(r["value"])
    upper = bands["fraction"][MATCHED["upper_lasing"] - 1]
    report = {}
    temperature_weighted = 0.0
    total_matched = 0.0
    for band, position in MATCHED.items():
        i = position - 1
        charge, temperature = bands["fraction"][i], bands["equivalent_temperature_K"][i]
        total_matched += charge
        temperature_weighted += temperature * charge
        reference = rows[band]
        report[band] = {"central_index_from_1": position, "computed_T_K": temperature,
                        "published_T_K": reference["equivalent_temperature"],
                        "computed_population_relative_to_upper": charge / upper,
                        "published_population_relative_to_upper": reference["occupation_relative_to_upper"]}
    return {
        "physical_period_T_K": observation["equivalent_temperature_K"],
        "central_all_bands_T_K": bands["population_weighted_temperature_K"],
        "matched_four_bands_T_K": temperature_weighted / total_matched,
        "matched_band_fraction_of_central_projection": total_matched,
        "published_four_bands_T_K": 159.0,
        "band_data": report,
    }


def case(reference, directory):
    field = reference["field_kV_cm"]
    primary = reference["primary"]
    measured, quadrature, stationary = resolved(directory / primary["file"], primary.get("selection"))
    current = measured["current"]
    mean = current["mean_internal_A_cm2"]
    alternatives = []
    for source in reference["sensitivity"]:
        changed, change_quadrature, _ = resolved(directory / source["file"], source.get("selection"))
        changed_mean = changed["current"]["mean_internal_A_cm2"]
        compared_mean = mean
        if "against" in source:
            baseline = source["against"]
            paired, _, _ = resolved(directory / baseline["file"], baseline.get("selection"))
            compared_mean = paired["current"]["mean_internal_A_cm2"]
        alternatives.append({**source, "change_in_mean_A_cm2": changed_mean - compared_mean,
                             "own_quadrature_difference_A_cm2": change_quadrature,
                             "profile_range_A_cm2": changed["current"]["full_range_A_cm2"]})
    sensitivity = max([quadrature, *(max(abs(x["change_in_mean_A_cm2"]),
                                         x["own_quadrature_difference_A_cm2"]) for x in alternatives)])
    observed = published_current(field)
    negf_bounds = [value for name in ("NEGF50", "NEGF50_original_raster")
                   for value in observed[name]["digitization_range_A_cm2"]]
    return {
        "field_kV_cm": field, "primary": primary, "stationary": stationary,
        "mean_internal_A_cm2": mean,
        "resolved_min_max_A_cm2": current["full_range_A_cm2"],
        "outward_A_cm2": current["outward_A_cm2"],
        "spatial_deviation_A_cm2": current["max_deviation_from_mean_A_cm2"],
        "spatial_tolerance_A_cm2": current["target_tolerance_A_cm2"],
        "observed_sensitivity_A_cm2": sensitivity,
        "primary_quadrature_difference_A_cm2": quadrature,
        "sensitivity": alternatives,
        "published": observed,
        "published_negf_digitization_envelope_A_cm2": [min(negf_bounds), max(negf_bounds)],
        "difference_from_published_A_cm2": {k: mean - x["current_A_cm2"] for k, x in observed.items()},
        "temperature": compare_temperature(measured) if field == 21 else None,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_list", type=Path)
    parser.add_argument("output", type=Path)
    opts = parser.parse_args()
    cases = read(opts.case_list)
    if sorted(x["field_kV_cm"] for x in cases) != [12.5, 21.0]:
        raise ValueError("use exactly the two documented fields")
    result = {"schema": "qcl-negf-v843-comparison/v1",
              "cases": [case(x, opts.case_list.parent) for x in cases]}
    with opts.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
