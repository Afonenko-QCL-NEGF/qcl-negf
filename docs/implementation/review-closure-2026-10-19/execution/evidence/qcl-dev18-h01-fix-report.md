# DEV18 H01 literal correction — frozen

Root supplied GREEN1:3197pass/2fail/0error. Both failures are H01 independent
raw bytes/SHA expectations for the built-in YAML codec. Reviewer independently
confirmed built-in YAML.write_file quotes string values. This is an expected
literal defect; production behavior/criteria are not weakened.

Only H01 changed: independent expected bytes are now literal `state: "new"\n`
instead of callback raw NEW `state: new\n`. Added precise comment separating
built-in YAML serialization from callback-written raw bytes. Expected bytes are
not derived from writer output or target read. Both exact byte/SHA assertions in
complete remain unchanged. Other54cells and old provenance/integrity fixture
remain byte-identical; no matrix expansion, no assertion removal.

Frozen files:

- `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGFRunner.jl/test/infrastructure/runtime_checkpoint_durability_faults.jl` SHA256 `db32630942eace2429ca7014df4caec66044fca2cd643386617a2c0413b1c69c`.
- `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGFRunner.jl/src/infrastructure/runtime/filesystem_repository.jl` SHA256 `44a1d6e907b985bdcd5fb89b73a50ca434ab6209462564d63936562317521849`.
- `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGFRunner.jl/test/infrastructure/yaml_repository_provenance_spans_and_checkpoint_integrity.jl` SHA256 `a672cc8313f92446b05778422c9d23408f47983782da0dc14822c94d92bc45ef`.
- `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGFRunner.jl/src/infrastructure/persistence/atomic_files.jl` SHA256 `7bfdcf14c2cee4a2c6fa63d0c739ed6c93f1d74b729a5abd3d22a9220eb6a9a4`.
- `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/QCLNEGFRunner.jl/docs/runtime-checkpoint-durability.md` SHA256 `d6df20992e22296eeeaa38d80919b39f6d439788a4ab7f4dceb942324f139ffc`.
- `/tmp/qcl-dev18-h01-fix.patch` SHA256 `e47ac818f7e4700a613c7048f0c7a6d2e093cf8a7a3be592381ef908764b54c3`.
- `/tmp/qcl-dev18-full-h01-fixed.patch` SHA256 `7defab1387e58b52e36eb1f971f91e10b0195fc78869ea281ad372aec64f99bc`.

Static checks: only H01 substring changed, no trailing whitespace, copied fixed
bytes match; production/oldfixture/atomic/doc hashes unchanged. No Julia/parser/
imports/tests/Git executed by writer. Original RED and GREEN1 failures/receipts
preserved; old patches/reports remain immutable historical evidence.

Root owns separately granted GREEN2 (third call total, retains initial2 history),
same2files/120s/1CPU/2GiB/16MiBtmp/2MiBlogs. No automatic retry loop.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| H01 literal corrected independently | Narrow patch, reviewer/root serialization finding | GREEN2 pending | дополнительно измерить |
| Production и остальные54cells сохранены | Exact source hashes + unchanged prefixes/suffixes | No new runtime by writer | сохранить |
| Native/scientific acceptance established | Evidence отсутствует | Engineering fixture correction only | данных недостаточно |

STOP: narrow/full patches and source frozen for root GREEN2.
