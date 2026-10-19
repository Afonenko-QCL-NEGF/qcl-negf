# RV11: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV11.md, fixes/RV11-*.md; reviews/RV11-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

### RV11 — publication, checkpoint и raw preservation

Входы: Runner `src/infrastructure/persistence/point_artifacts.jl::commit_point_artifacts/load_recovery_commit`,
`atomic_files.jl::_atomic_replace_file`,
`src/infrastructure/runtime/filesystem_repository.jl::save_runtime_checkpoint!`,
`src/composition/scratch_execution.jl::stage_result_tree`; Results
`state.py::StateReader/verify_recovery_bundle`, `archive.py::verify_archive`.

- [ ] Проследить generation→commit→receipt→pointer→reader, fsync и pruning;
  назвать сохраняемые raw/model/plan/attempt invariants.
- [ ] Читать Runner `test/infrastructure/scratch_execution.jl`,
  `production_restart_validates_metadata_and_restores_state.jl`, Results
  `tests/test_state_reader.py`, `test_series_commit_identity.py`.
- [ ] Составить partial-write/ENOSPC/NFS-loss/worker-loss packet;
  hash-valid external HDF5 и wrong attempt — negative cases.
- [ ] Выпустить `R/RV11.md`, раздельные local durability и production claims.

Приёмка: сохранены original arrays и failure evidence; receipt не science pass.
M04 — fault catalogue; M09 — recovery timeline requirements, RPO/RTO
`not_measured` без опыта. RV07 даёт выбранную identity semantics;
RV01 нужен только для архивного экземпляра, не synthetic/source audit.

