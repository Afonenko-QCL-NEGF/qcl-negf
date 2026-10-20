"""Prospective bounded Python SCI12 math capture; source-only prepared, not executed.
Root alone validates meaningful reviews, predecessor and global counter, then binds READY.
No return code is a scientific verdict. No cgroup, filesystem jail or hard RSS/TMP quota.
"""
import datetime
import hashlib
import importlib.machinery
import json
import math
import os
import pathlib
import re
import resource
import signal
import stat
import subprocess
import sys
import time
import traceback
import types

ROOT = pathlib.Path('/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf')
CANDIDATE = pathlib.Path('/tmp/qcl-sci12-math-results-worktree')
CONTRACTS = ROOT/'components/qcl-negf-contracts/src'
RUNTIME = ROOT/'.venv/bin/python'
RUNTIME_SHA = 'dd65a07e8f535525443d63e2bd6dd10efbf22bf22e0b6d65e634266acc7ac976'
BASE_HEAD = 'de70638a982f91b7e125ab1cfc70a2daef2a656d'
FIXTURE = CANDIDATE/'tests/test_equilibrium_map_math.py'
FIXTURE_SHA = '995b364b93a56c403859f9ad074d55ef4abb5dddb70e2ad0982f689cb1b45a6d'
PRODUCT = CANDIDATE/'src/qcl_negf_results/_equilibrium_map_math.py'
PLAN = pathlib.Path('/tmp/qcl-sci12-math-local-plan-v2.json')
RAW_HELPER = pathlib.Path('/tmp/qcl-local-julia-guard-v2.py')
RAW_SHA = 'e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f'
SAMPLER = pathlib.Path('/tmp/qcl-owned-temp-sampler-v2.py')
SAMPLER_SHA = '16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e'
F2_REVIEW = pathlib.Path('/tmp/qcl-sci12-math-fixture-v2-review.md')
F2_SHA = 'c855f328402a217225b13fda3821000a8a6e55ed6894235e42b57802f3e69ec9'
SCOPE = 'SCI12-MATH-local-v2'
WALL, RAM, TEMP, LOG = 90, 1024**3, 32*1024**2, 2*1024**2
STAGES = {'SCI12-MATH-RED-1': (88,89), 'SCI12-MATH-GREEN-1': (89,90)}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def digest(value):
    return type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None


def read(path, maximum=262144):
    path = pathlib.Path(path)
    info = path.lstat()
    require(path.is_absolute() and path.resolve(strict=True) == path, 'noncanonical source')
    require(stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid(), 'file owner/type')
    require(0 <= info.st_size <= maximum, 'file bound')
    with path.open('rb') as stream:
        data = stream.read(maximum+1)
    require(len(data) == info.st_size and len(data) <= maximum, 'file drift/bound')
    return data


def parse(data):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON member')
            result[key] = value
        return result
    def invalid(value):
        raise RuntimeError('nonfinite JSON '+value)
    return json.loads(data, object_pairs_hook=pairs, parse_constant=invalid)


def ref(refdata):
    require(type(refdata) is dict and set(refdata) == {'path','sha256'}, 'reference schema')
    require(digest(refdata['sha256']) and refdata['path'].startswith('/tmp/qcl-'), 'reference namespace/hash')
    payload = read(pathlib.Path(refdata['path']))
    require(sha(payload) == refdata['sha256'], 'reference changed')
    return payload


def runtime_hash():
    result = hashlib.sha256()
    with RUNTIME.open('rb') as stream:
        for block in iter(lambda: stream.read(65536), b''):
            result.update(block)
    return result.hexdigest()


