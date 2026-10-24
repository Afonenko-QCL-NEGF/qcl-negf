# Pure routing v5: независимый format-only и final pure closure review

2026-10-20. Verdicts: **PASS_FORMAT_ONLY** и **PASS_SOURCE_PURE_CLOSURE**, только для указанных final2files; **pure_only_slice=true**. Blocking findings не найдены. Whole native I2B CPP4903… остаётся CHANGES_REQUIRED; I2D/native path независим. Этот report не READY, не execution grant и не LINT/CHECK/unit/runtime acceptance.

Никакие scripts/target/parser/compiler/tests/formatter/linter/network/native reviewer не исполнял/импортировал. Прочитаны source bytes/diffs/retained receipts/Root metadata и ограниченная постобработка текста. Записаны только этот report и review-identity; owning files/Root CP не менялись.

## Before→final identity

Baseline root `/tmp/qcl-docs-routing-source-baseline-v5`, final root `/tmp/qcl-docs-test-routing-worktree`.

| Path | Baseline SHA256 | Final SHA256 |
| --- | --- | --- |
| ops/docs_tests.ts | 676a3db1a4de455bbd73a46e57f316b4ae7721e631aa3b7d81a2da8564340d8c | 38a56bff45bd7f7e36e8eb1a4542756b5225388d53827b6c24c73c9b059dc62b |
| tests/docs_test_routing_test.ts | f02f541d633c56280077701ba9fbee3928ae7c2e055cae8b2e78d759bd3a9761 | 8946e323023da597629f669dcb60c17bb6674f9c5a9bd9e2492dea280c35f16b |

Exact source sizes before25884/40125B; after28532/41460B. Baseline manifest SHA `a32abe802009a24ae5ccc4732b02fd859eaccf55adb9d2ef831e4c0acd720fdc` связывает baseline maps, Root107…/isolated2bb и exact v5guard/plan. Hashes/manifest independently rechecked.

Полный GNU unified diff просмотрен без пропусков:1093helper +775fixture lines,1868total. Дополнительный canonical diff в памяти, Python difflib.unified_diff с labels before/<path>/after/<path>, без timestamps: combined SHA `19154b2f0712472bc299fca961d0c77acdf1f915325f6e2e35e4a6cc1fdeeb45`; helper SHA `187282926f3d8e465d77318bc6d40b0e2907a2e24eb0d489eae17a4471de5a52`, fixture SHA `c5902dcba8a832a4f08f304e9a6caf65711d5d128a4ba882aa2b494ac9e28476`. Это идентификатор textual comparison, не parser/AST oracle.

## Почему изменения formatter-equivalent

Helper изменён разворачиванием type/object/array literals, constants, signatures и calls; прежние statement sequences разнесены по строкам с тем же порядком. SHA256 h/k constants, arithmetic/bitwise operators/operands/precedence сохранены, включая >>>/shift/XOR и порядок assignments. Long ternary/boolean chains получили переносы, grouping и short-circuit logic прежние.

Добавленные braces окружают прежние single-statement if/for/else bodies: check calls, steps.unshift и return object runner-smoke. Нет нового lexical declaration с изменившейся областью видимости; dangling else не переназначен. В parseUnitReport прежний else requireThat заключён в block с тем же единственным вызовом, включая необычное `{requireThat(...)}` оформление. Scope/summary/accepted counts/status/reasons не изменены.

Literal strings, escapes, template raw text, regex pattern/flags и comments проверены в изменённых hunks. Regex `.exec`/`.test` с переносом после закрытого literal сохраняет member call; newline до `.test` не становится новым statement. Fixture equal error template перенесён **внутри `${…}` expression**, raw quasi `Expected …, got ` не получает нового LF. Manufactured TAP/Python summary templates и command strings/argv arrays остаются теми же bytes/values. Нет замены data strings на executable source.

ASI-sensitive paths отдельно рассмотрены: return expressions остаются на той же logical return line/в expression position; нет `return`/`throw` с новым restricted line terminator, новая dot continuation и ternaries не меняют выражение. Не добавлены directives/imports/eval/dynamic modules, комментарии не поглощают statements. Типовые trailing commas и whitespace не меняют object/array/property iteration order.

Fixture mutations/callbacks/assertions/test names/loop bounds и injected sourceGraph exceptions сохранены. Все42текстовых callsite-prefix lines `Deno.test(` также совпали before/after; это дополнительное inert text check, не test discovery. Expanded finite registration loops остаются230(227+3), как независимо подробно проверено на exact baseline f02f… в v3/v4 source audits. No filter/only/ignore/skip options добавлены к реальным registrations; строки skipped/TODO/only/filter в manufactured report mutations остаются test data. Observed engine tests по-прежнему null.

## Final pure closure CPP

Для final helper38a56… нет imports, Deno API, real process/env/Git/filesystem/network operations или dynamic import/eval/Worker. Его9exports остаются pure functions над strings, descriptors и injected metadata; runChecks вызывает только предоставленный Executor, не platform adapter. Top-level содержит types/constants/function declarations.

Final fixture8946… импортирует только эти9exports из `../ops/docs_tests.ts`; fakeExecutor.sourceGraph/execute возвращают manufactured metadata/captures и лишь ведут локальный calls array. Strings с real-looking commands/paths/ENV/loader flags не исполняются. CLI/native16/environment/process/git modules не входят в closure; grant-free unit и отсутствие seed сохраняют применимость. Compiler/type correctness не проверялись; exact LINT/CHECK ещё нужны.

