#!/usr/bin/env python3
"""Index collected V843 measurements; diagnostic events are not admission decisions."""
from __future__ import annotations
import argparse, hashlib, json, math, tomllib, zipfile, tempfile
from pathlib import Path

POLICY = {
 'version':'v843-events/1',
 'scope':'Measurements must pass completeness, finite values and input-identity checks before classification. Diagnostics of collected member files only. No inference of stationary transport, no physical-model validation and no MAP admission.',
 'rules':{
  'I/RI':'For each reported part/probe and angle N=64,128,256,512,1024, use the recorded aggregate and worst-pair relative error against 4096. If the recorded 2048/4096 control is unstable (>0.1% in either metric), unresolved. Otherwise detected means max error >1%; not_detected means both errors <=1%. The limits are those in impurity.jl, not a bound on transport.',
  'G/RG':'Fixed Gaussian only: for each k compute D=trapz(|Agal-Acoord|)/trapz(Acoord), on fine and nested coarse (every other point). If Dfine-2*|Dfine-Dcoarse| > 0.01 detected; if Dfine+2*|Dfine-Dcoarse| <= 0.01 not_detected; otherwise unresolved. Any detected => detected; all not_detected => not_detected; else unresolved. Invalid or nonpositive data unresolved and separately flagged. Working 1% criterion, not a continuum error bound or gate.',
  'H/RH/T':'Max paired_H_relative_residual >1e-10 and >2*max translation_covariance_relative_residual => detected; paired <=1e-10 and covariance <=1e-10 => not_detected; else unresolved. Finite-window diagnostic, not private HOP.',
  'F':'Maximum absolute sorted spectrum difference across both twists divided by max(1 eV, max |E|) >1e-10 => detected, otherwise not_detected. Same-discrete zero-field consistency only.',
  'C':'No validated event rule/schema in this tool; unresolved.',
 },
 'caveat':'not_detected for I/RI means within the specified 1% diagnostic resolution only; empirical reference stability is not a rigorous uncertainty bound.'}

