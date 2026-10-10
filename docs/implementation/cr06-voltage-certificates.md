# CR06: voltage predecessor certificate

Owning draft PR: [Runner #5](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/5). Baseline
— Runner gitlink root `d06f182`; result определяется gitlink интеграционного commit.

Legacy voltage `:research` finite predecessor policy retired явно. Executable plans используют
`:independent` или `:strict`; typed load/resume старого research plan возвращает named error, без
policy alias, переписывания identity/fingerprint или result bytes. Independent Results/raw чтение
сохранённых данных остаётся отдельным путём. Inner SCBA→Poisson policies и Core evaluator не
менялись.

Strict predecessor eligibility явно усилена: один private gate для live и completed restore читает
already-produced Core stationary assessment и проверяет registry version, четыре ready Bool
summaries, whole/inner status/flags/quality. Live использует настоящий final report. Restore
удерживает assessment из verified commit, проверяет original flags и series metadata и не фабрикует
ConvergenceReport из старого флага. После успешного gate восстановлен только warm seed `Uᴴ/scba`,
который требуется существующим consumers.

Новый gate не содержит формул, новых thresholds/evaluator и не требует full
`scientific_accepted=true`: discretization, FD/FDR S01 и experimental evidence отдельны. Full S06
branch stop/error при failure, cold fallback и skip остаются follow-on; этот PR не устанавливает всю
S06 приёмку.

## Проверка и ограничения

| Проверка                                              | Результат                                                                          |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Genuine RED                                           | 5 pass / 5 fail / 10 total, 0 errors; 12.322 s                                     |
| GREEN                                                 | 233/233: 10 constructor и 223 status/adapter/certificate assertions; 11.534 s      |
| Диагностический объём двух вызовов                    | 7169 bytes; finite budget 2 calls, 60 s/call, total 64 KiB                         |
| Static module/caller/producer checks и diff check     | Соответствуют scope; whitespace без ошибок                                         |
| Независимый final review frozen files/hashes/receipts | Blocking findings отсутствуют                                                      |
| Public diff audit                                     | Known secret patterns/configured sensitive literals и private endpoints не найдены |

Fixture включает actual Base-only contracts и dependency-free production helper, imports только
Test. Oracle — hand-literal expected eligibility table. Проверены actual terminal/transient/unknown
statuses, inconsistent flags, false/missing/ not_measured/non-Bool assessment, registry mismatch,
commit/saved/series metadata и temporary restart status при original strict certificate. Scientific
false, discretization not_measured и historical warnings не превращаются в pass.

Новых Core/Runner imports, HDF5/CLI/frozen archive integrations, operators, solver, full suites,
installations, benchmarks, server/CI/deploy не выполнялось. Эти integration пути проверены только
статически. Шесть stdlib StyledStrings/Logging warnings в original logs сохранены; environment не
объявляется warning-free. Исходный RED показывает constructor/helper absence, не characterization
старого private eligibility predicate.

SHA256 original local logs:

- RED: `90091c9426dcec7bb44d69c190a11d1715dad5910671b320d3852eb10d1aae31`.
- GREEN: `436c40cb212b85355a56a2e13cb45061568eb12c053594839ff60ae0780cd3d6`.
- Frozen diff: `14c95fc89e052e244e3a64217883b94b113dccf257727cf561afa047aa52f109`.

| Утверждение                                           | Свидетельство                                                | Ограничение                                        | Решение             |
| ----------------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------- | ------------------- |
| Research policy не переинтерпретирует old frozen plan | Actual constructor fixture и static parser/load routing      | Старый archive не исполнялся                       | изменить            |
| Live/restore имеют единую certificate authority       | Actual helper, 223 assertions, Core producer/storage anchors | Metadata scope; existing verifier/producer trusted | изменить            |
| Synthetic restored report удалён                      | Scoped source diff и warm-seed consumer review               | Без HDF5/live integration                          | сохранить           |
| Core/model/thresholds и historical evidence сохранены | Six-file Runner diff; schema/fingerprint paths untouched     | Не numerical validation                            | сохранить           |
| Whole S06/S01/scientific acceptance достигнуты        | Таких свидетельств нет                                       | Follow-on/compute evidence отсутствуют             | данных недостаточно |
