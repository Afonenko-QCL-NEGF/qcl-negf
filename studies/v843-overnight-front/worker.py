#!/usr/bin/env python3
"""Isolated portable worker: SOURCE.zip CASE.json JOB.json OUTPUT.zip."""
import hashlib, json, os, platform, subprocess, sys, tempfile, time, traceback, zipfile
from pathlib import Path, PurePosixPath

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    if len(sys.argv) != 5: raise SystemExit(__doc__)
    source, casefile, jobfile, output = map(Path, sys.argv[1:]); output = output.resolve()
    job = json.loads(jobfile.read_text(encoding='utf-8'))
    status = {'job': job, 'ok': False, 'classification': 'technical', 'platform': platform.platform()}
    start = time.monotonic()
    with tempfile.TemporaryDirectory(prefix='v843-') as tmp:
        root = Path(tmp); result = root / 'result.toml'
        try:
            if platform.system() != {'linux':'Linux','windows':'Windows'}[job['target_os']]: raise ValueError('wrong OS')
            if sha(source) != job['source_sha256'] or sha(casefile) != job['case_sha256']: raise ValueError('input checksum mismatch')
            case = json.loads(casefile.read_text(encoding='utf-8'))
            if case['id'] != job['id'] or case['family'] != job['family']: raise ValueError('case identity mismatch')
            with zipfile.ZipFile(source) as z:
                for info in z.infolist():
                    p = PurePosixPath(info.filename)
                    if p.is_absolute() or '..' in p.parts or '\\' in info.filename or ':' in info.filename: raise ValueError('unsafe source path')
                z.extractall(root / 'source')
            app = root / 'source'
            catalog = json.loads((app / 'source-catalog.json').read_text())
            for name, digest in catalog.items():
                p = PurePosixPath(name)
                if p.is_absolute() or '..' in p.parts or '\\' in name or ':' in name or sha(app.joinpath(*p.parts)) != digest: raise ValueError('source catalog mismatch: ' + name)
            cpus = job['request_cpus']; visible = len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else os.cpu_count()
            if type(cpus) is not int or cpus < 1 or (visible and cpus > visible): raise ValueError('CPU allocation exceeds visibility')
            os.environ.pop('QCL_NEGF_PROJECT', None)
            family = case['family']
            julia_threads = cpus if family in ('I', 'RI', 'G', 'RG') else 1
            blas_threads = 1 if family in ('I', 'RI') else cpus
            status.update(julia_threads_requested=julia_threads, blas_threads_requested=blas_threads)
            os.environ.update(JULIA_NUM_THREADS=f'{julia_threads},0', OPENBLAS_NUM_THREADS=str(blas_threads), OMP_NUM_THREADS=str(blas_threads), MKL_NUM_THREADS=str(blas_threads))
            if platform.system() == 'Windows':
                home = root / 'home'; home.mkdir(); os.environ.update(HOME=str(home), USERPROFILE=str(home))
                if 'JULIA_DEPOT_PATH' not in os.environ:
                    depot = root / 'depot'; depot.mkdir(); os.environ['JULIA_DEPOT_PATH'] = str(depot) + os.pathsep
            julia = os.environ.get('QCL_JULIA', 'julia'); project = '--project=' + str(app / 'runner')
            status['julia_version'] = subprocess.check_output([julia, '--version'], text=True).strip()
            if status['julia_version'] != 'julia version 1.13.4': raise ValueError('Julia 1.13.4 required')
            status['thread_probe'] = subprocess.check_output([julia, '--startup-file=no', project, '-e', 'using LinearAlgebra; print(Threads.nthreads(), " ", BLAS.get_num_threads())'], text=True).strip()
            if status['thread_probe'] != f'{julia_threads} {blas_threads}': raise ValueError('thread probe mismatch')
            if os.environ.get('QCL_INSTANTIATE', '1') == '1': subprocess.run([julia, '--startup-file=no', project, '-e', 'using Pkg; Pkg.instantiate()'], check=True)
            p = case['parameters']; family = case['family']; folder = app / 'studies/v843-overnight-front'
            if family in ('H','RH'): script, args = 'translation.jl', [p['B'],p['rank'],p['Nz']]
            elif family in ('G','RG'): script, args = 'resolvent.jl', [p['B'],p['rank'],p['Nz'],p['eta_meV'],p['K'], 481 if family == 'G' else 961]
            elif family == 'F': script, args = 'floquet.jl', [p['Nperiod'],p['Nz']]
            elif family in ('I','RI'): script, args = 'impurity.jl', [p['Nz'],p['K'], 'BASE' if family == 'I' else 'FORWARD']
            else: raise ValueError('unsupported family')
            cmd = [julia, '--startup-file=no', project, str(folder / script), *map(str,args), str(result)]
            try:
                import resource
                before = resource.getrusage(resource.RUSAGE_CHILDREN)
            except ImportError:
                resource = None
            t = time.monotonic(); proc = subprocess.run(cmd); status['calculation_wall_seconds'] = time.monotonic()-t; status['returncode'] = proc.returncode
            if resource is not None:
                after = resource.getrusage(resource.RUSAGE_CHILDREN)
                status['calculation_cpu_seconds'] = (after.ru_utime + after.ru_stime) - (before.ru_utime + before.ru_stime)
                if status['calculation_wall_seconds'] > 0:
                    status['calculation_average_cpus'] = status['calculation_cpu_seconds'] / status['calculation_wall_seconds']
                    status['calculation_allocated_cpu_fraction'] = status['calculation_average_cpus'] / cpus
            if proc.returncode: raise RuntimeError('Julia process failed')
            if not result.is_file() or not result.stat().st_size: raise ValueError('missing result')
            status.update(ok=True, classification='completed', result_sha256=sha(result))
        except Exception:
            status['error'] = traceback.format_exc(); print(status['error'], file=sys.stderr)
        status['wall_seconds'] = time.monotonic()-start
        status['case_sha256_observed'] = sha(casefile) if casefile.exists() else None
        with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as z:
            z.writestr('status.json', json.dumps(status, indent=2)+'\n')
            if result.is_file(): z.write(result, 'result.toml')
    return 0 if status['ok'] else 1
if __name__ == '__main__': sys.exit(main())
