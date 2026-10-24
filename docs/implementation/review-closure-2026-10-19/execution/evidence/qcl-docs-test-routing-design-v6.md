# Docs routing D6 — узкое lifecycle дополнение к D5

2026-10-20, source-only; STOP для focused high recheck. D4 `24a7d68b612e7d3dc437404bb805df777ede1f5159c0bff39eca7d693ebe8fc0`; highD4 `ca5a8d36b04ff6e5f52817da420b6fb3ca92e95d9e70e45c1ea6f44f74b9fb48`; D5 `6049f427a10c769b69c2beaaa1374e583d217d6eb68926337204e560b824ed48`; highD5 `bb0319a40211616d36316c0adf04b8b0ac1f9bdefb8c71d274a96aecb3fd5d7d`; highI2 `5b7ec1e5f1fefad767315f539fe637c12c322902c78d542acea16639931ced60`. D5, его ledger/identity и все предыдущие artifacts неизменны. Это дополнение исправляет только D5-R1: достижимый порядок finish/driver exit/phase closure/setup closure.

Selected HEAD повторно `2bb05d3651af4509fe7f02c1253b40f1e5146fec`, status5tracked+6untracked, прежние8uninitialized gitlinks; coordinator HEAD отдельно `c5ef91f4d11a93bd2cdcc9d0b6b18bba0df80ed0`. Read-only Git observations, exact входные hashes и logical read ledger — в identity. No source/fixture/CP/git writes; target execution0.

## 1. Три точных scope closure, один прежний workload cgroup

D4:132–134 сохраняется: setup/broker, driver, command supervisors и их descendants учтены в **одной** admitted workload cgroup; existing trusted outer parent с control reserve находится снаружи. Новых cgroups/trust roots/authorization нет. Имена owner sets ниже — учёт pinned identities, не дополнительные ресурсные boundaries.

| Closure | Кто подтверждает и что закрывается | Что ещё может быть живо | Допустимый claim |
| --- | --- | --- | --- |
| Command | Native command owner: оба raw streams EOF, exact command descendants закрыты/reaped, supervisor terminal ACK/reap | Setup, driver и control/task participants | `command_descendants_closed`; никогда whole-empty |
| Phase | Producer: все phase commands закрыты; exact pinned driver и его descendants закрыты, stdout/stderr EOF, driver reaped | Setup/broker; клиент и pinned task/job leaders, ожидающие outcome либо продолжающие workflow | `phase_driver_subtree_closed`; `whole_workload_empty:'not_claimed'` |
| Setup | Outer trusted parent: producer и **все** owned workload participants/descendants закрыты/reaped, raw drained, final cgroup.events/events проверены | Только outer parent вне workload | Actual `populated=0`/whole-workload cleanup evidence |

Setup, broker client и task/job control ancestors заранее входят в pinned setup-participant set; они не переименовываются в command/driver descendants ради удобства. Client, ожидающий final phase receipt, не входит в закрываемый driver subtree. Их live CPU/RAM/pids и events учитываются общим guard до setup closure. Появление неизвестного identity/ancestry не разрешает исключить его из closure: failure/unknown, no pass, no next phase. Exact no-foreign-signal policy D4/D5 сохраняется.

`external_guard.close_and_verify_empty(workload_lease)` вызывается только outer parent на setup closure. Command/phase owners используют ownership/birth/pidfd descendant closure + EOF/reap; они продолжают проверять общие limits/events, но не требуют `populated=0` при живом setup. Это явная замена противоречивого D5 §3.8/§6/строки R2 и D4 слов `terminal-empty` там, где речь идёт о **command** lifecycle. Сам whole-empty predicate не ослабляется.

Initial-empty также проверяет outer parent **до первого gated bootstrap attach/exec**. Связанный allocation path/identity, monotonic sample, counters и expected producer birth передаются active factory из того же trusted parent handoff. Уже исполняющийся setup проверяет provenance этого observation, membership/limits/authority и дальнейшие events; он не требует, чтобы содержащая его cgroup была сейчас пуста.

## 2. Exact finish-validation ACK до closure

Все D5 capsule/hello-first, четыре env names, full pure Capture, chunk codec/caps, canonical digests и compact aggregate projection сохраняются. D5 driver request `finish {aggregate_summary,aggregate_sha256}` с прежним common envelope/sequence остаётся последним request. Только response `finished {terminal_ref,...}` **заменяется** следующим exact reply (common fields обязательны):

```text
{version:1,request_id,sequence,kind:'finish-validated',
 validation:'accepted'|'rejected',validation_ref,
 aggregate_sha256:<SHA|null>,summary_sha256:<SHA|null>,
 terminal:false,phase_closure:'pending',setup_closure:'pending'}
```

