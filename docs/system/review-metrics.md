# Метрики комплексного ревью QCL-NEGF

Статус: **предложение**, не принятые пороги, новые gates или поручение запускать
проверки.

Метрики нужны исследователю, оператору и разработчику на равных:
объяснить, какое свойство проверено, каким свидетельством и в каких пределах.
Их применение к полному review описывается в
[программе review](comprehensive-review.md), документации — в
[методологии](documentation-methodology.md). Формализация, документация,
ревью кода и научная приёмка имеют равный приоритет. Метрики помогают
декомпозировать каждое направление до проверяемых задач; ни одна группа не
задаёт общую очередь для остальных.

Срез исходников: root `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1` и восемь
его gitlinks. На 2026-10-14 root содержит уже существовавшие изменения
`AGENTS.md`, `README.md`, `TODO.md`, `docs/architecture.md`,
`docs/single-server-deployment.md` и локальный `docs/system/`; они сохранены.
Прежние документы этого корпуса — источники утверждений для перепроверки,
а не автоматически актуальное ТЗ. Каталог требований и target необходимо
актуализировать по RV00; факты о компонентах относятся к выбранному исходному
составу. Bootstrap и более новые PR имеют собственные
source/runtime identities и не наследуют приёмку этого среза. Gitlinks остаются
источником ревизий; таблица ниже не является вторым lock-файлом.

| Равноприоритетное направление | Что раскрывают существующие метрики | Что проверяется отдельным review |
| --- | --- | --- |
| Формализация | M01 — проверяемые требования; M06/M12 — состав и границы; M15 — ограничения конфигурации | Актуальность цели, альтернатив, оснований и статусов решений по RV00/RV03; число документов не мера полноты требований |
| Документация | M14–M17 — смысл API/config, drift, примеры и три человеческих сценария | Связное объяснение и применимость методики; generated reference не заменяет учебный текст |
| Код и инфраструктура | M02/M04–M13 — исполнение, отрицательные случаи, воспроизводимость, восстановление, связность и сложность | Адресные дефекты и refactoring tickets с owner; агрегированный балл качества не вводится |
| Научная приёмка | M03/M18–M20 — независимость oracle, полнота данных, критерии и стоимость свидетельства | Физическая применимость и сопоставимость с литературой; зелёный CI не является научным результатом |

Готовность agent ticket определяется [контрактом задачи](agent-review-workflow.md),
а применимость skills — [их отдельным аудитом](skills-and-instructions-review.md).
Отсутствие входа, oracle или конечного бюджета отмечается в конкретной карточке.
Закрытие карточки означает достижение её объявленного результата, а не общий
`pass` проекта. Один ticket выбирает нужные M-ID; все двадцать одновременно
не требуются.

## Репозитории, языки и область измерения

«Функции» здесь означают обязанности и конкретные публичные операции, а не
число функций или строк. Язык данных не равен языку исполнения. Тесты,
fixtures, инструменты и генерируемые assets следует учитывать отдельно от
runtime. Процент расширений файлов не выражает качество или стоимость расчёта.
M01, M06 и M12 применимы ко всем репозиториям; остальные связи показывают
основной предмет проверки, а не исключают интеграционные свойства.

