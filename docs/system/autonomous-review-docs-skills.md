# Автономный review документации и инструкций: RV16–RV19

Статус: исполнимый план review, 2026-10-14; не отчёт о выполнении. Цель —
получить самостоятельные проверяемые решения по документации и агентному
интерфейсу. [Общий план](autonomous-review-plan.md) определяет campaign,
состояния, READY-контракт и общий бюджет. Здесь четыре равные цели:
формализация, документация, код и наука; три равные роли: исследователь,
оператор, разработчик. RV17 проходит через все цели, а не образует общую
очередь, ожидающую завершения physics audit.

Исходный snapshot авторства: root code
`e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1` с его восемью gitlinks;
root docs ref `193f5bf8700b82e05f7e0f1fdd9c8f3ea0908f07`;
dirty overlay и content hashes — receipt
`/tmp/qcl-autonomous-plan-20261014/baseline/snapshot.json`. Это страховочная
копия чтения, не второй revision lock. Публичный docs ref и реальные Git
gitlinks остаются источниками состава. Старые roadmap, labels «С/Н/П», планы
и чаты — проверяемые claims, а не автоматически новое ТЗ.

**Архитектура исполнения.** Каждый пакет читает точный source, формулирует
свойство, ищет различающий negative case и отдаёт один отчёт с audit,
конкретным patch/design proposal и candidate будущего задания. READY требует
известных exact inputs, invariant, check, permissions и budget; иначе записать
`needs_data`/`needs_decision` и конечный discovery/design ticket.
`R = docs/implementation/comprehensive-review/<campaign>/`, где campaign
выводится из UTC date, короткого root HEAD и sequence по общему плану.
SI01–SI07 — отдельные пакеты внутри `R/RV17.md`, без дополнительного общего
контракта заданий. Writer один на путь; независимый reviewer получает вопрос
и первичные inputs до авторского диагноза. После заморозки candidate допускаются
не более двух исправительных раундов; недоказанное свойство заканчивается
точным unresolved outcome, сохраняя исходные находки.

**Граница и цена.** Здесь поручаются чтение, статическое сопоставление и
проектирование patches. Изменение AGENTS/skills/кода, установка генераторов,
docs build, imports/evaluation, tests, deploy, solver и benchmarks принадлежат
будущему явно порученному scope. Уже предоставленное разрешение учитывается;
повторный human approval каждого обратимого шага не вводится. Предлагаемый
лимит кампании — 6 h root wall для всех участников и review, до трёх workers;
атомарный source packet — до 20 min. Лимиты карточек ниже входят в этот envelope,
не суммируются как новые разрешения. В начале исполнения установить `S`:
фактический root HEAD + gitlinks + hashes разрешённого dirty overlay; e48 —
исходный срез, а не обязательный будущий старый checkout. Claims docs ref
`193f5bf…` перепроверяются на `S`; смена входа создаёт новый review round.
Лимит 20 min включает независимый review; extracts ≤96 KiB и отчёт ≤8 KiB
на packet. Один RV-отчёт может объединять несколько обозначенных packets.
При исчерпании остановить зависимую часть,
сохранить отчёт и продолжать готовые независимые части в оставшемся бюджете.

**Review focus.** Не смешивать historical и current source; generated signature
и смысл; schema default и effective origin; tabletop и наблюдаемое поведение;
HTML rendering, fixed light/offline и научную приёмку. [Метрики](review-metrics.md)
используются с явным применимым denominator и `not_measured`, без общей оценки
«зелёное». Формулы и acceptance остаются у Core/Research, форматы — Contracts,
resource admission — Platform/Runner, представление — Portal.

## RV16 · Сегментированная инвентаризация и три читательских маршрута

**Owner:** root и docs owners всех восьми компонентов. **Вход:**
`README.md`, `docs/architecture.md`, `docs/system/README.md`,
`docs/research-workflow.md`, `docs/single-server-deployment.md`; component
`README.md`/`CONTRIBUTING.md`; перечисленные ниже owning surfaces.

