# SCI07 — условный finite resource/storage admission для S1

2026-10-20. Source/design ultra, independent high R далее. **Статус: needs_admission.**
Научных submits, native/server probes, imports/parsers, solver, tests/build/network
и Git mutations в этом этапе нет. Этот документ завершает source contract и
готовит SCI08 tickets; он не выдаёт CP-SCI READY, native pass или числовую ёмкость
хоста. Missing обязательный input/guard останавливает зависимое действие.

## 1. Scope, полномочия и состав источников

Фиксирована stationary thermal equilibrium **0 mV/period, lattice/LO 70 K**,
LO/acoustic/impurity/IFR/alloy включены, **electron_electron=none** во всех
B0/E1/P1/K1/W2/W3/R/H. Scientific identity, численные сетки/варианты, basis,
window, embedding, thresholds и критерии приёмки остаются у Research/Core и
frozen scientific plan. SCI07 не выбирает новые формулы, solver/mixing или
физические tolerances. Недостаток RAM/storage не разрешает менять эту задачу.

Нормативные входы — science.md SCI07/08 и Admission/guards, P1 operator-permissions
S1/B; исторические PLAN/approved_standby в этих опубликованных документах не
отменяют последующий фактический EXEC/grant пользователя, переданный coordinator.
Текущий порученный этап всё равно только source/design. Engineering grant на
доступные ресурсы не является измерением availability и не снимает scientific
ceilings, foreign/host reserves, protected S01 или CI-once. Неотменённые B limits
учитываются отдельно; B build/store/depot resident budget нельзя тратить как
scientific disk, а общий физический filesystem должен вместить оба с reserves.
Новых вопросов об уже данном S1 approval здесь нет.

Published Root HEAD — `e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b`.
Audit inputs из discovery packet: Core `9f4a96d032ad868ec010ce92d915bb81087c8d92`,
Runner `fefaa27f194bfddf85dd51a0e255beef2218c06d`, Platform
`f729e2681224d6537538179ab760fefefd575003`, AiiDA
`d8f8092ca1c76523d85384b4bac8198d8bfa736b`. Core/Runner/Platform — опубликованные
owning commits в текущем gitlink overlay, а не уже опубликованный final Root graph.
Фактические selected named source bytes проверены immutable git show; hashes и
read ledger приложены отдельно. Наблюдённые refs в этом forensic receipt не
становятся параллельным revision lock. До execution нужен final Git-derived
source graph и Code/release/runtime binding через существующий owning маршрут.
Не следовать latest и не переносить старую full-release приёмку на новый Root.

Assumptions, которые **пока не установлены**: actual resolved configs каждой
variant; allocation/host boot/cgroup identity и capacity; filesystem/NFS namespace,
quota/counters/ownership; terminal copy/export placement; полный upper bound
serialization/audit/native overhead; signed fresh admission и enforced resource
leases. Их нет данных, не ноль. Current dirty checkpoint/прочие writers не
являются scientific input и здесь не меняются. Protected original checkout не
редактируется. Предположение о worker-local scratch для текущего S1 неверно:
при recovery.enabled Runner отключает staged scratch и публикует прямо в output.

## 2. Неизменяемые finite ceilings

| Slots | Attempts / execution node-hours | Resident disk peak /attempt | Cumulative writes /attempt | Cumulative reads /attempt | Logs /attempt |
| --- | --- | --- | --- | --- | --- |
| W1 B0/E1/P1/K1 | 4 / 288 | 128 GiB | 2 TiB | 4 TiB | 1 GiB |
| W2 W/Z/B/A/Q, W3 C, R, H | 9 / 648 | 256 GiB | 4 TiB | 8 TiB | 1 GiB |
| Вся S1 | **13 / 936** | **2 TiB current resident** | **44 TiB** | **88 TiB** | **13 GiB** |

Каждый execution ≤72 h, max_attempts=1 на submit, concurrency≤2, один node и
один threaded Julia process, BLAS1; один доступный worker означает serial.
Переходы волн и два одинаковых последовательных failure fingerprints остаются
science/P1: affected wave stops; remaining slots не дают blind retry. Wall,
CPU-seconds и allocated core-hours хранятся раздельно. Sum execution node-hours
≤936; parallelism не умножает grant. CP устанавливает конечный campaign deadline
и правила charged time по P1, не бессрочный polling при недоступном сервере.

