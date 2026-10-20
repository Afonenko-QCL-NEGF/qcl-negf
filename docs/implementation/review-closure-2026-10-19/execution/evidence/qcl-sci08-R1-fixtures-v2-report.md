# SCI08-R1 fixtures v2 — scoped D3 source correction

Статус: **READY_FOR_SCOPED_INDEPENDENT_HIGH_FIXTURE_REVIEW**, не ENG_READY.
Runner `/tmp/qcl-sci08-r1-runner-worktree`, branch
`codex/review-closure-sci08-r1-checked-resources`, HEAD
`fefaa27f194bfddf85dd51a0e255beef2218c06d`.

Основание D3 SHA256 `373a5da4ca765561e4a3ee46fa9c0bd06959a067ebf9f56c415e33666ad507c7`,
accepted high D3 `7b8108df1708f103a988ca567feb0e50c8b8c8f455ac657217033ed692c0ff46`.
D1+D2 и исходные fixture-v1 artifacts не переписаны. V1 report/identity/patch
остаются историческими; v2 patch содержит полный current fixture diff от Runner HEAD.
Прочитаны D3/high D3, primary journal/recorder source и selected integration fixture.

## Ровно один fixture correction

Изменён только `test/integration/native_phase_resource_contract.jl` относительно
предыдущего fixture candidate. Production `src` по-прежнему byte-exact HEAD:
`git diff --exit-code HEAD -- src`0. Other four selected fixture bytes unchanged.
Target Julia/import/parser/runtime/tests/build/solver/native/network/install=0;
commit/push/CP/Root writes=0. `git diff --check`0. C08 exhausted8/8 не использован;
новый ENG grant не выводится из D3/high review.

В integration создан literal boot file под `fake_proc=dirname(proc)`:
`joinpath(fake_proc,"sys","kernel","random","boot_id")`. A равно
`00000000-0000-4000-8000-000000000001`, B заканчивается `0002`.
Файл получает A+newline; callback продолжает получать оба fake roots, а actual
production event sink получает будущий `proc_root=fake_proc`. Используются прежние
actual production phase begin/end, вложенность, JSONL и pressure path.

Все прежние15 assertions текстуально сохранены. Добавлены ровно4:

1. Row1 clock_domain начинается с literal A * ":julia:".
2. `_NATIVE_PHASE_JOURNALS` содержит прежний String directory key root.
3. После записи B+newline вызов `_native_phase_journal(root;proc_root=fake_proc)`
   возвращает === тот же journal.
4. Cached journal.clock_domain остаётся равным первоначальному row1 clock_domain.

Новых phase events не добавлено; старые count4 assertions сохранены. `finally`
удаляет только exact root entries из journals/admissions через pop!(...,root,nothing).
Не используется cache preseed, global reader monkeypatch, clear! или host boot-id.

## Denominator и binding

Selection неизменна: checked_storage_forecast, strict_campaign_resource_admission,
execution_resource_contract, linux_process_resource_probe, native_phase_resource_contract.
F1–F6/B1–B5/D1–D4/S1–S9/O1–O4/L1–L3 =31 logical groups,33 @testset blocks.
V1 input/oracle rows сохранены без изменения;349 предполагаемых assertions = прежние
345+4, а не observed runtime count. Развёртка: новые F/B/D/S/O249, application55,
Linux26, integration19. D3 provenance assertions принадлежат существующим L groups,
32-я группа не создана. Source-only text check подтвердил, что15 baseline integration
assertion lines входят в19 current lines; target parser/test execution отсутствуют.

RED файл immutable `/tmp/qcl-sci08-R1-behavioral-red.jl` SHA256
`c519b715f645de58a27dea3e19cda5ad9142b393347a07dd8e4265edad914028`.
Ровно2 assertions: existing baseline forecast healthy16777728 и Bool dimension
ArgumentError expectation; production behavioral RED **не наблюдался**.
RED не включает integration/journal/new helpers и не требует раннего source edit.

## Полная таблица API для owning production writer ПОСЛЕ observed RED


D1 names three scalar helpers; D does not fix all adapter/seam names. This candidate
binds the following signatures for a coherent implementation/review, without modifying
production before Root behavioral RED. Types must permit invalid test inputs to reach
explicit ArgumentError validation; typed dispatch MethodError is not the oracle.

