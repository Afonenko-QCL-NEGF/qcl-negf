# Автономность, разрешения и checkpoints

**Статус: согласованные условные полномочия; текущий режим PLAN.** Разрешены чтение и редактирование
документов handoff. Разработка, tests продукта, установка среды, build,
сервер и научные запуски сейчас не выполняются. Отдельным последующим запросом
пользователь разрешил docs-only branch/commit/push/PR для handoff и public
review, без merge и без активации product execution. Будущее исполнение
активируется отдельным сообщением оператора. Основные ограничения —
[AGENTS](../../../AGENTS.md), effort — [canonical policy](../../system/release-roadmap.md#политика-ролей-и-координации).

Оператор утвердил [пакет P1: B/G1/S1](operator-permissions.md), S1 явно **без e–e**.
Статус **approved_standby**: активация EXEC остаётся отдельной командой.
Утверждённые late binding, G1 merge, B/S envelopes и measured-only RTO из P1
имеют приоритет над исходными conservative proposals этого handoff. Условия
технической готовности, scoped targets, fresh admission и запрет public release
без отдельного решения сохраняются.

## 1. Принцип автономности

После активации координатор выдаёт готовые задачи, организует independent review,
исправления и переходы без вопросов «продолжать ли?». Grant действует на заданные
классы действий, source и ресурсы; его не повторяют после каждого commit/test
или compaction. Missing input останавливает зависимую task; другие ready tasks
продолжаются. Unknown/непроведённое измерение не становится pass.

Оператор выбирает цель, существенные изменения модели и эксплуатационное
воздействие. Факты агент ищет, критерии выводит из модели/источников, интерфейсы
внутри scope проектирует сам. Научную истинность не предлагают выбрать голосованием.
Текст плана не выдаёт grants и не отменяет ограничения инструментов/sandbox.

## 2. Sol и effort

Сохраняется выбранная оператором **Sol**. При CP-START фиксируются actual model ID
и уровни выбранного клиента. Версия модели не подменяется автоматически Astra,
Luna или другим Sol. Если ID не наблюдаем, это activation input; глобальный config
не доказывает override текущей сессии. Настройки `~/.codex` сегодня не меняются.

| Роль | Effort | Результат | Граница |
| --- | --- | --- | --- |
| Координатор | `high` | Очередь, source/grants, зависимости и receipts | Не закрывает review собственного diff |
| Автор дизайна/документации/научной постановки | `ultra` | Один вопрос, alternatives, контракт и acceptance | Отдельный design deliverable до implementation |
| Исполнитель готового контракта | `medium` | Минимальный owning diff, checks и compatibility | Новый нерешённый interface возвращается в design |
| Независимый reviewer | `high` | Primary evidence, requirements, controls и limitations | Согласие не является физическим доказательством |
| Научный/resource audit | `high` | Анализ измерений и применимости | Новый criterion/model — design `ultra` |

Глубокий выбор локализуется в design `ultra`, после него реализация идёт `medium`.
`low` не назначается scientific review, lifecycle, admission или security review.
Effort не задаёт CPU/RAM/timeout/полномочия. Каждый spawn явно задаёт effort и
сохраняет модель. Brief изолирован: цель, immutable inputs, paths, checks, limits.

В текущем collaboration API explicit effort/model override требует
`fork_turns="none"`: координатор передаёт тот же actual Sol ID, нужный effort и
самодостаточный brief. Full-history fork override не принимает. При другом
клиенте использовать его подтверждённую схему; не менять глобальный config и
не считать автоматическое наследование доказательством применённого override.

Если native `ultra` недоступен, нельзя молча считать `max`/`xhigh` эквивалентом.
Используется ранее одобренное соответствие либо запрашивается ровно это решение;
доступные независимые tasks продолжаются. [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
и [config reference](https://learn.chatgpt.com/docs/config-file/config-reference)
подтверждают зависимость effort от модели/клиента и наследование permissions.
Официальные источники проверены 2026-10-19; project role policy задаёт распределение.

## 3. Согласованные grants, ожидающие активации

Все строки, кроме PLAN, **не активированы**. B/G1/S1 уже согласованы в P1;
оператор активирует нужный stage отдельной командой EXEC, без повторного
согласования принятых прав. Уже разрешённые обратимые действия внутри
scope не требуют новых согласований. Managed policy и tool approval обязательны.

| Grant | Разрешено после активации | Не входит | Inputs |
| --- | --- | --- | --- |
| PLAN | Источники/литература, handoff, формат/ссылки плана | Product edits/tests, installs, Git mutation, server/solve | Текущий режим |
| DOC_PR, одно поручение | Публикация полного handoff/public review отдельным root branch/commit/push/PR | Merge, product edits, server/build/science, public release | Прямой запрос пользователя опубликовать план; EXEC не активируется |
| DEV | Изолированные owning branches, code/docs, local commits, locked test env, адресные checks | Push/merge/publish, live services, global installs/config | Source, paths, accepted contract, resource envelope |
| PUBLISH | Own feature push, draft component/root PR и их обновление | Shared main push, merge, public release, deploy, сторонние сообщения | Repos/refs, reviewed diff и checks |
| MERGE_G1 | Условный merge component/root PR по утверждённому G1 | Force, обход protections, public release | Exact reviewed head, independent CP-CODE, required checks/protections и final-source identity |
| READ_NATIVE | Bounded read-only probes объявленных hosts/queues/storage | Install/restart/cancel, VM changes, новые trust roots | Trusted endpoint/identity/user, protected inputs, deadline |
| BUILD | Bounded preflight, immutable artifacts на назначенном builder, candidate staging в named private/lab destination; перечисленные rehearsal guests | Production mutation, public release, чужие disks/jobs, открытие admission | Fresh admission, paths/quota/destination, разрешённые namespaces/privileges, guest/disk/network IDs и cleanup scope; successful preflight до heavy build |
| OPS | Названный maintenance/deploy/restore на QCL ресурсах | Foreign state, необъявленные targets, общая очистка | CP-OPS: exact release/source/artifacts, target set, backup/window/rollback |
| SCI | Declared reads/analysis; submit/status/cancel своих attempts по каталогу | Новая physics, ослабление критериев, неразрешённые waves, чужие jobs | CP-SCI: model/plan/criteria/catalog, caps, admission, outputs/stops |

Удаление данных/форматирование вне B disposable targets, force/shared-history
rewrite, merge вне G1, новое trust/credential scope и смена научной задачи
рассматриваются отдельно в CP-EXCEPTION.
Общий scope «всё» не определяет destructive target. Будущий EXEC+DEV/PUBLISH
может разрешить все готовые owning tasks без per-ticket вопросов; сегодня EXEC нет.

## 4. Checkpoints

Технические checkpoints закрываются по evidence и independent review.
Человеческие разрешают конкретное воздействие или существенный выбор.

| Checkpoint | Кто | Вход | После pass |
| --- | --- | --- | --- |
| CP-START | Оператор | Handoff, EXEC, grants, Sol/capability, source/targets/protected inputs | Работать по всему принятому scope |
| CP-SOURCE | Координатор `high` | HEAD/status/gitlinks, dirty preservation, plan и artifact compatibility | Owning briefs |
| CP-DESIGN | Автор `ultra` + reviewer `high` | Interface, alternatives, invariants, failure/unknown semantics, acceptance | Implementation `medium` |
| CP-CODE | Reviewer `high` | Immutable diff, applicable red/green/controls, checks/limits | Commit/publish при active grants |
| CP-NATIVE | Координатор + reviewer | Active READ_NATIVE/BUILD, reviewed source candidate/refs/locks, fresh host/storage admission, результаты four-role/nginx preflight, trusted builder/targets | Тяжёлый immutable build или разрешённый isolated rehearsal |
| CP-OPS | Human policy — approved B; coordinator + reviewer закрывают BIND | Конкретное воздействие в пределах B, candidate/hash/targets/disks, preflight, backup/rollback/window; restore proof до production replacement | После EXEC один lifecycle owner исполняет named phase; новый human approval только вне B predicates |
| CP-RELEASE | Координатор + reviewer | Final published commits/gitlinks/locks, build/import binding, required native/restore/backend receipts и единственная final CI | Итоговый release dossier для OPS17/INT03; не разрешение BUILD/deploy |
| CP-SCI | Human policy — approved S1 без e–e; scientific author + reviewer закрывают READY | Frozen model/question/variants/criteria basis, S1 caps/guards/admission и finite attempts/stops | После EXEC автономные conditional waves без нового human approval каждой точки/criteria hash |
| CP-SCI-RESULT | Scientific reviewer `high` | Raw/fresh-map/FDR/gates/sensitivity/uncertainty | Verdict и разрешённая next wave |
| CP-EXCEPTION | Оператор | Concrete действие вне grant, последствия, evidence, альтернатива | Только названное расширение |
| CP-END | Координатор + reviewer | Coverage, deliverables, required receipts, открытые ограничения | Честный итог по каждому результату |

CP-DESIGN не требует оператора для обратимого внутреннего решения с сохранением
физики, внешнего контракта и доверия. Breaking API, новая trust boundary, отказ
от обязательного backend/критерия и новая модель идут в CP-EXCEPTION.

Подготовка не требует результата самой себя: scoped READ_NATIVE разрешает OPS01
collection; BUILD явно задаёт preflight namespaces и isolated rehearsal targets.
Их результаты закрывают CP-NATIVE перед heavy stage. First-use trust оформляется
CP-EXCEPTION до соединения с новым endpoint, без отключения проверки identity.
Coordinated backup, требующий паузы production writers, имеет собственный CP-OPS
на capture/pause/resume; первый isolated restore использует verified archive и
назначенный target, а не ещё не существующий результат этого restore. Проверенный
restore обязателен перед production replacement. Один operator packet может
сразу разрешить связанные conditional phases при неизменных bindings.

CP-SOURCE перепроверяется для публикуемого candidate перед CP-NATIVE, без
ожидания final CI. Owning commit/PR проходит CP-CODE+PUBLISH и не ждёт общего
CP-RELEASE. Final CP-RELEASE закрывается после native checks и OPS16; прежний
release pass не переносится на новую root identity.

## 5. Решения оператора

| Событие | Нужное решение | Независимая работа |
| --- | --- | --- |
| Сервер недоступен | Объявить восстановленный trusted access | DEV/design/docs; без повторяющихся probes по старым данным |
| Нет private input | Указать защищённый источник; секреты не публиковать в чате | Public contracts/fixtures |
| Готов production candidate | Внутри B: технический BIND release/targets/window/rollback; за пределами B — конкретное operator решение | Остальные source tasks |
| Нужен install target | VM/disk identity и допустимость записи | Recipes, checksums и инструкция |
| Есть jobs/foreign allocations | Внутри B: агент выбирает безопасное окно и отдельно отменяет только campaign-owned jobs; старый S01/чужие jobs требуют решения | Read-only accounting; foreign state не трогать |
| Не хватает ресурсов | Иной разрешённый host/storage или operational grant | Re-admission/ожидание; physics не упрощать |
| Нужна другая модель/bias/T/scattering/boundary | Принять новый объявленный scientific variant | Сохранить и анализировать исходные результаты |
| Требуется ослабление критерия | Новая постановка только с научным обоснованием; старый verdict сохранить | Error budget и причины отказа исследовать самостоятельно |
| Нет hardware required backend | Дать доступ либо явно изменить release scope | Остальные backend и science; полный выпуск остаётся partial |
| Нужны merge/release/destruction/новое доверие | G1 merge — technical gate; public release, destruction/trust вне B — named operator decision | Доступные checks и draft preparation |

Молчание и истечение времени не являются согласием. Решение имеет binding
к scope/predicates и допустимому воздействию. Новый candidate внутри approved
eligible source set получает свежий technical BIND; выход за scope/targets
не наследует старое согласование. После ответа fresh admission
снимается снова: согласование не сохраняет RAM и не продлевает receipt.

Один запрос оператору содержит: решение и его невыводимость; конкретный
candidate с refs/hashes/targets; evidence; рекомендуемое действие и альтернативу;
backup/rollback и риск; активируемый grant; независимую работу на время ожидания.
Связанные решения объединяются. Не спрашивать снова одобренный effort, каждый
тест/commit, реализацию internal helper и продолжение между ready tasks.

## 6. Единый контракт задания

| Поле | Обязательное содержание |
| --- | --- |
| Task / purpose | ID, coverage RV/SI/requirements, один проверяемый результат |
| Owner / role | Repository, writer, Sol effort, отдельный reviewer |
| Inputs / authority | Source/gitlinks или artifact identity, primary locators, private input paths |
| Paths / interface | Permitted writes, consumed/produced interface, compatibility/exclusions |
| Dependencies / grant | Required outputs, active permission class, checkpoints |
| Steps | Конечный checklist; proposed имена отличимы от existing; source recheck до edits |
| Acceptance | Denominator, positive/negative/near-zero cases, независимость oracle, units/weights/tolerance basis |
| Envelope / stop | Attempts/rounds, CPU/RAM/storage/wall/output, shared accounting, unknown behavior |
| Output / resume | Diff/commit, receipts/failed logs, claims/evidence/limits/decision и next state |

Неизвестный design — самостоятельный deliverable с вопросом, alternatives,
interface/invariants/acceptance. Implementation зависит от CP-DESIGN; это не
неопределённая задача «как-нибудь реализовать». Missing data не заменяются
заглушками. Docs-only corrections проверяются по смыслу/формату/ссылкам без
бессмысленных implementation-mirroring тестов и без подъёма численной среды.

## 7. Координатор, очередь и параллельность

1. Прочитать последнее сообщение оператора, handoff и checkpoint. Проверить
   режим: PLAN не переходит в DEV из-за текста будущего checklist.
2. Получить состав из Git. Различить review/current/imported/runtime identities;
   submodules не обновлять до latest, ручной lock SHA не создавать.
3. Проверить active grants/inputs и выбрать готовый пакет с наибольшим влиянием
   на приёмку. Не делать полный replan перед каждым заданием.
4. Выдать одному writer owned paths; второй агент независимо читает/reviews.
5. После design закрыть CP-DESIGN и назначить `medium`; после implementation
   провести independent CP-CODE. Автор не закрывает собственное review.
6. Сохранить результат и выбрать следующую ready task. Сообщать существенный
   прогресс; unchanged polls не превращать в пользовательский шум.

Concurrency ограничена slots, disjoint ownership и fresh RAM/I/O, а не числом
карточек. Для текущих четырёх slots ориентир: координатор + два writer + reviewer.
При активации capability проверяется заново. Tests/builds используют общий
admission/semaphore; число агентов не умножает память или scientific budget.
В Platform один writer владеет lifecycle entrypoint. DEV экспорт не меняет
одновременно actor lifecycle в том же файле; integration сериализуется.

После DEV независимы docs/contracts, export design, actor design, Platform owner
design, scientific criteria и installer design. Долгий server blocker не держит
эту очередь. Implementation ждёт только свой CP-DESIGN и required interfaces.

## 8. Ошибки и корректирующие циклы

Предлагаются два corrective rounds после первого review candidate. При новом
архитектурном вопросе координатор один раз назначает focused `ultra` design,
затем до двух новых rounds в принятом scope: всего до пяти author/review cycles.
Это условие replan, а не право принять load-bearing дефект. Нет progress/new
evidence — нет identical retry. Cap общий для задачи и всех её исполнителей.

Повторная причина получает fingerprint, original logs/input/source, контрпример
и самый дешёвый различающий check. Если все пути affected task выходят за grants,
формируется один CP-EXCEPTION. Task остаётся blocked; другие ready tasks идут дальше.

Environment error не выдаётся за семантический red test. Pre-existing failure
сообщается отдельно; deselect требует объяснения. Positive control обязателен
для негативного свойства. Повтор успешного suite нужен при новом diff/failure
или ином unresolved свойстве, а не по привычке после каждой Markdown правки.

Tool timeout/потеря SSH/закрытие чата не доказывают остановку remote action.
Перед повтором выполняется reconciliation по persisted operation/run/attempt IDs.
Unknown submit не порождает duplicate submit. Durable intent/failed receipt
не удаляют ради guard pass; destructive recovery требует своего решения.

## 9. Ресурсы и длительные операции

Финансовый предел пользователем не установлен. Реальный allocation ограничен
fresh CPU/RAM/storage и protected reserves гипервизора/foreign VM. Unlimited cost
не означает infinite retries. Task timeboxes — контрольные точки replan.

- DEV использует заданные в карточке bounds и измеренный host; при недостатке
  памяти tests не запускаются вслепую. Full numeric build не нужен docs-only.
- BUILD использует production-build по fresh inventory. `local-debug` не
  переносится на production. Nix/Julia/slice согласованы; native test contract
  и declared skips не ослабляются, CPU topology не подменяется фиктивной.
- SCI имеет заранее объявленные waves/recovery slots. Allocation CPU-hours
  и actual CPU/RSS/I/O разделены; неудачи и простои allocation учтены.
- Retained storage, cumulative writes, logs/output ограничены отдельно.
  Неожиданный расход ведёт к stop/re-admission, а не потере raw или урезанию physics.

Долгие jobs исполняются существующими AiiDA/Slurm или owned runtime units,
переживая завершение tool call/клиента. Checkpoint хранит IDs и safe status path.
Новый orchestration service/global cache/scheduler для handoff не создаётся.
Автоматизации будущих пробуждений и настройки аккаунта не меняются этим планом.

## 10. Checkpoint и resume

Один coordination checkpoint хранит ссылки на owning receipts; он не заменяет
AiiDA provenance, Results manifest или gitlinks. Private runtime evidence вне
Git, публичный progress только sanitized. Минимальное содержание:

- campaign/task IDs, mode, active grants, operator decision locator/expiry;
- source receipt, branch/worktree/owned paths, candidate diff/commit;
- actual model ID и effort каждого writer/reviewer;
- task states: planned/ready/running/awaiting_review/needs_input/needs_operator/failed/done;
- команды/timestamps/outcomes/receipt hashes, использованный envelope;
- active operation/workflow/CalcJob/Slurm IDs и unknown outcomes;
- unresolved findings, next discriminating check и ближайшая ready task.

Запись атомарно обновляется после launch/result/review/operator decision и перед
compaction/handoff. Raw data и секреты в checkpoint Git не попадают.
Resume: последнее указание оператора → mode/grants → source/dirty → active
operations reconciliation → receipts → readiness. Изменившийся input локально
инвалидирует dependent checks. Completed task не назначается заново без причины.

Для fresh clone синхронизировать опубликованную head branch docs PR
`codex/review-closure-handoff` либо принятый после merge source с этим handoff;
submodules обновить строго по gitlinks. [Startup prompt](start-new-session.md)
подтверждает P1 и активирует EXEC только при отправке человеком в новой сессии.
Primary public review и portable path map включены в Git. Старый чат,
`/tmp` patches и local bundle не являются скрытыми обязательными зависимостями.

## 11. Завершение

Done требует task acceptance receipt, independent review и нужных grants.
Coverage matrix перечисляет RV00–19/SI01–07: task, решение, evidence level и остаток.
Preserve закрывается обоснованием с locator; взаимоисключающие alternatives
не внедряются одновременно. Software/cluster/installer/science принимаются раздельно.
Отрицательный результат может завершить порученную научную попытку, но не
называется physical acceptance. Missing required backend оставляет выпуск partial.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Высокая автономность предусмотрена | Ready-task loop, scoped grants, technical checkpoints, resume | Исполнение начинается после CP-START | сохранить |
| Политика B/G1/S1 принята, exceptions остаются оператору | P1 decision table и technical BIND/READY | approved_standby, не EXEC; public release отдельно | сохранить |
| Effort заменяет проверку/полномочия | Раздельные роли, grants, receipts | Высокий effort не гарантирует правильность | изменить |
