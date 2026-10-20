# I2C — source correction, PARTIAL / CHANGES REQUIRED

Selected worktree `/tmp/qcl-docs-test-routing-worktree`, actual HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`. Один конечный source-only проход
по high CPP `4903c3d64d8254a7b4ac89fcc08efed049485a21b1a1c155922b515b6118c4ea`.
**Source PASS/READY не заявляется.** Сохраняются перечисленные ниже source и
coverage gaps; STOP для отдельного high CPP, без автоматического продолжения.

Изменены только native Python, driver TS и два native fixtures. Pure helper
SHA676a… и fixture SHAf02f… остались неизменны,230 nominal=227+3.
Root/main/CP/gitlinks не менялись. I2B report/identity/complete patch повторно
сверены:611ce7… /5dce8b… /c09188…; исходные артефакты не переписаны.

## Disposition восьми P1 групп

| CPP | Source correction и locator | Ограничение / disposition |
| --- | --- | --- |
| C1 parent lifecycle | `RunningDocsSetup:1555`, `_dispatch_control:1567`, `await_phase:1618`, `launch_phase:1642`, `await_terminal:1651`: один pump демультиплексирует phase-ready/leader-bound/closing; phase1 drain возвращает управление до final setup. Closing сопоставляется с parent phase ledger и actual refs. Fixed task launch использует existing lease before-exec hook; terminal adapter проверяет producer/job EOF/reap/ref/raw и whole-empty original guard, появился conditional complete branch. Failure wrapper сохраняет D6 failed setup receipt. | Конкретный queued phase-ready конфликт исправлен на source уровне. Полная syscall/error matrix и adapter integration ещё не проверены; отдельные fallback errors могут прервать сам fallback. Candidate, не closed CPP. |
| C2 retained readers | `read_katex_observation`: persisted record содержит только root/version/module/css SHA; external actual ref добавляется после чтения в normalized pure projection. Unit binding получает exact key set; runtime manifest читается и сверяется с parent registration, actual immutable files/hash/size; initial-empty decoded bytes сравниваются с registration payload. | Самоссылочный SHA fixed point удалён. Полная exact producer provenance/ownership manifest validation требует CPP; новые private attachment projections не считаются actual trust/BIND. Candidate. |
| C3 schemas/intents | `audit_intent:130` реализует D5 bootstrap/phase union с input/source/runtime/allocation/storage/deadline и только nonce/token hashes. `validate_request:1060` закрывает constructor/source/native/tools/storage/phase sets; actual full runtime inventory и все PhaseBinding fields сравниваются в parent ACK. Phase intent записывается до phase child. | Все nested registration scalar/authority/ref unions ещё не валидированы полностью; требуются отдельные finite ranges и unique manifest-entry checks. Частично. |
| C4 exception retention | Command pending record создаётся до child; command ledger существует независимо от successful captures. Fallback формируется и после reaped exception, содержит actual prefix refs/null и unknown counters. Native initial source/metadata moved inside run_phase guarded block. Driver object закреплён до constructor call; stderr теперь bounded pipe с observed EOF и retained raw; inherited FDs явно закрываются; producer subreaper/owner observation добавлены. Evidence index строится из native command ledger. | First-FD allocation failures, worker prctl/owner initialization, drain errors после KILL и dual-store failures требуют полной matrix. В отдельных error branches cleanup/final receipt всё ещё могут сами выбросить исключение. Не считать originals гарантированно retained при любых двух отказах. Частично. |
| C5 ledger | `StorageLedger.reserve/commit/release:388–401` разделяет outstanding capacity и actual committed bytes. Full cap больше не безвозвратный actual debit каждого Git. Failed written bytes не refund; unused reserve снимается после actual prefix reads. Owner handoff `adopt_existing:404` сохраняет накопленные on-disk bytes до producer и после reap; final parent writes charged. Compact pending≤384B/terminal≤1408B и index исключают прежние62MiB metadata. | Source upper-bound schedule проверяется до dispatch; actual actual-byte trace не измерен. Parent/native handoff и independent watchdog reserve должны быть сопоставлены CPP с owning trusted lease. Частично. |
| C6 source budgets | `admit_source_schedule:1106` выводит100/444 calls из fixed graph/native routes, требует unique source-controlled family byte caps и byte SHA для native blobs. Counters per-phase, storage/deadline global. Snapshot128/2MiB/20s;16 failed Git slots/256KiB reserved per phase. Blob raw hashes не требуют UTF8. Tickets phase-bound и закрываются после EOF. `noexec_git_metadata:1146` до Git отвергает filter/include/attribute indirection, читает worktree/common configs bounded nofollow. | Actual frozen Git family inventory/clean committed native16 ещё отсутствует. Native graph slots ограничены count, но complete exact ordinal argv sequence ещё не восстановлена; no-exec metadata/stat race review и snapshot final/failure accounting требуют CPP. Частично. |
| C7 protocol/finish | Python/TS reject depth>16/nonfinite nested values; chunk encoded cap проверяется до atob. Per-op wire caps и partial-prefix accounting добавлены. Native rejected finish создаёт durable validation/summary/index, sends rejected ACK, затем driver/phase closure. Positive aggregate exact step/runtime/attempt/stream/report-summary checks усилены; TS сверяет accepted digests/ref/enum. | Полная exact union validation responses/terminal scalars и ticket single-outstanding lifecycle ещё неполны. Finish ACK partial delivery и extra-frame/error matrix не исполнены. Частично. |
| C8 fixtures | Существующие8 Python methods +8 Deno registrations сохранены, subcases добавлены до соответствующих production edits: parent phase-ready duplicate/queued state, canonical capsule/base64, over-depth/overflow exponent, KaTeX without self-ref, reservation actual-vs-unused, terminal EOF/reap negative pairs, independent full-output report counts, encoded over-chunk. | Полного healthy factory→fake kernel→broker→prepare→execute→finish→parent final setup controls нет. Fakeproc/pidfd/cgroup/storage-full/partial drain/parent loss matrix не завершена. **C8 остаётся P1 к acceptance.** |

## Source schedule и границы evidence

Один clean owning graph=36Git; native16 binding=32Git (ls-tree+cat-file для
каждого fixed path). Preflight:36+2×32=100. Full check:7×36+6×32=444;
плюс4 unit commands. Preflight+full=544Git суммарно, каждый phase≤512; counters
обнуляются только per-phase. Общие storage/control/allocation/deadline не
обнуляются. Docs mode пока использует консервативный full upper bound444,
хотя actual3-step path короче; это не extra dispatch permission.

`expected_source.git_families` связывает exact root/argv, stdout/stderr upper
bytes и optional frozen stdout SHA. Native blob family обязана иметь bytes и
SHA того же fixed source object. Их actual measured freeze сейчас **не создан**:
overlay dirty, четыре native16 paths отсутствуют в HEAD. Missing/duplicate/
oversized/unfrozen inventory blocks attempt до dispatch; его нельзя заменить
выдуманными byte counts. Source schedule guard проверяет graph/native snapshot
≤2MiB, phase total+256KiB failure reserve≤8MiB, calls+16≤512.

Metadata source upper bound для548normal commands и16setup-wide failures:
`564×1792 +884736 +131072 =2026496B <2097152B`.1792=384pending+1408terminal;
884736 — D6 lifecycle+independent fallback reserve;131072 — compact index.
Это аналитическая bound-проверка **с текущими encoded record caps**, не actual
disk measurement или гарантия, что любой будущий path/field size поместится.
Actual retained root spelling bounded128B; generated index сохраняет shared
root и compact `(id,pendingSHA,terminalSHA,suffix,outcome)` rows, originals не
дублируются. Raw/unit/driver/source upper bounds сопоставляются с actual grant;
caps не повышены. Недостающий source freeze — явный runtime prerequisite,
остаточные source gaps выше — отдельное основание не объявлять completion.

Current native16 working bytes392173B. Точный authoritative size inventory
в companion identity; native Python126239B, каждый fixed source<262144B.
HEAD blob IDs приведены отдельно от working SHA: dirty overlays не выданы за
HEAD blobs. Полная clean native16 binding здесь не установлена.

## Parent evidence API correction

Concrete source adapter existing trusted lease теперь требует до bootstrap
`guard`, `storage_ledger`, `spawn_gated(...before_exec=hook)` и
`collect_docs_terminal(process,identity,participants,deadline)`.
Последний возвращает exact `{producer_terminal,streams,participants,retention_status}`;
actual terminal closure refs и raw refs читаются native parent, а не принимаются
из caller descriptor. This API remains inside existing trusted parent boundary;
он не создаёт новый grant/registry и не устанавливает серверный wrapper.
Если installation не реализует этот reviewed hook/evidence lifecycle — actual
attempt blocked. Source review должен отдельно проверить целостность adapter
и отсутствие fallback claims на JSON labels; local source implementation
этого external parent/kernel provider по нынешнему поручению не развёртывался.

## Остаточные blockers перед DEV

Нужен high CPP этой точной source packet. Не запускать8+8 как будто matrix
готова: C3 nested schemas, C4 first-FD/cleanup/fallback closure, C6 exact
operation slots/no-exec races и C7 terminal/refusal unions остаются source
risks. Parent fallback не переписывает существующий positive phase receipt;
delivery loss даёт failed setup/no next phase. Некоторые fallback IO/lookup
errors ещё могут не сохранить final ref — retention unknown, no success.

Доказательства выполнения отсутствуют. Выполнены только чтение, текстовые
patches, read-only Git, SHA256/wc и symbol inventory. Parser/compiler/import/
format/lint/tests/native/Deno/Julia/network/server/build/CI/science=0.
Ни implicit RED, ни GREEN не заявлялись; fixture denominators8/8/230 nominal,
observed=null. Исторические bytes не переписаны. Source packet READ ledger:
консервативный upper bound4MiB (<8MiB), включая SHA reads и high review;
CPU/RSS/physical I/O не измерены. Общий cap1CPU/1GiB/25min, один source pass.

Complete patch237096B SHA
`7fd92c7f21bcc63e16872fc7ea0f25b6267324e1277f2fa5a3c221a2ab61c13e`.
Это полный11-path overlay относительно selected HEAD; I2C менял только4paths.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Pure230 и I2B сохранены | unchanged676a…/f02f… и original I2B packet SHA | исполнения0 | сохранить |
| Конкретные C1/C2/C5/C6 дефекты исправлены | dispatcher/normalized KaTeX/reservation/per-phase schedule source | independent CPP/DEV впереди | изменить |
| Полная native source acceptance достигнута | остаются explicit C3/C4/C6/C7/C8 gaps | finite pass завершён, не READY | данных недостаточно |
| Kernel/tool/CI/science подтверждены | execution0 | source-only correction | данных недостаточно |

STOP отдельный high CPP. Product calls по этому source grant не разрешены.
