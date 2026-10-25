# DOC07 Contracts design identity/digest ledger

Stage: source-only DESIGN/DOC; artifact `/tmp/qcl-doc07-contract-plan.md`.
Root inspected: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
Root expected/observed HEAD: `d4113f43cddf02d46025434eb3a9dd8e110e90d6`.
Contracts expected/observed HEAD and published gitlink: `12fc26462bbab3df76904c6deb01f8c6596de7be`.
Canonical DOC03 expected/observed SHA256: `4b046312d0c1f04566c3a80ca6fb8a441ca7b025003c3c3b1c4c2bab2242f6cb`.
Contracts status at initial inspection: clean. Root initially dirty in Results/execution artifacts; no owning source edited by this subtask.

Envelope: source reads <=4 MiB, output <=128 KiB, <=30 min/1 CPU/2 GiB; no network/parser/import/runtime/tests/build/solver/children/commit/push/checkpoint writes. Shell text views/Git/SHA256 and `/tmp` Markdown writes only. Unique full file-size basis for root/owner sources inspected was 194721 bytes; selected excerpts/repeated reads plus skills remain below 4 MiB. This is a bounded accounting estimate, not measured IO telemetry; shell `rg` inventory searched source-only target directories, not arrays/archives.

Commands that checked source identity: `git rev-parse HEAD`, `git status --short`, `git submodule status --recursive`, `sha256sum` primary docs/owner routines. No package commands executed. One `rg` used a duplicated component prefix and failed `No such file`; rerun used relative `src/...` correctly. This failed text lookup did not alter state or count as verification.

Source digests and final observed source status follow. This ledger is evidence for this design task, not a parallel revision lock or authority for project composition.

44434ac8f418c5ad80c1750e34b1dd868112cd2c393d8bc0e3c2d59737a370a8  /tmp/qcl-doc07-contract-plan.md
ef2ef40fe24e1f83758a59497526017955df377827004fb39bd0d39ca90d9330  AGENTS.md
8e49c02d948891f31f6d27360564b4a2708d7a1546808d9f10f38d0c5ebec6b7  docs/architecture.md
4b046312d0c1f04566c3a80ca6fb8a441ca7b025003c3c3b1c4c2bab2242f6cb  docs/system/physics-documentation.md
17fc16b7808ae0e2b29732c65033a5f544bca79577788cbade386870e0246254  docs/implementation/review-closure-2026-10-19/documentation-instructions.md
1fd37fad1ac94e890e8fbc4b8f73147965b4a5eb5cd9ce735a98c2ff15d13be7  ops/git.ts
029859ad06814ad33740497d494227193b23593861c67423846176f8d3ce65bb  components/qcl-negf-contracts/CONTRIBUTING.md
b51e7599b313f6f2c35b51b6f53e98e199b71f488083edf9a1ce574b8af5a602  components/qcl-negf-contracts/pyproject.toml
41b5b746bbf28cd0e60bb85bc927f1c55ba0ac2695f3271b875f83c057a744d1  components/qcl-negf-contracts/src/qcl_negf_contracts/__init__.py
fd82f76a005519962b1edbfd5b9971f6e8d50c0806ca1f4070359e908fa205fa  components/qcl-negf-contracts/src/qcl_negf_contracts/messages.py
639ebd85f0a1612d2c036d11d8926f7c4bdd04778d5690a8778eb03e8cb6ccaa  components/qcl-negf-contracts/src/qcl_negf_contracts/artifacts.py
abed7316f061d1e386a210bc2ed95171ba38c9563e5bf4dd8d5b2701aa0e1256  components/qcl-negf-contracts/src/qcl_negf_contracts/schemas/scientific-plan.schema.json
cf0acc8fe09d86df5a4eead4eeca9161c516436ce65a517114c172294e42965c  components/qcl-negf-contracts/src/qcl_negf_contracts/schemas/point-status.schema.json
0231b4d437ed3086a2cb365a0ce2a3926da93008d67e99df598e8aced6f63fd7  components/qcl-negf-contracts/tests/test_contracts.py
d4113f43cddf02d46025434eb3a9dd8e110e90d6
 M components/qcl-negf-results
 M docs/implementation/review-closure-2026-10-19/execution/checkpoint.json
 M docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-current-bound-doc-publication-journal.json
 M docs/implementation/review-closure-2026-10-19/execution/qcl-targeted-receipt-census.json
 M tests/application_cd_test.ts
 M tests/solver_test.ts
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-doc04-root-red-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-doc04-root-red-v2-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-doc04-root-red-v2-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-cli-seam-design-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-cli-seam-design.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-platform-red-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-ops04-root-red-v2-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci03-M1-impl-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci03-M1-red-review.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci03-M1-red-v2-report.md
?? docs/implementation/review-closure-2026-10-19/execution/evidence/qcl-sci03-M1-red-v2-review.md
?? docs/implementation/review-closure-2026-10-19/execution/qcl-doc04-root-red-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-doc04-root-red-v2-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-doc04-root-red-v2-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-local-runtime-metadata-preflight-1.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-local-runtime-metadata-preflight-2.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-local-runtime-metadata-preflight-3.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-cli-seam-design-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-cli-seam-design-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-platform-red-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-red-v2-delta.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-ops04-root-red-v2-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-impl-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-red-intent.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-red-result.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-red-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-red-source-binding.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-red-v2-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/qcl-sci03-M1-red-v2-review-identity.json
?? docs/implementation/review-closure-2026-10-19/execution/tests/DOC04-NODE-RED-1/
?? docs/implementation/review-closure-2026-10-19/execution/tests/DOC04-PY-RED-1/
?? docs/implementation/review-closure-2026-10-19/execution/tests/OPS04-ROOT-RED-1/
?? docs/implementation/review-closure-2026-10-19/execution/tests/SCI03-M1-GREEN-2/
?? docs/implementation/review-closure-2026-10-19/execution/tests/SCI03-M1-RED-1/
?? tests/docs_math_test.mjs
?? tests/test_docs_assembly.py
 e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee components/QCLNEGF.jl (v0.2.0-15-ge431609)
 1acc165650fd4f4c2d49605cc679f90e3f6fcdae components/QCLNEGFRunner.jl (v0.2.0-27-g1acc165)
 d8f8092ca1c76523d85384b4bac8198d8bfa736b components/qcl-negf-aiida (v0.2.0-17-gd8f8092)
 12fc26462bbab3df76904c6deb01f8c6596de7be components/qcl-negf-contracts (v0.2.0-14-g12fc264)
 b067723c82382689bff5cc366981c56e99b926f8 components/qcl-negf-platform (v0.2.0-90-gb067723)
 2622de5ee28b454ff4f809cc3dd00c1e5bc2295d components/qcl-negf-portal (v0.2.0-17-g2622de5)
 3ed8a9fe5f16f51bbcb7547ff2d677e8d3608731 components/qcl-negf-research (v0.2.0-9-g3ed8a9f)
+de70638a982f91b7e125ab1cfc70a2daef2a656d components/qcl-negf-results (v0.2.0-23-gde70638)
12fc26462bbab3df76904c6deb01f8c6596de7be
