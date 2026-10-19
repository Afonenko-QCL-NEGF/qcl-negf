# RV08 first6 — независимое review frozen v1

Статус: **static first6 audit принят с адресными report corrections; научная/численная приёмка не установлена**. Первичный blind source этап сохранён до candidate в [RV08-first6-blind.md](RV08-first6-blind.md); candidate не читал до этой записи.

Source: Core `3108150dd1b6b1377470b384b15c26e272fe5c5d`; root S `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`, hashes/source-receipt overlay immutable. Reviewed **reviews-input/RV08-v1.md**, SHA256 `2c2d65e1e8751374bdfcfccc168440979bf4af300e1115c06ed9bdbb48115838` — независимо вычислен и совпал. Только 6 packets D/K/S/P/L/J и 18 declared properties. Remaining22 reference и6 PROD contracts не reviewed и не добавлены в denominator.

Supplemental источники reviewer перечислены в blind report; адресно добавлен `test/numerics/frozen_scientific_fixtures.jl` только для контраргумента об общей support/shift/LO-size независимости. Его impurity/PV testsets относятся к remaining queue и **не приняты здесь**. Named initial fixtures + source/math/criteria проверены статически. Execution fixture/solver/build/import/install/benchmark/browser/server=0; отсутствие measured science/test outcome сохранено.

Reviewer conservative envelope для каждого из шести packet: 2026-10-14 18:00:24 UTC → 2026-10-14 18:07:44 UTC, **440 s**, <8min. Это shared source-analysis/сборка review, не изолированные measurement часы; не суммировать 6×. Writer isolated times и author+review20min sum не measured; coordinator общий grant отдельно. Sequential bounded text reads/stdlib ≤1CPU, numerical payloads не читались; peak RSS не instrumented, 1GiB workload cap не выдаётся за измеренную telemetry. Sections ≤8KiB и shown source extracts ≤96KiB/packet.

## D — D1/D2/D3

Соответствие formula→symbol→criterion подтверждено: traceability EQ-DYSON-001 → theory07 eq-dyson-retarded → greens.jl::retarded_green → validation.jl:33–47::_dyson_residual → acceptance_metadata.jl:21–37. Full dense inversion D/s и /s algebraically exact; scaled dimensionless operands, no quadrature; η≥0, Hermitian h и dissipative ΣR — applicability, не enforced physical input validity этой функцией. Residual numerator Frobenius/denominator identity floor sqrt(Nb) — backward residual, не forward Green/current error. T070 literal line shape oracle независим от inv/spectral implementation, но only scalar spectral/κ. Candidate правильно не приписывает complex/matrix/negative fixtures или execution.

**P3/R08-02 — описание causal residual должно содержать positive part.** Frozen v1 D prose «eigmax(ImΣR)/(||ΣR||2+1e−14)» пропускает `max(0,...)`. На Core validation.jl:27–31 `_positive_imaginary_part` точно `max(0.0,eigmax(ImΣ))/(opnorm(ΣR)+floor)`; causal ΣR с строго отрицательным eigenvalue имеет нулевой defect, не отрицательный residual. Минимальная correction только report equation: `max(0,eigmax(Im_H ΣR))/(||ΣR||2+1e−14)` и max по blocks в _causality_residual. Actual source код корректен для этого contract; новый numerical test не запускать. Также `_dyson_residual` не включает η: regulated initial seed нельзя считать η=0 final proof; кандидат applicability не должен скрывать это различие.

## K — K1/K2/K3

Product algebra GRΣ<GR† даёт anti-Hermiticity/PSD congruence при declared inputs, no normalization/weights внутри product. Candidate отличает algebraic conditional вывод от measured gate. Критерий rK global unweighted norm, additive floor1e−14 в solver units и project tolerance1e−8 верно привязан к validation:60–71/metadata. PSD/eigenvalue budget не заменён знаками off-diagonal.

T070 не вызывает keldysh_green — reviewer независимо обнаружил это до candidate. Supplemental analytic_equilibrium_*:113–138 действительно вызывает target product, но zero flux/current и finiteness не direct ifA/anti-Hermitian/PSD expected assertion; общей arithmetic factor error могла бы остаться невидимой. Paired-occupation supplemental reviewer показывает другой iteration constraint и legacy negative Pauli case, не снимает назначенный noncommuting matrix gap. Candidate RV09 literal scalar/2×2+/− packet уместен, без заявления отсутствия всех Core tests. Static K1/K3 contract valid; K2 direct independent numeric evidence отсутствует.

