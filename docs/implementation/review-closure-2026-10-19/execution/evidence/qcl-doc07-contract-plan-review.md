# DOC07 schema-first Contracts plan: независимое high CP_DESIGN review

2026-10-20. **REQUEST NARROW D2** на plan SHA256
`44434ac8f418c5ad80c1750e34b1dd868112cd2c393d8bc0e3c2d59737a370a8`.
Архитектура, полный inventory и пять-format union пригодны; изменение scope,
новый human approval, новая provenance/capture authority или redesign не нужны.
Нужно замкнуть две явно оставленные альтернативы R4/R5 и записать конечные
status/null/reason условия R2/R3. Это техническая D2 автора ultra в уже принятом
B/DOC07 scope, не решение оператора о включении feature. STOP после report/identity.

## 1. Identity и первичные материалы

Сначала прочитаны primary `docs/system/physics-documentation.md:324–877`
(недостающая в одном truncated выводе середина525–716 прочитана отдельно),
Contracts12fc resource/offline loader, messages boundary и existing schema/test
examples. Затем candidate D/identity и focused R1–R6. Для generator/graph
references дополнительно проверены primary226–228 и `ops/git.ts` без исполнения.

Root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD
`d4113f43cddf02d46025434eb3a9dd8e110e90d6`. Read-only Git зафиксировал dirty
Results gitlink, concurrent root tests и execution coordination artifacts;
рецензент их не менял/не сканировал содержимое execution tree. Contracts HEAD и
root HEAD gitlink совпали: `12fc26462bbab3df76904c6deb01f8c6596de7be`, component clean.
Gitlinks остаются source-composition authority; этот отчёт не lock manifest.

| Источник | Проверенный SHA256 |
| --- | --- |
| Primary DOC03 | `4b046312d0c1f04566c3a80ca6fb8a441ca7b025003c3c3b1c4c2bab2242f6cb` |
| Candidate plan,41475 bytes | `44434ac8f418c5ad80c1750e34b1dd868112cd2c393d8bc0e3c2d59737a370a8` |
| Candidate identity.md,7787 bytes | `84d63e3d41e3ee1b1de9e49351f1adac8e6dec81d0765ba0fbafc3691e02373d` |
| Contracts `__init__.py` | `41b5b746bbf28cd0e60bb85bc927f1c55ba0ac2695f3271b875f83c057a744d1` |
| Contracts `messages.py` | `fd82f76a005519962b1edbfd5b9971f6e8d50c0806ca1f4070359e908fa205fa` |
| Contracts `artifacts.py` | `639ebd85f0a1612d2c036d11d8926f7c4bdd04778d5690a8778eb03e8cb6ccaa` |
| Contracts `tests/test_contracts.py` | `0231b4d437ed3086a2cb365a0ce2a3926da93008d67e99df598e8aced6f63fd7` |

Прочитаны applicable CONTRIBUTING, DOC07 card162–182 и существующие offline,
finite JSON, closed-object examples. Численные массивы/results/run provenance
не являются входом этой задачи; ни scientific correctness, ни S1 acceptance
не проверялись.

## 2. Полный inventory и five-format union: сохранить

| Branch | Required inventory сверено с primary | Verdict |
| --- | --- | --- |
| docs-bundle.v1 | format,sources,schema,generator,fragments,files,aliases; graph/descriptor/file/alias/generator children | Совпадает324–381 |
| model-help-fragment.v1 | format,id,source_revision,title,summary,scope,meaning_source,full,related,equations,inputs,api,assumptions,limitations | Совпадает389–406 |
| model-help-view.v1 | format,context,binding,fragment,inputs,input_status; InputView с distinct declared/used/assigning/effective/value-origin | Совпадает485–538,670–680 |
| model-help-inputs.v1 | format,context,phase,inputs,origin_bindings; raw InputView без Evidence/API value_origin/UUID/release fields | Совпадает556–574 |
| model-help-index.v1 | format,complete,entries; entry path,bytes,sha256,execution_id,point_id,attempt,status,reason | Совпадает619–637 |

