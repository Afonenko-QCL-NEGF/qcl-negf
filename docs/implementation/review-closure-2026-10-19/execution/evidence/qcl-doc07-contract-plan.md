# DOC07 Contracts schema-first: design и конечный implementation packet

> Для следующего исполнителя: выполнять только после независимого R `high` этого packet. Implementation — отдельный I `medium`; текущий этап source-only DESIGN/DOC. Путь artifact задан поручением, поэтому plan хранится в `/tmp`, не меняет owning source или execution checkpoint.

**Цель:** реализовать ровно принятые DOC03 форматы model/source help в одном Contracts resource `model-help.schema.json` Draft 2020-12 и отдельно проверить неизбыточные semantic bindings; reference origin не становится origin конкретного run по совпадению числа.

**Архитектура:** Contracts владеет формой и чистыми cross-binding проверками. Existing loader/offline validator автоматически обнаруживает schema resource. Core/Research авторствуют смысл/reference annotations; Runner выдаёт local metadata; AiiDA проверяет retrieved bytes и обогащает выбранным child; Portal проецирует scalar metadata и показывает exact retained fragment. Это не новый model registry, capture API или независимый release manifest.

**Стек:** existing pure Python Contracts, existing optional `jsonschema` Draft202012Validator + `referencing` offline registry; без новых dependencies. Source-only design не импортирует эти модули и не запускает validator.

**Spec:** `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/docs/system/physics-documentation.md:324–877`, exact SHA256 `4b046312d0c1f04566c3a80ca6fb8a441ca7b025003c3c3b1c4c2bab2242f6cb`. Дальнейшие локаторы `P:N` означают строку N этого exact файла. DOC07 card: `docs/implementation/review-closure-2026-10-19/documentation-instructions.md:162–182`.

## Authority и границы

- Root HEAD фактически `d4113f43cddf02d46025434eb3a9dd8e110e90d6`; Contracts checkout и опубликованный gitlink `12fc26462bbab3df76904c6deb01f8c6596de7be`, Contracts worktree clean при чтении. Root уже содержит чужие working changes Results/execution receipts; они не входят в этот packet и не изменялись.
- DOC03 technical contract принят; product implementation не подтверждена этим текстом (P:196–214). Feature DOC07 уже в EXEC scope; нового запроса на включение feature не требуется.
- DOC04 сейчас blocked на shared schema/public OFL/native BUILD; локальные adapters разрабатываются. Этот packet не означает public bundle ready, установленный release, browser/offline pass или numerical/scientific acceptance.
- Не создавать source graph lock-файл; source composition authority — existing Git gitlinks и `ops/git.ts:sourceGraph`. DOC03 source-facts root `9d8cf0c…` — исторический локатор наблюдений, не текущий root identity.
- Не менять scientific-plan/result schemas, result contract registry, archive/recovery closure, numerical defaults/criteria, dependencies или format versions.
- Текущий envelope: <=30 min, 1 CPU, 2 GiB RAM, logical source reads <=4 MiB, tool output <=128 KiB; no solver/build/parser/import/runtime/tests/network/children/commits/push/checkpoint writes. Выполнены только Git/read-only text/hash operations и запись этого `/tmp` design artifact.

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

Schema conditional minimum, который прямо следует из текста: Origin unknown => kind unknown, locators=[], непустой note; known research_assumption с [] => непустой note, именующий owning assumption. Quantity/number значения numeric; integer JSON integer (boolean не integer), boolean boolean, enum string, null JSON null; unit string|null. Пары quantity/unit, not_applicable origin и дополнительные known-kind ограничения вынесены на focused R ниже, а не молча ужесточены.

Для каждого `facts` в fixed slice schema `allOf` + `contains` обеспечивает присутствие всех десяти names, включая explicitly not_applicable/unknown. `uniqueItems:true` не обеспечивает uniqueness по name и не заменяет coverage. Accepted текст не требует ровно десять записей: не ставить `maxItems:10` до решения R1. Так один default fact может явно описать schema и typed context; существование числа 64 не выбирает один из них.

## Bundle/fragment: exact inventory

`Bundle.sources` — existing generated `qcl-negf.git-graph.v1` object ровно `format,revision,components`; components[] ровно `path,revision,url`, sorted по path. Это структурное описание existing graph внутри schema, не ручной набор выбранных eight pins. Dynamic graph equality/membership проверяются semantic layer.

