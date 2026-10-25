# SCI08-R2 — единый resident/growth permit Runner

2026-10-20. **D, source only; передать на независимый high review и STOP.** Это конечный I-контракт одного owning Runner PR, не реализация, не grant на тесты и не CP-SCI READY. Root `107bac5697b37cf0e47c3feb44883a907837645c`, Runner `4f60f1680c6903f79f6d07bf4d14ced74d8c4f3f`. Полный forensic binding и прочитанные диапазоны — в соседних identity/read-ledger JSON. Gitlinks остаются единственным composition authority.

Применён qcl-performance-audit как source audit хранения: analytical forecast, actual resident, RAM/cgroup, cumulative I/O и native evidence различаются. Новых результатов или измерений нет. Предполагаемая научная единица — frozen S1 из SCI07; сетки, basis, окно, рассеяние, tolerances, final audit, `archive.full_final` и исходные failed arrays не меняются.

## 1. Решение и граница одного PR

Предлагается один **Runner-owned capability на конечную операцию хранения**, обязательный при `resource_policy=:campaign_strict`. Он связывает immutable inventory с attempt, campaign, реальными filesystem/quota domains и уже выданным authority reservation. Все Runner writers получают дочерние permits из него; внутренний вызов не создаёт ещё один бюджет. Standalone API сохраняет прежний режим R1. Campaign не может получить standalone fallback, пустой context, unknown→0 или прежний default `8 GiB` как доказательство допуска.

Реализовать source gate и fault fixtures можно отдельно от live authority: production backend без обязательных доказательств **отказывает до первого `mkpath`, temp, `h5open`, truncate, copy или append**. Mock authority доказывает арифметику и последовательность вызовов; native capacity, concurrent campaigns и durability он не доказывает. Это честный, конечный I-ready scope даже при оставшихся P1/C1/R3 blockers: безопасный production outcome тогда — отказ.

R2 не создаёт daemon, service, общий registry, второй revision lock или параллельный atomic writer. Reservation port подключается к существующим coordinator/receipts; отсутствие настоящей межпроцессной authority — `needs_guard`, а не локальный Dict, выдаваемый за shared campaign enforcement. Portal, Core и scientific formulas не меняются. Рецепты kernel/FS quota не добавляются под видом Julia guard.

## 2. Source baseline и точные места интеграции

Все пути ниже относительно `components/QCLNEGFRunner.jl/`, commit выше. Существующие функции — baseline; новые имена явно помечены proposed.

