"""Stream the archived Fath physical vertices on an explicitly supplied radial grid."""

import argparse
import sys
from pathlib import Path
from types import SimpleNamespace

import numpy as np


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("historical_builder", type=Path)
    parser.add_argument("model", type=Path)
    parser.add_argument("radii", type=float, nargs="+")
    args = parser.parse_args()
    sys.path.insert(0, str(args.historical_builder.parent))
    import regrid as physical

    radii = np.array(args.radii)
    if np.any(np.diff(radii) <= 0):
        raise ValueError("radii must be strictly ordered")
    weights = physical.annulus(radii)
    model = physical.model_inputs(args.model)
    if radii[0] != model["k"][0] or radii[-1] != model["k"][-1]:
        raise ValueError("radial domain changed")
    vertex = physical.Vertices(
        SimpleNamespace(
            model={**model, "k": radii, "wk": weights},
            model_path=args.model,
            device=physical.spec_at(physical.RUN / "device.toml"),
            config=physical.spec_at(physical.RUN / "input.toml"),
        )
    )
    output = sys.stdout.buffer

    def send(block, dtype):
        array = np.asarray(block, dtype=dtype)
        if not np.isfinite(array).all():
            raise ValueError("physical kernel has nonfinite entries")
        output.write(array.tobytes(order="F"))

    send(weights, "<f8")
    for ring in range(len(radii)):
        for row, dtype in zip(physical.kernels(vertex, ring), ("<f8", "<c16", "<f8"), strict=True):
            send(row, dtype)


if __name__ == "__main__":
    main()