`Bundle.schema` — PublicRef Contracts `model-help.schema.json`, selector file. `generator` — ровно `name,version,uuid,git_tree_sha1,julia_version,project_sha256,manifest_sha256,recipes,toolchain_lock`: const Documenter/1.17.0/Julia1.13.0; UUID `e30172f5-a6a5-5a46-863b-614d45cd2de4`; git_tree_sha1 `56e9c37b5e7c3b4f080ab1da18d72d5c290e184a`; SHA256 fields, recipes PublicRef[], toolchain_lock PublicRef (P:235–237,371).

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

Предложение internal routine contract для R, **не объявление нового public Python API**: новый focused module `src/qcl_negf_contracts/model_help.py`; внутренние `_validate_model_help_bindings(document, *, retained)` и `_resolve_value_origin(reference, claim, *, phase, retained)` могут называться иначе до owning review. Первый принимает уже finite-decoded schema-valid object и detached immutable validation inputs; возвращает тот же object или existing ContractError. Второй строит ровно accepted ValueOriginView (без wrapper/receipt format); при отсутствующем proof возвращает unknown с accepted reason, при corrupt binding не выдаёт bound. Exact exported callable, если потребуется consumers, должен быть утверждён R, а не случайно стать public по имени этого packet.

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

## Focused R: решения до I, без нового scope approval

| Вопрос | Accepted факт / недостаток exactness | Минимальная рекомендация для R |
| --- | --- | --- |
| R1 Fact multiplicity | P:402 требует все десять классов; uniqueness по name/ровно10 не сказано; default contexts могут различаться | Обязательное присутствие каждого name; repeated names пока разрешены. Если нужен ровно один/class, закрепить решение в canonical DOC03, не только test |
| R2 Origin/Atom status matrix | Unknown exact; known/not_applicable cross-kind и unit applicability частично семантические | Known kind исключает unknown/not_applicable; not_applicable kindnot_applicable/locators[]; bound view требует known Origin+binding+ok, not_applicable view соответствующий Origin/null/not_applicable. Quantity numeric/string unit; остальные exact type, unit string|null. Подтвердить эти derived invariants, не изобретать unit catalog |
| R3 Binding/input reason matrix | Перечислены enums, примеры закрепляют wrong_release=incompatible, source_binding_missing=unknown; полный map не выписан | Bound/ok; unknown/source_binding_missing; incompatible/wrong_release или unsupported_version; unavailable/bundle_missing или fragment_missing. Input available/ok, invalid/snapshot_invalid, остальные unavailable. Сохранить известные nullable identity scalars у unbound, не требовать обнулить известную identity |
| R4 Inputs при fragment=null | P:508 только paths fragment.inputs; P:536 fragment=null unbound; P:673 historical frozen input даёт declared. Не определён path projection без доступного retained fragment | Не обращаться к current fragment. При отсутствии exact retained path mapping inputs=[]; при наличии exact retained mapping допускается declared projection без подмены fragment. R должен явно выбрать/закрепить этот branch, прежде чем I формализует его |
| R5 Public locator query safety | Accepted https:/doi: и запрет credentials/query secrets; детерминированное понятие secret query не задано | Scheme/control/userinfo/traversal запреты реализуемы; не создавать эвристический secret detector. R выбрать narrow no-query subset либо существующую reviewed exact public-locator allowlist для harmless queries; не молча заявлять full safety лишь по `format:uri` |
| R6 Shared semantic helper boundary | DOC03 требует validator, но не public function/module signature и не retained-release-receipt schema | Подтвердить focused pure module/internal call contract выше; не вводить новый receipt format/API. Retained claims/public bytes приходят от owning adapters, shape-only schema validation не поднимает bound |

Неизвестные поля не заполнять догадками. Эти вопросы — owning technical design review в уже принятом scope. До решения R4 нельзя считать view schema/public consumer contract окончательно ready. Остальные независимые schema branches можно специфицировать/готовить после high-review packet.

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

**Consumes:** accepted DOC03 digest и R1–R5 decisions. **Produces:** пять branch-valid synthetic fixtures, all nested objects closed, all ten fact coverage; existing resource loader/offline adapter понимает новый resource.

