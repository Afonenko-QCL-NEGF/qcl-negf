#!/usr/bin/env python3
"""Scalar V843 angular-quadrature diagnostic, requiring Python 3.11+ only.

Inputs: ../fath-v843/controls/v843-input/dupont/device.toml. Shapes match
V843TailVertices.assemble in that directory's v843_tail_vertices.jl. The
archived V843LinkedInput.new_input uses N_φ=32 and k_max=0.60 nm⁻¹. The rule
in QCLNEGF src/numerics/reference/grids.jl build_grids is φ_j=2πj/N.

The IFR shape is 2/(1+(Λq)²)^(3/2). The impurity matrix element is
exp(-q(d1+d2))/(q+qs)². Overall physical prefactors are omitted: this is
neither the full projected scattering kernel nor a transport calculation.
"""
import argparse
import json
import math
from pathlib import Path
import tomllib


DEVICE_PATH = (Path(__file__).resolve().parent / '../fath-v843/controls/'
               'v843-input/dupont/device.toml').resolve()
K_MAX_NM_INV = 0.60  # v843_linked_input.jl, V843LinkedInput.new_input
ANGULAR_NODES = (32, 64, 128, 256, 512, 1024)


def read_device(path):
    with path.open('rb') as stream:
        device = tomllib.load(stream)
    if device['identity'] != 'dupont-2012-V843-lindskog-2012':
        raise ValueError('unexpected device identity')
    if device['screening_model'] != 'density_temperature':
        raise ValueError('expected density_temperature screening')
    if device['ifr_correlation'] != 'exponential':
        raise ValueError('expected exponential IFR correlation')
    for key in ('period_nm', 'sheet_donors_m_minus_2', 'ionized_fraction',
                'spin_degeneracy', 'screening_temperature_K',
                'screening_mass_over_me', 'epsilon_static',
                'ifr_correlation_length_nm'):
        if not math.isfinite(device[key]) or device[key] <= 0:
            raise ValueError(f'{key} must be finite and positive')
    if not math.isclose(sum(device['layer_thickness_nm']), device['period_nm'], abs_tol=1e-9):
        raise ValueError('layer thicknesses do not match period in nm')
    if not all(math.isfinite(x) and x > 0 for x in device['layer_thickness_nm']):
        raise ValueError('layer thicknesses must be positive nm values')
    if not 0 < device['ionized_fraction'] <= 1:
        raise ValueError('ionized fraction outside physical range')
    if device['spin_degeneracy'] != 2:
        raise ValueError('unexpected spin degeneracy')
    return device


def screening(device):
    """Core screening_wavenumber(::ThomasFermiScreening2D), SI → nm⁻¹."""
    e = 1.602176634e-19
    eps0 = 8.8541878128e-12
    kb = 1.380649e-23
    hbar = 1.054571817e-34
    electron_mass = 9.1093837139e-31
    dos = (device['spin_degeneracy'] * device['screening_mass_over_me'] * electron_mass
           / (2 * math.pi * hbar**2))
    density = device['sheet_donors_m_minus_2'] * device['ionized_fraction']
    occupation = -math.expm1(-density / (dos * kb * device['screening_temperature_K']))
    return e**2 * dos * occupation / (2 * eps0 * device['epsilon_static']) * 1e-9


def value(kind, k, kp, phi, qs, distance, correlation_length):
    q = math.hypot(k - kp, 2 * math.sqrt(k * kp) * math.sin(phi / 2))
    if kind == 'ifr':
        return 2 / (1 + (correlation_length * q)**2)**1.5
    return math.exp(-q * distance) / (q + qs)**2


def uniform(kind, k, kp, qs, distance, correlation_length, n):
    if n < 4:
        raise ValueError('angular rule requires at least four nodes')
    return math.fsum(value(kind, k, kp, 2 * math.pi * j / n, qs, distance,
                           correlation_length) for j in range(n)) / n


def reference(kind, k, kp, qs, distance, correlation_length):
    # Independent adaptive Simpson on φ=πu²; angular symmetry reduces to [0,π].
    def f(u):
        return 2 * u * value(kind, k, kp, math.pi * u * u, qs, distance,
                             correlation_length)

    def simpson(a, b, fa, fm, fb):
        return (b - a) * (fa + 4 * fm + fb) / 6

    def refine(a, b, fa, fm, fb, whole, tol, depth):
        midpoint = (a + b) / 2
        fl = f((a + midpoint) / 2)
        fr = f((midpoint + b) / 2)
        left = simpson(a, midpoint, fa, fl, fm)
        right = simpson(midpoint, b, fm, fr, fb)
        delta = left + right - whole
        if abs(delta) <= 15 * tol:
            return left + right + delta / 15
        if depth == 0:
            raise RuntimeError('reference did not converge')
        return (refine(a, midpoint, fa, fl, fm, left, tol / 2, depth - 1)
                + refine(midpoint, b, fm, fr, fb, right, tol / 2, depth - 1))

    fa, fm, fb = f(0), f(0.5), f(1)
    initial = simpson(0, 1, fa, fm, fb)
    return refine(0, 1, fa, fm, fb, initial, 1e-12 * max(1, abs(initial)), 25)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--kernel', choices=['impurity', 'ifr'], required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    device = read_device(DEVICE_PATH)
    nominal_qs = screening(device)
    length = device['ifr_correlation_length_nm']
    if not 0 < nominal_qs < 1 or not 0 < length < 100:
        raise ValueError('screening or IFR length outside expected nm units')

    # Near-diagonal offsets are controlled probes, not archived radial nodes.
    pairs = [('diagonal', 0.3, 0.3), ('near_diagonal', 0.3, 0.3001),
             ('off_diagonal', 0.3, 0.45)]
    factors = [1.0, 0.1, 0.01] if args.kernel == 'impurity' else [1.0]
    distances = [0.0, 10.0] if args.kernel == 'impurity' else [0.0]
    rows = []
    for name, k, kp in pairs:
        for factor in factors:
            for distance in distances:
                qs = nominal_qs * factor
                if not (0 <= k <= K_MAX_NM_INV and 0 <= kp <= K_MAX_NM_INV
                        and qs > 0 and 0 <= distance <= device['period_nm'] * 2):
                    raise ValueError('probe outside declared physical dimensions')
                ref = reference(args.kernel, k, kp, qs, distance, length)
                if not math.isfinite(ref) or ref <= 0:
                    raise ValueError('invalid reference integral')
                values = {str(n): uniform(args.kernel, k, kp, qs, distance, length, n)
                          for n in ANGULAR_NODES}
                rows.append(dict(pair=name, k_nm_inv=k, kp_nm_inv=kp,
                                 q_min_nm_inv=abs(k-kp), q_max_nm_inv=k+kp,
                                 screen_factor=factor, qs_nm_inv=qs,
                                 distance_nm=distance, reference=ref, uniform=values,
                                 relative_error={n: abs(v-ref)/ref for n, v in values.items()}))
    result = dict(kernel=args.kernel, device_path=str(DEVICE_PATH),
                  screening_nominal_nm_inv=nominal_qs, ifr_correlation_nm=length,
                  reference='adaptive Simpson, phi=pi*u^2, symmetric angular mean',
                  unit_note='shape only; impurity nm^2, IFR dimensionless; prefactors excluded',
                  scope='one scalar coordinate element, not full device or transport', rows=rows)
    with open(args.output, 'w', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write('\n')


if __name__ == '__main__':
    main()
