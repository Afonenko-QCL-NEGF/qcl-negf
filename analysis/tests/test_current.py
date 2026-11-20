import h5py
import numpy as np
import pytest

from qcl_negf_results.current import _read_current_profile


def test_current_uses_saved_measure_and_orients_both_seams():
    with h5py.File("current-test.h5", "w", driver="core", backing_store=False) as state:
        state["grids_dimensionless/x"] = [0.25, 0.75]
        state["grids_dimensionless/wx"] = [0.5, 0.5]
        state["grids_dimensionless/wE"] = [0.5, 0.5]
        state["grids_dimensionless/wk"] = [2.0]
        state["profiles_dimensionless/mz_relative"] = [1.0, 3.0]
        state["scales/L0_m"] = 1e-8
        state["scales/E0_eV"] = 0.1
        state["scales/J0_A_per_m2"] = np.pi
        state["inputs/spin_degeneracy"] = 2

        def put(path, field):
            state[f"{path}/real"] = np.real(field)
            state[f"{path}/imag"] = np.imag(field)

        identity = np.eye(2)
        put("basis_dimensionless/Phi", identity)
        gl = 1j * np.asarray([[2, 0.5j], [-0.5j, 1]])
        put("state_dimensionless/GL", np.tile(gl, (2, 1, 1, 1)))
        put("state_dimensionless/GG", np.tile(-1j * identity, (2, 1, 1, 1)))
        for side, lesser, greater in (("minus", 0.25, 0.5), ("plus", 1, 1)):
            prefix = f"selfenergy_dimensionless/embedding_{side}"
            put(f"{prefix}/SL", np.tile(1j * lesser * identity, (2, 1, 1, 1)))
            put(f"{prefix}/SG", np.tile(-1j * greater * identity, (2, 1, 1, 1)))
        streamed = _read_current_profile(state, block_bytes=1)
        full = _read_current_profile(state, block_bytes=8192)

    kinetic_scale = 1.054571817e-34**2 / (2 * 9.1093837139e-31 * 0.1 * 1.602176634e-19 * 1e-16)
    assert streamed["current_density"] == pytest.approx([-2.0, -4 * kinetic_scale, 2.0])
    assert streamed["current_density"] == pytest.approx(full["current_density"])
    assert streamed["z_nm"] == pytest.approx([0.0, 5.0, 10.0])


def test_linked_reader_uses_the_two_oriented_seam_moments(tmp_path):
    import json
    from qcl_negf_results.current import linked_current_profile

    path = tmp_path / "linked-result.json"
    result = {
        "schema": "qcl-negf-linked-run/v1",
        "input": {"id": "test-profile"},
        "status": "completed",
        "exit_code": 0,
        "result_size_bytes": 0,
        "state": {
            "schema": "qcl-negf-linked-current-state/v1",
            "current_midpoints_nm": [0, 5, 10],
            "coordinate_frame_real": [[1, 0], [0, 1]],
            "coordinate_frame_imag": [[0, 0], [0, 0]],
            "packed_lesser_energy_moment_by_ring": [[2, 1, 0, 0.5], [2, 1, 0, 1]],
            "seam_real_lesser_energy_moment_by_ring": [[1, 2], [2, 1]],
            "hopping_by_ring": [[-1, -2, -3], [-3, -2, -1]],
            "radial_weights": [0.25, 0.75],
            "spin_degeneracy": 2,
            "current_scale_A_cm2": np.pi / 2,
        },
    }

    def write_result():
        while True:
            payload = json.dumps(result).encode("utf-8")
            if result["result_size_bytes"] == len(payload):
                path.write_bytes(payload)
                return
            result["result_size_bytes"] = len(payload)

    write_result()
    profile = linked_current_profile(path)
    assert profile["input_id"] == "test-profile"
    assert profile["terminal_status"] == "completed"
    assert profile["current_density"] == pytest.approx([-4.75, -1.75, -2.25])
    assert profile["outward_current_density"] == pytest.approx([4.75, -2.25])
    path.write_bytes(path.read_bytes() + b"\n")
    with pytest.raises(ValueError, match="byte count"):
        linked_current_profile(path)

    result.update(status="reference_mismatch", exit_code=1)
    write_result()
    assert linked_current_profile(path)["terminal_status"] == "reference_mismatch"
    result.update(status="failed")
    write_result()
    with pytest.raises(ValueError, match="usable terminal"):
        linked_current_profile(path)

    result.update(status="completed", exit_code=0)
    result["state"]["coordinate_frame_imag"] = [[0]]
    write_result()
    with pytest.raises(ValueError, match="invalid dimensions"):
        linked_current_profile(path)