def closure(ready):
    # Freeze all first-party Python source, not just the future math module.
    paths = {FIXTURE, CANDIDATE/'pyproject.toml'}
    for root in (CANDIDATE/'src', CONTRACTS):
        paths.update(root.rglob('*.py'))
    for parent in (pathlib.Path('/'), pathlib.Path('/tmp'), CANDIDATE, CANDIDATE/'tests'):
        for name in ('conftest.py','pytest.ini','.pytest.ini','setup.cfg','tox.ini'):
            require(not (parent/name).exists(), 'unreviewed implicit pytest config/conftest')
    require(len(paths) <= 512, 'source closure count')
    expected = ready['source_files']
    require(type(expected) is dict and set(expected) == {str(path) for path in paths}, 'exact source closure')
    total, observed = 0, {}
    for path in sorted(paths):
        payload = read(path)
        total += len(payload)
        require(total <= 3*1024**2, 'source closure bound')
        require(digest(expected[str(path)]) and sha(payload) == expected[str(path)], 'source digest')
        observed[str(path)] = sha(payload)
    require(observed[str(FIXTURE)] == FIXTURE_SHA, 'frozen F2 fixture')
    if ready['attempt'] == 'SCI12-MATH-RED-1':
        require(not PRODUCT.exists() and not PRODUCT.is_symlink() and ready['product_sha256'] is None, 'RED requires absent NEW module')
    else:
        require(digest(ready['product_sha256']) and observed.get(str(PRODUCT)) == ready['product_sha256'], 'GREEN exact future product hash')
    return observed


def reviewed_module(payload, path, name):
    module = types.ModuleType(name)
    module.__file__, module.__package__, module.__loader__, module.__cached__ = str(path), '', None, None
    module.__spec__ = importlib.machinery.ModuleSpec(name, loader=None, origin=str(path))
    module.__spec__.has_location = True
    exec(compile(payload, str(path), 'exec', dont_inherit=True, optimize=0), module.__dict__)
    return module


def rss_tree(pid):
    pending, seen, total = [pid], set(), 0
    try:
        while pending:
            current = pending.pop()
            if current in seen:
                continue
            seen.add(current)
            if len(seen) > 256:
                return None
            proc = pathlib.Path('/proc',str(current))
            rows = [line.split() for line in (proc/'status').read_text().splitlines() if line.startswith('VmRSS:')]
            if len(rows) != 1 or len(rows[0]) != 3 or rows[0][2] != 'kB':
                return None
            amount = int(rows[0][1])
            if amount < 0:
                return None
            total += amount*1024
            tasks = list((proc/'task').iterdir())
            if not tasks:
                return None
            for task in tasks:
                pending.extend(int(item) for item in (task/'children').read_text().split())
        return total if seen else None
    except (OSError,ValueError):
        return None


def child_limits():
    os.setsid()
    os.sched_setaffinity(0,{min(os.sched_getaffinity(0))})
    resource.setrlimit(resource.RLIMIT_CPU,(90,90))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))


