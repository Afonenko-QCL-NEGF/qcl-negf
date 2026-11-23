"""Build only static Fath operators with the archived physical vertex constructor."""

import argparse
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np


def radii(base, variant):
    if variant == "K25":
        return base.copy()
    window = np.flatnonzero((base >= 1.5 - 1e-14) & (base <= 2 + 1e-14))
    if len(window) != 3 or not np.allclose(base[window], [1.5, 1.75, 2.0], atol=1e-14):
        raise ValueError("the archived K25 must include the complete target window")
    phases = {"K27": [0.5], "K31": [0.25, 0.5, 0.75], "K31_shift": [0.2, 0.45, 0.7]}[variant]
    added = [base[i] + t * (base[i+1] - base[i]) for i in window[:-1] for t in phases]
    return np.sort(np.r_[base, added])


def build(args):
    sys.path.insert(0, str(args.historical_builder.parent))
    import regrid as physical

    old_path = args.archive
    spec = physical.spec_at(old_path / "spec.toml")
    if (spec["ne"], spec["nk"], spec["nb"], spec["r"], spec["voltage"],
        spec["physical_T_K"], spec["LO_temp_K"], spec["channels"]) != (
        481, 25, 7, 21, .54, 10., 10., physical.CHANNELS):
        raise ValueError("unexpected frozen physical parameters")
    old = {name: physical.mapped(old_path / f"{name}.bin", layout)
           for name, layout in physical.shapes(spec, 25).items() if name != "seed_packed_LG"}
    model_path = physical.RUN / "model.h5"
    if physical.sha(model_path) != spec["source_model_sha"]:
        raise ValueError("different source geometry")
    model = physical.model_inputs(model_path)
    if not np.array_equal(old["k"], model["k"]) or not np.array_equal(old["weights_k"], model["wk"]):
        raise ValueError("the archived reference differs from the physical K25 grid")
    k = radii(old["k"], args.variant)
    wk = physical.annulus(k)
    if np.min(wk) <= 0 or abs(wk.sum() - 9/np.pi) > 1e-14:
        raise ValueError("negative weights or different radial area")
    shared = np.searchsorted(k, old["k"])
    if not np.array_equal(k[shared], old["k"]):
        raise ValueError("some common radii changed")

    w = old["W"]
    kinetic = physical.CBAR / np.tile(model["mass_lateral"], len(spec["periods"]))
    mass = w.conj().T @ (kinetic[:,None] * w)
    mass = (mass + mass.conj().T) / 2
    h = old["H"][:,:,0,None] + mass[:,:,None] * k**2
    hop = np.repeat(old["hop"][:,[0]], len(k), axis=1)
    checks = {"H": physical.relative(h[:,:,shared], old["H"]),
              "hop": physical.relative(hop[:,shared], old["hop"])}
    h[:,:,shared] = old["H"]
    hop[:,shared] = old["hop"]
    u, u0 = k**2, old["k"]**2
    right = np.searchsorted(u0, u)
    exact = u == u0[right]
    left = np.where(exact, right, right - 1)
    f = np.zeros(len(u))
    f[~exact] = (u[~exact] - u0[left[~exact]]) / (u0[right[~exact]] - u0[left[~exact]])
    const = np.stack([physical.radial_transfer(old["anchor_by_channel"], left, right, f, 2, i)
                      for i in range(len(k))], axis=2)
    if not np.array_equal(const[:,:,shared,:], old["anchor_by_channel"]):
        raise ValueError("causal anchors changed at shared radii")
    if not np.allclose(const, const.swapaxes(0,1).conj(), rtol=2e-13, atol=1e-15):
        raise ValueError("causal anchors are not Hermitian")

    settings = physical.spec_at(physical.RUN / "input.toml")
    vertex = physical.Vertices(SimpleNamespace(model={**model, "k": k, "wk": wk},
                               model_path=model_path, device=physical.spec_at(physical.RUN / "device.toml"),
                               config=settings))
    checks.update({name: physical.relative(value, old[name]) for name, value in (
        ("acoustic", vertex.diagonal_strength["acoustic"]), ("alloy", vertex.diagonal_strength["alloy"]),
        ("ifr_sites", vertex.interfaces))})
    names = ("ifr_pair", "lo_covariance", "impurity_covariance")
    row_checks = {name: 0. for name in names}
    output = None if args.check_only else sys.stdout.buffer

    def send(block, dtype):
        if output is not None:
            output.write(np.asarray(block, dtype=dtype).tobytes(order="F"))

    for block, dtype in ((k,"<f8"), (wk,"<f8"), (h,"<c16"), (hop,"<f8"), (const,"<c16")):
        send(block, dtype)
    share_map = {int(i): j for j, i in enumerate(shared)}
    check_pairs = {name: [] for name in names} if args.check_only else None
    for i in range(len(k)):
        for name, row, dtype in zip(names, physical.kernels(vertex, i), ("<f8","<c16","<f8"), strict=True):
            if not np.isfinite(row).all():
                raise ValueError(f"{name} has a nonfinite pair at output ring {i}")
            if i in share_map:
                archived = old[name][..., share_map[i]]
                row_checks[name] = max(row_checks[name], physical.relative(row[..., shared], archived))
                row[..., shared] = archived
            send(row, dtype)
            if check_pairs is not None:
                check_pairs[name].append(row)
    reciprocal = {}
    if check_pairs is not None:
        for name, rows in check_pairs.items():
            numerator, scale = 0., 0.
            for j, row in enumerate(rows):
                for i, peer in enumerate(rows):
                    a, b = row[..., i], peer[..., j]
                    weight = wk[i] * wk[j]
                    numerator += weight * np.sum(np.abs(a - np.conjugate(b))**2)
                    scale += weight * np.sum(np.abs(a)**2)
            reciprocal[name] = float(np.sqrt(numerator / max(scale, np.finfo(float).tiny)))
        if max(reciprocal.values()) > 2e-12:
            raise ValueError(f"rebuilt pairs lost reciprocity: {reciprocal}")
    if max(*checks.values(), *row_checks.values()) > 2e-12:
        raise ValueError(f"shared blocks failed archive comparison: {checks}, {row_checks}")
    report = dict(variant=args.variant, radii_nm_inverse=(k/10).tolist(), weight_sum=float(wk.sum()),
                  minimum_weight=float(wk.min()), common_checks=checks, worst_common_row=row_checks, reciprocity=reciprocal,
                  arch_spec_sha256=physical.sha(old_path / "spec.toml"), Nphi=settings["Nphi"],
                  Nqz=settings["Nqz"])
    print(json.dumps(report), file=sys.stderr if output is not None else sys.stdout, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("historical_builder", type=Path)
    parser.add_argument("variant", choices=("K25", "K27", "K31", "K31_shift"))
    parser.add_argument("--check-only", action="store_true")
    build(parser.parse_args())
