# DEV05 D2 I — frozen narrow source correction

Дата:2026-10-19. **Source-only I correction передана high CP-SOURCE;
functional/runtime GREEN и CP-CODE не заявлены.**

Core identity от координатора:
`f5b73369a96d1225bd96fb34f5262c8dcf965f86`, branch
`codex/review-closure-final-state-oracle`; root identity от координатора
`c439355`. Git автором не выполнялся. Неинтегрированный SI03 CONTRIBUTING
не использовался и Core HEAD не менялся.

## Frozen outputs

Единственный owning path:
`components/QCLNEGF.jl/test/numerics/final_state_alignment_oracle.jl`.
Managed root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.

| Artifact | SHA256 |
| --- | --- |
| New test:44892 bytes/866 lines | `81fbb258f86c1760ed2ffb7964e189518fd1ec7608921e42080c969c4a55f852` |
| `/tmp/qcl-dev05-d2.patch`:incremental D1→D2,20904 bytes | `084980df8be88ed6ef03ee63eeed51973b64145c2ab133bbb26d11a0f5171fce` |
| `/tmp/qcl-dev05-d2-sourceidentity.json` | `e70ecfc571839ad62b8abcfa97401fca47dc8b1bdf195318863f47213b5d1d09` |
| Preserved full D1 `/tmp/qcl-dev05-d1-full.jl` | `6d0db8b15300dce5350bf1bb282cef008da494be57bd96b23780ab1b314049a9` |
| Approved D2 `/tmp/qcl-final-ug-design-v2.md` | `eb9e1a8c39ad08bafa480970392d844c2c9fffdef02d847397ef87c52111bfc9` |
| Narrow D mathdiff | `91959685fd63d02069c74f1c67b9c959e2674ce3914db63e88d1f810a0f7c217` |
| Independent CP-DESIGN D2 | `53c3e9b4061a6cdb42239d6d42f5b3f7a09b94eb36315b1ec22bfea103c4f55f` |

Patch применим только к frozen D1 `6d0db8…`; исходный full added-file D1
patch `/tmp/qcl-dev05-final-state.patch` сохранён. Его нельзя выдавать за
самостоятельный full D2 patch. Новый test можно восстановить исходным full
D1 patch плюс новым D2 delta. Все filenames/identities указаны явно, новый
ручной composition lock не вводится. Sourceidentity — receipt одной проверки.

## Сохранённые failed inputs и граница полномочий

До изменения сохранён полный D1 test. Original D1 author report, patch,
inventory delta, D1/D2 designs/reviews и GREEN-1 raw/receipt не переписаны.
Sourceidentity содержит проверенные SHA восьми protected inputs, включая:
GREEN-1 receipt `557f60ed…`, raw `6918099f…`, current owning passport `d51f984c…`.
Owning docs остаются D1 и не менялись; отдельный ultra writer решает их
обновление. Original dirty checkout, production, models, inputs, tolerance
policy, existing primitive tests и Git остаются untouched.

Фактический GREEN-1 остановился до coupled audit на false exact-wZ1 premise:
46pass/0fail/1error. Это failed D1 precondition, не production defect и не
scientific outcome. Автор прочитал raw и принятые D2/mathdiff/review целиком.
Применены qcl-physics-audit, ранее прочитанные TDD/receiving-code-review;
production code не пишется. Автор не исполнял Julia/parser/import/build/
solver/setup/tests/Git. Remaining1-of2 L-JL call по-прежнему принадлежит root
после независимого source approval:≤120s,1CPU,2GiB,TMP16MiB/log2MiB.
Новых execution попыток или третьего design round не предложено.

## Что изменено по утверждённому mathdiff

Локаторы далее относительно единственного нового owning test.

* `source_unit_literals:223` вычисляет literal RN chain до public builder:
  nm=RN(1/1e9), ell=RN(30nm), L0=RN(10nm), inputLp=ell/L0, h=inputLp/3,
  qL=RN(1/RN(h²)), v=RN(1/RN(sqrt3)). Exact hex guards соответствуют D2;
  h не извлекается из actual grids. Проверяются power-of-two stencil
  multiplications и row sum4qL. Strict guard physical layer/scale canonical
  metre coefficients, dimensions, all actual x/wZ и uniform εr1 расположен
  в `manufactured_problem:121`; false premise не заменена isapprox/fill1.
* `independent_literals:248`: h — exact real binary64 input внутри outward
  384-bit Ball. t0 — исходный transverse coefficient; tZ=t0/h²; H0/τ/c
  используют tZ. U/u=lambda*D*h factors, nideal=Dφ²/h, rounded n_f/U_f
  сохраняются отдельно и становятся exact subsequent inputs. Literal
  M/h² Uideal=lambda(nideal−D/(3h)) и weighted number relations проверяются
  outward. Gauge check сохранён через independent U rounding enclosure;
  rounded sums не объявлены равными ideal sums.
* `analytic_basis_phase:192`: Φ Euclidean unchanged up to phase; χ=φ/sqrt(h),
  Z/centre/spread имеют h; H0/T/window/Egrid имеют tZ. Mminus1/overlap и
  остальные physical/static expectations сохранены с прежними ATOL/RTOL.
