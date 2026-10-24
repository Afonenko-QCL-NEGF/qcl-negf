# Телеметрия и доказательства аудита

Карта к [аудиту производительности](../SKILL.md), не отчёт о скорости запуска.
Поле schema, writer, source теста и реально записанный counter — разные
свидетельства. Ни один из них отдельно не доказывает bottleneck или speedup.
Сравнивать time-to-accepted-solution при неизменном scientific contract.

## Три маршрута

| Маршрут | Что читать | Граница |
| --- | --- | --- |
| Текущий source-only | Selected source refs/gitlinks и dirty overlays; producers, admission, writer/consumer и owning acceptance | Выдать аудит наблюдаемости, coverage gaps и performance hypotheses. Не требовать production archive, но не выдумывать utilization, JIT/RSS/I/O или численный speedup. |
| Неизменяемый архив | Archived producer/model/plan/attempt/session/allocation identity, artifacts/hashes, source version, фактически собранные logs/counters и compatible reader | Метрики трактовать по архивным definitions/units/scope. Current schema/defaults/README не заполняют старые missing поля. Сопоставимость physics/acceptance проверяется до speedup. |
| Standalone installation | Доступный skill package, вопрос, сохранённые материалы/metadata, версии runtime/reader и их подтверждённые contracts | Root не обязателен для анализа предоставленного. Если owning module/docs нужной версии отсутствуют — назвать точный gap; не import/install/upgrade и не запускать profiler ради восстановления отсутствующих данных. |

В standalone сохранить вопрос/owner, immutable inputs и evidence level,
разрешённый этап/пути/полномочия, scientific invariants, oracle/acceptance и
протокол чтения, зависимости, конечный общий бюджет/stop и выход/limits/resume.
При доступном root ссылаться на канонический девятиполевой contract
`docs/system/agent-review-workflow.md`, «Разбиение до READY»; второй формы нет.
Уже выданный scope сохраняется, missing блокирует только зависимые действия.
Новый solver/test/build/benchmark/calibration/profile/install/server stage
требует его действующего поручения и finite envelope; повторного вопроса для
готового уже разрешённого действия нет. Fresh admission/technical BIND/READY,
protected data/jobs/VM и неотменённые scientific/resource/CI-once limits сохраняются.

## Current lookup по выбранному source

Пути от root, availability/symbols проверены чтением 2026-10-19. Перед новым
аудитом проверить actual HEAD/dirty/gitlinks и найти symbol через `rg` в
selected source. Записывать commit + path/symbol в evidence, не вести отдельный
ручной source lock. Номера строк старого snapshot не являются current locators.
Содержание формул, thresholds, schemas и storage defaults читать у owner.

