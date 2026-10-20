import pathlib,json,hashlib,os,subprocess,time,datetime
R=pathlib.Path('/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf');W=pathlib.Path('/tmp/qcl-sci12-math-results-worktree');CP=R/'docs/implementation/review-closure-2026-10-19/execution/checkpoint.json'
HEAD='107bac5697b37cf0e47c3feb44883a907837645c';BASE='de70638a982f91b7e125ab1cfc70a2daef2a656d';SCOPE='SCI12-MATH-local-v2';ATTEMPT='SCI12-MATH-RED-1'
H=pathlib.Path('/tmp/qcl-sci12-math-local-guard-v2.py');P=pathlib.Path('/tmp/qcl-sci12-math-local-plan-v2.json');REVIEW=pathlib.Path('/tmp/qcl-sci12-math-local-guard-v2-review.md');REVIEW_SHA='2227d19cce9c1169bf637234b15d583453f28cadae7e2682d89b6474365b1fa0'
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(p,cap=262144):
 p=pathlib.Path(p);assert p.resolve(strict=True)==p and p.is_file() and p.stat().st_uid==os.getuid() and p.stat().st_size<=cap
 b=p.read_bytes();assert len(b)<=cap;return b
def ref(p):return {'path':str(p),'sha256':sha(read(p))}
def exclusive(p,j):
 with p.open('x') as f:json.dump(j,f,ensure_ascii=False,indent=2);f.write('\n')
def cpwrite(j):
 j['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();q=CP.with_suffix('.json.math-red-tmp');q.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');os.replace(q,CP)
