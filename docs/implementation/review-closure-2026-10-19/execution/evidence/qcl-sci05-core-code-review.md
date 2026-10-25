# SCI05-C1 v2 — независимый FIRST full CP-CODE/source review

2026-10-19. **Вердикт: REQUEST_CHANGES.** Два P1 source-blocker-а связности модулей и один P2 gap независимого Poisson oracle. Runtime green и scientific acceptance не установлены. Кандидат не изменялся; исправлений в этом review нет.

Применён `qcl-physics-audit`; этап — source audit. Один review, envelope ≤60 min / 1 CPU / 2 GiB / output≤128 KiB. Единственный новый файл — этот отчёт. Julia/imports/tests/solver/benchmark/build/install/native/server calls=0; C08 calls=0. Git commit/push/checkout/index/submodule mutations=0. Использованы только чтение, Git read-only, SHA256 и `git diff --check`; последняя проверка успешна. Никаких archive scripts не исполнялось.

## Неизменяемые входы и фактическая identity

Root: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD `965ebed95d2b627423805d10c46d0ae8dd425e9d`.
Candidate: `/tmp/qcl-sci05-core-worktree`, branch по frozen identity `codex/review-closure-final-audit-evidence`, фактический HEAD `f5b73369a96d1225bd96fb34f5262c8dcf965f86`; submodule status пуст. Фактический status: четыре modified production files ниже, untracked `test/numerics/final_audit_evidence.jl`, иных candidate изменений нет.

| Артефакт | Проверенный SHA256 |
| --- | --- |
| `/tmp/qcl-sci04-design-v2.md` | `d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c` |
| `/tmp/qcl-sci04-design-v2-review.md` | `ae57a5b8986cf2d7f15a58ad13e26aa34927331ed44fcc1c584d1a5c0f27f0d1` |
| `/tmp/qcl-sci04-d2-status-clarification.md` | `a009526d44583f0198531c047b904052b6deb951c6439195b858f22063f690f8` |
| `/tmp/qcl-sci04-d2-status-review.md` | `f5a06df97644ec6d7c576f10ae6fdbbdcdb1187cbef6f4ba3d61cd3aa7f3dab3` |
| `/tmp/qcl-sci05-core-v2.patch` | `0125cecfb023f28d1d8d15fe950eed9852cc21b66f5e090ceebf4ce3209b5080` |
| `/tmp/qcl-sci05-core-v2-identity.json` | `b8f28b72e43adfdc08ae54b15b2445e530b9ff8ead74a9ffef92a6ceed7f1b24` |
| `/tmp/qcl-sci05-core-v2-report.md` | `58ba4f3dcc478fc4a9ae347a9214ef4ac8443169fd226bafdc93cf8065b59b1d` |
| `src/numerics/reference/validation.jl` | `50de158f55ea88b34f61dddd18fb62dd6954eb9c37ab9ac6e1bbe6f9289a338c` |
| `src/numerics/reference/final_audit.jl` | `ac20ca9ded521220224d4e3c0688b0149db0c1b3b9fb264c25b1cabd4367be73` |
| `src/numerics/reference/poisson.jl` | `730777452e3f17c6b55490fb05f190a9d97806d533a13b45666a91e1427e39c5` |
| `src/numerics/optimized/production_solver.jl` | `5d0fa48c016877897f97ccc919e3100fd4ba9fdedcd907166447d2bbc89ad0c2` |
| `test/numerics/final_audit_evidence.jl` | `d9984ead4f1e3de67e0c5b6f0277d5fd5ab105adf131504e97b626173fe2789a` |

Фактический root `git submodule status --recursive`:

```text
+f7b108bef206d2b2dc5afe0306b2dff60d27ac59 components/QCLNEGF.jl
 23860d9e660a3cddf6cb5203d449d1b62f3745a1 components/QCLNEGFRunner.jl
 d8f8092ca1c76523d85384b4bac8198d8bfa736b components/qcl-negf-aiida
 02a564b78dc9c5e19eacf496bc8c891361eafaab components/qcl-negf-contracts
 b067723c82382689bff5cc366981c56e99b926f8 components/qcl-negf-platform
+2622de5ee28b454ff4f809cc3dd00c1e5bc2295d components/qcl-negf-portal
 1eacefcd81a50e245ea9da74a0b717b33818c61e components/qcl-negf-research
 e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae components/qcl-negf-results
```

