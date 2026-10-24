# SCI04 — независимый CP-DESIGN D1

2026-10-19. **Вердикт: BOUNDED_CORRECTIONS.** Source/reuse conclusion принят; SCI05-C1/N1 ещё не READY до исправления R1–R3 ниже и адресного review изменённых bytes. Архитектурного blocker или причины менять физику не найдено. Это один read-only design review, не CP-CODE, не runtime green и не CP-SCI READY.

## Порядок и полномочия

Сначала прочитаны AGENTS, architecture, owning CONTRIBUTING, qcl-physics-audit с physics-checks, science SCI03–06, P1/autonomy; затем независимо восстановлен producer→fresh evaluator→assessment→history→serialization→reader chain. После source trace прочитан exact design, последним — author report. Author diagnosis не использовался для первоначального trace. Других рецензентов не привлекал. Прочитан только небольшой текстовый участок concurrent DEV05 fixture как контекст; fixture не включён в accepted production source/test evidence.

Grant: source/docs only, finite 60 min/1 CPU/2 GiB/output128 KiB; единственный созданный файл — этот отчёт. Не выполнялись Julia, project imports, tests, solver/SCBA/Poisson experiments, server/native probes, installation/build, Git mutations или чтение научных массивов. SHA256 и text reads — обычные read-only операции. Old S01, foreign resources не затронуты. Research runtime model остаётся equilibrium 0 mV/period, lattice/LO70 K, LO/acoustic/impurity/IFR/alloy, electron_electron=none; finite_chain4, grids/basis, strict tolerances, S1 attempts/bytes/admission и native gates не изменены.

## Identity

Root HEAD `9f8b08bbf8b2f941eaa6426bc07c2b436a2a81d8`.
Core `f5b73369a96d1225bd96fb34f5262c8dcf965f86`, Runner `2d0190d5573f74d847d92a0dac8dd6ec524d494c`, Results `17574ca4c5495f74d86ed9bef51c60dea8265062`, Contracts `26cacbe1688fee0af300d0949fc6b94e55a29f4a` совпадают с root gitlinks. Core dirty overlay: docs/src/development/review_oracle_contracts.md и untracked test/numerics/final_state_alignment_oracle.jl; `git diff -- src` пуст. Runner/Results/Contracts status пуст. Core production conclusions относятся к HEAD src, не к fixture overlay.

Actual Research HEAD `8325d228f5219bd1c219a1f9972a76db3c7a8c29` (published/G1 supplied), root gitlink ещё старый; owning equilibrium-measurement-contract SHA совпал с supplied/author exact bytes. Design/author report фиксируют более ранний Research b1a3be2b и untracked doc: это исторический source snapshot, не текущий checkout status. Семантического drift owning measurement doc нет.

Root status также содержит concurrent AiiDA/Platform/Research gitlinks, checkpoint/system docs и evidence/tooling. Actual other commits: AiiDA312ed8a6363103d05a971d14ac9cbcca1c782358 (+), Platform6a5d8048cd17e46d0149f529d03bef666276d5ce (+), Portalff1e25f22eed2cb6f48ba11c1ba0a52495e7f363. Эти изменения не принимались этим review.

Design `/tmp/qcl-sci04-design.md`: 31278 bytes, SHA256 `c4e61ff6a9aac94c349b9e941f35f8652606928a7be7c3a23e22245adbaf49fc`.
Author report `/tmp/qcl-sci04-design-report.md`: 8536 bytes, SHA256 `cf6bc724e2e9b6ea3af6e7e70f8cca61c0cb3f336aac806cb5c6ea9c9e82a824`.
Owning Research doc: 45385 bytes, SHA256 `758ac11c19317aba27ee6275d0ce3fdd9f40b639205d89228f4b08405872ad5f`. Принят только его bounded measurement/pilot смысл; εQ, conditioning, tail/truncation bounds и science runtime READY не установлены.

Run/plan/attempt/state/runtime binding = null, reason=source-only review; нет созданного scientific run или frozen runtime plan.

## Независимая цепочка и reuse

Aliases C=components/QCLNEGF.jl, N=components/QCLNEGFRunner.jl, V=components/qcl-negf-results, K=components/qcl-negf-contracts, R=components/qcl-negf-research.