Init/load/JIT, compute, fresh final audit, checkpoint/hash/fsync и stop/transfer,
пока allocation удерживается, входят в её charged wall. Stop reserve находится
**внутри**72 h/936 и соответствующих byte caps. Postprocessing/retrieval/export
не получает бесплатных bytes после process exit: они связаны с исходным attempt
и shared campaign debit. Их собственный CPU/wall stage требует своего finite
поручения; этот D такого запуска не разрешает. Нельзя считать936 core-hours или
обнулять bytes при смене процесса/агента/host/attempt directory.

P1 sums совпадают:4×2+9×4=44 TiB writes,4×4+9×8=88 TiB reads,
13×1=13 GiB logs. Поэтому безопасный minimal handoff — заранее выдавать каждому
из13 slots disjoint maximum read/write/log allowances, включая всех его consumers,
без loans и resets. Resident caps так не складываются:4×128+9×256=2816 GiB>
2 TiB, а finals/failures остаются после завершения job. Resident admission требует
отдельного общего reconcile/reservation перед выдачей каждого resident lease.

## 3. Что фактически установлено исходниками

Все Julia locators ниже — Runnerfefaa27/Core9f4a96d; Platformf729/AiiDAd8f809.
Это source facts, не native measurements или выполненные fault tests.

| Existing producer / locator | Установленный контракт | Существенная граница |
| --- | --- | --- |
| Runner auto_strategy.jl149–173,229–253; Core production_cache.jl431–608,622 | Actual enabled пятиканальный mix передаётся estimator; BigInt-based main inventory, numerical resident/peak, candidate/warm-state/workspace terms; уменьшение equivalent temporary chunk/columns перед отказом | Estimate не total RSS/cgroup peak или runtime guarantee; native/HDF5/allocator/audit liveness и reserves нужны отдельно |
| Runner resource_contract.jl18–54 | ExecutionEnvelope разделяет numerical/runtime/allocator allowances, sum≤hard; token и CPU ids; explicit envelope budget | Token/caller struct сам по себе не scheduler authority/lease; measured allocation proof отсутствует |
| linux_resources.jl1–15,68–87,160–194 | Ancestor cgroup bounds/headroom и affinity/quota probe | Empty/malformed/max сходятся к typemax; unreadable current местами превращён в0. Для строгого S1 это не evidence неограниченности/нулевого расхода |
| native_phase_telemetry.jl138–210 | Phase request, incremental burst, finite cgroup headroom, GC recheck без clean-cache credit; denied phase pauses на last committed state | directory=nothing, burst=nothing или no finite limit могут вернуть unavailable без отказа; source не доказывает fail-closed S1 coverage всех фаз |
| point_artifacts.jl513–545,760–787,986–1057 | Logical roots checked; checked sum; pre-prune pending; receipt и atomic pointer tail сериализуются/резервируются; publish/fsync/readback/receipt/pointers до prune | No every-HDF5-write/cumulative/NFS/external-growth enforcement. Forecast528–534 имеет unchecked intermediate arithmetic; archive не проходит recovery logical budget branch |
| hdf5.jl30–121,128–144,267+ | Native arrays lossless split-complex, deflate1, bounded1 MiB serialization slab; kernels/full state/restart provenance | Slab cap не heap/RSS/disk cap; HDF5 chunks/metadata/native cache/deflate expansion/write amplification требуют bounds |
| scratch_execution.jl34–112 | Source+pending-copy+reserve; observed free space перед controlled1 MiB copy; digest/readback/fsync/atomic rename | Not quota, не reserve против других writers; repeated hash/native verify reads; private staging temp cleanup не означает сохранение всех failed temp bytes |
| scratch_execution.jl134–136 | При portable recovery.enabled normal compute идёт в output storage; scratch staging disabled | Для S1 нельзя считать все I/O local block I/O. NFS coverage обязательна |
| scientific_execution.jl1080–1162,1264–1278,1377–1382 | Recovery callbacks, несколько triggers; full final archive обязательный; resource pressure использует ранее committed boundary | Timer не единственный trigger; final archive отдельный путь; pressure без checkpoint не создаёт resumable current state |
| Runner docs/results.md128–144 | Честно обозначены publication-boundary logical count и incomplete AC2 | Docs/source presence не устанавливает native quota или counter coverage |
| AiiDA validation.py76–104, calculation.py126–147 | One process/node, Julia threads/BLAS1; optional max_memory_kb; retrieval archive/recovery/executions/stdout/stderr, recovery/prior-archive copies | Resource request не actual cgroup; retrieval volume/log growth не ограничиваются этой list декларацией |
| Platform cluster.nix53–75,89–100; storage.nix17–25 | Cgroup-v2/cores/RAM/swap config intent; hard NFS4 mount, sync export, non-root persistent disks | Actual boot/config/limits/quota/NFS durability/cumulative coverage не измерены; declared NFS layout сам не guard |
| Platform host_storage_receipt.py1–16, slurm_job_evidence.py1–51 | Existing bounded cutover receipt и read-only job/PID/cgroup identity evidence | Не переименовывать эти B/OPS records в S1 resource authority/cumulative enforcement proof |

