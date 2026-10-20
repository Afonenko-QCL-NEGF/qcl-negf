# DOC07 C1 schema — независимый high source review

2026-10-20. **REQUEST_CHANGES: F1 — missing structural status cross-guard; F2 — exact token end-boundary.** Остальные прочитанные five-format/closed-object/Origin/Atom/ten-Fact формы соответствуют принятому контракту. Ни один parser/schema validator/import/test не запускался. Этот source verdict не устанавливает schema runtime validity, C2 binding, public/native/scientific acceptance.

Reviewer actions: только чтение primary normative text/actual schema/test source/loader, read-only Git metadata и SHA256; sole outputs этот report и identity. No target execution, Python/Node/Deno/Nix/Julia/build/network/children/product/checkpoint/Git mutations.20min/1CPU/2GiB/read2MiB/output64KiB — порученный envelope, не cumulative measured telemetry.

## 1. Authority и exact binding

Сначала прочитаны canonical managed-root DOC03 и accepted D2/review, затем actual schema целиком и loader; test source прочитан только после установления contract/source trace. Author C1 report прочитан после source assessment. Tests не использованы как нормативный контракт.

Canonical `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/docs/system/physics-documentation.md` SHA `fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794`, особенно324–573,619–637,978–1084. Accepted plan `/tmp/qcl-doc07-contract-plan-v2.md` SHA `20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b`; independent design review SHA `f62bbe6998b178ea746a3a28ae73e4e910c751742e0e7887ac4d77b63786b231`.

Contracts isolated `/tmp/qcl-doc07-contract-worktree`, HEAD/base `12fc26462bbab3df76904c6deb01f8c6596de7be`. Status — untracked новый schema resource и frozen tests/test_model_help.py; submodules отсутствуют. Tracked diff stat пуст, что само по себе не проверяет untracked resource; ниже actual hashes. CONTRIBUTING прочитан; отдельного AGENTS.md в owning root нет. Existing loader/API не менялись.

| Frozen artifact | Проверенный SHA256 |
| --- | --- |
| `src/qcl_negf_contracts/schemas/model-help.schema.json`,28857B | `cbca63eac4ce22ece53e5275b5ce458508edf9ab1d467aad28d9a8348534a3a0` |
| `tests/test_model_help.py`,31628B | `6a39ee353153a4de2d313323b5c67662026721f282adec1ae44305d95d1f2ebd` |
| `/tmp/qcl-doc07-C1-schema-full.patch` | `ede3357bdbbf265aadb06064b0cc38d69f01c48c286094777ed3de1f4d8e1987` |
| `/tmp/qcl-doc07-C1-schema-identity.json` | `ed2701ce764b58be5b7344b2983dbf69a26f9d18784f89789e26979467f371cb` |
| `/tmp/qcl-doc07-C1-schema-report.md` | `bd813c5a1c9ad6c46c5b5d94d2439a689d13b20be6f90776c21ac25f9ae7b3fd` |

## 2. Findings — полный набор

### F1 — P1: invalid/unavailable input_status всё ещё допускает used known

Локаторы schema315–330 (`InputStatus`, `View`), D2 R3 table и schema/semantic boundary, canonical1033–1036/513–518.

InputStatus правильно ограничивает status→reason, а EvidencedScalarState правильно ограничивает его **собственный** status→atom/evidence. Но View не связывает input_status с inputs[].used. Поэтому otherwise valid View, у которого `input_status={status:"invalid",reason:"snapshot_invalid"}`, может сохранять `inputs[0].used={status:"known",atom:<valid Atom>,evidence:<valid Evidence>}`. То же для unavailable/snapshot_missing и прочих accepted unavailable reasons. Ни одна current subschema не отвергает сочетание; имеющийся View allOf регулирует только fragment по documentation binding.

Normative D2 R3 прямо требует для invalid/unavailable used unknown и atom/evidence null, сохраняя independently available declared. Это внутренняя структурная связь одного JSON document, выразимая стандартной Schema; её нельзя отложить на C2 retained snapshot proof или смешать с независимостью documentation binding/science. C2 должен доказывать, действительно ли snapshot доступен/валиден, но accepted status уже не может противоречить known used в schema-valid output.

Минимальное correction: View conditional для input_status invalid/unavailable, требующий каждого existing input.used.status=unknown и тем самым atom/evidence null через ScalarState invariant. Не обнулять declared, не требовать inputs nonempty, не менять available/ok+inputs=[] и unbound-docs/verified-used independence. Не вводить новые public fields/status/reasons. Existing approved test `test_input_status_shape_matrix:412–426` уже содержит corresponding known-used mutant negative — source corroboration после нормативного вывода, не источник нормы и не executed failure.

### F2 — P2: `$` не обеспечивает exact end для digest/identity tokens

Локаторы schema13–17 (`Sha1`, `Sha256`, `Id`, `ScientificId`, `Uuid`); comparable fully anchored token patterns184/255/339. Primary333–334 и canonical request grammar требуют exact digest/identifier characters; D2 относит syntactic patterns к C1.

Завершение regex `$` может совпадать **перед финальным LF**. JSON Schema pattern является regex matching, не full-string equality; existing loader возвращает обычный Draft202012Validator, без отдельного fullmatch wrapper для этого resource. Поэтому string из40 lowercase hex плюс завершающий newline удовлетворяет текущему Sha1 pattern;64hex+LF аналогично Sha256, canonical UUID+LF и valid short Id/ScientificId+LF — их patterns. Schema не имеет exact length/end constraint, закрывающего suffix. Это source-derived counterexamples, не выполненные regex/schema tests. Raw JSON string с escaped newline остаётся finite legal JSON, так что finite decoder сам не решает этот дефект token grammar.

