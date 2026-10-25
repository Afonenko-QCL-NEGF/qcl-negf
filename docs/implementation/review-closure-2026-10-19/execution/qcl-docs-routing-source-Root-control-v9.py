import datetime, hashlib, json, os, pathlib, subprocess, time

R=pathlib.Path('/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf');W=pathlib.Path('/tmp/qcl-docs-test-routing-worktree')
CP=R/'docs/implementation/review-closure-2026-10-19/execution/checkpoint.json'
HEAD='107bac5697b37cf0e47c3feb44883a907837645c';BASE='2bb05d3651af4509fe7f02c1253b40f1e5146fec';SCOPE='docs-routing-pure-local-engineering-v9'
ATTEMPT='DOCS-ROUTING-SOURCE-CHECK-4';STAGE='CHECK4'
H=pathlib.Path('/tmp/qcl-docs-routing-pure-guard-v9.py');P=pathlib.Path('/tmp/qcl-docs-routing-pure-plan-v9.json');ENTRY=pathlib.Path('/tmp/qcl-docs-routing-pure-check-v9.py')
REVIEW=pathlib.Path('/tmp/qcl-docs-routing-pure-harness-v9-review.md');RID=pathlib.Path('/tmp/qcl-docs-routing-pure-harness-v9-review-identity.json')
HASHES={str(H):'e02576c6b421b158a00a570ca729b076737d47c1e79111606d15fb60a2cba01e',str(P):'e32f4b534b928cef44cc8e9f35f242e979752b12b70e9eea687c5cca3cc3b2af',str(ENTRY):'1dd84dcdf977f458b960e6dd78dbb100e4d3c3c83a60e29430d630a455f91f1a',str(REVIEW):'33a3902a914e8f270999eb6b9bd169c300776b95288577e5f2085ccf524ef009',str(RID):'d12595a7a38544161835b627c218772eaefb5273645d26555340aa0b677e8744'}
ENV={**os.environ,'GIT_OPTIONAL_LOCKS':'0','GIT_NO_LAZY_FETCH':'1'}
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(path,cap=262144):
    p=pathlib.Path(path);assert p.resolve(strict=True)==p and p.is_file() and p.stat().st_uid==os.getuid() and p.stat().st_size<=cap
    b=p.read_bytes();assert len(b)<=cap;return b
def ref(path):return {'path':str(path),'sha256':sha(read(path))}
def git(path,*args):return subprocess.check_output(['git','-C',str(path),*args],env=ENV,text=True,timeout=10).strip()
def exclusive(path,value):
    with path.open('x') as f:json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')
def cpwrite(value):
    value['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();temp=CP.with_suffix('.json.routing-source-v9-tmp');temp.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');os.replace(temp,CP)
for path,digest in HASHES.items():assert sha(read(path))==digest
plan=json.loads(read(P));assert plan['scope']==SCOPE
rid=json.loads(read(RID));assert rid['verdict']=='PASS_SOURCE' and rid['blocking_findings']==[]
for path,digest in rid['reviewed'].items():assert sha(read(path))==digest
assert git(R,'rev-parse','HEAD')==HEAD and git(W,'rev-parse','HEAD')==BASE
rows=git(R,'ls-tree','HEAD','components/').splitlines();assert len(rows)==8
for line in rows:
    mode,kind,oid,path=line.split(None,3);assert mode=='160000' and kind=='commit' and git(R/path,'rev-parse','HEAD')==oid and not git(R/path,'status','--short')
for line in git(R,'status','--short').splitlines():assert 'docs/implementation/review-closure-2026-10-19/execution/' in line
assert sha(read(W/'deno.json'))==plan['config_sha256']
source={name:sha(read(W/name)) for name in plan['formatted_source_files']};assert source==plan['formatted_source_files']
runtime=pathlib.Path(plan['runtime']['path']);st=runtime.stat();assert st.st_size==141648992;digest=hashlib.sha256();n=0
with runtime.open('rb') as stream:
    while True:
        block=stream.read(65536)
        if not block:break
        n+=len(block);assert n<=141648992;digest.update(block)
