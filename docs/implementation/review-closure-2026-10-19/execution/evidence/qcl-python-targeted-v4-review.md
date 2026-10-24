# Targeted Python harness v4 — narrow final review

**Verdict: scoped READY** for coordinator-owned selected OPS03 Python packet, with its finite budget/source binding. R1/R2 and safe-ID confinement conditions addressed. Reviewer did not execute harness/helper/target imports/tests/probes; only source/delta/hash and Python AST parsing.

Frozen v4 SHA256 `60f1e75cad84047e6a9322dab4d2531ca50713bac4893956bd6d9c68a654c38d`. Preserved v2 `9726bc355f0fd762cc382c69c23940112b0bf19659045dc49214c5fa44d6df8b`, v3 `f7648e421dee87ddae0a3fe6672d0744accac26ecb38e62aa2ee991adccb9be4`; accepted RawCapture helper `e88ca841c6d03fe74e82b83f0a46fff82f4f7c2cac3b0da721ce0d8395c2be3f` unchanged. All hashes independently verified. v4 AST parses without execution.

R1: Popen/collector/monitor exceptions now retain guard_error/guard-error.txt and failure reason. Unified finally stops own active process group, drains existing collector; when construction left captureNone, communicate fallback drains the pipe into the exclusive raw file. v4 uses memoryview write-all loop, counts actual progress, rejects zero/no progress, and advances until every returned byte is stored. CompleteTrue is assigned only after that loop; errors remain completeFalse/capture_error. Stream is closed on fallback/no-child paths. Original guard exception is not overwritten by success of drain. This closes v2 None.finish/raw-loss path and v3 short-write false-completion gap.

R2: exact post-drain captured_bytes>2MiB sets output_envelope_overrun and failure reason. Final return requires real child exit0, no stop/guard/capture error, complete capture and no overrun. Fast output burst that evades50ms early monitor therefore cannot PASS. Every original byte is retained, not truncated; planning threshold1.875MiB is separate from final2MiB envelope.

Task regex restricts known card prefixes+two digits; attempt regex admits only a bounded ASCII basename. Derived /tmp/qcl-TASK-ATTEMPT cannot contain slash/dot traversal. Exclusive attempt mkdir/log create prevents existing-folder adoption. Fixture realpaths remain confined below selected root/components; pytest :: suffix is excluded only for source-file hash resolution. Runtime fixed selected .venv Python, cleaned loader env, no install command.

TMPDIR and pytest basetemp point to owned temporary directory. Standard tempfile data routes there; explicit paths elsewhere remain unmeasured. RSS and temporary bytes sampled every50ms,1GiB/16MiB are monitored rather than hard quotas/transient peak proof;90s wall and per-process CPU/1CPU affinity retained. Raw output has exact final accounting. Harness/fixture hashes recorded at receipt time do not themselves replace coordinator freeze/before-after source checks. No generic hard process-tree termination/native/offline guarantee added.

Legacy receipts remain unchanged: former basetemp-only zero did not measure all temporary data; v4 does not retroactively certify them. Root must retain harness actual exit, receipt+original raw hashes and exclusive attempt identity. No new test attempt is implied by this review; future runs consume the previously assigned shared envelope, no automatic rerun.

| Claim | Evidence | Limitation | Decision |
| --- | --- | --- | --- |
| Collector-construction failure preserves raw or explicit capture failure | communicate +write-all +guard diagnostic +streamclose | unrecoverable storage/capture error cannot pass | сохранить |
| Output envelope overrun cannot pass | exact post-drain check +final predicate | allbytes retained, overrun remains failure | сохранить |
| Attempt/source paths confined | safeID regex/exclusivemkdir/fixture realpath | coordinator trusted selected files and sourcefreeze | сохранить |
| Future OPS03 packet can use v4 | scoped source/AST review, exactSHA | runtime not measured; root budget/slot remains required | сохранить |
| Legacy/native/fullCI/scientific acceptance established | no corresponding evidence | harness readiness is not test outcome | данных недостаточно |
