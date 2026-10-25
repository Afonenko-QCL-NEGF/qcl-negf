# SCI12-MATH-I1-DYADIC — F, только RED fixture authoring

2026-10-20. Авторский source candidate, **не наблюдённый RED/PASS**. STOP для независимого high fixture review, затем отдельного Root bounded RED. Применены qcl-physics-audit и test-driven-development в пределах прямого F grant: тестовый source написан до реализации; execution явно отложен поручением. Production source не создан.

## Identity и scope

Results worktree `/tmp/qcl-sci12-math-results-worktree`, branch `codex/review-closure-equilibrium-map-math`, HEAD `de70638a982f91b7e125ab1cfc70a2daef2a656d`. Начальный status пуст, submodule status пуст. Component AGENTS.md отсутствует; прочитаны managed Root AGENTS.md/architecture, owning CONTRIBUTING.md/pyproject и существующие source-ownership tests. Root HEAD `107bac5697b37cf0e47c3feb44883a907837645c`, восемь gitlinks сверены без изменений. Original Root dirty checkpoint и четыре untracked routing/batch15 artifacts сохранены; original рабочий checkout не менялся. Это source evidence, не архивный run.

Frozen primary D2 `/tmp/qcl-sci12-map-design-v2.md` SHA256 `5473c96d80ad44c1b045008c7fa1aa6055502b05681700d4191c54b46f42db17`; OPS `/tmp/qcl-sci12-map-ops-design.md` SHA256 `82a2fbc34cbfc2c6d879a160122362e54dc48586dca4153ae5229ff60ce93a3e`; independent high OPS review `/tmp/qcl-sci12-map-ops-design-review.md` SHA256 `3f0d7aa11fbc66cb3dbc5e66a0604d22eacb2e6705de165a4e1cc89198bd68d3`.

Единственная package mutation: `tests/test_equilibrium_map_math.py`, 16161 bytes, SHA256 `5e30ef6337374f281681e80e9dc94512043d7f4ee87890f2107d8973f003e1ce`. Patch `/tmp/qcl-sci12-math-fixture-patch.diff`, 16746 bytes, SHA256 `3f69757c5187913c636c35e601004fe4b2ffa9b32d4e2ab7cbc6512f6ef84e36`. Index/commit, public API/schema/CLI, configuration, Root/CP и `src/` не менялись.

## Регистрация и prospective route

26 `test_*` functions, **96 pytest cases** по ручному счёту decorators; collection/parser/import не выполнялись. В существующей pyproject регистрации `testpaths=["tests"]` файл обнаруживается стандартно, дополнительных markers/registration нет. 2 healthy literal controls без `api`; 94 cases зависят от `api`.

| test suffix | cases |
| --- | ---: |
| literal_normalization_oracle_control | 1 |
| literal_signed_and_partition_oracle_control | 1 |
| hat_clips_without_extrapolating | 8 |
| hat_signed_integral_and_partition | 1 |
| annulus_squared_measure_has_no_extra_pi | 7 |
| overlap_does_not_drop_partial_cells | 4 |
| restriction_preserves_signed_cell_integrals | 4 |
| restriction_sheet_literal | 1 |
| restriction_refuses_changed_domain_or_missing_cells | 6 |
| complex_product_keeps_offdiagonal_imaginary_and_order | 1 |
| gram_conjugates_left_operand | 1 |
| gram_discrepancy_is_not_renormalized | 1 |
| rectangular_gram_keeps_missing_third_subspace | 1 |
| density_bond_coherence_conjugation_and_unitary | 5 |
| unequal_dx_uses_actual_chi_for_density_and_phi_for_bond | 1 |
| scalar_invalid_inputs_are_contract_errors | 14 |
| product_refuses_implicit_copy_and_invalid_planes | 8 |
| matrix_outputs_reject_alias_and_invalid_storage | 8 |
| density_refuses_bad_scale_output_and_overflow | 7 |
| bond_refuses_bad_physical_inputs_and_output | 10 |
| density_mixed_complex_row_uses_conjugation_and_scale | 1 |
| gram_rank_deficiency_is_retained | 1 |
| product_three_by_three_zero_is_known_not_missing | 1 |
| product_overflow_is_not_a_finite_measurement | 1 |
| partial_annuli_keep_signed_weighted_numerator | 1 |
| partial_spatial_overlap_keeps_uncovered_strips | 1 |

Prospective invocation (НЕ исполнено): выбранный existing Python runtime + `PYTHONPATH=/tmp/qcl-sci12-math-results-worktree/src:<selected-contracts-src>` и `python -m pytest -q tests/test_equilibrium_map_math.py` из Results worktree, только после Root engineering envelope. Fixture сначала проверяет imported package `__init__.__file__` against actual candidate root, затем `find_spec` и exact future module origin, после import повторяет origin. Foreign installed/workspace Results не удовлетворяет guard. Нет sys.path mutation, broad import catch, stub, xfail/skip или production metadata flag. Missing dependency остаётся настоящей runtime/collection problem, а не маскируется как absent API.

Baseline `_equilibrium_map_math.py` отсутствует (filesystem existence check). В prepared runtime ожидается 94 **NEW_API_MISSING** failures из per-test fixture и 2 literal healthy controls; это прогноз, не измеренный результат. Так отсутствие нового API не становится collection error или ложным existing behavioral bug. Реальное collection/behavior ещё неизвестно.

## Literal oracle и mutation map

