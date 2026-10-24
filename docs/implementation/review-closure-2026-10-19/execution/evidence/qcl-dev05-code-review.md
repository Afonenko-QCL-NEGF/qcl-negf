# DEV05 — независимый source review перед bounded GREEN

Дата 2026-10-19. Reviewer high, source-first, read-only.

**CP-SOURCE: текущий frozen test требует одной узкой inventory correction;
первый bounded GREEN — только после её delta approval.**
**CP-CODE/runtime acceptance: pending, не установлен.**

Разрешённый предмет следующего измерения — complete manufactured final U/G
functional oracle, без SCBA/outer loops. Это не global scientific pass;
healthy global failed-key set обязан остаться `{r_sum}`. Условия L-JL:
один initial invocation ≤120s/1CPU/2GiB, TMP≤16MiB/logs≤2MiB; прежний общий
max2 не увеличивается. Сам reviewer Julia/import/Git/solver не запускал.
Проверка JLv5 launcher этим отчётом не дублируется; его отдельный receipt
остаётся отдельным основанием execution containment.

## Frozen inputs

Core base identity из задания:
`f5b73369a96d1225bd96fb34f5262c8dcf965f86`, branch
`codex/review-closure-final-state-oracle`; Git здесь не измерялся.
Managed root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.

| Artifact | SHA256 |
| --- | --- |
| `test/numerics/final_state_alignment_oracle.jl` | `975323f833f5f96be7f5888410bbb3246a1a748065be0fdd384c63a9cae24af9` |
| `/tmp/qcl-dev05-final-state.patch` | `0d69271f80c21edbf761931cf31e87469bb7c47d9899446c581aa20fa08970b9` |
| Approved D | `96c2c50a104b984c72603fa7066986d9bf6c02a8e59ba1ce0df9f06e321da162` |
| Independent CP-DESIGN | `11900d840a7155ac3a28161f4d0f5f16ac5e3cdb810e37e18c4fc9a5e834c52b` |
| Author report, read after new source | `e48b8f0e7e1d2cd597b223b82b6bd4948051cf4fce0756a460c5096a884379f1` |

Все hashes пересчитаны; совпали 18/18 primary Core file SHA из D/author
receipts. Added-file patch восстанавливает новый test побайтно и содержит
один owning path. 736 строк; завершающий newline присутствует, trailing
whitespace0. Это не Git diff/status проверка и не Julia parser receipt.

## Проверка реализации против D

Полный файл прочитан до author report, затем сопоставлен с принятыми D и
реальными types/final_audit/validation/Poisson/embedding/observables API.
Дополнительно прочитаны constants.jl/scaling.jl: независимые SI literals
совпадают с объявленными числовыми входами source conversions; expected
side не обращается к CODATA/_Cbar/_scaled_physics.

* `manufactured_problem`, `analytic_basis_phase` используют checked public
  builder, accepted :none/Nz3/Nb1 carrier и заранее approved donor D=1/64.
  Production constructors, channels, tolerances и S1 не меняются. Literal
  grid/profile/basis/shift/kernel/model assertions присутствуют.
* `independent_literals`, `literal_state` задают ненулевой L3/φ²/U/n и все
  шесть Green/Σ blocks через causal quadratic. Branch inventory фиксирован;
  radicand/denominator guards выполняются до sqrt/division. Пять нулевых
  spectral/lesser/greater blocks следуют из спектральной поддержки, при
  ненулевых real GR/ΣR. Pauli, partner, family sum, condition/scale checks
  присутствуют; target Dyson/SCBA не строит ожидаемые roots.
* Ball/CBall реализуют направленные 384-bit scalar операции. Фактический
  Float64 g — отдельный exact input с независимо ограниченным polynomial
  defect. Metric enclosures собираются до target fresh/final вызовов.
  Hamiltonian errors ограничены independently checked input fields;
  candidate expected TGT† построен из plain T на actual input side с
  отдельным gamma16 product budget. γ32/γ64 применяются только к коротким
  six-entry scalar paths. Positive denominator guards присутствуют.
* Poisson expected L3/b/U/zeta/neutrality фиксируется до tiny map call;
  actual Up имеет independent backward/forward enclosure через zero-mean
  eigenvalue3 и measured gauge. Exact unit wZ и uniform positive donor
  profile — fatal preconditions, проверяемые до этого вывода; отсутствует
  unbudgeted замена stencil из approximate spatial weight. Если платформа
  нарушит такой precondition, invocation должен завершиться failure, а
  не правкой gate или empirical tolerance.
* Физические density/sheet/population/number checks используют независимые
  меры и target D. `manufactured_solution` создаёт complete typed records,
  копии state/families/variant/history arrays. No-alias assertions охватывают
  Green, self-energy, candidate, variants и outer density/population arrays.
* SCBA ν1…4 / outer μ1…3 — явно manufactured constant algebraic sequence,
  с initial predecessor Inf/NaN и повторёнными same-field J/populations.
  History residuals — declared arithmetic upper bounds/exact identities,
  не вымышленные измерения solver run. Empty mixer/restart/optional payloads
  объяснены. Empty scattering reconstruction aggregate0 не называется
  Hilbert error measurement. Status solution остаётся manufactured и
  converged=false.
* Near-zero current не заменён unrelated history J=0: public same-field SI
  value повторяется и проверяется независимым absolute cancellation bound.
  Разные scaled-current и temporal SI floors сохранены. Power/edge/empty
  mechanism zeros имеют объяснение выбранным bias/support/model пределом.
