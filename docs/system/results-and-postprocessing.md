# Результаты: простое хранение, чтение и постобработка

Статус: исследование и предлагаемая архитектура, 2026-10-09. Аудит относится
к root `bce0aee` и его gitlinks. Новые операции/API ниже не реализованы;
solver, tests, transfer и NFS interruption experiments не запускались.

## Рекомендуемое решение

Сохранить **Slurm + AiiDA + Runner + NFS**. Большие scientific файлы имеют
одну основную копию на NFS. AiiDA хранит execution/attempt links, небольшие
inputs/status/summary и locator. Runner уже умеет сохранять закрытые native
generations и checkpoints; Results независимо читает их. Новая generic
система распределения, хранения или consensus validation не нужна.

Это adaptation существующих компонентов, а не новая реализация workunit
server с нуля. Physics HDF5 writer остаётся специализированным: готовая
система файлов сама не определяет units, наблюдаемые и научные статусы.

## Что полезно в других распределённых системах

| Система | Полезный механизм | Применимость |
| --- | --- | --- |
| BOINC / @home | Upload файлов, report завершения, application validator и assimilator — отдельные действия | Взять разделение delivery / registration / scientific interpretation. Replicas, quorum и credit для добровольных узлов нашему доверенному LAN не нужны |
| BOINC output handling | Постоянное сохранение результатов отделено от временного upload и cleanup | Не удалять finals/отрицательные результаты автоматически по правилу временного transport storage |
| HTCondor | File transfer и self-checkpointing имеют отдельные contracts | Взять различение process exit / output availability / checkpoint. Не добавлять HTCondor поверх выбранного Slurm только ради файлов |
| AiiDA | Нативные CalcJob retrieval и RemoteData locator | Использовать existing исполнение и малые metadata. Большие данные оставить NFS; RemoteData не обеспечивает их lifetime сам |

