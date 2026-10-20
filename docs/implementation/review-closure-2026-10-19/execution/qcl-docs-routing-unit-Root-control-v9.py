import datetime, hashlib, json, os, pathlib, subprocess, time

R=pathlib.Path('/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf');W=pathlib.Path('/tmp/qcl-docs-test-routing-worktree');CP=R/'docs/implementation/review-closure-2026-10-19/execution/checkpoint.json'
HEAD='107bac5697b37cf0e47c3feb44883a907837645c';BASE='2bb05d3651af4509fe7f02c1253b40f1e5146fec';SCOPE='docs-routing-pure-local-engineering-v9';ATTEMPT='DOCS-ROUTING-CORRECTION-E1'
H=pathlib.Path('/tmp/qcl-docs-routing-pure-guard-v9.py');P=pathlib.Path('/tmp/qcl-docs-routing-pure-plan-v9.json');REVIEW=pathlib.Path('/tmp/qcl-docs-routing-pure-harness-v9-review.md')
OUTCOME=pathlib.Path('/tmp/qcl-docs-routing-pure-source-outcome-v9-review.md');OUTCOME_ID=pathlib.Path('/tmp/qcl-docs-routing-pure-source-outcome-v9-review-identity.json')
OUTCOME_SHA='4f748f195841fc9543468cb7b40caeb268ccfb2960ce296115d725871bf3e3f8';OUTCOME_ID_SHA='7c07c4f61a96a3145fbe1b86de093463f8d16e69cc58c162a2e713492941673f'
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(path,cap=262144):
    p=pathlib.Path(path);assert p.resolve(strict=True)==p and p.is_file() and p.stat().st_uid==os.getuid() and p.stat().st_size<=cap
    b=p.read_bytes();assert len(b)<=cap;return b
def ref(path):return {'path':str(path),'sha256':sha(read(path))}
def exclusive(path,value):
    with path.open('x') as f:json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
def cpwrite(value):
    value['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();temp=CP.with_suffix('.json.pure-unit-v9-tmp');temp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');os.replace(temp,CP)
def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args],env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','GIT_NO_LAZY_FETCH':'1'},text=True,timeout=10).strip()
assert ref(H)['sha256']=='e02576c6b421b158a00a570ca729b076737d47c1e79111606d15fb60a2cba01e'
assert ref(P)['sha256']=='e32f4b534b928cef44cc8e9f35f242e979752b12b70e9eea687c5cca3cc3b2af'
assert ref(REVIEW)['sha256']=='33a3902a914e8f270999eb6b9bd169c300776b95288577e5f2085ccf524ef009'
assert OUTCOME_SHA!='PENDING_ROOT_SUBSTANTIVE_REVIEW' and ref(OUTCOME)['sha256']==OUTCOME_SHA
assert OUTCOME_ID_SHA!='PENDING_ROOT_SUBSTANTIVE_REVIEW' and ref(OUTCOME_ID)['sha256']==OUTCOME_ID_SHA
plan=json.loads(read(P));assert plan['scope']==SCOPE and plan['expected_tests']==232
assert git(R,'rev-parse','HEAD')==HEAD and git(W,'rev-parse','HEAD')==BASE
rows=git(R,'ls-tree','HEAD','components/').splitlines();assert len(rows)==8
for line in rows:
    mode,kind,oid,path=line.split(None,3);assert mode=='160000' and kind=='commit' and git(R/path,'rev-parse','HEAD')==oid and not git(R/path,'status','--short')
for line in git(R,'status','--short').splitlines():assert 'docs/implementation/review-closure-2026-10-19/execution/' in line
assert sha(read(W/'deno.json'))==plan['config_sha256']
source={path:sha(read(W/path)) for path in plan['formatted_source_files']};assert source==plan['formatted_source_files']
runtime=pathlib.Path(plan['runtime']['path']);st=runtime.stat();assert st.st_size==141648992;digest=hashlib.sha256();n=0
with runtime.open('rb') as stream:
    while True:
        block=stream.read(65536)
        if not block:break
        n+=len(block);assert n<=141648992;digest.update(block)
