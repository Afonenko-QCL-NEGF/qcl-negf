# Документация, требования и SI01–SI07: карточки handoff

**Только план.** Никакая карточка не активна без CP-START и её grant из
[autonomy](autonomy.md). Product source, AGENTS/skills и browser assets сегодня
не меняются. Обозначения: D — design/авторство `Sol ultra`, I — реализация
готового контракта `Sol medium`, R — независимый review `Sol high`.
Пути ниже от корня выбранного superproject; новые outputs явно proposed.
Source/RV ссылки сверяются в CP-SOURCE; исторический `e48e5b2` не равен
current root `93880c23`. Это датированные locators, не дополнительный source lock.

Общий output каждой task: owning diff/commit, primary locators, список реально
выполненных checks/limits, original failures и table claims/evidence/limits/decision.
Для author-пакета предлагается 90 минут до checkpoint, не более двух corrective
rounds без focused replan. Это не оценка трудоёмкости и не текущий compute grant.
Docs-only checks ограничиваются source/Markdown/YAML/links/format. Julia/imports,
docs build и browser execution имеют отдельные задачи/grants.

## DOC01 — актуализировать требования и их authority

**Owner/role:** Root/Research, D `ultra`, R `high`. Coverage RV00/RV03/SI01.
**Inputs:** current user goals, historical 59 IDs, RV00 ledger и первичные decisions;
`docs/system/{README,requirements,comprehensive-review,architecture,release-roadmap}.md`.
**Paths:** только эти owning docs и предложенный sanitized decision appendix;
никаких scientific config, arrays, runtime/installer mutations.
**Grant/deps:** DEV; CP-SOURCE, затем CP-DESIGN. Server не требуется.

- [ ] Связать каждый historical ID с requirement text, epoch, первичным decision
  и состоянием current/target/implemented/historical/unpublished/unknown.
- [ ] Применить текущие цели: все findings, cluster, worker distribution и
  convergence/physical attempt. Не превращать наличие кода в требование.
- [ ] Собрать только существенные противоречия в decision packets: например
  обязательность старых GUI/domain features, backend scope, scientific target.
  Не отправлять пользователю повторный опрос всех 59 строк.
- [ ] Принятый earlier decision сохранить без нового вопроса, если он не
  противоречит последнему поручению; противоречие локализовать с locator.
- [ ] Для каждого proposal дать implement/preserve/conditional/needs_operator
  с основанием. Неподтверждённый proposed интерфейс не выдавать за accepted.

**Acceptance:** 59/59 dispositions с источниками либо explicit unknown;
ни один новый conflict не удаляет историю. Requirements scope фиксируется CP-START/
CP-EXCEPTION один раз по связанным вопросам; остальные docs идут независимо.
**Check:** адресное сравнение ID sets с original ledger, Markdown links и
`git diff --check` после будущих правок. Не считать count semantic acceptance.
**Stop:** нет primary decision — needs_operator только dependent scope.

## DOC02 — три reader routes на существующих owning docs

**Owner/role:** Core/Runner/Root, D `ultra`, отдельные owning R `high`.
Coverage RV16/RV04/RV19. **Deps:** DOC01, D08 corrections из development.md.
**Paths:** Core `docs/src/theory/09_scba.md`, `12_validation.md`,
`docs/src/developer/traceability.md`; Runner `docs/src/user/{configuration,results}.md`,
`docs/src/api/public.md`; Root `docs/single-server-deployment.md`.
**Grant:** DEV. No imports/build/solve.

- [ ] Researcher route объясняет raw residual, mixed step, fresh final U/G,
  measured/not_measured, weights/near-zero; пример ограниченный, явно synthetic.
- [ ] Developer route показывает `configuration_source` и реальный override
  пример 17/23; formula/value/assigning/effective origins различаются.
- [ ] Operator route начинается с цели recovery: pending не resume;
  latest corrupt → verified previous; оба отсутствуют → error с preserved evidence.
