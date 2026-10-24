# DOC04 Core/Runner profiles — independent high CPP

**PASS_SOURCE.** Два owning `docs/make.jl` реализуют принятые D1+D2+D3 и D4 path/layout clauses. Блокирующих замечаний в actual source/diff не найдено. Default recipe сохранён побайтно; pilot guard branches стоят до imports/output. Это вывод по исходникам: Julia syntax/type/runtime, fake importer/output sentinel и render не исполнялись. BUILD не admitted этим verdict.

## Exact binding

| Вход | Identity |
| --- | --- |
| Core worktree/base | `/tmp/qcl-doc04-core-profile-worktree`, `e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee` |
| Core actual `docs/make.jl`, 7704 B | SHA256 `b26574d7632747feee06094ef99ce96edcc35c97d794a2f243f6921c2de3812e` |
| Core patch | `8ec0fd22e1c46ddcac0a9abed36a361c86a3530206bd9d1b542c684d5a0a1682` |
| Runner worktree/base | `/tmp/qcl-doc04-runner-profile-worktree`, `1acc165650fd4f4c2d49605cc679f90e3f6fcdae` |
| Runner actual `docs/make.jl`, 6068 B | SHA256 `6db896ca38bad4ac8ad6b5ba9103712d51383ca065709a1b856b25a99049f051` |
| Runner patch | `59c5354e289adf00f6a5d3a317f20c677d617c07aad9401d1e92c38a25633a64` |
| D3 `/tmp/qcl-doc04-recipes-design-v3.md` | `960a639dd281d7a5b99c582f2c9dc8b17e816715753557791460ebcef1159aee` |
| D4 `/tmp/qcl-doc04-profile-path-contract.md` | `ec7717494878fbec813fe89c1ded0c5c43dcbeb6942271d0ef8d113445f5a935` |
| Accepted D4 high review | `45d21330010644038db3b215a76f04d026e329dc0cf2844eb42ce00b99cac12a` |
| Author report / identity | `4fd88205ca941f0be378ac5ee49000d83a1a77a834a8ef019bd59ef564db513f` / `9524f3a526124dcfcdf98f092c3c9eb3320dee431c25c1eccc0286e80a3a7498` |

Read-only `GIT_OPTIONAL_LOCKS=0` Git inspection confirms both exact HEADs, only ` M docs/make.jl` in each worktree, no submodules. No new revision lock or changes to selected source graph were made. Primaries D3/D4, inherited D1/D2 and actual sources/patches were read before author report. Accepted D4 review and pinned Documenter source were used to check the intended API/path boundary.

## Default recipe preservation

`QCL_DOCS_PROFILE` is read once (:4). Missing/empty selects the else branch; any nonempty value other than literal `pilot-v1` throws at :5–6. The four pilot path variables are read only in the pilot branch. Their presence cannot select pilot from an unset/empty profile.

Independent shell text projection of everything between the top-level `else` and final `end`, compared by SHA256 to immutable `git show BASE:docs/make.jl`, gives:

| Owner | Extracted normal branch = immutable original |
| --- | --- |
| Core :117–138 | `edafb4e03b0fd9982039267dc24ba7c6332551f7e3770fca20b35fc8dae9380f` |
| Runner :113–130 | `0749b9989ce07c34034dddac2fe8127a9ecca72d43105425928f7468dae16cbc` |

Thus existing imports, DocMeta setup, modules, sitename, navigation, normal HTML arguments, `doctest=true`, `checkdocs=:exports` and `warnonly=false` remain a continuous byte-exact block. The wrapper adds branch selection; it does not rewrite the normal recipe. Its runtime effect was not measured.

Pilot page vectors were independently projected as text and compared with the immutable originals after removing only four added indentation spaces. Core page vector hash equals `2fc1944d9dcfe6381076b89b9010e43c303e93e73f04446ab019e49b6b90c275`; Runner equals `5fae53dd87a398bad128f38f42508f5778cd32388d7d1c3df51e09a8a1467909`. Both sides matched. All original pages are retained; `pagesonly=false` retains the full agreed staged scope, including unlisted files. This is not an executed anchor check.

## D4 before-import path guards

The guard region :11–84 is identical in structure for both owners, differing only in literal `core`/`runner`. The first owning/Documenter import is :86; first `makedocs` is :87. The guard contains Base strings/path/metadata operations and explicit errors, no package import/include, output creation/deletion, receipt permission flag, Pkg/setup/download or catch/fallback.

| Required predicate | Actual locator and consequence |
| --- | --- |
| Required exact Linux absolute normalized strings | :11–19 requires all four values, `/` absolute spelling, rejects trailing/repeated slash and `.`/`..` components, requires `value==normpath(value)`. Filesystem root is rejected by trailing-slash rule. Values are not silently normalized. |
| Every existing ancestor nonsymlink; canonical existing dirs | :20–26 walks each path to filesystem root using `islink`; :30–33 requires directory and exact `realpath`. :47–50 applies this to ROOT/ATTEMPT/SOURCE/raw parent. Errors are not swallowed. |
| Components rather than lexical prefix | :36–40 compares `splitpath` sequences with a length guard. `/tmp/a` is not treated as ancestor of `/tmp/ab`. |
| Disjoint ROOT/ATTEMPT and SOURCE/BUILD | :51–56 checks containment in both directions, including equality. |
| Absent current owner output, including dangling link | :57–58 rejects `ispath(BUILD)||islink(BUILD)`; no cleanup/mkdir is performed. Other owner raw outputs are not rejected merely for existing. |
| Exact Julia and locked root project path | :59 requires VERSION1.13.0; :60–76 requires regular nonsymlink canonical ROOT/julia/Project.toml and Manifest.toml, checks ancestors and exact `Base.active_project()` path. Manifest presence follows D1 locked-root-project prerequisite; it is not a dependency-content proof. |
| Exact owner tuple; canonical absent candidate | :77–82 requires SOURCE=`ATTEMPT/stage/<literal owner>/src`, BUILD=`ATTEMPT/raw/<literal owner>`; existing canonical raw parent plus literal owner forms the absent candidate, without `realpath(BUILD)`. |

