# RV13: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV13.md, fixes/RV13-*.md; reviews/RV13-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

### RV13 — публичный restore и границы private site

Входы: Platform `flake.nix`, `modules/state-archive.nix`, `storage.nix`,
`ops/state_archive.py::pack/verify/restore_admission/stop_services`,
`docs/state-archive.md`, `docs/host-storage.md`, IaC `tofu/proxmox/` и
`tofu/local-lab/`; root `docs/single-server-deployment.md`.

- [ ] Сопоставить четыре roles, config/storage owners, DB+repository consistency,
  backup/reinstall/cold-start и foreign VM/data exclusions.
- [ ] Читать `tests/test_state_archive.py`, `test_proxmox_storage_contract.py`;
  выделить synthetic bytes restore и реальные PostgreSQL/service гарантии.
- [ ] Описать negative cases mismatched DB/repository generation и общий
  filesystem AiiDA/Slurm; составить sanitized inventory contract без секретов.
- [ ] Выпустить `R/RV13.md`; продолжить public audit при missing site inputs.

Приёмка: отсутствующий admission блокирует только operation; сохранение
mutable datasets явно проверяемо. M09 — incident/recovered timeline;
M10 — managed objects; M11 — role/backend/scenario cells. Live restore
`not_measured`; зависит от RV06/11 outputs лишь для соответствующих transitions.

