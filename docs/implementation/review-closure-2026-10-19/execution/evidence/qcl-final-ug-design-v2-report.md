# DEV05 D2 author report — actual spacing after GREEN-1

Дата2026-10-19. **Design round2/2, reviewable frozen candidate; independent
CP-DESIGN pending.** Публикация Core и D1 owning-doc CP остановлены координатором.
Этот автор не закрывает собственную приёмку и не запускает execution.

## Что сделано

Независимо прослежены public constructors → Unitful nm prefix conversion →
canonical metre Float64 values → Lp ratio → grid step, затем basis normalization,
BDD hopping, volume/sheet density, literal periodic Poisson и bulk TGT† map.
Прочитаны original GREEN-1 raw/receipt до новых выводов. Применяется ранее
прочитанный qcl-physics-audit; source/design/arithmetic scope сохранён.
Новая математическая correction выдана отдельными outputs, не редактированием
failed originals. Julia/import/Git/solver/install/build/server0.

Файлы:

| Output | SHA256 | Bytes |
| --- | --- | --- |
| `/tmp/qcl-final-ug-design-v2.md` | `eb9e1a8c39ad08bafa480970392d844c2c9fffdef02d847397ef87c52111bfc9` | 28860 |
| `/tmp/qcl-final-ug-design-v2-mathdiff.md` | `91959685fd63d02069c74f1c67b9c959e2674ce3914db63e88d1f810a0f7c217` | 4014 |

D2 selected same public builder and **identical** physical/numerical input
arguments. Не выбран вариант с изменением30nm/10nm, dose, weights, mesh,
channels или S1 ради exact1. Не заменён false predicate на approximate equality.
Новый strict guard выводит expected h из независимой literal unit chain и
сверяет всю canonical layer/scale/grid chain точно; original false guard
сохраняется в immutable failed test. Разрешение заменить guard в future I
возникает только после independent D2 review, а не из этого авторского отчёта.

## Наблюдение и причина D1 failure

Actual GREEN-1:46passed/0failed/1error, fatal test662 exact wZ==ones3 false;
coupled final audits не достигнуты. Wall39.449s, sampled RSS928108544B,
ownedTMP sampled0, raw2183B complete, guards/stop_reason null. Это failed
D1 precondition, не установленный production bug и не scientific outcome.
Один из initial max2 DEV05 L-JL invocations использован; один остался.
Этот D2 не потратил ни одного и не назначает дополнительный metadata run.

Root-provided immutable Core identity:
`f5b73369a96d1225bd96fb34f5262c8dcf965f86`; Git здесь не выполнялся.
Reading source и независимая Python binary64 арифметика дают:

| Quantity | Source-derived expected result |
| --- | --- |
| nm→m factor | RN(1/1e9),hex0x1.12e0be826d695p-30 |
| Layer30nm coefficient |3.0000000000000004e-8m,hex0x1.01b2b29a4692cp-25 |
| Scale10nm coefficient |1e-8m,hex0x1.5798ee2308c3ap-27 |
| Lp_input64 |3.0000000000000004 |
| h64 |1.0000000000000002,hex0x1.0000000000001p+0 |
| RN(3h64) |3.000000000000001, **different from Lp_input64** |
| RN(sqrt(h64)) |1.0, so actual Float64 χ mayequalΦ |
| qL64=RN(1/RN(h64²)) |hex0x1.ffffffffffffcp-1 |
| v64=RN(1/RN(sqrt3)) |hex0x1.279a74590331dp-1 |

Raw log did not print actual h, поэтому это source-derived prediction,
не вымышленное measured value. Оно согласуется с observed exact1 rejection.
New exact chain guard independently tests the prediction; target grids/
`_scaled_physics`/Poisson output не вычисляют expected h.

D1 ошибочно считал exact unit-spacing следствием nominal30nm/(3*10nm),
игнорируя раздельные Float64 conversions. D2 учитывает также последующие
rounding distinctions inputLp/grid-length и sqrt(h) normalization; новые
false exact identities вместо старой не вводятся.

## Полный corrected mathematical contract

