# SCI03-M1 phase2 — additive streaming represented-current measurement

2026-10-19. I / Sol medium, source-only. **STOP для отдельного high CP_CODE; sole GREEN выполняет координатор после review/binding.** Здесь выполнены0 Python/import/parser/test/HDF/Julia/SCBA/Poisson/build/install/network/server/stage/commit/push/children. Реализация подготовлена, но GREEN/runtime/scientific acceptance не заявлены.

## Binding и RED evidence

Owning Results worktree `/tmp/qcl-sci03-M1-results-worktree`, branch `codex/review-closure-current-bound-measurements`, HEAD/base `33b1a39eab62b0c00532c4d6b30fa3279c06a5d3`. Только `src/qcl_negf_results/equilibrium.py` изменён этим этапом. Main Results `d6e1f18` и root не редактировались. Dirty frozen test из phase1 сохранён SHA `d4bb720fff951df9ed402709a4f11422f07680925e0dddf6e91dcc2dcef87f79`; README unchanged SHA `39c5c06b1335e6820b980ba3967a42ac25f8fad4b80a771e7297a5982d1363e9`. Protected original не записывался. `/tmp` clone по-прежнему использует read-only selected-source object alternates; metadata/source edits этого этапа только в `/tmp`.

Accepted D SHA `ca84b1cc763aa7bc017364ece4f7e95aff5bd0107c0c7277fb87eed250f215f7`, independent R SHA `fa1311a4bf16f08f6e417590b77b7e6179aa9320907934fbd4496ebc059ca4a9`, owning Research at `3ed8a9f`, contract file SHA `61058d7b33b21e8b43232239569012567e764035dd15900b80d742bd9d6ed38c` сохраняются. Изменений формулы/модели/criteria нет.

Прочитаны точные coordinator receipt и весь raw RED log по последовательным text ranges. Они сохранены без изменения:

- `/tmp/qcl-SCI03-M1-RED-1/receipt.json`, SHA `f685a7460f8c0747b73e5559fb36af44b5a3f7a956f36db38ee18d5dec718fa4`.
- `/tmp/qcl-SCI03-M1-RED-1/original.log`, SHA `bc72a87f5cdab8374d7ac719905f10df75ff0ab2699512baea285a1526620e53`.

Receipt: 13failed/38passed, pytest11.51s, wall12.212s, exit1; complete raw35438B; guard_error/stop_reason отсутствуют. Sampled peak RSS89419776B, owned TMP15534234B. Это coordinator execution с frozen tests и old production33b1, не мой запуск. Sampling не hard quota/peak guarantee. Historical baseline36 и M1_08/M1_09 healthy controls получили passes в этом конкретном RED; другие38 не подменяются scientific acceptance.

Все13 failures классифицированы; неожиданных mechanisms в raw нет:

| № | Exact case suffix | Наблюдаемый RED mechanism |
| --- | --- | --- |
| 1 | M1_01 `[False]` | missing `represented_current_bound`, test614; known-μ/bracket checks до этого прошли |
| 2 | M1_01 `[True]` | тот же namespace assertion; quarter-capacity known-μ checks до него прошли |
| 3 | M1_02 complex | тот же namespace assertion |
| 4 | M1_03 zero boundary | тот же namespace assertion; defined μ check прошёл |
| 5 | M1_04 `[missing_context-not_measured-missing_model_context]` | тот же namespace assertion; inherited μ/status checks прошли |
| 6 | M1_04 `[finite_drive-not_applicable-finite_drive]` | тот же namespace assertion; inherited μ/status checks прошли |
| 7 | M1_04 `[unequal_lo-not_applicable-unequal_LO_temperature]` | тот же namespace assertion; inherited μ/status checks прошли |
| 8 | M1_04 `[ee-unsupported_context-unsupported_electron_electron_closure]` | тот же namespace assertion; inherited μ/status checks прошли |
| 9 | M1_04 `[empty-not_measured-empty_represented_spectrum]` | тот же namespace assertion; inherited μ/status checks прошли |
| 10 | M1_04 `[iteration_limit-algorithm_limit-algorithm_limit]` | тот же namespace assertion; inherited μ/status checks прошли |
| 11 | M1_05 additive/read counts | тот же namespace assertion; read-count assertions ещё не достигнуты |
| 12 | M1_06 overflow | `DID NOT RAISE ContractError` at test183; old API не вычислял overflowing bound |
| 13 | M1_07 report cap | тот же namespace assertion; cap assertion ещё не достигнут |

