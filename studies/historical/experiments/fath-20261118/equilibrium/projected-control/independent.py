"""Read-only NumPy check of one aligned native handoff result, independent of Julia."""
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import tomllib

import numpy as np

HERE = Path(__file__).resolve().parent
RUN = HERE / "attempt01"
MODEL = RUN / "model.h5"
STATE = RUN / "state.h5"
SOURCE_DEVICE = HERE.parent / "attempt01/device.toml"


def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def check():
    metadata = tomllib.loads((RUN/"summary.toml").read_text())
    configuration = tomllib.loads(SOURCE_DEVICE.read_text())
    assert sha(MODEL) == metadata["model_sha256"]
    assert sha(STATE) == metadata["state_sha256"]
    state_header = subprocess.check_output(["h5dump", "-y", "-w", "0", "-d",
                                            "/model_identity", STATE], text=True)
    assert metadata["model_sha256"] in state_header
    with (RUN/"stock.csv").open() as history:
        row = list(csv.DictReader(history))[-1]
    assert int(row["stock_map"]) == metadata["stock_maps"]
    with tempfile.TemporaryDirectory(prefix="fath-projected-audit-") as temp:
        destination = Path(temp)/"field.bin"

        def read(source, path, shape):
            header = subprocess.check_output(
                ["h5dump", "-b", "LE", "-o", destination, "-d", "/"+path, source], text=True,
            )
            dimensions = re.search(r"DATASPACE\s+SIMPLE\s*\{\s*\(\s*([\d,\s]+)", header)
            assert dimensions is not None
            assert tuple(int(x.strip()) for x in dimensions.group(1).split(",")) == shape
            values = np.fromfile(destination, dtype="<f8").reshape(shape)
            assert np.isfinite(values).all()
            return values

        def complex_field(path):
            shape = (7,7,4,1201)
            value = read(STATE,path+"_real",shape) + 1j*read(STATE,path+"_imag",shape)
            return np.array(value.transpose(3,2,1,0), order="C")

        def axis(path, size):
            return read(MODEL, path, (size,))

        e0_eV, l0_m = .1, 1e-8
        spin, e_charge, hbar = configuration["spin_degeneracy"], 1.602176634e-19, 1.054571817e-34
        number_target = configuration["sheet_donors_m_minus_2"]*configuration["ionized_fraction"]*l0_m**2
        e = e0_eV*axis("energy_dimensionless",1201)
        we, wk = axis("weight_energy",1201), axis("weight_k",4)
        radial_k = axis("k_dimensionless",4)/(1e9*l0_m)
        weights = we[:, None]*wk[None, :]
        assert np.all(read(STATE, "hartree", (144,)) == 0)
        gr, gl, gg, a = (complex_field("green/"+name) for name in ("GR","GL","GG","A"))
        left = complex_field("selfenergy/embedding_minus/L")
        right = complex_field("selfenergy/embedding_plus/L")
        total_l = sum((complex_field("selfenergy/"+name+"/L") for name in
                       ("LO","acoustic","impurity","IFR","alloy","embedding")), start=np.zeros_like(gl))
        jp_g = complex_field("selfenergy/embedding_plus/G")
        jm_g = complex_field("selfenergy/embedding_minus/G")

    def energy_number(lesser):
        return spin/(2*np.pi)*np.sum(weights*np.trace(-1j*lesser,axis1=-2,axis2=-1).real)
    raw_l = gr@total_l@gr.swapaxes(-1,-2).conj()
    raw_lambda = energy_number(raw_l)/number_target

    def current(sl, sg):
        particle = np.einsum("ekij,ekji->ek",sg,gl)-np.einsum("ekij,ekji->ek",sl,gg)
        factor = (spin/(2*np.pi))*(e_charge**2*e0_eV/(hbar*l0_m**2))/1e4
        return float(factor*np.sum(weights*particle.real))

    jr, jl = current(right, jp_g), current(left, jm_g)
    spectral_integral = np.einsum("e,ekab->kab", we/(2*np.pi), a)
    spectrum = [{
        "k_nm_inverse": float(k),
        "relative_matrix_defect": float(np.linalg.norm(block-np.eye(7))/np.sqrt(7)),
        "trace": float(np.trace(block).real),
        "eigenvalues_min_max": np.linalg.eigvalsh(block)[[0,-1]].tolist(),
    } for k,block in zip(radial_k,spectral_integral,strict=True)]
    r_sum = max(row["relative_matrix_defect"] for row in spectrum)
    spectral_e = spin/(2*np.pi)*np.sum(weights*np.trace(a,axis1=-2,axis2=-1).real,axis=1)
    kt = 10 * 1.380649e-23/e_charge

    def fermi(mu):
        x = (e-mu)/kt
        q = np.exp(-abs(x))
        return np.where(x >= 0, q/(1+q), 1/(1+q))

    lo, hi = e[0]-128*kt, e[-1]+128*kt
    assert 0 < number_target < np.sum(spectral_e)
    for _ in range(90):
        mid = lo + (hi-lo)/2
        if np.dot(spectral_e,fermi(mid)) < number_target:
            lo = mid
        else:
            hi = mid
    mu = lo + (hi-lo)/2
    reference = a*fermi(mu)[:,None,None,None]

    def wn(x):
        return float(np.sqrt(np.sum(weights*np.sum(abs(x)**2, axis=(-2,-1)))))

    lower = {key: float(np.linalg.eigvalsh(matrix).min())
             for key,matrix in (("A",a),("Gn",-1j*gl),("Gp",1j*gg))}
    comparisons = {
        "raw_lambda_abs_difference": abs(raw_lambda-float(row["lambda"])),
        "Jplus_abs_difference_A_cm2": abs(jr-float(row["Jplus_A_cm2"])),
        "Jminus_abs_difference_A_cm2": abs(jl-float(row["Jminus_A_cm2"])),
        "r_sum_abs_difference": abs(r_sum-float(row["r_sum"])),
    }
    return {
        "check_scope": "archived mixed fields; fresh-map gates use the untouched e171 stock history",
        "state_sha256": metadata["state_sha256"], "stock_map": int(row["stock_map"]),
        "raw_lambda_mixed": float(raw_lambda), "rK_raw_mixed": float(np.linalg.norm(gl-raw_l)/(np.linalg.norm(gl)+1e-14)),
        "N_normalized_over_target": float(energy_number(gl)/number_target),
        "Jplus_out_A_cm2": jr, "Jminus_out_A_cm2": jl, "Jnet_out_A_cm2": jr+jl,
        "r_sum": float(r_sum), "spectral_sum_by_k": spectrum, "minimum_eigenvalues_solver_units": lower,
        "FDT_mu_meV": float(1000*mu), "FDT_relative_occupied": wn(-1j*gl-reference)/wn(reference),
        "spectral_identity_relative": wn(1j*(gg-gl)-a)/wn(a), **comparisons,
    }


if __name__=="__main__":
    (HERE/"independent.json").write_text(json.dumps(check(), indent=2) + "\n")
