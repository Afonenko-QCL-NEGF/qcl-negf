#!/usr/bin/env python3
"""Prepare a transferable V843 wave; no scheduler is contacted.

Prepare: python batch.py --work WORK --out BATCH --workers PRIVATE.json --commit HEAD
         --linux-python /path/python --windows-python C:/path/python.exe [--linux-only]
         [--wave ready|reserve-ready|all-ready]
Collect: python batch.py collect --out BATCH
Jobs have static machine assignments without work stealing; site submit files
need site review. CPU usage should be assessed from measured CPU and wall time,
not from the reserved CPU grant. A prepared
Julia 1.13.4 and Python 3.11+ are needed. Pkg.instantiate runs by default;
network and writable Julia depot are needed on a clean worker. Set
QCL_INSTANTIATE=0 only with a prepared depot. The FINAL
collector reports missing/technical results separately; completion is not a
scientific acceptance. Numerical decisions require inspecting the TOML.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, io, json, os, re, subprocess, sys, tarfile, tomllib, zipfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent

def digest(data): return hashlib.sha256(data).hexdigest()
def inventory(path, linux_only):
    spec = importlib.util.spec_from_file_location('placement', HERE.parent / 'v843-full-window-first-map/render.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module.inventory(path, linux_only)
def source_archive(commit):
    revision = subprocess.check_output(['git','-C',str(ROOT),'rev-parse','--verify',commit+'^{commit}'], text=True).strip()
    raw = subprocess.check_output(['git','-C',str(ROOT),'archive','--format=tar',revision]); files = {}
    prefixes = ('runner/', 'analysis/src/', 'studies/v843-spectrum/', 'studies/v843-overnight-front/', 'studies/fath-v843/controls/v843-input/dupont/')
    with tarfile.open(fileobj=io.BytesIO(raw)) as t:
        for m in t:
            if m.isdir(): continue
            if m.name.startswith(prefixes):
                if not m.isfile(): raise ValueError('non-file archive entry: '+m.name)
                files[m.name] = t.extractfile(m).read()
    for name in ('runner/Project.toml','runner/Manifest.toml','studies/fath-v843/controls/v843-input/dupont/device.toml', *(f'studies/v843-overnight-front/{x}' for x in ('worker.py','batch.py','events.py','queue.py','translation.jl','resolvent.jl','floquet.jl','impurity.jl'))):
        if name not in files: raise ValueError('commit lacks '+name)
    for name in ('worker.py','batch.py'):
        if files['studies/v843-overnight-front/'+name] != (HERE/name).read_bytes(): raise ValueError('committed '+name+' differs from checkout')
    if re.findall(rb'^path\s*=\s*"([^"]+)"', files['runner/Manifest.toml'], re.M) != [b'.']: raise ValueError('unexpected local Manifest path')
    files['source-catalog.json'] = (json.dumps({k:digest(v) for k,v in sorted(files.items())},indent=2)+'\n').encode()
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,'w',zipfile.ZIP_DEFLATED,allowZip64=True) as z:
        for k,v in sorted(files.items()): z.writestr(k,v)
    return revision,buf.getvalue(),files

def prepare(a):
    work=a.work.resolve(); out=a.out.resolve()
    for p in (work,out,Path(sys.executable).resolve()):
        if not re.fullmatch(r'[A-Za-z0-9_./-]+',str(p)): raise ValueError('use portable absolute paths without spaces: '+str(p))
    for p in (a.linux_python,a.windows_python):
        if not re.fullmatch(r'[A-Za-z0-9_./:-]+',p): raise ValueError('invalid worker Python path')
    workers=inventory(a.workers,a.linux_only); slots=workers['linux']+workers['windows']
    revision,source,files=source_archive(a.commit)
    namespace={'__name__': 'v843_pinned_queue'}
    exec(compile(files['studies/v843-overnight-front/queue.py'], 'pinned-queue.py', 'exec'), namespace)
    base, reserve = namespace['build']()
    data={'base':base, 'reserve':reserve}
    supplied=json.loads((work/'cases.json').read_text(encoding='utf-8'))
    if supplied != data: raise ValueError('cases.json differs from case definitions in pinned commit')
    waves = [('base', {'H','F','G','I'}, 65), ('reserve', {'RH','RG','RI'}, 16)]
    if a.wave == 'ready': waves = waves[:1]
    if a.wave == 'reserve-ready': waves = waves[1:]
    cases=[]; expected=0
    for key, families, count in waves:
        selected=[x for x in data[key] if x['family'] in families]
        if len(selected) != count: raise ValueError('invalid ' + key + ' count')
        expected += count
        # Interleave families before appending the next priority wave.
        # Order by numeric problem sizes rather than lexicographic ID strings.
        keys={'F':('Nperiod','Nz'), 'G':('B','rank','Nz','K','eta_meV'),
              'H':('B','rank','Nz'), 'I':('K','Nz'),
              'RG':('B','rank','Nz','K','eta_meV'), 'RH':('B','rank','Nz'), 'RI':('K','Nz')}
        groups={family:sorted((x for x in selected if x['family']==family),
                              key=lambda x: tuple(x['parameters'][k] for k in keys[family]))
                for family in sorted(families)}
        while any(groups.values()):
            for group in groups.values():
                if group: cases.append(group.pop(0))
    ids=[x['id'] for x in cases]
    if len(ids)!=expected or len(set(ids))!=expected or any(not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',i) for i in ids): raise ValueError('invalid wave case inventory')
    out.mkdir(parents=True,exist_ok=False,mode=0o700)
    for n in ('jobs','cases','returned','logs'): (out/n).mkdir()
    (out/'source.zip').write_bytes(source); (out/'worker.py').write_bytes(files['studies/v843-overnight-front/worker.py']); (out/'batch.py').write_bytes(files['studies/v843-overnight-front/batch.py']); (out/'events.py').write_bytes(files['studies/v843-overnight-front/events.py'])
    records=[]; lines=[]
    for i,case in enumerate(cases):
        machine_index=(i + i//len(slots)) % len(slots)
        slot=slots[machine_index]; name=case['id']; casebytes=(json.dumps(case,indent=2,ensure_ascii=False)+'\n').encode(); (out/'cases'/f'{name}.json').write_bytes(casebytes)
        job={'id':name,'family':case['family'],'source_commit':revision,'source_sha256':digest(source),'case_sha256':digest(casebytes),'target_os':slot['os'],'request_cpus':slot['cpus'],'request_memory_mib':slot['memory_mib']}
        records.append(job); (out/'jobs'/f'job-{name}.json').write_text(json.dumps(job,indent=2)+'\n')
        lines += [f'JOB {name} site-{slot["os"]}.sub', f'VARS {name} job="{name}" worker="{slot["filesystem_domain"]}" machine="{slot.get("machine", "")}" cpus="{slot["cpus"]}" memory="{slot["memory_mib"]}"',f'CATEGORY {name} machine_{machine_index:04d}', f'PRIORITY {name} {100 if case["family"] in ("H","F","G","I") else 0}']
    lines += [f'MAXJOBS machine_{i:04d} 1' for i in range(len(slots))]; lines.append('FINAL FINALIZE final.sub')
    (out/'campaign.dag').write_text('\n'.join(lines)+'\n')
    for osname,tag,python in (('linux','LINUX',a.linux_python),('windows','WINDOWS',a.windows_python)):
        if not workers[osname]: continue
        (out/f'site-{osname}.sub').write_text(f'''# Review site executable, Julia depot and resource grants before use.
universe = vanilla
executable = {python}
transfer_executable = FALSE
arguments = worker.py source.zip $(job).json job-$(job).json result-$(job).zip
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = worker.py, source.zip, cases/$(job).json, jobs/job-$(job).json
transfer_output_files = result-$(job).zip
transfer_output_remaps = "result-$(job).zip=returned/$(job).zip"
output = logs/$(job).out
error = logs/$(job).err
log = logs/$(job).log
request_cpus = $(cpus)
request_memory = $(memory)MB
request_disk = 4096MB
requirements = (TARGET.OpSys == "{tag}") && (TARGET.FileSystemDomain == "$(worker)") && (("$(machine)" == "") || (TARGET.Machine == "$(machine)"))
# environment = "QCL_JULIA=... QCL_INSTANTIATE=1 JULIA_DEPOT_PATH=..."
queue 1
''')
    (out/'final.sub').write_text(f'''universe = local
executable = {Path(sys.executable).resolve()}
arguments = {out}/batch.py collect --out {out}
output = logs/final.out
error = logs/final.err
log = logs/final.log
queue 1
''')
    (out/'manifest.json').write_text(json.dumps({'commit':revision,'wave':a.wave,'resource_policy':'whole machine','jobs':records},indent=2)+'\n')
    print(f'Prepared {len(records)} independent jobs at {out}; no scheduler contacted.')

def collect(out):
    out=out.resolve(); manifest=json.loads((out/'manifest.json').read_text()); counts={'completed':0,'technical':0,'missing':0}; receipts=[]
    for job in manifest['jobs']:
        name=job['id']; path=out/'returned'/f'{name}.zip'; state='technical'; detail=''
        if not path.exists(): state='missing'; detail='missing result (possibly held or not run)'
        else:
            try:
                with zipfile.ZipFile(path) as z:
                    names=z.namelist()
                    if len(names)!=len(set(names)) or any(x not in ('status.json','result.toml') for x in names): raise ValueError('unexpected archive entries')
                    status=json.loads(z.read('status.json'))
                    if status['job']!=job or status['case_sha256_observed']!=job['case_sha256']: raise ValueError('identity mismatch')
                    if not status['ok']: raise ValueError('worker failure: '+status.get('error','unknown'))
                    result=z.read('result.toml')
                    if digest(result)!=status['result_sha256']: raise ValueError('result checksum mismatch')
                    tomllib.loads(result.decode('utf-8'))
                    dest=out/'collected'/f'{name}.toml'; dest.parent.mkdir(exist_ok=True)
                    if dest.exists() and dest.read_bytes()!=result: raise ValueError('existing collected result differs')
                    if not dest.exists(): dest.write_bytes(result)
                    state='completed'; detail='measurement collected; scientific acceptance not assessed'
            except Exception as e: detail=str(e)
        counts[state]+=1; receipts.append({'id':name,'state':state,'detail':detail})
    report={'wave':manifest['wave'],'expected':len(manifest['jobs']),'counts':counts,'receipts':receipts}
    (out/'receipts.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(counts))
    event_script=out/'events.py'
    if not event_script.is_file():
        print('Optional events.py is missing; scientific events were not generated.', file=sys.stderr)
        event_status=0
    else:
        try:
            event_status = subprocess.run([sys.executable, str(event_script), '--batch', str(out)], check=False).returncode
        except OSError as error:
            print(f'Event generation failed: {error}', file=sys.stderr); event_status = 1
    return int(counts['technical']+counts['missing']>0 or event_status != 0)

def main():
    if len(sys.argv)>1 and sys.argv[1]=='collect':
        p=argparse.ArgumentParser(); p.add_argument('collect'); p.add_argument('--out',type=Path,required=True); return collect(p.parse_args().out)
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--work',type=Path,required=True); p.add_argument('--out',type=Path,required=True); p.add_argument('--workers',type=Path,required=True); p.add_argument('--commit',required=True); p.add_argument('--linux-python',required=True); p.add_argument('--windows-python',required=True); p.add_argument('--linux-only',action='store_true'); p.add_argument('--wave',choices=('ready','reserve-ready','all-ready'),default='ready')
    try: prepare(p.parse_args()); return 0
    except (ValueError,OSError,subprocess.CalledProcessError,KeyError) as e: p.exit(2,f'error: {e}\n')
if __name__=='__main__': sys.exit(main())
