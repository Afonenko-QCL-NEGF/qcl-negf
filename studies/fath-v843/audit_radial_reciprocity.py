#!/usr/bin/env python3
"""Check adjointness of the stored elastic radial kernels on their own measure."""

import argparse
import hashlib
import json
from pathlib import Path
import tomllib

import numpy as np


def audit(archive):
    path = archive / "spec.toml"
    content = path.read_bytes()
    spec = tomllib.loads(content.decode("utf-8"))
    nk, nz = spec["nk"], spec["nz"]
    weights = np.fromfile(archive / "weights_k.bin", "<f8")
    if len(weights) != nk or not all(weights > 0):
        raise ValueError("the radial weights must be positive and match the packet")
    result = {
        "spec_sha256": hashlib.sha256(content).hexdigest(),
        "radial_weights_sha256": hashlib.sha256(weights.tobytes()).hexdigest(),
        "rings": nk,
        "pair_measure": "w_k w_kprime",
        "operators": {},
    }
    for name, space_axes in (("impurity_covariance", (nz, nz)), ("ifr_pair", ())):
        path = archive / f"{name}.bin"
        kernel = np.fromfile(path, "<f8").reshape((*space_axes, nk, nk), order="F")
        defect = 0.0
        reference = 0.0
        maximum = 0.0
        for i in range(nk):
            for j in range(nk):
                different = kernel[..., i, j] - kernel[..., j, i].conj()
                measure = weights[i] * weights[j]
                defect += measure * np.sum(np.abs(different)**2)
                reference += measure * np.sum(np.abs(kernel[..., i, j])**2)
                maximum = max(maximum, np.max(np.abs(different)))
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        result["operators"][name] = {
            "sha256": digest,
            "maximum_pointwise_defect_solver_units": float(maximum),
            "relative_weighted_frobenius_defect": float(np.sqrt(defect/reference)),
        }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("output", type=Path)
    options = parser.parse_args()
    result = audit(options.archive)
    with options.output.open("x", encoding="utf-8") as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write("\n")
