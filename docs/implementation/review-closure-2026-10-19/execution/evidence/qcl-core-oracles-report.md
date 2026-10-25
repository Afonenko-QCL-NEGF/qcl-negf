# Core DEV03 / DEV08: frozen implementation candidate

2026-10-19. Этап: implementation новых bounded functional fixtures. Root
04eecba1ea795a7c8861c4bfd0bb5aa49f093ee6, Core
 a8d2c0de21dfdce3ed3c7c585c555656443f6d89. Создана ветка
`codex/review-closure-numerical-oracles` от actual Core a8d2c0d.
Core tracked files unchanged; ровно два новых untracked test-файла.
Никаких commits/push, Julia invocation/import, tests, solver, SCBA, build,
installation/network или spawn не выполнялось. CP-CODE/runtime не заявлены.
Прочитаны root AGENTS/architecture, handoff README/autonomy/P1/development
четыре cards, owning CONTRIBUTING/O08 passports и actual function signatures.
Применён qcl-physics-audit для конвенций/независимости; TDD ограничен новыми
fixtures, production implementation отсутствует. Runtime принадлежит root.

## Frozen packet

| Card | Path | File SHA256 | Diff snapshot / SHA256 |
|---|---|---|---|
| DEV03 | test/numerics/keldysh_literal_matrix_oracle.jl | 9a22526d104dc15e25b203a52631687819999ea1c84872627199c00062373d42 | /tmp/qcl-dev03-oracle.diff / 63de730d5844c7d86601cfdd813441f83fd317f402612a7d273a08722f291afa |
| DEV08 | test/numerics/principal_value_independent_oracle.jl | bae8a57957cd9df4da0d7369521a7d7ffa776b4c095859e0d1a9f86a9607eb6e | /tmp/qcl-dev08-oracle.diff / 5af101be36fa1dfbe274ad435724c9585d22885fcfe2b04245f690cffe4dc933 |

DEV08 path — точное proposed имя из card; первоначальный brief alternative
`direct_fft_principal_value_oracle.jl` не использован.

Source SHA256:
- src/numerics/reference/greens.jl: 25f476e3ac4f4c282433f55286ded0893994ac9bb1ce8c0ab17fe1c3b288f5b9
- src/numerics/reference/kernels.jl: ad3e5172d80eeaebab496d5e22a82b4db960a66e27ee4bcb3a234b987dbf055d
- src/numerics/optimized/production_operators.jl: 7b4e6cd55b259a2477b799ecfb30ae818ce17a3bbf5c6ff81d2087af17bb62df
- existing test/numerics/fft_linear_hilbert_map_equals_direct_principal_value.jl: b6ab4415751473d48f8b243fd91c00f127515b164736a3098432f4028ae33737

## Runtime request to shared-slot owner (NOT executed)

Prerequisite INT01 import READY and exact prepared environment binding.
Одна initially bounded L-JL invocation на card; не запускать одновременно.
Caps per invocation: 120s wall / 1 CPU / 2GiB RAM / 16MiB tmp / 2MiB logs;
root owns aggregate counters and stop. Не более двух calls/card по card
без silent retry; этот пакет calls=0.

From root worktree, prepared Julia executable/environment:

```
julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/numerics/keldysh_literal_matrix_oracle.jl")'
julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/numerics/principal_value_independent_oracle.jl")'
```

DEV03 numeric workload: one 2x2 product, fixed controls, <1MiB numeric data.
DEV08 largest NE=325,Nk=Nb=1; at most 1024 padded FFT length, sequential
small arrays, <1MiB simultaneous explicit numeric data; module import/JIT
may dominate RAM/time and is not measured. No result files expected, no
iterations or scientific solves. Stop on first failed assertion/limit;
preserve original output. Do not import unrelated existing nonlinear suite.

DEV03 evidence requested: all four complex entries exact, anti-Hermitian,
2x2 principal-minor PSD certificate, fixed-RHS negative variants.
DEV08 evidence requested: both APIs against fixed three-node literal RHS;
zero/sign/finite-diagonal/cyclic controls; center-only compact-support PV
with exact omitted-cell error, explicit omitted tail, W=3/5 contamination
control and h-proportional refinement. Existing 2e-13 arithmetic regression
budget retained; no continuum all-energy or physical-spectrum claim.

## Focused D gap DEV04 / DEV06 (no files created)

Actual `src/domain/types.jl::NumericalParameters` positional and keyword
constructors enforce NE>=3,Nk>=2. Accepted O08-04 specifies NE=Nk=Nb=2
for trace oracle and NE=Nk=1 for coherence. Public APIs need full
NEGFProblem. No inconsistent numerical/grid/array carrier or constructor
bypass created. Need exact consistent complete carrier + independent RHS
mapping without changing physical S1 model or weakening limits.

DEV04 direct Poisson four-cell inputs are specified, but assessment needs
NEGFSolution/problem carrier without seed/build hidden solve or unexplained
required fields. Existing acceptance_metadata_registry uses build_problem
and _seed_green and cannot be copied as independent full-state oracle.
Coordinator explicitly froze DEV04/06 until corrected ultra design + high
review; no new physics authority or human permission needed.

| Утверждение | Свидетельство | Ограничение | Решение |
|---|---|---|---|
| DEV03 literal independent fixture подготовлен | frozen file/diff hashes; actual keldysh signature | runtime/CP-CODE not_measured | дополнительно измерить |
| DEV08 discrete и center continuum разделены | fixed literals; analytic cell/tail formulas in fixture | runtime/CP-CODE not_measured; не general PV bound | дополнительно измерить |
| Existing production/controls сохранены | Core git diff empty; only two new untracked tests | untracked files require independent review | сохранить |
| DEV04/06 consistent carrier готов | actual constructor minima contradict accepted tiny cardinalities | focused design pending; files absent | данных недостаточно |
| Scientific acceptance получена | execution отсутствует | functional fixtures не scientific solve | данных недостаточно |
