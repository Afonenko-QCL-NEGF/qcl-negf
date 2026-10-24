# OPS03 RED packet — tests only, execution not measured

Source: Platform HEAD `6c5b11f3c74d44fed8b2c159f890b83e0b5456b9`, initially clean. Root observed `cbb24a61344a947761b6c049a6bb6687e14cff04`; unrelated root/other component edits retained.
Accepted D SHA256 `26374bcfb194aa5c9701bd00ceaae6016cd535dcc722e8b221719fec72450030`; independent R SHA256 `3d5f3c7e33f8c9f1e8a863c73fdefab4969c3af85c737415e294ac366a17a54a`; rechecked from files.

Edits: only `tests/test_application_release.py` and `tests/test_worker_shutdown_intent.py`. Production ops, docs, Nix/modules/bootstrap, Git indexes/checkpoints untouched. Tests/imports/builds/native/server/SSH/services executed by writer: **0**. `git diff --check`: clean. Patch frozen `/tmp/qcl-ops03-red.patch`.

New class `OPS03LifecycleOwnerTests`: real file publishers/profile symlinks and real `flock`, explicitly allowlisted fake external command kinds; fork controls use Pipe/Event handshake, watchdog <=5s, kill+join cleanup. Root must inspect test results before semantic RED release; missing-API assertions/signature errors alone are not semantic RED.

Suggested root-owned semantic selection, one invocation under shared finite L envelope (1 CPU/2 GiB/60s/1MiB):

```sh
PYTHONPATH=tests python3 -m unittest \
 test_application_release.OPS03LifecycleOwnerTests.test_o01_actual_update_process_blocks_public_activate_and_prepare \
 test_application_release.OPS03LifecycleOwnerTests.test_o01_reverse_public_activate_process_blocks_actual_update \
 test_application_release.OPS03LifecycleOwnerTests.test_o07_expiry_after_command_stops_next_persistent_mutation \
 test_application_release.OPS03LifecycleOwnerTests.test_o10_foreign_or_orphan_barriers_prevent_direct_api_mutation \
 test_application_release.OPS03LifecycleOwnerTests.test_o11_legacy_activation_fence_blocks_update_without_truncation \
 test_application_release.OPS03LifecycleOwnerTests.test_o14_public_activate_requires_matching_closed_selected_gate \
 test_application_release.OPS03LifecycleOwnerTests.test_o18_service_environment_uses_selected_gate \
 test_worker_shutdown_intent.ShutdownIntentTests.test_ops03_o15_same_node_startup_contends_during_runner_wait \
 test_worker_shutdown_intent.ShutdownIntentTests.test_ops03_o16_startup_node_lock_released_after_failed_preflight
```

Expected distinguishing behavior on baseline: missing refusal in public activate/prepare and reverse update; no deadline progression guard for standalone; direct activation ignores durable blockers/selected gate; update ignores legacy activation fence; global GATE written into selected service.env; startup has no same-node lock. Assertions are on refusal or persisted effects. Actual failure counts/outcome **not_measured**.

## Finite denominator and remaining tests

| ID | New control / existing locator | Remaining before complete O01–O18 evidence |
| --- | --- | --- |
| O01/O02 | Two actual public entrypoints in separate fork processes, reverse order | Controller-specific CLI path and independent complete mutation snapshot ledger |
| O03 | Real `_activate_owned` under whole_update capability; flock acquisition count, real temp env/profile/ready | Actual whole-update callback routing/envelopes and parent pending journal proof; direct helper positive alone is insufficient |
| O04 | Arbitrary object/dict/object.__new__, copy/deepcopy rejection | Pickle transport and constructor controls |
| O05 | Runtime/release/operation/deadline mismatch, stale context, replaced lock inode | Closed fd and replaced runtime directory; baseline missing API is not semantic red |
| O06 | Fork token rejected; child exit cannot unlock parent | Owner-parent exit plus orphan journal explicitly combined |
| O07 | Expiry after closure command blocks next mutation/units and retains intent | Each post-profile/registration/allowlist/ready/unlink boundary |
| O08 | 9 finite process kill cuts: first command, app, solver, registration, allowlist, env, ready:false, unit start, ready:true; retained marker + retry blocked | Original snapshots/receipt validation, before local terminal publication, whole-update pending cuts |
| O09 | Intent file fsync failure before command/profile mutation; existing gate failure fixture `test_review_gate_open_fsync_and_terminal_receipt_failure_keep_blocker` | Intent write/replace/dir fsync and ready/terminal file+dir matrices |
| O10 | Orphan lifecycle/admission/running-pending and cluster marker refuse direct activate; raw bytes retained | Foreign exact-lookalike same-attempt inode/schema controls |
| O11 | Actual legacy activation flock blocks update, bytes retained, delivery lock released | Separate legacy delivery contention is exercised by actual delivery owner in O01 |
| O12 | Both independently damaged GC roots, one setter and closed gate | Controller immutable Code UUID and orphan retry combination |
| O13 | Existing cold/exact/missing gate tests `test_initial_*` | Adapt to new owner API; preserve byte assertions |
| O14 | Selected gate direct API; existing enrollment authority tests | Local routing identity forgery/mismatch controls |
| O15 | Separate-process shutdown Runner wait blocks same-node startup | Node B progress + update/activate refusal while A waits |
| O16 | Node-lock bytes retained/released; existing orphan/vanished/terminal-after-RESUME tests | Audit all against new wrappers/owner deadline |
| O17 | Existing effective mask marker/foreign/inode tests | Finite worker local stop/activate/finish attempt contention process test |
| O18 | Selected gate in real env; stale owner refusal | Controlled expired/no-owner gate/cleanup helpers; concrete call-site audit |

This is the **first regression packet**, not complete O01–O18 acceptance. Remaining controls must be completed before CP-CODE; no test budget was spent by writer and no production fix has started. Await root semantic RED release or test repair findings.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Только regression tests изменены | Frozen diff, diff --check | Tests0, no semantic RED observed by writer | сохранить |
| Baseline public writers use incompatible lock/guard routes | `application_release.py::activate/deliver_cli/main`, `worker_lifecycle.py::startup`; controls above | Root execution pending | изменить |
| OPS03 complete / O01–O18 proven | Remaining matrix explicitly lists gaps | Not yet complete, no run receipt | данных недостаточно |
| Universal provisioning/OS writer closure and atomic effective admission commit | Accepted D/R residuals | Separate required follow-on, no waiver | данных недостаточно |
| Scientific/native acceptance | No native/scientific receipts | No execution authorized to writer | данных недостаточно |