| Caller / владелец | R2 изменение | Сохраняемый контракт |
| --- | --- | --- |
| `src/application/resource_contract.jl` (`ExecutionEnvelope`, `_grant_integer`) | Proposed отдельные storage structs/port в `src/application/resident_storage_contract.jl`; `ExecutionEnvelope` RAM не превращать в disk grant. Include рядом с owning resource contract. | Non-Bool integer validation, checked overflow, явная authority identity R1. |
| `src/infrastructure/persistence/point_artifacts.jl::_checkpoint_storage_forecast_bytes`, `_checkpoint_storage_preflight`, `_storage_bytes`, `_check_storage_budget`, `_check_storage_free` | R1 arithmetic/free guards оставить; forecast использовать только как diagnostic lower-confidence estimate. Новый proven operation inventory и permit проверять раньше `mkpath(root)` в `commit_point_artifacts`, независимо от `storage_class`. | Heuristic forecast не становится HDF5 upper bound. Existing recovery logical budget остаётся дополнительным guard; archive больше не обходит campaign resident gate. |
| `point_artifacts.jl::commit_point_artifacts` (787+, publication 1061+) | Один permit покрывает recovery **и archive**, pending directory, physics/analysis/history/config/progress/commit/receipt и old/new pointer tails. Subpermits на serialize, consolidation, receipt и pointer atomic temp. | Stage→fsync→verify/readback→rename→receipt→pointers→directory fsync сохраняются; last verified pointer и protected finals не заменяются отказом. Нельзя резервировать только размер готового `.h5`. |
| `src/infrastructure/persistence/hdf5.jl::_write_checkpoint` (267+), `_write_slab_array` (77+), `_write_native_dataset`, `_write_array`, `_write_complex`; `point_artifacts.jl::_attach_native_dimensions!`, `save_optical_physics`, `commit_operator_artifacts` | Протянуть scoped storage context от top writer; deny before dataset creation, attributes/dimension scales, slab growth и metadata append. Любой strict reachable writer без inventory/permit отказывает. Альтернативные operator/optical ветви либо покрыты inventory, либо явно strict-refused. | Slab memory bound — RAM, не physical disk bound. Нельзя заменить enclosing HDF5 writer вторым форматом/serializer. |
| `src/infrastructure/persistence/scientific_history.jl::ScientificHistoryRecorder`, `record_scientific_history!`, `flush_scientific_history!`, `consolidate_scientific_history` (243+) | До создания/append segment — ограниченный event-count/inventory и subpermit; consolidation резервирует destination при продолжающем существовании всех source segments. | Нельзя вычитать source history или старый consolidated file до подтверждённого окончания их lifetime. Незапланированные history rows не бесплатны. |
| `src/composition/scientific_execution.jl::durable_state` (1084+, recovery caller 1093), final `commit_point_artifacts` (1267+) | Создать/передать один attempt context из resolved plan и bound admission; phase-specific immutable operation inventory до callback writer. Recovery, failed-state serialization, final и imports используют одну authority, а не reset counter. | R1 prewriter memory/cgroup/boot/free checks, pause/stop provenance и full final остаются. `finally` не выдаёт новый grant. |
| `src/composition/scratch_execution.jl::stage_result_tree` (34+), `execute_scientific_plan_staged` (123+) | Proposed `storage_context`/operation permit keyword; bind source identity, destination filesystem, complete duplicate lifetime до `mkpath/cp`; исходный source — E, destination — P. Local recovery/prior archive import также должен иметь permit. | Existing tree validation, digests, no overwrite и atomic staging сохраняются. Перенос между FS всегда source+destination peak; `rename` с EXDEV не допускает скрытый fallback copy. |
| Exports / retrieval / AiiDA repository / Results (`components/qcl-negf-results/src/qcl_negf_results/export.py`, `export_budget.py`; D1 A1 `calculation.py` retrieve/local-copy) | R2 определяет переносимый immutable operation descriptor и authority callback boundary; чужих writers в этом PR не редактировать. Exact export filenames обнаружены, тела consumer API здесь не audited; A1 начинает с call-site trace своего owner. | A1 обязан подключить consumers; до этого coverage неполная и READY закрыт. Нельзя объявить Runner keyword enforceability стороннего exporter. |

Перед I автор обязан дешёвым source call-site trace перечислить все campaign-reachable opens/appends/copies/atomic-temp paths в этих файлах и подтвердить, что guard доминирует над первой mutation. Непрочитанный direct writer не считается покрытым по сходству имени. Полное содержание HDF5/execute функций здесь не утверждается проверенным: ledger отмечает выбранные диапазоны и усечённые чтения.

## 3. Proposed типы и API

Это локальный application/infrastructure contract Runner, не новый публичный artifact schema. Если later C1/A1 нужен межкомпонентный wire format, его owning Contracts PR отдельный.

