# Проверки по влиянию

Общая registry в `ops/impact.ts` выбирает группы и конкретные команды для `impact`, `test`,
`prepare` и ручного workflow. Gitlinks остаются источником состава; отдельного revision lock нет.
План не запускает package checks, подготовку зависимостей, Julia, Nix evaluation или документацию.

## План и выполнение

```sh
deno task impact --base BASE --head HEAD
deno task prepare --base BASE --head HEAD
deno task test --base BASE --head HEAD
```

`BASE` и `HEAD` должны разрешаться в уже доступные commit objects. Planner использует raw NUL Git
diff без rename detection, внешних diff/textconv и shell interpolation. Для изменённого gitlink он
читает old/new objects в owning компоненте; checkout и fetch не выполняются. `.gitmodules` читается
из выбранного head, а не из working tree. Filename с пробелами или tab остаётся одним argv.
Небезопасный ref/path или malformed raw diff отклоняется. Отсутствующий object, новый/удалённый либо
неизвестный gitlink даёт явную uncertainty и полный релевантный охват.

Planner может читать историческую или dirty рабочую директорию: он описывает committed range. `test`
и `prepare` перед исполнением требуют чистый `sourceGraph`, точное совпадение текущего head с
выбранным и неизменную композицию после команд. Release guard в `ops/git.ts` не ослаблен.

Без аргументов `test` и `prepare` выбирают все группы. `--full`, `--python`, `--julia`, `--infra`
добавляют ручной охват к range; один ref без второго, повторы и неизвестные flags отклоняются.
Legacy `--julia` сохраняет обе Julia docs build и Results integration. Legacy `--python` включает
все Python owners, Research validator и frontend tests. `lock` сохраняет прежние команды и не
получает path routing.

## Границы групп

| Изменение                                    | Выбор                                                      | Дополнительное свидетельство                                                      |
| -------------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Prose `docs/**/*.md`, README и инструкции    | D: формат изменённых существующих файлов                   | Review локальных ссылок и anchors обязателен, planner его не объявляет пройденным |
| README Contracts/Results/AiiDA/Portal        | Owning checks                                              | README входит в wheel metadata; native wheel verification остаётся gate           |
| Contracts source                             | Python consumers, Core/Runner, Results integration         | Сохранены полные `test/runtests.jl`, включая независимые fixtures/oracles         |
| Results / AiiDA                              | Results→AiiDA→Portal / AiiDA→Portal                        | Prepared locked Python workspace                                                  |
| Core или Runner source                       | Оба Julia packages и Python consumers, Results integration | Без автоматической Julia docs build для обычного source change                    |
| Portal frontend                              | Frontend и Portal                                          | Native frontend assets и wheel boundary                                           |
| Research config/literature                   | Research tests и validator                                 | Не означает научную приёмку постановки                                            |
| Platform source, Nix, Tofu                   | Platform и infra                                           | Provider preparation, native package/service/VM gates отдельно                    |
| Root assembly/build либо неизвестное влияние | Полная integration closure                                 | Uncertainty остаётся в плане; научный опыт не запрашивается                       |

`LICENSE`, package metadata, executable YAML, `docs/make.jl`, assets, Project/Manifest не считаются
обычным prose. Симлинки и неподдержанные modes дают uncertainty. Add/delete сохраняют modes;
удалённый Markdown требует review ссылок, но formatter не получает отсутствующий файл.

## Явная подготовка

`checkCommands` никогда не запускает `tofu init`, environment sync, bootstrap или Pkg instantiate.
Проверка отсутствующей зависимости завершается ошибкой; fallback установки нет. Сообщения
`Prerequisite/review gate` описывают невыполненные внешние условия, а не результаты проверки.

`prepare` выполняет только команды подготовки выбранных групп. Python использует единый locked
workspace через `uv sync`; Portal входит в этот workspace и его wheel hook требует предварительные
`npm ci --ignore-scripts` и frontend build даже при изменении другого Python owner. Это native
prerequisite, не Julia dependency. Platform использует свой существующий `python3 -m pytest`;
необходимые Python/pytest зависимости должны быть доступны отдельно, planner их не устанавливает.

Julia preparation явно включает pinned runtime bootstrap и `Pkg.instantiate()` текущего workspace.
Это отдельное потенциально дорогое действие, не скрытая часть проверки или D/L source audit. В CI
`JULIA` указывает на подготовленный Runner executable; локально оператор задаёт фактический `JULIA`
либо предоставляет `julia` в PATH. Tofu init находится только в prepare, с
`-backend=false -input=false -lockfile=readonly`. Nix `flake check --no-build` в infra остаётся
source evaluation, не service readiness.

## Ручной workflow

Trusted self-hosted workflow сохраняет `full` и `runner-smoke`; `changed` принимает существующий
локальный base ref. Вход передаётся через env как один аргумент и проверяется CLI, не вставляется в
shell source. Workflow последовательно печатает план, явно готовит выбранные зависимости и выполняет
выбранные checks. Для D prepare не запускает package commands. Shallow/missing refs не fetch-ятся
автоматически: нужно отдельно подготовить известные objects либо выбрать full.

Pinned checkout, `persist-credentials=false`, `cancel-in-progress=false`, trusted runner labels и
защита runner-smoke account сохранены. Автоматических PR/fork/CD triggers нет. Source/L planner
fixtures не доказывают фактическое выполнение workflow, package build или native cluster readiness.
`scientificStage` всегда `not_requested`; новый SCBA/Poisson требует отдельного поручения.