- [ ] В каждой route дать canonical API/schema/formula и реальный artifact locator
  только если он существует. Missing raw не заполнять примером от другого run.
- [ ] Сохранить expert reference и accepted scope: optical operator docs не
  означают обещание количественного gain в этом релизе.

**Acceptance:** три независимых reader scenarios имеют понятный вход, действие,
ожидаемый результат и ограничения. Формулы не скопированы в Portal/runbook.
**Check:** links/anchors/static example consistency; browser readability в DOC05.
**Stop:** missing artifact блокирует только конкретную иллюстрацию.

## DOC03 — источник model/source help и граница генерации

**Owner/role:** Core/Research/Contracts/Runner/Portal, D `ultra`, R `high`.
Coverage RV18/RV19/C06/R10/R11/D10; required/conditional статус после DOC01.
**Paths:** existing `docs/system/physics-documentation.md`, owning API/schema/model
docs; proposed contract в Contracts только после CP-DESIGN.
**Grant:** DEV. Product implementation в отдельной DOC07.

- [ ] Зафиксировать один canonical source для signature/units/constraints,
  научного смысла, происхождения value и assigning-source/effective input.
- [ ] Выбрать минимальный docs artifact route, сохранив existing Documenter.
  Сравнить hub-ссылки и полноценный search adapter по нужным reader journeys.
- [ ] Описать proposed fragment identity/release/source binding, allowlist,
  unknown provenance и version compatibility; private logs/arrays/secrets исключить.
- [ ] Указать serving `/docs/` до Portal catch-all и поведение direct anchors,
  offline assets и старых ссылок. Новый solver/model registry не создаётся.
- [ ] Согласовать optional UI help только если DOC01 подтверждает scope;
  technical contract может пройти CP-DESIGN без нового per-field approval.

**Acceptance:** exact consumed/produced fields, source ownership, example unknown,
selected generator/pins/build recipe prerequisites, five negative cases:
wrong release, missing source, private path, unknown origin, catch-all routing.
**Stop:** outside-scope UI или новая trust boundary → operator packet.

## DOC04 — один pinned light/offline publication pilot

**Owner/role:** authoring/generation design D `ultra`; recipe implementation I
`medium`; independent R `high`. Coverage RV18/RV19. **Deps:** DOC02/03,
DEV assets/import identity и OPS immutable builder admission.
**Paths:** Core/Runner `docs/make.jl`, docs Project/selected locks, authored sources;
Root docs entry; Portal/Platform serving files по принятому DOC03 contract.
**Grant:** DEV для recipes, BUILD для render. Только один writer на owning recipe.

- [ ] Выбрать три slice: физическая глава, API/config reference, operator recovery.
- [ ] Зафиксировать installed generator/version/source/locks и последствия imports,
  doctests/@examples. Не исполнять production solver при build/view страницы.
- [ ] Устранить auto-dark/theme alternatives в owning generation и закрепить
  локальные math/fonts/search assets; generated HTML не canonical source.
- [ ] Сформировать immutable public bundle, manifest и source/build receipt;
  проверить allowlist и отсутствие private payload/paths.
- [ ] Сохранить headings/anchors/known aliases; version pointer меняется только
  отдельной deployment stage, после acceptance.

**Envelope proposal:** один build candidate и до двух corrected builds при
изменившемся source, до 30 минут каждый; CPU/RAM/disk из fresh BUILD admission;
stdout/stderr до 8 MiB/attempt с retained original logs. Истечение — replan.
**Acceptance:** reproducible recipe/receipt и готовый candidate для DOC05;
один build exit не является browser/offline/light pass.
**Stop:** неизвестный import effect или missing pin — закрыть input, не установить latest.

## DOC05 — browser/reader acceptance и serving

**Owner/role:** independent evaluator `high`; bounded serving I `medium` после
DOC03 design. **Deps:** DOC04; OPS serving candidate для production mount.
**Grants:** BUILD для isolated preview, OPS для production serving; PLAN не подходит.

