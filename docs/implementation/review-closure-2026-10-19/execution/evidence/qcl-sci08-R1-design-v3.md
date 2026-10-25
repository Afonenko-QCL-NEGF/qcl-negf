# SCI08-R1 D3 — fake boot identity у producer journal

Статус: **D3_READY_FOR_FOCUSED_HIGH_REVIEW**; после independent PASS_SOURCE это
узкий I contract, а не ENG_READY/runtime grant. D1+D2 и accepted high D2 review
сохраняются immutable. Product/CP/runtime/parser/tests/native/network calls=0.

## 1. Frozen inputs и scope

| Input | SHA256 |
| --- | --- |
| D1 `/tmp/qcl-sci08-R1-design.md` | `16b07bbafce8235e0e103205e90c5b6e6b0db6c13c5bd4c883074f32888fe3c7` |
| D2 `/tmp/qcl-sci08-R1-design-v2.md` | `5a50afe3ca4014991dcb61d6dfb2879b2fef99e10f18347b5aa5d4eefe54d642` |
| Accepted independent high D2 | `23e50f07964c441f16b1e121f9d7952cf1bafd737544b81000a56a9da28e32fa` |
| Fixture source review | `7c7d9d3faff2d8b167eb401433be534cd3bdad59af04f2beee12a974d24575e9` |
| Separate existing-API behavioral RED | `c519b715f645de58a27dea3e19cda5ad9142b393347a07dd8e4265edad914028` |

Owning candidate `/tmp/qcl-sci08-r1-runner-worktree`, HEAD
`fefaa27f194bfddf85dd51a0e255beef2218c06d`. Status: modified application/Linux
fixtures и два new F/B/D/S/O fixtures; production src и integration fixture ещё
baseline, их targeted diff HEAD пуст. Recursive submodules пусты.

Source pair:
`src/composition/native_phase_telemetry.jl` SHA256
`9605f1a4852f5edbe8ca83652500c2e0a2352feec7a04cf9d0e85bd0e712f173`;
`test/integration/native_phase_resource_contract.jl` SHA256
`30c511c1b8a811855934d719b500192ff9be8efa301eb477651114143d37b5e0`.
Это one-time binding, не новый composition lock; authority остаётся Git gitlinks.

Ровно один новый вопрос: убрать реальное чтение boot-id из exact fake-only
integration selection, сохранив production journal initialization/provenance и
его cache identity. Ни resource guard, ни scientific contract не расширяются.

## 2. Подтверждённая трасса

Baseline integration fixture:22 задаёт
`event_sink = event -> _record_native_phase!(root,event)`. Phase begin/end:25–42
вызывают sink; recorder:44 вызывает `_native_phase_journal(directory)`;
journal:20–35 на первом `get!` читает настоящий
`/proc/sys/kernel/random/boot_id` (:24). Fake proc/cgroup callback roots fixture:17
не достигают journal. `catch` сохраняет fallback, но не отменяет попытку host read.
Остальная source matrix получила review без иных блокирующих findings:31 groups,
345 nominal assertions при достижении всех блоков; это не выполненный тест.

## 3. Минимальный owning I contract

После требуемого отдельного observed behavioral RED и разрешённого owning I
изменить только уже owning `src/composition/native_phase_telemetry.jl`:

1. Добавить private keyword `proc_root::String = "/proc"` к существующему
   `_native_phase_journal(directory::String)`.
2. Внутри **того же** lazy `get!(_NATIVE_PHASE_JOURNALS,directory) do ... end`
   заменить единственный hardcoded boot-file path на
   `joinpath(proc_root,"sys","kernel","random","boot_id")`.
   `strip(read(path,String))`, существующий `catch -> "boot_unknown"`, PID/time
   session, initial sequence0, UTC/monotonic anchors, stack/admissions constructor
   остаются прежними. Не заменять read на `_resource_read`: его empty-string
   fallback изменил бы provenance при failure.
3. Добавить тот же private keyword к
   `_record_native_phase!(directory::Union{Nothing,String},event::SolverEvent)`
   и передавать его в `_native_phase_journal(directory;proc_root=proc_root)`.
   Существующие early returns для directory=nothing и non-phase events остаются
   раньше mkpath/journal. Никаких новых global roots, reader objects или observers.
