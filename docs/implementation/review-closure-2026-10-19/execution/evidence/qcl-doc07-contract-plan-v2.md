# DOC07 Contracts schema-first: D2 closed implementation packet

> Для следующего исполнителя: выполнять только после независимого R `high` этого packet. Implementation — отдельный I `medium`; текущий этап source-only DESIGN/DOC. Путь artifact задан поручением, поэтому plan хранится в `/tmp`, не меняет owning source или execution checkpoint.

**D2 provenance:** независимый high-review D1 `/tmp/qcl-doc07-contract-plan-review.md`, SHA256 `7b0c262a1368d53cd98ed964ba46ae3f037de4f5c9b3dd9ab0d89a8d6ceeebdb`, подтвердил inventory/union и R1/R6, запросил конечные R2–R5. D1 SHA256 `44434ac8f418c5ad80c1750e34b1dd868112cd2c393d8bc0e3c2d59737a370a8` и original R сохранены. Этот D2 закрывает choices; его свежий independent high-review ещё не выполнен. Предлагаемое canonical уточнение — `/tmp/qcl-doc07-canonical-clarification.patch`, только append в exact DOC03; исходный файл в root не изменён.

**Цель:** реализовать ровно принятые DOC03 форматы model/source help в одном Contracts resource `model-help.schema.json` Draft 2020-12 и отдельно проверить неизбыточные semantic bindings; reference origin не становится origin конкретного run по совпадению числа.

**Архитектура:** Contracts владеет формой и чистыми cross-binding проверками. Existing loader/offline validator автоматически обнаруживает schema resource. Core/Research авторствуют смысл/reference annotations; Runner выдаёт local metadata; AiiDA проверяет retrieved bytes и обогащает выбранным child; Portal проецирует scalar metadata и показывает exact retained fragment. Это не новый model registry, capture API или независимый release manifest.

**Стек:** existing pure Python Contracts, existing optional `jsonschema` Draft202012Validator + `referencing` offline registry; без новых dependencies. Source-only design не импортирует эти модули и не запускает validator.

**Spec:** `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/docs/system/physics-documentation.md:324–877`, exact SHA256 `4b046312d0c1f04566c3a80ca6fb8a441ca7b025003c3c3b1c4c2bab2242f6cb`. Дальнейшие локаторы `P:N` означают строку N этого exact файла. DOC07 card: `docs/implementation/review-closure-2026-10-19/documentation-instructions.md:162–182`.

## Authority и границы

- Root HEAD фактически `d4113f43cddf02d46025434eb3a9dd8e110e90d6`; Contracts checkout и опубликованный gitlink `12fc26462bbab3df76904c6deb01f8c6596de7be`, Contracts worktree clean при чтении. Root содержит чужие working changes Platform/Results/tests/execution receipts; они не входят в этот packet и не изменялись.
- DOC03 technical contract принят; product implementation не подтверждена этим текстом (P:196–214). Feature DOC07 уже в EXEC scope; нового запроса на включение feature не требуется.
- DOC04 сейчас blocked на shared schema/public OFL/native BUILD; локальные adapters разрабатываются. Этот packet не означает public bundle ready, установленный release, browser/offline pass или numerical/scientific acceptance.
- Не создавать source graph lock-файл; source composition authority — existing Git gitlinks и `ops/git.ts:sourceGraph`. DOC03 source-facts root `9d8cf0c…` — исторический локатор наблюдений, не текущий root identity.
- Не менять scientific-plan/result schemas, result contract registry, archive/recovery closure, numerical defaults/criteria, dependencies или format versions.
- Текущий D2 envelope: <=20 min, 1 CPU, 2 GiB RAM, logical source reads <=3 MiB, tool output <=128 KiB; no solver/build/parser/import/runtime/tests/network/children/commits/push/checkpoint writes. Выполнены только Git/read-only text/hash/diff operations и запись `/tmp` design artifacts. D1 envelope не превращается в дополнительный runtime grant.

## Один resource и пять top-level документов

Создать только `components/qcl-negf-contracts/src/qcl_negf_contracts/schemas/model-help.schema.json` с `$schema=https://json-schema.org/draft/2020-12/schema`, local `$defs`, top-level `oneOf` на пять веток с различающим обязательным const `format`:

| `$defs` (внутреннее имя) | Exact public format | Поля object, все обязательны |
| --- | --- | --- |
| `Bundle` | `qcl-negf.docs-bundle.v1` | `format,sources,schema,generator,fragments,files,aliases` |
| `Fragment` | `qcl-negf.model-help-fragment.v1` | `format,id,source_revision,title,summary,scope,meaning_source,full,related,equations,inputs,api,assumptions,limitations` |
| `View` | `qcl-negf.model-help-view.v1` | `format,context,binding,fragment,inputs,input_status` |
| `Snapshot` | `qcl-negf.model-help-inputs.v1` | `format,context,phase,inputs,origin_bindings` |
| `Index` | `qcl-negf.model-help-index.v1` | `format,complete,entries` |

P:326 первоначально называет defs bundle/fragment/view; P:556–570 и P:619–623 затем задают ещё два exact detached object. Их local defs и union не создают новых форматов. Все описанные objects на каждом уровне получают `additionalProperties:false`; закрывать нужно leaf objects, а не блокировать union пустым closed wrapper. Никаких иных discriminators, fields/versions или remote `$ref`. Def names не публичный API.

`schema_names()/load_schema()/schema_validator()` уже автоматически читают `.json`; `__init__.py` не требует изменения. Existing `tests/test_contracts.py:test_all_schemas_are_valid_and_references_stay_in_bundle` и `test_offline_validator_resolves_bundled_schema_references` должны охватить resource. `$id` можно оставить existing loader default `https://qcl-negf.invalid/schema/model-help.schema.json`; это identifier, не сетевой fetch.

