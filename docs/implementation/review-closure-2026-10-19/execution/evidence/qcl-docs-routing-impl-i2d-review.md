# I2D boundary 1 — independent narrow high CPP

**CHANGES REQUIRED для полного boundary1; подтверждены отдельные source fixes.**
Прежнее повышение failed source read до measured по наличию rejected ref
удалено. Retention больше не следует из driver exit: требуется actual native
index/raw/terminal ledger и publisher-owned durability proof. Нынешний publisher
такого proof не создаёт, поэтому positive phase намеренно blocked/unknown.
Это корректная dependency boundary2, а не новый source/native READY.

P1-E/C3/C7 ещё не закрыты: coercing TS enum checks допускают нестроковые
значения, nested native/receipt schemas частичны, а paired finalizer control
подменяет сам новый retention validator. Нужны точные небольшие продолжения
кода и fixtures; broad design-only цикл не требуется.

## Frozen inputs, scope и внешние pure edits

| Артефакт | Проверенный SHA256 |
| --- | --- |
| I2D report | `acafce8a10efd7c411f30508c046f67d328df2121234040ec089cb9a370551de` |
| I2D identity | `051f0779058c59a34eb810fac49e3a7741d67a9cb9e1a515f06fa84fdfc32505` |
| I2D67002B delta | `0ed917aaefeab58b04a661c6b2406f62a08846c669576d11576029794aee1c9b` |
| Сохранённый I2C high CPP | `caeb6ee6f85b19ba0fa2d748c1256aaac60c5497b829e70a1285cbe2f1f19a5f` |

Selected actual HEAD `2bb05d3651af4509fe7f02c1253b40f1e5146fec`,5tracked+
6untracked source files,8uninitialized прежних gitlinks. Cumulative I2C patch
этим delta не заменён. Review locators относительны
`/tmp/qcl-docs-test-routing-worktree`; source overlay задают hashes, не HEAD.

Четыре native owning files оставались frozen при повторном hash read:

| Path | SHA256 |
| --- | --- |
| `ops/docs_tests_native.py` | `547fb2149a40e1e768434813f114dff0b3c03f4e263d1b58e04c55e7979acccc` |
| `ops/docs_tests_cli.ts` | `dc9cf494e4be657e4722094ee823a1856494d7f5276149eb3a09f7940d76c9ca` |
| `tests/test_docs_test_native.py` | `4357a8d7f08d2ac45cfd376522b27b00d6424e716cba1292f99d843d4229caea` |
| `tests/docs_test_native_protocol_test.ts` | `813e75cc27141373741880e775bc5a89ee6be42b39918dc045cc250ada7cd8b4` |

Delta headers содержат только эти4paths. Source/parser/compiler/import/scripts/
tests/Deno/network/native/server/build/CI/science не запускались. Никаких
source/fixture/CP/index edits этим review; только два review artifacts.
Сначала inspected actual guards/callers, затем авторский report. Ранее
исправленные queued-phase/self-SHA/counter loops повторно не ревьюились.

Внешняя Root FORMAT1 dependency зафиксирована отдельно. В начале проверки
helper `38a56bff45bd7f7e36e8eb1a4542756b5225388d53827b6c24c73c9b059dc62b`,
fixture `8946e323023da597629f669dcb60c17bb6674f9c5a9bd9e2492dea280c35f16b`.
Во время разрешённых Root двух targeted-comment edits,08:21:28UTC, actual
hashes стали соответственно
`68f0efb5b45a03f130a52d14279e427c83c11b317a3c244e43375dbac5b8d3f5` и
`2639be2132a88adb3e1ccd204112180efa065089e9ade5cae87e38c970952f99`.
Эти изменения вне четырёх frozen paths и вне I2D delta. Не отменялись и не
приписаны I2D writer. Whole native16 closure/старые pure hashes/результаты
проверок на новые bytes не наследуются: перед later execution Root связывает
актуальные dependency bytes/HEAD/descriptor/harness отдельно. Этот review не
повторяет проверку их behavior, format или lint.

## Подтверждённые узкие исправления

| Поддефект | Actual guard/caller | Source evidence и предел |
| --- | --- | --- |
| Rejected ref сам означал measured | native1619–1714: source_bound сбрасывается до required binds; source_validated только после native finish validation; final measured не зависит от ref | Исходный false positive устранён; source failure control196–222 изолирован, см. ниже |
| Driver exit сам означал retention complete | validate_phase_retention1298–1336 читает actual pending/receipt/index/raw refs, identities/SHA/bytes/reap; caller1711–1714 блокирует positive при incomplete | Readback не объявлен durability; пустой proof set оставляет unknown |
| Driver closure/retention смешивались |1702–1714 отдельно validate_terminal→driver_closed, отдельно retention | Ошибка publisher/driver proof не превращается в phase-driver-closure closed |
| Bool-as-int/individual negative caps | integer166–168, finite_number171–173; request1164–1194; terminal1896–1907 | Некоторые реальные scalar defects устранены до caller side effects; полный nested closure ещё отсутствует |
| Observation tool/duration/UTC не проверялись | read_tool_observation574–575,606–615 | Actual tool equality, duration integer, raw sizes/exit/complete, UTC parser и stale/future checks добавлены |
| Tiny task intent | launch_phase1817–1821 передаёт validate_intent(audit_intent(...)); bootstrap1939 и producer phase2027 также validated | Все три источника используют D5 exact redacted union, не plaintext env/capsule |
| Typed refusal legal16KiB ломался на Git4KiB cap | TS253–260 читает max(normal,16384), discriminates union, normal response повторно ограничен smaller cap | Представительский legal refusal now source-readable; real chunked wire не запускался |
| TS отсутствовал единый reply reader | responseFor62–78 вызывается в real stdio transport257 и checked wrapper83–84,163–164 | Не orphan helper; enum/map semantic closure ещё неполна |