def sha(b): return hashlib.sha256(b).hexdigest()
def finite(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def source(path, root):
 b=path.read_bytes(); return {'path':path.relative_to(root).as_posix(),'sha256':sha(b)},b

def validate(family, params, d):
 def need(ok, why):
  if not ok: raise ValueError('invalid or incomplete result: '+why)
 def allfinite(x):
  if isinstance(x,float): return math.isfinite(x)
  if isinstance(x,list): return all(allfinite(y) for y in x)
  if isinstance(x,dict): return all(allfinite(y) for y in x.values())
  return True
 need(allfinite(d), 'nonfinite TOML value')
 if family in ('H','RH','T'):
  rank=params['rank']; need(d.get('periods')==params['B'] and d.get('rank')==rank and d.get('nodes_per_period')==params['Nz'],'H geometry')
  ks=d.get('k_nm_inverse',[]); need(len(ks)==17 and all(finite(x) and x>=0 for x in ks) and all(ks[i]<ks[i+1] for i in range(16)),'H k grid')
  pairs=d.get('pairs',{}); need(set(pairs)=={'minus','plus'},'H both sides')
  for side,direction in (('minus',-1),('plus',1)):
   x=pairs[side]; rows=x.get('k_results',[])
   need(x.get('direction_periods')==direction and len(rows)==17,'H side or rows')
   need(all(len(x.get(k,[]))==rank for k in ('retained_gram_eigenvalues','lost_probability_per_column','principal_singular_values')),'H rank vectors')
   need(all(len(r.get('translated_energies_eV',[]))==rank and len(r.get('neighbor_energies_eV',[]))==rank and len(r.get('central_energies_eV',[]))==rank and r.get('k_nm_inverse')==ks[i] and finite(r.get('paired_H_relative_residual')) and finite(r.get('translation_covariance_relative_residual')) for i,r in enumerate(rows)),'H rank or k rows')
 elif family in ('G','RG'):
  rank=params['rank']; nk=params['K']; ne=481 if family=='G' else 961
  need(d.get('window_periods')==params['B'] and d.get('rank_per_period')==rank and d.get('nodes_per_period')==params['Nz'] and math.isclose(d.get('eta_meV',-1),params['eta_meV'],rel_tol=1e-12,abs_tol=1e-12),'G geometry or eta')
  es=d.get('energy_eV',[]); rows=d.get('cases',[]); need(len(es)==ne and len(rows)==nk,'G energy or k length')
  ks=[r.get('k_nm_inverse') for r in rows]; need(all(finite(k) and k>=0 for k in ks) and all(ks[i]<ks[i+1] for i in range(nk-1)),'G k grid')
  need(all(finite(x) for x in es) and all(es[i]<es[i+1] for i in range(ne-1)),'G energy grid')
  for r in rows:
   probes=r.get('probes',[]); need(len(probes)==rank+1 and sum(p.get('kind')=='fixed_gaussian' for p in probes)==1,'G probe count')
   need(all(len(p.get('coordinate_per_eV',[]))==ne and len(p.get('galerkin_per_eV',[]))==ne for p in probes),'G spectrum length')
 elif family=='F':
  n=params['Nperiod']; nz=params['Nz']; need(d.get('n_periods')==n and d.get('nodes_per_period')==nz,'F geometry')
  phases=d.get('boundary_phase_results',{}); need(set(phases)=={'periodic','antiperiodic'},'F both phases')
  for key,phase in (('periodic',0.0),('antiperiodic',math.pi)):
   x=phases[key]; need(math.isclose(x.get('phase_radians',-1),phase,abs_tol=1e-12) and x.get('count')==n*nz and len(x.get('ring_spectrum_eV',[]))==n*nz and len(x.get('primitive_union_spectrum_eV',[]))==n*nz,'F phase or spectrum length')
 elif family in ('I','RI'):
  nk=params['K']; need(d.get('nz')==params['Nz'] and d.get('nk')==nk and d.get('mode')==('BASE' if family=='I' else 'FORWARD'),'I geometry or mode')
  ks=d.get('radial_nodes',[]); ws=d.get('radial_weights',[]); need(len(ks)==nk and len(ws)==nk and all(finite(x) and x>=0 for x in ks) and all(finite(x) and x>0 for x in ws) and all(ks[i]<ks[i+1] for i in range(nk-1)),'I radial grid')
  results=d.get('results',{}); need(set(results)=={a+'_'+b for a in ('full','forward','rest') for b in ('diagonal','coherent')},'I six sector/probe combinations')
  for x in results.values():
   need(type(x.get('reference_2048_vs_4096_stable_0_1_percent')) is bool,'I reference state')
   comp=x.get('comparisons',{}); need(all(str(n) in comp for n in (64,128,256,512,1024,2048)),'I angular comparisons')
   for n in (64,128,256,512,1024,2048):
    z=comp[str(n)]; need(finite(z.get('weighted_relative_frobenius_error')) and finite(z.get('worst_pair_error_over_full_reference')) and len(z.get('worst_pair_1based',[]))==2,'I angular measurement')

def event(id, family, status, observation, index, reason):
 return {'case_id':id,'family':family,'status':status,'observation':observation,'index':index,'reason':reason}

def measure(id, family, data):
 out=[]
 if family in ('I','RI') and data.get('schema')=='v843-impurity-angle-coordinate-diagnostic/1':
  for key, r in sorted(data.get('results',{}).items()):
   comparisons=r.get('comparisons',{}); ref=comparisons.get('2048',{})
   a,b=ref.get('weighted_relative_frobenius_error'),ref.get('worst_pair_error_over_full_reference')
   stable=finite(a) and finite(b) and max(a,b)<=0.001 and r.get('reference_2048_vs_4096_stable_0_1_percent') is True
   for n in (64,128,256,512,1024):
    e=comparisons.get(str(n),{}); x,y=e.get('weighted_relative_frobenius_error'),e.get('worst_pair_error_over_full_reference')
    valid=finite(x) and finite(y) and min(x,y)>=0
    state='unresolved' if not stable or not valid else ('detected' if max(x,y)>0.01 else 'not_detected')
    out.append(event(id,family,state,{'weighted_relative_error':x,'worst_pair_relative_error':y,'reference_weighted_error':a,'reference_worst_pair_error':b,'reference_limit':0.001,'comparison_limit':0.01},{'part_probe':key,'angles':n,'worst_pair_1based':e.get('worst_pair_1based')},'Angular error versus 4096; empirical 2048/4096 control must meet 0.1%.'))
 elif family in ('G','RG') and data.get('schema')=='v843-finite-window-resolvent-v1':
  energy=data.get('energy_eV',[]); rows=[]; issues=[]
  def integral(xs,ys): return sum((xs[i+1]-xs[i])*(ys[i+1]+ys[i])*0.5 for i in range(len(xs)-1))
  for i,v in enumerate(data.get('cases',[])):
   probes=[p for p in v.get('probes',[]) if p.get('kind')=='fixed_gaussian']
   try:
    if len(probes)!=1: raise ValueError('exactly one fixed_gaussian required')
    a=probes[0]['coordinate_per_eV']; b=probes[0]['galerkin_per_eV']
    if len(energy)<3 or len(energy)%2!=1 or len(a)!=len(energy) or len(b)!=len(energy): raise ValueError('invalid nested energy grid or array length')
    if any(not finite(x) for x in energy+a+b) or any(energy[j+1]<=energy[j] for j in range(len(energy)-1)) or any(x<0 for x in a+b): raise ValueError('nonfinite, negative spectrum or nonmonotonic energy')
    def diff(xs,aa,bb):
     den=integral(xs,aa)
     if den<=0: raise ValueError('nonpositive coordinate spectral integral')
     return integral(xs,[abs(x-y) for x,y in zip(aa,bb)])/den
    fine=diff(energy,a,b); coarse=diff(energy[::2],a[::2],b[::2]); delta=abs(fine-coarse)
    state='detected' if fine-2*delta>0.01 else ('not_detected' if fine+2*delta<=0.01 else 'unresolved')
    rows.append({'k_index_zero_based':i,'k_nm_inverse':v.get('k_nm_inverse'),'Dfine':fine,'Dcoarse':coarse,'resolution_proxy':delta,'status':state})
   except (ValueError,KeyError,TypeError) as exc: issues.append({'k_index_zero_based':i,'reason':str(exc)})
  state='detected' if any(x['status']=='detected' for x in rows) else ('not_detected' if rows and not issues and all(x['status']=='not_detected' for x in rows) else 'unresolved')
  out.append(event(id,family,state,{'per_k':rows,'invalid_data':issues,'working_limit':0.01},{'probe_kind':'fixed_gaussian'},'Nested-grid empirical comparison, not a continuum bound or admission decision.'))
 elif family in ('H','RH','T') and data.get('schema')=='v843-full-window-translation-v1':
  rows=[(v.get('paired_H_relative_residual'),v.get('translation_covariance_relative_residual'),side,i,v.get('k_nm_inverse')) for side,p in data.get('pairs',{}).items() for i,v in enumerate(p.get('k_results',[]))]
  if rows and all(finite(x[0]) and finite(x[1]) and min(x[0],x[1])>=0 for x in rows):
   worst=max(rows,key=lambda x:x[0]); cov=max(rows,key=lambda x:x[1]); a,b=worst[0],cov[1]
   state='detected' if a>1e-10 and a>2*b else ('not_detected' if a<=1e-10 and b<=1e-10 else 'unresolved')
   out.append(event(id,family,state,{'maximum_paired_relative':a,'maximum_covariance_relative':b,'limit':1e-10},{'worst_pair_side':worst[2],'worst_pair_k_index_zero_based':worst[3],'worst_pair_k_nm_inverse':worst[4],'worst_covariance_side':cov[2],'worst_covariance_k_index_zero_based':cov[3],'worst_covariance_k_nm_inverse':cov[4]},'Finite-window neighboring blocks; not private HOP.'))
 elif family=='F' and data.get('schema')=='v843-independent-bdd-floquet/1':
  rows=[]
  for side in ('periodic','antiperiodic'):
   v=data.get('boundary_phase_results',{}).get(side,{})
   a=v.get('ring_spectrum_eV',[]); b=v.get('primitive_union_spectrum_eV',[])
   if not a or len(a)!=len(b) or any(not finite(x) for x in a+b): break
   aa=sorted(a); bb=sorted(b); d=max(abs(x-y) for x,y in zip(aa,bb)); rows.append((d, max(abs(x) for x in aa+bb),side))
  if len(rows)==2:
   worst=max(rows,key=lambda x:x[0]); scale=max(1.0,*(x[1] for x in rows)); rel=worst[0]/scale
   out.append(event(id,family,'detected' if rel>1e-10 else 'not_detected',{'max_spectrum_difference_eV':worst[0],'normalizer_eV':scale,'relative_difference':rel,'limit':1e-10},{'boundary_phase':worst[2]},'Same-discrete zero-field consistency only.'))
 if not out: out.append(event(id,family,'unresolved',{}, {},'Missing, unrecognized or incomplete measurement schema; no scientific decision.'))
 return out

def comparisons(records):
 """Compare adjacent planned values while holding every other case parameter fixed."""
 pairs=[]; skipped=[]
 definitions={'H':('B','rank'), 'RH':('B','rank'), 'T':('B','rank'),
              'G':('B','rank','eta_meV'), 'RG':('B','rank','eta_meV'),
              'I':('K','Nz'), 'RI':('K','Nz')}
 for family,axes in definitions.items():
  subset=[r for r in records if r['family']==family and r.get('parameters')]
  for axis in axes:
   groups={}
   for r in subset:
    p=r['parameters']; key=json.dumps({k:v for k,v in p.items() if k!=axis},sort_keys=True)
    groups.setdefault(key,[]).append(r)
   for key,group in sorted(groups.items()):
    group.sort(key=lambda x:x['parameters'][axis])
    for a,b in zip(group,group[1:]):
     if a['parameters'][axis]==b['parameters'][axis]: continue
     item={'family':family,'axis':axis,'fixed_parameters':json.loads(key),'case_ids':[a['id'],b['id']], 'axis_values':[a['parameters'][axis],b['parameters'][axis]],'states':[a['status'],b['status']]}
     if not a.get('metrics') or not b.get('metrics'):
      item['reason']='missing, incomplete or incompatible result'; skipped.append(item); continue
     ma,mb=a['metrics'],b['metrics']; metrics={}
     for name in sorted(set(ma)&set(mb)):
      x,y=ma[name],mb[name]
      if finite(x) and finite(y): metrics[name]={'first':x,'second':y,'difference':y-x,'ratio_second_over_first':y/x if x!=0 else None}
     if not metrics:
      item['reason']='no matching valid metric/index'; skipped.append(item); continue
     item['metrics']=metrics; pairs.append(item)
 return {'scope':'Adjacent planned one-parameter comparisons only; no causal interpretation, extrapolation, or MAP admission. Null ratio means zero denominator.', 'pairs':pairs,'skipped':skipped}

def comparison_metrics(family, data, ev):
 if family in ('H','RH','T'):
  o=ev[0]['observation']; return {'paired_max':o['maximum_paired_relative'],'covariance_max':o['maximum_covariance_relative']}
 if family in ('G','RG'):
  return {f"k={x['k_nm_inverse']}/{key}":x[key] for x in ev[0]['observation'].get('per_k',[]) for key in ('Dfine','Dcoarse','resolution_proxy')}
 if family in ('I','RI'):
  return {f"{x['index']['part_probe']}/128/{key}":x['observation'][key] for x in ev if x['index'].get('angles')==128 for key in ('weighted_relative_error','worst_pair_relative_error') if finite(x['observation'].get(key))}
 return {}

def main():
 p=argparse.ArgumentParser(description=__doc__); p.add_argument('--batch',required=True,type=Path); args=p.parse_args()
 root=args.batch.resolve(); parent=root/'scientific-events'; parent.mkdir(exist_ok=True)
 report=Path(tempfile.mkdtemp(prefix='snapshot-', dir=parent))
 # Policy is persisted before result files are read.
 (report/'policy.json').write_text(json.dumps(POLICY,indent=2,ensure_ascii=False)+'\n')
 manifest=json.loads((root/'manifest.json').read_text()); receipts=json.loads((root/'receipts.json').read_text())
 receipt={r['id']:r for r in receipts['receipts']}; events=[]; index=[]; records=[]
 for job in manifest['jobs']:
  ident=job['id']; fam=job['family']; row={'id':ident,'family':fam,'receipt':receipt.get(ident,{}).get('state','missing')}
  case=root/'cases'/f'{ident}.json'; result=root/'collected'/f'{ident}.toml'
  try:
   row['case'],raw=source(case,root)
   if sha(raw)!=job['case_sha256']: raise ValueError('case hash mismatch')
   c=json.loads(raw); row['parameters']=c.get('parameters',{})
   if c['id']!=ident or c['family']!=fam: raise ValueError('case identity mismatch')
   if row['receipt']!='completed': raise ValueError('collection not completed')
   row['result'],raw=source(result,root); data=tomllib.loads(raw.decode('utf-8'))
   archive=root/'returned'/f'{ident}.zip'
   # Bind the extracted result to the collector-verified member and current receipt.
   row['archive'],_=source(archive,root)
   with zipfile.ZipFile(archive) as z:
    status=json.loads(z.read('status.json')); member=z.read('result.toml')
   if status.get('job')!=job or not status.get('ok') or sha(member)!=sha(raw) or status.get('result_sha256')!=sha(raw): raise ValueError('result archive identity/hash mismatch')
   validate(fam,c['parameters'],data)
   member_events=measure(ident,fam,data); events.extend(member_events); row['schema']=data.get('schema')
   row['comparison_metrics']=comparison_metrics(fam,data,member_events)
   row['scientific_status']='detected' if any(x['status']=='detected' for x in member_events) else ('not_detected' if member_events and all(x['status']=='not_detected' for x in member_events) else 'unresolved')
  except (OSError,ValueError,KeyError,TypeError,zipfile.BadZipFile,tomllib.TOMLDecodeError) as exc:
   row['error']=str(exc); events.append(event(ident,fam,'unresolved',{}, {},str(exc)))
  index.append(row)
  records.append({'id':ident,'family':fam,'parameters':row.get('parameters'),'status':row.get('scientific_status',row['receipt']),'metrics':row.get('comparison_metrics',{})})
 (report/'comparisons.json').write_text(json.dumps(comparisons(records),indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 payload={'policy':'policy.json','events':events,'sources':index,'manifest':source(root/'manifest.json',root)[0],'receipts':source(root/'receipts.json',root)[0]}
 (report/'events.json').write_text(json.dumps(payload,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
 counts={s:sum(e['status']==s for e in events) for s in ('detected','not_detected','unresolved')}
 print(json.dumps({'output':str(report),'counts':counts}))
if __name__=='__main__': main()
