# RV14: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV14.md, fixes/RV14-*.md; reviews/RV14-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Selected denominator before review

8 links: Git→selected; source→Julia workspace; standalone→Core resolution; source/depot→solver build; source/lock→frontend derivation; source→release wheels; closures→release manifest; wheel payload→HTTP serving.

## Исходная карточка (frozen source, не дополнительная авторизация)

### RV14 — source/build/import/runtime closure

Входы: root `ops/git.ts::sourceGraph`, `ops/release.ts`, `ops/solver.ts::buildSolver`,
`ops/application_cd.ts::deploymentManifest`, `ops/ci.ts`, `nix/solver.nix`,
`flake.lock`, `uv.lock`, `julia/Manifest.toml`; Runner `Project.toml`,
`tools/prepare_workspace.jl`; Portal `hatch_build.py::CustomBuildHook.initialize`,
`frontend/package-lock.json`.

- [ ] Построить selected-source→lock→derivation→artifact→import/runtime chain,
  включая standalone versus workspace Core resolution.
- [ ] Прочитать saved receipts при наличии; проверить reused native output
  только по derivation, contents и native test contract, сохранив failed logs.
- [ ] Описать stale compiled assets и пакет `0.2.0` из другого commit как
  negative cases; связать Portal assets с source/lock.
- [ ] Выпустить `R/RV14.md` и отдельные rebuild/import tickets.

Приёмка: новый root ref не наследует full release acceptance. M06 — identity
links; M07 — declared bitwise outputs; M08 — consumer properties; последние
два `not_measured` без bounded rebuild. Будущий M07 check: два независимых
rebuilds одной derivation, SHA256 всех заранее declared outputs и byte diff;
это отдельный build envelope, без повторного final CI. Будущий M08 check:
`solver_executable self-check` через `solver_self_check`, receipt
`qcl-negf-self-check-v1/completed`, `scientific_accepted=false`, плюс declared
consumer fixtures. M20 — elapsed до claim; CPU/RSS/I/O неизвестны без
telemetry. RV01 нужен только для installed/archive цепочки.

