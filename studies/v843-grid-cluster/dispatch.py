#!/usr/bin/env python3
"""Prepare or collect the V843 grid without contacting a scheduler.

  python dispatch.py prepare WORK PACK --commit COMMIT --workers INVENTORY [--linux-only]
  python dispatch.py collect PACK WORK

WORK contains index.json and plans/<id>.json. COMMIT must contain this script,
worker.py and domain.jl. Prepare writes a fresh PACK; no git working-tree files
are used as source. PACK includes a DAG, isolated jobs, and editable site submit
files. INVENTORY lists idle partitionable workers and their measured resource
grants. A job requests all advertised CPUs of its selected worker, so campaign
jobs do not share that worker. The memory grant must fit the measured available
memory and the slot. OS weights follow the number of eligible workers.
--linux-python and --windows-python select the site executables.
On the submit host inspect site-*.sub: set the absolute executable path to
Python 3 on each OS, available CPUs/memory/disk, optional Julia/depot environment
and site requirements. Transfer is enabled, no shared output directories are used.
Use absolute WORK, PACK and analysis Python paths without spaces or special
characters. FINAL invokes collect and the committed finalize.py on the submit host,
even after failed jobs. The analysis Python must have its dependencies installed.
Submit the DAG only after site adaptation and pool inventory/capacity checks.
There is no automatic retry: retain failed archives/logs and choose a new attempt.

Julia 1.13.4 and a writable prepared depot are required on workers. Alternatively set
QCL_INSTANTIATE=1 in site environment and allow network for Julia Pkg; Manifest
must resolve its pinned published dependencies. Linux/Windows depots are separate.
--linux-only omits the Windows duplicate and marks cross-OS confirmation unavailable.
Collect after jobs terminate; it reports failures/missing files, never overwrites
existing output, and can be rerun after fixing or delivering missing results.
Successful process exit does not assert scientific stationarity or convergence.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import os
import re
import json
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile

IDS = [f'b{b}-r{r}-z{z}' for b in (7, 9, 11) for r in (7, 8, 11) for z in (96, 144, 216, 288)]
CONFIRM = 'b7-r7-z144'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def archive(commit):
    raw = subprocess.check_output(['git', 'archive', '--format=tar', commit])
    files = {}
    with tarfile.open(fileobj=io.BytesIO(raw)) as t:
        for m in t:
            if m.isdir():
                continue
            if not m.isfile():
                raise ValueError(f'unsupported source entry: {m.name}')
            if m.name.startswith('studies/v843-grid-cluster/evidence/'):
                continue
            if not (m.name.startswith(('runner/', 'analysis/src/', 'studies/v843-spectrum/', 'studies/v843-grid-cluster/')) or m.name == 'studies/fath-v843/controls/fig1/fig1_profiles.csv'):
                continue
            files[m.name] = t.extractfile(m).read()
    required = ('runner/Project.toml', 'runner/Manifest.toml', 'runner/bin/qcl-negf',
                'studies/v843-grid-cluster/worker.py', 'studies/v843-grid-cluster/domain.jl')
    for name in required:
        if name not in files:
            raise ValueError(f'commit lacks {name}; commit all campaign source first')
    worker = files['studies/v843-grid-cluster/worker.py']
    if worker != Path(__file__).with_name('worker.py').read_bytes():
        raise ValueError('the archived worker must match the dispatch checkout')
    # The only permitted path entry is the project package itself, relative to runner/.
    paths = re.findall(rb'^path\s*=\s*"([^"]+)"', files['runner/Manifest.toml'], re.M)
    if paths != [b'.']:
        raise ValueError('Manifest contains an unexpected local path dependency')
    files['source-catalog.json'] = (json.dumps({k: sha(v) for k, v in sorted(files.items())}, indent=2) + '\n').encode()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as z:
        for name, data in sorted(files.items()):
            z.writestr(name, data)
    return buf.getvalue(), worker


def load_workers(inventory, linux_only):
    rows = json.loads(inventory.read_text(encoding='utf-8'))
    workers = {'linux': [], 'windows': []}
    seen = set()
    if not isinstance(rows, list) or not rows:
        raise ValueError('worker inventory must be a non-empty JSON list')
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('expected an object for each worker')
        os_name = row.get('os')
        domain = row.get('filesystem_domain')
        if (os_name not in ('linux', 'windows') or not isinstance(domain, str)
                or not re.fullmatch(r'[A-Za-z0-9_.-]+', domain) or domain in seen):
            raise ValueError(f'expected a unique, portable worker domain and a supported OS: {row}')
        for key in ('cpus', 'memory_mib'):
            if type(row.get(key)) is not int or row[key] < 1:
                raise ValueError(f'{key} must be a positive integer for {domain}')
        seen.add(domain)
        workers[os_name].append(row)
    if not workers['linux'] or linux_only != (not workers['windows']):
        raise ValueError('a Linux worker is required; use --linux-only for an all-Linux inventory')
    return workers


def prepare(work, pack, commit, linux_only, analysis_python, inventory, linux_python, windows_python):
    work, pack = work.resolve(), pack.resolve()
    analysis_python = Path(os.path.abspath(analysis_python))
    if not analysis_python.is_file():
        raise ValueError('analysis Python does not exist on submit host')
    for path in (work, pack, analysis_python):
        if not re.fullmatch(r'[A-Za-z0-9_./-]+', str(path)):
            raise ValueError(f'Use portable absolute paths without spaces or special characters: {path}')
    workers = load_workers(inventory, linux_only)
    linux_weight, windows_weight = len(workers['linux']), len(workers['windows'])
    for executable in (linux_python, windows_python):
        if not re.fullmatch(r'[A-Za-z0-9_./:-]+', executable):
            raise ValueError('worker Python paths must use portable characters and forward slashes')
    index = json.loads((work / 'index.json').read_text(encoding='utf-8'))
    cases = index['cases']
    if len(cases) != len(IDS) or {x['id'] for x in cases} != set(IDS):
        raise ValueError('index must contain exactly the 36 grid IDs')
    plans = {i: (work / 'plans' / (i + '.json')).read_bytes() for i in IDS}
    for i, data in plans.items():
        json.loads(data)
    revision = subprocess.check_output(['git', 'rev-parse', '--verify', commit + '^{commit}'], text=True).strip()
    source, worker = archive(revision)
    pack.mkdir(parents=True, exist_ok=False)
    for name in ('jobs', 'plans', 'returned', 'logs'):
        (pack / name).mkdir()
    (pack / 'source.zip').write_bytes(source)
    (pack / 'worker.py').write_bytes(worker)
    with zipfile.ZipFile(io.BytesIO(source)) as z:
        z.extractall(pack / 'finalizer-source')
    final_script = pack / 'finalizer-source/studies/v843-grid-cluster/finalize.py'
    if not final_script.is_file():
        raise ValueError('commit lacks studies/v843-grid-cluster/finalize.py')
    for i, data in plans.items():
        (pack / 'plans' / (i + '.json')).write_bytes(data)
    jobs = []
    # Weighted fair assignment approximates the available 2-CPU slot counts.
    counts = {'linux': 1, 'windows': 0}
    def assign():
        if linux_only:
            return 'linux'
        chosen = 'linux' if counts['linux'] / linux_weight <= counts['windows'] / windows_weight else 'windows'
        counts[chosen] += 1
        return chosen
    for i in IDS:
        jobs.append((i, i, 'solver', '', 'linux' if i == CONFIRM else assign()))
    if not linux_only:
        jobs.append(('confirm-' + CONFIRM, CONFIRM, 'confirm', '', 'windows'))
    for b, preset in ((9, 'w11-wannier-proxy'), (11, 'b11-pzp')):
        for nz in (96, 144, 216, 288):
            i = f'b{b}-r11-z{nz}'
            jobs.append(('domain-' + i, i, 'domain', preset, assign()))
    dag = []
    records = []
    worker_counts = {'linux': 0, 'windows': 0}
    for name, case, kind, preset, osname in jobs:
        eligible = workers[osname]
        slot = eligible[worker_counts[osname] % len(eligible)]
        worker_counts[osname] += 1
        domain, cpus, memory = slot['filesystem_domain'], slot['cpus'], slot['memory_mib']
        job = {'name': name, 'case': case, 'kind': kind, 'preset': preset,
               'source_commit': revision, 'source_sha256': sha(source), 'plan_sha256': sha(plans[case]),
               'target_os': osname, 'request_cpus': cpus, 'request_memory_mib': memory}
        records.append(job)
        (pack / 'jobs' / ('job-' + name + '.json')).write_text(json.dumps(job, indent=2) + '\n', encoding='utf-8')
        dag += [f'JOB {name} site-{osname}.sub',
                f'VARS {name} job="{name}" case="{case}" worker="{domain}" cpus="{cpus}" memory="{memory}"']
    dag.append('FINAL FINALIZE final.sub')
    final_sub = f'''universe = local
executable = {analysis_python}
arguments = {pack}/finalizer-source/studies/v843-grid-cluster/dispatch.py final {pack} {work}
output = logs/final.out
error = logs/final.err
log = logs/final.log
queue 1
'''
    (pack / 'final.sub').write_text(final_sub, encoding='utf-8')
    (pack / 'campaign.dag').write_text('\n'.join(dag) + '\n', encoding='utf-8')
    manifest = {'commit': revision, 'resource_policy': 'full-machine',
                'cross_os_requested': not linux_only, 'jobs': records}
    (pack / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    for osname, condor_os, python in [('linux', 'LINUX', linux_python), ('windows', 'WINDOWS', windows_python)]:
        if not workers[osname]:
            continue
        # Paths are simple relative names. HTCondor transfers basename inputs to scratch.
        submit = f'''# Verify the site paths, transfer settings and requirements before use.
# Python and Julia must be installed on each matching execute worker.
universe = vanilla
executable = {python}
transfer_executable = FALSE
arguments = worker.py source.zip $(case).json job-$(job).json result-$(job).zip
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = worker.py, source.zip, plans/$(case).json, jobs/job-$(job).json
transfer_output_files = result-$(job).zip
transfer_output_remaps = "result-$(job).zip=returned/$(job).zip"
output = logs/$(job).out
error = logs/$(job).err
log = logs/$(job).log
request_cpus = $(cpus)
request_memory = $(memory)MB
request_disk = 4096MB
requirements = (TARGET.OpSys == "{condor_os}") && (TARGET.FileSystemDomain == "$(worker)")
# environment = "QCL_JULIA=... QCL_INSTANTIATE=1 JULIA_DEPOT_PATH=..."
queue 1
'''
        (pack / f'site-{osname}.sub').write_text(submit, encoding='utf-8')
    print(f'Prepared {len(jobs)} jobs at {pack}, commit {revision}; no scheduler invoked.')


def collect(pack, work):
    pack, work = pack.resolve(), work.resolve()
    manifest = json.loads((pack / 'manifest.json').read_text(encoding='utf-8'))
    errors = []
    for job in manifest['jobs']:
        name, case = job['name'], job['case']
        source = pack / 'returned' / (name + '.zip')
        try:
            with zipfile.ZipFile(source) as z:
                status = json.loads(z.read('status.json'))
                if status['job'] != job or status['plan_sha256'] != job['plan_sha256'] or not status['ok']:
                    raise ValueError('failed job or inconsistent status')
                prefix = 'result/'
                files = [x for x in z.namelist() if x.startswith(prefix) and not x.endswith('/')]
                if not files:
                    raise ValueError('empty result')
                for f in files:
                    p = PurePosixPath(f)
                    if p.is_absolute() or '..' in p.parts or '\\' in f or ':' in f:
                        raise ValueError('unsafe result path')
                if job['kind'] == 'domain':
                    if files != ['result/domain.toml']:
                        raise ValueError('unexpected domain result')
                    dest = work / 'domains' / (case + '.toml')
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    data = z.read(files[0])
                    if dest.exists():
                        if dest.read_bytes() != data:
                            raise FileExistsError(f'{dest} differs from returned result')
                    else:
                        with dest.open('xb') as out:
                            out.write(data)
                else:
                    dest = work / ('crosscheck' if job['kind'] == 'confirm' else 'results') / case
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    if dest.exists():
                        expected = {PurePosixPath(f).relative_to('result').as_posix(): sha(z.read(f)) for f in files}
                        actual = {p.relative_to(dest).as_posix(): sha(p.read_bytes()) for p in dest.rglob('*') if p.is_file()}
                        if expected != actual:
                            raise FileExistsError(f'{dest} differs from returned result')
                        print(f'Already collected {name}')
                        continue
                    with tempfile.TemporaryDirectory(dir=dest.parent) as temp:
                        tmp = Path(temp) / 'result'
                        for f in files:
                            p = tmp.joinpath(*PurePosixPath(f).parts[1:])
                            p.parent.mkdir(parents=True, exist_ok=True)
                            p.write_bytes(z.read(f))
                        tmp.rename(dest)
            print(f'Collected {name}')
        except (OSError, ValueError, KeyError, zipfile.BadZipFile) as e:
            errors.append(f'{name}: {e}')
    if not manifest['cross_os_requested']:
        print('Cross-OS confirmation unavailable: Linux-only pack.', file=sys.stderr)
    for error in errors:
        print(error, file=sys.stderr)
    return bool(errors)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='command', required=True)
    prep = sub.add_parser('prepare')
    prep.add_argument('work', type=Path)
    prep.add_argument('pack', type=Path)
    prep.add_argument('--commit', required=True)
    prep.add_argument('--linux-only', action='store_true')
    prep.add_argument('--workers', type=Path, required=True, help='private JSON inventory of whole-worker grants')
    prep.add_argument('--linux-python', default='/EDIT/PATH/TO/PYTHON')
    prep.add_argument('--windows-python', default='C:/EDIT/PATH/TO/PYTHON.EXE')
    prep.add_argument('--analysis-python', default=sys.executable, help='absolute Python executable on submit host, with analysis dependencies')
    coll = sub.add_parser('collect')
    coll.add_argument('pack', type=Path)
    coll.add_argument('work', type=Path)
    final = sub.add_parser('final', help=argparse.SUPPRESS)
    final.add_argument('pack', type=Path)
    final.add_argument('work', type=Path)
    args = p.parse_args()
    if args.command == 'prepare':
        prepare(args.work, args.pack, args.commit, args.linux_only, args.analysis_python, args.workers, args.linux_python, args.windows_python)
        return 0
    if args.command == 'final':
        try:
            collect_failed = collect(args.pack, args.work)
        except Exception as e:
            print(f'Collection failed: {e}', file=sys.stderr)
            collect_failed = True
        script = args.pack / 'finalizer-source/studies/v843-grid-cluster/finalize.py'
        command = [sys.executable, str(script), str(args.work)]
        try:
            if json.loads((args.pack / 'manifest.json').read_text(encoding='utf-8'))['cross_os_requested']:
                command.append('--require-cross')
        except Exception as e:
            print(f'Cannot read cross-OS policy: {e}', file=sys.stderr)
            collect_failed = True
            command.append('--require-cross')
        result = subprocess.run(command)
        return int(bool(collect_failed or result.returncode))
    return int(collect(args.pack, args.work))

if __name__ == '__main__':
    sys.exit(main())
