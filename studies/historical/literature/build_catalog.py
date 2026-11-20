"""Validate the canonical literature catalog and render the BibTeX index."""
import argparse
import csv
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
STATUS = {"read_full", "abstract_only", "metadata_only", "unavailable"}
REQUIRED = {
    "id", "authors", "title", "year", "venue", "doi", "arxiv", "url",
    "full_text_url", "access", "checked_on", "topics", "locator", "annotation",
    "rights", "version_relation", "inspection_extent",
}


def catalog():
    records = [
        json.loads(line) for line in (ROOT / "catalog.jsonl").read_text().splitlines()
        if line
    ]
    identifiers = []
    for record in records:
        assert REQUIRED <= record.keys(), record
        assert record["access"] in STATUS, record
        assert record["authors"] and record["topics"] and record["locator"], record
        assert record["url"].startswith("https://"), record
        assert record["full_text_url"] or record["access"] != "read_full", record
        assert re.fullmatch(r"[a-z0-9-]+", record["id"]), record
        identifiers.append(("id", record["id"]))
        if record["doi"]:
            identifiers.append(("doi", record["doi"].lower()))
        if record["arxiv"]:
            identifiers.append(("arxiv", re.sub(r"v\d+$", "", record["arxiv"])))
    assert len(set(identifiers)) == len(identifiers), "duplicate identifier"
    return records


def bibtex(records):
    blocks = []
    for record in records:
        kind = "article" if record["year"] else "misc"
        fields = {
            "author": " and ".join(record["authors"]),
            "title": "{" + record["title"] + "}",
            "year": record["year"],
            "journal" if kind == "article" else "howpublished": record["venue"],
            "doi": record["doi"],
            "eprint": record["arxiv"],
            "archivePrefix": "arXiv" if record["arxiv"] else None,
            "url": record["url"],
        }
        rows = [f"  {key} = {{{value}}}" for key, value in fields.items() if value]
        blocks.append(f"@{kind}{{{record['id']},\n" + ",\n".join(rows) + "\n}")
    return "\n\n".join(blocks) + "\n"


def check_references(records):
    keys = {record["id"] for record in records}
    for filename in ("methods-matrix.csv", "code-traceability.csv"):
        with (ROOT / "mappings" / filename).open() as stream:
            rows = list(csv.DictReader(stream))
        assert rows, filename
        for row in rows:
            assert None not in row and all(row.values()), (filename, row)
            assert set(row["source_ids"].split(";")) <= keys, (filename, row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="regenerate catalog.bib")
    args = parser.parse_args()
    records = catalog()
    path = ROOT / "catalog.bib"
    expected = bibtex(records)
    if args.write:
        path.write_text(expected)
    else:
        assert path.read_text() == expected, "catalog.bib differs from catalog.jsonl"
        check_references(records)
        print(f"{len(records)} unique catalog records; BibTeX and mapping references verified")
