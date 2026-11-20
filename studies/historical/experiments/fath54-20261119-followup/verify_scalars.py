"""Scalar LO and IFR quadrature controls for the Fath 54 mV campaign. Python 3."""

import json
import math


def trapezoid_ratio(nodes, distance, screening, cutoff):
    """Finite-window cosine transform divided by its value at zero distance."""
    spacing = 2 * cutoff / (nodes - 1)
    numerator = []
    denominator = []
    for i in range(nodes):
        q = -cutoff + spacing * i
        endpoint = 0.5 if i in (0, nodes - 1) else 1.0
        weight = endpoint / (q * q + screening**2)
        denominator.append(weight)
        numerator.append(weight * math.cos(q * distance))
    return math.fsum(numerator) / math.fsum(denominator)


def gauss_ratio(panels, distance, screening, cutoff):
    """Eight-point Gauss–Legendre per panel; exact finite-window denominator."""
    nodes = (0.1834346424956498, 0.5255324099163290,
             0.7966664774136267, 0.9602898564975363)
    weights = (0.3626837833783620, 0.3137066458778873,
               0.2223810344533745, 0.1012285362903763)
    half = cutoff / panels
    terms = []
    for panel in range(panels):
        center = -cutoff + (2 * panel + 1) * half
        for node, weight in zip(nodes, weights):
            for sign in (-1, 1):
                q = center + sign * half * node
                terms.append(half * weight * math.cos(q * distance) /
                             (q * q + screening**2))
    return math.fsum(terms) / (2 * math.atan(cutoff / screening) / screening)


def modified_bessel(order, x):
    """Positive series for I_order(x), used only for orders <=96 and x<=11.52."""
    term = (x / 2)**order / math.factorial(order)
    terms = [term]
    for i in range(1, 120):
        term *= (x / 2)**2 / (i * (order + i))
        terms.append(term)
        if term <= 1e-18 * math.fsum(terms):
            break
    return math.fsum(terms)


def check_roughness():
    correlation_nm = 8.0
    quadrature_max = 0.0
    float_max = 0.0
    for i in range(25):
        for j in range(25):
            k, kp = i * 0.025, j * 0.025
            x = correlation_nm**2 * k * kp / 2
            exact = modified_bessel(0, x)
            # Uniform 32-point averaging retains every 32nd Fourier harmonic.
            # The remaining terms beginning at I_128 are below 1e-115 for x<=11.52.
            aliases = math.fsum(modified_bessel(n, x) for n in (32, 64, 96))
            quadrature_max = max(quadrature_max, 2 * aliases / exact)
            angular = math.fsum(math.exp(x * math.cos(2 * math.pi * n / 32))
                                for n in range(32)) / 32
            float_max = max(float_max, abs(angular / exact - 1))
    assert 3.6e-15 < quadrature_max < 3.8e-15
    assert float_max < 7e-15
    return {"quadrature_relative_max": quadrature_max, "float_crosscheck": float_max}


def main():
    cutoff = 10.0
    screening = 0.20
    distance = 82 * 43.91 / 144
    coarse = trapezoid_ratio(81, distance, screening, cutoff)
    fine = trapezoid_ratio(321, distance, screening, cutoff)
    reference = gauss_ratio(512, distance, screening, cutoff)
    assert abs(reference - gauss_ratio(256, distance, screening, cutoff)) < 1e-12
    assert 0.99029 < coarse < 0.99031
    assert 0.006779 < fine < 0.006781
    assert 0.006768 < reference < 0.006771
    print(json.dumps({
        "distance_nm": distance,
        "phase_period_nm_81": 2 * math.pi / (2 * cutoff / (81 - 1)),
        "LO_finite_81": coarse,
        "LO_finite_321": fine,
        "LO_finite_reference": reference,
        "LO_full_line": math.exp(-screening * distance),
        "IFR": check_roughness(),
    }, indent=2))


if __name__ == "__main__":
    main()
