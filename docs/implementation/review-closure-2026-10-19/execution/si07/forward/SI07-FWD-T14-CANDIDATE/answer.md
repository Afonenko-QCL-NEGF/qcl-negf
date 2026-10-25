Данных достаточно для аудита наблюдаемости, но недостаточно для оценки времени до научной приёмки или выбора оптимизации. Это public synthetic fixture, не production evidence.

Источник: `/tmp/qcl-si07-cases/T14/telemetry.json`, `execution_id=SI07-public-telemetry`, `attempt=1`. Записаны wall 120 s, 12 завершённых итераций и exit 0. Отношение 120/12 = 10 s — амортизированное wall на итерацию, не измерение длительности итераций: границы wall и состав фаз неизвестны.

`scientific_accepted=null`, `raw_residual_latest=null` — данных нет. Exit 0 не доказывает сходимость, физические проверки, достаточность дискретизации или валидацию. Время до durable accepted result неизвестно; оно не равно доказанным 120 s, нулю или бесконечности. Нет source/model/plan identity и научного контракта для сравнения запусков.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Записаны 120 s и 12 итераций | `wall_seconds`, `completed_iterations` | Неизвестны границы/фазы | **keep / сохранить** с identity и scope |
| Приёмка не установлена | acceptance/residual: null | Нет gates и receipt | **measure / дополнительно измерить** |
| Общая запись на диск не доказана нулевой | `io_write_bytes=0`; scope: collector stdout | Job storage/NFS не покрыты | **change / изменить** трактовку отчёта: scope и «нет данных» |
| Bottleneck и ускорение не установлены | CPU/RSS/read I/O/JIT/GC: null | Нет ресурсов и фаз | **measure**; физический контракт **keep** |

Нельзя вычислить core-hours, utilization, peak RAM или стоимость checkpoint/fsync. Нулевой stdout-счётчик не доказывает отсутствие I/O или overhead телеметрии.

Минимально недостающие свидетельства:

1. **Core/Runner:** frozen научный паспорт (observable, модель, сетки/базис, scattering, precision, допуски), source/model/plan IDs, residual history, отдельные outcomes convergence/physical/discretization gates и receipt принятого артефакта с integrity identity.
2. **Runner/Results:** начало вычисления и durable acceptance, retries/resumes и их стоимость; границы launch, solve, audit, persistence/retrieval, queue отдельно. Указать часы, coverage и вложенность spans для исключения двойного счёта.
3. **Runner observer:** CPU seconds на тех же границах, peak memory в bytes с методом/scope, storage read/write bytes и I/O durations отдельно от stdout; allocation/quota/affinity, topology и Julia/BLAS/GC threads. Начать с границ существенных фаз и доступного high-water counter; пропуски сохранять.

Отдельное измерение JIT/GC нужно лишь при оставшемся вопросе об их вкладе; first call не измеряет JIT. Это предложения для отдельно разрешённого сбора: cadence, overhead и конечный бюджет здесь не заданы. Менять solver, сетку, scattering или допуски оснований нет.

Прочитаны request, telemetry и frozen `qcl-performance-audit/SKILL.md` с `references/telemetry.md`. Tests, profiling, benchmarks и solver не запускались. Аудит: `/tmp/qcl-si07-forward-fresh/SI07-FWD-T14-CANDIDATE/operations.json`.
