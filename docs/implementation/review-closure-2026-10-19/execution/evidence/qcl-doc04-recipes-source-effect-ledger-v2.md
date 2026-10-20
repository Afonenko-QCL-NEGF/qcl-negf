# DOC04 recipes — bounded continuation ledger v2

2026-10-20. Addendum to original ledger SHA256
`aed51dc14bbe08cdbf5414544715686ac80c807a902233b70c94a5f51886d1e3`.
Original failed resource predicate is preserved unchanged. This is a separately
authorized ≤2MiB/15min/1CPU/2GiB continuation, no target execution or product edits.

## Closed selected Markdown inventory

Exact43 selected/support Markdown files were read by explicit path, no assets
or repeated component-tree grep. Core35 pages include the unlisted
development/review_oracle_contracts.md because pagesonly=false; Runner8 pages.
Their combined logical payload is508210 bytes. One pass captured every leading
backtick/tilde fence and all @meta/@docs bodies; a second global marker scan
confirmed that no quoted/nested/inline marker escaped that inventory.

Core:362 total marker lines =181 opening+181 closing; labels:
@meta28, @docs8, math111, yaml2, julia6, text26.
Runner:24 marker lines =12 opening+12 closing; labels:
@meta1, @docs6, yaml3, julia2.
No tilde fences or extra nonleading markers. No @setup/@example/@eval/@repl/
jldoctest/@autodocs/@raw/@contents/@index in these exact Markdown bytes.
Plain julia/yaml/text/math blocks are displayed source; the functions mentioned
inside plain julia examples are not invoked by the documented Expander matchers.
No source block is stripped or rewritten.

All29 @meta bodies are exactly a CurrentModule assignment:
Core `CurrentModule = QCLNEGF`, Runner `CurrentModule = QCLNEGFRunner`.
All14 @docs blocks contain bare/dotted binding names, except the single Runner
type signature `scattering_options(::ResolvedRunConfiguration)` at
api/public.md224. These expressions request bindings/type signatures; they do
not call solve/run functions. No custom @meta RHS, setup/teardown or filter code
was found in these Markdown files.

Exact location and expression witness retained at
`/tmp/qcl-doc04-recipes-continuation-witnesses.txt`, SHA256
`38d6cc0f65c9b44eea7322a71d55bc04bff8ae2e84202726184b2f96c2a3c2c8`.
That file contains source observations, not a generated product or import receipt.
Original ledger's @meta/@docs body-review gaps are closed for these files only.

## Important remaining nested-docstring gate

Pinned Documenter expander_pipeline.jl143,209,254,260,265 explicitly makes Eval,
Example,REPL,Setup nested expanders. Thus fetched docstrings can themselves
execute those blocks. @docs binding-only source is not a blanket harmlessness
proof. DocsBlocks492 fetches actual docstrings; the original failed-budget
backtick scan found no matching executable fences in selected owning src, but
does not certify all alternative fences/dynamic docs or full include closure.

Consequently owning nested-docstring/dynamic-doc effects and upstream import/
extension/cache effects remain explicit unknown BUILD prerequisites. No render
may start while they are unknown. This does not prevent source I implementing
the profile and a fail-closed preflight; source I cannot label the unfinished
manifest reviewed. A missing proof returns blocked before package import, never
a stripped docstring, draft placeholder, ordinary-import probe or implied pass.
Documenter method/source mutation is not an alternative.

## Exact immutable Markdown identities

Blob IDs below are Git object identities at the frozen commits, not SHA256
substitutes for the future build receipt. The future preflight computes SHA256
of exact staged bytes under its own bounded I/BUILD stage. Component revisions:
Core e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee;
Runner1acc165650fd4f4c2d49605cc679f90e3f6fcdae.

