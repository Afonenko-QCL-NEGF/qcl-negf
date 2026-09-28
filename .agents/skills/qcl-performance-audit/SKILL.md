---
name: qcl-performance-audit
description: Аудит производительности QCL NEGF по исходному коду и сохранённым результатам. Применять для объяснения времени до научно принятого решения, CPU/RAM/I/O, Julia JIT/GC/BLAS, масштабирования и достаточности телеметрии; выдавать решения keep/change/measure без изменения физического контракта.
---

# Аудит производительности QCL NEGF

Цель — уменьшить **time-to-accepted-solution** при том же научном контракте. Загрузка CPU, скорость итерации и завершение процесса сами по себе не доказывают улучшение. Непринятое решение не становится быстрым принятым решением из-за малого wall time.

## Полномочия и источники

Начинай с read-only анализа кода, конфигурации, сохранённых результатов и уже собранных профилей. Прочитай корневой `AGENTS.md` и инструкции компонента. Карта кода, snapshot SHA, семантика метрик и минимальная предлагаемая телеметрия находятся в [references/telemetry.md](references/telemetry.md); проверь актуальность локаторов.

Не запускай solver, тесты, build, benchmark, калибровку, профайлер, установку зависимостей или сервер только ради аудита. Новое вычисление допустимо в явно разрешённой текущей задаче с определённым бюджетом времени/ресурсов и критерием остановки. Уже данное разрешение повторно не запрашивай. Иначе подготовь ограниченный план измерения. Это правило действует и без корневого `AGENTS.md`.

## Шесть шагов

1. **Зафиксируй научную единицу сравнения.** Запиши observable, структуру, материалы, граничные условия, температуру/bias, basis, grids/quadrature, scattering, precision, kernel/approximation modes, inner/outer algorithms, tolerance, budgets, acceptance gates и final audit. Добавь seed/checkpoint, continuation branch, порядок точек, consumed iterations и exact/approximate статус. Изучи resolved configuration и смысл fingerprints: одинаковый размер задачи ещё не означает одинаковую физику.
2. **Составь паспорт доказательств.** Запиши umbrella/submodule commits, fingerprints/hashes, execution/point/session/allocation IDs, Julia/libraries, CPU topology/SMT/NUMA, affinity/cpuset/quota и Julia/BLAS/GC threads. Помечай каждый вывод `факт`, `гипотеза` или `нет данных`, указывая источник, единицы, scope и coverage. Наличие schema, writer или теста не доказывает наличие измерений. Fixtures не являются production evidence.
3. **Проверь принятие результата.** Раздели process exit, completeness, convergence, physical gates, discretization evidence и validation. Сопоставь residual history, quality, limiting gates и final audit с observables. Speedup сравнивай между результатами одинакового требуемого контракта. Для failed/paused/unconverged сохрани потраченное время и причину; не исключай неудачные attempts незаметно.
4. **Восстанови временную шкалу.** Отдели queue, launch/load, возможный JIT, initialization, SCBA/Poisson, final audit, checkpoint/write/hash/fsync, stage-out/retrieval и postprocessing. Назови границы основной метрики: старт вычисления → durable accepted result; submit-to-result показывай отдельно. Учитывай retry/resume историю. Для параллельной кампании раздели critical-path wall time и суммарные CPU/core-hours. Не складывай вложенные inclusive spans.
5. **Определи стоимость существенных фаз.** Сопоставь CPU/wall, work units/task width, allocations/GC, RSS/peak/cgroup memory, I/O, pauses и sampling gaps. Прочитай фактические операторы и зависимости от `N_E`, `N_k`, `N_b`, scattering channels. FLOPs/storage estimate не заменяет runtime/RSS. Bottleneck остаётся гипотезой без измерения того же scope. Покажи альтернативные объяснения и ограничения данных.
6. **Выбери keep/change/measure.** `keep` — выбор оправдан в названных пределах; `change` — есть причинная опора и проверка scientific equivalence; `measure` — отсутствует конкретное доказательство. Для каждого решения укажи механизм, ожидаемое влияние, owner, минимальную проверку и риск регрессии. Реализацию выполняй только в пределах текущего поручения.

## Главные ловушки

- «Запрошено 16 CPU, используется 1–2» недостаточно для вердикта. Уточни единицу CPU, окно, фазу, allocation versus effective quota/affinity, реальные threads, work units, SMT, serial fraction, bandwidth, I/O/admission wait и конкуренцию. Process CPU не показывает, какие Julia/BLAS threads работали.
- Разделяй cold start и steady state: first observed call и `warmup` не являются измеренным JIT. Проверяй фактический BLAS/backend и вложенные thread pools. Scheduled scientific path задаёт BLAS=1; direct/configured callers могут отличаться. Это не доказательство универсально лучшей настройки.
- `ΔCPU_s/Δwall_s` даёт mean busy logical CPUs только при совпадающих identity и границах. Allocation utilization требует соответствующего знаменателя и coverage. Пропуски, resets, PID reuse и смена clock domain не равны нулю. Метка фазы в конце resource interval не описывает весь интервал.
- Не смешивай Julia allocation bytes, RSS, cgroup memory/cache и analytical storage estimates. Process-inclusive CPU/GC counters могут включать другую работу; вложенные интервалы перекрываются. Учитывай worker/native workspace, checkpoint duplication и headroom.
- Compression, hashing, fsync, retrieval, telemetry serialization/flush и polling имеют стоимость. Их устранение допустимо лишь при сохранении durability/recovery контракта. Наличие измерительной инфраструктуры не означает нулевой overhead.
- Scaling сравнивай на известной topology, affinity и одинаковом scientific contract. Разделяй strong scaling, weak scaling и throughput независимых точек. Показывай repeats, median/spread, memory/core-hour cost; при одном запуске не выдумывай uncertainty interval. Разница меньше разброса не подтверждает ускорение.

Не выдавай за performance optimization укрупнение grids, сокращение basis/domain, ослабление tolerances/gates, отключение scattering/diagnostics/final audit или недекларированный approximation mode. Это отдельные научные изменения с error budget. Workspace reuse, сокращение лишних copies/allocations, task granularity и batch I/O — кандидаты, требующие доказательств; изменение reductions может изменить численный путь. Синтетический kernel benchmark не заменяет полное принятое решение.

## Результат аудита

Начни с достаточности данных и scientific comparability. Приложи паспорт, основные затраты до принятия, пробелы и таблицу:

| Объект / фаза | Факт и источник | Гипотеза / альтернативы | Влияние на accepted solution | keep / change / measure | Проверка и owner |
| --- | --- | --- | --- | --- | --- |
| Символ или artifact | Значение, units, scope, coverage либо «нет данных» | Проверяемый механизм | Wall/CPU/memory/I/O и научный риск | Решение с причиной | Identity, метрика, criterion, бюджет |

Для `measure` используй reference telemetry plan: отличай существующий producer, поле schema и реально приложенные данные; задай units/scope/cadence/cost/owner. Proposed sampling и overhead budget не представляй наблюдёнными. Без production results выдай аудит наблюдаемости и гипотез без численного вердикта о скорости. Укажи прочитанные источники и какие вычисления не выполнялись.
