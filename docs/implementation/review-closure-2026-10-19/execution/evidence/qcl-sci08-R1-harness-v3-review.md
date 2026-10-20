# SCI08-R1 v3 — independent focused source review bootstrap и finite replan

**Вердикт: PASS_SOURCE_HARNESS_BOOTSTRAP_REPLAN_ONLY.** Проверенная correction соответствует фактическому pinned `Test.jl`; новый explicit finite replan сохраняет consumed RED1 и ограничивает будущий scope corrected RED2 + conditional GREEN1. Новых блокирующих source findings в этом scope не найдено. Это не execution grant и не observed RED2/GREEN1.

| Frozen input | SHA256, перепроверен по bytes |
| --- | --- |
| `/tmp/qcl-sci08-R1-local-unit-run-v3.py` | `f239938d9fe83e60f1623ee501f4cd32e5d77fa071f931d237cd13973a123528` |
| `/tmp/qcl-sci08-R1-engineering-plan-v3.json` | `c48d28709fb75a66652d8ca7d884e55a1158c7e9e950b5e8aa0861525db3c13e` |
| `/tmp/qcl-sci08-R1-harness-report-v3.md` | `30ffdbc25af2deef560153b87710ca26188f26368c012b32b19554b643cd06ec` |
| `/tmp/qcl-sci08-R1-harness-identity-v3.json` | `a31304d9b69b4ac8030ac650f6c3957cabb0f16c282971e37e5c054cdd3362ef` |
| Pinned Julia1.13 Test.jl | `36bf481a76fd9aa3166cc69af165a10052893935da63e7456174f8e06f7a1d7e` |
| Original RED1 receipt | `8d638a5de2c52db561ad50152194b6033536c99a1e903a2684c92348d0e653df` |
| Original RED1 raw725B | `cd29bae7df710592bb53eb10085abe42277de704e0699f2475a1cf455e1c16ba` |

Owning Runner HEAD заново `fefaa27f194bfddf85dd51a0e255beef2218c06d`; status — три modified и два untracked выбранных fixture files. `git diff HEAD -- src` пуст; `git diff --check` без ошибок; recursive submodules пусты. Core HEAD `9f4a96d032ad868ec010ce92d915bb81087c8d92`, Core status пуст. Bound Root HEAD при чтении `c5ef91f4d11a93bd2cdcc9d0b6b18bba0df80ed0`; его поздний status уже содержит checkpoint/batch14 publication files, восемь actual gitlinks подтверждены read-only. Это текущая forensic metadata, не final READY и не parallel revision lock.

## Фактический RED1 и граница прежней review

Прочитанный original raw сначала печатает правильную `QCL_IMPORT_IDENTITY` с owned environment sibling paths для Runner и Core, затем `UndefVarError: push_testset not defined in Test` в bootstrap top-level. QCL_COUNTS отсутствует. Original receipt имеет target_calls1, attempt_consumed=true, exit1, counts=null, raw_capture_complete=true, unchanged sources,142 valid RSS observations/0unknown и wall7.421130432980135s. Это **STOP_RECONCILE_NO_RERUN**, не behavioral RED. Failed receipt/raw сохранены без изменения, их SHA совпадают с v3 frozen map.

Предыдущая focused source review B1/B2 пропустила obsolete push/pop API; оговорка «runtime не запускался» не устраняет этот пробел проверки совместимости. V3 проверяется непосредственно по pinned source всех используемых Test API. Не утверждается, что source review заменяет будущий observed runtime.

## Bootstrap: все используемые Test API прослежены

Pinned source расположен в bound Julia runtime `.../.build/julia/share/julia/stdlib/v1.13/Test/src/Test.jl`.

