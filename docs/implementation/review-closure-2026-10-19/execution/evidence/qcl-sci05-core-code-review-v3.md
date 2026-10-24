# SCI05-C1 v3 — CPP2 / independent full CP-SOURCE review

2026-10-19. **Вердикт: APPROVE CP-SOURCE, eligible для первого отдельного bounded C08 check на exact source.** F1–F3 предыдущего review закрыты на уровне исходников. Новых load-bearing source findings в шести разрешённых файлах не обнаружено. Это не runtime GREEN, не полный code/runtime acceptance и не scientific acceptance. Первый C08 ещё не выполнен.

Это второй полный CPP/source round. Применён ранее прочитанный `qcl-physics-audit`; граница — исходники, нормативные документы и их hashes. Envelope≤45 min / 1 CPU / 2 GiB / output≤128 KiB, один review. Единственный новый файл — этот отчёт. Candidate, root, main Core, DEV05 и original v2/R1 не изменялись. Julia/imports/tests/solver/benchmark/build/install/native/server calls=0; C08 calls=0. Git mutations=0. Проверки: read-only Git/source/namespace/diff/hash review и успешный `git diff --check`. Третьего corrective/review cycle этот отчёт не начинает.

## Identity и входы

Candidate `/tmp/qcl-sci05-core-worktree`, фактический HEAD `f5b73369a96d1225bd96fb34f5262c8dcf965f86`, branch из frozen identity `codex/review-closure-final-audit-evidence`; recursive submodule status пуст. Фактический status: modified `src/QCLNEGF.jl`, четыре numerics src ниже и untracked новый `test/numerics/final_audit_evidence.jl`. Tracked существующие tests не изменены. Patch содержит ровно эти шесть путей.

Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, фактический HEAD `965ebed95d2b627423805d10c46d0ae8dd425e9d`. Protected Core HEAD `f7b108bef206d2b2dc5afe0306b2dff60d27ac59`, status пуст; `git diff HEAD -- src test` пуст; `git diff f5b73369... HEAD -- src` пуст. Protected DEV05 `test/numerics/final_state_alignment_oracle.jl` SHA256 `81fbb258f86c1760ed2ffb7964e189518fd1ec7608921e42080c969c4a55f852`.

Root status по-прежнему содержит concurrent modified QCL skills (SKILL.md/agents/references), Core/Portal gitlinks, execution checkpoint/census и прежние untracked evidence/tests DEV05-GREEN-2/DEV24-GREEN-2. Дополнительно при этом review modified `docs/single-server-deployment.md`; он не входит в SCI05 candidate/review. Root не чистый, его unrelated overlay не подменяет source кандидата.

Фактические gitlinks/submodule revisions: Core `+f7b108bef206d2b2dc5afe0306b2dff60d27ac59`; Runner `23860d9e660a3cddf6cb5203d449d1b62f3745a1`; AiiDA `d8f8092ca1c76523d85384b4bac8198d8bfa736b`; Contracts `02a564b78dc9c5e19eacf496bc8c891361eafaab`; Platform `b067723c82382689bff5cc366981c56e99b926f8`; Portal `+2622de5ee28b454ff4f809cc3dd00c1e5bc2295d`; Research `1eacefcd81a50e245ea9da74a0b717b33818c61e`; Results `e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae`. Это наблюдение review, не новый lock-файл. Submodules не обновлялись.