- `ResidentIdentity`: campaign/frozen-plan digest, run/execution/attempt/point, exact source/admission digest, lease/operation ID, generation/state sequence; `nothing` не означает unlimited. Не придумывать AiiDA UUID без существующего node.
- `StorageDomain`: filesystem identity + mount namespace/boot + quota/ownership domain; path binding основан на проверенном parent directory, а не только строке пути или mountpoint. Logical attribution group отдельно от physical allocation domain. Symlink/external HDF5/virtual-storage ambiguity — refusal.
- `StorageSnapshot`: authority-issued revision/epoch, finite monotonic freshness bounds, materialized inventory identities и views; total caps A и remaining H с доказанным baseline, applied reserve IDs, inode counts, outstanding leases. Snapshot не caller-created proof из произвольного free число.
- `StorageOperationInventory`: finite maximum simultaneous **additional** logical bytes, physical allocated upper bytes и inode growth по domains/phase; metadata/receipts/pointers/temps/log tails, max history events и all copies; payload digest; declared finite stop-obligation reference. Bounds checked, immutable; compression/reflink/sparse/dedupe saving не предполагать без owning proof.
- `AbstractResidentAuthority`: proposed `resident_snapshot(binding)`, `reserve_growth!(snapshot_revision, descriptor)`, `materialize_growth!(lease, sequence, delta)`, `commit_growth!(lease, evidence)`, `release_unmaterialized!(lease, evidence)`. Atomic compare-and-reserve semantics обязательны; default strict implementation refuses. C1 supplies authoritative concurrency/persistence, P1 supplies native domain authority. Функции не разрешают запуск/native probes.
- `StorageGrowthPermit`: unforgeable within process scoped capability, authority lease ID/revision, descriptor digest, writer/domain binding, residual suballowances и monotonic sequence/high-water; finalization state. Proposed `require_growth!(permit, mutation_descriptor)` до mutations; `with_storage_operation(context, descriptor) do permit ... end` централизует bounded abort/settlement.
- Refusal: отдельный machine reason `needs_admission` (нет fresh physical/ownership/identity evidence), `needs_guard` (нет enforced authority/bound/coverage), `resident_limit`, `stale_snapshot`, `inventory_overrun`, `identity_mismatch`. Existing R1 `ArgumentError`/checked arithmetic behavior и raw unknown/unlimited/malformed statuses не перехватывать в «pass» и не заменять fabricated capacity. Новая typed refusal обязана сохранять cause+phase+identity, без маскировки старых exception contracts.

Проверка fd/path binding нужна перед каждым новым handle и переходом phase; открытый fd привязан к установленному domain. Permissions/namespace/mount/authority epoch изменились — freeze/refuse. Это не устраняет hostile path races само по себе: безопасный native open/dirfd/owner discipline должен быть доказан P1, либо strict backend отказывает.

## 4. Baseline-consistent формулы

Источник — SCI07 D2 §§2–3, принят high `PASS_SOURCE`. Для каждого attribution scope/view отдельно: E — materialized; U — чужие относительно новой операции disjoint unmaterialized leases того же scope; P — proposed new operation peak; S — disjoint **ещё не materialized** stop obligation. Уже занятый stop входит E; зарезервированный в U/P не прибавляется повторно.

`G = checked(U + P + S)`; `T = checked(E + G)`.

**Total authority:** `T ≤ A`. Проверять per-attempt 128 GiB для W1 и 256 GiB для W2/W3/R/H, assigned owner/per-FS authorities и current resident всей S1 ≤2 TiB. Resident включает logs и immutable failed/final/import/export/repository copies завершённых attempts. У каждой копии attribution owner остаётся после exit. Если копия относится к нескольким attempts, C1 authority задаёт единственное обязательное attribution правило до допуска; неизвестная принадлежность — refusal, не omission.

**Independent incremental physical/quota headroom:** `Gphysical ≤ Hphysical`, где H уже remaining после materialized occupancy и protected/foreign reserves, но до ровно этих U/P/S. E **не добавлять** слева и не вычитать из H снова. Physical/inode predicates самостоятельны; logical bytes нельзя складывать с inodes либо выдавать за native block allocation. Hard quota total domain рассматривается по complete quota-domain usage, не только E attempt.

Если authority сообщает net Hnet после IDs подмножества R⊆U+P+S, canonical normalization `H=checked(Hnet+R)` допустима только при одном epoch, view и доказанном disjointness; materialized/preallocated blocks нельзя add-back. Independent oracle — `G−R≤Hnet`; production применяет только canonical predicate. Неизвестные H/authority/FS/native bounds означают refusal **до writer**. «Максимум доступной RAM» и cgroup memory.max не доказывают storage capacity. Не придумывать headroom=0: unknown хранится как unknown.