- [ ] Проверить каждый reader route с cold cache и отключённой внешней сетью:
  math/fonts/search/direct anchors работают из заявленного bundle.
- [ ] Проверить светлую тему при dark/light OS, reload и сохранённых preferences;
  нет альтернативной тёмной темы. Формы, error/loading, графики и dialogs читаемы.
- [ ] Проверить keyboard/focus/contrast, direct `/docs/…` и `/api/v1/…` routes,
  root Portal fallback; auth behavior сохраняется.
- [ ] Проверить stale/wrong release bundle, отсутствующий asset и private path
  как отрицательные случаи, сохранив screenshots/network/errors.
- [ ] Отдельно измерить runtime serving после OPS; preview receipt не переносить.

**Envelope:** до 60 минут на candidate, три journeys × offline/online × light/dark
OS; один correction/recheck для изменённых output paths. Browser receipts указывают
version/context/source. **Stop:** missing backend browser/asset остаётся unknown.

## DOC06 — static source-to-view prototype

**Owner/role:** D `ultra` выбор способа, I `medium` approved bounded prototype,
R `high`. Coverage RV19, optional tool choice из DOC03. **Grant:** DEV; BUILD
только если selected generator нуждается в runtime/import, это объявляется отдельно.
**Paths:** owning docs/recipe для одного API и одного config leaf; не весь corpus.

- [ ] Использовать `configuration_source` и `production.energy_chunk` как fixed slice.
- [ ] Зафиксировать все десять fact classes RV19: signature/units/default/constraint,
  effects/errors, formula/value/assigning origin, override/example/owner distinctions.
- [ ] Выбрать source-only extraction с запрещённым target inspection/import;
  config/plugins/extension effects также ограничить. Dynamic facts пометить partial.
- [ ] Проверить positive source, missing source, malformed schema, unsupported
  dynamic construct и target module с sentinel side effect, который не выполняется.
- [ ] Сравнить authored meaning и generated facts; не генерировать rationale
  допуска, private effective override или scientific applicability из имени поля.

**Acceptance:** один воспроизводимый bounded output + controls + source receipt;
нет требования заменить весь generator stack. Existing tools сохраняются при
отсутствии доказанной выгоды. **Stop:** missing version/API → focused discovery.

## DOC07 — model/source help integration, scope принят в P1

**Owner/role:** I `medium` по DOC03 contract, R `high`; новая неизвестная causal
semantics возвращается D `ultra`. Coverage R11/D10; включение DOC07 в scope явно
утверждено B/PERM14 из [P1](operator-permissions.md), approved_standby до EXEC.
**Deps:** DOC01/03/04, DEV schemas/config origins, OPS serving. **Grant:** DEV.
**Paths:** Contracts schema first, Core/Research content, Runner effective-source
adapter, Portal Help/field/run presentation; separate component PRs.

- [ ] Контракт отличает model/formula, numeric value и effective assigning input;
  unknown показывается как unknown, не ноль и не выдуманный DOI.
- [ ] Карточка run использует его immutable source/config, не current defaults.
- [ ] UI содержит ссылку на canonical fragment; формулы/thresholds не переносятся
  в React/scheduler. Чтение не запускает solve или тяжёлый derive.
- [ ] Проверить known/unknown source, override, historical run, wrong release и
  unavailable bundle; единицы и варианты сохраняются.
- [ ] Пройти owning targeted checks и DOC05 light/browser сценарии.

**Acceptance:** typed contract+fixtures+truthful UI, preserved existing submit.
**Stop:** новое требование за пределами accepted P1 scope → operator decision;
принятое включение DOC07 повторно не согласовывать.

## SI01 — authority/epoch claims

**Owner/role:** Root D `ultra`, R `high`. **Paths:** `docs/system/agent-review-workflow.md`,
`skills-and-instructions-review.md` и точные неверные claims AGENTS/skill references.
**Deps:** DOC01. **Grant:** DEV; no new authority registry/service.

- [ ] Сопоставить C01–C07 из original fixcard с current user scope и epochs.
- [ ] Сохранить old facts, отличить implementation/target/historical/unpublished;
  из «archive hash verified» не выводить scientific truth.
