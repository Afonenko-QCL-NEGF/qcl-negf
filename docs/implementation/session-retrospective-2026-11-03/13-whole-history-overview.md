# От initial import до текущего Source: корни межкомпонентной сложности

История не начинается 27 октября и не начинается с пустого solver. Уже initial public import 26
сентября содержит восемь компонентов, VM roles, workflows, проверяемые artifacts, restart, export и
telemetry. Поэтому позднейший рост общих механизмов следует рассматривать как несколько
последовательных расширений существующей системы. Из metadata нельзя вывести, что все они были
случайными, необходимыми или одинаково полезными.

Это Source-анализ для дальнейшего разбора, без реализации и инфраструктурных действий. Он охватывает
metadata всех девяти историй и выбранные semantic pivots, а не семантический аудит каждого commit.
Детальные memory/CD histories относятся к соседним отчётам; здесь важны связи между решениями.

## Полнота истории и предел наблюдения

Зафиксированный `repository-history-inventory.json` задаёт primary universe: 994 commits, достижимых
из девяти выбранных published heads. Все репозитории non-shallow. Дополнительно прочитана metadata
`git log --all`: 1070 видимых commits; 76 находятся вне этой selected ancestry. Это не значит, что
каждый из 76 нигде не публиковался: они лишь не входят в рассматриваемый состав. Side branches не
подмешиваются в вывод о published implementation.

Ниже counts включают merges и initial imports, используют committer date `%cs` и не измеряют объём
кода, стоимость, продуктивность или число решений. Source imports датируют первое доступное
публичное состояние, не момент создания всех включённых функций. Предшествующая разработка из этих
Git histories не восстанавливается. Root census snapshots/LOC здесь не пересчитываются: см.
[исторические срезы размера и их метод](16-history-size-and-coverage.md). В них ранний резкий рост
Root приходится преимущественно на plans/evidence; это нельзя переименовывать в рост numerical code
или стоимость исполнения.

| Repository; initial public commit; selected head | 26–30.09 | 01–18.10 | 19–26.10 | 27.10–03.11 | Selected / all visible |
| ------------------------------------------------ | -------: | -------: | -------: | ----------: | ---------------------: |
| Root `1e10299e99` → `a29fe2fb19`                 |        6 |       76 |       44 |         186 |               312 /328 |
| Core `92a217a31f` → `01d472141a`                 |        2 |        4 |       15 |          20 |                 41 /52 |
| Runner `c924d07dfa` → `97ab889ff8`               |        2 |       20 |       36 |          46 |               104 /105 |
| Contracts `c7cd6670f0` → `5eb0e61a9f`            |        2 |       10 |        7 |          30 |                 49 /59 |
| Results `abf3d54950` → `10a32422b9`              |        2 |       16 |       25 |          50 |                93 /100 |
| AiiDA `d5e793b57d` → `336358dfd1`                |        2 |       12 |       23 |          40 |                 77 /83 |
| Platform `66115da942` → `c47097225a`             |        4 |       87 |       28 |         103 |               222 /234 |
| Portal `dd7a286063` → `2c31e5fd59`               |        2 |        9 |       41 |          28 |                 80 /87 |
| Research `f884750b76` → `46fb51fbd5`             |        2 |        4 |        8 |           2 |                 16 /22 |
| Всего                                            |       24 |      238 |      227 |         505 |              994 /1070 |

## Четыре эпохи и проверенные pivots

**Initial import,26 сентября.** Root README уже назначает Julia numerics, AiiDA provenance, Slurm
resources, NixOS machines и self-hosted CI. Initial architecture объясняет независимый lifecycle
Core, Results без живого AiiDA, общие Contracts, flat gitlinks и отдельную private site boundary.
Platform декларирует storage/control/compute/CI плюс дополнительный libvirt worker. Это существующая
архитектура в исходном Source, а не поздний результат P01–P32. **[H01]**
[Root README](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1e10299e99f8d9f73a5dc3d3b53141459091d1fa/README.md),
[initial architecture](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1e10299e99f8d9f73a5dc3d3b53141459091d1fa/docs/architecture.md),
[Platform README](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/66115da942ed46e61fb60e95f33d9d9b5a8137bd/README.md).