Alias одного physical FS учитывается один раз в capacity domain; два реальных materialized файла на нём — два экземпляра. Logical attribution и native physical allocation не обязаны иметь одинаковую сумму. Hardlink/reflink sharing не даёт credit без доказательства идентичности и lifetime; conservative counting допустим, double charge одного lease в одной accounting view — ошибка. Cross-FS операция требует атомарной составной reservation всех domains либо отказа без частичного разрешения writer. Частичную reservation, ещё без записи, можно закрыть release-unmaterialized.

## 5. Snapshot → reservation → monotonic debit → commit/release

1. **Snapshot.** До mutation получить fresh authority snapshot; проверить exact identity, domain coverage, known finite counters, checked arithmetic, existing retained inventory, authority epoch и admitted stop reference. Inventory начинается с E всех живущих файлов; старые failed/final не удаляются и не игнорируются. Никакого storage probing сервера в этом D.
2. **Reserve.** Authority atomic compare-and-reserve проверяет T/A и G/H на одном revision и связывает unique operation ID. Stale revision требует нового bounded preflight, не blind retry/новый grant. До successful reservation не создаётся даже `.pending`/directory/receipt. Reserve включает complete worst-case operation peak и acknowledgement tails, а не только следующий slab.
3. **Monotonic debit.** На каждом growth boundary сначала проверить дочерний descriptor against remaining permit. Дочерние disjoint slots не могут перерасходовать parent. Sequence и materialized/high-water debt никогда не убывают/не сбрасываются при callback retry, exception, pause, point change или restart. Matched actual materialization переводится U→E один раз; ещё не наблюдаемый in-flight bound остаётся U. Capacity sample и transfer должны иметь совместимый epoch; несогласованный sample не освобождает reservation. Resident E может законно уменьшиться лишь после independently attested завершения lifetime; operation consumed/high-water и P2 counters от этого не уменьшаются.
4. **Commit.** Existing writer выполняет прежние sync/verify/receipt/pointer barriers. Только после acknowledged publication authority меняет pending attribution на committed; rename внутри FS переносит объект, а не удваивает его. Close/`filesize` alone не означает durable verified commit. Materialized final остаётся E после закрытия permit/attempt.
5. **Abort/release.** До mutation можно полностью вернуть U. После partial write release разрешён **только** для доказанно не materialized остатка, а partial/failed/temp остаётся E или conservatively retained U до reconciliation. `finally`/timeout/worker death ничего автоматически не обнуляет. Неизвестный результат commit → uncertain lease, freeze зависимые новые grants; не reuse lease ID и не «failed значит 0». R2 не вызывает delete/prune и не финансирует growth будущим удалением. Существующий retain/publication contract не расширяется разрешением чистить данные.

Синхронный cap check перед каждой HDF5 high-level call сам по себе не ограничивает внутренний native allocation между calls. R2 обязан требовать **доказанный native storage growth bound** для операции (payload + finite HDF5/filter/chunk/metadata/allocation overhead при фиксированных versions/layout/event counts) и независимую P1 enforceable ownership/capacity. Нынешний `16 MiB + 4×...` forecast явно heuristic и не удовлетворяет этому требованию. Пока bound/coverage неизвестны, strict serializer **не открывается**. После-file-size guard остаётся reconciliation, не proof отказа до uncontrolled write. Нельзя объявить штатным stop ни ENOSPC, ни OOM, ни исчерпание quota.

## 6. Stop и failure provenance

R2 по первой refusal замораживает новые normal/optional growth и возвращает structured cause с snapshot/lease/inventory/FS identity, phase, expected/observed seq, conservative materialized state и последним **acknowledged verified** commit pointer. Существующий R3 stop path получает только ранее зарезервированный stop capability, не новый normal permit. R2 не гарантирует его успешность без finite RAM/CPU/wall/read/write/log/disk/inode obligations и native evidence R3.

