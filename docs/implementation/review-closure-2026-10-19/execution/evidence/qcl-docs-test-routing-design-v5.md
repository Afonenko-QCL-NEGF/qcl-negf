# Docs routing D5 — конечный private contract перед I2B

2026-10-20. Этап: source-only уточнение недостающего контракта; затем STOP для high R. Governing D4 SHA256 `24a7d68b612e7d3dc437404bb805df777ede1f5159c0bff39eca7d693ebe8fc0`, focused high D4 review `ca5a8d36b04ff6e5f52817da420b6fb3ca92e95d9e70e45c1ea6f44f74b9fb48`, I2 CPP `5b7ec1e5f1fefad767315f539fe637c12c322902c78d542acea16639931ced60`. D3 SHA `c586234a65a647c3896eb17af4ac0ae0b8a02f4f56d41dcbf25728d997282554` сохраняется там, где D4/D5 явно не уточняют private transport.

Selected source `/tmp/qcl-docs-test-routing-worktree`: фактический HEAD `2bb05d3651af4509fe7f02c1253b40f1e5146fec`, пять tracked edits и шесть untracked source files; все восемь gitlinks uninitialized и неизменны. Все 18 production/DEV hashes I2 CPP совпали с actual bytes при freeze. Coordinator checkout `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf` имеет другой фактический HEAD `b07974b8e46bf8afdf1740947b842669a62a5ccc`; он не подменяет selected I2 overlay. Полные read-only Git observations и hashes — в companion identity. Это не новая ревизия lock и не committed/native acceptance.

Решение: **сохранить D4 hello-first**; server-first challenge I2 не принят и удаляется. Сделать два явных private уточнения: bounded capsule в значении существующего `QCL_DOCS_PHASE_TOKEN`; bounded chunk hydration для Git/Capture и компактный finish projection. Это разрешает I2B реализовать конечный здоровый route, сохранив public descriptor, pure Capture и четыре env names. Root подтвердил допустимость chunk hydration при chunk≤32KiB, aggregate cap, независимых originals и finish/log/receipt≤128KiB. Ни D5, ни capsule не являются execution grant.

## 1. Сохранённые границы и owning source

Не меняются exact12 descriptor sources/три tool entries/public schema, девять pure exports, D2 dedicated argv/clearEnv/env/permissions, полный pure `Capture.stdout/stderr`, порядок full workflow, native16 closure, owning sourceGraph semantics, восемь Git gitlinks, fixed13-node DOC06 seed и counts56/15/20, failure retention и non-downgrade. Historic fixture227/SHA04589… и current230/SHAf02f… различаются; source mapping +3 не превращается в observed pass. Sole pure GREEN, compiler-only checks, две DEV calls, native evidence, final CI и scientific acceptance остаются отдельными gates.

I2B owning files: `ops/docs_tests_native.py`, `ops/docs_tests_cli.ts`, узкий injected-reader seam `ops/git.ts`, два native DEV fixtures. `deno.json`, `ops/ci.ts`, два workflows — только если для D4/D5 routing нужна коррекция. Не расширять public inputs, pure helper/230 fixture, native16 imports, platform/component gitlinks, CP, historical evidence или научную модель. Python stdlib `base64` явно добавляется только для private capsule/chunk codec; finite import inventory обязан включить также фактически используемый `re`. Динамических/third-party imports нет; stdlib остаётся внутри admitted runtime closure. Это уточнение перечня imports, не новый trust root.

## 2. Точный phase binding через прежние четыре env names

### PhaseBindingV1

`PhaseBindingV1` — exact keys:

```text
{version:1, producer:'root-docs-setup-v1', setup_id, phase, attempt,
 input_sha256, source_head, source_graph_digest, native_source_digest,
 runtime_inventory_digest, scope, not_after_utc, setup_nonce_digest,
 token_sha256}
```

