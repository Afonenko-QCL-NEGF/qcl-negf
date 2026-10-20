# I2B — independent high source CPP

**CHANGES REQUIRED; native source integration пока не готова.** Есть новый
реальный producer/broker/driver route вместо прежнего always-refused setup,
но healthy final acceptance недостижима и несколько failure paths не замкнуты.
Это source defects, а не отсутствие сервера. D4/D5/D6 достаточно для I2C:
новый design-only цикл не требуется.

Pure helper/230 fixture остались byte-identical и import-safe. Native gaps
не блокируют отдельный, уже source-reviewed pure контракт; его будущий finite
GREEN требует своего Root plan/runtime/attempt binding и здесь не выполнялся.

## Identity, метод и owning manifest

Сначала просмотрены actual native/driver source и их call paths; авторский
failure list прочитан после первичной проверки constructor/run_phase/finalizer/
capture/ledger. Затем findings сопоставлены с report. Автор правильно пометил
результат partial и не заявил READY; это не отменяет independent CPP.

Immutable packet:

| Артефакт | Проверенный SHA256 |
| --- | --- |
| I2B report | `611ce7f52ca694418a68153cbeb41fda0354762c08a6809336a3b564f0bd8e78` |
| I2B identity | `5dce8bf047b9ca7a19e4ef39615b393254a6a8c21a10ee1883c3896026e7cbb0` |
| complete patch,191274B | `c09188ee67b41ffa3df20135b058e0798a49fb2812b8c3f478228f50d94dd3f5` |