Отказ до первого checkpoint: `no_verified_state`; после checkpoint: ссылка на последний verified generation, без заявления о сохранении незакоммиченного current state. Resource refusal/process exit/scientific acceptance — разные статусы. Crash между rename/receipt/pointer допускает retained unacknowledged generation; reader не повышает её автоматически в verified state. Failed final и original failed logs/receipts сохраняются.

Нельзя писать новый «отказной receipt» бесплатно после denied reserve. Durable refusal допустим лишь в заранее provisioned bounded control/stop region с capability; иначе structured in-memory failure + уже выделенный bounded channel, отсутствие durable receipt явно `unknown/not_recorded`, а не fabricated success. Process death/OOM, external stdout growth, observer loss и NFS partition требуют R3/P1/P2/C1 coverage; R2 local callback не является external log limiter.

## 7. Различающие controls для будущего I

Ни один control ниже не выполнен. Test cap SCI05/08 C08 **8/8 EXHAUSTED**; product runtime90 used, source8; full CI0/science0/heavy build0. Этот дизайн их не возобновляет. I может написать fixtures/source, но выполнение требует отдельного действующего finite grant. Не переносить исторический R1 «349 PASS» на R2/source graph.

Literal oracle отделён от production estimator, inventory builder и arithmetic helper. Fake FS/authority имеет handwritten event log, file identities/byte/inode bounds и mutation call counter; expected constants вводятся literal, не вычисляются тем же forecast/serializer. Все fixtures bounded, отдельного solver/science нет.

| Пара / fixture | Независимый literal oracle и ожидаемое различие |
| --- | --- |
| D2 total/free baseline | E=90 GiB,U=4 GiB,P=8 GiB,S=3 GiB,A=128 GiB,H=40 GiB: G=15,T=105, pass; H=15 GiB exact pass / H=15 GiB−1 byte deny до первой mutation; A=105 GiB exact / A−1 byte deny. E>H не причина отказа. |
| Net baseline | Hnet=11 GiB,R=4 GiB explicit IDs: canonical H=15, pass; Hnet−1 byte deny. Materialized stop falsely used as add-back, overlap IDs или wrong epoch deny. |
| S1/attempt независимость | Shared E=2199023255550 bytes, U=0,P=1,S=1,A=2199023255552: exact pass; P=2 deny. Отдельно attempt E=137438953470,P=1,S=1,A=137438953472 pass/one-byte-short deny; 256 GiB A=274877906944 отдельная literal boundary. Shared pass не заменяет attempt pass и наоборот. |
| Pending/metadata tails | Fake full operation P=100 payload+7 pending metadata+5 receipt+3 new pointer bytes, source E сохранён. Exactly115 additional passes/114 denies до mkpath; старые pointers и source history остаются E. Это invented test bytes, не HDF5 bound. |
| Все branches | Recovery, archive full-final, failed-final, operator/optical, history segment/append/consolidate, same-FS copy/import, cross-FS stage: каждый получает scope parent; нет permit/unknown bound → mutation count0. Final при двух retained recovery не получает bypass. |
| Aliases/copies/lifetimes | Два aliases одного FS не дают два H; source+destination distinct files charged дважды; два FS проверяются независимо. Same-FS rename не повторно debit file; EXDEV no hidden copy. Источник consolidation/export не исчезает из E при создании destination. |
| Reservation race | Два mocked callers получают один revision, вместе не помещаются; authority linearization grants только первому, второй stale/denied; event log доказывает writer2 count0. Это протокол R2, не native C1 proof. |
| Debit/exception boundaries | Failure before first write releases untouched U; after slab, after rename, before receipt, after receipt/before current pointer, after pointer/before fsync: materialized/uncertain retained debt не refund. Old verified current/previous/finals неизменны до соответствующего existing publish barrier. Restart/replay seq не debit twice и не grant again. |
| Inodes/physical | Independent fake physical/inode map: exact count passes / one inode short denies даже при bytes fit; logical fit при physical short denies. Missing mapping/counter/overhead bound отказывает. Compression ratio не подставляется как granted capacity. |
| Checked input | Bool, negative, overflow each intermediate, missing domain, malformed/max/unknown raw statuses, stale boot/namespace/attempt/plan mismatch, unsigned authority и expired snapshot deny before writer. Unknown не становится0. |
| R1+cgroup controls | Existing R1 integer/forecast/boot/free guards и literal oracles неизменны; fake cgroup forest с finite leaf/ancestor exact versus one-byte-short/unknown ancestor проверяет сохранение refusal до storage writer. Memory admission success + unknown FS всё равно deny; ample disk + R1 memory refusal всё равно deny. Никакого new native cgroup run. |