Пять веток с required mutually distinct const format в top-level oneOf не
меняют accepted formats: поздние Snapshot/Index дополняют первоначальные
bundle/fragment/view defs. Закрываются реальные objects на всех уровнях,
без пустого additionalProperties:false wrapper поверх union. Нет изменения
scientific-plan/result/contract_set/archive/recovery formats или maintained
revision registry. Def names внутренние, URI `$id` не fetch.

Полностью представлены Sha1/Sha256/Id/ScientificId, PublicRef/selector, DocRef,
Origin/locator, Atom, все десять Fact names, Evidence, ReferenceValueOrigin и
applicability/conditions, ValueOriginView/Binding, retained Claim/assignment
receipt/conditions, public и local scalar/assigning/effective shapes. Не потеряны
schema vs typed default, formula vs numeric-value origin, assigning vs full
effective chain, reference-only vs actual declared/used value origin.

Source graph shape соответствует `sourceGraph()`; sorted/unique ownership
проверяется по generated graph, не hardcoded eight pins. Documenter UUID/tree
в плане совпадают с primary226–228. Неблокирующая локаторная правка для D2:
план ссылается для этих facts на P235–237, правильный range226–228.

Caps сохранены: bundle/index2MiB, fragment32KiB/256pilot, view64KiB/32inputs,
snapshot64KiB/aggregate8MiB, index<=min(pointcount,10000), related/conditions12,
assumptions/limitations12×400chars, title160/summary1600. Oversized invalid
index entry может честно иметь bytes>64KiB; index не получает выдуманный
top-level reason. Byte guards до decode и Unicode maxLength не смешаны.
Local snapshot schema не приобретает AiiDA/root/release authority.

## 3. Что existing Contracts действительно обеспечивает

`schema_names/load_schema` автоматически обнаруживают JSON resource;
`schema_validator` создаёт Draft202012Validator с bundled Registry. Local defs
не требуют loader change/dependency/network. Existing loader tests проверяют
schema vocabulary и bundle-local references; новый resource попадёт в этот путь.
Это source observation, не executed new-schema validation.

`messages.decode/validate_json` обеспечивают bounded UTF-8 JSON, duplicate-key
rejection, depth и nonfinite float rejection; schema дополнительно проверяет
types/const/closed fields. Прямой вызов optional jsonschema над Python NaN/Inf
не заменяет finite boundary. `artifacts.relative_path` покрывает только часть
normalization: оно не доказывает no-dotfile/control/decoding traversal/symlink/
private bytes. План это ограничение правильно сохраняет.

Schema-valid не означает source-binding-valid: graph equality, full bytes/hash,
selector/HTML anchor existence, recipe/input/output allowlists, retained release
receipt, exact local plan/point/attempt/configuration hash, last assignment,
scientific applicability/phase и полный effective chain требуют отдельных proof.
Pure Contracts не выбирает child, не сканирует filesystem/ORM/HDF, не выполняет
Julia/derive, не читает network. Owning adapters передают bounded checked inputs;
их authority не появляется из JSON field name или syntactically valid digest.

## 4. Решения focused R1–R6 и минимальный D2

### R1 — APPROVE multiplicity recommendation

Все десять Fact classes должны присутствовать для fixed slice; каждый class
может иметь несколько authored context facts. `contains` coverage корректна,
uniqueItems не означает keyed uniqueness. Не добавлять ровно10/maxItems10 или
unique name как новое требование: primary354–360,402–406 этого не задаёт.
Schema default, typed constructor и example могут иметь разные default facts.

### R2 — APPROVE proposed invariants; записать closed matrix

Primary343–353,425–431 позволяют именно предложенные derived invariants:
known Origin kind не unknown/not_applicable; not_applicable Origin kind
not_applicable и locators=[]; unknown Origin kindunknown,[],required note.
Не изобретать новый обязательный DOI/measurement locator или unit catalog.
Research assumption с [] требует owning assumption note; остальные scientific
attributions проверяет owning source, а не выдуманная schema provenance.