`setup_id` —32 lowercase hex; token —32 random bytes в64 lowercase hex; SHA —64 lowercase hex; source_head —40 lowercase hex; phase=`preflight|check|docs`; attempt — unique parent literal `[A-Za-z0-9][A-Za-z0-9_-]{0,127}`. Scope точен: preflight=`prerequisites-only`, check=`full-root-check`, docs=`docs-units-only`; наружный setup scope обязан разрешать этот scope и порядок фаз. UTC в private transport/receipts имеет ровно `YYYY-MM-DDTHH:MM:SS.ffffffZ`, finite calendar value, без alternate timezone spelling; native conversion проверяет календарь, не один regex. Нельзя принимать future measured timestamp или истёкший phase/allocation. Host admission отдельно сохраняет owning60s expiry; tool expiry/capsule его не продлевают.

Canonical bytes для private binding/digest: UTF8 JSON, sorted ASCII keys рекурсивно, compact separators, no BOM/NUL/duplicate keys/NaN/Infinity, строки без нормализации. Здесь все значения ASCII; version —integer1. `binding_digest=SHA256(canonical(PhaseBindingV1))`. `setup_nonce_digest` и `token_sha256` — SHA256 от исходных32 random bytes, не от hex spelling. `native_source_digest` связывает fixed16 ordered tuples `(path,Root HEAD blob id,working SHA256)`; `runtime_inventory_digest` — canonical exact parent-admitted Python/runtime+four tool/Git inventory refs. Оба сверяются с соответствующим полным trusted startup attachment, не принимаются как самостоятельное доказательство.

### Capsule codec — явное уточнение только значения QCL_DOCS_PHASE_TOKEN

```text
QCL_DOCS_PYTHON    = ABS_ADMITTED_PYTHON
QCL_DOCS_BROKER    = ABS_PRIVATE_SOCKET
QCL_DOCS_SETUP_ID  = setup_id
QCL_DOCS_PHASE_TOKEN = 'qcl-docs-phase-v1.' + BASE64URL_NO_PADDING(canonical({
  token:<64lowerhex>, binding:<PhaseBindingV1>, binding_digest:<64lowerhex>
}))
```

Exact capsule keys только `token,binding,binding_digest`; prefix literal; encoded env value≤4096B ASCII; decoded JSON≤2048B; nesting≤3, member counts фиксированы. Decoder сначала проверяет byte cap/prefix/`[A-Za-z0-9_-]+`/допустимую длину, затем bounded decode; decoded bytes должны повторно кодироваться в **тот же** unpadded base64url и canonical JSON. Reject padding/whitespace/alternate encodings/duplicate or extra nested keys/неfinite numbers. `base64.urlsafe_b64decode` вызывается лишь после этих bound checks; никакого eval/import/path lookup. Capsule создаёт только live `RootDocsSetupV1`; parent получает её через inherited private control channel и держит exact binding в памяти. Client не читает attempt/source из caller JSON и не угадывает их из setup_id. Descriptor даёт actual payload/hash, который **сравнивается** с capsule и live record; он не задаёт phase authorization.

Это явная замена I2 plain-token **env encoding**; raw random256 token внутри сохраняет D4 semantics. Wire hello не меняется. Capsule не подписана и не объявляется authority: любой прочитанный набор полей остаётся inert до независимого server lookup raw token→live record, peer/subtree, source/input/admission/expiry checks. Same-uid hostile ptrace/env theft всё ещё исключены D4 trusted-local-harness premise. Создание caller capsule или копия filename/receipt не создают phase record.

### Hello-first и полный accepted binding

Client читает ровно четыре names, сохраняет их в bounded local structure и очищает собственное environment. Выполняет stable nofollow bounded descriptor read≤32768B, проверяет actual input hash/source_revision и phase argv против capsule; interpreter/source self-check — дополнительный drift guard, не runtime authority. Затем соединяется и **первым** посылает D4 exact hello:

```text
{version:1,setup_id,phase,attempt,input_sha256,source_head,token,
 client_pid,client_startticks}
```

Здесь attempt/source берутся из setup capsule, input_sha — от actual bytes. До hello server ничего не посылает; нет challenge/probe/fetch-binding API. Broker сверяет `SO_PEERCRED`, UID, exact `/proc` birth/ancestry и pinned phase leader pidfd из parent control, lookup raw token и все поля live PhaseBinding. Для найденного токена reserve делается атомарно **до** дальнейшей проверки входа; RESERVED никогда не возвращается в available. Unknown token не резервирует чужую фазу. Один phase в работе; concurrent/replay/out-of-order/mismatch/EOF/deadline ⇒ typed refusal+retention. CONSUMED ставится до первого dispatch gate; failure не выдаёт token заново.

