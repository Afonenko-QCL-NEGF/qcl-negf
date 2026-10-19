# RV09: source review capsule

Source S, overlay hashes: ../source-receipt.json. Root dirty inputs frozen: `/tmp/qcl-review-2026-10-14-e48e5b2-01/source`.
Owner/question/inputs/negative/acceptance/output: исходная карточка ниже.
Denominator фиксировать до чтения symbols; конечный selected catalogue явно записать в RV отчёт. Полный unseen catalogue остаётся partial.
Writes: только RV09.md, fixes/RV09-*.md; reviews/RV09-*.md независимый writer отдельно.
Stage review only; запрещены solver/tests/build/install/profile/server/product patches/publication.
Budget каждый atomic question <=20мин including reviewer; author <=12мин и review <=8мин ориентир; <=1CPU <=1GiB RAM; extracts<=96KiB; section<=8KiB; общий grant14ч с17:41UTC.
Stop: dispositions всем declared items, missing input, cap, следующий этап не поручен.

## Исходная карточка (frozen source, не дополнительная авторизация)

### RV09 — tests, свойства и независимость oracle

Входы: Core `test/physics/scalar_dyson_and_spectral_identity.jl`,
`manufactured_periodic_poisson_solution.jl`,
`analytic_equilibrium_sum_rule_lo_balance_and_zero_current_anchors.jl`,
`test/numerics/physics_first_exact_scba_candidate_equivalence.jl`;
Results manufactured fixture RV02; component harnesses и relevant tests RV07.

- [ ] Построить property→producer/consumer→fixture→assertion→mock-limit matrix.
- [ ] Проверить dependency graph analytic/manufactured oracle; общий helper
  и agreement reference/optimized отметить как ограниченную независимость.
- [ ] Описать negative mutation веса/знака/attempt, которую assertion различает;
  новые fixtures оставить tickets с применимостью из RV08.
- [ ] Выпустить `R/RV09.md`, выбрать минимальный будущий selected check.

Приёмка: наличие test отделено от исполнения и результата. M02 — repo×language
scope; Julia branch `not_measured` без проверенного инструмента. M04 — failure
denominator, M05 — только реальные comparable repeats. RV08 предоставляет
определения выбранных scientific properties, не блокируя harness inventory.

