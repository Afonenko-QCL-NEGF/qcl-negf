"""Independent equilibrium FDT check on one archived terminal Green state."""
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
ATTEMPT = HERE / "attempt01"
LINEAR = ATTEMPT / "linear"
BIASED = HERE.parent / "method/alpha-extended/attempt01/linear"
STATE = LINEAR / "fdt-state.h5"
KB_EV_K = 1.380649e-23 / 1.602176634e-19


def load_toml(path):
    return tomllib.loads(path.read_text())


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read_binary(destination, key, shape, dtype="<f8"):
    # HDF5.jl orders dataset dimensions in reverse on disk.
    output = subprocess.check_output(
        ["h5dump", "-d", "/" + key, "-b", "LE", "-o", destination, STATE], text=True,
    )
    if shape:
        dimensional = re.search(r"DATASPACE\s+SIMPLE\s*\{\s*\(\s*([\d,\s]+)\)", output)
        assert dimensional is not None
        disk_shape = tuple(int(x.strip()) for x in dimensional.group(1).split(","))
        assert disk_shape == shape, (key, disk_shape, shape)
    else:
        assert re.search(r"DATASPACE\s+SCALAR", output)
    result = np.fromfile(destination, dtype=dtype).reshape(shape)
    assert np.isfinite(result).all(), key
    return result


def fermi(energies, mu, kt):
    x = (energies-mu)/kt
    p = np.exp(-np.abs(x))
    return np.where(x >= 0, p/(1+p), 1/(1+p))


