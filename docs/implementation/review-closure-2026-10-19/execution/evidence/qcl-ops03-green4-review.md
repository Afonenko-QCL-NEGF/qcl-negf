# OPS03 GREEN4 — independent final scoped CP-CODE

**Вердикт: PASS / CP-CODE READY для reviewed cooperative Python lifecycle-owner scope; scoped source/G1 gate может закрываться coordinator.** Exact source repair и preserved controls теперь имеют полный selected runtime witness. Это не universal OS writer closure, не native deployment readiness, CP-OPS, final CI или scientific acceptance.

## Source/evidence binding

Owning baseline Platform6c5b11f3c74d44fed8b2c159f890b83e0b5456b9. Повторно независимо пересчитаны:

| Артефакт | SHA-256 |
| --- | --- |
| /tmp/qcl-ops03-green2-candidate.patch | db537a222ef74b72b49d6521c340445b00465bf2199f38377d29f5865c275498 |
| ops/application_release.py | 1d4422bed5986901ddef22890ca16fe600336e6af2bef17d83ae809ebe794df0 |
| ops/worker_lifecycle.py | b81c722ce9cbca8a5adfed24063de268e39ea0d012ae120bb11d9491ba2a0678 |
| tests/test_application_release.py | f56062eef912a7c63ab9743a24f1db8a5043c2e24620db0732ab516485c0ce21 |
| tests/test_worker_lifecycle.py | 7d8fd49aac1b3eb4527ef185e9bf3a2cfcd7a3265e92a447954ae4e2bef15a2b |
| tests/test_worker_shutdown_intent.py | 53017ecb166b5624dab6fe3d2b57498bdbf37882a83a9be0c9c7668fdc95bfa3 |
| GREEN4 receipt.json, 2526 B | b2411039050e39b38b8a95fc02e1a77f867d6933fc83836ffa049b33540ba7c7 |
| GREEN4 original.log, 149978 B | 3250cb95a1bdd239193d42155a3d5f79a7fe721f56b575b51e84444c7fc8104f |
| coordinator harness-v7 source review | bfb262c2fe6146f9606b54b8ccd545c5d005d6a2dbc4b72e843ac33824138730 |

Все actual five source hashes соответствуют frozen candidate и exact fixture hashes root receipt. Full patch по-прежнему four changed paths (две ops + application/shutdown tests), selected test_worker_lifecycle unchanged. Review цепочка сохранена: accepted OPS02 26374bcf…; accepted narrow B c673a2b1… / independent review81686033…; original CP-CODE6955b4cc…; root-cause/fixture review4a7786f9…; exact-repair reviewca1d08d9…; finite cost review7cb5713e…. Новое review не переписывает прежние failed/interrupted verdicts.

## Actual complete runtime gate

Root GREEN4 — один процесс, все три exact selected files, `pytest -vv --durations=0 -p no:cacheprovider` с новым basetemp. Receipt: exit0, wall94.294s, sampled process-tree RSS152178688 B, sampled owned TMP67572 B, raw149978 B complete, no stop/guard/capture error/overrun,1237 temp samples. Bound wall180s/affinity1/RSS1GiB/TMP16MiB/raw2MiB. Sampler SHA16a038c0c3a530e30989965593c1c66cfac1df841178d3ad849a9f03e292b12e, harness SHA47980ee8c5bfebdb10d8f14948bc98d40088ff38c9bc6ace6bdf734cacb3495a; source review v7 hash verified. Source review describes exact four budget/verbosity substitutions only, unchanged accepted sampler/raw preservation.

Raw has **234 unique nodeid PASSED rows**, zero failed/error/skip/xfail/xpass outcome rows, terminal `234 passed in 93.54s`. AST-only reconstruction с inherited unittest methods даёт **точно тот же набор234 nodeids**, missing0/extra0; без pytest collection/import. Имеется234 unique call-duration rows. Selected denominator: application_release203, worker_lifecycle10, shutdown_intent21. O03 whole local-helper control completed1.22s; два inherited post-RESUME negative controls12.12s/12.08s. Это поддерживает прежний cumulative-cost diagnosis; прежний wall90s interruption не был product FAIL/PASS и не пересертифицируется.

## Закрытие конкретных review findings

- **R1 addressed + measured**: frozen patch отличается от diagnostic source ровно тремя fresh dict value copies на local controller authority/check/fleet_health boundaries (:2781,:2797,:2836). Canonical bind_node_observation остаётся immutable MappingProxyType; dict-only identity_value и once-only binder сохраняются, None fallback отсутствует. Actual O03 now completed/open, full node envelope/Code/profile/no-self-mutating-SSH/two-flock/one-helper assertions passed. Последующие local check и fleet-health stages достигнуты; source diagnosis не подменён fixture dict-only shortcut.
- **R2 addressed + measured**: actual64MiB CAP-derived exhaustion/no-access/sentinel assertions retained; inherited F5/R4 cases passed. Production cap не уменьшен.
- **R3 addressed + measured**: synthetic UID0 совпадает со controlled stat ownership только нужных runtime/lock inodes; real inode/mode/nlink/flock сохранены; gate UID3000/read-count/restoration assertions passed. Прежний preliminary default-runtime UID blocker отозван и остаётся отозванным (installed runtime0755); native credentials этим synthetic case не доказаны.
- **R4 addressed + measured**: malformed subcases independent runtimes; old failed direct operation retains exact blocker/gate bytes, same-runtime retry refuses до callback; fresh healthy operation отдельно проходит. Unknown marker не стирался и не adopted ради success.
- **R5 addressed + measured**: actual remote-worker malformed check has fired injection exactly once, controller verified/worker failed/later second not_attempted/no later mutation/RESUME; selected gate publisher/readback совпадает. Existing gate-open/fsync/terminal/close-failure original controls passed; source/source assertions не ослаблены.

