# Независимый CP-DESIGN — DEV02 O08-03 → DEV05

Дата: 2026-10-19. Reviewer: отдельный high reviewer, source-first.

**Вердикт: CP-DESIGN PASS для полного manufactured функционального
контракта final U/G alignment. DEV05 READY к ограниченной реализации
этого контракта. Это не CP-CODE, runtime pass или scientific acceptance.**

Принят именно complete aligned discrete raw fixed point с ненулевым
пространственным Hartree U, полным six-node Green/Σ state, actual fresh
same-G bulk-feedback candidate и честным global report FAIL по известной
spectral quadrature. Обязательного all-gates global PASS первичный DEV05
контракт не содержит. Ни одного production gate этот вывод не отменяет.

## Проверенные входы и граница независимости

Managed root:
`/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
Immutable Core identity из поручения:
`f5b73369a96d1225bd96fb34f5262c8dcf965f86`.
Git не выполнялся согласно read-only reviewer scope; фактический root Git
status/rev/gitlinks здесь заново не измерялись. Immutable identity проверена
по 18/18 файловым SHA256 из reading receipt: все совпали с доступными bytes.
Это receipt одной проверки, не новый composition lock.

* Design `/tmp/qcl-final-ug-design.md` SHA256:
  `96c2c50a104b984c72603fa7066986d9bf6c02a8e59ba1ce0df9f06e321da162`.
* Author report `/tmp/qcl-final-ug-design-report.md` SHA256:
  `f29c32b7cd4c3dd5a089089cc80abb3a0eaa383bdb0f485655afa77e6d8e8a25`.
* Core passport SHA256:
  `673bc9641318b01ffe29bcbe6edc6198b5e243a0d246af8072a2190a70e072f2`.
* `final_audit.jl` SHA256:
  `8384e2022de0c3c912384c15f6e5b3697879dac984d554f38f0d5bc2d916a673`.
* `validation.jl` SHA256:
  `29e1b92daaed51f35d676bab8f70d60836fd0b5dc65c25c38a58646e0395005a`.

Последовательность: AGENTS/architecture и qcl-physics-audit с physics-checks;
первичный DEV02/DEV05 контракт, O08-03 и фактические final seams, builders,
Poisson/embedding/observables/types; затем авторский report. Design был
проверяемым первичным proposed artifact, авторский report не служил oracle.
Дополнительно независимо пересчитаны bounded scalar expressions Python
standard library: quadratic support/roots, Pauli margin, Poisson projection,
wrong-U/stale-G residuals и cancellation bounds. Julia/import/build/solver,
project edits, benchmark, server и публикация не выполнялись. Новых внешних
формул не использовано: алгебра выведена для буквальных source operators.

## Соответствие первичному контракту и source

`docs/implementation/review-closure-2026-10-19/development.md:289–316`
требует complete manufactured input с independent literal Dyson/Poisson
relation и designated fresh residual/gate failure при wrong-U/stale-G,
включая retained small stored Σ residual. Там нет требования, чтобы все
физические/дискретизационные gates healthy fixture прошли глобально.
O08-03 owning passport:408–449 требует prescribed applicable gates,
explicit manufactured applicability и independent candidate RHS; отдельно
уточняет, что все пять channels не обязаны быть ненулевыми в этом fixture.

Поэтому accepted healthy scope — согласованный coupled raw map, где
fresh/alignment/charge/Poisson gates проходят, а global failed-key set равен
`{r_sum}`. Это не ослабление r_sum: его величина и FAIL проверяются явно.
Трёхточечная спектральная квадратура непригодна для solution verification;
такой отрицательный факт обязателен в fixture. Положительное имя healthy
должно сопровождаться этим функциональным scope.

На Core f5b73369 проверены реальные пути:

* `reference/final_audit.jl:38–112`: h проектируется с переданным U, stored
  и candidate families участвуют раздельно, raw Keldysh number измеряется
  до нормировки, candidate λ учитывается отдельно; rΣ включает total/+/-.
* `reference/validation.jl:516–685`: `validate_solution` заменяет stored
  equation metrics свежими, вычисляет остальные physical gates и отдельно
  решает Poisson из published n, сравнивая Up с published U. Наличие полного
  solution/history здесь существенно и покрывается предложенным тестом.
* `validation.jl:688–783`: 38 base gates плюс candidate D/A/λ; candidate D
  limit равен rK, stored D limit rD; acceptance требует scba.converged.
* `reference/basis.jl:14–84,288–318`: checked :none carrier дает заявленную
  rank-one basis и h=H0+Φ†diag(U)Φ+kinetic term. `build_problem` с static
  validation сохранён; unchecked problem/grid/basis substitute не разрешён.
* `reference/periodicity.jl:109–163`: actual map именно T(WG)T†; при zero
  bias W=I и rank one он равен |T|²G. Это legacy bulk feedback, не cavity.
* `reference/poisson.jl:11–76`: для uniform εr=1, Δx=1, Nz=3 source L
  совпадает с literal L3; row scale4, bordered unit vector1/√3 и gauge
  согласованы с отдельными формулами ζ и U в design.
* `reference/kernels.jl:620–650`: all-channels-off map — empty dictionary,
  empty aggregate roundoff0. Это не Hilbert error measurement.
* `src/domain/types.jl:684,777,935,978,1022,1048,1084`: полный inventory
  problem/Green/inner-history/SCBA/candidate/outer-history/solution полей
  согласован с proposed assembly; provisional report не подменяет metric API.

Educational и production final source возвращают published_U и final Green,
строят final n из него и передают actual fresh candidate. Это source-positive
trace (`reference/solver.jl:226–248`, `optimized/production_solver.jl:1211–1217,
1252–1297`), не новый runtime/serialization результат.

## Независимая алгебра и различающие controls

При φ²=(1/4,1/2,1/4), D=1/64, n=Dφ², ND=D/3:
`L3 U=lambda*(n-ND)` для `U=lambda*D/36*(-1,2,-1)` и sum(U)=0;
`φ†Uφ=lambda*D/72=u>0`. Ненулевая пространственная Poisson задача
действительно связана с опубликованным scalar Hamiltonian через basis,
а не через unrelated sentinel fields.

Для c=t²/8 и всех шести E/k узлов causal quadratic root решает
`c*g²-z*g+1=0`. Единственный interior-band узел обоих состояний — e2,k1.
В нём c|g|²=1, поэтому G<=iB и G>=-i(A-B) вместе с Σ=cG удовлетворяют
raw Keldysh/spectral relations. В остальных пяти узлах действительный g
имеет нулевые A/lesser/greater, но ненулевые GR/ΣR остаются в Dyson
assertions. Эти нули выведены из поддержки причинного спектра.

Независимая мера дает N=gs/(2π)*wE2*wk1*B=D при B=16π²D.
Это raw и candidate число без fitted normalization; reconstructed n=Dφ².
Физический donor target1e16/64 m^-2 — явно отдельный manufactured input,
не правка S1 и не post-failure настройка. Pauli inequalities имеют большой
запас: B/A=.06573769394630923 (healthy), .04428429710722202 (stale).

Независимый scalar пересчёт воспроизводит:

| Величина | Healthy / N1 | Stale G / N2 |
| --- | --- | --- |
| active A | 37.5340379643918 | 55.717291713995564 |
| fresh wrong-U / stale-G rD | .08946567245753168 | .09013587908346123 |
| общая нижняя separation bound | .08897096039189235 | .08897096039189235 |
| r_sum | 4.9737276762318166 | 7.867682391975496 |
| flux cancellation bound | 7.376526486582284e-20 | 1.1201508432126118e-19 |
| derived rJ bound | 1.4753052973164568e-7 | 2.2403016864252238e-7 |

`Umax=.015707576544902624` в E0. Это гарантирует N1 rU failure при
default1e-7. N2 сохраняет healthy final U и n, потому Poisson rU проходит,
но fresh Dyson не проходит. Stored и fresh rΣ остаются small: bias0
same-G map не зависит от U, что делает distinction содержательным.
Σ-only acceptance эти controls действительно опровергают.

Optional N3 real retarded shift сохраняет family sums/Keldysh partner
identity, stored state и charge, но меняет supplied candidate Dyson/rΣ.
Полные массивные denominators в предложенной формуле rΣ соответствуют
source. N3 покрывает supplied-candidate substitution, не заменяет narrow
pole primitive и не обязан быть частью минимального DEV05.

Required exact final failed sets подтверждены source/algebra:

| Input | Exact expected failed-key set |
| --- | --- |
| Aligned U*,G* | `{r_sum}` |
| N1:2U*,G* | `{r_D,r_D_candidate,r_U,r_sum}` |
| N2:U*,G0 | `{r_D,r_D_candidate,r_sum}` |
| Optional N3 | `{r_Σ,r_D_candidate,r_sum}` |

Все остальные gates имеют основание из того же состояния: positivity и
partner identities, empty-channel conservation, zero bias power, support
away from energy/k edges, identical manufactured histories. Их нельзя
вставлять словарём нулей вместо вызова final API.

## Арифметика, floors и обязательства реализации

Design сохраняет исходные tolerances и source norms, включая unweighted
block-max Dyson, full-array Frobenius A/K/Σ, nonzero Poisson RHS denominator,
absolute E0 rU и два разных current floors. N1/N2 separation margins на
много порядков превышают unchanged gates.

Принят предложенный путь доказательства machine comparison bounds:
outward scalar enclosures; независимый high-precision polynomial defect
для фактического Float64 g; ηh/ηΣ из independently checked builder fields;
γ16 для коротких scalar complex triple products, γ32 для six-entry
norm/charge accumulation и γ64 для scalar Dyson metric assembly. Здесь нет
переноса этих потолков на большие BLAS/FFT. Denominator/radicand positivity
guards и comparison ledger обязательны до утверждений о runtime pass.
Poisson tiny solve дополнительно проверяет собственный backward residual;
forward bound следует из eigenvalue3 на zero-mean подпространстве, плюс
явно проверенный mean/gauge, а не из guessed solver accuracy.

Near-zero current обработан правильно: независимая величина равна нулю
с cancellation bound, но actual SI current из тех же полей повторяется в
history. При conversion roundoff это предотвращает ложный temporal
rJchange≈1 от unrelated zero history. Для scalar support один ненулевой
узел также делает forward/reverse accumulation roundoff точно одинаковым;
power/Im-current здесь имеют объяснённый zero/empty-set предел.

Это CP-DESIGN, поэтому реализация ещё должна материализовать и проверить:

1. Один literal inventory из 38 base и трёх candidate gate keys, не
   извлекаемый динамически из production limits; every required metric
   конечен, присутствует, сравнен и имеет exact failure-name assertion.
2. Полный field inventory, no-alias copies, valid static builder, fresh
   actual candidate versus literal TGT†, independent density/number,
   explicit histories с first-predecessor Inf/NaN и достаточной cardinality.
3. Конкретный operation ledger/outward rounding и runtime comparison
   enclosures; нельзя заменять их fitted rtol или расширять physical limits.
4. Реальные вызовы direct fresh metrics, `validate_solution` и explicit
   `_validate_solution_metrics`; exact failures должны исключать masking
   известным r_sum failure. Original failed outputs сохраняются.

Невыполненное обязательство блокирует соответствующий CP-CODE/runtime
вывод. Оно не даёт разрешения design/solve retry loop. Не найдено unknown
source prefactor/operator, требующего остановить текущий bounded design.

## Readiness и ограничения

DEV05 READY только для owning test file
`test/numerics/final_state_alignment_oracle.jl`, proposed testset
`Final state U G alignment`, complete manufactured raw-map scope выше.
Existing shared L-JL budget не увеличивается: ≤2 invocations суммарно,
≤120s/1CPU/2GiB каждый, aggregate4min, no solver loops/model/tolerance edit.
Текущая проверка ни одного L-JL invocation не использовала.

Iteration convergence здесь — algebraic manufactured state, не выполненный
SCBA/outer process. Physical gates — source/algebra expectations до runtime;
global spectral gate доказанно FAIL. Discretization adequacy — не
установлена и spectral quadrature специально неадекватна. Experimental
validation — отсутствует. S1 0mV/70K/all-five/e–e-none не изменён и никакой
приёмки не получает. Cavity embedding, production optimized common kernels,
five-channel raw map, serialized lineage, audit-error/process0 и alpha-step
controls остаются отдельными SCI04 dispositions.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Complete independent functional final U/G design пригоден | Literal L3/φ²/causal roots, actual TGT†, полные final API records и source seams | CP-DESIGN, rank1/channels-off/bias0 legacy map | сохранить |
| Wrong U/stale G различимы при stored и fresh small Σ | Full-interface N1/N2, rD lower bound>.08897 и distinct rU | Runtime не измерен | дополнительно измерить |
| Healthy имеет global PASS | Независимый r_sum=4.9737276762318166>1e-3 | Global FAIL обязателен | изменить |
| DEV05 готов к bounded implementation | Первичный DEV05 требует designated gates, complete assembly и fixed expected controls; design их задаёт | CP-CODE и L-JL receipts ещё отсутствуют | сохранить |
| Source/S1 научно принят | Только source/design и bounded scalar arithmetic | Нет solver/discretization/experimental evidence | данных недостаточно |