Это meaningful RED missing-feature evidence; row arithmetic, read counts и cap enforcement новых fields ещё требуют GREEN. Причин расширять допуски или менять tests нет.

## Реализация и mathematical ownership

`equilibrium.py:526–578` добавляет ровно12 streaming `_Norm` к existing pass2: raw/normalized occupied, empty и sum defects (6); по каждой side `(1−f)Γ`, `fΓ`, `Sn−fΓ` (6). Existing stored A/corr_n/corr_p norms переиспользуются; aggregate FDR сохраняет те же δN/δP values/order. `D=δN+δP` вычисляется full complex entrywise до norms; closure и c=n+p не предполагаются. State defects освобождаются перед boundary reads. Одна existing fitted relative μ и те же W=gs*wE*wk/(2π) идут в обе versions/sides; own μ-fit/normalization/A-derived replacement нет.

Side coefficients используют только соответствующие stored SL/SG: Sn=−iSL; Γ=Sn+iSG. Raw Keldysh как прежде использует stored enabled families+embedding_total ровно один раз. Existing full ordered boundary products/signs/common-z и signed compensated sums не менялись. Новых dataset selections/HDF reads/matrix products/public arguments нет. Сохраняются два passes и full-basis tiling; unknown/missing/axis/identity/receipt guards не обходятся.

Private `_represented_current_bound` (`equilibrium.py:138`) строит исключительно additive top-level namespace с точными accepted keys/units. При available μ: `measured/reason=None`; spectral/correction absolute norms независимы от μ. При unavailable μ: state/side/bound groups наследуют exact μ status/reason, dependent scalars и все terms=None прежде любого zero handling. Empty accumulators не превращаются в measured0. При defined μ literal zero coefficients дают zero products/B без division/J, floors, A/donor normalization или acceptance threshold.

Для каждого side/variant guard `_finite` проверяет dimensionless g*n/g*p, `a+c`, d*(a+c), каждую conversion J0*term; `_Sum` проверяет compensated sum и final value. Поэтому finite inputs не допускают measured Inf/NaN при overflow. Алгебра не предполагает commute/Hermiticity/PSD/spectral closure. Bound — Float64 RHS exact-arithmetic represented trace; `arithmetic_error_status=not_measured`, `arithmetic_error_bound=None`, scope `no acceptance`. Нет εJ/H/нового accuracy criterion/pass/accepted field. Current magnitude не становится scientific zero verdict.

## Allocation census и guards

Forecast вычисляется до чтения payload vectors/matrices. Старые `10*8*NE+4096+32*Nk+16*Nb+512*len(descriptions)` сохранены; добавлен fixed reserve12288B (4096scalar accumulators/scratch+8192bounded report reserve). Это accounting numeric scratch и ограниченной scalar metadata, не Python-object/RSS certificate. Per-energy allowance увеличен с24 до32complex slots: `32*16*Nb²`; admitted maximum_workspace_bytes не повышен. Tile/full-plane minimum и logical coordinate/I/O forecast автоматически пересчитываются existing logic. Максимальные single-read/chunk/I/O/report caps не увеличивались.

Новые live allocations при tile t, basis b, C=16*t*b² bytes:

