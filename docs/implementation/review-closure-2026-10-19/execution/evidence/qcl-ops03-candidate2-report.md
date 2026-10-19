# OPS03 candidate 2 — accepted local identity B, execution pending

Owning baseline remains Platform HEAD `6c5b11f3c74d44fed8b2c159f890b83e0b5456b9`. Root is sole Git mutator/executor. No application imports/tests/build/native/SSH/services or Git mutations were performed by this writer.

Exact released narrow D `/tmp/qcl-ops03-local-identity-design.md` SHA256 `c673a2b11df3be0096388b0280cc4714271be90c9dc11e11c409a59b25f4bfee`; independent PASS `/tmp/qcl-ops03-local-identity-design-review.md` SHA256 `81686033b646c4967d9af9e938cf1b808e195bcf3e642dcd081382084af91531`. Both read and hashes rechecked. Root explicitly released B implementation; this resolves the prior D question only within the named trusted-direct boundary.

## Frozen material

- Full baseline-relative source/control patch `/tmp/qcl-ops03-candidate2.patch`, SHA256 `3481c9cdf4e5910845a1e79169eb0749dd525fd03256f8aaf2dd6630c2dde648`.
- Intended delta review `/tmp/qcl-ops03-candidate2-intended.diff`, SHA256 `bffdb486c8d0a8801c22cf73560cf9d9eee2afeaa49b4a9cccb0cd9a055a92ef`. This is explicitly a **diff of frozen candidate1 and candidate2 patches**, not a directly applicable source patch. It shows the narrow change while keeping candidate1 archived; the full candidate2 patch above is directly reviewable against the owning baseline.
- `git diff --check`: clean. No candidate execution or CP-CODE acceptance is inferred from that static check.

| Current selected file | SHA256 |
| --- | --- |
| `ops/application_release.py` | `08f67097705f86d2ca842ae373306cb8945f47564c4d2ceb5e00e8272f31831f` |
| `ops/worker_lifecycle.py` | `b81c722ce9cbca8a5adfed24063de268e39ea0d012ae120bb11d9491ba2a0678` |
| `tests/test_application_release.py` | `1ad1908d49a396299739819a3d8c25da5272626be0fe19702906b459e5c06025` |
| `tests/test_worker_lifecycle.py` | `7d8fd49aac1b3eb4527ef185e9bf3a2cfcd7a3265e92a447954ae4e2bef15a2b` |
| `tests/test_worker_shutdown_intent.py` | `53017ecb166b5624dab6fe3d2b57498bdbf37882a83a9be0c9c7668fdc95bfa3` |

Only application ops and its test file changed relative to frozen candidate1. Worker ops, worker lifecycle tests and shutdown intent tests retain the exact candidate1 bytes. Full candidate1 OPS03 owner/journal/routing/control report remains `/tmp/qcl-ops03-candidate1-report.md`; its former identity-policy blocker is now replaced by the exact accepted B ruling, not silently waived.

## Exact narrow implementation

`_bind_activation_identity(owner, *, role, expected_node_identity)` is the one added private seam. It validates one of the two roles, normalizes/copies full flat identity into a protected `MappingProxyType` snapshot, checks same declared role and actual captured process boot, and stores `(role, full snapshot or None)` once in private registry. Exact-repeat binding is allowed; role/identity/full↔None rebinding is rejected. Whole-update cannot bind None. Worker update with an attempt locator requires full expected identity before journal entry.

`_activate_owned` uses this binding immediately after owner/runtime/operation/manifest validation. Provided ordinary identity runs the existing `assert_expected_node` before journal/application mutation. Stopped worker update runs existing stopped observation and binding first, then creates the journal, then removes its validated own mask. No running-daemon observer is inserted before stopped-mask removal. Final existing assertions and the process-only binder/owner recheck use the protected copied snapshot before ready:true. Mutating the original caller dict cannot change later expected checks or publication.

Public signature remains unchanged. Trusted direct None does not invoke a full observer or invent `node_identity`; PID/start/boot, runtime/inodes, gate, unknown journal guards, finite deadline and process ownership are still required. CLI omitted identity retains protected `settings.role == args.role` plus process ownership, **not full node assertion**. Explicit whole/update/startup callers still require full binding. The binder does not provide native target authority or CP-OPS readiness and no new native None invocation is admitted by source pass.

Existing full-node fake seams now bind synthetic observed boot consistently to the fake process-generation boot. Actual PID/start-generation portions still come from the real local generation reader. Controller contexts use controller boot; isolated worker contexts use their worker boot and real existing isolated observer. Negative mismatches are asserted rather than ignored. The positive whole helper O03 now supplies explicit controller full identity, preserving its real helper, publishers, acquisition count and no-self-SSH assertions.

