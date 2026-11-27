#!/usr/bin/env python3
"""Evaluate the registered V843 basis admission rule on named spectra."""

import argparse
import csv
import hashlib
import itertools
import json
from pathlib import Path
import tomllib

import numpy as np

from qcl_negf_results.presentation import inside
from qcl_negf_results.spectrum import read_cell_spectrum

RULE_PATH = Path(__file__).with_name("admission.toml")
FIGURE_PATH = RULE_PATH.parent.parent / "fath-v843/controls/fig1/fig1_profiles.csv"
ROLES = ("u", "l", "e", "i")
TRANSPORT = ("T17A32", "T17A128", "T33A32", "T33A128")


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def rule():
    with RULE_PATH.open("rb") as stream:
        document = tomllib.load(stream)
    if document["schema"] != "v843-basis-admission-v1":
        raise ValueError("unsupported V843 admission rule")
    return document


def figure(path, expected_digest):
    if digest(path) != expected_digest:
        raise ValueError("figure input checksum mismatch")
    with path.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    profiles = []
    for role in ROLES:
        entries = [r for r in rows if r["state"] == role]
        points = sorted((float(r["z_nm"]), max(0, float(r["relative_curve_height_eV_plot_units"])))
                        for r in entries)
        z, density = np.array(points).T
        (baseline,) = {1000 * float(r["baseline_eV_estimate"]) for r in entries}
        if (len(z) < 2 or not (np.diff(z) > 0).all() or not np.isfinite(density).all()
                or not np.isfinite(baseline) or not (density > 0).any()):
            raise ValueError(f"invalid reference profile for role {role}")
        profiles.append((z, density, baseline))
    return profiles


def cosine_on_axis(first, second, axis):
    denominator = np.sqrt(np.trapezoid(first**2, axis, axis=-1)
                          * np.trapezoid(second**2, axis, axis=-1))
    cross = np.trapezoid(first * second, axis, axis=-1)
    return np.divide(cross, denominator, out=np.zeros_like(cross), where=denominator > 0)


def compare_figure(z, energies_meV, densities, reference, settings):
    """Exhaustive distinct assignments, one z shift and one energy zero per assignment."""
    period, cuts = settings["period_nm"], settings["figure"]
    if (len(z) < 2 or not np.isfinite(z).all() or not np.all(np.diff(z) > 0)
            or len(energies_meV) < len(ROLES) or not np.isfinite(energies_meV).all()
            or not np.all(np.diff(energies_meV) >= 0)
            or densities.shape != (len(energies_meV), len(z))
            or not np.isfinite(densities).all() or not np.all(densities >= 0)):
        raise ValueError("invalid candidate spectrum for figure comparison")
    assignments = np.array(list(itertools.permutations(range(len(energies_meV)), len(ROLES))))
    delta = energies_meV[assignments] - [profile[2] for profile in reference]
    energy_rms = np.std(delta, axis=1)
    role_axis = np.arange(len(ROLES))
    best_shape = np.full(len(assignments), -np.inf)
    best_components = np.zeros_like(assignments, dtype=float)
    best_z = np.zeros_like(best_shape)
    for shift in np.linspace(-period, 0, cuts["shift_samples"]):
        scores = []
        for axis, ref_density, _ in reference:
            trial = np.array([np.interp(axis - shift, z, y, left=0, right=0) for y in densities])
            scores.append(cosine_on_axis(trial, ref_density, axis))
        components = np.asarray(scores)[role_axis, assignments]
        averaged = components.mean(axis=1)
        better = averaged > best_shape
        best_shape[better], best_components[better], best_z[better] = (
            averaged[better], components[better], shift,
        )
    winner, next_shape = np.argsort(-best_shape, kind="stable")[:2]
    energy_winner, next_energy = np.argsort(energy_rms, kind="stable")[:2]
    shape_margin = best_shape[winner] - best_shape[next_shape]
    energy_margin = energy_rms[next_energy] - energy_rms[energy_winner]
    details = dict(
        common_shift_nm=float(best_z[winner]),
        energy_offset_model_minus_article_meV=float(delta[winner].mean()),
        energy_rms_meV=float(energy_rms[winner]), shape_margin=float(shape_margin),
        energy_margin_meV=float(energy_margin), mean_cosine=float(best_shape[winner]),
        role_cosines=dict(zip(ROLES, best_components[winner].tolist(), strict=True)),
        role_indices=dict(zip(ROLES, (assignments[winner] + 1).tolist(), strict=True)),
        energy_best_role_indices=dict(zip(ROLES, (assignments[energy_winner] + 1).tolist(), strict=True)),
        role_energies_meV=dict(zip(ROLES, energies_meV[assignments[winner]].tolist(), strict=True)),
    )

    details["reasons"] = figure_failures(details, cuts)
    details["admitted"] = not details["reasons"]
    return details