A failing recipe guard reaches an error before the source control-flow import/output sites. The source establishes this order; no invalid/valid sentinel execution, filesystem race test or runtime exception behaviour is claimed. There is no solver/model/numerical-array or scientific criterion change.

## Pilot kwargs and pinned API

Core :87–115 and Runner :87–111 pass exact ROOT/SOURCE/BUILD, existing typed owner module vectors, `remotes=nothing`, D3 fixed nonempty sitenames, complete existing pages, `pagesonly=false`, `doctest=false`, `linkcheck=false`, `checkdocs=:exports`, `warnonly=false`, `draft=false`. DocTestSetup is omitted only in pilot, as accepted D2 specifies.

HTML args match accepted D1 contract: `prettyurls=false`, `edit_link=nothing`, `disable_git=true`, `analytics=""`, `warn_outdated=false`, `prerender=false`, `mathengine=nothing`, fixed light asset path and existing public repository link. No invented theme/offline/CDN kwarg or deployment call appears. Fixed-light bytes and final removal/replacement of Documenter dependencies remain Root staging/assembly proof; the asset filename or `mathengine=nothing` alone does not prove light/CSP/offline/public closure.

Primary pinned source rechecked:

- `.build/local-julia-int01/depot-1/packages/Documenter/AXNMp/src/documents.jl:404–434`, SHA256 `67ded455a9d8881b6fe3cf4a4cfbc97a992e27cd8e31ad3d28de23cbc3578e06`: accepted public document kwargs/types.
- Same package `src/html/HTMLWriter.jl:507–538`, SHA256 `72b261cbef5e06e9edc4159c038d740b5f5372134f9d75db06eeb35b894b29dd`: accepted HTML kwargs, `mathengine::Union{MathEngine,Nothing}` and explicit no-prerender branch. Full installed tree/native/cache identity is not inferred from these two files.

## Limits and evidence retention

The comments correctly leave ownership/permissions/exclusive namespace, staged internal symlink/special-file and byte/hash inventory, all nested docstrings/import/include/init/workload/extension effects, toolchain/cache identity, reviewed assets/licenses and fresh external BUILD admission to mandatory Root preflight. The recipes do not recursively inspect SOURCE and cannot establish these facts by themselves. A direct call with matching paths is not technical BUILD admission. Existing metadata TOCTOU, concurrent replacement, bind mounts/hardlink alias limitations of D4 remain. ROOT/source/input changes must invalidate external bindings before any dependent dispatch.

No source sentinel tests accompany these two owning edits, and the author explicitly marks them not_run. This source-only assignment does not authorize their execution or close that runtime prerequisite. Root's finite fake importer/output controls, missing artifacts/unknown effects checks and actual staging preservation remain separate gates; no runtime or source-correction cap is reset by this review.

Both actual `git diff --check` calls returned0. Author report assertions about byte equality were independently checked as above, not accepted solely from identity flags. Target-language parser/typecheck/import/test/Julia/Documenter/render/build/network/solver/server/children/Git mutation/product/checkpoint writes:0. Only this review and companion identity are created.

Named read accounting: D1/D2/D3/D4 and accepted R texts; both make files/patches and narrow numbered ranges; exact author report/identity; immutable original make and page projections; two named Documenter source extracts and hashes. Conservative complete-file charge with reserve is 2 MiB, below 6 MiB envelope; physical I/O/RSS/CPU were not instrumented. One `rg --files /tmp` name discovery traversed unrelated directory metadata and reported permission-denied entries; no unrelated contents were read or used. Subsequent reads were explicit named paths. Historical original design resource failure remains unchanged, not retroactively accepted. Output is below256KiB; source-only20min/1CPU/2GiB bounds retained.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Unset/empty branch preserves original owner recipe | Independent extracted/original byte hashes, exact bases | Branch runtime not executed | сохранить |
| Pilot implements D3/D4 guard order and kwargs | Actual two sources, patches and pinned API locators | Sentinel/parser/render checks not_run | сохранить |
| No scientific task or public schema changed | Only two docs/make.jl diffs, no numerical changes | Import/build costs/effects remain external prerequisites | сохранить |
| Guard establishes ownership/BIND/full payload/cache closure | It explicitly delegates these facts to Root | Required external evidence not supplied by guard | данных недостаточно |
| BUILD/native/public/science acceptance achieved | No execution evidence in this review | Source CPP only | дополнительно измерить |

STOP — PASS_SOURCE exact two owning profiles; BUILD/runtime gates remain open.
