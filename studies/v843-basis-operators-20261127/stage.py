#!/usr/bin/env python3
"""Stage one HTCondor graph from a committed campaign checkout and a fresh slot inventory."""

import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import zipfile

STUDY = "studies/v843-basis-operators-20261127"
BUNDLE = (
    "runner/Project.toml", "runner/Manifest.toml", "runner/src", "runner/ext", STUDY,
    "studies/fath-v843/controls/v843-input/dupont",
    "studies/fath-v843/controls/fig1",
    "studies/cluster-eight-20261126/v843_native.jl",
)
CAMPAIGN = "v843-basis-operators-v1"


def command(*args, cwd=None):
    return subprocess.check_output(args, cwd=cwd)


def inventory():
    attrs = "Name,Machine,QCLWorkerId,OpSys,State,Cpus,Memory,TotalSlotCpus,TotalSlotMemory,Disk"
    slots = json.loads(command("condor_status", "-json", "-attributes", attrs,
                               "-constraint", "PartitionableSlot =?= true"))
    rows = []
    for slot in slots:
        system = slot.get("OpSys")
        if system not in {"WINDOWS", "LINUX"}:
            continue
        name = slot.get("QCLWorkerId") if system == "WINDOWS" else slot.get("Machine")
        if system == "WINDOWS" and name not in {f"qcl-win-{i}" for i in range(1, 7)}:
            continue
        if system == "LINUX" and name not in {"dell", "qcl-condor"}:
            continue
        rows.append({"id": name, "os": system, "machine": slot["Machine"],
                     "cpus": slot["TotalSlotCpus"], "memory_mib": slot["TotalSlotMemory"],
                     "free_cpus": slot["Cpus"], "free_memory_mib": slot["Memory"],
                     "disk_kib": slot["Disk"]})
    rows.sort(key=lambda slot: slot["id"])
    keys = [slot["id"] for slot in rows]
    if len(set(keys)) != len(keys):
        raise ValueError("Duplicate worker IDs")
    return rows


def submit(task, part, os_name, cpus, ram, parents, policy, revision):
    archive = "source.zip" if os_name == "WINDOWS" else "source.tar.gz"
    files = [archive, *(f"results/{p}.toml" for p in parents)]
    args = [task, str(cpus), "8"]
    if part:
        args.append(part)
    if os_name == "WINDOWS":
        executable = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
        transfer = "False"
        files.append("worker.ps1")
        args = ["-NoLogo", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "RemoteSigned",
                "-File", "worker.ps1", *args]
    else:
        executable, transfer = "worker.sh", "True"
    return f"""universe = vanilla
executable = {executable}
transfer_executable = {transfer}
arguments = "{' '.join(args)}"
getenv = False
requirements = {policy}
request_cpus = {cpus}
request_memory = {ram}MB
request_disk = 3072MB
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = {', '.join(files)}
transfer_output_files = summary.toml
transfer_output_remaps = "summary.toml=results/$(JOB).toml"
output = logs/$(JOB).out
error = logs/$(JOB).err
log = events.log
job_machine_attrs = Name, Machine, OpSys, Cpus, QCLWorkerId
job_machine_attrs_history_length = 1
+QCLCampaign = "{CAMPAIGN}"
+QCLDriverRevision = "{revision}"
+QCLArm = "$(JOB)"
queue 1
"""