def fdt():
    terminal = load_toml(LINEAR / "execution.toml")
    identity = load_toml(ATTEMPT / "identity.toml")
    parameters = load_toml(ATTEMPT / "device.toml")
    state_digest = digest(STATE)
    assert state_digest == terminal["fdt_state_sha256"]
    assert identity["model_source_sha256"] == digest(ATTEMPT / "device.toml")
    ne, nk, nb, _ = identity["shape_julia"]
    shape = (nb, nb, nk, ne)
    with tempfile.TemporaryDirectory(prefix="fath-fdt-") as temp:
        out = Path(temp) / "dataset.bin"

        def scalar(name, dtype="<f8"):
            return read_binary(out, name, (), dtype).item()

        def vector(name, size):
            return read_binary(out, name, (size,))

        def complex_array(name):
            return read_binary(out, name + "_real", shape) + 1j*read_binary(out, name + "_imag", shape)

        map_count = scalar("map", "<i8")
        assert map_count == terminal["maps"]
        energy_scale = scalar("energy_scale_eV")
        length_scale = scalar("length_scale_m")
        spin = scalar("spin_degeneracy", "<i8")
        assert spin == parameters["spin_degeneracy"]
        temperature = scalar("temperature_K")
        assert temperature == identity["lattice_temperature_K"] == identity["LO_temperature_K"] == 10
        e = energy_scale*vector("energy_dimensionless", ne)
        k = vector("k_dimensionless", nk)/(1e9*length_scale)
        we, wk = vector("energy_weight", ne), vector("radial_weight", nk)
        assert np.all(vector("hartree_dimensionless", 144) == 0)
        a, gn, gp = complex_array("A"), -1j*complex_array("GL"), 1j*complex_array("GG")
        target = parameters["sheet_donors_m_minus_2"]*parameters["ionized_fraction"]*length_scale**2
        assert abs(scalar("target_number_dimensionless")/target - 1) < 1e-13
    assert np.all(we > 0) and np.all(wk > 0)
    assert np.all(np.diff(e) > 0) and np.all(np.diff(k) > 0)
    weights = wk[:, None]*we[None, :]
    spectral_e = spin/(2*np.pi)*np.sum(weights*np.trace(a, axis1=0, axis2=1).real, axis=0)
    assert spectral_e.min() >= -1e-13*np.max(abs(spectral_e))
    assert 0 < target < np.sum(spectral_e)
    kt = KB_EV_K*temperature
    lo, hi = e[0]-128*kt, e[-1]+128*kt
    for _ in range(90):
        mid = lo+(hi-lo)/2
        represented = np.dot(spectral_e, fermi(e, mid, kt))
        if represented < target:
            lo = mid
        else:
            hi = mid
    mu = lo+(hi-lo)/2
    occupation = fermi(e, mu, kt)
    n_fit = np.dot(spectral_e, occupation)
    assert abs(n_fit/target-1) < 1e-12
    n_saved = spin/(2*np.pi)*np.sum(weights*np.trace(gn, axis1=0, axis2=1).real)
    reference_n, reference_p = a*occupation, a*(1-occupation)
    delta_n, delta_p = gn-reference_n, gp-reference_p

    def weight_norm(x):
        return float(np.sqrt(np.sum(np.sum(abs(x)**2, axis=(0, 1))*weights)))

    max_k, max_e = np.unravel_index(np.argmax(np.sum(abs(delta_n)**2, axis=(0, 1))), weights.shape)
    per_block = np.linalg.norm(delta_n[:, :, max_k, max_e])
    return {
        "model": "Fathololoumi CBO149 at 0mV, fixed U=0, all five channels, no ee",
        "source_state_sha256": state_digest, "map": map_count, "strict_status": terminal["status"],
        "temperature_K": temperature, "kBT_meV": 1000*kt,
        "mu_meV_from_A_and_donor_number": 1000*mu,
        "target_number_cm-2": target/(length_scale**2 * 1e4),
        "number_from_FD_cm-2": float(n_fit/(length_scale**2 * 1e4)),
        "number_from_archived_lesser_cm-2": float(n_saved/(length_scale**2 * 1e4)),
        "FDT_Gless_weighted_Frob_over_FD_A": weight_norm(delta_n)/weight_norm(reference_n),
        "FDT_Gless_weighted_Frob_over_Gless": weight_norm(delta_n)/weight_norm(gn),
        "FDT_Gless_weighted_Frob_over_A": weight_norm(delta_n)/weight_norm(a),
        "FDT_Gless_unweighted_Frob_over_FD_A": float(np.linalg.norm(delta_n)/np.linalg.norm(reference_n)),
        "FDT_Ggreater_weighted_Frob_over_hole_A": weight_norm(delta_p)/weight_norm(reference_p),
        "spectral_identity_weighted_Frob_over_A": weight_norm(gn+gp-a)/weight_norm(a),
        "max_Gless_block_defect": {
            "dimensionless_Frobenius": float(per_block), "energy_meV": 1000*e[max_e],
            "k_nm_inverse": k[max_k],
        },
    }


def matched_rows():
    actual = load_toml(LINEAR / "execution.toml")["maps"]
    result = []
    for n in sorted({48, 128, 256, actual}):
        for voltage, base in ((0, LINEAR), (54, BIASED)):
            file = base / "rows" / f"{n:03d}.toml"
            if not file.exists():
                continue
            row = load_toml(file)
            flux_file = base / f"flux-{n:03d}.toml"
            flux = load_toml(flux_file) if flux_file.exists() else {}
            result.append({
                "voltage_mV": voltage, "fresh_map": n, "rSigma": row["r_Σ"], "rK": row["r_K"],
                "rLambda": row["r_λ"], "lambda": row["λ"], "J_right_out_A_cm2": row["J"]/1e4,
                "J_left_out_A_cm2": flux.get("J_left_out_A_cm2"),
                "J_net_out_A_cm2": flux.get("sum_out_A_cm2"), "strict_pass": row["strict_pass"],
            })
    with (HERE / "matched_rows.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(result[0]))
        writer.writeheader()
        writer.writerows(result)


if __name__ == "__main__":
    (HERE / "fdt.json").write_text(json.dumps(fdt(), indent=2, ensure_ascii=False) + "\n")
    matched_rows()