| Предмет | Owning path / symbol | Что проверить |
| --- | --- | --- |
| Timing options | `components/QCLNEGF.jl/src/numerics/optimized/production_contracts.jl`, `ProductionOptions` | `phase_timing`, event sink и фактические options run; наличие switch не доказывает recording |
| Iteration/phase counters | `components/QCLNEGF.jl/src/numerics/optimized/production_telemetry.jl`, `_emit_scba_progress`, `_production_counter_sample`, `_production_phase_begin`, `_production_phase_end` | Clock/CPU/GC/allocation scope, begin/end и условия записи; process-inclusive не thread-local и не measured JIT |
| Placement/coverage | `components/QCLNEGF.jl/src/numerics/optimized/production_solver.jl`, `_production_phase_begin` calls | Вложенность, exceptions, early exits и phase boundaries; task width не measured active CPU |
| Numerical memory | `components/QCLNEGF.jl/src/numerics/optimized/production_contracts.jl`, `ProductionMemoryEstimate`; `kernels.jl`, `_preflight_production_memory`; `fft_parallel.jl`, `production_fft_workspace_bytes` | Analytical storage/work estimate отдельно от RSS/native peak и actual workers |
| Native phase journal/admission | `components/QCLNEGFRunner.jl/src/composition/native_phase_telemetry.jl`, `_record_native_phase!`, `_native_phase_request`, `_native_phase_memory_permit!` | Producer clock/session/parent spans, cgroup limits, wait/GC boundaries; journal existence не overhead measurement |
| Hardware/resources | `components/QCLNEGFRunner.jl/src/infrastructure/resources/linux_resources.jl`, `probe_hardware`; `resource_reports.jl`, `hardware_profile_dict`, `execution_plan_dict`, `save_resource_diagnostics` | Discovery/affinity/quota/limits не continuous utilization sampler; проверить actual emitted artifacts |
| Execution/thread setup | `components/QCLNEGFRunner.jl/src/composition/scientific_execution.jl`, `BLAS.set_num_threads`; `configured_run.jl`, `BLAS.set_num_threads` | Scheduled/configured paths различаются; не переносить настройку одного caller на весь Core |
| Synthetic calibration | `components/QCLNEGFRunner.jl/src/application/execution_calibration.jl`, `_benchmark_execution_candidate`, `calibrate_execution_plan` | Synthetic scheduling evidence не full-solver accepted-solution benchmark; чтение не запускает calibration |
| Durability/acceptance | `components/QCLNEGFRunner.jl/src/infrastructure/persistence/point_artifacts.jl`, `commit_point_artifacts`, `verify_point_artifacts`; `components/QCLNEGF.jl/src/numerics/reference/acceptance_metadata.jl`, `_acceptance_metric_metadata`; Runner `docs/src/user/results.md` | State/receipt identity, analysis versus recovery, missing evidence и scientific gates |
| Telemetry field ownership | `components/qcl-negf-contracts/src/qcl_negf_contracts/telemetry.py`, `TELEMETRY_SCHEMA`, `TABLE_FIELDS` | Versioned declarations не доказывают producer или заполнение полей; не копировать schema в skill |
| CPU integration/durable tables | `components/qcl-negf-results/src/qcl_negf_results/telemetry.py`, `CpuCoverage`, `TelemetryWriter`, `_publish` | Stable deltas/identity/capacity, coverage/coarse intervals, pointers/catalog/source cursors и dropped/capture errors |
| Transport/native reader | `components/qcl-negf-results/src/qcl_negf_results/archive.py`, `receive`; `state.py`, `StateReader` | Reader compatibility подтверждается declared archive contract; transport integrity не scientific acceptance |
| AiiDA resource/result boundary | `components/qcl-negf-aiida/src/aiida_qcl_negf/validation.py`, `scheduler_options`; `calculation.py`, `QCLExecutionCalculation`; `parser.py`, `QCLExecutionParser`; `service.py`, `list_artifacts`, `open_artifact` | Requested allocation отдельно от utilization; plan/point/artifact validation отдельно от process exit и science |

В standalone эти locators — идентификаторы требуемых материалов. Если нет,
например, archived `telemetry.py::CpuCoverage` или native journal с указанным
session, сохранить этот gap. Не подставлять код текущей версии как доказанное
определение архивной метрики; отдельный source audit при этом возможен.

## Семантика чтения существующих измерений

- Identity, clock domain, allocation scope и capacity должны соответствовать
  counter interval. PID reuse/resets/gaps не являются нулевыми затратами.
  Стабильный длинный interval даёт coarse average, но не фазовую детализацию;
  endpoint phase label не описывает весь interval. Profile samples не считать
  повторно вместе с baseline. Unknown ancestor quota не означает отсутствие limit.
- CPU/GC/allocation counters могут включать другую одновременную работу процесса.
  Inclusive nested spans перекрываются; их сумма не wall time. Admission wait/GC
  и producer phase требуют проверки фактических границ, иначе возникает double count.
- `warmup`/first call не измеряет JIT отдельно. Initialization может включать
  compilation. Process RSS, Julia allocation bytes, cgroup memory/cache, analytical
  estimate и sampled maximum имеют разные scopes; sampled peak не полный peak.