## S — S1/S2/S3

SCBA текущий h(U)/G перед fresh candidate; rK/rΣ до mixing и без α factor подтверждены scba:190–235,323–325. fresh_fixed_point_metrics projects тот же U, сравнивает published G с raw candidate, отдельно raw/normalized charge и lambda; reference physical kernel остаётся общим риск-path. solver:157,229–245 использует published_U и previous_scba, validation:636–640 fresh Poisson rU сравнивает с solution.Uᴴ. Candidate source-order вывод не выдаёт full production/run proof.

Fresh_candidate_residual независимо строит scalar complex pole и delta/denominator arithmetic; positive stored/relativeΣ pass и fresh gate negative могут сосуществовать; default candidate limit rK source policy. Source fixture не вызывает full solve_scba/final_audit/assembly. Independent_nonlinear_and_continuum_anchors::Nonlinear SCBA causal root and honest finite budget **уже содержит** scalar Σ=λG causal quadratic-root oracle с linear/Anderson/seed variants и maxiter1 negative; он uses actual production Dyson/residual/mixer, не full reference final U/G. Предложенную RV09 scalar trajectory проверку сначала связать с existing exact-source anchor; wrong-U final fixture всё ещё отдельный gap. Это дополнение доступного source, не расширение18properties и не measured repeat.

## P — P1/P2/P3

Source/kernel assumptions N≥3 подтверждены NumericalParameters types:210/255, εr>0/uniform grid/positive donor sheet. Harmonic faces, cyclic stencil, b=−λP(ND−n), border v=ones/sqrtN, scales/moment/floors/tolerance source соответствуют описанию. Gauge arithmetic mean равен wx-weighted mean на uniform grid. Несовместимый source проявляется ζ/neutrality/residual; source subtraction не скрывает charge. rP candidate≠outer rU, candidate явно это разделяет.

T073 RHS=ND+L*Utest/λP с той же build_poisson_matrix — независимость stencil не доказана; candidate правильно ограничил утверждение «отсутствует в выбранном fixture», не всей Core. Reviewer supplemental exact source independent_nonlinear_and_continuum_anchors.jl:151–187 содержит **уже существующий** continuum sine RHS epsilon*(2π/L)^2 exact solution без L*U, N32/64/128 и >3.9 second-order assertions. Минимальный next step — адресно переиспользовать это existing positive oracle, а не создавать дубль. Nonneutral-source negative assertion в этих selected fixtures не найден; его scientific acceptance unknown.

## L — L1/L2/L3

Fröhlich prefactor J²m×qz integral length→J²m²/K0, dimensionless longitudinal F и tensor/radial qK восстановление source math подтверждены kernels:324–363,441–462 и theory08:97–158. Declared reference lesser+ω/greater−ω emission и opposite absorption корректны. Production named fixture вызывается actual configured kernel/cache; target production_operators:974+ — лишь selected edge, не all-PROD acceptance.

Fixture KMS/number/energy ratios, signed integrate before abs, norm/event_scale nearzero lack (nonzero gaussian), integer+/fractional negative/refinement trends совпали. Общий kernel scale мог бы сокращаться; shared _fermi и representation/shift helper не дают independent absolute Fröhlich oracle. qz amplitude/tensor orientation needs literal anchor; no measured thermal loop or S01 acceptance. Reviewer exact_kernel_rescaling LO signs uses common _static_contraction/apply_energy_shift; useful composition check, не alternative physical model. frozen_scientific_fixtures spectral sector balance тоже constrained transfer, не quantitative LO amplitude. Candidate сохраняет these limitations, no property n/N false pass.

## J — J1/J2/J3

Outgoing trace Σ>G<−Σ<G>, boundary number flux E0/(ħL0²), engineering electron-flow charge eΦ sign, wk×gs/(2π) и J0/E0eV resolved units проверены observables:175–280/scaling::ScaleSystem/theory11 EQ-CURRENT-001. Physical wE E0eV интегрирование assigned code действительно даёт e·boundary_flux. bond_current reconstructs all a,b and Nz−1 internal bonds, no seam; projected-basis equality/constant energy-resolved local current не universal gate. rJ scaled-flux1e−12 floor не rJchange A/m² floor.

