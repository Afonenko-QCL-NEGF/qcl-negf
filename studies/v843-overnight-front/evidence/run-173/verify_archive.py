#!/usr/bin/env python3
"""Verify the published DAG 173 evidence against a private campaign directory.

Usage: python3 verify_archive.py PRIVATE_CAMPAIGN_ROOT
Only reads files. The adjacent summary.json and run-receipt.json are the
published reference; this program does not authenticate those reference files.
"""
import hashlib
import json
import re
import sys
from pathlib import Path


class VerificationError(Exception):
    pass


def load_json(path):
    try:
        with path.open(encoding='utf-8') as stream:
            return json.load(stream)
    except (OSError, UnicodeError, ValueError) as exc:
        raise VerificationError(f'cannot read JSON {path}: {exc}') from exc


def checked_path(root, relative):
    if not isinstance(relative, str) or not relative:
        raise VerificationError(f'invalid artifact path: {relative!r}')
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts:
        raise VerificationError(f'unsafe artifact path: {relative!r}')
    candidate = (root / path).resolve()
    if not candidate.is_relative_to(root):
        raise VerificationError(f'artifact escapes campaign root: {relative!r}')
    return candidate


def verify_hash(root, relative, expected):
    if not isinstance(expected, str) or not re.fullmatch(r'[0-9a-f]{64}', expected):
        raise VerificationError(f'invalid SHA-256 for {relative}')
    path = checked_path(root, relative)
    digest = hashlib.sha256()
    try:
        with path.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                digest.update(chunk)
    except OSError as exc:
        raise VerificationError(f'cannot read {relative}: {exc}') from exc
    actual = digest.hexdigest()
    if actual != expected:
        raise VerificationError(f'SHA-256 mismatch for {relative}: expected {expected}, got {actual}')


def indexed(items, label):
    result = {}
    for item in items:
        identity = item['id']
        if identity in result:
            raise VerificationError(f'duplicate ID {identity!r} in {label}')
        result[identity] = item
    return result


def main(root):
    here = Path(__file__).resolve().parent
    summary = load_json(here / 'summary.json')
    published = load_json(here / 'run-receipt.json')
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise VerificationError(f'not a directory: {root}')
    artifacts = summary['artifacts']
    attempts = published['attempts']
    if len(artifacts) != 21 or len(attempts) != 2 or sum(len(a['artifacts']) for a in attempts) != 8:
        raise VerificationError('unexpected published artifact inventory')
    all_paths = set()
    for name, ref in artifacts.items():
        path = ref['path']
        if path in all_paths:
            raise VerificationError(f'duplicate published path: {path}')
        all_paths.add(path)
        verify_hash(root, path, ref['sha256'])
    for attempt in attempts:
        for path, sha in attempt['artifacts'].items():
            if path in all_paths:
                raise VerificationError(f'duplicate published path: {path}')
            all_paths.add(path)
            verify_hash(root, path, sha)
    print('OK: 21 result artifacts and 8 attempt artifacts match published SHA-256')

    by_dag = {a['dag']: a for a in attempts}
    if len(by_dag) != 2 or set(by_dag) != {'173.0', '206.0'}:
        raise VerificationError('unexpected DAG IDs')
    manifests, receipts = {}, {}
    for dag, attempt in by_dag.items():
        paths = attempt['artifacts']
        manifest_path = next(p for p in paths if Path(p).name == 'manifest.json')
        receipt_path = next(p for p in paths if Path(p).name == 'receipts.json')
        manifest = load_json(checked_path(root, manifest_path))
        receipt = load_json(checked_path(root, receipt_path))
        jobs = indexed(manifest['jobs'], f'{dag} manifest')
        records = indexed(receipt['receipts'], f'{dag} receipts')
        if set(jobs) != set(records) or receipt['expected'] != len(jobs):
            raise VerificationError(f'{dag}: manifest and receipt inventories differ')
        if manifest['commit'] != attempt['source']:
            raise VerificationError(f'{dag}: manifest source differs from published source')
        counts = {state: sum(r['state'] == state for r in records.values())
                  for state in ('completed', 'technical', 'missing')}
        if sum(counts.values()) != len(records) or counts != receipt['counts']:
            raise VerificationError(f'{dag}: invalid receipt state counts')
        if any(counts[state] != attempt[state] for state in counts):
            raise VerificationError(f'{dag}: receipt counts differ from published attempt')
        manifests[dag], receipts[dag] = jobs, records
    main_jobs, recover_jobs = manifests['173.0'], manifests['206.0']
    main_receipts, recover_receipts = receipts['173.0'], receipts['206.0']
    failed = {i for i, r in main_receipts.items() if r['state'] == 'technical'}
    recovered = {i for i, r in recover_receipts.items() if r['state'] == 'completed'}
    main_success = {i for i, r in main_receipts.items() if r['state'] == 'completed'}
    if len(failed) != 6 or recovered != failed or set(recover_jobs) != failed:
        raise VerificationError('recovery does not match the six technical failures')
    if any(main_jobs[i]['family'] != 'F' or recover_jobs[i]['family'] != 'F' for i in failed):
        raise VerificationError('recovered cases are not all family F')
    for identity in failed:
        old, new = main_jobs[identity]['case_sha256'], recover_jobs[identity]['case_sha256']
        if not re.fullmatch(r'[0-9a-f]{64}', old) or old != new:
            raise VerificationError(f'{identity}: original and recovery case hashes differ or are invalid')
    if main_success & recovered or len(main_success | recovered) != published['unique_results'] or len(main_success | recovered) != 81:
        raise VerificationError('successful IDs overlap or do not total 81')
    if not set(artifacts) <= main_success | recovered:
        raise VerificationError('published result ID absent from successful receipts')
    print('OK: 75 + 6 unique completed IDs; six recovered F case hashes match both manifests')
    print('Scope: hashes and inventories only; no scientific validation or unlisted files checked.')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: python3 {Path(sys.argv[0]).name} PRIVATE_CAMPAIGN_ROOT', file=sys.stderr)
        sys.exit(2)
    try:
        main(Path(sys.argv[1]))
    except (VerificationError, OSError, KeyError, TypeError, ValueError, StopIteration) as exc:
        print(f'FAILED: {exc}', file=sys.stderr)
        sys.exit(1)