Root status при старте: modified все четыре QCL skill `SKILL.md`, `agents/openai.yaml`, соответствующие references; modified Core/Portal gitlinks; modified `execution/{checkpoint.json,qcl-targeted-receipt-census.json}`; untracked evidence `{qcl-dev05-d2-code-review,qcl-dev24-auth-report,qcl-sci04-design-v2-report,qcl-sci04-design-v2-review,qcl-si04-checkmatrix,qcl-si04-design-report,qcl-si04-design-review}.md` и `tests/{DEV05-GREEN-2,DEV24-GREEN-2}/` под `docs/implementation/review-closure-2026-10-19/execution/`. Это concurrent root состояние, не часть candidate. Protected Core f7b108b имеет пустой status, пустой `git diff HEAD -- src test` и пустой production `git diff f5b73369... HEAD -- src`: источник review — изолированный candidate, не текущий опубликованный Core. Gitlinks остаются authority; эта таблица — наблюдение review, не новый lock-файл.

Run/attempt/state/plan/runtime binding=null, причина `source-only code review`; научные массивы отсутствуют и для этого вопроса не требуются. Сначала прочитаны root AGENTS/architecture, applicable CONTRIBUTING, physics skill, science SCI03–05 и normative D2/clarification; затем source/diff/tests и module composition. Author report прочитан после самостоятельной requirement/source оценки. Прежние review verdicts приняты как identity нормативных входов, не как доказательство candidate correctness.

## Findings

### F1 / P1 — новый Poisson helper недоступен в модуле final validation

**Наблюдение:** `src/QCLNEGF.jl:267–307` помещает `poisson.jl` в `QCLReferenceOperators`, где новый `_solve_periodic_poisson_with_diagnostics` определён (`poisson.jl:41–81`). `validate_solution` помещён в другой модуль `QCLNumerics` (`QCLNEGF.jl:493,642`) и теперь вызывает этот символ без qualification (`validation.jl:687`). Explicit `import ..QCLReferenceOperators` (`QCLNEGF.jl:578–624`) импортирует только прежний `solve_periodic_poisson`, новый символ отсутствует. Ни один из пяти candidate files не добавляет нужного binding.

**Вывод:** когда validation доходит до Poisson, имя нового helper не разрешается в `QCLNumerics`; ожидаемый runtime outcome — `UndefVarError`, а не прежний report/final artifact. Это относится и к fresh-available, и к `audit_failure` ветке, включая подготовленный public-validation test. Сам public wrapper остаётся в owning module и этого дефекта не устраняет.

**Контраргумент:** Julia допускает forward references функций внутри одного модуля. Здесь функции принадлежат разным sibling modules с explicit imports, поэтому аргумент неприменим. Automatic import новых private names отсутствует.

**Нарушенный контракт:** D2 §8.2, SCI05-C1 п.2–3: owning helper должен обслуживать final validation одним existing solve с сохранением outcome/API. **Решение: изменить.** Самый дешёвый distinguishing check после author correction — source/module binding check, затем уже разрешённый bounded targeted check в существующей среде; здесь он не запускался. Scope correction остаётся у координатора/author.

### F2 / P1 — новый regression source обращается к отсутствующим root bindings

**Наблюдение:** `test/numerics/final_audit_evidence.jl:3` задаёт `BN=QCLNEGF`; первый новый вызов — `BN._dyson_residual_evidence` на строке21. Новые evidence/record helpers определены в `QCLNumerics`; root `import .QCLNumerics` (`src/QCLNEGF.jl:735–...`) сохраняет explicit старый список, в том числе `_dyson_residual` на810, и не импортирует новые `_dyson_residual_evidence`, `_spectral_residual_evidence`, `_keldysh_residual_evidence`, `_selfenergy_residual_evidence`, `_audit_witness_record`, `_audit_norm_record`, `_final_fixed_point_record`. Новый Poisson helper принадлежит `QCLReferenceOperators` и также не импортирован в root. Полный `rg` этих новых имён подтверждает определения только в owning files и calls в новом тесте/validation.

