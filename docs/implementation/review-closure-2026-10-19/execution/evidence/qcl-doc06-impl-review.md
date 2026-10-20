# DOC06 production adapter — independent high CPP

**REQUEST_CHANGES — два P2 false-positive extraction paths.** Adapter не исполняет target source и в основном сохраняет accepted I/O/status/resource boundaries, но `typedDefault` может выдать known field default из Cmd literal или локальной переменной inner constructor. До sole GREEN нужны узкие консервативные исправления и literal negative controls. Test-only owned-buffer correction отдельно **APPROVED_SOURCE**; assertions не изменены.

## Immutable source/evidence packet

| Input | SHA-256 |
| --- | --- |
| `/tmp/qcl-doc06-worktree/ops/docs/static-slice.ts`,39087 B | `524582ec31305b6f34688b8f3e2fe1cd9c2ac03ae8d75ea1d46db2ee1144c128` |
| current `tests/docs_static_slice_test.ts`,27631 B | `2957b182f531bf08895ca705d8ad4d81d5d736a79ebef8b1ae7541989cb0dfa2` |
| preserved `/tmp/qcl-doc06-impl-v2-docs_static_slice_test.ts`,27558 B | `13c33da622b4d1c2e779dda4221057617b8fbd10942824dec52cf78e19fe80f2` |
| frozen D | `34b80d4ae1c8b94d23657124f17c9051251cea4763af8f92007d24929aafb2e8` |
| accepted D-R | `385c2ae4358a7fb296399d6d955eb4d9ac5995c26f8baa2c27526ad11677d5ce` |
| test-only delta,952 B | `d294e4eae87398ef614de69c56324195b8aaf8e9c7b75d00ab17f79e25138827` |
| full implementation patch,68217 B; hash verified, not applied | `4ee47106176f6527d71773a4887d8eb19d7d9e6ee2d62651acef49f828a18823` |
| author `/tmp/qcl-doc06-impl-report.md`,14367 B | `3a2d7f87e2f2c9c6a2b551cafbee8d3af4b4ac3a7745b4d13cd2461ac6409105` |
| original RED raw,1236 B | `0b7bfb1a1bb0379ea68de7258c827ba83b45369196a0c0384dacabfc7f50ec59` |
| original RED receipt,2453 B | `d2029a30e2a1bddee31dce0e59e3889290ff683a7c8482f632bdd93dd25a089a` |

Worktree base Root514; status содержит только new adapter directory и test. `ops/docs` inventory — только `static-slice.ts`. Selected Runner1acc165/Contracts12fc264/Coree431609 остаются frozen D authority; production не создаёт второй revision lock и не доказывает commit→bytes самостоятельно.

Порядок review: использованы ранее полностью прочитанные primary D/R с повторной проверкой hashes; затем полный production source, actual test-only diff и status. Первый finding передан Root **до** чтения author report. Report прочитан после самостоятельного source assessment и не заменял primary evidence. Никаких target runtime/import/parser/typecheck/test/build/network/commits/CP mutations reviewer не выполнял.

## R1 — P2: Cmd literal не маскируется и становится ложным default поля

Локаторы: `static-slice.ts::juliaText:220–259`, `typedDefault:292–307`, default publication :499.

Lexer распознаёт comments и `'`/`"`/triple-string delimiters, но не Julia backtick command literal. Поэтому field-like строка внутри multiline Cmd остаётся в `lex.mask` и подходит regex `energy_chunk::Int = DIGITS`. Это ошибочно публикуется как `known` literal source default с selector `ProductionOptions.energy_chunk`, хотя field отсутствует.

**Независимый literal source oracle, не исполнялся:** вместо Core source в existing matching receipt fixture:

```julia
Base.@kwdef struct ProductionOptions
    note::Any = `
    energy_chunk::Int = 64
    `
end
```

Реальный текстовый field здесь — `note`; строка `energy_chunk::Int = 64` принадлежит command literal. Статический trace: mask оставляет backticks и эту строку; structs.length==1; region до end содержит ровно один regex target; RHS digits64; функция возвращает64 без reason. `literal(...)` затем повышает typed-default до known. Это **не execution vulnerability**: target command не запускается. Это нарушение source-only extraction grammar/false evidence.