SCI04-D2 задаёт fresh final-map/audit measurement, current owning implementations
должны оставаться обязательными; исторические gaps D2 не утверждаются заново как
current defects. Его record cap64 KiB — metadata allowance, не весь audit cost.
SCI03-M1 review§4 увеличивает total tile allowance24→32 complex slots и
добавляет12 KiB к прежним fixed terms, сохраняя отсутствие нового data pass; это source accounting, не
measured Python/HDF5 RSS. При будущем чтении продолжают действовать actual
physical I/O callback, chunk/workspace/report caps и отдельно admitted read stage.
GREEN fixtures, если coordinator их имеет, не устанавливают S1/model acceptance.

## 4. Обязательные admission inputs и их доказательство

Не вводить второй общий schema/lock или daemon. Поля ниже — content obligations
существующих finite CP-SCI/Platform/AiiDA/Runner attempt receipts, не новая публичная
serialization. Если SCI08 понадобится новый переносимый field contract — сначала
owning Contracts change с independent review; не private schema по догадке.
Связывать exact retained bytes/hash/path и existing trusted signer/authority.
Hash/status/token не криптографическая подпись. Требуемая подпись/attestation
проверяется по уже принятому trusted identity; отсутствующий signer/admission
не заменяется самоподписанным JSON или новой trust root.

| Required content | Scope / units / binding | Условие допуска |
| --- | --- | --- |
| Campaign/slot/point/run/attempt | Existing IDs, catalog/frozen-plan/criteria/sourceGraph/release/runtime digests; parent attempt и remaining budgets | Exact active S1 membership,0 mV/70 K/5 channels/e–e none после resolve; no borrowed old S01 identity |
| Host/allocation | Host/machine/boot, VM/hypervisor, worker, Slurm job/step, process start/cgroup subtree, ancestors, namespace/mount IDs; controller observation time | Owned campaign target, no foreign cancel/reclaim; actual CPUs/affinity/quota/RAM mapping, unchanged authority |
| Memory | Bytes: physical/available/current/high/max/peak/events по всем applicable ancestors, runtime/allocator/numerical/serialization/audit/stop allowances | Complete finite effective bound и disjoint accounting, snapshot freshness; неизвестный ancestor/current/burst не pass |
| CPU/time | CPU ids, effective quota cores, threads/BLAS, allocated CPU count, monotonic start/deadline, charged/remaining node-wall, core-hours separately | ≤fresh authority after host/foreign reserves; pool provisioned before launch, BLAS1; compute+stop помещаются |
| Filesystem map | Each active source/destination/tmp/log/cache/repository/export root → actual FS/storage identity, mount namespace, NFS server/export identity, ownership/quota attribution | No undeclared copy domain; aliases dedup by proven backing store, non-root/protected-data constraints; unknown placement blocks |
| Capacity | Bytes/inodes: allocated+logical current, free/available, quota hard/remaining, host/foreign/build/site reserve, outstanding S1 resident leases | Exact per-FS and aggregate worst-case simultaneous peak+stop+protected reserve fits **both** authority and S1 caps |
| Inventory/events | Per artifact dataset/shape/dtype/bytes, chunk/filter metadata bounds, histories/config/receipts/pointers/logs/telemetry; max event counts/phase liveness | No compression credit or omitted optional/failed path; finite bound before growth, checked arithmetic |
| Cumulative I/O | Per operation and storage domain cumulative read/write baseline, counter epoch/units/coverage, protocol/hash/copy inclusion, transferred bytes and observer self-cost | Conservative complete accounting+enforcement before cap. Coverage proof spans NFS/remote/retrieval/export, not only worker block io.stat |
| Log/telemetry | All stdout/stderr/scheduler/Runner/native/observer/transfer logs, rotations and copies; telemetry buffers/segments/flush | External capture/production limits, retained bytes and pending tail charged; no discarded output called complete |
| Stop/fault capability | Bound time/CPU/RAM/disk/reads/writes/logs/inodes for frozen growth→verify last state→receipt/fsync→quiescence, last verified pointers | Durable stop reserved before work; native enforcement/fault proof as applicable; no ENOSPC/OOM stop strategy |