1. C/src/numerics/optimized/production_solver.jl:1042–1080 замораживает Uaccepted, решает SCBA при нём, затем published_U=copy(Uaccepted). Строки1092–1127 строят density того же GL, raw Poisson map и raw rU/rn перед mixing. Строки1200–1217 отличают следующий Unew от published_U; final_scba=previous_scba, U=published_U, nfinal из final GL. Аналогичная reference publication: reference/solver.jl:147–231. Это положительное source observation о producer, не автоматическая гарантия произвольного публичного NEGFSolution.
2. Production:1266–1287 строит fresh scattering из final_scba.green, затем selected embedding из этого scattering и h(Ufinal), без смешивания/λ fitting. optimized/production_operators.jl:872–902 для finite_chain требует именно local scattering+h. Reference final_audit.jl:1–7 использует shifted-neighbour closure. Их равенство не принимается за oracle finite_chain4.
3. reference/final_audit.jl:38–94: raw stored/candidate N, λ, candidate Dyson/spectral/Keldysh и maximum family/component Σ. validation.jl:33–81 определяет реальные нормы; α не участвует, rK не делится на λ. validation.jl:636–665 повторяет Poisson на solution.n, измеряет final raw rU и max last-history/final density difference. Generic validator не реконструирует solution.n для проверки равенства density(GL): precondition/DEV05 residual сохраняется.
4. validation.jl:549–566 при unavailable audit не сохраняет stale success: rK/rΣ/rλ=Inf. Candidate rD/rA/λ keys могут отсутствовать, поскольку _solution_validation_limits:742–746 включает их условно. final_audit::_final_quality_report требует outer/scba/report success; solution_scientific_assessment:144–251 отделяет iterative/physical/stationary/discretization/scientific, последний false. DomainError допускает сохранение failed aligned state; неожиданный exception rethrow не обещает final artifact.
5. N/persistence/hdf5.jl:478–515 сохраняет state/stored families, :517–608 — current inner/outer history, density/populations и все report.metrics. scientific_history.jl сохраняет отдельно streaming execution history; current SCBAResult history не вся история исполнения. point_artifacts.jl:916–931 передаёт Core stationary_assessment и exact state identity, owner inventory/hash. physics_diagnostics.jl:270–324 stationarity summary действительно не требует candidate rD/rA/λ, хотя full Core report их проверяет при наличии. Это локальный summary gap, а не доказанный bypass scientific acceptance.
6. V/state.py:296–344 сверяет commit/receipt/owner SHA/identity, native.py:174–199 проверяет native4/history contracts; K/artifacts.py проверяет inventory, не физический смысл residuals. equilibrium.py читает stored matrices/context и остаётся stored-only. Это независимое чтение/алгебра, не построение fresh physical map.

Design G1–G4 в этих пределах обоснованы. Нового solver API/service или дублирования научного evaluator не требуется. Existing scalar fresh_candidate_residual.jl проверяет лишь Dyson helper+threshold mapping; SCI05 skip не обоснован. Shared production kernels остаются общим риском даже после будущих literal residual tests.

## Обязательные bounded corrections перед ready I

### R1 — raw Dyson witness не является полной absolute residual norm

**Категория: вывод, medium; locator design:142,183–189; owning Research §5.4:250–260; C/validation.jl:33–43.**

Предложенный record хранит numerator/scale только в блоке, максимизирующем отношение. Из него нельзя восстановить max абсолютного ||DGR−I|| по всем E,k или global Frobenius norm: блок с меньшим ratio может иметь большую абсолютную невязку при большем denominator. Поэтому такой witness сам по себе не закрывает заявленный G1 «measured raw norms» для полной карты. Оговорка про unknown conditioning верна, но не исправляет отсутствие самого global raw measurement.

**Исправление:** оставить ratio-max witness с declared index/tie rule и добавить в том же проходе хотя бы global unweighted sqrt(sum ||DGR−I||F²) и max absolute numerator (с own witness), с dimensionless units/aggregation. Либо явно сузить G1 closure до witness-only и оставить full Dyson absolute norm открытым SCI03 measurement residual. Для ready SCI05 предпочтительно первое: O(1) scalars, без нового map/array/I/O pass. Не называть это forward error bound; D inverse/conditioning остаётся unknown.

