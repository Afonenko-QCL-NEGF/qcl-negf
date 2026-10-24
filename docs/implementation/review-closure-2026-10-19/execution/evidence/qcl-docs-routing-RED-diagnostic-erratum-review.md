# RED diagnostic erratum — независимый high D review

Вердикт: **PASS_DESIGN_EXACT_PREDECESSOR_ONLY**. Blocking findings в узком
design нет. Причинное объяснение TS7006 обосновано для exact frozen fixture;
самостоятельный дефект fixture не установлен. Это source-only D acceptance,
без разрешения исполнять harness/parser/tests/native или создавать READY.

## Неизменяемые основания

| Артефакт | SHA256 |
| --- | --- |
| Erratum D,15954 B | `6dfb097abf97aeabd9114354c987b5846fd19f449c4d0bfc2168299a1e03383b` |
| D identity | `3b58a17464d0ce2b12dadb5e8bec1c794a4b88247b2077aa3c3fe12d6fdc59b9` |
| D read ledger | `a366b49c742dd0b632dad98afe84fdf813e23b83137e36c57561d8e963c0e20c` |
| Retained RED receipt,2724 B | `e874825467896121a89e7c0d31272ed5b923da8b0cc08e30846adca56c6806b0` |
| Retained original raw,765 B | `6b044ed571751341f215353d5dafd384dcf009a70c4b471595ebdcb53b8589ad` |
| Frozen fixture,38723 B | `04589b3993e51885b2abc08cb516c7a6467709e3d278c593874c598ecaa9ecf3` |
| Historical v2 harness | `0061c27ec61bf8ca15d6e94d304db695072b12adc3fe6ca8ddef2ee254df82e7` |
| Historical v2 plan | `5147cab0a8df1d50fb908b3c247e8c7b0e11852ee01a990f8a35228b3e70157a` |
| Frozen API packet | `e0621ad8010399bb7013a35353496ecc6581193c8d0f90ea358ab00985070215` |

Первичные receipt/raw прочитаны полностью. Проверены D/identity/read ledger,
fixture13/235–248/300–314/625–635, API packet18/31 и actual v2 validator87–128,
195–239,320–340. Runtime/cache/TMP payload не читались; executable SHA
`cdd88de791341a151d80ee5c189abb4b7681beb0aca9f5c1a4b0f4fe9429e26c`
здесь retained receipt binding, не новое измерение бинарника/версии.

## Наблюдение и причинный вывод

Actual original raw содержит TS2307 `Cannot find module` для exact absent helper
URI на13:8 и TS7006 для `step` на311:36; итог `Found 2 errors.` и typecheck
failure. Cat-vET показывает ANSI CSI, порядок строк и terminal LF, согласующиеся
с полным normalized literal в D. Автоматический normalizer/parser не запускался.
Exact raw SHA связывает также все исходные ANSI bytes.

Receipt фиксирует exit1, capture complete, raw_bytes765 и совпадающий raw hash,
no overrun, null stop_reason/guard_error/raw_capture_error,29 samples,
wall1.3661311600008048s, sampled RSS261308416B и TMP333504B. Это evidence
завершённого guarded typecheck failure без зарегистрированной guard error;
sampled metrics не являются hard peak/квотой. Report отсутствует как TAP,
observed_engine_tests=null. Ошибок typechecker ровно2 по raw; никакие нули
errors/test counters не выдумываются. Из failure до execution не следует
измеренный engine count0 и тем более227 passed assertions.

Fixture303 получает `result` только из импортированного `runChecks`, объявление
которого недоступно при TS2307. У `result` нет локальной аннотации. Поэтому
цепочка311 `result.steps.slice(1).map` теряет контекстную callback signature,
что объясняет implicit-any TS7006. Напротив, строка304 использует локальный
array `executor.calls:Step[]`, а307/629/635 имеют явные callback annotations.
Это не произвольное принятие любого TS7006: error локализован непосредственно
в цепочке, зависящей от единственного unresolved imported return type.

API packet18 задаёт `runChecks -> AggregateReceipt`, packet31 — массив step
receipts и summary. При выполнении этого typed contract `.map` получает
контекстный тип элемента. Сам unannotated callback не доказывает дефект fixture.
Вывод условен: executed counterfactual не выполнялся, тип будущего actual helper
не проверен. GREEN обязан typecheck неизменённый fixture; если helper оставит
нетипизированную цепочку или выявится иной дефект, это failure, без annotation
patch/no-check/повторного RED из данного design.

## Почему exact exception допустим и чем ограничен

V2 validator125–127 ожидал другой literal `Module not found`, который отсутствует
в actual raw. Historical H/P связываются с текущими self/plan в92–105; новый
v3 hash не может удовлетворить это равенство. Исправить только строку diagnostic
недостаточно; переписать historical receipt либо выдать его за v3 запрещено.