Initial Runner уже предоставляет plan/run/checkpoint/scratch; Results — независимое
native4/results-v1 чтение, immutable inventory/hash checks, scientific/full-state export и
`TelemetryWriter`; Contracts — offline schemas, hostile JSON checks и checksum-bound vendoring.
Initial AiiDA WorkChain уже распараллеливает executions, сохраняя child results. Наличие этих
интерфейсов не доказывает успешный runtime, но исключает их приписывание одной последней неделе.
**[H02]**
[Runner README](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/c924d07dfa32949c72d390252a8cfd584668d6c9/README.md),
[Results README](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/blob/abf3d54950f1acaea55c5f300458b128a26fbeb0/README.md),
[Contracts README](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/blob/c7cd6670f0086a4d57ff913807ef3f2ab4f10430/README.md),
[initial WorkChain](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/blob/d5e793b57df82af71cf6efcdfc9db3928b8f9a44/src/aiida_qcl_negf/workflow.py).

**Начало октября: native интеграция и recovery.** Platform additions2–3 октября касаются isolated
CI, networking, state disks, actual bootstrap и application release admission. Появляется
`application_release.py` (`c50a771`, 03.10), затем bounded delivery и protected enrollment
(`587a895`/`dcc566c`, 09.10). AiiDA 03.10 получает
`QCLExecutionRestartWorkChain(BaseRestartWorkChain)` и `attempt_decision`: infrastructure retry
требует подтверждённой остановки и recovery; scientific terminal не становится retry. Это расширение
stock AiiDA, а не новый workflow engine с нуля. **[H03]**
[Первый release owner](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/c50a771a1ce4fbfc4ece5d4309cda65cb21ed458),
[restart diff](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/commit/1904cb51944d3fc5bc3e9f893addc03c191eb0bc).

В ту же эпоху Results усиливает original plan/point/attempt и HDF ownership, Runner отделяет
scientific finals от portable recovery, Research 09.10 вводит S01 equilibrium candidate. Commit
messages и последующие fixes Slurm shell, cgroup, NFS, drain/mask показывают работу над границами
native integration. Они не заменяют первичные incident logs и не доказывают причину каждого fix.

**14–26 октября: cross-component audit и evidence closure.** Публичная программа `9fe2849` 14.10
явно ставит рядом researcher/operator/developer scenarios, source/runtime/artifact identities,
ownership, timeout/partial failure и independent oracles. Она одновременно говорит, что новая
документация не prerequisite первого научного свидетельства. Это первичный источник требований в
репозитории, но не доказательство личного намерения пользователя/автора. **[H04]**
[Programme на момент появления](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/9fe2849f22e60d928cfced5ed00b595b0f2a2ee9/docs/system/comprehensive-review.md).

19.10 виден конкретный fan-out одного scientific evidence contract: Contracts `12fc264` задаёт final
fixed-point audit, Runner `1acc165` пишет его, Results `33b1a39` читает и связывает. Core добавляет
independent manufactured/ absolute/final-state oracles. Portal тогда же укрепляет actor deadline,
uncertain ownership и asset receipts. 20–25.10 появляются model-help source bindings, represented
equilibrium arithmetic, configurator, research cards, saved NFS/live views и capture. Следовательно,
formalization и generic metadata/lifecycle cost существовали до программы упрощения. **[H05]**
[Contracts](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/commit/12fc26462bbab3df76904c6deb01f8c6596de7be),
[Runner](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/commit/1acc165650fd4f4c2d49605cc679f90e3f6fcdae),
[Results](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/commit/33b1a39eab62b0c00532c4d6b30fa3279c06a5d3).

**27 октября–3 ноября: упрощение плюс новые strict interfaces.** Root `69d841f` публикует P01–P32.
Некоторые решения действительно сокращают старый путь: retirement `campaign_strict`, normal external
limits, artifact qualification отдельно от health, cached docs и impact routing. Одновременно public
exact Core state/native5, source-bound readers, actor/attempt guards и measured resource
qualification создают новые versioned interfaces. Это смешанная траектория, а не равномерное «только
усложняли» или «всё упростили». **[H06]**
[Первое опубликование плана](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/69d841fdd0fa84f835803560faf80bcfd682679c),
[latest programme](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/a29fe2fb19aba0bab216c520653627316f099cce/docs/implementation/project-simplification-2026-10-27.md).

