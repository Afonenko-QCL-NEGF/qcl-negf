#!/usr/bin/env python3
"""Create independent native Runner studies from the published V843 B7 input."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

REPO = Path(__file__).resolve().parents[2]
SOURCE = REPO / "studies/v843-spectrum/b7.yaml"
CATALOG = SOURCE.with_name("devices.yaml")


def replace_once(text: str, old: str, new: str) -> str:
    if text.count(old) != 1:
        raise ValueError(f"expected exactly one occurrence of {old!r} in B7")
    return text.replace(old, new, 1)


def verify_catalog() -> None:
    # Verify both the location and the actual content of the published sources.
    text = CATALOG.read_text(encoding="utf-8")
    entries = re.findall(r"^    - path: (.+)\n      sha256: ([0-9a-f]{64})$", text, re.M)
    if len(entries) != 2 or "  dupont-v843:\n" not in text:
        raise ValueError("unexpected V843 device catalog")
    for relative, expected in entries:
        source = (CATALOG.parent / relative).resolve(strict=True)
        if hashlib.sha256(source.read_bytes()).hexdigest() != expected:
            raise ValueError(f"device source hash mismatch: {source}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", help="new output directory inside the application checkout")
    parser.add_argument("--freeze", action="store_true",
                        help="resolve all studies into frozen Runner plans using Julia")
    args = parser.parse_args()
    root = Path(args.output).resolve()
    if root == REPO or not root.is_relative_to(REPO):
        parser.error("output must be a new directory inside the application checkout")
    if root.exists():
        parser.error("output already exists; choose a fresh directory")
    verify_catalog()
    template = SOURCE.read_text(encoding="utf-8")
    # Fail before creating the output if the published source contract changes.
    for old in ("id: dupont-v843-b7\n", "  catalog: devices.yaml\n",
                "      spatial_nodes: 144\n", "      basis_states: 7\n",
                "      basis_periods: 3\n"):
        if template.count(old) != 1:
            raise ValueError(f"unexpected B7 source: {old!r}")
    root.mkdir(parents=True, exist_ok=False)
    cases = []
    for window, periods in ((7, 3), (9, 4), (11, 5)):
        for rank in (7, 8, 11):
            for nz in (96, 144, 216, 288):
                case_id = f"b{window}-r{rank}-z{nz}"
                case_dir = root / case_id
                case_dir.mkdir()
                catalog = Path(os.path.relpath(CATALOG, case_dir)).as_posix()
                if (case_dir / catalog).resolve(strict=True) != CATALOG.resolve(strict=True):
                    raise ValueError("catalog path does not resolve to published catalog")
                study = replace_once(template, "id: dupont-v843-b7\n", f"id: {case_id}\n")
                study = replace_once(study, "name: Dupont V843 B7 static spectrum\n",
                                     f"name: Dupont V843 {case_id} static spectrum\n")
                study = replace_once(study, "  catalog: devices.yaml\n", f"  catalog: {catalog}\n")
                study = replace_once(study, "      spatial_nodes: 144\n", f"      spatial_nodes: {nz}\n")
                study = replace_once(study, "      basis_states: 7\n", f"      basis_states: {rank}\n")
                study = replace_once(study, "      basis_periods: 3\n", f"      basis_periods: {periods}\n")
                path = case_dir / "study.yaml"
                path.write_text(study, encoding="utf-8")
                cases.append({"id": case_id, "window": window, "rank": rank,
                              "nz": nz, "study": path.relative_to(root).as_posix()})
    (root / "index.json").write_text(json.dumps({"cases": cases}, indent=2) + "\n", encoding="utf-8")
    print(f"Created {len(cases)} studies in {root}", flush=True)
    if args.freeze:
        plans = root / "plans"
        plans.mkdir()
        project = str(REPO / "runner")
        julia = os.environ.get("JULIA", "julia")
        # Arguments go directly to Julia, avoiding shell quoting and platform differences.
        script = r'''
using QCLNEGFRunner
plans = ARGS[1]
for study in ARGS[2:end]
    id = basename(dirname(study))
    plan = resolve_scientific_plan(study; maximum_solver_runs=1)
    open(joinpath(plans, id * ".json"), "w") do io
        write_scientific_plan(io, plan)
    end
    load_scientific_plan(joinpath(plans, id * ".json"))
    println("Frozen and verified ", id)
end
'''
        subprocess.run([julia, "--compiled-modules=existing", "--startup-file=no", f"--project={project}", "-e", script,
                        str(plans), *(str(root / case["study"]) for case in cases)], check=True)
        print(f"Created {len(cases)} frozen plans in {plans}")


if __name__ == "__main__":
    main()
