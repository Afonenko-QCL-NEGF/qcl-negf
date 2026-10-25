# D5 — независимый high source review

**Вердикт: CHANGES REQUIRED по одному блокирующему lifecycle contract.**
Capsule/hello-first, redacted intents и bounded hydration/finish имеют
реализуемый source contract. До I2B нужен узкий exact amendment, разделяющий
command closure, phase closure и закрытие всего setup workload. Полный D5
SOURCE PASS сейчас не выдан. Девять I2 source findings сохраняются: этот review
дизайна не проверяет их исправление и не объявляет native READY.

## Неизменяемые входы

| Вход | Проверенный SHA256 |
| --- | --- |
| D5,39871B | `6049f427a10c769b69c2beaaa1374e583d217d6eb68926337204e560b824ed48` |
| D5 delta ledger | `c07e749848f5b4040c3ae0350b783faa9402627314d2dc80aacb9cc6b2a2202f` |
| D5 identity | `bf560be45400d2b7363fc730be1b6b0a4582ee4832506858f595d5556697ffd7` |
| I2 high review | `5b7ec1e5f1fefad767315f539fe637c12c322902c78d542acea16639931ced60` |
| Governing D4 | `24a7d68b612e7d3dc437404bb805df777ede1f5159c0bff39eca7d693ebe8fc0` |

D5 прочитан целиком; обрезанный первый tool output не считался прочитанным,
строки1–145 и143–184 перечитаны отдельными slices. D4 контракт и собственный
I2 review сохранены из предшествующего source review, релевантные D4:127–152
прочитаны заново. D5 identity и delta ledger проверены как evidence, не authority.