## Решения: требование → появление → evidence → повторное использование → остаток

«Первый anchor» ниже — первое установленное здесь публичное проявление конкретного
решения/изменения. Оно не означает дату рождения идеи или полный поиск всех исторических аналогов.
Native alternatives названы по реально используемым слоям; механическая эквивалентность нового
framework не заявлена.

| Решение / источник требования                                             | Первый видимый anchor или изменение                                                                              | Обоснование в actual Source                                                                                                     | Custom / native граница                                                         | Зрелость и будущий вопрос                                                                                                                                                                     |
| ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 8 owners и VM roles; initial README/architecture                          | Root `1e10299`, Platform `66115da`, 26.09 [H01]                                                                  | Independent Core/Results lifecycle, state/data isolation, единый gitlink composition                                            | Native Git/NixOS/Slurm/AiiDA; собственная multi-repo release coordination       | Архитектура есть initial; все runtime roles этим не приняты. Окупается ли coordination для текущего small cluster?                                                                            |
| Core public boundary; initial Core/Runner split, P02/P05                  | Existing Core dependency initial; public exact state `e4c4ef3`, 28.10                                            | Detached state, identity/validation, actual checkpoint/final context                                                            | Предметный in-memory API; не scheduler/codec framework                          | Новый public path есть; Runner97 `core_api.jl` ещё содержит legacy private imports. Какие callers реально мигрированы?                                                                        |
| Contracts/HDF5/checkpoint/history; initial portable output, P01/P04       | Native4/v1 и vendoring initial;03.10 `1f7dfe2`/`c4e5b37`; native5 `a0d9b9d`/`72df0c7`, 28.10                     | Exact selected state/history/parent cutoff и cross-language shape/IEEE semantics                                                | HDF5/JSON Schema reused; свои manifests/codec/context joins                     | Форматы менялись, не возникли впервые. Какой минимальный producer→reader compatibility набор нужен?                                                                                           |
| AiiDA restart и job ownership; initial WorkChain, recovery03.10, P07      | Initial parallel workflow; `1904cb5`, 03.10; typed native actor `49e16f9`, 30.10                                 | Scheduler-stopped/recovery classification; genuine original links/script                                                        | BaseRestartWorkChain/Slurm reused; новый guarded transport/claim слой           | Native branch в 336 требует one attempt до frontier integration. Что делает stock owner, а что обоснованно добавляет bridge?                                                                  |
| Независимый Results и science; initial README, audit14.10                 | Initial reader/export; audit19.10 [H05]; stored views `944f0ed`, 25.10; StateReader `855fea7`, 28.10             | Same-source/hash/attempt; recorded evidence отдельно от scientific acceptance                                                   | h5py/NumPy; project provenance and bounded readers                              | Selected Source capabilities есть, actual interoperability/latency/RSS отдельны. Не дублируется ли численная приёмка в read path?                                                             |
| CI impact и multi-repo publication; initial release graph, P15/P16/P27    | Gitlinks/locks initial; ready-dispatch `18bc5ec`, 09.10; impact `2a5ca8b`, 29.10                                 | Не запускать неподготовленный full CI; проверка по changed source                                                               | Native package managers/Actions; custom impact map и integration graph          | Правило cheaper checks опубликовано; commit/PR counts не progress. Где остаются повторные unrelated checks?                                                                                   |
| Docs/offline/static render; initial native docs, 14.10 programme, P17/P18 | Documenter initial; `ops/docs.ts` `9d08dbc`, 22.10; offline package `5fce486`, 24.10                             | Pinned assets, source-linked docs, light/offline view                                                                           | Documenter/static tooling/Nix cache; свой bundle/provenance pipeline            | Ordinary package появился до 27.10; actual browser/offline acceptance отдельна. Какие Source proofs нужны docs, какие избыточны?                                                              |
| Telemetry/monitoring; initial Writer, P29–P32                             | Writer initial; capture/live `edacf89`/`91e0f88`, 25.10; phase batches `ed691fd`, 28.10                          | Bounded collection, visible drops/gaps, separate scientific data                                                                | Parquet/proc/cgroup/native host tools; custom cursors/retention/source bindings | Не новый с нуля monitoring stack; новые constraints растут. Какова measured цена whole path?                                                                                                  |
| Portal research flow/help; initial API, 14.10 human journey, P09/P10      | Light theme `23e110a`, 08.10; cards/configurator `1091856`/`36c6349`, 25.10; retained-source UI31.10             | Explicit frozen selection, stale-response rejection, no solve on GET                                                            | React/FastAPI/AiiDA owner reused; own DTO/context/lifetime                      | UI/fixtures не полный installed journey. Какой простой пользовательский маршрут реально принят?                                                                                               |
| Worker portability/network; initial PVE+libvirt, P21/P22                  | Providers initial; local KVM `592f9b6`, 03.10; Linux profile `03e0859`, 28.10; NM guard `5c0ca8d`, 30.10         | Protected host identity/network/storage, one owned bridge/port                                                                  | Native libvirt/OpenTofu/NetworkManager; свой WAL/CAS guard                      | Guard staged Source, не общий network product. Где actual boot/reboot/RESUME и нужен ли custom guard при native checkpoint?                                                                   |
| QGA как административный канал; прямое поручение 30.10 [H07]              | Требование guest agent30.10; `RootQgaTransport` и `_admit_root_transport`, `74de4f3`, 03.11                      | Fixed role/action, original exec/status receipts, direct guest-agent parent и pinned reader; без нового shell/SSH/public action | Native QEMU guest agent/pvesh; собственные Source/ancestry/receipt joins        | Требование канала подтверждено; точный протокол каждого перехода выбран реализацией. Какие проверки необходимы для текущего закрытого privileged channel, а какие появились сверх требования? |
| Backup/restore/trust; initial state boundary, P23                         | Coordinated DB+repository initial; FS accounting `3241019`, 02.10; cache/enrollment `d0097db`/`dcc566c`,03/09.10 | Не заменить state empty root dirs; retain original trust/data owner                                                             | Native PostgreSQL/NFS/Nix/SSH; own safety/readback contracts                    | Written procedure не restore drill. Что проверено на isolated copy, без подмены live state?                                                                                                   |
| Tests/proof formalization; initial tests, 14.10 review                    | Hostile JSON/physics tests initial; `9fe2849`, 14.10; independent oracles/failure ownership19.10                 | Property→producer→consumer→oracle, preserving unknown/error                                                                     | Julia Test/pytest/native checks; свои fixtures/profiles/witnesses               | Source proof не Native/science. Какой каждый новый guard подтверждает различающий отказ?                                                                                                      |
| Research/S01 и physical criteria; initial catalog, P26                    | S01 candidate `5458212`, 09.10; model passport/measurement scope19.10; Russian handoff `627c334`, 29.10          | Model/value/assigning origins, fixed-point/raw FDR/current questions                                                            | Предметная научная постановка, не general orchestration                         | Candidate/plan не accepted dataset. Какие scientific criteria и primary evidence ещё отсутствуют?                                                                                             |
| Resource/CD общий слой; native topology initial, P11/P19/P20/P23          | Release owner03.10 [H03], durable lifecycle19.10; grants `733820e`, 28.10                                        | Partial effect/active floor/readback и single mutation owner                                                                    | Nix/systemd/pvesh/virsh используются; свои journals/qualification               | Подробно в memory/CD histories; нельзя объявлять native PASS по helpers/receipts constructors.                                                                                                |

