# OPS04.S Root phase2 — functional source freeze

2026-10-20. **Implemented source, not observed GREEN. STOP before separately authorized formatting and independent high CPP.** Coordinator authorized this implementation after ROOT-RED-1; this author executed no additional imports/parsers/checks/tests/Deno/Nix/builds. Only owning Root production files changed during phase2.

## Identity and preserved evidence

Root source authority `cfc38e1761f24caf436d938f378dbcdbf71a28f0`, local isolated clone `/tmp/qcl-ops04-root-worktree`, branch `codex/review-closure-depot-byte-binding`. Eight submodules remain uninitialized at selected gitlinks; no updates/network. Current integration Root advancements were not copied into this isolated source tree. Protected original `/home/tolya/Загрузки/qcl-negf` not written. Final status: modified three owning production files plus the two already frozen test files; phase2 did not change test bytes.

Design/review inputs SHA256 verified: D2 `19d56005eacf80aae3164291728530fe9b78eb9f43948f306e67c73d34c99147`, D2 independent R `12e811ec56093734fdeb7fd6aac370f312ef880c2b7a64edd9689c8bca26ec42`, named CLI seam `93ffbbcdd50770295f2f21e1a9befc47acc63231279b1ff79aebf48e7cc69a7f`, seam R `626159c6307b5664025d800f7d3d8101fb1ab55a4bd8a809f76b4aa949e653d5`, v3 narrow F1 R `ad3e2da9ffd6b84d4faec7a3e536df46c61d6365f1cd2342ec1bd1a740f22ceb`. Earlier test source/report/review artifacts were not written.

ROOT-RED-1 `/tmp/qcl-OPS04-ROOT-RED-1/receipt.json` SHA256 `3dff28530a17d48d4bb28fadffa1f8692d8f06dd935fb08acaca4329688491d3`; `original.log` SHA256 `5ab3e0c1ba7a178fd6dd60c297119cac38e86a0d39df0bfa24df7d8a88ccb943`. Receipt reports exit1, 17 failed/9 passed, suite113ms, wall1.639s, complete12460-byte raw capture, guard_error/stop_reason null. Typecheck of the two test files completed before their RED. These are coordinator receipts, not a rerun by this author. Root Deno counter1/2 remains coordinator-owned; this source phase consumed zero additional slots.

## All 17 RED failures classified against accepted requirements

Names below abbreviate the immutable full test names, preserving unique locator and source line from original RED log.

| # | Immutable test locator / RED observation | Requirement and production source repair |
| --- | --- | --- |
| 1 | solver_test:100 HTTPS exact JSON bytes; old helper threw source graph mismatch | D2 string/full-graph API, prepared JSON/SHA argv and binding observation in buildSolver |
| 2 | solver_test:116 A→B after capture; old helper source mismatch | D2 one immutable string, no late target path; same binding drives prefetch/build |
| 3 | solver_test:143 callback mutation; old helper source mismatch | D2 operative values/options copied before await/callback; frozen observation |
| 4 | solver_test:163 order/duplicates; old helper source mismatch | D2 one JSON.parse→JSON.stringify, original key/array order retained, unknown fields preserved |
| 5 | solver_test:191 command failure propagation assertion | Old API rejected before fake callback; accepted string API now dispatches validated input and propagates failure without success return |
| 6 | solver_test:233 exact65536 raw bytes; old helper source mismatch | D2 raw and produced UTF8 bounds checked separately, ≤65536 accepted |
| 7 | solver_test:256 legacy object/path assertion | D2 no object/path overload, runtime typeof string rejection before any callback |
| 8 | solver_test:331 progressing reads; missing capture function | Seam one-open stat/read/finally-close loop over bounded remaining storage |
| 9 | solver_test:346 sentinel oversize assertion | Missing reader never consumed sentinel; reader now rejects byte65537 immediately without another read |
| 10 | solver_test:355 close/error assertion | Missing reader never opened/closed; stat/read/no-progress/decode/size failure now passes finally-close, original I/O failures propagate |
| 11 | solver_test:380 real UTF8 capture; missing capture function | Actual Deno.open default, fatal decode, BOM/NUL and roundtrip rejection, regular-file stat |
| 12 | solver_test:404 solver CLI; missing function | Named runSolverBuildCli with stable dependencies, capture→owned graph→Manifest→buildSolver; real CLI build branch delegates |
| 13 | application_cd_test:102 explicit-empty password guard | T2 raw authority userinfo detects explicit colon before @ while preserving username-only and percent-encoded username colon |
| 14 | application_cd_test:206 A captured before first app callback; missing function | Named actual assembly captures and shared-preflights before .#application; same string feeds later helper |
| 15 | application_cd_test:276 valid B / dependency snapshots; missing function | Stable function references before await, structuredClone of derived graph; B used consistently, no-cache route retained |
| 16 | application_cd_test:356 graph drift assertion | Missing orchestration never reached recheck; actual named assembly retains graph recheck after path-info and before copy/writes |
| 17 | application_cd_test:389 pending collision assertion | Missing orchestration never reached writes; actual assembly retains createNew pending and rename with propagated failure |

No failure was a permission/runtime guard error. Nine RED passes do not establish a complete contract: in particular caught missing-function errors can satisfy negative zero-dispatch fixtures. Healthy missing-function and old-signature failures above are the distinguishing RED evidence. F1 wrong expected order was independently corrected before this immutable runtime packet; phase2 does not alter it.

## Implementation and caller coverage

`ops/solver.ts`:

