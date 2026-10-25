# I2B — конечная source continuation, PARTIAL / CHANGES REQUIRED

Этап: только изменение исходников в `/tmp/qcl-docs-test-routing-worktree`.
HEAD `2bb05d3651af4509fe7f02c1253b40f1e5146fec`, dirty overlay сохранён.
Это **не source completion, не READY и не разрешение запуска**. Девять групп
CPP не закрыты. Остановка после одного ограниченного source прохода;
следующий шаг — отдельный high CPP и решение Root о продолжении.

Изменены только четыре разрешённых existing owning paths: native Python,
permissionless driver, Python fixture и Deno protocol fixture. Старые I2 wiring,
pure helper и pure fixture не переписаны. Main/Root/CP/компоненты не изменены;
commit/network/server/native/CI/science не выполнялись. Архитектура и AGENTS
selected checkout прочитаны; восемь gitlinks остаются uninitialized и неизменны.

## Что подготовлено

До production edits усилены существующие8 Python methods и8 Deno nominal
registrations: capsule canonical/negative, strict base64url bound, section name,
forged startup/secret projection, Git ticket hydration и malformed chunks.
Это исходники будущих controls, не RED/GREEN или observed pass.

В `ops/docs_tests_native.py` появились capsule/binding codec, UTC helpers,
allowlisted intent projection, `ActiveDocsAttempt`, inherited-parent factory,
retained registration readers, fixed16 native rebinding, bounded Git executor,
независимая native translation Step→argv/env, `DriverPipe`, native report/finish
validators, `run_phase`, broker/leader handshake и outer `RunningDocsSetup`.
`setup_main` больше не unconditional source-incomplete refusal: есть путь
hello→reserved→input→driver→prepare→execute→finish-validation→phase receipt.
Client читает четыре QCL names, очищает environment, декодирует capsule и
первым отправляет hello; server-first challenge удалён. Raw token/nonce не
передаются в durable_intent; base environment в command receipt заменён hash.

Driver использует общую sequence, finite transport deadline, ticket hydration
по32768B decoded chunks,24MiB wire debit, fatal UTF8 и owning trimEnd для Git;
pure Capture сохраняет полные строки. Finish отправляет compact projection,
затем читает finish-validation ACK и выходит до phase/setup receipt.

Parent-side constructor держит control socket после ACK; leader binding
предшествует выдаче capsule. Producer создаёт final phase после driver close,
посылает phase-complete/phase-ready, затем setup-closing и ожидает parent
completion-ack до выхода. Outer finalizer читает whole cgroup после process.wait.
**Его producer terminal proof пока неполон: положительный final setup запрещён.**

Capture lifecycle теперь резервирует cap у parent до fork; proc_birth/pidfd
перенесены внутрь guarded lifecycle. Parent читает supervisor transport
nonblocking, посылает cancel TERM и ждёт cleanup owner; не убивает единственный
subreaper сразу при read exception. Worker пытается продолжить drain после TERM,
перечитывает actual retained prefix и создаётся actual exclusive command receipt.
Storage census использует bounded scandir iterator; disjoint roots/modes/literal
seed target проверяются. Это изменения source, не доказанные kernel guarantees.

## Обязательный failure list перед любым DEV/native

1. **R1 / outer lifecycle:** `RunningDocsSetup.await_terminal` ещё не получает
   independently parent-owned bootstrap stdout/stderr EOF/producer terminal
   receipt. `producer_terminal:null`, result failed/retention partial намеренно
   запрещают false success. Нет завершённого `launch_phase` gated parent route,
   parent loss fallback finalization и полного parent PhaseLedger comparison.
   Отсутствие actual server handoff не объясняет эти source gaps.
2. **R2 / cleanup:** ошибки до полного frame/stream или `DriverPipe.__init__`
   ещё могут оставить FDs/owned identities без полноценного terminal record.
   Command fallback содержит paths, а не проверенные partial raw refs/observed/
   discarded counts; worker cleanup drain и parent fallback не замкнуты при
   всех short-write/timeout/owner exceptions. Driver stderr EOF/reap доказаны
   недостаточно (`stderr_eof:true` нельзя считать наблюдением). Reject-finish ACK
   и durable rejected validation ещё не реализованы для всех failures.
3. **R3 / audit intent:** plaintext secrets из startup исключены, но exact
   D5 AuditIntentV1 bootstrap/phase schema и предзапись phase-intent с token
   hashes ещё отсутствуют. Текущая узкая projection не соответствует полному
   normative intent union. Historical artifacts сохранены, не redacted задним числом.
