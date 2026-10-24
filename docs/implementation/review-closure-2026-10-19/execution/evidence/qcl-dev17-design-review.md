# DEV17 independent CP-DESIGN

**Вердикт: PASS CP-DESIGN, scoped DEV18 I-ready** для указанных четырёх owning paths и55finite cells. Конкретных блокирующих interface/barrier gaps не обнаружено. Implementation, runtime, real-crash/NFS/native durability этим review не установлены. Reviewer никаких imports/tests/build/solver/SSH/Nix/Git mutations или owning writes не выполнял.

## Source-first и immutable packet

Actual Runner HEAD `12e4d025948847c1b5d18ef4eb43a9934d8e20da`; dirty только новый `docs/runtime-checkpoint-durability.md`, tracked source diff empty. Parent shorthand persistence/filesystem_repository исправлен на фактический `src/infrastructure/runtime/filesystem_repository.jl`. До candidate прочитаны save/load/codec/allocator/helpers, direct coordinator callers, only event lock, atomic_files и scientific point_artifacts **для сравнения**, applicable architecture/CONTRIBUTING/handoff DEV17/18. Собственный source-first вывод о missing barriers и отсутствии expected-attempt guard передан root до чтения design.

- Owning doc SHA256 `d6df20992e22296eeeaa38d80919b39f6d439788a4ab7f4dceb942324f139ffc`.
- Author report `/tmp/qcl-dev17-design-report.md` verified `466197b58198880c8d95c6b2281fac7fcbd51a866b052a5d40eda815a85fe4be`.
- `/tmp/qcl-dev17-design.patch` SHA256 `70acbddd74bd708cee028f231431fa6cdb4aefad03260315e1316b71dadc23b4`; owning doc bytes are primary binding. No production code candidate yet.
- Source repository `cd65f6f5b1e7128e3f5e7be9c6126a7eb5db799e2723431c86a9db36ae07a03f`; atomic_files `7bfdcf14c2cee4a2c6fa63d0c739ed6c93f1d74b729a5abd3d22a9220eb6a9a4`; hashes independently checked. `git diff --check` exit0;4relative source links resolve. No format/docs build claim.

## Independent baseline observations

Current save509–560: closes mktemp handle, codec writer returns, hashes/sizes, chmod, mv payload, _immutable_yaml envelope, returns reference. Generic _atomic_yaml and _atomic_replace_file give same-directory native namespace replacement and chmod but **no file/directory fsync**. Coordinator checkpoint! directly returns reference; three load sites add no enclosing durability barrier. repository.lock currently covers only event sequence, not generation allocation/save.

Current reader563–596 selects lexicographically last metadata, validates run/point/positive attempt/codec/size/SHA and then decodes. No metadata→nothing; corrupt last selected checkpoint fails rather than fallback. Current API has no exact expected-attempt input. Coordinator intentionally reads historical attempt for resume, so rejecting every different positive attempt would alter compatibility.

Scientific point_artifacts independently syncs closed generation files/directories, publishes, syncs parent, verifies, writes receipt/pointer barriers. Different module/path does not enclose generic save. Its current.json/previous.json, scientific schema/receipt/pruning cannot be silently introduced here.

## Sequence и primitive

Doc120–180 has coherent acknowledged publication protocol:

`codec closed → regular/nonlink +chmod0640 → hash/size → payload fsync → same-dir immutable payload rename → bottom-up checkpoint/point/points/run/root/anchor directory fsync → metadata written/closed/regular/chmod0640 → metadata fsync → immutable metadata rename → checkpoint directory fsync → published envelope/identity/bytes/hash readback → reference`.

Metadata filename is existing logical commit/selection update, **no generic pointer**. Readback before return is mandatory and does not decode codec twice. A post-metadata-rename failure may leave visible complete new checkpoint without writer acknowledgement; reader integrity return is explicitly distinct from writer persistence acknowledgement.

Publisher161–171 checks same-directory regular source and absent destination including dangling symlink, then one jl_fs_rename/error check with no post-fsync chmod, mv/copy/delete fallback or retry. Under one writer/object serialization, check-then-rename is intentionally not advertised as an OS-level concurrent no-replace primitive. Generic shared helpers keep their existing semantics; runtime-only helpers make scope clear.

Full save lock includes generation allocation, barriers and readback. Private active flag rejects recursive save under ReentrantLock before allocation/mutation; other tasks wait, then see released flag. Event callbacks/read-only immutable checkpoint reads remain permitted. Finally releases active/lock without deleting raw files or masking original exception. Errors propagate, partial temporary/named orphan/old generations survive; allocator accounts named orphan. There is no migration/GC/backfill of durability claims.

Directory ancestry: anchor is computed before mkdir, parent of existing repository root still included, and missing path chain synced bottom-up before metadata. Contract explicitly assumes trusted real ancestry, no symlink/external mutations, one writer across objects/processes/machines, and stable ancestry above selected anchor. Existence alone is not new measured proof of that assumed stable boundary; native mount/ownership/recovery evidence remains outside this packet. Within that stated boundary the full healthy trace must include intermediate parents, not just checkpoint directory. Unix fsync unsupported→pre-write error; scientific helper silent non-Unix no-op is not reused.

