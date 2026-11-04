# Общая инфраструктура, выросшая вокруг QCL: что существует и что можно переиспользовать

Да, рядом с научным QCL кодом появился существенный общеприменимый operational слой: доставка
releases, владение запуском и cleanup, выдача host memory, durable reconciliation, network guard,
проверка provenance и наблюдения. Это видно по исполняемым функциям и их callers, а не только по
названиям документов. Но из Source нельзя установить, что это произошло «случайно»: исходная
программа прямо включала deployment, worker enrollment, resource grants, recovery и monitoring.
Более точный предмет разбора — насколько глубоко реализация этих задач ушла в создание собственных
общих механизмов и какие из них действительно необходимы ближайшему полезному QCL запуску.

Наличие общего механизма не делает его готовым отдельным продуктом. В нём могут быть reusable идеи,
но ещё нет независимого контракта, переносимости и production evidence вне конкретной установки.
Ниже не предлагаются extraction, новая библиотека или новый framework. Это Source-анализ для
дополнения evidence PR130; код, зависимости, инфраструктура и данные сохраняются.

## Срез и способ чтения

Рассматриваются exact published refs: Platform `c47097225a4a798e4124e30245c7b5b2063eb32a`, Runner
`97ab889ff83b73d9fad5d34e278309b2efe3b299`, AiiDA `336358dfd10c698e4b4a71d8c93562aaa8ee7182`,
Results `10a32422b90a21ee728e73283217ac6b81bcf760`, Contracts
`5eb0e61a9fc12fa2215291e47b7cd28888ce64cc`. Утверждения об их поведении опираются на Git objects
этих revisions, не на dirty checkout. Опубликованный Source не удостоверяет installed composition
или выполненную native приёмку.

Учитываются только реализованные APIs и command paths. Private short-command witness design,
предполагаемые будущие backends и планы extraction не считаются готовыми инструментами. Уточнение
«новый» относится к диапазону исходных gitlinks программы→указанные refs: например,
`application_release.py` уже существовал и был изменён; `bootstrap_build.py` в этом диапазоне вообще
не менялся. Напротив, `delivery_requests.py`, `delivery_service.py`, `native_attempt.py`,
`host_resource_operations.py`, `linux_bridge_nm.py` и `monitoring_runtime.py` добавлены в Platform.
**[G01]** Это проверяется по
[диапазону Platform](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/compare/1b1370d2b8e83a267a97c8d49df14db220123478...c47097225a4a798e4124e30245c7b5b2063eb32a).

## Карта фактических механизмов

В таблице общность означает переносимость задачи, а не зрелость API. Колонка про native инструменты
показывает уже используемую основу; это не обещание механически удалить собственный слой без
проверки его обязанностей.

