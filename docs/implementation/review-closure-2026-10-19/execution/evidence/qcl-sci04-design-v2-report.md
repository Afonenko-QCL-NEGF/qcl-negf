# SCI04-D2 — последний bounded author round

2026-10-19. Второй из максимум двух design rounds. **STOP после этого отчёта.**
Независимый D2 CP-DESIGN ещё нужен; author не объявляет review pass. Никаких
implementation/test/runtime grants этим отчётом не добавлено.

## Exact artifacts

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| D1 preserved /tmp/qcl-sci04-design.md | 31278 | c4e61ff6a9aac94c349b9e941f35f8652606928a7be7c3a23e22245adbaf49fc |
| Independent D1 review | 22773 | 98c37f812b7a19aa9fc02714ef2b8dd092c6a79fbe064c7727060eb10e6a4a66 |
| D2 /tmp/qcl-sci04-design-v2.md | 61527 | d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c |
| Math/schema/source delta /tmp/qcl-sci04-design-v2.diff | 40400 | 3283019ddd99a7f1941d96f5a59e4ed2e4c6233f1441287038f723ca359c9c4b |

D1 author report cf6bc724e2e9b6ea3af6e7e70f8cca61c0cb3f336aac806cb5c6ea9c9e82a824
сохранён без изменения. Full source byte manifest остаётся в нём и D1 review;
это receipt, не parallel lock. Новые files только D2, diff и этот report.

## Независимая оценка R1–R3 и точная дельта

Применены qcl-physics-audit и receiving-code-review: сначала перечитан review,
затем source validation33–81, poisson41–73 и owning Research §5.4; замечания
проверены по actual equations, не приняты по одному согласованию агентов.

| R | Проверка | Изменение D2 | Ограничение |
| --- | --- | --- | --- |
| R1 | max ratio witness не определяет global/max absolute defect; контрпример D=(-1,10),GR=(1,1) даёт ratio witnesses и abs witnesses раздельно | §8.1: global sqrt(sum a²), max a, independent ratio/absolute witnesses, exact tie rule, same pass/O(1) scalars; §9 literal √85/9/2 negative | Conditioning/inverse-Jacobian/contraction unknown, forward accuracy не заявлена |
| R2 | Actual public Poisson four-tuple не содержит raw numerator/rhs/signed charge; исходный allowed-path list исключал owning evaluator | §8.2: private helper внутри poisson.jl, единственный solve, public four-tuple unchanged, raw scalars из тех же операций; neutral b0 control | Existing throws/rethrow boundaries сохраняются; не обещан durable final после exception |
| R3 | D1 допускал несколько representations и не задавал bounded status/null/equality inventory | §8.3–8.8: один fixed-width UTF-8 record_json≤64KiB + equal commit object; exact keys/types/units/row order/status/tagged-null/old/recovery rules; structural validator ownership | Это format/measurement contract, не scientific pass; unknown context не inferred |

D2 заменяет preferred typed raw table вариантом одного versioned JSON record.
Это deliberate frozen internal format choice до implementation; existing native
numeric metric/history arrays остаются прежними. JSON wrapper Float64/null/tags
одинаков в HDF5/commit; не вводятся vlen metadata allocation, public string-reader,
service endpoint или новый required solver argument. Contracts владеет schema,
Core — измерениями, Runner — binding/serialization, Results — чтением/equality.
Owner SHA не подменяет native↔commit equality.

Tiny controls включают norm0 и norm<<floor для A/K/Σ, nonpositive donor,
negative/nonfinite candidate raw, unavailable+finite0, same-state contradictory
records, legacy absence/recovery и каждый summary candidate fail/missing.
Literal matrix constants и fixture-only rounding bound выведены в §9 из
actual determinants, positive Γ и operation-count bounds. Near-zero bound
отдельный, tighter; device strict thresholds не меняются.

## Fresh source binding

D2 root HEAD c43935567df010d43cab9bcd8d851a9ed976a8d7. Git status прочитан:
Core docs/test overlay и root execution/checkpoint.json; остальные gitlinks match.
Actual Research 8325d228f5219bd1c219a1f9972a76db3c7a8c29 published/G1;
owningdoc45385 bytes/SHA758ac11c19317aba27ee6275d0ce3fdd9f40b639205d89228f4b08405872ad5f.
Core f5b73369a96d1225bd96fb34f5262c8dcf965f86; Runner
2d0190d5573f74d847d92a0dac8dd6ec524d494c; Contracts
26cacbe1688fee0af300d0949fc6b94e55a29f4a; Results
17574ca4c5495f74d86ed9bef51c60dea8265062. Git read-only GIT_OPTIONAL_LOCKS=0.

Повторно проверены hashes:

| Owning path | SHA256 |
| --- | --- |
| C/reference/final_audit.jl | 8384e2022de0c3c912384c15f6e5b3697879dac984d554f38f0d5bc2d916a673 |
| C/reference/validation.jl | 29e1b92daaed51f35d676bab8f70d60836fd0b5dc65c25c38a58646e0395005a |
| C/reference/poisson.jl | 8989ced0c4adc67e5d553b98863cd8ee3584705546ba445565cb5da0e7130645 |
| C/optimized/production_solver.jl | ae776c29b611a84553116d9b25be8e04e2c16b7ff258c5ca5b11e03f555d8eaa |

C aliases здесь — src/numerics/reference или src/numerics/optimized под pinned
Core. Core diff HEAD -- src пуст; production source не редактировался.
Concurrent DEV05 D2 reopened, accepted runtime green нет; его overlay не evidence.

## Выполненные операции и caps

Только text reads, read-only Git, bounded stdlib Fraction/math для четырёх
literal determinant constants и hashlib/difflib/Path для design artifacts.
Не выполнялись Julia/product imports/tests, solver/SCBA/Poisson experiment,
server/native probe, data/archive payload reads, build/install/profile или Git
mutation. Не редактировались component code/docs; Old S01 не затронут.

Новый test call count0; C08 восемь calls/два corrective code rounds общий с
SCI05/08 и не пополняется D2. Scheme64KiB — engineering metadata cap, не grant
на scientific I/O и не physical tolerance. 0mV/70K/all5/e–e none/finite_chain4,
existing strict gates и S1 finite catalog/caps сохранены. Run/plan/state/runtime
admission/BIND остаются null/unknown. Полный numerical/physical/discretization/
experimental acceptance отсутствует.

## STOP и следующий checkpoint

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1–R3 имеют concrete author corrections | D2 §8–9 и immutable diff/hash | Нужен independent exact-delta CP-DESIGN | изменить |
| Production aligned-map reuse сохраняется | Pinned source/hash и D1 independent trace | Source evidence, не runtime green | сохранить |
| Format и tiny measurement ambiguity закрыты автором | Exact v1 inventory/status/equality + fixture constants | Implementation/tests ещё не выполнены | дополнительно измерить |
| SCI05 I/runtime можно начинать по author report | CP-DESIGN ещё pending; admission/plans unknown | Третьего design retry нет; при остаточном load-bearing gap — concrete blocker | данных недостаточно |
