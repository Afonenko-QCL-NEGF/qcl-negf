# I2F high CPP: B1r+B2a/B2b/B2c

**CHANGES_REQUIRED.** Остался один узкий B2a propagation defect после healthy
capture. B1r, B2b и B2c по inspected source закрывают поставленные I2E defects;
основная B2a failure-path correction также реализована. Whole candidate не
native READY. Следующий I2G нужен только для описанного ниже propagation и
paired fixture; B3/B4 остаются отдельными packets, новый design цикл не нужен.

Проверка source-only: target scripts/import/parser/compiler/tests/runtime/
network/native/CI/science0; source/CP/index edits0. Product88/source8 — counters
Root из поручения; reviewer не добавляет product calls и не разрешает90 или
какой-либо actual retry. Source gate, source build, native gate и scientific
acceptance не отождествляются.

## Неизменяемый набор

Worktree `/tmp/qcl-docs-test-routing-worktree`, выбранный HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`; overlay four paths, не committed
native16 freeze. Governing I2E review
`c8224246cc32b3327680841a292a9b232fa82b87834ad52067577b1805827e62`;
D4/D5/D6 и прежние незакрытые boundaries сохраняются.

| Артефакт / owning path | SHA256 |
| --- | --- |
| I2F report | `f980611a22f90ecf82b224c827f17e26922f6a42015ca464011444111f2c28cf` |
| I2F identity | `bdd181224b3963226b35699d1076056e820e511fe1dd6a6077021b2ad8b36205` |
| Complete I2E→I2F delta,60319B | `1ac2e0b556153a05905542c01ce606d10bb5b10bb20cbdb225293a34e2ade464` |
| `ops/docs_tests_native.py` | `9ac8407583293567e05eb0217e77d83c58faa91c1ab59c96f22d8cce190d35fa` |
| `ops/docs_tests_cli.ts` | `268554ff880349939d7577cd07104762cc2d8f446dd597079171985e36c2cae7` |
| `tests/test_docs_test_native.py` | `36a52d7bb9b42fa27eab821f711d1d9b1eb8e624cbd350d464a7c5d330220b36` |
| `tests/docs_test_native_protocol_test.ts` | `a3c9baf9f095b230a0d78082fb5769f1f11b84efa3f16a2e440a21e55c311dd2` |

Actual pre-I2F copy находится в
`/tmp/qcl-docs-routing-i2e-frozen-before-i2f/manifest.sha256`, не manifest.json;
SHA `5a900b91914f1c544e315a3bb714507cf885b3bcba54a3812ec0ef0da2c0f2c7`.
Hashes всех четырёх сохранённых files проверены и совпадают с I2E86d041/70a28e/
25e6e9/eea410. Historical artifacts не менялись. Pure68f0ef/2639be зависимости,
Root107bac5, component gitlinks и CHECK1/v7 ограничения этим review не
переаттестовываются; whole closure на новые bytes не наследуется.

## Узкие source closures

Локаторы ниже — actual frozen I2F `ops/docs_tests_native.py`, кроме явно
обозначенных fixtures. Execution результатов этих controls не было.

| Ticket | Actual correction и paired evidence | Ограничение |
| --- | --- | --- |
| B1r actual typed JSON | validate_registered_shape298–319; canonical same_record322–324; actual initial/allocation readers1269/1275; read_registered_payload1406–1411. Accepted finish-validation binding2362 теперь validate_binding. Typed setup ACK2322–2336. TS startFor28–34 проверяет safe integers/hash/types | Actual bool/int aliases больше не проходят равенство registration. Python fixture50–84 содержит ACK/version/PID и actual admission int/bool/float pairs; полный C8 не заявляется |
| B2b private worker inherited FDs | Actual fork-child1010 вызывает census до worker1012; census1212–1226 закрывает весь set вне exact keep, tolerates только EBADF, остальные close errors запрещают dispatch. Worker gate закрывается892–894 | Python fixture118–133 проходит actual fork-child seam с producer/brokerFD900 и FD65537, проверяет closure до worker и сохранение channel/gate. Real fork/FD kernel не запускался |
| B2c same producer/participant manifest | validate_terminal_retention2303–2319: actual closure, same_record streams↔closure, raw_complete, exact raw bytes/hash/length и proof tuples. Production producer2256 и каждый participant2263 используют этот reader; finite unique participant identities2258–2262 | Python fixture299–317: same actual manifest, mismatched size/map, empty proofs, wrong identities, false raw_complete, missing raw. Это source controls, actual external provider BIND не получен |
| B2a independent failure cleanup | Worker945–975 разделяет TERM/KILL, drain/reap, pipe/raw/selector/owner close и reread; cleanup_stage327–333 сохраняет bounded first/secondary stage/error. Failure/frame/ACK retention977–990. Parent1075–1098 ждёт direct child даже при birth/pidfd failure, не пропускает closes/fallback. Active settlement1336–1369 independently attempts raw/metadata operations. Driver adopted reap error и fallback phase read также guarded в delta | Python fixture134–219 проверяет actual worker multiple errors, pinned-pidfd signalling при census error, post-fork birth/pidfd/attach и settlement faults. Healthy-return cleanup propagation отсутствует: finding ниже |

Уже принятые publisher, enum, queued-phase/self-reference/counter corrections
повторно не открывались. Положительные command raw/phase artifacts остаются
immutable observations; поздняя ошибка не разрешает их переписывать. Failure
общего attempt — отдельный факт от качества уже сохранённых raw observations.

## I2F-R1 / B2a — P1: recorded owner cleanup failure теряется после healthy return

**Primary locators:** `ops/docs_tests_native.py:1067`, `:1071–1098`,
`:1331–1338`, `:1365–1372`.

`execute_bounded` готовит успешный return1067 после command receipt и raw
publication. Затем finally вызывает cleanup_stage для pidfd/channel close1087–
1091; ошибка сохраняется в локальном failures, затем launch_state.failures1098.
Она не отменяет уже подготовленный return и не меняет capture result.

Actual caller Active.command получает этот успешный result1331–1335 и ставит
entry.outcome=complete. В собственном finally1337 он создаёт новый пустой
failures и добавляет только sys.exc_info primary; owner failures не импортирует.
`owner_failures=launch_state.get(...)`1368 читается только при уже непустом
caller failures1365. Если raw/metadata settlement нормален, эта ветка не
исполняется, ticket возвращается1370–1372 как complete. Следовательно, healthy
capture + secondary pidfd/channel close error может остаться positive command
и не сохранить cleanup failure в command index/attempt outcome. Это actual
control-flow gap; runtime failure не исполнялся и kernel leak не измерялся.

**Минимальный I2G contract, Python owner + existing fixture:**

1. Довести owner cleanup failures до Active.command до выдачи ticket; unknown
   cleanup исключает successful attempt, даже если capture/raw observations
   положительны. Сохранить already-published original receipt/raw как факты;
   не переписывать их SHA/body и не превращать good raw в fictional bad bytes.
2. Сохранить bounded primary/secondary history в отдельном failure/settlement
   record и связать его с native command ledger/index. При existing primary
   исключении оно остаётся исходным; late cleanup failures — secondary. При
   изначально healthy command first cleanup failure становится primary failure
   overall attempt, outcome unknown/failed; next command/phase не запускается.
3. Paired fixture проходит actual execute_bounded→Active.command caller seam:
   normal capture + EOF/reap/publication/settlement без close fault остаётся
   admissible; такой же capture с единственным pidfd-close либо channel-close
   fault сохраняет raw/ref hashes, записывает stage/error, не выдаёт positive
   ticket/ledger outcome. Все остальные доступные close/settlement attempts
   продолжаются. Дополнительная пара existing execute failure + cleanup fault
   сохраняет original primary и secondary ordering. Mock лишь OS/storage
   boundaries; не заменять validators/owner failure propagation готовым status.

Это один конкретный code/fixture packet. Дополнительный широкий audit или
изменение D4/D5/D6 не требуется. Source positive по B1r/B2b/B2c не означает,
что весь B2a теперь закрыт, и не разрешает actual retry.

## Сохранённые отдельные gates

B3: exact ordinal Git slots, failure cost finally debits, source/config binding,
полный raw/metadata/protocol/fallback physical-domain/global trace. Прежний
driver stdout path raw_root против protocol reservation и source measurement,
связанное с unit report, остаются отдельными ранее выявленными tickets. Здесь
они не исправляются и не объявляются заново inspected/closed.

B4: full manufactured existing lease→broker→driver→execute→D6 outer finalizer
coverage; nominal Python8+Deno8 без observed execution не доказывают полноту.
Finite DEV/compiler acceptance требуют отдельного grant. Actual provider BIND
должен обеспечить existing opaque capability, native publication ownership,
runtime/allocation inventories, gated partial spawn cleanup и all participants;
это prerequisite интеграции, не новый repo trust root и не source PASS claim.

## Ledger и решение

Начало09:12:46UTC; finite cap10min/1CPU/1GiB/read4MiB/output96KiB. Content/hash
read conservative upper3MiB; CPU/RSS/physical I/O не измерены. Source selections
узкие, некоторые tool outputs всё же truncated; точный aggregate byte counter
transcript не снимался, поэтому полное соблюдение96KiB не утверждается. Review
artifacts ограничены16KiB. Отдельно: автор I2F report110–113/identity сам
фиксирует неизвестный aggregate output cap; это не подтверждение within-budget
и не новое runtime свидетельство. Все target execution counters остаются0.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| B1r/B2b/B2c закрывают exact I2E defects | actual readers, fork caller, manifest/proof reader и paired source controls | source-only; provider/DEV не выполнены | сохранить |
| B2a полностью замкнут | R1: healthy return не учитывает owner cleanup failures | один finite propagation/control ticket | изменить |
| Whole native source/runtime READY | B3/B4/provider gates и R1 остаются | execution0 | данных недостаточно |