| Единица и actual symbols                                                                                                   | API, state и callers                                                                                                                       | Что общее и что связывает с QCL                                                                                        | Основа и предел зрелости                                                                                                                            |
| -------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Scientific state/persistence: Runner `open_exact_checkpoint`, `load_exact_solver_state`, Core state codec                  | Manifest, selected StateRef, history cutoff, checkpoint→actual Core state; вызывается execution/restart и readers                          | Atomic files/segments общие; mixer, Green/self-energy state, grid/units и scientific acceptance предметные             | HDF5/Julia переиспользованы; это QCL persistence, не общий workflow engine. [G02]                                                                   |
| Release/delivery: `prefetch_controller_closures`, `activate`, `deliver_cli`; `submit_update`, `run_update_service`         | Release descriptor→prepare/activation/health/commit; durable request, service generation, admission/reconcile; CLI и systemd delivery unit | Общая доставка immutable artifacts; roles, Code/release, worker health и admission проектные                           | Реальные Nix/systemd/SSH calls; собственный lifecycle вокруг них. Не новый builder или готовый общий CD продукт. [G03–G04]                          |
| Command/process lifetime: `command`, `group_cleanup_confirmed`, `Operation.command`                                        | argv/env, bounded streams, absolute deadline, one Popen/group, primary error и cleanup record; release/resource/native callers             | Общая задача supervision; Linux process ancestry/cgroups и fixed caller roles ограничивают переносимость               | subprocess/signals/kernel/systemd уже используются; observer — optional API, не отдельный CLI. [G05]                                                |
| Attempt/workflow bridge: `OrdinaryAttemptOwner`, `AttemptStore`, AiiDA `QCLExecutionRestartWorkChain`                      | claim→dispatch→ack→job/allocation→start/close либо HOLD; fixed client/serve/hook и original CalcJob                                        | Single-dispatch/idempotency общие; genuine AiiDA links, submit script, QCL result closure предметные                   | Slurm выбирает worker/очередь, AiiDA владеет workflow; новый bridge не независимый scheduler. Native retry frontier открыт. [G06–G07]               |
| Host resource broker: `HostResourceController`, `FileReceiptStore`, `MemoryBackend`                                        | request/grow/admit/finish/shrink/reconcile, grants, desired/readback, blocked/startup states; authenticated resource service               | VM memory reservations и crash accounting общие; owned policy, fixed roles, Slurm/task facts и site trust обязательны  | Actual pvesh/virsh, cgroups и systemd; появился собственный resource protocol/journal. Full dynamic qualification не установлена публикацией. [G08] |
| Qualification/witness machinery: `NativeQualificationService`, `CalibrationRepository`, `RootQgaTransport`                 | inspect/case/reconcile/report, original intents/receipts, measured guest/host facts, worker mirrors и fence                                | Harness для native effects общий по форме; текущие cases/Source/roles и physical predicates конкретны                  | Existing worker/command/QGA owner; `open_native_jobs` ещё явно CLOSED. Это не универсальный proof checker. [G09]                                    |
| Linux network guard: `decide`, `Store`, `reconcile`, `NativeNM.reapply`                                                    | status/reconcile command; PREPARED WAL, applied-version/token CAS, own suspend/restore authority; dispatcher/staged helper                 | Carrier/L3 recovery общие; один enrolled bridge/port, protected bindings и NM1.58 profile конкретны                    | Actual NetworkManager D-Bus Reapply, kernel readback; не реализован общий rollback произвольной сети. [G10]                                         |
| Metadata/provenance admission: Results `_MetadataArena`/`StateReader`; AiiDA `_Reads`/origin getters; Contracts validators | Finite read/copy/validation allowances, same-open bytes, original input/CREATE joins; вызываются parser, saved-source и result consumers   | Общие bounded I/O/provenance идеи; native5, exact schemas, AiiDA2.9.2 и pinned validation profile связывают реализацию | h5py/NumPy/JSON Schema/AiiDA уже используются; private internal mechanism не готовая generic library. [G11–G13]                                     |
| Observations: Runner `_NativePhaseObserver`; Results `supervise`, `TelemetryWriter`; Platform `NativeSampler`/cache        | Phase queue→sealed batches, process samples, retained summaries/cursors; monitoring commands и capture path                                | Общие telemetry/retention задачи; SolverEvent, state/Source epoch и QCL phases предметные                              | Parquet/Arrow, proc/cgroup, native host tools; свой protocol/accounting/cache, не полный универсальный monitoring product. [G14–G15]                |

## Где проходит научная граница

Ни grant broker, ни scheduler library не заменяют численный codec. Runner восстанавливает не просто
файл с пользовательскими данными: нужны сохранённые continuation arrays, mixer state, counters,
actual problem/domain, numerical policy и accepted history. Его `load_exact_solver_state` возвращает
именно `QCLNEGF.ExactSolverState`; `core_state_codec.jl` кодирует предметный public payload. Generic
artifact store может хранить эти bytes, но не определяет их математическую достаточность для exact
continuation. **[G02]**
[`production_state.jl`](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/97ab889ff83b73d9fad5d34e278309b2efe3b299/src/infrastructure/persistence/production_state.jl),
[`core_state_codec.jl`](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/97ab889ff83b73d9fad5d34e278309b2efe3b299/src/infrastructure/persistence/core_state_codec.jl).

Атомарная публикация, file references и chunked storage концептуально отделимы. Физические единицы,
scattering order, normalization, final observations и решение о научной допустимости должны остаться
у owning scientific components. Кроме того, новый public path нельзя выдавать за уже завершённое
глобальное отделение: `core_api.jl` в этом published Runner ещё импортирует и legacy private Core
symbols. Сам факт появления публичного API не доказывает, что весь пакет свободен от прежних
зависимостей.

## Доставка artifacts: orchestration поверх существующих Nix и systemd

Здесь действительно есть general-purpose поведение: descriptor immutable artifacts, closure hashes,
предварительная доставка, активация, health, закрытие admission при неопределённом исходе и
reconcile. Но actual build и перенос closures выполняют штатные команды:
`prefetch_controller_closures` вызывает `nix copy --from` и `nix path-info --json`. Собственный код
сравнивает Source/release identities и решает, когда выбранному worker можно вернуть admission. Это
добавленный coordination layer, не реализация аналога Nix. **[G03]**
[`application_release.py:prefetch_controller_closures/activate/deliver_cli`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/application_release.py).