Accepted exact D4 keys:

```text
{kind:'accepted',request_id:<fresh32lowerhex>,setup_nonce_digest,scope,binding_digest}
```

Client сравнивает все три binding values с capsule/parent expectation, request_id проверяет как fresh connection id и связывает с последующими сообщениями. После accepted клиент посылает exact `{kind:'input',request_id,input_path,input_sha256}`≤65536B; input_path должен **равняться** admitted exact path и actual hash, не выбирает файл native reader. Native повторно читает уже bound input ref. Terminal/typed refusal≤131072B содержит только status+refs/hashes; accepted/terminal от старой connection не принимаются. Native client stdout — одна redacted summary line≤131072B; child raw туда не копируется.

## 3. Constructor → producer → task → executor: замкнутый source route

D4 exact `start_docs_setup` signature сохраняется. Ни caller JSON, ни observation booleans не конструируют `execute_grant` или `ActiveDocsAttempt`. Минимальный внешний trusted-parent API — уже доверенный opaque объект с `authorize_docs_setup(request)->ParentLaunchLease`; lease предоставляет pre-exec immutable runtime/source verification, gated spawn/pidfd+cgroup attachment, independent watchdog/drains/fallback retention и current allocation inspection. Эти операции реально принадлежат existing Root/operator/runner parent, не descriptor plugin. Отсутствие такого parent — точный runtime prerequisite. При наличии валидного lease source route ниже обязан исполняться; запрет на permanent-refusal stub сохраняется.

Последовательность реализации, один owner:

1. `start_docs_setup`: exact request/finite bounds/ordered phases, grant scope/attempt/allocation/deadline; parent проверяет ожидаемые bootstrap Python+stdlib/loader/source bytes **до** repo exec. Из accepted inventory берутся expected_source/native16/tools/runtime refs. Никаких fresh `--version` probes. Существующие observation registrations передаются только из parent memory.
2. Parent резервирует total workload+control resources и storage, exclusive0700 control/retained roots, exclusive0600 bootstrap raw и pending/fallback receipt. Создаёт random32B setup nonce; редактированный intent из §4 публикуется **до** gated stub. `spawn_gated` получает isolated argv D4, env={}, exact cwd, close_fds/pass_fds и redacted intent, никогда startup transport object. Stub pin+birth+cgroup attach precede exec. Outer control reserve из D4 входит в allocation, не добавляется к1GiB.
3. Parent отправляет по socketpair один startup frame≤131072B: exact constructor projection без execute_grant плюс producer/version/nonce/parent registrations и `base_environment` из lease-held pre-routing snapshot (encoded≤32768B, ≤256names, value≤4096B, общий startup frame cap сохраняется). Snapshot экспортируется только trusted lease, не из descriptor; перед этим parent проверяет отсутствие четырёх routing names. Native `setup_main` читает только inherited FD, strict producer/version/schema; `make_active_docs_attempt(startup,live_parent_channel)` создаёт typed active object после проверки непрерывного parent channel, source/runtime inventory/registration, guard authority/delegation/initial-empty/control reserve/expiry и storage identity. Это локальный fixed constructor, не deserialize arbitrary admission. Startup JSON имеет силу лишь потому, что доставлен известным parent через непосредственно переданный FD; same-user файл её не имеет.
4. Setup готовит `bind_native_context(parsed,active,now,monotonic)` и exact retained readers (`read_tool_observation` для4tools, `read_katex_observation`, `read_reviewed_unit_binding`), complete runtime closure refs/raw SHA, live owning admission/guard и finite fixed16 HEAD/blob/working read schedule. До bootstrap ACK Git не исполняется. ACK связывает parent-verified expected source inventory, не выдуманный measured Git outcome; полный actual native binding выполняет `bind_native_context` в run_phase после ACK и до driver/unit gate. Missing/forged/stale refs⇒no context, no hidden measurement. Accepted existing observations + independent parent registrations достаточно: новая measurement не обязательна. Producer measurements возможны только отдельным stage/grant D4.
5. Setup создаёт socket0600 в private0700 dir, `PhaseLedger`, random32B token для каждой allowed phase и exact capsule. `setup-ack` exact `{kind:'setup-ack',producer,version,setup_id,nonce_digest,request_digest,scope,input_sha256,source_head,source_graph_digest,native_source_digest,runtime_inventory_digest,monotonic_deadline,pid,birth,uid,endpoint,phases}`≤131072B; phases≤2 exact `{phase,binding_digest,capsule}`. Parent сверяет полный request digest+все expected values и pinned producer identity до task launch. `request_digest` — canonical public constructor projection, исключая execute_grant/nonce; включает hashes registrations/resources/storage/deadline. Согласованный monotonic deadline берётся из того же active parent clock. ACK не создаёт runtime trust сам по себе.
6. `RunningDocsSetup` сохраняет **открытый** control socket/watchdog до terminal completion; `with makefile` не должен закрывать живой FD при возврате constructor. Предоставляет `launch_phase`/`bind_phase_leader`, `cancel`, `await_terminal`, `close`. Parent gated-launch exact task/job subtree; pin task leader UID/pid/birth/pidfd и membership **до exec**, посылает по parent channel exact `leader-bind` `{kind,setup_id,phase,binding_digest,pid,birth,uid}`. Setup проверяет active parent phase, регистрирует leader и ACK; только после ACK parent открывает task gate/выдаёт capsule именно нужному step. Для workflow existing external job wrapper связывает свой job leader и отдельно выдаёт preflight/check capsule в нужных steps; preflight consume не авторизует full. Нельзя саморегистрировать leader из client hello.
7. Client hello-first из §2 → reserve/input validation → `run_phase(active,phase)` → fixed Deno driver launch без script grants → driver preflight/owning sourceGraph через bounded native GitReader → independent native exact-plan translation → prepare fixed seed → ordered `execute_bounded` → pure report aggregation → native terminal validation/publication. Broker external ops только preflight/check/docs; driver private ops ниже доступны только pinned driver pipes. Direct check/docs также делают internal preflight. Никакого default Git/PATH/ambient shell или `execute arbitrary argv`.
8. Любая ошибка из любого пункта проходит общий guarded finalizer с момента создания первого child/gate/FD. Parent EOF/cancel/deadline наблюдаются nonblocking multiplexed вместе с stdout/stderr/status, не после blocking read_frame. Independent outer watchdog/fallback выживает при native/driver OOM/EOF. Owned TERM→KILL, continued bounded drain, wait/reap и terminal cgroup-empty обязательны; unknown ownership/closure/drain/publication даёт failure/unknown, запрещает следующие units. Completion ACK parent и terminal success client публикуются после durable receipt/cleanup; отсутствие driver aggregate не уничтожает completed captures.

Parent control после startup — closed NDJSON `leader-bind`, `completion-ack` и literal `C\n` cancellation; EOF равно cancel. Каждая control frame≤131072B, total serialized control history≤256KiB, timestamps/deadlines finite. Secret-bearing startup/ACK/capsules не включаются в persisted protocol history. `completion-ack` exact `{kind:'completion-ack',setup_id,terminal_ref}`; ref проверяется против actual terminal bytes/hash. Переиспользование setup/renewal/retry не разрешено. Если закончился deadline между preflight и full, full blocked, нужен отдельно разрешённый новый setup/attempt.

Base `Step.clearEnv=false` переводится native adapter в explicit inherited map из **parent-held pre-routing environment snapshot**, полученного до добавления четырёх QCL fields; snapshot не сериализуется в durable intent. Это сохраняет base inheritance D3, исключает утечку capsule и не делает base env={}. Dedicated maps остаются exact D2. Supervisor/client startup и Git maps — отдельные exact scopes; driver env={} без routing secrets и без script permissions. Actual final base inheritance provenance проверяется CPP; неизвестный snapshot ⇒ blocked, не ambient fallback.

## 4. Никаких secrets в durable intent, raw logs или receipt

