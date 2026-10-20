# DOC06 — implementation source handoff перед CPP/sole GREEN

2026-10-20. Исполнитель выбранной Sol/medium роли. Source-only implementation по accepted D/R и test-facing interface; **не runtime acceptance**. Единственный Root RED уже выполнен координатором. Исполнитель не запускал target runtime, parsers, typecheck, tests, builds или network. Root единолично владеет одним оставшимся GREEN после независимого CPP. Третьего автоматического вызова нет.

## Source identity и permitted diff

Worktree `/tmp/qcl-doc06-worktree`, branch `codex/review-closure-static-source-slice`, base HEAD `514cd9707a32cde60c630d60986973a898d35b18`. Selected source authority остаётся D: Runner `1acc165650fd4f4c2d49605cc679f90e3f6fcdae`, Contracts `12fc26462bbab3df76904c6deb01f8c6596de7be`, Core `e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee`; эти revisions не зашиты в production adapter. Он принимает derivable external receipt, не создаёт maintained revision lock.

Только два product-tree paths:

| Path/artifact | Размер / SHA256 |
| --- | --- |
| `ops/docs/static-slice.ts` новый | 643 lines,39087B; `524582ec31305b6f34688b8f3e2fe1cd9c2ac03ae8d75ea1d46db2ee1144c128` |
| `tests/docs_static_slice_test.ts` | 491 lines,27631B; `2957b182f531bf08895ca705d8ad4d81d5d736a79ebef8b1ae7541989cb0dfa2` |
| Full patch `/tmp/qcl-doc06-impl.patch` | `4ee47106176f6527d71773a4887d8eb19d7d9e6ee2d62651acef49f828a18823` |
| Test-only delta `/tmp/qcl-doc06-impl-test-delta.patch` | `d294e4eae87398ef614de69c56324195b8aaf8e9c7b75d00ab17f79e25138827` |

V2 source сохранён как `/tmp/qcl-doc06-impl-v2-docs_static_slice_test.ts`, SHA `13c33da622b4d1c2e779dda4221057617b8fbd10942824dec52cf78e19fe80f2`; v2 patch сохранён `/tmp/qcl-doc06-impl-v2.patch`. Старые reports, identity, v1/v2 sources/patches и original RED raw не перезаписаны. Main/managed Root, canonical docs, другие DOC04 files, component gitlinks/checkpoints/commits не менялись. Worktree submodules не initialized.

Authority: frozen D SHA `34b80d4ae1c8b94d23657124f17c9051251cea4763af8f92007d24929aafb2e8`, accepted D-R `385c2ae4358a7fb296399d6d955eb4d9ac5995c26f8baa2c27526ad11677d5ce`; v2 fixture R `de105…`, harness H `9bf3e58d14ee135ff047f045f12beac67310567febffd18d2a5005ce5c0ba32e`/R `293be95e…` из coordinator packet не изменялись и этим отчётом не пересертифицируются. Во время подготовки предварительно прочитан старый local-main docstring; затем selected Runner docstring/owning route явно перечитаны через immutable `git show 1acc165…`, и production meaning основано на них/D, не старом local-main тексте. Contracts и Core locators также сверены на selected commits.

## Фактический RED и TS2345 correction

Root original `/tmp/qcl-DOC06-RED-1/original.log`, SHA256 `0b7bfb1a1bb0379ea68de7258c827ba83b45369196a0c0384dacabfc7f50ec59`; receipt `/tmp/qcl-DOC06-RED-1/receipt.json`, SHA `d2029a30e2a1bddee31dce0e59e3889290ff683a7c8482f632bdd93dd25a089a`.

RED содержит **два compile errors**, не behavioral failure witness:

1. TS2307 — trusted adapter отсутствовал, ожидаемый missing-module error.
2. TS2345 в fixture hash helper — `Uint8Array<ArrayBufferLike>` допускает SharedArrayBuffer, тогда как Deno2.8/DOM `BufferSource` требует owned ArrayBuffer-compatible input. Эта проблема была непредвиденной в fixture source.

