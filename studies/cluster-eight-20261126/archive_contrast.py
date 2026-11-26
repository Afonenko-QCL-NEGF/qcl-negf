#!/usr/bin/env python3
"""Offline sign persistence of GL20 centered rank contrasts on archived Fath maps.

Run from any directory: python archive_contrast.py [snapshot.jsonl]
No fitting or fresh calculation. The late drift is a sensitivity indicator, not
an uncertainty bound or evidence of stationarity.
"""
import hashlib
import json
import math
import sys
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent.parent / 'fath54-common-q/evidence/fath-snapshot.jsonl'


def analyze(path):
    raw = path.read_bytes()
    maps = {}
    for line in raw.splitlines():
        item = json.loads(line)
        if item.get('kind') == 'map' and item.get('step') in (24, 32):
            if item.get('name') in ('W7_common', 'W8_common', 'W9_common'):
                if 'GL20' not in item.get('observation', {}):
                    continue
                key = (item['name'], item['step'])
                if key in maps:
                    raise ValueError(f'duplicate map {key}')
                maps[key] = item
    out = {'input_name': path.name, 'sha256': hashlib.sha256(raw).hexdigest(), 'pairs': {}}
    for low, high in ((7, 8), (8, 9)):
        contrasts = {}
        ratios = {}
        for step in (24, 32):
            a, b = (maps[(f'W{w}_common', step)] for w in (low, high))
            if any(m['Q'] != 28 or m['W'] != w or m['step'] != step
                   for m, w in ((a, low), (b, high))):
                raise ValueError('expected requested rank, step and common Q28')
            x = a['observation']['GL20']['centered']
            y = b['observation']['GL20']['centered']
            if len(x) != 145 or len(y) != len(x) or not all(math.isfinite(v) for v in x + y):
                raise ValueError('invalid profile')
            contrasts[step] = [v - u for u, v in zip(x, y)]
            ratios[step] = {}
            for k in ('rK', 'rSigma'):
                values = (a['row'][k], b['row'][k])
                if not all(isinstance(v, (int, float)) and math.isfinite(v) and v > 0 for v in values):
                    raise ValueError(f'{k} must be positive and finite: {values}')
                ratios[step][k] = max(values) / min(values)
        old, new = contrasts[24], contrasts[32]
        drift = max(abs(v-u) for u, v in zip(old, new))
        # A same-sign node whose magnitude exceeds observed late drift at both
        # times remains signed under this empirical sensitivity scale.
        stable = sum(u*v > 0 and min(abs(u), abs(v)) > drift for u, v in zip(old, new))
        flip = sum(u*v < 0 for u, v in zip(old, new))
        idx = max(range(len(new)), key=lambda i: abs(new[i]))
        out['pairs'][f'W{low}->W{high}'] = {
            'D24_A_cm2': max(map(abs, old)), 'D32_A_cm2': abs(new[idx]),
            'signed_peak32_A_cm2': new[idx], 'peak_index_zero_based': idx,
            'max_contrast_drift_24_32_A_cm2': drift,
            'same_sign_above_drift_nodes': stable, 'sign_flipped_nodes': flip,
            'total_nodes': len(new), 'residual_ratios': ratios,
            'residuals_matched': all(v <= 1.25 for row in ratios.values() for v in row.values()),
        }
    return out


def main():
    if len(sys.argv) > 2:
        raise SystemExit(__doc__)
    path = Path(sys.argv[1]).resolve() if len(sys.argv) == 2 else DEFAULT
    print(json.dumps(analyze(path), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
