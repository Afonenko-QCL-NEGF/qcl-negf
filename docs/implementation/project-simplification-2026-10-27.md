# Упрощение QCL-NEGF: целевой design и программа на семь дней

Дата: 2026-10-27, архитектурное уточнение после дополнительного исследования. Статус: **проект для
review, реализация не начата**. Цель следующего поручения — за семь рабочих дней получить
отлаженную, установленную систему и затем сосредоточиться на физике. Это целевой срок, а не уже
подтверждённая оценка или приёмка установок. Документ объединяет решения, границы контрактов,
небольшие owning PR, последовательность и проверяемые результаты. Полномочия исполнения задаёт
связанный ниже план Codex; подготовка документации не означает выполнения этих действий.

**Исполнение:** [план Codex на целевом ноутбуке](codex-execution-2026-10-27.md) фиксирует новые
разрешения на VM/results/merge, Sol/Terra routing, граф задач и сетевой режим. Пользователь разрешил
прерывать/перезагружать/менять QCL VM и удалять старые результаты после read-only оценки текущего
исследования при выпуске. Архивировать/переносить результаты этого run не нужно. Target normal
operation остаётся resident/no planned eviction; это не ограничивает разрешённый cutover данной
переработки. Семь дней — ориентир, дополнительных resource/time budgets нет.

Место итоговой установки — существующий кластер с нынешними изолированными VM и mutable state.
Linux/libvirt ноутбук — первый **дополнительный worker**, а не полный новый стенд с
controller/Portal/CI. Подключение Hyper-V workers и перенос существующей CI VM на другой Proxmox
идут после его приёмки.

## 1. Как начать и что считать решением