- [ ] Заменить только неверные универсальные утверждения; не переписать 59-ID ledger.

**Acceptance:** каждая строка имеет primary locator/допустимую unknown;
format/static comparison, semantic independent review. **Stop:** factual source
ищется агентом; невыводимый current requirement — один operator packet.

## SI02 — один task contract и autonomy route

**Owner/role:** Root D `ultra`, R `high`. **Paths:** existing nine-field contract
в `docs/system/agent-review-workflow.md`; ссылки из AGENTS/skills.
**Deps:** accepted autonomy.md; **Grant:** DEV.

- [ ] Дополнить existing contract denominator/evidence level, negative+control,
  immutable reviewer inputs, finite rounds, resume и already-authorized path.
- [ ] Сделать один канонический контракт; не копировать другой в каждый skill.
- [ ] Явно указать: scope grant сохраняется, missing input блокирует только dependents,
  routine reversible choices не требуют согласования; CP-OPS/SCI/EXCEPTION остаются.
- [ ] Проверить сценарии authorized check, docs-only change, missing raw и unknown
  remote outcome как static cases; не назвать их observed behavior pass.

**Acceptance:** no competing contract; all permissions/gates traced to user/owner.
**Stop:** conflict current operator vs historical prose решается текущим operator intent.

## SI03 — routing AGENTS и owning contribution instructions

**Owner/role:** Root/component docs authors D `ultra`, R `high`; narrow ready text
patch I `medium`. **Paths:** root `AGENTS.md`, восемь owning `CONTRIBUTING.md`;
component rules только в их PR. **Deps:** SI01/02. **Grant:** DEV.

- [ ] Добавить короткий action-class routing: docs/source audit/metadata,
  targeted code check, numerical environment, build, live/native, science.
- [ ] Сохранить целиком physics integrity, finite costly envelope, fresh admission,
  bootstrap preflight/nginx, protected foreign resources, CI-once и fixed-light.
- [ ] Qualified contribution commands: docs-only не требуют Julia/install;
  код требует relevant checks; full native suite имеет свой stage/envelope.
- [ ] Проверить requirements preservation с before/after checklist; сокращать
  bootstrap blocks можно только без потери конкретных gates.

**Acceptance:** восемь component dispositions, no weakened gates; отсутствие
локальной Julia не блокирует doc correction. **Stop:** generic cleanup вне owned scope.

## SI04 — четыре references и standalone lookup

**Owner/role:** scientific docs D `ultra`, R `high`. **Grant:** DEV. **Paths:**
`.agents/skills/qcl-research-framing/references/brief.md`,
`qcl-physics-audit/references/physics-checks.md`,
`qcl-results-analysis/references/comparison.md`,
`qcl-performance-audit/references/telemetry.md`.

- [ ] Разделить current source-only, immutable archive и standalone installation.
- [ ] Убрать универсальное «текущий README» как source старого результата;
  выбрать version-compatible primary reader и сохранять missing.
- [ ] Перепроверить symbols/paths по фактическому selected source; dated examples
  оставить датированными. Не копировать formulas/thresholds/schema into agent skill.
- [ ] Essential task fields доступны без root checkout; unavailable owner docs
  обозначены точным gap, а не выдуманным fallback содержимым.

**Acceptance:** четыре refs имеют три routes и working link/source locators;
no automatic runtime execution. **Stop:** missing archive/checkout ограничивает claim.

## SI05 — четыре SKILL.md и UI metadata

**Owner/role:** skill author D `ultra`, independent R `high`.
**Paths:** `.agents/skills/qcl-*/SKILL.md`, их `agents/openai.yaml`;
references только по SI04. **Deps:** SI01–04. **Grant:** DEV.

- [ ] Сохранить четыре name/description/trigger и области ответственности.
- [ ] Physics audit работает source-only без обязательного архивного run.
  Results audit требует existing data только для result claims, не для source checks.
