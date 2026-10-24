# DOC06 adapter v2 — independent high collated-correction recheck

**PASS_SOURCE — R1 и R2 закрыты.** Conservative guards устраняют оба ложных known field defaults, сохраняя healthy flat extraction. Прежние test assertions неизменны; добавлены ровно два независимо paired controls. Новых blocking findings в correction не найдено. Sole GREEN остаётся неисполненным reviewer и принадлежит Root после exact binding.

## Frozen packet

| Input | SHA-256 |
| --- | --- |
| current `ops/docs/static-slice.ts`,40336 B | `b56713b6534013511fb392b8dd403a76b01798fdf3a7338c6f6215cf17de7fc5` |
| current `tests/docs_static_slice_test.ts`,28755 B | `373354120983c1ecf9f591c09ff4b108e614567d58409ea6abbeae8704c52290` |
| `/tmp/qcl-doc06-impl-v2.patch`,70634 B; hash verified, not applied | `c14b4f0a3d101a633ade0f0dfabdf263509f941916e3831a5efd84f02f80190c` |
| preserved v1 production,39087 B | `524582ec31305b6f34688b8f3e2fe1cd9c2ac03ae8d75ea1d46db2ee1144c128` |
| preserved v1 test,27631 B | `2957b182f531bf08895ca705d8ad4d81d5d736a79ebef8b1ae7541989cb0dfa2` |
| adapter delta,4871 B | `46487ee003fc5bf7b57076a11d51c87eda9a2065959bafaafc92964d968152d0` |
| test delta,1793 B | `6e2c8b92fa5a9f7edaf6cd5aca9d91343195f180cd6d77e943955fbdb8bf1bfe` |
| prior CPP | `34307c58f4a98d7aca2c028fd39f28794c82cd1c415872b955ce15a40ad2b958` |
| selected Core `src/numerics/optimized/production_contracts.jl`,15596 B | `ebb614494b4e58477231dbaf25a5283e8867e1c612859b2e26690c167b61a019` |

Worktree `/tmp/qcl-doc06-worktree`. Frozen D34b80d/D-R385c2ae4 не менялись и не переаудировались глобально. Exact independent v1→current text diffs прочитаны и совпадают по содержанию с двумя frozen deltas. Author v2 report не требовался для source verdict и не использован как доказательство исправления.

## R1 — CLOSED

`JuliaText` получает private `hasCmd`. В `juliaText` после comment branches и до ordinary string branch backtick открывает bounded scan с escapes, маскированием offset/newline и `hasCmd=true`. Cmd interpolation/nesting не интерпретируются. `typedDefault` сразу возвращает `unsupported_command_literal` при этом флаге. Поэтому даже неполная поддержка Cmd grammar не может восстановить ложный known field из этих bytes. Файл с таким контекстом остаётся conservative unsupported для typed extraction.

Typed API header получает такой же conservative `!hasCmd` predicate; documented literal handling и прочие API/fact shapes не изменены. Backticks внутри уже masked ordinary/triple strings или comments не становятся Cmd execution; новых target-loading/evaluation paths нет.

Первый literal negative содержит ровно прежний reproducer: `note::Any` с multiline Cmd body `energy_chunk::Int=64`, без настоящего energy_chunk field. Hash/size для него формирует existing fixture preparation, не stale-receipt отказ. Expected unsupported helper требует **non-refused** projection, null typed-default, partial/unknown status и reason; literal example31 и canonical schema constraint должны сохраниться. Negative не может пройти за счёт blanket refusal.

## R2 — CLOSED

После existing struct/end bounds `typedDefault` требует flat nonempty typed field lines и отвергает block/method keywords. Конструкторная строка `function ProductionOptions()` и `new()` не являются допустимыми field lines; keyword predicate дополнительно отвергает function/body context. Поэтому first `end` больше не позволяет local assignment стать field default: region маркируется `unsupported_nested_struct_context` до поиска digits.

Второй literal negative совпадает с independent constructor reproducer из prior R. Он также требует null/partial-or-unknown/reason без refusal, unchanged example31 и independently expected schema constraint. Это отдельный oracle, не следствие Cmd flag.

