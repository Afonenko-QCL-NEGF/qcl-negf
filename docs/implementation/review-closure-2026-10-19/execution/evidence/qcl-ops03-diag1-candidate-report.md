# OPS03 diagnostic candidate — confirmed fixture repair, R1 not diagnosed

Read and verified independent CHANGES_REQUESTED `/tmp/qcl-ops03-code-review.md` SHA256 `6955b4cc506655fd887d08629faebfc0c1c9a1e2fdab972dda27a075c0914717`, raw GREEN1 failure material and affected source. Applied receiving-code-review/systematic-debugging: confirmed fixture causes were corrected individually; healthy whole-update cause was not guessed or changed in production.

Root GREEN1 remains original evidence: 198 passed / 36 failed methods, wall53.093s, raw69551 B complete, no guard termination. This is not a claim of 36 unique product bugs. Original files under `/tmp/qcl-OPS03-GREEN-1` were not changed. Writer runtime/import/test/build/native/SSH/service/Git mutations: **0**.

Owning baseline Platform `6c5b11f3c74d44fed8b2c159f890b83e0b5456b9`. Only `tests/test_application_release.py` changed relative to frozen candidate2. In particular production runtime ownership/modes, owner/B validators, gate/terminal handling and O01–O18/LI policies were not edited. `git diff --check` clean. Full baseline-relative frozen patch `/tmp/qcl-ops03-diag1-candidate.patch`.

## Source-confirmed corrections

- **R2:** F5 initial exhaustion and sentinel now use `UpdateScan.CAP-16` / `UpdateScan.CAP`, and R4 cap_manifest uses `UpdateScan.CAP-16`. The independent no-actual-access assertions remain. Production CAP=64 MiB is unchanged; no limit reduction or sentinel deletion.
- **R3:** The root_squash fixture's fake geteuid=0 now has matching fake root ownership only for the controlled runtime directory and its two lock-file dev/inode identities. stat/fstat retain native inode/mode/nlink and actual real flock operations; unrelated objects retain native metadata. Gate reads still require synthetic UID/GID3000 and credentials restore to UID0/GID42. At least four gate reads must be reached (node-check, guard and both owned-preparation reads). No production permission/mode policy changed; withdrawn installed-0755 concern was not revived as a product fix.
- **R4:** Each malformed remote-identity subcase receives its own runtime/gate. Partial failed direct deliver_pool retains its original intent bytes and matching closed gate; a same-runtime attempted retry explicitly must refuse before callbacks. A separate fresh runtime/gate may establish a healthy independent operation, while old blocker bytes remain untouched. No clearing/adoption/force-pass of a pending unknown attempt. Existing known CR04 retry/provenance tests were not mechanically changed into blanket refusal; their healthy route remains part of R1.
- **R5:** Cache/hash fixture calls now pass the same selected gate used by their fake command/readback boundary, with fresh explicit runtimes; silent publisher redirection was removed. The malformed remote-check fault explicitly targets the real remote worker in a complete three-node fixture, records exactly one reached injection, requires controller verified / selected worker failed / later second node not_attempted, and prohibits later copy/activate/finish/RESUME after the injection. It still fails if the intended fault is never reached; no arbitrary failed report is accepted as success. Final-publication/open/close/terminal safeguards were not removed or weakened.

## R1 evidence improvement only

`delivery_diagnostic(report, runtime, calls)` is a test-only assertion message helper. It emits bounded status/open/phase/node, per-node status/reason, a selected-runtime-only receipt's phase/pending fields and last command names. Reads at most 65537 bytes from the explicitly reported receipt, refuses >64 KiB as diagnostic-too-large, prints at most 6000 characters; no source validator is called as an oracle. Diagnostics cannot replace a semantic assertion.

Messages were attached to the actual healthy whole/local O03 status/open assertions, old healthy controller-prefetch open assertion and representative I14 healthy assertions. Existing expected completed/open, real helper/publisher/flock/no-self-SSH/envelope requirements remain unchanged. Cause of R1 remains **unknown** pending root DIAG1; no product repair or guess was applied.

Suggested exact root DIAG1 selection (one process, not executed by writer):

```text
tests/test_application_release.py::OPS03WholeRoutingTests::test_o03_whole_update_calls_real_local_helper_without_self_ssh_or_reacquire
tests/test_application_release.py::ApplicationReleaseTests::test_controller_fetches_and_checks_both_hashes_before_closing_admission
tests/test_application_release.py::I14WholeRepairTests::test_f6_positive_factory_full_body_transition
```

The old healthy selected-gate fixture is corrected before this diagnostic so it observes the same selected path as its real local helper. If any healthy control still fails, its unchanged assertion now includes actual report/node reason/receipt phase rather than an assertion-only False.

## Immutable source identities and budget

| File | Current SHA256 | Relative to candidate2 |
| --- | --- | --- |
| `ops/application_release.py` | `08f67097705f86d2ca842ae373306cb8945f47564c4d2ceb5e00e8272f31831f` | unchanged |
| `ops/worker_lifecycle.py` | `b81c722ce9cbca8a5adfed24063de268e39ea0d012ae120bb11d9491ba2a0678` | unchanged |
| `tests/test_application_release.py` | `f56062eef912a7c63ab9743a24f1db8a5043c2e24620db0732ab516485c0ce21` | diagnostic/fixture edits above |
| `tests/test_worker_lifecycle.py` | `7d8fd49aac1b3eb4527ef185e9bf3a2cfcd7a3265e92a447954ae4e2bef15a2b` | unchanged |
| `tests/test_worker_shutdown_intent.py` | `53017ecb166b5624dab6fe3d2b57498bdbf37882a83a9be0c9c7668fdc95bfa3` | unchanged |

Three historical root invocations consumed: RED1, RED2, GREEN1. Next root diagnostic is call **4**, <=90s/1CPU/1GiB/16MiB TMPDIR/2MiB logs through the accepted complete raw-capture harness. Latest human resource grant supports one later final GREEN call **5**, only after diagnosed cause and concrete coordinator checkpoint extension. The original four-call history is not reset. This writer stops without execution and does not initiate a rerun/retry/cancellation.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R2–R5 confirmed fixture issues corrected in source | Specific tests and preserved negative assertions above | No corrected candidate execution yet | дополнительно измерить |
| Healthy whole/local R1 root cause established | Not present in original assertion-only output | Needs one root DIAG1 with added bounded messages | данных недостаточно |
| Product ownership/permissions loosened to obtain green | Production hashes unchanged | No product repair made | сохранить |
| GREEN/CP-CODE accepted | Prior GREEN1 failed, no new receipt | Independent CHANGES_REQUESTED remains open | данных недостаточно |
| Native/OS/provisioning/CR04 atomic admission/scientific acceptance | No relevant receipts, required residuals retained | Separate gates remain open | данных недостаточно |
