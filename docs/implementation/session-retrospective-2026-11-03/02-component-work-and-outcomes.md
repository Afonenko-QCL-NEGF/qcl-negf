# Что изменилось в восьми компонентах и какой результат это доказывает

Срез на 3 ноября 2026 года. Это обзор опубликованного Source относительно gitlinks исходной
программы, а не отчёт об успешной установке всех новых версий. Работа дала новые публичные
интерфейсы состояния, хранения, независимого чтения и provenance; вместе с ними появился
значительный объём собственного кода проверки идентичности, ограничений и lifecycle. Полезность
этого кода следует оценивать по закрытым пользовательским сценариям и различающим отказам. Число PR,
тестов и строк не переводится здесь в процент готовности.

Исходный план сам разделял local/source, installed native и научную приёмку. Его недельный результат
включал работающий существующий кластер, дополнительный Linux worker, browser path, recovery и
restore; публикация библиотечных контрактов была промежуточным результатом. Поэтому одновременно
верны два наблюдения: изменения не сводятся к документации, но опубликованный код не равен
выполненной недельной программе. **[C01]**
[Программа от27 октября, §§7–8, опубликованный срез](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/a29fe2fb19aba0bab216c520653627316f099cce/docs/implementation/project-simplification-2026-10-27.md).

## Граница сравнения и три разных состава

Baseline ниже непосредственно сверяется с `git ls-tree d395044:components`. Published — component
tips из сохранённого `git-diff-stat.json`, проверенные чтением Git objects. Анализируется этот
диапазон, а не текущее содержимое dirty checkout. Полные SHA позволяют повторить сравнение
независимо от branch names.

| Компонент          | Gitlink исходного Root `d395044`           | Published срез                             |
| ------------------ | ------------------------------------------ | ------------------------------------------ |
| Core, `QCLNEGF.jl` | `0df7dd5a481c2c339e8520d2291c035253e7c0e2` | `01d472141a91c9429f43f7237460a17592d65845` |
| Runner             | `8264f48c01ccc524548036d4b3f44552a76f19b5` | `97ab889ff83b73d9fad5d34e278309b2efe3b299` |
| Contracts          | `41209389109d387912b0410a5244dbc29ff1ff42` | `5eb0e61a9fc12fa2215291e47b7cd28888ce64cc` |
| Results            | `f811d7c43bef8a70eb79ef74d554f08496a9af1c` | `10a32422b90a21ee728e73283217ac6b81bcf760` |
| AiiDA              | `7f4223eaff86b3a6104743098162ffa3fc4e0334` | `336358dfd10c698e4b4a71d8c93562aaa8ee7182` |
| Platform           | `1b1370d2b8e83a267a97c8d49df14db220123478` | `c47097225a4a798e4124e30245c7b5b2063eb32a` |
| Portal             | `104481fdce8e11c9734b8b5b0f2743c9e5760151` | `2c31e5fd597600ac632c292969c02dce0e50d020` |
| Research           | `408ca413a8df865110edfb480db2c8544452b8d0` | `46fb51fbd594be80127cf543c7160fc69d8e3b2d` |

