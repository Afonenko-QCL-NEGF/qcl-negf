# Пересмотр навыков и инструкций QCL-NEGF

Исторический статус: самостоятельный результат read-only аудита и предложений
изменений от 2026-10-14. Уточнение authority/epoch SI01 — 2026-10-19.
Формализация, документация, ревью кода/архитектуры и научная приёмка
имеют равный приоритет. Исследователь, оператор и разработчик — равноправные
читатели и исполнители. Цель пересмотра — задания, которые агент доводит до
проверяемого результата конечным циклом, без постоянного пересогласования.
Сам документ не поручает реализацию кода, solver или изменение навыков и не
отменяет уже выданные пользователем полномочия активного задания.

Корпус содержит решения и историю затянувшейся сессии; нормативные утверждения
требуют повторной проверки по запросу пользователя, коду и владельцам контрактов.
Старый roadmap не принимается автоматически как ТЗ. Физическая добросовестность
ограничивает допустимые научные выводы во всех равноприоритетных очередях.

## Основание и воспроизводимость

Исторический audit HEAD: `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`.
Стартовый status того чтения: изменены AGENTS, README, TODO, architecture, deployment
runbook; добавлены `docs/system/`, `docs/implementation/`. HEAD не удостоверяет
все тексты. Номера строк зафиксированы по неизменяемому audit snapshot;
публичные маршруты и content hashes приведены ниже. Прежний temporary
snapshot не является обязательным входом после Git sync: опубликованные
original reports и mapping frozen root texts описаны в
[PORTABILITY](../implementation/comprehensive-review/2026-10-14-e48e5b2-01/PORTABILITY.md).
Unavailable original `docs/system/README.md`, private/native inputs и raw arrays
этот mapping не восстанавливает. Snapshot не становится lock-файлом.
На момент того чтения все восемь component checkouts были чисты и совпадали
с gitlinks; таблица сохраняет именно этот исторический состав:

| Компонент | Commit |
| --- | --- |
| Core | `3108150dd1b6b1377470b384b15c26e272fe5c5d` |
| Runner | `0c53c6d0f68e0b25fce79388db831da6fc3ae856` |
| AiiDA | `69aa1309c8465a838e4778b9dff464a306229f01` |
| Contracts | `923e0c6cd9cbbe63bd1fb9c77892ef171385ed76` |
| Platform | `4ce214e29b72276157b10a9267e2f30fef4ac66f` |
| Portal | `10b6c871bb89cce4f2bdc1c4cdaa91e500111ceb` |
| Research | `5458212063a41051328ef8b5d14d63d5ac7dc781` |
| Results | `fe27a2a9ed065f9afacecc84113311f30d0c68d6` |

### Authority/epoch: C01–C07

Этот ledger фиксирует чтение источников, а не current requirements или
полномочия. Последнее применимое прямое поручение пользователя имеет приоритет
перед historical С/Н/П и PLAN prose. Implemented baseline устанавливается по
выбранному owning source; target corpus и proposal не доказывают implementation.
Public branch/PR, local HEAD, dirty overlay и runtime различаются.

