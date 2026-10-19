# RV12: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV12.md, fixes/RV12-*.md; reviews/RV12-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

### RV12 — retry, timeout, submit и cancellation

Входы: AiiDA `workflow.py::attempt_decision/QCLExecutionRestartWorkChain/QCLPlanWorkChain`,
`calculation.py::prepare_for_submission/_setup_metadata`, `service.py::kill_run`;
Runner `configured_execution.jl::_check_solver_run_budget`, staging RV11;
Platform `application_release.py::command`, `worker_lifecycle.py::jobs`.

- [ ] Составить parent/CalcJob/Slurm/Runner budgets, ownership и retry matrix;
  проверить сохранение spent budget после recovery.
- [ ] Читать AiiDA `tests/test_restart.py`, `test_submission_identity.py`,
  Runner `test/application/restored_stage_progress_consumes_the_original_budget.jl`.
- [ ] Разобрать submit acknowledged-but-response-lost, ambiguous scheduler owner,
  daemon unavailable и cancel failure; никакого скрытого duplicate submit.
- [ ] Выпустить `R/RV12.md` с exact selected check и отдельным native envelope.

Приёмка: завершение parent, job stop и recovery eligibility различены.
M04 — отказные пары; M11 — native submit/cancel cells неизвестны.
Зависимость: RV11 receipt invariant, RV06 lifecycle boundary выбранного пути.

