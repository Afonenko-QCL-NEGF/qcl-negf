# DOC04/DOC06 test routing — independent high design review

2026-10-20. Reviewer Root; design author separate ultra agent. Source-only.
D SHA256 fb8ca769d5406150ecac0381d8dbe250a2515664b16417dead7f4ebba5a88270.
Primary reads: complete D; selected Root deno.json, ops/ci.ts and both workflows
at e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b. No product execution/full CI.
Finite review <=20min/1CPU/2GiB/2MiB reads/128KiB output; actual source bytes read
below128KiB. Shared architectural agreement does not establish runtime proof.

Verdict: CHANGES REQUIRED, narrow descriptor completeness corrections before I.

## R1 — exact descriptor forbids the count input required later

D section3 declares Exact fields and Additional fields refuse. There is no
expected test counts field. Section4 says the source descriptor records each
expected count, and sections6–7 require a strict bound expected/observed count
with zero skips/TODO. An implementer must either add an unapproved field,
hardcode counts without their source binding, or lose the required predicate.
Specify one exact representation: for example a fixed three-entry units map
whose expected counts are paired with each exact reviewed test path/hash, and
include it in the descriptor whitelist. Say explicitly how base status is
validated separately from dedicated engine summaries; base contains multiple
checks and is not itself one TAP/unittest count. Manufactured control should
reject mismatch, missing unit, zero, skipped and unknown format. No need to
add/modify any existing scientific or docs assertions for this correction.

## R2 — optional child loader environment has no admitted input representation

Section4 permits measured indispensable native-loader fields admitted for the
executable, section6 records scoped environment names, while the exact fields
in section3 only provide tool path/version/hash/receipt_ref. No environment
allowlist/names/value binding is defined. This leaves I to invent permission
and secret-filtering semantics. Freeze either an exactly empty loader-env map
for the selected tools (explicitly block if a fresh host needs extra fields),
or a finite exact admitted allowlist and byte/digest binding. Never inherit
ambient NODE_OPTIONS/PYTHONPATH/PYTHONHOME/DENO_* or arbitrary descriptor env.
State Python child clearEnv semantics as precisely as Node and DOC06. Do not
claim a version was measured by preflight if its read/write/run=git permission
only permits checking retained tool identity receipts and bytes.

## Preserved decisions

Two exact discovery exclusions with mandatory dedicated group are appropriate;
future unrelated mjs is not excluded. Default/all cannot pass without docs.
ops/ci full invokes aggregate once, scoped modes retain prior meaning; workflow
preflight precedes heavy setup. No download or native readiness is implied.
Admitted process-tree/storage supervision remains an external mandatory gate;
this helper must not turn sampled or absent resource data into hard enforcement.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Existing Root generic route is incomplete/incompatible | deno.json check + D pinned discovery + Node fixture input contract | Source fact; no full check run | изменить |
| Proposed routing can preserve coverage/least capabilities | D sections2/4/5 | Descriptor R1/R2 incomplete | изменить |
| Source design proves native/full CI readiness | No native admission and no final execution | Independent gates pending | данных недостаточно |
