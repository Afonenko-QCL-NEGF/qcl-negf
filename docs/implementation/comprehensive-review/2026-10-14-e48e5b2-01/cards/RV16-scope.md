# RV16: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV16.md, fixes/RV16-*.md; reviews/RV16-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

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
- [ ] По [методике](/home/tolya/Загрузки/qcl-negf/docs/system/documentation-methodology.md) развить понятный пример:
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

