# SCI08-R1 D2 — fake-only fixture correction

Статус: **D2_READY_FOR_FOCUSED_HIGH_REVIEW**. Это additive override ровно одного
P2 finding из `/tmp/qcl-sci08-R1-design-review.md`; D1 не переписывается.
Source/text/Git/hash reading only; product/CP/runtime/parser/tests/native/network=0.

## Frozen input и проверенный finding

| Input | SHA256 |
| --- | --- |
| D1 `/tmp/qcl-sci08-R1-design.md` | `16b07bbafce8235e0e103205e90c5b6e6b0db6c13c5bd4c883074f32888fe3c7` |
| D1 identity | `bba244acc5e66421db0c460f128578ebfd06c120434107fbc8be4790a7141cc1` |
| D1 readledger | `f7565807b887c928e3fc63ec11181c3af0700cf152f0218d396ccdd4ba3860e2` |
| Independent high R | `a68ecf63af984355148b46d4a943cc5ca35adbe9da80102c512858d2b4847d69` |

Finding подтверждён без исполнения: Runner fefaa27,
`test/application/execution_resource_contract.jl:134–140` создаёт
`_native_phase_request(nothing)` без roots. Конструктор
`src/composition/native_phase_telemetry.jl:138–145` сразу вызывает
`_process_cgroup_path(proc_root)`, а `linux_resources.jl:44–56` читает
`joinpath(proc_root,"self","cgroup")`. Default `/proc` читается до memory skip.
Поэтому прежний exact selection D1§6 ещё не соответствовал fake-only обещанию D1§5.

