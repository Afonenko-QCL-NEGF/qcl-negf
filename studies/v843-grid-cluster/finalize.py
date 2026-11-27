"""Collect independent grid and paired-domain evidence after the batch leaves the queue."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import tomllib

HERE = Path(__file__).resolve().parent
SPECTRUM = HERE.parent / "v843-spectrum"
SOLVES = ("whole_window_observed_in_cell", "both_operator_and_basis_restricted_to_cell")
PRESETS = {"b11-pzp": 11, "w11-wannier-proxy": 9}
GRIDS = (96, 144, 216, 288)
FINE_CHANGE_MEV = 1.0


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_domain(work, preset, nz):
    window = PRESETS[preset]
    case = f"b{window}-r11-z{nz}"
    plan_path = work / "plans" / (case + ".json")
    plan = json.loads(plan_path.read_bytes())
    path = work / "domains" / (case + ".toml")
    with path.open("rb") as stream:
        payload = tomllib.load(stream)
    expected = {
        "configuration_source_plan_sha256": digest(plan_path),
        "configuration_source_plan_fingerprint": plan["fingerprint"],
        "configuration_source_execution_id": plan["executions"][0]["id"],
        "configuration_source_point_id": plan["points"][0]["id"],
        "spatial_nodes_per_period": nz, "hamiltonian_periods": window, "rank": 11,
        "case": preset, "observed_periods": 1, "historical_w11_reproduction": False,
        "driver_sha256": digest(HERE / "domain.jl"),
        "helper_sha256": digest(SPECTRUM / "domain-control.jl"),
    }
    if plan["root_definition_id"] != case or len(plan["points"]) != 1 or len(plan["executions"]) != 1:
        raise ValueError(f"wrong frozen parent for {case}")
    for key, value in expected.items():
        if payload.get(key) != value:
            raise ValueError(f"{case}: unexpected {key}")
    command = [sys.executable, str(SPECTRUM / "compare-domains.py"), str(path)]
    return json.loads(subprocess.check_output(command))


def fine_pair(rows, rms_cut):
    if 216 not in rows or 288 not in rows:
        return {"assessment": "unmeasured"}
    fits = [rows[n]["fits"] for n in (216, 288)]
    shifts = {s: abs(fits[1][s]["energy_rms_meV"] - fits[0][s]["energy_rms_meV"]) for s in SOLVES}
    same_roles = all(fits[1][s]["role_indices"] == fits[0][s]["role_indices"] for s in SOLVES)
    separated = all(f[SOLVES[0]]["energy_rms_meV"] <= rms_cut < f[SOLVES[1]]["energy_rms_meV"] for f in fits)
    stable = max(shifts.values()) <= FINE_CHANGE_MEV and same_roles
    assessment = "persistent_split" if separated and stable else "no_persistent_split" if stable else "unresolved"
    return {"assessment": assessment, "same_role_assignments": same_roles,
            "rms_changes_meV": shifts, "rms_threshold_straddled_at_both_grids": separated}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("work", type=Path)
    parser.add_argument("--require-cross", action="store_true")
    args = parser.parse_args()
    work = args.work.resolve()
    report = work / "report"
    report.mkdir(exist_ok=True, parents=True)
    grid_path = report / "native.json"
    # Each attempt has its own reader output, so a failed reader cannot reuse an older report.
    with TemporaryDirectory(dir=report) as attempt:
        fresh = Path(attempt) / "native.json"
        grid_run = subprocess.run([sys.executable, str(HERE / "readout.py"), str(work / "index.json"),
                               str(work), "--output", str(fresh)])
        native = json.loads(fresh.read_bytes()) if fresh.is_file() else {}
        grid_path.write_text(json.dumps(native, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    grid_ok = grid_run.returncode == 0 and native.get("status") == "complete"
    rule = tomllib.loads((SPECTRUM / "admission.toml").read_text(encoding="utf-8"))
    rms_cut = rule["figure"]["maximum_energy_rms_meV"]
    paired, errors, comparisons = {}, {}, {}
    lines = ["# Dupont V843. Зависимость от пространственной сетки", "",
             "| Вариант | Узлов на период | Полное окно, RMS (мэВ) | Один период, RMS (мэВ) |",
             "| --- | ---: | ---: | ---: |"]
    for preset in PRESETS:
        rows = {}
        for nz in GRIDS:
            try:
                rows[nz] = read_domain(work, preset, nz)
                a, b = (rows[nz]["fits"][s]["energy_rms_meV"] for s in SOLVES)
                lines.append(f"| {preset} | {nz} | {a:.4f} | {b:.4f} |")
            except (OSError, KeyError, ValueError, IndexError, subprocess.CalledProcessError) as error:
                errors[f"{preset}-z{nz}"] = str(error)
                lines.append(f"| {preset} | {nz} | нет измерения | нет измерения |")
        paired[preset] = rows
        comparisons[preset] = fine_pair(rows, rms_cut)
    cross = native.get("portability", {})
    failed_portability = cross.get("reproducible") is False or (args.require_cross and cross.get("reproducible") is not True)
    controls = {}
    for preset, rows in paired.items():
        if 144 in rows:
            name = "initial-b11-domains.json" if preset == "b11-pzp" else "initial-w11-wannier-proxy.json"
            reference = json.loads((SPECTRUM / "evidence" / name).read_bytes())["fits"]
            fits = rows[144]["fits"]
            controls[preset] = all(abs(fits[s]["energy_rms_meV"] - reference[s]["energy_rms_meV"]) <= 0.001
                                   and fits[s]["role_indices"] == reference[s]["role_indices"] for s in SOLVES)
    for row in native.get("cases", []):
        if row["id"] == "b7-r7-z144" and "translation_metrics" in row:
            baseline = rule["baseline"]
            controls["b7_translation"] = (row["status"] == "static_rejected" and
                round(row["translation_metrics"]["structure_translation"], baseline["rounding_digits"])
                == baseline["translation_rounded"])
    complete = grid_ok and not errors and not failed_portability
    anchors_match = len(controls) == 3 and all(controls.values())
    measured = sum(row.get("status") != "technical_failure" for row in native.get("cases", []))
    scope = "пройден" if cross.get("reproducible") else "расхождение" if cross.get("reproducible") is False else "нет измерения"
    lines += ["", f"Стандартных спектров прочитано {measured}/36. Межплатформенный контроль — {scope}.",
              "Ток и сходимость транспорта в программе не измеряются.", "",
              "| Сравнение 216 и 288 узлов | Разделение по порогу | Изменение RMS, окно / период (мэВ) |",
              "| --- | --- | --- |"]
    for preset, c in comparisons.items():
        change = c.get("rms_changes_meV", {})
        shifts = " / ".join(f"{change[s]:.4f}" for s in SOLVES) if change else "—"
        labels = {"unmeasured": "нет измерения", "unresolved": "неопределённо",
                  "persistent_split": "устойчиво на двух сетках", "no_persistent_split": "не подтверждено"}
        lines.append(f"| {preset} | {labels[c['assessment']]} | {shifts} |")
    lines += ["", "| Сетка | Измерено | Статический отказ | Отказ по рисунку | Прошли оба порога |",
              "| ---: | ---: | ---: | ---: | ---: |"]
    for nz in GRIDS:
        statuses = [row["status"] for row in native.get("cases", []) if row["nz"] == nz]
        lines.append(f"| {nz} | {sum(s != 'technical_failure' for s in statuses)}/9 | "
                     f"{statuses.count('static_rejected')} | {statuses.count('figure_rejected')} | "
                     f"{statuses.count('figure_admitted')} |")
    lines += ["", "Сверка с опубликованными контролями 144 узлов — " + ("пройдена." if anchors_match else "требует разбора.") ]
    summary = {"complete_scientific_measurements": complete, "anchor_checks": controls,
               "cross_os_requested": args.require_cross, "anchor_checks_passed": anchors_match, "native_measured": measured,
               "native_reader_exit": grid_run.returncode, "portability": cross, "domain_errors": errors,
               "threshold_meV": rms_cut, "fine_change_limit_meV": FINE_CHANGE_MEV,
               "domain_records": paired, "fine_grid_comparisons": comparisons, "transport_current_A_cm2": None}
    (report / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    (report / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0 if complete and anchors_match else 1


if __name__ == "__main__":
    raise SystemExit(main())