Minimum I acceptance: source call-site dominance table; independent paired fixture sources; no bypass in strict direct APIs; all callbacks receive original identity/lease; original atomic ordering и protected-data diff unchanged; exact owning diff и high review. Выполненные checks и неизрасходованные grants описывать отдельно от предложенных controls.

## 8. Composition points, оставшиеся gates

| Ticket | Что R2 предоставляет | Что остаётся вне R2 |
| --- | --- | --- |
| R3 stop reserve | Disjoint stop reference, refusal freeze, last verified pointer, bounded settlement status | Реальный finite stop resources/early trigger/quiescence/external log/timeout/native failure proof. |
| P1 native capacity/authority | Typed per-domain snapshot baseline, native bound requirement, freshness/boot/namespace binding, fail-closed port | Measured capacity/quotas/reserves/ownership/FS alias/inode/native enforcement; RAM max не storage proof. |
| P2 cumulative I/O/log | Stable operation IDs, monotonic event sequences, материализация и refusal reasons | Reads/writes/hashes/logs across NFS/process tree/retrieval; resident high-water не cumulative writes. Не выдавать quota за I/O cap. |
| A1 consumer duplication | Immutable inventory/permit boundary, source/dest lifetime+FS descriptors | Реальные AiiDA retrieval/repository/Results/export callers и independent read/write budgets; до подключения coverage gap. |
| C1 campaign ledger | Atomic authority protocol, uncertain lease semantics, no reset/refund on exit | Durable authoritative S1 multi-job reservation/reconcile/restart across all13 slots/936 node-hours, no second registry. |

Настоящий strict backend не вправе объявить READY, пока composition dependencies отсутствуют. Отдельно остаются reviewed code, fresh admission, native durability, final CI-once и science gates; design не потребляет и не выдаёт их бюджеты.

## 9. Вывод

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Total resident и incremental headroom должны проверяться отдельно | SCI07 D2 §§2–3; focused high review PASS_SOURCE | Manufactured arithmetic не measured capacity | сохранить |
| Один Runner operation permit может устранить recovery/archive и nested writer accounting обходы | Runner4f60 `commit_point_artifacts` preflight/publication, HDF5 slab API, scientific_execution callers, history/staging loci; §§2–5 | Это design; whole-callgraph/source implementation verification ещё не выполнены | изменить |
| Shared2 TiB и attempt128/256 GiB не доказывают свободный диск | science.md Admission/guards; D1/D2 baseline rules | Native authority/allocated bounds отсутствуют | данных недостаточно |
| Protected failed/final/history/copies остаются resident после exit/exception | D1 inventory; proposed monotonic settlement §§4–6 | P1/C1/A1 должны доказать external coverage/lifetime | сохранить |
| HDF5/free-size sampling не гарантирует pre-growth cap | R1 source помечает forecast heuristic; `_write_slab_array` native dataset/filter creation | Нет native storage upper bound/enforcement evidence | дополнительно измерить |
| R2 source-I ready как finite fail-closed guard, а resource READY ещё закрыт | Exact proposed API/branch mapping/literal controls и отдельные composition gates | Не выполнены implementation/runtime/tests/native/CI/science; независимый high review следующий | изменить |

**STOP: независимый high source review этого immutable D-пакета; реализации, запусков, server probes и новых grants нет.**