| Проверенный вход / файл | SHA256 |
| --- | --- |
| v3 patch `/tmp/qcl-sci05-core-v3.patch` (66818 B) | `305675ad283267034a3b3873d1cfb8ff010f7d5a7b7885c523f388e3483ac71e` |
| v3 identity `/tmp/qcl-sci05-core-v3-identity.json` | `a76ec63745bd73b972a74f3e90bba496240bdad81429c57d716c7a063e40ca3b` |
| v3 author report `/tmp/qcl-sci05-core-v3-report.md` | `f918786d386b9e4110916121ad86e32e820fba07462cee74437c0e2e8b172891` |
| D2 `/tmp/qcl-sci04-design-v2.md` | `d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c` |
| D2 independent review | `ae57a5b8986cf2d7f15a58ad13e26aa34927331ed44fcc1c584d1a5c0f27f0d1` |
| D2 status clarification | `a009526d44583f0198531c047b904052b6deb951c6439195b858f22063f690f8` |
| Status independent review | `f5a06df97644ec6d7c576f10ae6fdbbdcdb1187cbef6f4ba3d61cd3aa7f3dab3` |
| Accepted O08-03 `/tmp/qcl-final-ug-design-v2.md` | `eb9e1a8c39ad08bafa480970392d844c2c9fffdef02d847397ef87c52111bfc9` |
| O08-03 independent D2 review | `53c3e9b4061a6cdb42239d6d42f5b3f7a09b94eb36315b1ec22bfea103c4f55f` |
| `/tmp/qcl-dev02-accepted-technical-body.md` | `ca3c12e84ee41bee3f13d1e1294c030197d0f35adca0f2ef61ebb9cd92b1707b` |
| Original CPP1 review | `43d3aaad003e9c9afa42af1f0f144d3e9976e5e9f482c8199629f7972bb6c146` |
| `src/QCLNEGF.jl` | `cec01e69f58466511102138f01d7f2ab26624b22c3d0af77e825a0b8c51481f2` |
| `src/numerics/reference/validation.jl` | `50de158f55ea88b34f61dddd18fb62dd6954eb9c37ab9ac6e1bbe6f9289a338c` |
| `src/numerics/reference/final_audit.jl` | `ac20ca9ded521220224d4e3c0688b0149db0c1b3b9fb264c25b1cabd4367be73` |
| `src/numerics/reference/poisson.jl` | `730777452e3f17c6b55490fb05f190a9d97806d533a13b45666a91e1427e39c5` |
| `src/numerics/optimized/production_solver.jl` | `5d0fa48c016877897f97ccc919e3100fd4ba9fdedcd907166447d2bbc89ad0c2` |
| `test/numerics/final_audit_evidence.jl` (38516 B) | `6a2e954230c119a92e11e70c5bc8d31376fc06e209faa907429b9f6ee13455b5` |

Четыре numerics src SHA совпадают с независимо проверенным v2. Новое production изменение относительно v2 — одна private import строка, отдельно разрешённая координатором в `src/QCLNEGF.jl`; exports/public required arguments/types/API не меняются. Это расширение permitted path явно учтено, не скрыто в test correction.

Original v2 patch/report/identity и R1 review и copies `/tmp/qcl-sci05-preserved-CPP1-*` сверены: соответственно `0125cecfb023f28d1d8d15fe950eed9852cc21b66f5e090ceebf4ce3209b5080`, `58ba4f3dcc478fc4a9ae347a9214ef4ac8443169fd226bafdc93cf8065b59b1d`, `b8f28b72e43adfdc08ae54b15b2445e530b9ff8ead74a9ffef92a6ceed7f1b24`, `43d3aaad003e9c9afa42af1f0f144d3e9976e5e9f482c8199629f7972bb6c146`. Они не заменены новым verdict.

Прочитан v3 diff/source, явные module imports/calls, весь новый Poisson graph, retained overflow/schema controls; сопоставлены SCI03–05/D2 и O08-03 §5. Author report прочитан после независимой оценки исправлений. Run/attempt/state/frozen-plan/runtime binding=null с причиной `source-only review`; придуманные execution identity не используются.

## F1 и F2: namespace closure

**F1 закрыт source-only.** `src/QCLNEGF.jl:594` добавляет `_solve_periodic_poisson_with_diagnostics` именно в `QCLNumerics` import из sibling `QCLReferenceOperators`. Определение остаётся в owning `poisson.jl:41–81`; вызов `validate_solution` в `validation.jl:687` теперь имеет binding в собственном модуле. Include order Poisson до validation сохранён. Public wrappers `poisson.jl:83–89` сохраняют четыре позиционных результата. Private import не меняет формулу, число solve внутри final validation или catch boundary.

**F2 закрыт source-only.** Test3–5 содержит `BN=QCLNEGF`, `QN=QCLNEGF.QCLNumerics`, `QR=QCLNEGF.QCLReferenceOperators`. Все новые residual/evidence/record helpers вызываются через QN; private Poisson helper — через QR. В BN оставлены только старые явно импортированные root `_dyson_residual` и `_solution_validation_limits`. Root bindings sibling modules уже существуют вследствие module declarations; private exports не нужны. Старый auto-discovery `test/run_group.jl` подхватывает новый `.jl`. Это устраняет конкретные missing-symbol graph defects CPP1, но не доказывает успешный import/runtime теста.

## F3: независимый Poisson oracle