* `literal_state:286`, `hamiltonian_budget:344`: оба состояния используют
  h-correct H0/τ/c/u, но **k term остаётся t0*k²**, не tZ. Все causal roots,
  branch/radicand/denominator checks, full fields, physical/Pauli/partner
  identities и condition/scale checks сохранены. ηh/ηΣ по-прежнему выводятся
  из checked actual inputs относительно independent literal expectations.
* `poisson_enclosures:473`: floating operator — independently frozen qL*M;
  n_f — exact rounded published array, S вычисляется outward из этих floats.
  Exact actual-coefficient reference `la/(3qL) P*n_f` заменяет D1 shortcut.
  Uniform donor deviation ограничен D/(3h), λ actual input сравнивается с
  independent lambda. RHS/normalizers/floors не изменены. Three-row residual,
  zero-mean eigenvalue3qL и explicit mean gauge дают forward enclosure с
  retained γ3 formation/γ32 row/norm errors.
* Там же: до tiny call заморожены Q4=[M/4,v1;v1',0], rhs и exact ζ_v.
  Из literal sqrt3*v>.75 доказан inverse2norm4/3. После sole tiny call
  independently expanded R4 даёт `BzForward=(4/3)||R4||2`. **Fatal check
  `upper(BzForward)<=lower(BzShort)` сохраняет прежний γ32 budget**
  `gamma32*(la*D/(qL*h)+abs(ζ_v))`. Comparison использует меньший forward
  enclosure вокруг exact v64 reference; ideal-v reciprocal discrepancy
  вычислен явно, но не поглощён новым коэффициентом. Ни второй solve, ни
  guessed LAPACK forward accuracy не используются. ζ/neutral upper bounds
  и rP enclosure обязаны быть ниже прежних gates. Neutrality учитывает
  absolute weighted h-dot terms, а не relative error near0.
* `independent_checks:560`: public volume density сравнивается отдельно с
  intended Dφ²/h и rounded n_f, с measured actual χ input deviation и
  retained γ32 integration/SI conversion envelope. Canonical L064³/L064²
  используются для volume/sheet conversions; weighted χ normalization и
  h-integrated n_f charge имеют independent error accounting. Ни sheet,
  number, current measure, ни spectral sum дополнительного h не получили.
* `manufactured_solution:650`: history density/U автоматически получают
  h-correct literals; sheet chargeD и same-field SI current сохраняются.
  Comment различает source r_n normalizer D_actual/sqrt(inputLp64) от
  sqrt(3h); нового false exact period/grid-length равенства нет. Истории
  остаются explicitly manufactured sequences, не runtime measurements.

Operation ledger дополнен точными counts нового unit/stencil/v chain и
outward h factors. **Ни γ16/32/64, ни ATOL/RTOL, ни SolverTolerances не
расширены.** Измеренный Q4 residual не может увеличить retained ζ cap.

## Что сохранено побайтно и что проверено только статически

Source-only comparison подтвердило побайтное сохранение:

* literal GATES41/CANDIDATE_GATES3 inventory;
* Ball/CBall outward primitives;
* metric_enclosures и исходных charge/current/full-array norm formulas;
* check_candidate/assert_inventory/check_final с реальными fresh/validate/
  explicit evaluator calls, 38/41 actual-limit inventory assertions,
  finite metric assertions и exact expected failure-name comparisons.

Полные field/no-alias assertions сохранены; изменение derived input arrays
не заменено unrelated zero fields. Optional N3 не добавлен. N1/N2 сохраняют
stored и fresh smallΣ assertions. Exact final failures неизменны:

| Complete input | Expected failed keys |
| --- | --- |
| Healthy U_h*,G_h* | `{r_sum}` |
| N1:2U_h*,retainedG_h* | `{r_D,r_D_candidate,r_U,r_sum}` |
| N2:fixedU_h*,staleG0_h | `{r_D,r_D_candidate,r_sum}` |

Sourceidentity свежо подтверждает 17/17 прежних primary source/test bytes
(исторический passport исключён как заранее изменённый), плюс 11/11 D2
unit-chain primary files. Current owning passport d51 проверен отдельно
как protected, не отождествлён с прежним673bc964. Installed test совпал с
candidate bytes; final newline/trailing whitespace проверены. Diff адресный,
один owning path. Julia syntax/dispatch/platform guard/enclosure outcomes
нового D2 **не измерены**. Root выполняет собственный Git diff/status и
independent CP-SOURCE; автор не заменяет их своей самопроверкой.

Healthy остаётся functional aligned raw-map state с обязательным global
FAIL по coarse-grid r_sum. SCBA iterative convergence, discretization
adequacy и эксперимент не установлены; S1 all-five/e–e-none/0mV70K и SCI04
production/cavity/optimized/serialized-lineage controls приёмки не получили.
Любой новый failed guard/enclosure — concrete blocker, не auto retry/thirdD.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| D2 general-h correction реализована | Strict independent unit chain, tZ/t0, corrected χ/n/ND/U и floating Poisson/Q4 | Новый high CP-SOURCE и final bounded attempt ещё не выполнены | дополнительно измерить |
| Failed D1 и raw сохранены | Full snapshot6d0db8, protected receipts/patch/report/doc hashes | D1 не получает ретроактивного pass | сохранить |
| ζ budget ослаблен | Forward enclosure обязан fit прежний h-correct γ32 cap | Runtime fit not_measured | сохранить |
| Healthy/S1 научно принят | Healthy exact r_sum FAIL; S1 не запускался | Нет adequate discretization/experimental evidence | данных недостаточно |