assert n==141648992 and digest.hexdigest()==plan['runtime']['sha256'] and all(getattr(runtime.stat(),key)==getattr(st,key) for key in ('st_dev','st_ino','st_size','st_mtime_ns','st_ctime_ns'))
j=json.loads(CP.read_bytes());assert j['source_tool_active'] is None and j['counters']['targeted_test_active'] is None and not j['unknown_outcomes']
assert j['counters']['targeted_test_total_calls']==90 and j['counters']['milestone_source_tools_calls']==11
assert j['resource_current']['source_tools_milestone_call_cap']==12 and j['resource_current']['engineering_milestone_product_call_cap']==91
rootplan=json.loads(read('/tmp/qcl-docs-routing-diagnostic-Root-engineering-plan-v9.json'));assert rootplan['operation_id']=='ENG-REPLAN-DOCS-ROUTING-DIAGNOSTIC-CHECK4-1' and rootplan['limits']['aggregate_calls']==5 and rootplan['limits']['aggregate_wall_seconds']==600 and rootplan['limits']['aggregate_raw_bytes']==10*1024**2
assert rootplan['guard']['sha256']==HASHES[str(H)] and rootplan['review']['sha256']==HASHES[str(REVIEW)] and rootplan['review_identity']['sha256']==HASHES[str(RID)]
folder=pathlib.Path('/tmp/qcl-'+ATTEMPT);assert not folder.exists() and not any(o.get('id')==ATTEMPT for o in j['operations'])
binding=json.loads(read('/tmp/qcl-docs-routing-source-format-binding-v8.json'));cpp=binding['accepted_cpp'];fmt=binding['format_binding']
assert cpp['status']=='PASS_SOURCE_PURE_CLOSURE' and cpp['source_files']==source and cpp['pure_only_slice'] is True
# Baseline identity comes from immutable v9 plan, checked against exact source review.
assert cpp['baseline_cpp_ref']==plan['baseline_CPP'];PURE_CPP=plan['baseline_CPP'];assert sha(read(PURE_CPP['path']))==PURE_CPP['sha256']
assert cpp['report_ref']==plan['accepted_format_and_pure_CPP'] and sha(read(cpp['report_ref']['path']))==cpp['report_ref']['sha256']
assert fmt['status']=='PASS_FORMAT_ONLY' and fmt['unformatted_sources']==plan['baseline_source_files'] and fmt['formatted_sources']==source and fmt['review_ref']==cpp['report_ref']
previous={};prefix=[]
for name in ('FORMAT','LINT','CHECK'):
    p=pathlib.Path('/tmp/qcl-DOCS-ROUTING-SOURCE-'+name+'-3/receipt.json');reference=ref(p)
    assert reference=={k:rootplan['retained_prefix'][name][k] for k in ('path','sha256')}
    record=json.loads(read(p));assert record['target_calls']==1 and record['collector_terminal'] is True and record['raw_capture_complete'] is True
    prefix.append(record)
    if name!='CHECK':
        assert record['verdict']=='CAPTURED_REQUIRES_INDEPENDENT_SOURCE_REVIEW' and record['RSS_unknown_samples']==0 and record['source_after']==source
        previous[name+'3']=reference
    else:assert reference['sha256']==plan['failed_CHECK3']['receipt_sha256'] and record['verdict']=='STOP_RECONCILE_NO_RERUN' and record['RSS_unknown_samples']==1