φ discrete normalized не меняется. Continuous χ=φ/√h, spatial nbar=Dφ²/h,
NDbar=D/(3h), spatial weights h; sheet/raw/candidate number D=1/64 и
energy/radial current/number measure не получают лишнего h.
`tZ=t0/h²`, H0=(2−√2)tZ, τ=−tZ/4,c=tZ²/8; **k term remains t0*k²**.
Literal M3/h² и b=λD*d/(12h) дают U*=λDh*d/36,u*=λDh/72.
Causal six-node roots и same-G actual TGT† map сохраняют полный nonlinear
raw fixed point; no solver loop. Все h powers derived, не подобраны.

Poisson comparison различает ideal M/h² и independently source-rounded
qL64*M. Для literal published Float64 n inputs exact references используют
P n_float и eigenvalue3qL, без exact sum(n_float)=D/h предположения.
`Uexact=la/(3qL)P n_float`; ζ reference учитывает qL и source v64.
Independent measured Q4 residual и exact inverse2norm4/3 дают ζ forward
bound, который обязан поместиться в retained h-correct γ32 regression
budget; бюджет не расширяется. No guessed LAPACK accuracy coefficient,
no relaxed physical criterion. Existing γ16/32/64 scalar-operation bounds
и all source `SolverTolerances` сохраняются.

Complete problem/Green/SCBA/candidate/solution/history inventory сохраняется;
поля n/U/χ/tZ и related histories corrected consistently. Actual same-field
current history и zero-current absolute cancellation bound сохраняются.
Frozen38/41 gate inventory, real fresh/validate/explicit evaluator calls,
no-alias and no synthetic pass metrics remain mandatory.

| Complete input | Exact expected global failures |
| --- | --- |
| Healthy U_h*,G_h* |{r_sum} |
| N1 wrong-U2U_h*, retainedG_h* |{r_D,r_D_candidate,r_U,r_sum} |
| N2 fixedU_h*, staleG0_h |{r_D,r_D_candidate,r_sum} |

Independent scalar check gives N1≈.08946567246,N2≈.09013587908 and lower
bound≈.08897096039; rU_wrong≈.01570757654490 E0. Healthy r_sum≈4.9737276762
still FAIL unchanged1e-3; no full solution/science pass. D1 optional N3
не реализуется и не добавляет runtime scope. S1 all-five/no-e–e0mV70K
и acceptance criteria не менялись.

Дополнительно Fraction arithmetic проверила exact h-scaling identities
Poisson, φ†Uφ и weighted density для rational h=1/2,1,2; spectral support
assertions относятся только к declared h64. Python float enumeration
подтвердила single active node обоих actual-spacing analytic states,
Pauli margins и source qL row sums. Это bounded stdlib arithmetic, не
Julia run, SCBA, benchmark или new numerical environment.

## Preserved identity и source provenance

* D1 full design96c2c50a104b984c72603fa7066986d9bf6c02a8e59ba1ce0df9f06e321da162
  и CP-DESIGN11900d840a7155ac3a28161f4d0f5f16ac5e3cdb810e37e18c4fc9a5e834c52b
  unchanged. Их приёмка exact1 premise не переносится на actual failed run.
* Failed I test6d0db8b15300dce5350bf1bb282cef008da494be57bd96b23780ab1b314049a9
  и current owning docd51f984c68ac6c5ea9e25ecce21d2f66aca6b635de168f68cc4e711ce9005be3
  unchanged; hashes checked before and after D2 writing.
* Original receipt557f60ed37c4f325d09d552672730f6ad6db414781a0da84d57946c467b67c95
  и raw6918099fc6b8a06bc96b70424d08104915c64ed0eb98900b9c3b3a466ab7252e
  unchanged, read-only.
* D1 old18-file reading list included owning doc673bc964…; current docd51…
  is explicitly different historical/current documentation identity. The
  other17 inputs (13production+4oldtests) rehashed unchanged. No production
  source changed; no second maintained composition lock is created.

Additional primary files read for unit/normalization chain and their hashes:

