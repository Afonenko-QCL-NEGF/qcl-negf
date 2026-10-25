# SCI07 — source ledger и границы свидетельств

2026-10-20. Все действия source/text/metadata/hash only; никакого target parser/import/runtime, solver/test/build/network/server или Git mutation. Existing applicable brainstorm/writing-plan instructions used earlier; qcl-performance-audit applied/read in this task.

Design SHA256 `1f569ba726873d80715523621933caa6c0a0b0ad84e5a59ba9ef077b12001635`, bytes 42322.

## Named inputs: conservative full-file charges

| Input | SHA256 | Bytes | Charged passes |
| --- | --- | ---: | ---: |
| `//home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/AGENTS.md` | `ef2ef40fe24e1f83758a59497526017955df377827004fb39bd0d39ca90d9330` | 17383 | 2 |
| `//home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/docs/architecture.md` | `8e49c02d948891f31f6d27360564b4a2708d7a1546808d9f10f38d0c5ebec6b7` | 5501 | 3 |
| `//home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/docs/implementation/review-closure-2026-10-19/science.md` | `0f52fc7148456b9eeff6bb993b5d1e701825781c58733dc519972c5312b8c26a` | 42428 | 5 |
| `//home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/docs/implementation/review-closure-2026-10-19/operator-permissions.md` | `4887a5d4ad67a84424225d5b827ba2975ec97e319c94efe59a3e67b9120054a0` | 32033 | 6 |
| `//tmp/qcl-sci07-source-discovery.json` | `79bc31fda78d382ceda9f24f0678983bd5421fbe89e3ee0c03ca104364fae98d` | 3802 | 2 |
| `//home/tolya/Загрузки/qcl-negf/.agents/skills/qcl-performance-audit/SKILL.md` | `0ccc0aaed3c88c3620082bf9808113c3c725aaa2bc3b47b56db9d349e0d58f74` | 10475 | 2 |
| `//home/tolya/Загрузки/qcl-negf/.agents/skills/qcl-performance-audit/references/telemetry.md` | `1b7168a1bb12525f6e8c7677266ed3adb64faafebf6e1a7816337cb8df399d1b` | 21682 | 2 |
| `//tmp/qcl-sci04-design-v2.md` | `d787ad47f409b9fffb5a1ac5503857691d0282564bae88d774f0be85b033506c` | 61527 | 3 |
| `//tmp/qcl-sci03-current-bound-design.md` | `ca84b1cc763aa7bc017364ece4f7e95aff5bd0107c0c7277fb87eed250f215f7` | 39159 | 2 |
| `//tmp/qcl-sci03-M1-impl-review.md` | `c529835dfdb9ac374b3933af4403bab26ea2fb0b89494a56918f7960f8be7e8c` | 16264 | 3 |
| `components/QCLNEGFRunner.jl/docs/src/user/resources.md` | `11cd80689f7c7bb0c92bdf1c13b8891dbda7241689bd81b1300ffd19219184f5` | 1182 | 2 |
| `components/QCLNEGFRunner.jl/docs/src/user/results.md` | `39e1178fc88a940b69ad61298d54538f44d1e39df6b9d9c2dd8e5264f395f561` | 17568 | 2 |
| `components/qcl-negf-aiida/src/aiida_qcl_negf/parser.py` | `6639e9dc488a256fa26268784149820fb77b1c3bf9cf6a0671b4aa80931b91f3` | 7924 | 2 |
| `components/qcl-negf-platform/modules/runner.nix` | `2b644ec50be37b457aae0bcb86d335b7a22ddbe1531f1ba1cbfc208c22cdbbdc` | 6508 | 2 |
| `components/QCLNEGFRunner.jl/src/application/auto_strategy.jl` | `810c72af8e4289c3dd61d4f49549a083568472646fa69eb625f41c5702840326` | 19019 | 2 |
| `components/QCLNEGF.jl/src/numerics/optimized/production_cache.jl` | `5c10eda35300c4c1fcbe46e23f0f95a3e9e9783b280504fc2dc4bd4575c70ee8` | 32810 | 3 |
| `components/QCLNEGFRunner.jl/src/infrastructure/persistence/point_artifacts.jl` | `9e8c1d8f624bb828134129c10226211968360950cbac9ffd82e247a8ec294cd4` | 77381 | 5 |
| `components/QCLNEGFRunner.jl/src/composition/scratch_execution.jl` | `cad52756bb47a6d1fa63cd8c86a03c4e4dcd0d9a4e12383a0671dd766697f395` | 8476 | 2 |
| `components/QCLNEGFRunner.jl/src/composition/scientific_execution.jl` | `55a3737a35b21867d91992a2a3a7807729a3b9d83b0931006d99dc82addbf9cd` | 75664 | 3 |
| `components/QCLNEGFRunner.jl/src/application/resource_contract.jl` | `6be67c1ca1ded92b57063cec6e493a589c1520ccc282e569ca131b5f65effb8c` | 2669 | 1 |
| `components/QCLNEGFRunner.jl/src/composition/native_phase_telemetry.jl` | `9605f1a4852f5edbe8ca83652500c2e0a2352feec7a04cf9d0e85bd0e712f173` | 9091 | 2 |
| `components/QCLNEGFRunner.jl/src/infrastructure/resources/linux_resources.jl` | `eed7dc41e655fa94d3b29db514b5e5682e3023b862b91e53f58dbc18f3f363b8` | 8924 | 2 |
| `components/qcl-negf-aiida/src/aiida_qcl_negf/validation.py` | `f646ec62add9f5720ca5f70bd91ff29a99f363eff3f5fe796a780389bb495e50` | 5971 | 2 |
| `components/qcl-negf-aiida/src/aiida_qcl_negf/calculation.py` | `677eccfcf211b24230d8cb912955d2ec80a508d2d31d4e60d81cfbd2db1a156c` | 9641 | 2 |
| `components/qcl-negf-platform/modules/storage.nix` | `1518be74a9c353adaa547047635dc5bbd90cda0374ac50ce08d0631bf44eb0b1` | 2418 | 2 |
| `components/QCLNEGFRunner.jl/src/infrastructure/persistence/hdf5.jl` | `d9ceeec9a76b8a7bc4c41eb24aaa2d4bb1fc1994cbce0407b9a344bdacb8d143` | 31055 | 3 |
| `components/QCLNEGF.jl/src/numerics/optimized/production_contracts.jl` | `ebb614494b4e58477231dbaf25a5283e8867e1c612859b2e26690c167b61a019` | 15596 | 3 |
| `components/qcl-negf-platform/ops/host_storage_receipt.py` | `1db73c4979f8e5eb97c755cafde6631e4488e15a5df43ac5c4b181e39226fce4` | 9650 | 2 |
| `components/qcl-negf-platform/ops/slurm_job_evidence.py` | `71ff5a020e77af0d35202c076a1f751204db79dc8f28d056bc03548bd5ed6187` | 15701 | 2 |
| `components/qcl-negf-platform/modules/cluster.nix` | `2353d2013359e720cd5712a27827dbd47a611996623db4b483b5a1c250a0f636` | 6715 | 1 |

