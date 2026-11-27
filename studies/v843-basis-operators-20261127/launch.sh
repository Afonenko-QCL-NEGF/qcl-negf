#!/usr/bin/env bash
# Run only on the submit host from a staged directory after the native probes.
set -euo pipefail
umask 077
revision=$(cat revision)
[[ $revision =~ ^[0-9a-f]{40}$ ]]
run=$(pwd -P)
exec 8>launch.lock
flock -n 8

parent="JobUniverse == 7 && Iwd == \"$run\""
children='QCLCampaign == "v843-basis-operators-v1"'
find_existing() {
    {
        condor_q -allusers -constraint "$parent" -af ClusterId
        condor_history -constraint "$parent" -limit 100 -af ClusterId
        condor_q -allusers -constraint "$children" -af DAGManJobId
        condor_history -constraint "$children" -limit 150 -af DAGManJobId
    } | awk '/^[0-9]+$/ && $0>0' | sort -un
}
existing=$(find_existing)
if [[ $existing == *$'\n'* ]]; then
    printf 'Multiple matching DAG IDs. Resolve before submitting.\n%s\n' "$existing" >&2
    exit 7
fi
if [[ -f submission.json ]]; then
    expected=$(python3 -c 'import json; d=json.load(open("submission.json")); print(d["dagman_job_id"].split(".")[0])')
    [[ $expected == "$existing" ]]
    cat submission.json
    exit 0
fi
if [[ -n $existing ]]; then
    id=$existing
else
    test ! -e cluster.dag.condor.sub
    sha256sum --check inputs.sha256 > verified-inputs.log
    python3 - <<'PY'
import json
from pathlib import Path
import subprocess
import tomllib

required = {"LNX_PROBE": "LINUX", "WIN_PROBE": "WINDOWS"}
ids = json.loads(Path("probe-ids.json").read_text())
for name, system in required.items():
    record = tomllib.loads(Path(f"results/{name}.toml").read_text())
    history = subprocess.check_output(
        ["condor_history", ids[name], "-limit", "1", "-af", "JobStatus", "ExitCode"], text=True
    ).split()
    if history != ["4", "0"] or record["status"] != "measured" or record["runtime"]["op_sys"] != system:
        raise ValueError(f"{name} has not passed on {system}")
    if record["runtime"]["allocated_cpus"] != record["runtime"]["julia_threads"]:
        raise ValueError(f"{name}: Julia thread count differs from the slot request")
PY
    condor_submit_dag cluster.dag > submission.log 2>&1 || { cat submission.log; exit 9; }
    cat submission.log
    id=$(sed -nE 's/.*submitted to cluster ([0-9]+).*/\1/p' submission.log | tail -1)
    [[ -n $id ]] || id=$(find_existing)
fi
[[ $id =~ ^[0-9]+$ ]]
observed=
for ((attempt=0;attempt<12;attempt++)); do
    observed=$(condor_q "$id.0" -constraint 'JobUniverse == 7' -af:t Iwd JobStatus)
    if [[ -z $observed ]]; then
        observed=$(condor_history "$id.0" -constraint 'JobUniverse == 7' -limit 1 -af:t Iwd JobStatus)
    fi
    [[ -z $observed ]] || break
    sleep 1
done
read -r native_directory job_status <<<"$observed"
[[ -n $native_directory && -n $job_status ]]
if [[ $native_directory != "$run" ]]; then
    printf 'Existing DAG %s.0 in %s\n' "$id" "$native_directory"
    test -f "$native_directory/submission.json"
    cat "$native_directory/submission.json"
    exit 0
fi
python3 - "$id" "$revision" "$job_status" <<'PY'
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys

id_, revision, status = sys.argv[1:]
run = Path.cwd()
inventory = json.loads(Path("inventory.json").read_text())
receipt = {
    "state": "accepted_by_schedd",
    "campaign": "v843-basis-operators-v1",
    "dagman_job_id": id_ + ".0",
    "driver_revision": revision,
    "plan_revision": "7202e8c5768fab4e12c0dadd66581bf3fe3ce6b3",
    "job_status": int(status),
    "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
    "workers_at_stage": len(inventory["workers"]),
    "worker_cpu_capacity": {row["id"]: row["cpus"] for row in inventory["workers"]},
    "run_directory": str(run),
    "event_log": str(run / "events.log"),
    "dagman_log": str(run / "cluster.dag.dagman.log"),
    "node_status_file": str(run / "nodes.status"),
    "results_directory": str(run / "results"),
    "publication_directory": str(run / "publication"),
    "dag_sha256": sha256((run / "cluster.dag").read_bytes()).hexdigest(),
}
temp = Path("submission.json.tmp")
text = json.dumps(receipt, indent=2) + "\n"
temp.write_text(text)
temp.replace("submission.json")
print(text, end="")
PY