Два разных типа обязательны: `StartupTransport` (ephemeral inherited channel, содержит nonce; ACK содержит capsules) и `AuditIntentV1` (allowlisted durable projection). Никогда не передавать `durable_intent=frame`, `repr(request)`, полный env, exception message с payload, argv с capsule или сырой control transcript в raw/logs/receipts. В errors только fixed reason code + bounded безопасный locator; dump неизвестного объекта запрещён.

AuditIntent exact keys:

```text
{format:'root-docs-bootstrap-intent.v1'|'root-docs-phase-intent.v1',
 producer,version,setup_id,authorization_ref,
 scope,input_ref,source_head,source_graph_digest,native_source_digest,
 runtime_inventory_digest,request_digest,setup_nonce_digest,
 phase_bindings:[{phase,attempt,binding_digest,token_sha256}],
 allocation_ref,storage_binding_digest,wall_deadline_utc,created_at_utc}
```

Intent≤16384B; вложенные refs exact path/SHA с bounded path. До native generation tokens ещё не существуют: pre-child bootstrap intent имеет phase_bindings с exact parent phase values, `token_sha256:null,binding_digest:null`; позже отдельный bounded redacted phase-intent заполняет hashes до phase child. Не подменять null нулевым SHA. Обе ветви union имеют ровно показанный набор keys; format различает bootstrap/phase. В bootstrap null разрешён только для двух ещё не созданных phase hashes; в phase все hashes обязательны. Остальные поля обязательны в обеих ветвях. Raw nonce/token/capsule никогда не допустимы ни в одном из них. Bootstrap intent хранит nonce digest; phase-intent — окончательные hashes. Каждое record exclusive0600, no overwrite.

Bootstrap stdout/stderr — только redacted fixed diagnostics, ≤D4 log reserve; native client/driver не печатают secrets. Public receipt включает token/nonce **hashes**, source/runtime/input/attempt bindings, raw refs и actual capture counters. Unit inherited base environment не содержит QCL capsule. Если старый receipt/intent уже потенциально содержит token, не переписывать historical evidence; I2B report отмечает дефект, а новый setup не использует старые tokens.

## 5. Exact bounded protocol и сохранение полного pure Capture

### Общие readers и envelope

Private wire version1; strict UTF8 NDJSON, один outstanding request, no BOM/NUL/duplicate keys/nonfinite numbers/extra keys at every level. Encoded limits включают terminal LF. Проверить допустимую длину **до allocation/read/decode/write**; bounded partial buffer/read deadline; unexpected EOF/extra frame/sequence/late reply ⇒ cancel+retain. Wire `sequence` общий возрастающий1…4096 на phase для всех driver requests (Git и stream-read тоже), response echo; request_id32hex одинаков с start. Reply не принимается только по kind. Nesting≤16, arrays/maps имеют fixed plan/input limits; нет произвольного recursive object.

Native→driver `start` exact `{kind:'start',version:1,request_id,sequence:0,mode,input,workspace,binding_digest,remaining_ms}`≤65536B, input≤32768 UTF8B. Remaining_ms positive finite integer bounded by active deadline; native parent остаётся hard clock authority. Driver local inactivity timeout≤10s и absolute remaining budget не продлеваются ответами; native independently enforces same deadline. Вызов `start` не переносит capsule/token/nonce в driver.

Каждый последующий request имеет exact common keys `{version:1,request_id,sequence,op,...}`; response `{version:1,request_id,sequence,kind,...}`. Payload unions:

| Request / payload | Response / payload | Encoded caps request/response |
| --- | --- | --- |
| `preflight {input}` | `metadata {metadata,binding_digest}` | 65536 /131072B |
| `git-read {root,args}` | `git-capture {ticket_id,streams,exit_code,signal,complete,stop_reason}` | 4096 /4096B |
| `prepare {input_sha256,plan}` | `prepared {binding_digest,seed_ref}` | 32768 /16384B |
| `execute {index,step}` | `capture {index,ticket_id,capture_meta,streams}` | 16384 /16384B |
| `stream-read {ticket_id,stream,offset}` | `stream-chunk {ticket_id,stream,offset,data,eof,chunk_sha256}` | 512 /49152B |
| `finish {aggregate_summary,aggregate_sha256}` | `finished {terminal_ref,summary_sha256,result}` | 131072 /16384B |