assert n==141648992 and digest.hexdigest()==plan['runtime']['sha256'] and all(getattr(runtime.stat(),key)==getattr(st,key) for key in ('st_dev','st_ino','st_size','st_mtime_ns','st_ctime_ns'))
j=json.loads(CP.read_bytes());assert j['source_tool_active'] is None and j['counters']['targeted_test_active'] is None and not j['unknown_outcomes']
assert j['counters']['milestone_source_tools_calls']==12 and j['counters']['targeted_test_total_calls']==90
assert j['resource_current']['engineering_milestone_product_call_cap']==91 and j['resource_current']['source_tools_milestone_call_cap']==12
assert not any(op.get('id')==ATTEMPT for op in j['operations']) and not pathlib.Path('/tmp/qcl-'+ATTEMPT).exists()
rootplan=json.loads(read('/tmp/qcl-docs-routing-diagnostic-Root-engineering-plan-v9.json'));assert rootplan['limits']['aggregate_calls']==5 and rootplan['limits']['aggregate_wall_seconds']==600 and rootplan['limits']['aggregate_raw_bytes']==10485760
receipts={};records=[]
for stage,tail in [('FORMAT3','FORMAT-3'),('LINT3','LINT-3'),('CHECK4','CHECK-4')]:
    p=pathlib.Path('/tmp/qcl-DOCS-ROUTING-SOURCE-'+tail+'/receipt.json');record=json.loads(read(p));receipts[stage]=ref(p);records.append(record)
    assert record['verdict']=='CAPTURED_REQUIRES_INDEPENDENT_SOURCE_REVIEW' and record['exit_code']==0 and record['target_calls']==1 and record['RSS_unknown_samples']==0 and record['RSS_valid_samples']>=1 and record['collector_terminal'] is True and record['raw_capture_complete'] is True and record['source_after']==source
    raw=p.parent/'original.log';assert ref(raw)['sha256']==record['raw_sha256'] and len(read(raw,2097152))==record['raw_bytes']