Новые `delivery_requests` и `delivery_service` — уже самостоятельный мини-протокол maintenance
operations. `submit_update` фиксирует request и запускает `systemctl start --no-block`; service
сохраняет свою generation до входа в engine. Operation различает
queued/running/completed/failed/outcome_unknown/ reconciliation_required, не повторяет dispatch по
одному timeout и проверяет completion evidence. Callers и packaging существуют в
`modules/release.nix`. **[G04]**
[`delivery_requests.py`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/delivery_requests.py),
[`delivery_service.py`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/delivery_service.py),
[`delivery units`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/modules/release.nix).

Тонкий project adapter здесь мог бы ограничиваться descriptor/target selection, Nix artifact
operations и project health. Реализованный слой дополнительно владеет request durability, ambiguity
и согласованием нескольких nodes. Это реальная функциональность, но reusable CD library потребовала
бы отдельной границы roles, health/rollback и mutable-state obligations. Её сейчас нет; заявлять
готовый новый release product или drop-in replacement для чужого deployment нельзя. Installed
disconnect/partial activation/restore acceptance остаётся отдельным свидетельством.

## Исполнение и cleanup: дополнительный owner, не второй Slurm

`command` — наиболее общий отдельный primitive: один Popen, ограниченные stdout/stderr, общий
absolute end, проверка child/group cleanup и сохранение primary failure. Он используется разными
operational paths. Optional `process_observer` добавляет actual owner/child birth, executable и argv
hash; terminal record отличает original retained child от текущего PID. Это Linux-specific
supervision, а не просто удобный `subprocess.run` alias. **[G05]**
[`command/process observer`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/application_release.py),
[`Operation.command`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/native_attempt.py).

Над ним `OrdinaryAttemptOwner` и `AttemptStore` обеспечивают original claim, dispatch intent,
scheduler ack, привязку allocation и output closure одного CalcJob. Fixed client/serve/hook
действительно packaged в `nix/native-attempt.nix`; это исполняемый boundary, не только proposed
class. При потерянном ack Source не выводит отрицание из отсутствия scheduler row и не делает ещё
один sbatch. Привязка к AiiDA INPUT/CALL/CREATE, Code, original submit script и QCL final делает
этот owner гораздо уже generic task runner. **[G06]**
[`OrdinaryAttemptOwner/AttemptStore`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/native_attempt.py),
[`actual entrypoints`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/nix/native-attempt.nix).

AiiDA уже предоставляет WorkChain lifecycle; published `QCLExecutionRestartWorkChain` наследует
`BaseRestartWorkChain`. Slurm остаётся владельцем очереди и allocation. Для native branch Source
пока требует одну попытку и исключает recovery bundles до отдельной frontier integration. Поэтому
новые claim/closure checks не означают, что написан полноценный универсальный workflow engine или
принят native recovery. Тонкая интеграция с существующим workflow tool всё равно должна сохранить
project parser, scientific failure classification и exact-state handoff. **[G07]**
[`workflow.py`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/blob/336358dfd10c698e4b4a71d8c93562aaa8ee7182/src/aiida_qcl_negf/workflow.py).

## Resource broker и qualification: наиболее выраженный общий operational слой

`HostResourceController` имеет уже узнаваемый broker API: request/grow/admit/
finish/shrink/reconcile. `FileReceiptStore` хранит grants, bindings, desired, receipts, blocked и
startups под одним host lock; неизвестная mutation сохраняется charged. Controller зависит от
`MemoryBackend` protocol, а actual PVE/libvirt adapters вызывают `pvesh`/`virsh`. По назначению это
общий per-host VM resource broker, а не часть SCBA. **[G08]**
[`HostResourceController/FileReceiptStore`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_operations.py),
[`native backends`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_backends.py).

Однако это не общий cloud allocator: поддерживаются собственная owned policy, один доверенный host
owner, конкретные VM/runtime identities и full capacity accounting. Slurm выбирает worker, cgroups
ограничивают task; broker согласует гарантированную guest allocation с host memory. Нельзя заменить
только journal на произвольную БД и считать native safety перенесённой. Нужны прежние readbacks,
active-floor и foreign-capacity assumptions. Fixed reservation может сократить необходимость dynamic
механизма, но требует собственной actual qualification.