| Фаза | Дополнительные buffers и lifetime |
| --- | --- |
| Common f | f — view existing fermi; 1−f —8t bytes. При переходе tiles может кратко жить прежний vector до reassignment; ≤16t bytes суммарно, не более1C при b≥1 |
| State defects | δN и δP поC; при образовании второго defect или D временный product/sum ещёC. Max3C; δN/δP явно del до следующей version и до side loop |
| Side coefficients | Sn иΓ поC; при γ product или δS formation transient product/result доводят peak до4C. Γ/Sn явно del до existing flux GEMMs и до следующей side |
| Norm/finite scratch | Boolean `isfinite` ≤C/16; full-complex norm посещает real/imag plane views, `.ravel()` возможная bounded per-plane float copy ≤C/2; этот scratch в existing24slots, и margin8slots дополнительно покрывает перекрытие с new buffers/f vectors |

Таким образом additional complex-array peak≤4C, bounded f-vectors≤1C, finite/ravel scratch<1C; reserve8C остаётся консервативным source bound для новых numeric buffers. Existing allocation contract24C не объявляется independently measured RSS. Post-loop helper имеет только конечное число scalars/dicts, не хранит arrays/copies/pass. Ровно12 новых LASSQ entry traversals O(12NE*Nk*Nb²), no new O(Nb³) GEMM. Цена Python loops без benchmark неизвестна.

I/O selection неизменна; если tile уменьшается, coordinate/read-call overhead может вырасти. Physical callback budget остаётся authority actual admission; forecast не заменяет total bytes guard. Existing JSON `allow_nan=False` и maximum_report_bytes(default64KiB) проверяют весь итоговый additive report: при нехватке budget_exceeded, без truncation. Новая metadata конечна, accepted incremental reserve8KiB; фактические encoded bytes должен проверить coordinator GREEN. Source read counts не выдаются за измеренную I/O liveness.

## Frozen outputs и граница завершения

Production SHA `bb3d204378fd7d95691cfd9b58360afc6f48ede1b37fe7a0f6d2a6ff06944915` (36563B). Production-only patch `/tmp/qcl-sci03-M1-impl-patch.diff`, SHA `b9eb4c0000597dc725a14dbc8c947e7e0d232378447edb6f18ecd0a4c59df805`, +86/−5. Baseline сохранён `/tmp/qcl-sci03-M1-impl-baseline.py`, SHA `3f8ee56390741e15bc2c709de67d4b0c80260733c99752d8fbbb4f538e3042e6`. Frozen tests d4bb/README SHA перепроверены без изменений. Overall worktree также содержит прежний phase1 test delta+324; production-only patch не дублирует его.

Выполнены manual source/algebra/allocation review, raw RED classification, SHA, Git identity/status/diff и `git diff --check`. Python syntax/parser/compilation/tests не запускались; это ограничение stage, не success claim. Source-author envelope≤30min,1CPU,2GiB,reads4MiB,outputs96KiB; targeted text/hashes only, resource telemetry не инструментировалась. Этим этапом runtime calls0; campaign M1 consumed1/2 (coordinator RED), remaining1GREEN без automatic third call; SCI05/08 C08 exhausted8/8 без изменения.

S1 0mV/70K LO/acoustic/impurity/IFR/alloy e−e none и scientific caps/strict gates сохранены. Нет actual final arrays/run/attempt/frozen plan/native admission/H/εJ_abs. README reserved separate writer; owning contract publication gate принадлежит координатору. Следующий шаг: separate high CP_CODE по frozen source/tests/RED evidence, затем root binds reviewed bytes и sole bounded GREEN.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Missing-feature RED воспроизведён | Exact coordinator receipt/log, all13 classified | Old production; новых norms/terms не проверяет | сохранить |
| Additive12norm implementation подготовлена | Frozen production hash/patch, source formula/allocation census | Independent CP_CODE и GREEN ещё не выполнены | изменить |
| Frozen tests/README и scientific model сохранены | Exact unchanged hashes, owning source-only diff | Нет нового numerical experiment | сохранить |
| Bound доказывает physical accuracy/equilibrium | H/εJ_abs/actual arrays/admission неизвестны | Float64 RHS не outward enclosure | данных недостаточно |
