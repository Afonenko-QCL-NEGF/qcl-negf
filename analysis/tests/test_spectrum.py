from copy import deepcopy

import pytest

from qcl_negf_results.spectrum import compare_cell_spectra


def record():
    return {
        "plan_fingerprint": "a" * 64,
        "execution_id": "execution-1",
        "point_id": "point-1",
        "spectrum": {
            "energy_reference_eV": 0.0,
            "energies_eV": [0.125, 0.25],
            "z_nm": [0.5, 1.5, 2.5],
            "metric_nm": [1.0, 4.0, 1.0],
            "amplitudes_real_per_sqrt_nm": [[1.0, 0.0, 0.0], [0.0, 0.5, 0.0]],
            "amplitudes_imag_per_sqrt_nm": [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
        },
        "result_sha256": "b" * 64,
        "operator_verdict": "failed",
        "failed_checks": ["structure_translation"],
    }


def compare(first, second):
    return compare_cell_spectra(first, second, energy_atol_eV=1e-10, projector_atol=1e-8)


def test_same_weighted_subspace_can_reproduce_a_failed_operator():
    first = record()
    second = deepcopy(first)
    second["spectrum"]["amplitudes_real_per_sqrt_nm"][1][1] = 0.0
    second["spectrum"]["amplitudes_imag_per_sqrt_nm"][1][1] = -0.5
    result = compare(first, second)
    assert result["reproducible"]
    assert result["projector_distance"] < 1e-14
    assert result["operator_verdicts"] == ["failed", "failed"]


def test_equal_energies_do_not_certify_the_subspace():
    first = record()
    second = deepcopy(first)
    second["spectrum"]["amplitudes_real_per_sqrt_nm"][1] = [0.0, 0.0, 1.0]
    result = compare(first, second)
    assert result["max_energy_error_eV"] == 0.0
    assert result["projector_distance"] == pytest.approx(1.0)
    assert not result["reproducible"]


@pytest.mark.parametrize(("key", "changed"), [
    ("z_nm", [0.25, 1.5, 2.5]),
    ("metric_nm", [1.0, 4.0, 2.0]),
])
def test_comparison_rejects_mismatched_axes_and_measures(key, changed):
    first = record()
    second = deepcopy(first)
    second["spectrum"][key] = changed
    with pytest.raises(ValueError, match="share coordinates, measure and rank"):
        compare(first, second)