failed=json.loads(read('/tmp/qcl-DOCS-ROUTING-SOURCE-CHECK-3/receipt.json'));assert failed['verdict']=='STOP_RECONCILE_NO_RERUN' and failed['RSS_unknown_samples']==1
assert sum(record['wall_seconds'] for record in records)+failed['wall_seconds']+120<=600 and sum(record['raw_bytes'] for record in records)+failed['raw_bytes']+2097152<=10485760
binding=json.loads(read('/tmp/qcl-docs-routing-source-format-binding-v8.json'));cpp=binding['accepted_cpp'];fmt=binding['format_binding']
assert cpp['source_files']==source and cpp['report_ref']==plan['accepted_format_and_pure_CPP'] and ref(cpp['report_ref']['path'])==cpp['report_ref']
assert cpp['baseline_cpp_ref']==plan['baseline_CPP'] and ref(cpp['baseline_cpp_ref']['path'])==cpp['baseline_cpp_ref']
assert fmt['receipt_refs']==[receipts['FORMAT3']] and fmt['formatted_sources']==source
fmt['receipt_refs']=[receipts[stage] for stage in ('FORMAT3','LINT3','CHECK4')]
predecessor=pathlib.Path('/tmp/qcl-docs-routing-pure-predecessor-v7.json');pred=json.loads(read(predecessor));assert pred['scope']=='docs-routing-pure-local-engineering-v7' and pred['attempt']=='DOCS-ROUTING-RED-1'
shared={'milestone_start':90,'milestone_ceiling':91,'calls_before':90,'calls_reserved':1,'calls_after':91,'no_rerun':True}
handoff=pathlib.Path('/tmp/qcl-docs-routing-pure-Root-handoff-v9.json');ready=pathlib.Path('/tmp/qcl-docs-routing-pure-Root-ready-v9.json')
exclusive(handoff,{'status':'PURE_HANDOFF','issuer':'Root','scope':SCOPE,'attempt':ATTEMPT,'root_head':HEAD,'isolated_base_head':BASE,'source_files':source,'shared_budget':shared})
exclusive(ready,{'status':'READY','issuer':'Root','scope':SCOPE,'attempt':ATTEMPT,'created_unix':time.time(),'harness_sha256':ref(H)['sha256'],'plan_sha256':ref(P)['sha256'],'runtime_sha256':plan['runtime']['sha256'],'isolated_base_head':BASE,'root_head':HEAD,'root_source_handoff_ref':ref(handoff),'shared_budget':shared,'source_files':source,'accepted_cpp':cpp,'format_binding':fmt,'accepted_guard_review':{'status':'PASS_SOURCE','harness_sha256':ref(H)['sha256'],'plan_sha256':ref(P)['sha256'],'report_ref':ref(REVIEW)},'predecessor_ref':ref(predecessor),'explicit_environment_only_sampled_storage_acknowledged':True})
j['operations'].append({'id':ATTEMPT,'state':'reserved_single_correction_no_rerun','kind':'pure_docs_route_unit_only','root_head':HEAD,'READY_ref':ref(ready),'source_outcome_review':ref(OUTCOME),'source_outcome_review_identity':ref(OUTCOME_ID),'source_before':source,'shared_counter_before':90,'shared_counter_after':91})
j['counters']['targeted_test_active']=ATTEMPT
for key in ('targeted_test_total_calls','targeted_test_calls_total'):j['counters'][key]=91
j['counters']['targeted_tests_by_task']['DOCS_ROUTING']+=1;j['counters']['DOCS_ROUTING_unit_calls']+=1
j['resource_current']['targeted_completed_calls']=90;j['resource_current']['targeted_test_active']=ATTEMPT;cpwrite(j)
start=time.monotonic();result=None;failure=None
try:result=subprocess.run([str(R/'.venv/bin/python'),'-I','-B',str(H),'--execute',str(ready)],cwd=R,capture_output=True,timeout=145)
except BaseException as exc:failure=repr(exc)
outer={'operation_id':ATTEMPT,'wrapper_returncode':None if result is None else result.returncode,'wall_seconds':time.monotonic()-start,'outer_failure':failure,'stdout':None if result is None else result.stdout.decode(errors='replace')[:16384],'stderr':None if result is None else result.stderr.decode(errors='replace')[:16384]}
outer_path=pathlib.Path('/tmp/qcl-docs-routing-pure-Root-outer-v9.json');exclusive(outer_path,outer)
j=json.loads(CP.read_bytes());assert j['counters']['targeted_test_active']==ATTEMPT and j['counters']['targeted_test_total_calls']==91
op=next(op for op in j['operations'] if op['id']==ATTEMPT);op.update({'state':'completed_pending_independent_TAP_review' if result is not None else 'unknown_stop_no_rerun','outer_ref':ref(outer_path),'wrapper_returncode':outer['wrapper_returncode']})
receipt=pathlib.Path('/tmp/qcl-'+ATTEMPT+'/receipt.json')
if receipt.exists():
    record=json.loads(read(receipt));wall=round(record['wall_seconds'],3);op.update({'receipt_ref':ref(receipt),'guard_verdict':record.get('verdict'),'wall_seconds':wall,'target_calls':record.get('target_calls'),'observed_engine_tests':None})
    census_path=pathlib.Path('/tmp/qcl-targeted-receipt-census.json');census=json.loads(census_path.read_bytes());assert len(census)==90 and not any(row['id']=='qcl-'+ATTEMPT for row in census)
    census.append({'id':'qcl-'+ATTEMPT,'wall_seconds':wall,'raw_wall_seconds':record['wall_seconds'],'exit_code':record.get('exit_code'),'receipt_sha256':ref(receipt)['sha256'],'kind':'pure_docs_routing_unit_232_nominal_pending_TAP_review_not_native_science','guard_verdict':record.get('verdict')});census_path.write_text(json.dumps(census,indent=2)+'\n')
    total=round(sum(row['wall_seconds'] for row in census),3)
    for key in ('targeted_test_total_wall_seconds','targeted_test_wall_seconds_total'):j['counters'][key]=total
    j['resource_current'].update({'targeted_completed_calls':91,'targeted_wall_seconds':total})
    j['resource_census'].update({'targeted_receipts':91,'targeted_wall_seconds':total})
    j['targeted_receipt_census'].update({'count':91,'wall_seconds':total,'source_sha256':sha(census_path.read_bytes())})
else:op['receipt_ref']=None
j['counters']['targeted_test_active']=None;j['resource_current']['targeted_test_active']=None
if result is None or not receipt.exists():j['unknown_outcomes'].append({'id':ATTEMPT,'reason':failure or 'missing receipt','resume':'readback process/receipt; no duplicate rerun'})
cpwrite(j)
print(json.dumps({'operation_id':ATTEMPT,'wrapper_exit':outer['wrapper_returncode'],'guard_verdict':op.get('guard_verdict'),'product_calls':91,'wall_seconds':op.get('wall_seconds'),'receipt':str(receipt),'observed_tests':None}))
