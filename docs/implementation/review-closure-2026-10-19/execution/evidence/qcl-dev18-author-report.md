# DEV18 implementation candidate — frozen for root GREEN/CP-CODE

Scope: accepted DEV17 generic runtime checkpoint durability only.
Runner parent-provided source HEAD `12e4d025948847c1b5d18ef4eb43a9934d8e20da`;
managed root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
Production release received from root after independently inspected semantic RED.
No Julia/import/tests/build/install/Git/server/SCBA/Poisson execution by writer.

## Baseline evidence и RED release

Accepted immutable packet remains:
- Owning doc SHA256 `d6df20992e22296eeeaa38d80919b39f6d439788a4ab7f4dceb942324f139ffc`.
- CP-DESIGN review SHA256 `bbe7e46b440db2d02a361949cfa55e7ab7895bb470375bfc5af0038308f0eadb`.
- DEV17 author report SHA256 `466197b58198880c8d95c6b2281fac7fcbd51a866b052a5d40eda815a85fe4be`.

Root reports DEV18-RED-1, reviewed Julia bounds v3:233pass/53fail/0error,
exit1,wall12.353s,RSS508928000B,tmp25768B,raw83675Bcomplete,no guards.
Root independently checked R06 actual YAML.ParserError classification,
R09 filename/generation mismatch accepted with codec1, R15/R16 symlink accepted
with codec1. These are behavioral RED beyond absent new seam; writer treats
root receipt as supplied evidence and did not independently execute/relabel it.
Original raw RED/source identity remains owned by root. Initial sandbox write
failure and exact diagnostic retained in `/tmp/qcl-dev18-red-report.md`.

## Frozen changed files и patches

- `src/infrastructure/runtime/filesystem_repository.jl`:32599B,
  SHA256 `44a1d6e907b985bdcd5fb89b73a50ca434ab6209462564d63936562317521849`.
- New `test/infrastructure/runtime_checkpoint_durability_faults.jl`:22506B,
  SHA256 `4e74a26ab5caf80e12ddae3e85ca4b3bb793081686bd0bbaeeb0fa35028ac429`.
  Exactly the root-executed RED bytes;55cells preserved without criterion changes.
- Production-only patch `/tmp/qcl-dev18-production.patch`:17194B,
  SHA256 `1e64a8dea73abfe5cb674368013525aa52f6f2b2d2dfee7802fd4c306fefc58e`.
- Full component patch `/tmp/qcl-dev18-full.patch`:40265B,
  SHA256 `7b699bfa2e4bc129a1c2303ed7382917c46b43f44966c49c577cd9356e0875bf`.
  Both patches created by Python difflib; no Git operations.
- Baseline source snapshot `/tmp/qcl-dev18-repository-baseline.jl` has accepted
  SHA256 `cd65f6f5b1e7128e3f5e7be9c6126a7eb5db799e2723431c86a9db36ae07a03f`.

Unchanged hashes:
- existing YAML integrity fixture `a672cc8313f92446b05778422c9d23408f47983782da0dc14822c94d92bc45ef`;
- read-only atomic_files `7bfdcf14c2cee4a2c6fa63d0c739ed6c93f1d74b729a5abd3d22a9220eb6a9a4`;
- owning documentation remains exact accepted SHA above.
No coordinator, scientific implementation, HDF5/schema, runtime harness or
root checkpoint/state changes. Scoped escalated copies to the sole authorized
owning production path succeeded; no auto-review rejection occurred.

## Implementation и обоснование

Repository adds private `_checkpoint_active=false`, retaining one-argument
constructor. Full save under object ReentrantLock includes allocation,
all barriers and readback. Nested save rejects before generation/temporary;
finally clears active without deletion/masking original failure. Other tasks
serialize; cross-object/process/machine single-writer remains a precondition.

Pre-mutation validation covers run/point, positive non-Bool Int-representable
attempt/iteration, portable kind and portable metadata mapping. Unsupported
non-Unix fails before mutation. Anchor computed from dirname(root) upward
before mkpath. Payload is codec-closed, regular/nonlink, chmod0640, hashed/sized,
fsynced, published using one `jl_fs_rename`; every directory from checkpoint
up to anchor inclusive is fsynced. Metadata temporary is written/closed,
regular/nonlink, chmod0640, fsynced, renamed, then checkpoint directory fsynced.
Ten exact cuts and exact named context fields are preserved via private
_RuntimeCheckpointIO. Production cut no-op; no global hook.

Publisher requires same directory and absent destination including dangling
symlink. No post-fsync chmod, mv/copy/delete fallback, overwrite or retry.
Directory fsync records sync errno before close and preserves first error;
close failure also propagates if sync succeeded. Generic _atomic_yaml,
_immutable_yaml and _atomic_replace_file keep their old semantics.

Writer readback parses published YAML, verifies canonical envelope equals
expected, then verifies actual identity/basenames/regular files/bytes/SHA,
without codec decoder call. Only after publication_verified returns does
save return reference. Explicit integrity mismatch raises CheckpointIntegrityError;
writer readback I/O/parser exceptions retain original identity through
preserve_read_errors=true. All raw temporaries/orphans/published and old files
survive failure; next allocation includes existing named orphan.

Public reader keeps last-filename fail-closed selection/no fallback/no repair.
It additionally rejects metadata/payload symlinks and metadata filename/generation
mismatch. Parsing/envelope/read errors gain locator-bearing
CheckpointIntegrityError; InterruptException passes through. Optional explicit
expected_attempt validates positive non-Bool Int representation before listing,
then mismatched declared attempt raises exact `attempt mismatch` before payload
open or codec reader. Default nothing preserves historical cross-attempt
resume, and reference retains original attempt. No pointer/migration or new
wire fields introduced. Historical valid v1 bytes remain readable.

## Проверка и remaining gate

Only static Python checks executed: copied source bytes, final newline/no trailing
whitespace, unchanged test/atomic/docs hashes, source order of exact10cuts,
anchor-before-mkpath, sync-before-readback-before-return, one native rename,
absence of cleanup/mv/shared-atomic invocation in new checkpoint protocol.
These checks do not establish Julia parse/compilation, runtime correctness,
real-crash/NFS/device durability or scientific acceptance.

Root owns second/final initial L-JL packet: GREEN1 new faults+existing integrity
in one process, within accepted120s/1CPU/2GiB/16MiBtmp/2MiBlogs. Writer does not
consume/extend grant, run tests, change harness, rerun or start production work
beyond this frozen source. Independent CP-CODE and measured GREEN required.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Accepted scoped protocol реализован | Frozen source+full patch, exact seam/lock/barrier/readback order | Source/static evidence; GREEN pending | дополнительно измерить |
| RED различает реальные reader defects | Root233pass/53fail, R06/R09/R15/R16 raw inspection | Writer did not execute root run | сохранить |
| Tests и scope preserved | RED fixture hash unchanged; existing YAML/atomic/doc hashes unchanged | Root owns Git/source integration receipt | сохранить |
| Native/NFS/power-loss persistence измерена | Evidence absent | fsync/synthetic tests не native fault receipt | данных недостаточно |
| Scientific/model/numerical acceptance установлена | No scientific changes/runs | Generic engineering storage scope only | данных недостаточно |

STOP: source/patch frozen for root GREEN and independent CP-CODE.