Baseline CPP ref `/tmp/qcl-docs-routing-impl-i2b-review.md` SHA `4903c3d64d8254a7b4ac89fcc08efed049485a21b1a1c155922b515b6118c4ea` перехеширован. Его **только positive pure slice** переносится через проверенную format equivalence на final hashes. Настоящий verdict данного review PASS_SOURCE_PURE_CLOSURE не относится к целому I2B/I2D или native producers/driver/readers. Historical RED two-diagnostic evidence, original inconclusive и DOC06 E1 unknownFAILED не меняются.

## FORMAT1 outcome/provenance audit

Primary receipt `/tmp/qcl-DOCS-ROUTING-SOURCE-FORMAT-1/receipt.json`3771B SHA `d33fe2a43835ae48af6ff9a92d8abda2351bdac5e6ddff30c2590a216dba73a6`; original.log138B SHA `b9f584e863bc07b513e9c6808e9e1eb0f6bdba3dc88377b983560b1316fa6919`. Hashes пересчитаны; raw перечисляет ровно2owning files и Checked2files.

Receipt identity exact v5 guarde49c…/plan73b79…/format wrapperddb561…; target_calls1, exit0, CAPTURED_REQUIRES_INDEPENDENT_SOURCE_REVIEW, null stop/guard/capture errors, complete capture/collector_terminal=true и constructor_attempted=true. Source before/after maps равны actual baseline/final. Command — pinned Deno fmt --config exact isolated deno.json +только2paths; cwd exact isolated root. Env completely replaced ровно HOME/DENO_DIR/TMPDIR private stage dirs.

Config SHA `a637ff88ad0e1011480402de58895cb6d178eb1bbe98bdb27ca939b8821f6bce` вновь совпал; config содержит fmt.lineWidth100/strict=true и не изменялся. Runtime SHA cdd88… receipt-bound; reviewer бинарник не хешировал/не probe-ил.

Wall0.157800519s≤120s,4attempted=4valid/0unknown RSS; sampled peak55107584B<1GiB. Отдельный1N/A proof устанавливает poll returncode0 **до** RSS attempt для того же PID2967949; не выдаёт unknown за0sample. TMP6samples, all-entry peak78376B<32MiB, regular peak78096B; initial/final измерены. Raw138B<2MiB; no overrun. Sampled metrics доказывают эти observations, не hard transient maximum/квоту.

Root READY SHA `5b4ce388abc24b39ee75ad3b8cba60fa7b1eefc6d7a3b2b66b6c53a0841d415b` совпал с receipt; handoff SHA `01ae3f818baa39f22437d9d9248fea51eaa291536715478e829b60b358cfd085` совпал с READY. Root outer SHA `96bb3ab30a544e73e7e5739fe218919e66aa8bdd7e0700244767418e11975339` сохраняет wrapper_returncode0/no outerfailure. Root controller current source SHA `08bc98d19a22eeda32fba924091ef166f0cd6926214bb7f8bc2c96a359f87607` прочитан, не исполнялся.

Early admission failure отдельно сохранён: `/tmp/qcl-docs-routing-source-Root-admission-1-failure.json` SHA `fa98ca62417b3f1e4567be0c35b1e27f59f1c86889fa9b5473667bd7d5634043`; raw SHA `48f8f081a3d60f94524feaf6325002e1a719d2d238fddeb142450f04785e6524` показывает short-circuit stat assertion на64MiB executable cap до binary read. Retained record отмечает before-guard/reservation/READY/backup failure и formatter_calls0; subsequent FORMAT1 — один guarded submission, не повтор child. Это не повод скрыть initial failed admission или сбросить счётчик. Полный historical controller buffer до correction отдельно не исполнялся/не реконструировался.

Fresh read-only coordinator HEAD107bac… совпал с handoff; CP read-only snapshot502579B дал source counter3/product87, source/target active=null. Это metadata snapshot, не разрешение следующей фазы. FORMAT1 shared source2→3≤8, unit87unchanged. Isolated base2bb отдельно от global107; будущий Root handoff должен снова установить freshness.

## Решение и оставшиеся gates

Приняты exact format-only equivalence, final pure closure и FORMAT1 outcome в узком source scope. Теперь Root может использовать этот report как substantive review reference в **отдельно авторизованном** LINT/CHECK handoff с final maps. Reviewer их не запускает и не создаёт READY. Затем требуются all3accepted source receipts и unit source evidence/Root admission; sole GREEN230/native/fullCI/science не установлены.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Before/final source formatter-equivalent | Полный1868-line diff; literals/regex/template/ASI/control flow reviewed | Без parser/compiler execution | сохранить |
| Final pure closure сохраняет accepted slice | Helper38a56/fixture8946, only fake executor/import edge, CPP4903pure-only | Whole native CPP не PASS | сохранить |
| Static230 registrations/names сохранены | Before count227+3, unchanged loops+42callsite prefixes/full diff | Observed=null; unit не запускался | сохранить |
| Sole FORMAT1 и sampled guard complete | Exact receipt/raw/READY/handoff/outer,4valid0unknown+1provenN/A | Не LINT/CHECK/typecheck/unit/OS hard quota acceptance | сохранить |
| LINT/CHECK/GREEN/native/CI/science приняты | Соответствующих результатов в этом review нет | Нужны отдельные remaining gates | данных недостаточно |

Budget: conservative logical reads≤3MiB при cap4MiB, включая502579B read-only CP; wall<600s,1CPU/1GiB, report+identity<128KiB. Physical CPU/RSS/I/O reviewer не измерялись. Prepared-code/parser/compiler/runtime/tests/network executions0, source/CP writes0.

**PASS_FORMAT_ONLY + PASS_SOURCE_PURE_CLOSURE (pure_only_slice=true); no READY/runtime grant.**
