# SCI04 D2 — независимый последний CP-DESIGN

2026-10-19. **Вердикт: APPROVE для bounded SCI05 implementation contract.** R1–R3 из D1 закрыты exact D2. Новых load-bearing замечаний не найдено. Это design approval для instrumentation/format/oracle работы в принятом C08 scope, не CP-CODE, runtime green, numerical/scientific acceptance или CP-SCI READY.

## Scope и identity

Один review, конечный envelope45min/1CPU/2GiB/output128KiB; sole new output — этот файл. Применён qcl-physics-audit. D1 evidence/diagnosis/review сохранены. Прочитаны exact D2 и diff, сопоставлены R1–R3, актуальные AGENTS/CONTRIBUTING и owning source. Author report прочитан после оценки D2; его выводы не заменяли проверку.

Выполнялись read-only Git/text/hash operations и bounded literal арифметика в tool orchestration для четырёх2×2 matrices и Bmatrix. Не выполнялись project imports, Julia, tests, solver/SCBA/Poisson experiments, Git mutations, сервер/native probes, installation/build/profile, научные payload reads или implementation. Бюджет scientific/test calls не расходован. OldS01 и foreign resources не затронуты. Никакой third design round не назначен.

Actual root HEAD при review: `965ebed95d2b627423805d10c46d0ae8dd425e9d`. Source snapshot D2 `c43935567df010d43cab9bcd8d851a9ed976a8d7` остаётся историческим; review не переписывает D2 bytes. Root status: Core dirty docs/test overlay и execution/checkpoint.json. Core `src/` diff пуст.

| Component | Actual selected HEAD | Значение для review |
| --- | --- | --- |
| Core | f5b73369a96d1225bd96fb34f5262c8dcf965f86 | Прежний production source; concurrent DEV05 overlay не runtime evidence |
| Runner | 23860d9e660a3cddf6cb5203d449d1b62f3745a1 | С D1 2d0190d изменён только CONTRIBUTING.md |
| Contracts | 02a564b78dc9c5e19eacf496bc8c891361eafaab | С D1 26cacbe1 изменён только CONTRIBUTING.md |
| Results | e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae | С D1 17574ca4 изменён только CONTRIBUTING.md |
| Research | 1eacefcd81a50e245ea9da74a0b717b33818c61e | С published8325d228 изменён только CONTRIBUTING.md; measurement doc неизменен |
| AiiDA | d8f8092ca1c76523d85384b4bac8198d8bfa736b | Вне scientific measurement implementation этого review |
| Platform | b067723c82382689bff5cc366981c56e99b926f8 | Вне этого source/design verdict |
| Portal | d28d076c83611278153752d94cc3729d91b32667 | Вне этого source/design verdict |

Все фактические component HEAD совпадают с текущими root gitlinks. Contributor changes и AGENTS routing прочитаны; source-only граница, finite grants, independent review и разделение evidence уровней сохраняются.

| Frozen input | Bytes | SHA256 |
| --- | ---: | --- |
| /tmp/qcl-sci04-design-v2.md | 61527 | d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c |
| /tmp/qcl-sci04-design-v2.diff | 40400 | 3283019ddd99a7f1941d96f5a59e4ed2e4c6233f1441287038f723ca359c9c4b |
| /tmp/qcl-sci04-design-v2-report.md | 7438 | 21aec4cf299b0bc5eec58f3b90791a64cc6e8d102f65fb6e3308aa1ca6e43b7c |
| D1 independent review | 22773 | 98c37f812b7a19aa9fc02714ef2b8dd092c6a79fbe064c7727060eb10e6a4a66 |
| Research/docs/equilibrium-measurement-contract.md | 45385 | 758ac11c19317aba27ee6275d0ce3fdd9f40b639205d89228f4b08405872ad5f |

Run/attempt/state/plan/runtime binding и fresh scientific admission здесь null с причиной `source-only design review`. Контекст DEV05 D2 design53c3e9/sourcebb5b526 и GREEN2 running получен от координатора; accepted GREEN receipt не предоставлен и данным review не установлен.

## R1 — полная absolute Dyson norm и независимые witnesses

**Решение: закрыто.** D2:192–201,312–329,487–501,589,597–604.

