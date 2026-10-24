# SCI08-R1 — независимый high source review

Вердикт: **REQUEST_NARROW_CORRECTION**. Основной R1 source contract пригоден для узкой реализации, но exact будущий test selection содержит один P2 разрыв fake-only границы. До correction этот D не получает PASS_SOURCE. Ни runtime grant, ни SCI08 I/ENG READY, ни scientific acceptance не установлены.

## Immutable inputs и независимость

Сначала прочитаны owning source при Runner `fefaa27f194bfddf85dd51a0e255beef2218c06d`, затем авторский design/identity/ledger. Runner HEAD совпал, status пуст. Исходники не менялись. Первичный вопрос — checked forecast и strict unknown refusal до allocator/writer при сохранении standalone semantics; первичная source оценка сформирована без готового авторского диагноза. Дополнительных агентов нет: это независимый reviewer относительно автора D, но без второй внутренней рецензии.

| Input | SHA256 |
| --- | --- |
| R1 D `/tmp/qcl-sci08-R1-design.md` | `16b07bbafce8235e0e103205e90c5b6e6b0db6c13c5bd4c883074f32888fe3c7` |
| R1 identity | `bba244acc5e66421db0c460f128578ebfd06c120434107fbc8be4790a7141cc1` |
| R1 readledger | `f7565807b887c928e3fc63ec11181c3af0700cf152f0218d396ccdd4ba3860e2` |
| SCI07 D1 | `1f569ba726873d80715523621933caa6c0a0b0ad84e5a59ba9ef077b12001635` |
| SCI07 D2 | `fc78a0c77394f4d12a1c5633b7e4acb587429667abc106f5aa72c1dc4dd9d010` |
| SCI07 high R1 | `48f97407846b4b179de2442e1295e8cc2028ed7d4e3ca9c2f28c8079ac5d4e67` |
| SCI07 high R2 | `80e2f1ca784b9c4a082d0785e6ee6bc9ceb507eeecc43c63822f65f532a1d18e` |

Initial cwd Root HEAD `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1` — иной dirty checkout, не R1 source. Наблюдённый managed Root HEAD уже `2bb05d3651af4509fe7f02c1253b40f1e5146fec`, с coordinator checkpoint/manifest и evidence/publication changes. Historical D Root469 не переписывается и не выдаётся за нынешний HEAD. Exact `git ls-tree 469ef4ec36c1dfb967856108e5f9455429559c15` независимо подтвердил Runner fefaa27 и Core9f4a96d. Все пять named Runner source SHA и четыре test/selector SHA совпали с R1 identity. Актуальное recursive submodule status снято; Contracts f4009c9 не вход в этот review. Состав по-прежнему определяется gitlinks, эта таблица — forensic evidence.

## R1 — P2: один включённый legacy fixture читает настоящий /proc

**Воспроизводимый локатор:** D:127 (`Fake paths/counters only; no actual /proc/cgroup/disk measurements`), D:196,203 (include existing `test/application/execution_resource_contract.jl`), immutable Runner `test/application/execution_resource_contract.jl:134–140`, особенно135; `src/composition/native_phase_telemetry.jl:138–145`; `src/infrastructure/resources/linux_resources.jl::_process_cgroup_path` и `_resource_read`.

Existing application fixture вызывает `_native_phase_request(nothing)` без fake paths. Конструктор выполняет `_process_cgroup_path(proc_root)` сразу при создании callback, с default `proc_root="/proc"`, до проверки `directory===nothing` внутри memory permit. `_process_cgroup_path` читает `/proc/self/cgroup`. Следовательно proposed пять includes не являются полностью fake-only, даже когда memory permit затем возвращается как unavailable. Сам источник это показывает; выполнения теста для установления пути не было. Это не научный solve и не установленный cap bypass, однако exact engineering selection противоречит собственной finite fake-only границе и содержит неописанное host observation.

**Самое дешёвое разрешение:** additive D correction должен явно потребовать в этом existing fixture передавать временные fake `proc_root`/`cgroup_root` в `_native_phase_request(nothing; ...)`, заполнив tiny fixture или явно заданные отсутствующие fake files для legacy fallback. Сохранить assertions про directory=nothing/width и standalone unavailable. Допустима эквивалентная source реализация, лениво не читающая cgroups для legacy directory=nothing, если она отдельно проверена и не меняет strict semantics. Первый вариант минимален и не требует нового production поведения. Пять includes/31 groups/один process могут сохраниться; I diff и exact candidate identity должны включать fixture correction до ENG_READY. Полезен source trace/read sentinel, подтверждающий, что выбранные controls не используют default /proc. Не запускать extra C08 и не выдавать новый grant для исправления D.

## Остальной узкий контракт

По immutable `point_artifacts.jl:528–545,785–787` unchecked intermediate products/sums и forecast+reserve подтверждены. Checked pure core с независимыми literal/BigInt oracles закрывает именно arithmetic classification: все inputs валидируются до conversion, bool исключён, known zero допустим только для неотрицательных counts/bytes. Literal F1=16854140 и F2=16777728 согласуются с неизменной формулой. F6 threshold `floor((M-C)/4)-128` при единичных dimensions даёт representable fit; увеличение kernel operand на1 пересекает последнюю checked boundary. F5 должен проверять каждый указанный intermediate независимо, а не только итоговое throw. Это остаётся heuristic forecast, не proven HDF5 bound.

