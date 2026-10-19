# RV08 — concrete handoff, product/source patches не выполнялись

Owning component Core `3108150dd1b6b1377470b384b15c26e272fe5c5d`.
Это review dispositions, не поручение запуска/PR и не новое научное решение.

| Утверждение / ticket | Свидетельство | Ограничение / cheapest distinction | Решение |
|---|---|---|---|
| D08-01 исправить формулу энергетического тока | docs/src/theory/11_observables.md:53–55 EQ-CURRENT-002 против src/physics/observables.jl:251 и EQ-CURRENT-001:40; confirmed blind reviewer/root | добавить energy measure1/(2π) в owning formula; nonzero literal API integral отличит фактор. Не менять solver/code tolerance | изменить |
| D08-02 согласовать seed normalization prose | docs/src/theory/19_production.md:262 обещает post-root normalization; src/numerics/optimized/seed.jl::_seed_green_production final comment запрещает unilateral rescale after bisection | author candidate, independent review pending; описать фактически ifA from root без rescale; Pauli policy не менять | изменить |
| D08-03 согласовать accepted basis localization alias | docs/src/theory/05_basis.md:58–59 обещает legacy_pzp/pzp alias; src/numerics/reference/basis.jl:110 разрешает pzp/none/real_space; test/physics/full_window_basis_preserves_the_spectral_subspace.jl:70–78 явно ожидает legacy_pzp ArgumentError | bounded owning-doc proposal: использовать accepted pzp и описать rejection legacy_pzp. Не добавлять code alias/compatibility change. Negative assertion read-only, execution0 | изменить |
| O08-01 Keldysh noncommuting expected matrix | greens::keldysh_green; initial scalar fixture не вызывает его, zero-current indirect anchor не различает multiplier | bounded literal 2×2 GR/Σ< expected matrix, anti-Hermitian/PSD inputs; no shared product helper | дополнительно измерить |
| O08-02 Poisson compatibility negative | named manufactured fixture shared L, **existing** independent_nonlinear_and_continuum_anchors.jl:151–187 continuous RHS | reuse existing positive Nz refinement; добавить nonneutral-source case ζ/rneutral/rP failure; не создавать дубль continuous oracle | дополнительно измерить |
| O08-03 raw/final state gate | fresh_candidate_residual.jl literal resonant residual; existing independent_nonlinear... scalar quadratic root primitives | reuse root; actual full SCBA/final audit wrong-U negative remains gap; no synthetic unrelated zeros accepted | дополнительно измерить |
| O08-04 public current and truncated-basis reconstruction | cavity_current_and_spectral_oracles calls finite_chain_green only; bond_current full ΦGΦ† API not called | nonzero literal wE/wk/API integral with units, separate two-state coherence/basis truncation/seam contract | дополнительно измерить |
| O08-05 absolute kernels vs equilibrium identities | exact_kernel_rescaling/shared K; actual thermal LO normalized KMS/balance can cancel wrong global prefactor | independent single-state absolute Fröhlich/IFR/acoustic/alloy vertex magnitude with SI scale; existing frozen impurity positive midpoint angle oracle reuse | дополнительно измерить |
| O08-06 direct/FFT PV vs product integration | analytic_product_integration/frozen triangle oracle applies different operator from direct omitted-diagonal sum | reuse product oracle only for that contract; literal few-node direct sum and separate continuum window refinement | дополнительно измерить |
| S08-01 campaign scientific acceptance | predecessor RV01 identifies hashed frozen plan/schema/model/fingerprint/run/attempt1; RV08 source-only input, no archived numeric arrays | raw HDF5 completeness/source-import closure unresolved, all numeric verdicts not_measured; originals not reread | данных недостаточно |

Точные source chains, критерии и property dispositions — [RV08 revision3](../RV08.md).
M03/M19 остаются partial без frozen applicable numerical-property/criteria denominator.
34/34 прочитанных selected packets — административное coverage, не scientific pass.
RV09 должен сначала решить reuse/extend существующих oracle, с отдельным grant;
этот автор RV09 не начал. Source/review-only fixes-файл не меняет product code.