def figure_failures(details, cuts):
    values = [details[key] for key in ("shape_margin", "energy_margin_meV", "energy_rms_meV")]
    if not all(np.isfinite(value) for value in [*values, *details["role_cosines"].values()]):
        raise ValueError("nonfinite figure-comparison metrics")
    role_minima = {role: cuts["minimum_clipped_e_cosine"] if role == "e"
                   else cuts["minimum_role_cosine"] for role in ROLES}
    return [reason for failed, reason in (
        (details["role_indices"] != details["energy_best_role_indices"],
         "shape_and_relative_energy_match_different_roles"),
        (details["shape_margin"] < cuts["minimum_shape_margin"], "shape_margin_below_threshold"),
        (details["energy_margin_meV"] < cuts["minimum_energy_margin_meV"], "energy_margin_below_threshold"),
        (details["energy_rms_meV"] > cuts["maximum_energy_rms_meV"], "energy_rms_above_threshold"),
        (any(details["role_cosines"][role] < minimum for role, minimum in role_minima.items()),
         "role_cosine_below_threshold"),
    ) if failed]


def spectrum_arrays(item):
    spectrum = item["spectrum"]
    return (np.asarray(spectrum["z_nm"]), np.asarray(spectrum["energies_eV"]) * 1000,
            np.asarray(spectrum["amplitudes_real_per_sqrt_nm"])**2
            + np.asarray(spectrum["amplitudes_imag_per_sqrt_nm"])**2)


def window_confirmation(smaller, larger, first_fit, second_fit, settings):
    za, _, pa = spectrum_arrays(smaller)
    zb, _, pb = spectrum_arrays(larger)
    common = za[(za >= zb[0]) & (za <= zb[-1])]
    if len(common) < 2:
        raise ValueError("adjacent candidate windows have no common physical observation grid")
    cosines = {}
    for role in ROLES:
        first = np.interp(common, za, pa[first_fit["role_indices"][role] - 1])
        second = np.interp(common, zb, pb[second_fit["role_indices"][role] - 1])
        cosines[role] = float(cosine_on_axis(first, second, common))
    change = np.array([first_fit["role_energies_meV"][role] - second_fit["role_energies_meV"][role]
                       for role in ROLES])
    drift = float(np.ptp(change))
    cuts = settings["figure"]
    return dict(admitted=all(value >= cuts["minimum_confirmation_cosine"] for value in cosines.values())
                and drift <= cuts["maximum_confirmation_energy_meV"], role_cosines=cosines,
                relative_energy_max_change_meV=drift)


def read_candidates(frozen_path, root, settings):
    # The caller supplies the original frozen plan independently of delivery.
    frozen_payload = frozen_path.read_bytes()
    frozen_digest = hashlib.sha256(frozen_payload).hexdigest()
    frozen = json.loads(frozen_payload)
    delivered_plan = json.loads(inside(root, "scientific_plan.json").read_bytes())
    if delivered_plan != frozen:
        raise ValueError("delivered result uses a different frozen plan")
    series = json.loads(inside(root, "series_result.json").read_bytes())
    if series["plan_fingerprint"] != frozen["fingerprint"]:
        raise ValueError("series does not identify the frozen plan")
    expected = {f"b{window}-r{rank}": (window, rank) for window in settings["windows"]
                for rank in settings["ranks"]}
    points = {row["id"]: row for row in series["points"]}
    axes = {row["id"]: row for row in frozen["points"]}
    if len(points) != len(series["points"]) or len(points) != len(expected):
        raise ValueError("missing or duplicate candidate point")
    result = {}
    for execution in frozen["executions"]:
        name = execution["variant_id"]
        if name not in expected or execution["operation"] != "structure_spectrum":
            raise ValueError(f"unexpected plan operation or variant {name}")
        item_key = expected[name]
        if item_key in result:
            raise ValueError(f"duplicate planned candidate {name}")
        (point_id,) = execution["point_ids"]
        row = points[point_id]
        if row["execution_id"] != execution["id"] or row["status"] != "completed":
            raise ValueError(f"missing completed parent {name}")
        axis = axes[point_id]
        expected_voltage = settings["period_nm"] * settings["field_kV_cm"] * 1e-4
        if (axis["temperature_K"] != settings["temperature_K"]
                or axis["effective_inputs"]["lo_temperature_K"] != settings["temperature_K"]
                or abs(axis["voltage_per_period_V"] - expected_voltage) > 1e-14):
            raise ValueError(f"candidate {name} has a different temperature or voltage")
        relative = row["data"]["artifact_root"] + "/artifacts"
        native = read_cell_spectrum(inside(root, relative))
        if (native["plan_fingerprint"], native["execution_id"], native["point_id"]) != (
                frozen["fingerprint"], execution["id"], point_id):
            raise ValueError(f"wrong result identity for parent {name}")
        details = native["checks"]["structure_basis_orthonormal"]
        window, rank = item_key
        spectrum = native["spectrum"]
        if (details["basis_states"] != rank or 2 * details["basis_periods"] + 1 != window
                or len(spectrum["energies_eV"]) != rank
                or len(spectrum["z_nm"]) != settings["spatial_nodes"]
                or abs(details["period_nm"] - settings["period_nm"]) > 1e-10):
            raise ValueError(f"different geometry in candidate {name}")
        native["source"] = {"plan_fingerprint": frozen["fingerprint"],
                            "execution_id": execution["id"], "point_id": point_id,
                            "output": "cell_spectrum", "artifact_root": relative,
                            "sha256": native["result_sha256"]}
        result[item_key] = native
    if result.keys() != set(expected.values()):
        raise ValueError("incomplete V843 window/rank matrix")
    return frozen_digest, result


