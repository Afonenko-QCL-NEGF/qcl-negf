# DEV13 GREEN-3 — narrow queued lease close correction

Base Portal `fa80b5b5920dc16dfb911d164939b3d23e6be186`.
Independent GREEN2 review SHA256
`96ccd6d0368cf8e078cd2589615b1a257d60090eabcaee241e9719d8cac3abc4`.
Root semantic RED3:2failed(read/seek), exact KeyError versus ordinary local
closed-reader ValueError. Raw/receipt `/tmp/qcl-DEV13-RED-3` retained,
wall3.027s/RSS56143872/log10230B/stopnone. Root explicit production release
followed semantic RED. No project imports/tests/build/Git mutations by author.

## R4 correction and interleaving

Only `service.py::_release` changes after RED3. Under existing metadata Condition,
reader release marks closing and atomically removes all still-queued messages
for this exact lease. It marks them expired, sets the existing local ValueError
closed-reader refusal and uses existing `_expire_lease` to clear unstarted
outstanding state. The reserved close/exit remains owner-only. It releases the
metadata lock before signaling each response Future, then reacquires it only
for the existing bounded cleanup wait.

If owner dispatch acquired the same lock first, no message is queued to revoke;
its outstanding running read/seek remains owned until actual backend return,
as R2 requires. If close wins first, the message is absent from the mailbox
before owner priority cleanup can exit/pop the lease. Hence neither ordinary
backend dispatch nor queued deadline expiry can later index a removed lease.
The unrelated running operation and other leases are untouched.

No missing-lease `.get` fallback, KeyError suppression, unsafe forced unload,
registry deletion retry, new exception code/API or thread/supervisor was added.
Existing typed ValueError is used for this local closed-reader refusal. Actor
readiness/ownership and once-only cleanup remain the accepted lifecycle.

## Exact frozen packets

Full CODE/TEST `/tmp/qcl-dev13-green3.diff` SHA256
`c0675261cee2db5328bf1d95b7849d917c7643e0b22eb2b674bd390e18676336`.
Incremental production R4 `/tmp/qcl-dev13-r4-fix.diff` SHA256
`7e133368d558e2cbb7da93efb17118ddaeadfe717643483671a70c63a463dc63`.
Source service SHA256
`b4dd4da7da85bdfca7993da3928dcf720f78e4f3ca8e70e27a2df36b79d01ef3`.
RED3 fixture unchanged SHA256
`3eeb041b5d673e5e3fbdc5d48cbc094c91874a9fc2610a3b24022c62011b1f37`.
Other source hashes unchanged:
api`d324a9188d8b4f0b3a8bea5de38a0aa3891949a8f0b924c12790711496ea5e63`;
exports`1116d3717b8cafdd51278a60b0eff5887d49e66609a5086ade535848250351a8`;
settings`fc8986ec7d06a25b261517d458162438eba9096a6f2f1d8d3f04f71b10c3897c`.

Source-only Ruff service/newactorfixture PASS, gitdiffcheckPASS. These are source
checks, not project imports/test invocations. Scoped inherited api E501 findings
remain as previously reported; no broader lint pass claimed.
Root GREEN3 requested exact five files: actor_deadlines/service/stream_disconnect/
exports/api. Root finite packet6 ceiling90s/1CPU/1GiB, overall6/540s. Until root
runtime receipt and independent re-review, no GREEN/CP-CODE acceptance is claimed.
All prior R1–R3 regressions, RED3 read/seek cells, corrected stalled ASGI2cells,
original finite ASGI4cells and all existing assertions remain unchanged.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R4 reproduced before fix | Root semantic RED3 exact2 failures | Synthetic owner/handles | сохранить |
| Queued-close lifecycle source gap corrected | Atomic queued cancellation before lease cleanup; narrow diff/hash | Runtime GREEN3/re-review pending | дополнительно измерить |
| Running backend completion/count semantics preserved | Dispatch and close share lock; running absent from cancelled queue | Actual backend responsiveness unknown | сохранить |
| Full software/native/scientific acceptance achieved | Current receipt отсутствует | Эта карточка не запускает native/solver/fullCI | данных недостаточно |