**F3 закрыт source-only.** Широкая factor-two positive band удалена. Новый graph test187–291 реализует accepted O08-03 D2 §5 для homogeneous Nz3 stencil и не получает expected L/b/numerator через product matrix builder, norm или solve.

1. `literal_poisson_reference:221–243` до product solve фиксирует actual rounded Float64 input coefficients, uniform h/ε/ND guards и independently formed `q64=ε/(h*h)`. Для используемых ε=1 и4 harmonic face exact, diagonal factor2/row absolute-sum4q контролируются. Literal `M=3I−11ᵀ`, `b=λ(n−ND)`, `Uexact=λ/(3q)*(n−mean(n))`, `zeta_exact=sum(b)/(12q*v64)` соответствуют исходному sign/gauge. No product reducer supplies these expectations.
2. В Q4 upper-left `M/4`, off-diagonal `v64=0x1.279a74590331dp-1`, rhs `b/(4q)`. У Q4 два eigenvalues3/4 и два ±√3*v64; guard √3*v64>3/4 даёт exact inverse2norm4/3. Returned floats входят только в независимый четырёхстрочный residual и его outward norm, без второго solve. Эта алгебра применима и к ε4/h2 fixture: q масштабируется, Q4 остаётся тем же.
3. `literal_poisson_enclosure:246–269` отдельно разворачивает q*M*Up−b и zero-mean projection. Bound использует eigenvalue3q, измеренный gauge mean, retained γ3 b-formation и γ32 row/norm error. Raw numerator, RHS norm, denominator и quotient получают самостоятельные outward intervals; numerator не восстанавливается через ratio. Возле нуля применены absolute cancellation bounds, не division by zero residual.
4. `literal_poisson_matches:278` требует **оба** measured forward bounds≤нижняя граница прежнего `γ32*(λ*donorSheet/(q*h)+abs(zeta_exact))`. Поэтому *1.1/gauge/wrong-density результат не может расширить residual-dependent allowance до собственного pass. Это существенная защита от контрпримера F3. Далее analytic U, gauge и ζ сравниваются с независимыми enclosures; raw numerator/RHS/ratio/neutrality проверяются отдельными membership tests282–290. Дополнительных full-device tolerance или guessed LAPACK constants нет.
5. Test294–332 использует тот же healthy predicate для реальных observed-output mutants: sign, /4 missing-h² analogue, *1.1, constant gauge shift и altered-density product output. Neutral branch проверяет literal zero/floor. Nonneutral branch имеет ненулевой unbordered residual (uniform RHS component проецируется border-ом) и отдельно мутирует numerator, ratio, оба совместно: это делает factor2 error различимым вне zero cancellation budget.
6. Public validation test606–680 не ограничивается synthetic r_U=0: actual nonconstant positive density и published U заданы до calls; source-chain h/q hex guards634–640 сохранены из принятого O08-03. Independent reference заморожен перед tiny direct Poisson measurement; его rawU enclosure включает forward/subtraction error. `validate_solution` затем независимо измеряет r_U и переносит его в record; обе величины проверяются658–663. Mixed α=1/8 update и новая public validation с changed density должны выйти из того же rawU interval664–670.

Bounds и mutations здесь **прочитаны, не выполнены**. Интервальная реализация BigFloat/PBall, точный h guard, source λ/ND coefficients, tiny LAPACK output и факт прохождения всех positive/negative assertions остаются задачей первого bounded runtime receipt. Ни γ32, ни constants нельзя расширить при первом failure; сохранение original failed evidence и remaining aggregate limits обязательно.

## Полный retained SCI05-C1 контракт