Encoded reply≤16384B включая LF. `accepted` означает лишь successful validation полного digest/report/capture/plan/source bindings по D5, не phase/setup acceptance. `rejected` может иметь validated digests только где они фактически установлены; отсутствующее —null. Если receipt нельзя durably создать, reply не выдумывает ref: typed refusal/null retention по D5 и failure finalization. Driver после matching reply закрывает protocol outputs и выходит (accepted→exit0, rejected→exit1), не ждёт final phase/setup ref и не делает новых requests. Extra frame после finish/ACK — protocol failure. ACK read/write/driver exit ограничены остатком прежнего deadline; read loop остаётся multiplexed с cancel/EOF/guard.

`validation_ref` указывает на actual exclusive immutable retained receipt≤16384B с exact keys:

```text
{format:'root-docs-finish-validation.v1',binding:<D5 PhaseBindingV1>,
 request_id,finish_sequence,validation:'accepted'|'rejected',
 aggregate_sha256:<SHA|null>,summary_ref:<Ref|null>,summary_sha256:<SHA|null>,
 evidence_index_ref:<Ref|null>,validated_at_utc,
 terminal:false,phase_closure:'pending',setup_closure:'pending'}
```

Ref=`{path,sha256}`; SHA/UTC/strict JSON/canonical rules D5. Summary ref содержит прежний compact wire projection≤131072B; evidence index — уже native-owned bounded manifest actual capture/command/raw refs, без дублирования сотен записей в ACK. Reader использует exact owned expected ref и actual SHA/stat, не arbitrary caller path. Отдельные evidence records сохраняются даже при отсутствующем index. PhaseBinding содержит только nonce/token **hashes**; никаких raw tokens/nonce/capsule/env в этих receipts/logs. Ни название `validation`, ни ref не дают cleanup/pass.

## 3. Exact final phase receipt после driver closure

После finish-validation reply producer остаётся жив, bounded-drains driver, closes/reaps driver descendants, проверяет оба EOF и exit/birth/ownership. У каждой command к этому моменту уже есть command closure. После **этого**, при success или failure, producer создаёт actual exclusive phase receipt≤32768B:

```text
{format:'root-docs-phase-receipt.v2',binding:<D5 PhaseBindingV1>,request_id,
 finish_validation_ref:<Ref|null>,aggregate_sha256:<SHA|null>,
 summary_ref:<Ref|null>,evidence_index_ref:<Ref|null>,
 driver:<DriverTerminal|null>,command_closure:'closed'|'unknown',
 phase_driver_closure:'closed'|'unknown',
 result:'passed'|'ready_for_unit_attempt'|'failed'|'blocked',
 source_observation:'measured'|'not_measured',
 retention_status:'complete'|'partial'|'unknown',
 setup_state:'active'|'closing',whole_workload_empty:'not_claimed',closed_at_utc}
```

`DriverTerminal` exact `{identity:{pid,birth,uid},exit_code,signal,stdout_eof,stderr_eof,reaped,closure_ref}`; identities — finite safe integers (pid>0, birth/uid≥0), exit_code integer|null, signal bounded fixed OS signal name|null, EOF/reaped booleans, closure_ref actual native-owned Ref|null. Если driver ещё не запускался, DriverTerminal=null, reason отражён в bounded evidence; это blocked/failed, не proof closure работающего driver. Missing receipt/index/EOF/ownership/retention не заменяется нулём. Failure receipt допустим при closure unknown; **positive result** требует accepted validation, correct exit0, всех command/driver closures/EOF/reap, current source/guard/report predicates D5. Preflight positive result только `ready_for_unit_attempt`; он не passed units. Phase result никогда не claim whole-empty.

После durable phase receipt producer отправляет клиенту exact bounded terminal:

```text
{kind:'phase-complete',request_id,binding_digest,phase_ref,result,
 setup_state:'active'|'closing',setup_final_ref:null}
```

Frame≤8192B, result совпадает с phase receipt. Client сверяет binding/request/actual ref/hash, выдаёт redacted summary и завершает свой task. Его exit0 означает только допустимый **phase** outcome; final setup proof ещё нет. Parent также получает bounded `phase-ready {kind,setup_id,phase,attempt,binding_digest,phase_ref}`≤4096B и сверяет actual receipt по SHA. Next phase допустима только после positive final phase receipt и сохранения всех первоначальных grant/expiry/admission predicates. No next phase после любого failure/unknown/cancel/transport delivery failure; reserved/consumed tokens не возвращаются, неиспользованные tokens invalidated при setup closing.

## 4. Producer shutdown, parent ACK и final setup proof

После последней из≤2 разрешённых фаз **или первого failure/cancel/deadline** producer закрывает broker для новых admissions, сохраняет available phase/partial evidence и sends exact control frame≤4096B:

```text
{kind:'setup-closing',setup_id,phase_set_digest,
 phase_receipts:[{phase,attempt,binding_digest,ref}],
 unstarted_phases:[{phase,attempt,binding_digest,reason}],
 close_reason:'completed'|'phase_failed'|'cancelled'|'parent_lost'|'deadline'|'protocol_failure'}
```

Каждый список≤2 в первоначальном ordered phase order, без дублей. `reason` fixed safe code≤64ASCII; `phase_set_digest=SHA256(canonical({phase_receipts,unstarted_phases,close_reason}))`. Parent проверяет это против own PhaseLedger, consumed phases и retained actual receipt bytes, не against self-claimed booleans.

D5 неоднозначный `completion-ack {terminal_ref}` **заменяется** exact parent→producer frame≤1024B:

```text
{kind:'completion-ack',setup_id,phase_set_digest,disposition:'exit'}
```

Это разрешение завершить уже admitted producer lifecycle после фиксации фаз, **не** final setup acceptance и не ref будущего final receipt. Producer после matching ACK закрывает socket/свои streams и выходит; не ждёт whole-empty, не создаёт final setup receipt. Обычно exit0 только при close_reason=completed и positive required phases, иначе exit1. Parent не обязан ждать выхода job leader перед ACK: producer может выйти, пока tracked client/task/job participants заканчивают уже разрешённую работу; всё ещё учитывается в общей allocation.

EOF на parent channel **до** matching completion-ack означает cancellation/failure. Если ACK не может быть доставлен/прочитан, bounded cancellation/fallback, no success. После matching ACK штатный producer EOF/exit — ожидаемый переход `EXIT_AUTHORIZED→REAPED`, но сам по себе не success. Unexpected producer loss до ACK, wrong ACK/digest/extra frame либо поздний cancel/deadline переводит parent в failed cleanup; normal EOF нельзя использовать для обхода closure. При parent loss/deadline producer не ждёт ACK бесконечно: выполняет свой bounded cleanup/retention и выходит с failure; independent outer watchdog/fallback сохраняет известное, если доступен. Literal `C\n` остаётся cancellation во всех ещё active states.

Outer parent завершает/доводит до closure **всех** remaining owned workload identities, включая producer, clients, task/job leaders, supervisors и descendants; дренирует originals, reap-ит доступных children, проверяет отсутствие живых owned identities и actual whole-workload `cgroup.events populated=0`, final memory/events. Только после этих observations создаёт exclusive final setup receipt≤32768B:

```text
{format:'root-docs-setup-receipt.v1',version:1,producer:'root-docs-setup-v1',
 setup_id,authorization_ref,request_digest,scope,source_head,native_source_digest,
 runtime_inventory_digest,phase_set_digest,phase_receipts,unstarted_phases,close_reason,
 producer_terminal:<DriverTerminal|null>,participants_closed:boolean,
 workload:{allocation_ref,initial_empty_ref,terminal_ref:<Ref|null>,
           populated:0|1|null,events_ref:<Ref|null>,closure:'closed'|'unknown'},
 result:'complete'|'failed'|'blocked',retention_status:'complete'|'partial'|'unknown',
 closed_at_utc}
```

`producer_terminal` использует exact terminal identity/stream/reap fields из §3, но относится только producer; это не alias driver. `phase_receipts/unstarted_phases` те же bounded ordered lists. Positive `complete` требует required phase outcomes, producer normal completion, participants_closed=true, actual populated=0/closure=closed, guard/events/retention complete и native D5 predicates. Неизмеренная whole-empty ⇒ populated:null/closure:unknown и result failed/blocked. Whole-empty после failed phase может быть измерено и retained, но setup result остаётся failed. One-phase prerequisites-only setup при complete всё ещё доказывает только prerequisites, не units.

`RunningDocsSetup.await_terminal()` возвращает **этот final setup ref**, опубликованный outer parent после reap, а не driver validation/phase ref. Producer не должен ACK-ать receipt, созданный после собственного выхода. Outer API/Root получает ref directly от существующего trusted parent; никакого нового внешнего RPC/registry. Parent fallback после producer loss публикует тот же schema с available phase/raw refs, typed unknowns; при dual-store failure retention unknown, no forged durable ref/pass.

## 5. Root workflow и consumer claim gates

