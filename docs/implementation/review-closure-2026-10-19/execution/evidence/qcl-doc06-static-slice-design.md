# DOC06 — source-only fixed API/config prototype

2026-10-20. D ultra, для независимого high R перед medium I. Только design;
target imports/parsers/eval/tests/build/network не выполнялись. DOC04 BUILD,
render/asset/native admission и scientific grants не наследуются.

## 1. Scope и primary facts

Observed Root `514cd9707a32cde60c630d60986973a898d35b18`, canonical
physics-documentation.md SHA256
`fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794`.
Fixed slice: Runner `configuration_source` и leaf `production.energy_chunk`.
Selected sources: Runner1acc165650fd4f4c2d49605cc679f90e3f6fcdae,
Contracts12fc26462bbab3df76904c6deb01f8c6596de7be,
Coree431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee. Full hashes/locators/read ledger
находятся в companion source ledger. Pending Contracts C1/model-help resource
не selected authority; prototype не объявляется DOC03-conformant fragment.

Primary distinctions:

- Runner configuration_types.jl: documented two-argument API, typed declaration
  принимает ResolvedRunConfiguration и AbstractString. Lookup возвращает последнюю
  recorded history entry либо nothing при absent/empty history; не загружает
  source, не назначает default и не восстанавливает effective causal chain.
- Contracts run.schema.json: /properties/production/$ref → #/$defs/production.
  **Точный JSON Pointer leaf: /$defs/production/properties/energy_chunk**;
  required membership — /$defs/production/required. Integer>=1, default отсутствует.
  Runner packaged schema имеет те же54815 bytes/SHA62df4ac2…0e58b.
- Core ProductionOptions source отдельно объявляет energy_chunk::Int=64;
  _check_production_options отдельно требует >0. Это не schema assignment.
- Runner base fixture явно задаёт64. Docs'17/23 override example — authored
  synthetic expectation, не измерение и не результат вычисленного adapter merge.
- Runner _deep_merge! записывает absolute assigning filenames; auto_exact может
  менять chunk по ExecutionPlan и добавлять application:auto_exact. Статический
  prototype не читает реальную configuration/plan и не публикует private filenames.

Всё это source observations, не runtime method inventory или научная приёмка.
Tiny proposed canonical pointer erratum сохранён отдельно как candidate patch;
исходные fe1 bytes не менялись. Других DOC03 изменений нет.

## 2. Минимальный owning I

Root `ops/docs/static-slice.ts` — небольшой fixed-profile Deno adapter;
`tests/docs_static_slice_test.ts` — focused pure data controls. Никаких generator
или parser dependencies, Julia reflection, config loader, plugin loading,
Documenter inventory, live API, UI/code/model registry. Existing Documenter остаётся.
Новый authored научный текст или дублирующий справочник не нужен: short meaning
копируется/цитируется из existing owning docstring, schema description и Runner
configuration route; inferred rationale/DOI/used value не генерируются.

Future medium I envelope:≤40min,1CPU/2GiB,read≤2MiB,patch/report≤96KiB.
После source freeze — отдельный high R. Предлагаемые pure checks: одна RED и одна
GREEN invocation в существующем locked Deno2.8.3, каждая≤120s,1CPU/1GiB,
logs≤1MiB, owned temporary≤8MiB. Exact command/source/harness binds coordinator;
нет automatic third run, installation, full CI, Julia/Nix или DOC04 render.
Эта спецификация не выполняет и не разрешает запуск сама по себе.

## 3. Exact input boundary

Prototype читает ровно9 allowlisted files из detached exact source snapshot:

```text
runner/src/application/configuration_types.jl
runner/src/infrastructure/config/configuration.jl
runner/src/infrastructure/config/configuration_sources.jl
runner/src/application/auto_strategy.jl
runner/docs/src/user/configuration.md
runner/test/fixtures/configurations/base.yaml
runner/schema/run.schema.json
contracts/src/qcl_negf_contracts/schemas/run.schema.json
core/src/numerics/optimized/production_contracts.jl
```

