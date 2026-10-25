# OPS03 RED-2 — corrected test fixtures, execution pending

Platform source HEAD remains `6c5b11f3c74d44fed8b2c159f890b83e0b5456b9`. Accepted D/R and scope unchanged. Only two allowed test files changed; production code/Git/checkpoints untouched. Writer tests/imports/native executions: **0**. Root owns the shared attempt count: RED1 used invocation 1, RED2 is planned invocation 2 of 4; no reset from resource grant.

Read complete original `/tmp/qcl-OPS03-RED-1/original.log`: root result nine failed, wall 2.433 s, RSS 81608704 bytes, output 21088 bytes. This is **not** nine semantic RED witnesses: six stopped at the test fake rejecting the literal `timeout ... runuser ... self-check` argv; O15 stopped at valid incomplete-scope refusal. Reverse contention, legacy fence and node-lock controls separately show missing refusal in the raw log. No production release has been given.

Two narrow fixture corrections:

1. `OPS03LifecycleOwnerTests.SELF_CHECK_ARGV` allowlists exactly the full literal pinned self-check argv observed in production `solver_self_check` and RED1. Any other timeout argv still raises `AssertionError`; no real command is executed. Applied to both the main fake boundary and the crash-cut child's same boundary. Existing closed fake command kinds remain unchanged.
2. O15 keeps the original selection name for root's identical nine-test rerun, but uses **completed safe-stop scope under a still-live shutdown invocation**. A wrapper calls the real `_shutdown_owned_poll` through capture/finalize, verifies success, then waits on Event before returning to `shutdown_step`; its per-node flock is still held, while common ownership has been released. The parent verifies actual persisted `safe_to_power_off`, `capture_complete=True`, empty jobs, then invokes real new-boot startup and expects contention. No intent is fabricated/rewritten by the fixture. This is the node-lock negative control at the finite return boundary; it is **not** a new actual Runner-wait witness. The existing real Runner-wait test remains `ShutdownIntentTests.test_intent_is_durable_before_drain_and_common_lock_free_during_runner`. Full O15 node-B progress/update blocking remains a gap listed in the first report.

Root reruns the **same nine tests** selected in `/tmp/qcl-ops03-red-report.md` under the same finite shared envelope. Expected baseline now reaches real missing refusal and selected-gate env assertions instead of fake self-check rejection/incomplete scope. Actual RED2 outcome and counts: **not_measured** until root receipt. Writer will not run tests or start production code before root's semantic RED release.

`git diff --check`: clean. Frozen updated full tests-only diff `/tmp/qcl-ops03-red2.patch`. Previous RED1 logs/report/patch retained unchanged.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| RED1 failures are all semantic | Original log shows six unrecognized fake argv and incomplete-scope O15 | No universal RED claim justified | данных недостаточно |
| Fixtures now target intended semantic boundaries | Exact argv allowlist; real finalized safe-stop wait before invocation returns | Corrected tests not yet executed | дополнительно измерить |
| Production source fixed | Production files untouched | Root semantic release pending | данных недостаточно |
| Complete O01–O18/native/provisioning/admission acceptance | First report's remaining matrix and D/R residuals retained | Still required follow-on work | данных недостаточно |