4. Cache key остаётся **точно directory::String**, тип словаря и journal struct
   неизменны. Ни proc_root, ни boot string не добавляются к cache key. Первый
   journal фиксирует session/clock identity; последующие calls с тем же directory
   возвращают тот же объект без нового read, reset/sequence change или смены boot.
   Другой proc_root на cache hit не даёт rebind существующего journal.
5. Keyword остаётся private fixture seam, не export, CLI/YAML/model field,
   portable schema, resource envelope или authority input. Existing production
   callers по-прежнему вызывают recorder без keyword, т.е. читают **тот же**
   `/proc/sys/kernel/random/boot_id` с прежней failure semantics. Output schema,
   field names и clock-domain construction `boot * ":julia:" * session` прежние.
   Динамические PID/time естественно отличаются между запусками; алгоритм и
   default observable semantics эквивалентны baseline.

Выбран private proc-root seam вместо предварительной ручной вставки struct в
cache: integration тогда проходит actual lazy journal initialization и проверяет
происхождение clock prefix, не зависит от ручного копирования constructor layout.
Не реализовывать оба подхода и не preseed journal для сокрытия неправильного read.
Это единственный новый seam D3; root superproject/Core/Contracts не меняются.

## 4. Exact integration fixture adjustment

Изменить existing `test/integration/native_phase_resource_contract.jl`, сохранив
файл в пяти selected includes и **все прежние15 assertions без ослабления**:

1. В существующем mktempdir использовать его `fake_proc=dirname(proc)` для обоих
   consumers. Текущий callback продолжает получать явные
   `proc_root=fake_proc,cgroup_root=root`.
2. Под `fake_proc` создать literal file
   `sys/kernel/random/boot_id`, включая необходимые directories. Initial text:
   `00000000-0000-4000-8000-000000000001\n` (fixture boot A). Это fixture bytes;
   не читать реальный boot-id для наполнения fake file.
3. Event sink заменить на
   `event -> _record_native_phase!(root,event;proc_root=fake_proc)`.
   Настоящие N._production_phase_begin/end, вложенность, memory permit, JSONL и
   pressure path сохраняются. Ни begin/end, ни integration include не исключать.
4. После получения прежних four rows и проверки всех старых phase assertions
   добавить ровно четыре provenance/cache assertions:

   - `startswith(rows[1]["clock_domain_id"], boot_A * ":julia:")` — positive witness,
     что journal прочитал literal fixture A через actual constructor.
   - `haskey(_NATIVE_PHASE_JOURNALS,root)` — прежний String directory cache key.
   - Получить `journal=_NATIVE_PHASE_JOURNALS[root]`; заменить **fake** boot file на
     `00000000-0000-4000-8000-000000000002\n` (B); вызвать
     `_native_phase_journal(root;proc_root=fake_proc)` и проверить `=== journal`.
     Этот cache-hit witness не создаёт новый phase event и не меняет старый count4.
   - `journal.clock_domain == rows[1]["clock_domain_id"]` после замены fake file:
     cached provenance не перечитывается и не пересвязывается на B.

   Переменная `boot_A` содержит literal без trailing newline, file содержит newline;
   тем самым сохраняется production strip behavior. Старое сравнение row1/row4
   clock-domain остаётся отдельным неизменным assertion.
5. Обернуть использование owning temp-root journal в finally cleanup:
   `pop!(_NATIVE_PHASE_JOURNALS,root,nothing)` и
   `pop!(_NATIVE_PHASE_ADMISSIONS,root,nothing)`. Удалять только exact owned root
   entries, без clear!/обхода чужих journals. Cleanup не подменяет assertions и
   не исполняет extra native calls. Temp file B остаётся внутри mktempdir lifecycle.

Проектная source count delta: прежние345 nominal assertions +4 = **349**;
integration15→19;31 logical groups и five file includes неизменны. Новые assertions
относятся к существующим legacy L groups, не создают32-ю required group.
До I diff это proposed count, а не уже проверенный новый fixture receipt.
Source reviewer должен независимо пересчитать final diff и сохранить old345
как immutable baseline, не переименовывать их в runtime pass.