owner aliases выше разрешаются только через existing generated sourceGraph;
реальные PublicRef component paths — components/QCLNEGFRunner.jl,
components/qcl-negf-contracts,components/QCLNEGF.jl. Не проходить include graph,
не искать по corpus, не читать .git objects из Deno и не исполнять git subprocess.
Root source-preparation отдельно связывает snapshot bytes с exact selected graph.
Его ephemeral source receipt — производное evidence, не новый вручную maintained
component lock. Adapter проверяет full file bytes/SHA/size against receipt;
сам не доказывает Git commit-to-bytes binding и сообщает это ограничение.

CLI logical contract:
`static-slice.ts --snapshot DIR --source-receipt FILE --out NEW_DIRECTORY`.
Strict options, fresh output directory, no source/output overlap. Symlink/escape,
absolute/traversal input path, wrong owner/unknown file/hash mismatch — refusal.
Source receipt≤16KiB; files≤12, file≤128KiB, aggregate source≤512KiB. Fixed input
list, no recursive directory discovery. Reads are bounded before allocation;
UTF-8 strict; lexical text normalization LF is recorded, raw SHA uses original bytes.
No SOURCE/DEPOT/ENV interpolation and no fallback to installed/latest packages.

Future Deno process has read permission only for script/fixture snapshot/receipt,
write only for fresh owned output; no allow-run/net/env/ffi. Trusted adapter/test
imports are local fixed tooling only; no dynamic import()/eval()/Function()/
WebAssembly or loading target .jl/.json/.yaml as modules. No fetch or Pkg calls.
Version2.8.3 is the selected future toolchain requirement, not a measured native
binary identity in this D. Package/plugins/config code is always input bytes.

## 4. Narrow extraction grammar — no target interpretation

The adapter is a fixed source projection, not a Julia parser or validator of
arbitrary configuration. Exact source selectors and unsupported branches are
part of versioned profile `configuration-source-energy-chunk-v1`.

### Julia source

Recognize the immediately associated literal triple-quoted documented signature
and the literal typed declaration header for configuration_source. Accepted
header: function name, multiline parenthesized list of exactly the two named
arguments, ::ResolvedRunConfiguration and ::AbstractString, commas/whitespace,
then closing parenthesis. No where/default/macro-generated method is evaluated.
Documented signature is a known literal documentation fact. Typed header is a
partial textual declaration observation, explicitly not exhaustive method inventory.

Only the exact reviewed ProductionOptions textual struct/field location is
used for typed default: energy_chunk::Int = unsigned decimal integer literal.
Int literal must be safe finite JSON integer. A call, interpolation, arithmetic,
ENV lookup, type macro or other RHS returns partial with null extracted literal;
never evaluate, constant-fold or reuse previous64. Method bodies, guards, include
and planner code are not interpreted. Their documented meaning is authored
context with exact refs, and effects/error completeness stays partial where needed.

The recognizer distinguishes comments/literal strings in the bounded selected
region and rejects ambiguous/multiple target matches. A target occurrence in a
comment/string or metaprogramming wrapper is not promoted to a known runtime
declaration. Unsupported context gives partial/unknown at the affected fact.
It may still copy an independently literal documented signature, labelled as
documentation only. Other source text is not an execution permission or full
coverage claim. Sentinel content is always inert bytes.

### Schema

Use built-in JSON.parse only, with bounded lexical precheck for depth≤32,
tokens≤32768, strings≤16KiB, duplicate object keys, safe/finite numbers and
forbidden prototype keys in dictionaries used by the adapter. This is data
checking, no new package parser/validator framework. JSON syntax/duplicate-key/
nonfinite/shape failure records malformed_schema; no stale fallback.