**P2/R08-01 — source documentation normalization disagreement подтверждено независимо.** Core3108150 `docs/src/theory/11_observables.md:53–55` EQ-CURRENT-002 не содержит1/(2π); `src/physics/observables.jl:251` содержит gs/(2π), как интегрированный EQ-CURRENT-001:40. При той же definition веса/code units имеется factor2π. Это scientific doc contract finding, не numerical code regression и не разрешение менять solver. Минимальная owning Core correction: согласовать formula measure с implementation и explicit `integral j(E)dE=eΦ`; сделать bounded nonzero literal reference assertion по тем же units/weights в отдельном поручении. Unknown raw run не мешает algebraic mismatch.

Named cavity current oracle independent literal determinant Landauer проверяет finite_chain_green incoming+/− и bounded T, не boundary_flux/resolved/bond APIs. Supplemental equilibrium zero signal не увидит missing scalar factor. Candidate заранее отметил обе границы; independent reviewer подтвердил. J3 finite-basis/coherences reconstruction fixture остаётся отдельным gap.

## Metrics, scope, roles и smallest corrections

**P3/R08-03 — неправильные labels административных счётчиков.** V1 final «M03:6/6 initial source packets read»/«M19:0/6 packets independently reviewed» не definitions этих M-ID: frozen review-metrics SHA25671cef8a23f948fa7eb43e13d4baf17f9af6cdfdeaf907a1efcf81be1eace3e31:L98 — independent numerical oracle properties; L114 — fullydefined criteria/applicable frozen criteria (norm/weights/units/tolerance/nearzero/evidence). Минимальная correction: назвать6/6 packet-reading coverage и0/6 reviewer bookkeeping отдельно; M03 property/positive/negative independence ledger и M19 criterion completeness оставить ограниченным выбранными18properties/frozen inputs, без invented denominator pass. Report science unknown honest; это naming correction, не alleged solver pass.

Source-formula chains18/18 addressed, test execution0, independent source review6/6 завершён только для frozenv1. Criteria domains/tolerancebasis/nearzero/metamodel missing noted; actual runtime source/plan/model/run/attempt/HDF5 не supplied. Вектор execution/convergence/physics/discretization/experiment: все numerical outcomes **not_measured**, mathematical/source observations отдельны. Рецензент не оценивал22ref/6PROD remaining work writer и не менял shared sources/report/cards/fixes/progress/index.

Роли: Research выбирает applicability/oracle/tolerance basis в RV10, без zero-bias→transport validation подмены; operator сохраняет source/run/attempt/frozen plan и admission/budget будущей проверки; developer Core исправляет doc measure, сохраняет numericalcontract, адресно reuse existing fixtures в RV09 и выполняет только отдельно порученные checks. Writer уведомлён R08-02/R08-03 и supplemental anchors; core2π finding уже был вv1 и подтверждён reviewer.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| First6 properties source audit пригоден | Immutable Core + six packets/source/fixture assertions | Partial18; numeric/test execution0; remaining22+6unreviewed | сохранить |
| Resolved current doc/code measure расходится | Theory11:53/codeobservables:251/integratedformula:40 | No run-level current error demonstrated | изменить |
| Causal residual report needs positive part | Validation:27–31 versusv1Dprose | Actual source uses correct max(0,...) | изменить |
| M03/M19 не packet-bookkeeping counters | Frozen metric definitionsL98/L114 | Actual property/criterion N cannot invent from6packets | изменить |
| Existing continuum/nonlinear anchors доступны | independent_nonlinear_and_continuum_anchors positive/negative assertions | No execution/fullfinalU-G/nonneutral proof | дополнительно измерить |
| Numerical/scientific acceptance неизвестна | No frozen run/model/artifact inputs and no execution | Science gates don't inherit static review acceptance | данных недостаточно |

## First6 Round1 — scoped v2 recheck

Frozen v1 hash2c2d65e1e8751374bdfcfccc168440979bf4af300e1115c06ed9bdbb48115838 unchanged. Corrected v2 hash488fafaeb8b2de189d200c76bdc44a5515c2c5067c2f0992887167c2cf953925: causal residual now max(0,eigmax(...)); packet-read/reviewer counters явно administrative, M03/M19 partial; P/S next step reuses existing independent_nonlinear_and_continuum_anchors. Эти три corrections приняты. Fullfirst6code не re-read, solver/tests не executed.

Current2π docs issue remains; globalaggregate inputabsence scoped correction отдельно F-R08-06. Found RV01 original plan/runattempt не grant imported/source/model science acceptance. Этот recheck не меняет18property numerical status.
