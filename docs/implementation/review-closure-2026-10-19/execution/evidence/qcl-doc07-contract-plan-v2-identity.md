# DOC07 Contracts D2 identity/digest ledger

Stage: narrow source-only DESIGN/DOC revision, 2026-10-20. Output packet `/tmp/qcl-doc07-contract-plan-v2.md`; canonical proposal `/tmp/qcl-doc07-canonical-clarification.patch`. STOP before independent high-review D2 and later medium implementation.

Primary root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD `d4113f43cddf02d46025434eb3a9dd8e110e90d6`. Contracts HEAD/published gitlink `12fc26462bbab3df76904c6deb01f8c6596de7be`, status clean at D2 initial/final owner reads. Root concurrent Platform/Results/tests/execution artifacts are outside this task; no changes there were made. Gitlinks remain composition authority, not this ledger.

D1 original plan expected/observed SHA256 `44434ac8f418c5ad80c1750e34b1dd868112cd2c393d8bc0e3c2d59737a370a8` preserved. D1 independent high-review expected/observed SHA256 `7b0c262a1368d53cd98ed964ba46ae3f037de4f5c9b3dd9ab0d89a8d6ceeebdb` preserved. Primary canonical DOC03 expected/observed SHA256 `4b046312d0c1f04566c3a80ca6fb8a441ca7b025003c3c3b1c4c2bab2242f6cb`, 88916 bytes, 967 lines; root file remains unchanged.

Candidate `/tmp/qcl-doc07-canonical-candidate.md` is original exact file followed by `/tmp/qcl-doc07-canonical-clarification.txt`. `cmp -n 88916 original candidate` returned exit0. Generated unified diff contains only EOF additions under the original final three context rows; no source prefix replaced. Candidate is 97722 bytes; proposed added section lines969–1084, anchor `model-help-doc07-v1-clarifications`. Patch not applied; no `git apply`, schema parser or runtime validation was executed. `diff` exit1 was expected text difference, not failed implementation verification.

D2 outcomes:
- R1 and R6 closed consistently with D1 independent review.
- R2 complete Origin/Atom/ValueOriginView status/kind/null/reason matrices; finite JSON and semantic attribution separated.
- R3 closed documentation/input status-reason matrices; mandatory trusted actor UUID/attempt retained, known unbound identity scalars not erased.
- R4 exact retained Fragment+Bundle bytes/hash/selected source context only, otherwise inputs=[]; declared/used independent of served docs availability.
- R5 query-free public-emission subset for pilot, no query stripping/secret scanner/URI trust registry; existing reviewed source/recipe provenance remains required.
- Corrected Documenter facts locator P235–237 to primary P226–228, no change to actual pin values.

Envelope<=20min/1CPU/2GiB/logicalreads3MiB/output128KiB. Conservative logical text reads, including repeated hashes/copies/diffs/views, remain <2MiB; physical filesystem/Git-object I/O and actual peak RAM were not instrumented. No network, children, Python/Julia/import/parser/schema/runtime/tests/build/solver/server operations, product source edits, Git mutations, commits/push or checkpoint writes. Writes limited to the named `/tmp` artifacts. No current acceptance/BUILD/science pass claimed.

D2 source/text checks used shell Git/SHA256/wc/nl/sed/rg/cmp/diff and apply_patch only for `/tmp` Markdown. Original review and design were rehashed unchanged. Fresh independent high-review D2 is pending; packet has no unresolved choice menu for I.

Final digests and exact Git observations follow:

44434ac8f418c5ad80c1750e34b1dd868112cd2c393d8bc0e3c2d59737a370a8  /tmp/qcl-doc07-contract-plan.md
7b0c262a1368d53cd98ed964ba46ae3f037de4f5c9b3dd9ab0d89a8d6ceeebdb  /tmp/qcl-doc07-contract-plan-review.md
20e712a051b3ba9e326bf4dccc3598513b43beefbcab0862d57e287d676dcb8b  /tmp/qcl-doc07-contract-plan-v2.md
491c0894ef50774d4d88aec8bf762243a11b567fe2b7dad86f1061d7346d68de  /tmp/qcl-doc07-canonical-clarification.txt
fc9cf40c2a19c7d98369dca72af0922f37906635f0003cb14a57525cc2bee2f5  /tmp/qcl-doc07-canonical-clarification.patch
fe1df31aa294163f46ba5d8d9ddbd4aa0b636a402bee9f810de44299f402f794  /tmp/qcl-doc07-canonical-candidate.md
d4113f43cddf02d46025434eb3a9dd8e110e90d6
 M components/qcl-negf-platform
 M components/qcl-negf-results
 M docs/implementation/review-closure-2026-10-19/execution/checkpoint.json
 M docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-current-bound-doc-publication-journal.json
 M docs/implementation/review-closure-2026-10-19/execution/qcl-targeted-receipt-census.json
 M nix/solver.nix
 M ops/application_cd.ts
 M ops/solver.ts
 M tests/application_cd_test.ts
 M tests/solver_test.ts
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-doc04-root-impl-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-doc04-root-red-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-doc04-root-red-v2-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-doc04-root-red-v2-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-doc07-contract-plan-identity.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-doc07-contract-plan-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-doc07-contract-plan.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-cli-seam-design-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-cli-seam-design.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-platform-compat-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-platform-red-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-platform-red-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-platform-red-v2-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-platform-red-v2-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-root-code-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-root-impl-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-root-red-v2-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-root-red-v2-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-root-red-v3-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-root-red-v3-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-root-local-unit-harness-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci03-M1-doc-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci03-M1-doc-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci03-M1-final-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci03-M1-impl-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci03-M1-impl-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci03-M1-pr-body.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci03-M1-red-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci03-M1-red-v2-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci03-M1-red-v2-review.md
?? docs/implementation/review-closure-2026-10-19/execution/qcl-doc04-root-formatted-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-doc04-root-impl-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-doc04-root-red-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-doc04-root-red-source-binding.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-doc04-root-red-v2-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-doc04-root-red-v2-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-doc07-contract-plan-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-local-runtime-binary-identities.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-local-runtime-metadata-preflight-1.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-local-runtime-metadata-preflight-2.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-local-runtime-metadata-preflight-3.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-cli-seam-design-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-cli-seam-design-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-platform-compat-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-platform-first-intent.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-platform-first-result.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-platform-red-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-platform-red-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-platform-red-v2-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-platform-red-v2-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-platform-source-binding.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-code-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-formatted-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-green-intent.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-green-result.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-green-source-binding.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-impl-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-red-intent.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-red-result.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-red-source-binding.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-red-v2-delta.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-red-v2-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-red-v2-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-red-v3-delta.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-red-v3-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-red-v3-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-root-local-unit-harness-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-G1-preflight.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-active-G1.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-doc-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-final-source-binding.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-green-intent.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-green-result.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-green-source-binding.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-impl-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-impl-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-publication-journal.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-red-intent.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-red-result.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-red-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-red-source-binding.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-red-v2-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-red-v2-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/tests/DOC04-NODE-RED-1/
?? docs/implementation/review-closure-2026-10-19/execution/tests/DOC04-PY-RED-1/
?? docs/implementation/review-closure-2026-10-19/execution/tests/OPS04-PLATFORM-FIRST-1/
?? docs/implementation/review-closure-2026-10-19/execution/tests/OPS04-ROOT-GREEN-2/
?? docs/implementation/review-closure-2026-10-19/execution/tests/OPS04-ROOT-RED-1/
?? docs/implementation/review-closure-2026-10-19/execution/tests/SCI03-M1-GREEN-2/
?? docs/implementation/review-closure-2026-10-19/execution/tests/SCI03-M1-RED-1/
?? docs/implementation/review-closure-2026-10-19/execution/tooling/DOC04-FORMAT-1/
?? docs/implementation/review-closure-2026-10-19/execution/tooling/DOC04-LINT-1/
?? docs/implementation/review-closure-2026-10-19/execution/tooling/OPS04-FORMAT-1/
?? docs/implementation/review-closure-2026-10-19/execution/tooling/OPS04-LINT-1/
?? tests/docs_math_test.mjs
?? tests/test_docs_assembly.py
 e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee components/QCLNEGF.jl (v0.2.0-15-ge431609)
 1acc165650fd4f4c2d49605cc679f90e3f6fcdae components/QCLNEGFRunner.jl (v0.2.0-27-g1acc165)
 d8f8092ca1c76523d85384b4bac8198d8bfa736b components/qcl-negf-aiida (v0.2.0-17-gd8f8092)
 12fc26462bbab3df76904c6deb01f8c6596de7be components/qcl-negf-contracts (v0.2.0-14-g12fc264)
+cb0e7beb3f35cf9331bc708bdf116c050c87c619 components/qcl-negf-platform (v0.2.0-91-gcb0e7be)
 2622de5ee28b454ff4f809cc3dd00c1e5bc2295d components/qcl-negf-portal (v0.2.0-17-g2622de5)
 3ed8a9fe5f16f51bbcb7547ff2d677e8d3608731 components/qcl-negf-research (v0.2.0-9-g3ed8a9f)
+de70638a982f91b7e125ab1cfc70a2daef2a656d components/qcl-negf-results (v0.2.0-23-gde70638)
4b046312d0c1f04566c3a80ca6fb8a441ca7b025003c3c3b1c4c2bab2242f6cb  docs/system/physics-documentation.md
12fc26462bbab3df76904c6deb01f8c6596de7be