## Общие defs: exact accepted поля и граница проверки

| Тип | Форма и accepted ограничения | Что остаётся за пределами JSON Schema |
| --- | --- | --- |
| `Sha1/Sha256` | string exact 40/64 lowercase hex (P:333) | Digest exact bytes и equality с выбранным источником |
| `Id` | `[a-z][a-z0-9._-]{0,127}` (P:334) | Fragment membership в выбранном bundle |
| `ScientificId` | Existing scientific plan execution/point grammar `[A-Za-z0-9][A-Za-z0-9._-]{0,127}`; не более узкий fragment Id | Plan membership и path/context/child equality |
| `PublicRef` | ровно `component,revision,path,selector,sha256`; selector ровно `kind,value`, kind `symbol|anchor|json_pointer|file`, file value empty string (P:335–339) | component `root` или selected graph path; exact owner revision; normalized allowlisted source file; full blob hash; actual selector existence. Не suffix/name heuristics |
| `DocRef` | ровно `section,path,anchor`; section `core|runner|research|operator`, path relative `.html`, anchor string или null (P:340–342) | Actual allowlist/payload HTML/ID existence и exact version-local root |
| `Origin` | ровно `status,kind,locators,note`; status `known|unknown|not_applicable`; kind `publication|measurement|interpolation|fit|research_assumption|code_policy|unknown|not_applicable`; locator ровно `title,uri,location`; note plain text (P:343–349) | URI parsing, no credentials/query secrets; owning annotation/scientific attribution. DOI никогда автоматически не означает measurement |
| `Atom` | ровно `kind,value,unit`; kind `quantity|integer|number|boolean|enum|null`; scalar corresponding value; unit canonical string, `1` dimensionless, null when inapplicable; никаких arrays/objects/NaN/Inf (P:350–353) | Existing `decode/validate_json` finite boundary нужен и для Python values; canonical unit/meaning проверяется owning dimensional mapping, без нового unit registry |
| `Fact` | ровно `name,status,text,sources`; десять names `signature,units,default,constraint,effects,errors,formula_origin,value_origin,assigning_origin,effective_origin`; status `known|partial|unknown|not_assigned|not_applicable`; text string или null, sources PublicRef[] (P:354–360) | Meaning, explicit schema/typed-constructor/example default context; extraction provenance. Partial/unknown не pass |
| `Evidence` | ровно `container,sha256,selector`; container `frozen_plan|execution_input|execution_strategy|release_receipt|value_origin_receipt`; selector allowlisted JSON Pointer (P:530–533,439) | Hash exact bounded metadata bytes, pointer existence, ownership/phase/context. Не server URL/path/handle |

Closed schema matrices R2 ниже обязательны: Origin unknown => kindunknown/[]/непустой note; known исключает unknown/not_applicable kinds; not_applicable => kindnot_applicable/[]. Known research_assumption с [] требует owning assumption note. Quantity numeric + string unit; integer/number/boolean/enum/null соответствуют scalar types; unit applicability остальных kinds доказывает owning dimensional mapping, без нового unit catalog.

Для каждого `facts` в fixed slice schema `allOf` + `contains` обеспечивает присутствие всех десяти names, включая explicitly not_applicable/unknown. R1 закрыт high-review: repeated names разрешены для разных authored contexts; нет maxItems10/unique-by-name. `uniqueItems:true` не обеспечивает keyed uniqueness и не заменяет coverage. Schema/typed-constructor/example defaults могут быть разными Fact records; существование числа 64 не выбирает один из них.

## Bundle/fragment: exact inventory

`Bundle.sources` — existing generated `qcl-negf.git-graph.v1` object ровно `format,revision,components`; components[] ровно `path,revision,url`, sorted по path. Это структурное описание existing graph внутри schema, не ручной набор выбранных eight pins. Dynamic graph equality/membership проверяются semantic layer.

`Bundle.schema` — PublicRef Contracts `model-help.schema.json`, selector file. `generator` — ровно `name,version,uuid,git_tree_sha1,julia_version,project_sha256,manifest_sha256,recipes,toolchain_lock`: const Documenter/1.17.0/Julia1.13.0; UUID `e30172f5-a6a5-5a46-863b-614d45cd2de4`; git_tree_sha1 `56e9c37b5e7c3b4f080ab1da18d72d5c290e184a`; SHA256 fields, recipes PublicRef[], toolchain_lock PublicRef (P:226–228,371).

`fragments[]` ровно `id,file,sha256`; file exact `help/fragments/<id>.json`, unique id и file. `files[]` ровно `path,media_type,bytes,sha256`; bytes nonnegative integer, unique normalized path; весь public payload; `bundle.json` исключён. `aliases[]` ровно `from,to` DocRef. Реальная page/anchor обязательна у alias. Bundle identity — external SHA256 exact UTF-8 bundle bytes, не self-hash field. Production publication binding к release receipt остаётся owning publication operation; новый receipt public format здесь не вводится (P:368–381).

Fragment поля и limits:

- id Id; source_revision Sha1 == bundle.sources.revision; title<=160 Unicode characters, summary<=1600; scope enum `baseline|variant|operator_only|outside_study`.
- meaning_source PublicRef owning Core/Runner explanation; full DocRef; related<=12 DocRefs.
- equations[] ровно `id,doc`, existing equation ID и DocRef. Не повторять formulas, не вводить regex только по примеру EQ-KIFR-001.
- inputs[] ровно `path,schema_source,facts,reference_value_origin`; whitelisted dotted config leaf; schema_source PublicRef с selector kind=json_pointer; facts coverage выше. Не превращать принятый fixed Runner mapping из восьми leaves в глобальную вечную enum всех fragment inputs.
- api[] ровно `symbol,source,doc,facts`; public symbol, PublicRef, DocRef, facts coverage выше.
- assumptions/limitations <=12 strings каждый, <=400 Unicode chars на строку.
- Static assigning/effective facts показывают semantic function/source, не run values/history. Numeric leaf name не производит DOI или pseudo-formula (P:389–406).

## Origin objects и proof: exact inventory

`ReferenceValueOrigin` ровно `id,parameter,atom,applicability,origin`: Id, parameter PublicRef public parameter-set + JSON Pointer, Atom сгенерирован из exact parameter bytes; applicability ровно `status,conditions,note`, status `specified|unknown`; conditions<=12 объектов ровно `id,path,relation,atom,source`, relation const equal, path public scalar context/physical leaf, source PublicRef scientific applicability statement. Unknown требует note и не позволяет actual bound. Пустое conditions[] для specified текстом не запрещено; не выдумывать обязательную температуру/состав у каждого источника (P:412–423).

`ValueOrigins` ровно `declared,used`, каждое `ValueOriginView` ровно `status,origin,binding,reason`. Status `bound|unknown|not_applicable`; Origin; binding ValueOriginBinding|null; reason `ok|origin_not_recorded|override_unbound|conditions_unbound|source_unbound|value_unavailable|not_applicable`. Unknown => exact unknown Origin, [], null binding, explicit non-ok reason. Number/assigning могут быть known отдельно (P:425–431).

`ValueOriginBinding` ровно `reference_id,annotation,parameter,phase,value,assignment,conditions,receipt`. reference_id Id, annotation PublicRef Research annotation, parameter exact PublicRef leaf, phase `declared|used`, value/assignment/receipt Evidence, conditions Evidence[]. Assignment evidence указывает retained source-binding receipt, не pathname. Conditions нужны для всех authored applicability conditions (P:433–439).

`OriginBindingClaim` snapshot origin_bindings[] ровно `reference_id,annotation,parameter,phase,assignment_receipt,conditions`. Assignment receipt ровно `source,source_sha256,leaf_pointer,capture,plan_fingerprint,execution_id,point_id,attempt`; capture const retained_public_source_binding; source PublicRef; source_sha256 Sha256 equal source.sha256; leaf_pointer JSON Pointer assignment в frozen plan; plan fingerprint Sha256; ScientificIds; attempt positive integer. Conditions[] ровно `id,input_path,phase`, адресуют scalar того же snapshot/context; declared может адресовать exact frozen point passport. Никаких DOI-copy, private pathname, AiiDA UUID (P:441–450).

Процедура actual-origin должна доказать одновременно P:452–463: (1) selected graph/annotation/parameter bytes + applicability specified; (2) receipt exact последней assigning source/leaf + hash/context, а не filename history; (3) target Atom и все context conditions по phase; (4) plan/execution/point/attempt/phase + verified snapshot hash, без переноса declared proof через unbound runtime override. Missing proof => unknown; fixture, где вручную проставлено status=bound, сама по себе ничего не доказывает.

Selected source не сохраняет такие capture receipts. First DOC07 для существующих plans и новые snapshots без capture input: origin_bindings=[], actual value_origin unknown. Никакого backfill из current checkout/equality/filename; production known-origin capture не prerequisite этого scope и новый capture ingress/API не создаётся (P:465–475).

## Run View и local Snapshot

`View.context` ровно `run_uuid,execution_id,point_id,attempt,calcjob_uuid,plan_fingerprint,scientific_fingerprint,configuration_hash,model_revision`. Canonical full UUID strings и attempt>=1 обязательны после child selection; fingerprints Sha256, config hash Sha256|null, model_revision exact frozen plan nonempty string (не вводить новую model registry). ScientificId для execution/point.

`binding` ровно `status,release_id,release_manifest_sha256,source_revision,bundle_sha256,reason`; status `bound|unknown|incompatible|unavailable`; release_id retained portable label, SHA256/Sha1 fields nullable при отсутствии; reason `ok|source_binding_missing|wrong_release|bundle_missing|unsupported_version|fragment_missing`. Bound проверяет retained release manifest/receipt и exact graph, не только label/model_revision/number. Unbound => fragment=null. `fragment` когда bound ровно `id,url,sha256`, url только `/docs/<exact-source-revision>/help/fragments/<id>.json`, без current/fallback/path-from-user.

`inputs` <=32 InputView только requested fragment.inputs paths. `input_status` ровно `status,reason`, status `available|unavailable|invalid`, reason `ok|snapshot_missing|snapshot_invalid|point_not_executed_by_selected_child|inventory_unavailable|inventory_incomplete`.

InputView ровно `path,declared,used,assigning,effective_origin,value_origin`:

- declared/used ровно `status,atom,evidence`; known требует Atom+Evidence, unknown оба null. Declared из frozen point passport; used только exact attempt snapshot.
- assigning ровно `status,kind,source,rule,evidence`; status `known|unknown|redacted`; kind `config_file|generated_assignment|typed_constructor|execution_strategy|point_axis|unknown`; source PublicRef|null, rule allowlisted producer ID|null, Evidence|null. Known требует source или rule и evidence; unknown kindunknown и остальные null. Private path => redacted/source=null, без basename. Не придумывать redacted-kind/rule/evidence ограничения, которых текст не закрепил.
- effective_origin ровно `status,evidence`; status `known|partial|unknown`, Evidence[]. Known требует всю применимую causal chain; этот proof не выражается одной cardinality schema.
- value_origin exact ValueOrigins выше.