D сохраняет `completed_inconclusive_or_guardfailure_preserve_no_rerun`
как исходную классификацию. Новый record обозначает только
`SOURCE_REVIEWED_INCONCLUSIVE_PREDECESSOR_FOR_SINGLE_GREEN`, не ACCEPTED_RED
и не pass. Такой record разрешает узкую source-reviewed eligibility исторического
evidence; он не меняет результат уже израсходованного вызова.

Для реализации и следующего source R обязательны все D1–8 predicates вместе:

- Только единственный оставшийся `DOCS-ROUTING-GREEN-1`; никакого нового RED,
  alias/rerun/fallback. Исходный общий cap2, consumed1 сохраняется.
- Current v3 H/P проверяются fresh READY отдельно от historical fixed v2 H/P.
  Ancestor H/P/receipt/raw перечитываются по fixed canonical owned regular bounded
  paths и совпадают с константами D, record refs и actual buffers.
- Exact bounded predecessor record schema, duplicate refusal, original
  classification, scope/attempt/source/runtime, erratum ref и отдельный accepted
  high D review ref связаны hashes. Same-user JSON не удостоверяет Root authority.
- Все прежние receipt predicates остаются: exact command/cwd/env/limits/dependency
  hashes/helper=null/red_predecessor=null; exact exit1, complete capture, no
  overrun/error/stop, finite wall/sampled bounds и sample_count≥2, nominal227
  при observed=null. Missing/unknown observations блокируют GREEN.
- Exact765-byte raw identity плюс full normalized-layout equality: оба diagnostics
  в данном порядке, URI/coordinates/source line/marker spacing,2 errors,
  summary/info/hint/final LF. Только принятый ANSI CSI stripping; никаких trim,
  wildcard, code-set-only/substrings-only, удаления TS7006 или general layout
  relaxation. Hint `--no-check` остаётся данными, не runnable instruction.
- Predecessor проверяется до guard imports/submission/permanent GREEN reservation.
  Source bindings до/после и byte-preserving failed evidence сохраняются.
  Actual helper source/import-purity high review остаётся отдельным gate.

Два diagnostics нельзя обобщать в самостоятельную разрешённую категорию
TS2307+TS7006. Даже другой log с теми же codes должен fail closed. Будущий
source reviewer должен сверить exact literals/constants/ancestral-vs-current
branch и отдельный запрет RED, а не принять это D как проверенную реализацию.

Permissions/caps и command не расширяются: single frozen file, typecheck on,
no-config/no-lock/cached-only/no-npm/no-remote/no-prompt/TAP; script FS/env/run/
net/ffi grants отсутствуют; env заменён ровно DENO_DIR/TMPDIR/HOME под owned TMP.
120s/1CPU/RLIMIT_CPU120, sampled1GiB RSS/16MiB TMP/2MiB raw сохраняются.
GREEN всё ещё требует227 observed expected tests, all passed, complete names/
plan/counters, exit0 и source/guard/capture evidence. Это не actual integration,
native/build/full-CI/scientific acceptance.

## Контекст и учёт review

Root HEAD `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`, исходный root dirty status
сохранён;8 gitlinks прочитаны без обновления. Live routing worktree уже изменяется
другой работой: при review HEAD `2bb05d3651af4509fe7f02c1253b40f1e5146fec`,
status содержит untracked `ops/docs_tests.ts` и frozen fixture. Новый helper не
читался и не использовался для причинного вывода. D statement об absent helper
относится к historical RED receipt и его before/after source check, не к
текущему filesystem inventory. Frozen fixture SHA независимо перепроверен.
Historical source нельзя подменять текущим worktree HEAD.

Новых execution/import/compile/parser/tests/runtime/native/network calls0;
product/fixture/CP/index/commit mutations0. Созданы только requested review и
identity. Named logical reads conservatively≤384KiB<1MiB, deliverables<96KiB;
physical I/O/CPU/RSS/wall и aggregate transcript bytes не инструментированы.
Read ledger D изучен как заявленный accounting, не как physical measurement.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| RED показывает guarded typecheck failure с2 errors | Exact receipt/raw и hashes | No assertions/TAP; sampled guards | сохранить |
| TS7006 объясняется потерей imported contextual return type | Frozen fixture13/303/311; API packet18/31 | Нет executed counterfactual/проверки actual helper | сохранить |
| Exact historical predecessor может быть eligible без нового RED | D1–8: immutable refs, full layout, preserved inconclusive, separate identities | Будущие I/source R/Root handoff обязательны | изменить |
|227 passes/выполненный GREEN/native readiness установлены | observed_engine_tests=null | Source D review only | данных недостаточно |

STOP. D принят только в exact-artifact scope. Это не runtime approval,
не READY и не приёмка будущего v3 harness.
