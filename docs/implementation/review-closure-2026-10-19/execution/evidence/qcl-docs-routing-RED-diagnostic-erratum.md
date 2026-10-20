# DOCS-ROUTING-RED-1: source-only диагностический erratum

Решение D: допустим узкий будущий v3 validator предшественника для единственного уже сохранённого RED. Исходная классификация `completed_inconclusive_or_guardfailure_preserve_no_rerun` сохраняется. Erratum не является `ACCEPTED_RED`, разрешением исполнения, READY, результатом GREEN или доказательством 227 выполненных assertions. Новый RED не нужен и не разрешён. Этот документ требует независимого high D review до отдельной реализации medium; v3 harness/plan здесь не созданы.

## Неизменяемые основания

| Основание | SHA256 |
| --- | --- |
| v2 harness `/tmp/qcl-docs-routing-local-unit-run-v2.py` | `0061c27ec61bf8ca15d6e94d304db695072b12adc3fe6ca8ddef2ee254df82e7` |
| v2 plan `/tmp/qcl-docs-routing-engineering-plan-v2.json` | `5147cab0a8df1d50fb908b3c247e8c7b0e11852ee01a990f8a35228b3e70157a` |
| Frozen fixture `/tmp/qcl-docs-test-routing-worktree/tests/docs_test_routing_test.ts` | `04589b3993e51885b2abc08cb516c7a6467709e3d278c593874c598ecaa9ecf3` |
| Retained `/tmp/qcl-DOCS-ROUTING-RED-1/receipt.json`, 2724 B | `e874825467896121a89e7c0d31272ed5b923da8b0cc08e30846adca56c6806b0` |
| Retained `/tmp/qcl-DOCS-ROUTING-RED-1/original.log`, 765 B | `6b044ed571751341f215353d5dafd384dcf009a70c4b471595ebdcb53b8589ad` |
| Receipt-bound Deno executable, version label 2.8.3 | `cdd88de791341a151d80ee5c189abb4b7681beb0aca9f5c1a4b0f4fe9429e26c` |
| D1 `/tmp/qcl-docs-test-routing-design.md` | `fb8ca769d5406150ecac0381d8dbe250a2515664b16417dead7f4ebba5a88270` |
| D2 `/tmp/qcl-docs-test-routing-design-v2.md` | `bbb8cbeb4845a9a7b9514010f5c988beeac66080246d9fca1d6c12ee8a81cf70` |
| D2 high R `/tmp/qcl-docs-test-routing-design-v2-review.md` | `939555c9291e98be1200b063bcf06e344a7597907dfbf498bf28029927728967` |
| Fixture API packet `/tmp/qcl-docs-test-routing-red-report.md` | `e0621ad8010399bb7013a35353496ecc6581193c8d0f90ea358ab00985070215` |
| Harness v2 author report | `adbe4ed2aa3f96246ea68a5d49972eff10a4aa3a2007b3fe5e0fc7a473e4378d` |
| Harness v2 high R, current retained bytes | `e4766f8a2e93a5fed9eb0ecf4400b337c5324536c622d8d78f3c8f6641a6d0c4` |

Runtime executable повторно не читался и не запускался: его identity здесь — retained receipt/plan binding, а не новое измерение runtime. Будущий GREEN сохраняет собственную предварительную проверку executable hash.

## Наблюдение и причинность

Receipt фиксирует child exit 1, wall 1.3661311600008048 s, 29 samples, sampled peak process-tree RSS 261308416 B, owned-TMP lstat peak 333504 B. Capture complete, output overrun=false, stop_reason/guard_error/raw_capture_error=null. Это завершённый guarded child с typecheck failure. Nominal source registration count=227; observed_engine_tests=null. Такой результат не означает выполнение assertion или научную/интеграционную приёмку.

В exact fixture:3–13 все helper exports импортируются из отсутствующего `../ops/docs_tests.ts`; отсутствие helper подтверждено read-only filesystem existence check. `runChecks` вызывается в строке 303: `const result = await runChecks(planChecks("check", r), r, executor)`. В строке 311 `result.steps.slice(1).map((step) => ...)` использует тип результата этого импортированного вызова; локальная аннотация callback отсутствует. Другие callbacks над `result.steps` в строках 307, 629, 635 имеют явные локальные аннотации, а `executor.calls` в строке 304 — локально объявленный `Step[]` (236–248).