**Вывод:** существующий aggregator действительно auto-discovers новый `.jl` (`test/run_group.jl:7–16`), но первое evidence assertion до численной проверки не дойдёт: ожидаемая ошибка — отсутствующий binding в `QCLNEGF`. Ни independent literal oracle, ни per-field overflow mutations пока не являются исполнимой regression graph на выбранном source. Это отдельный дефект от F1: исправление production import в `QCLNumerics` само по себе root test namespace не исправит.

**Контраргумент:** прежние tests используют root private aliases. Для старых helpers они явно импортированы; новые aliases не возникают автоматически. **Решение: изменить.** Дешёвое разрешение — author обеспечивает корректные owning namespaces/bindings, сохраняя public API и allowed scope; затем bounded targeted test. Review не требует публиковать новые public exports и не запускает runtime.

### F3 / P2 — Poisson oracle не проверяет raw residual/gauge/rU независимо

**Наблюдение:** D2 §7/8.2 требует literal L/b, bordered residual/neutrality, raw rU/ζ и controls sign/h²/mixed update/altered density. Новый test на184–214 проверяет analytic U только широким условием `1/2 < up[i]/expected[i] < 2` (193); sign/h² «mutants» на194–195 меняют expected denominator, а не observed product path. `residual_ratio == residual_numerator_F/denominator == rp` (201) — внутренняя согласованность трёх полей одного helper, без независимого literal numerator/RHS. `zeta_signed==zeta` (202) также сравнивает два выхода одного solve. Нет gauge assertion, независимого residual numerator/ζ или actual final raw rU control. В record fixture `r_U=0` просто задан в synthetic metrics (236), а record equality проверяет транспорт этой константы (394–396).

**Вывод:** подготовленный Poisson control не закрывает этот заявленный D2 oracle contract. Например, source mutant `Uᴴ *= 1.1` после bordered solve с обычным последующим вычислением diagnostics сохраняет все показанные factor-two/sign/h²/neutrality assertions; nonzero residual увеличится, но его independent oracle/limit отсутствует. Neutral U=0 останется0. Отдельный mutant совместно умножающих p_num и rP также сохраняет assertion201. Следовательно, tautological raw-field equality не различает эти errors. Это аналитический контрпример к assertion coverage, не выполненная mutation run.

**Контраргумент:** sign/h² и neutral-zero controls полезны и есть в source; они покрывают часть требований, но не raw residual, gauge и raw-vs-mixed rU. Broad factor-two bound не является обоснованным roundoff bound для точного manufactured U. **Решение: изменить.** Нужны только frozen independent literal quantities/обоснованный fixture bound и actual observed mutations, без второго production solver/oracle helper и без изменения физических thresholds. Если frozen D2 не даёт требуемый bound, это конкретный вопрос координатору, не автономный redesign.

## Requirement → source → evidence disposition