К broker добавился отдельный qualification harness: finite plan/cases, `CalibrationRepository`,
`NativeQualificationService.inspect/run_case/reconcile/report`, Root QGA transport и actual readers.
Он сохраняет original native effect и не смешивает его с physical assessment; `NOT_MEASURED` не
выдаёт за PASS. Слово proof здесь обозначает программные witnesses и проверяемые assumptions, а не
универсальное формальное доказательство. Существенное ограничение published Source:
`open_native_jobs` всё ещё отказывает с `qualification_worker_phase_required`; live-only observer
также не решает все fast-process races. Это собственная qualification система с открытым end-to-end
gate, не зрелый reusable benchmark/proof product. **[G09]**
[`NativeQualificationService`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_qualification.py),
[`RootQgaTransport/actual sources`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_qualification_sources.py).

## Network guard: общий случай, узкая реализованная машина состояний

`linux_bridge_nm.py` действительно содержит исполняемый `--status/--reconcile` helper: `decide`
выбирает NOOP/SUSPEND_L3/RESTORE_L3/REFUSE, `Store` сохраняет WAL/wake marker, `reconcile` фиксирует
intent до RPC и проверяет версию/hash/token. `NativeNM` использует NetworkManager system D-Bus,
`GetAppliedConnection` и `Reapply`; kernel readback отдельно проверяет routes/addresses/carrier. Это
больше wrapper одной shell-команды. **[G10]**
[`linux_bridge_nm.py`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/linux_bridge_nm.py),
[`staging integration`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ansible/networkmanager-bridge.yml).

В то же время он привязан к enrolled bridge/port, NM1.58, source/binding и собственной suspension
authority. Это guard обратимого изменения L3 в конкретном сценарии, не общий NetworkManager
replacement. Ansible playbook только stage-ит файлы и прямо оставляет actual installation
checkpoint, owned-file rollback и console recovery отдельным этапом. Conceptual extraction возможно;
утверждение о production-ready network rollback tool без этих gates не следует из Source.

## Metadata accounting и provenance: общая задача, очень тесная реализация

Results `StateReader` совмещает safe open, same-handle hash, selected manifest/ catalog/array
verification и I/O limits. `_MetadataArena` отдельно обходит resident roots, учитывает
scratch/copies/validation и удерживает один prepaid context. Published code знает exact
package/schema profile; верхний предел context160 MiB и validation reservation112 MiB — constants
admission, не измеренный RSS. Такая arena — общий по смыслу механизм metadata budgeting, но её roots
и профили прямо знают устройство Results/Contracts. **[G11]**
[`StateReader/_MetadataArena`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/blob/10a32422b90a21ee728e73283217ac6b81bcf760/src/qcl_negf_results/state.py).

AiiDA `native_actor._Reads`, `load_native_launch` и `read_native_origin_inputs` проверяют original
typed nodes/links и file bytes. `read_projection` добавляет отдельный read-only SQL snapshot/cache
для поддерживаемой AiiDA2.9.2/PostgreSQL schema. Это reuse AiiDA provenance с project admission
вокруг него, не новая provenance database. Отдельные UUID, hash или decoded dict не являются source
authentication. **[G12]**
[`native_actor.py`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/blob/336358dfd10c698e4b4a71d8c93562aaa8ee7182/src/aiida_qcl_negf/native_actor.py),
[`read_projection.py`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/blob/336358dfd10c698e4b4a71d8c93562aaa8ee7182/src/aiida_qcl_negf/read_projection.py).

Contracts `schema_validator` уже делегирует offline structural validation библиотекам JSON Schema;
собственные `results/outward/telemetry` validators проверяют domain/context joins. Из них можно
мысленно отделить FileRef, canonical counters и generic validation helpers, но field graph Core,
native5 semantics и lineage не заменяются «универсальным валидатором». Часть reusable primitives
есть; отдельного поддерживаемого generic metadata/ provenance validation package из Source пока не
следует. **[G13]**
[`schema_validator`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/blob/5eb0e61a9fc12fa2215291e47b7cd28888ce64cc/src/qcl_negf_contracts/__init__.py),
[`result validators`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/blob/5eb0e61a9fc12fa2215291e47b7cd28888ce64cc/src/qcl_negf_contracts/results.py).

## Observations: собственный protocol поверх стандартного storage и host tools