Нынешний `durable_publications=set()` (`native1018–1021`) не загружается из
caller JSON. `validate_phase_retention:1334` требует доказательства publication
для всех собранных refs. Пока boundary2 не реализовал atomic publish+directory
durability, production retention unknown/failed — ожидаемый результат.
Заполнение set на основании простого readback/filename/SHA будет дефектом.

## R1 — C3/C7 typed union ещё допускает нестроковые enums

`docs_tests_cli.ts:66` проверяет
`includes(String(reply.code))` и `includes(String(reply.cleanup_status))`.
Поэтому JSON `code:["source_unavailable"]`, `cleanup_status:["unknown"]`
пройдёт enum branch, несмотря на exact string contract. Аналогичное coercion
в report_format56, stream73 и validation75. Это воспроизводимый source путь,
не гипотеза о parser/runtime: стандартное string conversion одноэлементного
array даёт его элемент. Refusal всё ещё приводит к failure, поэтому actual
product false pass отсюда не доказан; но закрытие P1-E/C7 заявлять нельзя.

Исправление: typed string enum helper без coercion, использовать до membership
на каждом таком поле; negative source pairs arrays/objects/numbers/null с
исходными допустимыми enum spellings внутри. `responseFor` должен возвращать
только exact wire type, не значения, которые later code нормализует по-своему.

Остальные конкретные incomplete native unions в этом scoped inspection:

- Active registration985: observation_registration rows не имеют finite row
  shape/types/unique tuple validation; native_receipt_sha/accepted_native_captures/
  runtime_closures maps не closed целиком. Proof refs должны быть typed до reads.
- Initial-empty994–999: populated/monotonic/birth/memory_events не проходят полный
  typed predicate; `False == 0` допускается для populated. Allocation record
  сравнивается с request через Python equality1005, где bool может совпасть с
  int в nested limits. Exact keys не заменяют typed nested scalar validation.
- validate_request1195–1203 не замыкает ordered phases/scope mapping/конечные
  container types; actual setup может отвергнуть их позже, но constructor
  contract требует раннего отказа. Это дополнение validators, не смена API.
- Parent phase receipt1739–1745 проверяет несколько positive labels, но не
  exact full phase union и native publication/driver/command/index refs в
  одном reader. Client/setup terminal branches должны использовать тот же
  normative receipt validator. Current partial behavior честно не READY.

Нужны complete bounded record validators и вызовы их на actual producer/
parent/client entrypoints. Invalid shape должен fail/refuse до соответствующего
FD/read/dispatch, а не попадать в generic KeyError после части работы. Accepted
records остаются independently parent-registered; новый trust root не нужен.

## R2 — propagation control не проверяет собственный новый retention guard

`tests/test_docs_test_native.py:196–222` действительно вызывает actual run_phase
и проверяет rejected ref/source label/missing-index outcome. Но Fake Driver
в202 возвращает `finish` с sequence1, тогда как actual caller1632 и
DriverPipe.receive1444–1457 разрешают первым только `preflight`. Fake игнорирует
allowed_ops, поэтому это намеренный shortcut в недостижимое normal wire state.
Он годится для изолированной propagation проверки, но не свидетельствует о
caller-consistent paired path.

Главнее: control209 целиком заменяет validate_phase_retention на готовую
строку complete/partial и validate_terminal на True. Ни один added case не
исполняет новый native index/pending/receipt/raw readback proof и правило
durable_publications пуст/заполнен. Поэтому claims «actual ref ledger guard
имеет paired evidence» пока сильнее имеющегося fixture source.

Минимальная коррекция без полного C8: in-memory artifact reader/store,
actual validators не заменяются. Healthy bound pending/command/index/raw/
terminal/proof-set даёт complete; missing index/required ref, mismatching
pending binding, raw SHA/size, false reap, missing durability дают
partial/unknown. Production-empty proof set всегда unknown. Mock лишь низкие
read handles/clock, а не результат проверяемого predicate.

Finalizer source control должен выдавать legal preflight then finish sequence
и соблюдать allowed_ops, либо быть явно назван private finalizer-only control
без claim о caller route. Negative case final source throw после накопленных
captures должен сохранять actual ledger refs; count execute0 из нынешнего
shortcut не заменяет этот тест. Полный healthy broker/kernel→parent acceptance
по-прежнему boundary4, здесь его не требуют выполнить.

