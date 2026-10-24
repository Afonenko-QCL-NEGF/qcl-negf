# DOC04 — owning recipes: medium I packet and BUILD admission boundary

2026-10-20. Source-only focused design, based on accepted DOC04 D/R. No product
edits or execution. Scope: Core/Runner pilot profile, root operator recipe and
root finite orchestrator; no new framework/dependency, solver/model change,
DOC03 schema copy, CSP relaxation, deploy or serving change. Independent high R
must precede I. **This packet does not admit BUILD.**

## 1. Frozen inputs and status

Accepted D `/tmp/qcl-doc04-design.md`, SHA256
`77ee8593655f98b2e66d762620279ba6ac7ec7da126c62a2ccbd56a0262bf12b`;
R `/tmp/qcl-doc04-design-review.md`, SHA256
`6caa4f15035e6a9f564d1ec86f14ecd64bbd31d73457556327e090e9d6628164`.
Plan `/tmp/qcl-doc04-root-worktree/ops/docs/pilot-plan.json`, SHA256
`cde7ee8b4e19878eeda8e92b4cfe6167b105dd3440409da351c0039e600e9e50`.
Root source HEAD observed `d4113f43cddf02d46025434eb3a9dd8e110e90d6`, with
coordinator/other writers' dirty files retained. Composition source is Git:
selected Coree431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee and
Runner1acc165650fd4f4c2d49605cc679f90e3f6fcdae. Do not build the mutable root
worktree or turn this packet into a second revision lock. Later publication
must select reviewed owning commits and a clean exact sourceGraph.

Operator reviewed source at `/tmp/qcl-doc04-operator-worktree/docs/public/operator-recovery.md`
has SHA256 `8f05ff4cced8579b09cccd4b4315101e861e1896b87321b42e597374da79de49`.
Coordinator reports its independent R passed; this author does not close that R.
No execution logs/private deployment material become recipe input or public prose.

Root locked project selects Julia1.13.0 and Documenter1.17.0,
UUIDe30172f5-a6a5-5a46-863b-614d45cd2de4, expected tree
56e9c37b5e7c3b4f080ab1da18d72d5c290e184a. The installed AXNMp source exposes
the public kwargs used below; complete tree/native/cache identity remains a
prerequisite. Standalone Runner docs/Project selects Corev0.2.0 and cannot supply
the pilot environment. No Pkg.instantiate/develop/update/precompile/bootstrap or
download is hidden in the recipes.

Companion `/tmp/qcl-doc04-recipes-source-effect-ledger.md` enumerates exact page
scope, directive observations, include/init/workload edges and unknowns. A broad
grep included static assets; its conservative scan breadth exceeded4MiB. Further
target-source reads stopped and this limit was reported. This packet does not
claim completed import/effect closure; completion is an explicit pre-render gate.

## 2. Owning I units and finite bounds

| Unit | Allowed product changes | Result / review boundary |
| --- | --- | --- |
| I-Core | Core docs/make.jl only | Conditional pilot branch; unchanged normal branch/navigation/doctest contract |
| I-Runner | Runner docs/make.jl only | Same, root environment only in pilot; no docs/Project dependency change |
| I-Root | Root docs/public/make.jl and ops/docs.ts; focused pure orchestration fixture test if needed | Operator staging + finite orchestration; consumes reviewed assembler/schema/runtime, does not rewrite them |

One medium writer per owning I unit. Source authoring/review preparation envelope
for these units combined:45min,1CPU,2GiB, named source reads≤3MiB,
patch/report output≤128KiB. This is a proposed finite I envelope for coordinator
binding, not a grant to execute now. No Julia/Nix/render/package setup/full CI
or scientific run in I. Relevant pure Root harness checks, if separately admitted,
are bounded to one RED and one GREEN,≤120s each,1CPU/1GiB,logs≤2MiB/attempt;
fake executables only, no Julia/solver. Do not spend a third run automatically.
Owning R checks actual diff/default branch preservation and meaningful gate cases.

Root adapters under CPP2 are independent frozen inputs. Do not modify their
implementation, math policy, shared DOC03 schema or assets pins in this I unit.
If their final API differs from accepted D, bind exact names after their R;
do not invent an adapter entrypoint now. A missing API binding blocks only the
dependent Root integration claim; Core/Runner source profile edits can proceed.

## 3. Pilot profile: exact control flow and public API

All three recipes use `QCL_DOCS_PROFILE`:

- Unset/empty: Core/Runner take the existing normal branch unchanged, including
  using owning package/Documenter, existing DocMeta DocTestSetup, page graph,
  doctest=true, checkdocs=:exports,warnonly=false and normal output paths.
- `pilot-v1`: validate mandatory root-supplied path/profile context before
  `using QCLNEGF`/`using QCLNEGFRunner`/`using Documenter`; then use the pilot
  branch. Root operator recipe has only this explicit profile.
- Any other nonempty value: error before owning-package imports or output writes.

Root supplies exact absolute paths via `QCL_DOCS_ROOT`, `QCL_DOCS_SOURCE`,
`QCL_DOCS_BUILD`; these are private attempt paths, not public payload values.
ROOT is selected source root, SOURCE is its isolated staged owner source,
BUILD is its isolated raw owner output. Missing/relative paths, source/output
overlap, symlink escape or output outside the owned attempt root refuse.
No recipe infers the root from cwd or silently falls back to docs/Project.
Pilot verifies VERSION1.13.0 and active project at ROOT/julia/Project.toml before
owning imports; Root preflight separately proves path package resolution, hashes,
full dependency/cache identity and all reviewed effects before launching Julia.
Receipt existence or a caller-supplied boolean alone is never approval.
Direct invocation does not bypass the mandatory external BUILD admission.

Core/Runner keep their exact existing `pages` vectors. Source scope is their
entire selected docs/src tree, including unlisted Markdown with pagesonly=false;
no `@ref` targets are trimmed to only primary journey pages. Pilot omits the
unneeded DocTestSetup assignment because doctests are off; normal branch retains
it unchanged. modules remain [QCLNEGF]/[QCLNEGFRunner]. Operator modules=[].

Exact public kwargs (Documenter AXNMp documents.jl404–431 and HTMLWriter507–538):

```text
makedocs(root=QCL_DOCS_ROOT, source=QCL_DOCS_SOURCE, build=QCL_DOCS_BUILD,
  modules=<owning module or []>, pages=<existing graph or operator graph>,
  pagesonly=false, remotes=nothing, doctest=false, linkcheck=false,
  checkdocs=:exports [operator :none], warnonly=false, draft=false,
  format=Documenter.HTML(prettyurls=false, edit_link=nothing, disable_git=true,
    analytics="", warn_outdated=false, prerender=false, mathengine=nothing,
    assets=["assets/qcl-fixed-light.css"], repolink=<owning public repository>))
```

The text above is an implementation contract, not runnable Julia syntax.
No theme/themes/offline/cdn kwargs, deploydocs, runtime math or Pkg calls.
`mathengine=nothing` does not remove all raw CDN head links: reviewed assembly
still removes/replaces pinned generated dependencies. No CSP change. All web
output remains fixed light; no OS-dark branch or alternative theme.
Staged assets/qcl-fixed-light.css must be supplied by exact reviewed root runtime
asset mapping; its current owning source/hash is not bound here. Missing input
blocks render, rather than writing a guessed stylesheet or bypassing the asset.

## 4. Deterministic operator mapping

Canonical input remains root docs/public/operator-recovery.md, not recovery.md.
The orchestrator copies its exact bytes to private staged operator/src/recovery.md
and records source path/revision/SHA/bytes → staged path/SHA/bytes. Both hashes
must match before render and after it. No filename-derived content rewrite,
absolute path interpolation or anchor substitution occurs.

Operator recipe owns the following fixed generated index source bytes (LF):

```text
# Документация оператора

[Восстановление прерванного запуска](@ref operator-recovery)
```

Its final newline is mandatory. It is generated source with a literal owned by
the versioned root recipe, not an additional canonical recovery text or hidden
template registry. Receipt records kind=generated, recipe identity and exact
index byte hash. Stage only index.md,recovery.md and required reviewed assets;
operator pages=["Home"=>"index.md","Recovery"=>"recovery.md"].
With prettyurls=false the produced targets are operator/index.html and
operator/recovery.html#operator-recovery. Root plan's primary URL stays exactly
that; no post-build rename from operator-recovery.html is needed. Existing
cross-section links from recovery.html to ../runner/user/results.html and
../core/theory/12_validation.html retain their literal bytes and named anchors.

## 5. Source/effect gate before any render

`doctest=false` is not an effect sandbox. Pinned Documenter separately evaluates
Meta/Docs/Eval/Example/REPL/Setup; draft=false remains required. Do not enable
draft to replace examples with placeholders, strip execution blocks from source,
or approve one regex scan as a complete import audit.

