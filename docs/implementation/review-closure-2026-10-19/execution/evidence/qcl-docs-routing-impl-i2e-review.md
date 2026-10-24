# I2E: независимый high CPP, narrow boundary1 residue + boundary2

**Вердикт: CHANGES_REQUIRED, whole native candidate не READY.** В I2E закрыты
конкретные прежние дефекты coercing enum, mock-retention shortcut и отсутствия
owning durable publisher. Boundary2 ещё не является total failure-safe lifecycle.
Ниже даны конечные implementation/fixture tickets; новый общий design цикл не
нужен. D4/D5/D6 остаются authority, все прежние незакрытые R1–R9 сохраняются.

Это source review actual guards/callers/fixture bodies, затем сопоставление с
author report. Target imports, scripts, parser/compiler/lint/tests/Deno/native/
network/server/CI/science не исполнялись. Static positive/negative walkthrough
не является observed test result. Product calls этим review не разрешаются.
Счётчики Root из поручения: product87/source7/CI0/science0/nativebuild0; review
не добавляет product/runtime calls и не меняет чужие counters/checkpoints.

## Frozen identity и граница проверки

Worktree `/tmp/qcl-docs-test-routing-worktree`, actual HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`. Это overlay, не committed native16
closure. Git status: modified `.github/workflows/ci.yml`,
`.github/workflows/release.yml`, `deno.json`, `ops/ci.ts`, `ops/git.ts`;
untracked `ops/docs_tests.ts`, `ops/docs_tests_cli.ts`, `ops/docs_tests_native.py`,
`tests/docs_test_native_protocol_test.ts`, `tests/docs_test_routing_test.ts`,
`tests/test_docs_test_native.py`. Восемь gitlinks uninitialized, не обновлялись.
Source/fixtures/CP/index не редактировались; созданы только этот review и identity.

| Frozen artifact/path | SHA256 |
| --- | --- |
| I2E report | `7d7fa3bc3a265da8c00dee17b5358996ae1e79f5ae4869dc9d433624a21fa2d4` |
| I2E identity | `569fd093509c4d388b51c4be40bd82b502b3e212ee43a63b924892b6232a194a` |
| I2D→I2E complete four-file delta,98658B | `1ce20122993d7868189332ff3f4dd8252937c1f8f62c5fc860dc7a0a8c46ac4a` |
| `ops/docs_tests_native.py` | `86d041a368ef6eb1607c2a92dfa58cb9d17e7f605e53d22505e43465a49d3d97` |
| `ops/docs_tests_cli.ts` | `70a28e1922352732e1484820df81eb0420021ff7c119aea05e37252c2843d798` |
| `tests/test_docs_test_native.py` | `25e6e9dfc6838238c892d65b4a221d2a18cb8a6a2e90fd6d6aa6eb6094667eb4` |
| `tests/docs_test_native_protocol_test.ts` | `eea4109924d857edeb5a12c4e5751c89759a007070cebc06d7d175e2af097110` |
| Prior I2D high review, preserved | `8a666cf1d9771aab53ce9fecc156faae2b139ce60cc4a9875ec9056f6f1f1916` |

D4 `24a7d68b612e7d3dc437404bb805df777ede1f5159c0bff39eca7d693ebe8fc0`,
D5 `6049f427a10c769b69c2beaaa1374e583d217d6eb68926337204e560b824ed48`,
D6 `80509e2b9fc8725a6309733c6857a75657a640addcc7047e5199d21002ddbcc6`.
Ранее принятые queued-phase/self-ref/counter-loop corrections не открываются
повторно; это не наследование whole source/runtime PASS.

Внешние pure dependencies actual hashes остаются
`68f0efb5b45a03f130a52d14279e427c83c11b317a3c244e43375dbac5b8d3f5`
(`ops/docs_tests.ts`) и
`2639be2132a88adb3e1ccd204112180efa065089e9ade5cae87e38c970952f99`
(`tests/docs_test_routing_test.ts`). Root FORMAT + две approved comments не
приписываются I2E. Их behavior/format/lint здесь заново не принимается. Старые
pure hashes676/f02 и прежняя native16 closure не переносятся на новые bytes.
CHECK1 unsupported cached-only failure сохранён как отдельный факт; v7 CLI
preparation не равна compiler/native acceptance. Следующий execution требует
actual Root binding текущих bytes и отдельного finite grant.

## Подтверждённые узкие закрытия

Все локаторы в таблице относятся к четырём frozen paths, строки actual I2E.

| Поддефект | Actual owning guard / fixture | Вывод и предел |
| --- | --- | --- |
| `String(value)` расширял enum до array/object | TS25–26 `typeof string`; responseFor68,76–77; metadata58; stdio247/271. Deno fixture59–64 содержит array/object/number/null отрицательные пары | Этот coercion устранён. Оставшиеся String при hydration111/capture199 и Error83 не являются enum membership; response reader вызывается до них. Не заявляется полная malformed-response matrix |
| Parent registration почти не имела nested schema | Python236–291 exact maps/6-tuples, typed bool/int/numeric caps, bounded manifests/env/initial/allocation/admission; actual callers1149 и2266 до construction/spawn | Сама переданная registration существенно замкнута. Это не закрывает отдельное чтение actual retained records: R3 ниже |
| Wrong phase order/scope | Python1371–1381 требует one target либо preflight→target по scope до authorizer/spawn | Actual request guard есть; dedicated positive/negative fixture matrix ещё нужна |
| Retention fixture подменяла predicate готовым status | Python fixture270–309 вызывает actual validate_phase_retention и validate_terminal; low-level artifact reader проверяет bytes/SHA/cap. Proof entries создаёт actual publish_bytes через fake handles. Faults index/binding/raw SHA/size/reap/proof-set | Прежний mock-retention shortcut устранён. Observed results отсутствуют; low-level memory handles не доказывают физическую durability |
| Finish-first fixture обходила legal wire state | Python fixture325–330 теперь preflight1→finish2 и actual allowed_ops; run_phase вызван339–340. Retention и terminal validators не заменены | Прежний shortcut исправлен. bind/source metadata/report providers ещё injected; это isolated finalization, не full C8 |
| Не было native owning publication proof | Python1008–1038 full write/size→file fsync→exclusive no-replace link→dir fsync→unlink pending→dir fsync→close; только затем add proof. publish_closed_raw1045–1074 аналогично после owner closure. Fixtures242–257: short write/file sync/link/dir sync faults и collision, сохранение originals | Source implementation publisher имеется; ref возвращается только после успешной последовательности. Не нужны self-SHA поля. Физический crash/storage runtime не измерен |
| Driver raw отсутствовал в retention proof | Driver stdout/stderr частичные originals1577–1583; EOF/reap closure1737–1750; actual raw publication1746–1747. Retention1483–1490 перечитывает driver streams и1521 требует proof tuples | Этот manifest omission закрыт. Budget/domain accounting и все failure paths ещё не закрыты |
| Positive final phase/setup publication была только label | Phase1971→1972 и final setup2158→2159 возвращают ref после owning publisher; publication failure не возвращает ref. Phase guard1968–1970 и producer guard2153–2155 не повышают unknown в positive | Self-publication fixed point не введён. Parent producer manifest ещё требует R4 |
| Первые socket/pipe/fork failures выпадали из finally | execute_bounded909–917 allocation внутри try, finally977–1005; fixture66–79 проверяет три pre-fork failures и created handle closure. Driver defaults1563–1570 перед initialize | Это подмножество закрыто. Post-fork birth/pidfd/attach и secondary cleanup failures не покрыты, R1 |
| Inherited FD≥4096 переживал driver exec | Actual census1119–1129, driver call1601; fixture80–85 содержит FD65537 | Старый4095 cap устранён на driver exec path. На private worker fork helper пока не вызывается, R2 |
| Потеря доставки требовала переписать positive phase | run_phase appends original ref1972 до delivery2420–2421; parent closing2020–2028 принимает actual original record, setup close_reason failure2423–2424 запрещает complete | Immutable positive phase сохраняется. Dedicated delivery-loss control ещё нужен; это не повторное открытие queued-phase fix |

Native import-safe граница по просмотренному source сохранена: Python module
top level содержит stdlib imports/constants/functions/classes; process/proc/env/
broker work внутри вызовов, main guarded. TS CLI actual stdio main guarded278;
injected sourceGraph path остаётся через broker reader, `ops/git.ts` main guarded,
`ops/process.ts` run не вызывается при import. Это source observation, target
import/permissionless runtime не выполнялся.

## Блокирующие остатки и наименьшие code tickets

### I2E-R1 — P1: worker и post-fork owner ещё не имеют total settlement

Локаторы: `ops/docs_tests_native.py:854–901`, `:927–929`, `:977–1005`,
`:1240–1258`, `:1731–1735`, `:2101–2113`.

В worker единый try858–876 содержит TERM, drain, writes и последующий KILL/reap.
Если `write_all`866–867, `os.read`862 или owner observe/reap бросит исключение,
переход в except877 пропускает оставшиеся KILL/reap. Это реальный control-flow
gap, хотя capture_complete становится false и positive блокируется. После
этого raw reread889–898 ловит только UnicodeError: OSError/Refusal может
прервать ended_at/write_frame, не оставить terminal failure frame и заменить
первичный failure вторичным. Даже первый except854 сохраняет только generic
`command_owner_failure`, без bounded primary stage/error identity. Selector.close
не закрывает сами зарегистрированные stdout/stderr file objects; требуются
независимые close attempts всех process pipes.

В parent `proc_birth`/pidfd_open927–928 могут упасть после fork. Finally ждёт
ребёнка только если pidfd уже получен982: закрытый dispatch gate запрещает
command launch, но direct child terminal/reap не установлен. При ошибке сигнала/
wait вне ProcessLookupError984–989 finally также может пропустить fallback и
остальные close attempts. В Active.command finally первый partial/stat/commit
failure может прервать settlement другого reservation и заслонить первичный
execute error. В Driver.close adopted waitpid1733 ловит только ChildProcessError;
другая failure уходит в outer catch до последующих stages. Parent fallback
readback2104 расположен вне своего retention try2110, поэтому повреждённый
старый phase ref может сорвать и fallback publication.

**Следующий ticket B2a, тот же owner Python+fixture:** хранить bounded primary
failure и отдельные secondary stage failures; независимо пытаться TERM, drain,
KILL owned descendants, reap, close pipes/Fds, settle каждый reservation,
retain partial manifest/fallback. Ни одна secondary failure не должна выключать
остальные доступные cleanup stages. Не убивать sole subreaper с незакрытыми
descendants; existing outer watchdog отвечает за неизвестную ownership. При
fork-success/pidfd-failure закрыть gate и установить bounded wait/reap либо
явно передать pinned identity existing outer owner; unknown никогда не pass.

Fixture acceptance: injected birth/pidfd/attach failure после fork, partial raw
write→drain write error, owner observe/signal/reap error, raw reread/frame error,
stat/commit/release/fallback error. Проверить primary сохранён, каждый созданный
FD получил close attempt, доступные последующие cleanup stages вызваны,
partial files/index entries сохранены, no forbidden dispatch, result unknown/
failed. Это fake OS/process matrix; реальные процессы не нужны для code ticket.

### I2E-R2 — P1: FD census закрывает driver exec, но не private supervisor fork

Локаторы: `ops/docs_tests_native.py:917–921`, `:1119–1129`, `:1601`, `:2354`.

Fork child закрывает только parent side нового socketpair и write_gate. Он
наследует producer parent-control, broker/listener/accepted-client, leader
pidfds и прочие FDs; `_capture_worker` их не закрывает. `close_fds=True`821
защищает только будущий command exec. `set_inheritable(control_fd,False)`2354
тоже действует на exec, не fork. Поэтому private supervisor удерживает чужие
control/authority FDs и может задержать EOF при аварии producer. Census helper
существует, но вызывается только в другом driver path.

**Ticket B2b:** в fork-child до worker ownership/dispatch закрывать actual
inherited set, сохранив только exact channel/gate/stdio для этого owner; после
чтения закрывать gate. Не передавать capability/control FDs в private owner.
Fixture должен пройти actual fork-child setup seam, иметь FD>4095 и специально
producer/broker FDs; утверждать exact keep set и их closure до gate/command.
Нынешний isolated helper fixture80–85 этого caller defect не ловит.

### I2E-R3 — P1 schema residue: typed registration не типизирует actual JSON

Локаторы: `ops/docs_tests_native.py:1171–1181`, `:1289–1294`, `:1796–1800`,
`:2205–2208`. Смежные readers `:671–683`, `:1309–1312`.

Переданная parent registration проверяется236–291, но actual persisted
initial/allocation/admission повторно проходит главным образом Python `==` и
частичные exact checks. В Python `False == 0`, `True == 1`, `1.0 == 1`.
Static reproducible case: зарегистрирован typed initial populated0, а actual
retained JSON populated:false;1172 принимает их равными. Аналогично actual
allocation.limits.cpu:true сравним с registered1 на1179/1181. Actual admission
limits могут содержать bool/float вместо registered int и пройти1293; позже
TS reader может отказать, но native actual normative schema уже не замкнута.
Accepted finish-validation.binding2208 сравнивается с typed expected binding,
но сам decoded binding не проходит validate_binding: version:true совпадёт с1.
SHA подтверждает bytes файла; он не устраняет эту разницу типов между bytes
и projected registration. Это не демонстрация caller authorization bypass.

**Ticket B1r:** переиспользовать одни typed nested record validators для
registration и каждого actual decoded artifact до equality/use; для exact
binding сравнивать validated canonical values/bytes. Не заменять это blanket
coercion. Добавить actual reader pairs: initial false/0; allocation cpu true/1;
admission limits true/1 и1.0/1; accepted validation binding version true/1;
positive exact records. Fakes подменяют только storage read, не validator.
Дополнить actual setup ACK/version/PID/phase-list typed reader и malformed
phase/setup response matrix, не полагаться на отдельные `==` guards.

### I2E-R4 — P1: producer terminal streams и retained stream evidence не связаны

Локаторы: `ops/docs_tests_native.py:2129–2155`, особенно2133–2138 и2152–2153;
`validate_terminal:2173–2180` проверяет typed closure stream map, но не raw bytes.

Parent читает producer_closure из terminal closure ref, затем независимо
перечитывает `evidence.streams`, не требуя equality этих двух stream maps.
Durability tuple list2152 содержит closure_ref и refs только из второго map.
Таким образом adapter defect может вернуть valid closure со stream refs A и
valid durable evidence map B; actual A не перечитаны и их proof tuples не
нужны, а producer_durable может стать true. Static counterexample не требует
поддельного grant: это несогласованность результатов existing trusted adapter,
которую promised independent readback сейчас пропускает.

**Ticket B2c:** validate_streams(evidence.streams) с producer caps, exact equality
с producer_closure.streams, actual read/hash/byte count и publisher proof для
того же exact set. Для participant terminals определить в existing adapter
тот же complete original/closure evidence и проверить transitive retained refs;
не считать label retention_status самостоятельным proof. Пары: одинаковый
actual manifest→допустимый positive predicate; разные maps, missing raw/ref,
false raw_complete, missing proof→unknown/failed; producer и каждый participant
identity/closure mismatch→failed. Phase/setup receipts сами публикуются затем,
без собственных будущих SHA полей и без переписывания старого positive phase.

Opaque external provider не становится repo implementation от этого review.
Для actual BIND он должен существовать в trusted parent и выполнить gated
spawn, runtime closure verification, partial-spawn ownership/watchdog, complete
participant collection и actual owning publication. JSON/booleans/manual set
population запрещены. Отсутствие provider/inventory/allocation — later runtime
blocker; оно не отменяет перечисленные конкретные repo guard fixes и не требует
нового broker/cgroup/trust architecture.

## Boundary3 и boundary4: точные следующие implementation boundaries

Это сохранённые отдельные tickets, не условие снова обсуждать D4/D5/D6.

1. **B3 schedule/debits:** `git_read1268–1275` увеличивает calls до command,
   но raw/time/snapshot debit только после успешного return. Failed actual
   bytes/time должны учитываться в finally. `run_phase1899–1905` считает groups
   of36 allowed reads, но не проверяет exact next root/argv slot. Требуются
   native-owned ordinal schedule и конфигурационная source identity/race
   binding, не только family allowlist. Полный trace сохраняет100/444 normal
   calls,16 failure reserve,512/8MiB/60s per phase; global storage не reset.
2. **B3 новый protocol-original debit:** `DriverPipe1580–1583` всегда выбирает
   stdout path в raw_root, но при domain protocol резервирует/commits в protocol.
   При нескольких domains физическая запись и charged domain расходятся.
   `admit_source_schedule1417–1420` ещё не включает оба possible24MiB driver
   stdout originals в полный physical-domain/global trace. Исправить actual
   path↔domain binding и finite upper trace до первого driver fork; grant/caps
   не увеличивать. Если existing allocation не вмещает выбранную retention,
   отказ до child честный, но healthy route не объявлять доказанным. Trace
   включает pending hard-link aliases, failed pending publications, metadata,
   cleanup/fallback, driver/producer raw, protocol bytes и sample history.
3. **B3 source truthfulness:** `source_validated1938` пока связан с успешным
   full finish/report validation. Safe false-positive исправлен ранее; failed
   unit report ещё может скрыть измеренный source как not_measured. Разделить
   independent source measurement criterion и unit result. Не возвращать
   прежний ref-exists⇒measured shortcut.
4. **B4/C8:** сохранить номинальные8 Python methods +8 Deno registrations,
   добавить manufactured existing-lease/process/pidfd/cgroup fixtures actual
   factory→broker→driver→execute→D6 finalizer. Нужны legal preflight→check и
   direct docs, hello/token/peer/ancestry/expiry отказ, exact dispatch order,
   failed source/unit capture, drains/publisher/cancel/ACK/late delivery loss,
   setup producer+all participants EOF/reap и outer whole-empty. Проверки B1r/
   B2a/b/c входят в этот finite acceptance matrix; сохраняются actual validators.
   После source review — отдельно разрешённые finite DEV8+8 и compiler checks.
   Nominal count без execution/coverage не означает native READY.

Рабочий порядок для sole medium writer: B1r+B2a/B2b/B2c как один ограниченный
boundary2 correction packet; fresh CPP на exact four-file manifest; затем B3
и B4 в отдельных конечных packets. Ошибка primary artifact остаётся retained,
новая attempt identity не стирает предыдущие failed logs. Не нужен perpetual
design-only отказ и не разрешены новые runtime calls этим source review.

## Ledger и итог решений

Начало review08:49:20UTC, конечный budget12min,1CPU,1GiB, read≤5MiB,
output≤128KiB. Review artifacts суммарно менее32KiB, но повторные source text
selections в tool responses превысили128KiB; совокупный точный byte counter
tool output не снимался. Это отклонение output budget; соблюдение этого cap
для всех transcript outputs не заявляется. Conservative content/hash read
upper bound3MiB; CPU/RSS/physical I/O не измерены. Использованы source text/hash/Git identity reads; no target
code execution. Historical artifacts сохранены. Окончательный review SHA и
exact manifest находятся в companion identity.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Enum coercion и mock-retention shortcut устранены | TS25/68/76–77; Python fixture270–309/325–340 | source-only, DEV не исполнялся | сохранить |
| Owning no-replace file+dir publisher реализован | Python1008–1074; callers969/1219/1746/2158; fixture242–257 | physical crash/provider не проверялись | сохранить |
| Total command/driver/error cleanup замкнут | R1/R2 точные control-flow gaps | positive обычно fail-closed, но cleanup/provenance недостаточны | изменить |
| Все actual nested schemas и producer manifests замкнуты | R3/R4 | registration/helper closure не заменяет actual reader validation | изменить |
| Full schedule/raw/metadata budgets и C8 доказаны | B3/B4 remain, actual path/domain mismatch1580–1583 | no full trace/DEV/native execution | изменить |
| External trusted provider actual BIND получен | только required adapter interface/guards | provider/runtime inventory/allocation здесь не измерены | данных недостаточно |
| Whole native source/runtime/CI/science acceptance получена | CHANGES_REQUIRED, execution0 | source gate ≠ source build ≠ native ≠ scientific gate | данных недостаточно |
