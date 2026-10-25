# Независимый high source CPP v6: локальные lint comments и source guards

Вердикты: **PASS_SOURCE** для exact v6 guard/plan/трёх wrappers; **PASS_COMMENT_ONLY_PURE_CORRECTION** для двух точных вставок; **PASS_SOURCE_PURE_CLOSURE** для текущей пары helper68f0…/fixture2639… в explicit pure-only slice. Блокирующих замечаний в этом узком source diff не найдено. Это source acceptance, не READY, не допуск исполнения и не наблюдённый FORMAT2/LINT2/CHECK1/GREEN PASS.

Проверены реальные v5→v6 diff guard/plan/wrappers и immutable postFORMAT1→current diff, а не только авторский narrative. Подготовленные scripts не импортировались/не исполнялись; parser/compiler/Deno/runtime/tests/network/native не запускались. Изменены только настоящие review artifacts в /tmp. Root, CP, source, исторические receipts/raw/index не редактировались. Новые controls/admissions и фактические три source calls принадлежат Root отдельно.

## Точная граница comment-only approval

| Файл | Frozen postFORMAT1 SHA256 | Current comment baseline SHA256 |
| --- | --- | --- |
| ops/docs_tests.ts | 38a56bff45bd7f7e36e8eb1a4542756b5225388d53827b6c24c73c9b059dc62b | 68f0efb5b45a03f130a52d14279e427c83c11b317a3c244e43375dbac5b8d3f5 |
| tests/docs_test_routing_test.ts | 8946e323023da597629f669dcb60c17bb6674f9c5a9bd9e2492dea280c35f16b | 2639be2132a88adb3e1ccd204112180efa065089e9ade5cae87e38c970952f99 |

Frozen files взяты из /tmp/qcl-docs-routing-pure-format1-frozen-v5; manifest SHA256 ed50c4ec8c8ba1b88ce93fdc8778c317446d08d716a799aa688771ed7c94846a. Независимо построенный unified diff побайтно равен patch916B SHA256 0ba7a8cdd4b18f7207acbd8f49c86e29b7012d8f25f19dfe8a0a14b6e60628e3. Удаление одной exact inserted line из каждого current файла побайтно восстанавливает соответствующий frozen файл.

В helper:200 добавлен только `// deno-lint-ignore no-control-regex -- Reject NUL..space/DEL, comma and backslash.` непосредственно перед прежним regexp. Буквальные regex bytes/flags и отклонение control/space/DEL/comma/backslash не изменены. В fixture:320 добавлен только `// deno-lint-ignore require-await -- Keep fake Promise returns and thrown errors as rejections.` перед прежним async execute. Async сохраняет Promise/rejection contract fake executor; dummy await и глобальное подавление lint не добавлены. Line comments стоят на отдельных строках внутри прежних syntactic positions, ничего не поглощают и не создают ASI-sensitive return/throw boundary.

Это намеренная локальная lint policy correction, отдельно от предыдущего format-only verdict. Prior FORMAT1 review SHA256 50b8d8d5c83d509df3928750a6ad947f8b779dcacaa2baa3b690c65f18b81ba2 сохраняет прежнюю цепочку original676a/f02f→postFORMAT1 38a/8946. Новый approved comment delta — только 38a/8946→68f/2639. Будущий FORMAT2 output SHA/receipt здесь неизвестен. Применимость directives к новой версии lint ещё не наблюдалась; LINT2 остаётся отдельным gate.

## Source guard, порядок и сохранение истории

Guard v6:204–224 требует exact `comment_only_cpp` schema `{status,pure_only_slice,before_sources,after_sources,patch_ref,prior_format_review_ref,report_ref}`, status PASS_COMMENT_ONLY_PURE_CORRECTION, true pure-only и точные old/new maps выше. Fixed patch/prior-format references сверяются по SHA; новый report_ref читается и хешируется. Это обязательный ключ unit READY (:348–351) и каждого source READY (:663–678), с повторной проверкой перед terminal source acceptance (:876) и через unit source_evidence (:227,:367,:546). Смысл/полномочия approval проверяет trusted Root: same-user JSON и hashes сами по себе не authentication.