Преобразование AiiDA max_memory_kb/Slurm limits в bytes также связывается с
actual owning adapter/tool version; label kB не разрешает угадать1000/1024 или
округлением превысить effective hard grant.

Every observed counter carries value or null, status/reason, units, subject/scope,
source tool/path/version, host/boot/cgroup/storage epoch, before/after timestamps,
coverage and actual sample interval. Legitimate kernel `max` отличается от
unreadable/malformed/missing; it does not remove finite S1/application limits.
No fresh value supplied here. Counter reset/wrap/PID reuse/reboot/mount change/
permission loss/stale sample/negative delta разрывают continuity. Unknown value
не0; unknown extent неempty. Сохранить last durable debit, outstanding tokens
считать израсходованными/зарезервированными до trusted reconcile, не выдавать
освободившийся grant из missing tail.

Freshness max age и worst observation/stop lag должны быть конечными и привязанными
к admitted actual mechanism, не выдуманным универсальным cadence. Sampled RSS/free
space/counters не являются hard guard: между samples нужно резервировать полный
bounded growth/in-flight bytes либо иметь independent enforceable owner limit.
Unsupported capability → needs_admission/needs_guard, а не sampled pass.

## 5. Memory/CPU admission: два разных predicate

1. **Plan before allocation:** existing exact estimator output и breakdown на
   actual resolved dimensions/algorithms/workers + все отдельно не включённые
   runtime/native/allocator/HDF5/serialization/history/audit/stop costs должны
   поместиться в численно frozen ExecutionEnvelope. Numerical+runtime+allocator
   (с явно размещённым stop allowance)≤hard≤fresh effective allocation after
   host/VM/foreign reserves. Сравнить с фактическими ancestor constraints и swap
   policy, не с machine catalogue. Memory cache reclaim нельзя считать эксклюзивным
   свободным ресурсом. Бюджет другой VM/build/job не является доступным.
2. **Before each growth/phase:** actual current memory + conservative **incremental**
   simultaneous phase burst + ещё не занятый stop margin≤каждый applicable bound.
   Не складывать total estimated peak с current, уже содержащим те же arrays;
   liveness ledger указывает existing/reused/new buffers и момент освобождения.
   Full final raw audit, Poisson-map, serialization, consolidation и transfer/
   reader caches имеют свои phase bounds. Missing burst или cgroup coverage —
   refusal до allocation в S1, не general low-level no-op с unavailable.

Estimator counts candidate_generation/retained_warm_start/physics witness pools,
но это не повод второй раз добавлять те же массивы или объявлять полную runtime
liveness доказанной. На source stage невключённые overheads остаются required
input, не arbitrary safety multiplier12–13 GiB. Rough B0/E1 numbers science.md
не RAM request и не measured RSS. Увеличение доступного CPU может увеличить
worker workspaces; выбирать только existing equivalent execution options и
повторно оценивать memory, сохраняя plan/scientific identity. Fresh resource
lease нужен и для2 concurrent executions, с суммарным host/VM budget.

## 6. Storage inventory и pre-prune peak

