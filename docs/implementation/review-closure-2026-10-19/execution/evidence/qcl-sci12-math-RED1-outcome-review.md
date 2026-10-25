# SCI12-MATH-RED-1 — независимый outcome review

2026-10-20. **Structural new-API RED подтверждён: 97 cases = 2 literal PASS + 95 call-phase assertion FAIL, setup ERROR0.** Блокирующих outcome замечаний нет. Это достаточное свидетельство отсутствующего нового API для перехода координатора к отдельно порученному bounded medium source-I восьми accepted helpers. Review не выдаёт grant/READY, не запускает I/GREEN и не устанавливает существующую физическую/behavioral ошибку.

Все команды review имели cwd `/tmp/qcl-sci12-math-results-worktree`. Results HEAD `de70638a982f91b7e125ab1cfc70a2daef2a656d`, status только `?? tests/test_equilibrium_map_math.py`; product module по полному src inventory всё ещё отсутствует. Fixture SHA `995b364b93a56c403859f9ad074d55ef4abb5dddb70e2ad0982f689cb1b45a6d` сохранён. Применены ранее прочитанные qcl-physics-audit/AGENTS/architecture и exact F2 source review.

## Точный frozen capture

- receipt14503B SHA256 `ad5a194bf61c6249db7c5c7a4d6cafad7af9896db82c8ae7044112956c4dddf1`;
- original.log63288B SHA256 `ddce3d47f93991ede4de574bb1f475e8f0549f107b8a1e304902a56291ca456e`;
- guard v2 SHA `d5b46ac8eaf1a9b9456b47d90bf5e04ec42ff6859363cf53847c6c1884ef858a`;
- plan v2 SHA `968c537b5b3bacf23f288d28254b50670930d27d8ae7e7afeceaba7ba463bf77`;
- Root controller v2 SHA `b314974a20b86d25e0b3aaf2146a213ba596fc53985c4253cb0dc618cd2b70af`;
- READY SHA `3ce08120f4ab9aeed049386bfc8f1a948553950be02f59ceddb7eabfee05ec26`;
- Root validation SHA `f69836d9447635742d6279cd77e2912513156f6d615a74b60b62932654b68a2c`;
- accepted guard review SHA `2227d19cce9c1169bf637234b15d583453f28cadae7e2682d89b6474365b1fa0`.

Эти actual hashes совпадают с receipt/ref bindings. Receipt сохраняет source_before/source_after для34 first-party files:8 Contracts,24 Results Python,pyproject,fixture; одинаковые записи прочитаны как текст. Guard closure проверяет exact набор/хеши до/после и absent product; terminal checks также связывают runtime,H/P/READY,helpers и review refs. Root controller делает fresh root107/Resultsbase/Gitlinks/status/counter checks, резервирует88→89 до единственного wrapper вызова. Это source+receipt evidence, не независимый syscall audit всех прочитанных файлов. История source v1/B1 не переписана этим review.

## Полный census и локаторы отказов

Проверены все95 failure summary node IDs,95 failure headers,95 ровно одинаковых AssertionError messages и95 traceback endpoints `tests/test_equilibrium_map_math.py:31 in __getattr__`. Другой exception/error payload среди строк `E` отсутствует: ещё95 строк `assert None is not None` и95 адресных пояснений `_candidate=None`. Все callers относятся к frozen fixture; исключения возникают до вызова product function.

Ниже `test_` подразумевается в каждой строке; line — actual caller в log. Param IDs сопоставлены с frozen decorators и всем summary, включая14 scalar args0–13,5 density/bond variants и полное Cartesian2×4 matrix-output множество.

| Function | Cases | Caller line |
| --- | ---: | ---: |
| hat_clips_without_extrapolating | 8 | 98 |
| hat_signed_integral_and_partition | 1 | 103 |
| annulus_squared_measure_has_no_extra_pi | 7 | 128 |
| overlap_does_not_drop_partial_cells | 4 | 138 |
| restriction_preserves_signed_cell_integrals | 4 | 148 |
| restriction_sheet_literal | 1 | 154 |
| restriction_refuses_changed_domain_or_missing_cells | 6 | 169 |
| complex_product_keeps_offdiagonal_imaginary_and_order | 1 | 176 |
| gram_conjugates_left_operand | 1 | 185 |
| gram_discrepancy_is_not_renormalized | 1 | 192 |
| rectangular_gram_keeps_missing_third_subspace | 1 | 201 |
| density_bond_coherence_conjugation_and_unitary | 5 | 222 |
| unequal_dx_uses_actual_chi_for_density_and_phi_for_bond | 1 | 233 |
| scalar_invalid_inputs_are_contract_errors | 14 | 263 |
| product_refuses_implicit_copy_and_invalid_planes | 8 | 283 |
| matrix_outputs_reject_alias_and_invalid_storage | 8 | 300 |
| density_refuses_bad_scale_output_and_overflow | 7 | 323 |
| bond_refuses_bad_physical_inputs_and_output | 10 | 352 |
| density_mixed_complex_row_uses_conjugation_and_scale | 1 | 359 |
| gram_rank_deficiency_is_retained | 1 | 366 |
| product_three_by_three_zero_is_known_not_missing | 1 | 373 |
| product_overflow_is_not_a_finite_measurement | 1 | 380 |
| partial_annuli_keep_signed_weighted_numerator | 1 | 384 |
| partial_spatial_overlap_keeps_uncovered_strips | 1 | 391 |
| restriction_cell_cap_rejects_lengths_before_element_reads | 1 | 419 |