BOINC явно разделяет upload, report, validator и assimilator:
[DataFlow](https://github.com/BOINC/boinc/wiki/DataFlow). Его validator может
сравнивать replicas или проверять формат — это не физическая приёмка QCL.
[Validators](https://github.com/BOINC/boinc/wiki/Validators). Политики постоянного
сохранения описаны отдельно: [Output handling](https://github.com/BOINC/boinc/wiki/Output-file-handling).

HTCondor `ON_EXIT` не возвращает файлы при removal/preemption; для eviction
есть другой режим. Application checkpoint должен быть пригодным до остановки,
а не обещанным результатом самого scheduler.
[File transfer](https://htcondor.readthedocs.io/en/lts/users-manual/file-transfer.html),
[Self-checkpointing](https://htcondor.readthedocs.io/en/lts/users-manual/self-checkpointing-applications.html).
Ни такой transfer, ни наш Runner не гарантируют последнее состояние после
hard VM power-off. Доступен последний успешно опубликованный checkpoint,
если он существует и его storage доступен.

AiiDA `retrieve_list` сохраняет данные в repository; временный retrieval
после parser очищается. Stash/RemoteData не дают автоматически retention и
immutability внешнего каталога.
[CalcJob usage](https://aiida.readthedocs.io/projects/aiida-core/en/stable/topics/calculations/usage.html),
[RemoteData](https://aiida.readthedocs.io/projects/aiida-core/en/stable/topics/data_types.html#remotedata).
Просмотренная stable документация — 2.9.3, проект выбирает 2.9.2. Для малого
metadata retrieval новый stash API не требуется; API выбранной версии
проверяется при implementation, не предполагается по latest документации.

Альтернатива — все payload хранить в AiiDA repository. Это ближе к обычному
CalcJob retrieval и проще для provenance closure, но не даёт привычный
сырой HDF5 каталог NFS без дополнительной проекции и может дублировать
массивы. Полная замена на BOINC/HTCondor оправдана при смене типа кластера,
а не при нескольких доверенных workers. Отдельный object store/CAS сейчас
не даёт установленной пользы для этого масштаба.

## Что уже реализовано и что меняется

Runner `src/infrastructure/persistence/point_artifacts.jl:747` содержит
`commit_point_artifacts`: immutable payload generations и атомарный малый
pointer. Этот механизм сохраняется, а не переписывается новым protocol.
Scientific final включает полный final state, recovery ограничивает число
generations; несошедшееся вернувшееся состояние тоже можно анализировать.

`src/composition/scratch_execution.jl:134–136` уже выбирает прямую публикацию
в output storage при enabled recovery. Путь с local scratch имеет готовый
`stage_result_tree`: temporary destination, проверка и rename (`54,92,105–108`).
Начальный рекомендуемый путь с checkpoints — существующие commits прямо
на общем NFS. Scratch/staging остаётся явной альтернативой, если измеренная
стоимость NFS потребует её; последняя локальная незавершённая запись тогда
не обещана доступной после жёсткой остановки VM.

Сейчас AiiDA `calculation.py:140–143` retrieves целые archive/recovery/
executions, а `service.py:319` открывает только retrieved repository.
Поэтому one-copy NFS — **ещё не реализованный контракт**. Изменение: retrieve
plan/summary/manifest/ограниченные logs; сохранить небольшой external locator;
result access перевести на независимый NFS reader. Форматы native файлов
и public/expert Julia API при этом не требуют переписи.

Native `RemoteData` может представить расположение, а `Dict` — manifest
locator без нового Data plugin. Ссылка должна относиться к устойчивому
storage namespace, а не исчезнуть при замене worker VM. Корень NFS и его
права задаёт Platform; API принимает нормализованный относительный locator,
не произвольный host path. Владение/retention внешних данных остаются явными.

## Малый контракт публикации

1. **Выделение места.** Каждый attempt получает отдельное пространство;
   повторный запуск не перезаписывает старый payload. Существующий внутренний
   archive/recovery layout сохраняется; пути берутся из native manifest.
2. **Вычисление.** Рабочие файлы, текущий progress и ещё записываемые массивы
   отличаются от опубликованных immutable generations.
3. **Commit.** Закрыть/sync файлы, при staging завершить перенос, выполнить
   назначенную integrity проверку, опубликовать generation и малый pointer/
   manifest через existing Runner механизм. Partial файл не называется final.
4. **Registration.** AiiDA сохраняет малые execution/status/locator records.
   Большой HDF5 остаётся NFS. Mutable progress не выдаётся за frozen final.
5. **Чтение.** Brief использует малые metadata; full перечисляет сохранённые
   файлы и capabilities; slice читает конкретный dataset/selection с лимитом.
6. **Failure.** После nonconvergence/crash/cancel доступны только реально
   опубликованные finals/checkpoints. Controller может отметить interrupted
   attempt даже без финального manifest; отсутствие state указано явно.
7. **Cleanup.** Published finals и отрицательные результаты сохраняются;
   recovery ограничен; temporary/scratch удаляется после успешной публикации
   либо явного решения оператора. Backup/restore — отдельная операция.

Новый общий журнал доказательств и SHA на каждый GET не нужны. Checksums
имеют назначение на границе publication/transfer, restart, export или
расследования corruption. Конкретные существующие повторные checks
сокращаются по [финальному аудиту](release-roadmap.md#финализация-evidence-и-sha-без-нового-global-cache),
а не отключаются без выяснения защищаемого инварианта.

## Конкретика read / derive / новый расчёт

| Действие исследователя | Откуда результат | Стоимость и исполнитель |
| --- | --- | --- |
| «Покажи J(V) и причины неприёмки» | Saved scalar observables + coordinates + point statuses | Results читает summary; новые SCBA и Julia не нужны |
| «Покажи n(z), potential, wavefunctions» | `analysis.h5`: `density_per_m3`, `potential_*_eV`, `effective_wavefunctions`, z в nm | Python Results читает готовые datasets/рисунок |
| «Покажи n(E,z) в выбранном окне» | Сохранённый `spatial_energy_density`, m⁻³/eV; E,z axes/weights | Ограниченное HDF5 чтение и отображение; не повторять проекцию GL |
| «Покажи spectral(E,k)» | Saved trace A и occupied trace, eV⁻¹, сохранённые E/k conventions | Чтение projection; это не A(z,E) и не автоматически momentum-integrated density |
| «Покажи населённости» | Saved localized/effective sheet-density matrices, m⁻²; доли безразмерны | Небольшая матрица; явно указать basis и mapping между вариантами |
| «Вычисли A(z,E)» | Полные A(E,k,a,b) и GL: текущий `spectral_maps` одновременно вычисляет occupied map; basis/wavefunctions, grids/weights/spin/scales | Core `spectral_maps`; явный Runner derive-job, при существенной стоимости AiiDA/Slurm + общий CPU grant |
| «Заново получи n(E,z), которого нет в projection» | Полный GL и basis/weights/scales | Core `spatial_energy_density`; derive, без SCBA. Если dataset уже сохранён, достаточно read |
| «Сравни две готовые дискретизации» | Saved observables, модели/условия, grids и отдельные статусы | Results/Runner read-only comparison; интерполяция рисунка не доказывает refinement |
| «Рассчитай более тонкую сетку» | Новые resolved inputs/plan с явным numerical diff | Новый variant и solver job; прежний final state не превращается в уточнённый через derive |

Оптические gain/absorption spectra отложены по S09. Другой текущий предел:
`J(z,E)` готовым public operator/dataset в рассмотренном пути не найден.
Есть boundary `j(E)` (`observables.jl:239`) и integrated local `J(z)`
(`266`), но их произведение не определяет J(z,E). Такая карта сначала
требует физического определения и owning Core реализации с conventions и
finite-basis limitations. UI не изобретает формулу.

Действующие пути: writer `point_artifacts.jl:385–482`, Python rendering
`qcl-negf-results/render.py:350–376`, Core `observables.jl:64,130,414`.
Формулы проекции остаются в Core; Runner вызывает их; Python Results
читает/рисует/сравнивает готовые величины, Portal показывает интерфейс.

Source files:
[native writer](../../components/QCLNEGFRunner.jl/src/infrastructure/persistence/point_artifacts.jl),
[scratch/staging](../../components/QCLNEGFRunner.jl/src/composition/scratch_execution.jl),
[AiiDA retrieval](../../components/qcl-negf-aiida/src/aiida_qcl_negf/calculation.py),
[AiiDA access](../../components/qcl-negf-aiida/src/aiida_qcl_negf/service.py),
[Core observables](../../components/QCLNEGF.jl/src/physics/observables.jl),
[Results reader](../../components/qcl-negf-results/src/qcl_negf_results/state.py),
[renderer](../../components/qcl-negf-results/src/qcl_negf_results/render.py).

Текущий CLI `qcl-negf analyze RESULTS OUTPUT` и Julia `postprocess_series`
уже обрабатывают сохранённое. Transport-only operations можно явно выбрать
в Julia: `iv`, `populations`, `density_map`, `potential_map`,
`energy_density_map`. Default CLI содержит optical operations, поэтому
поддерживаемый release путь должен явно исключить их до S09. Новый adapter
для `spectral_maps` и semantic HTTP slice API ещё не реализованы.

## Пример для GUI и агента

Карточка показывает capabilities: **готово / вычислимо из сохранённого
состояния / данных недостаточно / требуется новый solve**.

«Показать карту» читает exact attempt и нужный dataset/готовый рисунок.
«Вычислить A(z,E)» показывает prerequisites, доступный source state,
ожидаемый объём и создаёт явное derive задание. Оно сохраняет отдельный
производный результат со ссылкой на исходный final, не изменяя его.
«Уточнить сетку» создаёт variant с diff и новым прогнозом CPU/RAM.
Те же три операции доступны агенту; GET/brief/full не запускают дорогую
постобработку по отсутствующему dataset.

Оценка размера ответа отделена от рабочего RSS и I/O. NE×Nz float64 карта
сама занимает 8×NE×Nz bytes без координат; чтение комплексных blocks
A(E,k,a,b) зависит также от NK и NB². Compression не определяет peak RSS.
CPU/RAM estimate derive требует просмотра реализации и ограниченных
измерений; численные обещания времени сейчас не установлены.

## Failure и приёмка continuation

Ветка остаётся внутри одного запуска. При отказе точка/ветка не приняты,
последующие зависимые точки не запускаются; данные сохраняются для анализа.
Предыдущие завершённые точки не теряют своих собственных assessments.

Причины различаются: nonconverged final, failed physical check, interruption,
missing state, storage error. `scientific_accepted=false` само по себе не
означает нарушение физики: Core `final_audit.jl:237` выдаёт false также при
converged candidate с `discretization=not_measured`. Итоговый error/failure
ветки должен показывать причину, а не перекрашивать все её точки одним verdict.

Manual cancel/update по I14 сохраняет уже опубликованные данные. Не обещать
сохранение того, что существовало только в RAM или ещё записывалось.

## Проверки реализации

Малые synthetic fixtures: interrupt до/после publication; повтор и collision
attempt; partial HDF5 не виден как final; cancelled ветка с сохранёнными
первой/второй точками; unavailable NFS/missing payload; bounded slice с
axes/weights; brief без открытия больших HDF5. На реальном NFS отдельно
проверить rename/sync и interruption semantics.

`StateReader` уже ограничивает selection и output budget, включая axes/
weights (`state.py:170`), но constructor (`143`) проверяет полный owner SHA.
Небольшой ответ поэтому пока не гарантирует малого I/O. Renderer читает
целый выбранный dataset перед display sampling (`render.py:350`).
Нужны bounded analysis adapter и проверка назначенных integrity границ,
а не новый универсальный reader или cache.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Existing publication пригодна как основа | Native commits, recovery и staging Runner | Реальный NFS interruption не проверен | Сохранить |
| Daily one-copy NFS требует adaptation | AiiDA full retrieval и repository-only service | Новый access ещё не реализован | Изменить |
| Read и derive можно разделить конкретно | Saved projections и Core observable functions | Стоимость derive не измерена; J(z,E) не установлен | Дополнительно измерить |
| Hard stop не гарантирует последний state | Checkpoint semantics и lifecycle I14 | Нет failure experiment в этом анализе | Изменить |