4. **R4 / protocol:** реализованы основные stream/sequence/capsule шаги, но
   nested exact schema/depth/member validation, per-op encoded bounds до reads,
   ticket lifecycle exhaustion, parent/control/client multiplex и startup/ACK
   timeout handling неполны. TS `hydrateChunks` — fixture seam, не отдельный
   публичный wire contract. Native refusals/finish rejection не замкнуты.
5. **R5 / source/Git:** manual full-check schedule=7×36 owning graph reads +
   (initial+4pre-unit+finish)×32 native reads =444 Git children; preflight=100.
   Это расчёт по source, не measurement. Full snapshot count/time/raw debit,
   reserve final/failure schedule и phase counter reset между двумя phases
   ещё не реализованы. Local Git config/attributes no-exec review отсутствует.
   Native Git capture text decoding ещё недостаточен для arbitrary blob bytes.
   Current overlay не committed/clean; actual native binding обязан отказать.
6. **R6 / storage:** pre-reserve raw/metadata появился, но complete single-owner
   write/transport/seed/lifecycle/fallback ledger ещё не замкнут; child-copy
   storage.observe и sample history не дают общего accounted owner. Setup
   final writes не полностью charged. Full actual storage schedule не доказан.
7. **R7 / retained provenance:** parent registration shape в коде — кандидат
   attachment projection, нуждается в CPP against D4/D5/D6, не новый trust root.
   Runtime closure actual ref прочитан, но полная closure identity/authority/
   delegation/expiry/provenance initial-empty не восстановлена независимо.
   KaTeX record с nested self-ref и admission/count exact producer schemas
   требуют correction; metadata booleans не заменяют эти predicates.
8. **R8 / translation:** native plan повторяет exact D2 routes и base берёт
   parent snapshot; требуется CPP exact projection/permission/env/args и
   гарантированное отсутствие routing secrets в каждом parent-held snapshot.
9. **R9 / DEV matrix:**8+8 сохранились, но healthy parent→fake execute,
   fakeproc/pidfd/cgroup/guard-order/error cleanup/full storage/EOF/driver loss/
   final ACK matrix ещё не подготовлена полностью. Не запускать эти fixtures
   как будто CPP coverage или ready source contract уже получен.

Delivery failure не переписывает historical positive phase receipt: setup
переходит failed/no-next-phase. Однако полноценная parent-side запись причины
delivery failure/phase-ready loss и независимый fallback ещё в R1/R2.

## Identity, бюджет и проверка

Полные18 SHA256 — companion identity. Complete patch включает tracked diff и
все6 untracked source files относительно выбранного HEAD;191274B, SHA256
`c09188ee67b41ffa3df20135b058e0798a49fb2812b8c3f478228f50d94dd3f5`.
Не применялся и не исполнялся. Фактическая source closure не является trusted
runtime manifest или новым lock-файлом.

Исторические I2 v2 report/identity/patch SHA сохранены:
`16a9d55592ffd9d9f3a5bfee295c4c2234608668a665eff18ad2d5721921c769`,
`4b55bcc45c097c7afe887db031dfdc10851759677d8dd1c8fad6fb53293dbf54`,
`55da25d0b259014a57c1508b980187a7aad152a418c380b4407559fc898be729`.
Historical RED fixture SHA04589… неизменен; pure helper SHA676a… и current
pure fixture SHAf02f… неизменны.230 nominal=227 ancestral+3 retention cases.

Выполнены только source reads/patches, read-only Git observations, `sha256sum`,
`wc` и текстовая инвентаризация. Parser/compiler/format/lint/import/tests/
Deno/Python product/native/Julia/network/build/CI/science=0. Diff не является
компиляцией; синтаксическая/типовая корректность не заявляется. Source read
<8MiB, patch+report+identity<256KiB;1CPU/1GiB — cap, CPU/RSS не измерялись.
Новых попыток исполнения0; finite continuation не продлевается автоматически.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Pure API/230 ancestry сохранены | unchanged SHA676a…/f02f…/historical04589… | execution0 | сохранить |
| Producer route больше не unconditional refusal | native symbols factory/broker/run_phase + driver hydration | перечисленные R1–R9 ещё блокируют source completion | изменить |
| Native setup имеет положительную final acceptance | finalizer сохраняет failure с producer_terminal:null | полного producer drain proof нет | данных недостаточно |
| CPP/DEV/native/CI gates закрыты | запусков и accepted receipts нет | source continuation only | данных недостаточно |

STOP отдельный high CPP. Никаких product calls по этому source grant.
