# RV07: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV07.md, fixes/RV07-*.md; reviews/RV07-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

### RV07 — Contracts и consumer semantics

Входы: Contracts `src/qcl_negf_contracts/schemas/`,
`artifacts.py::validate_export_receipt/validate_commit/validate_execution_progress`;
Runner `schema/PROVENANCE.json`, `src/infrastructure/config/json_schema.jl`,
`configuration_contract.jl`; AiiDA `service.py::_select_child/get_export_plan/list_artifacts`;
Portal `exports.py::ExportStore.create/_prepare`, `api.py::ExportRequest`.

- [ ] Построить producer/consumer/version/migration matrix: attempt, missing,
  precision, limits, effective origin; найти existing schema drift guard.
- [ ] Сопоставить `tests/test_contracts.py`, AiiDA `tests/test_restart.py`, Portal
  `tests/test_exports.py`, Runner `test/contracts/draft_2020_12_configuration_contract.jl`.
- [ ] Задать valid/invalid corpus bool/int/NaN/Infinity/origin и два attempts:
  frozen plan и raw bytes должны иметь одну exact selection.
- [ ] Выпустить `R/RV07.md`; current и archived refs получить отдельные claims.

Приёмка: одинаковые schema hashes не заменяют guard; ambiguous export не
считается допустимым молча. M04 — corpus; M06 — schema identity edges;
M12 — contract ownership. От RV00 требуется лишь решение спорного ограничения.