Immutable source read ranges (inclusive source line numbers):

- `components/QCLNEGFRunner.jl@fefaa27f194bfddf85dd51a0e255beef2218c06d:src/application/auto_strategy.jl`: [[118, 175], [217, 255]]; full bytes charged per named read, not only displayed lines.
- `components/QCLNEGF.jl@9f4a96d032ad868ec010ce92d915bb81087c8d92:src/numerics/optimized/production_cache.jl`: [[540, 690], [412, 540]]; full bytes charged per named read, not only displayed lines.
- `components/QCLNEGFRunner.jl@fefaa27f194bfddf85dd51a0e255beef2218c06d:src/infrastructure/persistence/point_artifacts.jl`: [[460, 590], [760, 825], [970, 1075], [825, 914], [1, 42], [280, 375], [713, 746]]; full bytes charged per named read, not only displayed lines.
- `components/QCLNEGFRunner.jl@fefaa27f194bfddf85dd51a0e255beef2218c06d:src/composition/scratch_execution.jl`: [[1, 162]]; full bytes charged per named read, not only displayed lines.
- `components/QCLNEGFRunner.jl@fefaa27f194bfddf85dd51a0e255beef2218c06d:src/composition/scientific_execution.jl`: [[480, 560], [1080, 1162], [1240, 1285], [1370, 1408], [560, 600], [1000, 1042]]; full bytes charged per named read, not only displayed lines.
- `components/QCLNEGFRunner.jl@fefaa27f194bfddf85dd51a0e255beef2218c06d:src/application/resource_contract.jl`: [[1, 260]]; full bytes charged per named read, not only displayed lines.
- `components/QCLNEGFRunner.jl@fefaa27f194bfddf85dd51a0e255beef2218c06d:src/composition/native_phase_telemetry.jl`: [[138, 210]]; full bytes charged per named read, not only displayed lines.
- `components/QCLNEGFRunner.jl@fefaa27f194bfddf85dd51a0e255beef2218c06d:src/infrastructure/resources/linux_resources.jl`: [[1, 16], [68, 88], [160, 196]]; full bytes charged per named read, not only displayed lines.
- `components/qcl-negf-aiida@d8f8092ca1c76523d85384b4bac8198d8bfa736b:src/aiida_qcl_negf/validation.py`: [[76, 110]]; full bytes charged per named read, not only displayed lines.
- `components/qcl-negf-aiida@d8f8092ca1c76523d85384b4bac8198d8bfa736b:src/aiida_qcl_negf/calculation.py`: [[126, 150]]; full bytes charged per named read, not only displayed lines.
- `components/qcl-negf-platform@f729e2681224d6537538179ab760fefefd575003:modules/storage.nix`: [[1, 100]]; full bytes charged per named read, not only displayed lines.
- `components/QCLNEGFRunner.jl@fefaa27f194bfddf85dd51a0e255beef2218c06d:src/infrastructure/persistence/hdf5.jl`: [[267, 410], [425, 565], [1, 152]]; full bytes charged per named read, not only displayed lines.
- `components/QCLNEGF.jl@9f4a96d032ad868ec010ce92d915bb81087c8d92:src/numerics/optimized/production_contracts.jl`: [[1, 92], [88, 121]]; full bytes charged per named read, not only displayed lines.
- `components/qcl-negf-platform@f729e2681224d6537538179ab760fefefd575003:ops/host_storage_receipt.py`: [[1, 55]]; full bytes charged per named read, not only displayed lines.
- `components/qcl-negf-platform@f729e2681224d6537538179ab760fefefd575003:ops/slurm_job_evidence.py`: [[1, 52]]; full bytes charged per named read, not only displayed lines.
- `components/qcl-negf-platform@f729e2681224d6537538179ab760fefefd575003:modules/cluster.nix`: [[1, 210]]; full bytes charged per named read, not only displayed lines.

