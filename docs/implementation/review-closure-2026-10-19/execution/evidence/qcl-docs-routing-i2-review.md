# I2: независимый source review и конечный scope I2B

Вердикт: **CHANGES REQUIRED; I2 partial, native source integration не готова.**
Pure API и native integration оценены отдельно. Заявление автора о девяти
source gaps подтверждено; отсутствие live wrapper/credentials не объясняет
отсутствующие broker, readers, state machine и retention. Новый запуск сейчас
не нужен для установления этих дефектов. Этот review ничего не исполняет и
не разрешает DEV/native/CI/science.

## Неизменяемые входы и граница доказательства

Selected `/tmp/qcl-docs-test-routing-worktree` HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`, branch из I2 identity
`codex/review-closure-docs-test-routing`. Фактический status: пять tracked edits
(`deno.json`, `ops/ci.ts`, `ops/git.ts`, два workflows), шесть untracked source
files (`docs_tests.ts`, `docs_tests_cli.ts`, `docs_tests_native.py`, три fixtures).
Все восемь submodules uninitialized; их gitlinks прочитаны, не менялись.
Основной workspace имеет другой HEAD `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`
и dirty docs; он не использован как источник I2. Архитектура и selected AGENTS
прочитаны. Ни исходники, ни checkpoint не изменены.

Проверенные SHA256:

| Вход | SHA256 |
| --- | --- |
| D4 | `24a7d68b612e7d3dc437404bb805df777ede1f5159c0bff39eca7d693ebe8fc0` |
| D4 review | `ca5a8d36b04ff6e5f52817da420b6fb3ca92e95d9e70e45c1ea6f44f74b9fb48` |
| I2 report | `16a9d55592ffd9d9f3a5bfee295c4c2234608668a665eff18ad2d5721921c769` |
| I2 identity | `4b55bcc45c097c7afe887db031dfdc10851759677d8dd1c8fad6fb53293dbf54` |
| I2 complete patch | `55da25d0b259014a57c1508b980187a7aad152a418c380b4407559fc898be729` |
| Pure helper | `676a3db1a4de455bbd73a46e57f316b4ae7721e631aa3b7d81a2da8564340d8c` |
| Current pure fixture | `f02f541d633c56280077701ba9fbee3928ae7c2e055cae8b2e78d759bd3a9761` |
| Native Python | `4f87e4abd2ab06ecc4873f7eca4f66f37cb5f524df1b55ba52ddc53b4444e77f` |
| Driver | `e4349103a43e4050c6ae4bf28d4fc7d8d5dc8e3ad7f51cc57b6c3472db9a5832` |

Все 16 actual production source hashes и два new DEV fixture hashes сверены
с I2 identity. Patch проверен по SHA, заголовкам и соответствующим actual
source sections; его применение не выполнялось. D3 retained/source contracts
прочитаны дополнительно. Runtime/parser/compiler/lint/format/import/tests/
native/network/server/build/solver/CI=0. Чтение и хеширование файлов — source
audit, а не запуск target code. Консервативно прочитано <2MiB (<8MiB cap);
CPU/RSS/physical I/O не измерены. Субагенты не привлекались.

Далее locators относительны selected worktree; commit выше плюс приведённые
SHA задают overlay, поскольку новых committed blobs ещё нет.

## Pure API: что можно сохранить

`ops/docs_tests.ts:322–367` теперь сохраняет receipts при initial/per-child/final
`sourceGraph()` rejection, помечает `not_measured`, запрещает aggregate pass.
Это соответствует D3 retention rule. Дополнительные step plan/runtime/input/
source identities полезны, но SHA строк после UTF8 encoding не заменяет SHA
native raw bytes при invalid UTF8 или partial write.

Exact textual diff historic fixture `04589b3993e51885b2abc08cb516c7a6467709e3d278c593874c598ecaa9ecf3`
→ current показывает ровно две nonnull guards и три appended registrations
(`tests/docs_test_routing_test.ts:857–883`). Старые assertions не удалены и
не ослаблены. Поэтому mapping **227 ancestral +3 sourceGraph cases =230 nominal**
приемлем на source уровне. Это не observed230, не перенос исторического RED
на новые bytes и не расход sole GREEN.

`ops/git.ts:44–86` последовательно использует injected `readGit`; import
`process.ts` не запускает process, default `git()` здесь не выбирается driver.
`docs_tests_cli.ts:48–52` явно передаёт broker reader. Прямого `.output()`/
`communicate()`/`readAll()` в driver/native source нет. Default Git остаётся
в owning API для старых consumers. `ops/ci.ts:8,118` и workflow graph steps
по-прежнему относятся к общему full workflow, а не доказывают bounded native
docs adapter: не следует расширять claim на весь job.

## Блокирующие findings

### R1 — работающий admission→broker→executor путь отсутствует (P1)

`ops/docs_tests_native.py:694–708` всегда возвращает
`source-incomplete-active-factory-and-broker`. Нет `ActiveDocsAttempt`,
`bind_native_context`, broker accept loop, native driver launcher, независимого
native plan/index validation и native prepare/execute/finish owner. Constructor
`:622–658` проверяет несколько полей и делегирует неизвестному external object;
его ACK predicate `:656–657` связывает только kind/nonce/pid/birth, не весь
scope/source/input/runtime/deadline binding D4. `RunningDocsSetup` имеет только
cancel, нет completion ACK/finalization и task leader pinning API.

Отсутствие actual trusted external parent — допустимый отдельный runtime
prerequisite. Отсутствие перечисленного source кода — дефект реализации.
Исправление: реализовать замкнутый route с одной live фазой в работе,
SO_PEERCRED/UID/birth/ancestry/leader binding, consumed-before-dispatch gate,
nonce+source/input/runtime ACK и parent EOF/cancel terminal retention.

### R2 — потеря cleanup/retention при ошибках capture (P1)

`native.py:571–575` блокируется в frame read; cancel/EOF проверяется только
перед gate и после полного frame. Timeout/debit failure/frame refusal уходит
в `finally :590–598`, где SIGKILL получает supervisor, но parent не доказывает
закрытие его descendants, не вызывает `close_and_verify_empty`, не reap-ит
supervisor на этом пути. Именно в timeout/error сценарии может быть уничтожен
единственный subreaper до cleanup. Дополнительно `proc_birth/pidfd_open :562–563`
выполняются до `try`, так что их отказ оставляет fork/gate/FD вне cleanup.

`:587` возвращает caller-provided `receipt_ref`, хотя exclusive durable receipt
с actual SHA здесь вообще не создан; `:585–587` не может сделать это evidence
посредством synthetic booleans. В worker `:499–500` partial file write может
успеть записать prefix до исключения, но memory stream ещё не обновлён; затем
transport/string metadata не описывает actual retained bytes. При ошибке
`write_frame :540` parent теряет result; parent fallback receipt отсутствует.
Не объявляю, что raw обязательно удаляются: они могут остаться на диске, но
не существует обязательного durable, source-bound terminal указателя на них.

Исправление: единый guarded lifecycle с самого fork, nonblocking multiplex
status/cancel/deadline, independent parent fallback, продолжаемые bounded drain
и TERM→KILL cleanup, terminal-empty+wait/reap, durable partial raw byte hashes/
sizes/observed-discarded where known и typed cleanup-unknown. Не отправлять
`complete` до всех этих gates. Числовые `time.time()` в `:469,539` надо
проецировать в agreed ISO UTC для pure Capture (`docs_tests.ts:347`).

### R3 — plaintext phase tokens попадают в durable intent API (P1)

`native.py:642–649`: `frame` содержит `tokens`, и тот же объект передаётся как
`durable_intent=frame`. D4 прямо запрещает сохранять tokens в raw/log/receipt.
Даже при доверенном parent API нельзя передавать ему intended-for-persistence
secret-bearing объект и рассчитывать на недокументированную redaction.
Разделить startup transport и audit intent до `spawn_gated`: в audit только
token hashes и необходимые binding fields. Fake spy должен проверять отсутствие
сырых tokens/nonce-sensitive transport data во всех persisted/log projections.

### R4 — протокол не замкнут и не переносит допустимый aggregate (P1)

`docs_tests_cli.ts:90–99` ограничивает finish frame131072B, но aggregate несёт
все full stdout/stderr captures (до4MiB raw total, JSON ещё больше).
Корректный child с output >128KiB приводит к terminal transport failure.
`brokerReadGit :35` допускает262144B decoded text, stdio read для git-result
`:97` ограничен131072B ещё до JSON escaping. Это bound-refusal, а не memory
bypass; однако successful full envelope не реализован. Нельзя молча увеличить
лимит без общей storage/frame accounting.

Start `:95–96` и response readers `:33–35,42,59,66` не проверяют exact key sets,
types/finite lengths/response union полностью; нет общего sequence и bounded
inactivity/deadline во driver protocol. Client `native.py:680–685` вводит
server-first challenge, отсутствующий в D4 hello contract. Client env имеет
ровно4 reads, но transport не сверяет полный accepted binding.

Исправление: сохранить D4 hello-first; server выбирает live record по token,
а attempt/source заполняются reviewed совместимым способом с явным contract
решением Root, если четырёх env fields объективно недостаточно. Текущий
challenge delta не принят этим review. До реализации зафиксировать exact
union, encoded limits и finite full aggregate transfer (например bounded
chunks с canonical reassembly в existing envelope, либо reviewed larger
finish bound, вычисленный от total cap). Hash refs не должны незаметно заменить
обязательные full pure captures. Native owner сохраняет originals независимо
от доставки aggregate/finish ACK.

### R5 — нет native source closure и Git budgets; валидатор меняет semantics (P1)

`native.py:24–30` — лишь список имён; `validate_git :183–192` не читает fixed16
HEAD blobs/working bytes и не считает snapshot/phase debit. Он выводит section
name из basename component `:189–190`, хотя owning `ops/git.ts:58–67` берёт
фактический `.gitmodules` section. Валидный section, отличный от basename,
будет отвергнут. Blob-reader fixed argv variants также отсутствуют.

`brokerReadGit :36` возвращает text без owning `.trimEnd()` semantics
(`ops/process.ts:24`); raw `rev-parse HEAD\n` нельзя передать прямо owning
regex. Native handler должен делать именно owning normalization после полного
capture/fatal decode; NUL `ls-tree -rz` сохраняется. Existing Deno fixture
подаёт уже stripped text и этого несовпадения не ловит.

Исправление: fixed16 HEAD/blob/SHA+working-byte reader, повторный полный
binding перед/после и перед child, exact source-root/section allowlist derived
из проверенных owning данных, clear Git env/fixed argv, ≤128/2MiB/20s snapshot,
≤512/8MiB/60s phase, ≤5s/262144B child. Actual clean восьмикомпонентный graph
требует36 Git reads (4 root+4×8); current full driver делает initial+run initial+
4post-step+terminal=7 snapshots, то есть252 reads до native closure extra reads.
Это ручной source schedule, не measurement: writer обязан посчитать весь
schedule включая closure/failures и зарезервировать final/cleanup budget.
No-exec review local Git config/attributes metadata path остаётся обязательным;
одни fsmonitor/hooks flags не доказывают его.

### R6 — storage reserve проверяется поздно, census allocation не bounded (P1)

`native.py:574` aggregate debit происходит после capture; `:499` raw writes
не резервируют общий remaining allowance до записи. Parent/worker после fork
имеют отдельные Python copies ledger state. `StorageLedger :255–287` не
валидирует disjoint canonical roots; `os.listdir :279` материализует весь
каталог до проверки next-loop node bound, поэтому65k bound не ограничивает
одну allocation. `samples` ограничены числом, но не суммарным serialized bytes.
Seed canonical comparison `:238–239` вычисляет expected тем же resolve и
не сверяет отдельный literal backing path; modes0700/0600 не проверены.

Исправление: один native owner account, reserve/debit до каждой owned raw/
metadata/transport записи, failure debit без refund, bounded iterator census
с count/deadline до накопления списка, disjoint roots и literal seed target/
mode checks. Sampled TMP stop сохраняется именно sampled; hard disk quota
не выдумывается. Состояние partial seed остаётся retained при отказе.

### R7 — reader/guard objects не создают native trust самостоятельно (P1)

`read_tool_observation :338–364` имеет полезную independent registration lookup,
whole-output parser и raw checks. Но отсутствуют producer/registration import
construction, exact runtime_closure ref/read/binding, KaTeX/count readers и
agreed UTC normalization; nested refs валидированы не все. `CgroupGuard :291–329`
проверяет некоторые exact controls, но не доказывает authority/delegation,
initial private-empty state или allocation expiry/control reserve; terminal-empty
метод нигде не подключён. Эти predicates должен заполнить active factory по
trusted parent handoff и owning admission, а не persisted booleans.

Исправление: actual bound readers+typed active context, explicit no-probe
preflight, immutable tool/runtime source refs, fresh independent registration;
initial authority/empty/membership/limits before gate и terminal-empty after.
Accepted observations допустимы без нового probe; отсутствующие records дают
blocked. Не устанавливать новый trust root и не обращаться к серверу ради
завершения source кода.

### R8 — base inheritance и native executor schema несовместимы (P1)

Pure `planChecks :274–287` создаёт Step.executable+args и base clearEnv=false.
Native worker `:478` ожидает отдельный command.argv и всегда env=command.env;
adapter преобразования отсутствует. При прямой передаче план не исполним;
при argv-only bridge base наследование теряется. D3 отдельно сохраняет base
explicit inherited environment. Dedicated units должны сохранить точные D2
maps; supervisor/client startup и Git env — свои exact maps, driver no script
grants. Это разные scopes. Исправить в независимом native validation/translation,
не меняя pure Step или расширяя dedicated permissions ради удобства.

### R9 — DEV fixtures проверяют малую часть acceptance matrix (P1 к READY)

`tests/test_docs_test_native.py` содержит8 методов, но нет healthy factory→fake
execute, pre-exec gate-order spy, fakeproc/pidfd/cgroup/storage-full/partial-drain/
parentEOF/cleanup-unknown/terminal retention controls. `tests/docs_test_native_protocol_test.ts`
имеет8 nominal registrations: framing, Git seam, preflight refusal, graph healthy
и3graph failures; не exercising driver complete prepare→execute→finish route.
Отсутствуют max-frame/binding/terminal delivery and completed-capture retention
pairs. Поэтому 8+8 — source inventory, не native coverage или pass.

## Триаж девяти авторских gaps

| Gap I2 | Класс и срочность | Source correction |
| --- | --- | --- |
| 1 active factory/broker | Native обязательный; блокирует route | R1+R3+R7 |
| 2 driver owner/state machine | Native обязательный | R1+R4+R8 |
| 3 closure/Git budget | Native обязательный | R5 |
| 4 retained readers | Native обязательный | R7 |
| 5 capture lifecycle | Native обязательный; originals/ownership | R2 |
| 6 storage/seed | Native обязательный; prewrite and exact topology | R6 |
| 7 cgroup authority/reserve | Native source predicates обязательны; actual delegation отдельный live prerequisite | R7+R2 |
| 8 protocol aggregate | Native обязательный; healthy max capture must terminate | R4 |
| 9 matrix | Source tests обязательны до DEV readiness; execution отдельно | R9 |

Ни один из9gaps не требует изменения exact12 public inputs, pure9exports,
D2 unit argv/maps, scientific model, platform gitlink или final CI.

## Конечное поручение I2B одному medium writer

Предлагаемый конечный scope для Root: **один source-only проход**, без нового
design цикла или автоматических retries. Только существующие Root owning
`ops/docs_tests_native.py`, `ops/docs_tests_cli.ts`, узкий `ops/git.ts` seam
и два native DEV fixtures. `deno.json`, ops-ci и workflows менять лишь если
нужна строго D4-compatible routing correction; чистый helper/230fixture
сохранять. Public schema/12sources/3tools, scientific code, server/platform,
исторические I1/I2/RED artifacts и CP запрещены к изменению.

Последовательные завершённые deliverables:

1. До edits зафиксировать exact protocol compatibility и finite encoded
   frame/aggregate budget; удалить unsupported challenge или явно вынести его
   как unresolved contract choice. Замкнуть active context/factory/broker и
   healthy path с injected external parent, не permanent refusal.
2. Реализовать readers/closure/Git ledger, independent exact plan translation,
   prepare seed/storage и driver launch без script grants. Все execution paths
   проходят через один owner/capture API; ни default Git, ни arbitrary exec.
3. Исправить R2/R3/R6/R7: pre-child durable redacted intent, workload gate/control
   reserve, parent multiplexed cancellation/fallback, raw byte retention,
   descendant closure и final receipt publication на success/failure.
4. Написать до соответствующих production fixes manufactured paired source
   controls D4 и выше; healthy fake route вызывает fake executor ровно1раз,
   каждый отказ фиксирует zero forbidden dispatches и retained evidence.
   Новые fixture counts/hash и matrix публиковать отдельно; historical227 и
   current230 не переписывать. Controls не запускаются в I2B.
5. Выпустить immutable I2B report+identity+complete patch, точные всех changed
   bytes hashes, explicit full native16 source closure, actual Git schedule,
   protocol size calculation, coverage mapping и remaining gaps. Root final
   commit/blob binding остаётся отдельным финальным source binding; null blobs
   не выдаются за committed source. Stop для независимого CPP.

Для конечности Root может ограничить этот проход40min wall,1CPU/1GiB,
≤8MiB source reads и≤256KiB report/identity/patch output; это предложение
envelope, не новое execution authorization. При нехватке времени сохранить
reviewable partial patch+exact remaining list и STOP, не открывать ещё один
автоматический цикл. Только после полного source CPP Root отдельно решает
два compiler-only checks, два D4 DEV calls и sole pure GREEN по своим finite
plans/attempt identities. Ни один из них здесь не выполнен/не зарезервирован.

Actual external trusted wrapper, immutable admitted runtimes/tool records,
live delegation/admission/storage reserve и будущие kernel evidence остаются
отдельными runtime gates. I2B не должен подделывать их ради source READY,
но должен иметь обычный исполнимый source path при валидном handoff.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Pure sourceGraph failures сохраняют accumulated captures | helper322–367;3new source controls | Не исполнялось; native raw отдельно | сохранить |
| Historic227 preserved, current230 justified | Exact textual ancestral diff,2guards+3registrations | Observed count неизвестен | сохранить |
| Driver вызывает owning graph только через injected reader | driver48–52;git44–86;import-safe process.ts | Native broker/limits отсутствуют | сохранить |
| Native integration соответствует D4 | Always-refused setup694–708;R1–R9 | Source, не server blocker | изменить |
| Capture/receipt сохранены при любых failures | Нет parent fallback/terminal-empty;R2 | On-disk prefixes возможны, durable mapping отсутствует | изменить |
| 8Python/8Deno доказывают READY | Малый source matrix;execution0 | Kernel/tool/peer evidence отсутствует | данных недостаточно |
| Дальше нужен немедленный runtime запуск | Defects воспроизводимы по source locators | DEV только после I2B+CPP+finite plan | изменить |