Перед реализацией прочитать [AGENTS.md](../../AGENTS.md),
[baseline-архитектуру](../architecture.md), этот документ и инструкции затрагиваемого компонента.
Роли и усилия остаются в
[canonical policy](../system/release-roadmap.md#политика-ролей-и-координации): для текущей программы
models/efforts переопределены в исполнительном плане: Sol high/xhigh, Terra medium/high. Один writer
на файл, один владелец lifecycle операции. Не требовать повторного разрешения на уже порученную
работу внутри её scope.

Обозначения ниже: **Ф** — факт исследованного source; **Р** — решение пользователя; **К** — новый
целевой контракт; **А** — авторский выбор, который ещё должен пройти review. Пример API в этом
документе — предложение, а не обещание наличия такой функции. Внутренние имена определяет owning PR.
Старые implementation notes — история, а не дополнительный набор gates.

Снять `git rev-parse HEAD`, `git status --short` и `git submodule status --recursive`; сохранить
чужие изменения. Выбрать опубликованный source и перепроверить затронутые локаторы. Компонент
меняется своим PR; root затем обновляет опубликованный gitlink. Не обновлять все submodules до
`latest` и не создавать второй ручной lock компонентных ревизий. Ни готовый diff, ни merge сами по
себе не означают deploy.

### Короткий маршрут перед конкретным изменением

Не читать весь паспорт истории и все старые планы перед каждым PR. После общих инвариантов выбрать
owning PR из §7, его dependencies, соответствующий contract ниже и актуальные public docs владельца.
Полный source passport нужен для перепроверки finding, native runbook — только перед соответствующим
действием.

| Тема                                     | Нужный раздел    |
| ---------------------------------------- | ---------------- |
| API, config, ownership                   | §4.1, §4.5, §4.7 |
| Scientific history/checkpoint/reader     | §4.2             |
| Qualification, packages, CI и инструкции | §4.3–4.5         |
| Technical performance и cluster view     | §4.6             |
| Docs и научный handoff                   | §4.8             |
| Host/VM/Slurm resources                  | §5               |
| Update/boot/recovery/restore             | §6               |

## 2. Принятые границы и замена прежних правил

| Область          | Р / целевое поведение                                                                                                            | Следствие для реализации                                                                                             |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Репозитории и VM | Сохранить восемь component repositories, состав и VM isolation; новых dev VM нет                                                 | Менять owning modules, использовать существующие CI/worker VM; LAN-разнесение позже                                  |
| API и форматы    | Breaking rewrite разрешён; один новый поддерживаемый формат, без adapters, migration и поддержки старых данных                   | Старый формат получает явный `unsupported_format`, а не эвристическую интерпретацию                                  |
| История          | Новая система сохраняет полную компактную scientific history; старые QCL результаты разрешено удалить после read-only R00 оценки | Legacy read/migration и архив старого run не требуются; исторические тексты Git не переписываются                    |
| Физика           | Уравнения, scattering, grids, basis, окна, допуски и независимый reference oracle неизменны                                      | Рефакторинг не получает право менять научную постановку ради зелёного статуса                                        |
| Ресурсный proof  | **Р:** удалить незавершённый `campaign_strict` из первой устойчивой версии                                                       | Сначала inventory callsites; обычные memory admission и Slurm/systemd/cgroup caps остаются                           |
| Проверки         | Своевременные targeted checks и full CI по затронутому source/риску                                                              | Не переносить прежние «три попытки» и «единственный CI» как новые счётчики продукта                                  |
| Ресурсы          | Все доступные owned CPU/RAM по свежему измерению после reserves                                                                  | Нормальные timeouts, output limits, stop rules и защита других VM сохраняются; специального ручного мини-бюджета нет |
| Обновления       | Совместимые web/docs обновляются отдельно, без остановки science                                                                 | Maintenance может перезапускать owning services; VM power-off — только emergency или явная OS need                   |
| Постоянные VM    | Нет плановой preemption, eviction или выключения VM ради ресурсов                                                                | Idle RAM возвращать native memory mechanism; нехватка capacity означает wait/reject                                  |
| Hard update      | Не является wipe и не разрешает удалить mutable state                                                                            | Диски данных, AiiDA/PostgreSQL, NFS и backups имеют собственный lifecycle                                            |
| Восстановление   | После аварии controller/AiiDA автоматически продолжает exact checkpoint нового формата после проверок                            | Один recovery owner; никакого параллельного Slurm requeue или retry несошедшейся физики                              |
| Приёмка          | Новые synthetic fixtures и infrastructure scenarios; scientific run отдельно                                                     | Process exit, engineering readiness, convergence, physics и validation остаются разными свидетельствами              |

Эти решения заменяют противоречащие им будущие действия из старого entrypoint: CI↔science handoff
через остановку VM, обязательную отмену всей очереди перед любым application update, wipe как
обычное обновление и фиксированные retry счётчики. Сами исторические заметки и их failed receipts не
переписываются. До нового поручения этот документ остаётся reviewable планом, а не командой
применить новые правила к действующему серверу.

Дополнительные **Р** от 2026-10-27:

- Полная компактная scientific history сохраняется; technical detail — по необходимости.
- Общие лимиты исследования в ядро-часах и расходуемый campaign CPU grant удалить из целевой модели
  полностью, не откладывать. Resource allocation, защита host, numerical stopping criteria и
  timeouts управляющих операций — другие механизмы. CPU/core-hours остаются измерением стоимости, не
  разрешением на продолжение.
- Телеметрия нужна прежде всего для long-run технического анализа bottlenecks; экран текущего
  состояния вторичен. Не дублировать Proxmox графики без потребности.
- Фиксированный overhead gate 1% не принят. Влияние должно быть разумным по измерениям и пользе
  данных; дорогой verbose/profile включается отдельно.
- Эффективность достигается внутри прозрачных модулей и публичных API; обход границ и скрытые
  hot-path зависимости ради ускорения не допускаются.

### Принятое удаление незавершённого strict режима

`campaign_strict` — дополнительный режим подтверждения ресурсов, а не физическая модель. В
исследованном Runner его
[`_scientific_resource_preflight`](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/8264f48c01ccc524548036d4b3f44552a76f19b5/src/composition/native_phase_telemetry.jl#L247)
отклоняет запуск из-за отсутствующих bindings; это не описание поведения обычного `standalone` пути.
[Действующая заметка политики](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/d395044ac09b28c2ff573724f8911d625df43bf5/docs/implementation/review-closure-2026-10-19/resource-policy-2026-10-24.md#L13)
также не объявляет strict принятым. Пользователь 2026-10-27 подтвердил удаление незавершённого пути.
P13/P14 выполняют inventory и removal, сохраняя обычный memory admission, Slurm/cgroup limits и
проверку физики.

## 3. Паспорт исходных свидетельств

Исследованный опубликованный candidate — root
[`d395044ac09b28c2ff573724f8911d625df43bf5`](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/d395044ac09b28c2ff573724f8911d625df43bf5),
[PR #35](https://github.com/Afonenko-QCL-NEGF/qcl-negf/pull/35). Отчёт Platform опубликован в
[PR #32](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/32), head
`1a1341001ac4ccbb6b07ad254aabaa45c2532ce9`. Это source/report locators, а не подтверждение
установленного runtime. Локальный checkout при подготовке —
`93880c23bca889ddcb8b98edb995080b332dd99f`; его gitlinks старее и не объявляются составом candidate.
Локальный status содержал unrelated untracked review directory; её содержимое не менялось.
`git status` предупредил о недоступном `.sentry-native/`; содержимое этого каталога не проверялось.
Приведённые ниже commit citations фиксируют происхождение findings, не создают параллельный source
lock; состав выбранного релиза выводится из Git.

| Ф   | Source locator и наблюдение                                                                                                                                                                                                                                                                                                                | Что этим ещё не доказано                                                                                                                       |
| --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| F01 | Platform `1b1370d2b8e83a267a97c8d49df14db220123478`, `ops/application_release.py:1362–1387`, `fleet_health:2608`, post-RESUME `3046–3053`: `check` проверяет два Nix outputs и self-check; вызовы повторяются                                                                                                                              | Wall time и выигрыш от удаления повторов не измерены; immutable qualification и mutable health нельзя смешать                                  |
| F02 | Core `0df7dd5a481c2c339e8520d2291c035253e7c0e2`; Runner `8264f48c01ccc524548036d4b3f44552a76f19b5`, `src/core_api.jl:98–376`: bridge импортирует 278 private Core symbols; `production_workflow.jl:562`, `_completed_restart_solution` собирает scientific result через helpers                                                            | 278 exports не являются правильным публичным API; корректность результата требует owning Core assessment                                       |
| F03 | Portal `104481fdce8e11c9734b8b5b0f2743c9e5760151`, `model_help.py:7` использует private validator; Contracts `41209389109d387912b0410a5244dbc29ff1ff42` уже имеет публичный schema API                                                                                                                                                     | Новый schema service и ещё одна копия схемы не нужны                                                                                           |
| F04 | AiiDA `7f4223eaff86b3a6104743098162ffa3fc4e0334`, `service.py:get_run:398–437`, selection helper `89–111`: повторный обход children и plan; Portal `main.tsx:290–309` опрашивает каждые 10 s                                                                                                                                               | Частота polling сама по себе не доказывает bottleneck; нужен счётчик обращений и время той же операции                                         |
| F05 | Results `f811d7c43bef8a70eb79ef74d554f08496a9af1c`: constructor reader state и export context повторяют hashes; brief/slices/NFS provider уже существуют                                                                                                                                                                                   | Нельзя проектировать эти возможности как отсутствующие или обещать безопасное удаление всех hash checks                                        |
| F06 | Runner `8264f48…`, `scientific_history.jl:132–264`: HDF5 segments уже есть, index переписывает полный список; `consolidate_scientific_history!:322`, `point_artifacts.jl:788–927` повторно читают/сортируют history при commit. `scientific_execution.jl:1109–1192`: outer snapshots default analysis=true, checkpoint_sink analysis=false | Сегментацию не нужно изобретать; влияние copies/I/O на production peak RAM и wall пока не измерено                                             |
| F07 | Runner `8264f48…`, `configuration.jl:1757`: raw/typed/runtime представления конфигурации; root `d395044…`, `flake.nix:15` связывает `metadata.sources.revision == self.rev`, application использует `self.outPath`                                                                                                                         | Изменение документации не обязано менять scientific identity или все runtime derivations                                                       |
| F08 | Platform `1b1370d…`, `nix/application.nix`, postInstall: версии четырёх Python packages приравниваются root version; `apiStart:64–121` содержит embedded logic                                                                                                                                                                             | Совпадение версий не заменяет dependency compatibility; перенос logic не разрешает потерять argv/runtime inputs                                |
| F09 | Root `d395044…`, `ops/ci.ts`, workflows `full`/`runner-smoke`: грубые python/julia/infra группы, docs внутри Julia; `ops/docs.ts` — 2546 строк; `nix/docs.nix` запрещает substitutes                                                                                                                                                       | Размер файла не доказывает стоимость; сначала измерить build/reuse и сохранить offline math/fonts/search                                       |
| F10 | Среди шести исследованных repositories два standalone shell files, 8362 bytes: root `d395044…`, `ops/transfer-github.sh` — 7893 B; Runner `8264f48…`, `nix/launcher.sh` — 469 B. Embedded logic видна в Platform `nix/application.nix:apiStart`, root `ops/ci.ts`/`ops/docs.ts`                                                            | Количество shell files не описывает orchestration complexity; новый deploy framework не обязателен; меньше строк не доказывает эквивалентность |
| F11 | Root docs: 1547 файлов, из них 1511 под implementation; Portal README `195–207` отстаёт от `tools/asset-receipt.mjs`/`hatch_build.py`, `150` противоречит native cards `250`; Results README `97` содержит старые Runner lines; Platform `application-cd.md:89` неверно описывает oneshot timeout                                          | Число файлов не разрешает удаление истории; исправления нужны вместе с owning code/docs PR                                                     |

Дополнительные факты углублённого source review:

- **F12:** Results `f811d7c…`, `capture.py:169–259`, `journal_batch` перечитывает и SHA-хеширует
  весь обработанный prefix при reopen, затем читает новый tail; `capture_point:744–780` учитывает
  повторные bytes в lifetime credits. Это ещё один механизм растущего I/O; production overhead не
  измерен.
- **F13:** Results `capture.py:799–825` реально вызывает `TelemetryWriter` и `record_resource`;
  AiiDA `7f4223…`, `calculation.py:162–169` передаёт capture spec. Старая skill source map об
  отсутствии production caller к этому source неприменима. `ingest_spans` flush делает на каждом
  harvest; `stage_spans` уже поддерживает batch/cursor commit. `telemetry.py:515–528` уже имеет
  incremental catalog, его не нужно проектировать заново.
- **F14:** Runner `native_phase_telemetry.jl:121–129` синхронно открывает/пишет/ flush/closes JSONL
  и заменяет current snapshot на каждом begin/end. Отдельный `ScalarTelemetrySender`
  bounded/asynchronous, но до enqueue копирует и сериализует scalar tree; он не устраняет native
  journal I/O.
- **F15:** Platform `1b1370d…`, `modules/monitoring.nix:11–49`: node exporter и Vector collector
  optional, default disabled; Vector file sink best-effort, memory buffer/drop_newest/без
  acknowledgements. Наличие модуля не доказывает installed coverage. `cluster.nix:65–66` включает
  cgroup job accounting, но конфигурация sampler не доказывает доступный terminal accounting
  backend.
- **F16:** Portal `104481f…`, `api.py:714–747`: automatic resources подставляет административные
  maxima, это не оценка Runner. `model_help.py:33–63` used-value binding пока unknown/empty. AiiDA
  `research_cards.py` и `run_structure.py` уже реализуют cards/versions/reports/graph: эту семантику
  нужно сохранить.
- **F17:** Platform `modules/application.nix:78,98–105` связывает runtime savedResults/configurator
  с compile-time package/solver/catalog. Это расходится с независимым app update; bindings нужны в
  validated release descriptor. `modules/release.nix:6–26` устанавливает management CLI через OS:
  первый переход на новый delivery tooling требует отдельной установки capability.

Дополнительные исходные **наблюдения пользователя**, пока без нового native receipt: idle ballooned
VM имела мало guest `MemAvailable`, поэтому estimator не пускал job при доступной host RAM; при
превышении host capacity QEMU VM погибала от host OOM без достаточного объяснения в рабочем
интерфейсе. Это обязательные regression scenarios, а не уже доказанный диагноз каждого исторического
отказа. Distributed-memory solver в программу не входит.

## 4. Целевая архитектура и contracts

### 4.1. Один scientific contract и узкий Core API

**К:** Core владеет восстановлением in-memory state и scientific assessment; Runner владеет файловым
checkpoint, plan и execution. Предлагаемый публичный набор по смыслу: validate/restore exact solver
state, assess completed state, получить typed diagnostics. Не экспортировать 278 внутренних функций.
Core не зависит от файлового формата, AiiDA, Platform или Portal. Новые signatures, types и отказ
при неполном состоянии утверждаются в P02. Runner не конструирует «принятый» scientific result из
private helpers. Independent reference oracle сохраняется отдельным путём; общий helper
optimized/reference не становится единственным доказательством.

Observation API задаёт ownership/lifetime: scalar record — immutable value; научные vectors имеют
явный snapshot/transfer contract и не являются изменяемым view в workspace solver. Нужная копия
делается один раз на границе владельца, без копирования Green/Sigma на каждый technical event.
Consumer не читает private поля Core и не продлевает жизнь больших buffers случайной ссылкой в debug
payload.

До P01/P02 согласовать короткий semantic sketch: Core определяет полный exact state/assessment,
Contracts — файловую оболочку и validation. P02 реализуется без зависимости от Contracts package;
P01 фиксирует формат после определения Core state. Сериализация принадлежит Runner; формат не
диктует Core неполный state. Это снимает semantic circularity, не требует нового общего
архитектурного проекта.

**К:** resolved configuration — один immutable snapshot с physical/numerical values, units,
effective origins и identity. Raw input нужен для объяснения, а не как второе изменяемое runtime
state. Формы, YAML и CLI разрешаются к одному snapshot; unknown fields и conflicts — явная ошибка до
submit. Изменение orchestration/package identity не меняет model identity молча.

### 4.2. История, checkpoint и независимое чтение

**К:** Contracts задаёт новый versioned manifest, identity, statuses, checkpoint declaration и
public schema API. Новый writer/reader поддерживает только этот формат; несовместимые старые данные
остаются в архиве. Brief, bounded slices, full manifest и NFS source используют существующие Results
primitives с одним source/locator, без повторных retrieval branches. Read не запускает solve или
implicit expensive derive.

**Р:** сохранять полную компактную научную историю; большие solver states — в checkpoint и финале;
подробные технические события — по необходимости. Это не разрешает удалять scientific evidence,
требуемое Core assessment/reference oracle.

**Ф:** Runner уже пишет закрытые HDF5 segments и `index.json`; Results уже читает выбранные
segments. Переписывать writer с нуля не нужно. Лишняя работа возникает при eager consolidation всех
segments в каждом artifact commit; outer snapshots дополнительно могут строить analysis. Обычный
checkpoint sink передаёт `analysis=false`, поэтому утверждение «analysis строится в каждом
checkpoint» неверно.

**А:** сохранить существующий сегментный HDF5 путь, обновив manifest contract. Рассмотренный HDF5
SWMR требует отдельной filesystem qualification и усложняет публикацию нескольких datasets; для
первой устойчивой версии не выбран.
[HDF Group: SWMR](https://portal.hdfgroup.org/documentation/hdf5/latest/_s_w_m_r_t_n.html) описывает
требования к write ordering. Выбор не меняет физику или numerical state.

| Тип записи                      | Владелец смысла / записи          | Содержание и сохранность                                                                                                                                                                                                                                 |
| ------------------------------- | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Научная история                 | Core / Runner                     | Каждый записанный SCBA/outer шаг: counters, residuals, observables, assessments, units, missing reasons; outer populations/density не теряются. Сохранять принятую Core policy diagnostic witnesses, не превращать debug switch в scientific gate switch |
| Exact checkpoint                | Core state / Runner persistence   | Полный exact state, определённый публичным Core contract, identities и ссылки на историю; не анализ всей траектории                                                                                                                                      |
| Оперативный progress            | Runner                            | Небольшой заменяемый snapshot с revision/sequence; не источник scientific truth и не способ восстановить state                                                                                                                                           |
| Performance baseline            | Runner counters + Results capture | CPU/GC/allocations/I/O/wait/coverage и фазовые агрегаты; отдельный technical dataset                                                                                                                                                                     |
| Verbose trace/profile           | Owning producer + Results         | Явно включаемое diagnostic window с ограниченными buffers/storage; отсутствие trace не означает отсутствие события                                                                                                                                       |
| Deployment/stop/failure receipt | Platform/AiiDA                    | Компактная durable запись действия и неопределённого исхода, включая source/request/host/attempt identity; scientific history её не заменяет                                                                                                             |

Публикация: записать новый segment → close/sync → publish leaf → publish immutable catalog
generation → заменить малый current pointer. Checkpoint публикуется после всех зависимостей и
содержит точную generation/hash и sequence cutoffs. Normal finalize flush сохраняет всю научную
историю; после аварии гарантирован последний committed checkpoint/manifest, незакоммиченный хвост
может быть потерян и не объявляется сохранённым. Worker loss не равен потере storage host; backup —
отдельно.

Не использовать directory glob как authoritative list. Orphan после сбоя между rename и manifest
остаётся невидимым reader; salvage выполняется явно после validation. При неизвестном результате NFS
rename нужен readback/reconciliation. История после checkpoint и повторённые resume шаги получают
attempt/parent-state/ branch identity; нельзя склеивать их только по номеру внутренней итерации.

Append и checkpoint не перечитывают старые payload и не пересортировывают всю историю. Текущий
полный список `recorder.segments` в каждом index update заменить малой pointer + incremental catalog
pages по уже существующему в Results образцу. Pages содержат ranges/counts/new leaves и previous
reference; checkpoint pin имеет постоянный размер. Compaction не удаляет scientific leaves, на
которые ссылаются retained checkpoints/history; technical retention отдельно сообщает coverage.
Bounded reader читает нужные pages/leaves, pagination не требует загрузки всех arrays. Полный
consolidated export — явная потоковая операция; периодический read index допустим отдельно от
scientific checkpoint. Не строить собственную универсальную database/LSM систему ради этого формата.

Hash verification назначается на границу import/open immutable source, доверенный handle
переиспользуется внутри одной bounded операции. Смена source/size/identity, повреждение или новый
untrusted handle требуют повторной проверки. `not_measured`, missing и failed не превращаются в
pass.

### 4.3. Qualification отдельно от health и read projection

**А:** qualification относится к owning artifact, а health — к текущей активации. Qualification key:
node/enrollment identity + artifact narHash/derivation + native contract version + relevant
environment signature. Health binding: activation revision + boot/service generation +
endpoints/mounts + Slurm/capacity. Не включать общую activation generation в solver qualification
key: compatible Portal update не инвалидирует неизменённый solver. Restore, corruption, потеря
доверенного receipt или релевантная смена kernel/driver инвалидируют применимое свидетельство.
Status/RESUME выполняет cheap mutable health. Integrity audit — явная операция при подозрении, а не
повторный full verify по каждому poll.

**А:** AiiDA даёт краткую read projection с revision/status/children summary; plan/artifact
traversal выполняется по запросу деталей или новой revision. Polling дешёвый, без записи в
scientific state; ETag/revision caching инвалидируется state transition и не скрывает failure. Новый
database, event broker, global research cache или evidence ledger не вводятся. Portal использует
публичный Contracts API и этот read contract.

### 4.4. Packages, CI, docs и простые entrypoints

**К:** native package versions независимы; compatibility задаётся declared dependencies и lockfiles,
integration — gitlinks. Принудительное равенство четырёх Python version root version снимается с
проверкой совместимости. Nix filesets ограничивают inputs owning runtime; docs edit не меняет solver
closure. Source metadata сообщает фактическую provenance, не заставляет каждый unrelated root commit
пересобирать весь application workspace.

**А:** impact map выбирает targeted checks и native packages по changed paths и dependency edges,
неизвестное влияние выбирает полный соответствующий gate. Docs — обычный cached CI package на
существующей VM; сохранить offline fonts, math, search и light theme. Не вводить отдельную docs VM
или cache ledger. Повтор full CI нужен после затрагивающего source изменения/неустранённого failure;
CSS/docs edit не требует full scientific release перед каждым действием.

Orchestration Python/TypeScript выносится из Nix в owning small helpers; `writeShellApplication`,
`runtimeInputs` и безопасный argv остаются. Bounded subprocess runner общий в owning orchestration,
с timeout/output cap, return code и сохранением original log. Standalone Core не зависит от
Platform. Native Nix/systemd delivery — исходный выбор; `deploy-rs` допустим только если короткое
сравнение показывает удаление собственного кода без потери contracts.

### 4.5. Прозрачные модули и один developer loop

**А:** единый цикл: edit owning component → docs/static check либо targeted contract fixture →
owning PR → compatible root gitlink → требуемая integration/ native проверка. PR не является поводом
заново bootstrap всю систему. Full CI проверяет release composition и изменения с широким влиянием;
повтор оправдан изменённым source/failure, не формальным количеством PR. Unknown impact выбирает
полный соответствующий check, а не скрытый install/precompile во всякой команде.

Проверки четырёх видов: D — текст/формат/ссылки; L — локальный behaviour contract; N — реальная
package/service/backend проверка; S — отдельный научный опыт. Существующие команды маршрутизует
небольшая impact map восьми компонентов и changed paths. Есть явный override; workflow и CLI не
держат две копии этой map. Ручные группы проще сначала, но сохраняют риск пропустить dependency;
поэтому выбрана map без нового CI framework.

Root AGENTS содержит routing, владение, физические инварианты и границу этапов. CONTRIBUTING — один
поддерживаемый developer loop. Skills — метод анализа, не второй deployment policy. Bootstrap детали
и исторический CI-once остаются в своём датированном runbook; их не наследуют обычные новые задачи.
Source maps skills различают исторический snapshot и способ найти current symbol. Проверка
инструкций использует несколько конкретных сценариев docs-only/source-only/ already-authorized
check/old-spec-conflict; новый слой approval не вводится.

| Модуль    | Одна ответственность и публичная граница                                                 | Что исключается                                                                   |
| --------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Core      | Typed numerical inputs, in-memory solve/restore/assessment, небольшие typed observations | Файлы, HTTP, host probes, Contracts package, resource scheduling                  |
| Runner    | Resolve study, execution/point/branch, persistence, event batching, Core adapter         | Private Core imports, самостоятельно выведенная scientific acceptance             |
| Contracts | Wire schemas, versions, identities, units/status/locator envelopes, public validators    | Физические формулы, I/O, scheduler или новый service                              |
| Results   | Independent reader, capture/typed technical storage, bounded derive/export/comparison    | Решение о scientific retry, изменение исходных arrays                             |
| AiiDA     | Persistent execution/provenance, cards/report links, one emergency recovery owner        | Свой solver, повтор Slurm scheduling, campaign CPU credits                        |
| Platform  | Native resources, build/delivery/qualification/health/boot, host telemetry adapters      | Физическая модель, чтение private Runner state для управления                     |
| Portal    | Auth/transport, bounded DTO, формы/графы/представление capabilities                      | Собственный resolver, формулы, raw host paths или повторное ORM traversal по poll |
| Research  | Постановки, model/material/source content, примеры и научный handoff                     | Delivery policy, numerical implementation                                         |

Общие операции выносятся по настоящему владельцу: Platform identity/trust, bounded commands,
qualification, activation, delivery — отдельные модули вместо нового монолита. Results
переиспользует свои atomic I/O/catalog/reader primitives; Runner — свои persistence/segments. Разные
языки не требуют девятого utils repo. JSON Schema остаётся в Contracts; TypeScript types
генерируются, transport DTO не копируют физические правила. Проверка границ ловит private
cross-package imports и неверное направление dependencies, не запрещая полезные internal helpers
внутри владельца.

Порядок выбора инструмента: existing project primitive → native Nix/systemd/ Slurm/backend API →
готовая library → свой узкий adapter. На первую версию выбраны native delivery и existing
capture/segments. deploy-rs profile rollback не заменяет AiiDA/Slurm admission или uncertain
multi-node outcome, поэтому миграция на него сейчас не обоснована. Собственный supervisor заменять
native service только после сопоставления cancellation/child cleanup/output bounds; не удалять
проверенные failure semantics ради уменьшения строк.

### 4.6. Техническая наблюдаемость длинного расчёта

**Р/А:** цель — объяснять wall/CPU/RAM/I/O за длительный execution и всю историю attempts, а не
дублировать Proxmox dashboard. Основной путь — уже подключённый Results capture рядом с заданием,
producer counters Core/Runner и public performance dataset. Новых обязательных
Prometheus/Grafana/Loki/collector VM нет. Существующие Proxmox metrics/graphs/API дают host/VM
контекст; Linux/Hyper-V backend сообщает только реально доступные показатели с capability reasons.
Optional node exporter/Vector не становятся prerequisite solver и не объявляются квалифицированными
по наличию Nix options.

| Слой данных               | Для чего нужен                                              | Минимальный состав и ограничения                                                                                                                                   |
| ------------------------- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Host/VM context           | Конкуренция ресурсов, balloon/OOM, storage/network pressure | Host/VM/boot identity, assigned/actual/protected RAM, available/reserves, CPU allocation/pressure, диски/сеть; native источник, units и coverage сохранены         |
| Job resource baseline     | Длинные интервалы и смена режима работы                     | Cumulative CPU, cgroup/current/peak memory, RSS отдельно, I/O counters, throttling/pressure, allocation, timestamps; нет per-thread stack polling в обычном режиме |
| Producer phase aggregates | Где проходит время кода                                     | Инициализация, solve phases, GC/allocations, admission wait, checkpoint/write/compress/hash/sync/stage/derive; inclusive/nested scope явно отмечен                 |
| Diagnostic window         | Разрешить конкретную неоднозначность                        | Verbose phase events, stacks/alloc profile/hardware counters только по необходимости; результат не подменяет baseline                                              |
| Observer health/self-cost | Понять доверие к данным и цену измерения                    | Probe/parse/serialize/flush time, bytes read/written, buffers, dropped/coalesced counts, lag, gaps, incomplete reason                                              |

Идентичности: host/VM/boot → Slurm job/step/cgroup → execution/point/attempt → producer
session/clock/sequence. Monotonic intervals не смешивать между boot и session; UTC anchors нужны для
корреляции с Proxmox. CPU allocation отличается от использованных CPU seconds; core-hours
показываются как стоимость, без quota. RSS, Julia allocation bytes, anonymous/file cache и cgroup
memory — разные scopes. Job и его steps не суммируются повторно; observed peak не равен
гарантированному физическому пику. Нет sample/phase/counter — unknown, а не ноль.

Baseline поддерживает выводы о CPU occupancy, GC, ожидании, memory pressure и I/O с указанной
coverage. Высокая загрузка CPU сама не доказывает compute-bound, RSS около cap не доказывает
memory-bandwidth-bound. Для bandwidth/NUMA/cache вывода может понадобиться отдельное diagnostic
window; без него — гипотеза. Терминальный Slurm accounting читается только при подтверждённом
configured backend; его отсутствие не заменяется нулевыми TotalCPU/MaxRSS.

**А:** два режима: normal analysis и explicit diagnostic profile. Оба сохраняют одну scientific
history/физическую постановку. Normal analysis содержит дешёвые ресурсные пробы и агрегаты
существенных фаз; подробный begin/end trace не обязателен для каждой матричной операции. Точные
cadence/batch/retention параметры конфигурируются по measured site/workload, не копируются из
старого skill proposal как обязательные числа. Сохранить достаточные интервалы и итоговые агрегаты
для анализа всего long run, включая failed/restarted attempts.

Из numerical thread исключить файловый open/write/flush на каждый event и повторную JSON
serialization одного payload. Core выдаёт небольшой typed record через публичный observer, Runner
группирует и публикует закрытые technical segments; Results capture читает только новые segments и
переиспользует `TelemetryWriter`/batch staging. Cursor и принятые rows публикуются вместе. Проверка
identity/hash выполняется на границе закрытого segment и новой source session; перечитывание всего
prefix при каждом harvest удаляется с сохранением защиты от truncation/replacement. Read position
после restart берётся только из committed cursor, не из потерянного memory buffer.

Оценка механизма до runtime измерения: при линейном росте журнала повторная проверка всех прежних
bytes на каждом harvest даёт сумму порядка `b × (1 + 2 + … + n)`, тогда как incremental reader
обрабатывает новые `b × n` bytes плюс ограниченные metadata. Page cache может убрать physical disk
read, но не повторный hash/parse и memory traffic. Аналогично eager consolidation повторяет работу
над старой scientific history. Это причинная оценка сложности, не измеренный speedup и не
доказательство размера наблюдавшегося RAM excess.

Существующий incremental Parquet catalog переиспользуется. Нынешние lifetime
performance/scalar/processed-byte credits могут выключить capture на длинном run; вместо этого нужны
bounded buffers, разумная storage/retention policy, малые cumulative summaries и явное изменение
coverage. Telemetry storage не должен съедать reserve scientific outputs. При нехватке
места/доступности уменьшать technical detail или отмечать capture incomplete, не тормозить solver и
не выдавать missing за measured. Временно недоступный technical collector не является scientific
failure; ошибка обязательного scientific checkpoint — другой класс. Drop/coalesce запрещён для
обязательных scientific history rows.

**Р:** фиксированного overhead percentage gate нет. Engineering проверка сопоставляет normal
telemetry off/on на одинаковом representative synthetic workload с той же scientific history,
параллелизмом и warm/cold условиями. Смотрит wall/CPU/RSS/I/O, работу observer и объём файлов;
возможный разброс и cold effects показываются. Если влияние мешает полезной работе, сначала убрать
повторы, затем уменьшить cadence/verbose detail. Не вводить тяжёлый benchmark перед каждым PR или
заявлять нулевую стоимость из-за async producer.

Экран мониторинга использует дешёвые Platform/AiiDA projections: VM/services, queued/running jobs,
resource availability/grants, причина wait/failure, current release и свежесть данных. Графики
performance читает Results по bounded query; Proxmox host graphs можно связать ссылкой/native data.
Повторный qualification, full artifact hash или solve по открытию экрана не выполняются.

### 4.7. Исследовательский продукт и конфигурация

**А:** сохранить и довести существующие cards/versions/reports, structure/material editor и bounded
Runner configurator, не создавать новый workflow designer. Публичные DTO по смыслу: resolved study,
run brief, exact attempt selector, artifact/selection locator, action receipt. Имена/signatures
фиксирует owning PR; их смысл и owner не переопределяются UI.

Путь приёмки: цель → короткая форма и versioned protocol → resolved preview/diff → submit → граф
execution/attempt → готовые observables/выборки/явный derive → отчёт человека/агента с ссылками на
exact runs. Человек и внешний агент используют одни исследовательские операции; отключение клиента
не отменяет работу. Mutation timeout после возможной записи означает outcome_unknown и reconcile по
прежнему request ID; автоматический повтор с новым ID недопустим.

Runner один разрешает config и возвращает effective values/units/origins, protocol/material/model
identities, explicit variant diff, execution topology и resource estimate с unknown/confidence.
Автоматические ресурсы не равны подстановке административных maxima. Estimate задаёт заявку,
Platform/Slurm дают реальные ресурсы; неизвестный overhead не ноль и не скрытое упрощение модели.
Отдельный универсальный proof всей кампании не возвращается.

Independent executions допускают параллельность; continuation остаётся внутри Runner execution.
Failed/nonconverged point останавливает зависимую ветку, не становится accepted seed; предыдущие
точки сохраняют assessments, независимые ветки продолжаются. Exact аварийный resume не является
новым научным решением и не повторяет scientific failure автоматически.

Results обеспечивает J(V), populations/maps и сравнение сопоставимых сохранённых вариантов в
пределах фактически сохранённых capabilities. Read, явный derive и новый solve — разные операции; UI
показывает prerequisites и missing data. Большой payload долговременно хранится на NFS один раз;
AiiDA retrieves малые identity/status/manifest/locators/receipts, не дублирующий полный HDF5
archive. Временный bounded spool допустим; retention/права внешних данных принадлежат явному storage
contract. Метаданные AiiDA и backup не считаются лишними копиями scientific payload.

Help различает формулу/модель, источник численного параметра и effective override; привязывается к
used snapshot, доступен человеку и агенту. Canonical content идёт из Core/Research/Runner, UI не
хранит вторую формулу/material resolver. Unknown source допускается как явный исследовательский
вариант. Material editor не выводит новые физические параметры из `x_Al` без owning model rule.

### 4.8. Документация и передача обратно к физике

**А:** для каждого root/component docs набора — current/proposed/history inventory, owner и одна
точка входа. Проверить содержание и runnable examples, не только links; убрать stale instructions из
current route, сохранив исторические receipts. Матрица requirement/прежняя задача → actual
implementation → source/receipt → остаток/отменено показывает результат прошлой сессии и текущей
недели. Она не копирует Git revision lock и не становится новым runtime registry.

Русские manuals покрывают researcher/operator/admin/developer путь; API names английские. Справка и
учебный маршрут выпускаются из owning source, работают локально с math/search/fonts и светлой темой.
Полный новый учебник не объявлять готовым по наличию generated HTML: required content и ограничения
проверяются.

После engineering acceptance подготовлен runnable Research handoff
`config/studies/equilibrium-0-70.yaml`: равновесие опубликованной структуры при 0 mV/period, 70 K, с
сохранённой моделью. Ссылка на [научный контракт S01](../system/scientific-milestone.md) сохраняет
FDR/FD, neutrality/current/discretization checks; фактические readiness/accuracy пробелы не
скрываются. Сам scientific run — отдельное поручение, не недельный gate. Stationary
transport/ВАХ/populations/maps остаются в scope; gain/absorption, мощность, динамика и waveguide не
добавляются этой переработкой.

## 5. Резидентные VM и выдача реальной памяти

### 5.1. Host policy и область гарантии

**Р:** все VM постоянно resident; idle CPU мал, idle CI RAM возвращается через native
balloon/dynamic memory после квалификации фактического образа. Нельзя уменьшать RAM ниже active
job/build grant или убивать другую VM. Нельзя приравнивать virtual maximum, guest reclaimable pages
или configured Slurm memory к гарантированно доступной physical host RAM.

**А:** отдельный administrator policy file на каждый host задаёт owned VM,
`minimum/startup/maximum`, CPU/memory weights, host/control/foreign reserves, owned capacity pool,
timeouts и поддерживаемый active-grant mechanism. В public repository — schema и пример с
переменными; реальные inventory, addresses, capacity measurements, credentials и administrator
permissions private. Эта policy не новый scheduler/daemon и не ручной lock source revisions.
Per-host mutation имеет одного владельца в существующем Platform entrypoint через native host API.
Межхостового распределённого memory algorithm нет.

Соглашение с администратором чужого Proxmox определяет доступный owned pool, минимумы, reserves и
право удерживать grant. PVE Resource Pool — grouping, не физическая гарантия RAM. Локальная
блокировка QCL защищает только cooperating QCL calls, не foreign administrator или произвольные VM.
Без enforceable capacity agreement/caps такой host не принимает новую нагрузку: wait/reject, а не
оптимистичный admit.

**К:** per-host admission в bytes удовлетворяет `H + F + Σ(B_i + O_i) ≤ physicalRAM`. `H` — host
services/storage/safety reserve; `F` — согласованный максимум foreign VM, включая future
starts/growth и overhead; `B_i` — полный QCL guest grant, включая resident idle floor; `O_i` —
QEMU/VM overhead. Новый полный grant учитывается **до** growth, даже если его страницы ещё не
resident. `MemAvailable` — дополнительный pressure gate, а не основание дважды вычесть `ΣRSS`;
virtual max не подставляется вместо physicalRAM. Неизвестные reserves/overhead не считать нулём.
Числа определяет inventory.

### 5.2. Proposed per-host protocol

**А, требует native qualification:**
`REQUEST → HOST_GRANT → GROW/readback →
GUEST_ADMIT → RUN/protected grant → SHRINK/readback → RELEASE`.

1. REQUEST сообщает ресурсный demand job/build, host/VM identity и timeout. Низкий idle guest
   `MemAvailable` не блокирует сам запрос памяти.
2. HOST_GRANT сверяет свежую host capacity, reserves и все действующие grants; существующий Platform
   entrypoint под per-host lock сохраняет полный grant в небольшом durable receipt/VM metadata либо
   возвращает wait/reject. Новой базы или постоянно работающего scheduling daemon нет.
3. GROW применяет native memory settings и ждёт подтверждения host и guest. Requested/configured
   memory не равно фактически полученной. По timeout job не запускается; ambiguous host change
   остаётся charged до reconcile.
4. GUEST_ADMIT после grow сверяет actual guest capacity, measured guest OS reserve и task/build
   cgroup/Nix/Slurm limits внутри grant. Превышение одним job ограничивается внутри VM; Slurm
   capacity не превышает RAM после guest reserve. Выбор до dispatch или launch wrapper — owning PR,
   но resource request всегда предшествует guest `MemAvailable` rejection.
5. RUN удерживает grant до окончания всех дочерних процессов и durable output; планового shrink во
   время active work нет. Host pressure закрывает новый admission; idle memory других owned VM можно
   вернуть без их остановки.
6. SHRINK после завершения/проверенной cleanup возвращает measured idle floor; только подтверждённый
   readback позволяет RELEASE capacity. Timeout/TTL не отзывает active grant. Crash/reboot не
   разрешает сразу переиспользовать неизвестный grant: сначала reconcile identity, memory state и
   отсутствие живой нагрузки. Config, QMP и grant не atomic: частичный переход остаётся charged до
   однозначного восстановления.

**А, native PVE path:** для managed resident roles заранее provision enabled balloon device,
`shares=0` (manual balloon), `memory=upper cap`. Existing Platform CLI читает
`GET config?current=1`, затем отправляет `PUT config` с `balloon={grant_MiB}` и `digest`, читает
`GET status/current` и проверяет `status.balloon`, затем guest readiness. Native API выполняет
online balloon update; отдельный raw-QMP client не нужен. QMP `query-balloon.actual` — logical guest
memory, не physical reservation. Сериализация/digest защищают наши competing changes, capacity
agreement защищает host budget; ни одно из них не заменяет другое.

На первом этапе одновременно действует один grant mutation на host; Slurm и native Nix limits
распределяют выделенную гостю нагрузку дальше. Перед native stage P19/P20 должны определить crash
reconciliation, защиту active floor и наблюдаемые readbacks для конкретного backend. Если native API
не обеспечивает active-floor invariant, объявить unsupported динамический режим и использовать
проверенный conservative reservation, сохраняя resident VM и wait/reject; не обещать memory
overcommit без OOM.

### 5.3. Что подтверждают внешние источники

Proxmox документирует automatic memory, shares и CPU weights `cpuunits`; native balloon при pressure
может привести к guest swap/OOM. Это не гарантия active grant. Источник:
[PVE qm, `qm_ballooning` и resource limits](https://raw.githubusercontent.com/proxmox/pve-docs/master/qm.adoc).
Online manual balloon/readback проверен по source
[`PVE::QemuServer`, commit `71ea0ac…`, около L4659](https://github.com/proxmox/qemu-server/blob/71ea0ac7192bb935f63cb64beb59e87d6cecd3bf/src/PVE/QemuServer.pm#L4659).
Automatic `shares>0` не выбран для demand path: у исследованного official
[pvestatd source `299fddc…`](https://github.com/proxmox/pve-manager/tree/299fddc2c0b39d98032f05d2f21867e08747dfc8/PVE)
номинальный цикл 10 s и growth cap 100 MiB/pass. Это source observation, не версия установленного
PVE, не измерение latency и не обещание ETA. Microsoft документирует `DynamicMemoryEnabled`,
`MinimumBytes`, `StartupBytes`, `MaximumBytes`, `Priority` в
[Set-VMMemory](https://learn.microsoft.com/en-us/powershell/module/hyper-v/set-vmmemory?view=windowsserver2025-ps).
Это capability API, а не qualification NixOS guest; успешная Ubuntu VM не доказывает поддержку
конкретного NixOS image. Чужие примерные минимумы не копируются в site config. Реальные idle
floor/grant overhead измеряются.

Обязательные native regression cases: из idle low-RAM VM запрос дорастает и запускает job;
конкурирующий pressure не убивает QEMU/guest и не отзывает active grant. Проверять actual image,
hypervisor/guest driver versions, host/guest RSS/available/assigned memory, cgroups, grants и stop
reasons. Различать host kernel kill QEMU, guest task cgroup OOM, `systemd-oomd` и unknown VM loss.
Bounded persistent host journal и receipt сохраняют host/VM/time/QEMU PID/grant/pressure до AiiDA
emergency resume, вместе с guest/Slurm reason. Без host logs прежняя причина остаётся неизвестной;
отсутствие логов — failure наблюдаемости, не «ничего не произошло». Platform владеет per-host grant,
AiiDA запрашивает ресурс и recovery, Slurm владеет очередью/cgroups; второго scheduler в AiiDA нет.

Для ограничения task/build RAM использовать существующий механизм
[`memory.max` и `memory.events` cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html): он
ограничивает группу процессов, но не резервирует RAM физического host. Сохранность host logs
проверять через штатный
[journald: `Storage=persistent`, `SystemMaxUse`, `SystemKeepFree`](https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html),
с ограниченным объёмом и retention; отсутствие guest log не исключает host OOM.

### 5.4. CPU/RAM operation и связь со Slurm

**А:** одна Platform resource operation показывает desired/current/effective CPU/RAM, affected
limits и необходимость maintenance; её применение не является application deploy и не запускает
solver qualification при неизменённом artifact. Изменение native backend сохраняется в owning
private site resource policy; следующий declarative apply не должен молча откатить его. Уменьшение
ресурса ниже живой allocation запрещено; unsupported online change сообщает конкретную maintenance
need, не останавливает VM автоматически.

Slurm остаётся единственным владельцем выбора worker и allocation. Перед стартом scientific process
launch adapter запрашивает protected grant для уже выбранной allocation и делает guest admission
после grow. Ожидание host capacity видно как отдельная resource-wait стадия, не scientific failure;
Julia ещё не запущена. Настроенная Slurm capability — не разрешение использовать негарантированную
RAM. Native acceptance отдельно проверяет slurmd registration/resource reporting у idle ballooned
guest: если backend не поддерживает этот путь без deadlock или ложной capacity, worker использует
подтверждённую фиксированную reservation, а dynamic memory остаётся unsupported для этого backend.
CI grow перед build проверяется отдельно и не зависит от scientific scheduler.

Disk readiness учитывает совместный peak store/depot/build/tmp/images/staging, thin-pool metadata и
свободное место на guest/host/NFS. Старые «100 GiB» и размеры swap не считаются актуальным
измерением. Telemetry/log storage имеет отдельный reserve/retention и не вытесняет scientific
outputs; swap не physical capacity.

## 6. Обновление, recovery, backup и portable worker

**А:** release descriptor выбирает совместимые management/application/solver/docs artifacts, public
contract/capability versions и runtime bindings. Root Git SHA фиксирует composition/provenance, не
является приказом пересобрать каждую closure. Работающее задание pin-ит свой runtime; GC не удаляет
используемую closure. Nix задаёт users/mounts/security/static service envelope, а package/catalog
feature bindings читаются из validated descriptor вместо compile-time root workspace.

| Процедура             | Что меняется                                                  | Что проверяется и как заканчивается                                                                                                                 |
| --------------------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Soft application/docs | Только совместимые owning services/assets                     | Relevant artifact qualification + cheap health; synthetic job продолжает работу; unchanged solver не self-check заново                              |
| Maintenance           | Несовместимый owning API/runtime/service contract             | Закрыть новый admission affected scope, дождаться safe boundary/завершения jobs, activate/health/commit; ручная отмена только по отдельному решению |
| Hard OS/driver update | Заранее собранная owning NixOS role, явный необходимый reboot | Сохранить data volumes, проверить boot/mounts/secrets/network/native capability; неизвестный исход не открывает admission                           |
| Resource change       | CPU/RAM/backend и соответствующие guest/Nix/Slurm limits      | Native readback + guest capacity; application release не меняется                                                                                   |
| Restore               | Coordinated mutable dataset и нужные identities               | Consistency на копии; app rollback не подменяет rollback PostgreSQL/repository                                                                      |

Первая установка нового management tooling — отдельный migration step без legacy adapter: capability
probe до mutation, затем доставка exact management closure. Application update не предполагает, что
baked-in OS CLI уже умеет новый протокол. Доставка выполняется отдельной systemd service на
controller с durable request/ attempt identity; client запускает/читает operation, его отключение не
отменяет её. Scope service, не caller-owned transient scope; restart controller вызывает
reconciliation pending record, а не успех по пропавшему process.

Operation receipt содержит request/attempt, затронутые identities/artifacts, phase/outcome и ссылку
на original failure log. Он не копирует полный inventory, source tree и scientific arrays на каждом
шаге. Read-only status не дописывает неизменённые snapshots в journal. Подробные command logs нужны
для failure/debug; normal operation использует compact bounded metadata.

Prepare → activate owning generation → health → commit. Выбор поколения на node может быть atomic,
перезапуск нескольких services/nodes — нет. Partial activation, network timeout и потерянный ответ
дают outcome_unknown; admission остаётся закрыт для затронутой функции до readback/repair. Rollback
меняет только подтверждённые immutable artifacts; mutable state не откатывается автоматически. Не
возвращать старую обязательную отмену всех workflows/queue ради каждой web правки.

Boot readiness не зависит от порядка старта VM: state mounts → secrets/Munge/ PostgreSQL/NFS →
Slurm/AiiDA → API и worker admit. Существующие systemd dependencies переиспользуются; network-online
сам не доказывает доступность удалённого NFS или controller. Проверить задержанные dependencies,
service failure/retry и current release binding после штатной перезагрузки. Гипервизорный autostart
не заменяет эту readiness. Работать локально можно с установленными и заранее staged artifacts при
недоступном GitHub; новые Actions jobs/неподготовленный build offline не обещаны.

После fault controller/AiiDA — единственный recovery owner. Он проверяет failure class, exact
checkpoint completeness, code/model/plan identity, storage integrity и fresh capacity/grant, затем
создаёт связанную attempt. Тот же recovery event идемпотентен. Scientific nonconvergence/failed
physics не автоматически retry; partial data и причина сохраняются. Slurm не requeue тот же
scientific attempt вторым механизмом.

Один qualification сценарий normal restore проверяет controller PostgreSQL и AiiDA file repository
как coordinated dataset, нужные NFS manifests и enrollment identity. Restore не требует делать
полный backup перед каждой CSS/docs правкой. RPO/RTO, retention и backup location задаются private
site policy; NFS, binary cache и immutable image не заменяют backup mutable state. Restore drill
выполняется на копии в изолированных временных paths/ports существующей CI VM: отдельные
PostgreSQL/repository и проверяемый AiiDA profile, без замены live dataset и без новой dev VM. Это
проверка восстановления данных; восстановление целой VM после потери host учитывается отдельно.

Portable worker — один понятный install/enroll contract с backend-specific image/driver details.
Сначала простая русская ручная инструкция, затем автоматизация тех же шагов: import/install →
explicit controller/NFS endpoint → trusted enrollment → DRAIN → capacity/release/storage smoke →
reboot identity → RESUME. Stale/duplicate node identity отклоняется; секретов в image нет. Новые dev
VM не нужны. Сохранить простой путь добавить LAN worker позднее.

## 7. Реестр небольших owning PR

Ниже **А:** 32 review units, а не команда открыть их сейчас. Один PR может быть отвергнут без отката
соседнего независимого PR. В каждом — owning docs, failure fixture, output checks и limitations;
root gitlink обновляется после публикации component commit. Указанные files/symbols — границы
работы, не гарантия, что номера строк сохранятся. Dependencies относятся к contracts; независимый
design/fixture preparation может идти параллельно.

Вид проверки: **L** — дешёвая local fixture/static/native-package проверка; **N** — реальный
Linux/libvirt или installed native scenario; **H** — native этап после человеческой подготовки
другого host. L не доказывает N/H, synthetic fixtures не доказывают научную сходимость.

Приоритеты внутри полной недельной программы:

- **P0 — критический путь:** P02/P01 задают узкие contracts; P03–P07 дают проверяемые данные и
  recovery; P11/P12 и P19/P20 убирают дорогой повторный admission и закрывают два memory failure
  scenarios. Затем P21–P23/P27 доводят изменение до установленного существующего кластера и Linux
  worker.
- **P1 — параллельное упрощение:** P08–P10 — быстрый read path и рабочий GUI; P15–P18/P26 —
  независимые packages, CI/docs и русские руководства; P13/P14 удаляют незавершённый strict путь.
  P28 обновляет инструкции; P29/P30 — normal analysis, P31/P32 — наблюдаемость. Это часть готовой
  системы этой недели, а не необязательный backlog.
- **P2 — условные внешние этапы:** P24/P25 начинаются после Linux gate и человеческой подготовки
  hosts.

| PR / owner    | Scope и выдаваемый contract                                                                                                                  | Depends                                           | Конкретная приёмка / вид                                                                                                                                    |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P01 Contracts | schemas/public validators и generated TS types; новый manifest/catalog/cursor, identities/statuses/locators и checkpoint declaration; README | P02 semantic state/event definition               | Новый fixture читается; unknown fields/version отвергнуты; schemas не содержат physics rules; L                                                             |
| P02 Core      | public restore/assessment и small typed observation API; Core не зависит от файлового I/O/Contracts                                          | Общий semantic sketch                             | Synthetic exact-state roundtrip, incomplete state fail; independent oracle; disabled/normal/diagnostic observation не меняет scientific contract; L         |
| P03 Runner    | resolved snapshot/origins/protocol diff и честный resource estimate; common CLI/YAML/form semantic binding                                   | P01                                               | Одинаковые resolved inputs/identity; unknown/conflict fail; automatic resources не подмена maxima; L                                                        |
| P04 Runner    | reuse scientific segments; incremental catalog, checkpoint pin/cutoff без eager consolidation; outer vectors и attempt lineage               | P01, P02, P03                                     | Append/checkpoint не читают прошлые payload; crash/orphan/cutoff/duplicate cases; полный scientific history и exact resume; L                               |
| P05 Runner    | `core_api.jl`, `_completed_restart_solution`: перейти на узкий public Core, удалить private bridge                                           | P02, P04                                          | Import boundary check и fixture assessment равны owning Core result; private symbols не нужны; L                                                            |
| P06 Results   | reuse segment/NFS readers и verified handle; one-format bounded read, явный streaming derive/export/comparison; README                       | P01, P04                                          | Один locator; bounded slice не full array; tamper/new identity detected; явный derive и capability missing; L                                               |
| P07 AiiDA     | single emergency recovery owner; small retrieval/one-copy NFS; сохранить cards/reports и independent/continuation ownership                  | P04, P05, P20                                     | Fault idempotent; scientific failure не retry; no full HDF5 retrieval duplicate; client disconnect/card/report/branch scenarios; L затем N                  |
| P08 AiiDA     | `service.py:get_run`, selection helper: read projection/revision вместо повторного полного traversal                                         | P01                                               | Десять unchanged polls не обходят children/plan повторно; transition немедленно меняет revision/status; L                                                   |
| P09 Portal    | public schema/status/locator APIs, reuse cards/editor, typed DTO; исправить README; exact selector/revision                                  | P01, P06, P08                                     | Private validator import absent; cached status invalidation; mutation unknown outcome reconciled; L                                                         |
| P10 Portal    | Светлый researcher path: protocol/forms/resolved diff, run graph, saved maps/comparison/report и used-value help                             | P03, P09, P26                                     | Actual browser synthetic goal→variant→submit→attempt→slice/derive→report; help snapshot/unknown truthful, no solve on GET; L/N                              |
| P11 Platform  | split artifact qualification key и activation/boot health; identity/trust/qualification modules                                              | —                                                 | Unchanged solver proof reused after APP update; relevant environment/restore invalidates; wrong identity fail-closed; L                                     |
| P12 Platform  | runtime descriptor bindings вместо compile-time package; bounded commands; cheap health; native helper/service decomposition                 | P11                                               | argv/timeouts/output failure; changed APP не выключает configurator/Results; owning qualification only; L                                                   |
| P13 Platform  | Inventory `campaign_strict`, removal owning proof path, normal cap contract                                                                  | P19 contract                                      | Все callsites перечислены по owner; удалённый strict config явно отвергается, cgroup/Slurm caps действуют; old receipts остаются; L                         |
| P14 Runner    | Owning strict callsites/launch wrappers удалить по inventory; normal runtime resource limits и shared orchestration entry contract           | P13, P03                                          | Нет supported strict branch; launcher выполняет normal limits/argv и сохраняет original failure log; L                                                      |
| P15 Root      | `flake.nix`, source filesets, package compatibility graph; Platform package-version assertion меняется своим owning PR P12                   | P01, P05, P06, P09, P12                           | Docs-only diff не меняет solver/application runtime derivations; declared incompatible deps rejected; source graph выводится из gitlinks; L                 |
| P16 Root      | одна impact map/CLI/workflow: D/L/N/S checks, native commands без скрытого bootstrap; source/package integration                             | P15, P28                                          | Changed-path dependency fixtures, unknown impact fail-safe; docs path не Julia install/build; PR не full-CD gate; L                                         |
| P17 Root      | `ops/docs.ts`, `nix/docs.nix`: обычный reusable cached docs package вместо pilot orchestration                                               | P15, P16                                          | Два одинаковых inputs используют cached output; offline fonts/math/search и light page проверены; cache miss честно builds; L затем N                       |
| P18 Root      | docs content inventory всех repos, current/proposed/history route, русские manuals, прежняя задача→actual→остаток matrix                     | P03, P06, P16, P17                                | Current docs соответствуют коду/примерам; links valid; отменённые правила не возвращаются; архив не обязательное чтение; L                                  |
| P19 Platform  | Public schema/example per-host admin policy: resident min/start/max/weights/reserves/owned pool/active grant                                 | —                                                 | Fixture rejects pool overcommit/unknown ownership/shrink below grant; examples без secrets; per-host responsibility и foreign-admin boundary явны; L        |
| P20 Platform  | CPU/RAM request/grant/grow/readback/admit/release, durable reconciliation и private policy persistence                                       | P19, P12                                          | Low idle RAM не блокирует REQUEST; no capacity→wait; active floor; resize не deploy; Slurm balloon registration qualification/fallback; L/N                 |
| P21 Platform  | Portable worker image/manual install profile для Linux/libvirt ноутбука после fresh inventory; подключение к существующему controller        | P12, P19                                          | Реальный import/boot и network/storage/native drivers на actual image; controller/Portal/CI остаются в существующем кластере; N, первый дополнительный host |
| P22 Platform  | Enrollment/DRAIN/smoke/reboot identity и понятная автоматизация ручного worker пути                                                          | P21, P20, P14                                     | Worker проходит DRAIN→bounded synthetic Slurm job→reboot→identity check→RESUME; stale/duplicate identity rejected; N                                        |
| P23 Platform  | service-scoped delivery, initial management capability, OS/boot/offline, coordinated backup/restore drill                                    | P07, P11, P20, P22                                | UI update не прерывает job; disconnect/partial activation/oldCLI/reboot/lateNFS fail correctly; restore copy consistent; L/N                                |
| P24 Platform  | Proxmox profile и multi-endpoint/storage/trust qualification; перенос CI на другой PVE только после этих checks                              | P19–P23, Linux acceptance                         | Grow from idle и controlled host-pressure case без QEMU OOM; native grant readback/logs; отдельный administrator agreement; H после подготовки PVE          |
| P25 Platform  | Hyper-V profile/image/PowerShell memory controls и manual→automated install/enroll                                                           | P19–P23, Linux acceptance                         | Actual NixOS image boot/drivers/network/reboot/grant tests; Ubuntu evidence не подмена; H после подготовки Windows                                          |
| P26 Research  | Короткие protocol/material examples, versioned source/model/help content и runnable S01 handoff; русское руководство                         | P01, P03, P06                                     | Templates resolve новый формат; source formula/value/override различены; model/scattering/grids/tolerances unchanged; solver не запускать; L                |
| P27 Root      | published gitlinks, совместимая composition, final impacted CI и установленная acceptance matrix                                             | Owning PR включая P28–P32, доступные native gates | Existing cluster + Linux worker + browser/restore/performance receipts; PVE/HyperV measured или pending; science отдельно; L/N/H                            |
| P28 Root      | AGENTS/CONTRIBUTING/research-workflow/четыре skills: единый короткий developer loop, актуальные source maps, removal CPU credits             | Принятые решения, owner contracts                 | Docs/source-only/authorized-check/old-spec cases; нет новых разрешений/исторических counters; L                                                             |
| P29 Runner    | normal/diagnostic observation: batch sealed phase segments, small current snapshot, no per-event file I/O/duplicate serialization            | P01, P02                                          | Bounded buffers, event ordering/drop visibility; science/history неизменны; collector unavailable не тормозит solver; L                                     |
| P30 Results   | reuse capture/TelemetryWriter: incremental verified cursor, batch stage/flush, long-run performance report/self-cost без lifetime cutoff     | P01, P04, P29                                     | Новые bytes читаются один раз за source epoch; restart cursor atomic; gaps/replacement/overflow visible; synthetic off/on cost report; L/N                  |
| P31 Platform  | cheap cluster projection, native PVE context/host OOM diagnostics и telemetry/storage reserve                                                | P12, P19, P20                                     | State freshness/reasons, no full qualification on poll; native host metrics source/units, collector failure и log retention; L/N                            |
| P32 Portal    | Экран состояния services/VM/jobs/grants/wait/failure и bounded performance view; ссылки на PVE graphs                                        | P09, P30, P31                                     | Light browser показывает actual/unknown/stale; long-run report даёт причины/coverage, no solve/rehash on view; L/N                                          |

P15 не меняет Platform files через root PR: package assertion входит в P12, root лишь потребляет
опубликованный compatible component. Аналогично stale Results README исправляется в P06, Portal
README — P09, остальные инструкции идут вместе с владельцем поведения. Inventory P13 может выявить
дополнительные малые consumer edits внутри соответствующих owning PR, без одного cross-repo PR. Если
contract требует несводимый отдельный review unit, split допускается с сохранением dependency graph,
без нового общего перепланирования.

## 8. Семь дней от нового поручения на реализацию

T0 — явное поручение реализовать этот согласованный plan, fresh source, доступные существующий
кластер и Linux worker host. Программа ориентируется на семь рабочих дней; фактический календарный
финиш трёх backend зависит от окна пользователя. Missing credentials/inventory/host access блокируют
только зависимый stage, а не independent code/docs/fixture work. Внутри разрешённого этапа проверки
выполняются своевременно без вопроса перед каждым command/PR.

| День | Основной результат и параллельная работа                                                                                               | Выходной gate                                                                                                                                |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Fresh source/callsite inventory; P01/P02 contracts; P19 host policy; P28 developer loop; P11/P16 cheap-check design                    | Согласованные contract fixtures и memory failure scenarios; runnable tickets, без нового solver                                              |
| 2    | P03–P05 Runner; P06 Results; P08 read projection; P12 helpers; P15 dependency/filesets; P29/P30 append/capture fixtures                | Новый synthetic result читается независимо; нет private Core bridge; unknown state fail-closed                                               |
| 3    | P07 lifecycle, P09/P10 Portal, P13/P14 removal, P20 host grant; P17 docs package; P31/P32 monitoring projections                       | Local synthetic submit/read/cancel/recovery и low-idle grow protocol fixtures; light browser path                                            |
| 4    | P21/P22 подключение дополнительного Linux/libvirt worker к существующему кластеру, real memory qualification, P18/P26 manuals/examples | Linux worker boot/DRAIN/job/reboot accepted; begin→grow→run→release не убивает VM                                                            |
| 5    | P23 rollout существующего кластера, scoped update/fault/exact resume и coordinated backup/restore drill на копии; browser acceptance   | Обновлённый существующий кластер и Linux worker пригодны к работе, limits и failure logs проверены; normal telemetry cost/coverage объяснимы |
| 6    | **После Linux gate** пользователь подключает/готовит Windows Hyper-V и дополнительный Proxmox; P24/P25 идут независимо                 | Endpoint/storage/trust/admin policy проверены; actual backend tests либо конкретный local stage blocker                                      |
| 7    | P27 integration/final impacted CI, source-qualified timings, manuals and handoff; устранение обнаруженных failures                     | Честная readiness matrix по каждому backend; scientific run — следующее отдельное поручение                                                  |

Первое подключение нового worker выполняется на Linux/libvirt ноутбуке прошлой сессии. CachyOS
упоминался как наблюдение; актуальная OS, наличие VM и свободные ресурсы требуют fresh inventory.
Нельзя обещать, что прежний host доступен. Итоговая установка controller/Portal/CI и существующих
workers остаётся на текущем кластере; его необходимая проверка не означает создание второго кластера
на ноутбуке. Только после принятого Linux этапа пользователь сам готовит Windows и дополнительный
PVE. Все три backend обязательны в программе; недоступный host остаётся `pending`, не удаляется из
scope и не называется прошедшим по static evaluation.

Нормальный будущий CI переносится на дополнительный PVE лишь после проверки network endpoints, cache
signing/trust, builder identity, storage/permissions и administrator capacity agreement. По
умолчанию не переносить mutable shared state и не выполнять wipe. Позднее LAN-разнесение VM
использует те же явные endpoints; не требует новых dev VM или distributed solver.

## 9. Проверки, метрики и завершение

До тяжёлого native build — дешёвый preflight четырёх NixOS roles, nginx strict configuration,
executable paths, flake inputs, builder identity, Git index ownership, storage и fresh capacity по
[deployment runbook](../single-server-deployment.md). Read-only Git администратора использует
`GIT_OPTIONAL_LOCKS=0`. Измеренные production CPU/RAM, Nix/Julia parallelism и reserves записываются
в site policy; laptop local-debug не становится production default. Никаких новых сборок в этой
docs-сессии.

В будущем engineering stage использует доступные owned ресурсы после измерения, нормальные
caps/timeouts/output limits и stop on invariant failure. Проверки не запускаются бесконечно до
успеха: исправление причины или новый source объясняют повтор. Full CI повторять при затронутом
source/неустранённой ошибке; не требовать полный релиз перед каждым малым PR или service action.
Original failed logs и новые attempt/source identities сохраняются.

Before/after измерять на одном host, том же scientific workload/contract и одинаковых synthetic
inputs: qualification calls/time, status traversal calls/time, hash bytes, checkpoint I/O/peak
memory, docs cold/reused build и affected derivations. Разделять wall, CPU, allocations,
RSS/cgroup/host RAM и I/O. Для одного сравнения не придумывать статистическую уверенность. Новый
checkpoint не объявлять «вдвое экономнее» без данных; scientific speedup требует отдельно accepted
сопоставимых scientific results.

Resident memory принимается одним ограниченным engineering scenario на фактическом image после
laptop inventory; последующие PVE/Hyper-V stages повторяют применимый native contract, включая два
наблюдавшихся отказа. Перед запуском зафиксировать длительность, workload size/output cap, reserves,
controlled pressure ceiling и stop condition; не провоцировать host OOM ради доказательства.
Свидетельства: assigned/actual host+guest RAM, grant floor, job start/end, retained logs и VM state
после release.

Инкрементальность проверяется счётчиками прочитанных/записанных bytes и максимального buffer/spool,
включая длинный synthetic журнал без solver. Повторный poll без новых данных не читает scientific
payload или весь prefix. Off/on comparison technical collection не отключает scientific
history/acceptance. Overhead report — часть owning performance change и native qualification, не
обязательный тяжёлый gate каждой малой правки. Никакого фиксированного 1%.

До native этапа фиксируются также текущие timings resource resize, CI readiness, web/docs activation
и boot-to-ready. После изменения приводится то же измерение и объяснение оставшегося ожидания; новый
произвольный SLA не объявляется решением пользователя. Исходники Nix не заменяют backup mutable
state.

Каждый PR даёт reviewable diff, точный source, выполненные checks и ограничения. Первому
независимому reviewer передать вопрос/contract и первичные artifacts без готового диагноза; согласие
reviewers не заменяет проверку. Не требовать SCBA/Poisson, scientific environment install или
benchmark для docs-only PR. Окончательный report отдельно отмечает source publication, engineering
build, service/install, trust, restore, backend readiness и science.

## 10. Утверждения, ограничения и решения

| Утверждение                                                                       | Свидетельство                                                  | Ограничение                                                                                          | Решение                |
| --------------------------------------------------------------------------------- | -------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | ---------------------- |
| Восемь repos, isolation и независимый Core нужны                                  | Baseline architecture и решение пользователя                   | Реальное LAN-разнесение ещё не выполнено                                                             | сохранить              |
| Private bridges и повторные обходы/qualification усложняют путь                   | F01–F10 с commit/path/symbol                                   | Нет нового before/after runtime measurement                                                          | изменить               |
| Новый single format и lossless exact checkpoint заменяют legacy branches          | Принятое breaking решение, contracts P01–P06                   | Предложенный design ещё не реализован и не доказывает memory gain                                    | изменить               |
| Незавершённый strict proof path удаляется из supported product                    | Решение пользователя от 2026-10-27; preflight source выше      | Нужен inventory P13; ordinary limits и historical receipts сохраняются                               | изменить               |
| Native memory API пригодны для проверки resident policy                           | PVE/Microsoft primary docs и failure observations пользователя | Active grant/floor на actual NixOS images ещё не квалифицированы; foreign-admin agreement обязателен | дополнительно измерить |
| Linux, Hyper-V и Proxmox реально установлены и приняты                            | В этой сессии native receipts не получены                      | Linux first; два других host готовит пользователь после Linux gate                                   | данных недостаточно    |
| Семидневная система будет готова при доступных prerequisites                      | Dependency graph и дневные gates этого документа               | Effort estimate и человеческие окна не измерены; pending gate не pass                                | дополнительно измерить |
| Physics/model/reference oracle должны сохраниться                                 | Решение пользователя, AGENTS и owning Core boundaries          | Synthetic engineering acceptance не доказывает научную корректность/сходимость                       | сохранить              |
| Научный accepted result уже получен этим планом                                   | Новых научных запусков нет                                     | Science требует отдельного поручения и собственных критериев                                         | данных недостаточно    |
| Общие campaign CPU credits больше не нужны                                        | Прямое решение пользователя в этом обсуждении                  | CPU cost измеряется, resource protection остаётся                                                    | изменить               |
| Телеметрия должна объяснять long-run затраты без фиксированного процента overhead | Решение пользователя; F12–F15, existing capture/segments       | Runtime влияние normal mode ещё не измерено                                                          | дополнительно измерить |