Кодовые anchors остаточных границ:
[Runner97 `core_api.jl`](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/97ab889ff83b73d9fad5d34e278309b2efe3b299/src/core_api.jl),
[AiiDA336 native retry restriction](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/blob/336358dfd10c698e4b4a71d8c93562aaa8ee7182/src/aiida_qcl_negf/workflow.py),
[Results metadata context, введённый `38f80b3` 30.10](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/commit/38f80b3438a6fc25c7d16f831abff2c506c9cf51),
[Platform worker phase CLOSED при `c470972`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_qualification_sources.py).
Это проверяемые ограничения, не общий вердикт о качестве всех owners.

**[H07]** Прямое поручение пользователя, локатор `human53466`, 30.10.2026 17:36 UTC: guest agent
обязателен, аналитику следует по возможности оптимизировать через него. Этот источник обосновывает
выбор QGA, но не предписывает каждый Root-hop, формат журнала или ancestry proof. Опубликованный
выбор виден в
[`RootQgaTransport` / `_admit_root_transport`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_qualification_sources.py)
и
[commit `74de4f3`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/commit/74de4f3fa3cbbece97417d7b7b22b601dd56cb22).
Локатор сообщения не является публичной Git-ссылкой; для независимого разбора его следует сохранять
отдельно от интерпретации кода.

