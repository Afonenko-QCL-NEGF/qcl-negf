# Программа комплексного ревью QCL-NEGF

Статус: проект программы, 2026-10-14. Предмет ревью — код, связи компонентов,
приложения и инфраструктура, научные методы, тесты и документация всей системы.
Программа предназначена для работы после минимального развёртывания и первого
исследования; подготовку источников и статический аудит можно вести уже сейчас.
Она не поручает новые расчёты, сборки или изменения сервера.

Минимальный кластер с одним compute был развёрнут, существующий S01 физически
запущен. Его результаты и сходимость ещё не приняты. Это исходное состояние
по [датированному аудиту источников](../implementation/comprehensive-review-source-audit-2026-10-14.md),
а не утверждение о live-статусе сегодня. Первый шаг — восстановить конечное
свидетельство этого запуска, когда оно доступно; запускать новый для закрытия
пробела не требуется.

Программа ведётся в этом файле. [Requirements](requirements.md) определяют
объём релиза, [roadmap](release-roadmap.md) — его этапы, а здесь задаются вопросы
ревью и условия доказательного ответа. Реальные API и процедуры остаются в
owning repositories. Датированные отчёты сохраняют историю, не переопределяя
актуальный контракт. Новое ревью не переписывает весь release plan.

## Три равноправных сценария

Исследователь должен сформулировать модель, понять её ограничения, запустить
порученный опыт и интерпретировать сохранённый результат. Оператор должен
установить, наблюдать, отменить, обновить и восстановить систему, сохранив
научные данные и чужие ресурсы. Разработчик должен понять границы компонентов,
изменить владельца поведения, проверить последствия и выпустить воспроизводимый
состав. Все три сценария имеют одинаковый вес. Хороший научный интерфейс
не компенсирует опасное восстановление, а успешный deploy не подтверждает физику.

Ниже сплошные связи показывают существующие границы исходников; пунктир —
предлагаемую публикацию общей документации. Участие роли в схеме обозначает
точку доступа, а не её права на все HTTP-операции.

~~~mermaid
flowchart LR
  R[Исследователь] --> P[Существующий Portal]
  O[Оператор] --> P
  D[Разработчик] --> P
  P --> A[AiiDA]
  A --> S[Slurm]
  S --> J[Runner]
  J --> C[Core]
  J --> F[Сохранённые артефакты]
  X[Results] <--> F
  P -. Предлагаемая ссылка .-> H[Общий docs hub<br/>статический artifact релиза]
  H -.-> N[Core и Runner<br/>Documenter]
  H -.-> M[Markdown владельцев<br/>API, методы, runbooks]
~~~

Схема не изображает всю delivery topology и не утверждает наличие общего
docs route. Results читает артефакты независимо от живого AiiDA; Portal не
становится владельцем физики или scheduler. Точные job/data/release lifecycle
и deployment views — выход отдельного ticket.

## Что оценивать в коде и архитектуре