При неразрешённом import у `runChecks` нет доступной сигнатуры; восстановление typechecker даёт вызову error/any-type. Поэтому `result.steps.slice(1).map` не предоставляет контекстную сигнатуру callback, и параметр `step` получает TS7006. В этом выражении нет отдельного источника типа, который мог бы пережить потерю импортированной сигнатуры. Это source-causal cascade TS2307→утрата contextual typing→TS7006. В frozen API packet:18,31 контракт `runChecks` возвращает `AggregateReceipt` с массивом step receipts и typed `summary`; при соблюдении этого контракта callback получает тип из массива.

Вывод ограничен этой зависимостью: отдельный дефект fixture не установлен. Исполнение counterfactual с заглушкой, no-check, изменённым fixture или появившимся helper не выполнялось. Фактический helper пока отсутствует, поэтому тип его будущего результата не проверен. Если реализация оставит `runChecks`/`AggregateReceipt.steps` как any и TS7006 сохранится, GREEN провалится; erratum не разрешает annotation patch или смену fixture ради обхода этого gate.

## Почему v2 блокирует этот результат

`accepted_red`:87–128 требует exact v2 acceptance со статусом `ACCEPTED_RED`; строки 125–127 допускают только literal `Module not found "file:///tmp/qcl-docs-test-routing-worktree/ops/docs_tests.ts"` и ровно один `Module not found`. Actual Deno 2.8.3 печатает `TS2307 [ERROR]: Cannot find module 'file:///…'`, затем зависимый TS7006. Эти bytes не удовлетворяют v2 предикату. Это диагностическое несовпадение ожидаемой строки, а не guard failure, установленный receipt.

Дополнительно строки 92–105 связывают RED harness/plan с `self_sha`/`plan_sha` текущего GREEN. Любой новый v3 harness/plan по определению имеет другие hashes; простая замена matcher без разделения ancestral/current identities не примет genuine v2 RED и создаст давление переписать свидетельство. Переписывание запрещено.

## Точный контракт будущего v3 validator

1. Сохранить v2 harness, plan, receipt, original log и original inconclusive classification побайтно. Создать новые versioned v3 artifacts; не менять fixture, target/module, command или permissions. v3 не содержит разрешения ещё одного RED и отклоняет alias/rerun. Из исходных двух product calls один израсходован; единственный оставшийся — `DOCS-ROUTING-GREEN-1`.
2. Fresh Root READY для GREEN связывает **текущие** actual v3 harness/plan hashes, тот же fixture/runtime, actual helper hash и независимый source/import-purity review. Не подставлять ещё неизвестные future hashes. Текущие H/P проверять отдельно от retained ancestor H/P.
3. До guard imports, child submission и permanent GREEN reservation валидировать отдельную canonical owned regular ≤32KiB v3 predecessor-review record с exact schema, duplicate-key rejection и hash-bound refs. Его status должен явно обозначать `SOURCE_REVIEWED_INCONCLUSIVE_PREDECESSOR_FOR_SINGLE_GREEN`; original classification хранить без изменения. Это узкое разрешение использовать evidence, а не ложный `ACCEPTED_RED`. Record связывает scope, attempt, fixed v2 harness/plan hashes из таблицы, fixture/runtime, exact receipt/raw refs, source erratum ref и отдельный принятый high D review ref. READY связывает hash этого record. Неподписанный same-user JSON сам по себе не удостоверяет Root authority; это trusted Root handoff с retained evidence.
4. Прямо перечитать retained ancestor harness/plan/receipt/raw по фиксированным путям; canonicality, owner, regular type, size и actual SHA обязательны. Receipt/raw hashes и размеры должны совпасть **с указанными константами**, record и actual read buffer. Ancestor H/P сравнивать только с frozen v2 constants, никогда с текущим v3 self/plan hash. Reject любой другой RED attempt, raw, fixture, runtime, ancestor H/P или source erratum/review binding.
5. Сохранить все v2 direct receipt predicates: scope/attempt/argv/cwd/clearEnv+exact env/limits/dependency hashes; helper=null; red_predecessor=null; exact positive exit 1 для этого artifact; complete capture; no overrun/errors/stops; sample_count≥2; finite wall и sampled RSS/TMP внутри прежних caps; nominal227/observed=null. Проверять actual retained receipt, а не только утверждения нового record. Отсутствие обязательных данных блокирует GREEN. Сохранить before/after source bindings и byte-preserving evidence retention.
6. Raw predicate — **exact artifact identity плюс full-layout equality**, а не набор независимо допустимых diagnostics. После единственного уже принятого ANSI CSI stripping требуется полное равенство приведённому ниже UTF-8 literal, включая порядок, URI, координаты, строки, пробелы, info/hint и финальный LF. Никаких trim, wildcard-path, arbitrary counts, substrings-only, удалений вторичных errors, принятия любого TS7006 или future runtime layout. Даже другой лог с теми же двумя codes блокируется. Точный original raw SHA дополнительно фиксирует сами ANSI bytes.
7. Причинная source review привязана к неизменённому fixture и imported typed return contract, как разобрано выше. Если high D review обнаружит независимый fixture defect, иной источник типа или неподтверждённую причинность, predecessor не eligible: STOP/blocked, без нового RED и выдуманной приёмки.
8. После high D review отдельный medium implementation может реализовать только этот узкий validator/plan delta. Затем нужен независимый source R exact v3 H/P и отдельный Root READY. Никаких harness/parser/selftest/target запусков данный D не разрешает. GREEN после реализации target всё ещё требует полный TAP: ровно227 observed/expected, все227 passed, ноль fail/ignore/skip/todo/only, корректные names/plan/counters, exit0, complete capture, guards и source bindings. RED остаётся observed=null. Pure GREEN не закрывает actual task/workflow/CLI integration, native admission/build, full CI либо science.