- [ ] Убрать вечный статус RO-Crate из skill как нормативный факт; актуальный
  optional feature status искать в owning docs без превращения его в новый gate.
- [ ] UI prompt вызывает правильный skill и не обещает full scientific/runtime
  acceptance. Standalone fallback сохраняет scope и unknown inputs.
- [ ] Не добавлять новый perpetual approval flow; имена API/units/formулы не менять.

**Acceptance:** format и manual properties отдельно от SI07 forward behavior.
В future execution read installed `skill-creator` validator source/version; команда
`python3 "$SKILL_CREATOR_DIR/scripts/quick_validate.py" "$CANDIDATE_SKILL_DIR"`
допустима только после binding этих путей и hash. Это не сегодняшняя команда.
**Stop:** unknown validator scope не заменяет documented manual properties.

## SI06 — engineering route preserve / условный новый skill

**Owner/role:** аудит `high`; новый design `ultra` только при доказанном gap.
**Paths:** существующий routing/методика; новый skill сегодня не предполагается.
**Deps:** SI02/03 и realistic existing Portal/lifecycle task. **Grant:** DEV.

- [ ] Выполнить один ограниченный реальный engineering scenario существующим route.
- [ ] Проверить owner/failure/compatibility/review handoff, а не число прочитанных файлов.
- [ ] Если route достаточен, закрыть preserve с evidence и не создавать skill.
- [ ] Если повторяемый gap установлен, предложить минимальный design и проверить,
  что его не закрывает исправление existing task contract.

**Acceptance:** demonstrated preserve или конкретный independent counterexample;
один существующий Portal bug не доказывает необходимость нового framework.

## SI07 — independent formal/forward evaluation

**Owner/role:** independent evaluator `high`, автор SI01–05 не оценивает сам себя.
**Deps:** frozen SI01–05 candidates с source/file hashes. **Grants:** DEV для bounded
validator/read-only agent samples; никаких solver/build/server/install действий.

- [ ] Зафиксировать actual Python/validator source/version/hash; не устанавливать
  неизвестный validator. Original quick_validate проверяет frontmatter/name grammar
  и некоторые placeholders, но не folder/name equality и не behavior.
- [ ] Отдельно проверить name==basename, supported UI fields, short description
  25–64 characters, quoting/skill reference, Markdown targets и standalone paths.
- [ ] Подготовить frozen raw cases: T02 archive identity, T03 source-only physics,
  T05 already-authorized bounded check, T14 missing/null telemetry.
- [ ] Для каждого case получить ровно два fresh samples TOTAL: candidate guidance
  и no-candidate-guidance control. Baseline user authorization/safety одинакова;
  controls не получают права на запрещённый solve. Никаких previous answers.
- [ ] Samples изолированы по context/output; evaluator не получает авторский diagnosis.
  Проверяются scope/identity/missing/owner/oracle/completion/local stop/evidence.
- [ ] Сохранить raw failures/controls/unknowns и разногласия; agreement не score.

**Envelope:** 4×2=8 samples вместе с controls, до 40 минут общего wall,
не более двух workers и 1 CPU/1 GiB на read tools каждого, output total ≤128 KiB.
Это один proposed evaluation block; cap не умножается на число agents.
**Acceptance:** per-property observations и ограничения; 8 samples не доказывают
универсальную корректность. Unauthorized action/cap останавливает sample;
formal-format pass не превращается в forward behavior pass.

## Итог coverage и границы

| Утверждение | Свидетельство в плане | Ограничение | Решение |
| --- | --- | --- | --- |
| RV00/03/16/18/19 покрыты | DOC01–07 + owning DEV/OPS/SCI dependencies | Optional UI scope требует DOC01 disposition | сохранить |
| Все SI01–07 имеют конечный выход | SI карточки, validator scope и 8-sample protocol | Пока ничего не исполнялось | сохранить |
| Документация подтверждает runtime/science | Separate BUILD/browser/SCI receipts | Текст и format этого не доказывают | дополнительно измерить |