Fixture bytes полностью совпадают с independently reviewed f560. Только runtime witness добавился после прежнего source review; повторный глобальный source audit не выдаётся за новый факт.

## O01–O18 / LI01–LI10 coverage и пределы

Named passed controls: OPS03LifecycleOwnerTests27, OPS03WholeRoutingTests3, OPS03LocalIdentityTests10, OPS03StoppedIdentityTests1, плюс существующие application/I14/mask/worker/shutdown regression families.

| Accepted control | Exact passed source witness / meaningful assertion |
| --- | --- |
| O01/O02/O03 | Real cross-process forward/reverse contention; real parent-owned local helper no reacquire/self SSH, full final envelope |
| O04/O05/O06 | Arbitrary/copied/pickled/constructed capability; wrong runtime/release/operation/deadline; closed/replaced fd/inode; fork cannot use/unlock parent, dead-owner orphan remains |
| O07/O08/O09 | Deadline cuts; ten actual controlled SIGKILL publisher cuts + original snapshots; intent/ready/terminal syscall faults; original gate open/close/terminal CR04 controls |
| O10/O11/O12 | Foreign/orphan/exact-looking marker guards; legacy lock contention/nontruncation and protocol rejection; identical completed release repairs only damaged GC root, unchanged Code UUID |
| O13 | Existing initial-controller cold missing-gate, worker gate refusal, existing exact-byte/provenance preservation, deleted/malformed/conflicting state refusal controls |
| O14 | Forged local controller/full node role/authority rejected; selected closed gate; provided node assertion checks retained |
| O15/O16 | Other node progress while Runner wait, same-node startup contention, update inhibited by durable intent; vanished/orphan/new-boot/terminal-replace markers and namespace durability failures |
| O17/O18 | Real worker wrapper lock serialization; exact stop/mask/attempt guards; no/expired owner cannot publish gate or clean; selected service.env gate |
| LI01–LI04 | Two process-only roles no full observer/invented identity; invalid role/updateNone; provided schema/role/processboot mismatch and bad actual observation before journal |
| LI05–LI07 | Actual final drift inhibits ready; caller dict mutation cannot change snapshot; wholeNone/rebinding rejected, immutable snapshot/exact repeat |
| LI08–LI10 | CLI None protected-role mismatch; actual stopped proof before mask removal/running probe; changed process generation denied + shared O-controls |

Это finite synthetic coverage в trusted cooperative Python boundary; не proof всех possible crashes/interleavings. Direct None остаётся process-only assertion. Applicable CLI authority — protected role+observed process boot при omitted expected; explicit full binding обязателен whole/update/startup routes. Никакого automatic full-node/Slurm precondition для сохранённого standalone CLI не вводилось.

## Historical attempts и residuals

Семь calls сохранены как отдельные originals: RED1, RED2, GREEN1(198pass36failed methods), DIAG1(3failed), GREEN2(harness race interrupt), GREEN3(wall stop), GREEN4(current complete234pass). Counter/budget не сбрасывались; last packet был отдельно bound finite extension, не autonomous rerun loop. Прежние reports/raw не менялись. Planning110–140s было uncertain estimate; measured94.294s относится к этому packet, не universal bound/performance guarantee.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Reviewed cooperative Python owner code готов к scoped source/G1 gate | Exact source/D/R + complete234-method runtime gate | Coordinator/Git integration separate | сохранить |
| R1–R5 закрыты в named scope | Exact repair + preserved negative/positive fixtures, GREEN4 | Native behavior не измерен | сохранить |
| Universal OS/bootstrap/systemd writer closure готова | Нет такого evidence | OPS03-FOLLOWON-PROVISIONING остаётся required follow-on | данных недостаточно |
| prepare-initial privileged protected-role gap устранён | Он не менялся этим repair | Cold-controller gate contract tested; protected-role follow-on не waived | данных недостаточно |
| CR04 effective atomic job-admission crash protocol полностью закрыт | Owner/intent guards не заменяют общий reader commit protocol | Raw gate-open crash residual сохранился | данных недостаточно |
| Native/CP-OPS/finalCI/scientific/full release готовы | Только local selected engineering fixtures | Отдельные target/source/admission/native/science gates открыты | данных недостаточно |

Reviewer не выполнял tests/helper/project imports/build/Git/native/SSH/server и не менял owning files. Выполнены read-only hashes/source/receipt/raw nodeid+duration inspection и этот **новый** /tmp report. После exact independent PASS STOP; дальнейшего rerun не предлагается.
