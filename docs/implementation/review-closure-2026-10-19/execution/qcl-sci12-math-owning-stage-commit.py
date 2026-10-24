from pathlib import Path
import json,hashlib,subprocess,os,datetime
W=Path('/tmp/qcl-sci12-math-results-worktree');R=Path('/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf');CP=R/'docs/implementation/review-closure-2026-10-19/execution/checkpoint.json';J=Path('/tmp/qcl-sci12-math-publication-journal.json')
OP='OWNING-SCI12-MATH-PUBLISH-1';BASE='de70638a982f91b7e125ab1cfc70a2def2a656d'
BASE='de70638a982f91b7e125ab1cfc70a2daef2a656d'
files={'src/qcl_negf_results/_equilibrium_map_math.py':'0750ac7b1f74588278a4a6fd468ecf0a8ce739342383d717d719bc4126cfcdaa','tests/test_equilibrium_map_math.py':'995b364b93a56c403859f9ad074d55ef4abb5dddb70e2ad0982f689cb1b45a6d'}
sha=lambda b:hashlib.sha256(b).hexdigest()
def ref(p):
 p=Path(p);return {'path':str(p),'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
def git(*args):
 v=subprocess.run(['git','-C',str(W),*args],capture_output=True,timeout=30,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','GIT_NO_LAZY_FETCH':'1'})
 assert v.returncode==0, {'git':args,'exit':v.returncode,'stderr':v.stderr.decode(errors='replace')[:4096]}
 return v.stdout
j=json.loads(CP.read_text());assert j['counters']['targeted_test_total_calls']==90 and j['counters']['targeted_test_active'] is None and j['source_tool_active'] is None and not j['unknown_outcomes']
assert not J.exists() and not any(o.get('id')==OP for o in j['operations'])
assert git('rev-parse','HEAD').decode().strip()==BASE and git('branch','--show-current').decode().strip()=='codex/review-closure-equilibrium-map-math'
assert git('diff','--cached','--name-only')==b'' and git('diff','--name-only')==b''
for path,h in files.items():assert sha((W/path).read_bytes())==h
source_review=ref('/tmp/qcl-sci12-math-i1-review.md');outcome=ref('/tmp/qcl-sci12-math-GREEN1-outcome-review.md');assert source_review['sha256']=='9f785fbb16e804950be1ab24fb12da92f96f414a16ee73fe59711e1278073e07' and outcome['sha256']=='6737b7405ce987f885027b11d64caa87a857777492781bca14cf3582126979d3'
record={'id':OP,'state':'prepared_exact_two_file_commit','base':BASE,'base_branch':'codex/review-closure-current-bound-measurements-integration','branch':'codex/review-closure-equilibrium-map-math','repo':'Afonenko-QCL-NEGF/qcl-negf-results','files':files,'source_CPP':source_review,'GREEN_outcome':outcome,'observed_tests':97,'CI_dispatches':0,'scientific_submits':0,'no_auto_CI_workflows_at_base':True,'no_rerun':True,'created_at':datetime.datetime.now(datetime.timezone.utc).isoformat()}
def save():
 p=J.with_suffix('.json.tmp');p.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n');os.replace(p,J)
save();j['operations'].append({'id':OP,'state':'prepared_commit_no_duplicate','journal':ref(J),'base':BASE,'branch':record['branch'],'source_CPP':source_review,'GREEN_outcome':outcome})
j['SCI12_MATH_I1'].update({'state':'GREEN_highaccepted97PASS; owningcommit_publication_prepared','GREEN_outcome_review':outcome,'GREEN_outcome_identity':ref('/tmp/qcl-sci12-math-GREEN1-outcome-review-identity.json'),'product_source':ref(W/'src/qcl_negf_results/_equilibrium_map_math.py'),'source_CPP':source_review,'runtime_calls':2,'runtime_budget':'2of2EXHAUSTED; aggregate3.2474s63467B; no reruns; no native/scientificacceptance','owning_publication_operation':OP})
q=CP.with_suffix('.json.math-pub-tmp');q.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');os.replace(q,CP)
try:
 record['state']='before_exact_git_add';save();git('add','--',*files)
 assert set(git('diff','--cached','--name-only').decode().splitlines())==set(files)
 git('diff','--cached','--check')
 for path,h in files.items():assert sha(git('show',':'+path))==h
 tree=git('write-tree').decode().strip();record.update({'state':'before_sole_commit','index_tree':tree});save()
 output=git('commit','-m','Add bounded equilibrium comparison math primitives')
 commit=git('rev-parse','HEAD').decode().strip();assert git('rev-parse','HEAD^{tree}').decode().strip()==tree and git('status','--short')==b''
 record.update({'state':'committed_not_pushed','commit':commit,'tree':tree,'commit_output':output.decode()[:8192]});save()
except BaseException as e:
 record.update({'state':'commit_unknown_reconcile_no_retry','error':repr(e)});save();raise
j=json.loads(CP.read_text());op=next(o for o in j['operations'] if o['id']==OP);op.update({'state':record['state'],'commit':record['commit'],'journal':ref(J)});j['SCI12_MATH_I1'].update({'state':'owning_exact_two_files_committed_pending_push_PR_G1','owning_commit':record['commit'],'owning_tree':tree});j['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();q=CP.with_suffix('.json.math-pub-tmp');q.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');os.replace(q,CP)
print(json.dumps({'operation':OP,'state':record['state'],'commit':record['commit'],'tree':tree,'files':list(files),'tests':97,'root_gitlink_unchanged':True}))