- Workflow preflight client может вернуть exit0 после positive **final preflight phase receipt**: это разрешает только следующий уже порученный prepare step, при прежнем active grant; setup остаётся живым/admitted. Capsule для check отдельная и одноразовая. Истёкшие admission/allocation/deadline требуют block, не silent renewal.
- Full `ops/ci→check` client возвращает phase outcome после final check phase receipt, driver уже закрыт. Это позволяет Deno/task/job закончить свою работу и устраняет цикл. Client сам не печатает overall setup/CI pass.
- Existing external runner job-launch wrapper/Root parent владеет overall завершением: после required phase receipts, завершения owned task/job участников, producer exit/reap и whole-empty публикует final setup receipt. Для claim docs contribution к full workflow нужны final check `passed`, preceding preflight `ready_for_unit_attempt` если он был required, underlying full task/job exit0 **и** final setup `complete` с correct source/scope/attempt. Job wrapper не выдаёт final success по одному client exit/phase ref. Остальные CI checks и scientific gates этим не подменяются.
- Direct check/docs тем же outer parent ждут final setup proof после task return. Bare CLI без live trusted parent по-прежнему blocked. Если installation не умеет удерживать wrapper до final setup proof, native integration blocked; не приписывать Deno task способность закрыть собственный cgroup.

## 6. Дебиты, reserves, failures и конечные controls

Одна первоначальная monotonic deadline/active allocation на весь setup и≤2phases; новая стадия не добавляет seconds/CPU/RAM/storage/grant или attempts. Command/driver/producer shutdown и outer whole-empty observation заранее резервируются **внутри** этого deadline до первого child. All partial/failed writes и cleanup debits учитываются один раз общим owner ledger; phases не обнуляют global storage/control allocation. Per-phase D5≤24MiB wire, Git512/8MiB/60s, unit caps, total pids≤256 и D4 control reserve≤128MiB/log256KiB/metadata2MiB сохраняются. Finish request/response остаётся в прежнем wire slot; новый ACK меньше прежнего cap. Ни whole-empty, ни lifecycle не запускают fresh Git/tool probes.

Finite upper reservation для lifecycle metadata: на фазу projection≤131072 + validation≤16384 + final phase≤32768 + closure evidence≤16384 =196608B;≤2phases393216B; final setup≤32768 и whole-empty evidence≤16384 ⇒ суммарно≤442368B. Независимый fallback при необходимости второго durable store резервирует ещё≤442368B, а не пишет бесплатно. Новые parent/client lifecycle wire/history имеют отдельный reserve≤32768B в existing caps; typed failure/refusal prefixes входят в reserve. Existing evidence index/command receipts/raw/startup/capsules остаются в своих уже определённых ledger domains; эти bound numbers не заменяют actual complete schedule. Если сумма existing+новых+failure/fallback reserves не помещается в actual grant/metadata2MiB/control-history256KiB или monotonic reserve, refuse **до** первого child; caps не увеличивать. Secret startup/ACK не сохраняются как raw history; actual transport bytes учитываются существующим active transport ledger.

Driver linger/descendant escape/partial drain/phase delivery failure: no positive phase, no second phase, producer closing, outer parent escalation TERM→KILL только known-owned identities в remaining budget. Producer loss/whole-empty failure: fail setup, retain completed captures/phase receipts, no CI/full success. Unknown/foreign identity не signal; cleanup unknown сохраняет allocation/admission blocked по owning policy, не помечает её освобождённой. Конец бюджета не продлевает cleanup и не превращает populated/unknown в empty. Одновременная потеря stores не обещает durable evidence. No retry/relaunch/renewal из D6.

Будущий I2B готовит, но не исполняет paired manufactured controls: preflight→check на одном producer; driver waits validation ACK→exits→phase receipt; setup остаётся live/accounted без whole-empty claim; final producer exit→outer whole-empty; driver/producer loss до/после ACK; partial ACK/extra sequence/deadline; lingering command/driver/setup participant; failed first phase запрещает second; snapshot initial-empty только pre-bootstrap; success consumer отказывает validation/phase ref вместо final setup ref. Каждый refusal сохраняет prior raw/partial identity и zero forbidden dispatch. Все9I2 source findings остаются implementation gaps, fixtures nominal counts не pass.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Driver может выйти до final phase ref | §2 validation ACK/ref с terminal:false | Implementation/CPP/DEV ещё нет | изменить |
| Phase closure совместима с живым setup | §1/3 exact owner scope, no whole-empty claim | Kernel ownership evidence позже | изменить |
| Whole-workload empty имеет достижимого автора | §4 outer parent после producer+participants reap | Actual trusted wrapper/allocation не установлены | изменить |
| Capsule/chunk/full pure Capture/secrets contract меняется | D5 preserved; §2/4 только hashes | Lifecycle private union изменён явно | сохранить |
| D6 доказывает READY или закрытие9I2 defects | Source/fixture/execution0 | Только narrow design; high recheck впереди | данных недостаточно |

STOP high recheck. Никаких product/fixture/CP/parser/compiler/formatter/lint/target-import/test/runtime/native/network/server/build/solver/CI действий; только три новых D6 documents.
