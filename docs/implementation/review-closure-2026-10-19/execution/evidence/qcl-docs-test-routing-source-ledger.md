# Docs test routing — named source ledger

2026-10-20. Root e22d7bb64e4b6c91fdd10e51dcbb818d1aee3b4b observed clean;
git submodule status showed all8 selected gitlinks matching. Source-only reads,
no target imports/parser/runtime/CI. Existing AGENTS/architecture and applicable
brainstorm/writing-plan instructions already read in this session; source route
does not create a new approval request or framework.

## Exact current Root / owning sources

| Path | SHA256 | Bytes |
| --- | --- | --- |
| deno.json | a4043c0ec1c976c03704253316c90a94cb8c7ca2cfe4222f7182ea05565249b7 | 1480 |
| ops/ci.ts | 2d6750a2703fb1ac2a9ab7d6ec2195daa92a6f5bc3e51b762273bc935fe66702 | 3479 |
| ops/environment.ts | ac241561486efea1509d227b2640f525d64c562a7fd154ece2db4d726a5139f0 | 2343 |
| .github/workflows/ci.yml | 0d3be20e2a94584ea581b8e4e96ce6550a9a88a5096b8187c86050521cd72b08 | 1971 |
| .github/workflows/release.yml | 01777a020aecc29b27aee38584aeab6d127168242d1c44019bd019af8c2dd4db | 1911 |
| flake.nix | 4eeae196e7f561e3a61a4c073a13f88578f0ee306745ca0c1d0cff0e4f43771f | 2279 |
| selected platform/flake.nix | c77f554642dcfe6fd0f8e21141a1daa4415e9ee5530558927ef7c458279a1cc2 | 4105 |
| selected platform/modules/runner.nix | 2b644ec50be37b457aae0bcb86d335b7a22ddbe1531f1ba1cbfc208c22cdbbdc | 6508 |
| tests/docs_math_test.mjs | a3e47d219238e9e0b6be4b64ef42154a7057e4ac79776621f3bca84f58acc6a7 | 14430 |
| tests/test_docs_assembly.py | 2207f3bce01e55774b2a4f3a5930fbb5cc880b84fe6e1b38afeafab3a2a548ca | 22976 |
| ops/docs/math-render.mjs | 663c712d01db3bdc4bca66d3bb58b9aa6bbffd850c8961e1560c30292fd1aba5 | 20769 |
| ops/docs/assemble.py | 58d47789da8af18a66136676228c7398fcd50c8797838e8614c8aa07f3d64fda | 33127 |

`platform` here is components/qcl-negf-platform selected
f5bc368654414039f7368bb19ca3201fa7f29f9d. Root flake only inherits its component
checks, whose operations derivation copies the platform source; this is not the
Root tests directory. Runner module82 already supplies Node24/Deno/Python314;
source presence is not measured installed binary readiness.

Current Root DOC06 test/adapter paths do not exist. Candidate test only was read
at /tmp/qcl-doc06-worktree/tests/docs_static_slice_test.ts,
SHA3714933c7f34dc6da97db1189422e9381cf6d73589215e5692845402a260eb50,
25901B. Its import target ops/docs/static-slice.ts was absent at the named candidate
path when inspected. No implementation identity is invented. Candidate test
lines60–66 mandate one /tmp capability in Deno.args, with no env fallback;
its failed fixture retention is explicit. Full routing requires a later selected
published adapter+test, not this uncommitted path or historical source pin labels.

## Primary help and accepted contracts

- /tmp/qcl-pinned-deno-test-help.txt:14912B,
  SHA780289de4c03cddc3fe7a17f9e47db5171f3326c4b5be0a0924f5da76b530df0.
  Root supplied recorded pinned2.8.3 help. It explicitly documents mjs directory
  discovery, --ignore, -- [SCRIPT_ARG], scoped permissions, --no-config/--no-lock/
  --cached-only/--no-npm/--no-remote and reporter=tap. No fresh Deno binary call.
- Accepted DOC04 D77ee8593…bf12b/R6caa4f15…28164 and KaTeX binding
  c65c38f7…a25a2 were reused from immutable in-session design/source witnesses.
  Relevant fixed-input/license/source-only clauses were reread by named rg.
- Full accepted contract digests: DOC04 D
  77ee8593655f98b2e66d762620279ba6ac7ec7da126c62a2ccbd56a0262bf12b;
  R6caa4f15035e6a9f564d1ec86f14ecd64bbd31d73457556327e090e9d6628164;
  KaTeX D c65c38f74b5fd8168c9ed5ee2fc79649e2d7bafa5655a9248aee4aa81dca25a2;
  DOC06 D34b80d4ae1c8b94d23657124f17c9051251cea4763af8f92007d24929aafb2e8.
- DOC06 D34b80d4a…fb2e8 and independent R
  /tmp/qcl-doc06-static-slice-design-review.md SHA
  385c2ae4358a7fb296399d6d955eb4d9ac5995c26f8baa2c27526ad11677d5ce,
  16821B. R confirms approved narrow source-only design, exact no-env/run/net/ffi
  permission boundary and future checks, not target execution proof.
- DOC04 recipe R3 /tmp/qcl-doc04-recipes-design-v3-review.md SHA
  7db5ad18c7c9e197fb0430422b917228ddc0216f90c0cdfb37f78ee80e9a4211,
  8289B. Path/hash was inventoried; no new claim about recipe I/build acceptance
  is drawn from this receipt.

## Observations linked to decision

Node unit top-level imports node:test,read/process.env through exactInputs and
requires DOC04_KATEX_ROOT. Module/CSS exact SHA/version guards run before target
import; no source-tree fallback. Node unit intentionally tests static math;
it is not a pure Deno module or a public-font-license acceptance.

Root deno.json check currently includes only transfer Python unittest and restore
Nix check, plus generic directory Deno suite. ops/ci full branches test component
packages and infrastructure; neither route explicitly invokes Root docs Python
or dedicated Node/DOC06 units. Thus explicit aggregation preserves intended new
coverage rather than blessing an ignored directory file as pass.

CI workflow's Check typed operations step runs check for both scopes; native
prepare is full-only. Release workflow separately runs check+test. These facts
motivate base-only smoke and exactly one aggregate call in ops/ci full/default.
Workflow dispatch remains manual; cancel-in-progress:false is retained.

## Read/resource and scope accounting

Named source reads: full small task/workflow/flake files; Node test once plus
hash; DOC06 candidate first155 lines plus hash; Python test first55 lines plus
hash; targeted runner/env/help/contract text; file hashes and size metadata.
tests/git_environment_test.ts was a small supporting entrypoint search only.
No broad execution-tree/history/data scan, no installed target inspection.
Conservative full-file-equivalent named payload <2MiB, below4MiB cap; physical
Git/kernel I/O/RSS and exact cumulative shell read meter not instrumented.
Source-only design output stays below64KiB. No resource predicate is promoted
to native measured proof. Only /tmp design/identity/ledger written.

No test command, --help subprocess, import/eval/parser, Julia/Nix/Deno/Node/Python
target execution, package setup/build, network/server, child agent, Git mutation,
workflow dispatch or checkpoint edit occurred. final full CI count remains0.