| Вопрос → expected | Источник/свидетельство | Различаемая ошибка |
| --- | --- | --- |
| dx1/4, Phi=I, chi=2I, Cbar3/8, masses1/3, M=[[2,i/2],[-i/2,1]] → n8/4, sheet3, J−3; deliberate substitution chi→bond gives−12, Phi→density gives sheet3/4 | D2 §9 R1-01 hand derivation; test unequal_dx | Потеря dx, лишняя нормировка и смешение actual chi/Phi |
| Original dx1 Cbar6 coherence J−3, conjugate J+3, offdiag0 J0; U=[[0,1],[i,0]], transformed M=[[1,−1/2],[−1/2,2]] → same n2/1,J−3 | D2 §9 coherence/unitary; 5 cases | Знак/transpose/conjugation, diagonal-only current |
| Complex rows chi=(1,±i), L0=2 → n1/2,1/4 | Ручные row forms4,2 divided by8; mixed test | Missing conjugation, scale power |
| A=[[1,i],[0,2]], B=[[2,0],[i,1]] → AB=[[1,i],[2i,2]], A†A=[[1,i],[−i,5]] | Written independent literal entries | Product order/imaginary terms/left conjugation |
| Phi=diag1,2 → Gram diag1,4, trace5 vs native2; rank1 Gram ones; rectangular3×2/3×3 → S=[I2,0], retained n=[1,2,3] | D2 §9 Gram/missing-subspace, independent rank literal | Renormalization, assumed full rank/unitarity, missing third sheet3 |
| Hats clipped centre3, strips3/4+9/4; annulus squared pieces0,27/16,13/16 → weighted numerator53/8 | D2 §§4,9; literal tests | Dropped tails, endpoint halfweights, extra pi |
| Signed restriction [1,−1,2,−2]→[0,0]; fine density1/3/2/6→2/4 sheet6; partial interior17/4 and strips1/4,3/2 | D2 §§5,9 | Abs-before-sum, nearest neighbour, lost partial cells |
| Shifted origin/changed period/nonuniform/zero-width/empty/missing cells → ContractError | OPS §2 uniform full-period applicability | Silent redefinition/extrapolation/missing-as-zero |
| Bool/type/nonfinite/zero denominator/overflow, invalid plane dtype/layout/shape, readonly and input/component aliases → ContractError | OPS §§2–3; negative cases | Implicit copying, invalid_data represented as valid0, unsafe output writes |

Expected side uses literal dyadic values, exact equality/array_equal and elementary literal healthy-control arithmetic. No fitted atol/rtol. `plane` only creates input float64 arrays; `output` creates caller-owned buffers. No expected value calls tested helper, Core/reference/optimized kernel, BLAS, NumPy @/einsum, eigensolver, generic norm, sqrt, pi or exp. Candidate helper composition occurs only on actual side of hat/annulus/overlap totals and retained-space observables. Input snapshots are checked for the matrix product.

## Dependency graph и пределы

Test source → standard importlib/Path + pytest + NumPy fixtures/assertions. `api` → selected Results package → prospective private module → eight exact private helpers. Negative tests additionally → existing Contracts `messages.ContractError`. No state/native/HDF reader, Core, Runner, archive or numerical solver import is requested by this fixture; dependencies of a future candidate module must be source-reviewed separately. Source ownership is a guard, не арифметический oracle.

Восемь helpers не имеют scalar `count`/budget arguments: Bool rejection покрывается scalar geometry/scale/cbar и plane dtype; empty dimensions и pair/output shape проверяются. Огромные forged array shapes/overflow of dimension forecast не конструируются: безопасный executable count guard требует явно выбранного internal validation entrypoint либо admitted tiny metadata-only representation; этот специфический branch остаётся не проверенным, не passing. Общий no-copy census, shape multiplication bounds и fixed operation graph требуют independent source review actual implementation. Alias invalidity проверяется, atomic rollback partially written outputs не обещан контрактом.

Generic chi/Phi residual/norm/interval/projector capability не добавлялась; non-dyadic Gauss/pi/sqrt enclosure pending. Rank/missing-subspace rows здесь проверяют Gram и retained literal observations, не новый inverse/projector API. PAIR-I2/N0 constructor/library peak blocked. Финитные engineering assertions не дают scientific tolerance/enclosure, supplied-array relation proof для реального архива, S1 verdict или CP-SCI READY.

## Учёт и STOP

Только source/text/Git metadata чтения/записи. Logical source/text read conservatively <512KiB из cap2MiB; outputs fixture+patch+report+identity <64KiB из cap128KiB. Это оценка логического объёма, не syscall telemetry. 1CPU/1GiB и12min — finite grant envelope, не измеренный/enforced RSS/CPU claim. Arithmetic scripts/parser/compiler/import/pytest/tests/numerics/HDF5/solver/network/install/native/CI0. Executed only shell source writes, administrative readonly Git, rg/cat/sed/ls/test/sha256sum/wc; stray initial failed cat nonexistent path имел0 bytes source и никаких side effects. No subagents. Product calls87/science0/CI0/nativebuild0 остаются исходными; C08=8/8 не затронут.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Literal RED fixture candidate написан до product | Один untracked test source, exact SHA, module absent | Collection/runtime не исполнялись; high review впереди | сохранить |
| Все восемь private helper contracts представлены | 96 prospective cases и map выше | Count-overflow internal branch не испытан, source graph требует I review | дополнительно измерить |
| RED behavioral failure уже доказан | Только absent module observation | Нет test invocation; absent API не existing bug | данных недостаточно |
| Физическая приёмка S1 установлена | Новых science artifacts нет | 0mV/70K/all5/noe-e и прежние caps сохранены | данных недостаточно |

STOP. Не создавать implementation до high fixture review + отдельного Root bounded RED; никакого автоматического продолжения I.