Runner HEAD `fefaa27f194bfddf85dd51a0e255beef2218c06d`, status пуст;
три relevant source/fixture hashes совпали с D1. Managed Root теперь
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`; dirty coordinator CP/census/manifest и
evidence edits сохранены. D1 historical Root469 не переписывается в current HEAD.
Fresh recursive submodule metadata снята, composition authority остаётся Git.

## Единственный scope override к D1§6, L2 и L3

В future Runner I diff **обязательно** исправить выбранный existing fixture
`test/application/execution_resource_contract.jl`, testset
`"Phase width respects the fixed Julia pool"`:

1. В `mktempdir` создать отдельные `fake_proc` и `fake_cgroup`, оба под этим
   temporary root. Создать `fake_proc/self/cgroup` с tiny literal
   `0::/fixture.slice/solver.scope\n` и соответствующие fake cgroup directories.
   Эти bytes — fixture, не observation хоста. Directory=nothing legacy path не
   требует memory files: этот testset проверяет width/unavailable behavior.
2. Создать callback только как
   `_native_phase_request(nothing; proc_root=fake_proc, cgroup_root=fake_cgroup)`.
   Оба keyword задаются явно; передать лишь один root недостаточно. Не оставлять
   default-root invocation рядом как positive/negative control. Никаких `/proc`,
   `/sys/fs/cgroup`, actual diskstat или host-resource reads для этой correction.
3. Сохранить четыре существующих behavioral assertions: width1→1,
   width=pool→pool, width=pool+1→pool, width0→ArgumentError. Directory=nothing
   продолжает standalone unavailable semantics; production callback lazy-read
   поведение ради этого fixture не меняется. Строгая policy D1 неизменна.
4. В том же testset добавить test-local attempted/completed continuation counters.
   Перед каждым из существующих четырёх callback invocations increment attempted;
   completed increment только после successful return реального callback.
   После трёх healthy widths assert attempted=completed=3. После width0 assert
   attempted=4 и completed=3. Таким образом positive witness выполняется, а negative
   не достигает continuation. Это дополнительный assertion witness внутри L2,
   не новая группа, не дополнительный callback вызов, не новый target process call.
   Assertions проверяют actual callback results; counters не заменяют эти результаты.
5. До ENG_READY owning I diff/source trace должен подтвердить, что выбранный
   callback получает именно эти две fixture variables и `_process_cgroup_path`
   достигает только fake `self/cgroup`. Показать exact caller→constructor→read
   path и normalized ancestor chain внутри `fake_cgroup`. При наличии test-local
   read tracing использовать только уже поддерживаемую fixture seam; не monkeypatch
   global Base.read, не добавлять production observer ради теста. Сам по себе
   continuation counter **не доказывает** отсутствие host read; это source-trace
   obligation плюс явные roots. Если trace остаётся неизвестен — ENG_READY закрыт.

Healthy/assertcounter witnesses требуют нулевого solver work. Temporary fixture
добавляет один tiny text file и directories внутри прежнего16MiB write proposal.
Existing Linux/integration fixtures в selection по-прежнему используют fake roots;
focused I review проверяет, что после edits никакой включённый callback не вернулся
к default roots. Пять includes и31 property groups сохраняются; assertion count
будет дополнительно bound по final I diff, как требовал D1.

## TDD и будущий engineering plan

D1§6 single-process GREEN command/envelope остаётся **tentative proposal**, не
принятый execution protocol и не исключение из TDD. Source D/D2 не наблюдали RED
или GREEN. Нельзя трактовать D1 как разрешение написать production code до
различающего RED evidence или как готовый runtime grant.

Координатор может вместо этого отдельно принять конечный **двухвызовный RED/GREEN**
engineering plan: exact RED test/source candidate, затем exact GREEN candidate,
общее finite resource/output envelope и supervisor stop, без reruns. RED должен
показать требуемое behavioral failure на baseline (например, запрещённый Bool
в existing forecast input), а не undefined new helper, import/configuration error
или отсутствие среды. Healthy control и полный31-group denominator остаются
обязательными в accepted selection. Конкретные commands, counts и общий бюджет
обоих вызовов устанавливает этот отдельный plan, а не D2.

Этот текст **не добавляет** вызов к D1 proposal, не выбирает второй plan, не
выдаёт approval и не открывает C08. Пока finite RED/GREEN plan не bound/authorized,
настоящая реализация и её checks не могут ссылаться на D2 как на TDD exception.
Runtime stages/полные suites не запускаются по общему skill требованию в обход
явно заданной project cost boundary. Если позже принят другой test protocol,
сохранить D1/D2 и original receipts, а актуальный grant записать отдельно.

## Сохранённые predicates и пределы

Остальной D1 сохраняется: checked arithmetic/oracles, strict unknown refusal,
separate standalone policy, actual allocator/writer seam witnesses, exactly31
groups и five named file selection. Изменённый fixture становится частью owning
Runner I candidate до ENG_READY. Один writer/отдельный high review и общий SCI08
≤2 code rounds не меняются. Full campaign remains needs_guard/needs_admission;
R2/R3/P1/P2/A1/C1 не закрываются этой correction.

S1 сохранён:0mV/period, lattice/LO70K, LO/acoustic/impurity/IFR/alloy,
electron_electron=none;13 attempts/936 execution node-hours/72h attempt/concurrency≤2,
one threaded process/node/BLAS1. W1 четыре128GiB/2TiB writes/4TiB reads/1GiB logs;
остальные девять256GiB/4TiB/8TiB/1GiB. Shared2TiB/44TiB/88TiB/13GiB, stop внутри
прежних caps. Physics/grids/basis/window/mixing/tolerances/acceptance неизменны.
C08 exhausted8/8. Science attempts/tests/native calls этой correction равны0.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| P2 real-/proc путь подтверждён | Immutable fixture135→constructor144→resource read | Runtime не выполнялся | изменить |
| Future selection станет fake-only | Explicit two roots + source trace + width/counter witnesses | I diff и focused rereview ещё нужны | изменить |
|31 groups/standalone/S1 сохранены | Узкий override выше и D1 | Нет нового test/native grant | сохранить |
| TDD уже выполнен или RED/GREEN разрешён | Ни одного target call | Separate finite plan не принят D2 | данных недостаточно |

STOP. Только additive D correction и два accompanying evidence files; далее focused
source rereview тем же независимым high reviewer, без runtime/product/CP действий.
