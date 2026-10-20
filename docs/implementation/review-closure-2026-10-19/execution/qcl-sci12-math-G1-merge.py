from pathlib import Path
import json,hashlib,subprocess,os,datetime
R=Path('/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf');CP=R/'docs/implementation/review-closure-2026-10-19/execution/checkpoint.json';J=Path('/tmp/qcl-sci12-math-G1-journal.json');PUB=Path('/tmp/qcl-sci12-math-publication-journal.json')
OP='G1-SCI12-MATH-RESULTS-c00bc60';REPO='Afonenko-QCL-NEGF/qcl-negf-results';SHA='c00bc60790a3d50bf2eac7e999ab45a60ace9047';BASE='de70638a982f91b7e125ab1cfc70a2daef2a656d';TREE='ea560717fe63b2a7010e533bafde55366d6cd271';TARGET='codex/review-closure-current-bound-measurements-integration';URL='https://github.com/'+REPO+'/pull/10'
sha=lambda b:hashlib.sha256(b).hexdigest()
def ref(p):
 p=Path(p);return {'path':str(p),'sha256':sha(p.read_bytes())}
x=json.loads(CP.read_text());assert x['counters']['targeted_test_active'] is None and x['source_tool_active'] is None and not x['unknown_outcomes'] and x['counters']['targeted_test_total_calls']==90
assert not J.exists() and not any(o.get('id')==OP for o in x['operations'])
assert ref('/tmp/qcl-sci12-math-c00-commit-binding-review.md')['sha256']=='27042f970a5ab61c5e713901ba3f7d938018ec3948e07083b2d310fe4e2f7cbe'
assert ref('/tmp/qcl-sci12-math-GREEN1-outcome-review.md')['sha256']=='6737b7405ce987f885027b11d64caa87a857777492781bca14cf3582126979d3'
j={'id':OP,'state':'prepared_conditional_merge','PR':URL,'reviewed_head':SHA,'reviewed_tree':TREE,'expected_base':BASE,'base_branch':TARGET,'CP_CODE':ref('/tmp/qcl-sci12-math-c00-commit-binding-review.md'),'GREEN':ref('/tmp/qcl-sci12-math-GREEN1-outcome-review.md'),'PR_attached':True,'sole_ready_and_merge':True,'no_admin_bypass':True,'root_gitlink_unchanged':True,'calls':{}}
def save():
 j['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();q=J.with_suffix('.json.tmp');q.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');os.replace(q,J)
def cpwrite(x):
 x['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();q=CP.with_suffix('.json.math-G1-tmp');q.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');os.replace(q,CP)
