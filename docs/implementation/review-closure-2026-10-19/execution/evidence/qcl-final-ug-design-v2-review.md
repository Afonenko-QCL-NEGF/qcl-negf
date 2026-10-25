# DEV02 O08-03 / DEV05 — independent CP-DESIGN D2

2026-10-19. Reviewer high, round2/2, source-first.

**CP-DESIGN D2 PASS для complete manufactured final U/G functional
oracle с source-derived actual spacing.** Допустима отдельная owning I
correction ровно по этому контракту, затем новый frozen source review.
Этот вердикт не разрешает немедленный runtime: последняя из двух DEV05
L-JL attempts остаётся нетронутой до I/source approval и root dispatch.
CP-CODE, functional GREEN и scientific acceptance не установлены.

## Входы, последовательность и сохранность

Сначала прочитаны actual GREEN-1 receipt/original log и первичные Core,
Unitful1.28.0, Julia1.13 source definitions; затем D2/mathdiff. Авторский
D2 report прочитан после независимого source/algebra cross-check.
Применён qcl-physics-audit. Scope: только чтение и короткая стандартная
scalar/Fraction арифметика Python, без numerical packages. Julia/import/
Git/solver/tests/build/server и project edits не выполнялись. Единственный
созданный output — этот новый review.

| Artifact | Проверенный SHA256 |
| --- | --- |
| D2 `/tmp/qcl-final-ug-design-v2.md` | `eb9e1a8c39ad08bafa480970392d844c2c9fffdef02d847397ef87c52111bfc9` |
| Mathdiff | `91959685fd63d02069c74f1c67b9c959e2674ce3914db63e88d1f810a0f7c217` |
| Author report | `7b7f49450c282d66994cccdd459add63a9ae41b213cf001807a8b4640f977765` |
| GREEN-1 receipt | `557f60ed37c4f325d09d552672730f6ad6db414781a0da84d57946c467b67c95` |
| GREEN-1 original log | `6918099fc6b8a06bc96b70424d08104915c64ed0eb98900b9c3b3a466ab7252e` |
| Failed/current I test | `6d0db8b15300dce5350bf1bb282cef008da494be57bd96b23780ab1b314049a9` |
| Current owning passport | `d51f984c68ac6c5ea9e25ecce21d2f66aca6b635de168f68cc4e711ce9005be3` |

