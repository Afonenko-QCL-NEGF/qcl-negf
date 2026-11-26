#!/usr/bin/env python3
"""Collect V843 native diagnostics in the persistent run directory.

Run: python3 /path/to/collect_v843.py
Input: ./cluster.dag VARS D... field="..." rings="..." angles="..." and
./results/<node>.toml, copied from the native driver's summary.toml. Output:
./summary.json, atomically replaced on each invocation. Each result includes its
SHA-256. Missing, malformed, failed and incomplete returns remain visible.

A quantitative pair requires both SCBA flags true, all three finite nonnegative
terminal residuals <= 1e-8, and eight finite, consecutive, matching iteration
numbers and J values in each arm, plus matching provenance. Differences and per-arm last-eight J ranges
are reported separately; these checks do not establish transport convergence.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shlex
import sys
import tempfile
import tomllib

RESIDUALS = ('r_K', 'r_Σ', 'r_λ')
FIXED = ('schema', 'field_kV_cm', 'voltage_mV_per_period', 'temperature_K', 'hartree', 'method',
         'energy_min_meV', 'energy_max_meV', 'energy_nodes', 'energy_trust_margin_meV',
         'spatial_nodes', 'basis_states', 'basis_periods', 'basis', 'qz_nodes',
         'k_max_nm_inverse', 'qz_max_nm_inverse', 'seed_eta_meV', 'embedding_periods',
         'alpha_sigma', 'channels', 'light', 'electron_electron_collisions', 'screening',
         'ifr_correlation', 'cold_start')
HASHES = ('driver_sha256', 'device_sha256', 'manifest_sha256', 'core_source_tree_sha256', 'runner_source_tree_sha256')


def finite_number(x):
    return type(x) in (int, float) and math.isfinite(x)


def manifest(path):
    cases = {}
    for line in path.read_text(encoding='utf-8').splitlines():
        parts = shlex.split(line, comments=True)
        if len(parts) < 2 or parts[0] != 'VARS' or not parts[1].startswith('D'):
            continue
        node = parts[1]
        if not re.fullmatch(r'D[A-Za-z0-9_]+', node) or node in cases:
            raise ValueError(f'invalid or duplicate node {node!r}')
        args = {}
        for entry in parts[2:]:
            key, sep, value = entry.partition('=')
            if not sep or key in args:
                raise ValueError(f'invalid VARS for {node}')
            args[key] = value
        field, rings, angles = float(args['field']), int(args['rings']), int(args['angles'])
        if field not in (12.5, 21.0) or rings not in (9, 17, 33) or angles not in (32, 128):
            raise ValueError(f'unexpected parameters for {node}')
        cases[node] = {'field_kV_cm': field, 'radial_nodes': rings, 'angular_nodes': angles}
    expected = {(f, k, 32) for f in (12.5, 21.0) for k in (9, 17, 33)} | {(21.0, k, 128) for k in (17, 33)}
    actual = [(v['field_kV_cm'], v['radial_nodes'], v['angular_nodes']) for v in cases.values()]
    if len(actual) != 8 or set(actual) != expected:
        raise ValueError('manifest must contain eight unique required V843 VARS parameter combinations')
    return cases


def read_result(node, params):
    path = Path('results') / (node + '.toml')
    result = {'parameters': params, 'status': 'missing', 'sha256': None, 'issues': []}
    if not path.is_file():
        result['issues'].append('result file absent')
        return result
    raw = path.read_bytes()
    result['sha256'] = hashlib.sha256(raw).hexdigest()
    try:
        data = tomllib.loads(raw.decode('utf-8'))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        result.update(status='failed', issues=[f'invalid TOML: {exc}'])
        return result
    result['native_status'] = data.get('status')
    result['scba_converged'] = data.get('scba_converged')
    if data.get('status') == 'failed':
        result.update(status='failed', issues=[str(data.get('error', 'native run failed'))])
        return result
    issues = result['issues']
    for key, value in params.items():
        if key not in data:
            issues.append(f'missing {key}')
        elif not finite_number(data[key]) or data[key] != value:
            issues.append(f'mismatched {key}')
    if not isinstance(data.get('status'), str) or not data['status']:
        issues.append('missing status')
    elif data['status'] in ('building', 'running'):
        issues.append('native run has not finished')
    if type(data.get('scba_converged')) is not bool:
        issues.append('missing scba_converged')
    history = data.get('iterations')
    if not isinstance(history, list) or not history or not all(isinstance(row, dict) for row in history):
        issues.append('missing iterations')
        history = []
    terminal = history[-1] if history else data.get('last_iteration', {})
    if not isinstance(terminal, dict):
        terminal = {}
    supplied_last = data.get('last_iteration')
    meaningful = ('ν', 'J_A_cm2', *RESIDUALS)
    if not isinstance(supplied_last, dict) or any(
            key not in terminal or key not in supplied_last or terminal[key] != supplied_last[key]
            for key in meaningful):
        issues.append('missing or inconsistent meaningful last_iteration fields')
    result['terminal'] = {}
    for key in ('J_A_cm2', *RESIDUALS):
        value = terminal.get(key)
        if not finite_number(value) or (key in RESIDUALS and value < 0):
            issues.append(f'missing or invalid terminal {key}')
        else:
            result['terminal'][key] = value
    tail = history[-8:]
    indices = [row.get('ν') for row in tail]
    currents = [row.get('J_A_cm2') for row in tail]
    if (len(tail) != 8 or not all(type(i) is int for i in indices)
            or any(b != a+1 for a, b in zip(indices, indices[1:]))
            or not all(finite_number(v) for v in currents)
            or not all(finite_number(row.get(k)) and row[k] >= 0 for row in tail for k in RESIDUALS)):
        issues.append('missing or nonconsecutive finite last-eight history')
    else:
        result['last8'] = {'iterations': indices, 'J_min_A_cm2': min(currents), 'J_max_A_cm2': max(currents), 'J_range_A_cm2': max(currents)-min(currents), 'J_end_minus_start_A_cm2': currents[-1]-currents[0]}
    provenance = {key: data.get(key) for key in (*HASHES[:3], *FIXED)}
    for package in ('core', 'runner'):
        identity = data.get(package)
        provenance[package + '_source_tree_sha256'] = identity.get('source_tree_sha256') if isinstance(identity, dict) else None
    result['provenance'] = provenance
    for key in HASHES:
        if not isinstance(provenance[key], str) or not re.fullmatch(r'[0-9a-fA-F]{64}', provenance[key]):
            issues.append(f'missing or invalid provenance {key}')
    for key in FIXED:
        if provenance[key] is None or (isinstance(provenance[key], float) and not math.isfinite(provenance[key])):
            issues.append(f'missing or invalid fixed parameter {key}')
    axis, density = data.get('density_z_nm'), data.get('density_z_cm_minus_3')
    if (isinstance(axis, list) and isinstance(density, list) and len(axis) == len(density)
            and len(axis) > 0 and all(finite_number(x) for x in axis + density)):
        result['density'] = {'z_nm': axis, 'cm_minus_3': density}
    result['status'] = 'inconclusive' if issues else 'complete'
    return result


def collect():
    cases = manifest(Path('cluster.dag'))
    results = {node: read_result(node, params) for node, params in cases.items()}
    lookup = {(p['field_kV_cm'], p['radial_nodes'], p['angular_nodes']): node for node, p in cases.items()}
    pairs = []
    requested = [(f, k, 32, f, k2, 32, 'radial') for f in (12.5, 21.0) for k, k2 in ((9, 17), (17, 33))]
    requested += [(21.0, 17, 128, 21.0, 33, 128, 'radial')]
    requested += [(21.0, k, 32, 21.0, k, 128, 'angular') for k in (17, 33)]
    for f, k, n, f2, k2, n2, kind in requested:
        a, b = lookup[(f, k, n)], lookup[(f2, k2, n2)]
        left, right = results[a], results[b]
        reasons = []
        for node, res in ((a, left), (b, right)):
            if res['status'] != 'complete':
                reasons.append(f'{node}: {res["status"]}')
            elif res['scba_converged'] is not True:
                reasons.append(f'{node}: SCBA not converged')
            elif any(res['terminal'][key] > 1e-8 for key in RESIDUALS):
                reasons.append(f'{node}: residual exceeds 1e-8')
        if not reasons:
            for key in (*HASHES, *FIXED):
                if left['provenance'][key] != right['provenance'][key]:
                    reasons.append(f'provenance or fixed parameter mismatch: {key}')
        pair = {'kind': kind, 'nodes': [a, b], 'status': 'inconclusive' if reasons else 'quantitative', 'reasons': reasons}
        usable = all(res.get('native_status') not in (None, 'building', 'running', 'failed') and
                     'J_A_cm2' in res.get('terminal', {}) for res in (left, right))
        if usable:
            pair['delta_J_A_cm2'] = right['terminal']['J_A_cm2'] - left['terminal']['J_A_cm2']
            pair['value_kind'] = 'quantitative' if not reasons else 'descriptive'
            pair['observed_last8_J_ranges_A_cm2'] = [res.get('last8', {}).get('J_range_A_cm2') for res in (left, right)]
        ld, rd = left.get('density'), right.get('density')
        if usable and ld and rd and ld['z_nm'] == rd['z_nm']:
            delta = [v-u for u, v in zip(ld['cm_minus_3'], rd['cm_minus_3'])]
            pair['density_difference'] = {'z_nm': ld['z_nm'], 'right_minus_left_cm_minus_3': delta,
                                          'max_abs_cm_minus_3': max(map(abs, delta)),
                                          'value_kind': 'quantitative' if not reasons else 'descriptive'}
        pairs.append(pair)
    relevant = [p for p in pairs if p['kind'] == 'radial' and
                [cases[n]['field_kV_cm'] for n in p['nodes']] == [21.0, 21.0] and
                [cases[n]['radial_nodes'] for n in p['nodes']] == [17, 33]]
    cross = {'status': 'inconclusive', 'definition': '(J33-J17)128 - (J33-J17)32'}
    if len(relevant) == 2 and all('delta_J_A_cm2' in p for p in relevant):
        by_angle = {cases[p['nodes'][0]]['angular_nodes']: p for p in relevant}
        p32, p128 = by_angle[32], by_angle[128]
        cross['delta_A_cm2'] = p128['delta_J_A_cm2'] - p32['delta_J_A_cm2']
        ranges = p32['observed_last8_J_ranges_A_cm2'] + p128['observed_last8_J_ranges_A_cm2']
        cross['sum_four_last8_ranges_A_cm2'] = sum(ranges) if all(x is not None for x in ranges) else None
        cross['nodes'] = p32['nodes'] + p128['nodes']
        baseline = results[cross['nodes'][0]].get('provenance', {})
        same_provenance = all(results[n].get('provenance', {}) == baseline for n in cross['nodes'])
        cross['status'] = 'quantitative' if same_provenance and all(p['status'] == 'quantitative' for p in relevant) else 'descriptive'
        cross['provenance_matches_all_four'] = same_provenance
    return {'cross_difference': cross, 'schema': 'v843-collection-v1', 'dag_sha256': hashlib.sha256(Path('cluster.dag').read_bytes()).hexdigest(), 'cases': results, 'pairs': pairs, 'qualification': 'Native SCBA checks alone do not establish full transport convergence; observed drifts are not error bounds.'}


def main():
    if sys.argv[1:] == ['--help']:
        print(__doc__)
        return
    if len(sys.argv) != 1:
        raise SystemExit(__doc__)
    try:
        summary = collect()
        payload = json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
        fd, name = tempfile.mkstemp(prefix='.summary-', suffix='.tmp', dir='.')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as stream:
                stream.write(payload)
            os.replace(name, 'summary.json')
        finally:
            if os.path.exists(name):
                os.unlink(name)
    except (OSError, ValueError, KeyError) as exc:
        raise SystemExit(f'collection failed: {exc}')
    print('Wrote summary.json; native SCBA does not establish full transport convergence.')


if __name__ == '__main__':
    main()
