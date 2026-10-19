# DOC07 C1 RED test sources: независимое high review

2026-10-20. **CHANGES REQUESTED** на source SHA256
`c2fdf66a51a5b772e270cd520e1c560794c11a39c191bfe2ed8abc61e33bf684`:
одно узкое blocking test-strength замечание R1 к трём boundary+1 mutations.
Остальные examined shape/oracle sources пригодны; новой schema/proof semantics
не требуется. Tests/runtime/collection не выполнялись. STOP перед Root RED.

## R1 — три cap negatives проверяют ещё и duplicate row

Локатор `/tmp/qcl-doc07-contract-worktree/tests/test_model_help.py`,
`test_declared_array_caps:576,581,588`:

```
healthy['fragments'] + [healthy['fragments'][0]]
healthy['inputs'] + [healthy['inputs'][0]]
healthy['entries'] + [healthy['entries'][0]]
```

Positive rows до cap имеют уникальные id/path/point, но negative cap+1 добавляет
точный дубликат. Поэтому допустимый duplicate rejection, например uniqueItems,
отвергнет bad case даже при отсутствующем maxItems256/32/10000. Suite не
различит ошибку обязательного cap и не докажет заявленный isolated boundary+1.
Это source-вывод, не результат executed mutation test.

Минимальная правка: дополнительный fragment с новым id/file `pilot.256`,
additional view input с новым path `physical.public_leaf_32`, additional index
entry с новым point_id/path `P-10000`; остальные fields оставить здоровыми.
Каждая mutation тогда нарушает только cap. D2/primary743–746 и619–637 уже задают
эти limits; новых ограничений, допусков или test calls не требуется. Conditions
cap на строке594 **исправлять не нужно**: generated IDs pilot.condition-0…11,
а appended original id pilot.condition уникален. Первоначальное промежуточное
сообщение включало conditions ошибочно; вывод после чтения entries исправлен.

Категория: независимость negative oracle; влияние — ложная защита regression
maxItems в будущем GREEN. Контраргумент: корректная schema может одновременно
иметь cap и uniqueness. Это не устраняет test ambiguity: faulty schema с одной
uniqueness тоже проходит данное assertion. Решение: **изменить три negatives
до freeze/sole RED**, сохранить исходный snapshot и новый exact hash.

## 1. Source binding и read order

Сначала сверены published canonical Root DOC03 с append, accepted D2/high R и
Contracts12fc loader/messages boundaries; затем candidate tests/report/identity/
patch. Предыдущие full contract reviews применяются; source comparisons этого
review не переопределяют accepted schema-vs-proof границу.

| Input | Проверенный SHA256 |
| --- | --- |
| Canonical DOC03 | `fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794` |
| Accepted D2 | `20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b` |
| Accepted D2 R | `f62bbe6998b178ea746a3a28ae73e4e910c751742e0e7887ac4d77b63786b231` |
| New test source,30871B/624lines | `c2fdf66a51a5b772e270cd520e1c560794c11a39c191bfe2ed8abc61e33bf684` |
| Author report | `844f6e1f9124237a27241be4984b23cafa102c355073369a604b2aadb50ea68a` |
| Author identity | `90b1caebc279461d7b209916a8e2d3822949776a8608d4ba9737b29bc0164cb9` |
| Frozen test patch | `45d7cb0e2184363932da4ec5b5160b55cb453605a7935a562f9e404984b34d92` |
| Preserved tracked test_contracts.py | `0231b4d437ed3086a2cb365a0ce2a3926da93008d67e99df598e8aced6f63fd7` |
| Preserved loader __init__.py | `41b5b746bbf28cd0e60bb85bc927f1c55ba0ac2695f3271b875f83c057a744d1` |
| Preserved messages.py | `fd82f76a005519962b1edbfd5b9971f6e8d50c0806ca1f4070359e908fa205fa` |

Owning worktree `/tmp/qcl-doc07-contract-worktree`, HEAD
`12fc26462bbab3df76904c6deb01f8c6596de7be`. Actual status ровно
`?? tests/test_model_help.py`; tracked tests diff exit0, git diff --check
без сообщений. Production schema и model_help.py отсутствуют: два отдельных
shell existence checks завершились exit0. New patch additions, снятые с leading
`+` без header, совпали cmp с exact source. Ни tracked production, ни schema,
ни root/checkpoint рецензентом не менялись.

## 2. Пять literal factories и отсутствие tautological oracle

Bundle/Fragment/View/Snapshot/Index задаются literal public fields/format values
и synthetic scalar/reference metadata, а не извлекаются из будущей schema.$defs.
Factory inventory соответствует accepted required fields. PublicRef/DocRef,
Origin/Atom/Fact/Evidence, applicability, ValueOriginBinding/assignment receipt,
local/API contexts и effective steps представлены. Exact generator pins и
formal ScientificId/UUID/hash/selector values source-согласованы.

`object_paths(healthy)` перечисляет authored instance objects; closure/required
mutations проверяют каждый exercised nested object после healthy validation.
Это не schema-derived expected inventory. Единственное чтение schema tree
`test_resource_name_and_offline_local_refs` ограничено проверкой `$ref`/
`$dynamicRef` local-only; оно не строит expected data/assertions из schema.
Unrelated malformed record не используется как основа главных paired negatives:
`assert_bad` сначала вызывает validate healthy, затем меняет одну property.

Factories здесь **shape healthy**, не proof healthy: arbitrary hashes/example
URLs и literal statusbound не доказывают actual source/owner/release/origin.
Например meaning_source в fragment сейчас использует Research PublicRef через
generic helper, хотя actual owning explanation primary394 относится Core/Runner.
Не переносить этот объект как semantic-positive C2 source fixture; при желании
можно сделать его Core/Runner-shaped уже сейчас, но C1 не должен доказывать
ownership одной строкой component. Никакого существования blob/equation/HTML
anchor/source graph membership эти literals не утверждают. C2 semantic-positive
нуждается в своих checked bytes/context/proofs.

