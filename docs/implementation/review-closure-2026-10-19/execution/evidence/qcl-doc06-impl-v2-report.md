# DOC06 implementation v2 — CPP R1/R2 correction source

2026-10-20. Узкий collated correction cycle перед тем же independent high R. Tests/runtime/imports/parsers/typechecks/format/network/build/commit/CP calls исполнителя: **0**. Root sole GREEN не потреблён. Это source handoff, не GREEN или native/scientific acceptance.

Base/worktree/branch прежние: Root `514cd9707a32cde60c630d60986973a898d35b18`, `/tmp/qcl-doc06-worktree`, `codex/review-closure-static-source-slice`. Product edits только `ops/docs/static-slice.ts` и append к `tests/docs_static_slice_test.ts`. Canonical, main/managed Root, harness, gitlinks, checkpoints и original RED raw не менялись.

## Frozen artifacts

| Artifact | SHA256 |
| --- | --- |
| CPP `/tmp/qcl-doc06-impl-review.md` | `34307c58f4a98d7aca2c028fd39f28794c82cd1c415872b955ce15a40ad2b958` |
| v1 adapter сохранён `/tmp/qcl-doc06-impl-v1-static-slice.ts` | `524582ec31305b6f34688b8f3e2fe1cd9c2ac03ae8d75ea1d46db2ee1144c128` |
| v1 test сохранён `/tmp/qcl-doc06-impl-v1-docs_static_slice_test.ts` | `2957b182f531bf08895ca705d8ad4d81d5d736a79ebef8b1ae7541989cb0dfa2` |
| v1 patch `/tmp/qcl-doc06-impl-v1.patch` | `4ee47106176f6527d71773a4887d8eb19d7d9e6ee2d62651acef49f828a18823` |
| v1 report `/tmp/qcl-doc06-impl-v1-report.md` | `3a2d7f87e2f2c9c6a2b551cafbee8d3af4b4ac3a7745b4d13cd2461ac6409105` |
| v2 adapter,665 lines/40336B | `b56713b6534013511fb392b8dd403a76b01798fdf3a7338c6f6215cf17de7fc5` |
| v2 test,513 lines/28755B | `373354120983c1ecf9f591c09ff4b108e614567d58409ea6abbeae8704c52290` |
| Full patch `/tmp/qcl-doc06-impl-v2.patch` | `c14b4f0a3d101a633ade0f0dfabdf263509f941916e3831a5efd84f02f80190c` |
| Adapter delta `/tmp/qcl-doc06-impl-v2-adapter-delta.patch` | `46487ee003fc5bf7b57076a11d51c87eda9a2065959bafaafc92964d968152d0` |
| Test delta `/tmp/qcl-doc06-impl-v2-test-delta.patch` | `6e2c8b92fa5a9f7edaf6cd5aca9d91343195f180cd6d77e943955fbdb8bf1bfe` |

V1 identity также сохранён как `/tmp/qcl-doc06-impl-v1-identity.json`; исходные report/identity/fullpatch не перезаписаны. Frozen D34b80…/D-R385c2… и выбранные component revisions прежние. Minimal owned ArrayBuffer hash fix остаётся approved source без изменений.

## R1: Cmd text

CPP source trace подтверждён по lexer/typedDefault: backticks раньше оставляли fake `energy_chunk::Int =64` видимым. Lexer теперь маскирует bounded backtick literal с escapes/newlines, не выполняя Cmd или interpolation. Наличие любого unmasked Cmd в selected file записывается как `hasCmd`; typed default этого файла возвращает `unsupported_command_literal`/null ещё до struct extraction. Typed API header также не повышается при hasCmd. Это намеренно консервативный отказ извлекать typed evidence в нераспознанном lexical context, а не общий Julia Cmd/interpolation parser. Backticks внутри уже замаскированных обычных strings/docstrings/comments не становятся Cmd.

Добавлен independent negative с literal CPP source: единственное field — `note::Any`, а target-looking assignment лежит внутри multiline Cmd. Matching receipt строится тем же существующим fixture writer с новыми raw bytes/hash/size. Assertions требуют null/partial-or-unknown/reason без blanket refusal, unaffected example31 и schema constraint1. В том же test сначала отдельный healthy flat ProductionOptions default64/example31 pair, не позволяющий сделать весь Core unknown.

## R2: inner constructor local

Перед target field matching recognizer теперь принимает только flat nonblank typed declaration lines. Любая non-field строка, macro context или nested block keyword в selected pre-end region возвращает explicit unsupported/null. Поэтому `function ProductionOptions()` в inner-constructor fixture отвергается до local `energy_chunk::Int =64`; первое найденное end больше не может превратить такую local assignment в known field. Default RHS других flat fields остаются opaque; no AST/body evaluation/general parser added.

Добавлен второй независимый negative по CPP literal constructor source, также с отдельным healthy64/example31 pair и untouched schema/example assertions. Existing source controls/assertions не изменялись и не ослаблялись; два new Deno.test cases appended. Номинальный count теперь56 (не collected/runtime measurement). Здоровая reviewed flat ProductionOptions region с typed fields остаётся поддержанной; реальные constructor/multiline/block forms консервативно unsupported даже если семантически допустимы Julia.

## Проверки и limits

Только Git/text/hash operations, просмотр collated CPP и изменённых regions; `git diff --no-index --check /dev/null` обоих files не нашёл whitespace errors. Форматтер, parser, typecheck и tests не запускались. Поэтому compile/behavior claims не повышаются. First RED остаётся историческим **TS2307+TS2345 compile-stage** результатом, не behavioral guard proof.

Delivered fullpatch+two deltas+report+identity укладываются в96KiB. Named logical read верхняя оценка <1MiB, ниже2MiB; включая обязательное сохранение v1, repeated file-equivalent diff/hash reads. Сохранённые source/patch copies — требуемые архивные артефакты, не новая ревизия продукта. CPU/RSS/kernel physical I/O не инструментированы. No new runtime capability/dependency/model/threshold/API decision.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Cmd literal не считается полем | Mask+hasCmd early unsupported; independent paired negative | Source-only, execution0 | сохранить |
| Constructor local не считается struct field | Flat-region gate до target matching; second paired negative | General Julia grammar не поддерживается | сохранить |
| Existing controls/byte oracle сохранены | Test delta только appended two cases | Compile/GREEN ещё не выполнялись | дополнительно измерить |
| Product/native/science accepted | Таких receipts нет | Independent R и sole Root GREEN впереди | данных недостаточно |

**STOP до того же independent high R; sole GREEN принадлежит Root.**
