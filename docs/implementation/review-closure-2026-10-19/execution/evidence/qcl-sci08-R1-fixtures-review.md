# SCI08-R1 — независимый fixture-only source review

**Вердикт: CHANGES_REQUIRED_SOURCE. Один блокирующий P2: выбранный integration fixture читает настоящий `/proc`, несмотря на fake-only границу. ENG_READY закрыт.** Matrix и behavioral RED в остальном пригодны как source handoff с указанными ниже ограничениями. Никакой target code не исполнен.

## Frozen candidate

Owning Runner `/tmp/qcl-sci08-r1-runner-worktree`, HEAD `fefaa27f194bfddf85dd51a0e255beef2218c06d`. `git status --short`: ровно два modified test files и два new test files из candidate identity. Recursive submodule status пуст. `git diff --exit-code HEAD -- src` и `git diff --check` завершились 0; untracked production paths в status отсутствуют. Baseline integration fixture имеет пустой diff HEAD.

| Input | SHA256 |
| --- | --- |
| D1 | `16b07bbafce8235e0e103205e90c5b6e6b0db6c13c5bd4c883074f32888fe3c7` |
| D2 | `5a50afe3ca4014991dcb61d6dfb2879b2fef99e10f18347b5aa5d4eefe54d642` |
| High R final D2 | `23e50f07964c441f16b1e121f9d7952cf1bafd737544b81000a56a9da28e32fa` |
| Candidate identity | `35684ed22b678cd1b74229aa29642a69d854da6a72b07f89b3987f47d97b0e27` |
| Candidate patch | `869d11d7f7c59c24313dda77650bf96a90903a66062dc27048782c4543d3a5d6` |
| Candidate report | `9557a176d31c78c261846809c3945a555dad39c18363fcbf61a63a110a889b03` |
| Separate RED | `c519b715f645de58a27dea3e19cda5ad9142b393347a07dd8e4265edad914028` |

Все пять fixture SHA256 совпали с candidate identity. Начальный общий checkout зафиксирован отдельно: HEAD `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`, dirty docs/AGENTS; его восемь gitlinks сняты read-only, он не источник Runner candidate. Изменений общего checkout и Git writes нет.

## Блокирующее замечание P2 — fake roots не покрывают boot-id read

Воспроизводимый локатор при Runner HEAD выше:

`test/integration/native_phase_resource_contract.jl:22` задаёт `event_sink = event -> QCLNEGFRunner._record_native_phase!(root, event)`. В этом же fixture строки 25–42 вызывают реальные phase begin/end. Их event sink достигает `src/composition/native_phase_telemetry.jl:44` → `_native_phase_journal(directory)` → строка 24: `strip(read("/proc/sys/kernel/random/boot_id", String))`.

Это жёсткий настоящий `/proc` путь, независимый от переданных callback keywords `proc_root`/`cgroup_root` на строке 17 fixture. На первом phase event journal для нового temp root отсутствует; тело `get!` выполняется. `catch` не устраняет попытку host read. Следовательно пять выбранных includes не fake-only. Сам integration файл не менялся, но является частью exact selection и знаменателя 345; прежний PASS_SOURCE D2 проверял другой membership path и не закрывает эту трассу.

Решение: до ENG_READY исправить fixture или узкий fixture contract и повторно проверить эту трассу. Самый дешёвый source-only кандидат без production edit и global monkeypatch: предварительно заполнить существующий `_NATIVE_PHASE_JOURNALS[root]` тестовым `_NativePhaseJournal` с literal fixture clock identity и очистить запись в `finally`. Это использует уже существующий private journal seam и сохраняет phase begin/end assertions; это предложение, не внесённый или проверенный патч. Не удалять integration include/утверждения ради fake-only. Не менять production boot identity и не добавлять production observer ради теста. Source review текущего scope не разрешает это изменение или runtime.

## Проверка matrix и чисел

Независимая ручная развёртка source loops подтверждает 31 logical groups и 345 nominal assertions при достижении всех блоков. Это не runtime receipt и не гарантия достижимости после import.

| Часть | Groups | Nominal assertions |
| --- | --- | ---: |
| F1–F6 | 6 | 49 |
| B1–B5 | 5 | 46 |
| D1–D4 | 4 | 23 |
| S1–S9 | 9 | 116 |
| O1–O4 | 4 | 15 |
| Application L1/L2 controls | распределены в L1–L3 | 55 |
| Linux legacy controls | распределены в L1–L3 | 26 |
| Integration phase controls | распределены в L1–L3 | 15 |
| Итого | 28 новых + 3 legacy = 31 | 249 новых + 96 legacy = 345 |

33 actual `@testset` blocks не противоречат 31 logical groups. Пропусков required matrix rows, skip/broken или отбора только healthy cases в просмотренных файлах нет.

