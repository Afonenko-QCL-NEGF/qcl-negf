#!/usr/bin/env python3
"""Compare two explicitly different V843 domains with the same Fig. 1 rule."""

import argparse
import json
from pathlib import Path
import tomllib

import numpy as np

from campaign import FIGURE_PATH, RULE_PATH, compare_figure, digest, figure, rule


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("domain_control", type=Path)
    args = parser.parse_args()
    with args.domain_control.open("rb") as stream:
        control = tomllib.load(stream)
    if control["schema"] != "v843-new-rank11-domains-v1":
        raise ValueError("unsupported rank-11 domain control")
    settings = rule()
    profiles = figure(FIGURE_PATH, settings["figure_sha256"])
    axis = np.asarray(control["z_nm"])
    metric = np.asarray(control["metric_nm"])
    if metric.shape != axis.shape or not np.isfinite(metric).all() or not (metric > 0).all():
        raise ValueError("invalid cell probability measure")
    fits = {}
    for key in ("whole_window_observed_in_cell", "both_operator_and_basis_restricted_to_cell"):
        observation = control[key]
        density = np.asarray(observation["density_nm_inverse"])
        fits[key] = compare_figure(axis, np.asarray(observation["energies_eV"]) * 1000,
                                   density, profiles, settings)
        probability = density @ metric
        if (not np.allclose(probability, observation["retained_probability"], rtol=0, atol=1e-10)
                or np.max(probability) > 1 + 1e-10):
            raise ValueError("probability inconsistent with the declared measure")
        if key == "both_operator_and_basis_restricted_to_cell" and not np.allclose(
                probability, 1, rtol=0, atol=1e-10):
            raise ValueError("restricted solve amplitudes must be normalized in the cell")
        fits[key]["retained_probability_range"] = [float(np.min(probability)), float(np.max(probability))]
    report = {key: control[key] for key in (
        "schema", "configuration_source_plan_fingerprint", "configuration_source_execution_id",
        "configuration_source_point_id", "voltage_per_period_V", "temperature_K", "lo_temperature_K",
        "driver_sha256", "case", "spatial_nodes_per_period", "rank",
        "hamiltonian_periods", "observed_periods", "energy_reference_eV", "historical_w11_reproduction",
        "localization", "boundary",
    )}
    if "restricted_vs_cell_max_energy_difference_eV" in control:
        report["restricted_vs_cell_max_energy_difference_eV"] = control["restricted_vs_cell_max_energy_difference_eV"]
    report.update(fits=fits, control_sha256=digest(args.domain_control), rule_sha256=digest(RULE_PATH),
                  figure_sha256=settings["figure_sha256"])
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