Пусть C=16·NE·Nk·Nb² — **uncompressed** bytes одной полной ComplexF64 state array.
Core/Runner не выполнялись для получения этих размеров. Full native owner пишет
4 Green arrays GR/GL/GG/A,3×5 scattering families и3×3 embedding families:
28C только этих fields. B0 C=135172400 B,28C=3784827200 B;
три такие копии =11354481600 B **до** kernels/basis/histories/metadata/analysis.
Это консервативный uncompressed planning inventory, не measured compressed disk
lower bound и не утверждение, что любой actual generation обязательно столь велик.
Deflate1 есть; credit за будущую compressibility не используется для admission.
Нужны отдельные finite deflate expansion/chunk/HDF5 metadata/allocation bounds.

Обязательный полный inventory включает:

- physics.h5: state/selfenergy28C, kernels Khat actual shapes+F_LO, h/U/density,
  condition_number/dyson_scale, grids/weights, profiles/basis, numerical/model/
  toolchain/algorithm identity, histories/witnesses/final-audit record;
- analysis.h5 при analysis=true: native observables/spatial-energy density,
  projections/basis/history/audit copies, без выдуманного полного Green дубля;
- consolidated history.h5 **и** продолжающие существовать source histories,
  resolved_configuration.json, recovery.json reference (не второй physics owner),
  execution_progress.json, commit/receipt and current/previous pointer files;
- active attempt/result/telemetry/log/control files, imported recovery/earlier
  archives, incomplete/failed/unacknowledged published generations, finals всех
  завершённых/failed attempts, staging/retrieval/AiiDA repository/export copies;
- temporary compression/chunk/atomic pointer/receipt metadata, file+directory
  allocation/inode overhead, cross-filesystem copy simultaneous source+destination.

Для каждого filesystem f построить phase/lifetime table. На recovery publication
считать старые retained generation1+2, **полную pending generation3**, старые
pointers и новые receipt/current/previous atomic temps, текущие attempt/history/
log/telemetry, immutable finals/imports и отдельный durable-stop reserve. Только
после verified receipt/pointer acknowledgement existing prune может убрать surplus
recovery; не кредитовать это освобождение заранее. При failed/unacknowledged
публикации учесть всё реально оставшееся до следующего admission.

При final archive считать retained recovery + full pending final/analysis/history
+ metadata/receipt + existing immutable finals + stop reserve. Final не проходит
ветку recovery logical-budget check, поэтому его growth требует campaign guard
на existing archive path; нельзя уменьшить full_final или удалить failed raw.
Prior-point final archives участвуют и в pause/stop verification, включая повторные
hash reads. archive_byte_budget default64 GiB — checker bound, не capacity;
actual prefix должен fit отдельно привязанный budget и remaining reads.

При recovery import считать source bundle+local imported copy+prior archive copies
и все уже имеющиеся roots. При stage_result_tree/copy/transfer/export считать обе
копии до verified publication, независимо от разных filesystems. Один и тот же
backing filesystem по двум mount aliases нельзя считать двумя независимыми
пулами capacity. Hardlink/dedup/reflink/compression savings не кредитовать без
immutable ownership/lifetime proof. Консервативно сравнить и logical upper bytes,
и allocated physical upper bytes+metadata с соответствующим resident allowance.

Required predicate в каждой reachable phase: existing resident + all outstanding
reserved growth + proposed growth + remaining stop reserve≤min(owned authority,
free/quota after protected reserves, assigned attempt bound); shared simultaneous
resident across **всех** filesystems/copies≤2 TiB. Inodes проверяются отдельно.
Resident includes logs; логовый cap не добавляет ещё1 GiB сверх resident cap.
Числовых free/quota/lease values здесь нет, следовательно predicate не proven.

8 GiB recovery default/64 MiB reserve остаются implementation defaults, не доказанный
S1 admission. Даже uncompressed2retained+pending baseline inventory не допускает
консервативно сертифицировать8 GiB без compression credit/полного inventory.
SCI09 должен freeze вычисленный recovery operational budget/reserve внутри
назначенного S1 lease послеSCI08; не молча повысить глобальный default или считать
128/256 GiB реально доступными. При невозможности fit — blocked, не physics edit.

## 7. Cadence и cumulative bytes

