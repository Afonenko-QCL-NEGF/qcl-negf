"""Replay the one-shot periodic Hartree response from the compact public density table."""
import csv
import hashlib
from pathlib import Path
import tomllib

import numpy as np

HERE = Path(__file__).resolve().parent
E_CHARGE = 1.602176634e-19
EPSILON_0 = 8.8541878128e-12


def weighted_mean(value, weight):
    return np.dot(value, weight)/weight.sum()


def flux_integral(rhs, eps, dx):
    """Integrate cyclic face fluxes, then integrate their potential differences."""
    face_eps = 2 * eps * np.roll(eps,-1)/(eps+np.roll(eps,-1))
    flux = -dx*np.cumsum(rhs)
    # The integration constant makes the sum of all increments exactly zero.
    flux -= np.sum(flux/face_eps)/np.sum(1/face_eps)
    differences = dx*flux/face_eps
    potential = np.r_[0,np.cumsum(differences[:-1])]
    return potential-potential.mean(), face_eps


def uniform_fft(rhs, eps, dx):
    n = len(rhs)
    m = np.arange(n//2+1)
    eigenvalue = 4*eps*np.sin(np.pi*m[1:]/n)**2/dx**2
    transform = np.fft.rfft(rhs)
    transform[0] = 0
    transform[1:] /= eigenvalue
    return np.fft.irfft(transform,n=n)


def table(csv_path, metadata):
    output = {}
    with csv_path.open() as f:
        for row in csv.DictReader(f):
            label = row.pop("case")
            output.setdefault(label,[]).append({name:float(val) for name,val in row.items()})
    for label, rows in output.items():
        assert [int(p["node"]) for p in rows] == list(range(1,len(rows)+1))
        z,dx,eps,donor,n,native = np.array([[p[k] for p in rows] for k in (
            "z_nm","weight_nm","epsilon_r","donor_m3","electron_m3","native_U_meV")])
        dz = dx*1e-9
        assert np.allclose(dx,dx[0],rtol=0,atol=1e-14)
        assert np.allclose(z,(np.arange(len(z))+.5)*dx[0],rtol=0,atol=1e-12)
        raw_number = donor-n
        compatible_number = raw_number-weighted_mean(raw_number,dz)
        # Use SI and meV directly. The factor e/eps0 gives the energy in eV
        # per SI discrete Poisson RHS, and x is now in metres.
        scale = -1000*E_CHARGE/EPSILON_0
        rhs = scale*compatible_number
        result,face_eps = flux_integral(rhs,eps,dz[0])
        flux = face_eps*(np.roll(result,-1)-result)/dz[0]
        resid = -(flux-np.roll(flux,1))/dz[0]-rhs
        rel_resid = np.linalg.norm(resid)/np.linalg.norm(rhs)
        native_error = np.max(abs(native-result))
        assert rel_resid<1e-11 and native_error<1e-10, (label,rel_resid,native_error)
        fft_error = None
        if np.all(eps==eps[0]):
            fft_answer = uniform_fft(rhs,eps[0],dz[0])
            fft_error = float(np.max(abs(fft_answer-result)))
            assert fft_error < 1e-10
        donor_sheet = float(np.dot(donor,dz))
        electron_sheet = float(np.dot(n,dz))
        raw_sheet = float(np.dot(raw_number,dz))
        corrected_sheet = float(np.dot(compatible_number,dz))
        amplitude = float(np.ptp(result))
        sigma = float(np.sqrt(weighted_mean((result-weighted_mean(result,dz))**2,dz)))
        assert abs(donor_sheet-metadata["cases"][label]["target_donor_m_minus_2"]) <= 1e-12*donor_sheet
        assert abs(electron_sheet-metadata["cases"][label]["sheet_density_matrix_trace_m_minus_2"]) <= 1e-12*electron_sheet
        output[label]=dict(z=z,weights=dz,curve=result,row=dict(
            case=label,maps=metadata["cases"][label]["source_maps"],voltage_mV=metadata["cell_bias_mV"],
            peak_to_peak_mev=amplitude,sigma_mev=sigma,min_mev=float(min(result)),max_mev=float(max(result)),
            z_min_nm=float(z[np.argmin(result)]),z_max_nm=float(z[np.argmax(result)]),
            cell_mean_mev=float(weighted_mean(result,dz)),
            pct_of_54mv=100*amplitude/metadata["cell_bias_mV"],
            donor_sheet_cm2=donor_sheet*1e-4,electron_sheet_cm2=electron_sheet*1e-4,
            raw_net_donor_minus_electron_sheet_cm2=raw_sheet*1e-4,
            raw_net_charge_C_m2=raw_sheet*E_CHARGE,
            compatible_source_net_sheet_cm2=corrected_sheet*1e-4,
            compatible_source_net_charge_C_m2=corrected_sheet*E_CHARGE,
            removed_uniform_net_number_m3=float(weighted_mean(raw_number,dz)),
            native_r_P_raw=metadata["cases"][label]["native_r_P_raw"],
            native_r_P_compatible=metadata["cases"][label]["native_r_P_compatible"],
            flux_compatible_r_P=rel_resid,native_flux_max_abs_difference_mev=float(native_error),
            fft_flux_max_abs_difference_mev=fft_error,
        ))
    return output


def write_csv(path, records):
    with path.open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)


def main():
    source = HERE/"density-input.csv"
    metadata = tomllib.loads((HERE/"density-sources.toml").read_text())
    assert hashlib.sha256(source.read_bytes()).hexdigest()==metadata["density_csv_sha256"]
    results = table(source,metadata)
    write_csv(HERE/"response-summary.csv",[r["row"] for r in results.values()])
    comparisons = [
        ("native54-03","compact54-pzp7"),
        ("native54-03","compact54-bloch7"),
        ("native54-03","wide54-pod9"),
        ("native54-03","native54-long-alpha02/checkpoint-0128"),
        ("compact54-pzp7","compact54-bloch7"),
        ("compact54-pzp7","compact54-pzp7-wide-upper"),
    ]
    rows = []
    for a,b in comparisons:
        before,after = results[a],results[b]
        np.testing.assert_array_equal(before["z"],after["z"])
        delta = after["curve"]-before["curve"]
        w = before["weights"]
        rows.append(dict(reference=a,comparison=b,
            delta_peak_to_peak_mev=float(after["row"]["peak_to_peak_mev"]-before["row"]["peak_to_peak_mev"]),
            difference_max_abs_mev=float(max(abs(delta))),
            difference_rms_mev=float(np.sqrt(weighted_mean(delta**2,w)))))
    write_csv(HERE/"response-sensitivity.csv",rows)


if __name__=="__main__":
    main()
