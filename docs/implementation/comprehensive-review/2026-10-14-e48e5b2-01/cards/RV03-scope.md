# RV03: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV03.md, fixes/RV03-*.md; reviews/RV03-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Selected denominator before review

12 edges: Runner→Core; Results→Contracts; AiiDA→Contracts; Portal→AiiDA; Portal→Results; Root→Git-selected components; Browser→Portal StaticFiles/API; Portal actor→AiiDA profile/handles; AiiDA CalcJob→Runner CLI/configured_run; Runner artifacts→retrieved AiiDA/Results; Platform application closure→Portal/AiiDA services; storage/controller/worker state owners.

## Исходная карточка (frozen source, не дополнительная авторизация)

## RV03 — actual views и обоснованные alternatives

**READY:** source-only views. Owner Root/all component owners.
**Входы:** `docs/architecture.md`, manifests каждого gitlink `S`;
Root `ops/{git,environment}.ts`; Core/Runner `src/QCLNEGF*.jl`;
AiiDA `src/aiida_qcl_negf/{service,workflow}.py`; Portal
`src/qcl_negf_api/api.py`; Platform `flake.nix`, `nix/application.nix`,
`ops/{application_release,worker_lifecycle}.py`. Target — docs-ref
`docs/system/architecture.md`, адресные RV00 rows.

- [ ] Отдельными пакетами восстановить dependency/import, context/container,
  job/data/release lifecycle и deployment/storage views.
- [ ] Для каждого edge записать source commit+path/symbol, направление,
  owner, interface и изменяемое состояние; проследить вызов или файл на обеих сторонах.
- [ ] Сопоставить actual с target; alternatives обозначить proposed, указать
  сохраняемый invariant, counterexample, цену и owner следующей проверки.

**Oracle/negative case:** две стороны контракта и executable/config evidence;
metadata DAG против dynamic/file cycle, repository против process boundary.
**Acceptance:** каждый показанный edge подтверждён либо marked unknown;
installed/deployment observation не приписана source baseline. **Выход:**
`R/RV03.md`, M06/M12; локальные views доступны RV04–RV07/RV13–RV19.
RV01 нужен лишь для installed/archive overlay, не для завершения остальных views.