72 h /1800 s =144 nominal interval slots. **Это не верхняя граница всех checkpoint
publications.** scientific_execution observer/checkpoint_request также вызывает
snapshot и SCBA/outer cadence. Core defaults checkpoint_every_scba=25,
checkpoint_every_outer=5; actual resolved config ещё не bound и может отличаться.
По source-only максимум2048 SCBA×128 outer при every25 уже даёт10368 cadence
opportunities, отдельно outer/snapshot/stop; это worst-case count illustration,
не наблюдение production write count и не новый разрешённый compute budget.

Admission обязан получить actual positive/disabled cadences, iteration limits,
observer triggers, timer reset/coalescing semantics и max manual/pause/terminal
calls. Conservative event bound Nrec≤Ninterval+Nscba+Nouter+Nsnapshot+Nstop/import
считает overlaps повторно, пока их coalescing не доказан. Include history growth,
repeated consolidation и verification; retained2 ограничивает resident, **не**
cumulative rewrites/hash reads. Для history использовать bound каждого события,
а не final-history bytes×1. Recovery storage checks также сканируют metadata;
verification/prune может повторно hash retained payloads. Sufficient exact bound
считается по owning call graph, не по названию «checkpoint».

Per phase/operation inventory задаёт request upper reads/writes/log bytes,
resident incremental peak, metadata/protocol overhead, max invocations и stop cost.
Перед I/O debit/reserve, после — actual counter reconciliation; не переносить
неизмеренный unused остаток. Logical application reads включают hash/readback/
verify/copy/parser/export даже при page-cache hits. Запись HDF5 chunk/metadata,
transfer payload/retries и внешних logs не исчезает из бюджета. Counter coverage
matrix определяет, какие реальные действия покрывает каждое наблюдение; один
и тот же underlying event не суммировать повторно как два независимых измерения,
но отдельные copy/hash/transport phases обязательно charge отдельно. Нельзя брать
max/min несовместимых cgroup/block/NFS counters и назвать его полным расходом.
Conservative overreservation допустимо явно, undercount или blind compression
credit — нет. Physical/storage amplification/protocol coverage остаются required
proof, если logical producer accounting их не покрывает.

Cgroup io.stat не считается NFS coverage. Даже project quota/resident free-space
limit не ограничивает cumulative overwritten bytes/reads. Для текущего recovery
NFS path Platform должен предъявить storage-side attributable accounting и
исполняемый admission/stop механизм **либо** доказанно полную bounded-I/O coverage
всех writers/readers/transport с резервированием до каждого bounded operation и
независимым resident enforcement. Выбирать недоказанный механизм наугад нельзя;
отсутствие complete mechanism — SCI08/native blocker, не READY. Samples сами не
обеспечивают cap между samples. Observer/telemetry self-cost тоже charge.

Самый маленький общий ledger не требует нового параллельного writer: coordinator
использует existing campaign/slot state и выдаёт disjoint operation allowances,
owning Runner/AiiDA/Results/transfer consumers возвращают immutable attempt-bound
receipts. External permissions не должны позволять unaccounted side writers.
Перед new resident lease coordinator сохраняет authoritative reconcile текущих
finals/failures/copies+outstanding leases; одновременно выданные budgets не могут
обещать один и тот же свободный byte двум jobs. При потере consumer/counter tail
его outstanding allowance остаётся debited/reserved. Никакого второго manual Git
revision list или независимого campaign status journal не создавать.

## 8. Durable stop reserve и state machine

До допуска normal growth отдельно зарезервировать по каждому f объём/inodes,
read/write/log allowance, CPU/RAM и wall для **конкретного** stop path.64 MiB —
только existing floor/default, не универсальное доказательство достаточности.
Stop reserve содержит оставшиеся metadata/pointer/receipt temporaries,
verification hashes/prior archive reads, bounded log/telemetry flush и fsync;
если путь должен создать новый accepted-boundary generation — также весь этот
payload и serialization/native workspace. Уже включённый payload нельзя считать
дважды; нельзя считать возможность будущего prune средством финансирования stop.

```text
needs_admission -> admitted lease -> running
 running -> growth denied / pressure / approaching deadline
         -> freeze new optional/compute/copy growth
         -> verify last acknowledged compatible state (если существует)
         -> existing pause/stop receipt + bounded flush/fsync + quiescence
         -> paused/terminal with verified provenance
```

