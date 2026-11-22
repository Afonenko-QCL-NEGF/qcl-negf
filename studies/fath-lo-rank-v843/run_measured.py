#!/usr/bin/env python3
"""Run the Julia CLI and record CPU, RAM and job writes, including temporary writes."""
import json
import os
from pathlib import Path
import subprocess
import sys
import time


def run(receipt, command):
    start = time.monotonic()
    child = subprocess.Popen(command)
    while True:
        try:
            # Observe the final process I/O counters before releasing the process.
            result = os.waitid(os.P_PID, child.pid, os.WEXITED | os.WNOHANG | os.WNOWAIT)
            if result is not None:
                break
        except InterruptedError:
            continue
        time.sleep(2)

    counters = {}
    try:
        for line in Path(f"/proc/{child.pid}/io").read_text().splitlines():
            key, raw = line.split()
            counters[key.rstrip(":")] = int(raw)
    except OSError:
        pass
    _, status, usage = os.wait4(child.pid, 0)
    child.returncode = os.waitstatus_to_exitcode(status)
    data = {
        "command": command,
        "exit_code": child.returncode,
        "elapsed_seconds": time.monotonic() - start,
        "cpu_user_seconds": usage.ru_utime,
        "cpu_system_seconds": usage.ru_stime,
        "peak_rss_KiB": usage.ru_maxrss,
        "file_output_blocks": usage.ru_oublock,
        "proc_io_bytes": counters,
    }
    receipt.write_text(json.dumps(data, indent=2) + "\n")
    return child.returncode


if __name__ == "__main__":
    sys.exit(run(Path(sys.argv[1]), sys.argv[2:]))
