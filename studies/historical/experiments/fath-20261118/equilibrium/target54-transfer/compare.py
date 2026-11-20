"""Read original SCBA rows on identical map indices and audit the aligned target HDF."""
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import tomllib

import numpy as np

HERE = Path(__file__).resolve().parent
RUN = HERE / "attempt02"
COLD = HERE.parents[1] / "method/alpha-extended/attempt01/linear/rows"
DEVICE = HERE.parent / "attempt01/device.toml"
SAMPLES = (48, 128, 256)
METRICS = ("rSigma", "rK", "rLambda", "rPSD", "rJchange")


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def compare():
    with (RUN / "rows.csv").open() as stream:
        native = {int(r["map"]): r for r in csv.DictReader(stream)}
    with (HERE / "matched.csv").open("w", newline="") as stream:
        fields = ["map", "initialization", *METRICS, "max_algebra", "Jplus_A_cm2",
                  "Jminus_A_cm2", "Jnet_A_cm2", "r_sum", "strict"]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for i in SAMPLES:
            cold = tomllib.loads((COLD / f"{i:03}.toml").read_text())
            r = {key: cold[v] for key, v in zip(METRICS, ("r_Σ", "r_K", "r_λ", "r_PSD", "r_Jchange"), strict=True)}
            writer.writerow(dict(map=i, initialization="cold", **r, strict=cold["strict_pass"],
                                 max_algebra=max(r[key] for key in METRICS[:3]), Jplus_A_cm2=cold["J"]/1e4))
            if i in native:
                new = native[i]
                field_map = {key: new[key] for key in fields if key in new}
                writer.writerow(dict(initialization="transfer", **field_map,
                                    max_algebra=max(float(new[key]) for key in METRICS[:3])))
    return native[max(native)]


def audit(row):
    metadata = tomllib.loads((RUN / "summary.toml").read_text())
    model, state = RUN / "model.h5", RUN / "state.h5"
    assert sha(model) == metadata["model_sha256"] and sha(state) == metadata["state_sha256"]
    assert int(row["map"]) == metadata["maps"]
    header = subprocess.check_output(["h5dump", "-y", "-w", "0", "-d", "/model_identity", state], text=True)
    assert metadata["model_sha256"] in header
    device = tomllib.loads(DEVICE.read_text())
    with tempfile.TemporaryDirectory(prefix="fath-target-audit-") as folder:
        binary = Path(folder) / "data.bin"

        def read(file, field, shape):
            subprocess.run(["h5dump", "-b", "LE", "-o", binary, "-d", "/" + field, file],
                           check=True, stdout=subprocess.DEVNULL)
            values = np.fromfile(binary, dtype="<f8").reshape(shape)
            assert np.isfinite(values).all()
            return values

        def field(name):
            shape = (7,7,4,1201)
            z = read(state,name+"_real",shape) + 1j*read(state,name+"_imag",shape)
            return np.ascontiguousarray(z.transpose(3,2,1,0))

        assert np.all(read(state,"hartree",(144,)) == 0)
        we, wk = read(model,"weight_energy",(1201,)), read(model,"weight_k",(4,))
        weights = we[:,None]*wk[None,:]
        gr, gl, gg, a = (field("green/"+name) for name in ("GR","GL","GG","A"))
        total_l = sum((field("selfenergy/"+name+"/L") for name in
                     ("LO","acoustic","impurity","IFR","alloy","embedding")),start=np.zeros_like(gl))
        electron, hbar, scale_l, scale_e = 1.602176634e-19, 1.054571817e-34, 1e-8, .1
        measure = device["spin_degeneracy"]/(2*np.pi)
        number = lambda x: measure*np.sum(weights*np.trace(-1j*x,axis1=-2,axis2=-1).real)
        norm = lambda x: float(np.sqrt(np.sum(weights*np.sum(abs(x)**2,axis=(-2,-1)))))
        target = device["sheet_donors_m_minus_2"]*device["ionized_fraction"]*scale_l**2
        raw_l = gr@total_l@gr.conj().swapaxes(-1,-2)
        currents = {}
        for side in ("plus","minus"):
            left, right = (field("selfenergy/embedding_"+side+"/"+component) for component in ("L","G"))
            flow = np.einsum("ekij,ekji->ek",right,gl)-np.einsum("ekij,ekji->ek",left,gg)
            prefactor = measure*electron**2*scale_e/(hbar*scale_l**2)/10000
            currents[side] = float(prefactor*np.sum(weights*flow.real))
        integrated = np.einsum("e,ekab->kab",we/(2*np.pi),a)
        rsum = float(np.max(np.linalg.norm(integrated-np.eye(7),axis=(1,2)))/np.sqrt(7))
        output = dict(scope="mixed archived state, original fresh metrics are in rows.csv",
                      map=metadata["maps"], state_sha256=metadata["state_sha256"],
                      N_normalized_over_target=float(number(gl)/target),
                      raw_lambda_mixed=float(number(raw_l)/target),
                      rK_raw_mixed=norm(gl-raw_l)/norm(gl),
                      spectral_identity_relative=norm(1j*(gg-gl)-a)/norm(a),
                      minimum_eigenvalues={name: float(np.linalg.eigvalsh(x).min())
                                           for name,x in (("A",a),("Gn",-1j*gl),("Gp",1j*gg))},
                      Jplus_A_cm2=currents["plus"], Jminus_A_cm2=currents["minus"], r_sum=rsum,
                      Jplus_abs_error=abs(currents["plus"]-float(row["Jplus_A_cm2"])),
                      Jminus_abs_error=abs(currents["minus"]-float(row["Jminus_A_cm2"])),
                      r_sum_abs_error=abs(rsum-float(row["r_sum"])))
        assert output["Jplus_abs_error"] < 1e-7 and output["Jminus_abs_error"] < 1e-7
        assert output["r_sum_abs_error"] < 1e-11
        (HERE/"independent.json").write_text(json.dumps(output,indent=2)+"\n")


if __name__ == "__main__":
    audit(compare())
