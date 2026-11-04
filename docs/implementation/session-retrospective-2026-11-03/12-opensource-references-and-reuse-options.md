# Open-source references: чем заменить собственную обвязку и где замена неполна

Дополнение к ретроспективе по запросу пользователя4ноября2026. **Только анализ и evidence.** Ничего
не выделено в новую библиотеку, не установлено и не переписано. Исполнение программы, инфраструктура
и расписания остаются остановленными. Это карта сопоставления, а не новый большой migration plan.

## 1. Короткий ответ

Значительную часть общей функциональности можно назвать и отделить концептуально уже сейчас; карта
по Source — в[09](09-emergent-tools-and-reuse-boundaries.md). Это не доказывает, что её следует
превращать в отдельный продукт. Новая general-purpose library потребовала бы дополнительного API,
поддержки и тестов, а текущие runtime gaps никуда бы не исчезли.

Наибольшая потенциальная экономия — снова использовать уже выбранные Slurm/AiiDA/Nix/systemd как
владельцев их штатных операций и оставить небольшие QCL-specific adapters. Сначала требуется
доказать совпадение семантики на конкретном call path. Нельзя посчитать весь custom code лишним по
совпадению названий с open-source проектом.

## 2. Метод и сила выводов

Прочитаны primary official docs/repositories ниже4ноября2026 по Europe/Minsk. Capability из
документации отделена от вывода о применимости к QCL. Мы не запускали эти проекты, не измеряли
стоимость перехода, не проверяли все версии/лицензии/dependencies/installed compatibility и не
делали proof-of-concept. URLstable/latest может измениться; для реализации потребовался бы pinned
version и адресный review.

Локальный source log: `.build/session-evidence-followup-20261104/opensource-source-log.json`. Он
содержит12primary URLs, дату и scope. В публичный report не копируются raw web pages или private QCL
inventories. Для Parsl один старый guide URL и redirect дали404; этот route не используется как
подтверждение, прочитаны работающие official project/SlurmProvider pages. Не делается вывод «мы
исследовали эти альтернативы до написания кода»: исторического evidence такого сравнения пока нет.

## 3. Прямое переиспользование уже имеющихся инструментов