Resource guard не делает current partially evaluated G/Σ accepted boundary.
Использовать existing exception/pause path и последний verified generation.
Если до первой публикации state отсутствует — сохранить explicit no_state/
no_verified_checkpoint terminal metadata; не выдумывать resumable checkpoint или
scientific pass. До первой required publication нужен bound её полного роста.
Existing full final, если уже immutable committed, не отзывается более поздней
operational ошибкой. Complete/full raw failures и protected old data не удалять.
Owned incomplete staging temp cleanup existing writer не означает обещания сохранить
каждый промежуточный byte; его событие/ошибка и last verified inputs/receipts должны
оставаться. Не вводить второй atomic/fsync writer вместо existing producer.

Trigger before next normal operation, когда remaining resource < next-operation
bound+stop bound, включая equality semantics: точное равенство допускается только
при доказанном полном upper bound; one-byte-short отказывает **до** изменения
acknowledgement/prune. До wall deadline оставить bounded stop time внутри cap.
Не начинать audit/final/copy, если их complete worst-case плюс stop не помещается.

NFS hard mount и local publication_scope не дают bounded remote completion при
LAN/powerloss. Требуется отдельное native доказательство либо явный отказ от
READY для зависимого действия. Kill PID/direct child не доказывает остановку всех
writers/blocked I/O; Slurm/cgroup/process-tree quiescence и remote committed data
проверяются по actual authority. Если durable stop не завершился — failed/unknown,
original logs/partial receipts сохраняются, cancel/retry не становятся automatic.
Нет стратегии «упереться в quota/ENOSPC/OOM и назвать это нормальным stop».

## 9. Ready source guard tickets для SCI08

Tickets ниже готовы к **source I** после независимого high R. Native admission
и реальные quotas/NFS/LAN/powerloss checks остаются blocked без fresh facts.
Owning writers отдельные, ≤2 code rounds в общем SCI08 cap; tests запускаются лишь
в отдельном принятом finite envelope, не этим D. Изменять только адресный gap,
не создавать parallel persistence writer. New portable format — Contracts first.

| Ticket / owner | Exact proposed source locus и минимальное изменение | Required controls / evidence |
| --- | --- | --- |
| SCI08-R1 Runner: checked forecast and strict S1 unknowns | point_artifacts.jl::_checkpoint_storage_forecast/_check_storage_budget/_check_storage_free; resource_contract.jl, linux_resources.jl и native_phase_telemetry.jl strict campaign entry. Все intermediate products/additions/size conversions checked или BigInt→checked Int; unknown/malformed/current/burst не0/max/unlimited для admitted S1. Low-level standalone defaults не превращать молча в новую policy | Huge dimensions/Bool/negative/overflow/unknown limit/current; exact-fit и1-byte-short; missing phase burst отказ до allocator/writer sentinel; реальные allocations не нужны для controls |
| SCI08-R2 Runner: common resident/growth gate | Existing commit_point_artifacts recovery **и archive** branches, hdf5.jl::_write_slab_array/native metadata paths, scientific_execution durable_state/final, consolidate history/import paths. Bind immutable operation allowance к existing attempt/source/FS inventory; reserve полный operation bound до открытия/growth, reconcile actual bytes; не только after-file size |2retained+pending+receipt+old/new pointers; final при retained recovery; history/source coexistence; failure before/after rename/receipt; last pointer и finals не теряются; old closure/C08 regressions сохраняются |
| SCI08-R3 Runner/Platform: stop reservation and coverage | _native_phase_memory_permit!, scientific_execution resource-pressure catch и existing pause/stop receipts; existing Platform job/cgroup authority. Freeze next growth до cap, preserve last acknowledged boundary, account stop resources, verify process-tree quiescence | pressure before first checkpoint явный no-state; pressure после verified checkpoint provenance; insufficient stop budget отказ до compute; unknown/timeout stop не paused-pass; external log growth/observer loss retained failure |
| SCI08-P1 Platform: actual capacity/authority inputs | Existing cluster.nix/storage.nix resource ownership и measured private site inventory, existing Slurm evidence paths. Реальный job/cgroup ancestor bounds, quotas/reserves/FS identities, owner-scoped resident enforcement и safe max CPUs/RAM after foreign/host/build reserves | Signed fresh admission/boot/namespace/job binding; finite cgroup ancestors; foreign/S01 protected; aliases/shared FS/concurrent leases/inodes; declared Nix не native pass |
| SCI08-P2 Platform+Runner: cumulative coverage/debits | Existing job/attempt resource receipts и controlled I/O boundaries: all HDF5 writes+hash verification/staging/import/log/telemetry. Предъявить exact local+NFS attributable coverage/enforcement; нет coverage — preflight refuses S1. Quota alone не accepted cumulative guard | NFS blind io.stat, counter reset/wrap/stale/negative delta, budget near0, unaccounted side writer, blocked in-flight write, protocol/retry/log amplification; one-byte-short до operation; no sampled/quota substitute |
| SCI08-A1 AiiDA/Runner, Results/export owning consumer | calculation.py retrieve/local_copy lists и parser recovery/archive validation; scratch_execution stage_result_tree/imports; existing Results StateReader/export budget callbacks. Before consumer operation bind source attempt allowance, all duplicate FS lifetime peaks и reads/writes; preserve UUID only when actual AiiDA node exists | Recovery+prior archive import, retrieval plus repository copy, two points/attempt reuse, export duplicate, bad/missing manifest/counter; archive prefix>checker cap blocks; no invented UUID/no gratis post-exit read |
| SCI08-C1 Coordinator/owning receipts | Existing single campaign/catalog/checkpoint authority only: slot reservation, outstanding resident leases, monotonic consumed wall/attempt/bytes, retained failures and admission refs. No second hand-written revision lock/state writer |2 concurrent jobs cannot reserve same remaining capacity; observer crash/restart retains debit; no bytes/attempt reset on agent/host change; all13/936/caps and per-wave controls preserved |