Минимальная коррекция helper выделяет `new Uint8Array(bytes.length)`, копирует `owned.set(bytes)` и передаёт `owned.buffer` WebCrypto. Byte oracle/algorithm/expected SHA/assertions/fixtures не меняются; нет cast, `--no-check` или weakening. Production SHA helper использует ту же реальную ownership-copy технику (без использования test helper как oracle).

Receipt координатора: 1.338s, sampled RSS264060928B, owned TMP332984B, raw1236B complete, guard_error/null, stop_reason/null. Это metadata Root attempt, не измерение исполнителя. Поскольку compilation остановилась, positive/negative controls, no-eval sentinels, cap guards и фактический adapter ещё не исполнялись. Ошибка типа сама по себе не доказывает refusal, bounded reads или физическую корректность.

## Реализованная boundary

Export сохранён: `generateStaticSlice({snapshotDir,sourceReceiptPath,outDir}) -> {status,reason?}`. Strict CLI: `--snapshot DIR --source-receipt FILE --out NEW_DIRECTORY`, ровно три уникальных известных флага с values, без extra options. При import trusted module нет file-I/O/CLI работы; CLI активируется только `import.meta.main`.

Adapter не имеет imports/dependencies, target loader, eval/Function/WebAssembly, process/run/env/net/FFI/config/plugin calls. Все выбранные `.jl/.json/.yaml/.md` — input bytes. Нет include/corpus discovery, Git subprocess/.git reads, установленного-package fallback или solver activity. Переданные paths не интерполируются из ENV. Test harness capability остаётся обязательной `Deno.args[0]` внутри owned `/tmp`; изменений harness/permissions нет.

Receipt format и private extraction interface соответствуют v1/v2 report. Проверяются fixed9 paths/owners, unique full paths, full40 revision/full64 SHA, safe integer byte sizes, graph digest, count≤12. Unknown/missing receipt entries/identity/namespace refusals не получают public facts. Missing actual selected file при корректном expected entry даёт `source_missing`, actual SHA/bytes=null и dependent unknown/partial без packaged fallback.

Snapshot root/receipt/output parent проверяются realpath/lstat; selected ancestors и final files не могут быть symlinks. Absolute/traversal/unknown receipt paths rejected. Snapshot/output overlap и existing destination rejected; existing output не затирается. Каждый file stat проверяется до ограниченной allocation; bounded open/read/stat использует не более size+1≤cap+1 buffer и не вызывает `readFile`, который мог бы неограниченно аллоцировать после stat. Raw bytes hash/length сверяются с receipt; text decoding strict UTF-8, extraction normalization LF отдельно отражена. Source receipt≤16KiB, file≤128KiB, aggregate≤512KiB проверяются до чтения/проекции. В receipt сохраняются expected и actual identities, missing не заменён нулём.

Filesystem race caveat сохранён: Deno stat/realpath/open не являются kernel no-follow transaction против adversarial concurrent namespace mutation. Frozen snapshot/единственный владелец fresh output — предпосылка. Checks не выдаются за аппаратные filesystem quota/RSS/physical-I/O guarantees.

## Извлечение, статусы и output

JSON data guard ограничивает container depth32, tokens32768 и decoded string16KiB; проверяет синтаксис, duplicate decoded keys, forbidden prototype keys, finite/safe numeric representation до full built-in JSON.parse. Это ограниченный precheck, не framework/dependency. Malformed schema даёт explicit unsupported reason и null selected observations; lexical overruns refuse. Canonical Contracts projection не заменяется packaged schema: packaged independently prechecked, raw hash mismatch — отдельный diagnostic.

Project только owning root required-production, selected production object/local ref chain, required membership и leaf type/minimum/default/description. Local pointers используют own properties и `~0/~1`, missing/cyclic/remote refs unsupported, >8 hops refuse. Root refs, unhandled selected keywords/combinators/ref siblings conservative partial; unused `$defs` data не интерпретируются как selected validation. Полный schema/instance validation не заявлен.

