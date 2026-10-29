# QCL-NEGF

An integrated, reproducible workspace for quantum-cascade transport research. Julia computes the
numerical model, AiiDA records scientific workflows, Slurm allocates resources, and NixOS defines
the machines. GitHub hosts source and workflow state; CI runs on your own runner.

## Текущая программа и руководства

Для исполнения программы от 2026-10-27 начните с
[исполнительного плана](docs/implementation/codex-execution-2026-10-27.md),
[архитектурных решений программы](docs/implementation/project-simplification-2026-10-27.md) и
[AGENTS.md](AGENTS.md). Их актуальные scoped полномочия определяют порядок работ.
[Текущий рабочий маршрут](docs/current-workflow.md) связывает руководства исследователя,
разработчика и оператора с их owning компонентами и проверками.

[Корпус требований](docs/system/README.md) и прежняя
[точка входа этапа 1](docs/system/implementation-entrypoint.md) сохраняют контекст проекта; для
продолжения программы используйте исполнительный план выше. [Архитектура](docs/architecture.md)
описывает границы компонентов. Опубликованный исходный код, сборка, установленная система и научная
приёмка имеют отдельные свидетельства: публикация PR сама по себе не подтверждает готовность
сервера.

Новый научный запуск — отдельный следующий этап после инженерной synthetic-приёмки. Постановка
первой стационарной точки приведена в
[Research S01](components/qcl-negf-research/docs/equilibrium-s01.md).

## Components

Each directory below is an independent Git submodule. The superproject commit identifies the
complete compatible source set; there is no separate manually maintained source-revision lock.

| Submodule                       | Responsibility                                                                               |
| ------------------------------- | -------------------------------------------------------------------------------------------- |
| `components/QCLNEGF.jl`         | Julia scientific library: domain types, physics, numerical operators and in-memory solving   |
| `components/QCLNEGFRunner.jl`   | Julia scientific execution: plans, file adapters, checkpoints, CLI and local scratch staging |
| `components/qcl-negf-contracts` | Shared schemas and validation                                                                |
| `components/qcl-negf-results`   | Independent reading, verification, export and visualization of results                       |
| `components/qcl-negf-aiida`     | CalcJob, Parser, WorkChain and workflow service                                              |
| `components/qcl-negf-portal`    | Authenticated FastAPI service and its React client                                           |
| `components/qcl-negf-research`  | Scientific input catalog and literature provenance                                           |
| `components/qcl-negf-platform`  | NixOS roles, OpenTofu infrastructure and Arch host preparation                               |

See [architecture](docs/architecture.md), [GitHub initialization](docs/publication.md), and
[infrastructure](components/qcl-negf-platform/docs/infrastructure.md). For existing checkouts, see
[the organization transfer procedure](docs/organization-transfer.md).

## Исследовательская работа с агентами

