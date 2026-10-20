# OPS08 — независимый source audit выбранного Platform

**Вердикт: REQUEST_CHANGES / PARTIAL_AUDIT; ресурсный результат FAILED_RESOURCE_CAP.** Установлены два воспроизводимых пробела в existing whole-update source и одно расхождение документации с кодом. Для них достаточно узкого I по существующему контракту; нового архитектурного решения D не требуется. Полнота OPS08, whole-final, native и full DEV25 не доказана.

## Этап, identity и ограничения

Этап — только чтение выбранных исходников, contracts и уже сохранённых receipts. Никакие Python/Julia imports, parsers, tests, helper execution, Nix/build, SSH/network/server/deploy, solver, children или Git mutations не выполнялись. Изменены только этот отчёт и companion identity в `/tmp`; checkpoint и product source не менялись.

Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`: HEAD `514cd9707a32cde60c630d60986973a898d35b18`. Root не clean: coordinator-owned checkpoint/census/evidence, DOC04 files и Contracts untracked state сохранены без вмешательства. Selected gitlink и actual clean owning HEAD Platform совпадают: **`f5bc368654414039f7368bb19ca3201fa7f29f9d`**, путь `components/qcl-negf-platform`. Обычный `git status --short` владельца пуст. Owning `AGENTS.md` и вложенные AGENTS не обнаружены; применены Root AGENTS, architecture, implementation-entrypoint, canonical role policy и owning CONTRIBUTING. Навык using-superpowers прочитан: его SUBAGENT-STOP исключает workflow для делегированного audit; физический/results навык к этому operational source review не применялся.

| Primary input | SHA-256 |
| --- | --- |
| `ops/application_release.py`, 190991 B | `1d4422bed5986901ddef22890ca16fe600336e6af2bef17d83ae809ebe794df0` |
| `ops/aiida_update_check.py`, 2927 B | `401022a96a0c553e496430b8202d86767177bfaeda2d65d1b11b7388bbae8dc0` |
| `tests/test_application_release.py`, 264761 B | `3b39987d1a3e1914ba45c8224af6d600dc92cffa6c030a9feaa955dfb0e326d6` |
| `docs/application-cd.md`, 28454 B | `2d7add594947768ed1423efd0e8b3dae45b6c1f904e583b0cb1eb2e8f4f97414` |
| `CONTRIBUTING.md` | `1e957beb71b3c4d1ad632453f3aefdb7cfe97ecc02fbce038020480af1182f39` |
| Root `docs/implementation/review-closure-2026-10-19/platform-worker.md`, OPS08:180–190 | `34631baca67be3e4312facd0905fc9f205a9e9fe54d6bc05746cdf69ffc1d5eb` |
| Root `docs/system/requirements.md`, I14:84 | `af8febf7c71a409ee3f8e05720103ef4013117e67215dfabb2c87dfe96e7c6d8` |
| Root `docs/system/review.md`, CR02/I14 | `1496ef1538b15c26b6bd4f7780eed0b50653e3c2f3807c69a14110bc227867c3` |
| portable bundle `docs/implementation/comprehensive-review/2026-10-14-e48e5b2-01/RV14.md` | `430c4bca1cdfa821c80feaaf8f1665243aa51c2a2ac205cb7497f1942b353c0b` |
| same bundle `reviews/RV14-review.md` | `e201ee02d52377a18f5b4ddf0117fc3f6549ef9663946b947d72ef0e7f215f6b` |

В portable RV14 прочитаны также capsule, blind review и asset follow-up. RV14 относится к восьми source/build/import/runtime links, assets и переносимости acceptance. Он **не является I14 maintenance review**. Его требование не наследовать native/full-release acceptance по новому HEAD применимо здесь; maintenance denominator берётся из OPS08 и normative I14, а не из совпадения числа 14.

## Конкретные findings

### R1 — P2: semantically failed release check допускает dispatch следующему узлу

Локаторы на выбранном `f5bc368`: `ops/application_release.py::verify_node_envelope:584–597`, `_deliver_pool_owned:1594–1613`, remote `deliver` check path примерно :2808–2827. Contract: owning `docs/application-cd.md:213–214` обещает прекращение later dispatch после failed activation/incomplete check; OPS08 требует отсутствие later dispatch по предполагаемому успеху.

`verify_node_envelope` корректно маркирует `uncertain=True` при неверной schema или node identity (:585–593). Но correct envelope + correct node identity + отсутствующий/false `release.ready`, malformed release или другой валидный release вызывает обычный `ValueError` (:594–596). В outer node loop после записи failed status `break` выполняется только для `CommandFailure` или `error.uncertain` (:1611–1612). Поэтому проверка release после remote activation может отказать, а следующий node всё равно получает copy/activate. Gate при этом не открывается — это ограничивает последствие, но не выполняет declared stop-dispatch contract.

**Самый дешёвый различающий source fixture, не исполнен:** на базе `I14UpdateTests.commands/deliver` с существующим порядком controller, worker, second подменить только JSON ответа action `check` первого worker. Сохранить exact ENVELOPE_SCHEMA и фактическую node identity; независимо задать `release.ready=False`, затем отдельным случаем валидный `release_id='other-release'`. Healthy sibling пропускает исходный ответ. Assert: injection достигнут ровно один раз после actual worker activation; worker failed, second not_attempted; после injection нет второго worker copy/activate/RESUME/finish-update; admission закрыт. Не патчить validator/owner/high-level deliver. Existing `ApplicationReleaseTests.test_malformed_remote_check_is_unknown_and_stops_pool:482` подставляет синтаксически неполный JSON и потому не различает этот sibling. Wrong node/schema уже covered production uncertain path; этот finding к ним не относится.

**Готовый I-follow-up:** сделать failure любой требуемой проверки узла stop-dispatch boundary, сохранив existing known/unknown classification и fail-closed behavior. Не превращать каждый known negative в invented native uncertainty, не добавлять permissive retry. Сначала literal RED source, независимый review, затем отдельный конечный engineering envelope у Root; этот audit не даёт test call.

### R2 — P1: final local-journal failure после открытия admission обходит recovery close

Локаторы: `_deliver_pool_owned:1622–1633` открывает gate и публикует completed; `_deliver_cli_locked:2881–2916`; `_finish_owned:994–1006`; `_begin_local_mutation:934–979`; `guard:1511–1523`.

Controller activation создаёт local lifecycle journal под тем же whole-update owner. После успешного fleet health/RESUME `_deliver_pool_owned` открывает admission. Outer callback завершает worker markers; его ошибки уже покрыты `close_after_failure` (:2887–2888). Но следующий `_finish_owned(owner, deadline=deadline)` (:2889–2890) стоит вне такого recovery boundary. В нём publication completed local journal и unlink local intent остаются fallible (:1004–1006). Их OSError/PermissionError/deadline исключение попадает в outer handler :2906, который публикует failed receipt, но **не вызывает close_after_failure** и сам не выставляет reconciliation для обычного OSError. Gate может остаться `open=True` при failed completion. Оставшиеся durable intents блокируют lifecycle retry; `guard` проверяет gate/local ready, но этих intents не читает, поэтому их наличие не доказывает closed job admission.

Это конкретная пойманная exception path внутри cooperative Python owner, а не требование обещать атомарность на любом OS crash. Известный более широкий raw gate-open/crash commit-protocol residual из OPS03 также сохраняется и этим замечанием не закрывается.

**Самый дешёвый различающий fixture, не исполнен:** расширить actual `OPS03WholeRoutingTests` healthy whole-update body. One-shot fault в `publish_json` только когда `value.operation=='whole_update'` и `value.status=='completed'` (именно nested local journal, а не outer `whole_cluster_update` receipt). Зафиксировать, что до fault gate уже open и все fleet controls достигнуты. Отдельный sibling — OSError при unlink собственного `*.lifecycle-intent.json` в `_finish_owned`, без удаления чужих files. Требовать recovery close, truthful failed/reconciliation summary и сохранённый исходный intent; при injected close failure — `open=None/critical_admission_failure`, не fabricated closed. Same-runtime retry должен блокироваться без новых child commands. Positive sibling проходит исходный full route.

Existing `test_review_gate_open_fsync_and_terminal_receipt_failure_keep_blocker:586` проверяет outer delivery-attempt terminal publication; `test_o09_ready_and_terminal_durable_publisher_syscall_fault_matrix:3669` выбирает standalone `operation=='activate'` при исходно закрытом gate. Они полезны, но не покрывают именно whole-update local-journal finalization после уже успешного open.

**Готовый I-follow-up:** включить final local-journal завершение в existing post-open recovery/error boundary; сохранить immutable originals, own-intent identity, global deadline, close failure unknown и no-auto-retry. Не разрешать просто удалить blocker. Нового D не нужно для обработки этой bounded exception path по существующему контракту.

### R3 — P3: documented metadata cap не соответствует выбранному source

`docs/application-cd.md:382` называет 32 MiB/action. `UpdateScan.CAP` в `ops/application_release.py:1679` — **64*1024*1024 B**; общий объект расходуется action-wide. Existing F5/R4 controls выводят cap из actual `CAP`; они не доказывают literal 32 MiB. Исправить owning текст на фактическую величину и сохранить различие prepaid logical upper bounds/returned bytes/server physical I/O. Это docs correction, не предложение менять cap ради прохода.

## Disposition по обязательным controls OPS08

Статус «source present» ниже означает найденный механизм и meaningful fixture source, а не новый test/native PASS. Из-за read-cap failure эта таблица не является exhaustive proof отсутствия иных дефектов.

| Требуемый контроль | Выбранный source / fixture witness | Disposition и предел |
| --- | --- | --- |
| Local controller authority до writes/mutation | `deliver_cli:2480–2508`, preflight :525–572, enrolled local/remote match, owner locks; O14 forged binding | сохранить source; real inventory/host authority неизвестны |
| Complete enrollment, offline нельзя исключить | `validate_enrollment:284–307`; equality :2495; I14 complete_enrollment и missing_offline_node | сохранить; trusted retirement — отдельное изменение, не inferred skip |
| Closure hashes до gate/services | `prefetch_controller_closures:1059+`, validate_only до authority, actual prefetch до quiesce; existing hash/cache fixtures | сохранить; actual Nix signatures/import/closures отдельно |
| Installed capabilities каждого узла | exact capability object :2667–2671; I14 uninstalled capability; OPS03 legacy protocol negative | сохранить; installed native support неизвестен |
| Original healthy IDLE/zero allocation/full Reason | `capture_original`, registration parser/safety :2289+, retained provenance :2349+; F3 and R2/R3 fixtures | сохранить; no foreign DRAIN overwrite, no arbitrary prefix ownership |
| All QCL parent/retry/CalcJobs cancellation, no automatic cancellation | helper `nonterminal_filter/inspect_profile`, `aiida_cancellation_check:2250+`; I14 active paused retry, standalone restart, terminal parent/nonterminal child, orphan CalcJob, no-cancel commands | сохранить source; bounded existence query с limit(1) не pagination последней страницы, оба типа в одном predicate; native SQL NULL semantics неизвестны |
| NULL/missing/unknown state, malformed/query failure | helper OR missing-key/NULL/not-terminal; I14 null/error and paused/null/missing fixtures | сохранить; Python fake QueryBuilder проверяет форму predicate, не backend execution |
| Fresh cancellation после snapshots/restart и перед RESUME/gate | `quiesce` cancellation до и после stopped barrier; `admit` после health, перед каждым RESUME/в readback/после loop; post_restart fixture | сохранить; trusted concurrent/native submit races не измерены; check не замена admission guard |
| Stop all workers до первой activation/copy | :2767–2769 full set + each stopped receipt; I14 all_worker_stop_barrier and F2 stopped drift | сохранить source; VM poweroff/RAM reclaim не обещаны |
| Unknown cgroup member/daemon replacement force запрещают | `physical_stop_scan:1913–1975`, singleton_scope:1978, stop_update:2188–2248; F1 unknown root/subgroup, ticks/exe/invocation/snapshot drift и delegated leaf | сохранить; positively bound singleton, full members/executable/classification; real proc/cgroup permissions неизвестны |
| Measured stop/readback и mask ownership | stop_update, observe_stopped_update, verify_stop_response; effective runtime-mask and F2 malformed nested receipts | сохранить; synthetic file/syscall boundary не real systemd/mask proof |
| Failed stop/copy/activate/check не дают later dispatch | stopped_observation unknown boundary, dispatch uncertain, node loop | **изменить R1**; syntax/type/node negatives не покрывают correct identity + bad release |
| One owner/durable intent/reconciliation/no hidden retry | lifecycle_owner:809+, _begin_local_mutation:934+, unresolved_deliveries:609+; O01/O04–O11/O17, retained original bytes | сохранить controls; **изменить R2** для composition после open; общий atomic reader/crash residual остаётся |
| Global deadline/output и bounded workspace | command/dispatch, authority used-output handoff, UpdateScan, F5/R4 | сохранить mechanisms; source limits не hard real-time/fsync interrupt proof; **изменить R3** documentary cap |
| Same-generation full health/RESUME readback | fleet_health:2411+, current_worker_health/owned_resume_state :2377+, admit bounded10 polls; F4 stale/down/daemon and resume-lost failure patterns | сохранить; no open на incomplete generation/readback; native Slurm wire/time/actor semantics неизвестны |
| NFS/root_squash write/read/fsync failure | admission_reader, fleet_health own probe, F6 actual probe failure matrix, root_squashed gate fixture, terminal fsync negatives | сохранить; synthetic UID/filesystem effects не actual export/durability proof; R2 finalization sibling дополнить |
| Public redaction/private original receipts | private attempt command/raw prefixes vs safe_summary/public delivery-report; existing failure summary tests | сохранить; full private-data scan не проводился |

## Сопоставление с уже выполненными OPS03/04 — после собственного verdict

Собственный source verdict и R1/R2 были сформированы и переданы Root **до** чтения OPS03/04 reviews/raws. Затем прочитаны указанные Root артефакты; они не подменяли первичный диагноз.

OPS03 GREEN4 receipt `/tmp/qcl-OPS03-GREEN-4/receipt.json` SHA `b2411039050e39b38b8a95fc02e1a77f867d6933fc83836ffa049b33540ba7c7`, original log содержит terminal **234 passed in 93.54s**, receipt wall **94.294 s**, exit0, raw complete/no guard error. Старый full test source hash — `f56062eef912a7c63ab9743a24f1db8a5043c2e24620db0732ab516485c0ce21`; production application_release SHA совпадает с текущим `1d4422…94df0`. Log слишком велик для одного tool response и был усечён в выводе; полный outcome/nodeid denominator здесь независимо не реконструировался. Сохранённый high review сообщает verified234; собственное подтверждение ограничено receipt и доступным terminal/raw excerpts. GREEN4 не исполнялся заново.

Current test source — другой hash `3b39987…326d6`. OPS04 final review + journal описывают test-only amendment и compatibility update, сохранив production ops. `/tmp/qcl-OPS04-PLATFORM-GREEN-2/receipt.json` SHA `a3483add4b4c805e6719a78c9e9cc5ca4657a30594954b61e5f7a86248574fc8` привязывает current tests hash и selected16 controls; original99-byte log **16 passed in0.87s**, receipt wall **1.558s**, exit0/raw complete. Это конкретный narrow engineering result, не новая whole-suite acceptance текущего hash и не проверка новых R1/R2 regressions.

Publication journal SHA `ab3467e1d4e43b71c08d70f7e69f67d34a68246bd96edfaa6caa1c3a1ca7817e` фиксирует owning PR19, head f5bc368 и G1 merge. Local Git log соответствует test-only последних commits; actual selected owning HEAD f5bc368 clean и совпадает с Root gitlink. Удалённый GitHub ref/network здесь не проверялся. Последовательность component-before-root согласуется с представленным journal; полного DEV25/source-to-runtime closure отсюда не следует.

Прежний OPS03 scoped CP-CODE PASS сохраняется **для заявленного cooperative owner scope и тех fixtures**. Наличие 234 PASS не означает exhaustiveness; R1/R2 — дополнительные неразличённые source paths. Его открытые provisioning/prepare-initial/raw-gate crash/native residuals не сняты. Original failed/interrupted attempts и finite consumed counters сохраняются. Новых test calls не выделено, OPS03 cap исчерпан; этот отчёт не даёт hidden rerun или reset.

## Ресурсный сбой этого audit

Порученный envelope: ≤25 min, 1 CPU, 2 GiB, source-read cap **2,097,152 B**, report≤96 KiB. Точного предзаряженного per-read ledger я не вёл. Ошибка метода: повторные `sed -n` без early quit читали whole files, а я первоначально учитывал только выбранные excerpts. Уже минимум двенадцать полных проходов по `application_release.py` составляют **2,291,892 B**, то есть превышают cap без учёта tests/docs/hash passes. Фактический aggregate больше этого lower bound; точное число и physical I/O/RSS неизвестны.

Это **FAILED_RESOURCE_CAP**, не PASS и не ретроактивное продолжение. После обнаружения прекращены source reads; далее записаны только review artifacts. Root уведомлён отдельно. Выполненные замечания сохранены как partial audit; дальнейшее независимое чтение/проверка требует нового явного finite continuation у координатора. Нарушение лимита не скрывается положительными controls или существующим GREEN. Output report остаётся в пределах96 KiB; никакого execution-cost бюджета не потреблено.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Correct node + failed release может позволить later dispatch | verify_node_envelope:594–596; node loop:1611–1613 | Статический trace, новый regression не исполнялся | изменить |
| Local-journal finalization после open не имеет recovery-close boundary | :2889–2890 → :994–1006 → outer:2906–2916 | Конкретный controlled exception, не universal crash proof | изменить |
| Документированный cap32MiB расходится с actual64MiB | docs:382 vs UpdateScan.CAP | Не предложение менять cap | изменить |
| Основные I14 source guards и meaningful negative fixtures существуют | Таблица controls и frozen packet | Partial read audit, shared synthetic model, cap превышен | сохранить |
| OPS03/04 engineering receipts действуют в собственном scope | GREEN4 и GREEN2 originals/receipts, exact production hash | Current whole suite/native/new regressions не доказаны | сохранить |
| OPS08 whole-final/native/DEV25 закрыты | Нет достаточного свидетельства; есть R1/R2 и ресурсный сбой | Native unavailable; проверка не exhaustive | данных недостаточно |

**STOP.** Готовы узкие I-follow-ups R1/R2 и docs correction R3; source-only artifacts не разрешают execute/test/deploy. Новый D нужен только если автор предложит менять existing failure/admission policy, чего здесь не предлагается.