assert fmt['receipt_refs']==[previous['FORMAT3']]
assert sum(p['wall_seconds'] for p in prefix)+2*120<=600 and sum(p['raw_bytes'] for p in prefix)+2*2097152<=10485760
shared={'maximum_calls':12,'calls_before':11,'calls_reserved':1,'calls_after':12,'no_rerun':True}
handoff=pathlib.Path('/tmp/qcl-docs-routing-source-CHECK4-Root-handoff-v9.json');ready=pathlib.Path('/tmp/qcl-docs-routing-source-CHECK4-Root-ready-v9.json')
exclusive(handoff,{'status':'SOURCE_HANDOFF','issuer':'Root','scope':SCOPE,'stage':STAGE,'root_head':HEAD,'isolated_base_head':BASE,'source_before':source,'config_sha256':plan['config_sha256'],'shared_source_budget':shared})
review_binding={'status':'PASS_SOURCE','wrapper_sha256':HASHES[str(ENTRY)],'guard_sha256':HASHES[str(H)],'plan_sha256':HASHES[str(P)],'report_ref':ref(REVIEW)}
exclusive(ready,{'status':'READY','issuer':'Root','scope':SCOPE,'stage':STAGE,'attempt':ATTEMPT,'created_unix':time.time(),'wrapper_sha256':HASHES[str(ENTRY)],'guard_sha256':HASHES[str(H)],'plan_sha256':HASHES[str(P)],'runtime_sha256':plan['runtime']['sha256'],'config_sha256':plan['config_sha256'],'isolated_base_head':BASE,'root_head':HEAD,'root_source_handoff_ref':ref(handoff),'shared_source_budget':shared,'source_before':source,'accepted_guard_review':review_binding,'accepted_pure_cpp_ref':PURE_CPP,'pure_only_slice':True,'format_binding':fmt,'previous_receipt_refs':previous,'explicit_environment_only_sampled_storage_acknowledged':True,'accepted_cpp':cpp})
j['operations'].append({'id':ATTEMPT,'state':'reserved_one_diagnostic_source_call_no_rerun','kind':'local_bounded_source_tool','stage':STAGE,'root_head':HEAD,'guard_review_sha256':HASHES[str(REVIEW)],'READY_ref':ref(ready),'source_before':source,'shared_counter_before':11,'shared_counter_after':12})
j['source_tool_active']=ATTEMPT;j['counters']['milestone_source_tools_calls']=12;j['resource_current']['source_tools_milestone_calls_used']=12;cpwrite(j)
start=time.monotonic();result=None;failure=None
try:result=subprocess.run([str(R/'.venv/bin/python'),'-I','-B',str(ENTRY),'--execute',str(ready)],cwd=R,capture_output=True,timeout=145)
except BaseException as exc:failure=repr(exc)
outer={'operation_id':ATTEMPT,'wrapper_returncode':None if result is None else result.returncode,'wall_seconds':time.monotonic()-start,'outer_failure':failure,'stdout':None if result is None else result.stdout.decode(errors='replace')[:16384],'stderr':None if result is None else result.stderr.decode(errors='replace')[:16384]}
outer_path=pathlib.Path('/tmp/qcl-docs-routing-source-CHECK4-Root-outer-v9.json');exclusive(outer_path,outer)
j=json.loads(CP.read_bytes());assert j['source_tool_active']==ATTEMPT and j['counters']['milestone_source_tools_calls']==12
op=next(o for o in j['operations'] if o['id']==ATTEMPT);op.update({'state':'completed_source_attempt_pending_independent_result_review' if result is not None else 'unknown_stop_no_rerun','outer_ref':ref(outer_path),'wrapper_returncode':outer['wrapper_returncode']})
receipt=folder/'receipt.json'
if receipt.exists():
    record=json.loads(read(receipt));op.update({'receipt_ref':ref(receipt),'guard_verdict':record.get('verdict'),'target_calls':record.get('target_calls'),'wall_seconds':record.get('wall_seconds'),'source_after':record.get('source_after'),'RSS_unknown_samples':record.get('RSS_unknown_samples'),'diagnostics':record.get('RSS_failure_diagnostics')})
else:op['receipt_ref']=None
j['source_tool_active']=None
if result is None or not receipt.exists():j['unknown_outcomes'].append({'id':ATTEMPT,'reason':failure or 'missingreceipt','resume':'readback retainedreceipt/process ownership; no duplicate rerun'})
cpwrite(j)
print(json.dumps({'operation_id':ATTEMPT,'wrapper_exit':outer['wrapper_returncode'],'source_calls':12,'product_calls':90,'receipt':str(receipt),'guard_verdict':op.get('guard_verdict'),'wall_seconds':op.get('wall_seconds'),'RSS_unknown':op.get('RSS_unknown_samples'),'diagnostics':op.get('diagnostics')}))