def write_stage(source, run):
    revision = command("git", "rev-parse", "HEAD", cwd=source).decode().strip()
    if command("git", "status", "--porcelain", cwd=source):
        raise ValueError("Staging requires a committed checkout")
    rows = inventory()
    windows = [row for row in rows if row["os"] == "WINDOWS"]
    linux = [row for row in rows if row["id"] == "qcl-condor"]
    if not windows or not linux:
        raise ValueError("Both Windows and the Linux coordinator must advertise execute slots")
    win_cpu = {row["cpus"] for row in windows}
    if len(win_cpu) != 1:
        raise ValueError("Windows slots differ in CPU capacity; select submit requirements per capacity")
    host = linux[0]
    linux_cpu = host["cpus"]
    windows_cpu = win_cpu.pop()
    windows_ram = min(row["memory_mib"] for row in windows)
    if host["memory_mib"] < 16384 or windows_ram < 16384:
        raise ValueError("Insufficient advertised memory for campaign allocations")
    run.mkdir(mode=0o700)
    for folder in ("results", "logs", "site"):
        (run / folder).mkdir()
    (run / "revision").write_text(revision + "\n")
    (run / "inventory.json").write_text(json.dumps({"workers": rows}, indent=2) + "\n")
    archive = command("git", "archive", "--format=tar.gz", revision, "--", *BUNDLE, cwd=source)
    (run / "source.tar.gz").write_bytes(archive)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar, zipfile.ZipFile(
        run / "source.zip", "w", zipfile.ZIP_DEFLATED
    ) as zipped:
        for member in tar.getmembers():
            if member.isfile():
                zipped.writestr(member.name, tar.extractfile(member).read())
    for name in ("worker.sh", "worker.ps1", "gate.py", "collect.py", "finalize.sh", "launch.sh", "forecasts.md", "experiment-matrix.json"):
        shutil.copy2(source / STUDY / name, run / name)

    windows_policy = f'TARGET.OpSys == "WINDOWS" && TARGET.TotalSlotCpus == {windows_cpu} && regexp("^qcl-win-[1-6]$", TARGET.QCLWorkerId)'
    linux_policy = f'TARGET.OpSys == "LINUX" && TARGET.TotalSlotCpus == {linux_cpu} && TARGET.Machine == "qcl-condor"'
    if any(row["id"] == "dell" for row in rows):
        # SHIFT has nine independent combinations and does not need a full 28-CPU slot.
        shift_policy = 'TARGET.OpSys == "LINUX" && TARGET.Machine == "dell"'
    else:
        shift_policy = linux_policy
    matrix = []
    dag = []
    plan = json.loads((run / "experiment-matrix.json").read_text())
    for spec in plan["nodes"]:
        node, task, part, os_name = (spec[key] for key in ("node", "direction", "part", "os"))
        parents = tuple(spec["parents"])
        cpus = windows_cpu if os_name == "WINDOWS" else linux_cpu
        ram = 16384
        policy = windows_policy if os_name == "WINDOWS" else linux_policy
        if node in {"SHIFT", "SELECT"}:
            cpus, ram = (9, 4096) if node == "SHIFT" else (1, 4096)
            policy = shift_policy if node == "SHIFT" else linux_policy
        sub = f"site/{node}.sub"
        (run / sub).write_text(submit(task, part, os_name, cpus, ram, parents, policy, revision))
        matrix.append({"node": node, "direction": task, "part": part or None,
                       "parents": list(parents), "os": os_name, "cpus": cpus, "memory_mib": ram})
        dag.append(f"JOB {node} {sub}")
        predecessor = "SELECT" if node == "PILOT" else "PILOT" if node.startswith("T") else None
        if predecessor:
            dag.extend((f'SCRIPT PRE {node} /usr/bin/python3 gate.py {predecessor} {node}', f"PRE_SKIP {node} 42"))
    for name in ("LNX_PROBE", "WIN_PROBE"):
        os_name = "LINUX" if name == "LNX_PROBE" else "WINDOWS"
        cpus, policy = (linux_cpu, linux_policy) if os_name == "LINUX" else (windows_cpu, windows_policy)
        (run / f"site/{name}.sub").write_text(submit("PROBE", "", os_name, cpus, 4096, (), policy, revision))
    dag.extend(f"PARENT {' '.join(spec['parents'])} CHILD {spec['node']}"
               for spec in plan["nodes"] if spec["parents"])
    dag.extend(("PRIORITY B11 10", "PRIORITY SHIFT -10", "NODE_STATUS_FILE nodes.status 60",
                "FINAL COLLECT site/COLLECT.sub"))
    (run / "cluster.dag").write_text("\n".join(dag) + "\n")
    (run / "site/COLLECT.sub").write_text("""universe = local
executable = finalize.sh
output = logs/COLLECT.out
error = logs/COLLECT.err
log = events.log
queue 1
""")
    (run / "matrix.json").write_text(json.dumps(
        {"campaign": CAMPAIGN, "revision": revision, "nodes": matrix}, indent=2
    ) + "\n")
    hashes = ["source.tar.gz", "source.zip", "worker.sh", "worker.ps1", "collect.py", "gate.py",
              "finalize.sh", "launch.sh", "forecasts.md", "experiment-matrix.json", "matrix.json", "cluster.dag"]
    hashes += [f"site/{path.name}" for path in sorted((run / "site").glob("*.sub"))]
    (run / "inputs.sha256").write_text("".join(
        f"{hashlib.sha256((run / path).read_bytes()).hexdigest()}  {path}\n" for path in hashes
    ))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: stage.py NEW_RUN_DIRECTORY")
    write_stage(Path(__file__).resolve().parents[2], Path(sys.argv[1]).resolve())