**Дешёвый discriminating control:** двухблочная literal fixture, где argmax ratio и argmax absolute numerator различаются. Mutation «global norm = ratio-witness numerator» должна падать; healthy control обязан совпасть с literal sum. Новый scientific threshold не нужен.

### R2 — согласовать Poisson measurement с owning evaluator и allowed paths

**Категория: наблюдение/вывод, medium; locator design:163–168 против195–197; C/poisson.jl:49–64.**

Design требует rP numerator, ||b||, λP floor и signed neutrality из actual map, но owning solve возвращает только U,ζ,rP,abs-normalized neutrality. C1 не разрешает poisson.jl. Восстановление numerator как rP*denominator не является raw measured numerator; переписывание L/b/residual формулы в validation ради record создаёт второй measurement evaluator. Это исправимый scope gap, не новый algorithm design.

**Исправление:** явно разрешить узкую instrumentation правку poisson.jl: internal helper возвращает существующие result+scalar diagnostics из единственного выполненного solve, публичный solve_periodic_poisson сохраняет прежний four-tuple/API и операции. Зафиксировать signed numerator = dot(wZ,ND−n), target = dot(wZ,ND)>0, rP numerator=norm(L*Umap−b), denominator=norm(b)+λP*1e−14, signed ζ. Не менять sign/gauge/face ε/normalization и не выполнять второй solve. Alternative compatible data collector допустим, если это буквально тот же owning evaluator, а не копия формул.

**Control:** literal Nz3 sign/h²/neutrality test уже предложен; добавить neutral b=0 case, где rP denominator=λP*1e−14 и signed neutrality=0. В отчёте source-only review не называть фактический float residual точно нулевым до наблюдения.

### R3 — заморозить portable schema/status semantics и near-zero negative set

**Категория: вывод, medium; locator design:176–205,217–243,267–283.**

Record marker/общие типы/units и rejection goals заданы, но ready cross-component contract ещё оставляет выбор scientific representation: sum-of-squares «либо sqrt», available/unavailable/error без единой state table, numeric NaN/Inf «declared semantics» без конкретного JSON/HDF mapping и fixed required field inventory. Consumer должен отвергать missing/wrong units/status и native/commit mismatch; без такой таблицы несколько независимо реализованных representations удовлетворяют prose и несовместимы между собой. O(channels) также не заменяет concrete per-record byte/row cap для untrusted UTF-8 metadata.

**Исправление до handoff I:** добавить одну нормативную table path/key→dtype/shape→units→aggregation→required/applicability, finite permitted statuses и mapping JSON null ↔ HDF availability/value. Отдельно зафиксировать measured zero, measured nonfinite/error, unavailable reason и old absent=not_recorded; stale final record на recovery запрещён. Unknown context не должен становиться утверждением aligned/finite_chain/none. Commit/native records должны совпадать по canonical semantic fields и state identity; owner SHA не гарантирует их взаимного равенства. Выбрать конкретную scalar aggregation и bounded maximum fields/rows/UTF8 bytes; эти маленькие лимиты — engineering format policy, не новые физические критерии.

**Обязательные tiny controls:** norm=0 и norm<<1e−14 для rA/rK/rΣ сохраняют existing additive-floor formula; donor target≤0 сохраняет error, candidate negative/nonfinite raw N не clipped и не pass; unavailable+finite zero rejected; native/commit same-state contradictory raw values rejected; absent old native4 readable as not_recorded. Healthy measured-zero record читается. Existing weights/transpose/λ/α/attempt/state/schema controls сохранить. Tiny roundoff tolerances заранее вывести для выбранных literal constants/operation count; device strict values не менять.

Таблица может быть частью revised design/owning Contracts doc. Для этих corrections не требуется operator permission или запуск расчёта; после exact-delta review можно назначать I в оставшемся общем cap. До этого medium implementation не должна самостоятельно решать scientific schema/measurement ambiguity.

## Остальные observations и ограничения

