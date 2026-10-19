# DEV04 / DEV06 — frozen implementation candidate

2026-10-19, medium I, sole Core writer. Core source
`a8d2c0de21dfdce3ed3c7c585c555656443f6d89`, existing branch
`codex/review-closure-numerical-oracles`. No Git mutations, tracked edits,
Julia execution/import, tests, solver loops, builds, installation/network or
spawns in this continuation. Runtime/CP-CODE not_measured.

Accepted design SHA256:
`17c6dda56a2223bde9d20e98928e659d9e60fb7d6615b72ff94dcf190b829ea1`;
independent review SHA256:
`b5b3f58eb879272ed4be2081f36fa5c21c9f3733e961951d4649b6feb2edc348`.
Root selected exact DEV04 donor precondition, not the alternative shifted RHS.

| Card | New file | SHA256 | Frozen diff / SHA256 |
|---|---|---|---|
| DEV04 | test/physics/nonneutral_periodic_poisson_assessment.jl | 3cd3ef409e82e790bfe1581c392cf1d3209900d4c753e419564d5f583518beaa | /tmp/qcl-dev04-oracle.diff / d2fb3a167556b07e5a4f4cd93bbf3e45de5ebb50f8c03e1379cede2725ff2b32 |
| DEV06 | test/physics/nonzero_public_current_oracle.jl | 17fed2fae5b45549c65cec576cc108f68922a04e3830c0246313ccafd4ee8d01 | /tmp/qcl-dev06-oracle.diff / 22f53f66b07c0dbe13dc71e70bd95e607def6194977e836999bfac3094fb3d46 |

Machine packet: `/tmp/qcl-dev04-dev06-oracle-freeze.json`.
DEV03/08 original file hashes rechecked byte-identical:
`9a22526d104dc15e25b203a52631687819999ea1c84872627199c00062373d42`,
`bae8a57957cd9df4da0d7369521a7d7ffa776b4c095859e0d1a9f86a9607eb6e`.

## Scope and evidence requested

Both fixtures construct physical and numerical objects through existing
checked constructors and `build_problem(validate_static=true)` with
manufactured microscopic channels explicitly disabled. They assert all
actual grid axes/weights, profiles, kernels, four shifts, model defaults and
independent SI scale ratios. They do not assemble or modify NEGFProblem,
ModelGrids, MaterialProfiles, BasisData or KernelSet directly. Helpers are
local to each module; no new shared registration/framework/files introduced.
Production all-five S1 model is unchanged.

DEV04: Nz=Nb4 real-space analytic basis inventory; exact
`problem.profiles.Nᴰ==ones(4)` assertion AND explicit fatal stop before
any Poisson solve/synthetic construction if false. No approximate fallback,
RHS update or tolerance change. Two direct bordered 5x5 Poisson solves only.
Healthy diagnostic zero and declared gates; incompatible fixed RHS gives
U0,zeta=lambda/2,rP=2/(2+1e-14),neutrality1. Zeta absolute comparison1e-10
retained, other arithmetic comparisons inherited. Mean-removal negative uses
the already computed compatible source; no third Poisson solve.

Synthetic routing envelope has explained Green/self-energy fields, derived
constant density, equal plus/minus split, finite/shape/no-alias checks,
consistent explicitly synthetic SCBA classification, empty histories,
nonaccepted outer placeholder. Frozen explicit gate sentinel table is NOT
obtained from production limit registry. Full bad metrics produce exactly
three named messages; each isolated actual diagnostic must produce its one
named failure. Explicit spectral defect4pi-1 prevents full-science overclaim.
No call to complete scientific assessment/validation/persistence.

DEV06: checked3x2 axes, analytic Nb2 sine basis with phase-only mapping;
full basis inventory and static gates; every Green/family block phase mapped;
metadata from independently derived actual D singular values/row sums;
all shape/finite/no-alias/PSD/Keldysh checks before plain container assembly.
Resolved current compared against [19,43,67]/(8pi^2), physical-dE integration
against43/(4pi^2), boundary flux separately against the same SI literal.
Bonds compared against15t/(8pi^2), diagonal-only and checked genuine Nb1
carrier each against0, retaining the nonzero full-basis RHS distinction.
Sign/2pi/momentum-weight/energy-weight/physical-dE negative distinctions
retain original expected values. No constant-current requirement outside
this analytic two-column fixture; no truncated-charge renormalization.

## Runtime request to shared-slot root, not executed

Only after INT01 exact import/compiler-image readiness and independent
CP-CODE. Each invocation max120s /1CPU /2GiB /16MiB tmp /2MiB logs;
sequential, total calls here0, shared counters root-owned. Stop first failed
assertion/timeout/OOM/nonfinite/static/phase condition, preserve original log;
no blind retry or scientific solve.

Root cwd, prepared executable/environment with bounds enabled:

```
julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/physics/nonneutral_periodic_poisson_assessment.jl")'
julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/physics/nonzero_public_current_oracle.jl")'
```

DEV04 one no-solve static builder (max12x12 Hwin), two direct5x5 solves,
3x2x4x4 Green/family arrays; DEV06 two no-solve static builders (max9x9),
3x2x2x2 arrays and Nb1 truncation. Numeric data <1MiB each; import/JIT
cost dominates and remains unmeasured. No old nonlinear/refinement suite
included. Parent owns additional runtime source binding and finite attempts.

Read-only `git diff --check` passed tracked files; explicit new-file
trailing-whitespace scan passed. These do not establish Julia syntax/runtime.

| Утверждение | Свидетельство | Ограничение | Решение |
|---|---|---|---|
| DEV04 exact healthy-source guard реализован | frozen new test: @test + fatal error before solve | actual guard outcome not_measured | дополнительно измерить |
| DEV04 isolated Poisson gates различимы | retained RHS + full/isolated synthetic routing assertions | runtime/CP-CODE pending; routing sentinels not measurements | дополнительно измерить |
| DEV06 consistent public carrier/RHS реализован | checked builders + analytic basis/measure/SI/metadata assertions | runtime/CP-CODE pending; manufactured functional only | дополнительно измерить |
| DEV03/08 и production сохранены | original hashes unchanged; tracked diff empty | tests remain untracked until root review/Git | сохранить |
| S1 all-five acceptance получена | новых solves/measurements нет | DEV05/07 blocked, science outside scope | данных недостаточно |