Managed root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`;
Core immutable identity из поручения:
`f5b73369a96d1225bd96fb34f5262c8dcf965f86`.
Git status/revision/gitlinks reviewer не измерял. 17 исходных primary
source/test файлов D1 повторно совпали по SHA; historical D1 passport SHA
673bc964… явно отличается от current authored docd51… и не выдан за тот же
артефакт. Все11 дополнительных primary hashes из D2 report (Core constants/
scaling/presets/hamiltonian, Manifest, Unitful sources, Julia rational/
promotion) независимо совпали. Новый revision lock не создавался.

## Что установлено actual failed attempt

Raw log:46 passed,0 failed,1 error; fatal `wZ==ones3` в test:662, до
построения coupled states/fresh final audits. Receipt: exit1,39.449s,
sampled RSS928108544B, owned TMP sampled0, raw2183B complete, no guard error
или stop reason. Sampling caveats receipt сохраняются; это не hard RSS/TMP
peak proof. Actual h в raw отсутствует. Ни physics failure, ни production
bug, ни успех complete U/G audit этим запуском не установлены.

D1 review принял exact unit-spacing precondition как проверяемую premise;
GREEN-1 её опроверг. Предшествующие approximate carrier guards не доказывали
exact spacing. D2 правильно сохраняет failure и заменяет falsified premise
новым independently derived exact contract, а не isapprox, удалением guard
или сменой physical input. Предыдущий CP-DESIGN не переносится как runtime
приёмка failed D1/I.

## Независимый source proof unit chain

Прямо проверены:

* Core `types.jl:1–67`, `constants.jl:63–81`: Layer получает Float64 metre
  coefficient через `_length`; повторная metre conversion сохраняет его.
* `scaling.jl:10–23,35–40` и `presets.jl:236`: ScaleSystem отдельно
  канонизирует10nm; one-layer period и length scaling не объединяют
  преобразования30nm и10nm в одну exact rational quotient.
* `reference/grids.jl:12–25`: Δx=scaled_Lp/Nz, x=(g-.5)Δx, wZ=fill(Δx).
* Locked Manifest selects Unitful1.28.0/tree57e1b2c9…; local Unitful
  display/pkgdefaults/user/conversion definitions задают nano=-9 и
  rational1//1e9 factor; `conversion.jl:96–102` умножает coefficient
  на этот factor. Julia `rational.jl:162–165,187–189` плюс generic Number
  multiplication `promotion.jl:433–436` подтверждают Float64 promotion
  rational factor перед multiplication. Special float×rational alternate
  multiplication, меняющего этот путь, в inspected rational source нет.

Из literal input arguments, до чтения target fields, IEEE RN chain даёт:

| Independent expression | Результат |
| --- | --- |
| RN(1/1e9) | `0x1.12e0be826d695p-30` |
| RN(30*nm64) | `0x1.01b2b29a4692cp-25` =3.0000000000000004e-8m |
| RN(10*nm64) | `0x1.5798ee2308c3ap-27` =1e-8m |
| RN(ell64/L064) | 3.0000000000000004 |
| h64=RN(Lp64/3) | `0x1.0000000000001p+0` |
| RN(h64*h64) | `0x1.0000000000002p+0` |
| RN(1/RN(h64*h64)) | `0x1.ffffffffffffcp-1` |
| RN(sqrt(h64)) | 1.0 |
| RN(3*h64) | 3.000000000000001 |
| RN((1e16/64)*RN(L064*L064)) | D=1/64 exact |

Это независимо воспроизведённое source prediction, не значение actual h
из failed log. Proposed exact checks actual layer coefficient/scales L0/
all wZ/all x против этой цепочки сохраняют различающий guard. `h=actual_wZ`
или target scaling helper в expected side не допускаются. Input Lp64 и
grid3h различены; новое ложное exact равенство между ними не вводится.

## General-h физическая и дискретная алгебра

При точном real h=Float64 h64 Euclidean φ остаётся прежней; χ=φ/√h.
Идеальные n=Dφ²/h, ND=D/(3h) имеют правильную volume-density размерность
и h-weighted интеграл D. Sheet/number measure gs*wE*wk/(2π) не получает h.
Actual χ, source-rounded sqrt(h), actual donor profile и independently
rounded n_f проверяются с раздельными roundoff bounds; expected n нельзя
заменять выводом target electron_density. Source sqrt(h64)=1 объясняет,
почему χ может совпасть с actual Φ побайтно, но не отменяет real normalization
relation и propagation budget. r_n denominator использует input Lp64.

BDD tZ=t0/h² следует из `hamiltonian.jl:36–48`; H0, T и Egrid используют tZ.
Φ†diag(U)Φ не получает дополнительный h. Transverse kinetic term остаётся
t0*k² по `basis.jl:288–318`; смешение t0/tZ было бы иной equation oracle.
Z/centre/spread корректно масштабированы h, Euclidean overlap/Mminus1 не
меняются. Масштабы density SI используют canonical L064³, sheet — L064²,
с short-conversion rounding, а не nominal exact-length shortcuts.

Для M3 и d=(-1,2,-1) независимо:
`(M/h²)*(lambda*D*h*d/36)=lambda*D*d/(12h)`;
φ†Uφ=lambda*D*h/72. Fraction arithmetic для exact h64 подтверждает identity.
Это coupled spatial density→Poisson→projected-U relation, а не unrelated
sentinel values. Independently rounded U_f/n_f становятся exact input
floats для actual-comparison enclosures; идеальное равенство их округлённых
сумм не предполагается.

## Floating Poisson и retained ζ contract

Для actual-spacing source stencil qL64*M, face εr=1 и row scale4qL64
выведены независимо. У данного qL умножения на2/4 и row sums не вводят
новый coefficient error. После division на scale actual top-left bordered
matrix равен M/4. `build_poisson_matrix` не нужен на expected side.

При independently rounded n_f и checked actual la/uniform nd exact input-side
reference верен:

`U_a=la/(3qL)*P*n_f`,
`ζ_sqrt=la*(sum(n_f)-3nd)/(4qL√3)`,
`neutral=abs(sum(n_f)-3nd)/(3nd)`.

Uniform donor rounding влияет на ζ; zero-mean U определяется P*n_f.
Это корректная замена D1 shortcuts, не подгонка n/Up. Three-row residual
и gauge дают заявленный infinity forward bound через eigenvalue3qL.
Source b/row/norm/dot rounding учитывается отдельно; rP floor/gate сохранены.

Additional Q4 construction также корректен. Для v64=RN(1/RN√3) source
matrix `[M/4,v64*1;v64*1',0]` имеет zero-mean eigenvalues3/4 и остальные
±√3*v64. Exact literal v64 имеет √3*v64>.75, поэтому inverse2norm=4/3.
Exact reference `ζ_v64=sum(b_a)/(12qL*v64)` имеет верную нормировку.
С independently expanded directed residual R4 от returned Float64 Up/ζ
получается `abs(ζ-ζ_v64)≤(4/3)||R4||2`; direct residual включает difference
между exact b_a/rhs и source-rounded formation/solve. Второй solve и target
reference vector не используются.

Критично сохранён cap: measured forward bound должен помещаться в прежний
h/q-corrected γ32 short-formation budget; меньший enclosure используется
для comparison. Большой residual не может сам расширить допустимость
ошибочного ζ. Reciprocal-v ideal-reference difference имеет explicit outward
term; budget не повышается. Не заявляется универсальная LAPACK forward
accuracy из eps. Если cap не выполнится на настоящем tiny solve, это final
failure/blocker, а не разрешение менять γ/physical tolerances.

## Full U/G raw map и gates

С h-dependent H0/τ/c и unchanged transverse t0k² независимая scalar enumeration
снова даёт один active узел(e2,k1) для healthy и old-U0 state. Все прочие
real GR/ΣR остаются ненулевыми, A/lesser/greater нули следуют из поддержки.
c|g|²=1 обеспечивает raw Keldysh/spectral identities, B=16π²D сохраняет
raw/candidate/normalized chargeD и Pauli margin. Actual same-G map остаётся
legacy TGT† при bias0/empty scattering; fixture не является S1/cavity oracle.

Независимые scalar ориентиры при h64:

| Quantity | Healthy/N1 | Stale/N2 |
| --- | --- | --- |
| active A | 37.534037964391786 | 55.71729171399558 |
| B/A | .06573769394630925 | .044284297107222016 |
| bad fresh Dyson | .0894656724575317 | .0901358790834613 |
| r_sum | 4.973727676231814 | 7.867682391975498 |

Common lower separation=.08897096039189244; ideal wrong-U rU≈
.015707576544902627 E0. Actual final rU сравнивается с rounded-input/actual-
coefficient Poisson enclosure, не с этой rounded decimal как exact reference.
Separation велики относительно неизменных stored-D1e-11/candidate-D1e-8/
rU1e-7 gates. Current cancellation bound меняет только τ_h; меры и разные
scaled/SI current floors не меняются. Same-field SI current history сохранён.

Complete field inventories, no-alias rules, constructed-history semantics,
actual fresh map и три final API calls остаются binding. Все frozen38/41
metric/limit-key assertions и точные failure inventories сохраняются:

| Complete input | Обязательные exact global failed keys |
| --- | --- |
| Healthy U_h,G_h | `{r_sum}` |
| N1 wrong2U_h, retained G_h | `{r_D,r_D_candidate,r_U,r_sum}` |
| N2 fixedU_h, staleG0_h | `{r_D,r_D_candidate,r_sum}` |

Stored и fresh small rΣ должны пройти одновременно в N1/N2. Full report
нельзя заменить primitive/fake-metric dictionary; r_sum нельзя отключать,
чтобы получить global pass. Optional N3 не добавлен. Physical/static
tolerances и γ16/32/64 product/sum/Dyson budgets не изменены; h-dependent
extra formation ledger обязателен в I, не поглощается новым rtol.

## Вердикт, пределы и stop

Блокирующих математических/source findings D2 не обнаружено. D2 исправляет
конкретную falsified dimensional premise при прежних physical/numerical
inputs и задаёт проверяемые exact replacement guards. Авторское согласие
или агентский consensus не служили доказательством: использованы source
chain, exact scalar arithmetic и operator identities.

Следующий допустимый шаг — I только нового DEV05 test по narrow mathdiff,
с новым hash freeze/source review. Это последний design round; никаких
третьих design rounds, metadata Julia probes или автоматических reruns
этот review не разрешает. Один remaining L-JL call из initialmax2 должен
сохранить ≤120s/1CPU/2GiB/TMP16MiB/log2MiB и прежний aggregate≤4min.
Review использовал0 L-JL invocations. Failed D1/I/doc/receipt/log originals
сохраняются и не переписываются новой приёмкой.

Runtime exact chain guards, solve enclosures и final gate outcomes пока
не измерены. Iterative SCBA convergence не установлена. Healthy global
spectral gate доказанно FAIL; discretization adequacy и experiment не
валидированы. S1 all-five/no-e–e/0mV70K не менялся и приёмки не получает.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| D1 exact-spacing premise опровергнута | Actual46pass/1error, exact-wZ guard | Actualh не напечатан; coupled audit не достигнут | изменить |
| D2 h64 prediction и general-h equations корректны | Core/Unitful/Julia source chain, independent bit/Fraction arithmetic, BDD/Poisson/normalization identities | New exact runtime guards ещё не измерены | сохранить |
| ζ correction не ослабляет roundoff regression | Q4 exact inverse norm4/3, residual enclosure должен fit retained γ32 cap | Tiny-solve measured residual пока отсутствует | дополнительно измерить |
| Complete alignment oracle готов к narrow I correction | Full state/map/history/38+3gate contract и unchanged N1/N2 failure sets | Нужны новый code freeze/source review и последний bounded receipt | изменить |
| Healthy/S1 имеет scientific acceptance | Healthy exact r_sum FAIL; S1 не запускался | Нет adequate discretization/experimental evidence | данных недостаточно |