## Что объясняет история, а что остаётся гипотезой

**Наблюдение:** small change в scientific evidence может затрагивать несколько owners. 19.10 один
final-audit carrier потребовал producer, schema и independent consumer; 28–31.10 exact state/native
sources добавили публичные identities, validators, metadata contexts и UI selection. **Гипотеза:**
значительная часть расходов возникла из fan-out строгих cross-language/source contracts и проверки
их consumers, а не из новых физических уравнений. Это согласуется с selected pivots, но не измеряет
долю LOC, actual effort или необходимый минимум кода.

**Наблюдение:** initial Source уже различает execution/science и имеет trust, budgets и independent
readers; 14–19.10 эти требования оформляются в более подробную review/failure/oracle программу.
**Гипотеза:** стремление сохранять каждую границу unknown/ownership/copy/byte identity способствует
росту новых profiles и lifecycle states. Нельзя заключить, что каждый guard лишний, или приписать
это личному намерению человека без отдельной primary communication.

**Наблюдение:** есть и движение к упрощению — отказ от незавершённого strict пути, ordinary external
limits, public Core, reusable docs и impact routing. **Вывод:** правильный вопрос — какие
обязанности уже надёжно покрывают Slurm, AiiDA, Nix, systemd и reader libraries, и какой тонкий QCL
adapter ещё нужен. Whole-history counts не доказывают exponential growth, readiness или
бесполезность. Для этого нужны Root census, code/semantic comparison и actual workflow cost.

Nix и Julia задают важные свойства сборки и numerical runtime, но сами по себе не ограничивают число
custom protocols, state machines и межъязыковых adapters. Ожидание compiled/declarative системы с
небольшим glue нужно проверять по этим обязанностям и callers; история не обосновывает новую
миграцию языка.

Покрыты все девять metadata histories и перечисленные 15 decision families. Selected semantic reads
включают initial architecture/README/WorkChain, restart diff 03.10, programme 14.10,
producer/schema/consumer pivots 19.10 и актуальные ограничения. Не выполнены полный 994-diff audit,
attribution индивидуального effort, поиск всей переписки, installed revalidation или официальное
сравнение возможностей каждого alternative. Это ограничения отчёта, не новые gates и не поручение
начать ещё один framework.

| Утверждение                                                            | Свидетельство                                                         | Ограничение                                              | Решение                                                    |
| ---------------------------------------------------------------------- | --------------------------------------------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------- |
| Базовая многокомпонентная система существовала до 27.10                | Initial public imports и H01/H02                                      | Pre-import история неизвестна; README не runtime receipt | сохранить точку отсчёта                                    |
| Formalization/общая инфраструктура росли до последней недели           | H03–H05, датированные additions/diffs                                 | Не все commits семантически прочитаны                    | сохранить temporal distinction                             |
| Рост вызван только numerical core или только ошибочным generic tooling | Metadata и selected pivots показывают смешанные причины               | Нет количественного causal/effort decomposition          | данных недостаточно                                        |
| Нужна глобальная замена архитектуры                                    | Native owners уже переиспользуются; есть точечные открытые boundaries | Mechanical replacement не доказана                       | дополнительно проверить обязанности, без нового grand plan |