Snapshot ровно format/context/phase/inputs/origin_bindings, phase const solver_input. Context ровно `plan_fingerprint,scientific_fingerprint,model_revision,execution_id,point_id,attempt,configuration_hash`, те же local types; **нет** nullable fake run_uuid/calcjob_uuid/release_id/source_revision/bundle fields. Raw inputs ровно `path,declared,used,assigning,effective_origin`: scalar state `status,atom`; assigning `status,kind,source,rule`; effective origin `status,steps`; steps[] ровно `kind,source,rule`, kind `configuration_merge|point_axis|execution_strategy|checkpoint_restore`. Общие status/null invariants применяются с удалением отсутствующих Evidence полей. Никакого API value_origin в snapshot (P:556–574).

Placement/capture — Runner/AiiDA responsibility, не schema: immutable per-point solver-entry file actual allocated attempt; exact logical path `result/executions/<execution_id>/<point_id>/attempt-<attempt>/model-help-inputs.json`; closed bytes, atomic no-replace; no snapshot до checkpoint restore; не выдумывать used для skipped/restored-imported point. Configuration_hash остаётся declared passport hash, не actual-runtime hash. Known used mapping только восьми source-verified leaves P:583–601; остальные unknown до owning mapping.

## Detached index и limits

Index entry ровно `path,bytes,sha256,execution_id,point_id,attempt,status,reason`; status `valid|invalid`, reason `ok|malformed|identity_mismatch|too_large|unsupported_version`. Exact path grammar использует ScientificId, attempt positive без leading-zero/path ambiguity. `valid` => reason=ok; `invalid` => non-ok. В entry.bytes нельзя ставить max64KiB: typed invalid too_large обязан сообщать measured/inventory размер oversized file. Индекс не добавляет UUID или top-level reason (его нет в accepted object).

| Граница | Accepted cap | Где проверяется |
| --- | --- | --- |
| Bundle bytes | <=2 MiB | До decode, byte guard |
| Fragment bytes | <=32 KiB; <=256 fragments/pilot | Byte guard + schema maxItems256 для descriptors в pilot resource |
| Help View bytes | <=64 KiB, inputs<=32 | Byte guard; schema array cap |
| Snapshot payload | <=64 KiB/file | Parser/writer bytes guard, invalid too_large entry; не читать arrays |
| Snapshot aggregate | <=8 MiB/execution/attempt | Runner cumulative publish, AiiDA inventory sum **до payload reads** |
| Index | <=2 MiB; <=min(plan point count,10000) entries | Byte guard/schema maxItems10000 + semantic count |
| Related, applicability conditions | <=12 | Schema maxItems12 |
| Assumptions/limitations | <=12×400 Unicode chars | Schema maxItems/maxLength |
| Inputs field mappings | Fixed eight used leaves only | Runner adapter; no universal reflection |

Остальным arrays/strings не назначать произвольные новые caps; finite serialized-byte guards уже ограничивают документ. JSON Schema maxLength считает Unicode characters, не serialized bytes. Existing actor/API меньший cap имеет приоритет (P:743–746). Обычный enum boolean не пройдёт integer type; finite rejection дополнительно обязателен на Python/JSON boundary.

Complete=false index не trusted; aggregate overrun => entries=[] и downstream inventory_incomplete. Incomplete generic inventory не становится pass, partial good sibling доверяется только если complete inventory/index. Index не scientific pass; raw invalid files сохраняются; scientific exit codes не меняются (P:614–637).

## Semantic слой: только проверяемые связи, не дублирование schema

R6 закрыт high-review: focused private module `src/qcl_negf_contracts/model_help.py`, без `__init__` re-export и нового публичного API. Для I закреплены внутренние `_validate_model_help_bindings(document, *, retained)` и `_resolve_value_origin(reference, claim, *, phase, retained)`. Первый принимает уже finite-decoded schema-valid object и detached immutable validation inputs, возвращает тот же object или existing ContractError. Второй строит ровно accepted ValueOriginView без wrapper/receipt format. Missing proof => unknown с accepted reason. Corrupt/contradictory attempted bound record => ContractError; resolver не выдаёт bound и не backfills proof. При необходимости публичного exported callable later owning API review отделён от этого packet.

`retained` — только in-memory checked evidence выбранного owner: selected graph, exact bytes/hash descriptors, explicit recipe input/output/selector allowlists, frozen plan/passport и selected local context, retained origin claims/assignment chain/phase, retained release binding. Это внутренний аргумент, не новый serialized registry. Contracts не читает arbitrary filesystem, network, AiiDA ORM, Julia target modules или HDF5. Owning IO передаёт bounded bytes; может проверять provenance на своей стороне, но не переписывает публичную форму.

JSON Schema проверяет типы, закрытые поля, const formats/enums, branch status/null/source-or-rule, syntactic patterns, declared limits и десять fact classes. Existing finite boundary проверяет UTF-8/duplicate keys/depth/NaN/Inf. Semantic layer проверяет только то, что стандартной JSON Schema не выразить:

1. Equality с selected graph/owner revision и exact full source bytes; actual allowlist/selector/HTML anchor. Source graph sort/unique path и keyed uniqueness descriptors/files/input paths/condition IDs (везде, где идентификатор используется для однозначного lookup).
2. Dynamic `id -> help/fragments/<id>.json`, expected-version URL, fragment hash/files membership; bundle self-hash exclusion; aliases actual payload.
3. Normalized POSIX paths, symlink-free/output-safe inventory и no decoding traversal/control/dotfile/private payload; URI parser/credentials policy. Filesystem/symlink observations предоставляет owning collector; pure Contracts не делает scan.
4. Snapshot context/path/selected plan/point/attempt/configuration_hash и index/size/hash equality; count<=plan point count; selected actor UUID enrichment проверяется AiiDA boundary. Contracts не выбирает child и не исправляет snapshots.
5. Retained release receipt -> exact root graph -> bundle digest -> fragment bytes. Missing receipt остаётся source_binding_missing, historical A никогда не заменяется B/current. Standalone bundle не обещает installed release.
6. Все четыре origin-binding proof conditions P:452–463. Сравнение Atomic scalar строго с kind/unit и сохранённой scientific applicability; boolean не numeric; numerical equality без source+last assignment+context+phase не proof. Никакого преобразования единиц/derive в Contracts: производитель уже нормировал Atom.
7. Полнота effective chain: только при наличии полного owning перечня применимых planning/runtime steps; если такого proof нет — partial/unknown, не правило «evidence nonempty => known».

Не переносить структурные проверки в semantic function второй ручной schema. Не вызывать schema_validator при import; optional validation extras остаются optional, schema loader остаётся dependency-free. Публичный semantic вызов без достаточных retained inputs должен fail/unknown по назначению поля, не выдавать successful binding из shape-only validity.

## D2: закрытые R1–R6, исполняемые без выбора новой semantics

R1/R6 подтверждены independent high-review D1; R2/R3 ниже записывают approved derived invariants полностью; R4/R5 выбирают рекомендованные compatible branches. Новых public fields/formats/API или physics/model decisions нет. Append-only canonical clarification patch содержит те же нормы; после D2 high-review Root может отдельно опубликовать именно это уточнение. До review это candidate, а не уже изменённый canonical DOC03.

### R2: Origin, Atom и ValueOriginView — schema и proof

Все поля каждого object остаются обязательны. Текстовые note всегда string; пустая строка допускается только там, где ниже не требуется непустое объяснение.

| Origin.status | Допустимый kind | locators | note | Дополнительный semantic proof |
| --- | --- | --- | --- | --- |
| known | publication,measurement,interpolation,fit,research_assumption,code_policy | Locator[]; schema не требует обязательного DOI/locator для каждого kind | Для research_assumption с [] непустая owning-assumption note; иначе plain-text string | Exact authored annotation/source bytes и attribution; URI сам по себе не доказывает origin kind |
| unknown | unknown | [] | Непустой explicit unknown note | Не выдумывать отсутствующий источник |
| not_applicable | not_applicable | [] | Plain-text string | Применимость determined owning fragment/input context, не по отсутствию данных |

| Atom.kind | Value schema type | Unit schema type | Проверка вне schema |
| --- | --- | --- | --- |
| quantity | number | непустая string | Canonical unit данного physical quantity по owning dimensional mapping |
| integer | integer | string или null | Boolean не integer; если dimensionless, canonical unit `1` |
| number | number | string или null | Finite numeric; dimensionless/неприменимость по owning mapping |
| boolean | boolean | string или null | Unit applicability по owning mapping |
| enum | string | string или null | Смысл enum и unit applicability по owning mapping |
| null | null | string или null | Known-null — известное JSON null, не missing value |

Finite rejection NaN/Inf/-Inf/overflow и duplicate-key JSON обеспечиваются **до** schema existing finite boundary. Schema не добавляет unit registry; она не принимает array/object вместо scalar. Quantity без строки unit invalid. Для остальных kinds shape допускает string|null, но это не разрешение выдавать некорректную canonical unit: producer и semantic evidence должны соответствовать selected mapping.

| ValueOriginView.status | origin | binding | reason | Что ещё нужно для принятия |
| --- | --- | --- | --- | --- |
| bound | Origin.status=known | Nonnull ValueOriginBinding | ok | Все четыре P:452–463 proof conditions, включая last assignment/context/phase; shape-only record не bound evidence |
| unknown | Origin unknown/kindunknown/[]/непустой note | null | Только origin_not_recorded,override_unbound,conditions_unbound,source_unbound,value_unavailable | В note точный missing proof, numeric/assigning known могут сохраниться отдельно |
| not_applicable | Origin not_applicable/kindnot_applicable/[] | null | not_applicable | Owning applicability proof; отсутствие receipt не является not_applicable |

Resolver сначала отвергает доказанное противоречие/hash/context tamper attempted claim через ContractError; это не missing proof. Для остальных случаев reason выбирается конечным порядком: применимость явно not_applicable -> not_applicable; target phase value unavailable -> value_unavailable; retained evidence явно показывает unbound assignment/runtime override/derived step или target Atom отличается от reference -> override_unbound; известные applicability conditions противоречат retained context -> conditions_unbound; retained claim отсутствует -> origin_not_recorded; claim/source bytes/graph не доступны для проверки -> source_unbound; exact last-assignment binding receipt не подтверждён -> override_unbound; applicability unknown либо нет всех exact phase/context conditions -> conditions_unbound; только все proof checks -> bound/ok. Equal scalar не устанавливает отсутствующий proof. Порядок нужен лишь для нескольких одновременно отсутствующих proofs и не делает scientific attribution по string note. Если источник/контекст ещё не доступен для этих comparisons, соответствующий earlier mismatch не придумывается.

### R3: documentation binding, input_status и null obligations