Project only root required-production membership, local $ref chain, production
object/required membership and energy_chunk's type/minimum/default/description.
Resolve JSON Pointer escapes ~0/~1, own properties only, ≤8 local-ref hops,
cycle detection. Remote $ref is never fetched; unsupported constructs produce
partial with source file/selector and reason. Minimum must be finite number,
type integer exact, required array unique strings; description literal string.
Missing default → not_assigned in **schema** context. Present literal default is
reported as declaration only, never applied to a configuration. Unrecognized
validation combinators/keywords affecting the selected path remain partial;
do not claim complete schema/instance validation from this projection.

Compare Runner packaged schema bytes with selected Contracts source before
describing them as identical. Mismatch is an explicit diagnostic; the canonical
Contracts projection and packaged mismatch remain distinct, not merged silently.

### Example and authored context

Optional illustrative scalar extraction supports only the selected base fixture's
unique top-level `production:` block and two-space `energy_chunk: DIGITS` leaf,
with whitespace/comment suffix. No YAML parser, tags/anchors/aliases/merge keys,
expressions, includes, environment/config evaluation or deep merge. Unsupported
target syntax → partial example fact, not an inferred default or runtime value.
Other YAML sections are opaque and are not declared validated.

Short authored meaning/override explanation comes from the existing Runner
configuration section and configuration_source docstring. Store exact excerpt
selectors in source receipt. The17/23 expectation is quoted as a synthetic source
example; adapter never loads those YAMLs or executes the Julia inspection block.
Owner/source distinction and generic missing-data notes may be authored in the
view, with receipt mode=authored-context; they are not presented as extracted
code proof. No material formula, threshold rationale or actual value origin is
invented from an identifier.

## 5. All ten fact classes, with honest modes

Both subjects cover all ten names. Multiple rows per class are permitted,
especially the three distinct default contexts. Fact shape remains exactly
{name,status,text,sources} from accepted DOC03; per-fact extraction mode and
selector diagnostics live in the separate prototype receipt, not added to Fact.
Status vocabulary: known/partial/unknown/not_assigned/not_applicable.

| Class | configuration_source | production.energy_chunk |
| --- | --- | --- |
| signature | known documented text; separate partial typed-header observation | known schema type; partial textual Int field declaration, no runtime inventory |
| units | authored not_applicable for source identifier/nothing | authored known count of energy nodes; dimensionless count, not eV/grid spacing, citing schema description/owning route |
| default | not_assigned for argument defaults in recognized header | schema not_assigned; typed literal64 known; explicit example64 known — separate rows/contexts |
| constraint | partial typed argument constraints; no schema validation inferred from lookup | known direct integer/minimum1/required declarations; any unhandled path condition partial |
| effects | known documented provenance-only lookup; full call/runtime effects not certified | authored scheduling meaning from schema/route; no scientific task/model change inferred or executed |
| errors | partial/unknown: docstring is not an exhaustive throws contract | partial: direct schema rejection/known Core guard source are not a complete loader error inventory |
| formula_origin | authored not_applicable for this lookup | authored not_applicable for scheduling count; no physical equation generated |
| value_origin | not_applicable for physical numeric-value origin; no actual returned identifier supplied | partial source code policy/default context; actual instance numeric origin unknown |
| assigning_origin | partial: documented last recorded identifier rule; actual history absent | partial static merge/marker explanation; actual assigning identifier unknown |
| effective_origin | unknown: no retained run/execution context | unknown: no effective configuration/ExecutionPlan/snapshot; no backfill from64/17/23 or application:auto_exact |

All known semantics explicitly say documented/authored/source declaration where
appropriate. Partial/unknown is not extraction pass. Equality of schema/typed/
example values does not establish origin. Static source cannot identify a
private effective override or its full causal chain.

## 6. Standalone output and reproducibility

Produce one bounded `facts.json`, plus private `source-receipt.json` and optional
bounded diagnostics text. Prototype wrapper format
`qcl-negf.doc06-static-slice.v1` is local DEV output, not a shared format/schema:

```text
{format, profile, source_manifest_sha256,
 subjects:[{kind:'api'|'input',key,facts:Fact[]}],
 coverage:{fact_classes,scope:'fixed-slice',status:'partial'},
 binding:{status:'source-prototype',application_release:null,run:null}}
```