CONTINUATION (:44–56) пинит v5 H/P, v5 safety review140472…, prior FORMAT1 review, frozen manifest/files, старые FORMAT1 receipt/raw, failed LINT1 receipt/raw и patch. Старый FORMAT1 receipt SHA256 d33fe2a43835ae48af6ff9a92d8abda2351bdac5e6ddff30c2590a216dba73a6 и raw b9f584e863bc07b513e9c6808e9e1eb0f6bdba3dc88377b983560b1316fa6919 остаются ancestry. LINT1 receipt SHA256 c14d85854326c2bd8bd6ac4fcd009fc57dc346e538dcd015b1f70a3b0bdadf10 и raw1279B c480b2473669fb26ad2b45494a09443e195eee25c4361ddda1399bb017e3f787 независимо перехешированы: child exit1, STOP_RECONCILE_NO_RERUN/source_child_nonzero_or_unknown, complete capture,3valid RSS/0unknown, ровно два сохранённых diagnostics. Guard :211–215 сохраняет failed/consumed classification. Эти artifacts не становятся good prerequisites.

SOURCE_STAGES :606 фиксирован: FORMAT2 fmt4→5, LINT2 lint5→6, CHECK1 check6→7 при ceiling8. `source_attempt` :619–620 даёт DOCS-ROUTING-SOURCE-FORMAT-2/LINT-2/CHECK-1; закрытый enum исключает произвольный номер. Exclusive folder mkdir (:715) сохраняет одноразовость; stage не запускает следующий stage. :695–705 требуют exact predecessor sets: пусто для FORMAT2, только FORMAT2 для LINT2, FORMAT2+LINT2 для CHECK1. Каждый predecessor проходит scope/stage/attempt/exit/capture/RSS/command/env/config/raw/source gates (:622–654), а не только exit0.

FORMAT2 допускает только текущий comment baseline и format_binding=None (:699–700). LINT2/CHECK1 требуют новый independent PASS_FORMAT_ONLY baseline68f/2639→actual FORMAT2 final плюс точный FORMAT2 receipt (:703–705). Unit :236–243 требует три distinct refs в порядке FORMAT2/LINT2/CHECK1 через zip и прямую проверку каждого receipt, новый format-only/final pure closure approval и comment-only approval. Старые FORMAT1/LINT1 не проходят новые stage/scope/failure predicates. Никакие будущие hashes/receipts в packet не сфабрикованы.

## Неизменённые safety predicates

Фактический guard diff не меняет принятый R1b/R2 safety behavior v5. Дополнительно inert source comparison подтвердил полное byte equality участка rss_tree/limits/receipt helpers и unit lifecycle, а также source reservation/watchdog setup. Три wrappers меняют exact v6 guard path/hash и fixed FORMAT2/LINT2 stage, сохраняя bounded owned regular buffer→SHA→compile/exec этого же buffer, no pyc, exact READY argv. Это обзор исходного lifecycle, а не его запуск.

R1b unit :468,:487–505 и source :798,:816–831: attempted устанавливается до RawCapture construction. Attempted+capture=None означает неизвестного владельца возможного non-daemon reader; competing fallback/read/close не выполняется. Сохраняется failed incomplete receipt с nullable raw/count и отдельно observed retained prefix, затем force os._exit под активным watchdog. Known capture thread проверяется terminal до alarm cancel (:596–603,:926–932); live reader ведёт к failed receipt/force exit. Receipt writes best-effort; disk failure/SIGKILL/host failure не получают обещания невозможной durability.

R2 unit observe :424–441 и source :758–771: только poll(), доказавший returncode до RSS attempt, даёт отдельное N/A proof с pid/returncode/time. Если процесс не proven reaped и rss_tree возвращает None, unknown сохраняется, failure ставится немедленно. Финальные gates требуют valid≥1 и unknown=0 (:561–563,:893–896). Predecessors :637–644 требуют unknown=0, attempted=valid+unknown и exact pre-sampling N/A proofs. Ретроспективный waiver отсутствует; старый DOC06 E1 unknownFAILED не пересматривается.

