# SCI08-R1 I1 — независимый аудит GREEN1 и G1 eligibility

**Вердикт: PASS_BOUNDED_RUNTIME_EVIDENCE; CP-CODE узкого SCI08-R1 пригоден для owning draft и условного G1 source publication.** Блокирующих расхождений в сохранённых GREEN1 свидетельствах не обнаружено. Это завершённый fake-only unit selection на exact I1, не actual campaign, full native CI, release или scientific acceptance. G1 не объявлен выполненным, публикация этим review не производится.

Read-only evidence audit; применение qcl-results-analysis не расширяет scope. Runtime/parser/compiler/import/tests/Julia/Pkg/network/build/native calls этого review=0; повторных checks/RED/GREEN нет. Source/index/Root CP/Git writes=0. Записаны только два requested /tmp review artifacts. Достаточно сохранённых text receipts/raw и прежнего independent C/P/P: распаковка, scientific arrays и новое выполнение не нужны.

## Привязка evidence

| Артефакт | Bytes / SHA256 |
| --- | --- |
| GREEN1 receipt `/tmp/qcl-SCI08-R1-ENG-GREEN-1/receipt.json` |69829 / `5d54f61aca6db32adef3cd6dda2da94cede325dbecf4320548d1f8d1954896a6` |
| GREEN1 complete raw `original.log` |2942 / `351970830a9fc01123a5e91759565d411bed58a4ac85516d27ab7b23f1035a02` |
| Root GREEN1 READY `/tmp/qcl-sci08-R1-GREEN1-ready-v3.json` |32150 / `6fbbac46c8431d53df02e23e0e35346ee04a73da6e5175285330df36a972be80` |
| Independent C/P/P |`00c798cf1fdfe0cd14b245cbab997567a7e7628c25957789fded840fb9bdf6d1` |
| Independent C/P/P identity |`b10f208967bcef20bb9cee78454bef5921a3092fb83a88bed6b704025d5be479` |
| Approved actual O1/O2 source traces |`3cbf2efa4de706f7b4bae9b9fc1a27445881c760fb413a656a8f7fb5f1f7dea7` |
| Frozen production patch |`7c5d0a56dfc56081aa3a3e78e91adae936130482167614dec4867779b520c9e6` |
| Accepted engineering plan v3 |`c48d28709fb75a66652d8ca7d884e55a1158c7e9e950b5e8aa0861525db3c13e` |
| Harness v3 as recorded in GREEN1 executable_before |`f239938d9fe83e60f1623ee501f4cd32e5d77fa071f931d237cd13973a123528` |

Receipt:2–8 identifies single consumed `SCI08-R1-ENG-GREEN-1`, phase GREEN, operation `SCI08-R1-ENG-GREEN-1-v3-Root-c5ef91f-once`, verdict BOUNDED_GREEN, target_calls1, stop_reason null. Receipt:183–195 binds plan/harness/READY and ordinal2 of the finite RED2/GREEN1 grant, no_rerun true. READY binds accepted medium I, my high C/P/P, actual O1/O2 approval, RED2 exact receipt,349/31 and explicit environment/sampled-storage limitation acknowledgement. No attempt alias/rerun is present in this evidence.

Recorded Root/Runner/Core identities are respectively `c5ef91f4d11a93bd2cdcc9d0b6b18bba0df80ed0`, `fefaa27f194bfddf85dd51a0e255beef2218c06d`, `9f4a96d032ad868ec010ce92d915bb81087c8d92`; receipt:172–181 and417–426. Frozen patch SHA is identical before/after. Immutable equality is reported true:428. No new claim about current remote refs is inferred from these historical snapshots.

The exact ten recorded source/fixture paths in receipt source_before:111–156 and source_after:356–401 match the prior independently recomputed C/P/P hashes, all unchanged:

| Runner path | SHA256 |
| --- | --- |
| src/composition/native_phase_telemetry.jl |`aba27f8c873b28f4b3f99d7736c9bedf40368ca4154e7c0af0ab592fc7ece216` |
| src/composition/scientific_execution.jl |`52aded550f1362b67f7c3781e2d45daac0e001a6dd0248a730f29299d443645f` |
| src/composition/scientific_workflow.jl |`b391a455247208a4293ea1aa000b4a288c097a70c23abd45f59e9f1b29a01337` |
| src/infrastructure/persistence/point_artifacts.jl |`18bcd0fe2c6ff42050c500b57f17678b06a38f14871a9a3de437841cb5f8d1ad` |
| src/infrastructure/resources/linux_resources.jl |`c6cceec4f6c8706485dbfa2902531f3c76d95b7c47dcffb773d9934de267f39f` |
| test/contracts/checked_storage_forecast.jl |`f3f263ad0b1b13dcc8a20b5668bfdccb7bb7fa5d30937bd72d7793a0013d2cc4` |
| test/infrastructure/strict_campaign_resource_admission.jl |`b6470f1d8e3b89b5ad71b9a8cb6cbcc9873221c85a2515cb8e3188306831b8c2` |
| test/application/execution_resource_contract.jl |`42fb1de375ee1c6e3e0b4710dc045a8b308b3507790468eb6a112bd01e836aa9` |
| test/infrastructure/linux_process_resource_probe.jl |`fb36182464c643c42951bcd89a0ad59f6f0118f0524050c3dbe0c0a80c3a581c` |
| test/integration/native_phase_resource_contract.jl |`63d83e77025c74140cd67af9d9efb2b1bb7df735bebf7ac9c06c4c16e3476a6a` |

Receipt command:209–225 includes exactly the five frozen files, no whole-group runner. It records Julia1.13.0 assertion, one thread, check-bounds, compiled-modules/pkgimages existing, and four `realpath(pkgdir/pathof)` identity assertions before tests. Raw:1 reports Runner and Core overlay package/source locations; environment:429–461 records unchanged Project/Manifest bytes and symlink literal/resolved destinations to the reviewed Runner and Core. `pkg_identity_observed=true`:494. Pinned runtime SHA `02618fb870c4b0f35976837605b39026b55ed998fc51dfe1edb95ae928c85d4f` is the same in both source snapshots. This confirms expected import identity within the recorded harness contract; it is not an OS-enforced read-only mount or dependency-closure proof.

## Полнота и denominator

Raw is fully readable2942B and its measured SHA agrees with receipt:466–468. Raw:1–38 includes import identity, counts, verbose named summary and terminal `QCL_SELECTION_FINISHED`. Receipt:462–465 has exit0, guardian_error null, capture complete true and capture_error null. Thus acceptance uses independent count/identity/completeness evidence in addition to exit status.

Raw:2 and receipt:480–492 agree:349 passes,0 fails,0 errors,0 broken,33 nested named testsets. All per-group counts match prior source expansion. F/B/D rows:5–19 total118; S/O:20–32 total131; three application rows:33–35 total55; Linux:36 total26; integration:37 total19. Their sum349 and frozen F/B/D15+S/O13+legacy L3=31 required logical groups are unchanged.33 is the physical named-testset count, not a replacement denominator of31 logical properties. No skipped/missing property group is visible in the complete raw summary.

This observed GREEN1 now supplies runtime evidence for the tiny manufactured controls and standalone regressions previously marked nominal. O1/O2 runtime checks still exercise shared private seams with tiny inputs; the independently accepted actual production caller/source ordering supplies their binding to real entry/commit. No typed full scientific entry, NEGFSolution payload publication or all-write guard was executed by these fixtures. D3 fake boot constructor/cache controls are included in integration19; they do not establish native boot/admission identity.