def git(p,*args):return subprocess.check_output(['git','-C',str(p),*args],env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','GIT_NO_LAZY_FETCH':'1'},text=True,timeout=10).strip()
assert sha(read(H))=='d5b46ac8eaf1a9b9456b47d90bf5e04ec42ff6859363cf53847c6c1884ef858a'
assert sha(read(P))=='968c537b5b3bacf23f288d28254b50670930d27d8ae7e7afeceaba7ba463bf77'
assert REVIEW_SHA!='PENDING' and sha(read(REVIEW))==REVIEW_SHA
assert git(R,'rev-parse','HEAD')==HEAD and git(W,'rev-parse','HEAD')==BASE and git(W,'branch','--show-current')=='codex/review-closure-equilibrium-map-math'
assert not git(W,'diff','--name-only') and git(W,'status','--short')=='?? tests/test_equilibrium_map_math.py'
for line in git(R,'ls-tree','HEAD','components/').splitlines():
 mode,kind,oid,path=line.split(None,3);assert mode=='160000' and kind=='commit' and git(R/path,'rev-parse','HEAD')==oid and not git(R/path,'status','--short')
for line in git(R,'status','--short').splitlines():assert 'docs/implementation/review-closure-2026-10-19/execution/' in line
j=json.loads(CP.read_text());assert j['counters']['targeted_test_total_calls']==88 and j['counters']['milestone_source_tools_calls']==8
assert j['counters']['targeted_test_active'] is None and j['source_tool_active'] is None and not j['unknown_outcomes']
assert j['resource_current']['engineering_milestone_product_call_cap']==90
assert not any(o.get('id')==ATTEMPT for o in j['operations']) and not pathlib.Path('/tmp/qcl-'+ATTEMPT).exists()
rootplan=json.loads(read('/tmp/qcl-sci12-math-engineering-plan-Root-v1.json'));assert rootplan['shared_limits']['global_ceiling']==90 and rootplan['shared_limits']['maximum_new_calls']==2
predpath=pathlib.Path('/tmp/qcl-DOCS-ROUTING-GREEN-1/receipt.json');assert sha(read(predpath))=='ea7d990e99e87834148d10b8c7ec7c3e0ac0c701c152de967b6bbacb45d66cf3'
assert j['routing_source_v7']['observed_tests']==230 and j['routing_source_v7']['failed']==9
f2=pathlib.Path('/tmp/qcl-sci12-math-fixture-v2-review.md');assert sha(read(f2))=='c855f328402a217225b13fda3821000a8a6e55ed6894235e42b57802f3e69ec9'
manifest=json.loads(read('/tmp/qcl-sci12-math-preRED-source-manifest-v1.json'));source={p:sha(read(p)) for p in manifest['files']}
assert source=={p:v['sha256'] for p,v in manifest['files'].items()}
product=W/'src/qcl_negf_results/_equilibrium_map_math.py';assert not product.exists() and not product.is_symlink()
budget={'calls_before':88,'calls_reserved':1,'calls_after':89,'global_ceiling':90,'source_C08':'8/8 unchanged','no_rerun':True}
base={'status':'ROOT_VALIDATED_FOR_SINGLE_CALL','issuer':'Root','scope':SCOPE,'attempt':ATTEMPT,'harness_sha256':ref(H)['sha256'],'plan_sha256':ref(P)['sha256'],'root_head':HEAD,'candidate_base_head':BASE,'source_files':source,'product_sha256':None,'budget':budget,'accepted_guard_review':ref(REVIEW),'accepted_source_review':ref(f2),'predecessor_ref':ref(predpath),'meaningful_reviews_predecessor_counter_and_aggregate_budget_validated':True}
validation=pathlib.Path('/tmp/qcl-sci12-math-RED-Root-validation-v2.json');exclusive(validation,base)
ready={k:v for k,v in base.items() if k not in ('meaningful_reviews_predecessor_counter_and_aggregate_budget_validated',)}
ready.update({'status':'READY','created_unix':time.time(),'runtime_sha256':json.loads(read(P))['runtime_sha256'],'root_validation_ref':ref(validation),'sampled_guards_acknowledged':True})
ready_path=pathlib.Path('/tmp/qcl-sci12-math-RED-Root-ready-v2.json');exclusive(ready_path,ready)
j['operations'].append({'id':ATTEMPT,'state':'reserved_no_rerun','kind':'new_private_math_API_structural_RED_only','root_head':HEAD,'READY_ref':ref(ready_path),'shared_counter_before':88,'shared_counter_after':89,'source_before':source})
j['counters']['targeted_test_active']=ATTEMPT
for k in ['targeted_test_total_calls','targeted_test_calls_total']:j['counters'][k]=89
j['counters']['targeted_tests_by_task']['SCI12_MATH']=1;j['counters']['SCI12_MATH_calls']=1;j['resource_current']['targeted_test_active']=ATTEMPT;cpwrite(j)
start=time.monotonic();result=None;failure=None
try:result=subprocess.run([str(R/'.venv/bin/python'),'-I','-B',str(H),'--execute',str(ready_path)],cwd=R,capture_output=True,timeout=115)
except BaseException as e:failure=repr(e)
outer={'operation_id':ATTEMPT,'wrapper_returncode':None if result is None else result.returncode,'wall_seconds':time.monotonic()-start,'outer_failure':failure,'stdout':None if result is None else result.stdout.decode(errors='replace')[:16384],'stderr':None if result is None else result.stderr.decode(errors='replace')[:16384]}
opfile=pathlib.Path('/tmp/qcl-sci12-math-RED-Root-outer-v2.json');exclusive(opfile,outer)
j=json.loads(CP.read_text());assert j['counters']['targeted_test_active']==ATTEMPT and j['counters']['targeted_test_total_calls']==89
op=next(x for x in j['operations'] if x['id']==ATTEMPT);op.update({'state':'completed_pending_independent_RED_outcome_review' if result is not None else 'unknown_stop_no_rerun','outer_ref':ref(opfile),'wrapper_returncode':outer['wrapper_returncode']})
receipt=pathlib.Path('/tmp/qcl-'+ATTEMPT+'/receipt.json')
if receipt.exists():
 rec=json.loads(read(receipt));wall=round(rec['wall_seconds'],3);op.update({'receipt_ref':ref(receipt),'guard_verdict':rec.get('verdict'),'wall_seconds':wall,'target_calls':rec.get('target_calls'),'observed_tests':None})
 census_path=pathlib.Path('/tmp/qcl-targeted-receipt-census.json');census=json.loads(census_path.read_text());assert len(census)==88 and not any(x['id']=='qcl-'+ATTEMPT for x in census)
 census.append({'id':'qcl-'+ATTEMPT,'wall_seconds':wall,'raw_wall_seconds':rec['wall_seconds'],'exit_code':rec.get('exit_code'),'receipt_sha256':ref(receipt)['sha256'],'kind':'97nominal_newAPI_missing_structural_RED_not_physics_pending_raw_review','guard_verdict':rec.get('verdict')});census_path.write_text(json.dumps(census,indent=2)+'\n');total=round(sum(x['wall_seconds'] for x in census),3)
 for k in ['targeted_test_total_wall_seconds','targeted_test_wall_seconds_total']:j['counters'][k]=total
 j['resource_current'].update({'targeted_completed_calls':89,'targeted_wall_seconds':total});j['resource_census'].update({'targeted_receipts':89,'targeted_wall_seconds':total});j['targeted_receipt_census'].update({'count':89,'wall_seconds':total,'source_sha256':sha(census_path.read_bytes())})
else:op['receipt_ref']=None
j['counters']['targeted_test_active']=None;j['resource_current']['targeted_test_active']=None
if result is None or not receipt.exists():j['unknown_outcomes'].append({'id':ATTEMPT,'reason':failure or 'missing receipt','resume':'readback process/receipt ownership before further actions; no duplicate rerun'})
j['SCI12_MATH_I1'].update({'state':'RED_attempt_consumed_pending_independent_fullraw_review_no_implementation_yet','RED_receipt':None if not receipt.exists() else ref(receipt),'runtime_calls':1})
cpwrite(j);print(json.dumps({'operation':ATTEMPT,'wrapper_exit':outer['wrapper_returncode'],'guard_verdict':op.get('guard_verdict'),'product_calls':89,'wall_seconds':op.get('wall_seconds'),'receipt':str(receipt),'observed_tests':None}))