def select(candidates, reference, settings):
    rows = []
    fits = {}
    baseline = settings["baseline"]
    measured = candidates[baseline["window"], baseline["rank"]]["checks"]["structure_translation"]["value"]
    baseline_reproduced = round(measured, baseline["rounding_digits"]) == baseline["translation_rounded"]
    for (window, rank), item in sorted(candidates.items()):
        checks = item["checks"]
        metrics = {name: checks[name]["value"] for name in settings["translation_limits"]}
        for name, threshold in settings["translation_limits"].items():
            value = metrics[name]
            if (not np.isfinite(value) or value < 0 or checks[name]["threshold"] != threshold
                    or checks[name]["passed"] != (value <= threshold)):
                raise ValueError(f"inconsistent structural evidence for {name}")
        # Core reports the second pair separately. The registered V843 rule
        # constrains the maximum of the first and second neighboring pairs.
        key = "structure_translation_two_pairs"
        metrics[key] = max(metrics["structure_translation_nearest"], metrics[key])
        failures = set(item["failed_checks"])
        if metrics[key] > settings["translation_limits"][key]:
            failures.add(key)
        row = dict(window_periods=window, rank=rank, source=item["source"],
                   translation_metrics=metrics, reasons=sorted(failures))
        if row["reasons"]:
            row["status"] = "static_rejected"
        else:
            match = compare_figure(*spectrum_arrays(item), reference, settings)
            row.update(status="figure_admitted" if match["admitted"] else "figure_rejected",
                       figure_comparison=match, reasons=match["reasons"])
            if match["admitted"]:
                fits[window, rank] = match
        rows.append(row)
    confirmations = []
    for rank in settings["ranks"]:
        for smaller, larger in itertools.pairwise(settings["windows"]):
            a, b = (smaller, rank), (larger, rank)
            if a in fits and b in fits:
                result = window_confirmation(candidates[a], candidates[b], fits[a], fits[b], settings)
                confirmations.append(dict(result, rank=rank, smaller_window=smaller, larger_window=larger))
    passing = sorted((row for row in confirmations if row["admitted"]),
                     key=lambda row: (row["rank"], -row["larger_window"]))
    choice = passing[0] if baseline_reproduced and passing else None
    if choice is not None:
        selected = candidates[choice["larger_window"], choice["rank"]]["source"]
        reason = "minimum_rank_confirmed_by_neighbor_window"
    else:
        selected = None
        reason = ("no_static_and_figure_admitted_rank_stable_under_window_expansion"
                  if baseline_reproduced else "b7_archive_baseline_did_not_reproduce")
    return dict(status="admitted" if selected else "rejected", reason=reason,
                baseline_reproduced=baseline_reproduced, candidates=rows,
                expansion_checks=confirmations, selected_source=selected)


def route(selection, pilot=None):
    """Resolve dependencies using a named, immutable selected-cell output."""
    source = selection["selected_source"]
    if selection["status"] == "rejected" and source is None:
        if pilot is not None:
            raise ValueError("test result cannot belong to a rejected selection")
        return dict.fromkeys(("PILOT", *TRANSPORT), "skipped_by_gate")
    if selection["status"] != "admitted" or source is None:
        raise ValueError("invalid scientific selection result")
    if pilot is None:
        return {"PILOT": "ready", **dict.fromkeys(TRANSPORT, "awaiting_pilot")}
    if pilot["input"] != source or pilot["output"] != "transport_pilot":
        raise ValueError("pilot result has a different parent or output name")
    status = pilot["status"]
    if status not in {"admitted", "rejected", "technical_failure"}:
        raise ValueError("unknown pilot status")
    child = {"admitted": "ready", "rejected": "skipped_by_gate",
             "technical_failure": "blocked_by_failure"}[status]
    return {"PILOT": status, **dict.fromkeys(TRANSPORT, child)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frozen_plan", type=Path)
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    settings = rule()
    reference = figure(FIGURE_PATH, settings["figure_sha256"])
    plan_hash, candidates = read_candidates(args.frozen_plan, args.result, settings)
    selection = select(candidates, reference, settings)
    report = dict(schema="v843-basis-admission-result-v1", rule_sha256=digest(RULE_PATH),
                  criterion_source=settings["source"], figure_sha256=settings["figure_sha256"],
                  frozen_plan_sha256=plan_hash, selection=selection, routing=route(selection),
                  transport_current_A_cm2=None)
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
