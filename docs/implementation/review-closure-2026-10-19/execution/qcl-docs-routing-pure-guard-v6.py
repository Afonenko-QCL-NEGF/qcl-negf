#!/usr/bin/python3
"""SOURCE ONLY: sole DOCS-ROUTING-GREEN-1, after independent high review/Root READY.
No product code is imported by this guard. No retry, RED, native unit or CI route.
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
import select
import signal
import stat
import subprocess
import sys
import time
import traceback
import types

ROOT = pathlib.Path('/tmp/qcl-docs-test-routing-worktree')
PLAN = pathlib.Path('/tmp/qcl-docs-routing-pure-plan-v6.json')
ATTEMPT = 'DOCS-ROUTING-GREEN-1'
SCOPE = 'docs-routing-pure-local-engineering-v6'
ANCESTOR_SCOPE = 'docs-routing-pure-local-engineering-v1'
FIXTURE = 'tests/docs_test_routing_test.ts'
HELPER = 'ops/docs_tests.ts'
BASE_HEAD = '2bb05d3651af4509fe7f02c1253b40f1e5146fec'
RUNTIME = pathlib.Path('/nix/store/xn4n2ijvg7pq49qm8kl5252j21sq3g3m-deno-2.8.3/bin/deno')
RUNTIME_SHA = 'cdd88de791341a151d80ee5c189abb4b7681beb0aca9f5c1a4b0f4fe9429e26c'
RAW_HELPER = pathlib.Path('/tmp/qcl-local-julia-guard-v2.py')
RAW_SHA = 'e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f'
SAMPLER = pathlib.Path('/tmp/qcl-owned-temp-sampler-v2.py')
SAMPLER_SHA = '16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e'
WALL, RAM, TEMP, LOG = 120, 1024**3, 16*1024**2, 2*1024**2
BASELINE = {
 FIXTURE: '2639be2132a88adb3e1ccd204112180efa065089e9ade5cae87e38c970952f99',
 HELPER: '68f0efb5b45a03f130a52d14279e427c83c11b317a3c244e43375dbac5b8d3f5'}
FORMAT1_SOURCES = {
 FIXTURE: '8946e323023da597629f669dcb60c17bb6674f9c5a9bd9e2492dea280c35f16b',
 HELPER: '38a56bff45bd7f7e36e8eb1a4542756b5225388d53827b6c24c73c9b059dc62b'}
CONTINUATION = {
 '/tmp/qcl-docs-routing-pure-guard-v5.py':'e49cda399947c9ce9a60352c9def75076d8f5bab29d054f16a8d6874837e1372',
 '/tmp/qcl-docs-routing-pure-plan-v5.json':'73b79ab73cf2b0702ace55de6f6c0cca6f48106bf0eaa7556221bad4804f9b06',
 '/tmp/qcl-docs-routing-pure-harness-v5-review.md':'140472debae1d9a47c8c694b964ed36213003fd3dbffe172001928b141bfb084',
 '/tmp/qcl-docs-routing-pure-format-final-v5-review.md':'50b8d8d5c83d509df3928750a6ad947f8b779dcacaa2baa3b690c65f18b81ba2',
 '/tmp/qcl-docs-routing-pure-format1-frozen-v5/manifest.json':'ed50c4ec8c8ba1b88ce93fdc8778c317446d08d716a799aa688771ed7c94846a',
 '/tmp/qcl-docs-routing-pure-format1-frozen-v5/ops/docs_tests.ts':FORMAT1_SOURCES[HELPER],
 '/tmp/qcl-docs-routing-pure-format1-frozen-v5/tests/docs_test_routing_test.ts':FORMAT1_SOURCES[FIXTURE],
 '/tmp/qcl-DOCS-ROUTING-SOURCE-FORMAT-1/receipt.json':'d33fe2a43835ae48af6ff9a92d8abda2351bdac5e6ddff30c2590a216dba73a6',
 '/tmp/qcl-DOCS-ROUTING-SOURCE-FORMAT-1/original.log':'b9f584e863bc07b513e9c6808e9e1eb0f6bdba3dc88377b983560b1316fa6919',
 '/tmp/qcl-DOCS-ROUTING-SOURCE-LINT-1/receipt.json':'c14d85854326c2bd8bd6ac4fcd009fc57dc346e538dcd015b1f70a3b0bdadf10',
 '/tmp/qcl-DOCS-ROUTING-SOURCE-LINT-1/original.log':'c480b2473669fb26ad2b45494a09443e195eee25c4361ddda1399bb017e3f787',
 '/tmp/qcl-docs-routing-pure-lint-comment-correction-v1.patch':'0ba7a8cdd4b18f7207acbd8f49c86e29b7012d8f25f19dfe8a0a14b6e60628e3'}
CONFIG = ROOT/'deno.json'
CONFIG_SHA = 'a637ff88ad0e1011480402de58895cb6d178eb1bbe98bdb27ca939b8821f6bce'
PURE_CPP = {'path':'/tmp/qcl-docs-routing-impl-i2b-review.md',
            'sha256':'4903c3d64d8254a7b4ac89fcc08efed049485a21b1a1c155922b515b6118c4ea'}
OLD_FIXTURE_SHA = '04589b3993e51885b2abc08cb516c7a6467709e3d278c593874c598ecaa9ecf3'
ANCESTORS = {
 '/tmp/qcl-docs-routing-local-unit-run-v2.py': '0061c27ec61bf8ca15d6e94d304db695072b12adc3fe6ca8ddef2ee254df82e7',
 '/tmp/qcl-docs-routing-engineering-plan-v2.json': '5147cab0a8df1d50fb908b3c247e8c7b0e11852ee01a990f8a35228b3e70157a',
 '/tmp/qcl-docs-routing-historical-RED-fixture.ts': OLD_FIXTURE_SHA,
 '/tmp/qcl-DOCS-ROUTING-RED-1/receipt.json': 'e874825467896121a89e7c0d31272ed5b923da8b0cc08e30846adca56c6806b0',
 '/tmp/qcl-DOCS-ROUTING-RED-1/original.log': '6b044ed571751341f215353d5dafd384dcf009a70c4b471595ebdcb53b8589ad',
 '/tmp/qcl-docs-routing-RED-diagnostic-erratum.md': '6dfb097abf97aeabd9114354c987b5846fd19f449c4d0bfc2168299a1e03383b',
 '/tmp/qcl-docs-routing-RED-diagnostic-erratum-review.md': '9537f35088687da532bd44f551ed637e320b40481ee6c76628621ba712d426f1',
 '/tmp/qcl-docs-test-routing-design-v2.md': 'bbb8cbeb4845a9a7b9514010f5c988beeac66080246d9fca1d6c12ee8a81cf70',
 '/tmp/qcl-docs-test-routing-design-v2-review.md': '939555c9291e98be1200b063bcf06e344a7597907dfbf498bf28029927728967'}
OLD_RAW_LAYOUT = b"""TS2307 [ERROR]: Cannot find module 'file:///tmp/qcl-docs-test-routing-worktree/ops/docs_tests.ts'.
    at file:///tmp/qcl-docs-test-routing-worktree/tests/docs_test_routing_test.ts:13:8