Budget predicate `used+reserve+additional<=budget` и free predicate `required<=available` сохраняют разные baselines; D2 E/U/P/S normalization не присваивается R1. Pure path adapters не создают второй writer. Commit root mkdir отдельно оговорён, поэтому O2 не должен утверждать отсутствие вообще любых filesystem effects. Actual production seam/source trace обязателен: toy gate-then-thunk не закрывает O1–O3.

`resource_contract.jl` уже имеет корректный non-Bool representable validator и disjoint grant sum. Explicit envelope/policy propagation без повторного ambient default чтения — подходящий узкий интерфейс. Separate strict raw interpretation нужен: legacy `_resource_integer` теряет различие max/missing/malformed, probe заменяет unknown current на0, native permit пропускает directory/burst/no-finite-limits. Source D исправляет это только для выбранного strict режима. Known max на ancestor при полном chain с другим finite bound допустим; unknown ancestor/current/CPU path не превращается в permit. Current+burst checked в refusal evidence исключает wrapped arithmetic. Реализация strict CPU parser должна также сохранять finite tiny metadata work и не развертывать произвольный большой CPU range в Set; это I-review check, не требование нового native механизма.

Strict campaign entry остаётся безусловно closed с needs_guard/needs_admission до R2/R3/P1/P2/A1/C1 integration. Helper positive controls не являются S1 launch. Caller symbol/envelope token не становится новым trust root. Нет нового private site schema, portable result schema, lease ledger или второго campaign authority. Standalone parser/default probe/callback semantics сохраняются через отдельный режим и L regressions; arithmetic safety применяется обоим режимам.

Denominator корректен: F6+B5+D4=15, S9+O4=13, L3=3, всего31 groups. Pair exact-fit/1byte-short, unknown-vs-zero, overflow и positive sentinel полезны и различающи. Внутренние parameter rows остаются обязательными;31 — группы, не число assertions. Source suite selection исключает solve_scba_production fixture и whole groups. Existing integration phase fixture использует fake cgroup и только phase begin/end, tiny telemetry/pressure files; это не solve. До исполнения требуется проверенный I diff всех перечисленных rows.

ENG-1 отделён от C08: proposed один process, пять includes, max_attempts1,600s,1CPU,2GiB,1MiB output,16MiB fixture writes, prepared exact candidate. Из source можно обосновать tiny body и ноль science iterations. Fit600s/2GiB не измерен, package load/JIT остаются неизвестными. Требуются фактический supervisor resource cap/stop и no retry; его отсутствие блокирует ENG_READY. Этот review не разрешает ни один target call. C08 остаётся8/8 exhausted, code rounds общие≤2.

Model/criteria и caps D1+D2 сохранены в D§7:0mV/period, lattice/LO70K, LO/acoustic/impurity/IFR/alloy, electron_electron=none;13 attempts/936 execution node-hours/72h attempt/concurrency≤2/one threaded process/BLAS1. W1 четыре128GiB/2TiB writes/4TiB reads/1GiB logs, остальные девять256GiB/4TiB/8TiB/1GiB; shared2TiB/44TiB/88TiB/13GiB. Stop внутри прежних caps. Новый physics/grid/basis/window/mixing/tolerance/acceptance выбор не внесён. Это проверка сохранения source contract, не исполненной научной постановки.

## Ограничения и учёт

Source/text/hash/Git metadata only; Julia/import/target parser/tests/build/solver/native/network/server/Git mutations/product/CP edits=0. Под target parser подразумевается выполнение целевого кода, не `sed`/`rg` чтение текста. Часть ранних batched outputs была truncated; relevant primary source и D1/D2/review ranges прочитаны отдельно. Не заявляется полный аудит всех Runner файлов или всех SCI07 domains. Filename-only поиск /tmp получил отказы на чужих private directories, содержимое не читалось.

Read accounting: conservative upper bound2752512B<3145728B, включая whole Runner src charge1049142B за широкое rg, повторные полные named-file charges для ranged/hash reads и metadata reserve. Это логический source-volume bound, не измеренные OS I/O/CPU/RSS. Envelope15min/1CPU/1GiB/report128KiB соблюдён по действиям; report существенно меньше128KiB. Только два owned output в /tmp. Runtime measurements0.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Узкая checked arithmetic/strict separation определена | Immutable Runner symbols + D§3–5 | Implementation/fixtures ещё отсутствуют | сохранить |
| Exact пять includes полностью fake-only | D:127,196,203 vs application fixture135 и constructor | Обнаружено чтение actual /proc при будущем запуске | изменить |
| Standalone semantics могут сохраниться | Separate strict reader/policy, L1–L3 | Нужен I diff и выполненные regressions в отдельном grant | дополнительно измерить |
| ENG-1 tiny/distinct/finite | Один process/31 groups/explicit caps |600s/2GiB fit не измерен; grant отсутствует | сохранить после correction |
| Model/S1 caps и C08 exhaustion сохранены | D§7 vs D1§2/D2§5 | Native/scientific evidence отсутствуют | сохранить |
| Полный SCI08/S1 storage/native guard принят | R2/R3/P1/P2/A1/C1 остаются blockers | Helpers/source verdict не admission | данных недостаточно |

STOP. Требуется только узкая correction fake-only fixture selection, затем focused source rereview. Никаких target запусков или product/CP edits этим отчётом не разрешено.