Selected `/tmp/qcl-docs-test-routing-worktree` повторно даёт HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`; status тот же:5 tracked edits,
6 untracked source files;8 uninitialized submodules с прежними gitlinks.
Native Python `4f87e4…`, driver `e43491…`, pure helper `676a3d…`, current
fixture `f02f54…` повторно хешированы и совпали с I2. Нового implementation
overlay нет. Coordinator HEAD из D5 не заменяет selected source.

Это отдельный source design review. Target imports/parser/compiler/lint/
formatter/tests/native/runtime/network/server/build/solver/CI=0;
source/fixture/CP edits=0. Разрешены только два новых review artifacts.
Консервативный charged read bound<1MiB, при лимите6MiB; новые output<32KiB,
при лимите128KiB. CPU/RSS/physical I/O не измерены. Субагенты не привлекались.

## Блокирующее D5-R1: terminal-empty scope противоречит живому producer

Точные immutable locators:

- D4:132–134: setup Python, driver, supervisors и Git descendants находятся
  **в том же** bounded workload cgroup до dispatch; trusted outer parent
  располагается с control reserve снаружи. Этот контракт D5 явно сохраняет.
- D5:76–77: setup создаёт broker/PhaseLedger и до2capsules; RunningDocsSetup
  держит открытый control socket до completion, последовательно запускает
  preflight и затем check/docs.
- D5:78–81: setup/broker обслуживает driver finish и client outcome;
  `terminal cgroup-empty` обязателен, а completion ACK/client success публикуются
  после durable receipt/cleanup. Setup остаётся живым для этого обмена и,
  после первой фазы, для второй разрешённой фазы.
- D5:149: terminal receipt требует `owned tree reaped+empty`, двух EOF и
  complete capture; D5:160 переносит empty+reap в I2B обязательства.
- Current I2 `ops/docs_tests_native.py:326–329`: terminal-empty означает
  буквально `cgroup.events populated == 0`, не проверку command descendants.

Следствие выводится из source contract, без kernel probe: пока setup находится
в общей cgroup и сам формирует terminal receipt/ответ, эта cgroup не пуста.
При первой из двух фаз она обязана оставаться занятой setup/broker. При finish
driver также может ещё ждать `finished {terminal_ref,...}` (D5:121), прежде
чем закрыть pipes и выйти. Нельзя одновременно требовать его reap/EOF для
создания final ref и держать этот ref обязательным ответом до его выхода.

Writer не должен обходить конфликт ослаблением `populated==0`, исключением
setup/driver из RAM/CPU boundary или маркировкой phase subtree closure как
whole-workload-empty. Это не runtime prerequisite и не отсутствие server
credentials; контракт сейчас не задаёт достижимый healthy terminal порядок.

### Узкое обязательное исправление до I2B

Сохранить один admitted workload cgroup и существующий trusted outer parent;
новая child-cgroup архитектура не нужна. Явно определить разные результаты:

1. **Command closure:** закончились command producer streams, все принадлежащие
   этой command descendants reaped, supervisor terminal ACK завершён. Живые
   setup/broker/driver не выдаются за command descendants; их identities входят
   в отдельный pinned phase/setup owner set. Resource/memory events продолжают
   проверяться по общему workload, но здесь нельзя требовать `populated=0`.
2. **Phase closure:** driver получает ограниченный finish acknowledgement,
   завершается, outer/setup owner доводит driver descendants до closure и
   проверяет EOF/reap. После этого создаётся final phase receipt и client
   outcome. Setup/broker остаётся внутри того же admitted workload и может
   обслужить только следующую заранее разрешённую фазу. Phase receipt явно
   различает phase-descendant-closure и ещё активный setup; не содержит claim
   whole-cgroup-empty.
3. **Setup closure:** после последней фазы или cancel/EOF/deadline producer
   завершается, а **outer trusted parent** закрывает remaining owned subtree,
   reap-ит producer и проверяет whole-workload `populated=0`/events. Только он
   может опубликовать final setup receipt/whole-workload cleanup evidence.
   При аварии остаётся independent fallback; partial/raw не исчезают.

Нужно exact wire решение для шага2: нынешний `finished.terminal_ref` не может
ссылаться на final phase receipt, если этот receipt требует завершения ещё
ожидающего driver. Минимальный допустимый путь — bounded immutable
pre-closure finish-validation receipt/ref с явным статусом, затем driver exit,
затем отдельный final phase receipt; client/outer success только по второму.
Имена и exact schemas/sequence/digest/debit должен заморозить narrow amendment,
не medium writer по догадке. Допустим другой точный двухшаговый порядок,
сохраняющий те же gates и128KiB caps. Pre-closure ref не означает cleanup pass.

Также exact amendment должен уточнить parent control завершение: D5:81
`completion-ack {terminal_ref}` относится к phase либо final setup, кто и когда
посылает его, а какие channel EOF являются штатным завершением после ACK.
Не смешивать штатное producer exit после последней фазы с cancel до commit.
Initial-empty evidence для setup берётся outer parent **до** gated bootstrap;
native active factory получает его связанным с тем же allocation/birth, а не
требует пустоты cgroup, в которой уже исполняется сам setup.

Минимальные manufactured source controls будущего I2B: preflight→check на одном
живом setup; driver ждёт finish ACK и выходит; phase closure оставляет setup
учтённым/admitted; setup shutdown перед whole-empty; producer/driver loss до и
после ACK; no empty/pass claim при lingering descendant. Эти controls готовятся
как source, не исполняются в D5/I2B.

## Подтверждённые решения D5, без новых design blockers

**Четыре env names и hello-first:** D5:19–64 задаёт exact PhaseBinding,
scope/expiry/attempt, raw256 token и canonical bounded capsule. Client получает
attempt/source из live producer capsule, actual input hash сверяет отдельно,
server lookup/peer/leader checks остаются независимыми. Unsigned capsule служит
transport, не authority; caller JSON/self-hash не создают registry/grant.
≤4096B encoded/≤2048B decoded, fixed members/depth и re-encode equality дают
конечный decoder. SHA от raw32B, не hex spelling, снимает двусмысленность I2.

**Producer/factory/live allocation:** D5:68–78 связывает existing opaque parent
grant с pre-exec source/runtime checks, admitted allocation/control reserve,
nonce/request/source/input/runtime ACK, pinned leader-before-exec и обычным
factory→readers→broker→driver→executor route. Parent handoff и actual allocation
остаются irreducible runtime prerequisites. Их отсутствие не оправдывает
permanent source stub. Это не новый trust registry и не выдача execution grant.

**Secrets:** D5:87–102 разделяет ephemeral StartupTransport и exact durable
AuditIntent. Bootstrap null phase hashes явно допускаются до generation;
phase intent содержит actual hashes, plaintext nonce/token/capsule/env запрещены.
Это устраняет missing design для I2 R3, но сам дефект `durable_intent=frame`
в неизменённом native.py:649 ещё существует. No historical rewrite сохраняется.

**Hydration и24MiB wire envelope:** D5:108–141 задаёт closed sequence/union,
ticket-bound immutable streams, decoded chunk≤32768B/encoded≤49152B, offset/
eof/SHA/size и bounded fatalUTF8 reconstruction. Base64 full chunk43691B плюс
≤1024B response overhead укладывается в49152B. Raw12MiB дают≤16MiB base64
плюс finite rounding; заявленные≤904chunks с overhead/request1536B дают
<1.325MiB;512Git headers/requests≤4MiB ипрочее≤1MiB оставляют reserve в24MiB.
Это консервативная арифметика upper bounds, не actual measured schedule.

Actual source schedule/native closure extra reads и failed prefixes должны
fit в заявленные caps; иначе blocked до dispatch. Гидратация только stdout Git
не отменяет native retained stderr/raw debit. Preflight/finish не получают
arbitrary path-read/exec operation. Stream tickets и caps не авторизуют callers.

**Pure Capture и компактный finish:** D5:125–147 сохраняет полные strings для
pure `runChecks`, aggregate4MiB bound и wire-only projection streams/ref/SHA.
Native independently сверяет actual raw/report grammar/counts и reconstructs
digest; synthetic summaries не повышают failure/unknown.128KiB terminal/raw
control outputs не содержат копию многомегабайтного aggregate. Это coherent
data contract, но lifecycle ref/ACK порядок требует D5-R1 amendment выше.

**Сохранение original evidence:** D5:149–151 требует actual durable receipt
ref/SHA, parent fallback, pre-child reserve и partial byte identity после short
write. При dual-store failure честно unknown, без обещания durable pass.
До реализации это требования, не evidence выполненного cleanup/retention.

## Обязательные I2B CPP условия после narrow amendment

Эти условия уже следуют D3/D4/D5 и не являются новыми design blockers:

- Реализовать все9I2 findings; exact producer/active factory/registration/readers,
  no hidden probes, source16 committed blob/working SHA binding и Git
  per-child/snapshot/phase ledger≤512/8MiB/60s. Clean8graph=36reads,
  current7snapshots=252reads до closure; проверить полный schedule.
- Owning `.gitmodules` sections, `.trimEnd()` и valid NUL framing сохранять;
  native driver всегда injected reader, zero default `git/run/Command.output`
  на binding/failure/terminal paths. Local Git config/attributes no-exec closure
  проверять по реальным selected paths; одни hooks/fsmonitor flags недостаточны.
- Exact canonicalization vectors между JS/Python, включая non-ASCII captures,
  escaping, safe integer fields и null/unsubmitted captures; digest совпадает
  для full pure aggregate, а wire projection не меняет pure return value.
- Все encoded caps включают LF; reserve/debit проверять до каждого buffer
  append/write; source raw, transport bytes и storage retained bytes имеют
  явные ledger domains, не обнуляются между fork/failure/cleanup.
- Driver runtime/cache/HOME/TMP, если используются, должны помещаться в owned
  storage domains при exact env/argv; env={} само не доказывает отсутствие
  runtime cache writes. Не расширять dedicated D2 maps/permissions.
- Manufactured paired source controls из D5:159–167 и D5-R1 выше покрывают
  max captures, chunk/sequence/short-write/EOF/deadline/fallback и no-secrets
  projections.8+8 ancestral nominal counts не превращаются в observed pass.

Source design → I2B implementation → independent CPP → separately budgeted
compiler/DEV/pure GREEN → native/kernel gates → final CI — разные gates.
Проверка source contract не является source build, компиляцией или выполнением
проверок. Final committed HEAD/blob binding не наследуется dirty2bb overlay.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Capsule решает four-env/hello-first handoff | D5:19–64 exact codec+live lookup | Source design; producer/client не исправлены | сохранить |
| Secrets исключены из intended durable schema | D5:87–102 | I2 secret-bearing call пока существует | сохранить |
| Full pure captures помещаются в bounded transfer | D5:108–147 chunk/ticket/debit/projection | Actual schedule и cross-runtime codec нужны в CPP/DEV | сохранить |
| Healthy phase/setup terminal lifecycle исполним | D4:132–134 против D5:76–81,121,149 | Setup/driver alive, whole cgroup не empty | изменить |
| D5 закрывает9I2 defects кодом/доказывает READY | Source overlay unchanged; execution0 | Только design review | данных недостаточно |
| Нужны новые server measurements до исправления контракта | Противоречие видно по immutable locators | Native evidence gates позже | изменить |

STOP: Root фиксирует узкий lifecycle amendment и получает его focused source
review; medium I2B ждёт. Никаких automatic execution/retry/CP changes.