**Минимальная коррекция:** маскировать ограниченный backtick literal с escapes/newlines либо консервативно возвращать unsupported/null для такого контекста до field extraction. Не выполнять Cmd, Julia parser, shell или general macro expansion. Добавить negative с matching hash/size и healthy flat struct sibling; ожидать typed-default null/partial-or-unknown/reason и unaffected example31. Существующие dynamic/string/comment/sentinel assertions сохранить.

## R2 — P2: inner-constructor local assignment ошибочно признаётся struct field

Локаторы: `typedDefault:296–304`, особенно first `end` search :299 и flat line regex :303.

После struct header recognizer берёт всё до **первого** `end`, не устанавливая field-level scope и не отвергая nested method/body. Локальное typed assignment внутри inner constructor проходит тот же regex.

**Независимый literal oracle, не исполнялся:**

```julia
struct ProductionOptions
    function ProductionOptions()
        energy_chunk::Int = 64
        new()
    end
end
```

У struct нет поля energy_chunk. Но первый end завершает constructor, region до него содержит local assignment; regex допускает произвольную indentation и возвращает64. В false source fact появляется known field default, хотя исходник задаёт только локальную переменную constructor.

**Минимальная коррекция:** ограничить recognizer поддерживаемым flat declaration region и conservative unsupported для inner constructors/nested executable blocks/неподдерживаемого struct context. Не строить общий Julia AST/parser и не вычислять bodies. Добавить отдельный negative sibling для constructor case, matching source receipt и unchanged literal healthy default. Простое backtick masking R1 не закрывает этот второй путь; оба должны различаться controls.

Оба findings следуют из accepted D§4: только точный reviewed struct/field location и отсутствие promotion чужого literal/string/metaprogramming context. Known относится к source declaration, но даже такая declaration должна быть именно полем, а не текстом Cmd или local variable. Более консервативный partial/null допустим; ложный known — нет. Нового D/model/threshold/trust policy не требуется.

## Проверенные contract boundaries

**Нет target execution.** Production содержит zero imports/dependencies и не вызывает eval/Function/dynamic import/WebAssembly/fetch/process/run/env/FFI/config loaders. Модуль при import создаёт constants/encoder/decoder/functions; file I/O выполняется только при API call, CLI — только `import.meta.main`. Julia/YAML/Markdown/schema читаются как bounded bytes; JSON.parse используется как data parsing. Sentinel source reviewer не исполнял. No-eval property не следует из будущего exit code или только permissions, но source path для target execution здесь не найден.

**Namespace/identity/I/O.** Fixed9 allowlist/owner map, exact count9 after ≤12 guard, unique paths, full hash/revision/size shape и aggregate expected≤512KiB проверяются до selected reads. Receipt graph/revision labels не выдаются за upstream proof. Realpath/lstat checks и selected component traversal reject symlinks/special files; absolute escaping receipt paths не допускаются; out fresh и не пересекается snapshot/receipt. `boundedRead` предварительно проверяет regular file/size, читает size+1 buffer через open/read/stat и подтверждает actual size/hash. Missing expected file даёт null actual hash/bytes и source_missing, не zero/fallback. Frozen snapshot/single writer остаются внешними premises; kernel TOCTOU/bind-mount/hardlink security proof не заявлен.

**Resource guards.** File128KiB, receipt16KiB, source512KiB, count12 и fixed9; JSON depth32/token32768/string16KiB и ≤8 ref hops присутствуют. JSON lexical recursion/counters bounded, duplicates decoded keys/prototype/unsafe finite numbers проверяются до full parse. Literal strings отдельно bounded before whole JSON object parsing; это не измерение peak allocation. Facts/receipt32KiB, diagnostics8KiB, fact text2048, docstring4096 и signature512 отказывают вместо truncated classes/JSON. Output serialisation и limited string decoding сами аллоцируют bounded data; hard RSS/quota или physical IO из этого не следуют.

**Schema/source/unknown.** Canonical Contracts остаётся authority; packaged hash mismatch — diagnostic, не replacement. Direct required/type/minimum/default/description projections отделены от full schema validation. Own-property local pointers поддерживают ~0/~1; missing/cyclic/remote refs и unsupported affecting keywords дают partial/null, cap overrun — refuse. Unselected `$defs` data opaque; v2 paired cap controls согласованы с этим. Default declaration не применяется к configuration; schema absent default not_assigned, typed/example independent. API documented signature known, typed header partial/no exhaustive method inventory; actual assigning/effective origins unknown. R1/R2 ограничены ложной field extraction и не означают, что target execution найден.

