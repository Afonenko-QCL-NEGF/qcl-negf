# I2E — boundary1 corrections + boundary2 candidate, PARTIAL

Selected worktree `/tmp/qcl-docs-test-routing-worktree`, HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`. Governing high I2D review
`8a666cf1d9771aab53ce9fecc156faae2b139ce60cc4a9875ec9056f6f1f1916`.
**Source candidate, CHANGES REQUIRED / не READY.** Один конечный source-only
проход. Ни boundary3 schedule/ledger, ни full C8 не объявляются завершёнными.
Некоторые total-cleanup/provider/error paths ещё требуют коррекции/CPP ниже.

Complete patch — полный four-file I2D→I2E delta,98658B, SHA256
`1ce20122993d7868189332ff3f4dd8252937c1f8f62c5fc860dc7a0a8c46ac4a`.
Predecessor bytes сохранены отдельно в `/tmp/qcl-routing-i2e-baseline`; exact
before/after SHA — identity. Original I2D report/identity/delta сохранили
`acafce…` /`051f07…` /`0ed917…`; старые cumulative packets не заменены.

Ровно4native paths; native16 import path list и stdlib imports не увеличены.
Pure Root FORMAT/comments не трогались: actual68f0ef… /2639be… — внешняя
Root dependency, отсутствует в delta. Root/CP/index/gitlinks не менялись.

## Поддефект → actual guard → paired fixture → remaining gate

Все source conclusions ниже — candidate до fresh high CPP; execution0.

| Поддефект | Actual owning guard/call | Paired fixture | Remaining gate |
| --- | --- | --- | --- |
| Array/object enum coercion TS | `isEnum` требует typeof string до includes; responseFor/operation/start/finish больше не используют String coercion для enum membership. | Existing Deno refusal case: arrays/objects/numbers/null в code/cleanup_status отвергаются; request/stream/validation enums используют тот же guard. | Fresh CPP; finite Deno DEV отдельно. |
| Open nested parent registrations | `validate_registration:236`: exact top/map/row shapes, bounded unique6-tuples, tools/runtime manifests/captures, actual typed initial populated/monotonic/birth/events, allocation/caps/reserve/env. Вызывается до producer construction и до bootstrap spawn. | Existing malformed grant/scalar cases + positive in-memory artifact cases; full forged nested registration matrix ещё не завершена. | C3 remaining coverage; no fake grant/registry. |
| Wrong phase order/scope | validate_request теперь проверяет container types и one target либо preflight→target по scope до authorize/spawn. | Existing request negative cap/forbidden authorization case; ordered-phases dedicated matrix ещё нужна. | Fresh CPP; boundary3 ordinal slots отдельно. |
| Partial phase readers parent/client | `read_phase_receipt:2184` exact D6 phase union, full binding/scalars/ref/enums, actual driver closure and accepted validation cross-refs; используется parent dispatcher/closing и native client. `validate_setup_record:2212` закрывает final setup shape/partition/workload/scalars и positive conjunction до final publication. | Actual phase receipt/artifact store case: valid refs проходит; positive+unknown/partial retention отвергается. Queue fixture отдельно mock-ит validated reader, не выдаётся за full phase proof. | Full parent/client malformed union matrix и external lease integration ещё нужны. |
| Shortcut finish-first fixture | Fake Driver теперь выдаёт legal preflight(sequence1) → finish(sequence2), проверяет actual allowed_ops; Native run_phase вызывается. | Existing propagation cases source-final throw/missing index/healthy path. Underlying source/report provider injected, но **validate_phase_retention/validate_terminal не mocked**. | Это isolated producer finalization, не full C8/broker/kernel route. |
| Retention guard подменялся готовым status | In-memory artifact reader проверяет actual bytes/hash/caps; actual native pending/command/index/raw/terminal/proof validators исполняются при будущем DEV. Proof entries в fixture создаёт **actual native publisher** на fake low-level handles. | Healthy complete; missing index; pending binding mismatch; raw SHA/size; false reap; empty proof set. Точные complete/partial/unknown assertions. | Пока source-only, observed=null. |
| No durable no-replace publisher | `publish_bytes:1008`: exclusive random pending, full write/actual size, file fsync, atomic link refusing existing final, directory fsync, pending unlink, second directory fsync, close; proof tuple только после всех операций. Ref вычисляется снаружи bytes после publication, собственного SHA в body нет. | Fake handles: partial write, file sync, link collision, directory sync failure сохраняют bytes и empty proof set; healthy operation order + second publication refuses overwrite/original remains. | Real filesystem/crash semantics, close/unlink/second-sync faults отдельно. |
| Raw bytes не имели actual owning publication | Worker пишет только `.partial`; parent после reap и complete producer/drain proof вызывает `publish_closed_raw:1045`, создаёт final original/ref/proof. Unknown closure не публикуется как complete. Command pending/receipt/index/phase теперь используют actual publisher с тем же owner proof set. | Actual artifact/proof pairs; publisher fault seams. | Full worker/fork/write/error matrix ещё неполна. |
| Driver raw отсутствовал в manifest | Driver stdout protocol и stderr — separate bounded originals; stdout≤24MiB wire envelope, stderr≤256KiB. После EOF/reap publish_closed_raw, closure содержит exact streams + raw_complete; retention перечитывает эти refs и требует durability. Failure raw_complete=false запрещает complete. | Artifact closure/raw/proof pairs + publisher lower seam. | New protocol-original storage reservation должен войти в полный boundary3 trace; cap не повышен. |
| First FD outside owner | execute_bounded allocates socketpair/pipe/fork inside guarded lifecycle; launch_state distinguishes fork/gate/reap. Active.command records ledger before reserves, guarded reservation/pending writes, known unopened gate permits unused capacity release. DriverPipe constructor installs defaults before first allocation and calls idempotent close on failure. | socketpair/pipe/fork failures: gate false, no forbidden fork before ready allocation, all created handles closed, failure cleanup unknown. | All descriptor/stat/commit/error-preservation permutations ещё не покрыты. |
| Inherited FD≥4096 survived exec | `close_inherited_fds:1119` enumerates actual /proc/self/fd with finite bound; closes complete observed set except0/1/2. Producer inherited control FD explicitly noninheritable before later forks. | Fake census contains65537; actual helper closes it and preserves stdio. | Real isolated startup/native fd validation later. |
| Drain error skipped TERM/KILL/reap | DriverPipe.close now stores first failure, independently attempts drain/reap/owned TERM→KILL, then independent handle close/reservation settle/owner close/failure artifact. Unknown ownership/EOF cannot produce terminal proof. Worker owner init moved inside try; handle closes attempted independently. | First-allocation controls + EOF/reap/retention pairs; complete fake pidfd/signal/drain matrix still absent. | Boundary2 remains candidate, not total closure proof. |
| Later delivery failure lost positive phase history | Parent closing accepts verified actual phase receipt even if phase-ready delivery was lost, correlates parent-launched phase; stores immutable record. close_reason failure still prohibits setup complete/next phase; old positive receipt is not rewritten. | Existing phase/ref consistency cases; exact delivery-loss control ещё нужен. | D6 paired transport/syscall execution later. |

## Publication proof ownership и self-publication

В production proof tuples добавляют только `publish_bytes` и
`publish_closed_raw` после actual file/directory operations. Нет caller JSON
registration, filename/readback-only unblock или ручного заполнения set.
Active owner передаёт тот же set StorageLedger; parent использует свой existing
trusted lease/storage publication owner. Native retained records, command
raws, driver stdout/stderr, phase, final setup и fallback подключены к publisher.

Phase/setup body не содержит собственного будущего SHA. Actual ref возникает
после successful no-replace durable publish; только затем producer может
выдать phase ref или outer parent вернуть setup ref. Ошибка публикации не
выдаёт complete ref и сохраняет pending/known original bytes where possible.
Directory-sync failure после link может оставить final name на диске: это
не claimed durable ref/proof и не повод overwrite/cleanup-delete evidence.

**Producer bootstrap streams остаются обязанностью existing trusted outer
lease.** Native parent проверяет exact terminal closure (streams/raw_complete),
raw bytes/hash, required producer publication tuples в outer owner's set;
их отсутствие даёт failed/unknown, а не complete. Поставщик этого opaque
lease/kernel bootstrap не развёртывался и не исполнялся. Для valid integration
он должен использовать actual owning publisher, а не передать labels или
вручную добавить tuples. Source guard не создаёт operator authority.

## Честный remaining failure list

1. Boundary2 **не закрыт полностью**: Active.command settlement/stat/commit и
   worker cleanup/raw-read/write-frame могут ещё породить secondary exception;
   полный error-preserving retained primary-failure trace требует CPP/control.
   Parent bootstrap provider обязан самостоятельно закрывать partially spawned
   gated stub при throw внутри opaque spawn_gated. Repo adapter закрывает свои
   channels, но не выдумывает чужой pidfd/ownership.
2. Некоторые fallback errors могут не сохранить final ref при исчерпании
   stores/budget; это unknown/no pass. Signal/owner scan error не разрешает
   foreign signalling или досрочное убийство единственного subreaper.
3. Native publisher file/dir durability и no-replace operations подготовлены,
   но все filesystem race/close/unlink/fsync permutations и actual crash tests
   не выполнены. No physical guarantees claimed from source/mock agreement.
4. Boundary3 не выполнялся: failed Git cost finally, exact ordinal graph slots,
   config identity race binding и полный replayable write/transport/fallback
   trace ещё открыты. Driver protocol raw теперь имеет reservation до driver
   fork; при недостаточном existing storage grant он блокируется. Actual24MiB
   wire cap не расширен; новая raw retention cost не спрятана за100/444 claim.
5. Conservative source measured по-прежнему связано с fully validated finish;
   failed report может дать not_measured при прочитанном source (I2DR R3).
   Независимый measurement criterion относится к boundary3.
6. Полная malformed nested reader matrix и manufactured existing lease→kernel
   →broker→driver→executor→setup route отсутствуют. Source fixture8+8 — nominal;
   это не full C8/DEV READY. Синтаксис/типы/format не проверялись.

## Identity и finite source ledger

Working hashes четырёх файлов — identity; actual native Python167817B на
предварительном source read, последняя точная SHA задаёт overlay, не committed
HEAD blob. Это не actual native source/family freeze и не новые Git probes.
Git использовался только для repository identity HEAD/status/gitlinks; native
broker Git/version/process calls=0. Read cap8MiB: conservative content upper
bound4MiB, включая predecessor copies, selected source/diff/hash reads и high
review. CPU/RSS/physical I/O не измерены; cap25min/1CPU/2GiB, один pass.

Parser/compiler/import/scripts/tests/Deno/Julia/runtime/native/network/server/
CI/science=0. Product attempts не расходованы. Старые artifacts/Root comments
сохранены; no commits/index/CP writes. Основные paired fixtures добавлялись
перед соответствующим publisher/reader change; supplemental failure controls
добавлены при source inspection, не выдаются за runtime RED/GREEN.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Coercing enums / mock-retention shortcut устранены | typed helper + actual artifact/publisher controls source | fresh CPP/finite DEV впереди | изменить |
| Publication proof производится owning operations | no-replace file+dir publisher и подключённые guards | filesystem/provider/full error matrix не выполнены | изменить |
| Boundary2 total cleanup завершён | remaining list1–3 | partial candidate | данных недостаточно |
| Boundary3/full C8 или native READY получены | не выполнялись | отдельные finite boundaries | данных недостаточно |
| Runtime/CI/science подтверждены | execution0 | source-only | данных недостаточно |

STOP fresh high CPP. Никаких product calls этим grant.