Минимальное уточнение D2 для ValueOriginView:

- bound => known Origin, nonnull binding, reasonok;
- unknown => exact unknown Origin, null binding, reason только
  origin_not_recorded/override_unbound/conditions_unbound/source_unbound/value_unavailable;
- not_applicable => corresponding not_applicable Origin, null binding,
  reasonnot_applicable.

Это замыкает перечисленные accepted enums, не вводит новых причин. Quantity
имеет numeric value и строковую canonical unit; остальные kinds соответствуют
их scalar types, boolean не numeric/integer. Unit applicability и scientific
meaning доказывает owning dimensional mapping; known-null не unknown.

### R3 — APPROVE proposed status/reason mapping; записать null obligations

Primary496–538,670–680,715–722 поддерживает предложенный closed map:
bound/ok; unknown/source_binding_missing;
incompatible/wrong_release|unsupported_version;
unavailable/bundle_missing|fragment_missing.
Input available/ok; invalid/snapshot_invalid; unavailable с четырьмя remaining
reasons snapshot_missing/point_not_executed_by_selected_child/
inventory_unavailable/inventory_incomplete.

В D2 явно сохранить: bound documentation требует полного доказанного selected
release/graph/bundle/fragment binding, а не один statusok; fragment descriptor
nonnull только bound, fragmentnull на остальных branches. Unknown identity
scalars null, **известные** retained scalars при unbound не обнулять только
из-за статуса. Trusted actor context UUID/attempt всегда обязательны после
успешной selection. Input metadata availability не выводится из documentation
binding и наоборот: это отдельные axes. Эти условия уже accepted, не новые поля.

### R4 — REQUEST freeze одного precise branch

План152 всё ещё разрешает неопределённое «exact retained path mapping» без
точного источника этой mapping. Primary508 ограничивает paths fragment.inputs,
536 требует fragmentnull при unbound,673 допускает declared из retained plan.
Нельзя оставить I выбор между current fragment, произвольным global leaf list
или hidden registry; это различает ответы публичного API.

Минимальный accepted-compatible выбор для D2: input path slice берётся только
из exact requested fragment **того же retained selected source context**, если
его bytes/hash и path inventory уже проверены owning adapter. Descriptor может
не выдаваться как bound static URL, если documentation binding unavailable.
При отсутствии такой exact retained fragment/mapping inputs=[], без current
fallback и без нового mapping registry. Context/input_status остаются truthful.

Если mapping доступна, declared и used оцениваются независимо по их accepted
retained evidence; не превращать доказанное used в unknown только потому, что
docs bundle не обслуживается. Plan/default никогда не заполняет missing used.
Value origin остаётся отдельным proof и без receipt unknown, даже при known
value/assignment. Если автор выбирает более узкий declared-only projection,
пусть D2 явно обоснует его primary контрактом и покажет, где останется known
used metadata; молчаливое склеивание documentation/used axes не принимается.
Это техническая точность уже принятого поведения, не новый human decision.

### R5 — REQUEST выбрать конечную accepted public-locator ветку

План153 оставляет «no-query subset либо reviewed allowlist»; I не должен
изобретать secret-query detector/новый trust registry. Primary343–349 задаёт
https:/doi: без credentials/query secrets; primary736–740 уже запрещает
credential/query/token bytes в public output и требует reviewed public recipes.

Минимальный D2 выбор: query-free locator subset для pilot public emission;
URI parser проверяет schemes/userinfo/control и existing path/output запреты.
Query-bearing locator не исправляется удалением query и не публикуется на
основании format:uri; affected source/artifact остаётся unverified/rejected
до уже предусмотренного owning recipe/source review. Это не глобальная новая
политика доверия и не новый public ingress/API. Если реально нужен harmless
query, D2 должен назвать **существующую** exact reviewed recipe allowlist и
её evidence вместо создания ещё одного registry/эвристики. В текущих inputs
такая allowlist не дана; не утверждать её существование. Scientific origin
или known attribution из самого URL не выводятся.

### R6 — APPROVE focused private pure boundary

