# Сопоставимость и доказательства

Памятка к [анализу результатов](../SKILL.md). Для result claims нужны
существующие данные; source-проверка reader/контракта возможна без архива и
не является result acceptance. Неизмеренное и недоступное не заменяется нулём.

## Три маршрута чтения

| Маршрут | Что установить | Граница |
| --- | --- | --- |
| Текущий source-only | Selected root/gitlinks или owning commit, actual dirty overlays; source reader, validator и producer contracts | Проверить заявленное поведение/совместимость по source. Наличие кода/schema/tests не доказывает успешное чтение реального архива или scientific pass. |
| Неизменяемый архив | Inventory частей/receipt/hashes, archived source/model identity, frozen plan/criteria, run/attempt и фактический declared transport/native contract | Выбрать primary reader по доказанной поддержке этого контракта. Reader может быть иной ревизии, только если совместимость установлена; current README или похожие dataset names её не доказывают. |
| Standalone installation | Версия и identity доступного reader/package, его документация, metadata существующего набора и предоставленные исходники | Не требовать root checkout, если доступный reader подтверждённо совместим. Не import/install/upgrade автоматически; отсутствие reader/source/raw назвать точным ограничением зависимого чтения. |

Для standalone-задания сохранять вопрос/owner и evidence level, inputs/hashes,
этап/пути/полномочия, scientific invariants, oracle/acceptance и протокол чтения,
зависимости, finite shared attempts/CPU/RAM/wall/I/O/output и stop, ожидаемый
выход/limits/resume. Если root доступен, это канонический контракт
`docs/system/agent-review-workflow.md`, «Разбиение до READY»; отдельной формы нет.
Missing input блокирует только dependent claims/actions; уже разрешённое
доступное чтение не требует повторного согласования.

Для архива сначала разделить transport verification и native interpretation.
Поддержка legacy multipart не обещает поддержку старого HDF5 layout. Проверять
реальные `verification_scope`, role/schema declarations, identity и полноту;
не мигрировать original arrays и не исполнять вложенные скрипты. Оценить место,
распаковку, память и hash/I/O до чтения; использовать bounded slices и сохранять
derived отдельно. Missing/incompatible контракт — gap, а не permissive fallback.

## Матрица сопоставимости

| Группа | Что извлечь из каждого запуска |
| --- | --- |
| Identity | Archived root/component commits и dirty snapshot, frozen plan fingerprint, declared contracts, run/attempt; отдельно reader/analysis code version |
| Физика | Геометрия/материалы, T, bias/units, density, boundaries, scattering, broadening, seed/continuation |
| Дискретизация | E step/window/phase, k density/cutoff, z/interfaces, basis/periods, embedding, quadratures |
| Метод | Алгоритм/mixing, archived raw residual definitions, inner/outer tolerances, strict final checks, iteration limits |
| Результат | Наблюдаемые, statuses/threshold applicability и основания, фактические iterations/stop reason, missing data; единое U/G состояние |
| Стоимость | Hardware/SMT/affinity, Julia/BLAS threads, RAM, wall/CPU/JIT/GC/I/O, все attempts и accounting scope |

Для каждой строки: совпадает, контролируемое отличие, несопоставимо или
неизвестно. Малый SCBA residual не заменяет discretization evidence.
Snapshot integrity, process completion, convergence, physics, discretization и
experimental validation принимать раздельно. Failed/paused/unconverged attempts
сохранять. `pass`, `fail`, `not_measured`, `not_applicable` с основанием и `error`
не смешивать; derived оценку не выдавать за recorded archive assessment.

## Owning reader и source locators

Пути от root; наличие перечисленных файлов/symbols проверено чтением
2026-10-19. Карта не устанавливает reader compatibility для другого архива;
для него найти соответствующий source object/docs без переключения текущих
submodules на historical/latest. Численные transport ceilings и schema contents
живут в owning Contracts/Results, а не в этой reference.

| Предмет | Primary locator |
| --- | --- |
| Совместимость и доступные transport routes | `components/qcl-negf-results/README.md`, разделы Inspect and export / Modules; читать версию выбранного reader |
| Single archive + dispatch legacy multipart | `components/qcl-negf-results/src/qcl_negf_results/archive.py`, `receive`, `verify_archive`; `multipart.py`, `receive` — legacy transport |
| Committed native state и bounded arrays | `components/qcl-negf-results/src/qcl_negf_results/state.py`, `StateReader`, `verify_recovery_bundle`; `native.py`, `validate_native_handle` |
| Model/hash identity | `components/qcl-negf-results/src/qcl_negf_results/model.py`, `validate_model`, `canonical_bytes` |
| History/witness provenance | `components/qcl-negf-results/src/qcl_negf_results/history.py`, `verify_cumulative_history`; `witnesses.py`, `selected_witness_records`, `verify_selected_witnesses` |
| Shared declarations и validators | `components/qcl-negf-contracts/src/qcl_negf_contracts/artifacts.py`, `require_contract_set`; `schemas/` внутри этого package |
| Restart versus analysis | `components/QCLNEGFRunner.jl/docs/src/user/results.md`, `@id native-result-formats`, `@id solver-quality-contract` |

`validate_native_handle` в проверенном source принимает declared supported
format без legacy-layout fallback; точные поддержанные версии читать в его
owning declarations. Это source observation, не универсальное обещание новых
или будущих readers. Analysis result не обязательно пригоден для exact restart.

В standalone отсутствие, например, `state.py::StateReader` нужной версии или
archived `results.md` фиксируется как конкретный недоступный источник. Можно
описать inventory/metadata gap; нельзя угадывать schema, resumability или физику.

Историческая карта root `efb68778a9267cb11c6e9f49701ea2c247c35645` описывала
multipart receipts и их транспортный предел. Это датированное наблюдение,
не лимит всех новых экспортов и не лимит загрузки ChatGPT. Текущий reader
и archived producer устанавливаются заново по своему contract.

Шаблон утверждения: «Для run R, attempt A, artifact SHA256 H, dataset D, slice S,
при предпосылках P наблюдается X; это поддерживает Y в пределах Z. Не проверено W».
Performance claim передать в qcl-performance-audit вместе с этой матрицей,
а не только с итоговыми временами.