- Durable committed pointers/catalog/hashes отличать от staging и неполного tail.
  `missing_reason`, capability gaps, `not_measured`, unavailable/null сохранять;
  ноль допустим при реально измеренном нуле. Buffer/flush settings не sampling
  cadence и не доказательство overhead. Writer сам по себе не background sampler.
- Scientific comparability, failed/paused attempts, consumed restart work и
  completeness входят в performance verdict. Изменение grid/basis/model/scattering/
  tolerances/diagnostics/final audit не является эквивалентной оптимизацией.

## Предложение измерения при конкретном gap

Сначала использовать existing data. Только если различающего evidence нет,
описать минимальное измерение: accepted representative input/checkpoint,
source/model/plan identity, неизменяемый scientific contract и independent oracle,
сравниваемые execution settings, cold/warm, repeats/spread, units/scope/coverage,
cadence/duration, общий attempts/CPU/RAM/wall/I/O/output cap и stop/resume.
Числа и thresholds не наследуются из старой reference; их даёт текущий порученный
measurement contract и fresh resource admission. Сам план не разрешает запуск.

| Нужный evidence | Что ограничить/различить | Owner → downstream |
| --- | --- | --- |
| Scientific passport | Point/attempt/criteria/source, acceptance и consumed budget | Core/Runner → Contracts/Results/AiiDA |
| Hardware/allocation | Topology/affinity/quota/threads, process/group/cgroup scope и изменения | Runner/AiiDA → Results |
| Phase CPU/wall/GC/allocation | Begin/end, nesting, admission/I/O boundaries и serialization cost | Core/Runner → Results |
| Resource baseline/memory peak | Actual interval/counter coverage, kernel high-water versus sampled peak, native headroom | Runner observer → Results |
| I/O/durability | Checkpoint/write/compress/hash/fsync/stage/retrieve bytes и telemetry own writes | Runner/AiiDA → Results |
| JIT/threads/scaling | Отдельный bounded profile window лишь для unresolved question; synthetic kernel отдельно от solver | Runtime/Runner → Results |
| Telemetry self-cost | Dropped/capture errors/lag/buffer, disabled/enabled scientific equivalence | Producer/Results → consumers |
| Scheduler accounting | Job/step identity, original units, allocated versus actual CPU, no duplicate totals | AiiDA/scheduler → Results |

Добавление collector/schema/producer — отдельная owning задача при наличии
поручения; audit не назначает её автоматически. Возможное измерение проверить
на observational effect; не обещать нулевой overhead и не заменять full-solver
scientific equivalence synthetic kernel тестом.

## Исторический snapshot и внешние источники

Read-only проход 2026-09-28 изучал root
`efb68778a9267cb11c6e9f49701ea2c247c35645` и его Gitlinks. Тогда в просмотренном
checkout не были обнаружены сохранённые production phase/Parquet/HDF5/resource
artifacts; tests генерировали fixtures, production resource sampler не был
установлен этим чтением. Это ограниченное историческое наблюдение, не current
inventory и не факт об отсутствии пользовательских данных вне дерева. Старые
line locators, storage defaults, sampling proposals и overhead target не являются
текущими настройками или выданным budget.

Следующие ссылки сохранены из чтения 2026-09-28; новой web-проверки здесь нет.
Версия actual Julia/Slurm определяется run, online `v1`/scheduler docs движутся.
Ни одна ссылка не доказывает bottleneck конкретного запуска.

- [Julia Performance Tips](https://docs.julialang.org/en/v1/manual/performance-tips/):
  compilation/allocations/types/array access и взаимодействие thread pools.
- [Julia Profiling](https://docs.julialang.org/en/v1/manual/profile/): uncertainty,
  API/version и observer cost; текущие online docs не разрешают profiler run.
- [Slurm sacct](https://slurm.schedmd.com/sacct.html): actual versus allocated CPU,
  job/step scope и plugin-dependent completeness.
- [Slurm sstat](https://slurm.schedmd.com/sstat.html): live task/step aggregation,
  RSS scope/units и ограничения scheduler evidence для фазовых выводов.