| binding.status | Единственно допустимые reason | Identity scalars | fragment |
| --- | --- | --- | --- |
| bound | ok | release_id непустой retained string; release_manifest_sha256/source_revision/bundle_sha256 nonnull и правильного digest типа | Nonnull exact id/url/sha256 |
| unknown | source_binding_missing | Каждый scalar exact retained value, если verified/known, иначе null | null |
| incompatible | wrong_release,unsupported_version | Каждый scalar exact retained value, если verified/known, иначе null | null |
| unavailable | bundle_missing,fragment_missing | Каждый scalar exact retained value, если verified/known, иначе null | null |

`bound` schema branch требует nonnull descriptor и все identity scalars; semantic layer отдельно доказывает receipt→selected graph→bundle→fragment exact bytes. Source/release labels, model_revision, package version и equal number не заменяют этот proof. Unbound не обнуляет уже известные retained scalars. Обязательные trusted actor run_uuid/calcjob_uuid/attempt и frozen-plan context не становятся nullable из-за отсутствия docs/snapshot; конфигурационный hash null только когда declared passport отсутствует.

| input_status.status | Единственно допустимые reason | Used metadata |
| --- | --- | --- |
| available | ok | Snapshot metadata прошла выбранный child/path/hash/context checks; scalar known только при exact path mapping и retained value evidence |
| invalid | snapshot_invalid | used unknown, atom/evidencenull; raw invalid bytes сохраняются |
| unavailable | snapshot_missing,point_not_executed_by_selected_child,inventory_unavailable,inventory_incomplete | used unknown, atom/evidencenull; existing declared evidence сохраняется, когда есть exact retained slice |

Index valid/ok и invalid/non-ok matrix из inventory выше сохраняется. Все scalar known/unknown/null и assigning known/source-or-rule/evidence, unknown/kindunknown/null, redacted/source=null schema invariants обязательны. Для effective_origin known требуется полный verified chain; partial/unknown не повышается по cardinality evidence. input_status, documentation binding и value_origin — независимые axes; schema не выводит одну из другой. В частности available/ok допустим с fragmentnull и даже inputs=[] при отсутствии безопасной mapping; это статус selected-child metadata, не утверждение полноты projection.

### R4: единственный источник path slice и независимый used

Input paths берутся только из `inputs[].path` exact requested Fragment v1 **того же retained selected source context**. Для этого owning adapter должен иметь проверенные exact UTF-8 bytes Fragment и Bundle manifest, descriptor id/file/hash, manifest digest и graph, которые привязаны к этому selected run/execution retained source/release receipt. Manifest является уже существующим Bundle, а fragment — уже существующим accepted artifact; нового mapping registry/sidecar/receipt format нет. Hash/graph/selector metadata не принимается как голый unverified boolean. Проверенный fragment byte projection может храниться/читаться как immutable часть уже retained bundle; текущий installed fragment не заменяет отсутствующий.

Schema shape View не содержит hidden mapping field. Semantic helper получает exact fragment/manifest bytes и retained selection proof как detached internal inputs и проверяет: fragment.id=requested id, fragment.source_revision=retained graph revision, descriptor/hash и каждый projected InputView.path принадлежат этому fragment. URL в View остаётся null при небиндированном docs status; API не обещает served fragment, даже когда fragment bytes используются для безопасной projection.

Если точного retained fragment/manifest/mapping proof нет — `inputs=[]`. Context и input_status сохраняют доказанные selected-child факты; нельзя вместо missing mapping брать current fragment, global leaf list, first fragment, имя поля или план целиком. В частности source_binding_missing без доказанного selected source context не даёт права использовать source fragment как mapping.

Если mapping есть, declared и used оцениваются **независимо** по своим retained evidence. Missing/unserved docs asset/bundle может давать unavailable/bundle_missing и fragmentnull, но не обнуляет verified used snapshot этого selected child. Missing used snapshot не заполняется plan/default; declared из exact retained frozen point configuration остаётся known, когда его evidence доступно. Пустая mapping не объявляет отсутствующим сам snapshot; статус available/ok может сосуществовать с inputs=[]. Static value origin остаётся reference-only; actual origin требует отдельного receipt proof.

| Exact retained mapping | Snapshot/input evidence | Ожидаемый View projection при fragmentnull |
| --- | --- | --- |
| Нет | Любой snapshot availability | inputs=[]; trusted context/input_status truthful, no current fallback |
| Есть | Valid selected-child snapshot | Exact slice; declared/used каждый known только со своим evidence; docs unavailability не меняет verified used |
| Есть | Missing/invalid/unavailable snapshot | Declared может known из frozen passport; used unknown; typed input_status сохранён |

### R5: конечная pilot public-locator policy и её provenance

Для **public emission этого pilot** принимается query-free locator subset. Структурная проверка URI parser допускает только schemes https/doi, запрещает URI userinfo/credentials и control characters; https требует корректный absolute public URI. Любое presence query delimiter/component, включая пустой `?`, блокирует emission affected source/artifact. Query не вырезается/не переписывается, URL не fetch. `format:uri` и hash shape не заменяют эту проверку. No arbitrary secret scanner, token-name heuristics, новый trusted URI registry или public ingress.

Эта policy — конечный recipe/output restriction в accepted P:343–349,728–741 public source/allowlist review. Provenance: источник locator должен быть authored annotation/owning public source exact graph/revision/hash из versioned input allowlist уже reviewed recipe, а факт такого source review сохраняется в owning source/build review receipt. Query-free URI сама по себе **не доказывает** отсутствие private token в path, scientific origin или measurement; public-content review и output guards остаются обязательны. Нельзя автоматически объявить непроверенную строку known/public по одной схеме URI. При отсутствии exact source/recipe review evidence affected artifact остаётся unverified/rejected для publication; не создавать fake pass или silently заменять locator/Origin.