| Bootstrap API/поле | Первичный source locator и поведение |
| --- | --- |
| `Test.DefaultTestSet(...;verbose=true)` | Test.jl:1212–1259: struct, fields `results`, ctor verbose keyword, parent/default failfast |
| `Test.@with_testset ts begin ... end` | Test.jl:2115–2141: CURRENT_TESTSET/TESTSET_DEPTH scoped values; macro устанавливает current set и depth+1, затем scope восстанавливается; сам `finish` не вызывает |
| `Test.Error(:nontest_error, Expr(:tuple), err, Base.current_exceptions(), LineNumberNode(...), nothing)` | Test.jl:210–270: подходящий constructor с ExceptionStack/LineNumberNode/context; `nontest_error` сохраняет exception stack |
| `Test.record(ts, error)` | Test.jl:1283–1303: добавляет Error в results; Test.jl:41–43 задаёт failfast=false по умолчанию; fixed child environment не передаёт JULIA_TEST_FAILFAST |
| Child `record(parent_ts, ts)` | Test.jl:1325,1426–1440: child set прикрепляется к current parent при depth≠0 |
| `Test.get_test_counts(ts)` и восемь direct/cumulative fields | Test.jl:1510–1564: TestCounts fields и recursive aggregation child sets; суммы bootstrap не удваивают nested totals |
| `ts.results`, `x isa Test.DefaultTestSet` в `nsets` | Struct/record/count source выше: results хранит nested sets; рекурсия возвращает число всех nested DefaultTestSet, исключая созданный wrapper |
| `Test.finish(ts)` | Test.jl:1426–1460: одно завершение; outer depth0 печатает summary и бросает TestSetException при fail/error; child depth≠0 только прикрепляет set |

`format_duration(ts)` Test.jl:1598–1600 допускает time_end0 и возвращает пустую duration, поэтому count до единственного outer finish является поддержанным source path. Никакие удалённые push/pop вызовы в bootstrap v3 не остались.

Harness:27–49 создаёт ts, enters scoped context и вызывает тот же `Base.include(Main,f)` для exact selection. Fixture @testset входит в depth2, восстанавливает depth1 и прикрепляется к ts; ожидаемая failed assertion при failfast=false не прерывает include. После outer scoped context depth0 восстановлен. Тогда печатается ровно одна QCL_COUNTS строка и вызывается ровно один `Test.finish(ts)`. Ожидаемый RED fail бросает TestSetException до completion marker; GREEN без nonpass возвращается из finish и печатает completion marker.

Внешний catch:35–39 фиксирует необработанный include error как Error **до** counts. Ошибка внутри штатного child @testset уже записывается его macro и учитывается recursive count. Ни то ни другое не может удовлетворить ожидаемым errors0. InterruptException rethrow не создаёт behavioral RED; отсутствие expected counts/marker даёт STOP. Сам Error construction failure также оставит несовпадающий runtime outcome. Это source reasoning; API/parser/runtime в этой review не выполнялись.

## Assertions и конечный replan сохранены

Отдельный RED `c519b715…` и все пять fixture hashes заново совпали с v2. RED остаётся двумя existing `_checkpoint_storage_forecast` assertions: healthy literal16777728 и Bool→ArgumentError expectation; одно nested testset, nominal1pass/1fail/0error/0broken, expected exit1. GREEN остаётся349 nominal assertions,31 logical groups,33 nested sets и five includes; expected349/0/0/0, exit0 и completion marker. Source correction не меняет forecast API/physics, fixtures или expected counts. Production src остаётся baseline до observed corrected RED.

V3 `engineering_replan_id=SCI08-R1-BOOTSTRAPFIX-v3`, harness:148–157 и fixed exclusive folders разрешают только новое поручение **RED2** и оставшийся условный **GREEN1**, по одному будущему call каждого, максимум2 future calls/1200s total. Это не повторное использование RED1 slot: RED1 остаётся consumed в истории. Каждая будущая фаза600s,1CPU,2GiB sampled RSS,16MiB sampled TMP,1MiB admitted complete raw; early stop580s, CPU570/575s, terminal595s. Ceiling shared milestone81→88 отражён и в plan, и в READY predicate; Root owns reservation/counters. Этот source PASS сам не увеличивает budget и не создаёт grant. C08 exhausted8/8, science и CI не переоткрыты.