| Требование / утверждение | Source evidence на замороженном candidate | Ограничение / disposition |
| --- | --- | --- |
| Existing Float64 residual APIs, Dict metric keys/formulas сохранены | `validation.jl:33–128`; `final_audit.jl:38–98`; diff к f5 | Формулы/старые scalar quotient/max/floors сохранены source-only; новые helper allocations scalar-sized. Runtime equivalence не измерена |
| Dyson distinct global/max/ratio aggregates, independent maxima, first-invalid/ties | `validation.jl:36–73`; new test17–46 | Sum a², max a, max ratio независимы; `(e,k)` e-outer/k-inner, first invalid overrides both witness, first healthy zero=(1,1). Tests блокированы F2 |
| Approved finite ratio0 / normalization overflow mapping | `final_audit.jl:461–480,599–604`; new test243–365 | Actual finite quotient сохраняется; error reason без forged tag; actual D_F/denominator tagged, finite absolutes measured. Per-field predicate и payload mutants проверяют каждый ratio, finite absolutes/Inf fields; healthy companion есть. Runtime phenotype не наблюдён |
| Spectral/Keldysh unweighted norms, additive floor, no λ division | `validation.jl:79–110`; test48–70,116–170 | Source соответствует D2; literal inverse2/scalar matmul/Frobenius/weighted number graph не вызывает tested reducers для expected quantities; measured runtime отсутствует |
| Σ rows canonical actual enabled + embedding total/plus/minus ×R/L/G | `final_audit.jl:64–77,525,606–627`; validation113–128 | Ровно `3*(enabled+3)`, first canonical winner ties; total map не складывает plus/minus повторно; rΣ старый max и raw differences без α сохранены |
| Signed/nonfinite raw charge, optional actual history | `final_audit.jl:527–585`; tests399–418,459–486 | Candidate negative measured; candidate nonfinite tagged, dependent λ undefined; target/stored invalid statuses существуют, public existing ArgumentError unchanged. Actual end/end−1 ν и end μ, а не ν−1. Existing raw invalid exception может не дать final artifact согласно D2 |
| Candidate unavailable явно выдаёт все fresh gates/rows | `validation.jl:594–622`; final_audit535–554,592–652; tests432–455 | Все required fresh fields unavailable/null, никаких guessed zeros; stored unmeasured charge честно unavailable, Poisson сохраняется; original failed report metrics/boundary catch source не ослаблены. Но runtime final path сломан F1 |
| Один owning Poisson solve/public four-tuple, no copied L/b formulas | `poisson.jl:41–89`; validation687–692 | Арифметика и sign/gauge unchanged; helper instrumentation same-pass; public overloads four-tuple. Integration blocker F1, independent oracle gap F3 |
| Actual production selectors/alignment, generic unknown | `production_solver.jl:1213–1248`; final_audit481–523 | Marker поставлен после frozen published_U/final_scba и density reconstruction только на actual final return path; context берёт actual restart algorithms/problem scales/model, не AlgorithmOptions defaults. Generic solution без producer context остаётся unknown; production kernels shared=true и independent=false |
| Append-only internal template/assessment transport | final_audit246–251,411–415,644–652; validation731–733 | Полный internal numerical inventory без `state_identity`; это намеренно НЕ schema-valid portable record до Runner binding шести actual fields. No format/native/commit/Results acceptance claim |
| Existing DomainError/rethrow boundary сохранён | production_solver1267–1296; diff production только два context keys | Candidate build один; existing catch only DomainError/unexpected rethrow unchanged; durability после unrecoverable exception не обещается |
| Independent oracle regression исполнима | test file, aggregator, module composition | **Опровергнуто source-only F2**; Poisson coverage F3. Existing resonant scalar test сохранён, но production map kernels остаются общим риском, не independent physics oracle |

## Научные границы и STOP

Итерационная сходимость неизвестна; физические gates неизвестны; достаточность discretization неизвестна; валидация экспериментом неизвестна. Этот patch занимается measurement instrumentation, не выведением forward-error bound. Нет нового измеренного nonlinear contraction, conditioning или full-device uncertainty bound. Tiny manufactured algebra не является thermal Fermi solution, моделью прибора или scientific run. Production shared map не доказывает независимость физики.

Два source blockers достаточны для отказа CP-CODE. Author report корректно не заявляет runtime green, но его утверждение о подготовленной regression graph ограничено F2/F3. Нужны конкретные исправления в уже согласованной координации и отдельная проверка candidate identity; review сам не начинает дополнительный corrective round, не расходует C08 и не расширяет allowed files/budget. STOP после этого отчёта.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| CP-CODE/source candidate готов | F1/F2 точные module/symbol locators | Runtime не запускался; source graph уже недостаточен | изменить |
| Poisson oracle contract закрыт | F3: test184–214 и synthetic rU | Нет независимого raw residual/gauge/rU oracle | изменить |
| Frozen equations/ratios/strict limits не ослаблены | Четыре production diff к f5, unchanged DomainError/rethrow | Только source reading, integration defects остаются | сохранить |
| D2 overflow status трактовка отражена в source | Same-pass fields и per-field literal/mutant test source | Tests не исполнены из-за namespace blocker | сохранить |
| Runtime и full scientific acceptance достигнуты | Такого evidence нет; C08 calls0 | Все numerical/native/science gates открыты | данных недостаточно |