- Candidate rD/rA сравниваются с rK=1e−8, не stored linear rD=1e−11; candidate λ с rλ=1e−8. rA/rK/Σ unweighted; N использует gs/(2π)*wE*wk единожды. U native×E0_eV, sheet native/L0². Poisson wZ и h реальные, donor positive, floors не physical accuracy bounds. Design сохраняет эти различия.
- Proposed λ masking (q>1,qf<1), 2×2 complex coherence, nonunit weights, α mutation, Nz3 Poisson sign/h², unavailable audit, summary omission и serialization identity — хорошие различающие controls. Они ещё не исполнялись; literal residual algebra не доказывает независимость production scattering/finite-chain kernels или реального outer publication control flow. Такие claims остаются source-based, даже если tiny tests позднее пройдут.
- DEV05 D2 reopened отдельно. Concurrent fixture/status, старый failed first GREEN и планы D2 не являются current accepted runtime green. Ничего из этого не закрывает SCI04/SCI05 tests; accounting SCI05/08 C08 общий, не новый cap.
- Тест summary должен включать healthy all-required pass, each candidate gate fail, each candidate gate absent и unavailable record. У full Core stationary acceptance остаются strict evaluator/history/scba/outer dependencies; summary сам по себе не acceptance.
- SCI06 raw empty numbers/FDR corrections и represented-current coefficients, SCI12 directional/tail/interaction bounds, SCI03 finite εQ/conditioning остаются отдельными. Нет runtime plan/admission/guards, native receipts или new scientific arrays. Поэтому уровни execution/equations/physical/discretization/external validation все **не установлены этим review**.

## Source byte manifest

Ниже exact читаемые bytes; receipt, не maintained lock. Все manifest hashes source совпали с author report там, где файлы пересекаются; Research doc hash пережил публикацию без изменения.