Selected `/tmp/qcl-docs-test-routing-worktree` фактически HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`,5tracked modifications и6untracked
source files;8submodules uninitialized с прежними gitlinks. Никакие indexes/
gitlinks/CP/source не менялись этим review. Locators ниже относительны этому
worktree; overlay определяется exact SHA, а не приписывается committed2bb.

| Owning path | SHA256 | Отношение к I2 |
| --- | --- | --- |
| `ops/docs_tests_native.py` | `0e7616ffc39fe209d7c47d469562bac09d9246bb09908504e8b9162d95e82669` | changed |
| `ops/docs_tests_cli.ts` | `4276c0222c627100a8fbc0ebb8bd8c5aaeff85de91a4918020a66be8457bdfc6` | changed |
| `tests/test_docs_test_native.py` | `6e279b7ec70f805bba9eef06ee7bc3f6f6d65ce4dade46449134a71d0440275f` | changed,8nominal methods |
| `tests/docs_test_native_protocol_test.ts` | `07c6d2510a8903a409be4cc96c40e99ed0f1f03d0bd1d9933335f6b9a6adedbe` | changed,8nominal registrations |
| `ops/docs_tests.ts` | `676a3db1a4de455bbd73a46e57f316b4ae7721e631aa3b7d81a2da8564340d8c` | unchanged pure |
| `tests/docs_test_routing_test.ts` | `f02f541d633c56280077701ba9fbee3928ae7c2e055cae8b2e78d759bd3a9761` | unchanged230 |
| `ops/git.ts` | `f1b37ea11c20bd3e64ac7e57ce4d5bc649897a8db9f099ccdc87ada4e4e65764` | unchanged injected seam |
| `ops/process.ts` | `8783e0e7dddd07df7c58d1f2d22f4a44d5ac8a634c68b6ca4722ab25e214f249` | unchanged |

Все16production+2DEV hashes сверены с I2B identity; остальные10production
paths exact native16 не менялись. Complete patch hash/headers соответствуют
owning11-path overlay относительно HEAD; patch не применялся. Сохранены
accepted D4/D5/D6 и D6 review `ba96c60c…`; ни source build, ни runtime evidence
из предыдущих design PASS не наследуется.

## C1 — parent route не завершает healthy setup и ломает две фазы (P1)

`native.py:1202–1227` после process.wait всегда пишет
`producer_terminal=None,result='failed',retention_status='partial'`. Это
честный fail-closed partial result, но valid handoff не может достичь D6 final
setup complete. Producer raw EOF/actual terminal proof, remaining participant
ownership/cleanup и fallback здесь не реализованы. `status` результата wait
вообще не используется. Guard пересоздаётся после wait (`:1218`), поэтому его
initial memory.events — уже финальные; future positive path обязан сохранить
original admitted baseline, а не обнулить наблюдение OOM/max.

Независимая конкретная ошибка двух фаз: после preflight producer пишет
`phase-ready` в parent channel (`:1389`). Следующий
`bind_phase_leader('check',...) :1192–1199` читает следующий frame как
`leader-bound`, но там ещё queued `phase-ready`; вызов откажет.
`await_terminal :1205–1215` умеет читать phase-ready, однако не возвращает
управление до setup-closing, который требует запуска второй фазы. Нет
`await_phase`/общего control dispatcher и parent PhaseLedger correlation.
Также нет concrete `launch_phase` before-exec gated task API.

Исправить в existing parent lease contract: один bounded control pump,
раздельные leader ACK/phase-ready/setup-closing states; parent-held phase
expectations и full digests; admitted gated task launch; complete producer
raw/status/EOF/reap proof и actual D6 final setup receipt с positive branch
только после required phases/job outcomes/whole-empty. Shared source API
должен получать terminal evidence от уже trusted lease, без нового trust root.

## C2 — KaTeX reader требует самоссылочный SHA; readers не closed (P1)

`native.py:895–909` сначала читает persisted record по `ref`, затем требует
`record['ref'] == ref`. Поле ref содержит SHA **того же record**, поэтому
обычное создание record→SHA→ref меняет собственные bytes. Это не корректный
artifact format, а требование криптографического fixed point. Healthy KaTeX
reader практически не может быть удовлетворён.

Исправить persisted producer record без self-ref; actual external ref добавить
лишь в normalized pure projection после чтения. Это private reader correction,
public KaTeX descriptor/pure retained_katex менять не надо. Привязать runtime/
KaTeX/count/admission formats к точным producer schemas и parent registration.
`read_reviewed_unit_binding :913–918` не проверяет exact record key set;
runtime reader `:447–451` проверяет SHA manifest ref, но не полную admitted
closure contents/identity. Active initial-empty `:828–831` читает ref, но не
сопоставляет его decoded fields с принимаемыми registration labels.

## C3 — AuditIntent и startup/ACK/attachment не соответствуют exact unions (P1)

`audit_intent :119–123` безопаснее прежнего plaintext dump, но создаёт новый
`root-docs-setup-intent.v1` с несколькими полями. D5 задаёт exact
bootstrap/phase-intent union с input/source/runtime/allocation/storage/deadline/
nonce/token hashes. Phase intent перед phase child отсутствует. Request digest
этой projection включает producer/version, а constructor ACK сравнивает
digest request без этих keys (`:1271`): это не одно binding.

`ActiveDocsAttempt :801–843` проверяет exact только верхний registration set,
но не exact startup/request/nested producer attachments, finite scalar ranges,
allocation/delegation authority/expiry/initial proof/reserve consistency.
ACK содержит runtime_inventory_digest, однако `:1270–1273` его не сравнивает
с независимо ожидаемым inventory. `:1274–1277` сравнивает capsule главным
образом по phase/attempt, не весь allowed PhaseBinding. `:1332` digest берётся
из runtime_closures subset, а D5 требует exact admitted Python/runtime/four-tool
inventory identity.

Сохранить ephemeral transport/no-secrets allowlist, реализовать нормативные
closed schemas и exact full expected comparisons. Не принимать JSON labels
как authority; known inherited parent channel — transport trusted handoff,
но не замена проверки привезённых bytes/bindings.

## C4 — exception retention/cleanup всё ещё теряет captures (P1)

`run_phase :1123–1126` делает native Git/metadata до общего try/finally.
Source failure здесь оставляет новые command originals без final phase record.
`driver=DriverPipe(active) :1130` присваивает объект только после успешного
constructor; exception после fork внутри `DriverPipe.__init__ :964–985`
оставляет `driver is None`, и caller cleanup его не видит. Constructor finally
закрывает несколько FDs, но не доказывает child closure/reap.

`execute_bounded :703–724` создаёт command receipt только на полном happy
transport path. Если supervisor уже reaped, но status/guard/raw-read/publication
ошибка бросает исключение, fallback `:739` пропускается из-за `not reaped`.
`Active.command :868–874` тогда не регистрирует capture/ticket; raw файлы могут
остаться, но authoritative aggregate/evidence index теряет их.
Fallback `:741–742` содержит paths, а не actual bounded raw refs/hashes/partial
bytes/observed-discarded unknowns. Worker перед capture try также выполняет
prctl/owner scan (`:563–564`); их ошибка не порождает terminal result.

В worker cleanup drain `:619–634` управляется наличием owned processes, а не
EOF обоих streams. После смерти producer в pipes могут оставаться bytes;
их EOF/drain не доказаны. `DriverPipe.close :1037` просто выставляет
`stderr_eof=True`: stderr пишется child прямо в file (`:970`), отдельного
bounded observed EOF/drain/size/hash contract нет. Driver constructor также
должен закрыть все unrelated inherited FDs перед exec, включая bootstrap
parent FD, а не полагаться только на CLOEXEC новых pipe FDs.

Решение: guarded owner от первого FD/fork, durable pre-child command index;
при **каждом** outcome terminal record из actual on-disk prefixes, preserve
first failure, bounded nonblocking status/cancel/drains и explicit unknown
closure; parent fallback независимо от того, успел ли reaped=true. Phase index
строится из native ledger, не только successful `active.captures`.

## C5 — reserve/debit делает нормальный444-read route непроходимым (P1)

`execute_bounded :662` безвозвратно debit-ит полный per-command cap262144B для
каждого Git, а `Active.command :867` —147456B metadata на каждый command.
`StorageLedger.debit :347–350` складывает их как совершённые bytes, unused
reservation не освобождается. Для source schedule444Git reads это111MiB raw
и62.4375MiB metadata **до unit output**, хотя source raw phase максимум8MiB,
а D6 требует actual complete metadata/control schedule в своих capped domains.
Это не измеренный расход, а искусственно списанная сумма максимумов.

Нельзя исправить увеличением8MiB/2MiB caps или тихим refund failed bytes.
Нужны distinct outstanding reservation и committed actual debit, immutable
parent ledger до writes, снятие только неиспользованной reservation, failures
charged по actual written/observed/reserved uncertainty. Actual Git bytes и
final/failure reserve надо планировать целиком до unit dispatch. Parent-side
final writes `:1222–1226` сейчас вообще обходят shared ledger. Transport send/
receive :989–1008 считает wire bytes, но не все partial prefixes до read и
не связывает storage/metadata debit. Driver stderr file пишет в обход raw cap.

## C6 — phase/snapshot budgets и full source gates неполны (P1)

`git_calls/git_raw/git_seconds` инициализируются только в Active constructor
`:838`, не сбрасываются на новую фазу. Healthy preflight100+full444=544reads
превышает global512 на второй фазе даже без failures. D4 cap — **per phase**,
а общий storage/allocation/deadline при этом не сбрасывается. Snapshot128calls/
2MiB/20s и reserve финального binding не реализованы. `run_phase :1140–1148`
разрешает git-read/old tickets без exact binding-slot lifecycle; ticket не
связан с request/phase/index и после EOF не закрывается.

Native fixed16 rebinding полезен (`:921–938`), однако после unit меняется только
driver graph, полный native16 повторяется перед следующей unit/finish. Если
граф после failure бросает, driver returns failure, а native finish валидатор
`:1083` требует stable=True и бросает до retained rejected validation. Native
raw blobs вообще проходят текстовый worker fatalUTF8 path (`:643–652`), хотя
hash должен оставаться byte-based. No-exec local Git config/attributes closure
не доказана. Сохранить injected owning sourceGraph, section names и trimEnd/NUL;
не заменять их default git/run/output ради завершения.

## C7 — private protocol/data validation ещё не полна (P1)

Python `decode :138–146` не ограничивает nesting/member/scalar shape;
`json.loads` overflow exponent не запрещается одним parse_constant. Driver
`boundedJson :51–70` также не даёт depth16/finite nested-number contract.
Native send/receive :987–1008 применяет generic128KiB, а не per-op caps D5;
stdio TS :160–178 аналогично даёт generic request cap. Oversized malformed
binding не должен доходить до allocation/process side effects.

Native `validate_driver_finish :1075–1098` реализует почти только success:
failure aggregate/rejected validation вызывает исключение, rejected ACK и
durable validation record отсутствуют. Exact aggregate/step/runtime/attempt/
summary unions проверены частично: raw report перепроверяется, но например
`step.summary` не сверяется с независимо разобранными counters. TS finish ACK
`:184–186` не проверяет actual returned digest/ref/validation enum полностью.
`hydrateChunks :25–37` выделяет decoded part до encoded32768 bound; actual
stdio frame bound ограничивает общий memory, но one-byte-over-chunk source
control должен отвергать его до decode. Fixture seam не заменяет actual codec.

Нужны exact finite readers для всех existing unions и active operation state
machine; healthy/rejected/transport-lost finish идут по D6 closure sequence
без потери уже сохранённых captures. Chunk/full pure Capture/compact projection
не менять ради упрощения. Данные invalidUTF8 остаются raw+failed.

## C8 — DEV8+8 не покрывают implementation acceptance (P1 к native READY)

Оба source fixtures прочитаны целиком: восемь Python methods и восемь Deno
registrations сохранены и усилены codec/seam assertions. Нет healthy
trusted-parent→broker→prepare→fake execute→finish→driver closure→producer
closure→final setup acceptance. Нет fakeproc/pidfd/cgroup gate-order, partial
write/storage-full/owner exception, two-phase parent-control pump, driver
stderr, terminal binding/source failure и complete failure-retention matrix.
`test_forged_grant… :78–88` проверяет bool/None и два secret substrings,
но не exact normative AuditIntent или реальный independent grant route.

До DEV source fixtures надо дополнить paired manufactured controls этих
реальных paths. Можно сохранить8+8 top-level registrations, расширив parallel
subcases; можно изменить counts с отдельной frozen mapping. Ни source counts,
ни согласие автора/reviewer не объявляются observed pass.

## Pure/import closure — отдельный положительный source вывод

Pure fixture импортирует только9exports из `ops/docs_tests.ts`; helper не
импортирует native driver/Python/git/process, не имеет top-level env/process/
filesystem/network calls. Его exact hash и current230 fixture неизменны.
Fixture registers manufactured Deno.test closures; runtime/FS wrappers не
конструируются при module import. Отдельный later pure GREEN не проверяет
и не авторизует native path. Никаких actual registrations/tests этим review
не наблюдалось.

Driver imports helper→none и git→process; top-level создаёт TextEncoder/Map,
workspace URL string, functions/types. CLI entry guarded by import.meta.main.
Native Python имеет только finite stdlib imports, constant tuples/maps,
functions/classes; main guarded by __name__. Никаких discovered dynamic imports
в production source. Этот source import-safety вывод не доказывает исполнение
чужого runtime/stdlib closure или actual bootstrap isolation.

## Сопоставление с авторским failure list

Все9авторских gaps подтверждаются в owning source. Дополнительно конкретизированы
двухфазный parent channel conflict, KaTeX self-SHA fixed point,444command
over-reservation,544read counter failure и потеря raw после reaped exception.
R8 native Step translation по inspected routes соответствует D2 args/maps;
base использует parent snapshot, dedicated maps не расширены. Это source
candidate, пока exact snapshot authority, protocol/schema и closure не закрыты.
Новые findings не требуют нового public/private архитектурного решения:
D4/D5/D6 уже задают desired behavior.

## Наименьший конечный ready-contract I2C

Один source-only writer в тех же **четырёх** I2B owning files, затем STOP для
high CPP. Не трогать pure helper/230fixture, public schema/exact12, source16
paths, component/server/platform/CP, original reports/patches/RED и gitlinks.
Не тратить execution slot ради диагностики очевидных source defects.

Завершённые deliverables в порядке зависимостей:

1. Native exact schemas/parent attachment/AuditIntent/readers без self-ref,
   full expected ACK/capsule/inventory binding. Existing trusted lease получает
   exact producer stream/status/participant evidence API; это concrete source
   adapter существующего parent, не новый trust source или server installation.
2. Один parent control dispatcher+phase ledger+gated launch; preflight→check
   дважды корректно проходят existing frames. Реализовать final setup positive
   predicate, producer proof и parent-owned fallback с D6 scope separation.
   Нельзя просто заменить failed на complete или прочитать process.wait exit0.
3. Shared reservation/actual-debit ledger и explicit phase/snapshot/source
   schedule: preflight100, full444 до added failure reserve; counters per-phase,
   storage/deadline global; byte-based blobs и terminal source failure retention.
   Полный actual envelope fit до dispatch, без изменения caps.
4. Замкнуть command/driver first-fork exception cleanup, raw EOF/hash/size/partial
   ledger на всех outcomes, finite per-op readers/tickets/chunks и rejected
   finish-validation/D6 finalization. Parent fallback должен работать и после
   reaped supervisor. Никакого synthetic stderr_eof или lost-capture→absent.
5. До соответствующих production fixes добавить paired source controls C1–C8
   в существующие two DEV fixtures: healthy complete route и каждый failure
   с no-forbidden-dispatch/retained-evidence checks. Два nominal counts/hashes
   заморозить заново; не запускать imports/parser/compiler/tests в I2C.

I2C source acceptance = обычный complete reachable healthy route при valid
trusted handoff + source controls всех critical refusal/retention paths +
immutable report/identity/complete patch/owning manifest/full byte-and-call
schedule. Actual runtime/credentials/delegation могут отсутствовать — тогда
конкретный native attempt blocked, source route всё равно обязан быть полным.
Если один конечный проход не завершён, сохранить partial result/remaining exact
locators и STOP, без автоматических повторов и без следующего D-only отказа.
Root задаёт finite source envelope; разумный ceiling40min/8MiB reads/1CPU/1GiB,
output≤256KiB — предложение, не исполнение этого review.

Только после corrected source CPP отдельно разрешаются compiler-only/native
DEV plans. Pure current230 — независимый доступный later gate; final clean
committed HEAD/blob binding, kernel/tool/native acceptance и final CI/science
остаются отдельными и не наследуются от source audit.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Pure contract/230 import closure сохранены | Exact676a…/f02f…; only helper fixture import | Не исполнено; native ничего не доказывает | сохранить |
| Producer больше не unconditional refusal | setup1323–1405→run_phase1121–1181 | Healthy final setup всё ещё always failed | изменить |
| Две фазы проходят parent handoff | phase-ready1389 vs bind1192–1199 | Нет control dispatcher/await_phase | изменить |
| Full native route fits budgets | cap reservations662/867 и counters838 |111MiB/62.4375MiB reserve;544cumulative calls | изменить |
| Failure originals гарантированно представлены | run_phase pretry, constructor/capture exception paths | Files могут остаться без authoritative refs | изменить |
| Native8+8/READY подтверждены | Только source declarations;execution0 | Matrix иimplementation incomplete | данных недостаточно |

Read-only audit <3MiB conservative content charges (<8MiB); CPU/RSS/physical
I/O не измерены. Parser/compiler/lint/format/import/tests/runtime/native/network/
server/build/solver/CI=0; source/fixture/CP/index writes=0. STOP для Root I2C.