| Owner | Path | Git blob | Bytes |
| --- | --- | --- | --- |
| core | docs/src/index.md | `4b3f31e3a1e79e5a7f18e1ae0a18f698050429f2` | 593 |
| core | docs/src/user/convergence.md | `3c2f37248316e80444572cca222a85adc08cb54e` | 14697 |
| core | docs/src/api/operators.md | `122e70cc111819304442d00a94fe9f01acf77942` | 6053 |
| core | docs/src/api/public.md | `bcfecf86d9ade943a94ca318881df4d1bb279689` | 4900 |
| core | docs/src/theory/01_model.md | `871eaf5a56c5e5bb0be57a4998f13ad8d79ce91b` | 7724 |
| core | docs/src/theory/02_reference2019.md | `b86d4ed45e90b1a081bd46bcc8d04d2e1fa0b545` | 4816 |
| core | docs/src/theory/03_arrays.md | `31b3598b127aed3c2417777cc652fa3d05ede227` | 5693 |
| core | docs/src/theory/04_scaling.md | `35bf936854927d603f6f3ad1354d07c4c7df8b6e` | 6029 |
| core | docs/src/theory/05_basis.md | `447cbe903585c2b72611957c8a635a4013cc130b` | 8584 |
| core | docs/src/theory/06_periodicity.md | `1bc5e8d942f3b9be66541ea861879ea9b21e7714` | 10045 |
| core | docs/src/theory/07_greens.md | `b6338c7ed584466272f3a3682c8d957987577d18` | 7182 |
| core | docs/src/theory/08_kernels.md | `c0d8af179614c20d8291c51f49aec554619384e3` | 12221 |
| core | docs/src/theory/09_scba.md | `06b479304042f43cf901dd91a5d96d2299a39d0f` | 10788 |
| core | docs/src/theory/10_poisson.md | `df0076971053343dc9fca840b85951f6b51e70ba` | 6738 |
| core | docs/src/theory/11_observables.md | `4835c72e4b93237a5cf442c254e92ff49c607fe2` | 8180 |
| core | docs/src/theory/12_validation.md | `687b6164398bec2be03d08c1edb6c2e4d165ef62` | 30020 |
| core | docs/src/theory/13_visualization.md | `30909c8017e456f5cf1d9af5cde0a7ab66390824` | 7978 |
| core | docs/src/theory/14_cost.md | `185939d02f8d99530a9682ab1b9e76a2c8b7be4a` | 9452 |
| core | docs/src/theory/15_limitations.md | `3ed2aadebe5d4e1f8d69bdf5c59b80eec54d94bf` | 6557 |
| core | docs/src/theory/16_input_contract.md | `53a05e1385948d325ef336de45a9df333f234cb1` | 8326 |
| core | docs/src/theory/17_implementation_plan.md | `b9ef7ed04e5d0488abe864bcbb9a2701b708947e` | 9826 |
| core | docs/src/theory/18_optical_response.md | `054c5e5752b9184d9ece690d0db4dc260ac87e1b` | 9076 |
| core | docs/src/theory/19_production.md | `00e17e39811351d5157ab244e669025eb4155113` | 24632 |
| core | docs/src/theory/20_optimization_decision_tree.md | `1fd57e5ce2409b618c37db047e563f9e93c67453` | 16347 |
| core | docs/src/physics/models.md | `0f2c42629e786f14d395cbae3303f47270d364ba` | 19876 |
| core | docs/src/physics/numerical-policy.md | `7de5fec3ae08c222ae9ed46bd4a51911145315f5` | 8411 |
| core | docs/src/tutorials/localization.md | `c46aee99a86353e0caf4cfc9290eab561d98c9bf` | 20494 |
| core | docs/src/tutorials/physical-atlas.md | `d60ec3eaf67317f2f70682ac19b64ec4d347622f` | 28216 |
| core | docs/src/developer/architecture.md | `d7262e3193c3c12dd2b2df76383b386d3f6c39ab` | 1622 |
| core | docs/src/developer/physics_operators.md | `af07568c91f10c65cacdfbfa1fd079bba205100f` | 6684 |
| core | docs/src/developer/traceability.md | `dce97ef6055b659642f56c1e595c33a3acee786f` | 9711 |
| core | docs/src/glossary.md | `720fd0cd2805f40b13ffd1d6c3a7749a62d9a901` | 9713 |
| core | docs/src/references.md | `bf976e49d6bc8ce87284a5c7d4b2280f3b391925` | 4941 |
| core | docs/src/references_optimization.md | `6df4b39aa6c20e1c04567514d20bc208abf070bc` | 20380 |
| core | docs/src/development/review_oracle_contracts.md | `6bb0d8595453f6ce020df20c41079e1ddd8c7cb5` | 98738 |
| runner | docs/src/index.md | `11c25bf9e34ed0a3a9131d362f9bf096bd9da6d4` | 534 |
| runner | docs/src/user/comparison.md | `44052a29c642ffcb89354042aaa7e6042dfe4efb` | 3401 |
| runner | docs/src/user/configuration.md | `9e9c7e855cc81bfde427b46583420c6ea4a4a074` | 10648 |
| runner | docs/src/user/plotting.md | `96a2e673d4d4a90fcacb7fedd14ae4f966469350` | 893 |
| runner | docs/src/user/resources.md | `af36dd1873725a875696c907655a40a6bc574503` | 1182 |
| runner | docs/src/user/results.md | `e1785d63f9a380490e02d25fc122d8144b7d316c` | 17568 |
| runner | docs/src/api/public.md | `8d585d7692b20bd653697da37476eb3807077590` | 7050 |
| runner | docs/src/developer/architecture.md | `d4a400dada88d70a0bdddb7721434405e2befdb6` | 1691 |

## Resource accounting and limits

Two explicit Markdown passes consume1016420 logical payload bytes. Pinned
Documenter expander slices/grep are bounded by three times that named file's
size; object-size metadata do not constitute a payload audit. Conservative
continuation target-text allowance is below1.5MiB, within the separate2MiB cap.
Physical Git/decompression/kernel I/O and process RSS were not instrumented.
No claim is made that phase1's original4MiB resource predicate passed.

No imports/parsers/Julia/Nix/Deno/render/test/build/network/server/children or
Git mutations occurred. Only source text extraction/metadata and /tmp artifacts.
STOP for independent high R.