| Path | Bytes | SHA256 |
| --- | ---: | --- |
| `AGENTS.md` | 13393 | `b795916b286983cc4c71ed3614bc0fb431acfc1d29974594565e71a30e66b648` |
| `docs/architecture.md` | 5501 | `8e49c02d948891f31f6d27360564b4a2708d7a1546808d9f10f38d0c5ebec6b7` |
| `docs/implementation/review-closure-2026-10-19/science.md` | 42428 | `0f52fc7148456b9eeff6bb993b5d1e701825781c58733dc519972c5312b8c26a` |
| `docs/implementation/review-closure-2026-10-19/autonomy.md` | 29026 | `056fb2bcbca56ea7700fa2a4de36b0da9ad7533a44e4e6b0dfcfab94ed76b1bd` |
| `docs/implementation/review-closure-2026-10-19/operator-permissions.md` | 32033 | `4887a5d4ad67a84424225d5b827ba2975ec97e319c94efe59a3e67b9120054a0` |
| `components/qcl-negf-research/docs/equilibrium-measurement-contract.md` | 45385 | `758ac11c19317aba27ee6275d0ce3fdd9f40b639205d89228f4b08405872ad5f` |
| `components/QCLNEGF.jl/src/domain/types.jl` | 36507 | `f428a6c7ce2c7d4796d6be2983decffcdbfc25f21ec400a600038863f673e71b` |
| `components/QCLNEGF.jl/src/numerics/reference/final_audit.jl` | 17312 | `8384e2022de0c3c912384c15f6e5b3697879dac984d554f38f0d5bc2d916a673` |
| `components/QCLNEGF.jl/src/numerics/reference/validation.jl` | 30956 | `29e1b92daaed51f35d676bab8f70d60836fd0b5dc65c25c38a58646e0395005a` |
| `components/QCLNEGF.jl/src/numerics/reference/poisson.jl` | 2385 | `8989ced0c4adc67e5d553b98863cd8ee3584705546ba445565cb5da0e7130645` |
| `components/QCLNEGF.jl/src/numerics/reference/solver.jl` | 10736 | `3a0f68b0a7774bbe363f2aeaef2288b20a5f7b26fa02a1f7a13e5853a5919636` |
| `components/QCLNEGF.jl/src/numerics/reference/acceptance_metadata.jl` | 30629 | `4d1880b7d6e475534d0bbfa229ced25dd40b062f674ec8a2ea86b45e0db1dd86` |
| `components/QCLNEGF.jl/src/numerics/optimized/production_solver.jl` | 52279 | `ae776c29b611a84553116d9b25be8e04e2c16b7ff258c5ca5b11e03f555d8eaa` |
| `components/QCLNEGF.jl/src/numerics/optimized/production_operators.jl` | 50736 | `7b4e6cd55b259a2477b799ecfb30ae818ce17a3bbf5c6ff81d2087af17bb62df` |
| `components/QCLNEGF.jl/src/numerics/optimized/certification.jl` | 5278 | `de2dd971a8d466b53b0b2b4c682e085c743cd789b7e9e0c839f0a9042c5a13e3` |
| `components/QCLNEGF.jl/test/numerics/fresh_candidate_residual.jl` | 1276 | `8ab459b5be0c39f96839b862aad38e1dbcd6a8dc633770838fd239c8a871a6a0` |
| `components/QCLNEGFRunner.jl/src/infrastructure/persistence/hdf5.jl` | 30957 | `c946ba5fb71f035d1a0b564b561700b9a5c3360ed67bf890c668b0ced769d511` |
| `components/QCLNEGFRunner.jl/src/infrastructure/persistence/physics_diagnostics.jl` | 17287 | `9f54466882634797a165e30c156b3e7bd2e64f9156da7a7549ef0c5cda2fc043` |
| `components/QCLNEGFRunner.jl/src/infrastructure/persistence/point_artifacts.jl` | 76808 | `81e3886870643a0a096bcfa8f439a95cce57a4bbce12aca4062675121bbb754a` |
| `components/QCLNEGFRunner.jl/src/infrastructure/persistence/scientific_history.jl` | 12277 | `afecbfb4ad3716af06c0ee0d7fc49563387b69948061a0102f1240e1ab6189a1` |
| `components/QCLNEGFRunner.jl/src/infrastructure/persistence/light_results.jl` | 10363 | `75c418fcc02e1023f951ccca216d60a0fd78e662f2a21fac1a477e609b141f06` |
| `components/qcl-negf-results/src/qcl_negf_results/state.py` | 25269 | `a8e96fc0edcc087aa71126dcbad57bc3ab2acdddbef4630b17c685dcafa7d323` |
| `components/qcl-negf-results/src/qcl_negf_results/native.py` | 10798 | `892d6ba60ea4775cb48de44721d2a68c83ab22cfc288df73af44166acbff104b` |
| `components/qcl-negf-results/src/qcl_negf_results/equilibrium.py` | 31385 | `3f8ee56390741e15bc2c709de67d4b0c80260733c99752d8fbbb4f538e3042e6` |
| `components/qcl-negf-contracts/src/qcl_negf_contracts/artifacts.py` | 13757 | `639ebd85f0a1612d2c036d11d8926f7c4bdd04778d5690a8778eb03e8cb6ccaa` |

## Решение и STOP

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Actual producer возвращает aligned final U/G/n и свежую unmixed selected map | C production_solver1042–1297, validation549–665, exact hashes | Source trace; generic solution.n/candidate precondition | сохранить |
| Ratios/numbers/history/failed scientific status передаются existing owners | N hdf5/point_artifacts, V StateReader, Core assessment | Не raw components/explicit final-map record; summary subset | изменить |
| SCI05 skip обоснован | Existing scalar test не покрывает coupled/status/transport | DEV05 reopened; tests не запускались | дополнительно измерить |
| SCI05 source design готов к medium implementation | Design G1–G4 + bounded R1–R3 | До corrections schema/raw Dyson/Poisson scope не frozen | изменить |
| Физика/strict thresholds могут сохраняться при corrections | Narrow instrumentation + append-only record + literal controls | Shared production kernels остаются общим риском | сохранить |
| Runtime green/scientific acceptance/native gates установлены | Новых measurements/receipts нет | SCI03 bounds, plans, admission, native и SCI06/12 residuals открыты | данных недостаточно |

STOP после этого review. Никакого implementation, tests, нового run или повторного review этим отчётом не активировано.
