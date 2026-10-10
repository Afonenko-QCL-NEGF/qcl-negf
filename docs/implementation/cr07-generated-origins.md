# CR07: происхождение generated overrides

Owning draft PR: [Runner #4](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/4).
Независимое review не нашло actionable findings для schema-valid inputs; публичные
code/fixture/report проверены на known secrets и private endpoints.

Runner `definitions.jl:resolve_scientific_configuration` и `_scientific_single_study` используют
existing `_deep_merge!` для generated run identity, convergence policy, temperature axis, study и
output fields. Stable labels `#generated:<policy>` называют механизм присваивания, а не источник
физических данных. Copied photon controls сохраняют прежние histories. Quantity mapping→scalar
удаляет phantom descendant origins по существующему merge contract. Provenance schema остаётся
прежней; full plan fingerprint может измениться вслед за исправленной history.

Baseline определяется Runner gitlink root `24b6dc1`; final owning source — gitlink интеграционного
commit. Валидные effective inputs, precedence, units, first-axis выбор и физическая модель
сохраняются. Unsupported extra key в late study.convergence override, который раньше молча удалялся
whole-Dict replacement, теперь достигает существующего parser и отклоняется. Эта граница установлена
статически; runtime case для malformed override не выполнялся, schema не менялась.

## Локальная проверка

Exact cached Julia 1.13.0 проверена по owning bootstrap checksum; source paths Runner/Core
подтверждены в isolated worktree. Использованы existing immutable depot и temporary overlay, offline
mode, без установки зависимостей. Fixture вызывает только configuration/planning/freeze/load, без
operator/solver execution.

| Проверка                      | Результат                                         |
| ----------------------------- | ------------------------------------------------- |
| Genuine RED до patch          | 67 pass / 32 fail / 99 total, 0 errors; 103.309 s |
| GREEN после patch             | 99/99 pass, 0 errors; 99.084 s                    |
| Scoped Deno cached-only check | exit 0, 0.527 s                                   |
| Diff check                    | exit 0                                            |

Oracle задаёт вручную expected raw values/history: base 70 K → definition 180 K → variant 190 K →
inherited 195 K → generated 200 K, обе температуры; весь generated набор; unchanged
numerical/scattering/photon controls; mapping cleanup; четыре planned executions и сохранение
sources после freeze/load. Solver/S01, полный Julia suite и production проверка не выполнялись.

Три native invocations: initial cache failure без assertions, RED и GREEN. Первый file-size
ограничитель ошибочно затронул Julia compile cache и завершил StyledStrings precompile сигналом;
original log сохранён. После отдельного budget ruling применён stdout/stderr-only capped supervisor,
180 s/2 MiB на invocation, без file-size limit. Более ранний wrapper с отсутствующим time binary не
запускал Julia. Два StyledStrings warnings в genuine RED/GREEN сохранены, не подавлены.

Original logs остаются локально; SHA256:

- Initial native failure: `a4f78532b60a3073d49b61b4e73d7e78ab97288542debabfd87ab490cffef756`.
- Genuine RED: `3f4615dd8b4a69ea96a150481ddad6380a94237a8caf372515d9ea4f0a7ad197`.
- GREEN: `4924d89735682bc61613019d695c3423019fc42a6fd2ff3ac4edd59e16ce8909`.
- Deno check: `80dd525accf2943059a5e8c9e89f44ed19151289ce1adfe25fbae2317984d425`.

| Утверждение                                                 | Свидетельство                                          | Ограничение                                                                   | Решение             |
| ----------------------------------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------------- | ------------------- |
| Effective generated leaf имеет truthful assigning authority | Hand-written history assertions; RED32fail→GREEN99pass | Engineering origin label, не физический reference                             | изменить            |
| Valid raw inputs и untouched histories сохранены            | Fixture literals и scoped source diff                  | Не все допустимые конфигурации; malformed extra key меняет rejection boundary | сохранить           |
| Frozen plan сохраняет origins                               | Public planning/freeze/load four-execution fixture     | Execution/recovery не проверялись                                             | сохранить           |
| Научная/production приёмка достигнута                       | Свидетельства отсутствуют                              | Metadata scope                                                                | данных недостаточно |