* F/B/D: literals 16854140 и 16777728 согласуются с исходной формулой. Test-local BigInt oracle не вызывает production forecast/validator. F3/F4 независимо меняют каждый аргумент; F5 покрывает шесть требуемых небезопасных промежуточных границ; F6 использует соседнюю representable границу. B/D различают exact fit и нехватку 1 byte, known zero, malformed/unknown, два addition overflow. B4/D4 имеют reader counters с healthy witness. Больших массивов из fake dimensions нет. Это scalar correctness, не физический upper bound HDF5 и не actual capacity evidence. F5 exception сам по себе не доказывает checked каждого промежуточного оператора: production source trace всё ещё обязателен.
* S: три ancestor positions и все required malformed/missing bound/current perturbations присутствуют. Known `max`, known 0, unknown, malformed, out_of_range имеют отдельные assertions. Missing burst/directory, Bool/nonrepresentable width, current+burst overflow, CPU affinity/quota/cpuset и overrides не подменены zero/unlimited. Exact fit/1-byte-short и burst0/unknown-current различимы. Все новые probe/phase callback roots явно fake; probe имеет explicit physical/available/count/vendor values. Strict implementation должна сохранить raw distinctions и не перечислять огромные CPU ranges в Set. На baseline этих APIs пока нет — полный GREEN selection сейчас не является behavioral RED.
* L: application correction корректно связывает fake membership → callback constructor → `_process_cgroup_path(fake_proc)` → fake `self/cgroup` → fake leaf/slice/root. Source bytes содержат обычный Julia `\n` escape. Directory=nothing memory path возвращается до memory reads. Четыре callback invocations и witnesses 3/3 затем 4/3 сохранены. Linux meminfo задан fixture literal, поэтому его legacy available-memory fallback до Sys.free_memory по этим healthy inputs не достигается. Настоящий journal `/proc` read выше остаётся отдельным пробелом selection.
* O: O1/O2 используют future private seams, затем test-local continuation. Report и comments честно требуют actual caller trace; они не выдают эти thunks за закрытие `execute_scientific_plan`/`commit_point_artifacts`. O3 использует настоящий callback seam, но actual allocator propagation тоже требует source проверки. O4 имеет healthy continuation и literal checkpoint control. Для полного S1 эти controls не заменяют R2/R3/P1/P2/A1/C1.

## Behavioral RED и handoff

`/tmp/qcl-sci08-R1-behavioral-red.jl` содержит ровно 2 assertions, вызывает существующий untyped `_checkpoint_storage_forecast(solution)` при baseline `src/infrastructure/persistence/point_artifacts.jl:528–535`. Tiny NamedTuple предоставляет ровно читаемые `.problem.numerical` и `.problem.kernels.K/.Fᴸᴼ`; payloads — реальные пустые `UInt8` vectors. Healthy 1/1/1 даёт по source literal 16777728. Единственная замена NE=true проходит baseline unchecked arithmetic как 1 и не бросает ArgumentError; отрицательное `@test_throws` поэтому должно провалиться по поведению. Future undefined helper в этом файле не вызывается. Нет SCBA, writer или host reader в данном вызове.

Это **source prediction**, не observed RED. Prepared environment, package resolution и harness обязаны отдельно bind точный worktree baseline; import/configuration error не принимается за нужный RED. Production source writer ждёт различающего RED receipt. Все предложенные helper signatures в candidate report соответствуют fixture uses и могут стать стабильным handoff после RED; ослабление typed dispatch до явной ArgumentError validation ожидаемо и должно отдельно пройти source review.

Actual later production trace остаётся ENG_READY prerequisite: entry preflight до `scientific_execution.jl:456` mkdir/466 plan writer/684 problem build; тот же explicit envelope до reservation вместо повторного ambient default в baseline строке 178; policy до phase request строки 966; checkpoint seam до `point_artifacts.jl:806` temporary generation/HDF5 writer; проверяемая reserve addition вместо baseline строки 787. Campaign-strict остаётся closed needs_guard/needs_admission. Наличие private helpers не является admission authority.

## Границы работы

Применён qcl-performance-audit для различения source fixtures и production resource evidence. Прочитаны D1/D2/final high R, candidate report/patch/identity, RED, пять selected files, common/resource support и указанные owning source ranges. Выполнены только текстовые/Git/hash/size проверки. Source-only чтение вместе с повторениями и metadata консервативно <2MiB из лимита 3MiB; physical I/O/CPU/RSS не измерялись. Соблюдён scope 15min/1CPU/1GiB/report≤128KiB. Target Julia/import/parser/runtime/tests/build/SCBA/Poisson/native/network/install/product/CP/Git mutations = 0. C08 exhausted8/8 не затронут. Записаны только этот report и review identity.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Baseline production src сохранён | Runner fefaa27, empty src diff + status | Нет runtime | сохранить |
| 31 groups / 345 nominal assertions | Ручная развёртка пяти exact sources | Не test receipt | сохранить |
| Selection fake-only | Integration:22 → native_phase_telemetry:44 → :24 настоящий `/proc` | Один source blocker; ничего не запускалось | изменить |
| RED различает baseline Bool defect | Existing forecast:528–535 и 2 assertion source | Нет observed failure и environment binding | дополнительно измерить |
| O1/O2 actual entry ordering закрыт | Только future seams/test-local continuation | Нужен later production caller trace | данных недостаточно |
| Полный campaign/S1 admitted | Partial helper contract | Owning guard integration отсутствует | данных недостаточно |

STOP. CHANGES_REQUIRED_SOURCE не выдаёт ENG/runtime/native/science grant.