Runner `_NativePhaseObserver` имеет bounded queue, drop reasons, lifetime generation и batch worker;
Results `TelemetryWriter` stage/flush/rotate/resume и retained-window accounting.
`capture.supervise` владеет process capture, а phase/scientific data сохраняют разные domains. Это
реальная общая telemetry функциональность с собственными cursors/commits/coverage, не просто
несколько logging statements. Но SolverEvent, source epochs, exact state anchors и phase profiles
связывают её с QCL; универсальный monitoring backend из неё не получается механическим переносом
файлов. **[G14]**
[`phase_segments.jl`](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/97ab889ff83b73d9fad5d34e278309b2efe3b299/src/infrastructure/telemetry/phase_segments.jl),
[`TelemetryWriter`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/blob/10a32422b90a21ee728e73283217ac6b81bcf760/src/qcl_negf_results/telemetry.py),
[`capture.supervise`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/blob/10a32422b90a21ee728e73283217ac6b81bcf760/src/qcl_negf_results/capture.py).

Platform `NativeSampler`, `sample_native_status` и cache reader вызывают native
pvesh/virsh/systemctl/journalctl, нормализуют freshness/OOM/unknown и отдают bounded projection. Это
уже часть управления и наблюдения кластера, но не доказательство installed collector coverage или
операционной пользы в конкретном run. Logical limits, unit fixtures и generated service ещё не дают
measured overhead, storage fit и diagnosis реального failure. **[G15]**
[`native_monitoring.py`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/native_monitoring.py),
[`monitoring_runtime.py`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/monitoring_runtime.py).

## Что можно сказать о замене существующим open source

Замена должна относиться к обязанности, а не к названию Python файла. В рассматриваемом Source уже
есть существенный reuse: Nix строит/переносит artifacts, systemd держит services и cgroups, Slurm —
queue/allocation, AiiDA — workflow/provenance, NetworkManager — network configuration,
HDF5/Parquet/JSON Schema — данные и structural validation. Убирать эти зависимости в пользу нового
своего универсального engine оснований нет.

Для сравнительного review полезно разделить две вещи. Тонкий adapter должен связать выбранный tool с
QCL plan/Code/result, typed scientific failure, storage и нужным lifecycle. Собственный engine
начинается там, где проект сам хранит общие request states, grants, durable dispatch,
reconciliation, retention debt или универсально выглядящие memory/provenance proofs. Именно вторая
часть требует вопроса: какую реальную гарантию она добавляет к native tool и на каком counterexample
это необходимо?

Официальное сравнение AiiDA/Slurm/Nix/systemd и кандидатов ReFrame, Submitit, Parsl, Snakemake
относится к отдельному evidence разделу. Этот Source-only обзор не утверждает, что какой-либо из них
механически реализует текущие Root identity/fence, host balloon, exact native5 codec или physical
acceptance. Также он не запрещает упрощение: если обязанность уже надёжно принадлежит штатному
владельцу, custom duplicate lifecycle может оказаться ненужным. Решение требует сопоставить реальные
API/guarantees и минимальный сценарий, а не сразу запускать extraction/refactor либо объявлять весь
слой лишним.

Итак, по наблюдаемому назначению появились части cluster control plane, per-host resource broker,
artifact delivery и provenance/metadata validation. Это вывод из перечисленных APIs, states и
callers. Наличие отдельного зрелого универсального продукта, безопасной mechanical replacement или
готовой научной системы этим не доказано. Следующий предмет разбора — что оставить тонким QCL
adapter, что передать существующему owner и что отложить; не новый проект по превращению этих частей
в продукты.

| Утверждение                                                    | Свидетельство                                          | Ограничение                                               | Решение                                                 |
| -------------------------------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------- | ------------------------------------------------------- |
| Общие operational механизмы действительно реализованы          | G03–G15: actual functions, states, entrypoints/callers | Source не устанавливает намерение «случайно»              | сохранить фактическое разграничение                     |
| Есть части broker/control-plane/delivery/provenance tooling    | G04/G06/G08/G10–G15                                    | Нет независимой product qualification и общей portability | данных недостаточно для нового product claim            |
| Всё можно заменить одним готовым framework                     | Разные обязанности и уже reused native owners          | Mechanical equivalence не предъявлена                     | данных недостаточно                                     |
| Численный state codec можно заменить scheduler/storage wrapper | G02: exact scientific state и Core binding             | Generic bytes storage не знает scientific continuation    | сохранить предметную owning границу                     |
| Часть custom machinery можно упростить                         | Сопоставление own states с native responsibilities     | Нужны official API comparison и конкретный scenario       | дополнительно измерить/проверить, без реализации сейчас |