Теперь один pass измеряет три различные quantities: max block ratio, sqrt(sum block numerator²), max absolute block numerator. Ratio witness и absolute witness выбираются независимо, с one-based координатами и first lexicographic tie. Нулевой healthy defect имеет определённый witness(1,1); nonfinite не пропускаются. Добавляются O(1) scalars, full E×k residual arrays/map/I/O pass не вводятся.

Literal counterexample Nb1, GR=(1,1), D=(−1,10) корректен: absolute numerators(2,9), denominators(2,11), ratios(1,9/11), global norm√85. Ratio winner(1,1) и absolute winner(2,1) различаются. Подмена global norm numerator-ом ratio winner2 действительно различима. Исходная проблема D1 witness-only больше не остаётся скрытой.

Нормы dimensionless/unweighted; raw diagnostics не называются forward error. Bound ||D⁻¹||, nonlinear q/inverse-Jacobian и finite observable εQ остаются unknown. Это согласовано с owning Research §5.4 и Core validation.jl:33–43. Threshold rD_candidate остаётся existing rK, а не linear stored rD.

## R2 — единственный owning Poisson solve с прежним API

**Решение: закрыто.** D2:173–178,206–211,331–359,495,592.

Allowed path включает reference/poisson.jl. Новый private helper возвращает solution four-tuple плюс diagnostics из тех же target/signed_charge/L/b/bordered solve/norm операций. Public overloads сохраняют positional arguments и прежний four-tuple; final validation вызывает helper один раз. В validation/Runner/Results формулы L/b не копируются. p_num не восстанавливается как ratio×denominator. rU остаётся у caller с Ufinal.

Текущий source poisson.jl:49–64 действительно содержит нужные scalar operations; instrumentation не требует изменения sign, face harmonic ε, unweighted gauge, sP, λP floor, matrix solve или арифметики acceptance. Signed ζ/neutrality и положительный target различены. Invalid target/error semantics не заменяют существующий public exception/arithmetic contract и не обещают durable artifact при неожиданном исключении.

Neutral n=ND control математически имеет b=0, signed charge0, p_den=λP*Float64(1e−14). D2 явно не объявляет наблюдённые Float64 zeros. Non-neutral Nz3/sign/h²/actual weights controls сохранены. Это instrumentation owning evaluator, не новый Poisson method или второй scientific evaluator.

## R3 — versioned portable record, statuses, identity, near-zero

**Решение: закрыто.** D2:231–260,361–579,590–595.

Выбран один payload: fixed-width UTF-8 scalar record_json в `/diagnostics/final_fixed_point_audit`, marker v1, ≤65536 bytes. Vlen/object/external/filtered representation исключены. Есть bounded depth/member/row/text limits, exact keys/types/units/aggregation inventory и additionalProperties=false. Второй typed raw table не создаётся. Existing metric/history datasets и native4 requirements остаются прежними.

Measure M всегда содержит status/value/nonfinite/reason. Measured0 сохраняется как finite value0; unavailable не допускает value0. Nonfinite только error+tag+null; finite invalid domain сохраняет signed value с reason; optional history has explicit no-previous/not-applicable semantics. Record measured/partial_error/unavailable зависит от выполненного candidate и required measurement status, не от scientific pass. Unknown model/context/alignment не превращаются в inferred default. Negative finite candidate N остаётся signed measured; λ/abs(λ−1) оценивает existing Core gate без clipping.

Полный family inventory фиксирован: canonical enabled channels плюс embedding_total/plus/minus, внутри R/L/G, ровно3*(channels+3) rows. Ratios/absolute norm aggregations/formulas и mapping existing report fields заданы явно. GS/(2π), wE/wk и normalized/raw distinctions сохраняются; embedding_total не складывается повторно с plus/minus. Charge и Poisson target scalars имеют отдельные происхождения.

Runner связывает record со state_identity execution/point/attempt/plan/state_id/state_sequence и переносит тот же semantic object в commit assessment. Обе копии проверяются по bounded format и реальной native/commit identity; equality сравнивает все semantic fields, floats по exact parsed IEEE64, с round-trip serialization и canonical zero. Common owner SHA не заменяет equality. One-sided presence/contradictory values/status/context — corrupt record. Legacy absent+absent остаётся not_recorded; recovery не наследует final group/key и даёт not_applicable/not_a_final_state. Optional analysis copy ссылается на canonical physics.full, не притворяется full array owner.