У fakeboot bytes/file count tiny finite delta: два successive37-byte text values
одного файла, без simultaneous full copies; это часть прежнего fixture write
allowance, не измеренная production storage cost. Не нужны synthetic arrays,
solve, real diskstats, `/proc`, `/sys/fs/cgroup`, hostname/boot probes или network.

## 5. Source acceptance и полномочия

Independent I review обязан проследить actual chain
integration sink→recorder keyword→journal keyword→fake path construction/read.
Доказательство отсутствия host read опирается на этот source trace и explicit
fake inputs; четыре cache assertions одни этого не доказывают. Проверить, что
default path/strip/catch/session/anchors/row schema/get! key/early returns не
изменились. Known fake boot не native observation и не valid admission BIND.

Private keyword не создаёт native authority. Strict BIND должен независимо
проверять trusted host/boot/process/source identity существующим admission owner;
clock-domain text из producer journal и caller fixture roots не удовлетворяют
этому контракту и не дают pass. Strict campaign по-прежнему closed с
needs_guard/needs_admission до R2/R3/P1/P2/A1/C1. Не добавлять accepted-strict
fixture identity или `guards_complete` переключатель ради этого seam.

O1/O2 actual production caller traces из D1+D2 и fixture review остаются
обязательными: entry preflight до root mkdir/plan writer/problem allocation;
checkpoint preflight до temporary generation/HDF5 writer; exact envelope/policy
propagation; checked reserve addition. Test-local toy thunk не закрывает их.
Boot seam не изменяет эти ordering obligations и не заменяет every-write guard.

## 6. RED отделён от integration и от I

Existing `/tmp/qcl-sci08-R1-behavioral-red.jl` остаётся отдельным RED selection:
ровно2 assertions, только existing untyped `_checkpoint_storage_forecast`, tiny
NamedTuple, empty real UInt8 kernel vectors; healthy forecast16777728 и Bool
ArgumentError expectation. Source предсказывает behavioral failure baseline,
но runtime не выполнялся. RED не включает integration fixture, journal,
producer event sink или новые helpers — ни прямо, ни через group runner.

До observed RED и отдельного owning I production source не меняется ради того,
чтобы integration прошёл раньше. Source-only fixture adjustment можно подготовить
как текст; new keyword пока не существует, поэтому полный future GREEN selection
не запускается на baseline и не считается behavioral RED. Нужен exact baseline
ref/RED SHA binding; import/missing environment error не принимается за RED.

После разрешённого I future GREEN selection сохраняет пять файлов D1 с corrected
existing application/Linux fixtures, F/B/D/S/O и corrected integration. Этот D3
не добавляет engineering process calls и не выбирает finite RED/GREEN plan.
Actual calls/ресурсы/supervisor stop/нет reruns определяет отдельный принятый plan.
Не использовать C08:8/8 exhausted. Никаких runtime/tests/native/science grants
из PASS_SOURCE D3 не следует. Общий SCI08≤2 code rounds не умножается.

## 7. Invariants и вывод

D1+D2 policy/oracles сохраняются. S1:0mV/period, lattice/LO70K,
LO/acoustic/impurity/IFR/alloy, electron_electron=none;13 attempts/936 execution
node-hours/72h attempt/concurrency≤2/one threaded process/node/BLAS1.
W1 четыре128GiB/2TiB writes/4TiB reads/1GiB logs, остальные девять
256GiB/4TiB/8TiB/1GiB; shared2TiB/44TiB/88TiB/13GiB. Stop внутри caps.
Physics/grids/basis/window/mixing/tolerances/acceptance без изменений.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Journal имеет отдельный real boot-id read | Integration22→recorder44→journal24 при fefaa27 | Source observation, не runtime | изменить |
| Minimal seam сохраняет journal provenance/defaults/cache key | Contract§3 + proposed fake constructor/cache witnesses§4 | Требуется accepted D3, I diff и independent source trace | изменить |
| Старые legacy assertions/31 groups сохранены | Existing15 + proposed4;345→349 nominal | Новый count ещё не проверен на final source | сохранить |
| RED требует early production edit/integration | Separate2-assertion existing-API file§6 | RED не исполнен | сохранить |
| Full S1/native guard или ENG_READY достигнут | Только source design | Admission/guard/runtime receipts отсутствуют | данных недостаточно |

STOP. Три requested D3 artifacts, затем focused high D3 rereview. No product/CP edits.