TS7006 [ERROR]: Parameter 'step' implicitly has an 'any' type.
  equal(result.steps.slice(1).map((step) => {
                                   ~~~~
    at file:///tmp/qcl-docs-test-routing-worktree/tests/docs_test_routing_test.ts:311:36

Found 2 errors.

error: Type checking failed.

  info: The program failed type-checking, but it still might work correctly.
  hint: Re-run with --no-check to skip type-checking.
"""

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def hexsha(value):
    return type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None

def plain(data):
    return re.sub(rb'\x1b\[[0-?]*[ -/]*[@-~]', b'', data)

def read_file(path, maximum=262144):
    path = pathlib.Path(path)
    info = path.lstat()
    require(path.is_absolute() and path.resolve(strict=True) == path, 'noncanonical file')
    require(stat.S_ISREG(info.st_mode) and info.st_uid == os.getuid(), 'file owner/type')
    require(0 <= info.st_size <= maximum, 'file size bound')
    with path.open('rb') as stream:
        data = stream.read(maximum+1)
    require(len(data) == info.st_size and len(data) <= maximum, 'file changed/over bound')
    return data

def json_buffer(data):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON member')
            result[key] = value
        return result
    def invalid(value):
        raise RuntimeError('nonfinite JSON number '+value)
    return json.loads(data, object_pairs_hook=pairs, parse_constant=invalid)

def ref_bytes(ref, expected_path=None, maximum=262144):
    require(type(ref) is dict and set(ref) == {'path', 'sha256'}, 'exact reference')
    require(hexsha(ref['sha256']), 'reference SHA')
    path = pathlib.Path(ref['path'])
    require(expected_path is None or path == pathlib.Path(expected_path), 'reference path')
    require(str(path).startswith('/tmp/qcl-'), 'reference namespace')
    data = read_file(path, maximum)
    require(sha(data) == ref['sha256'], 'reference digest')
    return data

def finite(value):
    return type(value) in (int, float) and math.isfinite(value)

def command():
    return [str(RUNTIME), 'test', '--no-config', '--no-lock', '--cached-only',
            '--no-npm', '--no-remote', '--no-prompt', '--reporter=tap', str(ROOT/FIXTURE)]

def predecessor(ref):
    # This entire function precedes any guard-code imports or GREEN reservation.
    record = json_buffer(ref_bytes(ref, '/tmp/qcl-docs-routing-pure-predecessor-v6.json', 32768))
    fields = {'status', 'scope', 'attempt', 'original_classification', 'ancestor_refs',
              'historical_fixture_sha256', 'runtime_sha256', 'observed_engine_tests'}
    require(type(record) is dict and set(record) == fields, 'predecessor schema')
    require(record['status'] == 'SOURCE_REVIEWED_INCONCLUSIVE_PREDECESSOR_FOR_SINGLE_GREEN', 'predecessor status')
    require(record['scope'] == SCOPE and record['attempt'] == 'DOCS-ROUTING-RED-1', 'predecessor identity')
    require(record['original_classification'] == 'completed_inconclusive_or_guardfailure_preserve_no_rerun', 'preserve RED classification')
    require(record['historical_fixture_sha256'] == OLD_FIXTURE_SHA and record['runtime_sha256'] == RUNTIME_SHA, 'ancestral source/runtime')
    require(record['observed_engine_tests'] is None, 'RED never measured tests')
    refs = record['ancestor_refs']
    require(type(refs) is dict and set(refs) == set(ANCESTORS), 'ancestral closure')
    buffers = {}
    for path, expected in ANCESTORS.items():
        require(refs[path] == {'path': path, 'sha256': expected}, 'fixed ancestral reference')
        buffers[path] = ref_bytes(refs[path], path)
    receipt_path = '/tmp/qcl-DOCS-ROUTING-RED-1/receipt.json'
    raw_path = '/tmp/qcl-DOCS-ROUTING-RED-1/original.log'
    require(len(buffers[receipt_path]) == 2724 and len(buffers[raw_path]) == 765, 'fixed RED sizes')
    old = json_buffer(buffers[receipt_path])
    expected = {
      'scope': ANCESTOR_SCOPE, 'attempt': 'DOCS-ROUTING-RED-1', 'red_predecessor': None,
      'harness_sha256': ANCESTORS['/tmp/qcl-docs-routing-local-unit-run-v2.py'],
      'plan_sha256': ANCESTORS['/tmp/qcl-docs-routing-engineering-plan-v2.json'],
      'fixture_sha256': OLD_FIXTURE_SHA, 'helper_sha256': None, 'runtime_sha256': RUNTIME_SHA,
      'RawCapture_sha256': RAW_SHA, 'sampler_sha256': SAMPLER_SHA,
      'command': command(), 'cwd': str(ROOT), 'exit_code': 1,
      'stop_reason': None, 'guard_error': None, 'raw_capture_error': None,
      'raw_capture_complete': True, 'raw_output_overrun': False,
      'raw_bytes': 765, 'raw_sha256': ANCESTORS[raw_path],
      'nominal_source_registration_count': 227, 'observed_engine_tests': None,
      'environment_clear': True,
      'environment': {key: '/tmp/qcl-DOCS-ROUTING-RED-1/owned-tmp/'+name
        for key, name in [('DENO_DIR','deno-cache'),('TMPDIR','tmp'),('HOME','home')]},
      'limits': {'wall_seconds': WALL, 'cpu_affinity_count': 1, 'RLIMIT_CPU_seconds': 120,
        'sampled_RSS_stop_bytes': RAM, 'sampled_owned_TMP_stop_bytes': TEMP, 'raw_bytes_envelope': LOG}}
    require(all(key in old and old[key] == value for key, value in expected.items()), 'retained RED predicates')
    require(type(old['exit_code']) is int and type(old['sample_count']) is int and old['sample_count'] >= 2, 'RED exit/samples')
    require(finite(old['wall_seconds']) and 0 <= old['wall_seconds'] <= WALL, 'RED wall')
    for key, cap in [('sampled_peak_process_tree_RSS_bytes', RAM), ('sampled_peak_owned_tmp_all_entry_st_size_bytes', TEMP)]:
        require(type(old[key]) is int and 0 < old[key] < cap, 'RED sampled observation')
    require(plain(buffers[raw_path]) == OLD_RAW_LAYOUT, 'RED full diagnostic layout')
    return record

def reviewed_module(path, expected, name):
    payload = read_file(path)
    require(sha(payload) == expected, 'guard module digest')
    module = types.ModuleType(name)
    module.__file__, module.__package__, module.__loader__, module.__cached__ = str(path), '', None, None
    module.__spec__ = importlib.machinery.ModuleSpec(name, loader=None, origin=str(path))
    module.__spec__.has_location = True
    exec(compile(payload, str(path), 'exec', dont_inherit=True, optimize=0), module.__dict__)
    return module

def snapshot(sources):
    require(type(sources) is dict and set(sources) == {FIXTURE, HELPER}, 'pure two-file closure only')
    result = {}
    for path, expected in sources.items():
        require(hexsha(expected), 'current source SHA')
        result[path] = sha(read_file(ROOT/path))
        require(result[path] == expected, 'current source differs from READY/review')
    return result

def comment_correction_evidence(ready):
    # Fixed history is evidence of consumed attempts, never a good v6 prerequisite.
    buffers = {path:ref_bytes({'path':path,'sha256':expected},path)
               for path,expected in CONTINUATION.items()}
    fmt1 = json_buffer(buffers['/tmp/qcl-DOCS-ROUTING-SOURCE-FORMAT-1/receipt.json'])
    lint1 = json_buffer(buffers['/tmp/qcl-DOCS-ROUTING-SOURCE-LINT-1/receipt.json'])
    require(fmt1['stage'] == 'FORMAT1' and fmt1['source_after'] == FORMAT1_SOURCES and fmt1['exit_code'] == 0, 'retained FORMAT1 ancestry')
    require(lint1['scope'] == 'docs-routing-pure-local-engineering-v5' and lint1['stage'] == 'LINT1'
      and lint1['source_before'] == FORMAT1_SOURCES and lint1['source_after'] == FORMAT1_SOURCES
      and lint1['exit_code'] == 1 and lint1['verdict'] == 'STOP_RECONCILE_NO_RERUN'
      and lint1['stop_reason'] == 'source_child_nonzero_or_unknown'
      and lint1['raw_capture_complete'] is True and lint1['RSS_unknown_samples'] == 0, 'failed LINT1 must remain consumed failure')
    cpp = ready['comment_only_cpp']
    require(type(cpp) is dict and set(cpp) == {'status','pure_only_slice','before_sources','after_sources',
      'patch_ref','prior_format_review_ref','report_ref'}, 'comment-only CPP exact schema')
    require(cpp['status'] == 'PASS_COMMENT_ONLY_PURE_CORRECTION' and cpp['pure_only_slice'] is True
      and cpp['before_sources'] == FORMAT1_SOURCES and cpp['after_sources'] == BASELINE, 'new exact comment-only CPP required')
    for key,path in [('patch_ref','/tmp/qcl-docs-routing-pure-lint-comment-correction-v1.patch'),
                     ('prior_format_review_ref','/tmp/qcl-docs-routing-pure-format-final-v5-review.md')]:
        require(cpp[key] == {'path':path,'sha256':CONTINUATION[path]}, 'comment ancestry reference')
    ref_bytes(cpp['report_ref'])

def source_evidence(ready):
    comment_correction_evidence(ready)
    sources = ready['source_files']
    before = snapshot(sources)
    cpp = ready['accepted_cpp']
    require(type(cpp) is dict and set(cpp) == {'status','source_files','report_ref','pure_only_slice','baseline_cpp_ref'}, 'CPP binding schema')
    require(cpp['status'] == 'PASS_SOURCE_PURE_CLOSURE' and cpp['source_files'] == sources, 'CPP current source binding')
    require(cpp['pure_only_slice'] is True and cpp['baseline_cpp_ref'] == PURE_CPP, 'whole I2B CPP is not PASS')
    ref_bytes(cpp['baseline_cpp_ref'])
    ref_bytes(cpp['report_ref'])
    fmt = ready['format_binding']
    require(type(fmt) is dict and set(fmt) == {'status','unformatted_sources','formatted_sources','review_ref','receipt_refs'}, 'format binding schema')
    require(fmt['status'] == 'PASS_FORMAT_ONLY' and fmt['unformatted_sources'] == BASELINE and fmt['formatted_sources'] == sources, 'format-only ancestry')
    ref_bytes(fmt['review_ref'])
    require(type(fmt['receipt_refs']) is list and len(fmt['receipt_refs']) == 3, 'three source tool receipts')
    require(len({r['path'] for r in fmt['receipt_refs']}) == 3, 'distinct source receipts')
    for stage, ref in zip(('FORMAT2','LINT2','CHECK1'),fmt['receipt_refs']):
        source_receipt_ref(ref,stage,sources)
    review = ready['accepted_guard_review']
    require(type(review) is dict and set(review) == {'status','harness_sha256','plan_sha256','report_ref'}, 'guard review schema')
    require(review['status'] == 'PASS_SOURCE' and review['harness_sha256'] == ready['harness_sha256'] and review['plan_sha256'] == ready['plan_sha256'], 'guard review identity')
    ref_bytes(review['report_ref'])
    # Approval meanings are verified by trusted Root; arbitrary same-user JSON is not authority.
    return before

def directory(path):
    info = path.lstat()
    require(path.resolve(strict=True) == path and stat.S_ISDIR(info.st_mode), 'canonical directory')
    require(info.st_uid == os.getuid() and stat.S_IMODE(info.st_mode) == 0o700, 'owned directory mode')

def tmp_bytes(root):
    total, count, pending = 0, 0, [root]
    while pending:
        path = pending.pop()
        try:
            info = path.lstat()
        except FileNotFoundError:
            continue
        count += 1
        require(count <= 65536 and info.st_uid == os.getuid(), 'TMP census owner/count')
        require(stat.S_ISREG(info.st_mode) or stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode), 'TMP special entry')
        total += info.st_size
        if stat.S_ISDIR(info.st_mode):
            try:
                with os.scandir(path) as entries:
                    for entry in entries:
                        pending.append(pathlib.Path(entry.path))
                        require(count+len(pending) <= 65536, 'TMP pending bound')
            except FileNotFoundError:
                continue
    return total

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
            proc = pathlib.Path('/proc', str(current))
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
    except (OSError, ValueError):
        return None

def child_limits():
    os.setsid()
    os.sched_setaffinity(0, {min(os.sched_getaffinity(0))})
    resource.setrlimit(resource.RLIMIT_CPU, (120,120))
    resource.setrlimit(resource.RLIMIT_CORE, (0,0))

def stop_owned(process):
    if process is None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
    try:
        process.wait(timeout=1)
    except subprocess.TimeoutExpired:
        pass
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    process.wait(timeout=2)

def receipt_write(folder, record, name='receipt.json'):
    try:
        pending = folder/(name+'.pending')
        pending.write_text(json.dumps(record, indent=2, allow_nan=False)+'\n')
        os.replace(pending, folder/name)
        return True
    except BaseException:
        try:
            os.write(2, b'FAILED_RECEIPT_WRITE: reserved attempt consumed; reconcile\n')
        except BaseException:
            pass
        return False

def main():
    require(len(sys.argv) == 3 and sys.argv[1] == '--execute', 'exact --execute Root-READY path required')
    self_bytes = read_file(pathlib.Path(__file__))
    plan_bytes = read_file(PLAN, 32768)
    plan = json_buffer(plan_bytes)
    ready_bytes = read_file(pathlib.Path(sys.argv[2]), 32768)
    ready = json_buffer(ready_bytes)
    fields = {'status','issuer','scope','attempt','created_unix','harness_sha256','plan_sha256',
      'runtime_sha256','isolated_base_head','root_head','root_source_handoff_ref','shared_budget',
      'source_files','accepted_cpp','format_binding','accepted_guard_review','predecessor_ref',
      'explicit_environment_only_sampled_storage_acknowledged','comment_only_cpp'}
    require(type(ready) is dict and set(ready) == fields, 'exact READY schema')
    require(ready['status'] == 'READY' and ready['issuer'] == 'Root' and ready['scope'] == SCOPE and ready['attempt'] == ATTEMPT, 'Root READY identity')
    require(finite(ready['created_unix']) and 0 <= time.time()-ready['created_unix'] <= 300, 'fresh READY <=300s')
    require(ready['harness_sha256'] == sha(self_bytes) and ready['plan_sha256'] == sha(plan_bytes), 'current v3 H/P')
    require(ready['runtime_sha256'] == RUNTIME_SHA and ready['isolated_base_head'] == BASE_HEAD, 'runtime/isolated base')
    require(type(ready['root_head']) is str and re.fullmatch('[0-9a-f]{40}', ready['root_head']), 'fresh global Root HEAD')
    root_handoff = json_buffer(ref_bytes(ready['root_source_handoff_ref'],maximum=32768))
    require(root_handoff == {'status':'PURE_HANDOFF','issuer':'Root','scope':SCOPE,'attempt':ATTEMPT,
      'root_head':ready['root_head'],'isolated_base_head':BASE_HEAD,
      'source_files':ready['source_files'],'shared_budget':ready['shared_budget']}, 'explicit Root pure SourceRef handoff')
    require(ready['shared_budget'] == {'milestone_start':81,'milestone_ceiling':88,'calls_before':87,'calls_reserved':1,'calls_after':88,'no_rerun':True}, 'sole remaining shared call')
    require(ready['explicit_environment_only_sampled_storage_acknowledged'] is True, 'no OS/native isolation claim')
    require(plan['scope'] == SCOPE and plan['attempts'] == [ATTEMPT] and plan['expected_tests'] == 230, 'finite plan')
    require(plan['baseline_source_files'] == BASELINE and plan['ancestor_files'] == ANCESTORS, 'plan frozen/current separation')
    pred = predecessor(ready['predecessor_ref'])
    before = source_evidence(ready)
    # Runtime hashing streams the installed executable; it is never executed as a probe.
    h = hashlib.sha256()
    with RUNTIME.open('rb') as stream:
        for block in iter(lambda: stream.read(65536), b''):
            h.update(block)
    require(h.hexdigest() == RUNTIME_SHA, 'runtime digest')
    require(sha(read_file(RAW_HELPER)) == RAW_SHA and sha(read_file(SAMPLER)) == SAMPLER_SHA, 'guard helpers before reservation')
    # Exact predecessor and review gates above precede imports and permanent reservation.
    raw_module = reviewed_module(RAW_HELPER, RAW_SHA, 'reviewed_raw_capture')
    sampler = reviewed_module(SAMPLER, SAMPLER_SHA, 'reviewed_owned_tmp_sampler')
    folder = pathlib.Path('/tmp/qcl-DOCS-ROUTING-GREEN-1')
    folder.mkdir(mode=0o700, exist_ok=False)
    started = time.monotonic()
    process = capture = stream = None
    collector_construction_attempted = False
    record = {'scope':SCOPE,'attempt':ATTEMPT,'attempt_consumed':True,'target_calls':0,
      'verdict':'STOP_RECONCILE_NO_RERUN','stop_reason':'reserved_not_terminal',
      'ready_sha256':sha(ready_bytes),'harness_sha256':sha(self_bytes),'plan_sha256':sha(plan_bytes),
      'source_before':before,'source_after':None,'runtime_sha256':RUNTIME_SHA,
      'root_head':ready['root_head'],'isolated_base_head':BASE_HEAD,'shared_budget':ready['shared_budget'],
      'red_predecessor':pred,'nominal_source_registration_count':230,'observed_engine_tests':None,
      'unit_result':'requires_independent_complete_TAP_review'}
    require(receipt_write(folder, record), 'reservation receipt unavailable')
    def terminal(signum, frame):
        try:
            if process is not None:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            record.update(stop_reason='terminal_guard_120s', target_calls=int(process is not None),
                raw_capture_complete=False, sampled_peak_process_tree_RSS_bytes=None,
                RSS_status='unknown_terminal_guard',collector_construction_attempted=collector_construction_attempted,
                collector_ownership='unknown' if collector_construction_attempted and capture is None else ('known' if capture is not None else 'not_attempted'))
            receipt_write(folder, record, 'terminal-guard-receipt.json')
            receipt_write(folder, record)
        finally:
            os._exit(2)
    signal.signal(signal.SIGALRM, terminal)
    signal.setitimer(signal.ITIMER_REAL, max(.001,WALL-(time.monotonic()-started)))
    temporary = folder/'owned-tmp'
    reason = error = capture_error = None
    complete, captured = False, 0
    peak_rss = None
    rss_attempts = rss_valid = rss_unknown = tmp_samples = 0
    rss_na_proofs = []
    peak_temp = regular_peak = None
    initial_tmp = final_tmp = None
    after = None
    env = None
    raw_digest = None
    def observe():
        nonlocal rss_attempts, rss_valid, rss_unknown, peak_rss, tmp_samples, peak_temp, regular_peak, reason
        value = tmp_bytes(temporary)
        payload = sampler.sample_owned_temporary_bytes(temporary)
        tmp_samples += 1
        peak_temp = value if peak_temp is None else max(peak_temp,value)
        regular_peak = payload if regular_peak is None else max(regular_peak,payload)
        if process is not None:
            # poll() establishes waitpid/reap or an already-owned terminal returncode
            # BEFORE deciding whether to attempt RSS. No retrospective waiver.
            reaped_code = process.poll()
            if reaped_code is not None:
                rss_na_proofs.append({'proof':'Popen.poll_returncode_before_RSS_attempt',
                  'pid':process.pid,'returncode':reaped_code,'elapsed_seconds':time.monotonic()-started})
            else:
                rss_attempts += 1
                value = rss_tree(process.pid)
                if value is None:
                    rss_unknown += 1
                    reason = reason or 'attempted_live_RSS_unknown'
                else:
                    rss_valid += 1
                    peak_rss = value if peak_rss is None else max(peak_rss,value)
        if time.monotonic()-started >= 108:
            reason = reason or 'wall_stop_108s_terminal_reserve'
        if peak_temp is not None and peak_temp >= TEMP:
            reason = reason or 'owned_TMP_cap'
        if peak_rss is not None and peak_rss >= RAM:
            reason = reason or 'sampled_RSS_cap'
        if capture is not None and capture.bytes >= LOG-128*1024:
            reason = reason or 'raw_output_stop_threshold'
        if capture is not None and capture.error:
            reason = reason or 'raw_capture_error'
        return peak_temp
    try:
        directory(folder)
        temporary.mkdir(mode=0o700)
        for name in ('deno-cache','home','tmp'):
            (temporary/name).mkdir(mode=0o700)
            directory(temporary/name)
        directory(temporary)
        env = {key:str(temporary/name) for key,name in [('DENO_DIR','deno-cache'),('TMPDIR','tmp'),('HOME','home')]}
        require(snapshot(ready['source_files']) == before, 'prelaunch source drift')
        stream = (folder/'original.log').open('xb', buffering=0)
        initial_tmp = observe()
        require(reason is None, 'prelaunch resource bound')
        process = subprocess.Popen(command(), cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, preexec_fn=child_limits)
        observe()
        collector_construction_attempted = True
        capture = raw_module.RawCapture(process.stdout, stream)
        while process.poll() is None:
            observe()
            if reason:
                break
            time.sleep(.05)
        if not reason:
            process.wait(timeout=1)
    except BaseException:
        error = traceback.format_exc()
        reason = reason or 'guard_exception'
    finally:
        # Failures of individual terminal operations cannot skip the consumed receipt.
        try:
            stop_owned(process)
        except BaseException:
            error = (error or '')+traceback.format_exc()
            reason = reason or 'cleanup_unknown'
        if collector_construction_attempted and capture is None:
            # Thread.start can raise after its native thread started. Ownership is
            # UNKNOWN; neither fallback pipe reads nor stream.close are safe here.
            retained_prefix_bytes = None
            try:
                retained_prefix_bytes = (folder/'original.log').stat().st_size
            except BaseException:
                pass
            record.update(verdict='STOP_RECONCILE_NO_RERUN',stop_reason='collector_construction_unknown',
              target_calls=int(process is not None),guard_error=error,collector_construction_attempted=True,
              collector_terminal=None,raw_capture_complete=False,raw_sha256=None,
              raw_bytes=None,retained_prefix_observed_bytes=retained_prefix_bytes,
              RSS_attempted_samples=rss_attempts,RSS_valid_samples=rss_valid,RSS_unknown_samples=rss_unknown,
              RSS_NA_after_reap_count=len(rss_na_proofs),RSS_NA_after_reap_proofs=rss_na_proofs,
              sampled_peak_process_tree_RSS_bytes=peak_rss,
              sampled_peak_owned_tmp_all_entry_st_size_bytes=peak_temp)
            receipt_write(folder,record)
            # Alarm remains active; do not enter non-daemon shutdown join.
            os._exit(2)
        try:
            if capture is not None:
                complete = capture.finish(2)
                captured, capture_error = capture.bytes, capture.error
            elif process is not None and stream is not None:
                # Preserve a bounded prefix on collector failure; EOF alone proves complete.
                os.set_blocking(process.stdout.fileno(), False)
                deadline = time.monotonic()+2
                while time.monotonic()<deadline and captured<LOG:
                    if not select.select([process.stdout],[],[],.05)[0]:
                        continue
                    block = os.read(process.stdout.fileno(), min(65536,LOG-captured))
                    if not block:
                        complete = True
                        break
                    view = memoryview(block)
                    while view:
                        count = stream.write(view)
                        require(type(count) is int and count>0, 'capture fallback no progress')
                        captured += count
                        view = view[count:]
                reason = reason or 'collector_not_started'
        except BaseException:
            capture_error = traceback.format_exc()
            reason = reason or 'capture_finalize_failure'
        try:
            if capture is None and stream is not None and not stream.closed:
                stream.close()
        except BaseException:
            error = (error or '')+traceback.format_exc()
        try:
            final_tmp = observe()
        except BaseException:
            error = (error or '')+traceback.format_exc()
            reason = reason or 'terminal_TMP_unknown'
        try:
            after = snapshot(ready['source_files'])
            require(after == before and sha(read_file(pathlib.Path(__file__))) == sha(self_bytes) and sha(read_file(PLAN,32768)) == sha(plan_bytes), 'terminal source/H/P drift')
            require(sha(read_file(RAW_HELPER)) == RAW_SHA and sha(read_file(SAMPLER)) == SAMPLER_SHA, 'terminal guard helper drift')
            require(sha(read_file(pathlib.Path(sys.argv[2]),32768)) == sha(ready_bytes), 'READY drift')
            source_evidence(ready)
            predecessor(ready['predecessor_ref'])
        except BaseException:
            error = (error or '')+traceback.format_exc()
            reason = reason or 'terminal_binding_unknown'
        try:
            if complete and captured <= LOG:
                data = read_file(folder/'original.log',LOG)
                require(len(data) == captured, 'raw capture size reconciliation')
                raw_digest = sha(data)
        except BaseException:
            error = (error or '')+traceback.format_exc()
            reason = reason or 'raw_readback_failure'
        elapsed = time.monotonic()-started
        if rss_valid < 1:
            reason = reason or 'RSS_not_measured'
        if rss_unknown != 0:
            reason = reason or 'attempted_live_RSS_unknown'
        if initial_tmp is None or final_tmp is None:
            reason = reason or 'TMP_not_measured'
        if not complete or capture_error:
            reason = reason or 'incomplete_capture'
        if captured > LOG:
            reason = reason or 'raw_output_overrun'
        if elapsed > WALL:
            reason = reason or 'terminal_wall_cap'
        if process is None or process.returncode != 0:
            reason = reason or 'child_nonzero_or_unknown'
        good = reason is None and error is None and raw_digest is not None and after == before
        record.update(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
          verdict='CAPTURED_REQUIRES_INDEPENDENT_TAP230_REVIEW' if good else 'STOP_RECONCILE_NO_RERUN',
          target_calls=int(process is not None), child_pid=process.pid if process is not None else None, command=command(), cwd=str(ROOT),
          environment_clear=True, environment=env, source_after=after,
          exit_code=process.returncode if process is not None else None, wall_seconds=elapsed,
          RSS_attempted_samples=rss_attempts,RSS_valid_samples=rss_valid,RSS_unknown_samples=rss_unknown,
          RSS_NA_after_reap_count=len(rss_na_proofs),RSS_NA_after_reap_proofs=rss_na_proofs,
          sampled_peak_process_tree_RSS_bytes=peak_rss,RSS_status='sampled_with_gaps' if rss_valid and rss_unknown else ('sampled' if rss_valid else 'unknown'),
          TMP_sample_count=tmp_samples,sampled_peak_owned_tmp_all_entry_st_size_bytes=peak_temp,
          sampled_regular_payload_peak_bytes=regular_peak,initial_TMP_bytes=initial_tmp,final_TMP_bytes=final_tmp,
          raw_capture_complete=complete,raw_capture_error=capture_error,raw_bytes=captured,
          raw_sha256=raw_digest,raw_output_overrun=captured>LOG,stop_reason=reason,guard_error=error,
          collector_construction_attempted=collector_construction_attempted,
          collector_terminal=(not collector_construction_attempted) if capture is None else not capture.thread.is_alive(),
          RawCapture_sha256=RAW_SHA,sampler_sha256=SAMPLER_SHA,
          limits={'wall_seconds':WALL,'cpu_affinity_count':1,'RLIMIT_CPU_seconds':120,
            'sampled_RSS_stop_bytes':RAM,'sampled_owned_TMP_stop_bytes':TEMP,'raw_bytes_envelope':LOG},
          limitations='Explicit env only; no OS filesystem/cgroup/native isolation. Sampled RSS/TMP permit overshoot; unknown samples remain explicit. Process-group cleanup is local engineering only. TAP230/name/count/skip/fail/only acceptance is independent; guard return0 is not test pass.')
        saved = receipt_write(folder,record)
        # R1: finish(timeout)==False does not establish non-daemon thread termination.
        # Retain incomplete original and consumed receipt, then avoid Python shutdown join.
        if capture is not None and capture.thread.is_alive():
            record.update(verdict='STOP_RECONCILE_NO_RERUN',stop_reason='collector_not_terminal',
                          raw_capture_complete=False,collector_terminal=False)
            receipt_write(folder,record)
            os._exit(2)
        if not saved:
            os._exit(2)
        signal.setitimer(signal.ITIMER_REAL,0)
    return 0 if good and saved else 1

SOURCE_STAGES = {'FORMAT2': ('fmt',4,5), 'LINT2': ('lint',5,6), 'CHECK1': ('check',6,7)}
SOURCE_TEMP = 32*1024**2

def source_command(stage):
    verb = SOURCE_STAGES[stage][0]
    args = [str(RUNTIME),verb,'--config',str(CONFIG)]
    if stage == 'CHECK1':
        args += ['--no-lock','--cached-only','--no-npm','--no-remote']
    return args+[HELPER,FIXTURE]

def observed_source_files():
    return {name:sha(read_file(ROOT/name)) for name in (HELPER,FIXTURE)}

def source_attempt(stage):
    return 'DOCS-ROUTING-SOURCE-'+stage[:-1]+'-'+stage[-1]

def source_receipt_ref(ref, stage, sources):
    attempt = source_attempt(stage)
    folder = pathlib.Path('/tmp')/('qcl-'+attempt)
    record = json_buffer(ref_bytes(ref,str(folder/'receipt.json'),32768))
    require(record['scope'] == SCOPE and record['attempt'] == attempt and record['stage'] == stage, 'source predecessor stage')
    require(record['verdict'] == 'CAPTURED_REQUIRES_INDEPENDENT_SOURCE_REVIEW', 'source predecessor captured result')
    require(type(record['target_calls']) is int and record['target_calls'] == 1, 'one source tool call')
    require(type(record['exit_code']) is int and record['exit_code'] == 0, 'source tool exit0')
    require(record['source_after'] == sources and record['config_sha256'] == CONFIG_SHA, 'source predecessor output/config')
    require(record['source_before'] == (BASELINE if stage == 'FORMAT2' else sources), 'source predecessor input ancestry')
    require(record['test_registration_performed'] is False and record['observed_engine_tests'] is None, 'source tools do not register tests')
    require(record['command'] == source_command(stage) and record['cwd'] == str(ROOT), 'source predecessor command')
    require(record['guard_error'] is None and record['stop_reason'] is None and record['raw_capture_error'] is None, 'source predecessor errors')
    require(record['raw_capture_complete'] is True and record['raw_output_overrun'] is False and record['collector_terminal'] is True, 'source predecessor complete')
    require(record['collector_construction_attempted'] is True, 'source predecessor known collector construction')
    require(type(record['RSS_valid_samples']) is int and record['RSS_valid_samples'] >= 1, 'source predecessor RSS')
    require(type(record['RSS_unknown_samples']) is int and record['RSS_unknown_samples'] == 0, 'attempted-live RSS unknown blocks predecessor')
    require(type(record['RSS_attempted_samples']) is int and record['RSS_attempted_samples'] == record['RSS_valid_samples']+record['RSS_unknown_samples'], 'RSS attempted counters reconcile')
    proofs = record['RSS_NA_after_reap_proofs']
    require(type(proofs) is list and len(proofs) <= 4 and type(record['RSS_NA_after_reap_count']) is int and record['RSS_NA_after_reap_count'] == len(proofs), 'RSS terminal N/A counters')
    for proof in proofs:
        require(type(proof) is dict and set(proof) == {'proof','pid','returncode','elapsed_seconds'}, 'RSS terminal proof shape')
        require(proof['proof'] == 'Popen.poll_returncode_before_RSS_attempt' and type(proof['pid']) is int and proof['pid'] > 0 and proof['pid'] == record['child_pid'] and type(proof['returncode']) is int and proof['returncode'] == record['exit_code'] and finite(proof['elapsed_seconds']) and 0 <= proof['elapsed_seconds'] <= WALL, 'RSS pre-sampling terminal proof')
    require(finite(record['wall_seconds']) and 0 <= record['wall_seconds'] <= WALL, 'source predecessor wall')
    require(type(record['sampled_peak_process_tree_RSS_bytes']) is int and 0 <= record['sampled_peak_process_tree_RSS_bytes'] < RAM, 'source predecessor RSS cap')
    require(type(record['sampled_peak_owned_tmp_all_entry_st_size_bytes']) is int and 0 <= record['sampled_peak_owned_tmp_all_entry_st_size_bytes'] < SOURCE_TEMP, 'source predecessor TMP cap')
    require(record['limits'] == {'wall_seconds':WALL,'cpu_affinity_count':1,'RLIMIT_CPU_seconds':120,
      'sampled_RSS_stop_bytes':RAM,'sampled_owned_TMP_stop_bytes':SOURCE_TEMP,'raw_bytes_envelope':LOG}, 'source predecessor limits')
    require(record['environment_clear'] is True and record['environment'] == {
      key:str(folder/'owned-tmp'/name) for key,name in [('DENO_DIR','deno-cache'),('TMPDIR','tmp'),('HOME','home')]}, 'source predecessor env')
    data = ref_bytes({'path':str(folder/'original.log'),'sha256':record['raw_sha256']},maximum=LOG)
    require(type(record['raw_bytes']) is int and len(data) == record['raw_bytes'] <= LOG, 'source predecessor raw size')
    return record

def source_main(stage, wrapper_path, wrapper_bytes, guard_bytes):
    # Called by one of three exact-buffer wrappers; never selected from caller input.
    require(stage in SOURCE_STAGES and len(sys.argv) == 3 and sys.argv[1] == '--execute', 'exact source stage READY call')
    plan_bytes = read_file(PLAN,32768)
    plan = json_buffer(plan_bytes)
    ready_bytes = read_file(pathlib.Path(sys.argv[2]),32768)
    ready = json_buffer(ready_bytes)
    fields = {'status','issuer','scope','stage','attempt','created_unix','wrapper_sha256',
      'guard_sha256','plan_sha256','runtime_sha256','config_sha256','isolated_base_head',
      'root_head','root_source_handoff_ref','shared_source_budget','source_before',
      'accepted_guard_review','accepted_pure_cpp_ref','pure_only_slice','format_binding',
      'previous_receipt_refs','explicit_environment_only_sampled_storage_acknowledged','comment_only_cpp'}
    require(type(ready) is dict and set(ready) == fields, 'exact source READY fields')
    attempt = source_attempt(stage)
    require(ready['status'] == 'READY' and ready['issuer'] == 'Root' and ready['scope'] == SCOPE and ready['stage'] == stage and ready['attempt'] == attempt, 'source Root identity')
    require(finite(ready['created_unix']) and 0 <= time.time()-ready['created_unix'] <= 300, 'source READY freshness')
    require(ready['wrapper_sha256'] == sha(wrapper_bytes) and ready['guard_sha256'] == sha(guard_bytes) and ready['plan_sha256'] == sha(plan_bytes), 'source executable current hashes')
    require(sha(read_file(wrapper_path)) == sha(wrapper_bytes) and sha(read_file(pathlib.Path(__file__))) == sha(guard_bytes), 'same-buffer executable identity')
    require(plan['scope'] == SCOPE and plan['baseline_source_files'] == BASELINE and plan['ancestor_files'] == ANCESTORS, 'source plan immutable bindings')
    require(ready['runtime_sha256'] == RUNTIME_SHA and ready['config_sha256'] == CONFIG_SHA and sha(read_file(CONFIG)) == CONFIG_SHA, 'source runtime/config')
    require(ready['isolated_base_head'] == BASE_HEAD and type(ready['root_head']) is str and re.fullmatch('[0-9a-f]{40}',ready['root_head']), 'separate global/isolated revisions')
    before = snapshot(ready['source_before'])
    comment_correction_evidence(ready)
    h = ref_bytes(ready['root_source_handoff_ref'],maximum=32768)
    handoff = json_buffer(h)
    expected_handoff = {'status':'SOURCE_HANDOFF','issuer':'Root','scope':SCOPE,'stage':stage,
      'root_head':ready['root_head'],'isolated_base_head':BASE_HEAD,'source_before':before,
      'config_sha256':CONFIG_SHA,'shared_source_budget':ready['shared_source_budget']}
    require(handoff == expected_handoff, 'explicit Root SourceRef handoff, not CP authority marker')
    _, prior_calls, after_calls = SOURCE_STAGES[stage]
    require(ready['shared_source_budget'] == {'maximum_calls':8,'calls_before':prior_calls,'calls_reserved':1,'calls_after':after_calls,'no_rerun':True}, 'source total eight-call ceiling')
    require(ready['pure_only_slice'] is True and ready['accepted_pure_cpp_ref'] == PURE_CPP, 'pure-only CPP slice, whole I2B remains changes-required')
    ref_bytes(PURE_CPP)
    require(ready['explicit_environment_only_sampled_storage_acknowledged'] is True, 'source env-only acknowledgment')
    review = ready['accepted_guard_review']
    require(type(review) is dict and set(review) == {'status','wrapper_sha256','guard_sha256','plan_sha256','report_ref'}, 'source supervisor review schema')
    require(review['status'] == 'PASS_SOURCE' and all(review[key] == ready[key] for key in ('wrapper_sha256','guard_sha256','plan_sha256')), 'source supervisor review identities')
    ref_bytes(review['report_ref'])
    previous = ready['previous_receipt_refs']
    required_previous = {'FORMAT2':set(),'LINT2':{'FORMAT2'},'CHECK1':{'FORMAT2','LINT2'}}[stage]
    require(type(previous) is dict and set(previous) == required_previous, 'source stage ordering')
    for previous_stage, ref in previous.items():
        source_receipt_ref(ref,previous_stage,before)
    if stage == 'FORMAT2':
        require(before == BASELINE and ready['format_binding'] is None, 'FORMAT2 exact new comment baseline only')
    else:
        fmt = ready['format_binding']
        require(type(fmt) is dict and set(fmt) == {'status','unformatted_sources','formatted_sources','review_ref','receipt_ref'}, 'independent format-only binding')
        require(fmt['status'] == 'PASS_FORMAT_ONLY' and fmt['unformatted_sources'] == BASELINE and fmt['formatted_sources'] == before and fmt['receipt_ref'] == previous['FORMAT2'], 'format-only comment baseline to final')
        ref_bytes(fmt['review_ref'])
    # Root verifies substantive approvals/provenance; same-user JSON is not authentication.
    rh = hashlib.sha256()
    with RUNTIME.open('rb') as stream:
        for block in iter(lambda:stream.read(65536),b''):
            rh.update(block)
    require(rh.hexdigest() == RUNTIME_SHA,'source runtime executable hash')
    raw_module = reviewed_module(RAW_HELPER,RAW_SHA,'source_reviewed_capture')
    sampler = reviewed_module(SAMPLER,SAMPLER_SHA,'source_reviewed_sampler')
    folder = pathlib.Path('/tmp')/('qcl-'+attempt)
    folder.mkdir(mode=0o700,exist_ok=False)
    start = time.monotonic()
    process = capture = stream = None
    collector_construction_attempted = False
    reason = error = capture_error = None
    complete, captured, digest = False, 0, None
    after = env = initial_tmp = final_tmp = None
    peak_rss = peak_tmp = regular_peak = None
    rss_attempts = rss_valid = rss_unknown = tmp_samples = 0
    rss_na_proofs = []
    record = {'scope':SCOPE,'stage':stage,'attempt':attempt,'attempt_consumed':True,
      'verdict':'STOP_RECONCILE_NO_RERUN','target_calls':0,'stop_reason':'reserved_not_terminal',
      'wrapper_sha256':sha(wrapper_bytes),'guard_sha256':sha(guard_bytes),'plan_sha256':sha(plan_bytes),
      'ready_sha256':sha(ready_bytes),'root_head':ready['root_head'],'isolated_base_head':BASE_HEAD,
      'source_before':before,'source_after':None,'config_sha256':CONFIG_SHA,'runtime_sha256':RUNTIME_SHA,
      'shared_source_budget':ready['shared_source_budget'],'pure_only_slice':True,
      'observed_engine_tests':None,'test_registration_performed':False}
    require(receipt_write(folder,record),'source reservation receipt unavailable')
    def terminal(signum,frame):
        try:
            if process is not None:
                try:
                    os.killpg(process.pid,signal.SIGKILL)
                except ProcessLookupError:
                    pass
            record.update(stop_reason='terminal_guard_120s',target_calls=int(process is not None),
                raw_capture_complete=False,collector_terminal=False,sampled_peak_process_tree_RSS_bytes=None,RSS_status='unknown_terminal_guard',
                collector_construction_attempted=collector_construction_attempted,
                collector_ownership='unknown' if collector_construction_attempted and capture is None else ('known' if capture is not None else 'not_attempted'))
            receipt_write(folder,record,'terminal-guard-receipt.json')
            receipt_write(folder,record)
        finally:
            os._exit(2)
    signal.signal(signal.SIGALRM,terminal)
    signal.setitimer(signal.ITIMER_REAL,max(.001,WALL-(time.monotonic()-start)))
    temporary = folder/'owned-tmp'
    def observe():
        nonlocal rss_attempts,rss_valid,rss_unknown,peak_rss,peak_tmp,regular_peak,tmp_samples,reason
        value = tmp_bytes(temporary)
        regular = sampler.sample_owned_temporary_bytes(temporary)
        tmp_samples += 1
        peak_tmp = value if peak_tmp is None else max(peak_tmp,value)
        regular_peak = regular if regular_peak is None else max(regular_peak,regular)
        if process is not None:
            reaped_code = process.poll()
            if reaped_code is not None:
                rss_na_proofs.append({'proof':'Popen.poll_returncode_before_RSS_attempt',
                  'pid':process.pid,'returncode':reaped_code,'elapsed_seconds':time.monotonic()-start})
            else:
                rss_attempts += 1
                value = rss_tree(process.pid)
                if value is None:
                    rss_unknown += 1
                    reason = reason or 'attempted_live_RSS_unknown'
                else:
                    rss_valid += 1
                    peak_rss = value if peak_rss is None else max(peak_rss,value)
        if time.monotonic()-start >= 108:
            reason = reason or 'wall_stop_108s_terminal_reserve'
        if peak_tmp >= SOURCE_TEMP:
            reason = reason or 'source_TMP_cap'
        if peak_rss is not None and peak_rss >= RAM:
            reason = reason or 'sampled_RSS_cap'
        if capture is not None and capture.bytes >= LOG-128*1024:
            reason = reason or 'raw_stop_threshold'
        if capture is not None and capture.error:
            reason = reason or 'raw_capture_error'
        return peak_tmp
    try:
        directory(folder)
        temporary.mkdir(mode=0o700)
        for name in ('deno-cache','home','tmp'):
            (temporary/name).mkdir(mode=0o700)
            directory(temporary/name)
        directory(temporary)
        env = {key:str(temporary/name) for key,name in [('DENO_DIR','deno-cache'),('TMPDIR','tmp'),('HOME','home')]}
        require(snapshot(before) == before and sha(read_file(CONFIG)) == CONFIG_SHA,'source prelaunch bindings')
        stream = (folder/'original.log').open('xb',buffering=0)
        initial_tmp = observe()
        require(reason is None,'source prelaunch resources')
        process = subprocess.Popen(source_command(stage),cwd=ROOT,env=env,stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,preexec_fn=child_limits)
        observe()
        collector_construction_attempted = True
        capture = raw_module.RawCapture(process.stdout,stream)
        while process.poll() is None:
            observe()
            if reason:
                break
            time.sleep(.05)
        if not reason:
            process.wait(timeout=1)
    except BaseException:
        error = traceback.format_exc()
        reason = reason or 'source_guard_exception'
    finally:
        try:
            stop_owned(process)
        except BaseException:
            error = (error or '')+traceback.format_exc()
            reason = reason or 'source_cleanup_unknown'
        if collector_construction_attempted and capture is None:
            retained_prefix_bytes = None
            try:
                retained_prefix_bytes = (folder/'original.log').stat().st_size
            except BaseException:
                pass
            record.update(verdict='STOP_RECONCILE_NO_RERUN',stop_reason='collector_construction_unknown',
              target_calls=int(process is not None),guard_error=error,collector_construction_attempted=True,
              collector_terminal=None,raw_capture_complete=False,raw_sha256=None,
              raw_bytes=None,retained_prefix_observed_bytes=retained_prefix_bytes,
              RSS_attempted_samples=rss_attempts,RSS_valid_samples=rss_valid,RSS_unknown_samples=rss_unknown,
              RSS_NA_after_reap_count=len(rss_na_proofs),RSS_NA_after_reap_proofs=rss_na_proofs,
              sampled_peak_process_tree_RSS_bytes=peak_rss,
              sampled_peak_owned_tmp_all_entry_st_size_bytes=peak_tmp)
            receipt_write(folder,record)
            os._exit(2)
        try:
            if capture is not None:
                complete = capture.finish(2)
                captured,capture_error = capture.bytes,capture.error
            elif process is not None and stream is not None:
                os.set_blocking(process.stdout.fileno(),False)
                deadline = time.monotonic()+2
                while time.monotonic()<deadline and captured<LOG:
                    if not select.select([process.stdout],[],[],.05)[0]:
                        continue
                    block = os.read(process.stdout.fileno(),min(65536,LOG-captured))
                    if not block:
                        complete = True
                        break
                    view = memoryview(block)
                    while view:
                        count = stream.write(view)
                        require(type(count) is int and count>0,'source fallback no progress')
                        captured += count
                        view = view[count:]
                reason = reason or 'source_collector_not_started'
        except BaseException:
            capture_error = traceback.format_exc()
            reason = reason or 'source_capture_finalize_failure'
        try:
            if capture is None and stream is not None and not stream.closed:
                stream.close()
        except BaseException:
            error = (error or '')+traceback.format_exc()
        try:
            final_tmp = observe()
        except BaseException:
            error = (error or '')+traceback.format_exc()
            reason = reason or 'source_terminal_TMP_unknown'
        try:
            after = observed_source_files()
            require(stage == 'FORMAT2' or after == before,'lint/check mutated source')
            require(sha(read_file(CONFIG)) == CONFIG_SHA,'source config drift')
            require(sha(read_file(wrapper_path)) == sha(wrapper_bytes) and sha(read_file(pathlib.Path(__file__))) == sha(guard_bytes) and sha(read_file(PLAN,32768)) == sha(plan_bytes),'source executable drift')
            require(sha(read_file(pathlib.Path(sys.argv[2]),32768)) == sha(ready_bytes),'source READY drift')
            require(sha(read_file(RAW_HELPER)) == RAW_SHA and sha(read_file(SAMPLER)) == SAMPLER_SHA,'source helper drift')
            require(ref_bytes(ready['root_source_handoff_ref'],maximum=32768) == h,'source Root handoff drift')
            ref_bytes(review['report_ref'])
            ref_bytes(PURE_CPP)
            comment_correction_evidence(ready)
            for previous_stage,ref in previous.items():
                source_receipt_ref(ref,previous_stage,before)
            if stage != 'FORMAT2':
                ref_bytes(ready['format_binding']['review_ref'])
        except BaseException:
            error = (error or '')+traceback.format_exc()
            reason = reason or 'source_terminal_bindings_unknown'
        try:
            if complete and captured<=LOG:
                data = read_file(folder/'original.log',LOG)
                require(len(data) == captured,'source raw size reconciliation')
                digest = sha(data)
        except BaseException:
            error = (error or '')+traceback.format_exc()
            reason = reason or 'source_raw_readback_failure'
        elapsed = time.monotonic()-start
        if rss_valid<1:
            reason = reason or 'RSS_not_measured'
        if rss_unknown != 0:
            reason = reason or 'attempted_live_RSS_unknown'
        if initial_tmp is None or final_tmp is None:
            reason = reason or 'TMP_not_measured'
        if not complete or capture_error:
            reason = reason or 'incomplete_capture'
        if captured>LOG:
            reason = reason or 'raw_output_overrun'
        if elapsed>WALL:
            reason = reason or 'terminal_wall_cap'
        if process is None or process.returncode != 0:
            reason = reason or 'source_child_nonzero_or_unknown'
        good = reason is None and error is None and digest is not None and after is not None
        record.update(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
          verdict='CAPTURED_REQUIRES_INDEPENDENT_SOURCE_REVIEW' if good else 'STOP_RECONCILE_NO_RERUN',
          target_calls=int(process is not None),child_pid=process.pid if process is not None else None,command=source_command(stage),cwd=str(ROOT),environment_clear=True,environment=env,
          source_after=after,exit_code=process.returncode if process is not None else None,wall_seconds=elapsed,
          RSS_attempted_samples=rss_attempts,RSS_valid_samples=rss_valid,RSS_unknown_samples=rss_unknown,
          RSS_NA_after_reap_count=len(rss_na_proofs),RSS_NA_after_reap_proofs=rss_na_proofs,
          sampled_peak_process_tree_RSS_bytes=peak_rss,RSS_status='sampled_with_gaps' if rss_valid and rss_unknown else ('sampled' if rss_valid else 'unknown'),
          TMP_sample_count=tmp_samples,sampled_peak_owned_tmp_all_entry_st_size_bytes=peak_tmp,
          sampled_regular_payload_peak_bytes=regular_peak,initial_TMP_bytes=initial_tmp,final_TMP_bytes=final_tmp,
          raw_capture_complete=complete,raw_capture_error=capture_error,raw_bytes=captured,raw_sha256=digest,
          raw_output_overrun=captured>LOG,stop_reason=reason,guard_error=error,
          collector_construction_attempted=collector_construction_attempted,
          collector_terminal=(not collector_construction_attempted) if capture is None else not capture.thread.is_alive(),
          RawCapture_sha256=RAW_SHA,sampler_sha256=SAMPLER_SHA,
          limits={'wall_seconds':WALL,'cpu_affinity_count':1,'RLIMIT_CPU_seconds':120,
            'sampled_RSS_stop_bytes':RAM,'sampled_owned_TMP_stop_bytes':SOURCE_TEMP,'raw_bytes_envelope':LOG},
          limitations='Source tools only, no tests/registration/module execution by check. No native/CI/science acceptance. Sampled env-only guards permit gaps/overshoot; independent source/format review required.')
        saved = receipt_write(folder,record)
        if capture is not None and capture.thread.is_alive():
            record.update(verdict='STOP_RECONCILE_NO_RERUN',stop_reason='collector_not_terminal',raw_capture_complete=False,collector_terminal=False)
            receipt_write(folder,record)
            os._exit(2)
        if not saved:
            os._exit(2)
        signal.setitimer(signal.ITIMER_REAL,0)
    return 0 if good and saved else 1

if __name__ == '__main__':
    sys.exit(main())