## 3. Examined matrices и property controls

| Контракт | Test source observation | Verdict/limit |
| --- | --- | --- |
| Five formats и unsupported/nonobject | Literal const format у каждого; wrong version и nonobject rejected; loader basename check | Meaningful shape contract; runtime ещё нет |
| Required/closure | Healthy validate → remove each key / add unexpected key каждого instance | Хорошая nested coverage |
| Ten facts/multiplicity | По inputs/api удалить каждый из10 names; repeated schema/typed/example defaults accepted | Не ошибочный max10/name-unique oracle |
| Atom | Все6 kinds, scalar arrays/objects/type cross-pairs, bool≠number/integer, quantity nonempty unit, known-null | Соответствует accepted matrix |
| Finite JSON | Existing validate_json/encode NaN/Inf/−Inf и decode NaN/Infinity/−Infinity/1e400, correct healthy token before mutation | Finite boundary отдельно от jsonschema |
| Origin/ValueOrigin | Known/unknown/N/A и matching kinds/locators/note; пять unknown reasons, bound/nonbound binding and Origin cross-pairs | Statusshape не actual proof |
| Docs binding/input status | Closed reason/null pairs; nonnull bound identities, known scalars survive unbound; trusted UUID/attempt; invalid/unavailable used unknown | Не склеивает documentation и metadata availability |
| Empty mapping | available/ok + inputs=[] + fragmentnull accepted | Наличие/отсутствие mapping proof отложено C2 |
| Scalar/assigning | Known Atom+Evidence, unknownnull; source-or-rule known, unknown strictnull, redacted sourcenull | Evidence truth/last assignment вне C1 |
| Snapshot | No actor/release/API-origin fields, solver_input phase, allowed step kinds, origin_bindings=[] допустим | No capture backfill |
| Index | valid/ok vs invalid reasons, measured bytes65537 for too_large, no leading-zero attempt/path grammar, completefalse[] | Inventory trust/aggregate byte guards C2/owner |
| Limits/references | Unicode character cap, IDs/digests/generator/DocRef, no permanent eight-leaf enum, no mandatory condition | Три array cap negatives требуют R1 |

Отдельная неблокирующая coverage рекомендация: положительные Fact.status
проверяются на unknown/known, но partial/not_assigned/not_applicable сейчас не
имеют distinct positive controls. В текущем source нельзя утверждать, что suite
отличит ошибочно урезанный Fact.status enum. Добавить их в узкую параметризацию
полезно перед freeze; это проверка уже accepted five-status domain, не новая
семантика. Даже если C1 correction ограничится R1, full schema source review
обязан отдельно сверить эти три разрешённых значения и не заявлять executed
coverage, которой нет. Duplicate-key JSON уже покрыт штатным existing
test_contracts.py boundary test; selected C1 command вызывает не всю эту suite.

## 4. Meaningful RED и остающиеся границы

Production resource отсутствует при unchanged existing loader. Поэтому первый
feature signal — missing resource/assertion или fixture setup ValueError от
schema_validator, а не intended parse/import failure. Tests source не исполнялся,
точные collection count/fail/pass/runtime/syntax здесь не заявляются. Finite
boundary tests без validator fixture могут пройти baseline; это healthy existing
boundary reuse, не наличие DOC07 implementation.

28 test functions — source count автора, не collection receipt. Первый RED
не проверит все новые matrices, пока resource отсутствует; будущий GREEN и
schema code review должны проверить фактическую силу negative/positive cases.
Root должен сохранить неожиданные failures и сверить imports/exact source до
production edits; автоматических reruns из этого review нет.

C1 не проверяет graph/current-vs-historical/fragment mapping, retained release
receipt, origin last assignment/phase/conditions/full chain, URI query-free
reviewed-provenance policy, public path safety или dimensional conversions.
Их явное отложение в C2/owning adapters корректно. В частности schema-valid
literal bound record не становится verified bound; equality числа не создаёт
origin receipt. C2 обязана отклонить false claims и unknown proof, а не reuse
эти literals как provenance evidence. Solver/scientific/UI/native acceptance
не следует из shape checks.

## 5. Scope и итоги

Только explicit source/primary/receipt reads, hashes, cmp и read-only Git.
No schema validation, imports/parser/Python/pytest/collection/HDF/network/
children/source edits/Git mutations/build/solver/fullCI. Записаны только review
и identity. Envelope≤20min/1CPU/2GiB/read3MiB/output96KiB; conservative repeated
logical text reads<1MiB, physical filesystem/Git I/O не инструментирован.
Broad execution subtree search отсутствует. Combined C1/C2 четырёх-call finite
runtime budget остаётся у Root и этим reviewer не расходовался/не расширялся.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Factories/матрицы authored независимо от schema defs | Exact source factories/helpers и literal domains | Shape-only, не source-binding proof | сохранить |
| Три cap negatives изолируют только accepted limit | Duplicate rows на576/581/588 | Может отвергать uniqueness без maxItems | изменить |
| Все Fact.status domains имеют positive runtime coverage | Только known/unknown distinct positives | Остальные3 статуса требуют source сверки/лучше positive controls | дополнительно измерить |
| Production/schema/tracked tests сохранены | HEAD12fc, sole untracked source, hashes/diff/absence checks | Runtime не выполнялся | сохранить |
| First RED already observed / shape validity proves science | Resource отсутствует; никаких executions | C1 source preparation только | данных недостаточно |

**STOP: CHANGES REQUESTED R1 на три cap mutations; заморозить исправленный
source/patch перед Root sole RED.**