Предложенный `model_help.py` и private validation/resolution helpers допустимы
как internal implementation choice. Existing ContractError, finite/schema-valid
precondition и bounded detached retained evidence подходят. Не требуется новый
serialized retained-release receipt, capture API или __init__ re-export.
Внутреннее имя функции не public contract. Будущая public signature, если нужна
вне этого private owning scope, получает свой обычный owning code/API review.

D2 должен только закрепить error/unknown boundary: missing proof возвращает
accepted unknown reason или отвергает attempted bound record; corrupt/contradictory
claim не сохраняется как bound. `_resolve_value_origin` не backfills proof.
Retained inputs не могут быть одними unverified status booleans: для заявленных
proofs нужны проверенные bytes/hash/selection/assignment/context, как уже указано
в primary452–475. Наличие full-chain proof не равно evidence.length>0.

## 5. Граница следующего этапа

Нужен узкий D2 от независимого автора ultra, который запишет выбранные R4/R5
ветви и точные R2/R3 conditions; полный inventory/форматы/owners переписывать
не требуется. Можно повторно проверить только delta и matrices с unchanged
primary digest. Это не разрешение I «самому решить неоднозначность» и не вопрос
пользователю: соответствующие technical decisions уже входят в accepted B.

C1/C2/C3 scope рационален: schema resource и shape fixtures, отдельные pure
cross-binding checks, focused owning review/publication, затем adapters/UI.
Предложенные targeted checks — future recommendation, не executed pass и не
автоматически принятый новый runtime budget. Existing optional validation extra
остаётся optional. Ни build/Julia/native/documentation renderer, ни scientific
checks/solver, ни full suite не следуют из schema-first approval.

Важные future controls сохранены: five complete objects/closed branches, ten
facts coverage, known-null/finite/duplicate keys, referenceA/overrideB включая
равное число с иной assignment/context, remove-one proof, declared→used override,
historicalA/currentB, source/hash/selector mismatch, private path/redaction,
two points/retry/imported point/no snapshot, index incomplete/oversized invalid
entry и no runtime side effects. Shape-positive statusbound fixture обязательно
отделяется от semantic-positive fixture с полными proofs. UI truth/light/offline,
selected-child/auth/serving и DOC04 BUILD остаются later owning gates.

## 6. Scope и evidence limits

Только source/text/Git/hash reads explicit primary/Contracts/plan paths. No
implementation/schema edits; единственные записи — этот review и identity.
Imports/parsers/validators/tests/network/children/Nix/Julia/build/solver/server/
Git mutations/checkpoint writes=0. Envelope≤25min/1CPU/2GiB/read4MiB/output96KiB.
Conservative logical source text, включая repeated full inputs sed/rg, <2MiB;
physical filesystem/Git-object I/O не инструментировался. Lookup несуществующего
Contracts examples directory дал no-such-file; затем прочитаны штатные tests
как examples. Это не выполненная verification и не изменение scope.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Полный five-format inventory соответствует DOC03 | Primary324–877 и candidate tables/shared defs | Schema ещё не реализована | сохранить |
| Loader/offline/finite boundary можно переиспользовать | Contracts12fc loader/messages/tests source | Новые schema/helper не запускались | сохранить |
| Model/formula/value/assigning/effective/used различены | Static/reference и dynamic proof shapes, owner boundaries | R4 должен сохранить независимые availability axes | сохранить |
| Packet достаточно exact для I без новых design choices | R4/R5 остаются альтернативами, R2/R3 условные matrices не закрыты | Исполнитель иначе выберет public semantics | изменить: narrow D2 |
| Schema validity доказывает bound origin/release/science | Primary452–475,643–661 и semantic boundary | Full retained proof и owner verification обязательны | данных недостаточно |
| Для этих уточнений нужен новый human approval | Accepted DOC07 card/P1 B; новых model/trust/capture целей не предложено | Вне accepted predicates scope не расширять | сохранить текущие полномочия |

**STOP CP_DESIGN: REQUEST NARROW D2 exact candidate44434…70a8.**