## R3 — source label стал безопаснее, но measurement criterion ещё связан с pass

`source_validated` устанавливается1682 только после полного
validate_driver_finish, который проверяет в том числе report summary/exit/
result. При успешно прочитанном source и malformed/failed unit report
measured1712 будет false. Это fail-closed и устраняет исходный ложный positive,
но означает «полностью validated finish» вместо отдельного source observation.

До boundary3 допустимо сохранять conservative not_measured и явно так
описывать его ограничение; нельзя объявить доказанной независимость source
measurement и unit acceptance. Boundary3 должен выводить source criterion из
actual complete bound graph/native reads и сравнения identity, независимо от
ошибки report parser. Ровно measured disagreement — measured/failed binding;
reader/transport rejection — not_measured. Ни наличие, ни отсутствие accepted
validation ref само по себе не является этим criterion.

## Retention dependency для boundary2: что нельзя потерять при подключении proof

Current validator1304–1334 собирает index, terminal closure, required summary/
validation и native command pending/terminal/raw refs. Driver stderr raw,
который хранит отдельный DriverPipe, не имеет stream ref в DriverTerminal/
closure schema1896–1907 и не входит в all_refs. Сейчас пустой durability set
не даёт false complete; future publisher должен добавить actual driver raw
stream identity/durability в owning closure evidence и retention manifest,
а не просто заполнить имеющиеся tuples.

Также publication positive самого final phase/setup receipt должно появляться
только после successful owning publish/directory proof; body label complete
не удостоверяет durability собственного final filename. Эти обязанности уже
следуют I2C boundary2. Нынешний retain_record902–913 не исправлен и не принят
как durable publisher этим narrow CPP.

## Точный следующий I-ready contract

Не повторять уже source-fixed queue/self-SHA/counter loops. Same four owning
files, D4/D5/D6 schemas/caps/source16, никаких native calls/CP/component/server
изменений или широкого design-only этапа. Оставшиеся последовательные boundaries:

1. **Закрыть остаток boundary1:** typed enums и nested C3/C7 records; normative
   readers на parent/client/driver endpoints; caller-consistent propagation
   pairs и actual retention-validator artifact pairs R1/R2. Сохранить publisher
   unknown до реально реализованного proof, не «разблокировать» set вручную.
2. **Boundary2 cleanup/publisher:** полный owner от первого FD/fork; закрытие
   inherited FDs без4095предположения; error-preserving TERM/KILL/drains/reap;
   actual partial raw/index/fallback на каждом outcome; no-replace atomic
   publication + file/directory durability; proof-set только из этих операций,
   включая driver/producer streams и phase/setup records. Positive unknown
   запрещён. I2C known C4/P1-C остаются до этой реализации, заново не аудированы.
3. **Boundary3 exact slots/ledger:** exact ordinal source/native graph slot
   states, failure counters finally, source measurement independent from
   reports, no-exec metadata identity и complete write/fallback/transport
   budget trace.100/444 schedule,512/8MiB/60s per phase,2MiB metadata/global
   storage/deadline не расширять. Actual clean/family freeze — отдельный runtime
   prerequisite, guards — обязательный source output.
4. **Boundary4/C8:** manufactured existing trusted lease/fake handles/clock/
   process/pidfd/cgroup exercising actual factory→broker→driver→executor→D6
   terminal flow, legal preflight→check/direct docs. Healthy exact dispatch и
   paired failures before/after gates/ACK, wrong schema, storage/drain/EOF,
   source-final throw, missing/unknown durability; no forbidden dispatch and
   exact retained refs/status.8+8 остаются nominal, пока нет measured execution.

После каждого законченного source boundary — immutable report/identity/patch
с точными закрытыми subdefects и remaining lines; после corrected source CPP
Root отдельно связывает compiler/DEV plans. Этот review не выдаёт новых calls.
Product87/source4/CI0/science0/native-build0 не пересчитываются и не меняются.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Rejected ref больше не даёт false measured | Native1619–1714 separate state | Conservative criterion ещё coupled finish/report | сохранить |
| Driver exit сам даёт retention complete | Native1298–1336 actual manifest/proof gate | Actual validator source pairs отсутствуют; publisher pending | изменить |
| D5 intent используется на трёх launch paths |142–159,1818,1939,2027 | Actual publication boundary2 | сохранить |
| Typed reply unions закрыты полностью | TS66 coercing enums; partial native nested schemas | P1-E/C3/C7 remaining | изменить |
| Whole source/native READY достигнут | Empty durability proof + explicit remaining boundaries | No execution/source build/native evidence | данных недостаточно |
| Pure bytes совпадают с прежним freeze | Root FORMAT/comments changed hashes вне4paths | Нужно свежее dependency binding before execution | дополнительно измерить |

STOP для Root. Conservative reads<2MiB (<5MiB), output<40KiB (<128KiB),
wall<12min. CPU/RSS/physical I/O не измерены. Source/fixture/CP/index writes=0;
parser/compiler/import/scripts/tests/Deno/runtime/native/network/server/build/
CI/science=0. Original I2C/I2D artifacts не переписаны.