## LI01–LI10 controls

All controls are present in selected `tests/test_application_release.py`, with real binder and existing validators in positive paths. No new public test switch, observer argument, CLI flag, dependency or command execution is introduced.

| ID | Exact test method / denominator | Expected discriminating assertion | Outcome |
| --- | --- | --- | --- |
| LI01 | `OPS03LocalIdentityTests.test_li01_trusted_none_roles_complete_without_full_observer_or_invented_identity` — worker/controller | Real activation succeeds under owner/gate/journal; full observer must not run; no invented node identity | not_measured |
| LI02 | `test_li02_invalid_role_and_worker_update_none_refuse_before_journal` | Invalid role and update None reject before intent/profile/Code/env/ready/mask changes; original bytes retained | not_measured |
| LI03 | `test_li03_schema_role_and_process_boot_mismatch_refuse_before_journal` — schema/role/boot cases | ValueError before observer/journal; no process-only fallback | not_measured |
| LI04 | `test_li04_provided_expected_never_falls_back_after_bad_actual_observation` — machine/role/boot cases | Existing pre-observation validator rejects before journal/application mutation | not_measured |
| LI05a | `test_li05_actual_final_drift_blocks_ready_and_retains_journal` | Actual final drift leaves ready:false + intent, no successful cleanup | not_measured |
| LI05b | `test_li05_mutating_caller_dict_cannot_change_pinned_identity` | Original caller dict mutation does not change immutable pinned full identity or published record | not_measured |
| LI06 | `test_li06_whole_update_cannot_downgrade_to_process_only` | PermissionError before intent/application mutation | not_measured |
| LI07 | `test_li07_binding_once_forbids_full_none_role_and_identity_rebind` — four rebind cases + exact repeat | Full→None, None→full, role/identity changes reject in actual owned helper before journal; exact repeat and immutable snapshot verified | not_measured |
| LI08 | `test_li08_cli_none_cannot_bypass_protected_role` | CLI None with protected role mismatch rejects before application mutation/native command | not_measured |
| LI09 | `OPS03StoppedIdentityTests.test_li09_stopped_proof_precedes_mask_removal_and_running_observer_waits_for_restart` | Real stopped marker/effective mask body accepted, no premature running probe, post-restart full checks required | not_measured |
| LI10 | `test_li10_none_cannot_bypass_changed_process_generation` + candidate1 actual O01–O18 controls | Changed process generation rejects even in None mode; existing runtime/release/inode/deadline/foreign intent/open-gate controls remain required | not_measured |

These are 11 new test methods with finite literal subcases; LI05 remains two separate controls. LI10 composes the existing concrete O-controls rather than replacing them with a pass label. No claim about actual passing counts is made before root execution.

## Execution gate and preserved limits

Root-owned RED1 and semantic RED2 remain consumed attempts 1 and 2. Next allowed root GREEN1 is all three selected test files in one process, count **3 of 4**, <=90 s / 1 CPU / 1 GiB / 16 MiB TMPDIR / 2 MiB raw logs, through the accepted v4 RawCapture/write-all/TMPDIR harness. No counters were reset. Writer stops at this frozen packet; no test, import, automatic rerun, cancellation or retry was initiated. Unknown outcomes remain unknown until root diagnosis/reconciliation.

No source scope or operational permission expanded: provisioning/OS/systemd writer closure remains `OPS03-FOLLOWON-PROVISIONING`; prepare-initial protected-role gap is unchanged and named by D/R; CR04 atomic effective job-admission commit/read remains unresolved. Engineering source acceptance cannot establish native/source/G1/CP-OPS/scientific gates by implication, and a source/G1 pass does not authorize a new production trusted-direct None route.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Narrow B identity boundary defined | Exact accepted D/R hashes and root release | Trusted direct/process-only; not full node/target authority | сохранить |
| Binder/ordering/LI controls implemented | Frozen candidate2 source + exact test locators | No candidate execution/review receipt yet | дополнительно измерить |
| O01–O18 contracts retained | Candidate1 report and unchanged worker files; explicit full O03 fixture update | Full selected GREEN still pending | дополнительно измерить |
| GREEN / CP-CODE achieved | No GREEN receipt | Root sole executor, next shared attempt 3/4 | данных недостаточно |
| Native/provisioning/atomic admission/scientific/full release accepted | No relevant native/scientific receipts; named residuals retained | Separate required gates and operational bindings | данных недостаточно |