No DOC03 bundle/generator/DocRef compatibility claim until selected published
Contracts shared resource exists and integration independently validates it.
Do not copy the pending C1 schema or generate a replacement registry. Source refs
use selected full owner revisions, repo-relative allowlisted paths, full raw
source SHA256 and exact symbol/JSON-pointer/file selectors. Missing source has
no fabricated hash/PublicRef. Header/tool name does not prove commit binding.

Receipt fields: tool/profile identity, supplied graph/manifest digest and external
binding limitation, each input path/revision/expected+actual hash/bytes/status,
per-subject/fact-index mode (literal-extraction|authored-context|dynamic-unknown),
selectors/unsupported reasons, aggregate source bytes, output hash/bytes and
result produced/partial/refused. Unknown sizes/hashes=null; never0. No private
paths/filename histories or credentials in facts. No run_uuid/release invented.

Canonical UTF-8/LF JSON, fixed key/order and source/fact ordering, two-space
indent/final newline; no timestamps, temp paths, random IDs or host facts in
facts.json. Same source/profile bytes must produce identical output SHA.
Limits: text≤2048 chars/fact, selected docstring≤4096 bytes, signature≤512 bytes,
facts.json≤32KiB, receipt≤32KiB, diagnostic output≤8KiB. Overrun refuses rather
than truncating JSON or dropping fact classes. Any partial artifact is clearly
labelled; it is not an admitted public bundle. No HTML/palette/help UI is created.

## 7. Required controls — future pure execution only

| Control | Distinguishing assertion |
| --- | --- |
| Positive frozen source | Documented two-argument signature, exact schema pointer/type/minimum/required/default-absent, typed64 and example64 separate; all10 classes per subject; actual origins remain unknown; deterministic bytes twice |
| Missing configuration_types or schema | Dependent facts unknown/partial with source_missing; no stale/default backfill; unaffected independently sourced facts retain their own evidence |
| Malformed schema | Invalid JSON, duplicate energy_chunk key, wrong minimum type, missing/cyclic local ref, nonfinite/unsafe number rejected or classified unsupported; no network/fallback |
| Unsupported dynamic construct | Replace default RHS with ENV/call, macro-generated signature, selected YAML alias/tag or schema combinator: affected values null+partial reason, never eval/constant-fold; documented facts may remain independently literal |
| Sentinel module | Target bytes include top-level code that would write a marker under owned writable temp if evaluated; adapter returns bounded supported/partial data and marker stays absent. Include a valid JS sentinel raw-data control so no-eval evidence is not only a Julia syntax failure |
| Source identity mismatch/private path | Explicit refusal; no public projection from wrong bytes or escaping/symlink path |
| Overrun | Source/file/depth/token/output caps refuse before over-allocation; no truncated success |

Tests import only the trusted adapter, pass target code as inert bytes/files and
observe marker absence plus absence of target process/module loading in code
review. Sentinel absence alone is not universal no-execution proof. No Julia
configuration methods or plugin callbacks serve as expected-value oracles.

## 8. Acceptance and scope stop

Independent high R checks primary facts/locators, exact unsupported branches,
default/override/owner distinction, all ten classes, no target execution path,
finite permissions/caps, deterministic output and meaningful controls. Medium I
may proceed after that review/coordinator binding without waiting for DOC04
native BUILD or DOC07 UI. Source-only checks do not claim target runtime/science.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Static fixed slice is useful without target imports | Primary declarations/schema/docstring and explicit grammar above | No dynamic method/config/plan evaluation | изменить |
| Schema, typed default, example and actual origin differ | Pointer chain, Core64, fixture64, Runner provenance/auto_exact source | Actual run/history/snapshot absent | сохранить |
| Full API/errors/effective origin can be generated from this text | Missing runtime/authoring proof; explicit partial/unknown facts | No inferred rationale/physical applicability | данных недостаточно |

STOP after frozen D/identity/ledger/erratum; no product or checkpoint writes.