Новые negative controls покрывают zero и norm≪floor для A/K/Σ, additive-vs-max floor, target≤0, negative/nonfinite candidate N, unavailable+finite0, native/commit contradiction, malformed/oversized/vlen/duplicate-key record, stale recovery и каждый candidate summary fail/missing. Healthy measured-zero и legacy absence controls сохранены. Format validator принадлежит Contracts, measurement equations — Core, binding — Runner, independent bounded reading — Results. Новый final_audit.py — pure format helper, не registry/service/scientific gate.

## Oracle arithmetic и предел design evidence

D2 §9 constants проверены независимо bounded literal complex arithmetic, без продукта/Julia/тестов. Для E outer/k inner determinants равны:

| E,k | det(EI−h+iΓ/2) | ||D||F | ||D⁻¹||F |
| --- | --- | ---: | ---: |
| −1/2,1 | 65/256−23i/64 | ≈1.042083 | ≈2.368256 |
| −1/2,2 | 7/16−7i/16 | ≈1.185854 | ≈1.916630 |
| 3/4,1 | 65/256+27i/64 | ≈1.042083 | ≈2.116382 |
| 3/4,2 | 1/8+11i/32 | ≈0.883883 | ≈2.416488 |

Это согласуется с frozen |det|>1/3, ||D||F<5/4, ||GR||F<5/2; Γ Gershgorin lower bound3/8 положителен. Bmatrix=2^24γ4096≈7.62939453125347e−6, заявленное <7.63e−6 верно. Near-zero tight scalar bound отделён от этого conservative fixture-only budget. All-zero и power-of-two helper controls не превращаются в требование zero-number full physical solution.

Для implementation обязательны frozen literal helper graph, controlled operation order, actual mutation assertions и unchanged strict gate checks. Bmatrix не заменяет strict device tolerance и не разрешает weakened acceptance. Spec operation-count/conditioning allowance — design bound для выбранной tiny pipeline; если реальный implementation graph выходит за этот контракт, нельзя молча расширять tolerance. Это конкретный code-review blocker, а не автоматический design/test retry.

Full-matrix fixture прямо помечен manufactured algebra, f(E,k) не объявлен thermal FD solution. Reference closure не подменяет selected finite_chain4 map. Даже будущий pass residual/algebra tests не докажет независимость shared production scattering/embedding kernels или реального outer publication path: source trace и независимые analytic assertions остаются разными evidence.

## Production chain и неизменяемые ограничения

D1 independent trace переиспользуется по совпавшим production hashes: production_solver1042–1080/1211–1297 возвращает final_scba с published_U, nfinal из того же GL, fresh scattering и selected embedding с h(U); validation549–566/636–665 заново измеряет candidate/Poisson и failed-audit outcome. Generic externally supplied solution.n/candidate сохраняет declared producer/reconstruction precondition; record не делает её автоматически доказанной.

Runner transport existing metric_values/history/commit assessment сохраняется; summary candidate rD/rA/λ completeness получает targeted fix. Full Core evaluator остаётся acceptance authority. Unavailable/error state не подменяется process0. Unexpected exceptions не получают нового обещания final output.

Не изменяются equilibrium0mV/70K, all5 LO/acoustic/impurity/IFR/alloy, electron_electron=none, finite_chain4, сетки/базис, strict thresholds, S1 finite attempt/byte caps, protected S01/foreign state, native gates и CI-once. Engineering64KiB record cap не создаёт дополнительного I/O grant. Общий C08 SCI05/08 ≤8 calls/2 corrective code rounds сохраняется; coordinator обязан учитывать фактический remaining budget и DEV05 отдельно. Данный review не запускал и не принимал GREEN2.

SCI03 finite εQ/nonlinear conditioning/tail/truncation bounds, SCI06 corrections/current coefficients, SCI12 directional/mapping/interaction evidence, runtime frozen plans/source/admission/guards/native receipts остаются отдельными requirements. Все scientific уровни execution/equations/physical/discretization/external validation этим source/design review **не установлены**.

## Source hash recheck