| Сегмент | Точные начальные пути; далее только достижимые public surfaces |
| --- | --- |
| Core | `components/QCLNEGF.jl/docs/src/`, `src/QCLNEGF.jl`, `docs/make.jl` |
| Runner | `components/QCLNEGFRunner.jl/docs/src/`, `src/infrastructure/config/`, `src/application/configuration_types.jl` |
| Contracts | `components/qcl-negf-contracts/src/qcl_negf_contracts/schemas/` |
| Results | `components/qcl-negf-results/README.md`, `docs/export-budget.md`, `src/qcl_negf_results/cli.py` |
| Research | `components/qcl-negf-research/docs/scientific-inputs.md`, `config/`, `literature/` |
| AiiDA | `components/qcl-negf-aiida/docs/service.md`, `docs/deployment.md`, `src/aiida_qcl_negf/` |
| Portal | `components/qcl-negf-portal/src/qcl_negf_api/api.py`, `settings.py`, `frontend/src/api.ts` |
| Platform | `components/qcl-negf-platform/docs/`, `modules/`, `tofu/`, `examples/` |

- [ ] Составить repository-wide manifest документов/API/CLI/config; для каждого
  сегмента отметить owner, purpose, audience, source/date/status и пропуск.
  Неизвестный публичный API не объявлять private. Inventory отделить от глубины
  semantic review: охват всех repositories не означает чтение каждой функции.
- [ ] Выбрать один связанный срез: Core `docs/src/physics/numerical-policy.md`,
  Runner `docs/src/api/public.md` и `docs/src/user/results.md`. Проверить одну
  самостоятельную главу, reference и goal runbook; записать точный выбранный
  subsection и его prerequisites. При недостатке материала предложить текст.
- [ ] По [методике](documentation-methodology.md) развить понятный пример:
  точное правило → предсказуемый результат → причина → изменение одного условия
  → граница переноса. Использовать метод Java PR13 на
  `a0d1bdb9d8343809560e3ce7f9a2141d4473ee3f`, сохраняя QCL conventions;
  пять проектов курса и Quarto/QRC не становятся форматом QCL.
- [ ] Провести три статических journeys: найти criterion/raw locator;
  prerequisites/recovery boundary; API/units/error/test/owner. Зафиксировать
  вопросы читателей и proposal исправления связности.

**Выход:** `R/RV16.md`: manifest, три образца с patch proposal, journey gaps,
owning candidates с readiness/disposition. **Приёмка:** M14/M15/M16/M17, отдельно inventory coverage
и semantic coverage; все три роли находят нужный факт либо точно локализованный
gap. **Negative case:** короткий config имеет schema default, но не назначивший
его effective override; назвать отсутствие вместо подстановки. **Зависимость:**
начинать сейчас; RV03 owner выбранного edge, RV07 API contract, RV08 config
origin нужны только соответствующим спорным строкам. **Cap:** три packets,
до 60 min; большие главы читаются по выбранным sections.

## RV19 · Source of truth и генерация рядом с реализацией

**Owner:** owning code/docs owners. **Вход:** semantic row RV16;
Core/Runner `docs/make.jl` и public API; Runner
`src/infrastructure/config/configuration_sources.jl`,
`configuration_contract.jl`; Contracts `schemas/run.schema.json`; Portal
`src/qcl_negf_api/api.py`, `frontend/src/api.ts`; Platform
`modules/application.nix`, `tofu/proxmox/variables.tf`, `outputs.tf`.

- [ ] Для одного API и одной config boundary выписать signature, units,
  defaults/constraints, effects/errors, effective assigning origin, override,
  canonical example и owner. Formula origin, value origin и assigning origin
  держать отдельными полями; отсутствие любого не заменять другим.
- [ ] Сравнить нынешний docstring/schema/manual маршрут с кандидатами:
  Documenter; Griffe со static AST и `allow_inspection=False`; Sphinx autodoc;
  OpenAPI; TypeDoc; Nix options docs; terraform-docs; Literate.jl. Матрица
  фиксирует retained meaning, imports/evaluation/side effects, locked-version
  prerequisites, cross-links, offline assets и стоимость migration.
- [ ] Начать со static extraction: прочитать exports/routes/options/descriptions
  и proposed mapping, не импортировать packages. Отдельно перечислить import
  side effects, Julia compilation/doctests, Nix evaluation, OpenAPI app creation
  и example execution, если выбранный generator их требует.
- [ ] Предложить точечные owning docstrings/schema descriptions и включение
  canonical Markdown/example без независимо редактируемых копий. Составить
  candidate prototype с условиями READY: выбранные generator/version, inputs,
  exact command, isolated side effects, полномочия и bounded envelope.
  Неизвестная совместимость остаётся вопросом; неизвестные prerequisites
  получают discovery/decision ticket.