| API | Contract used by fixtures |
| --- | --- |
| `_checkpoint_storage_forecast_bytes(ne,nk,nb,kernel_sizes,f_size)` | dimensions positive non-Bool Int-representable; sizes nonnegative; return Int forecast; checked all intermediate arithmetic |
| existing `_checkpoint_storage_forecast(solution)` | gather actual sizeof and delegate to same scalar helper; tiny NamedTuple uses existing duck-typed baseline API |
| `_storage_budget_used(used,budget,reserve,additional)` | validate all; budget>0; checked used+reserve+additional≤budget; return used |
| `_storage_free_permit(available,required)` | validate known nonnegative bytes; required≤available; return available |
| existing `_check_storage_budget(paths,budget,reserve,additional; storage_reader=_storage_bytes)` | validate caller args before reader; delegate used validation/predicate; reader called once only for valid caller args |
| existing `_check_storage_free(path,required; available_reader=...)` | default adapter returns raw diskstat.available without lossy preconversion; validate required before reader; unknown rejects, reader error propagates; delegate scalar validation |
| `_checkpoint_storage_preflight(solution,reserve)` | same forecast adapter plus checked validated forecast+reserve; return `(forecast_bytes=F,required_bytes=F+reserve)`; actual commit must use seam before generation/HDF5 writer |
| `_strict_resource_integer(raw::AbstractString)` | NamedTuple with `.status` :finite/:unlimited/:unknown/:malformed/:out_of_range; finite `.value` exact Int; max distinct from unknown0 |
| existing `_native_phase_request(directory;proc_root,cgroup_root,resource_policy=:standalone)` | strict refuses missing path/unknown estimate/bounds/current; validates width before Int; known pressure existing _NativePhasePressure; checked current+burst |
| existing `_native_phase_memory_permit!(directory,groups,request;resource_policy=:standalone)` | strict empty groups refuses; same helper is actual callback memory seam |
| existing `probe_hardware(;...,resource_policy=:standalone)` | strict raw CPU/count/override/path validation, no fallback from unknown; all fixture calls give roots and capacities/vendor explicitly |
| `_scientific_resource_preflight(resource_policy,envelope)` | unknown policy/missing strict envelope refuse; :campaign_strict always ArgumentError needs_guard/needs_admission until owning guard integration; standalone nothing returns nothing |
| existing `execute_scientific_plan(...;resource_policy=:standalone,envelope=default_execution_envelope())` | call same entry preflight before mkdir/plan/attempt/problem allocation; propagate selected envelope/policy, no second ambient default read |
| existing `_native_phase_journal(directory::String;proc_root::String="/proc")` | D3: same lazy `get!(_NATIVE_PHASE_JOURNALS,directory)`; first initialization reads `strip(read(joinpath(proc_root,"sys","kernel","random","boot_id"),String))`; same catch boot_unknown; directory-only cache key and constructor/session/anchors/sequence unchanged |
| existing `_record_native_phase!(directory::Union{Nothing,String},event::SolverEvent;proc_root::String="/proc")` | D3: same early returns before mkpath/journal; forward exactly `proc_root` to journal; unchanged row schema; default production callers keep old path/semantics |

These seams are engineering mechanics, not physical policy, authority tokens,
private portable schemas, lease ledgers or S1 admission. Standalone defaults remain.
Probe keyword count/capacity validations must be explicit even for Float/Bool/>M;
current typed override signatures may need widening to reject with ArgumentError.
Strict CPU range parser must not enumerate arbitrarily large intervals into Sets.

## Полная explicit-fake трасса и оставшиеся obligations

Integration memory path:
`callback(...;proc_root=fake_proc,cgroup_root=root)` → existing constructor →
`_process_cgroup_path(fake_proc)` → fake `self/cgroup` literal `0::/group` →
`_cgroup_ancestors(root,"group")` → fake group/root paths. Memory files group-owned.
Membership/callback и producer journal теперь используют одну fake_proc variable.

Integration boot path, **предписанный для later production I**:
actual N._production_phase_begin/end → options.event_sink closure with explicit
`proc_root=fake_proc` → `_record_native_phase!(root,event;proc_root=fake_proc)` →
`_native_phase_journal(root;proc_root=fake_proc)` → lazy get! initialization →
`read(joinpath(fake_proc,"sys","kernel","random","boot_id"),String)` → strip.
Все boot bytes literal. Pressure/JSONL reads/write относятся к owning mktempdir.
При directory cache hit после A→B journal не перечитывается/не пересвязывается.

Baseline recorder/journal ещё НЕ принимают keyword и ещё содержат actual /proc
boot-id read: это обязательная production correction **после observed RED**, а не
уже реализованная fake-only цепочка. Поэтому current five-file selection не запускать
на baseline и не использовать keyword MethodError как behavioral RED. Независимый
later I source review должен замкнуть recorder→journal→fake path и подтвердить
неизменность default path, strip/read/catch, early returns, directory-only get! key,
struct, session, anchors, sequence и portable row schema. Fake producer clock prefix
не удостоверяет actual host/process/boot и не является strict admission BIND.

Остальные selected paths сохраняют v1 explicit fake roots/readers: storage adapters
через injected fake readers; strict callbacks/probe с обоими fake roots и capacity/
count/vendor overrides; application D2 width callback с fake_proc/fake_cgroup;
legacy Linux probe с fixture meminfo и physical/count/vendor overrides, malformed
current sibling дополнительно с available override. Известный boot reader выделен
выше; runtime read tracing/аудит transitive package initialization не заявляется.

O1/O2 pending actual production caller traces остаются: entry preflight до
output-root/plan writer/problem allocator; checkpoint preflight до temporary
generation/HDF5 writer, checked forecast+reserve и direct envelope/policy propagation.
Toy gate/continuation не закрывает actual ordering. Strict campaign остаётся closed
needs_guard/needs_admission до R2/R3/P1/P2/A1/C1, независимо от helper controls.

Выполнены лишь source/text/Git/hash checks. Scope1MiB reads/8min/1CPU/1GiB/
report64KiB; conservative logical read charge <524288B; physical RSS/CPU/I/O не
измерены. Ни runtime fit, ни numerical correctness не заявлены. Separate finite
Root RED/GREEN grant/harness/stop необходим до каждого target execution.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| D3 integration source correction prepared | explicit fake sink root + four exact assertions + scoped finally | future keywords absent in baseline | сохранить |
|349 nominal assertions/31 logical groups |345 prior +4;15 old integration assertions retained | not executed/parsed | дополнительно измерить |
| Production preserved until behavioral RED | empty src diff, unchanged RED c519… | RED не наблюдался | сохранить |
| Entire actual fake-only boot chain implemented | future API table + fixture caller | post-RED production I source trace absent | данных недостаточно |
| ENG/S1/native admission open | no target calls/grant | owning gates remain closed | данных недостаточно |

STOP для scoped independent high fixture source review. No production/runtime/CP action.
