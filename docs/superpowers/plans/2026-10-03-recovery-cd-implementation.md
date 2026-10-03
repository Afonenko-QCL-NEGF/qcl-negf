# CPU recovery, scientific archive and application CD Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Подготовить локально проверяемые изменения T0–T7 для последующего внедрения без доступа к
серверу.

**Architecture:** Core владеет численным состоянием и формулами; Runner — архивом, recovery и
standalone исполнением; contracts/results — независимыми форматами и чтением. AiiDA управляет
конечными попытками, Slurm ресурсами, platform согласованной активацией одного CPU-релиза и Windows
lifecycle.

**Tech Stack:** Закреплённые Julia/Python/AiiDA, HDF5, Nix/NixOS, Slurm, GitHub Actions,
PowerShell/Hyper-V.

**Spec:** [Согласованные требования](../../../qcl-negf-codex-requirements.md). Пользователь поручил
начать согласованную реализацию и локальные проверки 2026-10-03; повторное согласование этого объёма
не требуется.

## Global Constraints

- Только CPU; не менять физическую модель, tolerances, mixing и numerical budget инфраструктурным
  retry.
- Старые массивы утрачены; каталог пользовательских результатов не менять и не использовать как
  обязательную fixture.
- Gitlinks остаются authority состава. Не обновлять umbrella gitlinks на неопубликованные
  компонентные commits.
- Нет production deployment, серверных SSH, отмены текущих исследований и полной сборки ОС. Для
  локальных тестов допускается временный depot с точными версиями существующего Manifest; package
  update/resolve запрещены.
- Общий бюджет локальных тестов всех агентов: 4 CPU одновременно, 10 GiB RAM, 4.5 часа тестового
  wall time, 4 GiB временных данных. Максимум 4 исправления на один сбой, затем явная фиксация
  причины. Численные probes ограничены §10 требований с авторизованным расширением для
  JIT/исправлений: 30 минут суммарно, 1 CPU, 3 GiB RAM, 10 MiB вывода по
  [fixture plan](../../../components/qcl-negf-research/docs/fresh-fixtures-2026-10-03.md). Полный
  solver sweep запрещён.
- Одно расширение первоначального общего предела 4 часа до 15:20 UTC использует явное поручение
  пользователя повысить локальное время. Guard полного Runner suite 2100 секунд сохраняется; при
  timeout разрешён один focused run только незавершённого хвоста immutable ревизии, максимум 20
  минут, 2 CPU/6 GiB. Повтор whole suite и новые научные постановки этим расширением не разрешены.
- Логи локальных проверок: `/tmp/qcl-implementation-tests/`; краткий долговечный отчёт —
  `docs/implementation/recovery-cd-local-validation.md`.
- Критерии реальной LAN/Slurm/Windows инфраструктуры фиксировать `not_verified`, отсутствие
  измерений — явно.

## Review Focus

- Disk full/crash между publish и acknowledgement не уничтожает предыдущий recovery и не создаёт
  ложный durable receipt.
- Analysis/history/continuation не ссылаются на удалённый payload и не удерживают бесконечную
  цепочку поколений.
- Неоднозначная потеря связи не создаёт двух исполнителей; nonconvergence не вызывает
  инфраструктурный retry.
- Частичный CD и старый offline worker оставляют admission закрытым; solver Code сохраняет immutable
  path.
- Shutdown ждёт сохранения всех jobs и доступности bundles постоянному узлу, но не новой allocation.

## Task 0: Исходный состав и согласованный interface

**Files:** требования, architecture, существующие package manifests и schemas.

- [x] Прочитать требования/инструкции, зафиксировать фактические HEAD/status/submodules.
- [x] Создать локальную ветку umbrella `codex/recovery-cd-preparation`; сохранить пользовательские
      untracked файлы.
- [x] Зафиксировать canonical output policy и recovery/attempt receipt interface до интеграции
      consumers.
- [x] Проверить release graph без нового вручную поддерживаемого revision lock.

## Task 1: Runner archive/recovery/telemetry

**Files:** `components/QCLNEGFRunner.jl/src/application/scientific/contracts.jl`,
configuration/definitions, scientific_execution, persistence/point_artifacts, scientific_history,
postprocessing, соответствующие tests/examples/docs.