120s/108s stop,1CPU/1GiB sampled RSS/2MiB raw, source32MiB TMP/unit16MiB TMP, capture/error/terminal cap predicates не ослаблены. Sampled guards допускают gaps/overshoot и не доказывают hard peak/cgroup/disk quota. Environment остаётся complete replacement HOME/DENO_DIR/TMPDIR private directories без seed; unit argv grant-free/no-config/no-remote/no-npm/cached-only. Config strict/lineWidth100 SHA256 a637ff88ad0e1011480402de58895cb6d178eb1bbe98bdb27ca939b8821f6bce и runtime pin cdd88… неизменны. Runtime binary здесь не перечитывался целиком и не исполнялся.

## Pure closure и Root boundary

Удаление exact двух comments восстанавливает уже подробно reviewed postFORMAT1 source pair, поэтому current source сохраняет pure helper без imports/Deno API/real process/Git/env/filesystem/network/eval и fixture с единственным helper import и manufactured fake executor. Тела, import edges, loop bounds, test names, assertions/async/regex не менялись. Предыдущий finite registration audit 227+3=230 (42 textual callsites, expansion конечных registration loops) сохраняется. Это denominator Deno registrations, не число assertions и не наблюдённые 230 passes. Наблюдённый engine count=null; новых filter/only/skip/ignore options нет.

Explicit accepted CPP — только pure slice4903c3d64d8254a7b4ac89fcc08efed049485a21b1a1c155922b515b6118c4ea; whole I2B/native CPP остаётся CHANGES_REQUIRED. Native I2D,16native/integration/fullCI/science не включены. Historical v2 H/P/04589 fixture, полный TS2307+TS7006 RED raw, receipt и original inconclusive classification в diff неизменны. Новых RED/retry/unit calls не добавлено; sole unit DOCS-ROUTING-GREEN-1 остаётся87→88.

Read-only Git подтвердил coordinator Root HEAD107bac5697b37cf0e47c3feb44883a907837645c и isolated HEAD2bb05d3651af4509fe7f02c1253b40f1e5146fec. Root dirty CP/evidence и isolated I2B/I2D overlay учтены; Git status/submodule status прочитаны, восемь isolated gitlinks не инициализированы. Root и isolated revisions раздельны. Текущий CP counters показывает source_tools4 и product87; historical source_format_v5 entry3 отражает прежний FORMAT1 шаг. CP служит учётом, не issuer authority. Fresh actual Root HEAD/status/gitlinks/counters/control admission и SourceRef перед каждым actual call должен независимо проверить Root; новый controller данным review не проверен и не допущен.

Все семь v6 packet hashes и patch сверены с identity595fbd4fb60a9c622555e3b0f03a80e0eb8cc883b14c2ae51e38c1414b5ae397; точный source hash map сохранён в companion review-identity.json. Чтения ограничены source/metadata/logs, консервативно менее5MiB; review output менее192KiB. Физические CPU/RSS/I/O reviewer отдельно не измерялись. Запуски prepared scripts/parser/compiler/tests/runtime/network0, Root/CP/product mutations0.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Две локальные lint-policy вставки сохраняют software semantics | Exact patch916B; удаление двух строк восстанавливает frozen38a/8946 | LINT2 applicability не наблюдалась | сохранить |
| Guard v6 сохраняет R1b/R2 и finite stage ordering | Реальный v5→v6 diff, перечисленные locators, hashes | Source proof не runtime observation или run grant | сохранить |
| Current helper68f/fixture2639 сохраняют pure-only230 registration contract | Comment-only equality и prior detailed source audit50b8/CPP4903slice | Observed count=null; native whole CPP не PASS | сохранить |
| Старый LINT1 остаётся failed/consumed, новая цепочка требует3новых good receipts | c14d/c480 pins, guard204–243/606–705 | FORMAT2/LINT2/CHECK1 ещё не приняты | сохранить |
| Готовность actual source/unit исполнения установлена | Fresh Root controls/SourceRefs и actual новые receipts здесь отсутствуют | READY/admission/sole GREEN — отдельные gates | данных недостаточно |