- Named DepotInputFile/OpenDepotInput, BuildCliDependencies, readonly DepotBinding internal contracts; default opener Deno.open(read:true) and default Manifest SHA WebCrypto over actual existing julia/Manifest.toml bytes.
- captureDepotMetadata opens once, stats regular file before read, loops using remaining subarray of a65537-byte buffer, rejects no-progress/invalid counts, stops at sentinel, closes exactly once in finally. Raw NUL/BOM reject, fatal UTF8 decoder and byte roundtrip; no late file/path use. No FIFO-race/hard-blocked-I/O guarantee.
- Shared internal prepareDepotMetadata is imported only for assembly preflight and used by buildSolver. It accepts only string, independently bounds raw and produced UTF8 bytes, parses once, validates top object/depot/Julia/Manifest, graph format/root/full path→revision+URL set, duplicate/missing/extra components and string archive fields. Object key/array order is not used for matching and not canonicalized; normalization preserves unknown metadata fields. All operative strings are captured before async hashing/callbacks. Raw and consumed SHA/count differ explicitly; immutable observation returned only after successful build.
- buildSolver now has only accepted string/full-graph/Manifest signature. Existing profile/worker validation is retained and copied locally. File prefetch uses captured URL/hash/name; HTTPS retains normal fetchurl admission. Source is still git+file with exact captured root revision/submodules1. Nix receives exact bound JSON and its SHA via separate --argstr data; target pathname/realPath removed.
- runSolverBuildCli captures dependency function refs before first await, validates existing tail argv/options, performs actual capture, owns graph snapshot and measures Manifest, then calls same helper. Private solver build branch delegates; depot-generation branch retains prior behavior/guards/archive/schema/checksum.

`ops/application_cd.ts`: early shared cache guard applies to both deploymentManifest and named CLI. It checks type, existing argument guards and parsed URI, plus literal password delimiter before raw authority @; encoded colon in username is preserved. No new scheme allowlist, blanket username restriction or secret-query scanner. runApplicationCdCli keeps dependency refs/owned graph, actual capture and common full preflight before first dispatch; existing application build then same-string helper, path-info, deploymentManifest, graph recheck, optional literal cache copy and actual createNew pending/rename remain. Existing release_id digest unchanged. import.meta.main delegates to the same named function; stdout capture policy preserved. No test-only orchestration.

`nix/solver.nix`: required depotManifestJson/depotManifestSha256 strings, outer type and hashString assertions before fromJSON; no readFile/path fallback. Existing mkPreparedDepot/mkSolver/profile/worker arguments retained. Source review only: Nix assertion/parser execution remains an admitted future gate, not simulated by fake Deno dispatch.

Bounded source search across root ops/nix and two tests identifies the same two operational TS callers: private solver build branch→runSolverBuildCli→buildSolver, and application main→runApplicationCdCli→buildSolver. No DepotSpec consumers remain in ops. `nix/local-lab-packages.nix::input.depotManifest` is a separate recipe that does not call nix/solver.nix; it is unchanged and receives no new consumption claim. No Platform/DOC04/docs/schema/physics/trust-root modifications.

## Functional freeze hashes and next gate

| File | SHA256 |
| --- | --- |
| ops/solver.ts | 22b6a3cd5bb847538ea790d4f644c12763e2e9705e9b776f4b3df2227512822a |
| ops/application_cd.ts | 4062fa974dd319d28f73c7906a13704a40fcd65721b11fdd5bcdb7d3ad218ce1 |
| nix/solver.nix | dacc900b41f3e9866e3b164243385ce81fdf9df3925061573bc8731f26e71e8b |
| tests/solver_test.ts immutable | d2c5da7ad9783bbc65e5e76baef8cb43282eb4388393f8dc130172be74c8b1d5 |
| tests/application_cd_test.ts immutable | bd92a82d858ea17d1a124f2a9d257a76329f7f1630e423aad5ba1840c1982f85 |
| production-only patch.diff | c54078e4d06fea5b5d7c11f11c33a1e3f0e06e9583bdf14927583c79dfbe4488 |

The patch contains only three production files relative to cfc38e1, suitable for integration atop already-published frozen tests. Functional source was frozen **before formatting**; formatting/typecheck execution has not been performed, and current long lines/retained assembly indentation are left for separately authorized formatting as instructed. git diff --check returned exit0, whitespace only. Any formatter changes require fresh hashes/source binding before final CPP/GREEN; RED original raw hashes stay unchanged.

Envelope ≤40min/1CPU/2GiB/read≤5MiB/output≤128KiB. Cumulative CPU/RAM/read telemetry not instrumented, not represented as measured values. This phase used text/SHA/Git metadata/diff reads, three source edits and /tmp attempt artifacts. No imports/parsers/typecheck/formatter/Deno/Nix/tests/network/server/build/install/stage/commit/push/main/children/checkpoint writes. No science/C08 changes.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| All17 RED failures map to accepted D2/seam requirements | Original complete raw log/receipt and17-row table | Author performed no rerun; corrected behavior not measured yet | дополнительно измерить |
| Functional T1/T2 Root implementation frozen | Three owning source files and exact hashes/production patch | Separate formatting, high CPP and sole coordinator GREEN ahead | изменить |
| Immutable tests and RED receipts preserved | Exact original source/raw/receipt hashes | Formatted future bytes need new binding | сохранить |
| Nix/native/release/scientific acceptance established | No corresponding execution receipts | Source-only implementation gate | данных недостаточно |

**STOP: handoff to coordinator for separately authorized formatting, final high CPP, then sole remaining bounded GREEN.**
