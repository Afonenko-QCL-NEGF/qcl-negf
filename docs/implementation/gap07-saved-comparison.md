# GAP07: сравнение готовых report snapshots

Runner добавляет `compare_saved_results(CATALOG.csv, OUTPUT; reference_id)` и
`qcl-negf compare CATALOG.csv OUTPUT --reference-id ID`. Frontend читает только готовый legacy
report catalog и materialized summary CSV. Explicit plan/run-plan остаются отдельными compute
routes; legacy `run_comparison_study` сохраняет compute behavior с предупреждением до execution.
Runtime этого warning отдельно не проверялся. Новый путь не достраивает недостающие результаты
solver/optics.

Каждый canonical input path captured bounded один раз; SHA и parser используют те же bytes. Default
общий input limit 16 MiB — engineering read budget. Matching atols сначала проверяются как finite
nonnegative Real и effective Float64; это locator tolerances K/V, не scientific thresholds.
Reference обязателен; ambiguous coordinates, несопоставимые declarations и insufficient data дают
явную ошибку до report publication. Missing/nonfinite остаются unavailable; reference=0 не создаёт
относительную точность. Failed/unconverged source points сохраняются как descriptive observations.
Report показывает обе coordinates, signed deltas, caller/effective atols и компактные
path/SHA/byte-count selectors. Native execution/attempt/branch/commit и полная model/scientific
identity недоступны в этих CSV: provenance scope `declared_saved_report`.

`analysis_status=completed|partial` относится к выполнению сравнения, не к
SCBA/Poisson/physics/discretization/experimental acceptance. Markdown использует формулировки
differences/unverified declarations. После review исправлена запись completed Markdown до coverage:
final completion-bearing Markdown атомарно публикуется последним. Failed CSV writes могут оставить
частичные CSV; общей транзакции/rollback/durable scientific bundle этот путь не обещает.

Изменены семь owning Runner paths. Initial RED отсутствующего API, original GREEN120, metadata-only
return GREEN121 и I/O RED123/1fail → GREEN124 сохранены отдельно. Review обнаружил auto-include
fixture pollution: старый fixture менял production methods в общем процессе. Actual include RED
дал124 fixture pass, затем11 caller failures; исправленный wrapper выполняет intrusive body в одном
bounded Julia child. Fresh final evidence: child124/124 и caller11/11; parent methods/capture
table/seven bindings неизменны. Body byte-identical исходным124 assertions, actual saved
frontend/CLI/writers проверяются. Backend tripwires покрывают configuration/problem entry;
отсутствие direct solve/derive также проверено по source. Full shared/scientific suite не
выполнялся.

Child наследует selected Julia/project/environment и allocated thread counts;
deadline180s/output128KiB, outer verification240s/128KiB. Последняя narrow поправка сохранила
original normal-completion child log после caller exit:635bytes, SHA
`de280217428d5159a12dd4e94b6d01b2e024784171c9a73dc3094aada0feec2c`. Deadline/overflow/reader-fault
branches проверены по source, не отдельным runtime. Cached StyledStrings warnings и intentional CLI
errors сохранены. CPU/RAM не ограничивались искусственно; peak resources not_measured. Scientific
attempts0, новых installs/downloads/server actions/CI/deploy/merge нет.

Final seven-path diff SHA256: `224bd7451af71a2e0d3efada95a0db06804bb5fc6c77d7a5debe0cfa1f758e18`.

| Утверждение                                       | Свидетельство                                                 | Ограничение                             | Решение             |
| ------------------------------------------------- | ------------------------------------------------------------- | --------------------------------------- | ------------------- |
| Saved compare не заполняет пробелы расчётом       | Actual API/CLI124 assertions, entry tripwires и source review | Toy CSV, no native adapter              | изменить            |
| Анализ не выдаёт scientific certificate           | Raw status/coverage/declared provenance assertions            | Полная native/model identity недоступна | сохранить           |
| I/O failure не публикует новый completed Markdown | Real coverage-error RED → GREEN; atomic-last source           | Partial CSV возможны                    | сохранить           |
| Fixture не меняет caller methods/bindings         | Actual include11/11 и bounded child124/124                    | Не full scientific suite                | сохранить           |
| Scientific/production приёмка установлена         | Таких свидетельств нет                                        | Scientific attempts0                    | данных недостаточно |