Для любой операции допустим exact `refused {code,retained_ref,cleanup_status}`≤16384B: code fixed enum, ref actual bounded path/SHA илиnull, cleanup_status=`complete|unknown`; это terminal, не next-step permission. `result` только `failed|blocked|passed|ready_for_unit_attempt`, scope проверяется отдельно. Unknown kind/op/index/plan/task/extra field ⇒ terminal failure. Response schemas metadata/plan/step — existing exact pure types плюс independent native validators; `aggregate_summary` определён ниже. `index` integer0…3, ровно следующий expected step; no duplicates/reordering. Preflight после start один; prepare один только units mode; git-read разрешён лишь в предусмотренном binding slot; execute только после native prepare. Stream-read только пока текущий ticket открыт; finish закрывает протокол. No arbitrary file/exec/ref-read API.

`streams` — exact `{stdout:{ref,bytes,sha256},stderr:{ref,bytes,sha256}}`, refs actual retained files, bytes integer≥0, ref.sha256=stream.sha256. Native owner создаёт random ticket_id32hex с immutable binding request/index/stream identities; client не выбирает path. `capture_meta` — полный existing Capture **без** stdout/stderr; supervision evidence_ref actual native receipt. Git combined raw≤262144B, unit combined raw≤per_step_log_bytes≤1MiB; aggregate units≤4MiB. Complete flags/UTC/exit/signal/cleanup проверены независимо; partial capture всегда retained и failed. stream ref не означает complete.

### Chunk hydration

`data` — strict canonical unpadded base64url, decoded≤32768B. `offset` должен равняться текущему expected offset; каждый nonfinal chunk ровно32768B, final=min(32768,remaining), eof истинно iff offset+decoded==recorded size. Empty data допустимо только для нулевого stream на offset0/eof=true. Никаких client-selected chunk size/paths/range rewind/retry; chunk SHA и конечные size+raw SHA сверяются с ticket. Response overhead≤1024B; request≤512B. Native читает только immutable actual raw через bounded nofollow handle, сверяет stat identity; short/read/drift⇒failed retained capture.

Driver на execute гидратирует максимум один bounded1MiB capture, проверяет bytes/SHA, fatal UTF8, восстанавливает **тот же** pure Capture и передаёт существующему `runChecks`. Накопленные pure captures вместе≤4MiB raw; явный raw byte ledger до append/concat, никаких readAll/unbounded buffers. Полные строки остаются в pure result/in-memory contract; refs не подменяют stdout/stderr. Invalid UTF8 сохраняет raw, aggregate failed; replacement decode не разрешён. JS memory для UTF16/temporary bounded conversions учитывается workload envelope, не выдаётся за measured RSS.

`brokerReadGit` таким же образом гидратирует только нужный stdout≤262144B, fatal-decodes **после** полного retained capture и применяет owning `.trimEnd()` из `ops/process.ts`; `ls-tree -rz/-z` internal NUL сохраняются. Остальные metadata streams reject неожиданный NUL. Native blob reader хеширует bytes до text decode. Не пересылать262144B в один128KiB frame и не менять owning section names на basenames.

### Закрытый aggregate budget

Один общий native owner учитывает сериализованные bytes обоих направлений, failed/partial frames и retention writes **до** записи; fork copies не ledger. Hard protocol phase maximum24MiB; actual active storage grant может быть меньше и тогда предварительно проверенный schedule должен fit или phase blocked. Нельзя молча выделить24MiB сверх grant. Bootstrap/parent control reserves отдельные, также входят в total allocation/storage.

Предельный транспортный расчёт: source raw≤8MiB и unit raw≤4MiB ⇒ base64≤16MiB плюс≤2B округления на stream; ≤512 source stdout streams +≤8 unit streams ⇒ ≤904 chunks (sum ceil плюс empty-stream bound). При overhead+request≤1536B/chunk это <1.325MiB. ≤512 git requests+headers по4096B с каждой стороны дают≤4MiB. Остальные start/preflight/metadata/prepare/execute/finish/refusal control вместе≤1MiB, число всех requests≤4096. Итого <22.326MiB, остаётся >1.67MiB внутри24MiB для bounded framing/failed-prefix reserve; конкретный implementation schedule обязан включить все операции и не потратить этот reserve до finalization. Повторные/failed captures не возвращают debit. Если native closure transport/новая операция не входит в этот расчёт, она не разрешена автоматически: читать closure внутри native owner, либо блокировать/пересчитать source contract до исполнения.