RED2 remains primary differential evidence, exact receipt SHA `1ae6c4cd1ac24f82dbc43558f9f145654468347e4a9b91ef81563ff2ed59714c`: healthy pass plus prohibited Bool forecast not throwing yields1 pass/1 fail/0 errors, as already independently inspected. READY explicitly binds it. GREEN1 receipt:196–207 preserves original RED1 bootstrap failure consumed, receipt `8d638a5de2c52db561ad50152194b6033536c99a1e903a2684c92348d0e653df`, raw `cd29bae7df710592bb53eb10085abe42277de704e0699f2475a1cf455e1c16ba`. RED1 is not renamed behavioral RED. C08 exhausted8/8 remains unrelated and unchanged.

## Ресурсы и ограничения

Receipt:469–479 records wall27.972184391s, sampled RSS peak622735360B,550 attempts/550 valid/0 unknown observations, sampled owned TMP peak32791B,551 TMP samples; raw2942B. These are below the recorded per-call600s/2GiB/16MiB/1MiB caps. Command records threads1 and runtime identity. Sampled RSS/TMP do not prove transient hard peaks, arbitrary dependency writes or absence of network syscalls. No actual CPU-seconds field is present here; measured CPU usage must not be inferred from one requested thread. Receipt:495–501 preserves these limitations; Root READY acknowledged them. No production throughput, speedup, capacity or accepted-solution timing conclusion follows from a27.97s unit process.

## CP-CODE и условный G1

The reviewed source and observed bounded controls are sufficient for **narrow SCI08-R1 CP-CODE** and preparation of an owning Runner draft containing exactly the five source files plus five frozen fixtures above. Logs, receipts, depots, scientific arrays, schema, Root files and unrelated changes must not enter that component code commit. Evidence remains separately retained with original failed attempts.

Conditional G1 eligibility is a **source gate only**, with these unresolved publication conditions left to Root rather than fabricated as current observations:

1. Published owning commit/PR must contain the same ten reviewed blobs and no semantic source/fixture delta; bind resulting exact commit/tree and retain complete C/P/P, O1/O2, RED1/RED2/GREEN1 identities. A new commit hash alone does not invalidate equal blobs, and it does not inherit full release acceptance.
2. Use the owning Runner PR and then published gitlink in Root under existing publication authority. Obtain fresh exact PR head/base, current required checks/protection/mergeability and resolve any G1 repository-policy obligations for that exact source. This read-only review has no live remote metadata and grants no merge/deploy action.
3. Keep campaign-strict unconditionally `needs_guard/needs_admission`; R2/R3/P1/P2/A1/C1, all-write/resident storage, native ownership/freshness/leases/admission, full native CI and science remain open. No S1 launch or scientific/experimental acceptance claim may be attached to this unit GREEN.
4. Retain single-attempt accounting: GREEN1 consumed, RED2 consumed, original failed RED1 consumed; no automatic rerun or resurrection of C08. Publication must report349 targeted assertions/31 logical groups and scope accurately.

These are conditions on eligible publication, not a demand to rerun tests or an assertion that remote G1 already passed. Fresh metadata/source publication checks belong to Root's separately authorized publication stage.

Audit content reads were limited to saved receipts/raw/READY, prior C/P/P identity and narrow policy/CP excerpts, below4MiB logical content. No physical resource sampler was run for this audit; no claim of measured reviewer CPU/RSS/I/O. Two report artifacts remain well below128KiB output. Missing guessed policy filenames were reported by read tools and not replaced with invented content; current source-gate policy and supplied scope were used.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Exact I1 bounded GREEN completed | Receipt hash, raw1–38,349/0/0/0,complete capture,identities | Fake-only unit scope | сохранить |
| Ten reviewed blobs and denominator unchanged | Before/after hashes match C/P/P; per-row counts | Historical receipt, not live remote ref | сохранить |
| Narrow CP-CODE / owning draft eligible | Accepted design+C/P/P+O1/O2+RED2+GREEN1 | Only ten named code/fixture files | сохранить |
| G1 publication already complete | No PR/live policy metadata in this audit | Exact commit and fresh G1 conditions remain | данных недостаточно |
| Full SCI08/S1/native/science accepted | Strict closed; remaining guard bindings open | No campaign/science/full CI evidence | данных недостаточно |
