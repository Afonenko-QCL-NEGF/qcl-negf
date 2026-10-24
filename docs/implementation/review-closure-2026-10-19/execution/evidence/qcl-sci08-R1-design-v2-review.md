# SCI08-R1 D2 — focused independent high source rereview

**Вердикт: PASS_SOURCE.** P2 из предыдущего review закрыт additive design correction. D1+D2 образуют принятый узкий source contract для последующего owning I. Это не утверждение, что fixture уже изменён или выполнен. Product diff, ENG_READY, полный SCI08 guard, S1/native admission и scientific acceptance этим review не установлены.

| Frozen input | SHA256 |
| --- | --- |
| D1 `/tmp/qcl-sci08-R1-design.md` | `16b07bbafce8235e0e103205e90c5b6e6b0db6c13c5bd4c883074f32888fe3c7` |
| Prior R `/tmp/qcl-sci08-R1-design-review.md` | `a68ecf63af984355148b46d4a943cc5ca35adbe9da80102c512858d2b4847d69` |
| D2 `/tmp/qcl-sci08-R1-design-v2.md` | `5a50afe3ca4014991dcb61d6dfb2879b2fef99e10f18347b5aa5d4eefe54d642` |
| D2 identity | `56a018f3eb0b09d6904e2137709619f8afafda2e2b725cd4554783fd409d516f` |
| D2 delta/readledger | `8284573df9b482e38fa09317d63fe70c0702384b9b41732dd1cf8f5aa7239533` |

Runner HEAD заново подтверждён: `fefaa27f194bfddf85dd51a0e255beef2218c06d`, status пуст. Три relevant whole-file SHA совпали с D1/D2: `linux_resources.jl` eed7dc41…; `native_phase_telemetry.jl` 9605f1a4…; `execution_resource_contract.jl` c6eabaad…. Current coordinator Root не используется как изменившийся source input; historical observations и D1 bytes не переписаны. Это focused correction review тем же независимым reviewer, не новый полный аудит Runner/SCI07.

P2 был воспроизводим по immutable test/application/execution_resource_contract.jl:135 → src/composition/native_phase_telemetry.jl::_native_phase_request → linux_resources.jl::_process_cgroup_path/_resource_read. Callback constructor читает cgroup membership ещё до directory=nothing skip. D2 требует в этом существующем fixture создать tiny `fake_proc/self/cgroup` с literal `0::/fixture.slice/solver.scope`, fake directory chain и передать **оба** roots явно в реальный callback. Это устраняет default `/proc` read по названному пути без изменения production lazy-read policy.

Независимая source трассировка correction: `_process_cgroup_path(fake_proc)` читает только `joinpath(fake_proc,"self","cgroup")`; после удаления leading slash relative становится `fixture.slice/solver.scope`. `_cgroup_ancestors(fake_cgroup, relative)` вычисляет цепочку fake leaf → fake slice → fake root. Сам этот helper directories не читает. При callback с directory=nothing memory permit возвращается до чтения memory files. Следовательно tiny fake membership file и явные roots достаточны для исходного width testset. При future I требуется подтвердить те же реальные variables/call path на exact candidate; это не заменяется авторской prose или counter assertion.

D2 сохраняет четыре behavior checks и ровно четыре callback invocations. Attempted/completed counters после healthy cases 3/3, после invalid width0 4/3 — полезный дополнительный witness внутри L2. They demonstrate continuation ordering только в дополнение к реальным callback outcomes. D2 явно говорит, что counters не доказывают отсутствие host reads, запрещает global Base.read monkeypatch и production observer ради теста, требует source trace и закрывает ENG_READY при неизвестной трассировке. Это корректно разделяет evidence.

Пять named includes и31 required property groups остаются прежними: assertion count может увеличиться внутри L2. Ни новые test groups, ни whole-suite invocation, ни solver work не добавлены. Tiny fake file/directories укладываются в прежний proposed fixture-write budget; runtime fit не измерен. Future I review должен проверить также отсутствие default-root callbacks во всей выбранной selection. Ранее проверенные Linux/integration fake fixtures не нуждаются в новом host reading или новом native механизме для этой correction.

TDD абзац не выдаёт execution grant: D1 single GREEN — tentative proposal, двухвызовный RED/GREEN — альтернативное предложение, commands/counts/общий finite budget/stop/exact candidate устанавливает отдельное решение Root. Behavioral RED должен различать baseline defect, а не undefined new helper/import error. Source D2 не подтверждает RED/GREEN и не добавляет вызов к одному из grants. Ни C08, ни SCI attempts не открываются. Конкретный ENG protocol остаётся решением координатора; этот review его не выбирает.

D1 checked arithmetic/independent oracles, strict unknown refusal и separate standalone policy сохранены. Strict campaign entry остаётся closed needs_guard/needs_admission; actual allocator/writer seam witness и R2/R3/P1/P2/A1/C1 integration всё ещё обязательны. Новый trust root/private schema/lease ledger не введён. All S1 model/criteria/caps и C08 exhausted8/8 не меняются: correction касается fixture membership paths и его evidence, не физических параметров, дискретизации или научных gates.

Source/text/hash/Git metadata only. Target runtime/import/parser/tests/build/solver/native/network/product/CP/Git mutations=0; только два requested /tmp outputs. Прочитаны D2+identity+delta полностью и три narrow immutable source ranges; D1/prior R semantics сохранены из предыдущего review, D1/prior R hashes пересчитаны. Conservative full-file read charge с metadata/output reserve≤262144B<1MiB. Physical I/O/CPU/RSS не измерены. Scope5min/1CPU/1GiB/report64KiB; target execution не выполнялся.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| P2 design устраняет default /proc path | D2 two explicit roots + source trace выше | Fixture implementation ещё нет | сохранить |
| Counters не подменяют read coverage | D2§override4–5 | Нужен exact future I caller trace | сохранить |
|31 groups/standalone/model/caps неизменны | D2 preserved predicates, immutable D1 | Runtime regressions не выполнялись | сохранить |
| RED/GREEN test grant установлен | Отдельный plan только предложен | Root decision/candidate/envelope отсутствуют | данных недостаточно |
| Полный SCI08/S1/native guard готов | Остальные owning guards не входят в D2 | needs_guard/needs_admission сохраняются | данных недостаточно |

STOP. PASS_SOURCE закрывает P2 на design уровне; разрешения запускать tests/native/science или менять product/CP не даёт.