**Выход:** `R/RV19.md`, source-to-view matrix, patches/design и prototype
candidate с readiness/disposition.
**Приёмка:** M06/M12/M14/M15/M16: у каждого показанного факта один owner и
воспроизводимый locator; generated и authored meaning различимы.
**Negative case:** autodoc import запускает initialization; такой путь
не считается безопасной static проверкой. **Зависимость:** выбранная строка
RV16, а не весь inventory или science verdict. **Cap:** два packets, 40 min;
никаких install/import/build в review.

## RV18 · ADR единого входа документации

**Owner:** root/docs/Portal/Platform. **Вход:** три selected materials RV16,
mapping RV19; `components/QCLNEGFRunner.jl/docs/build/index.html`,
`objects.inv`, `search_index.js`, `assets/`; Portal `api.py`,
Platform `modules/application.nix`; root `README.md`, `docs/system/README.md`.
Existing Runner HTML доступен локально, но его source/build receipt пока
не установлен; это материал чтения, не current-release evidence.

- [ ] Подготовить ADR: static hub MkDocs или Quarto + existing Documenter;
  Antora; Backstage; минимальные ссылки на owning artifacts. Сравнить единый
  поиск, multi-repo version binding, ownership, maintenance, local assets,
  private exclusions и migration стоимости; выбор обосновать выбранным срезом.
- [ ] Спроектировать один pilot главы/API/runbook и docs-entry integration:
  source/release locator, prefix до catch-all, стабильные anchors и migration
  старых links. Публичный bundle исключает inventories, credentials, private
  supplements и raw operational logs. Portal показывает owning смысл ссылками.
- [ ] Статически инвентаризировать существующий HTML и assets; описать отдельный
  future browser protocol: light при dark OS, прямой anchor, поиск/math/fonts
  без внешней сети, доступные focus/contrast/error states. Предложить pilot
  ticket; исполнять pilot лишь в scope, включающем build и browser checks.

**Выход:** `R/RV18.md`: ADR, layout/integration proposal, candidate pilot.
READY pilot требует выбранных generator/version, source/build identity,
точных checks, разрешённого build/browser этапа и принятого бюджета.
**Приёмка:** M06/M16/M17; source binding и три journeys представлены явно;
offline/light пока `not_measured`, если проверен лишь source. **Negative case:**
светлый Portal окружает docs с auto-dark или внешним math/font CDN;
это gap, не выполненный M17. **Зависимость:** concrete selected outputs RV16/19;
ADR alternatives можно читать раньше. **Cap:** два packets, 40 min.
Произвольный dashboard/site build в этой карточке отсутствует.

## RV17 · Семь самостоятельных instruction packets

**Owner:** root/skill owners с тремя ролями. **Вход:** actual `AGENTS.md`,
восемь `CONTRIBUTING.md`, Portal `AGENTS.md`,
[skills review](skills-and-instructions-review.md),
[готовый проект workflow](agent-review-workflow.md) и четыре каталога
`.agents/skills/qcl-{research-framing,physics-audit,results-analysis,performance-audit}/`:
`SKILL.md`, их named reference и `agents/openai.yaml`.

На docs ref `193f5bf…` SI01 имеет source ledger и частичную заготовку claims,
требующую revalidation; это не актуализированный requirements ledger.
SI02 имеет повторно используемый проект READY/authorization/finite-loop
контракта, а не новый параллельный contract. SI03 имеет routing предложение,
SI04–SI05 — конкретные gaps/locators, SI06 — условный design нового skill,
SI07 — каталог T01–T16. Это частичная подготовка документации. Actual four
skills/references/UI не изменены; validator и fresh forward testing не выполнены.
Проверять фактическое действие инструкций, не считать старые labels исполнением.

- [ ] **SI01 — revalidation claims.** Из AGENTS, `docs/architecture.md`,
  `implementation-entrypoint.md`, `release-roadmap.md` и исходников восстановить
  owner/status/evidence каждого применяемого claim. Повторно использовать source ledger;
  old «С» против текущего user scope — negative case. M01/M06; результат:
  актуализированный claims ledger и correction candidate с readiness/disposition.
- [ ] **SI02 — canonical task contract.** Проверить поля и конечный loop в
  `agent-review-workflow.md` относительно master. Предложить минимальный patch
  туда; остальные документы ссылаются на него. Проверить immutable inputs,
  paths/actions, oracle, общий budget/stop, output, один writer и handoff.
  M01/M04; negative: blocker одной линии останавливает остальные либо повторный
  approval уже порученной проверки. Зависимость — применимые claims SI01.
