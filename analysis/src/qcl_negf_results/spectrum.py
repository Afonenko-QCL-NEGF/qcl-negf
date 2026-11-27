"""Independent comparison of a named central-cell spectrum on its declared measure."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
from pathlib import Path

import numpy as np

from .presentation import committed_generation, inside


def read_cell_spectrum(artifact_root: Path) -> dict:
    generation, commit, _ = committed_generation(artifact_root)
    if commit.get("terminal_status") != "completed":
        raise ValueError("the spectrum requires a completed diagnostic process")
    records = [
        item for item in commit["artifacts"]
        if item.get("role") == "science.comparison"
        and item.get("schema") == "qcl-negf-operator-diagnostics-v4"
    ]
    if len(records) != 1:
        raise ValueError("one operator diagnostic artifact is required")
    record = records[0]
    content = inside(generation, record["path"]).read_bytes()
    if len(content) != record["bytes"] or hashlib.sha256(content).hexdigest() != record["sha256"]:
        raise ValueError("cell spectrum artifact does not match its commit")
    payload = json.loads(content)
    if (payload.get("schema") != record["schema"]
            or payload.get("contract_set") != commit["contract_set"]
            or payload.get("operation") != "structure_spectrum"):
        raise ValueError("expected structure_spectrum diagnostic")
    identity = commit["identity"]
    fingerprint = identity.get("plan_fingerprint")
    if not isinstance(fingerprint, str) or re.fullmatch(r"[a-f0-9]{64}", fingerprint) is None:
        raise ValueError("cell spectrum must identify its frozen plan")
    if any(not isinstance(identity.get(key), str) or not identity[key]
           for key in ("point_id", "execution_id")):
        raise ValueError("cell spectrum must identify its execution and point")
    checks = payload["checks"]
    if not checks or any(not isinstance(row, dict) or type(row.get("passed")) is not bool
                         or not isinstance(row.get("name"), str) for row in checks):
        raise ValueError("operator diagnostics must declare every check verdict")
    if len({row["name"] for row in checks}) != len(checks):
        raise ValueError("operator checks must have unique names")
    spectra = [row["cell_spectrum"] for row in checks if "cell_spectrum" in row]
    if len(spectra) != 1:
        raise ValueError("one named cell_spectrum output is required")
    failed = sorted(row["name"] for row in checks if not row["passed"])
    return {
        "plan_fingerprint": fingerprint,
        "execution_id": identity["execution_id"],
        "point_id": identity["point_id"],
        "result_sha256": record["sha256"],
        "spectrum": spectra[0],
        "operator_verdict": "failed" if failed else "passed",
        "failed_checks": failed,
    }


def _weighted_basis(spectrum: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    axis = np.asarray(spectrum["z_nm"], dtype=float)
    weights = np.asarray(spectrum["metric_nm"], dtype=float)
    energy = np.asarray(spectrum["energies_eV"], dtype=float)
    real = np.asarray(spectrum["amplitudes_real_per_sqrt_nm"], dtype=float)
    imag = np.asarray(spectrum["amplitudes_imag_per_sqrt_nm"], dtype=float)
    if (axis.ndim != 1 or energy.ndim != 1 or not 0 < energy.size <= axis.size
            or weights.shape != axis.shape or real.shape != (energy.size, axis.size)
            or imag.shape != real.shape):
        raise ValueError("inconsistent spectrum and metric dimensions")
    if (any(not np.isfinite(a).all() for a in (axis, weights, energy, real, imag))
            or not np.all(np.diff(axis) > 0) or not np.all(weights > 0)
            or not np.all(np.diff(energy) >= 0)):
        raise ValueError("invalid spectrum coordinates, metric or eigenvalues")
    samples = np.sqrt(weights[:, None]) * (real + 1j * imag).T
    if np.linalg.norm(samples.conj().T @ samples - np.eye(energy.size), ord=2) > 1e-10:
        raise ValueError("cell spectrum violates the declared weighted normalization")
    orthogonal, _ = np.linalg.qr(samples, mode="reduced")
    return axis, weights, energy, orthogonal


def compare_cell_spectra(first: dict, second: dict, *, energy_atol_eV: float,
                         projector_atol: float) -> dict:
    """Compare equal-rank spectra and U U† after orthogonalizing sqrt(M) W."""
    if any(not math.isfinite(t) or t < 0 for t in (energy_atol_eV, projector_atol)):
        raise ValueError("comparison tolerances must be finite and nonnegative")
    if any(first[key] != second[key] for key in ("plan_fingerprint", "execution_id", "point_id")):
        raise ValueError("cell spectra belong to different frozen plan points")
    a, b = first["spectrum"], second["spectrum"]
    reference = a["energy_reference_eV"]
    if not math.isfinite(reference) or reference != b["energy_reference_eV"]:
        raise ValueError("cell spectra must share an energy reference")
    za, ma, ea, ua = _weighted_basis(a)
    zb, mb, eb, ub = _weighted_basis(b)
    if not np.array_equal(za, zb) or not np.array_equal(ma, mb) or ea.size != eb.size:
        raise ValueError("cell spectra must share coordinates, measure and rank")

    energy_error = float(np.max(np.abs(ea - eb)))
    projector_error = float(np.linalg.norm(ua @ ua.conj().T - ub @ ub.conj().T, ord=2))
    matching_checks = first["failed_checks"] == second["failed_checks"]
    return {
        "plan_fingerprint": first["plan_fingerprint"],
        "rank": int(ea.size),
        "spatial_nodes": int(za.size),
        "max_energy_error_eV": energy_error,
        "max_energy_error_limit_eV": energy_atol_eV,
        "projector_distance": projector_error,
        "projector_distance_limit": projector_atol,
        "same_failed_checks": matching_checks,
        "operator_verdicts": [first["operator_verdict"], second["operator_verdict"]],
        "failed_checks": [first["failed_checks"], second["failed_checks"]],
        "result_sha256": [first["result_sha256"], second["result_sha256"]],
        "reproducible": (
            energy_error <= energy_atol_eV and projector_error <= projector_atol and matching_checks
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", type=Path)
    parser.add_argument("second", type=Path)
    parser.add_argument("--energy-atol-ev", type=float, required=True)
    parser.add_argument("--projector-atol", type=float, required=True)
    args = parser.parse_args()
    result = compare_cell_spectra(
        read_cell_spectrum(args.first), read_cell_spectrum(args.second),
        energy_atol_eV=args.energy_atol_ev, projector_atol=args.projector_atol,
    )
    print(json.dumps(result, indent=2, allow_nan=False))
    return 0 if result["reproducible"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
