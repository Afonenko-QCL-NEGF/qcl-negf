#!/usr/bin/env python3
"""Render a private, site-adaptable DAG without invoking a scheduler.

Requires sibling campaign.toml and the published grid-cluster inventory validator.
The caller must supply the referenced site-*.sub and final.sub before submission.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import tempfile
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
IDENTIFIER = re.compile(r'[A-Za-z][A-Za-z0-9_-]*\Z')


def inventory(path: Path, linux_only: bool) -> dict:
    source = HERE.parent / 'v843-grid-cluster' / 'dispatch.py'
    spec = importlib.util.spec_from_file_location('v843_grid_dispatch', source)
    if spec is None or spec.loader is None:
        raise ValueError(f'cannot load inventory validator: {source}')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(rows, list):
        raise ValueError('worker inventory must be a non-empty JSON list')
    domains = {}
    machines = set()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError('expected an object for each worker')
        domain, machine = row.get('filesystem_domain'), row.get('machine')
        if not isinstance(domain, str) or not re.fullmatch(r'[A-Za-z0-9_.-]+', domain):
            raise ValueError(f'invalid worker domain: {domain!r}')
        if machine is not None:
            if not isinstance(machine, str) or not re.fullmatch(r'[A-Za-z0-9_.-]+', machine):
                raise ValueError(f'invalid machine: {machine!r}')
            if machine.casefold() in machines:
                raise ValueError(f'duplicate machine: {machine}')
            machines.add(machine.casefold())
        domains.setdefault(domain.casefold(), []).append(row)
    for domain, group in domains.items():
        if len(group) > 1 and any(not row.get('machine') for row in group):
            raise ValueError(f'shared domain {domain!r} requires a unique machine for each row')
    if all(len(group) == 1 for group in domains.values()):
        return module.load_workers(path, linux_only)
    # Preserve the published validator and its OS/resource checks; surrogate names
    # only bypass its domain-uniqueness rule after the stricter checks above.
    surrogates = [dict(row, filesystem_domain=f'worker-{i:08d}') for i, row in enumerate(rows)]
    with tempfile.TemporaryDirectory() as temp:
        surrogate_path = Path(temp) / 'workers.json'
        surrogate_path.write_text(json.dumps(surrogates), encoding='utf-8')
        module.load_workers(surrogate_path, linux_only)
    return {os_name: [row for row in rows if row['os'] == os_name] for os_name in ('linux', 'windows')}


def levels(path: Path) -> list[list[dict]]:
    with path.open('rb') as file:
        data = tomllib.load(file)
    tasks = data.get('task')
    if not isinstance(tasks, list) or not tasks:
        raise ValueError('campaign.toml requires a nonempty [[task]] list')
    by_id = {}
    for task in tasks:
        name = task.get('id')
        if not isinstance(name, str) or not IDENTIFIER.fullmatch(name) or name.upper() == 'FINALIZE':
            raise ValueError(f'invalid or reserved task id: {name!r}')
        if name in by_id:
            raise ValueError(f'duplicate task id: {name}')
        parents = task.get('parents', [])
        if not isinstance(parents, list) or any(not isinstance(p, str) for p in parents) or len(set(parents)) != len(parents):
            raise ValueError(f'{name}: parents must be a list of distinct task IDs')
        memory = task.get('minimum_memory_mib', 1)
        if type(memory) is not int or memory < 1:
            raise ValueError(f'{name}: minimum_memory_mib must be a positive integer')
        if type(task.get('prefer_memory', False)) is not bool:
            raise ValueError(f'{name}: prefer_memory must be a boolean')
        by_id[name] = task
    for name, task in by_id.items():
        unknown = set(task.get('parents', [])) - by_id.keys()
        if unknown:
            raise ValueError(f'{name}: unknown parents: {sorted(unknown)}')
    remaining = dict(by_id)
    done = set()
    result = []
    while remaining:
        ready = [task for task in remaining.values() if set(task.get('parents', [])) <= done]
        if not ready:
            raise ValueError(f'cycle in task graph: {sorted(remaining)}')
        result.append(ready)
        done.update(task['id'] for task in ready)
        for task in ready:
            del remaining[task['id']]
    return result


def render(graph: list[list[dict]], workers: dict, out: Path) -> None:
    slots = workers['linux'] + workers['windows']
    # Index is the unique inventory entry, validated as one physical machine.
    counts = [0] * len(slots)
    categories = [f'machine_{i:04d}' for i in range(len(slots))]
    placements = []
    by_id = {}
    for frontier in graph:
        used = set()
        # Place the most constrained tasks first, preserving order for ties.
        ordered = sorted(frontier, key=lambda t: (not t.get('prefer_memory', False), -t.get('minimum_memory_mib', 1)))
        for task in ordered:
            eligible = [i for i, s in enumerate(slots) if s['memory_mib'] >= task.get('minimum_memory_mib', 1)]
            if not eligible:
                raise ValueError(f"{task['id']}: no worker meets minimum_memory_mib")
            available = [i for i in eligible if i not in used]
            if available:
                eligible = available
            # Normal tasks balance per-machine usage, which weights OS by machine count.
            # Memory-preferring tasks take the largest available grant, with fair ties.
            if task.get('prefer_memory', False):
                best = max(slots[i]['memory_mib'] for i in eligible)
                eligible = [i for i in eligible if slots[i]['memory_mib'] == best]
            index = min(eligible, key=lambda i: (counts[i], i))
            slot = slots[index]
            domain = slot['filesystem_domain']
            used.add(index)
            counts[index] += 1
            record = {'id': task['id'], 'parents': task.get('parents', []),
                      'os': slot['os'], 'filesystem_domain': domain,
                      'cpus': slot['cpus'], 'memory_mib': slot['memory_mib'],
                      'machine': slot.get('machine', ''), 'category': categories[index]}
            placements.append(record)
            by_id[task['id']] = record
    lines = ['# Site submit descriptions and final.sub are supplied by the executor.']
    for frontier in graph:
        for task in frontier:
            p = by_id[task['id']]
            name = p['id']
            lines.extend([f"JOB {name} site-{p['os']}.sub",
                          f'VARS {name} job="{name}" worker="{p["filesystem_domain"]}" cpus="{p["cpus"]}" memory="{p["memory_mib"]}" target_os="{p["os"].upper()}" machine="{p["machine"]}"',
                          f'CATEGORY {name} {p["category"]}'])
    for frontier in graph:
        for task in frontier:
            if task.get('parents'):
                lines.append(f"PARENT {' '.join(task['parents'])} CHILD {task['id']}")
    for category in categories:
        lines.append(f'MAXJOBS {category} 1')
    lines.append('FINAL FINALIZE final.sub')
    snippet = '''# Copy into each science site submit description before queue 1.
# Preserve the OS/domain guard when adding site requirements.
request_cpus = $(cpus)
request_memory = $(memory)MB
requirements = (TARGET.OpSys == "$(target_os)") && (TARGET.FileSystemDomain == "$(worker)") && (("$(machine)" == "") || (TARGET.Machine == "$(machine)"))
'''
    # No output is created until the entire graph and placement are valid.
    out.mkdir(mode=0o700, parents=False, exist_ok=False)
    (out / 'campaign.dag').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    (out / 'full-machine.sub.inc').write_text(snippet, encoding='utf-8')
    private = out / 'placements.json'
    private.write_text(json.dumps({'resource_policy': 'full-machine', 'tasks': placements}, indent=2) + '\n', encoding='utf-8')
    private.chmod(0o600)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers', type=Path, required=True, help='private inventory JSON')
    parser.add_argument('--out', type=Path, required=True, help='new private output directory')
    parser.add_argument('--linux-only', action='store_true')
    args = parser.parse_args()
    try:
        graph = levels(HERE / 'campaign.toml')
        workers = inventory(args.workers, args.linux_only)
        render(graph, workers, args.out)
    except (ValueError, OSError, tomllib.TOMLDecodeError) as error:
        parser.exit(2, f'error: {error}\n')
    print(f'Prepared {sum(map(len, graph))} tasks at {args.out}; executor files are still required.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
