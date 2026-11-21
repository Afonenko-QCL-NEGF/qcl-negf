#!/usr/bin/env python3
"""Compare V843 central-mode probabilities to the vector curves in Fig. 1."""

import argparse
import csv
import hashlib
import itertools
import json
from pathlib import Path
import tomllib

import numpy as np


def original_modes(path):
    with (path / "spec.toml").open("rb") as stream:
        spec = tomllib.load(stream)
    if spec["device"] != "dupont-2012-V843-lindskog-2012" or spec["voltage"] != 0.75936:
        raise ValueError("the primary figure uses V843 at 21 kV/cm")
    nz, nb, nm = (spec[name] for name in ("nz", "nb", "n_modes"))
    periods = spec["periods"]
    center = periods.index(0)
    state_slice = slice(center * nb, (center + 1) * nb)
    frame = np.fromfile(path / "W.bin", "<c16").reshape((nz * len(periods), nm), order="F")
    h0 = np.fromfile(path / "H.bin", "<c16").reshape((nm, nm, spec["nk"]), order="F")[:, :, 0]
    block = frame[:, state_slice]
    metric = block.conj().T @ block
    change = np.linalg.solve(np.linalg.cholesky(metric).conj().T, np.eye(nb))
    energies, eigenstates = np.linalg.eigh(change.conj().T @ h0[state_slice, state_slice] @ change)
    modes = block @ change @ eigenstates
    faces = np.array(spec["coordinates_of_current_midpoints_nm"])
    period = faces[-1] - faces[0]
    z = np.hstack([(faces[1:] + faces[:-1])/2 + i*period for i in periods])
    return z, 100*energies, abs(modes)**2, period


def compare(path, curves):
    z, energy, shapes, period = original_modes(path)
    labels = "ulei"
    with curves.open(newline="") as stream:
        digitized = list(csv.DictReader(stream))
    reference = []
    for label in labels:
        entries = [r for r in digitized if r["state"] == label]
        x = np.array([float(r["z_nm"]) for r in entries])
        sort = np.argsort(x)
        height = np.maximum(0, [float(r["relative_curve_height_eV_plot_units"]) for r in entries])
        reference.append((x[sort], height[sort], 1000*float(entries[0]["baseline_eV_estimate"])))
    assignments = np.array(list(itertools.permutations(range(energy.size), len(labels))))
    basis_ids = np.arange(len(labels))
    differences = energy[assignments] - np.array([r[2] for r in reference])
    aligned_energy_rms = np.std(differences, axis=1)
    best_scores = np.full(assignments.shape[0], -np.inf)
    best_shifts = np.zeros_like(best_scores)
    best_individual = np.zeros(assignments.shape)
    for shift in np.linspace(-period, 0, 361):
        scores = np.zeros((len(labels), energy.size))
        for i, (x, height, _) in enumerate(reference):
            trial = np.array([np.interp(x - shift, z, y, left=0, right=0) for y in shapes.T])
            norm = np.sqrt(np.trapezoid(trial**2, x, axis=1) * np.trapezoid(height**2, x))
            scores[i] = np.trapezoid(trial*height, x, axis=1) / np.maximum(norm, 1e-300)
        component = scores[basis_ids, assignments]
        mean = component.mean(axis=1)
        update = mean > best_scores
        best_scores[update] = mean[update]
        best_shifts[update] = shift
        best_individual[update] = component[update]
    sorted_shape = np.argsort(best_scores)[-5:][::-1]
    sorted_energy = np.argsort(aligned_energy_rms)[:5]

    def row(i):
        return {
            "indices_in_ascending_energy_from_1": dict(zip(labels, (assignments[i]+1).tolist(), strict=True)),
            "single_shift_from_model_to_article_nm": float(best_shifts[i]),
            "mean_probability_cosine": float(best_scores[i]),
            "probability_cosine": dict(zip(labels, best_individual[i].tolist(), strict=True)),
            "energy_offset_model_minus_article_meV": float(differences[i].mean()),
            "energy_rms_after_offset_meV": float(aligned_energy_rms[i]),
        }

    return {
        "convention": "S-orthonormalized principal eigenstates of the central H(k=0) block",
        "publication_curve_sha256": hashlib.sha256(curves.read_bytes()).hexdigest(),
        "archive_spec_sha256": hashlib.sha256((path / "spec.toml").read_bytes()).hexdigest(),
        "central_eigenvalues_meV": energy.tolist(),
        "ranked_by_probability": [row(i) for i in sorted_shape],
        "ranked_by_relative_energy": [row(i) for i in sorted_energy],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("fig1_csv", type=Path)
    parser.add_argument("output", type=Path)
    opts = parser.parse_args()
    result = compare(opts.archive, opts.fig1_csv)
    with opts.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