Правила с приоритетом физической корректности находятся в [AGENTS.md](AGENTS.md). Четыре навыка в
`.agents/skills` помогают подготовить постановку, проверить физику, разобрать готовые результаты и
оценить производительность. См. [рабочий процесс, Codex и веб-ChatGPT](docs/research-workflow.md) и
[задачу упаковки результатов в RO-Crate](TODO.md#results-ro-crate).

## Подготовка и проверки

Клонируйте выбранную ветку вместе с зафиксированными компонентами:

```sh
git clone --branch codex/project-simplification-2026-10-27 --recurse-submodules https://github.com/Afonenko-QCL-NEGF/qcl-negf.git
cd qcl-negf
git rev-parse HEAD
git status --short
git submodule status --recursive
```

В существующем checkout сначала сохраните посторонние изменения. Не обновляйте submodules до latest
ради воспроизведения выбранного состава. Его определяют root gitlinks; package locks определяют
внешние зависимости.

[Проверки по влиянию](docs/impact-checks.md) разделяют подготовку и выполнение:
`deno task impact --base BASE --head HEAD` только показывает план по committed Git objects.
`deno task prepare --base BASE --head HEAD` явно готовит выбранную среду;
`deno task test --base BASE --head HEAD` выполняет проверки без скрытого bootstrap. Без refs
сохраняется полный охват. Запуск проверок требует подходящей подготовленной среды; для source D
достаточно форматирования, ссылок и review.

Nix development shell предоставляет инструменты разработки; Julia 1.13.0 подготавливается отдельно
по owning инструкции Runner. Локальный `JULIA` выбирает интерпретатор для разрешённых проверок, но
не доказывает эквивалентность квалифицированной Nix factory. Изменения зависимостей оформляются
через native resolvers командой `deno task lock` с review полученных locks, а не ручным заполнением
hashes.

[Документация](docs/cached-documentation.md) имеет отдельные `docs:plan`, `docs:prepare`,
`docs:build` и source-only `docs:check` с явными подготовленными inputs. Последняя команда требует
asset map, Node 24 и Python 3.14 с PyYAML/jsonschema; она не устанавливает prerequisites. Unit
checks не подтверждают render, cache hit или браузерную приёмку.

## Local scientific work

The core library can be cloned and used independently on Arch Linux without any server services.
Inside this workspace, run a small example using the prepared environment:

```sh
"$JULIA" --project=julia components/QCLNEGF.jl/examples/02_bdd_and_basis.jl
"$JULIA" --project=julia components/QCLNEGF.jl/examples/03_scalar_green.jl
```

The runner provides the same scientific CLI used by AiiDA. Scientific parameters are explicit;
resource limits never silently reduce the numerical model or relax convergence criteria.

## Builds and infrastructure

```sh
deno task graph
deno task release /var/lib/qcl-negf-releases --build
deno task solver:depot /var/lib/qcl-negf-artifacts/julia-0.2.0
deno task solver:build /var/lib/qcl-negf-artifacts/julia-0.2.0/solver-depot.json
```

The release command checks the actual Git source graph, builds four Python wheels using the locked
build environment, retains their hashes and source provenance, and optionally builds the Nix
application. Julia has its own prepared dependency depot and Nix package, so changing the web client
does not re-prepare the numerical environment.

`solver:depot` downloads the dependencies selected by the committed Julia manifest into a fresh
depot, creates an archive and computes its hash automatically. It writes `solver-depot.json` for the
local build and private site flake. Copy this JSON into the private site repository; retain the
archive outside source control. The default artifact URL is local to the build machine.
`solver:build` first uses `nix store prefetch-file` to verify a local archive against the receipt's
hash, with the same stable output name as the Nix depot fetcher. Run this step on the builder before
building private-site images: a cold, direct site build cannot read an arbitrary local `file://`
archive through the filesystem sandbox. Retain the original archive so the verified prefetch can be
repeated after garbage collection; its store copy counts toward the artifact disk budget. A receipt
still contains only the artifact URL and hash, never archive bytes. For another builder, pass
`--url https://YOUR-ARTIFACT-SERVER/depot.tar.gz` and upload the generated archive to that exact
address through your artifact storage. The command itself does not upload.

Существующий Proxmox-кластер разделяет storage, control, compute и изолированную CI VM. Первый
дополнительный worker программы — Linux/libvirt на ноутбуке; доступность и готовность подтверждаются
отдельными boot/enrollment/synthetic checks. Hyper-V и другой Proxmox проверяются после подготовки
пользователем. NFS принадлежит storage VM; scratch worker остаётся локальным. CPU/RAM задаются по
свежим ресурсам и защите хоста. Значения прежних примеров не являются текущим grant или
доказательством готовности; SMT threads не равны физическим ядрам.

Keep real host addresses, credentials, disk choices and application state outside this public
workspace. Use the platform's private-site example and its image/provisioning commands. The source
repository never contains generated VM images, dependency depots or scientific results.

For an initial deployment with only the four Proxmox roles, see the
[single-server deployment procedure](docs/single-server-deployment.md).

MIT license. See [CONTRIBUTING.md](CONTRIBUTING.md).
