# Точка входа в реализацию QCL-NEGF

Назначение: передать согласованный объём следующего релиза новой сессии
CODEX и начать адресную реализацию с этапа 1. Этот документ задаёт первый
проход и формат задания; порядок всего релиза остаётся в
[roadmap](release-roadmap.md), требования — в [requirements](requirements.md).
Предлагаемые интерфейсы и инструменты сохраняют свой статус предложения.
Создание этой точки входа само по себе не запускает реализацию, расчёты,
пересборку или операции на сервере.

**Доступность исходников:** корпус `docs/system/` включён в эту версию
исходников. Для работы из свежего clone выберите опубликованный docs ref,
содержащий весь корпус, и его gitlinks. В существующем checkout сохраняйте
локальные изменения; источником служит выбранный ref, а не отдельная
историческая заметка о подготовке передачи.

## Как читать перед конкретным заданием

Начать с запроса, [корневых инструкций](../../AGENTS.md) и
[реализованной baseline-архитектуры](../architecture.md). Затем сопоставить
нужные требования с [целевой архитектурой](architecture.md),
[первым научным рубежом](scientific-milestone.md) и
[roadmap](release-roadmap.md). Для выбранного изменения прочитать его
[review](review.md) и инструкции/публичные контракты owning component.
Весь корпус не является обязательным линейным чтением перед каждым ticket.

| Задача | Дополнительный материал |
| --- | --- |
| Identity, lifecycle, статусы, origins этапа 1 | Нужный CR01–CR07 в review, исходники и существующие targeted fixtures владельца |
| Подготовка S01 | Scientific milestone, Research/Core/Runner inputs и применимый физический навык |
| NFS, brief/full/slices, постобработка | [Results contract](results-and-postprocessing.md); явно различать read, derive и новый solve |
| Model help, учебник, Julia docs | [Physics documentation](physics-documentation.md); formula/value/effective origin принадлежат разным источникам |
| Bootstrap, диски, ресурсы, delivery | [Rebuild](rebuild.md), [deployment runbook](../single-server-deployment.md) и owning Platform instructions; только в порученном этапе |

Требования со статусами С/Н сохраняются. Статус П не превращается в принятый
API оттого, что исполнитель нашёл подходящую библиотеку. При расхождении
исторического плана с текущими требованиями использовать текущий корпус и
зафиксировать конкретный конфликт, а не переписывать всю архитектуру.

## Источники и первый read-only проход

В начале новой сессии снять фактическое состояние из корня checkout:

```sh
git rev-parse HEAD
git status --short
git submodule status --recursive
```

Gitlinks выбранного root commit определяют состав компонентов. Не создавать
второй ручной lock ревизий, не выполнять `reset` поверх чужих изменений и не
обновлять все submodules до `latest`. Для административного read-only Git
на сервере применять `GIT_OPTIONAL_LOCKS=0`; серверный доступ не нужен для
этого первого прохода.

Аудит [review](review.md) выполнен на
`bce0aee088313fd28b2440f55350980e21ed46bd` и его gitlinks. Это локатор
аудита, а не обязательная ревизия будущего начала или новый source lock.
Перед изменением проверить, что нужный path/symbol и failure scenario ещё
действуют. Сверить выбранный source с опубликованными root/component PR
heads и доступностью component commits; опубликованный PR, локальный HEAD
и uncommitted diff различать явно. При недоступной metadata сообщить, что
именно не сверено. Сохранить локальный corpus и unrelated changes; отсутствие
свежей публикации не разрешает объявить локальный документ частью fresh clone.

Первый координатор выполняет короткий проход:

1. Фиксирует source и границы разрешённого этапа, проверяет применимые
   локаторы и выбирает минимальный путь к S01.
2. Выделяет наименьший готовый критический ticket этапа 1 с воспроизводимым
   сценарием, владельцем и дешёвой локальной проверкой. CR02–CR05 приоритетны
   для будущих production-переходов; CR01 — для доверенного нового result API.
