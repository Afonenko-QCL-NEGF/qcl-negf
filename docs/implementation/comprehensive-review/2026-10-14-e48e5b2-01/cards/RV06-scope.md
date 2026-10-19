# RV06: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV06.md, fixes/RV06-*.md; reviews/RV06-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

### RV06 — Platform lifecycle ownership

Входы: Platform `ops/application_release.py::lifecycle_owner/activate/deliver_cli/guard`,
`ops/worker_lifecycle.py::shutdown_step/startup`, `ops/bootstrap_build.py::main`;
`tests/test_application_release.py`, `test_worker_lifecycle.py`,
`test_worker_shutdown_intent.py`, `test_build_admission.py`.

- [ ] Выписать desired/observed states, flock scope, durable intent, ready/admission
  publications и recovery transitions.
- [ ] Сопоставить assertions со сценарием crash между profiles, environment,
  allowlist и ready marker; проверить отсутствие второго lifecycle writer.
- [ ] Разобрать negative cases stale admission и disappeared job без receipt.
- [ ] Выпустить `R/RV06.md`, указать публичный fixture и отдельный live check.

Приёмка: неопределённый исход не открывает admission по предполагаемому успеху.
M04 — отказные переходы; M10 — declared managed objects и неизвестный live drift;
M11 — role×scenario catalogue, native cells `not_measured`. Private inputs
ограничивают runtime cells, сохраняя source conclusions.

