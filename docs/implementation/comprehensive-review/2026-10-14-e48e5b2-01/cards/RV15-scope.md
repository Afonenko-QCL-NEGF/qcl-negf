# RV15: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV15.md, fixes/RV15-*.md; reviews/RV15-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

### RV15 — security boundaries и rejected paths

Входы: Portal `api.py::BodyLimit/create_app/byte_range`, `settings.py::Settings`,
`exports.py`; AiiDA `validation.py::validate_scratch_root/scheduler_options`,
`calculation.py::prepare_for_submission`, `service.py::_artifact_path`;
Platform `application_release.py::read_protected_file/freeze_ssh_trust`,
`ops/bootstrap_ownership.py`, root `.github/workflows/`.

- [ ] Составить auth/read/submit/cancel/download, executable input и trusted CI
  boundary matrix; учитывать single trusted team scope.
- [ ] Читать Portal `tests/test_api.py`, AiiDA `tests/test_artifact_locator.py`,
  Platform `tests/test_bootstrap_ownership.py`; найти public logging/redaction.
- [ ] Описать path traversal, symlink/FIFO, oversized body и untrusted executable
  как negative cases; не читать реальные token/private inventory.
- [ ] Выпустить `R/RV15.md` с минимальными rejected-input tickets.

Приёмка: threat assumptions, failure locators и пределы mock известны;
source audit не утверждает отсутствие всех уязвимостей. M04 — rejected paths;
M12 — trust edges. RV07/12 дают только конкретные contract/cancel outputs.

## Завершение этой редакции

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Все 11 инженерных RV разложены до автономного audit | Точные symbols, checkboxes, negative cases и `RVxx.md` выше | Будущее исполнение требует task capsule и общего envelope | сохранить |
| Public baseline доступен независимо от live/site данных | HEAD/gitlinks, адресно прочитанные owning source/tests/manifests | Candidate PR6 object отсутствует локально; remote diff ещё не прочитан | сохранить |
| Runtime, coverage, rebuild и recovery не установлены | На этапе автора выполнено только чтение и статическая проверка плана | Suites/builds/server/solver/profile не запускались | данных недостаточно |
