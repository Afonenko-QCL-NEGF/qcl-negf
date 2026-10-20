from pathlib import Path
import json,subprocess,hashlib,os,datetime
R=Path('/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf');W=Path('/tmp/qcl-sci12-math-results-worktree');CP=R/'docs/implementation/review-closure-2026-10-19/execution/checkpoint.json';J=Path('/tmp/qcl-sci12-math-publication-journal.json');j=json.loads(J.read_text());assert j['state']=='committed_not_pushed'
SHA='c00bc60790a3d50bf2eac7e999ab45a60ace9047';BASE='de70638a982f91b7e125ab1cfc70a2daef2a656d';BRANCH=j['branch'];TARGET=j['base_branch'];REPO=j['repo'];URL='https://github.com/'+REPO+'.git'
hashb=lambda b:hashlib.sha256(b).hexdigest()
def ref(p):
 p=Path(p);return {'path':str(p),'sha256':hashb(p.read_bytes())}
def save():
 j['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();q=J.with_suffix('.json.tmp');q.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');os.replace(q,J)
def run(key,args):
 assert key not in j.setdefault('calls',{});j['calls'][key]={'state':'before_call','argv':args};save()
 v=subprocess.run(args,cwd=W,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','GIT_NO_LAZY_FETCH':'1'},capture_output=True,timeout=60)
 assert len(v.stdout)+len(v.stderr)<=131072
 log=Path('/tmp/qcl-sci12-math-publication-'+key+'.json');assert not log.exists();log.write_text(json.dumps({'exit':v.returncode,'stdout':v.stdout.decode(errors='replace'),'stderr':v.stderr.decode(errors='replace')},ensure_ascii=False,indent=2)+'\n')
 j['calls'][key].update({'state':'returned','exit':v.returncode,'capture':ref(log)});save();assert v.returncode==0, {'call':key,'exit':v.returncode,'log':str(log)}
 return v.stdout.decode().strip()
x=json.loads(CP.read_text());assert x['counters']['targeted_test_active'] is None and x['source_tool_active'] is None and not x['unknown_outcomes']
try:
 head=run('local-head',['git','rev-parse','HEAD']);assert head==SHA
 assert run('local-status',['git','status','--short'])==''
 before=run('remote-before',['git','ls-remote',URL,'refs/heads/'+BRANCH,'refs/heads/'+TARGET]);refs={row.split()[1]:row.split()[0] for row in before.splitlines()};assert refs.get('refs/heads/'+TARGET)==BASE and refs.get('refs/heads/'+BRANCH) in (None,SHA)
 j['state']='before_sole_push';save()
 if refs.get('refs/heads/'+BRANCH)!=SHA:run('push',['git','-c','credential.helper=!gh auth git-credential','push',URL,BRANCH])
 else:j['calls']['push']={'state':'already_confirmed_no_duplicate_submit','commit':SHA};save()
 after=run('remote-after',['git','ls-remote','--exit-code',URL,'refs/heads/'+BRANCH]);assert after.split()[0]==SHA
 j['state']='pushed_confirmed';save()
 existing=json.loads(run('pr-list',['gh','pr','list','-R',REPO,'--head',BRANCH,'--state','all','--json','number,url,state,baseRefName']))
 assert len(existing)<=1
 if existing:
  pr=existing[0];assert pr['baseRefName']==TARGET and pr['state']=='OPEN';url=pr['url'];j['PR_reused']=True
 else:
  j['state']='before_sole_PR_create';j['body']=ref('/tmp/qcl-sci12-math-owning-pr-body.md');save()
  url=run('pr-create',['gh','pr','create','-R',REPO,'--draft','--base',TARGET,'--head',BRANCH,'--title','Add bounded equilibrium comparison math primitives','--body-file','/tmp/qcl-sci12-math-owning-pr-body.md'])
 assert url.startswith('https://github.com/'+REPO+'/pull/')
 j.update({'state':'PR_created_or_reconciled_needs_attachment','PR':url});save()
except BaseException as e:
 j.update({'state':'publication_unknown_or_blocked_reconcile_no_duplicate','error':repr(e)});save();raise
x=json.loads(CP.read_text());op=next(o for o in x['operations'] if o['id']==j['id']);op.update({'state':j['state'],'PR':url,'commit':SHA,'journal':ref(J)});x['SCI12_MATH_I1'].update({'state':'owning_draft_PR_created_pending_attach_and_G1_checks','PR':url,'owning_commit':SHA});x['updated_at']=datetime.datetime.now(datetime.timezone.utc).isoformat();q=CP.with_suffix('.json.math-pr-tmp');q.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');os.replace(q,CP)
print(json.dumps({'operation':j['id'],'state':j['state'],'PR':url,'commit':SHA,'body':j.get('body'),'root_gitlink_unchanged':True}))