Полный normalized layout (ровно один LF после последней строки):

```text
TS2307 [ERROR]: Cannot find module 'file:///tmp/qcl-docs-test-routing-worktree/ops/docs_tests.ts'.
    at file:///tmp/qcl-docs-test-routing-worktree/tests/docs_test_routing_test.ts:13:8

TS7006 [ERROR]: Parameter 'step' implicitly has an 'any' type.
  equal(result.steps.slice(1).map((step) => {
                                   ~~~~
    at file:///tmp/qcl-docs-test-routing-worktree/tests/docs_test_routing_test.ts:311:36

Found 2 errors.

error: Type checking failed.

  info: The program failed type-checking, but it still might work correctly.
  hint: Re-run with --no-check to skip type-checking.
```

Строка hint сохранена как observed diagnostic data; это не инструкция запускать `--no-check`.

## Границы и учёт

Root checkout HEAD `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`; исходный dirty status сохранён. Frozen fixture worktree HEAD `e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b`, status `?? tests/docs_test_routing_test.ts`. Root gitlinks перечитаны без обновления. Ни fixture, ни product/CP/native/git state не изменялись. Новых engine calls, imports, target/harness compile/parser/typecheck/tests, сетевых действий и runtime probes=0. Созданы только этот документ, identity и read ledger.

Read ledger conservatively charges every full underlying file for excerpts/hash passes; source reads ограничены <1MiB, без чтения runtime/cache/TMP payload. Metadata-only `/tmp` filename discovery однажды затронуло недоступные directory names, без payload reads. Несколько batched outputs были усечены; необходимые locator excerpts перечитаны. Полнота отображённого batch output не заявляется. Wall/CPU/RSS физически не инструментировались; отдельная source работа без target execution. Суммарный transcript-output byte count не измерен и соответствие его лимиту64KiB не заявляется; собственные три deliverables обязаны уложиться в64KiB. Это ограничение учёта не заменяет ни один gate.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Сохранённый child завершился typecheck failure без measured guard failure | Exact receipt/raw hashes; exit1, complete capture, null errors | Sampled peaks; assertion execution отсутствует | сохранить |
| TS7006 зависит от отсутствующего typed import | Fixture13,303,311; API packet18,31 | Source proof; будущий typed helper ещё отсутствует | сохранить |
| v2 matcher/identity pairing непригоден для exact actual predecessor после v3 correction | v2 harness87–128,230; retained raw | Результат остаётся inconclusive | изменить |
| Разрешён только exact-artifact predecessor exception | V3 design1–8; fixed ancestor H/P/test/runtime/receipt/raw | Требует independent high D R, затем отдельные I/R/READY | изменить |
| GREEN либо227 passes уже доказаны | observed_engine_tests=null | Единственный GREEN остаётся неиспользованным | данных недостаточно |

STOP. Не создан v3 harness, acceptance/eligibility record или READY; ни один call не выполнен.