- [ ] **SI03 — AGENTS routing.** Спроектировать patch root AGENTS и mapping
  component checks по action class. Bootstrap подробности направить в
  `docs/single-server-deployment.md` и Platform `docs/bootstrap.md`,
  `build-admission.md`; сохранить gates, scoped CI-once, fixed light и ownership.
  M12/M01; negative: docs-only приводит к полной Julia suite. Зависимость — SI02.
- [ ] **SI04 — references.** Проверить `brief.md`, `physics-checks.md`,
  `comparison.md`, `telemetry.md` в соответствующих `references/`.
  Разделить historical `efb6877…`, current symbol lookup и archive-version route;
  ссылать formula/schema authority владельца, сохранять оригинальные snapshots.
  M06/M18; negative: новый reader молча трактует старый archive. Вход — SI01.
- [ ] **SI05 — четыре SKILL и UI.** На четырёх exact paths предложить отдельные
  patches applicability/inputs, unit of work, evidence, actions, failure/unknown,
  handoff и cost/stop. Physics получает conditional source-only/archive input;
  framing сохраняет scientific brief; results — compatible reader; performance
  — неизменный scientific contract. UI сохраняет `$skill-name`, узкую discovery,
  implicit policy и existing fields; standalone bundle имеет versioned references.
  M01/M04/M19; negative: source-only code audit требует отсутствующий archive.
  Зависимость — применимые outputs SI02–04.
- [ ] **SI06 — условный engineering skill.** На реальном bounded API/failure
  вопросе сравнить общий contract/native review с кандидатом
  `.agents/skills/qcl-engineering-review/SKILL.md`. Привести воспроизводимый
  routing gap либо решение сохранить текущий маршрут; только при gap дать
  creation candidate с readiness. Docs authoring ссылается на методику. M12/M04;
  negative: architecture verdict объявлен scientific verdict. Вход — SI02
  и revalidated owning boundary; создание skill остаётся будущим изменением.
- [ ] **SI07 — раздельная проверка.** Подготовить formal validator protocol
  для frontmatter/naming/UI/links; отдельно статический tabletop T01–T16:
  standalone, frozen archive, source-only, docs-only, authorized check,
  missing budget, untrusted archive, old spec conflict, shared file,
  new model, near-zero, native/CI-once, disagreement, null telemetry,
  operator unavailable, insufficient data. Затем отдельный candidate forward ticket:
  realistic request + raw artifacts без подсказанного диагноза, isolated output,
  fresh evaluator и no-guidance control. Предложенный будущий общий envelope:
  максимум 4 cases × 2 fresh samples, включая control, 40 min root wall,
  до двух workers; локальные read tools ≤1 CPU/1 GiB каждый,
  суммарный output ≤128 KiB, без solver/build/server/install. Commands и
  выбранные cases фиксируются в ticket перед READY; превышение cap или
  неразрешённое действие завершает sample с original output.
  M01/M04; negative: validator pass или прочитанный tabletop объявляет
  autonomous behavior pass. Зависимость — frozen candidate instructions;
  каталог всех 16 cases не означает их execution.

**Выход:** только `R/RV17.md`, семь independently reviewable sections с
candidate patches, locators, unresolved и readiness/disposition будущих packets. **Приёмка:**
каждый из четырёх skills имеет собственную audit row; authority/routing
конфликты сохранены; formal, tabletop и forward evidence имеют разные статусы.
**Зависимость:** начать без завершения RV00–RV16; семантику конкретного API
или критерия сверять только с нужным owning output, не со всей physics очередью.
**Cap:** семь packets до 20 min каждый, внутри campaign envelope;
SI07 fresh execution использует свой будущий общий budget, не текущую квоту.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| RV16/19/18 имеют отдельные достаточные входы | Карточки и source surfaces выше | Report и pilot ещё не исполнены | сохранить |
| Заготовки SI01/02 следует использовать повторно | Docs ref `193f5bf…`, source ledger/draft workflow | Claims требуют revalidation; actual behavior не доказано | изменить |
| Instruction proposal отличается от доказательства автономности | SI07 разделяет formal/tabletop/forward | Новых agent samples здесь нет | дополнительно измерить |
| Rendered docs не подтверждают physics или release acceptance | M16/M17 отдельно от M18/M19 | Builds/tests/solver/server не выполнены | данных недостаточно |