Healthy pair **в каждом** из двух appended cases использует прежний `sources(64,31)` и требует known literal typed64 плюс explicit31 до запуска adversarial sibling. Таким образом исправление «все Core sources unknown» не удовлетворяет controls.

## Healthy source и отсутствие contract drift

Selected Core source дополнительно сопоставлен с новым flat predicate: actual `Base.@kwdef struct ProductionOptions` содержит indented typed fields, literal `energy_chunk::Int=64`, comments и ordinary one-line opaque RHS. Comments маскируются; поля с `Union{Nothing,Function}` не совпадают с lowercase block-keyword test. Existing global `@eval` других symbols не переносится в выбранный field region. New field guard не требует вычислять typemax/constructors других полей. Для показанного healthy region условия known64 сохраняются по source trace, **не по Julia execution**.

Independent test diff — только appended22 lines после полного прежнего prefix; ни один existing assertion/fixture/cap/BufferSource ownership fix не переписан. Два table entries создают два Deno.test registrations, manual count54→56; каждый содержит собственную healthy/negative pair. Expected values literal и не выводятся production recognizer. Новый private lexer flag/reasons не меняют Fact shape, wrapper/public schemas, source graph authority, fixed paths/owners, caps, modes/origins или I/O/CLI contract.

Production delta ограничен Cmd state/flag и flat-region guard; file read/hash/path/schema/YAML/source receipt/publication/determinism/resource handling не меняются. General Julia parsing или runtime declaration inventory не вводятся. Conservative unsupported остаётся принятым результатом, effective origin/run/release не восстанавливаются. Known count13 duplicate-path coverage limit из прежнего fixture R остаётся прежним.

Полный implementation source повторно глобально не проверялся; остальные scoped выводы prior CPP сохраняют их ограничения. Это narrow recheck двух accepted findings и их regression controls, не доказательство всех возможных Julia syntax forms. Никакого target evaluation path новой коррекцией не добавлено.

## Runtime, budget и ledger

Reviewer target runtime/import/parser/typecheck/tests/format/build/network/server/children/product writes/Git/CP/checkpoint/C08/science — **0**. Original RED compile-stage TS2307+TS2345 сохраняется; его нельзя повысить до behavioral acceptance. Этот report не потребляет sole GREEN и не создаёт дополнительный call. Root связывает exact source/test/harness/operation и отдельно классифицирует original GREEN raw/receipt. FullCI/native/shared-format/public/scientific acceptance не наследуется.

Envelope≤10min/1CPU/2GiB/read2MiB/output96KiB. Консервативный ledger списывает full file за каждый text extract/search/hash/diff; повторный анализ использовал cached output.

| Group | Upper bound B |
| --- | ---: |
| Current production/test/fullpatch + prior R SHA pass | 155658 |
| Current production extract + test tail, full files charged | 69091 |
| Adapter/test delta full texts | 6664 |
| Independent old/current production+test diff | 135809 |
| Preserved v1 production/test + two delta SHA pass | 73382 |
| Selected Core extract + SHA pass | 31192 |
| **Total source-read upper bound** | **471796** |

Metadata/inventory и собственные review artifacts отдельно; physical I/O/RSS не измерены. Исторические failed/interrupted resource/runtime attempts не переписывались и не пересертифицировались.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Cmd bytes больше не дают ложный known field | New hasCmd/masking/early unsupported + independent pair | Source-only, не generic Cmd parser proof | сохранить |
| Constructor local assignment больше не field default | Flat-line/block guard + distinct pair | Source-only, supported flat grammar намеренно узкая | сохранить |
| Healthy literal64 и прежние assertions сохранены | Selected Core region, two healthy siblings, exact diffs | Runtime/typecheck ещё не измерены reviewer | сохранить |
| Packet готов к Root sole GREEN | Exact corrected hashes и prior frozen contract | Root binding/admission/counter отдельно | сохранить |
| Product/native/public/science accepted | Нового execution evidence нет | Source PASS не runtime acceptance | данных недостаточно |

**STOP. PASS_SOURCE exact collated correction; sole GREEN остаётся Root.**
