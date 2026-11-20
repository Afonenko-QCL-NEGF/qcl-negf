# Документация QCL-NEGF

QCL-NEGF рассчитывает квантовый транспорт в структурах квантово-каскадных
лазеров. Julia Core реализует модель и численные методы. Runner готовит
постановку, вызывает Core и пишет результаты. Results читает их независимо
от запущенного solver.

## Запустить и прочитать расчёт

- [CLI Runner](../runner/README.md).
  Команды `plan`, `run-plan` и `analyze`, настройка Julia Pkg и ограниченный
  пример на публичном входе.
- [Конфигурация](../runner/docs/src/user/configuration.md)
  и [результаты и restart](../runner/docs/src/user/results.md).
  YAML, замороженный план и соглашения о состоянии.
- [Независимый Results](../analysis/README.md).
  Проверка сохранённых артефактов, графики, экспорт и приём архивов.
- [Проверенный сквозной пример](implementation/stationary-checkpoint-2026-11-18.md).
  Один диагностический вход запущен локально и через HTCondor. Оба результата
  прочитаны независимо. Строгая сходимость этой точки не получена.

## Julia solver и физическая модель

- [Документация Core](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/db26a0ef49673d8246ae336cbe73bafe6d7482ac/docs/src/index.md)
  и [публичный API](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/db26a0ef49673d8246ae336cbe73bafe6d7482ac/docs/src/api/public.md).
- [Итерации SCBA](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/db26a0ef49673d8246ae336cbe73bafe6d7482ac/docs/src/theory/09_scba.md),
  [Poisson](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/db26a0ef49673d8246ae336cbe73bafe6d7482ac/docs/src/theory/10_poisson.md),
  [наблюдаемые](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/db26a0ef49673d8246ae336cbe73bafe6d7482ac/docs/src/theory/11_observables.md)
  и [критерии приёмки](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/db26a0ef49673d8246ae336cbe73bafe6d7482ac/docs/src/theory/12_validation.md).
- [Научные постановки и литература](../studies/historical/README.md)
  и [итоги кампании #133](campaigns/issue133-postboot-report.md).

## Кластер и интерфейсы

- [Руководство по кластеру](../lab/README.md). HTCondor, OpenTofu, Ansible,
  добавление Linux worker и использование очереди.
- [Добавление Windows worker](../lab/windows-workers.md) и
  [хранилище для восстановления](../lab/checkpoint-storage.md).
- [Open OnDemand](../lab/README.md#использование-первого-опыта).
  В лабораторной сети доступны подача инженерных заданий, их состояние,
  отмена и открытие файлов. Научный GUI и наблюдение за физикой в ходе
  расчёта ожидают интеграции.
- [Beszel](../lab/monitoring-qa-2026-11-17.md). История ресурсов хостов,
  состояние агентов и проверка светлой темы.
- [Контрольная точка инфраструктуры](implementation/cluster-checkpoint-2026-11-17.md).
  Подтверждённые проверки Linux worker, GUI и мониторинга.

[Архитектура интеграционного workspace](architecture.md) описывает границы
компонентов и прежний путь с AiiDA, Slurm и отдельным Portal. Для действующей
лаборатории начните с руководства HTCondor выше.
