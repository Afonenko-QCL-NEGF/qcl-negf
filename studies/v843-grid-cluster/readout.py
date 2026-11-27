#!/usr/bin/env python3
"""Audit independent V843 native outputs against separately frozen plans."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import re
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'analysis/src'))
spec = importlib.util.spec_from_file_location('v843_campaign', REPO / 'studies/v843-spectrum/campaign.py')
campaign = importlib.util.module_from_spec(spec)
spec.loader.exec_module(campaign)
from qcl_negf_results.presentation import inside
from qcl_negf_results.spectrum import read_cell_spectrum, compare_cell_spectra


def author_inputs():
    catalog = REPO / 'studies/v843-spectrum/devices.yaml'
    text = catalog.read_text(encoding='utf-8')
    entries = re.findall(r'^    - path: (.+)\n      sha256: ([0-9a-f]{64})$', text, re.M)
    if len(entries) != 2 or '  dupont-v843:\n' not in text:
        raise ValueError('unexpected published V843 device catalog')
    receipts = []
    for relative, expected in entries:
        path = (catalog.parent / relative).resolve(strict=True)
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError('published catalog input digest mismatch: ' + relative)
        receipts.append({'name': path.name, 'sha256': actual})
    return receipts


def validate_plan(case, frozen, expected_inputs):
    if len(frozen['executions']) != 1 or len(frozen['points']) != 1:
        raise ValueError('expected exactly one frozen execution and point')
    execution, axis = frozen['executions'][0], frozen['points'][0]
    if (frozen['root_definition_id'] != case['id']
            or execution['definition_id'] != case['id']
            or execution['author_device'] != 'dupont-v843'
            or execution['author_inputs'] != expected_inputs):
        raise ValueError('frozen definition or published author input identity mismatch')
    if axis['execution_id'] != execution['id']:
        raise ValueError('frozen point execution identity mismatch')
    return execution, axis


def read_case(case, plan_path, root, settings, expected_inputs):
    frozen_bytes = plan_path.read_bytes()
    frozen = json.loads(frozen_bytes)
    if json.loads(inside(root, 'scientific_plan.json').read_bytes()) != frozen:
        raise ValueError('delivered plan differs from independently frozen plan')
    series = json.loads(inside(root, 'series_result.json').read_bytes())
    if series['plan_fingerprint'] != frozen['fingerprint']:
        raise ValueError('series plan fingerprint mismatch')
    execution, axis = validate_plan(case, frozen, expected_inputs)
    if len(series['points']) != 1:
        raise ValueError('expected exactly one series point')
    row = series['points'][0]
    if execution['operation'] != 'structure_spectrum' or execution['point_ids'] != [axis['id']]:
        raise ValueError('unexpected operation or execution point')
    if (row['id'], row['execution_id']) != (axis['id'], execution['id']):
        raise ValueError('series execution/point identity mismatch')
    if row['status'] != 'completed':
        raise ValueError('point status is ' + str(row['status']))
    expected_voltage = settings['period_nm'] * settings['field_kV_cm'] * 1e-4
    if (axis['temperature_K'] != settings['temperature_K']
            or axis['effective_inputs']['lo_temperature_K'] != settings['temperature_K']
            or abs(axis['voltage_per_period_V'] - expected_voltage) > 1e-14):
        raise ValueError('temperature or voltage differs from registered condition')
    relative = row['data']['artifact_root'] + '/artifacts'
    item = read_cell_spectrum(inside(root, relative))
    if (item['plan_fingerprint'], item['execution_id'], item['point_id']) != (frozen['fingerprint'], execution['id'], axis['id']):
        raise ValueError('native receipt identity mismatch')
    basis, spectrum = item['checks']['structure_basis_orthonormal'], item['spectrum']
    if (basis['basis_states'] != case['rank'] or 2*basis['basis_periods']+1 != case['window']
            or len(spectrum['energies_eV']) != case['rank'] or len(spectrum['z_nm']) != case['nz']
            or abs(basis['period_nm'] - settings['period_nm']) > 1e-10):
        raise ValueError('native geometry differs from index')
    item['source'] = {'plan_sha256': hashlib.sha256(frozen_bytes).hexdigest(),
                      'plan_fingerprint': frozen['fingerprint'], 'execution_id': execution['id'],
                      'point_id': axis['id'], 'artifact_root': relative, 'sha256': item['result_sha256']}
    return item


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('index', type=Path)
    p.add_argument('artifacts_root', type=Path, help='directory containing plans/, results/ and optional crosscheck/')
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    settings = campaign.rule()
    reference = campaign.figure(campaign.FIGURE_PATH, settings['figure_sha256'])
    expected_inputs = author_inputs()
    cases = json.loads(args.index.read_text(encoding='utf-8'))['cases']
    expected = {(w, r, n) for w in (7, 9, 11) for r in (7, 8, 11) for n in (96, 144, 216, 288)}
    coordinates = [(c['window'], c['rank'], c['nz']) for c in cases]
    if len(cases) != 36 or set(coordinates) != expected or len(set(coordinates)) != 36:
        raise ValueError('index must contain exactly the registered 36 distinct coordinates')
    for c in cases:
        if c['id'] != f"b{c['window']}-r{c['rank']}-z{c['nz']}":
            raise ValueError('index ID does not match coordinates')
        inside(args.index.parent, c['study'])
    rows, items, failures = [], {}, []
    for c in cases:
        case_id = c['id']
        row = {'id': case_id, 'window': c['window'], 'rank': c['rank'], 'nz': c['nz']}
        try:
            item = read_case(c, inside(args.artifacts_root, f'plans/{case_id}.json'),
                             inside(args.artifacts_root, f'results/{case_id}'), settings, expected_inputs)
            metrics = {}
            for name, threshold in settings['translation_limits'].items():
                check = item['checks'][name]
                value = check['value']
                if not math.isfinite(value) or value < 0 or check['threshold'] != threshold or check['passed'] != (value <= threshold):
                    raise ValueError(f'inconsistent static evidence: {name}')
                metrics[name] = value
            metrics['structure_translation_two_pairs'] = max(metrics['structure_translation_two_pairs'], metrics['structure_translation_nearest'])
            static_reasons = set(item['failed_checks'])
            if metrics['structure_translation_two_pairs'] > settings['translation_limits']['structure_translation_two_pairs']:
                static_reasons.add('structure_translation_two_pairs')
            fit = campaign.compare_figure(*campaign.spectrum_arrays(item), reference, settings)
            row.update(status='static_rejected' if static_reasons else ('figure_admitted' if fit['admitted'] else 'figure_rejected'),
                       static_reasons=sorted(static_reasons), translation_metrics=metrics,
                       figure_comparison=fit, figure_interpretation='diagnostic_only_static_rejected' if static_reasons else 'registered_gate', source=item['source'])
            cross = args.artifacts_root / 'crosscheck' / case_id
            if cross.exists():
                second = read_case(c, inside(args.artifacts_root, f'plans/{case_id}.json'), cross, settings, expected_inputs)
                if case_id != 'b7-r7-z144':
                    raise ValueError('unexpected crosscheck coordinate')
                row['crosscheck'] = compare_cell_spectra(item, second, energy_atol_eV=1e-10, projector_atol=1e-8)
            elif case_id == 'b7-r7-z144':
                row['crosscheck'] = {'status': 'missing'}
            items[(c['window'], c['rank'], c['nz'])] = (item, fit)
        except Exception as exc:
            row.update(status='technical_failure', error=f'{type(exc).__name__}: {exc}')
            failures.append(case_id)
        rows.append(row)
    contrasts = []
    for w in (7, 9, 11):
        for r in (7, 8, 11):
            for a, b in zip((96, 144, 216), (144, 216, 288)):
                if (w, r, a) in items and (w, r, b) in items:
                    first, fit1 = items[w, r, a]; second, fit2 = items[w, r, b]
                    comparison = campaign.window_confirmation(first, second, fit1, fit2, settings)
                    comparison['interpretation'] = 'diagnostic_grid_comparison_not_a_registered_grid_gate'
                    contrasts.append(dict(window=w, rank=r, nz=[a, b], **comparison))
    expansions = []
    status_by_id = {row['id']: row['status'] for row in rows}
    for n in (96, 144, 216, 288):
        for r in (7, 8, 11):
            for a, b in ((7, 9), (9, 11)):
                if all(status_by_id[f'b{w}-r{r}-z{n}'] == 'figure_admitted' for w in (a, b)):
                    first, fit1 = items[a, r, n]; second, fit2 = items[b, r, n]
                    expansions.append(dict(nz=n, rank=r, windows=[a, b],
                                           **campaign.window_confirmation(first, second, fit1, fit2, settings)))
    report = {'schema': 'v843-grid-readout-v1', 'status': 'incomplete' if failures else 'complete',
              'rule_sha256': campaign.digest(campaign.RULE_PATH), 'figure_sha256': settings['figure_sha256'],
              'cases': rows, 'grid_contrasts': contrasts, 'window_confirmations': expansions, 'technical_failures': failures,
              'portability': next((r.get('crosscheck', {'status': 'unavailable'}) for r in rows if r['id'] == 'b7-r7-z144'), {'status': 'unavailable'})}
    rendered = json.dumps(report, indent=2, allow_nan=False) + '\n'
    if args.output:
        args.output.write_text(rendered, encoding='utf-8')
    else:
        print(rendered, end='')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