## Codec, reader и attempt compatibility

Closed codec contract124–126 is essential: writer returns after closing all handles, no background writes/sidecars. YAML and callback paths share repository protocol; production HDF5 codec copying into temporary is allowed as payload creation, never publication fallback.

Reader extension83–118 precisely adds expected_attempt::Union{Nothing,Integer}=nothing. Explicit value must be positive non-Bool representable Int, checked before listing; mismatched declared attempt raises real production CheckpointIntegrityError before payload open/codec decode. Default existing three coordinator callsites retain cross-attempt resume; latest reference keeps original attempt. Existing calls are **not** described as enforcing the new optional guard. Missing metadata remains nothing, including guarded call.

Regular non-symlink metadata/payload, metadata filename/generation match, envelope/size/SHA checks precede decode. Bad latest has no fallback/fresh-start repair. YAML/read/envelope errors become locator-bearing CheckpointIntegrityError except InterruptException passthrough. Old complete v1 wire fields/reference/filenames unchanged and readable without rewriting; new writer barriers do not retroactively certify them.

## Exact DEV18 seam, paths и55-cell matrix

Private _RuntimeCheckpointIO and _save_runtime_checkpoint! signatures are concrete;4operation adapters +cut, runtime factory and context fields/types named. Ten cut names correspond exactly to closed/hashed/synced/published payload, ancestry sync, closed/synced/published metadata, final dirsync, publication verified. No process-global mutable hook; production cut no-op. Fault adapters throw before selected operation, trace records prefix, ENOSPC writer closes partial file and preserves original SystemError.

Count independently checked:20C +9E +16R +2Rguard +5H +3L =55. Both empty/old baselines, all10 cuts, file/publish/first and final dirsync errors, partial payload/metadata, E09same-size corruption forcing **actual writer readback failure**,16malformed/identity/size/hash/symlink cases, invalid/matching/mismatched optional attempt, fresh+sequential+callback+literallegacy+orphan healthy, concurrent/reentrant/failed-save lock cases are bounded and distinguishing. H01 covers missing nested root/anchor trace, H02 existing path. Old bytes preserved; H success cannot hide behind unavailable; newer corrupt generation cannot fall back.

Independent reader owns directory enumeration/last metadata regex, literal expected identity/payload/generation/attempt, bytes/SHA checks. It does not call production validation/reference/hash/load/codec helpers. YAML parser/SHA implementation shared explicitly, not independent cryptography proof. Public reader rejected-tree assertions are separate; positive wrong-attempt test actually supplies new keyword, not fixture-only check.

Source-selected isolated module include uses real composition/application_runtime.jl, which depends only SHA/YAML and own solver-independent files. It avoids Core/HDF5 import for new fixture and labels source-selected evidence honestly; existing integrity fixture remains separate owning-package/HDF5 invocation. No fake module/package or semantic numerical acceptance. Each tiny cell fresh temp tree; retained output bounded8MiB; no automated matrix expansion/rerun.

Approved owning paths: filesystem_repository.jl; existing yaml_repository_provenance_spans_and_checkpoint_integrity.jl; new runtime_checkpoint_durability_faults.jl; owning doc for actual locators. atomic_files remains read-only comparator, no scientific/coordinator/schema changes. Two future L-JL commands/1CPU2GiB120s per call/counters bounded by actual master grant; no runtime is implied by this PASS. Existing compile/dependency cap may block runtime and must remain explicit.

## Limits и решения

Synthetic exception cuts inspect live bytes/order, not dropped dirty pages, NFS cache/device/power failure. Local POSIX guarantee is conditional on successful real fsync/rename behavior and trusted/stable ancestry assumptions; syscall success does not identify FS type. No durability of generic events/status/results, global OS writer closure, new pointer semantics, scientific/model/discretization/experiment or S1 acceptance is inherited.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Baseline generic barrier отсутствует | actualsave/helpers/callers, no fsync | source evidence | изменить |
| Proposed publication ordering closes scoped gap | closed/chmod/sync/native rename/ancestry/metadata/readback sequence | conditional local POSIX; implementation pending | сохранить |
| Identity и cross-attempt behavior совместимы | v1 unchanged/defaultnothing/explicit optional guard | existing callers intentionally notexact-attempt | сохранить |
| DEV18 имеет конкретный bounded implementation target | exactseam/4paths/55cells/independentreader | source/runtimeCP-CODE ещё требуются | сохранить |
| Native/NFS/device/power-loss persistence measured | evidence отсутствует | synthetic cuts не realcrash | данных недостаточно |
| Numerical/scientific acceptance установлена | новый scientificsolve отсутствует | genericstorage design only | данных недостаточно |