| Ref | Наш общий слой                                                                       | Native reference / что уже умеет                                                                                                                                                                                        | Что остаётся QCL/site-specific                                                                                                | Вывод по применимости                                                                                                                                                                                              |
| --- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| O01 | Job lifecycle, transfer/retrieval, provenance и их дополнительные state/receipt слои | [AiiDA CalcJob](https://aiida.readthedocs.io/projects/aiida-core/en/stable/topics/calculations/concepts.html): remote external code; upload→submit→update→retrieve; input/output provenance; transport failure handling | Подготовить input, выбрать executable, распознать result и scientific status, сохранить правильный exact-state/result binding | Первый кандидат на сокращение дублирующих lifecycle функций: framework уже выбран. Его retry transport не равен повтору несошедшегося scientific solve                                                             |
| O02 | Guest job memory enforcement, CPU/proctrack/accounting, cleanup cooperation          | [Slurm cgroup.conf](https://slurm.schedmd.com/cgroup.conf.html): configured memory/core constraints и proctrack/cgroup; настройка требует совпадения Slurm/OS capacity                                                  | Physical hypervisor RAM, foreign agreement, guest OS reserve, dynamic-balloon active-floor гарантия                           | Внутри guest использовать штатные limits вместо второго scheduler. Документация предупреждает, что memory-limit OOM не обязательно автоматически завершит все остальные процессы step; closure нельзя предполагать |
| O03 | Административный subprocess lifetime, process-tree cleanup, unit ownership           | [systemd.kill](https://www.freedesktop.org/software/systemd/man/latest/systemd.kill.html): unit lifecycle и KillMode=control-group для оставшихся процессов                                                             | Exact QCL operation/output identity, policy authority и cross-host reconciliation                                             | Проверить, какая часть собственного process supervision действительно нужна поверх unit/cgroup. Kernel absence/provenance и «мы послали stop» всё ещё разные факты                                                 |
| O04 | Closure copy/cache/staging как часть own release protocol                            | [nix copy](https://nix.dev/manual/nix/2.34/command-ref/new-cli/nix3-copy.html): перенос store closures между stores, substituters и profiles                                                                            | Выбор совместимого release, service health, mutable data и координация maintenance                                            | Часть delivery plumbing уже native. Сам copy не делает атомарной смену всего кластера; manual помечает CLI experimental, installed version отдельно                                                                |
| O12 | Bridge transaction rollback                                                          | [NetworkManager D-Bus](https://networkmanager.dev/docs/api/latest/gdbus-org.freedesktop.NetworkManager.html): CheckpointCreate с автоматическим rollback и явный CheckpointRollback                                     | Какие интерфейсы/профили наши, проверка connectivity, постоянная policy после reboot/IP change                                | Native rollback доступен через этот API. Published policy guard/WAL и Reapply из09 — отдельный механизм; они не заменяются одной строкой checkpoint и не являются реализацией нового native rollback               |

Эта группа не требует одновременно добавлять пять новых технологий: они уже являются частью
выбранного stack. Вопрос будущему review — где собственный код только связывает необходимые
scientific/site semantics, а где повторяет механизм владельца. Source-модули и границы сверены в09,
а происхождение требований в10/11.

## 4. Близкие сторонние проекты как references или альтернативы

| Ref / проект                                                                                                                                     | Подтверждённая функция                                                                                                  | С чем сравнивать в QCL                                                                             | Реальная граница / цена замены                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| O05 — [deploy-rs](https://github.com/serokell/deploy-rs)                                                                                         | Nix-flake multi-profile deployment; profile activation и auto/magic rollback при неподтверждённой connectivity          | Общую часть release/activation/delivery вокруг `application_release` и service-scoped profiles     | Не обещает coordinated PG/NFS backup или атомарный distributed transaction. Его SSH/privilege model надо сопоставить с VM isolation и нашими fixed capabilities. Кандидат для сравнительного разбора, не установлен                                  |
| O06 — [Colmena](https://colmena.cli.rs/unstable/)                                                                                                | Stateless NixOS deployment, тонкая оболочка над Nix-командами, parallel nodes                                           | Оркестрацию сборки/copy/activation нескольких декларативных NixOS roles                            | Manual прочитан дляunstable, не pinned release. Не scientific workflow и не владелец mutable application state; при simple maintenance-only rollout может быть ближе исходной цели, но соответствие ещё не проверено                                 |
| O07 — [Submitit](https://github.com/facebookincubator/submitit)                                                                                  | Небольшая Python submission abstraction поверх Slurm/local execution, logs/results; CommandFunction для внешней команды | Минимальную толщину adapter submit/status/log/cancel для существующего Julia executable            | Это не собственная task queue и не замена QCL exact checkpoint. Scientific continuation нужно сохранить внутри execution. Если остаётся AiiDA, вторая submission abstraction может только добавить слой; полезен прежде всего как reference масштаба |
| O08/O09 — [Parsl](https://parsl-project.org/) и [SlurmProvider](https://parsl.readthedocs.io/en/stable/stubs/parsl.providers.SlurmProvider.html) | Dataflow apps с dependencies; Python/external applications; provider использует sbatch/sacct/scancel                    | Собственную scheduling/workflow glue для независимых executions                                    | Это альтернативный workflow engine, не библиотека для подмешивания поверх AiiDA без нового lifecycle owner. Нет обещания physical PVE reservation или scientific acceptance                                                                          |
| O10 — [Snakemake Slurm executor](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html)                               | File-oriented workflow execution на Slurm, resource mapping кmemory/CPU/runtime и profiles                              | Внешнюю цепочку input→executable→output/analysis, если именно файловый workflow нужен пользователю | Замена модели workflow и provenance, а не drop-in исправление нынешнего actor protocol. Dependency points и exact-resume semantics не выводятся из факта существованияoutput file                                                                    |
| O11 — [ReFrame](https://reframe-hpc.readthedocs.io/en/stable/)                                                                                   | Portable HPC regression/benchmark pipeline: environments, compilation, job submission/status, sanity/performance checks | Объём собственной infrastructure qualification harness и platform-specific acceptance glue         | Не замена unit tests физического ядра и не generic scientific oracle. Внедрять новый test framework сейчас может увеличить сложность; полезно сравнить, какие host/test lifecycle механизмы мы повторили                                             |

Для этих проектов речь об общей функциональности, а не об обещании совместимости. Представленные
capabilities не обосновывают процент удаления кода, новый срок или «всё можно заменить одной
библиотекой». Установка/добавление всех references одновременно противоречила бы цели упрощения.

## 5. Что не найдено как готовая одношаговая замена

Комбинация «все VM resident + foreign physical reserves + online balloon/grow/shrink + durable
неизвестный исход host mutation + Slurm allocation + scientific output closure» не покрывается одним
из перечисленных инструментов целиком. Slurm управляет guest job allocations; PVE управляет VM;
AiiDA управляет scientific process/provenance; Nix управляет immutable software. Между владельцами
нужна некоторая согласующая policy или более узкий поддерживаемый режим.

Отсюда не следует, что необходимо дописать весь наш proof framework. Есть два разных решения:
сохранить сложный dynamic contract и обосновать его стоимость либо выбрать уже разрешённый fixed
reservation режим, где online переходов нет. Это **изменение поддерживаемой capability/ветви
исполнения**, а не заменаphysical гарантий красивой библиотекой. Какая ветвь нужна пользователю,
должна быть явным продуктовым решением; текущее поручение реализации не разрешает.

Ни один reference не проверяет уравнения NEGF, сохранность exact adaptive state, согласованность
физической модели, независимый reference oracle, сходимость или достаточность сетки. Эти части
scientific code нельзя объявить обвязкой только потому, что они имеют schemas или checkpoint API.

## 6. Извлечь наш общий код или заменить его?

Уже сейчас можно составить карту потенциальных leaf units: bounded command capture, atomic file
publication, stable artifact references, reusable read-only views, native observations. Но «не
содержит словаQCL» ещё не означает независимость: могут оставаться fixed role paths, Source
namespaces, budgets, UID/creator rules, state schema и runtime authority. Для выделения потребовался
бы реальный consumer внеQCL и contract, не завязанный на нашу историю failed attempts.

В отношении крупных units вывод строже: `host_resource_*` выглядит как специализированный control
plane/resource broker, а delivery/native-attempt — как части execution/activation protocol. Это
полезная **диагностика смещения задачи**, а не основание гордиться новым продуктом или немедленно
его выделять. Их готовность ниже обещания общего инструмента: есть незакрытые Native/workload gates.
Сохранить evidence и boundaries сейчас важнее, чем дать им новые названия/package repositories.

Порядок будущего анализа может быть простым:

1. Показать один реальный пользовательский call path и его владельцев.
2. Для каждого custom механизма указать required guarantee и соответствующий native API.
3. Если native API уже покрывает guarantee, оценить удаление wrapper/state duplication. Если нет —
   решить, нужна ли сама capability.
4. Лишь после этого выбирать между небольшим adapter, полноценной чужой системой или поддержкой
   собственного general unit.

Это вопросы для анализа сохранённого Source, не четыре новые implementation задачи.

## 7. Проверяемые выводы

| Утверждение                                                     | Свидетельство                                                                                     | Ограничение                                                | Решение                                        |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------- |
| Часть написанного относится к другим классам инструментов       | Source09: broker/delivery/verification/qualification; O01–O12 соответствующие existing mechanisms | Функциональная похожесть не означает готовую library       | сохранить карту и проверить necessity          |
| Open-source references есть                                     | 12 primary sources открыты при исследовании; конкретные capabilities выше                         | Нет runtime/compatibility/license assessment всего состава | сравнивать адресно, не устанавливать по списку |
| Всё наше можно заменить одним продуктом                         | Разные владельцы physicalVM/job/provenance/store/science                                          | Drop-in equivalence не установлена                         | данных недостаточно                            |
| Превратить обвязку в отдельный продукт — сокращение работы      | Потребуются новые contracts/support/consumers                                                     | Полезность нового продукта не запрошена                    | не начинать выделение                          |
| Требования заставляли обязательно написать именно такую систему | Initial plan допускает alternatives;10/11 показывают выбор трактовок                              | Часть гарантий действительно сложна                        | отличать requirement от решения                |