Git raw/time/count caps D4 неизменны: child≤262144B/5s; snapshot≤128 calls/2MiB/20s; phase≤512 calls/8MiB/60s, общая phase deadline не reset. SourceGraph full clean8graph=36reads, current7snapshots=252reads **до** closure/native extra reads. I2B обязан предоставить actual complete schedule initial/pre-unit/post-unit/final/full16 binding + failed/cleanup reserve≤512; нельзя доказать fit лишь максимумом каждой snapshot. Raw source files, protocol cache и retained receipt bytes входят в storage ledger. `status/config/ls-tree/cat-file` no-exec config/attributes paths проверить source CPP; fsmonitor/hooks flags не полное доказательство.

## 6. Finish — summary/ref/SHA, независимые originals и terminal receipt

Driver сначала получает полный pure aggregate с unchanged Captures. Для wire делает explicit `project_aggregate`: все existing aggregate/step fields сохраняются, но в каждом nonnull capture только stdout/stderr заменяются exact `streams` refs/bytes/SHA из соответствующего native ticket. Остальные CaptureMeta/summary/plan/runtime/input/source/attempt fields сохраняются; не оставлять hidden `stdout`/`stderr` string ни в nested reason. Reason — bounded fixed code + safe detail≤1024B, максимум4steps. Projection≤131072B; actual canonical encoded size проверяется до write. Это **private transport projection**, не новая форма pure return value и не право перестать сохранять originals.

`aggregate_sha256` — SHA256 canonical full pure aggregate до projection. Native `validate_driver_finish` проверяет exact projection shape, fixed plan/order/input/source/runtime/attempt and all captures against its immutable receipts/stream hashes, rehydrates только свои bound streams с aggregate4MiB cap и reconstructs canonical full aggregate для проверки digest. Native independently checks guard/cleanup/source gate outcomes и exact report grammar/counts из retained complete raw; summary не может повысить failure/unknown в pass. Допустим ограниченный in-memory reconstruction; писать дубликат многомегабайтного aggregate/strings в logs/control/receipt запрещено. Native report grammar соответствует existing `parseUnitReport` full-output layout, counts берутся только reviewed final fixture binding; base composite остаётся not_applicable. Unknown reporter layout⇒failed/retain, не liberal fallback.

Native finalizes exclusive terminal receipt≤131072B с compact projection/ref/SHA, actual native outcome, raw byte hashes/lengths/EOF/observed/discarded where known, source observation measured/not_measured, cleanup status, independent driver aggregate digest илиnull. Receipt содержит actual stream refs даже если finish/ACK/driver потерян; parent fallback публикует такой же bounded typed missing-driver record из own capture ledger. Не возвращать caller-provided receipt_ref как якобы созданный artifact. Завершение требует actual durable ref/SHA, owned tree reaped+empty, двух EOF и полного capture; uncertain cleanup/OOM/partial write/drain/storage/transport failure всегда fail closed. Prefix bytes сверяются по actual on-disk bytes после short write; отсутствующие данные —null/not_measured, не0.

Terminal publication и failure fallback резервируются **до первого child**, частичные originals не удаляются, bounded cleanup/drain имеет reserve внутри того же deadline. На physical storage failure independent parent control reserve пытается сохранить fallback; если и он недоступен, retention_status=unknown и никакого claimed durable receipt/pass. Нельзя обещать сохранение при двух отказавших stores. Ни failure, ни SUCCESS не запускают retry автоматически.

## 7. Конечные I2B source corrections и paired controls

I2 CPP R1–R9 сохраняются; этот D5 устраняет только missing contract, не сами defects. Один writer/один source-only проход I2B, затем CPP, без execution. Закрыть:

| CPP finding | Implementable обязательство I2B | Парный manufactured source control |
| --- | --- | --- |
| R1 factory/broker/route | §2–3 concrete active constructors, leader/phase lifecycle, valid route | valid parent→hello→prepare→fake execute ровно1; missing/wrong grant/peer/binding zero forbidden dispatch |
| R2 capture/cleanup/receipt | §3/6 guard от первого fork, multiplex, fallback, empty+reap | complete versus short-write/timeout/EOF/driver-loss; original byte prefixes/hash retained, no next unit |
| R3 tokens durable | §4 distinct allowlisted intent, no raw transport/env serialization | spy all persisted/log objects versus secret sentinel; plaintext token/nonce/capsule absent |
| R4 protocol | §2 hello-first/capsule; §5–6 exact unions/chunks/compact finish | max healthy capture+Git frame sizes versus one-byte oversize/dup/extra/sequence/partial/timeout; pure strings remain exact |
| R5 closure/Git | full fixed16 reads, owning sections/trimEnd/NUL, exact complete schedule | section≠basename and raw trailing LF/NUL healthy; unknown root/path/argv/drift/ledger failure zero bypass |
| R6 storage/seed | one owner reserve before write; disjoint canonical roots; iterator census bounded before allocation; literal seed targets+modes | healthy13nodes versus aliases/unbounded dir input/seed partial/full storage; failed debit not refunded |
| R7 readers/guard | full tool/runtime/KaTeX/count registration and authority/expiry/control reserve predicates | accepted retained observations without probe; self-hash/forged boolean/missing registry/expired/wrong membership refuse |
| R8 native translation | independently rebuild exact Step.argv/cwd/maps; base pre-routing inherited snapshot | base inheritance preserved; dedicated exact maps unchanged; routing secrets absent and no arbitrary argv |
| R9 DEV matrix | coverage map all above, fakeproc/pidfd/cgroup ownership/error cases | healthy route and each refusal assert dispatch count+retained evidence; no claim from nominal method count |

DEV fixture code может быть подготовлен в I2B; tests/import/parser/compiler/format/lint/runtime/native/network/CI не запускать в этом source stage. Не переписывать historical8+8 как новые observed results. После source CPP Root отдельно связывает final fixture counts/hashes/runtime/harness/finite plans для двух DEV invocations, compiler checks и sole pure GREEN. Fake kernel adapters не доказывают actual isolated startup, peers, subreaper/pidfd, cgroup/OOM, storage peak или tool compatibility.

## 8. Условные gates и решение

Обычный исполнимый code path при valid native handoff обязателен. Сегодня не установлены actual trusted runner wrapper/execution grant, independently admitted immutable runtimes/tools/KaTeX/count records, live cgroup delegation/authority/control reserve/current admission/storage allocation, committed clean full16/source graph и реальные kernel/process evidence. Отсутствие любого prerequisite блокирует **конкретный** native attempt до dispatch; оно не оправдывает source stub и не разрешает выдумать READY/authorization/source pass. D5 не устанавливает wrapper и не обращается к серверу.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| D4 hello-first реализуем с четырьмя env names | §2 bounded setup capsule + independent live token record | Codec/producer/client ещё не реализованы и не reviewed high R | изменить |
| Полный pure Capture совместим с bounded wire | §5 chunk≤32KiB/24MiB debit; §6 compact finish | Требуются actual schedule, implementations и paired controls | изменить |
| Durable intent может не содержать phase secrets | §4 explicit projections, pre-child reserve | Source spy/CPP и runtime evidence ещё не получены | изменить |
| Existing authority/physics/contracts сохранены | §1/3 existing parent grant, exact12/D2/native16/fixed13 | Не выдаёт новый trust root или execution authority | сохранить |
| I2B/native source уже приняты или READY | I2 CPP R1–R9 остаются; execution=0 | D5 только design; high R и I2B CPP впереди | данных недостаточно |
| Native/runtime/final CI или science подтверждены | Новых receipts/запусков нет | Только read-only source/Git + три D5 deliverables | данных недостаточно |

STOP для независимого high R. Product/fixture/CP/git writes=0; parser/compiler/format/lint/import/test/runtime/native/network/server/build/solver/final CI=0. Logical source reads и output bytes указаны в identity как явный charged file-content ledger; RSS/CPU/physical I/O не измерены.