Query-bearing locator rejected в pilot до owning source/recipe review/replan; текущий packet не вводит query exception route. Harmless query support потребует последующего reviewed technical recipe contract с конкретным evidence; это не выбор для I данного packet и не новый запрос scope approval сейчас. Scientific model/value не меняются из-за этого ограничения публичного payload.

R6 error/unknown closure: internal helper не импортирует targets и не выполняет IO/derive, берёт bounded closed bytes и trusted selected context. Missing proof -> accepted unknown; проверяемое противоречие/attempted false bound -> existing ContractError. Одна schema validity или unverified status boolean не является retained source/release/origin/full-chain evidence.

### Mapping D1 review → D2 → append-only canonical proposal

Patch target — exact original DOC03 SHA256 `4b046312d0c1f04566c3a80ca6fb8a441ca7b025003c3c3b1c4c2bab2242f6cb`, 88916 bytes/967 строк. Candidate `/tmp/qcl-doc07-canonical-candidate.md` имеет неизменённый original byte prefix и добавляет только новый anchor `model-help-doc07-v1-clarifications` в EOF. Candidate SHA256 `fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794`; patch SHA256 `fc9cf40c2a19c7d98369dca72af0922f37906635f0003cb14a57525cc2bee2f5`. Root canonical по-прежнему original; эти hashes не заявляют публикацию.

| D1 review / primary locator | Закрытие в этом D2 | Candidate canonical строки |
| --- | --- | --- |
| R1; P:354–360,402–406 | Все десять, repeated contexts allowed, без max10 | 978–981 |
| R2; P:343–353,425–431 | Origin/Atom/ValueOriginView closed matrices; separate proof | 983–1010 |
| R3; P:505–538,663–675 | Binding/input_status enums и null obligations; independent axes | 1012–1036 |
| R4; P:508,536,659–675 | Exact retained fragment+manifest mapping, иначе inputs=[]; used independent | 1038–1059 |
| R5; P:345–349,728–741 | Query-free pilot emission + existing source/recipe review provenance | 1061–1077 |
| R6; P:452–475,643–661 | Private pure helper; missing vs corrupt proof; no new API/registry | 1079–1084 |
| Generator locator correction | P:226–228 вместо ошибочного235–237 | Canonical content без изменения |

## Узкая таблица owner fixtures и ожидаемый oracle

Все future fixtures synthetic, не production/science evidence. Для каждой негативной мутации сохранить исходный positive fixture и проверять обе стороны. Эти проверки сейчас **не исполнялись**.

| Fixture/control | Contracts oracle | Owning integration oracle вне Contracts |
| --- | --- | --- |
| Все пять complete happy objects | top-level union принимает каждый exact format; неизвестный format/extra field на любом уровне отвергается | Loader resource входит в штатный offline registry, no fetch |
| Ten facts | Удаление любого класса отвергается; явно unknown/not_applicable допустимы, не extraction pass | DOC06 source-only extraction не изобретает dynamic default |
| Known/unknown reference | Unknown Origin exact []/note; known reference сохраняется только reference object | Research public annotation/parameter hash проверены; UI reference-only подпись |
| Reference-vs-run и equal override | A=.10 и B=.15 без receipt => unknown/override_unbound; B=.10 с другой assignment/context также unknown | Runner не конструирует receipt из history; Portal не переносит static known в used |
| Origin proof positive | Exact A/annotation/public parameter/last assignment/conditions/phase/context/hash => bound ValueOriginView | Удалить по одному из четырёх proofs и каждого condition => unknown; fixture не production атрибуция |
| Declared→used runtime override | Declared proof не создаёт used bound без exact used proof | auto_exact/execution strategy/checkpoint restore отражены в used snapshot |
| Historical A / installed B | Exact retained A принимается; одинаковые id/label/number при graph B => incompatible/wrong_release и fragmentnull | Actor uses one selected child and retained receipt; no latest/current fallback |
| Missing/unavailable bundle/source | Missing public blob/selector/hash не проходит required source binding; bundle absent => unavailable/bundle_missing | No-source historical => source_binding_missing; existing submit/run сохранён |
| Invalid URL/private path | http/javascript/file/credential URI, traversal/dotfile/control/backslash unsafe path отвергаются; private assignment redacted/source=null, no basename | Collector checks symlinks and source maps; API response bytes не содержат private path |
| Finite Atom + known-null | scalar kind/type validation; NaN/Inf/-Inf/overflow 1e999/duplicate-key JSON reject before schema; known-null != unknown; boolean != integer | Runner dimensional adapter canonical units; no universal numeric/unit conversion |
| Two points / retry | P1/P2 distinct local context paths/hashes; wrong path/context/attempt/plan hash invalid; UUID injected rejects additional property | C2-imported P1 => point_not_executed_by_selected_child; original C1 bytes остаются доступны |
| Index size/incomplete | max10000/count; no acceptance of incomplete index; invalid too_large entry может иметь bytes>64KiB | Inventory aggregate guard до read; <=one guarded read/file; index before scientific early exits; raw retained |
| No snapshot | available declared evidence допускается при exact frozen passport; used atom/evidencenull + typed input_status | selected actor trusted UUID/attempt сохраняются; нет поиска других children/HDF5 |
| Wrong schema/media/hash | Exact branch version и source/byte binding проверены; syntactically valid hash недостаточен | DOC04 publish receipt и DOC05 browser/light/offline — отдельные later gates |

## Конечные implementation tasks после high R

### C1 — Single resource и shape fixtures