**Interfaces:** Сохранить существующий `commit_point_artifacts` и immutable commit manifest как
исходную границу; расширения согласовать в Task 0. Outputs определяют archive/recovery/telemetry,
operational limits не определяют scientific quality.

- [x] Написать failing behavioral tests final/nonconverged/pause, actual algorithm contract, optics
      single owner.
- [x] Реализовать согласованный output/provenance, явную миграцию legacy policy и optical
      source-quality receipt.
- [x] Написать failing fault-injection tests retention/corruption/staging/budget/transfer.
- [x] Реализовать durable publication, bounded recovery, verification/fallback, portable
      dependencies и publication/import/export logical budget guards; aggregate physical quota
      остаётся deployment requirement (partial AC2).
- [x] Проверить existing test groups в ограниченном local environment; сохранить вывод и
      компонентный diff.

## Task 2: Contracts и независимые results consumers

**Files:** `components/qcl-negf-contracts/src/qcl_negf_contracts/`, schemas/tests;
`components/qcl-negf-results/src/qcl_negf_results/`, tests.

**Interfaces:** Использовать фактические manifests и identities Task 1. Выборочный reader принимает
HDF5 dataset path + selection и проверяет shape/axes/units/receipt до возврата небольшого блока.

- [x] Failing tests: конфликт identity, неизвестная quality, optical embedded receipt, selective
      read.
- [x] Обновить validation/readers/exporters и схемы всех callers без второй output policy.
- [x] Выполнить component pytest suites и fixture round-trip; не требовать старые matrices.

## Task 3: Конечные attempts AiiDA

**Files:** `components/qcl-negf-aiida/src/aiida_qcl_negf/{workflow,calculation,parser,service}.py`,
entrypoints/tests/docs.

**Interfaces:** `BaseRestartWorkChain` оборачивает существующий CalcJob; checkpoint/attempt identity
и integrity receipt из Task 1. Не создавать Slurm independent requeue.

- [x] Failing tests pause/failure/nonconvergence/repeated event/ambiguous ownership/budget.
- [x] Реализовать bounded restart и точный attempt/commit selection/retrieval.
- [x] Проверить AiiDA unit tests с изолированным существующим test profile; real Slurm migration
      оставить `not_verified`.

## Task 4: Platform application CD и Windows lifecycle

**Files:** `components/qcl-negf-platform/modules/{application,runner,cluster}.nix`, ops/workflow,
Windows adapters/tests/runbook.

**Interfaces:** Release identity и immutable Code executable path; общий Runner safe-pause и durable
receipt. Activation закрывает admission при любом частичном сбое.

- [x] Failing behavioral tests idempotent activation/partial failure/stale worker/old job.
- [x] Реализовать stable profile/runtime config и release workflow без routine `nixos-rebuild`.
- [x] Подготовить startup/shutdown адаптеры для всех jobs, публичный фиктивный access template,
      collector example.
- [x] Выполнить unit/Deno/syntax/Nix проверки доступные без hardware; записать недоступные
      приёмочные проверки.

## Task 5: Свежие scientific fixtures и research plans

**Files:** core numerical fixtures/tests, research definitions/examples/bounded plan.

**Interfaces:** Существующие adaptive impurity, finite-window Hilbert и safe callbacks; без новой
физической модели.

- [x] Проверить существующие малые fixtures и независимость oracle.
- [x] Добавить недостающие diagnostics §10 только с заранее заданными малыми размерами и бюджетами.
- [x] Обновить research examples canonical outputs; описать finite next plan без запуска кампании.

## Task 6: Независимое ревью и передача

- [x] Проверить diffs, формат, локальные ссылки и release graph.
- [x] Независимый reviewer проверяет concrete changes относительно требований, без утверждения
      hardware pass.
- [x] Исправить блокирующие замечания с regression tests внутри бюджета.
- [x] Сохранить отчёт AC0–AC8, команды/счётчики/ограничения, стоимость хранения и hardware blockers.
- [x] Отдельные reviewable component commits; без push/PR/merge/deploy и без публикации исходных
      массивов/секретов.
