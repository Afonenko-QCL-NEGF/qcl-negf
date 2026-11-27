#!/usr/bin/env python3
"""Read the published DAG 66 archive and reconstruct a checksummed summary."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tomllib


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        canonical = str(key)
        if canonical in result:
            raise ValueError(f"duplicate JSON key {canonical!r}")
        result[canonical] = value
    return result


def checked_payload(archive, reference, digest):
    relative = PurePosixPath(reference)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("archive reference must stay inside the archive")
    path = (archive / relative).resolve(strict=True)
    if not path.is_relative_to(archive):
        raise ValueError("archive reference resolves outside the archive")
    payload = path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != digest:
        raise ValueError(f"archive checksum mismatch: {reference}")
    return payload


def collect(archive):
    archive = archive.resolve(strict=True)
    inventory = unique_object(
        (path, digest)
        for digest, path in (line.split(maxsplit=1)
                             for line in (archive / "SHA256SUMS").read_text().splitlines())
    )
    inputs = {}

    def read(reference):
        payload = checked_payload(archive, reference, inventory[reference])
        if reference.endswith(".json"):
            return json.loads(payload, object_pairs_hook=unique_object)
        return tomllib.loads(payload.decode())

    summary = read("summary.json")
    matrix = read("matrix.json")
    if summary["dagman_job_id"] != "66.0" or summary["driver_revision"] != matrix["revision"]:
        raise ValueError("archive must identify the published DAG 66 source")
    for node in matrix["nodes"]:
        name = node["node"]
        if name in inputs:
            raise ValueError(f"duplicate DAG node {name}")
        entry = summary["cases"][name]
        reference = entry["artifact"]
        if inventory[reference] != entry["artifact_sha256"]:
            raise ValueError(f"inconsistent inventory for {name}")
        data = read(reference)
        if data.get("task") != node["direction"] or data.get("status") != entry["status"]:
            raise ValueError(f"result identity or terminal status differs for {name}")
        inputs[name] = (reference, data)
    select = inputs["SELECT"][1]
    skips = [node for node, (_, item) in inputs.items() if item["status"] == "skipped_by_gate"]
    if select["status"] != "rejected" or select["qualified"] or select["expansion_checks"]:
        raise ValueError("DAG 66 must have rejected SELECT and no window confirmations")
    children = [node["node"] for node in matrix["nodes"] if "SELECT" in node["parents"]]
    if set(skips) != set(children) or len(skips) != 5:
        raise ValueError("DAG 66 must have five skipped SELECT descendants")
    for node in skips:
        if set(inputs[node][1]) != {"task", "status", "qualified", "reason"} or inputs[node][1]["qualified"]:
            raise ValueError(f"unexpected observable or qualification on skipped node {node}")

    # The native identifier is an integer. JSON object keys are strings; check
    # collisions while forming the mapping, before any value can be overwritten.
    bloch = unique_object(
        (grid["spatial_nodes"], grid["minimum_gap_meV"])
        for node in matrix["nodes"] if node["direction"] == "BLOCH"
        for grid in inputs[node["node"]][1]["grids"]
    )
    if set(bloch) != {"144", "288"}:
        raise ValueError("archive must contain Bloch grids 144 and 288")
    return {
        "dagman_job_id": summary["dagman_job_id"],
        "driver_revision": matrix["revision"],
        "selection": {
            "source": {"output": "SELECT", "representation": inputs["SELECT"][0]},
            "status": select["status"],
            "reason": select["reason"],
            "candidates": [
                {"rank": row["rank"], "window_periods": row["window_periods"], "status": row["status"]}
                for row in select["candidates"]
            ],
        },
        "bloch_minimum_gap_meV": bloch,
        "skipped": {
            node: {"output": node, "representation": inputs[node][0], "reason": inputs[node][1]["reason"]}
            for node in skips
        },
        "transport_current_A_cm2": None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    print(json.dumps(collect(args.archive), indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
