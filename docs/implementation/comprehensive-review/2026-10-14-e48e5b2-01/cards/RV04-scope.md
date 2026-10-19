# RV04: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV04.md, fixes/RV04-*.md; reviews/RV04-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

### RV04 — Core/Runner cohesion и impact

Входы: `components/QCLNEGF.jl/src/QCLNEGF.jl`, `src/domain/`,
`src/numerics/reference/`, `src/numerics/optimized/`; Runner
`src/QCLNEGFRunner.jl`, `src/core_api.jl`,
`src/application/coordinator.jl::run_sweep!`,
`src/composition/configured_execution.jl::execute_configured_run`.

- [ ] Построить include/import/call/mutation карту одного operating-point→persist
  пути; отдельно dynamic, file и orchestration edges.
- [ ] Проверить владельца каждого эффекта и hotspot по состояниям/exception
  paths, сопоставить relevant tests.
- [ ] Рассмотреть negative case: перенос persistence в Core или общего helper
  в oracle; предложить только bounded alternatives с invariant.
- [ ] Сохранить `R/RV04.md`: карта и change-impact tickets.

Приёмка: source каждого edge, owner и affected interfaces/tests известны;
LOC не объявлен дефектом. M12 — SCC/forbidden edges выбранного graph; M13 —
объяснённые hotspots, численный CFG неизвестен без инструмента. RV03 нужен
только для утверждения спорной локальной границы, не начала чтения.