Итог log: `95 failed, 2 passed in 1.69s`; progress начинается `..`. Полный failure census исчерпывает95 API cases. Два оставшихся frozen tests — `test_literal_normalization_oracle_control` и `test_literal_signed_and_partition_oracle_control`; поэтому они идентифицируются как PASS. Quiet log не печатает отдельные PASS node rows: идентификация опирается на frozen source+полное исключение всех остальных95+итог, а не на выдуманный verbose receipt. Error/skip/xfail/xpass/collection surprise отсутствуют в полном итоговом составе; negative `pytest.raises(ContractError)` не поглотил missing-API assertion.

## Source/env/ownership и ограничения

Единственный target: selected prepared `.venv/bin/python -m pytest -q --tb=short -p no:cacheprovider tests/test_equilibrium_map_math.py`, cwd exact worktree; child exit1 ожидаем именно для RED, не сам по себе доказателен. Clear env задаёт candidate/src PYTHONPATH, selected Contracts source env, отключённый plugin autoload/bytecode, hashseed0, BLAS/OMP/MKL/NUMEXPR1 и owned HOME/TMPDIR. Нет maxfail/filters/повторного запуска.

Всем95 API cases setup дошёл до wrapper `_candidate=None`. Поэтому Results package origin assertion fixture43 прошёл; unexpected import/source exceptions setup не наблюдались. Origin candidate module не проверялся по ветке импортированного module: module отсутствовал, что подтверждено guard и actual source inventory. **Contracts actual imported origin отдельно не утверждается:** fixture только импортирует messages.ContractError, guard/source env freeze сам по себе origin не доказывает; это известное ограничение accepted guard. Оно не меняет structural missing-API outcome, но последующий GREEN нельзя описывать как независимую проверку Contracts origin без дополнительного свидетельства.

Receipt: target_calls1,attempt_consumed=true,calls88→89,ceiling90,no_rerun=true; source8,C08=8/8/scientificCI0 сохранены по поручению. Root107 и predecessor hash отражены в receipt/validation; review не читает и не меняет CP, не переоформляет счётчик или grant.

Capture_complete=true,collector_terminal=true,raw_capture_error/guard_error/stop_reason=null; raw bytes/hash совпали с actual file. Guard wall2.328175543s; pytest1.69s — разные часы. RSS47 attempted/47valid/0unknown, sampled peak62525440B; одна explicit post-poll N/A с returncode1 не заменена0. TMP49 samples, logical regular-file peak/initial/final0. Эти измерения не доказывают hard/transient RSS/TMP peaks, physical I/O, filesystem isolation либо escaped descendants. Caps90s/1CPU/RLIMIT_CPU90/sampleRSS1GiB/TMP32MiB/raw2MiB не превышены по сохранённым наблюдениям; aggregate180s/4MiB остаётся обязанностью Root. Unknown resource/capture outcome здесь не заявлен.

Review выполнял только text/Git/hash/count utilities и запись двух `/tmp` outputs. Новых runtime/import/parser/math/script/pytest/network/native/subagent вызовов нет; product/index/CP/source не менялись. Ошибки `rg` о несуществующем conftest — read-only inventory diagnostics, не target errors. Source reads меньше1MiB; hard CPU/RSS reviewer не измерялись.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Structural new API RED наблюдён | Full95node/message/line census;2PASS summary;exit1 | Отсутствующий новый API, не physics defect | сохранить |
| Capture пригоден для следующего bounded source-I8helpers | Frozen F2,origin setup,matching receipt/log/H/P/refs | Grant/READY оформляет только Root | сохранить |
| Все import origins и hard resource peaks доказаны | Results assertion;sampled telemetry | Contracts origin/hard peaks не доказаны | данных недостаточно |
| Behavioral/scientific/native correctness получена | Product отсутствует;science executions0 | RED не проверяет численные helpers | данных недостаточно |

STOP. Rerun и GREEN этим review не выполняются и не разрешаются.