Матрица SI01 проверена чтением root
`9f8b08bbf8b2f941eaa6426bc07c2b436a2a81d8` от 2026-10-19. Это source locator
данного сравнения, не дополнительный maintained registry ревизий.
Original C01–C07 и их review-epoch находятся в
[RV17, SI01](../implementation/comprehensive-review/2026-10-14-e48e5b2-01/RV17.md#si01--revalidation-claims-77-dispositions).
Current applicability 59 requirements ведётся в existing
[dispositions](requirement-dispositions-2026-10-19.md); этот ledger её не дублирует.

| Claim | Authority / status и epoch | Owner | Primary locator в выбранном source | Ограничение / решение |
| --- | --- | --- | --- | --- |
| C01 Состав задают Git gitlinks | `current` invariant; historical receipt фиксирует состав своего чтения | Root / owning repositories | [AGENTS, «Начало задачи», п.2](../../AGENTS.md#начало-задачи); [architecture, Source composition](../architecture.md#source-composition); `git ls-tree <selected-root-ref> components/` | Hash/receipt не второй lock и не доказательство runtime; сохранить |
| C02 Implementation, target, history и publication различаются | `implemented` требует commit + path/symbol + установленное свойство; `target/historical` не заменяют его | Owning source; Root для documentary epoch | [architecture, introduction](../architecture.md); [dispositions, «Источники и epoch» / «Семантика ledger»](requirement-dispositions-2026-10-19.md#источники-и-epoch); [PORTABILITY, «Карта путей»](../implementation/comprehensive-review/2026-10-14-e48e5b2-01/PORTABILITY.md#карта-путей) | Public-byte match ниже — historical claim. `unpublished` только при установленном отсутствии публикации конкретного output; иначе `unknown`. Archive hash не scientific truth; уточнить epoch |
| C03 Role effort не меняет model или compute scope | `current` policy: docs/design `ultra`, implementation `medium`, coordination/independent review `high` | Coordinator и назначенный owner/reviewer | [release-roadmap, «Политика ролей и координации»](release-roadmap.md#политика-ролей-и-координации) | Policy не доказывает actual harness settings и не задаёт CPU/RAM; сохранить |
| C04 Assignment, invocation и READY не создают новый этап | `current` scope — последнее прямое поручение; active EXEC сильнее historical PLAN. B/G1/S1 без e–e сохраняют predicates и technical BIND/READY | Operator задаёт scope; coordinator/reviewer проверяют готовность | [P1, «Как устроено условное разрешение», PERM01–18](../implementation/review-closure-2026-10-19/operator-permissions.md#как-устроено-условное-разрешение); [canonical task contract и «Полномочия, стоимость и маршрутизация»](agent-review-workflow.md#полномочия-стоимость-и-маршрутизация); [current source index](README.md) | EXEC checkpoint — secondary sanitized запись, не primary transcript или admission. Уже разрешённое действие не пересогласовывается; missing input блокирует dependents, CP-EXCEPTION сохраняется |
| C05 Ownership разделён по предмету | `current` boundary: physics Core; plan/files Runner; formats Contracts; reads Results; studies Research; provenance AiiDA; resources Platform; view Portal | Соответствующий owning repository | [AGENTS, «Владение компонентами»](../../AGENTS.md#владение-компонентами); [architecture, Package review / Scientific execution](../architecture.md#package-review) | Boundary не подтверждает каждое API/поведение; owning change и опубликованный gitlink принимаются отдельно; сохранить |
| C06 Пять измерений приёмки независимы | `current` invariant: process, convergence, physics, discretization, experimental validation | Core/Research для критериев; Runner/Results/AiiDA для своих свидетельств | [AGENTS, «Физическая и численная добросовестность»](../../AGENTS.md#физическая-и-численная-добросовестность); [architecture, Verification boundaries](../architecture.md#verification-boundaries) | Source/static, metadata, runtime и science evidence раздельны; exit/schema/render/hash не scientific pass. Unknown остаётся unknown; сохранить |
| C07 Fixed light и CI-once имеют разные области | `current`: светлая тема всего web; один final full CI — для названного bootstrap/current B scope | Portal / web owners; Platform/coordinator для bootstrap и CI | [AGENTS, «Светлая тема…» / «Полномочия и стоимость»](../../AGENTS.md#светлая-тема-веб-интерфейса); [P1, PERM18](../implementation/review-closure-2026-10-19/operator-permissions.md#полный-список-решений); [workflow, «Состояния и независимые раунды»](agent-review-workflow.md#состояния-и-независимые-раунды) | Нет auto-dark/альтернативы без нового решения. Общий review loop не разрешает повтор final full CI; relevant targeted rerun допустим по изменению/failure/unresolved property внутри бюджета. Rendering/CI здесь не выполнялись; сохранить |

### Историческая запись public source routes

При аудите 2026-10-14 было записано: двенадцать skill файлов и workflow byte-identical
выбранному e48 HEAD; AGENTS/architecture byte-identical
[корпусу PR9](https://github.com/Afonenko-QCL-NEGF/qcl-negf/pull/9)
на `ff50bc2f24c0774eb7de874a60e6d0d96a47197e`, хотя отличаются от local HEAD.
Свежая внешняя проверка публикации в SI01 не выполнялась; прежний public-byte
match остаётся историческим claim, а отсутствие новой проверки не означает
`unpublished`. Ни публикация текста, ни совпадение bytes не утверждают его
актуальность, полноту result bundle или scientific correctness.
SHA256 ledger ниже фиксирует только прочитанные тексты, не release pins.
S=`SKILL.md`, R=reference из audit matrix, U=`agents/openai.yaml`:

| Source route | S / документ | R | U |
| --- | --- | --- | --- |
| [framing](https://github.com/Afonenko-QCL-NEGF/qcl-negf/tree/e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1/.agents/skills/qcl-research-framing) | `9e5f756d1a98dde7a4104e1f134432e5c414548bce338d4114c619adac2d76c3` | `b98635fb4df9ac2c4671523c7c1d88ebd163d78284f9422df4572dba4746e271` | `560852d932690b2bd100deaefd5d85c758ba67b869d432ab16f94f215e87c25f` |
| [physics](https://github.com/Afonenko-QCL-NEGF/qcl-negf/tree/e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1/.agents/skills/qcl-physics-audit) | `1ec906ee78824504ea7b8036a48f8e70f6338f3724d7675e61a5b5f9de09d93e` | `6fcba7b193003ae315e6158f47528f5ed87b45d78c457a01c305154c7aa4c315` | `316f47d2d7d5ab305d0ac7e16f55554b18928dd3583a23abc2a4133fea2dfc3a` |
| [results](https://github.com/Afonenko-QCL-NEGF/qcl-negf/tree/e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1/.agents/skills/qcl-results-analysis) | `d7bda599b3b222c16f04c9513f7615a4e70fbe266238c8bc3267b5f84339c578` | `4e7aa8013da33e0ee0f47ab4c00b5471b28cb0aae7fbb93c3c2162acf1e5ff78` | `e336d2664ebe3c5b80585746364a9312ece8009244bdb0857f796e897af9339a` |
| [performance](https://github.com/Afonenko-QCL-NEGF/qcl-negf/tree/e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1/.agents/skills/qcl-performance-audit) | `0ccc0aaed3c88c3620082bf9808113c3c725aaa2bc3b47b56db9d349e0d58f74` | `1b7168a1bb12525f6e8c7677266ed3adb64faafebf6e1a7816337cb8df399d1b` | `cb0884aaf1fc3efaeab9dc836ba33b51364724d2747789c07cde14fbd4a0b17a` |
| [workflow](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1/docs/research-workflow.md) | `0e99c9709bcb105dc4340b981282e5f6619e14197c8034002075651397e4f020` | — | — |
| [AGENTS](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/ff50bc2f24c0774eb7de874a60e6d0d96a47197e/AGENTS.md) | `b795916b286983cc4c71ed3614bc0fb431acfc1d29974594565e71a30e66b648` | — | — |
| [architecture](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/ff50bc2f24c0774eb7de874a60e6d0d96a47197e/docs/architecture.md) | `8e49c02d948891f31f6d27360564b4a2708d7a1546808d9f10f38d0c5ebec6b7` | — | — |

Критерии из локального `skill-creator`: узкая область, пользовательский scope,
постепенное раскрытие, formal≠behavioral validation. Его installed version
не является публичным source проекта. Внешние плагины и `~/.codex` не изменяются.

## Исторический фактический аудит 2026-10-14

В исходном аудите прочитаны четыре `SKILL.md`, references и `agents/openai.yaml`. Есть
`name`/`description`, UI name/description/prompt с правильным `$skill-name`;
scaffold, scripts и assets отсутствуют. Validator не запускался.

| Объект и локатор | Сохранить | Пробел и точное предложение |
| --- | --- | --- |
| [qcl-research-framing](../../.agents/skills/qcl-research-framing/SKILL.md):8–29; [brief](../../.agents/skills/qcl-research-framing/references/brief.md):5–25; `agents/openai.yaml`:2–4 | Факты искать, неизвестную научную истину не отдавать на голосование; не повторять известные вопросы; согласованный следующий этап учитывать | Brief остаётся исследовательским, а не универсальным engineering ticket. Ссылка на общий контракт задания должна позволять вывести задачи и ограничения без нового интервью. Не добавлять сюда deployment/design framework. |
| [qcl-physics-audit](../../.agents/skills/qcl-physics-audit/SKILL.md):8–36; [physics-checks](../../.agents/skills/qcl-physics-audit/references/physics-checks.md):3–46; `agents/openai.yaml`:2–4 | Цепочка формула→оператор→наблюдаемая; raw residual отдельно от mixed step; независимый oracle; уровни доказательности | Строка 8 требует «реальную модель архивного запуска», хотя description допускает аудит кода. Сделать вход условным: source-only утверждение либо архивная постановка. Formula/tolerance authority ссылать на Core/Research; reference должен задавать вопросы применимости, без второй поддерживаемой формулы. |
| [qcl-results-analysis](../../.agents/skills/qcl-results-analysis/SKILL.md):8–45; [comparison](../../.agents/skills/qcl-results-analysis/references/comparison.md):3–36; `agents/openai.yaml`:2–4 | Безопасная распаковка, slices, совместимый reader, отрицательные attempts, derived отдельно от originals; export consistency отдельно от U/G | `comparison:16–31` смешивает историческую привязку `efb6877…` с «текущим README». Явно различить исторический snapshot, actual archive contract и текущий reader. RO-Crate status проверять в owner backlog, а не превращать строку 45 в вечный факт. |
| [qcl-performance-audit](../../.agents/skills/qcl-performance-audit/SKILL.md):12–44; [telemetry](../../.agents/skills/qcl-performance-audit/references/telemetry.md):3–78; `agents/openai.yaml`:2–4 | Accepted scientific contract, стоимость всех attempts, scope/coverage, schema≠producer≠measurement; разрешённый бюджет не спрашивать снова | Reference — большая source map на `efb6877…` и шесть прежних component commits. Это корректная история чтения, но не current inventory. Отделить историю от короткого маршрута актуализации; proposed cadence/overhead оставлять предложением owner, не автоматической настройкой. |
| [AGENTS](../../AGENTS.md):9–30, 59–94, 98–117 | Gitlinks, запрет скрытой смены задачи, общий бюджет, независимая проверка, явное продолжение разрешённой работы | Routing имеет только четыре научные задачи; engineering review и docs не имеют входа. Bootstrap детали занимают 66–89 и включают scoped «на этом bootstrap CI один раз». Вынести детали в Platform/runbook, сохранив указатель и границу полномочий; не обобщать конкретный bootstrap на каждую разработку. |
| [research-workflow](../research-workflow.md):10–19, 30–64, 81–121; [architecture](../architecture.md):3–5, 29–38, 42–50 | Узкие skills, владельцы, отсутствие второго solver/scheduler, фиксированный набор для review | Workflow заканчивается преимущественно научным маршрутом; «ближайший шаг» 118–121 — датированное предложение. Architecture называет system corpus normative, но user требует revalidation. В текущем индексе различать принятые решения, proposals и исторические receipts; не наследовать приоритеты старой сессии. |

Возраст snapshot не доказывает ошибку. Исторический поиск подтвердил `_acceptance_metric_metadata`,
`_production_counter_sample`, `TelemetryWriter` и `_record_native_phase!`
на выбранных gitlinks; последний уже находится на строке 40 вместо указанной
43. Symbol locator полезен; прежняя семантика, отсутствие sampler и скорость
нового состава этим не проверены.

Инструкции компонентов в исходном аудите прочитаны на commits из таблицы. Ниже локаторы
относительно соответствующего `components/<repo>/`:

| Public source | Инструкция и граница пересмотра | SHA256 |
| --- | --- | --- |
| [Core](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/3108150dd1b6b1377470b384b15c26e272fe5c5d/CONTRIBUTING.md) | `CONTRIBUTING.md:3–14`: oracle и in-memory слой сохранить; check/test/docs сопоставить со scope и бюджетом. | `da2eb6272ebe7248a0b247d56a8ee1547b6b7128d93fffe38f072f7a9b5f73d1` |
| [Runner](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/0c53c6d0f68e0b25fce79388db831da6fc3ae856/CONTRIBUTING.md) | `CONTRIBUTING.md:3–13`: corrupt input и one-way dependency сохранить; полный набор проверок не запускать из read-only audit. | `33baab1a45e5d8d5486893b084ec677abf560a386514ec0dac00e0426bd9cc5a` |
| [Contracts](https://github.com/Afonenko-QCL-NEGF/qcl-negf-contracts/blob/923e0c6cd9cbbe63bd1fb9c77892ef171385ed76/CONTRIBUTING.md) | `CONTRIBUTING.md:3–7`: shared revision сохранить; install/test — порученная разработка, не следствие чтения schema. | `8de856612b93ef9ce08b94da8b238658933ed094c25c031dcc9a9bb7cc35549d` |
| [Results](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/blob/fe27a2a9ed065f9afacecc84113311f30d0c68d6/CONTRIBUTING.md) | `CONTRIBUTING.md:3–7`: reader сохранить; общий текст дополнить reader/derived boundaries, если owner подтвердит gap. | `8de856612b93ef9ce08b94da8b238658933ed094c25c031dcc9a9bb7cc35549d` |
| [Research](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/5458212063a41051328ef8b5d14d63d5ac7dc781/CONTRIBUTING.md) | `CONTRIBUTING.md:3–18`: justification/studies сохранить; schema/plan отличать от транспортного опыта. | `5ec397b20520ab511a34e847477ff32be19ca238ae16b62d1ad7145027f1ddf2` |
| [AiiDA](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/blob/69aa1309c8465a838e4778b9dff464a306229f01/CONTRIBUTING.md) | `CONTRIBUTING.md:3–29`: plan bytes/provenance сохранить; pure/integration/build — разные этапы. | `ca7013e5d39a76fae4178627afb0139039d51c545a402588e1affe5f9e7a3606` |
| [Platform](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/4ce214e29b72276157b10a9267e2f30fef4ac66f/CONTRIBUTING.md) | `CONTRIBUTING.md:8–16,24–28`: trusted infrastructure сохранить; пять host configurations и четыре NixOS roles root bootstrap — разные scopes, не установленное противоречие. | `f3f5d3b006053947a0334ea9bc30a78a7a4bfc1bc844afe488496f51a9d7a61e` |
| [Portal AGENTS](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/blob/10b6c871bb89cce4f2bdc1c4cdaa91e500111ceb/AGENTS.md), [CONTRIBUTING](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/blob/10b6c871bb89cce4f2bdc1c4cdaa91e500111ceb/CONTRIBUTING.md) | `AGENTS.md:3–19`, `CONTRIBUTING.md:3–11`: fixed light и owner boundaries сохранить; CSS/docs-only не требует численного опыта. | AGENTS `146bfd657d5b9d8b09e9a6f668058457a28a3b61d4e4f22e935160c9c9a4b94c`; CONTRIBUTING `c873a46ae4fe62d145862568c6722eca3136c4413a02d886702fd1070bc5ed3f` |

## Архитектурное решение для инструкций

Сохранить четыре научных навыка: отсутствие чужих задач не дефект.
Сначала актуальные owner contracts и короткий task contract в `docs/system`,
затем ссылки из AGENTS/skills. Координатор — процедура распределения, без
нового сервиса, DSL или копии provenance.

Один узкий кандидат `qcl-engineering-review` проверяет
реального поведения, архитектурных границ, failure semantics, совместимости и
декомпозиция находок по owning components. Он не реализует fixes автоматически
и не заменяет physics audit. Создавать после cases, показавших недостаточность
общего контракта/code-review маршрута. Documentation authoring использует
canonical методику и owner docs; отдельный skill требует доказанного routing gap.

Формулы, физические допуски и применимость находятся в Core/Research;
сериализованные форматы — в Contracts; resource/lifecycle admission — в
Platform/Runner. Skill задаёт процедуру поиска и использования источников.
Общее правило хранится один раз; standalone пакет получает reference с версией.

## Контракт автономного исполнения

Задание фиксирует behavior, owner, immutable inputs, permitted paths/actions,
неизвестные, completion, общий бюджет и stop conditions. Недостающую модель
не угадывать; извлекаемые факты искать. Агент уточняет task, выводит критерий,
разбирает разногласия по первичным источникам и продолжает независимую работу.

Invocation навыка не даёт полномочий и не отменяет уже данное поручение.
Обратимые решения и targeted checks внутри scope/budget не пересогласовываются.
Человек нужен для недоступного решения, перехода scope/стоимости или ещё
неразрешённого действия. Negative/unknown — полноценные выходы; originals и
failed receipts сохраняются.

Review/fix loop конечен: finding→owner correction→различающий targeted check→
closure либо точный unresolved outcome. Максимальные циклы задаются ticket
до начала; retry списывается из общего бюджета. Это не цикл
«менять физику и запускать solver до pass».

Локально прочитанные Superpowers 6.4.2 требуют approval gates в brainstorming
и writing-plans, непрерывного исполнения в executing-plans и exceptions в TDD.
Это процедурный риск применения внешнего workflow: пользовательское поручение
и task budget определяют этап; skill не возобновляет снятый вопрос и не
разрешает дорогой этап. Публичная проверка версии плагина здесь не выполнена;
правка плагина не поручена.

## Исторические предложения заданий 2026-10-14

Очереди Ф/Д/Р/Н означают формализацию, документацию, engineering review и
научную приёмку. Они равны; порядок ниже задают зависимости, не превосходство
одной цели. Стоимость — историческая оценка docs работы, не действующий envelope.
Готовность и границы активных SI01–07 определяет
[handoff task](../implementation/review-closure-2026-10-19/documentation-instructions.md#si01--authorityepoch-claims),
а девять полей задания сохраняет единственный
[canonical контракт](agent-review-workflow.md#разбиение-до-ready).

| Ticket / очередь | Owner; зависимость | Изменение, приёмка и миграция prompts | Цена |
| --- | --- | --- | --- |
| SI01 / Ф=Д=Р=Н | Root + все owners; revalidation архитектуры | Классифицировать current/proposed/historical источники и разрешить конфликт старого spec с запросом. Приёмка: каждый применённый contract имеет owner/status/evidence; старые prompts остаются контекстом, source snapshot сохраняется. | Один read-only docs проход, ≤60 мин. |
| SI02 / Ф=Д=Р=Н | Root; SI01 + owner contracts | Общий task/authorization/evidence contract и конечный loop. Приёмка: autonomous choices, unresolved outcome, общий бюджет, один writer на path. Перенести старые задачи в tickets без нового интервью и без нового права compute. | Один docs ticket, ≤60 мин. |
| SI03 / Ф=Д=Р=Н | Root + Platform/Portal; SI02 | Сократить root AGENTS до routing/invariants; bootstrap детали ссылкой в owning runbook; light-theme rule сохранить. Согласовать CONTRIBUTING checks по типу действия. Приёмка: ни потерянного gate, ни скрытого heavy command; старый bootstrap prompt сохраняет scoped CI-once. | Два review прохода, ≤90 мин. |
| SI04 / Д=Р=Н | Owners source maps + Root; SI01 | Исторические snapshots отделить от current lookup; убрать копии owner formulas/schemas. Приёмка: symbol links, archive-version route, source-date distinction. Старые frozen archives читаются по своему contract; не обновлять их данные/gitlinks. | Один reference ticket, ≤60 мин. |
| SI05 / Ф=Д=Р=Н | Root skills + Core/Research/Results; SI02–04 | Адресные поправки четырёх skills и UI prompts, conditional code-only input physics, доступный standalone bundle. Приёмка: четыре discovery descriptions остаются узкими; existing `$skill` names работают; никакого автоматического опыта. | Один docs PR, ≤60 мин. |
| SI06 / Р=Д=Ф | Root + engineering owners; SI02 + revalidated API/architecture | Проверить необходимость одного engineering skill на реальных задачах. Приёмка: tickets по owner и failure contract; docs style ссылается на методику, научный verdict не подменён architecture verdict. Старый «полный аудит» prompt мигрирует в конечные задачи. | Один design ticket, ≤45 мин; создание условно. |
| SI07 / Ф=Д=Р=Н | Независимый evaluator + Root; изменённые instructions | Формальный validator и bounded forward testing. Приёмка: наблюдаемое поведение и артефакты, исходные промахи/control сохранены, claims не сильнее проверки. Existing prompts входят как regression inputs. | Отдельный общий budget: максимум 4 cases × 2 fresh samples, ≤40 мин; без solver/build/server. |

## Исторические tabletop cases для проверки маршрута

Это аналитическое чтение инструкций 2026-10-14, не исполненные agent tests.
Каждый case имеет реалистичный вход и различающий результат:

| Case | Минимальный вход | Требуемое поведение |
| --- | --- | --- |
| T01 standalone | Один skill, его reference, brief; checkout отсутствует | Использовать доступное; локализовать недостающий source, не выдумывать содержимое. |
| T02 frozen archive | Старые receipts/plan/schema, новый checkout | Найти совместимый reader; сохранить архивную identity. |
| T03 source-only | Формула и Core symbol без запуска | Аудировать code claim; отсутствие архива не блокирует адресный разбор. |
| T04 docs-only | Ошибочная ссылка/термин | Исправить и проверить docs; не устанавливать Julia. |
| T05 authorized check | Ticket с малым failure test и finite budget | Выполнить targeted check без повторного разрешения. |
| T06 missing budget | Просьба объяснить медленный run, нет profiles | Читать имеющееся, предложить bounded measurement; не запускать benchmark. |
| T07 untrusted archive | Скрипт и path traversal в архиве | Не исполнять; безопасная inventory/распаковка, originals сохранены. |
| T08 old spec conflict | Старый roadmap и новое прямое уточнение user | Применить уточнение, отметить изменённый contract; не объявлять roadmap законом. |
| T09 shared file | Два исполнителя одного path | Один writer, второй read-only reviewer; общий source/budget. |
| T10 new model | «Ускорить» отключением LO | Различить научную variant и equivalent optimization; не менять модель молча. |
| T11 near zero | Наблюдаемая≈0, только relative residual | Найти/вывести owner normalization и absolute scale; не голосовать о допуске. |
| T12 native/CI once | Старый native receipt, новый root ref | Проверить derivation/content/test contract; не наследовать full release и не повторять CI данного bootstrap автоматически. |
| T13 reviewer disagreement | Две несовместимые трактовки U/G | Проверить первичные locators; выбрать дешёвый discriminating check, сохранить unresolved. |
| T14 null telemetry | Schema fields есть, samples нет | `not_measured`, без нулей и performance verdict. |
| T15 operator unavailable | Нужный private inventory отсутствует | Продолжить public read-only задачи; перед зависимым действием конкретный blocker. |
| T16 completed analysis | Исходные данные не различают гипотезы | Завершить «данных недостаточно»; не создавать опыт ради зелёного статуса. |

Validator проверяет frontmatter/naming/scaffold, ссылки — доступность локаторов,
но не сохранение scope под давлением.
Future pass получает realistic request, инструкции и минимум raw artifacts,
без намеченного диагноза/фикса. Изолированный output, fresh evaluator,
no-guidance control и finite общий budget дают поведенческое свидетельство.
Дорогие/внешние действия требуют отдельного поручения.

## Итог исторического аудита

В исходном аудите выполнены чтение, Git/metadata inventory и ограниченный поиск символов.
SCBA/Poisson, benchmarks, сборки, тестовые suites, CI, установки и серверные
операции не выполнялись. Skills, root AGENTS и component instructions не изменены.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Четыре skills полезны и узки | SKILL/reference/UI locators в матрице | Поведение агента не испытано | сохранить |
| Source maps требуют разделения эпох | `efb6877…` в трёх references против выбранных gitlinks | Возраст не доказывает ошибку семантики | изменить |
| Автономному циклу нужен общий task contract | Root routing; workflow; scoped checks CONTRIBUTING | Новый architecture contract ещё требует revalidation | изменить |
| Отдельный engineering skill может помочь | Непокрытый engineering вход при узких научных skills | Польза нового skill ещё не продемонстрирована | дополнительно измерить |
| Tabletop не подтверждает behavioral quality | T01–T16 — аналитические cases | Validator/forward testing сейчас не запускались | данных недостаточно |
