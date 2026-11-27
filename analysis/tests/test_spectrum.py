from copy import deepcopy
import shutil

import pytest

from qcl_negf_contracts.artifacts import COMMIT_SCHEMA, CONTRACT_SET
from qcl_negf_results.commits import artifact_row, json_bytes, publish_pointer
from qcl_negf_results.export import export_snapshot
from qcl_negf_results.render import materialize
from qcl_negf_results.spectrum import compare_cell_spectra, read_cell_spectrum
from native_result_fixtures import point_status


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


def test_named_cell_result_requires_agreement_with_hash_bound_operator_verdict(tmp_path):
    generation = tmp_path / "generation-000001"
    generation.mkdir()
    cell = record()
    diagnostic = generation / "operator_checks.json"
    schema = "qcl-negf-operator-diagnostics-v4"
    checks = [
        {"name": "central_spectrum", "passed": True, "cell_spectrum": cell["spectrum"]},
        {"name": "structure_translation", "passed": False, "value": 0.162},
    ]
    diagnostic.write_bytes(json_bytes({
        "schema": schema, "schema_version": "4.0", "contract_set": CONTRACT_SET,
        "operation": "structure_spectrum", "checks": checks,
    }))
    commit = {
        "schema": COMMIT_SCHEMA, "contract_set": CONTRACT_SET, "generation": 1,
        "identity": {key: cell[key] for key in ("plan_fingerprint", "execution_id", "point_id")},
        "scientific_status": point_status("completed", operator="failed"),
        "artifacts": [artifact_row(diagnostic, relative=diagnostic.name, role="science.comparison",
                                   media_type="application/json", schema=schema)],
    }

    def publish():
        payload = json_bytes(commit)
        (generation / "commit.json").write_bytes(payload)
        publish_pointer(tmp_path / "current.json", "generation-000001/commit.json", payload, 1)

    publish()
    result = read_cell_spectrum(tmp_path)
    assert result["checks"]["structure_translation"]["value"] == 0.162
    assert result["failed_checks"] == ["structure_translation"]
    assert result["scientific_status"]["process"] == "completed"
    assert result["scientific_status"]["operator"] == "failed"
    assert result["scientific_status"]["campaign_verdict"] == "unknown"

    commit["scientific_status"]["operator"] = "passed"
    publish()
    with pytest.raises(ValueError, match="verdict differs from commit"):
        read_cell_spectrum(tmp_path)
    with pytest.raises(ValueError, match="verdict differs from commit"):
        materialize(generation, commit, "fixture", tmp_path / "figures")

    run = tmp_path / "run"
    shutil.copytree(tmp_path / "generation-000001", run / "artifacts/generation-000001")
    shutil.copyfile(tmp_path / "current.json", run / "artifacts/current.json")
    with pytest.raises(ValueError, match="verdict differs from commit"):
        export_snapshot(run, tmp_path / "exports")

    commit["scientific_status"] = point_status("completed", operator="failed", campaign_verdict="accepted")
    publish()
    with pytest.raises(ValueError, match="cannot attest a stationary or campaign verdict"):
        read_cell_spectrum(tmp_path)

    diagnostic.write_bytes(diagnostic.read_bytes() + bytes([10]))
    with pytest.raises(ValueError, match="artifact does not match its commit"):
        read_cell_spectrum(tmp_path)