Published Root `a29fe2fb19aba0bab216c520653627316f099cce` уже выбирает новые Core, Contracts, AiiDA,
Portal и Research, но его gitlinks Runner `195e42af…`, Results `c50c9ee0…`, Platform `e3861b2c…`
предшествуют трём последним tips из таблицы. Таким образом, «изменение merged в component» и «его
потребляет опубликованный Root» — два разных факта. **[C02]**
[Публичный состав Root](https://github.com/Afonenko-QCL-NEGF/qcl-negf/tree/a29fe2fb19aba0bab216c520653627316f099cce/components).

Есть ещё две отдельные identities: private Root source `e37f755c75e1098ae66aca32ef519773d946df34` и
installed runtime build source `f2db3115b423c8508d65fa4422441918806d92c6`. Их нельзя заменять public
Root SHA или component tip. Здесь приводятся только source identities из административного readback;
private адреса, host inventory, runtime payload и machine identifiers не публикуются. **[C03]**
Сохранённый original readback: private receipt
`P19-Root127-single-bind-fresh-after-20261103-attempt1`, поля установленного `runtimeBuildSource`;
это источник installed identity, не утверждение о native приёмке всех восьми библиотек. Реальные
installed scenarios рассматриваются в отдельной матрице evidence.

## Core: публичный exact state и наблюдения вместо private bridge

P02 требовал узкий in-memory restore/assessment API без файлового I/O и Contracts. Он опубликован:
`ExactSolverState`, `ExactRestartIdentity`, `validate_exact_state`, `restore_exact_state`,
`restore_completed_solution` и `solution_scientific_assessment`. Snapshot отделяет arrays от
producer; identity различает actual problem, numerical policy и execution context. Проверка
целостности и shapes предшествует восстановлению. Добавлены public diagnostic и optimized-operator
entry points, которыми P05 Runner может пользоваться без обращения к private Core symbols. **[C04]**
[PR18](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/pull/18),
[PR19](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/pull/19),
[публичный API при `01d4721`](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/01d472141a91c9429f43f7237460a17592d65845/docs/src/developer/public_state_api.md).

Позднейшие изменения важны для фактического producer: `checkpoint_context_sink` передаёт actual
problem именно текущего домена, а bound final observations сохраняют контекст того же returned
solution. Это позволяет Runner не реконструировать used inputs из первоначального preset. Здесь
изменялись и ветви numerical runtime: saved continuation, mixer position, counters и checkpoint
boundaries в `production_solver.jl`. Называть весь Core diff только новыми exports было бы неверно.
**[C05]** [PR20](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/pull/20),
[PR21](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/pull/21),
[`public_state_capture.jl`](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/01d472141a91c9429f43f7237460a17592d65845/src/numerics/optimized/public_state_capture.jl).

Переиспользованы существующие solver, reference path и численные библиотеки; новый слой — typed
state/identity/callback contract и его validation. Source tests проверяют exact restart, adaptive
barriers, snapshot lifetime и observation equivalence. Они содержат различающие случаи, но наличие
этих тестов само по себе не подтверждает actual installed execution и научную точность. Конструктор
snapshot и совпавший digest не заменяют independent oracle, сходимость, достаточность сетки и
экспериментальную validation. Сохранение уравнений и допусков — требование, а не вывод из числа
зелёных тестов.

## Runner: resolved inputs, segmented history и ограниченный actual producer

P03/P04/P05/P14/P29 образуют здесь связанный набор. Появились resolved configuration с assigning
origins и resource estimates, append-only scientific history/catalog, exact checkpoints и связи
parent/cutoff; `core_api.jl` и production adapter потребляют public Core. HDF5, атомарная публикация
файлов и обычные Julia entry points переиспользованы. Собственный код отвечает за canonical
input/identity, сериализацию state, publication barriers и согласование научной и технической
истории. **[C06]**
[PR29 — configuration](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/29),
[PR30 — segmented checkpoints](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/30),
[PR38 — public producer](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/38),
[`scientific_history.jl`](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/97ab889ff83b73d9fad5d34e278309b2efe3b299/src/infrastructure/persistence/scientific_history.jl).

Удалён незавершённый `campaign_strict` с resident authority/lease/ledger: запрос удалённого policy
явно отвергается, обычные planning, Linux affinity, cgroup и Slurm/systemd caps сохраняются. Это
конкретное упрощение, а не переименование прежнего механизма. Технические phase observations
записываются batch segments; callback не обязан делать отдельный файл на каждый event. **[C07]**
[PR39](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/39),
[`resident-storage-refusal.md`](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/97ab889ff83b73d9fad5d34e278309b2efe3b299/docs/resident-storage-refusal.md),
[PR32 — phase batches](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/32).

Самый поздний published PR51 соединяет ordinary single-point stationary Core return со штатной
native5 final publication. В source regression успешное исполнение намеренно даёт `converged=false`:
это полезная проверка различия process completion и science. Но тот же файл явно отвергает
multipoint, adaptive-domain, optical, educational backend, attempt-two/import и отсутствие original
origin/plan. Ранее добавленный constructor-only `native-publication-fixture` также не выполняет
SCBA/Poisson. Поэтому два разных producer нельзя описывать как уже работающий полный
исследовательский workflow. **[C08]**
[PR50](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/50),
[PR51](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/51),
[`p05_stationary_native5_path.jl`](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/97ab889ff83b73d9fad5d34e278309b2efe3b299/test/focused/p05_stationary_native5_path.jl).

## Contracts: общий язык данных, не дополнительный научный арбитр

P01 дал closed schemas и public validators для manifest/catalog/cursor, checkpoint/state, final
diagnostics/observations, resolved plan и outward result. Core field graph отражается
`reflect_core_layout.jl`; schema и generated TypeScript types производятся из него. Это уменьшает
риск ручного расхождения field inventories между Julia/Python/TS. JSON Schema validation использует
существующие `jsonschema`/`referencing`; собственные функции проверяют контекстные связи selected
state, parents, lineage и source refs. **[C09]**
[PR16](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/pull/16),
[`results.py`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/blob/5eb0e61a9fc12fa2215291e47b7cd28888ce64cc/src/qcl_negf_contracts/results.py),
[`reflect_core_layout.jl`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/blob/5eb0e61a9fc12fa2215291e47b7cd28888ce64cc/tools/reflect_core_layout.jl).

Дальнейшие additions обслуживают потребителей: phase/technical telemetry, retained-window/cumulative
summaries, performance anchors, outward native source и used-input help. IEEE bits, decimal
counters, units, missing reasons и original source identities сохраняются явно. Это уже больше
первоначального малого manifest contract; каждый новый envelope увеличивает объём compatibility
работы у Runner, Results, AiiDA и Portal. Польза — воспроизводимое чтение и отказ от угадывания
latest/формата. Цена — связность версий и несколько уровней валидации одного контекста. **[C10]**
[PR25 — outward](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/pull/25),
[PR27 — retained telemetry](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/pull/27),
[PR29 — used help](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/pull/29).

Validators не открывают указанные файлы, не удостоверяют присланные UUID/SHA, не выполняют numerics
и не объявляют physical PASS. Pure schema fixture и реальное JuliaHDF5→Python interoperability —
разные evidence. Именно эта граница нужна для review: не приписывать structural validation результат
producer/reader или научную приёмку.

## Results: независимый native5 read path с явной стоимостью

P06/P30 сделали Results отдельным потребителем одного выбранного `qcl-negf.results.v2` / native HDF5
5.0 source. `StateReader` открывает exact StateRef либо явный live/recovery pointer;
`history_batch`, cursors и `read_array` отделяют metadata от bounded array selection. Unchanged
pointer poll не перечитывает catalog/HDF payload. Использованы h5py/NumPy и существующие
HDF5/Parquet данные, без Julia solve или обязательного AiiDA profile. **[C11]**
[PR18](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/pull/18),
[`StateReader` и limits](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/blob/10a32422b90a21ee728e73283217ac6b81bcf760/src/qcl_negf_results/state.py),
[README](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/blob/10a32422b90a21ee728e73283217ac6b81bcf760/README.md).

Добавленные `FinalDiagnosticsReader`, final-observation/AnalysisReader, saved views, явные
export/derive/comparison, capture ingress и performance views дают полезный независимый read path.
Собственный слой обеспечивает safe open, same-handle hash, exact metadata context, provenance и
stream accounting. Здесь bounded slice не означает дешёвую операцию: selected immutable owner может
потребовать полный SHA pass, HDF chunk decode и повторную проверку после reopen. Это прямо
оговорено; logical byte budgets не гарантируют process RSS. **[C12]**
[PR20](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/pull/20),
[PR22](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/pull/22),
[PR31 — retained telemetry](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/pull/31).

Последний PR42 поднял разрешённый верхний предел явно выбранного closed metadata context со128 до160
MiB; validation reservation112 MiB сохранилась. Это не ускорение, не новая scientific capability и
не измерение RSS. Оно показывает реальную стоимость разросшейся metadata closure и необходимость
совместного resource review readers/consumers. **[C13]**
[Точный PR42 diff](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/pull/42),
[`describe_native_metadata_context`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/blob/10a32422b90a21ee728e73283217ac6b81bcf760/src/qcl_negf_results/final_observations.py).
Native format support не означает автоматическую миграцию прежних архивов; legacy/multipart fallback
в новом raw reader не обещан. Чтение recorded diagnostics также не превращает recorded failure в
accepted result.

## AiiDA: reuse provenance и scheduler lifecycle, новый exact native bridge

P08 реализован в `read_projection.py`: bounded read-only PostgreSQL snapshot для поддерживаемой
AiiDA2.9.2 schema плюс detached payload cache. Он использует существующие
PostgreSQL/SQLAlchemy/AiiDA backend, но recursive SQL и projection revision/cache — собственный
schema-dependent adapter. Это конкретное сокращение повторного полного ORM traversal; actual
latency/DB cost должны подтверждаться installed read, а не описанием алгоритма. **[C14]**
[PR18](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/pull/18),
[`read_projection.py`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/blob/336358dfd10c698e4b4a71d8c93562aaa8ee7182/src/aiida_qcl_negf/read_projection.py).

P07 развился в opt-in `native_actor`/`native_backend`, parser и saved-source getters. Они читают
genuine INPUT/CALL/CREATE, original plan/graph/execution и созданный CalcJob submit script; AiiDA
nodes и Slurm остаются владельцами provenance/очереди. Platform получает fixed public
launch/execution reads, а не доверяет словарю с предъявленным UUID. Small locators/bindings
связывают retained result; новый read path не требует retrieval полной HDF копии. **[C15]**
[PR20](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/pull/20),
[PR23](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/pull/23),
[`native_actor` public ports](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/blob/336358dfd10c698e4b4a71d8c93562aaa8ee7182/docs/native-actor.md).

Полный новый native recovery из этого не следует. В опубликованном
`QCLExecutionRestartWorkChain.setup` native branch требует `max_iterations=1` и отвергает recovery
bundle/prior archive до отдельной frontier integration. Прежняя классификация infrastructure retry и
scientific terminal остаётся в WorkChain; второй retry owner не добавлен. Constructor-only
publication fixture проводится отдельной командой и сохраняет scientific failure. Поэтому наличие
BaseRestartWorkChain и source tests не доказывает фактически принятый native fault→exact resume
сценарий. **[C16]**
[`workflow.py:attempt_decision/setup`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/blob/336358dfd10c698e4b4a71d8c93562aaa8ee7182/src/aiida_qcl_negf/workflow.py),
[PR36](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/pull/36),
[PR37](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/pull/37).

## Platform: native backends сохранены, собственный admission вырос существенно

P11/P12 отделили artifact qualification от activation/boot health и ввели runtime bindings
выбранного release. `release_identity`, `release_trust`, `release_qualification`, `release_health` и
`runtime_bindings` разнесли обязанности; `application_release.command` ограничивает
argv/output/deadline и владеет cleanup одного subprocess. Это reuse Nix/systemd и существующего
command engine, а не новый package manager. P13 удалил неподдержанный strict proof scaffolding.
**[C17]** [PR35](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/35),
[PR36](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/36),
[PR34](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/34).

P19/P20 добавили собственную per-host policy, capacity accounting, durable
operation/reconcile/fence, authenticated ingress, cleanup и qualification records. Backend actions
при этом идут через native `pvesh` либо `virsh`, guest facts через существующие systemd/Slurm/cgroup
interfaces. P21/P22 дают Linux/libvirt image/profile, manual install/enroll и guarded startup; P23 —
durable delivery requests в existing controller service; P31 — native sampler и cache-only
projection. Поэтому «всё самописное» было бы неверно, но и «только тонкая обвязка native tools» уже
недостаточно: собственная state machine и identity/readback contracts занимают самостоятельный
operational слой. **[C18]**
[PR33 — host policy](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/33),
[PR38 — grants](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/38),
[`host_resource_backends.py`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_backends.py),
[PR39 — delivery](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/39),
[PR44 — monitoring](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/44).

Особенно важна граница последнего published PR82: actual Source adapters, Root QGA transport,
canonical mirrors/capacity joins и optional process observer подключены, но `open_native_jobs()` всё
ещё явно возвращает `qualification_worker_phase_required`. Live-only observer может не получить exe
у уже завершившейся fast command; неизвестный Root PID нельзя исключить по UID. Следовательно, merge
этого PR не означает synthetic body/negative closure, готовый dynamic admission или production RUN.
Отдельный short-command witness остался private design; он не включён в published tip таблицы.
**[C19]** [PR81](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/81),
[PR82](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/82),
[`open_native_jobs`/`GuestGateSources`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_qualification_sources.py),
[`command` observer](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/application_release.py).

Это не делает dynamic route обязательным условием всякой полезной работы: programme §§5.2/5.4
допускает verified fixed reservation. В Source есть conservative backend и отдельная fixed
qualification; full allocation, actual fixed readback, Source/guest/registration facts и protected
profile требуются заново. Dynamic NOT_MEASURED не становится fixed PASS автоматически. P21/P22
import/boot/reboot/RESUME, P23 coordinated restore, P24 дополнительный PVE и P25 Hyper-V требуют
своих native evidence. Этот обзор не подменяет их наличием Nix/Tofu fixtures или manuals. **[C20]**
[Published qualification guide](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/docs/host-resource-qualification.md).

## Portal: явные сохранённые данные и светлый UI, без научного решения на GET

P09/P10/P32 переиспользуют существующие researcher cards/editor и owner AiiDA thread, добавляя typed
routes для точного point/source, saved arrays/history, catalog/J(V), explicit derive/compare и
загрузки authored reports. Frontend сбрасывает старый view/cursor при смене selection и отвергает
late reply. Public Results readers используются из ограниченного child; HTTP не получает
произвольный путь к файлу. Это Source-интерфейсы, которыми можно пользоваться после qualification
storage/installed composition, без запуска solve на чтение. **[C21]**
[PR31 — retained point](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/pull/31),
[PR33 — catalog](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/pull/33),
[PR34 — report](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/pull/34),
[PR35 — history](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/pull/35),
[saved-results contract](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/blob/2c31e5fd597600ac632c292969c02dce0e50d020/docs/saved-results.md).

Cluster screen читает paginated Platform cache, показывает unknown/stale/partial и прекращает poll
при hidden/disconnect. Performance route выбирает exact retained/current anchor и передаёт Results
view с coverage/self-cost; он не создаёт новый collector. Светлая тема сохранена. Собственный Portal
слой — DTO/API/UI, source selection, request/child lifetime и mount/access checks; ресурсы и научная
приёмка остаются у владельцев. **[C22]**
[PR28](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/pull/28),
[PR36](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/pull/36),
[cluster guide](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/blob/2c31e5fd597600ac632c292969c02dce0e50d020/docs/cluster-status.md).

Published performance guide прямо оставляет owner I/O/heap/RSS `not_measured`, отдельные real RO
NFS, browser interaction и reserve-fit gates. Legacy live history сообщает `capability_unavailable`;
stored history и U1 performance не выдают себя за его исправление. Последний PR39 синхронизирует
whole-suite fixtures с выбранными contracts; он не новая installed capability. Actual
goal→variant→submit→attempt→slice→report acceptance нельзя вывести из frontend render tests.
**[C23]**
[Ограничения U1](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/blob/2c31e5fd597600ac632c292969c02dce0e50d020/docs/live-performance.md),
[PR39](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/pull/39).

## Research: уточнённый handoff, научный результат ещё отдельная работа

P26 в этом диапазоне меняет четыре documentation files, а не solver/model implementation. Добавлены
русский researcher route и S01 equilibrium handoff: как связать вопрос, model/value/assigning
origins, frozen used inputs, raw final и независимые проверки. Existing reference model, scattering,
grids и tolerances не объявляются улучшенными от появления руководства. **[C24]**
[PR11](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/pull/11),
[researcher guide](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/46fb51fbd594be80127cf543c7160fc69d8e3b2d/docs/researcher-guide.md),
[S01 brief](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/46fb51fbd594be80127cf543c7160fc69d8e3b2d/docs/equilibrium-s01.md).

Полезный результат — воспроизводимый кандидат одного equilibrium point и честные неизвестные,
включая происхождение части параметров и условия FD/FDR/current oracle. Сам brief прямо не
предъявляет final dataset или numerical S01 evidence. Это подготовка возвращения к физике; успешный
plan, constructor fixture или small stationary engineering solve не принимают полную
исследовательскую постановку. В самом P26 source-handoff solver не запускался; это утверждение о той
работе, не blanket-утверждение обо всех последующих инженерных проверках программы.

## Что проверять при разборе результата недели

Все32 исходных review units сохраняют владельцев: Contracts — P01; Core — P02; Runner —
P03–P05/P14/P29; Results — P06/P30; AiiDA — P07/P08; Portal — P09/P10/P32; Platform —
P11–P13/P19–P25/P31; Research — P26. P15–P18/P27/P28 принадлежат Root и не превращаются в
accomplishments одного компонента. Эта привязка воспроизводит original §7, а не новую декомпозицию.
Разбиение implementation на дополнительные PR не означает, что добавилось столько же выполненных
пользовательских целей.

Для последующего review существенны следующие вопросы, а не новый framework:

1. Какой exact published/installed состав нужен ближайшему полезному synthetic trial? Где его
   original receipt, а где только component tip или private build?
2. Какие новые identity/lifetime checks закрывают воспроизводимый отказ, который не закрывают уже
   используемые Slurm/AiiDA/systemd механизмы? Какие можно отложить вместе с dynamic memory, не
   ослабляя verified fixed path?
3. Где стоимость повторных validation/copies/whole-file integrity измерена на actual output? Явные
   resource ceilings нельзя называть ни actual footprint, ни доказанной достаточностью, ни
   достигнутой производительностью.
4. Каким минимальным end-to-end evidence закрываются producer→Results→AiiDA→UI, exact recovery и
   restore? Нужен original failure/receipt и конечный вывод; очередной passing fixture не должен
   сдвигать цель незаметно.

Практический остаток следует выбирать по маршруту. Для dynamic остаются worker phase/body/closure и
native qualification; fixed lane может сократить критический путь только после собственной проверки.
Затем нужны coherent installed graph, полезная synthetic приёмка и отдельно разрешённый научный
опыт. Ни отсутствующий Native PASS, ни явно закрытый unsafe path не обосновывают вывод «весь код
бесполезен»; они обосновывают более узкий вывод: существенная часть недели дала Source/contract
foundation, а предъявленная пользовательская готовность пока требует отдельного доказательства.

| Утверждение                                                              | Свидетельство                                         | Ограничение                                        | Решение                                             |
| ------------------------------------------------------------------------ | ----------------------------------------------------- | -------------------------------------------------- | --------------------------------------------------- |
| В восьми owners опубликованы конкретные interfaces и изменения поведения | C04–C24: exact commits, symbols, owning PR            | Публикация не installed attestation                | сохранить установленную границу Source              |
| Native tools и существующие owners переиспользованы                      | C07, C14–C18, C22: Slurm/AiiDA/Nix/systemd/HDF5       | Собственный adapter/lifecycle слой всё равно вырос | дополнительно измерить цену и необходимость         |
| Полный native research/recovery route готов                              | C08/C16/C19/C23 содержат явные ограничения            | Full end-to-end evidence здесь не предъявлено      | данных недостаточно                                 |
| Dynamic qualification обязательно задерживает всякий полезный trial      | C20 и programme §§5.2/5.4 допускают fixed reservation | Fixed lane также требует actual qualification      | изменить приоритет после проверки existing fallback |
| S01 научно принят                                                        | C24 предъявляет handoff, не final dataset             | Нет отдельной полной научной приёмки               | данных недостаточно                                 |

## Уточнение после анализа4ноября

Появление public Core state/observation API не доказывает полного удаления private Core imports из
всего Runner. В published `97ab889ff83b73d9fad5d34e278309b2efe3b299` `src/core_api.jl` ещё
импортирует `_scaled_physics`, `_seed_green` и другие legacy bindings. Утверждения выше о public
boundary относятся к новому selected path, а не ко всем прежним callers. Это source-only ограничение
дополнительно сохранено в[09](09-emergent-tools-and-reuse-boundaries.md); код не изменялся.
