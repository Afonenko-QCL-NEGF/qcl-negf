# OPS08 — independent high review literal RED fixtures

**PASS_SOURCE.** Блокирующих замечаний к новым 11 test methods не найдено. Fixtures различают два установленных source gaps, сохраняют healthy/uncertain controls и достигают целевых границ по структуре actual route. Это допуск источников к отдельно связанному Root first RED, **не observed RED/GREEN** и не разрешение reviewer запускать тесты.

## Immutable packet

Worktree `/tmp/qcl-ops08-worktree`, actual HEAD **`f5bc368654414039f7368bb19ca3201fa7f29f9d`**. Status: только новый untracked `tests/test_maintenance_failure_boundaries.py`; tracked diff пуст. Production/docs unchanged; sole product writer остаётся OPS08 I. Root/owning инструкции и scope прочитаны в текущей цепочке; эта фаза — отдельный узкий CPP fixture-source review.

| Input | SHA-256 |
| --- | --- |
| new test, 11446 B | `4cf04db2e0884afd5c0ec24171df29374c363569209b2fd0c181f3a23b7c73ad` |
| `/tmp/qcl-ops08-red.patch`, 11949 B | `7d9f5d4ee2008a1ce57d464d88328b3ae201bdcd6662c8a7d0b860cf1708bc8d` |
| `/tmp/qcl-ops08-red-report.md`, 8316 B | `3377447aeea86bdd289bc7381d65e7d556cfbb48960882b3e5eb0dac35413a44` |
| `/tmp/qcl-ops08-red-identity.json`, 1318 B | `01f90bc6af5b39d39b639fb10412ba1d375179dbdafbb2c47132765d2f519b9b` |
| actual production `ops/application_release.py`, 190991 B | `1d4422bed5986901ddef22890ca16fe600336e6af2bef17d83ae809ebe794df0` |
| `ops/aiida_update_check.py`, 2927 B | `401022a96a0c553e496430b8202d86767177bfaeda2d65d1b11b7388bbae8dc0` |
| actual `docs/application-cd.md`, 28454 B | `2d7add594947768ed1423efd0e8b3dae45b6c1f904e583b0cb1eb2e8f4f97414` |
| existing `tests/test_application_release.py`, 264761 B | `3b39987d1a3e1914ba45c8224af6d600dc92cffa6c030a9feaa955dfb0e326d6` |
| existing `tests/test_node_enrollment.py`, 58668 B | `d99c003fccc308c9cffed172f38ec69eeaa744f2753c7a95c28794d07aca305d` |

Новый файл и patch прочитаны целиком; их frozen hashes совпадают с поручением. Прочитаны actual helper/command model, FakeProtectedFS/registry/pool, preflight/trust и выбранные production boundaries. Target code/import/parser/test не исполнялся.

## Authority, namespace и healthy reachability

Новый `MaintenanceFailureBoundaries.setUp` **не использует** `I14UpdateTests.setUp`, где существующий старый fixture подменяет high-level preflight. Он переиспользует только class setup для загрузки production module при будущем test execution. В новом setup patch targets ограничены `/etc` config/profile IO helper, host identity facts, process boot UUID и selective protected-namespace syscalls. Actual `deliver_cli`, `_deliver_cli_locked`, `preflight_controller_authority`, `load_enrollment`, `freeze_ssh_trust`, enrollment/node/release validators, lifecycle owner/locks, `_activate_owned`, check, publishers и finalization остаются production functions.

FakeProtectedFS seeded независимыми root-owned `/protected/enrollment.json`/known_hosts facts и предками configured TRUST_SNAPSHOTS. Routing различает synthetic `dir_fd`/fds; fake descriptors начинаются выше1,000,000, поэтому не подменяют обычные реальные runtime descriptors. Абсолютный root open и его protected child traversal направлены в handwritten namespace; остальные runtime/profile/journal/gate syscalls реальные temporary IO. Actual protected reader/stat checks и actual freeze write/fsync/close выполняются над этими facts, а не заменены ready authority result.

SSH adapter выбирает actual generated UserKnownHostsFile, независимо сверяет frozen bytes с literal `b'independent synthetic key bytes'`, затем временно адаптирует только existing command fixture TRUST path. Production snapshot/hash/trust option validators сохранены. Это не attestation настоящего root namespace или SSH host key. Local observer synthetic CONTROLLER и synthetic process boot нужны для согласованного host boundary; они не доказывают native identity. Real PID/start ticks остаются у process generation.

Healthy control требует completed/open, exact gate release-a, два ordered RESUME и отсутствие lifecycle/admission intents. Он вызываeт полный actual delivery path с controller+worker+second enrollment, а не подставленный completed report. Existing command model даёт literal capability, measured-stop shape, generation/registration, check/health/finish responses; actual validators продолжают их проверять. На source уровне не найден ранний missing prerequisite, который заведомо делал бы все новые тесты unrelated failures. Runtime достижение ещё не измерено.

## R1: semantic release negatives отделены от envelope negatives

Локаторы: new `semantic_check`, пять `test_*` siblings; production `verify_node_envelope:584–597`, `_deliver_pool_owned:1594–1613`.

Injection применяется **после** actual external-command fixture response первого worker `check`. Preconditions требуют фактический controller profile setter и remote worker activate. Для ready false/missing/wrong valid release меняется только соответствующее release поле; envelope schema и node identity сохраняются. Отдельные wrong_schema/wrong_node siblings затрагивают именно существующий uncertain path. В expected values нет вызова production validation helper или вывода результата из его return value.