| Path relative to managed root | SHA256 |
| --- | --- |
| `components/QCLNEGF.jl/src/domain/constants.jl` | `54a46355ac6701df6f9ede11746f2ec48751ae84d8f54024b164b106df086c7c` |
| `components/QCLNEGF.jl/src/domain/scaling.jl` | `2049ea6638da871c406718dad9f1aa4eb5cee68f4ce8941a8270e050dd7eb9f0` |
| `components/QCLNEGF.jl/src/domain/presets.jl` | `84a0fffbb732fbd7c51889be2e0c06c46abd74eb7a03dce11beb8fc72dce5050` |
| `components/QCLNEGF.jl/src/numerics/reference/hamiltonian.jl` | `7cfea79a21f853754b0edf5cd15922c03457c279b69c6f5a228e2e4c9b6b53a4` |
| `.build/local-julia-int01/import-phase-1/environment/julia/Manifest.toml` | `a6cb226a2d6fe990e9a067658c16b44acdbaf984e68c3474232a22f72d8d8b47` |
| `.build/local-julia-int01/depot-1/packages/Unitful/HhRY9/src/conversion.jl` | `c7121ec8ee73a853bdc744f1b8e8de57d7bfb17b9fd836f9dd866c236a3818a0` |
| `.build/local-julia-int01/depot-1/packages/Unitful/HhRY9/src/user.jl` | `5ac0f35618b17313cc1b613bc19cecf13195def5aea90389b02cf50941a47a4e` |
| `.build/local-julia-int01/depot-1/packages/Unitful/HhRY9/src/pkgdefaults.jl` | `268b555ed54bc50c112a790935ac4998314b49384857f2714a851eea6b81897b` |
| `.build/local-julia-int01/depot-1/packages/Unitful/HhRY9/src/display.jl` | `c74b3f28a7b8a77dc6d5d97958db7ba0b7c1b91fb224a9a5292b124e800e94f0` |
| `components/QCLNEGFRunner.jl/.build/julia/share/julia/base/rational.jl` | `0a0345a11cab9d2ba3c7bb1554c896813e3b1611771803616d2f3f7376f0141e` |
| `components/QCLNEGFRunner.jl/.build/julia/share/julia/base/promotion.jl` | `22dcacddb90e746239066659cb5a086eac7e968619f4aa32a25fd8a816ef51dc` |

Locked Manifest selects Unitful1.28.0 tree57e1b2c9…, local package HhRY9
source inspected read-only. Julia1.13 rational and generic Number multiplication
source confirms promotion/conversion order. No package code was imported;
no installation or runtime identity probe. These local primary definitions
make an external web formula unnecessary for the stated discrete arithmetic.

## Checks, limits и передача

D2 files: strict UTF-8, final newline, no trailing whitespace, paired fenced
blocks checked. Before/after protected hashes and17 source inputs checked.
Output files remain below128KiB together. Work uses only source reads and
short stdlib scalar/Fraction arithmetic within1CPU/2GiB; no numerical engine.
Wall-time source envelope90min from root brief is not re-opened by this report.

Reviewer should independently verify exact Unitful/Float64 chain, distinction
between inputLp/grid3h, χ/Φ normalization, tZ versus t0 kinetic, floating qL
and rounded-n Poisson references, retained ζ budget/forward proof, and unchanged
failure inventories before authorizing I. No owning source/doc/test update
or remaining L-JL dispatch is performed by this author. This is round2/2;
new failed premise after final attempt requires concrete blocker disposition,
not third round, rerun or tolerance/model tuning. Другие DEV tasks продолжаются.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| GREEN-1 продемонстрировал coupling oracle failure | Raw stops at exact wZ guard;46 static pass/1error | Coupled audits not reached | данных недостаточно |
| D1 premise требует correction | Constructor/Unitful/Float64 source chain and actual exact1 rejection | Actualh absent from raw; new exact prediction guard pending | изменить |
| Complete h-dependent D2 candidate выведен | Unit maps, χ/n/BDD/Poisson/TGT algebra, unchanged N1/N2 cases | Independent D2 CP-DESIGN/runtime pending | дополнительно измерить |
| Originals и physical scope сохранены | Protected hashes,17inputs unchanged,no source mutation | Publication halted; one L-JL call left | сохранить |
| Healthy/S1 научно принят | Healthy r_sum still FAIL; S1 unchanged/not run | No adequate discretization/experiment | данных недостаточно |
