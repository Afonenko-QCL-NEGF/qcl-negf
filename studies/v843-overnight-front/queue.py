#!/usr/bin/env python3
"""Generate a portable inventory of independent cases and an optional gated stage.

No numerical calculation, worker inventory, scheduling, or resource estimates.
"""
from __future__ import annotations
import argparse
import itertools
import json
from pathlib import Path


def case(family, id, description, **parameters):
    return {'id': id, 'family': family, 'description': description, 'parameters': parameters}


def build():
    base = []
    for b, rank, nz in itertools.product((7, 9, 11, 15), (8, 11, 14), (216, 288)):
        base.append(case('H', f'H_B{b}_R{rank}_Z{nz}', 'Hamiltonian window and rank control', B=b, rank=rank, Nz=nz))
    for k, nz in itertools.product((9, 17, 33, 65), (216, 288)):
        base.append(case('I', f'I_K{k}_Z{nz}', 'Impurity angular sweep with two nested reference grids in one job', K=k, Nz=nz, phi=[64,128,256,512,1024], phi_reference=[2048,4096]))
    for b, rank, eta in itertools.product((9, 11, 15), (8, 11, 14), (0.25, 0.5, 1.0)):
        label = str(eta).replace('.', 'p')
        base.append(case('G', f'G_B{b}_R{rank}_ETA{label}', 'Full-coordinate versus projected resolvent on nested energy grids', B=b, rank=rank, eta_meV=eta, Nz=288, K=17, E=[241,481]))
    for n, nz in itertools.product((7,9,11), (144,288)):
        base.append(case('F', f'F_N{n}_Z{nz}', 'Floquet period control at both boundary phases', Nperiod=n, Nz=nz, theta=[0, 'pi'], implementation='floquet.jl'))
    for e, k in itertools.product((239,477), (17,33)):
        base.append(case('C', f'C_E{e}_K{k}', 'Frozen five-channel source response with normalized test input; actual Q constructed and measured for the candidate', E=e, K=k, Q='measured_for_exact_candidate', input='normalized', channels=5))
    for b, rank in itertools.product((9,11,15), (11,14)):
        base.append(case('T', f'T_B{b}_R{rank}', 'Translated-basis candidate control', B=b, rank=rank, Nz=288))
    reserve = []
    for b, rank, eta in itertools.product((11,15), (11,14), (0.25,0.5)):
        reserve.append(case('RG', f'RG_B{b}_R{rank}_ETA{str(eta).replace(".","p")}', 'Reserve full-coordinate versus projected resolvent', B=b, rank=rank, eta_meV=eta, Nz=384, K=33, E=961))
    for b, rank in itertools.product((15,19), (11,14)):
        reserve.append(case('RH', f'RH_B{b}_R{rank}', 'Reserve Hamiltonian window and rank control', B=b, rank=rank, Nz=384))
    for k, nz in itertools.product((33,65), (288,384)):
        reserve.append(case('RI', f'RI_K{k}_Z{nz}', 'Reserve impurity forward-sector measurement, distinct from base angular sweep', K=k, Nz=nz, measurement='forward_sector_separately_resolved'))
    return sorted(base, key=lambda x:x['id']), sorted(reserve, key=lambda x:x['id'])


def graph(cases):
    return ''.join('[[task]]\n' + f'id = {json.dumps(c["id"])}\nparents = []\n' + f'description = {json.dumps(c["description"])}\n\n' for c in cases)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True, help='new output directory')
    args = p.parse_args()
    base, reserve = build()
    ids = [x['id'] for x in base + reserve]
    assert len(base) == 75 and len(reserve) == 16 and len(ids) == len(set(ids))
    # Narrow anchor frontier; alternative candidates require their own complete evidence.
    anchors = ['H_B11_R11_Z288','I_K17_Z288','T_B11_R11','C_E239_K17','G_B11_R11_ETA0p5']
    assert set(anchors) <= set(ids)
    optional = {
        'dispatch_by_default': False,
        'external_decision': 'ADMIT',
        'anchor_ids': anchors,
        'decision_rule': 'Review anchor diagnostics, then apply the complete pinned DAG 154 protocol to the exact MAP input and its actual retained Q. Require static assignment and neighboring window, the original H(k) test at 1e-10, the two original scalar/coherent impurity action tests at 1% with a stable reference, all five channels, current cuts, seed and measured memory feasibility. Bind code, inputs, projection and operators by hash. A changed basis or quadrature needs its own certificate. The reduced I, finite H/G and zero-field F do not pass any original gate by proxy. With missing original source, validation or hash equality leave MAP blocked.',
        'tasks': [
            {'id':'ADMIT', 'parents':anchors, 'kind':'external_decision'},
            {'id':'MAP0', 'parents':['ADMIT'], 'kind':'conditional_calculation', 'condition':'ADMIT explicitly accepts the candidate and its matching hashes'},
            {'id':'READ0', 'parents':['MAP0'], 'kind':'conditional_review'}
        ],
        'graph_note': 'For a combined graph append these tasks to base.toml; the external decision must enforce the scientific condition. No optional task belongs to the independent base or reserve.',
    }
    args.out.mkdir(parents=False, exist_ok=False)
    (args.out/'cases.json').write_text(json.dumps({'base':base,'reserve':reserve}, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    (args.out/'base.toml').write_text(graph(base), encoding='utf-8')
    (args.out/'reserve.toml').write_text(graph(reserve), encoding='utf-8')
    (args.out/'optional-stage.json').write_text(json.dumps(optional, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    print(f'base={len(base)} reserve={len(reserve)} optional={len(optional["tasks"])}; output={args.out}')

if __name__ == '__main__':
    main()