**Files:** create `src/qcl_negf_contracts/schemas/model-help.schema.json`; create `tests/test_model_help.py` и минимальные synthetic factory helpers в этом test file; README коротко назвать resource/format union и shape-vs-binding distinction. Existing package loader менять только при выявленном defect; не добавлять registry/version field.

**Consumes:** exact DOC03 digest, этот D2 и принятый independent high-review D2; closed R1–R5 и canonical append-only clarification. **Produces:** пять branch-valid synthetic fixtures, all nested objects closed, all ten fact coverage; existing resource loader/offline adapter понимает новый resource. Исполнитель не выбирает альтернативную R4/R5 semantics.

- [ ] Сначала shape tests exact fields/unknown/finite controls без запуска scientific modules.
- [ ] I запускает один targeted RED: existing prepared Python/pytest, `pytest tests/test_model_help.py tests/test_contracts.py::test_all_schemas_are_valid_and_references_stay_in_bundle tests/test_contracts.py::test_offline_validator_resolves_bundled_schema_references -q`; сохранить missing resource/contract failures, не чинить environment скрыто.
- [ ] Реализовать resource, без дублирования числа pins или formula text.
- [ ] Targeted GREEN тем же набором; успех требует всех checks, не exit code scientific process. Никаких full-suite/build/Julia/install.

### C2 — Pure semantic proof и fixtures

**Files:** create focused `src/qcl_negf_contracts/model_help.py` с private helpers R6; extend `tests/test_model_help.py`. No `__init__` re-export/API в этом scope.

**Consumes:** C1 schema-valid objects, closed byte inputs/selected graph/allowlists/frozen context и retained proof. **Produces:** verified unchanged objects или existing ContractError; accepted ValueOriginView с bound только при всех proofs и unknown при missing proof. Не новый public serialization.

- [ ] Сначала targeted semantic RED controls table: exact source/release/history binding, origin proof/remove-one, invalid public URL/private path, keyed collisions, wrong point/attempt/hash.
- [ ] Добавить D2 paired controls: unserved exact retained fragment + valid snapshot сохраняет known used при fragmentnull; missing exact mapping даёт inputs=[] с truthful input_status; query-bearing URI, включая пустой `?`, rejected без stripping; query-free reviewed-source control принят; known identity scalars сохранены на unbound branches; каждый недопустимый status/reason/null cross-pair rejected.
- [ ] Реализовать только cross-document relationships, переиспользовать existing finite JSON/path helpers настолько, насколько они покрывают accepted policy; missing unsafe-output checks не считать покрытыми existing `relative_path` (он не проверяет все P:736–739).
- [ ] Один targeted GREEN `pytest tests/test_model_help.py -q`; при budget stop сохранить исходный failure и конечный diff; дальнейшие попытки требуют нового finite packet, без autonomous retry до pass.

### C3 — Component review и handoff

- [ ] Source/diff/link checks; no numerical claims. Fresh independent R `high` получает exact component commit/tree + canonical DOC03 digest + raw RED/GREEN outputs, без готового диагноза.
- [ ] Owner Contracts PR публикуется отдельно, затем root обновляет опубликованный gitlink. Не выполнять commit/PR в текущем design stage.
- [ ] Handoff Core/Research fragments, Runner local snapshot, AiiDA index/actor, Portal view/serving и DOC04 collector только с принятым resource, proof rules и fixture bytes; они остаются owning отдельными PRs.

Предлагаемый следующий I envelope, который Root должен сопоставить с уже активным общим grant: одна подготовленная Python среда; не более 2 RED + 2 GREEN targeted invocations суммарно, <=15 min wall, <=1 CPU/2 GiB RAM, output<=128 KiB; без network/install/full suite/build/solver. Это recommendation, не измеренное resource admission и не исполненная проверка.

## Self-review и evidence limits

Coverage: P:324–408 resource/shared types/bundle/fragment; P:412–480 origin proof; P:485–538 API view; P:542–601 snapshot; P:605–690 index/retrieval; P:694–722 unknown/compatibility; P:726–785 allowlists/limits/build; P:789–835 serving/UI; P:839–872 controls. Serving/browser/math/OFL/native BUILD остаются dependencies, не Contracts tests.

Проверка source-only: exact DOC03 digest подтверждён shell SHA256, Contracts base/clean подтверждены Git; loader/offline/finite/path routines и existing schema/test patterns прочитаны в D1, narrow primary ranges повторно сверены в D2. Python/parser/schema/import/runtime/build/tests не запускались. Научная correctness/convergence/accuracy/experimental validity не исследовались. D1 independent high-review потребовал эту narrow D2; свежая high-review D2 пока не выполнена, Root должен передать exact D2/patch digests рецензенту до I.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Один schema resource может покрыть все пять accepted documents | DOC03 exact digest P:326,389,504,556,619; existing dynamic loader at Contracts12fc264 `__init__.py` | Resource ещё не реализован; schema-valid не binding-valid | изменить |
| Нужна отдельная проверка source/release/context/origin proof | DOC03 P:452–475,643–661,715–722; closed D2 R2–R6 | Private helper не public API; original receipts отсутствуют у existing plans | изменить |
| Existing plan без retained capture receipt остаётся actual-origin unknown | DOC03 P:465–475, snapshot origin_bindings=[] | Это не запрет exploratory solve и не scientific rejection | сохранить |
| Public-ready/DOC04 browser/native pass пока не доказан | DOC04 dependency state и P:760–785,839–858 | Текущий source-only этап не исполняет эти проверки | данных недостаточно |
| D2 choices закрыты для повторного independent R | R1/R6 approved D1 review; exact D2 matrices/R4/R5 и append-only patch | D2 high-review ещё не выполнена; canonical root пока не изменён | дополнительно измерить |
