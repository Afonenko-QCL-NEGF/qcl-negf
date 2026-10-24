# DEV03 / DEV04 — test-only correction 1, frozen

2026-10-19; Core source a8d2c0de21dfdce3ed3c7c585c555656443f6d89,
existing numerical-oracles branch. Sole TEST writer; no Julia/import/tests,
solver/build/install/network, Git mutation, tracked source or docs edit.

Reviewed source evidence: `/tmp/qcl-core-four-oracles-review.md` SHA256
6232b77a7026e81b45d42b53b032ea07680cbd0fb6e0c8203c4652d1bd99523f;
original logs `/tmp/qcl-DEV03-GREEN-1/original.log` and
`/tmp/qcl-DEV04-GREEN-1/original.log` read and retained unchanged.
Receiving-code-review skill used for evidence-first correction.

DEV03 original15pass/1fail is not converted into pass: literal matrix entries
passed; auxiliary exact `det(B)` composite failed. Replaced only two det
calls by explicit2x2 `a*d-b*c`, retaining exact expected1/10 and all entries,
PSD principal-minor/sign/negative controls. No tolerance added. All operands
and elementary products remain small Gaussian integers, so the accepted
exact arithmetic rationale now applies to the minor calculation itself.

DEV04 original ParseError occurred before assertion/Poisson. Replaced only
`κ[m]^2.*I4` with `κ[m]^2 .* I4`. ExactND fatal guard, literal Poisson RHS,
all diagnostics and synthetic routing unchanged. Read-only regex inspection
of all four fixtures found no other exponent-immediately-dot-multiplication
pattern; no speculative additional edits.

| Card | Full file SHA256 after correction | Incremental diff / SHA256 |
|---|---|---|
| DEV03 | 6adaeea85abf95e21dd0beb763dada3a73d588cae1ed5a5d536eb0e8841a2a1e | /tmp/qcl-dev03-oracle-fix1.diff / b97aab38a24987b7ea60a339da1aa659054cbb8a8fe017b95f026aaabd2a4a03 |
| DEV04 | 9aab7a4eea3a7fcb93033d2c9f6f3b420f6b1872843168e0deb98461f2602730 | /tmp/qcl-dev04-oracle-fix1.diff / 477b7a8dd9b317b290c3bced3ac6023e28e8b4984198e1d6183703f05b367a11 |
| DEV06 unchanged | 17fed2fae5b45549c65cec576cc108f68922a04e3830c0246313ccafd4ee8d01 | no diff |
| DEV08 unchanged | bae8a57957cd9df4da0d7369521a7d7ffa776b4c095859e0d1a9f86a9607eb6e | no diff; ratio-design pending separately |

Machine receipt `/tmp/qcl-core-oracles-fix1-freeze.json` contains before/after
hashes and incremental diff hashes. Original full diffs/reports remain intact.

Root owns separate DEV03-GREEN-2 and DEV04-GREEN-2 packets, each120s,
1CPU/2GiB and original aggregate counters/stop unchanged. Author calls0.
No automatic retry or success claim; preserve fresh runtime evidence.

| Утверждение | Свидетельство | Ограничение | Решение |
|---|---|---|---|
| Exact minor no longer invokes rounded LU | explicit2x2 entry formula in frozen incremental diff | revised runtime not_measured | дополнительно измерить |
| Reported DEV04 lexical ambiguity corrected | whitespace-only incremental diff at offending expression | revised parse/runtime not_measured | дополнительно измерить |
| DEV06/08 immutable and production unchanged | original file hashes retained, only03/04 new tests edited | no new full scientific evidence | сохранить |
| Scientific acceptance established | no scientific solve/measurements in correction | fixture-only evidence | данных недостаточно |
