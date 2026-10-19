# RV17: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV17.md, fixes/RV17-*.md; reviews/RV17-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

## RV17 · Семь самостоятельных instruction packets

**Owner:** root/skill owners с тремя ролями. **Вход:** actual `AGENTS.md`,
восемь `CONTRIBUTING.md`, Portal `AGENTS.md`,
[skills review](/home/tolya/Загрузки/qcl-negf/docs/system/skills-and-instructions-review.md),
[готовый проект workflow](/home/tolya/Загрузки/qcl-negf/docs/system/agent-review-workflow.md) и четыре каталога
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
