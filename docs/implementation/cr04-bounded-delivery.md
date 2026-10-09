# CR04: конечное ожидание delivery и неопределённый исход

Owning draft PR: [Platform #6](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/6).
Baseline — Platform gitlink root `24b6dc1`; final owning source определяется gitlink интеграционного
commit. CR05 profiles и immutable release/Code identity сохранены.

Native command adapter ограничивает combined stdout/stderr и ожидание child/pipes, сохраняет
nullable returncode и bounded prefixes, завершает свою local process group и проверяет её состояние
в исходном cleanup reserve. Delivery использует один monotonic deadline и output budget для
phases/nodes, bounded SSH options и отдельный NIX_SSHOPTS env. Injected `run(args)` interface
сохранён.

Private per-attempt receipts сохраняют running/pending/terminal evidence. Unknown remote outcome
прекращает dispatch и требует trusted reconciliation; остановка SSH не доказывает завершение remote
mutation. Отдельный durable admission intent публикуется до открытия gate и блокирует retry при
failure финальной gate/receipt publication. При доступном storage выполняется одна попытка закрыть
gate; неподтверждённое закрытие отображается как critical unknown. CLI использует current safe
in-memory summary, без вывода старого `open:false` из предыдущего report. Без текущего свидетельства
выводится unknown.

Defaults: command 360 s с cleanup reserve 2 s; delivery 1800 s; combined output 1 MiB/command и 8
MiB/delivery. CPU/RAM caps не вводились. Command flags проходят native CLI actions; delivery
deadline не передаётся normal worker shutdown, который продолжает ждать scoped safe-stop без
конечного внешнего timeout.

## Локальные свидетельства

| Проверка                                | Результат и применимость                                                                           |
| --------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Первичный RED                           | 43 tests, 29 expected missing-interface errors                                                     |
| Initial GREEN attempt                   | 46 tests, 2 failures; original log сохранён                                                        |
| Исправленный targeted                   | 46 passed, 1.504 s                                                                                 |
| Единственный full local check           | 22 Deno; 255 Python passed, 5 skipped, 174 subtests; до последующих review fixes                   |
| Isolated post-dispatch deadline concern | 1 passed, 0.021 s                                                                                  |
| Review fixes                            | 3 focused passed; затем 50 application tests passed, 1.556 s; offline format/lint/typecheck passed |
| Последний combined CLI failure fixture  | 51 application tests passed, 1.587 s                                                               |
| Independent final focused review        | actionable findings отсутствуют в bounded scope                                                    |

Первый GREEN проверял descendant сразу после SIGKILL; исправлена конечная acknowledgement проверка
без ослабления отсутствия живого child. Production adapter отдельно подтверждает group cleanup.
Fake-clock ожидание разделено по phase: failure до maintenance сохраняет gate, после закрытия —
closed state. Независимый review затем выявил gate replace→fsync/terminal checkpoint failure,
pre-spawn environment facts и потерянные CLI flags; новые fixtures исправили их. Повторный review
обнаружил stale CLI summary при combined storage/close failure; последний fixture проверяет actual
main, unknown stdout, exit 1 и отсутствие следующего dispatch. Failed receipts и все предыдущие
diffs сохранены.

Бюджет: initial 4 targeted + 1 full; отдельно назначены 2 review-fix targeted и 1 финальный
targeted. Полный suite не повторялся: final source имеет адресные 51 tests и static review evidence,
а не final full-suite evidence. Последний format check нашёл только reflow документа; coordinator
исправил его formatter, не меняя code/tests и не повторяя runtime.

SHA256 original full log: `c150b29c9ef1c6c7361f273eeb8847560a8e84053d770704c2bf1d03da074713`. Final
targeted log: `d86bd41628a6c1533b2ba15eb56059a521ed01168d40d798346ae0eae575c4be`. Publication diff:
`80a61fb54ba751248d05542c5c5345e8e8e08dd03aef4a20730735b81f20734b`. Полные original diagnostics
остаются локально, с ограничениями приватности.

Actual Nix/SSH/services/VM, solver, deploy, merge и final CI не выполнялись. CR02 lifecycle, CR03
enrollment, whole-cluster I14 и trusted reconciliation implementation остаются отдельными gates.
Linux /proc visibility обязательна; stalled kernel/filesystem не дают hard real-time. Broken storage
не позволяет гарантировать сохранность или закрытие gate; это unknown, не pass.

| Утверждение                                                  | Свидетельство                                                     | Ограничение                                    | Решение             |
| ------------------------------------------------------------ | ----------------------------------------------------------------- | ---------------------------------------------- | ------------------- |
| Child/pipes и diagnostic output ограничены                   | Native analytic child/cap/group fixtures, scoped code review      | Linux evidence; не hard real-time              | изменить            |
| Unknown mutation блокирует новый dispatch/retry              | Failure/receipt fixtures и durable guard                          | Remote reconciliation требует trusted evidence | сохранить           |
| Final publication failure не подменяет unknown закрытым gate | Deterministic replace/checkpoint/failed-close и real main fixture | Broken storage не гарантирует durable write    | сохранить           |
| CR05/immutable identity/normal safe shutdown сохранены       | Existing targeted regressions и scoped diff                       | Нет actual production experiment               | сохранить           |
| Final full release/scientific acceptance достигнута          | Такие свидетельства отсутствуют                                   | Earlier full check не final full gate          | данных недостаточно |
