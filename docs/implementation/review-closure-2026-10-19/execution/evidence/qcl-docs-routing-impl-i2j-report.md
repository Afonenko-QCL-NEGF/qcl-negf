# I2J: focused native TAP R1/R2

**Source candidate; STOP fresh independent high CPP.** Изменены только
ops/docs_tests_native.py::validate_unit_report и независимые literal controls
в tests/test_docs_test_native.py. Worktree HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`.

Входной I2I review SHA256
`eb81697fe8339decc511e47c6d82178cfeeb6008abeda823e1b84cefa4ab0acd`
и identity `1397b31314a48c56871d4ea9d4368d639963963e3a8d2e4f469422d39748e2d0`
сверены. До правок exact old4 source bytes сохранены в
`/tmp/qcl-docs-routing-i2i-before-i2j`; manifest.sha256:4 OK, backup<2MiB.
Accepted I2I header/directives/seven-counter correction сохранена.

**R1.** Native TAP gate отдельно запрещает case-insensitive ASCII
`Bail out!|not ok` anywhere в stdout, включая success-result name и comment.
Это не result-only SKIP/TODO gate: оба independent условия сохранены.

**R2.** Только TAP branch получил local explicit ECMAScript trim character
set: TAB/LF/VT/FF/CR/SPACE, NBSP, OGHAM SPACE, U+2000–U+200A, U+2028/U+2029,
U+202F/U+205F/U+3000/FEFF. stderr trim и stdout trimEnd используют именно этот
set, не Python default strip. U+0085/U+001C/U+180E не исчезают как whitespace.
Планы, result IDs, counters и duration используют ASCII [0-9]; result/Subtest
bodies исключают CR/LF/U+2028/U+2029, сохраняя ordinary Unicode names.
Нет CRLF/Unicode normalization всего report или general parser framework.

Root снял первоначальный вопрос о per-line `$` по первоисточнику
[ECMAScript CompileAssertion, Assertion::$](https://tc39.es/ecma262/multipage/text-processing.html#sec-compileassertion):
при отсутствии Multiline требуется actual end; per-line result/full grammar
не имеют m, в отличие от global failure/directive guards. Поэтому сохраняется
literal fullmatch. Whole-report trimEnd удаляет только конечный JS whitespace,
а line-final CR/U+2028/U+2029 перед следующей строкой остаётся invalid layout.
Это source citation/решение Root; web/runtime/parser probes здесь не выполнялись.

Fixtures написаны перед production correction, без shared production oracle/
pure import. Пары Node+Deno: inline/mixed-case failure tokens и nearby valid
ASCII names; ordinary Unicode, NEL внутри name, Kelvin ordinary-name boundary;
NEL/control stderr и trailing stdout отказ; JS whitespace/BOM positive trim;
internal CR/U+2028/U+2029 result/Subtest отказ; line-final terminators перед
следующей plan/counter line отказ с healthy counterpart; Arabic duration и
fraction отказ, ASCII1.2 positive. Последняя уточняющая line-final matrix
добавлена после решения Root, без исполнения. Existing typed summary и
Python unittest20 branch/fixture не менялись. Node counters, exact header,
directive boundary pairs и plan/count/ID controls I2I сохранены.

TS pair byte-identical I2I, pure/config/ops/git/CP/Git index/commits не менялись.
Eight gitlinks остались прежними uninitialized; статус owning paths сохранён.
Выполнены source/hash/Git reads, frozen manifest4 OK и diff --check двух changed
files без whitespace diagnostics. Nominal8 Python methods/8 Deno registrations
сохранены. Все scripts/import/parser/compiler/tests/formatter/linter/solver/
native/network/CI/science executions0; children0.

Root counters product91/91 и source12/12 EXHAUSTED не увеличивались. E1
software-looking232 не используется как accepted result: resourceFAILED,
44 valid/1 unknown captured Z/noVmRSS сохраняется; independent TAP outcome
review — отдельный gate. Нет waiver/rerun/RSS-fixed/native READY/S1 claims.
Historical reports/failed raw не менялись.

Exact I2I→I2J delta7512bytes, SHA256
`5c20f5aa4c81ac303fbd97d3cc1446d13f93d961b503dd3242272a6f08dba305`.
Old4/new4 hashes — companion identity. Следующий шаг только fresh high CPP.

Ledger:8min/1CPU/1GiB/read≤6MiB/output≤96KiB, каждый chunk≤3000chars.
Один early selected-source response дал truncation; per-chunk3000 compliance
не подтверждено. Остальные outputs короткие. Exact aggregate transcript bytes,
physical I/O/CPU/RSS не измерялись; conservative source/hash/diff read estimate
5MiB, полного метрического compliance claim нет. Никакого target execution
для измерения или исправления ledger не добавлено.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1/R2 исправлены в native reader | Exact narrow diff и independent literal pairs | Source-only, fresh CPP впереди | дополнительно измерить |
| Python20 и accepted I2I controls сохранены | TAP-local branch, unchanged old fixtures/summary | Не runtime outcome | сохранить |
| E1 ресурсно принят/RSS cause устранён | Нет; resourceFAILED остаётся | Unknown sample не waived | данных недостаточно |
| Native READY/S1 получены | Не выполнялись | Прежние B3/B4/BIND gates остаются | данных недостаточно |
