# SCI08-R1 — checked forecast и строгие unknowns S1

Статус: **D_READY_FOR_INDEPENDENT_HIGH_REVIEW**, не I_READY и не runtime/science READY.
Этап — source design. Product/CP/source edits, Julia/import/parser/tests/build/native/network calls=0.
Один последующий owning writer — Runner; reviewer независим от автора D и I.

## 1. Вопрос, входы и граница

Вопрос: можно ли гарантировать отказ при непредставимом storage forecast и неизвестном
ресурсном входе выбранного строгого S1-пути до допуска allocator/writer, сохранив
самостоятельных callers? Успех здесь — адресный source contract и различающие
manufactured fixtures; не доказательство actual capacity или полного storage guard.

Read-only source root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`:
HEAD `469ef4ec36c1dfb967856108e5f9455429559c15`; Runner tree/clean worktree
`fefaa27f194bfddf85dd51a0e255beef2218c06d`; Core gitlink
`9f4a96d032ad868ec010ce92d915bb81087c8d92`.
Root dirty: coordinator CP/census/evidence, DOC06/DOC07 untracked work и Contracts checkout
`f4009c9...` вместо tree gitlink `d791dea...`. Они не inputs R1, не изменяются.
Это forensic binding, не второй revision lock; состав берётся из Git tree.

Primary D1 SHA256 `1f569ba726873d80715523621933caa6c0a0b0ad84e5a59ba9ef077b12001635`;
D2 `fc78a0c77394f4d12a1c5633b7e4acb587429667abc106f5aa72c1dc4dd9d010`;
high R1 `48f97407846b4b179de2442e1295e8cc2028ed7d4e3ca9c2f28c8079ac5d4e67`;
high R2 `80e2f1ca784b9c4a082d0785e6ee6bc9ceb507eeecc43c63822f65f532a1d18e`.
D2 overrides D1 total/headroom inequality и chronology. Его E/U/P/S normalization
не переносится в forecast как выдуманное enforcement: R2/P1/C1 остаются owners.

## 2. Установленная baseline API

| Source при Runner fefaa27 | Наблюдение | Адресное действие R1 |
| --- | --- | --- |
| `src/application/resource_contract.jl:1–54` | `default_execution_envelope()=nothing`; `_grant_integer` уже отвергает Bool/noninteger/unrepresentable; ExecutionEnvelope проверяет disjoint numerical+runtime+allocator≤hard через BigInt; `execution_budget` сверяет только hardware hard/pool | Сохранить envelope и defaults. Переиспользовать integer validator с minimum=0/1; explicit envelope не считать native authority |
| `src/infrastructure/persistence/point_artifacts.jl:513–545` | `_storage_bytes` checked sum; forecast содержит unchecked `128*N_E*N_k*N_b^2`, kernel sum, `arrays+kernels`; budget/free inputs отдельно не валидируются; diskstat available преобразуется через Int | Изолировать pure scalar checks; полностью checked products/sums/conversions; unknown не превращать в 0/typemax |
| Там же `:760–786` | `commit_point_artifacts` typed NEGFSolution; byte budget/reserve typed Int; forecast перед HDF5, но после mkpath; `forecast+reserve_bytes` unchecked | Заменить addition на checked; invalid forecast получить до first growth-capable writer/temporary generation. Если directory creation оставлено раньше, это явно отдельный эффект, не no-write assertion |
| `src/infrastructure/resources/linux_resources.jl:9–15,68–87,160–194` | `_resource_integer` сводит blank/max/malformed/out-of-range к typemax; missing cgroup→root; unknown current→0 в probe; finite limit+unknown current даёт headroom0 | Оставить legacy parser; добавить strict interpretation, не реконструировать measurement из sentinel |
| `src/composition/native_phase_telemetry.jl:138–210` | Width приводится Int до проверки; directory=nothing, burst=nothing, no finite limits пропускают memory admission; current+burst в pressure evidence unchecked; GC разрешён до отказа | В строгом режиме запретить unavailable skip; валидировать width/burst/current/limits до арифметики; checked required bytes даже для отказного receipt |
| `src/composition/scientific_execution.jl:436–459,665–684,966` | `execute_scientific_plan` не имеет resource policy/envelope kwarg; root mkdir/plan write раньше configured problem; phase callback строится без strict policy; reservation читает default envelope повторно | Явно прокинуть выбранную policy/envelope через entry/preflight/reservation/phase callback, без ambient mutable global |
| `test/run_group.jl:1–22` | runner выбирает group и includes все .jl; individual file filter отсутствует | Не запускать entire group ради R1; отдельная bounded selection ниже |

## 3. Минимальная арифметика и owning edits

Все размеры/bytes — Integer, кроме Bool; представимы Int и неотрицательны. Dimensions,
budget и task_width строго положительны. Reserve/additional/kernel-size/current/burst
могут быть ровно0, если значение известно. `nothing`, string, float, NaN, Inf, negative,
Bool и >typemax(Int) отказывают до conversion. Нормировка — literal bytes/counts;
допуск0, exact integer comparison. Никакой rounded GiB equality.

1. В point_artifacts выделить pure private scalar core
   `_checkpoint_storage_forecast_bytes(N_E,N_k,N_b,kernel_sizes,F_size)`;
   существующий `_checkpoint_storage_forecast(solution)` собирает реальные sizeof и
   делегирует. Не создавать массивы по fake dimensions. Формула сохраняется:
   `C=16777216; A=128*N_E*N_k*N_b*N_b; K=sum(kernel_sizes)+F_size; F=C+4*(A+K)`.
   Каждый product/addition/size conversion checked либо exact BigInt с range-check
   на всех Int boundaries. Предпочтительный минимальный путь — existing validator и
   Base.checked_mul/add. Суммирование kernel sizes начинается с известного0.
   Это старый heuristic allowance, не новый proven HDF5/physical upper bound.
2. В point_artifacts pure cores `_storage_budget_used(used,budget,reserve,additional)`
   и `_storage_free_permit(available,required)` — предлагаемые private имена.
   Existing path adapters остаются единственными readers и делегируют проверку.
   Validate scalar arguments до scan/diskstat; used и available после чтения проходят
   такую же validation. Budget: checked `used+reserve+additional<=budget`.
   Free: `required<=available`; available после validated conversion. Не смешивать
   used с remaining free: separate predicates сохраняются.
3. Закрыть `forecast+reserve_bytes` при entry commit и checked `current+burst`
   при pressure evidence. Никакое diagnostics serialization overflow не должно
   превратить отказ в permit или fake paused success. Переполнение может дать
   OverflowError; malformed input — ArgumentError; существующие budget-exhaustion
   exception types сохранить. Если пользовательский контракт требует единый тип,
   нормализовать только на owning entry с исходной причиной, не catch-and-continue.
4. Прочие unchecked expressions вне этих R1 call chains записать отдельными gaps;
   не объявлять весь Runner integer-safe. Archive/recovery common resident/growth
   enforcement, all HDF5 slab writes и stop/cumulative receipts — R2/R3/P2, не R1.

## 4. Строгий путь и совместимость

Предлагаемый узкий internal API: `resource_policy::Symbol=:standalone` на
`execute_scientific_plan`, принимающий только `:standalone` и `:campaign_strict`,
и `envelope::Union{Nothing,ExecutionEnvelope}=default_execution_envelope()`.
Это выбор поведения, **не authority**; `:campaign_strict`, token или caller Bool
не удостоверяют admission. Не добавлять S1 policy в physics/YAML model или portable
result schema. Frozen S1 launcher должен явно bind этот keyword; standalone output
не получает S1-admitted claim. Названия можно менять только до D acceptance.

Campaign selection валидируется до output root/plan/attempt allocation. Missing
envelope/unknown policy даёт отказ. Explicit envelope передаётся дальше напрямую;
`_scientific_memory_reservation` получает envelope аргументом и не вызывает
ambient default второй раз. Callback `_native_phase_request(...; resource_policy=...)`
и strict OS probe получают тот же immutable policy. В standalone kwarg по умолчанию
сохраняет нынешние permissive callbacks, fallback probe и memory authority semantics.
Общие arithmetic исправления применяются к обоим режимам.

Отдельный strict reader в linux_resources сохраняет статусы `finite`, `unlimited`,
`unknown/malformed/out_of_range`; legacy `_resource_integer` не меняет sentinel API.
Из raw `"max"` не получается finite value или measured zero. Требуются доказанные
cgroup-v2 path/ancestor chain и finite effective hard bound; known `max` допустим
на отдельном ancestor при полном chain и другом finite bound. Missing/unreadable/
malformed ancestor запрещает strict permit, даже если другой ancestor finite.
Missing self/cgroup не выдаётся за actual root. Current должен быть известным
nonnegative finite Int для всех applicable bounds; malformed current не0.
Все raw override CPU/thread/count inputs проверяются с исключением Bool и range;
strict CPU affinity/quota/path unknown не маскируется host fallback. Это validation
input mechanics, не native ownership/freshness/CPU-max proof.

В strict phase permit: directory=nothing, missing burst, missing finite bound,
unknown current/limit, invalid task_width или overflow отказывают до allocator
continuation. Unknown до GC/receipt writer по возможности; known insufficient
capacity использует существующий GC+resample, затем pressure exception. Clean cache
credit=0 сохраняется; burst=0 не отменяет проверку known bounds/current.
Сравнение выполняется checked через `required=current+burst; required<=limit`.
Exact fit разрешается, limit−1byte отказывает. Kernel `max` не нулевой current.

До объединения R2/R3/P1/P2/A1/C1 строгий campaign entry **обязан оставаться closed**
с явной причиной `needs_guard`/`needs_admission`; source I R1 не должен разрешить
scientific execution через частичный guard. Минимальная безопасная реализация R1
сейчас — fail-closed entry для campaign-strict плюс independently callable strict
scalar/probe/phase helpers. Не вводить `guards_complete=true` или fictitious proof
object. Подключение принятых owning guards позже — отдельная reviewable integration.
Строгие fake helper tests не считаются production S1 launch.

## 5. Независимая manufactured matrix

Denominator: 31 required property groups (F1–F6, B1–B5, D1–D4, S1–S9,
O1–O4, L1–L3). Внутри строки все перечисленные perturbations обязательны;
неприменимые/missing не пропускаются. Oracle — literals или test-local BigInt
арифметика; она не вызывает production forecast/validator для expected результата.
`M=typemax(Int)`. Fake paths/counters only; no actual /proc/cgroup/disk measurements.

| Group | Given / independent oracle | Required observation |
| --- | --- | --- |
| F1 | NE2,Nk3,Nb5,K=[7,11],F13 | literal forecast16854140 bytes |
| F2 | NE=Nk=Nb=1,K=[],F0 | literal16777728 bytes; zero kernel sizes legitimate |
| F3 | Each dimension independently true,0,−1,1.0,nothing,M+1 | Reject before allocation/size factory |
| F4 | K entry and F independently true,−1,1.0,nothing,M+1 | Reject; unknown size not0 |
| F5 | Six isolated overflow sites: Nb²;128*NE;sumK;A+K;4*(A+K);C+scaled | BigInt expected >M at selected boundary; no wrapped finite permit |
| F6 | Representable scalar upper boundary, then increase one exact operand by1 | First literal BigInt fit agrees; second rejects; do not allocate |
| B1 | used17,reserve3,additional5,budget25 | exact-fit permit; used17 returned |
| B2 | B1 with only budget24 | reject; all other inputs unchanged |
| B3 | used0,reserve0,additional0,budget1; used26,budget25,reserve/add0 | known zero permits; already over-budget rejects |
| B4 | Each argument independently Bool/negative/float/nothing/>M; budget0 | Reject before storage-reader sentinel |
| B5 | used=M,reserve1,additional0; used=M−1,reserve1,additional1 | First and second addition overflow independently reject |
| D1 | available25,required25 | exact-fit permit |
| D2 | D1 with only available24 | reject1byte short |
| D3 | available=required=0; each value independently Bool/negative/float/nothing/>M | known zero permits; malformed rejects |
| D4 | diskstat unavailable/throws; invalid required with reader sentinel | no fabricated0/unlimited; invalid required rejects before reader |
| S1 | Fake3-ancestor chain with root max, parent finite100,leaf max; all currents known90,burst10 | strict exact-fit permit; task width bounded by fixed pool |
| S2 | S1 only finite bound99 | pressure refusal; allocator sentinel0; optional GC resample remains99/90 |
| S3 | Each memory.max independently blank/malformed/negative/>M/missing | strict refusal; cannot filter bad ancestor as unlimited |
| S4 | All memory.max max; no groups; missing/wrong self/cgroup | strict refusal; no implicit root/finite hard grant |
| S5 | Each applicable current independently blank/max/malformed/negative/>M/missing | strict refusal; no current0 fallback |
| S6 | Burst absent/nothing/Bool/negative/float/>M; directory=nothing | strict refusal; unavailable does not pass |
| S7 | Known current90,burst0,bound100; unknown current with same burst0 | first permit; second refuses |
| S8 | task_width Bool/0/negative/float/>M; current=M,burst1 | refuse before width conversion/allocation; pressure sum checked |
| S9 | Missing/invalid CPU affinity/quota/chain and invalid override counts | strict preflight refuses; known max retains distinct status |
| O1 | strict entry missing envelope, wrong policy, missing remaining guards | fail before output-root/plan writer and problem allocator sentinels |
| O2 | malformed forecast then writer continuation | writer sentinel0; source trace confirms actual commit calls same core before generation writer |
| O3 | strict phase missing burst then phase allocator continuation | allocator sentinel0; no success admission row |
| O4 | healthy tiny finite gate control | sentinel1; proves refusal sentinel can fire; no solver/HDF5 payload needed |
| L1 | existing `default_execution_envelope()===nothing` and manual envelope=nothing | standalone semantics remain |
| L2 | existing native callback with directory=nothing/missing burst | legacy unavailable behavior remains only standalone |
| L3 | existing Linux legacy malformed/max/current fallback fixtures | legacy compatibility assertions remain; strict sibling refuses same bad input |

F5 uses tiny scalar construction, e.g. `isqrt(M)+1` for Nb², `fld(M,128)+1`
for128*NE, K=[M,1] for sum, K=[M−127] for A+K, and test-local exact
BigInt formulas for the final factor/addition thresholds. No production helper
calculates its own oracle. F6 choose NE=Nk=Nb=1 and vary a kernel size at
floor((M−C)/4)−128; exact representable expected is computed independently.

Sentinel limit: a gate-then-thunk control proves gate ordering only. To claim actual
entry ordering, bind the thunk to the production private preflight seam used by
execute_scientific_plan/phase callback and inspect actual call path. A separate
toy `guard(); writer()` test alone cannot close O1–O3. Do not construct a huge
NEGFSolution, call existing solver fixture, or run full publication to test refusal.
No claim of every-HDF5-write enforcement follows; that remains R2.

D2 oracles E90GiB/U4/P8/S3, T105/G15, A105 then A−1, H15 then H−1,
Hnet11/R4 then Hnet−1 remain required R2/P1/C1 controls. R1 tests must not
silently implement a second lease ledger or claim those later controls passed.

## 6. Точная будущая test selection и distinct finite envelope

Сейчас ничего из этого не авторизовано к исполнению; C08=8/8 exhausted сохраняется.
Предложение координатору **SCI08-R1-ENG-1**, отдельный от C08 engineering grant:
1 Julia process invocation, max_attempts1, no automatic retry;1CPU/2GiB RAM,
wall≤600s, output≤1MiB, temp fixture writes≤16MiB; no installs/instantiate/precompile,
no scientific solve, no profiling/benchmark/native access/network. Prepared environment
и exact new candidate ref должны быть bound до READY. Если runtime/packages missing,
unknown outcome, cap или identity mismatch — stop и сохранить original log.
Исправление после failed call требует нового явного оставшегося finite test allowance.

Proposed new test files в Runner, каждый independent module, using existing
`test/support/common.jl` pattern:

1. `test/contracts/checked_storage_forecast.jl` — F/B/D (15 groups).
2. `test/infrastructure/strict_campaign_resource_admission.jl` — S/O (13 groups).
3. Existing `test/application/execution_resource_contract.jl`.
4. Existing `test/infrastructure/linux_process_resource_probe.jl`.
5. Existing `test/integration/native_phase_resource_contract.jl` — последние3 дают L1–L3.

Один вызов в prepared Runner workspace, без группового runner:

```sh
julia --startup-file=no --check-bounds=yes --project=test -e 'for f in ["test/contracts/checked_storage_forecast.jl", "test/infrastructure/strict_campaign_resource_admission.jl", "test/application/execution_resource_contract.jl", "test/infrastructure/linux_process_resource_probe.jl", "test/integration/native_phase_resource_contract.jl"]; include(f); end'
```

Итого 1 process call/5 named file includes/31 property groups. Exact assertion count
фиксируется I diff до ENG_READY; future reviewer проверяет, что все parameter rows
развёрнуты. Не include `resource_pause_checkpoint_provenance.jl`: он вызывает
solve_scba_production. Не include C08/whole infrastructure/integration suites.
Existing phase test использует fake cgroup и production phase begin/end, не solve.
Existing run_group включает всю группу, поэтому для этого envelope непригоден.

Source-derived estimate: body tiny scalar/fake-file controls; scientific iterations0.
Wall dominated package load/JIT, количественных прошлых timing receipts нет.
Planning estimate2–10min, верхняя граница600s — proposed stop budget, не benchmark
или обещание fit2GiB. Entry seam design может потребовать дополнительный fixture
file; это изменение selection должно попасть в accepted ENG plan до вызова.

## 7. Implementation handoff и сохранённые границы

После independent high PASS_SOURCE этого D: один medium owning I в Runner, ≤2 code
rounds в общем SCI08, no product writes этим D. D before ready I; полный patch и
31-group disposition затем отдельному high reviewer на неизменяемом candidate.
Source-only checks сейчас — source/hash/Git metadata reading. Даже PASS_SOURCE I
без ENG evidence не даёт runtime pass. Publishing Runner PR/gitlink — coordinator
scope; root/Contracts edits не нужны для private helpers и неперсистируемой policy.

S1 invariants сохранены:0mV/period, lattice/LO70K, LO/acoustic/impurity/IFR/alloy,
electron_electron=none;13 attempts/936 execution node-hours/72h per attempt,
concurrency≤2, one threaded process/node, BLAS1. W1 four attempts:128GiB resident,
2TiB writes/4TiB reads/1GiB logs each; remaining9:256GiB/4TiB/8TiB/1GiB.
Shared resident2TiB, cumulative44TiB writes/88TiB reads/13GiB logs. Stop resources
внутри прежних caps. Grids/basis/window/mixing/tolerances/acceptance не меняются.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 arithmetic и unknown gaps локализованы | Runner fefaa27 symbols§2, hashes identity | Это source observation | изменить |
| Минимальный строгий путь может сохранить standalone API | Explicit policy/envelope propagation§4, L1–L3 | Proposed API до high D acceptance | изменить |
| R1 tiny controls различают границы и ordering | Literal oracles/paired1byte controls§5 | Не исполнены; sentinel actual seam обязателен | дополнительно измерить |
| C08/S1 caps и модель сохранены | D1+D2 + invariants§7 | Science/test calls0 | сохранить |
| Полный campaign resident/cumulative/native guard готов | R2/R3/P1/P2/A1/C1 отсутствуют в R1 | strict campaign entry остаётся closed | данных недостаточно |

STOP. Артефакт D не открывает runtime, C08, native admission или научный запуск.