| Требование → source | Независимая source оценка v3 | Ограничение |
| --- | --- | --- |
| Existing metric values/API/arithmetic/strict limits: validation33–128, final_audit38–98, poisson41–89 | Wrapper Float64 ratios, Dict keys, additive floors, quotient/max order, public Poisson four-tuple сохранены; четырём numerics src соответствует прежний SHA | Bitwise/runtime equivalence не измерена |
| Dyson global/max/ratio witnesses: validation36–73 | В одном проходе sqrt(sum a²), max a, max ratio; maxima выбираются отдельно, e-outer/k-inner first tie, first-invalid coordinates; нет новых E×k arrays/map | Overflow phenotype ещё не выполнен |
| D2 finite-zero overflow status: final_audit461–480,599–604; test364–486 | Finite old quotient value0 сохраняется, error/nonfinite_measurement без forged tag; actual Inf normalization tagged-null; finite independent raw absolutes measured. Predicate читает каждый M и mutations, healthy zero companion retained | Original numeric evaluator ratio остаётся0; metadata correction сама не доказывает scientific failure/pass |
| A/K/Σ raw norms: validation79–128; final_audit64–77,606–627 | Unweighted Frobenius norms/additive1e−14; candidate K без λ division; raw Σ без α; actual enabled canonical rows + embedding_total/plus/minus ×R/L/G, fixed3*(enabled+3), first winner | Production map kernels общие с solver |
| Charge/history: final_audit527–585; test489–601 | Signed negative candidate raw measured; nonfinite candidate tagged, λ/constraint invalid-prerequisite; target/stored invalid values explicit; actual end/end−1 ν и μ, optional empty/one-row history retained | Existing raw-charge ArgumentError может прервать caller без final artifact по принятому D2 |
| Availability: validation594–622; final_audit592–652; test551–574 | Все fresh-dependent M/rows explicitly unavailable/null; old failure outcome не ослаблен, необследованные stored charge не выданы measured0 | Runtime unavailable final пока не получен |
| Same-pass Poisson instrumentation: poisson41–89, validation687–692 | Один existing solve в production validation; raw numerator/RHS/ζ/target/neutrality сохранены внутри owning helper; validation добавляет raw rU | Tests явно содержат дополнительные tiny direct calls; это test-only, не extra production solve |
| Context/alignment: production_solver1213–1248, final_audit481–523 | Actual final_return после frozen published_U/final_scba/density reconstruction получает producer_aligned/shared=true; generic context unknown; selectors из actual restart/problem, не defaults | Нет независимой reconstruction proof произвольного supplied state |
| Internal template/assessment transport: final_audit246–251,411–415,644–652 | Append-only in-memory record без invented six-field state_identity; assessment переносит его; units/row/status inventory сохранены | **Portable schema-valid record ещё отсутствует до Runner binding/validation/serialization** |
| Exception and science boundary: production_solver1267–1296 | DomainError catch/unexpected rethrow unchanged; candidate map не дублируется; failure durability не обещана | No new runtime/physics/discretization/experiment evidence |

Матрица literal inverse2/complex off-diagonal/adjoint/nonunit number weights и near-zero additive-floor controls сохранена с owning QN calls (test19–173); expected numbers не вызывают tested residual/number/solve reducers. Это независимый manufactured algebra oracle для указанных функций, а не физический oracle production kernels. Согласие reference/optimized shared map не трактуется как отдельное доказательство.

## Следующий gate и STOP

Exact v3 source eligible для **первого** coordinator-owned C08 в уже разрешённом finite aggregate envelope. Этот verdict не разрешает install, environment bootstrap, full suites/CI, новые solver attempts, mutation main/DEV05 или дополнительный corrective round. Перед call координатор связывает фактический source/runtime с этим hash и считает общий оставшийся cap; source approval само не расходует и не пополняет grant. Source/runtime failure сохраняется целиком и не запускает silent third cycle.

Итерационная сходимость неизвестна; физические gates неизвестны; discretization accuracy неизвестна; экспериментальная валидация неизвестна. Science/state/run/attempt не созданы этим review. У author report нет runtime GREEN claim, и этот отчёт его также не добавляет.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1/F2 namespace defects закрыты | One private import594, owning QN/QR aliases/calls | Source graph; runtime import ещё не выполнен | сохранить |
| F3 independent Poisson residual/gauge/rU graph подготовлен по accepted bounds | Literal M/q/b/Q4, inverse4/3, retained γ3/γ32 cap, observed mutants и actual validation rU | Positive/mutant predicates пока не исполнялись | дополнительно измерить |
| v3 CP-SOURCE eligible для первого bounded C08 | Exact six-file/hash review; новых load-bearing findings нет | Только exact source и existing finite grant, не runtime approval | сохранить |
| Physics/API/strict limits/original evidence сохранены | Четыре прежних numerics SHA, private-only module diff, originals/copies SHA | Current root имеет unrelated overlay | сохранить |
| Runtime/scientific acceptance получена | C08/Julia/tests/solver calls0 | Все numerical/native/science gates остаются открыты | данных недостаточно |

STOP после отчёта. Исходники и original CPP1 report не изменялись.
