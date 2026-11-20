# Warm128 max26: independent static delta

Initial reviewed freeze: driver `0a73ca830ea2b881a65d0c2c197ac5d9c8bb5d0fb74c305067e3507fbdf99ba9`, loader `64f33caa948f3d12adf585572a10439e630452f3999f971eb8c59bfbab460630`, false bound input `922e662ee83bfc9d5dc0faa8f933c2a3d3f6c313f4766ae68a9456ba9b8bcd09`. **HOLD actual для этого freeze:** обнаружен детерминированный parent resource-contract mismatch; нужна минимальная отдельная delta. Reviewer не запускал Julia/Pkg/solver/large-HDF reads.

## Устранённые прежние findings

Loader V2 проверяет metadata shape обоих real/imag datasets до GP.read_complex; тем самым singleton broadcasting больше не обходит shape guard. Tiny negative fixtures покрывают singleton с обеих сторон. Driver/comments/input верно различают128fresh map evaluations, первая повторяет parent boundary, т.е. максимум127новых Green states иnominal global iteration159 после parent32. Native equations и max128 не меняются.

## Blocker actual parent

`warm_initial.jl::parent_contract` inherited-equality loop не исключает `memory_max_bytes` и`memory_high_bytes`. Для **обоих** фактических frozen parents проверен text/TOML конфликт:12616466432/12348030976B против новых23085449216/22548578304B. Поэтому actual заведомо завершится ошибкой `warm changed inherited frame/control` после source hashing. Новый tiny, строящий parent с новыми caps, этого не обнаружит.

Минимальное закрытие: явно проверить ровно объявленную parent11.75/11.5→child21.5/21GiB пару и исключить **только эти два** поля из inherited equality; tiny может иметь совпадающую новую пару только в tiny-ветке. Остальные physics/grid/algorithm/units/ownership проверки не ослаблять. Root уведомлён до actual; reviewer исходники не правил.

Малые input/identity/summary/driver whole SHA обоих parents независимо совпали с bound input; state/model hashes совпали с owning summary. Большие stateSHA здесь не перечитывались; runtime loader обязан сверить их перед arrays. Voltage/remaining inherited controls уже согласуются.

## Остальная delta

AlgorithmOptions/all5/noEE/U0/N24001/directC/LO PIFFT/finitechain4/α0.2 и native raw gates не изменены. Parallel worker/capacity/thread identity4→26, CPU≤2600%, BLAS1; hard21.5GiB=23085449216B/high21GiB=22548578304B, reserve1468006400B, native budget21617442816B. Это изменение исполнения, не обещание ускорения или roundoff equivalence. Exact built-cache/native guard, mandatory plan/tiny и свежая host/data admission остаются за Root. Same-voltage parent4Green иall24Σ загружаются без FD/interpolation/repair; boundary replay затем измеряет фактическую совместимость.

Metadata callbacks не участвуют в acceptance. Но заявленная cadence8 **не сокращает** фактические marker вычисления: production_solver задаёт `_ensure_scba_physical_markers!(terminal=decision.terminal||checkpoint_due)`, а harness checkpoint_request=true накаждомmap. Поэтому markers и balance callback останутся практически накаждом completedmap. Это не math blocker; нельзя приписывать каденции экономию, которой код не достигает. Raw history/gates по-прежнему everymap.

Phase timing/event_sink добавлены только для telemetry. Logger пишет `phase-events.log` вкорень package, вне per-case/pair data counter; tiny/plan/actual используют одну append-точку без voltage/attempt ownership. Root следует сохранить/разделить этот файл перед actual и не трактовать смешанный лог как чистый benchmark. Эти metadata не заменяют actual process/cgroup measurements.

128/1800s-case/4200s-global/120s-save/UTC13 и4GiBcase/8GiBpair сохранены. Parent остаётся unresolved seed; replay не scientific acceptance. Fine cancellation пользователем — прекращённый отдельный опыт с сохранёнными rawfiles, не автоматическое научное опровержение fine модели. Данная проверка не возобновляет отменённый опыт и не разрешает дополнительные процессы.
