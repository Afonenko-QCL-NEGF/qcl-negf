# RV08: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV08.md, fixes/RV08-*.md; reviews/RV08-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

## RV08 — операторные научные карточки

**READY:** статический аудит одного оператора, 2–3 properties на пакет.
Owners Core/Research. **Входы:** Core `docs/src/developer/traceability.md`,
соответствующая глава `docs/src/theory/`, `docs/src/physics/numerical-policy.md`,
`src/numerics/reference/acceptance_metadata.jl`, выбранный implementation
и literal/analytic fixture. Prefix путей таблицы — `components/QCLNEGF.jl/`.

| Пакет / properties | Точные implementation и начальный oracle |
| --- | --- |
| Dyson inversion/causality | `src/numerics/reference/greens.jl::retarded_green`; `test/physics/scalar_dyson_and_spectral_identity.jl` |
| Keldysh adjoint/scalar limit | `src/numerics/reference/greens.jl::keldysh_green`; `test/physics/scalar_dyson_and_spectral_identity.jl` |
| SCBA raw residual/final U–G | `src/numerics/reference/{scba,final_audit}.jl::{solve_scba,fresh_fixed_point_metrics}`; `test/numerics/fresh_candidate_residual.jl` |
| Poisson compatibility/gauge | `src/numerics/reference/poisson.jl::{build_poisson_matrix,solve_periodic_poisson}`; `test/physics/manufactured_periodic_poisson_solution.jl` |
| LO pair/balance | `src/numerics/reference/kernels.jl::lo_phonon_kernel`; `test/physics/production_lo_equilibrium_discretization.jl` |
| Current/basis reconstruction | `src/physics/observables.jl::{boundary_flux,energy_resolved_current,bond_current}`; `test/physics/cavity_current_and_spectral_oracles.jl`; EQ-CURRENT-001/002 |

Остальная очередь также конечна: отдельный пакет на каждый
`build_bdd_hamiltonian` (`hamiltonian.jl`), `build_localized_basis`,
`project_hamiltonians` (`basis.jl`), `build_shift_matrix`, `embedding_self_energy`
(`periodicity.jl`), `number_functional`, `normalize_lesser` (`greens.jl`),
`impurity_kernel`, `interface_roughness_kernel`, `acoustic_kernel`,
`alloy_kernel`, `_static_contraction`, `_lo_contraction`,
`direct_hilbert_transform`, `retarded_self_energy` (`kernels.jl`),
`electron_density`, `sheet_density_matrix`, `effective_levels`, `collision_balance`,
`power_balance` (`src/physics/observables.jl`), `validate_problem`,
`validate_solution` (`validation.jl`). Имена `.jl` без prefix относятся к
`src/numerics/reference/`. Каждый такой пакет проверяет формулу/размерность и
нормировку/квадратуру, третьим свойством — соответствующий ограниченный предел
из traceability. Production counterpart проверяется отдельным пакетом на те
же свойства по PROD-ID traceability, с literal oracle; не весь optimized путь сразу.

- [ ] Привязать 2–3 свойства назначенного оператора к traceability и ограничить
  applicability; записать exact source/fixture symbols на `S`.
- [ ] Построить formula→assumptions→discretization→symbol→observable→criterion;
  проверить units, norm, weights, tolerance basis и near-zero правило.
- [ ] Проследить independence oracle до helper graph; прочитать positive и
  negative assertion, не считать наличие fixture выполненным test.
- [ ] Зафиксировать отсутствующий критерий/предел и минимальный различающий
  analytic check или dataset slice. Прежняя S01 seed-карточка включается без дубля.

**Acceptance:** verdict для выбранных properties не сильнее evidence;
малый mixed step не заменяет raw residual, старое G не принимает новое U,
общий kernel не независимый oracle. **Выход:** `R/RV08.md`, M03/M19;
RV09 получает fixture/oracle gaps, RV10 — применимые критерии. Данные запуска
нужны только для измеренного verdict, не для source audit.

