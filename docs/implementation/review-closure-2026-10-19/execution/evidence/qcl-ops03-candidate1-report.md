# OPS03 candidate 1 — source/control packet, execution pending, identity D held

Platform baseline HEAD `6c5b11f3c74d44fed8b2c159f890b83e0b5456b9`. All Git mutations belong to root; writer performed none. Accepted OPS02 D SHA256 `26374bcfb194aa5c9701bd00ceaae6016cd535dcc722e8b221719fec72450030`, independent review SHA256 `3d5f3c7e33f8c9f1e8a863c73fdefab4969c3af85c737415e294ac366a17a54a`.

Root witnessed OPS03 RED1 (nine failures, mixed fixtures) and RED2 (nine semantic failures after exact fixture repair). Root receipts/raw logs remain `/tmp/qcl-OPS03-RED-1` and `/tmp/qcl-OPS03-RED-2`. RED2 root receipt: wall 1.624 s, RSS 78487552 B, log 11625 B. Writer executions/imports/tests/builds/native/SSH/services: **0**. Shared initial invocation count: 2 consumed, next root GREEN1 would be 3/4, no reset. Root named finite next packet: all three selected test files in one process, <=90 s, 1 CPU, 1 GiB, bounded output; no author invocation or automatic rerun.

## Candidate

Only four accepted owning files changed: `ops/application_release.py`, `ops/worker_lifecycle.py`, `tests/test_application_release.py`, `tests/test_worker_shutdown_intent.py`. `tests/test_worker_lifecycle.py` stays unchanged, included in requested root verification. No owning docs/Nix/modules/bootstrap/runtime services/foreign states changed. Full frozen diff `/tmp/qcl-ops03-candidate1.patch`; `git diff --check` clean.

- Nonconstructible/noncopyable/nonpicklable exact process-local capability held by strong registry; actual local PID/start ticks/boot, canonical runtime directory/lock dev+inode, exact operation/manifest and nonrenewable finite deadline. No-follow/nonblocking/CLOEXEC regular single-link common lock plus legacy activation fence; no truncate/unlink. Fork child clears registry and closes inherited descriptors without LOCK_UN. Revocation precedes close; closed descriptors do not leak the other fence during exit.
- Public activation/preparation/deliver_pool/worker stop/repair/finish acquire owners. Direct activation requires matching closed selected gate, unknown guards and exact worker marker routing. Private activation consumes the same parent capability. Optional direct API machine-observation policy is **held for D**, below.
- Immutable exclusive mode0600 lifecycle intent with file+directory barriers before application mutation; bounded original release/env/allowlist bytes plus hashes and profile target snapshots in receipt. Snapshot reads share inherited metadata accounting when present. Live exact registered own artifacts alone can self-exclude; forged same-attempt or replaced inode cannot. Failed/pending/orphan/cluster-update evidence is retained. Terminal receipt precedes final intent unlink; no later fsync introduces a new failing cleanup step after the sole barrier is gone. An unsynced deletion may reappear after crash and inhibit conservatively.
- Controller whole update requires exact v2 capability advertisement on every node. After protected config/enrolled/local/remote rechecks, direct real local activation/check/fleet_health use the same owner/deadline/output/metadata budget, no mutating self SSH or self Nix copy. Parent durable pending_local_mutation precedes helper writes and clears only after local envelope verification. Existing worker copies/commands use bound remote identity/attempt/trust.
- Normal lifecycle uses per-node lock then common owner. Capture/finalize have separate short common ownership with the original finite poll deadline; Runner waits release common ownership. Startup holds same-node lock and common owner through health/RESUME, retains independent marker semantics. Concrete normal state publishers receive before callbacks. Remote startup receives remaining finite duration.
- Concrete gate publishers/final cleanup require local owner and original deadline; selected service.env uses the supplied gate. Expired whole checkpoint updates only in-memory outcome, retains last durable pending state and performs no new write. Existing deadline tests now distinguish in-memory failed report from retained running/pending receipt, rather than demanding an after-deadline terminal write.

## Finite O01–O18 control denominator

New tests are `OPS03LifecycleOwnerTests` and `OPS03WholeRoutingTests`; existing full-body controls remain. All process children use explicit Pipe/Event readiness, watchdog <=5 s and kill/join cleanup. New external boundaries never execute a real command. Actual native/provisioning/Slurm/NFS power loss is not simulated as PASS.