3. Передаёт готовый ticket исполнителю по
   [policy ролей и координации](release-roadmap.md#политика-ролей-и-координации).
   Исполнитель может менять код и выполнять порученные targeted fixtures
   без нового общего перепланирования или повторного разрешения обратимых
   действий внутри уже заданного scope.
4. Если не определён новый интерфейс или scientific contract, выделяет
   конкретный вопрос и brief его владельцу. Архитектурное решение требует
   соответствующего автора; это не повод останавливать независимые готовые
   tickets или создавать ещё один проект всего релиза.
5. После изменения сверяет diff и контракт, получает независимую проверку
   на том же source наборе и записывает фактические проверки/ограничения.

### Рекомендуемый первый ticket: CR05

Owner — Platform, исполнитель `medium` по canonical policy. Source —
фактический выбранный gitlink; [CR05](review.md#cr05--p2-identical-activation-не-восстанавливает-solver-profile)
и [application_release.py](../../components/qcl-negf-platform/ops/application_release.py).
При correct application profile + ready record missing/wrong solver profile
должен независимо восстановиться через identical retry, включая solver GC root.
Release/Code identity сохраняется; исправные profiles остаются идемпотентными.
Основа — injectable stdlib fake `Commands` в
[test_application_release.py](../../components/qcl-negf-platform/tests/test_application_release.py),
`ApplicationReleaseTests.test_activation_publishes_only_after_identity_and_health_check_then_retry_is_idempotent`.
В будущей code-сессии проверить existing case + новую регрессию командой
`python3 -m unittest discover -s tests -p test_application_release.py` из
`components/qcl-negf-platform`: максимум 4 вызова, каждый 1 CPU, 2 GiB RAM,
60 s wall, без real commands/services/SSH/solver/Nix builds. Здесь тест не
выполнялся. Если на новом HEAD дефект уже закрыт, выбрать другой готовый
критический ticket; не восстанавливать старый failure ради этого задания.

## Первый научный рубеж и зависимости

Первый обязательный S01 — самосогласованное тепловое равновесие
опубликованной GaAs/AlGaAs-структуры при **0 mV/period и 70 K**. Общий oracle
— Fermi–Dirac и равновесное FDR итогового Green state с одной μ и thermal
baths. Boltzmann допустим только при обоснованном невырожденном пределе.
Fermi seed, нулевой ток или успешный process exit сами не доказывают решение
SCBA/Poisson. Не менять модель, рассеяние, базис, сетку, окно или допуски
ради pass. Полные критерии, нормировки и ограничения задаёт
[scientific milestone](scientific-milestone.md), а не этот prompt.

Этап 1 закрывает CR01–CR07 адресными малыми fixtures. Это набор работ,
не общий gate «исправить всё до S01»: CR02–CR05 закрываются до production
resource/delivery переходов, CR01 — до доверенного нового result API.
CR06 legacy approximate continuation не является prerequisite независимой
S01; нужные для её used inputs origins проверяются адресно. CR08 и DOC02
относятся к отложенному оптическому пути и не задерживают S01.

Ранней S01 достаточно объяснимых used inputs, существующих Julia/Runner CLI
и независимых readers, а перед compute — конечного совокупного бюджета.
Новый domain resolver, общий серверный CPU grant, полный учебник, все GUI
вкладки и три installer backend не являются её prerequisites. Готовность
существующего локального runtime устанавливается отдельно; ранний
exploratory run не заменяет cold-start приёмку нового релиза. Новые расчёты
не разрешены поручением только на подготовку этой документации или fixes.

## Инварианты полного релиза, которые ticket должен сохранить

Подробный объём и приёмка находятся в [requirements](requirements.md).
Следующие группы помогают не потерять смысл при разбиении работы:

- **Julia и постановка (C01–C13):** независимый in-memory Core/API и локальный
  Runner; короткие шаблоны, версии protocol и явные variants; формы и полный
  YAML согласованы; видны resolved inputs и effective origins. Physics/model
  contract не переносится в UI или scheduler.
- **Карточка и результаты (R01–R04, R09):** цель, варианты, исполнения,
  attempts и анализ связаны; граф и запуск через формы; один сохранённый
  scientific payload на NFS; brief, full manifest и bounded slices сохраняют
  точный locator. Read не запускает solve/тяжёлый derive; SHA имеет назначенную
  границу. Новый global research cache и избыточный evidence ledger не нужны.
- **Агент и ВАХ (R05–R08, R12, S04–S06):** внешнему агенту доступны
  исследовательские запуски по общему admission/budget, процессы переживают
  отключение клиента, итог сохраняется файлом отчёта. Budget считает выделенные
  ядра × время allocation, failures включены, actual CPU показан отдельно.
  Independent sweep и continuation выбираются явно; ветка continuation
  остаётся внутри одного execution. Failed branch сохраняет доступные данные
  и отмечается ошибкой; прежние точки сохраняют собственные assessments.
- **Help и GUI (C11–C13, D09–D11, I08–I09):** человек и агент получают
  model/source help; целевой путь — локальная публикация Documenter
  HTML/search/math без запуска Julia при просмотре, детали D10 предложены.
  Все web surfaces фиксированно светлые.
  Portal, штатный Proxmox UI и Documenter составляют выбранное направление;
  Semaphore Community — кандидат. React Flow, Plotly.js и Monaco предложены,
  а не установлены. Performance aggregators — отдельная задача.
- **Границы науки и workers (S02–S03, S09, I07):** стационарный transport,
  populations/maps и уровни структуры остаются в scope; gain/absorption
  отложены, мощность, динамика и волновод исключены. Proxmox/libvirt/Hyper-V
  имеют отдельную приёмку; initial install может быть ручным, controller/NFS
  endpoints явны, enrollment доверенный, узел DRAIN до проверок.

## Серверные этапы остаются отдельными поручениями

При будущем bootstrap сначала выполнить дешёвый preflight четырёх NixOS
roles и строгую проверку nginx, executable paths, flake inputs, builder
identity/permissions и свежего admission по runbook. Heavy build, CI и
scientific run требуют своего конечного бюджета. Engineering build, trust/
delivery, guest services, restore, final CI и scientific acceptance — разные
gates; final CI выполняется один раз на final ready source ref кандидата.

Обычный builder/CI ↔ compute handoff ждёт освобождения задач и подтверждает
RAM после reserves гипервизора, storage/control и foreign VM. Swap не равен
physical Slurm RAM. Whole-cluster update следует I14: оператор вручную
отменяет верхние AiiDA workflows/retries и всю Slurm очередь/jobs, затем
подаёт сигнал доставки; delivery закрывает gate, проверяет отмену,
останавливает всех QCL workers, hard stop допустим при необходимости,
активирует один релиз и открывает admission после общего health check.
Rolling/multiversion queue migration не вводятся; неопубликованный state
после hard stop не обещан.

Wipe относится только ко всем QCL-owned ресурсам, включая inactive, без
переноса старого QCL state. Foreign VM остаются активными. До teardown
проверяются ownership/inventory, SSD и смысл тома «100 ГБ», protected reserves,
private inputs, доступность опубликованного source/gitlinks и seed первого
builder. Неизвестная принадлежность или seed — blocker до удаления.
Конкретные процедуры — в [rebuild](rebuild.md); это план, а не поручение
исполнять его из стартового prompt ниже.

Суточный ориентир касается минимальной инфраструктуры, не всего релиза или
времени сходимости. Общий research deadline отложен. Точные RAM/disks,
numerical tolerances и expensive-run budgets закрываются перед своим этапом;
они не являются общим барьером для дешёвого изменения кода.

## Формат задания исполнителю

Один ticket должен содержать:

| Поле | Содержание |
| --- | --- |
| Цель и связь | Requirement IDs, CR/GAP при наличии, проверяемое свойство и причина приоритета |
| Owner и source | Owning component, immutable root/component source, опубликованный PR/ref, применимые инструкции |
| Permitted paths | Файлы/каталоги и ветка; один пишущий владелец, зависимости на другие component tickets явны |
| Behavior/contract | Точный before/after, failure scenario, identity/status/units и compatibility/migration |
| Приёмка и стоимость | Targeted fixture/независимый oracle и предел локальной проверки; для дорогого этапа attempts, CPU/RAM/wall/output, stop rule и различающее свидетельство |
| Output contract | Reviewable diff, обновлённый контракт/пример, фактические checks, blockers/unknowns; таблица «утверждение / свидетельство / ограничение / решение» |
| Exclusions | Запрещённые переходы этапа, unrelated files, изменения физической модели/критериев и server actions |

Готовые независимые tickets разных owning components можно выполнять
одновременно по canonical policy roadmap. Component change публикуется
отдельным PR, затем обновляется его опубликованный root gitlink. Не собирать
весь релиз одним огромным PR. Новый runtime action не следует автоматически
из code diff. Пользователю задавать только действительно необходимый вопрос,
продолжая независимую разрешённую работу.

## Стартовый prompt для новой сессии CODEX

Скопировать после выбора checkout, содержащего этот корпус:

```text
Начни реализацию QCL-NEGF по docs/system/implementation-entrypoint.md с
этапа 1 docs/system/release-roadmap.md. Цель первого прохода — выбрать и
исправить наименьший готовый критический ticket с адресной дешёвой локальной
проверкой, сохранив минимальный путь к S01: опубликованная GaAs/AlGaAs,
0 mV/period, 70 K, FD/FDR итогового состояния; seed не является acceptance.

Прочитай AGENTS.md, implemented baseline docs/architecture.md, нужные
requirements/target architecture/scientific milestone/roadmap и только
применимые review/component instructions. Сними read-only HEAD/status/
submodule status, сохрани uncommitted work; сверяй локаторы аудита bce0aee…
с фактическим и опубликованным PR source. Gitlinks authoritative: не reset
чужие изменения, не update всех submodules latest, не создавать второй lock.
Если fresh clone не содержит docs/system, сначала установи опубликованный
docs ref; не считать локальный корпус уже опубликованным.

Применяй policy ролей/effort/координации из roadmap, сохрани выбранную model.
Разбей независимые owning tickets, выдай immutable source, permitted paths,
behavior/contract, acceptance, output contract и exclusions. Готовый code
ticket исполняй без нового общего перепланирования; новый неясный interface
или scientific вопрос выделяй отдельному соответствующему owner.

В этой сессии разрешены адресные изменения owning code/docs и bounded
targeted cheap local fixtures этапа 1. Не ждать весь CR01–07 перед S01:
CR02–05 закрыть до production transitions; CR01 до trusted нового result
API; legacy CR06 не блокирует independent S01; CR08/DOC02 deferred optics.
Не поднимать окружение, полные suites/builds, benchmarks, SCBA/Poisson,
CI/deploy, серверный bootstrap, inventory/диски/VM wipe или отмену jobs
без отдельного порученного этапа и конечного бюджета там, где он нужен.
Недоступный runtime обозначь в проверках, продолжай доступную работу.

Не менять физическую задачу, модель, рассеяние, сетку/базис/окно и критерии
ради pass. Сохрани различия execution/convergence/physics/discretization/
validation и missing/not_measured. Проверь diff/ссылки и адресное поведение,
проведи независимый review на том же source. Заверши reviewable результатом
и таблицей «утверждение / свидетельство / ограничение / решение». Component
PR и последующий root gitlink делай в порученном publication scope.
```