Минимальное correction: строгий end/character boundary, совместимый с используемым Draft2020-12 regex dialect/validator, или эквивалентные длина+character constraints там, где длина фиксирована. Провести ту же проверку fully anchored descriptor/URL/index patterns, не объявляя outer trailing newline частью допустимой identity. Independent suffix-LF negative и healthy exact tokens должны различаться. Нормализация PublicRef paths/URI/public allowlists остаётся C2: finding не требует перенести все path security/provenance проверки в schema. Digest equality с retained bytes остаётся отдельным C2 proof, но не заменяет exact C1 syntax.

## 3. Подтверждённое соответствие остальных shape contracts

Top-level Draft2020-12 oneOf имеет ровно пять обязательных distinct format consts: Bundle/Fragment/View/Snapshot/Index. Concrete objects closed с required complete field sets; conditional/ref wrappers не ошибочно закрывают поля поверх composed base. Все `$ref` локальные. Existing schema_names/load_schema/schema_validator динамически подхватывают resource; __init__ re-export/registry/version fork отсутствуют. JSON syntax/metaschema validity в этом review не измерена.

Origin56–68 реализует exact known-kind set, unknown kind/empty locators/nonempty note, N/A kind/empty locators, assumption with no locators requiring note. Не введены обязательный DOI/locator, measurement inference или физический positive constraint. Atom70–80 разделяет quantity numeric+nonempty unit и scalar integer/number/boolean/string/null по kinds, unit остальных string|null. Finite/nonfinite/duplicate-key boundary, unit canon/applicability и физическая интерпретация принадлежат указанным owners; schema не invents numeric model limits/denominator guards/unit registry. Known-null отличается от unknown.

Facts90–103 содержит десять independent contains constraints поверх закрытого Fact item. Все names покрыты; нет maxItems10/unique-by-name, repeated authored default contexts остаются valid. Text nullable/status enum/source refs сохранены. Fragment length/related/short-note/applicability maxima и Bound View input cap32 присутствуют; Bundle descriptors cap256, Index cap10000. Остальные arbitrary arrays/strings не получили новых придуманных caps.

ValueOriginView bound требует known Origin/nonnull binding/reasonok; unknown — unknown Origin/null binding/пять exact reasons; N/A — corresponding Origin/null/reason. ReferenceValueOrigin/claims/assignment receipts/conditions имеют exact accepted fields, phases/selectors/capture const. Complete scientific source/value/context/last-assignment proof не заявлен shape validation. Binding239–252 требует four nonnull identities для bound/ok, сохраняет known retained scalars на unbound branches, exact reason matrices; View nonnull fragment только при bound, null в остальных branches. Actor UUID/attempt required regardless docs availability. Available/ok с inputs=[] и fragmentnull допускается корректно.

ScalarState/EvidencedScalarState локально правильно различают known и unknown/null. Assigning known имеет source-or-rule и Evidence, unknown kindunknown/nulls, redacted source=null. Raw snapshot исключает API value_origin/Evidence/actor UUIDs и имеет solver_input const/local context/claims; effective steps enum exact. EffectiveOrigin known не выводится из minItems/evidence nonempty: полный chain proof intentionally C2. Index valid/ok vs invalid/non-ok exact; bytes не ограничены64KiB, чтобы typed too_large measurement сохранялся. Index completeness/aggregate/count/path→context equality остаются owning semantic checks.

## 4. Что правильно оставлено C2/owners

Не являются C1 findings: selected graph sorting/key uniqueness/membership; exact owner revision/blob/selector/HTML anchor; normalized safe paths/private/output allowlists; descriptor id→file и URL/source revision equality; exact payload/source hash; bundle self-hash exclusion; fragment retained mapping to selected run/child; canonical unit/applicability; release/assignment/value-origin/effective-chain proof; metadata UTF8 byte caps/aggregate inventory reads; source/public-content review. Locator только prefixhttps/doi shape здесь намеренно недостаточен для publication: query delimiter/userinfo/URI controls parser и reviewed-source provenance C2, без fetch/rewriting/нового trust registry.

Проверки, которые требуют retained inputs, не подменены status booleans. Missing capture receipt должен оставаться actual origin unknown; static reference не proof конкретного run. Ни schema valid, ни test pass не заменяют physical/model/experimental acceptance.

## 5. Handoff / ограничения

Root сообщил retained initial missing-resource RED и used1/4 DOC07 calls; reviewer их не переисполнял и не расходовал слот. Known F1 нужно закрыть до следующего GREEN, без автоматического retry до pass. F2 нужны strict-token controls в owning finite correction packet; этот review сам не разрешает новую попытку/сброс counters. Новые schema bytes требуют fresh exact source identity и independent narrow review; runtime/metaschema/loader tests остаются Root-only после admission/binding.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Five closed formats/Origin/Atom/ten Facts faithful | Actual schema1–354 и canonical/D2 trace выше | Parser/metaschema не запускались | сохранить |
| Invalid/unavailable запрещает known used | Нет View cross-conditional | F1 contradictory status document принимается по shape | изменить |
| Exact token grammar исключает suffixLF | Patterns13–17 и отсутствие strict end/length | F2 regex boundary, не retained hash proof | изменить |
| C2 proof/IO/physics не перенесены в schema | Comments + deliberately separate normative layer | C2 ещё не реализован | сохранить |
| Schema/runtime/public/native/science acceptance получены | Таких новых measurements нет | Source findings и отдельные gates | дополнительно измерить |

**STOP. REQUEST_CHANGES F1/F2; reviewer executions=0.**