После injection требуется ровно одно достижение, controller verified/worker failed/second not_attempted и буквально пустой later command list. Дополнительный no-copy/activate/check/finish/RESUME assert избыточен, но совместим с этой границей. Gate обязан быть closed. Три known release negatives сохраняют `requires_reconciliation=False` и не выдумывают unknown; два envelope siblings требуют прежний unknown/reconciliation.

На frozen baseline три known-negative siblings должны различить plain ValueError ветку, которая продолжает loop. Healthy sibling и два existing uncertainty siblings служат positive controls. Это **статическое ожидаемое RED**, не результат запуска. Fixtures не предлагают расширить uncertainty policy ради получения pass.

## R2: фактическая local-journal граница после open

Локаторы: new `finalization_fault`, `reached`, `local_publish`, `local_unlink`, `gate_publish`; production `_finish_owned:994–1006`, outer :2881–2916.

Фильтр `operation=='whole_update' && status=='completed'` выбирает nested local journal. Outer attempt имеет `operation=='whole_cluster_update'`, поэтому его terminal publication не является случайной точкой fault. В unlink sibling выбирается собственный lifecycle-intent, который в route удаляется `_finish_owned`, а не admission marker.

Перед каждым one-shot fault `reached()` независимо проверяет **уже open gate**, ordered два RESUME и ordered два `finish-update`; затем сохраняет exact bytes единственного actual lifecycle intent. Поэтому ранний preflight/activation failure не может удовлетворить test. Callback не подменяет `_finish_owned` или journal factory.

Пять siblings различаются:

| Fault | Реальная injection boundary | Literal required outcome |
| --- | --- | --- |
| journal | OSError до actual completed local-journal publication | failed/reconciliation, подтверждённый closed gate |
| journal_after_replace | actual publisher завершается, затем one-shot OSError | тот же recovery close; это failure после publisher, не отдельная syscall-fsync oracle |
| unlink | PermissionError на actual own lifecycle-intent unlink | recovery close, исходный intent сохранён |
| deadline | monotonic100→1901 при original delivery deadline1900, затем actual publisher guard | failed, open=None/unknown/critical, фактический gate ещё open |
| close_failure | journal OSError плюс отказ subsequent close publication | failed, open=None/unknown/critical, фактический gate ещё open |

Во всех случаях первоначальные intent bytes должны сохраниться. Same-runtime retry после снятия temporary fault/clock patches обязан остановиться по **настоящему durable blocker** до новых command callbacks; marker не удаляется ради retry. Clock не получает новый budget. Unknown outcomes не подменены closed только по exit или наличию receipt.

Frozen baseline должен отказать этим пяти expectations на незащищённом finalization path; runtime не наблюдён. Это конечный набор exception controls. Он не доказывает universal crash protocol, OS durability, реальное NFS/root_squash, privilege mapping или работу native services.

## Независимость и границы проверки

Commands/NativeUpdateModel/control_response — общая инфраструктура с existing I14/OPS03. Их reuse обеспечивает compatibility и достижимость, но может разделять ошибку; это **не второй независимый native oracle**. Новые различающие expectations literal: phase preconditions, no later commands, gate state, known/unknown classification, preserved bytes и retry barrier. Healthy end state не вычисляется из production validator.

Существующий OPS03 cap исчерпан; старые source/receipt результаты не переисполнялись. Новые RED calls этот review не выделяет: Root должен отдельно bind frozen packet и конечный первый RED. Нет production implementation, observed RED/GREEN, native/full-final/CI/scientific claims. Original auditor FAILED_RESOURCE_CAP остаётся неизменным; эта новая fixture-review фаза его не пересертифицирует.

## Named read ledger

Envelope ≤15min/1CPU/2GiB/read4MiB/report64KiB. Для каждого `sed`/`rg`/SHA pass консервативно списан **полный размер named file**, даже если early quit или extracts меньше. Прочитанное содержимое затем использовано из tool/context cache; повторные source passes перечислены явно.

| Группа | Charged upper bound B |
| --- | ---: |
| Full new fixture/report/identity + их SHA pass | 42160 |
| Existing application fixture extract, full-file charge | 264761 |
| Existing enrollment definitions rg, full-file charge | 58668 |
| Production/docs/helper/patch SHA pass | 234321 |
| Enrollment source extract, full-file charge | 58668 |
| Production boundary extract, full-file charge | 190991 |
| Full patch read | 11949 |
| SHA pass обоих existing helper fixture files | 323429 |
| **Total** | **1184947** |

Git/status/file-size metadata не выдаются за physical-source read telemetry. Physical I/O/RSS не измерены; консервативная source-byte граница ниже4MiB. Reviewer actions: target imports/parsers/tests/builds/network/server/children/product writes/Git mutations/checkpoint writes/C08/science — **0**. Только эти review artifacts в `/tmp`.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| 11 fixtures привязаны к нужным phase boundaries | Actual route + literal reached/injection assertions | Source-only, healthy completion не наблюдён | сохранить |
| R1 differentiates known release failure и envelope uncertainty | Три release mutations и два отдельные siblings | Synthetic transport, expected RED ещё не измерен | сохранить |
| R2 охватывает post-open finalization/recovery/unknown | Пять one-shot fault bodies, preserved intent/retry assertions | Не universal crash/native durability proof | сохранить |
| Authority/owner/high-level validators сохранены | Exact patch и selective syscall/host/command boundaries | Host facts synthetic, shared model | сохранить |
| RED/GREEN/native acceptance получены | Нового execution evidence нет | Root first bounded RED ещё впереди | данных недостаточно |

**STOP. PASS_SOURCE exact fixture packet; Root отдельно связывает и исполняет sole first RED.**
