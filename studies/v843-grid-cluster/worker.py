#!/usr/bin/env python3
"""Run one isolated job: worker.py SOURCE.zip PLAN.json JOB.json OUTPUT.zip.

Julia must be on PATH; QCL_JULIA optionally names it. QCL_INSTANTIATE=1 permits
Pkg.instantiate() in a writable depot; otherwise a prepared depot is required.
A result archive is produced even on failure, with status.json and partial output.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import platform
import subprocess
import sys
import tempfile
import time
import traceback
import zipfile


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def safe_extract(z, dest):
    for item in z.infolist():
        name = PurePosixPath(item.filename)
        if name.is_absolute() or '..' in name.parts or '\\' in item.filename or ':' in item.filename:
            raise ValueError('unsafe archive path')
    z.extractall(dest)


def main():
    if len(sys.argv) != 5:
        raise SystemExit(__doc__)
    source, plan, jobfile, output = map(Path, sys.argv[1:])
    job = json.loads(jobfile.read_text(encoding='utf-8'))
    status = {'job': job, 'platform': platform.platform(), 'python': sys.version, 'ok': False,
              'logical_cpus_visible': os.cpu_count()}
    if hasattr(os, 'sched_getaffinity'):
        status['affinity_cpus'] = len(os.sched_getaffinity(0))
    started = time.monotonic()
    output = output.resolve()
    with tempfile.TemporaryDirectory(prefix='qcl-job-') as temp:
        root = Path(temp)
        try:
            expected_os = {'linux': 'Linux', 'windows': 'Windows'}[job['target_os']]
            if platform.system() != expected_os:
                raise ValueError(f'wrong OS: expected {expected_os}, got {platform.system()}')
            if sha(source) != job['source_sha256'] or sha(plan) != job['plan_sha256']:
                raise ValueError('input checksum mismatch')
            with zipfile.ZipFile(source) as z:
                safe_extract(z, root / 'source')
            app = root / 'source'
            catalog = json.loads((app / 'source-catalog.json').read_text(encoding='utf-8'))
            for name, digest in catalog.items():
                path = PurePosixPath(name)
                if path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name:
                    raise ValueError('unsafe catalog path')
                if sha(app.joinpath(*path.parts)) != digest:
                    raise ValueError(f'source checksum mismatch: {name}')
            frozen = root / 'plan.json'
            frozen.write_bytes(plan.read_bytes())
            cpus = job['request_cpus']
            visible = status.get('affinity_cpus') or status['logical_cpus_visible']
            if type(cpus) is not int or cpus < 1 or (visible is not None and cpus > visible):
                raise ValueError(f'invalid CPU grant ({cpus}) for available CPUs ({visible})')
            status.update(julia_threads_requested=1, blas_threads_requested=cpus)
            if expected_os == 'Windows':
                home = root / 'julia-home'
                home.mkdir()
                os.environ.update(HOME=str(home), USERPROFILE=str(home))
                if 'JULIA_DEPOT_PATH' not in os.environ:
                    depot = root / 'julia-depot'
                    depot.mkdir()
                    os.environ['JULIA_DEPOT_PATH'] = str(depot) + os.pathsep
            julia = os.environ.get('QCL_JULIA', 'julia')
            os.environ.pop('QCL_NEGF_PROJECT', None)
            threads = str(cpus)
            os.environ.update(JULIA_NUM_THREADS='1,0', OPENBLAS_NUM_THREADS=threads,
                              OMP_NUM_THREADS=threads, MKL_NUM_THREADS=threads)
            project = f'--project={app / "runner"}'
            status['julia_version'] = subprocess.check_output([julia, '--version'], text=True).strip()
            if status['julia_version'] != 'julia version 1.13.4':
                raise ValueError('expected Julia 1.13.4')
            status['thread_probe'] = subprocess.check_output([julia, '--startup-file=no', project, '-e',
                'using LinearAlgebra; print(Threads.nthreads(), \" \", BLAS.get_num_threads())'], text=True).strip()
            if status['thread_probe'] != f'1 {cpus}':
                raise ValueError(f"expected 1 Julia / {cpus} BLAS threads, observed {status['thread_probe']}")
            if os.environ.get('QCL_INSTANTIATE') == '1':
                subprocess.run([julia, '--startup-file=no', project, '-e', 'using Pkg; Pkg.instantiate()'], check=True)
            result = root / 'result'
            if job['kind'] == 'domain':
                result.mkdir()
                cmd = [julia, '--startup-file=no', project, str(app / 'studies/v843-grid-cluster/domain.jl'), str(frozen), job['preset'], str(result / 'domain.toml')]
            else:
                cmd = [julia, '--startup-file=no', project, str(app / 'runner/bin/qcl-negf'), 'run-plan', str(frozen), str(result)]
            subprocess.run(cmd, check=True)
            status['ok'] = True
        except Exception:
            status['error'] = traceback.format_exc()
            print(status['error'], file=sys.stderr)
        status['wall_seconds'] = time.monotonic() - started
        status['plan_sha256'] = sha(plan)
        with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED, allowZip64=True) as z:
            z.writestr('status.json', json.dumps(status, indent=2) + '\n')
            result = root / 'result'
            if result.exists():
                for path in sorted(result.rglob('*')):
                    if path.is_file():
                        z.write(path, 'result/' + path.relative_to(result).as_posix())
    return 0 if status['ok'] else 1

if __name__ == '__main__':
    sys.exit(main())
