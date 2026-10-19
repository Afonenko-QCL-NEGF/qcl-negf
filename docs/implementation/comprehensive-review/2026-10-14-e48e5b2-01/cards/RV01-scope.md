# RV01: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV01.md, fixes/RV01-*.md; reviews/RV01-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

## RV01 — паспорт наблюдавшегося исполнения

**READY:** metadata-only audit. Owners Results/Research/operator.
**Входы:** source audit, receipt
`canonical-update-ROOT-recovery-attempt4/ROOT-result.original.json`, SHA256
`4c8e87704377cd8693ed6e79ada4c338d973e6192fd065e4b197506c1bbdd3e3`;
run `dfb75b38-6019-4861-b868-f51648c71f02`, frozen-plan SHA256
`4d69332f0770734102c77089ad6cbe4cb2a35b1dde71380cfb59fa13680929f9`;
saved status SHA256
`d6a022f9c11fdb3c5191f796aa795ad9fb383779d67ac5ac036b1bcb6a989a90`.
Reader semantics — Results `src/qcl_negf_results/{multipart,native,model}.py` на `S`.

- [ ] Сопоставить доступные originals с hashes; если доступны только записи
  source audit, явно оставить первичную верификацию неизвестной.
- [ ] Разнести selected source, installed release `qcl-5d779b52-s01-20261012`,
  imported runtime, plan/model/schema, run, attempt и artifact profile по полям.
- [ ] Проверить `/native_owned_closure/runtime/ready`,
  `/native_owned_closure/gate/open`, `/native_owned_closure/delivery_report/status`,
  `/scientific_accepted`, `/full_release_CI_accepted`; составить inventory частей и gaps.
- [ ] Записать отдельный вектор execution/convergence/physics/discretization/
  experiment; назначить HDF5-подпакет только при доступных raw identity,
  schema/shapes/axes/weights и отдельном bounded объёме чтения.

**Oracle/negative case:** exact attempt + plan/hash; технический completed
при scientific=false, неполный multipart и старый RUNNING.
**Acceptance:** все поля имеют verified locator, secondary evidence или missing;
RUNNING от 2026-10-13 17:46 UTC не объявлен live now. **Выход:** `R/RV01.md`,
M06/M18/M19/M20; metadata-паспорт DONE не принимает физику. Missing matrices
создают `needs_data` только для raw-проверки RV08/сравнения RV10; новый submit
не восстанавливает provenance старой попытки.

