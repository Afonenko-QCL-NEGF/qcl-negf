#!/usr/bin/env python3
"""Extract resource totals without workstation paths or commands."""
import json
from pathlib import Path
import sys

log_dir = Path(sys.argv[1])
out = Path(sys.argv[2])
wanted = {
    "User time (seconds)": "cpu_user_seconds",
    "System time (seconds)": "cpu_system_seconds",
    "Maximum resident set size (kbytes)": "peak_rss_KiB",
    "File system outputs": "filesystem_output_blocks",
    "Exit status": "exit_code",
}
report = {}
for path in sorted(log_dir.glob("*.resources")):
    details = {}
    for line in path.read_text().splitlines():
        stripped = line.strip()
        for source, field in wanted.items():
            label = source + ": "
            if stripped.startswith(label):
                details[field] = float(stripped.removeprefix(label))
        if stripped.startswith("Elapsed (wall clock) time (h:mm:ss or m:ss): "):
            parts = stripped.rsplit(" ", 1)[-1].split(":")
            details["wall_seconds"] = sum(float(x)*60**i for i,x in enumerate(reversed(parts)))
    if details:
        report[path.stem] = details
out.write_text(json.dumps(report,indent=2)+"\n")
