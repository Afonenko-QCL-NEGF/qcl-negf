"""Synthetic routing and independent replay of the published DAG 66 numbers."""

import json
import os
from pathlib import Path
import unittest

import numpy as np

from campaign import TRANSPORT, figure_failures, route, rule, select


def named_candidate(z, energy_eV, density, values, failed_checks, window, rank):
    settings = rule()
    return {
        "spectrum": {
            "z_nm": z, "energies_eV": energy_eV,
            "amplitudes_real_per_sqrt_nm": np.sqrt(density),
            "amplitudes_imag_per_sqrt_nm": np.zeros_like(density),
        },
        "source": {"output": "cell_spectrum", "test_id": f"{window}:{rank}"},
        "failed_checks": failed_checks,
        "checks": {name: {"value": values[name], "threshold": limit, "passed": values[name] <= limit}
                   for name, limit in settings["translation_limits"].items()},
    }


class CampaignRoutingTests(unittest.TestCase):
    def test_synthetic_admission_and_pilot_rejection(self):
        settings = rule()
        settings.update(windows=[7, 9], ranks=[4, 7])
        z = np.linspace(0, 60, 301)
        energies_meV = np.array([3, 73, 214, 509])
        profiles = np.exp(-((z[None, :] - np.array([12, 24, 35, 44])[:, None]) / 1.5)**2)
        reference = [(z, profiles[index], energies_meV[index] - 100) for index in (2, 1, 0, 3)]
        candidates = {}
        values = dict.fromkeys(settings["translation_limits"], 0.0001)
        bad_values = dict(values, structure_translation=0.162285)
        high_energies_meV = np.r_[energies_meV, [650, 860, 1100]]
        high_profiles = np.r_[profiles, np.exp(-((z[None, :] - np.array([4, 56, 59])[:, None]) / 1.5)**2)]
        for window in settings["windows"]:
            candidates[window, 7] = named_candidate(z, high_energies_meV / 1000, high_profiles,
                bad_values, ["structure_translation"], window, 7)
            candidates[window, 4] = named_candidate(z, energies_meV / 1000, profiles,
                values, [], window, 4)
        selected = select(candidates, reference, settings)
        self.assertEqual(selected["status"], "admitted")
        self.assertEqual(selected["selected_source"]["test_id"], "9:4")
        self.assertEqual(route(selected), {"PILOT": "ready", **dict.fromkeys(TRANSPORT, "awaiting_pilot")})

        pilot = dict(input=selected["selected_source"], output="transport_pilot", status="rejected")
        self.assertEqual(route(selected, pilot), {"PILOT": "rejected",
                                                    **dict.fromkeys(TRANSPORT, "skipped_by_gate")})
        pilot["status"] = "technical_failure"
        self.assertEqual(route(selected, pilot), {"PILOT": "technical_failure",
                                                    **dict.fromkeys(TRANSPORT, "blocked_by_failure")})
        pilot["input"] = dict(pilot["input"], test_id="another candidate")
        with self.assertRaisesRegex(ValueError, "different parent"):
            route(selected, pilot)

    @unittest.skipUnless(os.environ.get("V843_DAG_66"), "published compact DAG 66 directory unavailable")
    def test_dag_66_reapplies_rules_to_archived_observables(self):
        settings = rule()
        root = Path(os.environ["V843_DAG_66"])
        reports = {window: json.loads((root / f"results/B{window}.json").read_bytes())
                   for window in settings["windows"]}
        native = {(window, row["rank"]): row for window, report in reports.items()
                  for row in report["candidates"]}
        historical = json.loads((root / "results/SELECT.json").read_bytes())
        self.assertEqual(len(native), len(historical["candidates"]))
        for row in historical["candidates"]:
            source = native[row["window_periods"], row["rank"]]
            static_failed = any(source[name.removeprefix("structure_")] > limit
                                for name, limit in settings["translation_limits"].items())
            self.assertEqual(static_failed, row["status"] == "static_rejected")
            if not static_failed:
                observed = row["figure_comparison"]
                failures = figure_failures(observed, settings["figure"])
                self.assertEqual(row["status"], "figure_rejected")
                self.assertTrue(failures)
                self.assertCountEqual(failures, observed["reasons"])
        self.assertEqual(historical["expansion_checks"], [])
        self.assertEqual(route(dict(historical, selected_source=None)),
                         dict.fromkeys(("PILOT", *TRANSPORT), "skipped_by_gate"))


if __name__ == "__main__":
    unittest.main()