| ID | Control locators in selected tests | Evidence status |
| --- | --- | --- |
| O01/O02 | actual public delivery vs activation/preparation process contention, reverse ordering | RED2 witnessed differentiating failures; GREEN pending |
| O03 | real owned helper acquisition count; actual whole-update callback -> real helper/temp profiles/env/ready/check/NFS fake boundary, pending receipt, no self SSH/copy | added, not executed |
| O04 | arbitrary object/dict/PID/object.__new__, copy/deepcopy, constructor, pickle | added, not executed |
| O05 | wrong runtime/manifest/operation/deadline; revoked context, replaced lock/runtime inode, replaced and literally closed fd; symlink/FIFO/hardlink lock rejection | added, not executed |
| O06 | inherited token refused and parent flock retained after child exit; killed owner releases lock but persisted orphan still blocks activation | added, not executed |
| O07 | expiry after closure/app/solver/registration; before ready:false/true and terminal receipt; existing during-allowlist publication test | added/retained, not executed |
| O08 | ten controlled local process cuts: pending-before-command, app, solver, registration, allowlist, env, ready:false, units, ready:true, before terminal receipt. Original release/env/allowlist bytes and immutable intent retained; one controlled retry blocked | added, not executed |
| O09 | intent write/file-fsync/dir-fsync; ready and terminal write/replace/file-fsync/dir-fsync matrix; old open/close/terminal gate failure fixture retained and updated to preserve unknown raw replacement | added/retained, not executed |
| O10 | prior lifecycle/admission/running-local/cluster marker; same-attempt lookalike and same-bytes replaced own intent | added, not executed |
| O11 | legacy activation fence, delivery contention, v1 protocol refusal before quiesce, lock bytes retained | RED2 fence failure; expanded controls not executed |
| O12 | both independent damaged GC roots; existing controller immutable UUID repair test and identical UUID guard; orphan retry controls O06/O10 | retained/expanded, not executed |
| O13 | cold controller vs worker/existing installation missing gate, exact old bytes, conflict and racing gate tests retained; fixture only permits new lock files | retained, not executed |
| O14 | closed selected direct gate; explicit forged local controller generation before app mutation; existing enrollment/expected identity guards retained | gate RED2 witnessed; full-node omitted-identity boundary D held |
| O15 | same-node lock contention at real finalized return boundary; actual Runner wait lets node B finalize while update/activate are inhibited by A durable intent | new concurrent controls, not executed |
| O16 | vanished/orphan/unknown normal lifecycle, failed terminal after RESUME independent marker retained; per-node bytes/release control | retained/expanded, not executed |
| O17 | actual public worker stop wrapper parks under owner/journal; foreign attempt activate/finish contend; actual physical stop/effective mask/origin predicates retain existing full-body controls | added + full-body fixtures, not executed; parked stop body is explicit boundary hook |
| O18 | no-owner/expired gate and cleanup helper calls, selected env gate, before callbacks at concrete call sites | selected env RED2 witnessed; expanded controls/audit not runtime evidence |

The new controls exist, but no GREEN/control counts are claimed. A few proof dimensions intentionally compose independent controls (for example worker wrapper contention + existing full-body mask checks); this is not a claim that a native stop race or final atomic job-admission commit ran.

## Explicit D blocker, not waived

Exact question `/tmp/qcl-ops03-local-identity-question.md` SHA256 `ec2b485b779d299cb84f8d996833c442a4d42bffcfdb004407e920461230583d`: accepted §3 retains expected_node_identity=None; §4 explicitly requires CLI protected role/full observed identity and adds direct API closed gate, but omitted-identity direct API observation is ambiguous. Root holds this exact boundary before final readiness/CP-CODE and will obtain explicit ultra D ruling. Candidate preserves optional direct trusted Python observation shape pending that ruling, while CLI/whole-update routes enforce protected authority; this is **not** an accepted security exception. No new trust probe or unsafe CLI flag was invented.

## Unchanged required residuals

`OPS03-FOLLOWON-PROVISIONING` OS/systemd/provisioning writers remain outside this Python edit set; universal single-writer closure is not claimed. CR04 effective atomic job-admission commit/read remains separate: a crash after authorized shared gate replace is not proven effectively closed for all readers by a controller-local intent. No waiver or new distributed protocol was introduced. Native/scientific/full release acceptance is absent.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Semantic baseline regressions witnessed | Root RED2 receipt/raw log | Nine selected controls only | изменить |
| Candidate implements scoped cooperative owner and local route | Frozen owning diff + control locators above | No candidate test execution/review yet | дополнительно измерить |
| Omitted-identity direct API policy accepted | Exact question and root hold | Ultra D ruling required before readiness | данных недостаточно |
| Candidate CP-CODE / all GREEN | No GREEN receipt | Root execution/review pending; shared counters retained | данных недостаточно |
| Universal OS writer closure / atomic effective admission | Accepted D/R residuals retained | Separate required follow-on gates | данных недостаточно |
| Native/scientific/full release accepted | No corresponding receipts | Writer made no runtime execution | данных недостаточно |