Пути относительно selected owning component. Это review receipt, не parallel revision lock. Полный D1 manifest сохранён; пересекающиеся production files ниже совпали byte-for-byte.

| Path | SHA256 |
| --- | --- |
| Core/src/numerics/reference/final_audit.jl | 8384e2022de0c3c912384c15f6e5b3697879dac984d554f38f0d5bc2d916a673 |
| Core/src/numerics/reference/validation.jl | 29e1b92daaed51f35d676bab8f70d60836fd0b5dc65c25c38a58646e0395005a |
| Core/src/numerics/reference/poisson.jl | 8989ced0c4adc67e5d553b98863cd8ee3584705546ba445565cb5da0e7130645 |
| Core/src/numerics/reference/acceptance_metadata.jl | 4d1880b7d6e475534d0bbfa229ced25dd40b062f674ec8a2ea86b45e0db1dd86 |
| Core/src/numerics/optimized/production_solver.jl | ae776c29b611a84553116d9b25be8e04e2c16b7ff258c5ca5b11e03f555d8eaa |
| Core/src/numerics/optimized/production_operators.jl | 7b4e6cd55b259a2477b799ecfb30ae818ce17a3bbf5c6ff81d2087af17bb62df |
| Runner/src/infrastructure/persistence/point_artifacts.jl | 81e3886870643a0a096bcfa8f439a95cce57a4bbce12aca4062675121bbb754a |
| Runner/src/infrastructure/persistence/physics_diagnostics.jl | 9f54466882634797a165e30c156b3e7bd2e64f9156da7a7549ef0c5cda2fc043 |
| Runner/src/infrastructure/persistence/hdf5.jl | c946ba5fb71f035d1a0b564b561700b9a5c3360ed67bf890c668b0ced769d511 |
| Runner/src/infrastructure/persistence/light_results.jl | 75c418fcc02e1023f951ccca216d60a0fd78e662f2a21fac1a477e609b141f06 |
| Results/src/qcl_negf_results/native.py | 892d6ba60ea4775cb48de44721d2a68c83ab22cfc288df73af44166acbff104b |
| Results/src/qcl_negf_results/state.py | a8e96fc0edcc087aa71126dcbad57bc3ab2acdddbef4630b17c685dcafa7d323 |
| Contracts/src/qcl_negf_contracts/artifacts.py | 639ebd85f0a1612d2c036d11d8926f7c4bdd04778d5690a8778eb03e8cb6ccaa |
| Root/AGENTS.md | ef2ef40fe24e1f83758a59497526017955df377827004fb39bd0d39ca90d9330 |
| Root/docs/architecture.md | 8e49c02d948891f31f6d27360564b4a2708d7a1546808d9f10f38d0c5ebec6b7 |
| Root/handoff/science.md | 0f52fc7148456b9eeff6bb993b5d1e701825781c58733dc519972c5312b8c26a |
| Root/handoff/autonomy.md | 056fb2bcbca56ea7700fa2a4de36b0da9ad7533a44e4e6b0dfcfab94ed76b1bd |
| Root/handoff/operator-permissions.md | 4887a5d4ad67a84424225d5b827ba2975ec97e319c94efe59a3e67b9120054a0 |

## Итог и STOP

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 full absolute Dyson diagnostics/witness contract закрыт | D2§8.1/8.6/9, literal√85 counterexample | Нужен actual implementation/test; conditioning unknown | сохранить |
| R2 owning same-pass Poisson instrumentation совместима | D2§8.2, current source49–64, preserved public four-tuple | Code/API regression ещё не исполнялся | сохранить |
| R3 portable record/status/equality/near-zero contract frozen | D2§8.3–8.8/9 | Schema/writer/reader code и mutations ещё впереди | сохранить |
| SCI05 bounded medium implementation design READY | Exact D2/hash, R1–R3 closure и fixed owning paths/oracle matrix | Coordinator binds remaining budget/source; CP-CODE обязателен | изменить |
| Runtime GREEN DEV05/SCI05 либо physical acceptance установлен | Такого receipt в review нет | SCI03/06/12, runtime/native gates остаются открыты | данных недостаточно |

STOP после отчёта. Третьего design round, implementation или нового запуска этот reviewer не начинает.
