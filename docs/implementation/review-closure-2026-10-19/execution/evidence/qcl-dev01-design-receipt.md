# DEV01 design receipt — CP-DESIGN pending

Время подготовки: 2026-10-19T12:03:39.871211+00:00.
Роль: D ultra, gpt-6.1-sol; packet L-SOURCE (не numerical run).
Root: e0f244d075dd49874ba4f3847f4efa693f3b3622.
Core: 3108150dd1b6b1377470b384b15c26e272fe5c5d.
Source: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGF.jl`. Source status перед подготовкой clean.
Scratch proposed diff: `/tmp/qcl-dev01-design.patch`.
SHA-256 patch: `84c5fa33deab71b2a70e43afdaacbd7e30370ffd01d984d296a9616bb8f587ea`.
Product edits: 0. Imports/tests/builds/SCBA/Poisson: 0.
Independent reviewer читает immutable sources; candidate пока не approved.

## Предлагаемый контракт

Только owning prose и EQ-CURRENT-002 в трёх разрешённых theory files.
Code/API/model/scattering/criteria/schema/test/generated HTML не меняются.
Сохраняются 0 mV/period, lattice/LO70 K, LO/acoustic/impurity/IFR/alloy,
electron–electron=none, strict criteria и fixed light UI.

| Proposed sentence/claim | Core3108150 primary locator | Что устанавливает источник | Ограничение |
| --- | --- | --- | --- |
| D08-01: prefactor eg_s/(2πℏ) | src/physics/observables.jl:239–253::energy_resolved_current | sum wk·Re(trace), затем gs/(2π), J0/E0_eV и A/m²/eV | Static expression; nonzero numeric oracle не запускался |
| D08-01: J=ΣwE·j=eΦ, weights in eV, ℏ in eV·s | src/physics/observables.jl:175–204::_current_trace/_boundary_flux_complex, :226–230::boundary_flux; src/domain/scaling.jl:17–22; src/numerics/reference/grids.jl:24–27; docs/src/theory/04_scaling.md:45–50 | wEbar без2π; wE_phys=E0_eV·wEbar, J0=eE0/(ℏL0²); исходящий знак | Algebraic API consistency, no new tolerance/acceptance |
| D08-01: preserve bond reconstruction | src/physics/observables.jl:266–280::bond_current | all a,b coherence, wE·wk·gs/(2π), J0, internal Nz−1 bonds | Finite basis/seam accuracy не certified |
| D08-02: μ0 from target, final G< filled once | src/numerics/optimized/seed.jl:177–198::_seed_green_production; :118–125::_seed_lesser_production! | scaled target ND²D, Bisection root, one allocate/fill with ifA | Finite quadrature seed, no full SCBA convergence claim |
| D08-02: no unilateral post-root scaling; Fermi bounds motivation | src/numerics/optimized/seed.jl:196–198; src/numerics/optimized/production_operators.jl:1304–1331::_green_state_production | explicit comment, direct return G>/A derived, GL preserved | No extra numerical Pauli test; policy unchanged |
| D08-03: pzp canonical; accepted pzp/none/real_space; legacy rejection | src/numerics/reference/basis.jl:101–110::build_localized_basis, :124–156, :206–217, :268–275::build_basis | exact accepted tuple, ArgumentError otherwise; pzp truncation/Löwdin; wrapper forwards | Full-window methods remain separate and unchanged |

## Existing anchors (read only)

- `test/physics/full_window_basis_preserves_the_spectral_subspace.jl:54–79`:
  real_space N_b==N_z requirement, `legacy_pzp` throws, positive `pzp` call.
- `test/numerics/production_seed_chemical_potential_trials_are_scalar.jl:19–36`:
  scalar q-vector and same finite quadrature (16eps assertion); :38–44 allocation bound.
- `test/physics/analytic_equilibrium_sum_rule_lo_balance_and_zero_current_anchors.jl:132–137`:
  zero-current only; does not distinguish a wrong global current prefactor.
- `test/numerics/formula_anchors_remain_traceable.jl:43–45/:51–54`:
  anchor/symbol existence, no formula truth assertion.

Все anchors только прочитаны; assertions execution не заявляется. O08-04 remains
separate DEV02–06 contract and nonzero API oracle.

## Alternatives и решение для review

1. Исправить owning documentation по selected implementation (предложено).
2. Менять current measure, seed Pauli policy или добавлять legacy alias в code:
   выходит за DEV01; не предлагается и не выполняется.
3. Оставить несовпадающие заявления: читатель получит factor2π discrepancy,
   несуществующий post-root scaling и unsupported localization input.

CP-DESIGN reviewer проверяет source→sentence и semantic scope. Если ambiguity
касается numerical/formula contract, спорную correction передать DEV02, не solver edit.

## Static acceptance после CP-DESIGN

- Candidate diff затрагивает ровно 3 permitted files.
- Сохранены anchors EQ-CURRENT-001/002, eq-boundary-flux/eq-resolved-current и API refs.
- Prefactor, физические веса, sign и единицы совместны с actual API algebra.
- Seed prose не обещает post-root normalization и не меняет Pauli policy.
- Basis prose перечисляет exact accepted tuple, `legacy_pzp` только rejection.
- `git diff --check`, focused `rg`, проверка local refs и source→sentence review.
- Не выполнять deno docs/check/test, Julia import/solve либо environment bootstrap
  в docs-only packet; runtime/convergence/physical gates/discretization/experiment
  остаются not_measured, docs статическая проверка их не закрывает.

## Source hashes перед scratch diff

- `docs/src/theory/11_observables.md`: `e83506c6ce49601fbeb43d76df3e4c8a62eaf7701cf09036bfedbf0a0cdfc2da`
- `docs/src/theory/19_production.md`: `b38bc5d5e5d93afc582adc660dd71040f65873814eee82bcdd85f6cffa54d949`
- `docs/src/theory/05_basis.md`: `3e80f5e8d1f1023c85274c60252c2b0cd78f899c56d3f6652073efaea7424411`

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Три предложенных owning corrections отражают selected source | locators и exact scratch diff выше | CP-DESIGN/CP-CODE ещё не закрыты; product edits=0 | изменить |
| Current seed/basis численно верифицированы этим packet | runtime execution=0 | numerical/model/experimental acceptance не измерены | данных недостаточно |