* `check_candidate` действительно вызывает `_reference_audit_candidate`
  для каждого полного state и сравнивает actual arrays с независимым
  scalar coefficient RHS; `check_final` вызывает реальные
  `fresh_fixed_point_metrics`, `validate_solution` и explicit
  `_validate_solution_metrics(...;accept_approximate_scba=false)`.
  Нет словаря fake pass metrics и нет скалярного primitive вместо assembly.

GATES содержит ровно41 уникальный literal key: все38 current base limits
и три candidate keys. Проверено независимо source extraction. Каждый key
проверяется на actual report presence/finiteness; fresh subset сопоставлен
с actual validate_solution metrics, quantitative equations — с замороженными
outward enclosures. Exact final message failure sets обязательны:

| Input | Expected failed-key set |
| --- | --- |
| healthy | `{r_sum}` |
| wrong U | `{r_D,r_D_candidate,r_U,r_sum}` |
| stale G at fixed final U | `{r_D,r_D_candidate,r_sum}` |

Stored last rΣ и actual fresh rΣ одновременно должны пройти unchanged limit
у N1/N2. Positive/negative separation, rU и r_sum подтверждаются до final
вызовов. Supplemental metric-copy substitutions не подаются evaluator;
они проверяют невозможность satisfy bad-state enclosures старыми healthy
значениями. Optional N3 не реализован, что допустимо принятому minimum D.
Existing narrow-pole/causal SCBA primitives не переименованы complete test.

## Findings и ограничения

**Один адресный source finding: actual gate-limit key inventory ещё не
сопоставлен с frozen GATES. По решению координатора это обязательная
коррекция перед первым bounded invocation. Иных source blockers не найдено.**
Runtime, Julia syntax/dispatch, platform rounding/enclosure outcomes ещё
не проверены; PASS в этом отчёте означает source eligibility, а не зелёный
тест. Failed precondition/enclosure не разрешает автоматический retry или
ослабление physical gates. Сохранить исходные failed receipt/logs, если
они появятся, и вернуть exact failure на review.

**Обязательная узкая коррекция покрытия, locator test:27–39,620–626.** Комментарий
про «required final gate dropped» шире фактического generic покрытия:
`assert_inventory` проверяет presence/finiteness metrics, но не сравнивает
literal GATES с key set `_solution_validation_limits`. Удаление limit
currently-passing gate, например r_PSD, при сохранении вычисления самой
metric не изменило бы текущие expected failure sets. U/G gates удаление
ловится N1/N2, missing metric — inventory. Текущий production source
содержит все41 gates и не изменён. Координатор выбрал test-only коррекцию
до первого GREEN: сравнить actual limits key sets с independently frozen
GATES, не генерируя expected inventory из target. До этого шага не заявлять
generic mutation coverage всех41 gate-limit removals.

Безопасные exact assertions на existing API (no model/threshold mutation):

```julia
# Once in the testset; empty metrics select the 38 unconditional base gates.
const CANDIDATE_GATES = (:r_D_candidate, :r_A_candidate, :r_lambda_candidate)
base_expected = setdiff(Set(GATES), Set(CANDIDATE_GATES))
base_actual = QCLNEGF._solution_validation_limits(
    SolverOptions().tolerances, Dict{Symbol,Float64}())
@test length(base_expected) == 38
@test Set(keys(base_actual)) == base_expected

# In check_final after the real validate_solution report exists, for each
# variant; off-channel report has exactly the 38 base plus 3 candidate gates.
actual_limits = QCLNEGF._solution_validation_limits(
    solution.options.tolerances, report.metrics)
@test Set(keys(actual_limits)) == Set(GATES)
```

`CANDIDATE_GATES` следует объявить на module scope либо использовать literal
tuple локально без const; Julia const внутри function не вводить. Expected
base set зависит только от frozen literals41/3, не от target. Empty dict
здесь — аргумент query limit inventory, не synthetic metrics для acceptance.
Actual final metrics/failure assertions и все enclosures сохранить. Такой
added assertion не требует нового D round; нужен новый file/patch freeze и
короткий независимый delta review, до него runtime не выполнять.

Healthy raw-map alignment не означает adequate spectrum: обязательный
r_sum FAIL сохранён. Iterative convergence/SCBA execution не измерены,
discretization adequacy отвергается этим coarse spectral fixture,
experimental validation отсутствует. S1 0mV/70K/all-five/e–e-none,
production/cavity/optimized independence, serialized lineage и SCI04
оставшиеся dispositions приёмки не получают.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Frozen DEV05 соответствует bounded complete assembly D | Full source review, actual API calls, fields/literals/enclosures/negative variants | Julia runtime pending | сохранить |
| Первый bounded GREEN source-eligible | Осталась narrow inventory correction, согласованная координатором | После нового freeze и reviewer delta approval; общий L-JL max2 не увеличен | изменить |
| Любое удаление любого gate-limit гарантированно ловится | Presence41 проверяется, exact failure sets покрывают designated negative gates | Passing-limit deletion generic coverage отсутствует | изменить |
| Healthy можно назвать global PASS | Exact expected `{r_sum}` FAIL | Сpectral quadrature непригодна для solution verification | изменить |
| CP-CODE и scientific acceptance завершены | Runtime receipt отсутствует | Source-only review, S1 не запускался | данных недостаточно |
