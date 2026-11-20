"""Verify that the Julia constructor delivers the independently scanned rank-nine space."""
import json
import tomllib

import numpy as np

from refine import HERE, NATIVE, TEST, NCELL, cell_blocks, fd_chain, snapshot_modes, static_metrics


def main():
    source = tomllib.loads((HERE/"verification.toml").read_text())
    case = next(c for c in NATIVE["cases"] if (c["cbo_mev"],c["nz"])==(149,144))
    lp,x,h,t,z,m,delta = cell_blocks(case)
    raw = snapshot_modes(h,t,7)[:,:9]
    built = np.asarray(source["phi"])
    difference = np.linalg.norm(raw@raw.T-built@built.T,ord=2)
    assert difference < 1e-9
    exact_bloch = np.array([np.linalg.eigvalsh(h+q*t+q.conjugate()*t.T)[:4]
                            for q in np.exp(1j*TEST)])
    finite = fd_chain(h,t,z,m,lp,NCELL,0.0,delta)
    scores = static_metrics(built,h,t,z,lp,delta,finite,exact_bloch)
    assert scores["static_05_pass"]
    out = dict(julia_native_and_numpy_projector_difference=float(difference),
               implementation_holdout=scores,adapter_sha256=source["adapter_sha256"])
    (HERE/"adapter_holdout.json").write_text(json.dumps(out,indent=2)+"\n")


if __name__=="__main__":
    main()
