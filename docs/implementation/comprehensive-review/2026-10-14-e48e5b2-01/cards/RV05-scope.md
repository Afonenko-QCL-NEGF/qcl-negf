# RV05: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV05.md, fixes/RV05-*.md; reviews/RV05-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

### RV05 — AiiDA actor и HTTP complexity

Входы: Portal `src/qcl_negf_api/service.py::AiidaService._call/close/open_artifact`,
`api.py::create_app/ClosingStreamingResponse`, `exports.py::ExportStore`;
AiiDA `src/aiida_qcl_negf/service.py`, `workflow.py`; Portal
`tests/test_service.py`, `test_stream_disconnect.py`, `test_exports.py`.

- [ ] Табулировать profile/loop/handle owners, queue, deadlines, errors и close;
  читать assertions о единственном thread и освобождении reader.
- [ ] Проследить exception/cancel пути HTTP→actor→AiiDA и export→spool.
- [ ] Описать stalled operation и disconnect как negative cases; отделить
  подтверждённый synchronous wait от недоказанного production hang.
- [ ] Выпустить `R/RV05.md` с targeted fixture tickets и contract gaps.

Приёмка: каждое обещание responsiveness имеет boundary и witness/unknown.
M04 — property×failure catalogue; M13 — состояния/fan-out выбранных функций.
Зависимость RV07: только semantics выбранной операции.

