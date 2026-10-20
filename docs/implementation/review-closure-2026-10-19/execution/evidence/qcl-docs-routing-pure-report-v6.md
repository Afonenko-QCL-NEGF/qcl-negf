# Pure routing v6 — два lint comments и конечное source continuation

Внесены ровно две разрешённые строки comments в owning pure files; подготовлены
новые guard/plan v6 и FORMAT2/LINT2/CHECK1 entries. Исполнений0. STOP перед fresh
independent high review comment-only correction и exact v6 package. Root
сохраняет владение actual formatter/control/admission. CP/control/index,
native4 I2D paths, source config и старые artifacts не менялись.

В helper непосредственно над intentional regexp добавлен локальный
`deno-lint-ignore no-control-regex` с причиной reject NUL..space/DEL, comma,
backslash; regex bytes/flags остаются прежними. В fixture непосредственно над
async fake execute добавлен `deno-lint-ignore require-await` с причиной сохранить
Promise return и rejected throws. Async/body/regex/assertions/registrations
не изменены, dummy await/global disable отсутствуют. Patch916B содержит только
эти2insertions; SHA `0ba7a8cdd4b18f7207acbd8f49c86e29b7012d8f25f19dfe8a0a14b6e60628e3`.
Это намеренная локальная lint policy correction, не ложный format-only шаг.

| Path | Immutable postFORMAT1 | New comment baseline |
| --- | --- | --- |
| ops/docs_tests.ts |38a56bff45bd7f7e36e8eb1a4542756b5225388d53827b6c24c73c9b059dc62b|68f0efb5b45a03f130a52d14279e427c83c11b317a3c244e43375dbac5b8d3f5|
| tests/docs_test_routing_test.ts |8946e323023da597629f669dcb60c17bb6674f9c5a9bd9e2492dea280c35f16b|2639be2132a88adb3e1ccd204112180efa065089e9ade5cae87e38c970952f99|

Сохраняется явная цепочка original676a/f02f → единственный FORMAT1 final38a/8946
→ две comment-only вставки68f/263 → будущий FORMAT2 final (пока неизвестен).
Immutable postFORMAT1 frozen manifest ed50… и оба frozen files не редактировались.
Accepted format/final pure CPP ref50b8… связывает только прежний format шаг;
он не утверждает approval новых комментариев. V6 READY требует **новый**
comment_only_cpp с PASS_COMMENT_ONLY_PURE_CORRECTION, explicit pure_only_slice,
exact before/after maps, patch/prior-format refs и independently approved
report_ref. Writer такого approval/READY не создаёт.

Source LINT1 завершился единственным child exit1: retained receipt c14d…,
original raw1279B c480…,3valid RSS/0unknown, complete capture. Две findings —
intentional no-control-regex и require-await. Он остаётся failed/consumed,
не превращается в good prerequisite. FORMAT1 receipt d33f…/raw b9f5… и
accepted review сохраняются только как ancestry. Guard CONTINUATION прямо
перехеширует v5 H/P/accepted review, immutable frozen baseline, format1 receipt/
raw/review, failed lint1 receipt/raw и correction patch. Предикат failed LINT1
сохраняет source maps, exit1, failure verdict/reason; hash pinning сохраняет все
прочие exact observations. Результаты не перезаписываются и счётчик не сбрасывается.

Новые distinct entries и IDs:

| Entry | Attempt | Source counters |
| --- | --- | --- |
| FORMAT2 | DOCS-ROUTING-SOURCE-FORMAT-2 |4→5|
| LINT2 | DOCS-ROUTING-SOURCE-LINT-2 |5→6|
| CHECK1 | DOCS-ROUTING-SOURCE-CHECK-1 |6→7|

Ceiling8 сохранён; это явно порученное continuation после comment correction,
не alias/retry старого LINT1. source_attempt теперь берёт номер из fixed stage,
поэтому CHECK1 сохраняет1, новые format/lint получают2. Stages не запускают
следующий stage. FORMAT2 требует exact new comment baseline + accepted new
comment CPP; LINT2 — новый FORMAT2 receipt/raw и independent format-only
new-baseline→final binding; CHECK1 — новые FORMAT2+LINT2. Unit принимает только
три **новых good** receipts FORMAT2/LINT2/CHECK1 в этом порядке, новый comment
CPP, новый format-only/final pure closure review и fresh Root handoff.
FORMAT1/LINT1 в эти slots не проходят по stage/scope/attempt/failure predicates.

R1b/R2 safety behavior не менялся: attempted-before-constructor, unknown collector
ownership→failed/incomplete receipt+force exit под активным watchdog; known
non-daemon thread terminal проверяется до alarm cancel. Live attempted RSS None
сразу failure, final unknown=0/valid≥1, predecessor counters/proofs строгие.
Только poll-proven terminal **до** RSS attempt получает отдельный N/A proof;
retrospective waiver нет. Original raw retention, fallback/overrun failures,
108s early stop и120s alarm, exact-buffer wrappers/helpers без pyc прежние.

Caps unchanged:1CPU/1GiB sampled RSS/120s/2MiB raw, source32MiB TMP, unit16MiB
TMP. Runtime cdd88…/Deno2.8.3, config a637… strict/width100, source exact2paths,
unit no-config/grants-empty, private HOME/DENO_DIR/TMPDIR/no seed. Fake-only
fixture→helper closure и positive CPP4903 **pure slice** не расширены до whole
native CPP. Static230 registrations сохраняются comments-only diff; observed
engine count остаётся null. Source compiler CHECK1 и sole GREEN не выполнялись;
unit ID DOCS-ROUTING-GREEN-1/global87→88 неизменён.

Historical v2 H/P/RED04589/receipt/raw/erratum/high-review и полный normalized
TS2307+dependent TS7006 layout не затронуты. Original inconclusive и DOC06
unknownFAILED сохраняются. Versioned v6 predecessor ещё не создан. Isolated
base2bb отдельно от fresh global Root HEAD; SourceRef issuer только trusted
Root, CP file не authority marker. Никаких new RED/native/full-CI/science.

Авторская проверка: immutable before→current GNU unified diff ровно2comment
insertions, named source sections, SHA/size. Parser/scripts/compile/import/
formatter/linter/tests/runtime/Deno/Julia/native/network0. Diff не доказывает
будущую lint directive applicability — это проверяется отдельным LINT2 после
high review; fallback/повтор автоматически запрещены. Начальный batch вывод
был truncated, нужные source/receipt/raw/frozen metadata перечитаны отдельно.
Grant15min/5MiB reads/1CPU/1GiB/192KiB output; conservative reads<5MiB,
deliverables<128KiB. Physical CPU/RSS/I/O не измерялись.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Изменены только2targeted comments | Patch916B, exact frozen before/current maps | Нужен новый comment-only CPP | изменить |
| LINT1 не выдан за passed prerequisite | Retained c14d/c480 bytes, failure check, новые2/2/1IDs | Новый LINT2 ещё не выполнялся | сохранить |
| V6 конечен в исходном budget |4→7≤8source, unit87→88sole, unchanged caps/safety | Fresh high/Root admission обязательны | сохранить |
| Accepted format2/CPP/unit/native/CI существуют | Таких receipts/approval ещё нет | Исполнений0 | данных недостаточно |

STOP: fresh independent high comment-only+v6 source review, затем Root.
