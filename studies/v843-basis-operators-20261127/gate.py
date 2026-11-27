#!/usr/bin/env python3
"""Read the scientific parent's explicit verdict for a conditional DAGMan node."""

import json
from pathlib import Path
import sys
import tomllib

parent, child = sys.argv[1:]
if not (parent == "SELECT" and child == "PILOT" or parent == "PILOT" and
        child in ("T17A32", "T17A128", "T33A32", "T33A128")):
    raise ValueError(f"Unknown DAG gate: {parent} -> {child}")
with (Path("results") / f"{parent}.toml").open("rb") as stream:
    verdict = tomllib.load(stream)
if verdict.get("task") != parent or type(verdict.get("qualified")) is not bool:
    raise ValueError(f"Missing explicit verdict from {parent}")
if verdict["qualified"]:
    sys.exit(0)
out = Path("results") / f"{child}.toml"
temporary = out.with_suffix(".tmp")
message = f"{parent} did not qualify; see results/{parent}.toml"
temporary.write_text(
    f'task = "{child}"\nstatus = "skipped_by_gate"\nqualified = false\n'
    f'reason = {json.dumps(message)}\n'
)
temporary.replace(out)
sys.exit(42)
