# Native e171: pre-review 0 / 1 mV на период

Область: READ ONLY source review Core `e171caa60cce676c6c4238dd671e7c527f2bd977`, tree `742ed5a6fe82f1e5c63fc1a2290ed77f89ca6da8`, перед frozen harness. Ни Julia, ни HDF5 source arrays, ни новый Φ не запускались. Это не разрешение actual до проверки harness/source bindings/resource admission.

## Физический смысл и полный маршрут

`src/domain/presets.jl::reference_parameters` задаёт F_bias=V_period/Lp (если F_bias явно не override); при reference Lp=29,61nm положительные1mV/period соответствуют примерно3,3772e4V/m. `domain/scaling.jl::_scaled_physics` даёт Eᵖ=F Lp, т.е.1meV physical /0,01 native при E₀=0,1eV. Это field-periodic infinite cascade, не finite-device two-terminal1mV и не два reservoir chemical potentials.

Bias должен менять **оба**: `reference/basis.jl::project_hamiltonians`, h=H₀−F(Z−z₀I)+Uᴴ_projected+transverse, и energy shift ±Eᵖ в embedding. `optimized/production_operators.jl::_embedding_self_energy_production` вычисляет все R/</> components plus/minus из сдвинутых Green и T±; total=sum plus+minus ровно один раз. Sparse nodal interpolation на1mV может быть нецелым числом ΔE; invalid exterior rows zero, без wrap. Поэтому это конкретная конечная real-energy дискретизация, не непрерывная точность по bias/window.

`optimized/production_state.jl::_current_green_production` суммирует все irreducible scattering + embedding, решает GR=[EI−h−ΣR]⁻¹ с η=0, затем независимо GLraw=GRΣLGA и GGraw=GRΣGGA. После них native paired_convex constraint фиксирует число частиц; raw λ=Nraw/target обязан стремиться к1. Малый mixed step или нормированная плотность этого не доказывают. `production_solver.jl` на каждом шаге строит все mechanism candidates и fresh embedding из одного current Green, измеряет raw map defects до mixing. FD/подгонкаμ относится лишь к seed (`optimized/seed.jl`), не к finite-bias distribution. При finite bias equilibrium/FDR markers имеют статус finite_bias, а не pass/fail равновесного тождества.

Native elastic_retarded=:hilbert, retarded_real_part=:kramers_kronig, hilbert=:fft и default embedding=:full_cell_resolvent должны быть явно записаны для сравнения с исходным C/Hilbert baseline. Direct-static Mats endpoint из предыдущего опыта — иной вариант; его fixedpoint/скорость/μ не доказывают finite-bias convergence данного маршрута. Новая equilibrium Mats функциональность не заменяет GL/GG карту.

## «Без e–e» и Hartree

`domain/electron_electron.jl::ElectronElectronOptions()` имеет mode=:none. `optimized/electron_electron.jl::add_sppa_kernel` при :none возвращает исходный KernelSet; в enabled не должно быть :electron_electron. Корреляционный SPPA/exchange e–e отсутствует. Проверяется одновременно mode и actual enabled set=LO/acoustic/impurity/IFR/alloy (alloy требуется включить явно: default_scattering() включает только4).

Это **не** отключение электростатического Hartree. `solve_production` выполняет periodic Poisson outer loop независимо от SPPA. Прямой `solve_scba_production(problem,zeros(Nz))` — полный fixed-Hartree SCBA, но U=0/noPoisson, а не selfconsistent electrostatic device. Scope должен совпадать с поручением и быть явно записан; прежний U=0 не превращает новый запрос о bias в принятый Poisson-result.

## Базис, transfer и live memory

`reference/basis.jl::build_localized_basis` строит фиксированное ZERO-FIELD PzP пространство из repeated band/mass profiles, затем проецирует H₀/Z/M⁻¹/T±. При неизменной геометрии/material/basis controls bias сам не перестраивает этот базис или kernels. Поэтому exact same-grid FD128/0V state допустим как начальное приближение. Нельзя переносить convergence status, raw histories или Anderson history через изменение bias. Нужны resume_iterations=false и новый mixer; source state label not_converged сохраняется.

Для warm input native solver проверяет shape и mechanism names, **не** численные ε/k/basis/scales/source physics; harness обязан связать эти contents/hash и U. Совпадение NE недостаточно. `production_cache.jl::_cache_source_contract` требует actual grid/kernel ownership, `_cache_shift_contract` проверяет ±Eᵖ; 0V cache нельзя молча применять к1mV. Использовать штатный retarget/rebuild с новыми shifts и bounds metadata.

`solve_scba_production` по default копирует selfenergies warm input, делит initial Green только до нового Dyson. consume_initial=true разрешает перенос владения PRIVATE loaded buffers; caller не должен затем использовать их. Callback borrowing запрещает накапливать все итерационные full states. В `production_cache.jl::_estimate_production_memory` отдельно учтён retained_warm_start=(4+3M+9)fields; M5→28 full complex fields, помимо resident/candidates/FFT/mixing. Native peak guard должен быть реально ≤ OS hard cap на тех же алгоритмах/workers/chunks/history. Нельзя добавлять скрытый HDF loader dictionary/full old solution copy сверх этой live-set модели. Если estimate≈12,92GB при hard≈13,019GB, это только тесное admission, не гарантия фактического RSS/JIT/GC; provenance должна сохранять честные bytes и runtime refusal/stop, без обхода guard.

## Требования к frozen review

Одинаковые physical/all5/noEE/basis/scales/window/Nk/Nz/U/algorithm/mixing/tolerances для0 и1mV; одинаковый canonical NE, не смешивать30704/30721 как один matched grid. Единственная physics delta — V_period/F/Eᵖ. Не добавлять surrogate bath, η в nonlinear Dyson, FD repair, clipping или новых физических closure. Initial-state transfer и source SHA отдельно от exact restart.

Сохранить stage counts, fresh aligned Γ/Green/Σ candidate raw residuals, λ, Keldysh/spectral/PSD diagnostics, boundary-current and power/continuity witnesses с native near-zero floors. При16–32 шагах возможны лишь конечные measured attempts; iteration limit/stagnation не convergence. Исходный0V C/Hilbert baseline уже имел unresolved defects: маленький V не исправляет их задним числом. Достаточность сетки/окна, Poisson, basis/k и experimental transport validation остаются отдельными границами.