The exact input boundary is35 Core Markdown pages (34 navigation+unlisted
development/review_oracle_contracts),8 Runner pages, operator chapter+generated
index, all docstrings reached by14 observed @docs blocks, and imported package
source/include/init/workload/extension closure. Static support assets are
enumerated separately for public allowlist/closure, never executed/regenerated.
No examples/,test/,benchmark/,archives/,private site or numerical results become
build input merely because they live in a repository.

Before BUILD the source gate binds a finite manifest to selected graph plus
Project/Manifest/recipe hashes. Per entry record owner,revision,path,SHA256,bytes,
directive kind/location/body hash, effect classification and reviewer evidence.
It must inventory all fences including long/tilde/nested forms, @meta bodies,
@docs expressions and their actual docstrings, not only matching backticks.
Only exact reviewed CurrentModule assignments and specific reviewed symbol/type
resolution expressions are allowed; arbitrary @meta RHS/signature evaluation is
not accepted by a name-only pattern. Every executable @setup/@example/@eval/
@repl/jldoctest block must have explicit classification; initial text scan found
none, but unknown syntax/docstring edges still block render. A new/changed file,
directive/body/hash or dynamic docstring source invalidates the gate.

For current scope the cheapest accepted outcome is complete review of fixed
inputs with zero scientific executable documentation blocks. If a block invokes
SCBA/Poisson/benchmark, do not run, strip or rewrite it silently: stop that render
as a concrete source-policy conflict for focused review. Scientific executable
examples require their own stage and budget, not a docs pilot exception.

Import manifest reuses accepted D fields
{package,revision/tree,entrypoints,includes,init_effects,package_image_workload,
docs_directives,status,evidence}. Root receipt imports={manifest_sha256,status,
unknown_edges}; reviewed only if unknown_edges is empty and review actually
closed every bound edge. Source-change invalidation is mandatory. Core workload
contains tutorial Hamiltonian/retarded/spectral work, not an explicit SCBA call;
it is package-image cost, not a free ordinary-import guarantee. Runner's unused
same-named workload file must not be invented as an include. Full HDF5/FFTW/
Documenter/dependency/extension cache behavior remains unknown here.

## 6. Root ops/docs.ts orchestrator contract

Source-only entry preflight is allowed to emit blocked receipt without launching
Julia. BUILD execution is a separately admitted action. New CLI exact logical
interface for I: `docs.ts preflight --plan PLAN --attempt-directory DIR`, and
`docs.ts build --plan PLAN --attempt-directory DIR --admission RECEIPT`.
Arguments are data, parsed strictly; unknown/duplicate options or reused existing
attempt directory refuse. `DIR` is private owned output, not auto-cleaned root.
No shell strings, download/install/fetch or latest fallback.

Preflight consumes:

1. existing sourceGraph(requireClean=true), exact current component gitlinks;
2. versioned plan/schema and source/recipe byte identities, root locked project;
3. reviewed import manifest and source directive ledger bound to those bytes;
4. complete Documenter tree and Julia/toolchain/cache identities;
5. assets lock + immutable bytes/full licenses/public review, reviewed adapter API;
6. BUILD mode only: fresh external builder inventory/admission, credentials if
   its actual required action needs them, and finite process-tree resource grant.

Preflight does not import a target package to discover its identity. Unknown or
mismatch is recorded and blocks the dependent step. No schema-valid/receipt-
exists shortcut. DOC03 shared schema is consumed from selected published Contracts;
do not copy it into Root or synthesize a fallback. Its absence blocks final
bundle serialization; raw HTML, if separately admitted, must retain its weaker
identity and cannot be labelled a DOC03-conformant bundle.

Future admitted step order:

```text
sourceGraph + inputs/toolchain/import/assets/admission gate
isolated source staging and operator name mapping
Julia Core recipe -> raw/core
Julia Runner recipe -> raw/runner
Julia operator recipe -> raw/operator
reviewed assembler/math bridge -> candidate public tree
static closure/allowlist/hash/anchor/light/CSP checks
sourceGraph/input recheck -> immutable candidate receipt
```

Use selected Julia executable directly with argv
[--project=ROOT/julia,--startup-file=no,--history-file=no,RECIPE]; no call to
component tools/ci.ts that might perform environment setup. ROOT is the exact
source root; RECIPE one of the three selected owning files. Empty/controlled
environment contains explicit trusted PATH/HOME/depot paths, profile/source/build
paths, JULIA_LOAD_PATH=@:@stdlib and fixed single-thread controls appropriate to
admission. Do not reuse real HOME/private depot by accident or treat env offline
flags as network isolation. The reviewed import/cache manifest and external
network/process-tree boundary remain mandatory. Additional Julia cache-control
flags are not invented here: bind supported flags/prepared cache behavior against
the selected binary/source before BUILD or block.

