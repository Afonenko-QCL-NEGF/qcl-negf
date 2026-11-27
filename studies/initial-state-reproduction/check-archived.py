"""Verify available payload roles in an archived QCL study without loading arrays."""
import argparse
import hashlib
import json
from pathlib import Path
import tomllib


def main():
    catalog_path = Path(__file__).with_name("archived-inputs.toml")
    catalog = tomllib.loads(catalog_path.read_text(encoding="utf-8"))
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset", choices=catalog["datasets"])
    parser.add_argument("files", metavar="ROLE=FILE", nargs="*")
    args = parser.parse_args()
    dataset = catalog["datasets"][args.dataset]
    roles = dataset["roles"]
    supplied = {}
    for value in args.files:
        role, sep, path = value.partition("=")
        if not sep or not path or role not in roles or role in supplied:
            parser.error(f"unexpected, empty or repeated role: {value}")
        supplied[role] = Path(path)

    results = {}
    for role, record in roles.items():
        path = supplied.get(role)
        if path is None or not path.is_file():
            results[role] = {"status": "missing", "expected_sha256": record["sha256"]}
            continue
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        results[role] = {
            "status": "verified" if digest == record["sha256"] else "mismatch",
            "expected_sha256": record["sha256"],
            "sha256": digest,
        }
    statuses = {value["status"] for value in results.values()}
    print(json.dumps({"dataset": args.dataset, "roles": results}, indent=2))
    if "mismatch" in statuses:
        return 2
    return int("missing" in statuses)


if __name__ == "__main__":
    raise SystemExit(main())