Julia lexer маскирует comments (включая nested block comments)/strings, сохраняя offsets/newlines. Associated literal triple docstring отделяется от assigned/string-macro literal; dynamic interpolation не извлекается как literal documentation. Header recognizer требует ровно два typed arguments и отсутствие default/where/macro context, выдаёт partial textual header вместо method inventory. `ProductionOptions.energy_chunk::Int = DIGITS` извлекается из literal reviewed struct region; dynamic RHS, comments/strings/duplicates/macros/unsafe literal дают null/partial. `Base.@kwdef` не выполняется; known относится к source field default, не созданному instance. General Julia parsing/runtime coverage не заявлены.

YAML support — только unique top-level production block и unique two-space decimal leaf с comment suffix; selected aliases/tags/anchors/merge/expression/duplicates unsupported/null. Other sections opaque. Никакого deep merge/config loading нет.

Для обоих subjects сохранены все ten Fact classes и exact `{name,status,text,sources}`. Documented signature/effects — literal docstring; schema declarations, typed default и explicit example раздельны; private receipt содержит mode/context/value/reason/selectors. Missing source не имеет fabricated PublicRef. Available source refs содержат full owner revision, repo-relative path, raw SHA и exact symbol/file/JSON-pointer selectors. Unknown actual assigning/effective origins не восстанавливаются из defaults или markers. Authored route excerpts (recorded assignment, synthetic fixture expectation, application:auto_exact policy) цитируются только при literal unique paragraph match, labelled authored/static, не computed merge/planner output. Физические formulas, threshold rationale/DOI/actual private filenames не генерируются.

Facts wrapper — `qcl-negf.doc06-static-slice.v1`, profile fixed, release/run=null, coverage fixed-slice/partial. Результат честно `partial`, поскольку ten classes включают unknown runtime context. Это local DEV prototype, не DOC03 shared Fragment/Bundle или public admission. Canonical UTF-8/LF JSON с two-space indentation/final newline, fixed ordering, без timestamps/host/temp paths/random IDs в facts. Manifest digest — hash raw supplied receipt, не доказательство upstream Git binding.

Перед output directory creation проверены fact text≤2048 chars, docstring≤4096B, signature≤512B, facts/receipt≤32KiB и diagnostics≤8KiB. JSON не усекается и classes не отбрасываются. Fresh output содержит private receipt, затем bounded `facts.pending.json`, после successful write rename публикует complete `facts.json`. Failed pending I/O evidence не удаляется; raw logs не затрагиваются. Atomic rename относится к fresh single-writer premise, не adversarial namespace guarantee.

## Проверка и limits

Выполнены только source/text/Git metadata/SHA операции и whitespace checks `git diff --no-index --check` для обоих files. Test delta просмотрен как одна owned-buffer коррекция. **Ни typecheck, ни parser, ни tests, ни target import не запускались исполнителем.** Compile correctness/behavior/54 controls пока не подтверждены. Existing count13 duplicate-path confound из v2 report сохранён; фактический implementation count guard стоит перед unique path validation, но отдельного runtime witness пока нет.

Named logical source/read allowance этого pass консервативно <2MiB при grant6MiB; включая repeated full-file equivalents selected sources, frozen D, собственные source/diff/hash reads. Output artifacts: adapter/test sources≈66KiB, full patch≈67KiB, component patches/delta/report/identity сохраняются в общем <256KiB envelope. Kernel/Git physical I/O, CPU/RSS cumulative telemetry отдельно не измерялись. Wall budget40min не используется как основание success; execution calls0.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Source-only adapter и minimal hash fix готовы к CPP | Exact source/test/fullpatch/delta hashes | Нет typecheck/runtime GREEN | сохранить |
| RED подтвердил behavioral guards | Original log: TS2307+TS2345 | Compilation остановилась до fixtures | данных недостаточно |
| Known source contexts отделены от actual origins | Fact/receipt modes и null effective/run context | Source recognizers не runtime/model validation | сохранить |
| Adapter проходит controls и finite runtime envelope | Execution evidence отсутствует | Единственный GREEN ещё принадлежит Root | дополнительно измерить |

**STOP после source implementation. Отдельный high CPP на этом frozen source до sole Root GREEN.**