def stop_owned(process):
    if process is None:
        return
    try:
        os.killpg(process.pid,signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(process.pid,signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait(timeout=2)


def write_receipt(folder, record):
    try:
        pending = folder/'receipt.json.pending'
        pending.write_text(json.dumps(record,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
        os.replace(pending,folder/'receipt.json')
        return True
    except BaseException:
        os.write(2,b'FAILED_RECEIPT_WRITE: consumed attempt; reconcile, no rerun\n')
        return False


def main():
    require(len(sys.argv) == 3 and sys.argv[1] == '--execute', 'requires exact --execute fresh Root READY path')
    ready_path = pathlib.Path(sys.argv[2])
    self_bytes, plan_bytes, ready_bytes = read(pathlib.Path(__file__)), read(PLAN), read(ready_path)
    ready, plan = parse(ready_bytes), parse(plan_bytes)
    fields = {'status','issuer','scope','attempt','created_unix','harness_sha256','plan_sha256',
        'runtime_sha256','candidate_base_head','root_head','source_files','product_sha256',
        'budget','root_validation_ref','accepted_guard_review','accepted_source_review',
        'predecessor_ref','sampled_guards_acknowledged'}
    require(type(ready) is dict and set(ready) == fields, 'exact READY schema')
    require(ready['status'] == 'READY' and ready['issuer'] == 'Root' and ready['scope'] == SCOPE, 'Root READY identity')
    attempt = ready['attempt']
    require(attempt in STAGES, 'finite attempt')
    before_count, after_count = STAGES[attempt]
    require(type(ready['created_unix']) in (int,float) and math.isfinite(ready['created_unix']) and 0 <= time.time()-ready['created_unix'] <= 300, 'fresh READY <=300s')
    require(ready['harness_sha256'] == sha(self_bytes) and ready['plan_sha256'] == sha(plan_bytes), 'H/P binding')
    require(ready['runtime_sha256'] == RUNTIME_SHA and ready['candidate_base_head'] == BASE_HEAD, 'runtime/base binding')
    require(type(ready['root_head']) is str and re.fullmatch('[0-9a-f]{40}',ready['root_head']), 'Root HEAD')
    require(ready['sampled_guards_acknowledged'] is True, 'sampled limits acknowledged')
    require(ready['budget'] == {'calls_before':before_count,'calls_reserved':1,'calls_after':after_count,'global_ceiling':90,'source_C08':'8/8 unchanged','no_rerun':True}, 'global reservation binding')
    require(plan['scope'] == SCOPE and plan['attempts'] == list(STAGES) and plan['target_argv'] == command(), 'frozen plan')
    references = {key:ref(ready[key]) for key in ('root_validation_ref','accepted_guard_review','accepted_source_review','predecessor_ref')}
    handoff = parse(references['root_validation_ref'])
    require(handoff == {'status':'ROOT_VALIDATED_FOR_SINGLE_CALL','issuer':'Root','scope':SCOPE,'attempt':attempt,
        'harness_sha256':sha(self_bytes),'plan_sha256':sha(plan_bytes),'root_head':ready['root_head'],
        'candidate_base_head':BASE_HEAD,'source_files':ready['source_files'],'product_sha256':ready['product_sha256'],
        'budget':ready['budget'],'accepted_guard_review':ready['accepted_guard_review'],
        'accepted_source_review':ready['accepted_source_review'],'predecessor_ref':ready['predecessor_ref'],
        'meaningful_reviews_predecessor_counter_and_aggregate_budget_validated':True}, 'Root validation/handoff')
    require(sha(read(F2_REVIEW)) == F2_SHA, 'frozen high F2 review')
    before = closure(ready)
    require(runtime_hash() == RUNTIME_SHA, 'runtime before')
    raw_bytes, sampler_bytes = read(RAW_HELPER), read(SAMPLER)
    require(sha(raw_bytes) == RAW_SHA and sha(sampler_bytes) == SAMPLER_SHA, 'helper hashes')
    # Same bytes hashed above are exactly what is compiled/imported inside the future call.
    raw = reviewed_module(raw_bytes,RAW_HELPER,'reviewed_raw_capture')
    sampler = reviewed_module(sampler_bytes,SAMPLER,'reviewed_owned_temp_sampler')
    folder = pathlib.Path('/tmp/qcl-'+attempt)
    folder.mkdir(mode=0o700,exist_ok=False)
    started = time.monotonic()
    process = capture = stream = None
    collector_attempted = False
    record = {'scope':SCOPE,'attempt':attempt,'attempt_consumed':True,'target_calls':0,
        'verdict':'STOP_RECONCILE_NO_RERUN','stop_reason':'reserved_not_terminal',
        'harness_sha256':sha(self_bytes),'plan_sha256':sha(plan_bytes),'ready_sha256':sha(ready_bytes),
        'budget':ready['budget'],'source_before':before,'root_head':ready['root_head'],
        'candidate_base_head':BASE_HEAD,'runtime_sha256':RUNTIME_SHA,'RawCapture_sha256':RAW_SHA,
        'sampler_sha256':SAMPLER_SHA,'reference_hashes':{key:sha(value) for key,value in references.items()},
        'nominal_cases':97,'observed_outcomes':None,'scientific_acceptance':'not_measured'}
    require(write_receipt(folder,record),'reservation receipt')
    def terminal(signum,frame):
        try:
            if process is not None:
                try:
                    os.killpg(process.pid,signal.SIGKILL)
                except ProcessLookupError:
                    pass
            record.update(stop_reason='terminal_wall_guard',raw_capture_complete=False,
                target_calls=int(process is not None),collector_construction_attempted=collector_attempted,
                collector_ownership='unknown' if collector_attempted and capture is None else ('assigned' if capture is not None else 'not_attempted'),
                RSS_status='unknown_terminal_guard')
            write_receipt(folder,record)
        finally:
            os._exit(2)
    signal.signal(signal.SIGALRM,terminal)
    signal.setitimer(signal.ITIMER_REAL,max(.001,WALL-(time.monotonic()-started)))
    temporary = folder/'owned-tmp'
    reason = error = capture_error = None
    complete, captured, raw_digest, after = False, None, None, None
    rss_attempts = rss_valid = rss_unknown = tmp_samples = 0
    rss_na, peak_rss, peak_temp = [], None, None
    initial_tmp = final_tmp = None
    env = None
    def observe():
        nonlocal reason,rss_attempts,rss_valid,rss_unknown,peak_rss,tmp_samples,peak_temp
        value = sampler.sample_owned_temporary_bytes(temporary)
        tmp_samples += 1
        peak_temp = value if peak_temp is None else max(peak_temp,value)
        if process is not None:
            code = process.poll()
            if code is not None:
                rss_na.append({'proof':'Popen.poll_returncode_before_RSS_attempt','pid':process.pid,'returncode':code,'elapsed_seconds':time.monotonic()-started})
            else:
                rss_attempts += 1
                value = rss_tree(process.pid)
                if value is None:
                    rss_unknown += 1
                    reason = reason or 'attempted_live_RSS_unknown'
                else:
                    rss_valid += 1
                    peak_rss = value if peak_rss is None else max(peak_rss,value)
        if time.monotonic()-started >= 78:
            reason = reason or 'wall_stop_78s_terminal_reserve'
        if peak_temp >= TEMP:
            reason = reason or 'owned_TMP_cap'
        if peak_rss is not None and peak_rss >= RAM:
            reason = reason or 'sampled_RSS_cap'
        if capture is not None and capture.bytes >= LOG-128*1024:
            reason = reason or 'raw_output_stop_threshold'
        if capture is not None and capture.error:
            reason = reason or 'raw_capture_error'
        return peak_temp
    try:
        temporary.mkdir(mode=0o700)
        for name in ('home','tmp'):
            (temporary/name).mkdir(mode=0o700)
        env = {'PYTHONPATH':str(CANDIDATE/'src'), 'QCL_NEGF_TEST_CONTRACTS_SOURCE':str(CONTRACTS),
            'PYTEST_DISABLE_PLUGIN_AUTOLOAD':'1','PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0',
            'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1',
            'HOME':str(temporary/'home'),'TMPDIR':str(temporary/'tmp')}
        require(closure(ready) == before,'prelaunch source drift')
        stream = (folder/'original.log').open('xb',buffering=0)
        initial_tmp = observe()
        require(reason is None,'prelaunch bounds')
        process = subprocess.Popen(command(),cwd=CANDIDATE,env=env,stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,preexec_fn=child_limits)
        collector_attempted = True
        capture = raw.RawCapture(process.stdout,stream)
        observe()
        while process.poll() is None and reason is None:
            observe()
            time.sleep(.05)
    except BaseException:
        error = traceback.format_exc()
        reason = reason or 'guard_exception'
    finally:
        try:
            stop_owned(process)
        except BaseException:
            error = (error or '')+traceback.format_exc()
            reason = reason or 'cleanup_unknown'
        if collector_attempted and capture is None:
            # Native thread may have started before constructor raised: no competing read/close.
            record.update(stop_reason='collector_construction_unknown',guard_error=error,
                target_calls=int(process is not None),collector_construction_attempted=True,
                collector_ownership='unknown',collector_terminal=None,raw_capture_complete=False,
                raw_bytes=None,raw_sha256=None,RSS_valid_samples=rss_valid,RSS_unknown_samples=rss_unknown,
                RSS_NA_after_reap_proofs=rss_na,sampled_peak_process_tree_RSS_bytes=peak_rss)
            write_receipt(folder,record)
            os._exit(2)
        try:
            if capture is not None:
                complete = capture.finish(2)
                captured,capture_error = capture.bytes,capture.error
            elif stream is not None:
                stream.close()
                reason = reason or 'collector_not_attempted'
        except BaseException:
            capture_error = traceback.format_exc()
            reason = reason or 'capture_finish_exception'
        try:
            final_tmp = observe()
        except BaseException:
            error = (error or '')+traceback.format_exc()
            reason = reason or 'final_observation_unknown'
        try:
            after = closure(ready)
            require(after == before and runtime_hash() == RUNTIME_SHA,'source/runtime after')
            require(read(pathlib.Path(__file__)) == self_bytes and read(PLAN) == plan_bytes and read(ready_path) == ready_bytes,'H/P/READY after')
            require(read(RAW_HELPER) == raw_bytes and read(SAMPLER) == sampler_bytes,'helper after')
            require(sha(read(F2_REVIEW)) == F2_SHA,'F2 review after')
            require(all(ref(ready[key]) == value for key,value in references.items()),'review/reference after')
        except BaseException:
            error = (error or '')+traceback.format_exc()
            reason = reason or 'terminal_binding_unknown'
        try:
            if complete and captured is not None and captured <= LOG:
                payload = read(folder/'original.log',LOG)
                require(len(payload) == captured,'raw size reconciliation')
                raw_digest = sha(payload)
        except BaseException:
            error = (error or '')+traceback.format_exc()
            reason = reason or 'raw_readback_unknown'
        elapsed = time.monotonic()-started
        if rss_valid < 1 or rss_unknown:
            reason = reason or 'RSS_not_measured_or_unknown'
        if initial_tmp is None or final_tmp is None:
            reason = reason or 'TMP_not_measured'
        if not complete or capture_error:
            reason = reason or 'capture_incomplete'
        if captured is None or captured > LOG:
            reason = reason or 'raw_envelope_unknown_or_exceeded'
        if elapsed > WALL:
            reason = reason or 'terminal_wall_cap'
        expected_exit = 1 if attempt == 'SCI12-MATH-RED-1' else 0
        if process is None or process.returncode != expected_exit:
            reason = reason or 'child_exit_unexpected_or_unknown'
        good = reason is None and error is None and raw_digest is not None and after == before
        record.update(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            verdict='CAPTURED_REQUIRES_INDEPENDENT_97CASE_REVIEW' if good else 'STOP_RECONCILE_NO_RERUN',
            stop_reason=reason,guard_error=error,target_calls=int(process is not None),
            exit_code=process.returncode if process is not None else None,wall_seconds=elapsed,
            command=command(),cwd=str(CANDIDATE),environment=env,environment_clear=True,source_after=after,
            RSS_attempted_samples=rss_attempts,RSS_valid_samples=rss_valid,RSS_unknown_samples=rss_unknown,
            RSS_NA_after_reap_proofs=rss_na,sampled_peak_process_tree_RSS_bytes=peak_rss,
            TMP_samples=tmp_samples,sampled_peak_owned_regular_logical_bytes=peak_temp,
            initial_TMP_bytes=initial_tmp,final_TMP_bytes=final_tmp,
            raw_capture_complete=complete,raw_capture_error=capture_error,raw_bytes=captured,raw_sha256=raw_digest,
            collector_construction_attempted=collector_attempted,
            collector_terminal=None if capture is None else not capture.thread.is_alive(),
            limits={'wall_seconds':WALL,'affinity_CPUs':1,'RLIMIT_CPU_seconds':90,'sampled_RSS_bytes':RAM,'sampled_TMP_bytes':TEMP,'raw_envelope_bytes':LOG},
            limitations='Sampled RSS/TMP, regular-file logical bytes; no hard peak/OS quota/native isolation. Root validates aggregate180s/4MiB, exact predecessor and counter. Independent full pytest/name/count/assertion/error/skip review required; no science claim.')
        saved = write_receipt(folder,record)
        if capture is not None and capture.thread.is_alive():
            record.update(verdict='STOP_RECONCILE_NO_RERUN',stop_reason='collector_not_terminal',raw_capture_complete=False,collector_terminal=False)
            write_receipt(folder,record)
            os._exit(2)  # Do not cancel watchdog or enter non-daemon shutdown join.
        if not saved:
            os._exit(2)
        signal.setitimer(signal.ITIMER_REAL,0)
    return 0 if good and saved else 1


def command():
    return [str(RUNTIME),'-m','pytest','-q','--tb=short','-p','no:cacheprovider','tests/test_equilibrium_map_math.py']


if __name__ == '__main__':
    try:
        result = main()
    except BaseException:
        # Pre-reservation rejection creates no target call and never implies a retry grant.
        os.write(2,traceback.format_exc().encode('utf-8','replace'))
        result = 1
    sys.exit(result)