| Репозиторий | Основные языки; вспомогательные форматы | Цель, задачи и функции владельца | Первичный локатор; метрики |
| --- | --- | --- | --- |
| Root `qcl-negf` | TypeScript/Deno; Julia, Nix, Python, Bash, TOML/YAML | Состав релиза, интеграционное окружение, lock/CI/release/depot; `sourceGraph`, `sync`, `lock` | [deno.json](../../deno.json), [pyproject.toml](../../pyproject.toml), [ops/git.ts](../../ops/git.ts), [ops/environment.ts](../../ops/environment.ts); M02, M07–M08, M11, M16 |
| `QCLNEGF.jl` | Julia; TS/Python tooling, CSV reference data | In-memory модель, reference/optimized операторы, SCBA/Poisson, наблюдаемые; `build_problem`, `solve`, `retarget_problem` | [Project.toml](../../components/QCLNEGF.jl/Project.toml), [API exports](../../components/QCLNEGF.jl/src/QCLNEGF.jl), [README](../../components/QCLNEGF.jl/README.md); M02–M04, M13–M14, M16, M19–M20 |
| `QCLNEGFRunner.jl` | Julia; TS, Nix, YAML/JSON/HDF5 | CLI и resolver, frozen plan, resource inspection, checkpoint, staging, анализ/optional plots; `main`, `execute_scientific_plan_staged`, `stage_result_tree` | [Project.toml](../../components/QCLNEGFRunner.jl/Project.toml), [API exports](../../components/QCLNEGFRunner.jl/src/QCLNEGFRunner.jl), [README](../../components/QCLNEGFRunner.jl/README.md); M02–M04, M08–M09, M13–M16, M18–M20 |
| `qcl-negf-contracts` | Python; JSON Schema/JSON | Форматы, чистая валидация и semantic boundary; `decode`, `scientific_plan`, `branch_reason`, `validate_commit` | [pyproject.toml](../../components/qcl-negf-contracts/pyproject.toml), [README](../../components/qcl-negf-contracts/README.md), [messages.py](../../components/qcl-negf-contracts/src/qcl_negf_contracts/messages.py); M02, M04, M14–M16, M18–M19 |
| `qcl-negf-results` | Python; Julia fixture generators, HDF5/Parquet | Независимое чтение и диагностика сохранённых данных, snapshots/export; `StateReader`, `verify_recovery_bundle`, `export_snapshot` | [pyproject.toml](../../components/qcl-negf-results/pyproject.toml), [state.py](../../components/qcl-negf-results/src/qcl_negf_results/state.py), [README](../../components/qcl-negf-results/README.md); M02–M04, M09, M13–M14, M16, M18–M20 |
| `qcl-negf-aiida` | Python; JSON fixtures | Provenance и исполнение: CalcJob/Parser/WorkChain, submit/restart/cancel, exact artifact locator; `submit_plan`, `get_export_plan`, `open_artifact` | [entry points](../../components/qcl-negf-aiida/pyproject.toml), [service.py](../../components/qcl-negf-aiida/src/aiida_qcl_negf/service.py); M02, M04–M05, M08–M09, M13–M14, M18–M20 |
| `qcl-negf-portal` | Python/FastAPI и TypeScript/TSX/React; CSS/HTML, Nix | Authentication/admission, HTTP и светлое представление, bundled browser assets; submit/status/result/download/cancel, без собственного solver/scheduler | [pyproject.toml](../../components/qcl-negf-portal/pyproject.toml), [package.json](../../components/qcl-negf-portal/frontend/package.json), [README](../../components/qcl-negf-portal/README.md); M02, M04–M05, M08, M13–M17, M18–M19 |
| `qcl-negf-research` | YAML/CSV с Python validator; Markdown | Постановки и литература, variants и контролируемые сравнения; `validate`, S01/equilibrium и convergence inputs | [README](../../components/qcl-negf-research/README.md), [validate.py](../../components/qcl-negf-research/tools/validate.py), [scientific-inputs](../../components/qcl-negf-research/docs/scientific-inputs.md); M03–M04, M15–M19 |
| `qcl-negf-platform` | Nix, Python, TS/Deno, HCL/OpenTofu; PowerShell, YAML | NixOS roles, VM/provider lifecycle, build admission, activation, trust/cache, storage/recovery, Windows worker operations | [flake.nix](../../components/qcl-negf-platform/flake.nix), [deno.json](../../components/qcl-negf-platform/deno.json), [README](../../components/qcl-negf-platform/README.md), [tofu](../../components/qcl-negf-platform/tofu); M02, M04–M05, M07–M11, M13–M17, M18, M20 |

## Что заимствовать из отлаженных процессов

Проверены первоисточники 2026-10-14. Это основание предложенных способов
проверки, а не доказательство их внедрения в QCL-NEGF.

