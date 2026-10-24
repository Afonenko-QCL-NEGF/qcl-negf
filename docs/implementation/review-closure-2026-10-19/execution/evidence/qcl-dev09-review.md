# DEV09 — независимый CP-CODE review

Дата: 2026-10-19. Reviewer /root/reviewer, gpt-6.1-sol high.
Verdict: **PASS**; blocking gaps нет. Scope — только новый
`docs/export-selection.md` и одна ссылка в `README.md` AiiDA.

Base AiiDA `53e2a20544a469dd7ee5560243ebe530a6310f0a`, root source
`e0f244d075dd49874ba4f3847f4efa693f3b3622`.
Exact review package `/tmp/qcl-dev09-review.diff` SHA256
`cf8ce5e27bcc1b41e638fd7ab5a06dfdd901bc1c60e0f1a78cf26e49007780a1`.
Owning doc SHA256 `9f819402f8fc50d2d4635b8dfe0a25cd3e1ef04d7850a12722c77f015bd76ec6`;
README SHA256 `99f005c6bff8ff55a74e2fef643d426abc822b1bbe3d6baeb2efd83f7f8094c8`.
Все три hash независимо измерены и совпали с handoff.

`diff -u` owning doc против approved design
`d261082ec1eed08534fa98759ac304ae131901d9799f3b397329ad427c8bc40d`
показал ровно две согласованные editorial differences: header теперь отмечает
accepted CP-DESIGN; present result explicitly разрешает шесть source statuses,
а synthetic unknown только при absent result link. Других contract changes нет.

Сохранились exactly4fields, strict selectors и effective exact pair,
resolve-once/default selection authority, bounded result metadata read,
missing/corrupt distinction, frozen status, same-child later-status cache policy,
new mismatch422/old single-file404, raw-plan decoded equality, positive/negative
fixture matrix и отсутствие runtime/native/scientific acceptance claims.
README получает одну owning link с существующим target.

Reviewer checks: package reverse-apply check exit0; targeted tracked
`git diff --check` exit0; stdlib UTF-8/trailing whitespace/single-final-newline
check двух документов pass; README local target существует.
`git diff -- src/aiida_qcl_negf/service.py` пуст. Concurrent untracked
`tests/test_export_selection.py` принадлежит DEV10 и исключён из этого review.
Tests, imports продуктовых packages, build, server и solver не запускались;
глобальный source audit не повторялся.

Неблокирующее editorial замечание: заключительная таблица документа ещё
упоминает CP-DESIGN reviewer как будущую зависимость; accepted header и этот
receipt задают текущий статус. Это не меняет контракт и не требует нового round.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Owning docs передают accepted DEV09 contract | Exact hashes + two-change comparison с approved design | Implementation/fixtures DEV10/11 отдельно | сохранить |
| README link и source format корректны | Target exists, reverse check, whitespace/UTF-8 checks | Docs render не выполнялся | сохранить |
| Runtime/native/scientific acceptance установлена | Таких receipts нет | No product imports/tests/build/server/solve | данных недостаточно |