## Additional bounded locator/accounting scope

`persistence/*.jl` one function-locator pass charged 223986 B across 10 named .jl files; names/sizes below. Directory-name-only `rg --files`, wc/stat and missing root-level component AGENTS lookups add no claimed source content. Metadata/unknown small-read reserve 65536 B. Root/component AGENTS at the four component roots were absent; root instructions remain applicable.

- `components/QCLNEGFRunner.jl/src/infrastructure/persistence/atomic_files.jl`: 1680 B
- `components/QCLNEGFRunner.jl/src/infrastructure/persistence/hdf5.jl`: 31055 B
- `components/QCLNEGFRunner.jl/src/infrastructure/persistence/hdf5_backend.jl`: 451 B
- `components/QCLNEGFRunner.jl/src/infrastructure/persistence/light_results.jl`: 10363 B
- `components/QCLNEGFRunner.jl/src/infrastructure/persistence/packed_witnesses.jl`: 10776 B
- `components/QCLNEGFRunner.jl/src/infrastructure/persistence/physical_markers.jl`: 20138 B
- `components/QCLNEGFRunner.jl/src/infrastructure/persistence/physics_diagnostics.jl`: 31201 B
- `components/QCLNEGFRunner.jl/src/infrastructure/persistence/point_artifacts.jl`: 77381 B
- `components/QCLNEGFRunner.jl/src/infrastructure/persistence/production_state.jl`: 28664 B
- `components/QCLNEGFRunner.jl/src/infrastructure/persistence/scientific_history.jl`: 12277 B

Conservative logical source-read upper bound **2234548 B**, against this task grant8,388,608 B. It includes repeated ranged/rg/hash reads and whole-file charges. Physical filesystem/Git-object I/O, RSS/wall and cumulative tool-output bytes were not instrumented; do not call them measured/enforced. Some multi-source tool outputs were truncated; subsequent narrow immutable reads supplied cited code ranges. All final report artifacts are finite and individually/collectively below256 KiB. No full-tree import closure/runtime proof is inferred.

The discovery packet has its own earlier scan accounting: initial known census upper bound3,222,997 B; its later2 MiB applies only to named preparation. Preserve that record unchanged, no retroactive PASS or absorption into this task. This ledger is forensic evidence, not a manual source selection lock.

Root initial observed HEAD e22; tracked gitlink overlay and coordinator execution/evidence state were dirty. Source pins are immutable named inputs above. A later metadata-only snapshot is retained verbatim in identity; it does not replace the published/final graph. No clean/final release claim.

No raw scientific arrays/private inventory were read, parsed or copied. No source execution, deployment, cancellation, expensive environment, science attempts, CI dispatch or shared checkpoint edit. No children. STOP for independent high R.