Existing ops/process.ts run() buffers output and has no finite timeout/resource
policy; do not call it as the unbounded build runner. Root I supplies bounded
argv-based process handling with concurrent stdout/stderr drains, byte caps,
deadline and terminal/error receipt retention. External admitted job/cgroup owns
CPU/RAM/descendant cleanup; killing only the immediate Deno child does not prove
process-tree termination. Retain partial output, cap/kill/drain failures and
observed exit separately. No retry, target import probe or deploy follows failure.
Before/after graph/input mismatch fails the attempt and keeps original outputs.

## 7. BUILD prerequisites and receipts

Currently missing/not proven: final CPP2 adapter API binding; public OFL/font-
specific notices and full asset/license closure/assets.lock; full installed
Documenter tree/native toolchain/cache identity; reviewed full import/docstring
effect manifest; fresh native builder inventory/admission. Existing KaTeX source
binding does not close these other prerequisites. No latest install substitutes.

BUILD budget is supplied afresh externally, not inherited from this design/I.
It must bind attempt, selected source/recipe hashes, CPU/RAM, wall/deadline,
per-stream and total log bytes, output/scratch bytes, process-tree ownership and
stop/drain evidence. It covers exactly3 render steps+one assembly chain, no
scientific solve, docs example solve, install, full CI or automatic rerun.
If it cannot be enforced/measured as required, return blocked with reason before
launch. This design does not select a production resource allocation without
fresh host/VM measurements.

Consume the existing accepted Root docs-build-receipt schema fields from D§7.2,
not a second shared format: sources,plan/assets/schema hashes,inputs,toolchain,
admission,imports,assets,steps,measurements,transforms,checks,result,parent_attempt.
Exact proposed operator staging mapping is an inputs/transforms entry; generic
source input paths and source graph remain their owning authorities. Normalized
public-relative argv/env may appear in sanitized summary; actual paths, stdout/
stderr, inventory/credentials stay private. Unknown measurements are null plus
not_measured, never0. source-only preflight does not produce fake toolchain/import
or native pass. Build exit alone cannot close browser_light/browser_offline,
production_serving,restore or scientific gates. Public output hashes are computed
after transformations; no release/version pointer mutation or public release.

## 8. Meaningful future controls / review

| Input/control | Required distinction without Julia render |
| --- | --- |
| Unknown profile or missing/escaping stage path | Refuse before fake owning importer is invoked; normal unset profile remains normal contract |
| Changed input hash/@example block/docstring/meta body or unknown import edge | Gate refuses; no child launched, originals retained |
| Standalone Runner old Core or wrong active project | Refuse pilot instead of resolving/developing fallback dependencies |
| operator-recovery.md frozen input | Exact staged recovery.md bytes/anchor survive; expected recovery.html target follows pages mapping, no guessed rename |
| Missing license/assets/schema/admission/toolchain identity | Explicit per-prerequisite blocked/mismatch, no install/latest/fake pass |
| Fake child emits beyond cap or times out/fails | Partial logs preserved with correct cap/termination/drain status; no unbounded run()/auto retry |
| Source graph changes during admitted fake process | Attempt fails binding; no candidate publication |

Tests must assert these observable gates with minimal fake inputs/processes, not
mirror source strings or run a solver. Exact harness/source freeze and finite
execution authorization belong to coordinator after D R. Existing full docs
build remains separately admitted; normal doctests are not weakened for pilot.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Existing public Documenter APIs support the proposed profile | Selected recipes; AXNMp documents404–431/HTMLWriter507–538 | Complete tree/native/cache identity unproven | сохранить |
| Pilot can preserve normal defaults and complete support scope | Exact page graphs; explicit profile/default split | I and independent R not yet done | изменить |
| Operator URL can be produced without changing canonical prose | Frozen8f05 bytes→staged recovery.md, prettyurls=false, explicit anchors | Render/browser gate still pending | изменить |
| No scientific effect will execute merely because doctest=false | Separate source/import gate; explicit unknown ledger | Full directive/docstring/transitive closure not yet reviewed | данных недостаточно |
| BUILD/native/restore/science ready | Missing inventories/assets/import/cache/admission evidence | Source design is insufficient | данных недостаточно |

STOP for independent high CP-DESIGN before medium I. No product/source Git state
was changed; written only this design, companion ledger and identity in /tmp.