**Output/determinism/failure.** All10 classes per subject, exact Fact shape, private extraction modes/selectors, source-prototype/null run/release и coverage partial сохраняются. Production всегда возвращает partial для честного limited projection. Canonical fixed output ordering, UTF8/LF/two-space/final newline и отсутствие runtime clocks/random IDs/temp-directory fields обеспечивают deterministic output для identical raw source receipt/source/profile inputs. `source_manifest_sha256` — raw receipt hash; semantic equivalence при иной whitespace/order receipt не заявляется этим review. Private raw receipt/input data не выдаются за shared DOC03 schema или accepted Bundle. Output directory создаётся только после successful projection/cap checks, facts публикуется последним через pending rename. I/O failure сохраняет bounded refused reason и pending evidence; adversarial atomicity не утверждается.

**Authored context.** Direct excerpts помечены documented/authored/source; no physical formula/rationale/actual used config invented. Статические слова о defaults/assigning policy не заменяют отсутствующий retained run context. Public refs имеют observed raw hashes и selected receipt revisions; missing input не получает fabricated ref. Dynamic/unsupported classification не повышается до scientific/model/native acceptance.

## Actual first RED и test-only correction

Original raw+receipt подтверждают **TS2307 missing adapter + TS2345 BufferSource generic mismatch**, exit1/wall1.338s/raw1236B complete/no guard error. Это compile-stage result; ни54 test bodies, ни sentinel/causal cap negatives не исполнялись. Runtime hint `--no-check` в raw — диагностический текст, не инструкция; implementation не добавляет такой bypass.

Independent v2→current test diff — ровно owned buffer allocation, `owned.set(bytes)` и передача `owned.buffer` в тот же SHA-256 WebCrypto call. Expected values, source fixtures, cap/sentinel assertions и counts не изменены. **APPROVED_SOURCE exact test delta**: копируются все исходные байты в собственный ArrayBuffer, не cast/skip/parser обход. Production hash helper использует такую же memory ownership technique, но не вызывает test helper как oracle. Typecheck/runtime success этой source оценкой не устанавливается.

Sole remaining GREEN принадлежит Root; review не исполняет и не добавляет call. До него нужны R1/R2 source repair, literal negatives и независимый narrow recheck на новых hashes. Original v1/v2/RED artifacts сохраняются. Generic full CI, DOC04 BUILD/native, shared DOC07/C2 integration и science не admitted.

## Named read ledger и действия

Envelope≤20min/1CPU/2GiB/read6MiB/output256KiB. Каждый source hash/search/extract/diff заряжен полным named file size; чтение затем использовалось из tool/context cache.

| Group | Conservative B |
| --- | ---: |
| Three source hashes + D/R hashes, production API search, test diff both files | 223866 |
| Full production read in3 text extracts, full-file charged each | 117261 |
| Author report text/search/hash after independent source verdict | 43101 |
| Original raw/receipt/testdelta text + raw/receipt/testdelta/fullpatch hashes | 77499 |
| **Total source-read upper bound** | **461727** |

Metadata/Git/file inventory и own review artifacts отдельно; physical I/O/RSS/time cumulatives не инструментировались. Target runtime/import/parser/typecheck/tests/build/network/server/children/product writes/Git mutations/CP/checkpoint/C08/science — **0**. Первичный OPS08 read-cap failure остаётся в собственном историческом отчёте и этим отдельным DOC06 CPP не пересертифицируется.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Cmd text может стать ложным known field default | juliaText:240–257, typedDefault:303–307, independent literal R1 | Source trace, regression не исполнялся | изменить |
| Constructor local assignment может стать field default | typedDefault:first-end region:299–304, independent literal R2 | Source trace, нет Julia execution | изменить |
| Exact buffer-copy correction сохраняет oracle/assertions | Full v2→current diff; TS2345 original raw | Нет нового typecheck/runtime | сохранить |
| Fixed I/O/status/no-target-execution contract преимущественно соблюдён | Полный production source и primary D/R | Два extraction gaps и no runtime GREEN | сохранить |
| Product/54 controls/native/science accepted | Original RED остановлен при compile; иных run receipts нет | Sole GREEN ещё впереди | данных недостаточно |

**STOP. REQUEST_CHANGES R1/R2; no GREEN/CP mutation выполнялись.**