def run(key,args):
 assert key not in j['calls'];j['calls'][key]={'state':'before_call','argv':args};save()
 v=subprocess.run(args,cwd=R,capture_output=True,timeout=60,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'});assert len(v.stdout)+len(v.stderr)<=131072
 p=Path('/tmp/qcl-sci12-math-G1-'+key+'.json');assert not p.exists();p.write_text(json.dumps({'exit':v.returncode,'stdout':v.stdout.decode(errors='replace'),'stderr':v.stderr.decode(errors='replace')},ensure_ascii=False,indent=2)+'\n');j['calls'][key].update({'state':'returned','exit':v.returncode,'capture':ref(p)});save();assert v.returncode==0, {'phase':key,'exit':v.returncode,'capture':str(p)}
 return v.stdout.decode().strip()
save();x['operations'].append({'id':OP,'state':'prepared_conditional_merge_no_duplicate','PR':URL,'reviewed_head':SHA,'journal':ref(J),'CP_CODE':j['CP_CODE']});cpwrite(x)
try:
 fields='url,state,isDraft,headRefOid,headRefName,baseRefName,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup,files,body'
 pr=json.loads(run('preflight',['gh','pr','view','10','-R',REPO,'--json',fields]));assert pr['state']=='OPEN' and pr['headRefOid']==SHA and pr['baseRefName']==TARGET and pr['mergeable']=='MERGEABLE' and pr['mergeStateStatus']=='CLEAN' and pr['reviewDecision'] in ('','APPROVED') and pr['statusCheckRollup']==[]
 assert {v['path'] for v in pr['files']}=={'src/qcl_negf_results/_equilibrium_map_math.py','tests/test_equilibrium_map_math.py'}
 assert pr['body'].rstrip('\n')==Path('/tmp/qcl-sci12-math-owning-pr-body.md').read_text().rstrip('\n')
 base=json.loads(run('base',['gh','api','repos/'+REPO+'/branches/'+TARGET.replace('/','%2F')]));assert base['commit']['sha']==BASE and base['protected'] is False
 if pr['isDraft']:run('ready',['gh','pr','ready','10','-R',REPO])
 current=json.loads(run('before-merge',['gh','pr','view','10','-R',REPO,'--json','state,isDraft,headRefOid,mergeable,mergeStateStatus,statusCheckRollup']));assert current['state']=='OPEN' and current['isDraft'] is False and current['headRefOid']==SHA and current['mergeable']=='MERGEABLE' and current['mergeStateStatus']=='CLEAN' and current['statusCheckRollup']==[]
 j['state']='before_sole_merge_submit';save();run('merge',['gh','pr','merge','10','-R',REPO,'--merge','--match-head-commit',SHA])
 post=json.loads(run('after',['gh','pr','view','10','-R',REPO,'--json','state,headRefOid,baseRefName,mergeCommit,mergedAt,url']));assert post['state']=='MERGED' and post['headRefOid']==SHA and post['baseRefName']==TARGET
 commit=post['mergeCommit']['oid'];proof=json.loads(run('merge-tree',['gh','api','repos/'+REPO+'/git/commits/'+commit]));assert proof['tree']['sha']==TREE and {v['sha'] for v in proof['parents']}=={BASE,SHA}
 j.update({'state':'G1_merged_exact_tree_confirmed','merge_commit':commit,'merged_at':post['mergedAt'],'tree_proof':{'reviewed_source_tree':TREE,'merged_tree':proof['tree']['sha'],'parents':[v['sha'] for v in proof['parents']]}});save()
except BaseException as e:
 j.update({'state':'merge_unknown_or_blocked_reconcile_no_duplicate','error':repr(e)});save();x=json.loads(CP.read_text());o=next(o for o in x['operations'] if o['id']==OP);o.update({'state':j['state'],'journal':ref(J)});x['unknown_outcomes'].append({'id':OP,'reason':repr(e),'resume':'read currentPRstate+head+mergeTree; no repeat ready/merge until reconciled'});cpwrite(x);raise
pub=json.loads(PUB.read_text());pub.update({'state':'G1_merged_exact_tree_confirmed','PR_attached':True,'G1_operation':OP,'merge_commit':commit});q=PUB.with_suffix('.json.tmp');q.write_text(json.dumps(pub,ensure_ascii=False,indent=2)+'\n');os.replace(q,PUB)
x=json.loads(CP.read_text());o=next(o for o in x['operations'] if o['id']==OP);o.update({'state':j['state'],'merge_commit':commit,'journal':ref(J)});p=next(o for o in x['operations'] if o['id']==pub['id']);p.update({'state':'G1_merged_exact_tree_confirmed','PR_attached':True,'merge_commit':commit,'journal':ref(PUB)});x['SCI12_MATH_I1'].update({'state':'owning_PR10_G1_merged_exact_tree; Rootgitlink_pending_futurebatch','PR':URL,'G1_operation':OP,'G1_merge':commit,'source_head':SHA,'source_tree':TREE,'scientific_acceptance':'not_measured','PAIR_N0':'not_ready'});cpwrite(x)
print(json.dumps({'operation':OP,'state':j['state'],'PR':URL,'reviewed_source_head':SHA,'merge_commit':commit,'merged_tree':TREE,'root_gitlink_unchanged':True,'fullCI':0,'science':0}))
