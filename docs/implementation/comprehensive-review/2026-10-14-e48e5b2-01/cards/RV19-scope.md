# RV19: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV19.md, fixes/RV19-*.md; reviews/RV19-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

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