- [ ] Сначала shape tests exact fields/unknown/finite controls без запуска scientific modules.
- [ ] I запускает один targeted RED: existing prepared Python/pytest, `pytest tests/test_model_help.py tests/test_contracts.py::test_all_schemas_are_valid_and_references_stay_in_bundle tests/test_contracts.py::test_offline_validator_resolves_bundled_schema_references -q`; сохранить missing resource/contract failures, не чинить environment скрыто.
- [ ] Реализовать resource, без дублирования числа pins или formula text.
- [ ] Targeted GREEN тем же набором; успех требует всех checks, не exit code scientific process. Никаких full-suite/build/Julia/install.

### C2 — Pure semantic proof и fixtures

**Files:** create focused `src/qcl_negf_contracts/model_help.py` только после R6; extend `tests/test_model_help.py`. No `__init__` re-export/API без R6.

**Consumes:** C1 schema-valid objects, closed byte inputs/selected graph/allowlists/frozen context и retained proof. **Produces:** verified unchanged objects или existing ContractError; accepted ValueOriginView с bound только при всех proofs и unknown при missing proof. Не новый public serialization.

- [ ] Сначала targeted semantic RED controls table: exact source/release/history binding, origin proof/remove-one, invalid public URL/private path, keyed collisions, wrong point/attempt/hash.
- [ ] Реализовать только cross-document relationships, переиспользовать existing finite JSON/path helpers настолько, насколько они покрывают accepted policy; missing unsafe-output checks не считать покрытыми existing `relative_path` (он не проверяет все P:736–739).
- [ ] Один targeted GREEN `pytest tests/test_model_help.py -q`; при budget stop сохранить исходный failure и конечный diff; дальнейшие попытки требуют нового finite packet, без autonomous retry до pass.

### C3 — Component review и handoff

- [ ] Source/diff/link checks; no numerical claims. Fresh independent R `high` получает exact component commit/tree + canonical DOC03 digest + raw RED/GREEN outputs, без готового диагноза.
- [ ] Owner Contracts PR публикуется отдельно, затем root обновляет опубликованный gitlink. Не выполнять commit/PR в текущем design stage.
- [ ] Handoff Core/Research fragments, Runner local snapshot, AiiDA index/actor, Portal view/serving и DOC04 collector только с принятым resource, proof rules и fixture bytes; они остаются owning отдельными PRs.

Предлагаемый следующий I envelope, который Root должен сопоставить с уже активным общим grant: одна подготовленная Python среда; не более 2 RED + 2 GREEN targeted invocations суммарно, <=15 min wall, <=1 CPU/2 GiB RAM, output<=128 KiB; без network/install/full suite/build/solver. Это recommendation, не измеренное resource admission и не исполненная проверка.

## Self-review и evidence limits

Coverage: P:324–408 resource/shared types/bundle/fragment; P:412–480 origin proof; P:485–538 API view; P:542–601 snapshot; P:605–690 index/retrieval; P:694–722 unknown/compatibility; P:726–785 allowlists/limits/build; P:789–835 serving/UI; P:839–872 controls. Serving/browser/math/OFL/native BUILD остаются dependencies, не Contracts tests.

Проверка source-only: exact DOC03 digest подтверждён shell SHA256, Contracts base/clean подтверждены Git; loader/offline/finite/path routines и existing schema/test patterns прочитаны. Python/parser/schema/import/runtime/build/tests не запускались. Научная correctness/convergence/accuracy/experimental validity не исследовались. Независимая high-review этого packet пока не выполнена; root должен дать его свежему рецензенту до I.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Один schema resource может покрыть все пять accepted documents | DOC03 exact digest P:326,389,504,556,619; existing dynamic loader at Contracts12fc264 `__init__.py` | Resource ещё не реализован; schema-valid не binding-valid | изменить |
| Нужна отдельная проверка source/release/context/origin proof | DOC03 P:452–475,643–661,715–722 | Public helper signature/R4/R5 не закреплены; original receipts отсутствуют у existing plans | изменить |
| Existing plan без retained capture receipt остаётся actual-origin unknown | DOC03 P:465–475, snapshot origin_bindings=[] | Это не запрет exploratory solve и не scientific rejection | сохранить |
| Public-ready/DOC04 browser/native pass пока не доказан | DOC04 dependency state и P:760–785,839–858 | Текущий source-only этап не исполняет эти проверки | данных недостаточно |
| Semantic edge choices требуют focused independent R | R1–R6 выше с exact primary locators | Нельзя утверждать окончательный ready-contract до R | дополнительно измерить |