Начать с фактических зависимостей: package imports, вызовы между модулями,
CLI/HTTP, schemas, файловые форматы, ресурсы и mutable state. Репозитории
и runtime-процессы различны. [C4](https://c4model.com/diagrams) помогает
показать контекст, containers и deployment; из [arc42](https://arc42.org/overview/)
нужны границы, runtime scenarios, решения и риски, без обязательного заполнения
всех разделов шаблона. Каждый рисунок показывает actual или proposed состояние
и ссылается на source composition.

Связность оценивать по совместно изменяющимся обязанностям, направлению
зависимостей, циклам и последствиям изменения контракта. Проверить, не
переопределяют ли consumers acceptance, retry, identity, schemas или staging
своими копиями. Отдельно разобрать владельцев данных, буферов, профиля AiiDA,
артефактов и lifecycle операции. Общая утилита полезна лишь при совпадении
семантики; совместный код reference/optimized может сохранить общую ошибку.

Сложность оценивать через число состояний и допустимых переходов, вложенность
управления, скрытые побочные эффекты, exception paths, зависимости от порядка
вызовов и объём рассуждения для локального изменения. Большой файл или высокий
LOC — повод выбрать участок, а не доказательство дефекта. Для каждого
предложения рефакторинга назвать сохраняемый invariant, границу мутации,
изменяемый owner и различающую проверку.

[Карта компонентов и метрик](review-metrics.md) связывает язык, цель, задачи
и публичные функции каждого repository с измеряемыми свойствами. Метрики
выбираются по вопросу ревью и границе свидетельства, без универсального
порога сложности или рейтинга компонентов по числу строк.

Устойчивость требует разбора timeout, bounded retry, idempotency, отмены
parent workflow и job, конкурентных запросов, частичной записи, ENOSPC,
потери worker/NFS и восстановления. Успешный путь дополняется failure path:
что сохранено, что неизвестно, кто продолжает операцию и когда admission
может открыться. Ошибка доставки не должна незаметно изменить физическую
модель или превратить missing data в physics failure.

Воспроизводимость приложений связывает Git composition, native locks,
runtime versions, фактическое содержимое artifact и используемый solver.
Для инфраструктуры нужны declarative roles, private configuration boundary,
drift, cold start, reinstall и coordinated restore базы с AiiDA repository.
Замена VM image не разрешает уничтожить data volume. Повторяемый build,
повторяемое выполнение и воспроизводимый научный вывод — разные свойства.

## Источники и независимость ревью

Перед каждым направлением зафиксировать immutable root ref, его gitlinks,
dirty overlay, выбранный runtime и primary artifacts. Checkout, опубликованный
PR, installed release, resolved plan и архив могут иметь разные identity.
Старый finding перепроверяется по symbol и фактическому поведению; согласие
агентов или зелёный CI прежнего ref не переносятся на новый состав.

Первый рецензент получает вопрос, предпосылки и первичные источники без готового
диагноза. Затем сопоставляются выводы и возражения. Ticket хранит самый дешёвый
различающий check. Противоречие не закрывается голосованием; отсутствие данных
остаётся явным. Один агент пишет выбранный файл/ветку; независимые owners
работают параллельно по [policy координации](release-roadmap.md#политика-ролей-и-координации).

## Покрытие свойств тестами

Процент покрытия строк показывает исполненные участки, но не качество oracle
и не проверенные свойства. Нужна карта property → producer/consumer →
test/fixture → assertion → предел mock. Мутация входа, восстановление
сохранённого состояния, отсутствие двойного submit и immutable attempt
selection требуют явных проверок. Mock transport не доказывает Slurm/NFS
поведение, а manufactured scientific fixture не доказывает приборную модель.

Матрица ниже задаёт два независимых измерения ревью; клетки обозначают вопросы
к свидетельствам, а не уже полученные pass.

| Уровень утверждения | Unit | Contract | Integration | Failure | Recovery | Human journey |
| --- | --- | --- | --- | --- | --- | --- |
| Процесс и приложение | Локальный результат и эффекты | Identity/status/errors | Границы реальных adapters | Timeout/retry/cancel/concurrency | Повтор без дубля | Submit/read/cancel/restore |
| Решение уравнений | Независимый операторный oracle | Raw residual/units/state | Один согласованный U/G | Stagnation/nonfinite/budget | Seed/restart eligibility | Верное прочтение остановки |
| Физические проверки | Выведенное тождество | Применимость/norm/weights | Сохранённые diagnostics | Отключённый/неизмеренный gate | Сохранение исходных verdict | Ограничения модели |
| Дискретизация | Аналитическая квадратура | Axes/cutoffs/basis | Контролируемое refinement | Потеря хвоста/coverage | Сопоставимость grid identity | Отличие точности от residual |
| Эксперимент | Units/digitization | Условия/uncertainty | Независимое сравнение | Model discrepancy | Provenance исходных данных | Обоснованный вывод |

Неприменимая клетка получает основание. Приоритет — независимый oracle и
существенные границы, а не тест, повторяющий реализацию. Изменение сетки,
рассеяния, базиса, допусков или optical scope требует отдельного научного
решения, даже если оно удешевляет тест.

## Последовательность и стоимость

P0 устанавливает источники и переносимость уже существующих проверок. Затем
статический аудит архитектуры, кодовых свойств и материалов идёт параллельно;
его выводы выбирают адресные изменения owners. Научные вопросы S01 используют
сохранённый результат и отдельную physics review цепочку. Общая документация
не становится prerequisite получения первого научного свидетельства.

Стоимость назначается каждому различающему check, а не всему проекту одним
словом «тесты». Для дорогого этапа заранее фиксируются attempts, суммарный
CPU/RAM, wall time, output limit, stop condition и ожидаемое свидетельство;
бюджет общий для всех агентов. Уже порученные действия не требуют повторного
согласования.

| Класс | Назначение и граница |
| --- | --- |
| Static | Чтение, graph/links/schema inspection, review исходников; без установки среды |
| Docs build | Import/precompile, doctests/examples, HTML/assets; отдельный конечный бюджет, без скрытого production solve |
| Unit/contract | Выбранные локальные свойства и synthetic fixtures; предел mocks записан |
| Integration | Реальные package/adapters/process границы; явно проверить, вызывает ли suite Julia producer |
| Production | Build/boot/delivery/cancel/staging/restore на целевой инфраструктуре; fresh admission и private inputs |
| Science | SCBA/Poisson/refinements/experimental comparison; frozen model/criteria и научный бюджет |

Полные suites не повторяются без новых изменений, failure или неразрешённого
свойства. Component PR публикуется первым, затем обновляется root gitlink.
CI запускается на final ready ref в порученном окне. Локальная проверка docs
не объявляется full release или scientific acceptance.

## Задания ревью

Каждая строка — вопрос и проверяемый выход, а не поручение автоматически
изменить код. Локаторы используют выбранные gitlinks; исторические материалы
из [source audit](../implementation/comprehensive-review-source-audit-2026-10-14.md)
нуждаются в собственном source binding.

### Источники и архитектура

| ID / приоритет | Owner и вопрос | Выход и критерий | Зависимость / дешёвое свидетельство |
| --- | --- | --- | --- |
| RV01 / P0 | Root/Research/Results: какой состав породил существующий S01? | Source/runtime/plan/attempt/artifact паспорт; terminal result либо точный gap, без нового submit | Bounded receipts/metadata read; checkout и installed source разделены |
| RV02 / P0 | Results: переносимы ли existing diagnostics tests? | Проверить [draft PR6](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/pull/6), без дубликата; личные абсолютные пути устранены, source identity проверяется переносимо | tests/test_equilibrium_diagnostics.py:37–38,112–113; сначала diff/source, затем отдельно bounded selected check |
| RV03 / P1 | Root/all owners: соответствует ли код границам системы? | C4 context/container, dependency graph, job/data/release lifecycle, deployment/storage views; actual/proposed различимы, каждый edge имеет owner/source | RV01; imports, calls, configs; схемы содержат сохраняемые данные и trust boundaries |
| RV04 / P1 | Core/Runner: правильно ли разделены вычисление и управление? | Карта cohesion/coupling, mutation ownership, cycles/change impact; physics остаётся Core, persistence/resources — Runner | src/QCLNEGF*.jl, composition/, application/, infrastructure/; invariant и targeted check для каждого change |
| RV05 / P1 | AiiDA/Portal: контролируема ли сложность execution/API state? | Таблица состояний/errors/concurrency и dependency direction; один владелец профиля/handles, bounded HTTP admission | service.py, workflow.py, api.py; static paths и выбранные concurrent/failure fixtures |
| RV06 / P1 | Platform: однозначен ли lifecycle owner? | Desired/observed state, durable intent, serial entry, recovery transitions; отказ не открывает admission | ops/application_release.py, worker_lifecycle.py, bootstrap_build.py; transition table до серверных опытов |

### Контракты и научные свойства

| ID / приоритет | Owner и вопрос | Выход и критерий | Зависимость / дешёвое свидетельство |
| --- | --- | --- | --- |
| RV07 / P1 | Contracts/consumers: едина ли semantics API/schema/status? | Producer/consumer/version/migration matrix; attempt selection, missing statuses, precision и limits согласованы | README/API/schema/source; проверить README export bytes ambiguity и vendored hash drift guard |
| RV08 / P1 | Core/Research: какие физические утверждения реализованы? | Формула→assumptions→discretization→symbol→observable→criterion; units/norm/weights/near-zero и конечный basis явны | theory/, physics/, traceability.md, S01 inputs; актуальный независимый physics audit |
| RV09 / P1 | Core/Runner/Results/Research: достаточно ли test properties? | Матрица выше с assertions/oracles/gaps; reference/optimized agreement не единственный oracle | Existing tests и analytic fixtures; независимые origins; numerical runs отдельны |
| RV10 / P1 | Research: формализованы ли методы и задачи? | Brief на вопрос: гипотезы, alternatives, observables, discriminating evidence, criteria/budget/stop; calibration/validation различаются | docs/equilibrium-s01.md, passports/config graph; negative result остаётся результатом |

### Устойчивость и воспроизводимость

| ID / приоритет | Owner и вопрос | Выход и критерий | Зависимость / дешёвое свидетельство |
| --- | --- | --- | --- |
| RV11 / P1 | Runner/Results: сохраняются ли данные при отказе? | Publication/checkpoint/staging/read границы и ENOSPC/partial write/NFS/worker loss сценарии; исходные массивы и provenance сохранены | Persistence/state/archive source, saved fixtures; durability отдельно от scientific verdict |
| RV12 / P1 | AiiDA/Runner/Platform: bounded ли выполнение и отмена? | Timeout/retry/idempotency/cancel parent+job/budget matrix; отказ после submit не вызывает скрытый дубль | workflow.py, staging, Slurm adapters; fixtures прежде production cancellation |
| RV13 / P1 | Platform/private site: восстановима ли инфраструктура? | Roles/config/drift/cold-start/reinstall/restore contract; DB+repository coordinated, VM/data ownership и foreign preservation явны | Public IaC/options/runbooks + sanitized inventory; реальный restore — отдельный конечный опыт |
| RV14 / P1 | Root/Platform: воспроизводимы ли build и release? | Native lock/source/artifact/runtime chain, offline requirements, reused-output contract; новый ref не наследует full acceptance | ops/, native locks, Nix/application/solver outputs и receipts; затем scoped build при необходимости |
| RV15 / P1 | Portal/AiiDA/Platform: корректны ли security boundaries? | Auth/read/submit/cancel/download credentials, private configs, executable inputs, trusted CI и logging review; rejected paths проверены | Existing API/auth/config source; synthetic inputs, без чтения токенов и private публикации |

### Документация и работа агентов

| ID / приоритет | Owner и вопрос | Выход и критерий | Зависимость / дешёвое свидетельство |
| --- | --- | --- | --- |
| RV16 / P1 | All docs owners: понятен ли код без автора? | Docs/API/config inventory и три journeys; пробная глава по [методике](documentation-methodology.md), reference и goal runbook; owner/source/status у active материалов | RV03/07/08; read-through, signatures/links; историю сохранить отдельно |
| RV17 / P1 | Root/skill owners: правильно ли маршрутизируется работа? | AGENTS router, applicability/check-cost matrix, навыки без копий physics rules; standalone и already-authorized случаи не расширяют scope | .agents/skills, AGENTS/CONTRIBUTING; tabletop cases без solver |
| RV18 / P2 | Root/Portal/Platform/docs owners: как опубликовать все материалы? | ADR генератора, static bundle, общий search/anchors/source bindings; offline/local assets/fixed light и private exclusions проверяемы | RV16/19; existing artifact inspection; pilot/docs build отдельным бюджетом |
| RV19 / P1 | All code/docs owners: какие факты держать непосредственно в коде? | Source-of-truth matrix из [методики](documentation-methodology.md#документация-рядом-с-кодом); generated signatures/fields/options и source-included examples, без independently edited copies | RV07/16; prototype одного owner с проверкой imports/evaluation/cost, без установки всего набора средств |

## Документация рядом с кодом

Одновременно рассмотреть docstrings, type hints, schema/option descriptions,
generated API/OpenAPI/options reference, doctests и canonical example sources.
Рассказ об архитектурном решении и вывод формулы остаются в owning chapters;
проверяемые signatures, defaults и errors располагаются ближе к реализации.
Поведенческий PR обновляет source documentation и targeted checks вместе.
Генерация фактов уменьшает ручное расхождение, но не доказывает их семантику.
RV19 выбирает механизм по языку и import/evaluation риску, а не устанавливает
все инструменты. Derived HTML и каталоги не редактируются независимо.

## Общая публикация документации

Предпочтительный путь — статический release artifact рядом с существующим
Portal, с общим входом и сохранением native Documenter. Owning Markdown
подключается при сборке, а не копируется для независимого редактирования.
Существующая practical HTML публикация — материал для RV18, не готовая
общая release интеграция.

| Маршрут | Преимущество | Цена и вопрос ревью |
| --- | --- | --- |
| Статический hub с MkDocs или Quarto + Documenter | [MkDocs](https://www.mkdocs.org/user-guide/configuration/) подходит Markdown/nav; [Quarto book](https://quarto.org/docs/books/) — связной книге, [crossrefs](https://quarto.org/docs/books/book-crossrefs.html) и [поиску](https://quarto.org/docs/websites/website-search.html) | Сравнить на главе, API и runbook; search по произвольному Documenter не появляется автоматически |
| Antora | Native multi-repo/version [content aggregation](https://docs.antora.org/antora/latest/how-antora-works/) | Native [AsciiDoc pages](https://docs.antora.org/antora/latest/pages-directory/) означают migration/adapters нынешних Markdown/Documenter |
| Backstage TechDocs | Общая developer platform с docs reader | [Backend и обработка MkDocs HTML](https://backstage.io/docs/features/techdocs/architecture/), включая удаление JS; импорт Documenter требует отдельного решения |

Сейчас выбирать runtime framework и переносить все тексты преждевременно.
RV18 сравнивает варианты по цене миграции, owner workflow, formula/API links,
поиску и версиям. Book-style из Java применяется независимо от генератора.
Документацию открывают без Julia/solver/build; весь HTML фиксированно светлый,
math/search/fonts доступны локально. URL будущего bundle указывает release
source ID из существующей composition, без второго ручного revision lock.

Public build получает allowlist sources и sanitized config examples.
Описание private конфигурации включает поля, единицы, зависимости и errors;
реальные адреса, identities, credentials и inventories остаются в private
operator supplement. Source arrays и raw operational logs не коммитятся.

## Завершение ревью

Ревью завершено, когда каждый существенный вопрос получил локализованный
вывод и решение, а каждое предложенное изменение — owner, invariant и
самую дешёвую приёмку. Findings оформляются отдельными component PR;
неизвестный научный результат не задерживает адресный обратимый docs fix.
Неразрешённые gaps получают конкретный следующий check, без догадок о сроках.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Существуют минимальный runtime и начатый S01 | Датированные receipts/source audit | Terminal/scientific verdict ещё не установлен | Дополнительно измерить |
| Есть native docs и owning boundaries | Selected code, Documenter, README/runbooks | Общая полнота и устойчивость не доказаны | Сохранить |
| Код и инфраструктура требуют property review | RV03–RV15 и матрица свидетельств | Статический finding не runtime verdict | Дополнительно измерить |
| Нужны связанные docs и правила их авторства | RV16–RV19, методика | Выбор генератора/реализация впереди | Изменить |
| Полная научная и release приёмка ещё открыта | Раздельные gates и источники | Нельзя вывести из build/docs/process pass | Данных недостаточно |