Source controls используют literal dimensions/fake FS/counters/writer sentinels
и existing recovery/archive/C08 fixtures; нельзя начинать full-size arrays/solver
для проверки отказа. Tiny controlled fixtures доказывают ordering/arithmetic,
не реальные quota/NFS durability. Native faults требуют отдельного Platform
scope/admission, actual targets/process ownership и ограниченного fault envelope.

## 10. Conditional CP-SCI decision и missing facts

Для каждого конкретного slot технический READY возможен только при одновременном
закрытии: final source/release/plan/model/criteria bindings; source SCI08 guards +
independent review; fresh authorized host/cgroup/FS allocations; complete bounded
inventory/event counts и estimator/liveness/headroom; per-FS/shared resident
fit; monotonic cumulative+log coverage/enforcement; durable stop+deadline reserve;
actual checkpoint/archive/retrieval ownership/durability proof по соответствующим
native gates. Model/physical/discretization acceptance остаётся отдельным verdict.

Сейчас все actual availability/peaks/counters/quotas/NFS latency/stop hard bounds
имеют null/not_measured с причиной отсутствия fresh inputs. Нет подписанного
native resource admission, final Root graph или S1 artifacts. Поэтому:
**source design frozen, guard tickets ready for source review/I; CP-SCI resource
status needs_admission (и названные coverage gaps needs_guard), scientific READY
не выдан**. Доступные независимые source работы могут продолжаться. Любое missing
обязательство блокирует лишь dependent action, без повторного human approval уже
утверждённого S1 и без замены данных догадкой.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Baseline science/caps сохраняются | science/P1 exact S1 scope и таблица§2 | Actual resolved/runtime identity отсутствует | сохранить |
| Numerical memory estimator и durable publication ordering полезны | Core cache431–608; Runner artifacts986–1057 | Source facts, не total RSS/AC2/native proof | сохранить |
| Default8 GiB/144 checkpoints доказывают fit | Полный pre-prune inventory и дополнительные triggers§6–7 | Compression/event/runtime facts unknown | данных недостаточно |
| Strict overflow/unknown/growth/cumulative/consumer gaps адресуемы | Named SCI08 tickets и source locators§9 | Не выполнены implementation/fault checks | изменить |
| Actual host/NFS/storage/stop ресурс допустим | Fresh counters/authority/admission не представлены | Никаких probes/solve не было | дополнительно измерить |
| S1 native READY/physics acceptance достигнуты | Нет bound final graph/admission/new scientific artifacts | Source design не substitutes | данных недостаточно |

STOP: этот finite D packet направляется на независимый high review. Product,
shared checkpoint, server и scientific execution не затронуты.