| Проект / практика | Адаптация к QCL-NEGF |
| --- | --- |
| SciPy связывает PR с tests, public docstrings/examples и проверкой rendering. Его `special` содержит сравнения с mpmath и точками DLMF; это конкретный пример внешнего numerical oracle. [Workflow](https://docs.scipy.org/doc/scipy/dev/contributor/development_workflow.html), [test_mpmath.py](https://raw.githubusercontent.com/scipy/scipy/main/scipy/special/tests/test_mpmath.py) | M03, M14, M16: формула/аналитический предел или независимо вычисленный эталон. Совпадение двух путей с общей реализацией не доказывает независимость. Чужие tolerances не переносить |
| NumPy описывает parametric numerical assertions, форму/dtype, абсолютный и относительный допуск; doctests проверяются отдельно. Numpydoc задаёт Parameters/Returns/Raises/Notes/References/Examples. [Testing](https://numpy.org/doc/stable/reference/testing.html), [docstring guide](https://numpydoc.readthedocs.io/en/latest/format.html) | M04, M14–M16: единицы, оси, веса, ошибки и применимость вместе с API; Julia docstrings могут иметь ту же смысловую структуру. Текст примера не означает его выполнения |
| CPython требует соответствующие tests для semantic changes, различает line/branch и рекомендует измерять собственные tests выбранного модуля отдельно от косвенного исполнения. [Coverage](https://devguide.python.org/testing/coverage/) | M01–M02: адресный denominator и отчёт о пропусках. Его стремление к 100% не устанавливает порог QCL; вывод о недостаточности line coverage следует из различия исполнения строки и проверки свойства |
| Kubernetes разделяет unit/integration/e2e, использует повторения для flakes, owners и историю TestGrid; critical conformance имеет отдельный предмет проверки. [Testing guide](https://github.com/kubernetes/community/blob/main/contributors/devel/sig-testing/testing.md), [SIG Testing](https://www.kubernetes.dev/community/community-groups/sigs/testing/), [conformance dashboard](https://testgrid.kubernetes.io/conformance) | M04–M05, M11: failure history и критический lifecycle на реальном backend. Не копировать Kubernetes, Prow, частоту reruns или его release gates |
| Nixpkgs consumer tests отделены от build environment; NixOS tests запускают VM. `nixosOptionsDoc` получает данные из объявленных options. Nix отдельно предупреждает о nondeterminism и ограниченности двух rebuilds. [Nixpkgs](https://nixos.org/manual/nixpkgs/stable/#var-passthru-tests), [NixOS tests](https://nixos.org/manual/nixos/stable/#sec-nixos-tests), [options source](https://raw.githubusercontent.com/NixOS/nixpkgs/master/nixos/lib/make-options-doc/default.nix), [reproducibility](https://reproducible.nixos.org/) | M07–M11, M15–M16: eval, consumer behavior, VM, native backend и restore — отдельные свидетельства. Declarative configuration сама не гарантирует воспроизводимость или исправность услуг |

## Реестр предлагаемых метрик

Каждое множество в denominator фиксируется **до проверки** после актуализации
его требований: версия каталога,
owner, source, applicability, exclusions с причиной. Запись свидетельства
содержит source ref, report hash, query/selection, tool/version и runtime hash;
неизмеренные поля имеют статус `not_measured`, не нулевые значения. Показывать
`n/N` вместе
с процентом; `N=0` означает `not_applicable` с объяснением, неизвестный `N` —
`not_measured`. Не менять denominator после неудачи. Численные значения метрик
здесь не измерялись; наличие тестового файла не подтверждает pass. Каталоги
требуют согласования.

Стоимость: **0** — metadata/адресное чтение/static review; **1** — bounded
unit/docs/fixture checks в уже доступном окружении; **2** — build, VM или
production backend; **3** — solver, numerical experiment или профилирование.
Уровни 1–3 не разрешены данным документом: ticket задаёт конечный общий
бюджет attempts, CPU/RAM, wall time, output, stop rule и ожидаемое свидетельство.
Чтение ранее сохранённого bounded отчёта возможно на уровне 0.

| ID / назначение | Определение, scope и denominator | Источник / требуемое свидетельство; стоимость | Смысл и ограничение |
| --- | --- | --- | --- |
| **M01 Property coverage** | `n/N`: актуальные принятые проверяемые properties с воспроизводимым evidence / все применимые properties выбранного ticket/release. Отдельно наличие проверки и её результат | Перепроверенные requirements/owner contract → test/scenario → report на exact source; статус и основание решения; 0/1–3 | Не процент строк; старый docs-каталог не автоматически denominator. Mock, production и scientific claims раздельны |
| **M02 Исполнение кода** | Для каждой пары repo×язык: executed/instrumentable lines; taken/declared branch outcomes. Scope production source, exclusions/generated/vendor/tests перечислены | Instrumentation report, tool/version, suite/environment, skipped paths; 1–3 | Не усреднять языки или line/branch. Julia line report не подменяет branch report |
| **M03 Независимые oracles** | `n/N`: numerical properties, имеющие проверенный независимый oracle / каталог требующих oracle properties; аналитика, manufactured solution, внешний high-precision путь отдельно | Core `test/physics`, `test/numerics`, Results analytic fixtures; derivation и зависимостный graph oracle; 0/1/3 | Общий helper/reference допускает общую ошибку; oracle применим лишь к объявленной области |
| **M04 Fault-case coverage** | `n/N`: проверенные пары property×failure case / согласованный risk catalogue: wrong attempt/hash, truncation, duplicate, zero/NaN, restart/cancel/resource denial | Contracts/Runner/Results/AiiDA/Portal/Platform fixtures и observed outcome; 0/1/2 | Количество tests не denominator. Synthetic solver подтверждает orchestration, не SCBA |
| **M05 Flakiness** | `n/N`: tests с pass+fail / tests с достаточными одинаковыми повторами; minimum repeats и окно заранее согласованы. Per test: fail/valid runs, counts, exact source/environment/inputs | Неотброшенные original logs, seed, host/tool identity, timestamps; 1/2/3 | Failure fraction не flaky fraction; all-fail не flaky. Infra failures отдельны; нет rerun-until-green |
| **M06 Source/dependency closure** | `n/N`: проверенные identity links / все links в производном source/build/import graph; unresolved/mismatched edges списком. Отдельно selected source, package metadata и фактически imported source | Gitlinks, native locks, derivation/runtime receipt, imported paths/hash; 0, build/import evidence 1/2 | `0.2.0` не identity. Lock не доказывает, что runtime его использовал; второй ручной revision lock не нужен |
| **M07 Bitwise rebuild** | `n/N`: побитно совпавшие declared outputs / все declared outputs сравнимых независимых rebuilds; host/environment/source фиксированы | Output hashes и diff, derivations, rebuild logs; 2 | [Определение reproducible build](https://reproducible-builds.org/docs/definition/) требует идентичности bytes; две удачные сборки — ограниченная выборка |
| **M08 Functional rebuild** | `n/N`: выполненные consumer properties / все заранее объявленные functional properties каждой build/runtime pair | Native package/CLI tests, ABI/API/config compatibility reports; 1/2 | Может pass при разных bytes; не заменяет M07 или научную приёмку |
| **M09 Recovery** | Для scenario×dataset: observed RPO = incident time − latest recovered consistent commit time; RTO = validated recovery time − incident time, секунды; loss generations/bytes отдельно | Coordinated PostgreSQL+repository archive/restore, Runner checkpoint/staging receipts, incident timeline; 2/3 | Только измеренная область и окно; estimate/backup schedule не measured bound. NFS и scratch не автоматически backup |
| **M10 Idempotence/drift** | Повторный apply: objects с unexpected changes / объявленные managed objects; drift: mismatching observed objects / inventoried managed objects на дату | Desired config, actual inventory, first/second receipts и diff; 1 fake, 2 real | Fake Commands не подтверждают production. Private inventory отсутствует — неизвестный denominator |
| **M11 Cold/native lifecycle** | Матрица role×backend×scenario: install/boot/enroll/submit/cancel/stage/restart; `n/N` принятых cells / применимые cells утверждённой матрицы | Fresh-source build/boot receipts и native Proxmox/libvirt/Hyper-V scenarios; 2 | Nix eval и QEMU VM не являются native acceptance всех backend; scientific payload отдельно |
| **M12 Coupling/ownership** | По каждому runtime/build/import graph: SCC с >1 узлом, self-cycles, запрещённые edges; fan-in/out. Denominator edges выбранного graph; violation count и локаторы | Package metadata, imports/calls, executable/file boundary, утверждённые owner rules; 0 | Metadata DAG не исключает dynamic import, file или orchestration cycles; shared contract edges допустимы |
| **M13 Complexity/blast** | Per function: CFG complexity `E−V+2P` (edges, vertices, components), fan-out; hotspot = changes/window×complexity. Blast = число transitive affected interfaces/tests выбранного graph | AST/CFG с описанием Julia dispatch, Git window и review сопоставления; 0/1 | Ranking для адресного review, не defect и не LOC gate; без CFG/tool/window число неизвестно |
| **M14 API docs semantics** | `n/N`: public API items с проверенным обязательным смыслом / каталог exports, CLI commands/flags, HTTP endpoints; params/units/returns/errors/side effects/status/origin по применимости | Source signatures, docstrings/OpenAPI/CLI reference и semantic review; 0/1 | Generated signature не объясняет физический смысл; undocumented API не становится private автоматически |
| **M15 Config docs semantics** | `n/N`: public config paths×conditions с type/default/effective origin/units/constraints/override/migration / каталог paths×conditions выбранных schemas/options/resolver | Contracts schemas, Runner resolver, Platform options, Research YAML; source-to-doc mapping; 0/1 | Schema default не всегда effective value; синтаксическая validation не проверяет уравнения |
| **M16 Drift/examples** | Drift: symmetric difference declared/generated documented item sets + broken links. Examples: verified safe executable examples / предварительный список safe examples; costly examples отдельным статусом | Exact-source doc generation report/diff, example logs; 0/1, costly 2/3 | Rendering, links и examples — отдельные результаты; непроверенный solve-пример остаётся `not_measured` |
| **M17 Три doc journeys** | `n/N`: выполненные journey×condition cells / agreed matrix researcher/operator/developer×light/offline/search; success/time/ошибки отдельно | Задачи: найти критерий+raw locator; release+restore; API+test+owner. Browser/static bundle review; 0/1 | Три равные роли; offline = без внешней сети, локальные assets/math/search. Не usability процент без protocol/participants |
| **M18 Provenance/raw closure** | `n/N`: verified required references/files/datasets / closure выбранного declared archive profile; hashes, frozen plan, model/source, run/attempt/state, axes/units/weights | Artifact hash + commit/manifest/HDF5 path+selection, независимый Results reader; 0/1 | Integrity не convergence; missing weights/state — missing. Полнота profile не означает полноту всех научных вопросов |
| **M19 Научные критерии/статусы** | `n/N`: полностью определённые criteria / применимые frozen criteria: нормировка, веса, единицы, допуск/основание, near-zero правило, evidence. Отдельный вектор execution/convergence/physics/discretization/experiment | Owning Core/Research criteria, raw map/Poisson/FDR evidence, controlled refinements и literature experiment; 0/3 | Нет общего зелёного среднего. Experimental validation требует сопоставимой постановки; unknown не pass |
| **M20 Стоимость свидетельства** | Wall seconds до принятого claim; для недостигнутого claim censored elapsed. Allocated core·s и actual CPU s раздельно, peak RSS bytes, I/O bytes, attempts; scope все участники | Saved telemetry с source/run/sample window/overhead и admission receipts; 0, новая telemetry/profile 2/3 | Время процесса не время до решения; missing CPU/RAM/I/O не ноль. Модель и tolerances ради метрики не менять |

Для M02 кандидаты инструментов: Python `coverage.py --branch`, Julia
`--code-coverage`/LCOV и Deno coverage, для portal Node test coverage с проверкой
source mapping к TS. Они не установлены и не запускались этим review.
[Python branches](https://coverage.readthedocs.io/en/latest/branch.html),
[Julia source-line coverage](https://docs.julialang.org/en/v1/manual/command-line-interface/),
[Deno line/branch/function](https://docs.deno.com/runtime/reference/cli/coverage/),
[Node 24 test coverage](https://nodejs.org/docs/latest-v24.x/api/test.html#collecting-code-coverage).
Для Julia branch остаётся `not_measured` без подходящего отдельно проверенного
инструмента. Для Nix/HCL сначала M01/M04/M10–M11; format/eval/plan не выдавать
за line coverage. Тесты TS helpers не покрывают весь React/UI journey.

## Как вводить без превращения метрик в самоцель

Первая волна — по одному ограниченному срезу каждого направления, параллельно
на уровне 0: актуализировать requirements/owner properties (M01/M12),
сопоставить один API и его объяснение (M14/M16), разобрать один риск границы
компонентов и уже сохранённые tests (M04/M06), проверить определения одного
научного критерия и полноту доступного evidence (M03/M18/M19).
Полученные каталоги и gaps обсуждаются до назначения численных targets.
Например,
property «export выбирает один exact attempt вместе с plan и raw bytes»
проверяется интеграционной synthetic fixture нескольких attempts; line coverage
каждой функции по отдельности не подтверждает согласованность границы.
Будущий запуск этой fixture требует своего bounded ticket.

При owning changes выбирать M02/M15–M17 для кода и документации; M05 — только
с настоящей историей повторений; M07–M11/M20 — к порученному build/operator/
scientific этапу; M13 — к конкретному hotspot. Все двадцать метрик не становятся
обязательными gates каждого PR. Target обсуждать по baseline, цене ошибки,
критичности и стоимости проверки; не копировать универсальные «80%» из чужих
проектов. Для critical property предлагать конкретный обязательный сценарий,
для остальных — видимый gap и адресную следующую проверку.

Issue фиксирует property/risk/owner/source/denominator/budget. Component PR
связывает изменение с M-ID, обновляет близкий к коду контракт и прикладывает
точный report либо `not_measured` с причиной. Root затем обновляет опубликованный
gitlink. На общей светлой doc-панели предлагается **представлять** эти reports
по трём равным journeys: значение `n/N`, applicability, дата, source/runtime,
cost, witness и limitation, с ссылкой на owning source; централизовать копии
формул и правил приёмки там не следует. Это предложение представления,
не новый runtime telemetry service или автономный запуск проверок.

Owner обновляет запись при изменении соответствующего API/contract/source;
старое свидетельство сохраняет старую identity. Researcher проверяет научный
смысл, operator — реальные runtime/recovery пределы, developer — реализацию и
tests; разногласие сохраняется вместе с дешёвым различающим check. Dashboard
не переименовывает skipped, blocked, missing или not_measured в pass.

## Рабочие выводы

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Владение и языки различаются; один общий coverage % скрывает смысл | Root `e48e5b2` + gitlinks; manifests и локаторы таблицы | Это статический срез, не runtime inventory | сохранить |
| Версия пакета недостаточна для source identity | Runner `Project.toml` с `rev="v0.2.0"`; root gitlink Core `3108150…`; workspace `prepare_workspace.jl` и `julia/Manifest.toml` выбирают local paths | Standalone и workspace resolution различаются; imported runtime здесь не исполнялся | дополнительно измерить |
| Test portability — отдельное property | Results `fe27a2a…`, `tests/test_equilibrium_diagnostics.py:37–38,112–113`: абсолютные owning paths; [draft PR6](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/pull/6), head `a1492b7…` | Этот review не запускал candidate tests; full integration требует отдельного свидетельства | изменить |
| Есть основания для метрик свойств и документации | Проверенные первоисточники SciPy/NumPy, CPython, Kubernetes, NixOS/Nixpkgs | Они не задают универсальные tolerances/пороги QCL | сохранить |
| Проценты, flakiness, rebuild, RPO/RTO и science acceptance пока неизвестны | Выполнены только адресное чтение исходников и литературы; suites/build/VM/solver/profile не запускались | Наличие tests и declarative config не evidence pass | данных недостаточно |