Original failed RED1 receipt/raw входят в frozen inputs обеих фаз и в before/prelaunch/after snapshot. Fresh READY обязан явно признать exact failed_red1_receipt_sha256, а новый receipt наследует prior_failed_RED1 object. GREEN использует только exact `/tmp/qcl-SCI08-R1-ENG-RED-2/receipt.json`: SHA из READY; проверяет id/phase, EXPECTED_BEHAVIORAL_RED, target_calls1, **тот же v3 executable_before**, old failed RED1 object и1/1/0/0/1 counts. Failed RED1 нельзя подставить вместо RED2. Root должен наблюсти corrected RED2, затем accepted medium I, independent CPP, actual O1/O2 traces и final349/31 до GREEN READY. Нет нового fallback/alias/autonomous rerun после любого failed corrected call.

## Fresh Root binding и сохранённые ограничения

Hardcoded Root HEAD constraint удалён. Harness:168–171 требует exact40 lowercase hex из fresh READY и равенство source_before.root_head. Before/prelaunch/after snapshots запрещают наблюдённый drift **в ходе** call. Publication может завершиться до READY; root_head_at_preparation — forensic only. Reviewed content hashes Project/Manifest, Runner/Core source, helpers, schema/tool/exact_cpu, fixtures, frozen plans/reviews и executable bytes остаются обязательны. Новая Root публикация сама не разрешает заменить эти bytes. Перед call Root должен завершить свои mutable CP/publication writes, иначе source equality штатно откажет.

Diff v2→v3 ограничен bootstrap, new finite attempt/replan, prior failure binding и late Root HEAD binding. B1/B2/finalizers v2 сохранены. Sampled RSS contract по-прежнему требует valid≥1; prior valid+later unknown может дать sampled PASS с честным unknown counter, это не fully fail-closed unknown==0 policy. Unknown никогда не подменяется нулём. Environment/offline-only остаётся Root-acknowledged trusted engineering предположением; OS filesystem/network enforcement, hard resident/disk quotas и native isolation не установлены. Prepared dependency/native caches доверенные, не заново доказанный замкнутый binary closure. Полный raw сохраняется normal capture path; fallback prefix всегда STOP. Best-effort terminal receipts не дают абсолютной гарантии при external guardian kill/FS/kernel hang. Runtime fit и научная приёмка из исходного import failure не следуют.

Выполнены только чтение/actual hashes/Git metadata/diff checks и просмотр точных pinned Test source ranges. Candidate/helper/parser/compiler/selftest/tests/import/Julia/Pkg/network/solver calls0. Root/CP/production/fixtures/Git writes0; созданы только этот report и review identity. Conservative logical read/hash/metadata charge менее1MiB из4MiB; physical I/O/CPU/RSS не измерялись. Source scope10min/1CPU/1GiB/report128KiB, без утверждений о measured peaks.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Исходный RED1 failed до assertions и consumed | Exact receipt/raw SHA, counts=null, UndefVarError | Не behavioral RED | сохранить |
| V3 Test context/catch/count/finish соответствуют pinned source | Test.jl actual hash и API table, single outer finish | Runtime/API compatibility ещё не наблюдалась | сохранить |
| RED2/GREEN1 — новый конечный scope, prior failure сохранён | Exact ids, frozen RED1, v3 predecessor, replan/ceiling88 predicate | Root отдельно выдаёт fresh READY/reservation | сохранить |
| Assertions/production scope не ослаблены | Unchanged six target hashes и empty src diff | Counts349/31 nominal до GREEN | сохранить |
| Fresh Root HEAD связан без obsolete hardcode | READY40hex + source snapshot equality | Root writes во время call дадут STOP | сохранить |
| RED2/GREEN1/native/science приёмка достигнуты | Новых target calls0 | Нет соответствующего runtime evidence | дополнительно измерить |

**STOP. Source approval относится только к exact v3 bootstrap/replan. Нужны отдельные fresh Root READY и finite shared reservation; новые runtime calls этой review не разрешены.**
