# Docs test routing D2 — independent high review

PASS_DESIGN for frozen D1+precise D2 overrides, source-only.
D1 fb8ca769d5406150ecac0381d8dbe250a2515664b16417dead7f4ebba5a88270;
D2 bbb8cbeb4845a9a7b9514010f5c988beeac66080246d9fca1d6c12ee8a81cf70;
prior R 9e16ff7519453db4661833455450da9d83c72b5f76c9eefd4fb27370da812930.
Root reviewer high; separate ultra design author. Review reads D1, D2 complete,
prior R, e22 deno.json/ops/ci.ts/workflows and source-level child launch contract.
No runtime/parser/import/tests/build/network/full CI or product changes.
Finite review <=15min/1CPU/2GiB/2MiB reads/96KiB output, named source bytes<128KiB;
physical I/O and RSS not instrumented.

R1 closed: D2§2 exact units whitelist contains three fixed test path/hash/count/
report-format bindings, rejects extras/duplicates and count coercion. Expected
counts cannot come from observed output. Missing final DOC06 binding blocks.
D2§3 distinguishes composite passed_base from dedicated passed_unit; no fake
base TAP aggregate and no missing unit promoted from not_measured to pass.

R2 closed: D2§4 exact empty loader_env plus clearEnv maps for every dedicated
child. Python disables user-site and bytecode output with fixed literals;
Node gets only KaTeX/TMPDIR, DOC06 only explicit CLI cache. Base alone retains
existing environment, explicitly bounded to base scope. Unsupported loader
requirements block rather than inherit injection fields. D2§5 versions are
retained-receipt-bound, not freshly measured by read-only preflight.

D1 routing obligations remain: exactly two discovery exceptions; full/default
requires all4 steps once; docs-only and smoke are separately scoped; workflows
preflight before heavy preparation and full ops/ci aggregate once. No helper
recursion or new global permissions for generic suite. No default count/version,
automatic package fetch, retry or fallback is allowed. Exact sourceGraph and
consumed source byte binding are still required; metadata refs do not establish
native trust/ownership by themselves. External process-tree/storage admission
and supervisor evidence remain mandatory and cannot be replaced by direct-child
kill, sampled metrics or an arbitrary JSON status. The implementation must leave
those predicates unknown/blocked unless provided by the trusted active harness.

Meaningful fake-executor/report controls are specified; no existing DOC04/DOC06
unit assertions need modification. Actual new focused route test first must be
independently reviewed and run under a finite DEV envelope; it cannot invoke
real base/full suites or tool probes. Base tool identities/cache compatibility
and final descriptor are not currently asserted ready. Final full CI remains0.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1/R2 make contract implementable without invented inputs | Exact D2§2–§5 source binding and status/env distinctions | Source review only | сохранить |
| Routing I may proceed on frozen contract | D1+D2 and independent R | CPP + finite fake controls precede real CI | изменить |
| Native/CI readiness is established | No admitted final descriptor/execution | Required independent gates remain | данных недостаточно |
