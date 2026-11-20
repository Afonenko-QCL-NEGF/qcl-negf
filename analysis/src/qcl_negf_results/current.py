"""Reconstruct the native projected BDD current on every link and both seams."""
from __future__ import annotations

import hashlib
from pathlib import Path

from .native import validate_native_handle
from .presentation import committed_generation, inside


def _complex(group, selection):
    return group["real"][selection] + 1j * group["imag"][selection]


def _read_current_profile(state, *, block_bytes: int) -> dict:
    import numpy as np

    grid = state["grids_dimensionless"]
    z = grid["x"][:]
    energy_weights, radial_weights = grid["wE"][:], grid["wk"][:]
    faces = state["profiles_dimensionless/mz_relative"][:]
    basis = _complex(state["basis_dimensionless/Phi"], slice(None))
    step = float(grid["wx"][0])
    length = float(state["scales/L0_m"][()])
    energy = float(state["scales/E0_eV"][()])
    current_scale = float(state["scales/J0_A_per_m2"][()])
    spin = int(state["inputs/spin_degeneracy"][()])
    lesser, greater = (state[f"state_dimensionless/{field}"] for field in ("GL", "GG"))
    boundaries = [state[f"selfenergy_dimensionless/embedding_{side}"] for side in ("minus", "plus")]
    ne, nk, rank, second_rank = lesser["real"].shape
    expected = (len(energy_weights), len(radial_weights), rank, rank)
    groups = [lesser, greater] + [side[name] for side in boundaries for name in ("SL", "SG")]
    if second_rank != rank or any(group[part].shape != expected for group in groups for part in ("real", "imag")):
        raise ValueError("native state and quadrature axes do not agree")
    if basis.shape != (z.size, rank) or faces.shape != z.shape or np.any(faces <= 0) or step <= 0:
        raise ValueError("native projected BDD geometry does not agree with the state")

    # Keep each matrix intact. Stream a bounded number of energy slabs at once.
    per_energy = 16 * nk * rank**2 * len(groups)
    rows = max(1, block_bytes // per_energy)
    density = np.zeros((rank, rank), dtype=complex)
    exterior = np.zeros(2)
    for first in range(0, ne, rows):
        section = slice(first, min(first + rows, ne))
        weight = energy_weights[section, None] * radial_weights
        gl, gg = (_complex(group, section) for group in (lesser, greater))
        density += np.einsum("ek,ekab->ab", weight, gl)
        for index, boundary in enumerate(boundaries):
            sl, sg = (_complex(boundary[name], section) for name in ("SL", "SG"))
            outgoing = np.einsum("ek,ekab,ekba->", weight, sg, gl)
            incoming = np.einsum("ek,ekab,ekba->", weight, sl, gg)
            exterior[index] += (outgoing - incoming).real

    # CODATA constants and the independent nearest-neighbor BDD stencil.
    hbar = 1.054571817e-34
    electron_mass = 9.1093837139e-31
    electron_charge = 1.602176634e-19
    kinetic_scale = hbar**2 / (2 * electron_mass * energy * electron_charge * length**2)
    hopping = -2 * kinetic_scale / (step**2 * (faces[:-1] + faces[1:]))
    projected = np.einsum("ia,ab,ib->i", basis[1:], density, basis[:-1].conj())
    prefactor = current_scale * spin / (2 * np.pi)
    current = np.r_[-exterior[0], 2 * hopping * projected.real, exterior[1]] * prefactor
    if not np.all(np.isfinite(current)):
        raise ValueError("nonfinite current in native state")
    return {
        "orientation": "+z electron flow",
        "units": "A/m^2",
        "z_nm": (np.r_[z[0] - step / 2, (z[:-1] + z[1:]) / 2, z[-1] + step / 2] * length * 1e9).tolist(),
        "current_density": current.tolist(),
    }


def committed_current_profile(artifact_root: Path, *, block_bytes: int = 8 * 1024**2) -> dict:
    """Read the immutable full state from a point's artifacts directory."""
    import h5py

    if block_bytes < 1:
        raise ValueError("block_bytes must be positive")
    generation, commit, digest = committed_generation(artifact_root)
    states = [item for item in commit["artifacts"] if item["role"] == "physics.full"]
    if len(states) != 1:
        raise ValueError("current profile requires one committed full state")
    item = states[0]
    path = inside(generation, item["path"])
    with path.open("rb") as stream:
        if path.stat().st_size != item["bytes"] or hashlib.file_digest(stream, "sha256").hexdigest() != item["sha256"]:
            raise ValueError("full state differs from the committed size or SHA-256")
        stream.seek(0)
        with h5py.File(stream, "r") as state:
            validate_native_handle(state, "physics.full", item["schema"])
            return {"commit_sha256": digest, **_read_current_profile(state, block_bytes=block_bytes)}


def linked_current_profile(result_path: Path) -> dict:
    """Rebuild J(z) from the linked solver's compact, energy-integrated state."""
    import numpy as np
    from .commits import read_json

    result, payload = read_json(result_path, maximum=32 * 1024**2)
    if result.get("schema") != "qcl-negf-linked-run/v1":
        raise ValueError("unsupported linked run schema")
    if result.get("result_size_bytes") != len(payload):
        raise ValueError("linked result byte count does not match its declaration")
    status = result.get("status")
    if (status, result.get("exit_code")) not in (("completed", 0), ("reference_mismatch", 1)):
        raise ValueError("linked run has no usable terminal current profile")
    input_info = result.get("input")
    input_id = input_info.get("id") if isinstance(input_info, dict) else None
    if not isinstance(input_id, str) or not input_id:
        raise ValueError("linked result has no input identity")
    state = result.get("state")
    if not isinstance(state, dict) or state.get("schema") != "qcl-negf-linked-current-state/v1":
        raise ValueError("linked run has no supported terminal current state")
    try:
        cuts = np.asarray(state["current_midpoints_nm"], dtype=float)
        q_real = np.asarray(state["coordinate_frame_real"], dtype=float)
        q_imag = np.asarray(state["coordinate_frame_imag"], dtype=float)
        packed = np.asarray(state["packed_lesser_energy_moment_by_ring"], dtype=float)
        seams = np.asarray(state["seam_real_lesser_energy_moment_by_ring"], dtype=float)
        hopping = np.asarray(state["hopping_by_ring"], dtype=float)
        radial = np.asarray(state["radial_weights"], dtype=float)
        spin = float(state["spin_degeneracy"])
        scale = float(state["current_scale_A_cm2"])
    except (KeyError, TypeError) as error:
        raise ValueError("malformed linked current state") from error
    if q_real.ndim != 2 or q_real.shape != q_imag.shape or cuts.ndim != 1 or radial.ndim != 1:
        raise ValueError("invalid dimensions in linked current state")
    q = q_real + 1j * q_imag
    coordinates, rank = q.shape
    rings = radial.size
    if (coordinates < 2 or rank == 0 or rings == 0 or cuts.shape != (coordinates + 1,)
            or packed.shape != (rings, rank**2) or seams.shape != (rings, 2)
            or hopping.shape != (rings, cuts.size)):
        raise ValueError("linked current state arrays differ in their declared axes")
    if (not all(np.all(np.isfinite(values)) for values in (q, cuts, radial, packed, seams, hopping, spin, scale))
            or np.any(np.diff(cuts) <= 0) or np.any(radial <= 0) or spin <= 0 or scale <= 0):
        raise ValueError("invalid measure or nonfinite linked current state")

    moment = np.zeros((rings, rank, rank), dtype=complex)
    diagonal = np.arange(rank)
    moment[:, diagonal, diagonal] = packed[:, :rank]
    # The upper triangle is packed by successive columns in the Julia ABI.
    lower_row, lower_col = np.tril_indices(rank, k=-1)
    upper = packed[:, rank::2] + 1j * packed[:, rank + 1::2]
    moment[:, lower_col, lower_row] = upper
    moment[:, lower_row, lower_col] = upper.conj()
    interior = np.einsum("za,kab,zb->kz", q[1:], 1j * moment, q[:-1].conj()).real
    coherences = np.concatenate((seams[:, :1], interior, seams[:, 1:]), axis=1)
    current = (scale * spin / np.pi) * np.einsum("k,kz,kz->z", radial, hopping, coherences)
    if not np.all(np.isfinite(current)):
        raise ValueError("nonfinite current in linked state")
    return {
        "input_id": input_id,
        "terminal_status": status,
        "result_sha256": hashlib.sha256(payload).hexdigest(),
        "orientation": "+z electron flow",
        "units": "A/cm^2",
        "z_nm": cuts.tolist(),
        "current_density": current.tolist(),
        "outward_current_density": [-float(current[0]), float(current[-1])],
    }
