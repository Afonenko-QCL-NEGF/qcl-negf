# OPS03 candidate2 — independent CP-CODE review

**Вердикт: CHANGES_REQUESTED / CP-CODE не закрыт.** Source inspection подтверждает основные owner/B binding mechanisms, но healthy whole-update/O03 route не продемонстрирован: actual GREEN1 имеет 36 failed methods / 198 passed. Причина healthy routing failure из сохранённого assertion-only вывода не установлена; production fix по догадке не предлагается. Ни source PASS, ни native readiness этим отчётом не выдаются.

## Immutable scope и evidence

Platform baseline 6c5b11f3c74d44fed8b2c159f890b83e0b5456b9. До author report прочитаны actual owning source и assertions; затем принятые OPS02/B contracts и root runtime log. Accepted D: OPS02 26374bcfb194aa5c9701bd00ceaae6016cd535dcc722e8b221719fec72450030; narrow B c673a2b11df3be0096388b0280cc4714271be90c9dc11e11c409a59b25f4bfee. Coordinator подтвердил: applicable authority по entrypoint, не новый обязательный full-node/Slurm probe для сохранённого standalone CLI.

Самостоятельно пересчитанные SHA-256 actual/frozen:

| Input | SHA-256 |
| --- | --- |
| /tmp/qcl-ops03-candidate2.patch, 176933 B | 3481c9cdf4e5910845a1e79169eb0749dd525fd03256f8aaf2dd6630c2dde648 |
| ops/application_release.py | 08f67097705f86d2ca842ae373306cb8945f47564c4d2ceb5e00e8272f31831f |
| ops/worker_lifecycle.py | b81c722ce9cbca8a5adfed24063de268e39ea0d012ae120bb11d9491ba2a0678 |
| tests/test_application_release.py | 1ad1908d49a396299739819a3d8c25da5272626be0fe19702906b459e5c06025 |
| tests/test_worker_lifecycle.py | 7d8fd49aac1b3eb4527ef185e9bf3a2cfcd7a3265e92a447954ae4e2bef15a2b |
| tests/test_worker_shutdown_intent.py | 53017ecb166b5624dab6fe3d2b57498bdbf37882a83a9be0c9c7668fdc95bfa3 |
| author candidate2 report | 2d0300560299c0aeddaec32f76492e5409534f1e7fbcf67c640e9b77128f608d |
| GREEN1 receipt | 7d750f0db40d1a314d048dbf9d644791ade8c86efcfa521b24b0633b3dcd3781 |
| GREEN1 original.log, 69551 B | 09cd958d38b6b2306dbacb7abac5df000fdf98ddde694106cca29f2f3bbad8c1 |

Five selected file hashes совпадают с root receipt; actual source остался frozen после GREEN. Full patch имеет четыре changed paths: две ops + application/shutdown tests; третий selected lifecycle test unchanged. Runtime witness — root packet, не reviewer rerun: три selected files, pytest exit1, 198 passed/36 failed methods, wall53.093s, sampled RSS102707200 B, owned TMP1040813 B, raw complete, no stop/guard error/overrun. Failed methods — denominator методов pytest, не число unique product defects; inherited I14SlurmInfinity повторяет ряд I14WholeRepair controls.

## Подтверждённые blocking findings / correction contract

### R1 — Healthy whole/local routing gate остаётся unresolved

Locators: tests/test_application_release.py:3617 (`OPS03WholeRoutingTests.test_o03_whole_update_calls_real_local_helper_without_self_ssh_or_reacquire`), :1530/:2385 и inherited healthy I14 tests; raw log около :399–440, :450–495 и :943–975. Expected completed/open, actual failed/False. Это обязательный accepted OPS02 O03 positive gate; standalone binder successes его не заменяют. Several negative failures также не достигают intended phase (например :533 registration-effect assertion, :1546 health-query assertion, :1640 post-restart query denominator).

Из raw нельзя вывести actual caught reason: `_deliver_pool_owned`/whole route возвращает per-node failure вместо выброса, а assertion не печатает result/receipt. **Cheapest distinct check**: сохранить все semantic assertions, добавить bounded diagnostic message на healthy result assertion (result status/nodes reason/phase + relevant receipt pending fields и command names), затем coordinator может выполнить один отдельно bound finite diagnostic packet. Не менять product/validators для получения green до actual reason. Сохранять original GREEN1 и source/counter identity. Это evidence blocker; здесь не утверждается конкретный production root cause.

### R2 — Budget fixtures используют stale 32 MiB вместо actual CAP

Locators: production `UpdateScan.CAP` :1679 =64*1024*1024 (эта константа не менялась данным patch); tests :2316–2319 (`test_f5_read_reservation_precedes_access_and_sentinel`) и :2653 cap_manifest в `test_r4_actual_main_update_budget_routes`, дважды через inheritance. Установка scan.bytes=32MiB−16 не достигает 64MiB cap, поэтому actual IO/parse разрешён корректным резервированием; F5 raw явно показывает IO happened, R4 не получает ожидаемый refusal.

Correction: derive exact exhaustion из `UpdateScan.CAP`, оставляя independent oracle «резервирование отказывает ДО access» и исходные no-IO assertions. Не уменьшать production cap, не убирать sentinel/control, не считать failing fixture доказательством product overrun. R4 raw не маркирует subcase; cap_manifest defect подтверждён source-wise, другие subcases не объявляются проверенными только по этому объяснению.

### R3 — UID fixture несовместим с новым truthful namespace ownership predicate

Locator test :703–741 (`test_root_squashed_shared_gate_is_read_as_scientific_owner_without_relaxing_guards`); raw :240–391. Test подменяет geteuid→0, но actual temp runtime st_uid остаётся invoking user. `lifecycle_owner` :827–829 корректно отказывает до NFS read. Это fixture identity mismatch, не свидетельство отказа root_squash read policy.

Correction: согласовать fake credential/stat ownership только на нужной controlled boundary, сохранив real owner acquisition/fstat/stat/inode semantics и NFS UID3000 assertions/restoration. Не ослаблять runtime ownership validation и не bypass owner. Проверка должна действительно дойти до intended shared-gate branch.

### R4 — Independent malformed cases / old blind retry используют один уже inhibited runtime

Locators :1249–1255 (`test_malformed_remote_identity_is_reported_per_node`), :1186–1205 (`test_partial_fleet_delivery_closes_admission_until_every_selected_node_verifies`), wrappers :299–304; production :934–1010/:1540–1557. После first failed direct deliver_pool pending lifecycle intent специально сохраняется, согласно accepted D. Следующий malformed subcase либо прежний same-runtime retry теперь correctly rejected guard на :619; raw :105–196.

Correction: independent cases получают independent runtime/gate/context. Same unknown attempt обязан проверять refusal и unchanged original blocker; healthy case на свежем runtime не выдаётся за retry/reconciliation того же unknown. Не очищать intent в fixture перед «retry» для apparent pass и не менять product для принятия unknown. Если нужен новый known-failure retry контракт, это D decision, а не mechanical expectation update.

### R5 — Some migrated assertions/fault seams по-прежнему описывают старый remote-controller route

Locators :449–465 malformed remote check ожидает worker not_attempted, но первая реальная remote check теперь worker (controller local helper/check), raw :86–103; :976–984 redirected publish fixture пишет другой gate, чем actual helper проверяет по `gate=self.gate`. Эти tests обязаны адресовать текущую supported path, сохраняя различающий смысл.

Correction: malformed remote envelope inject на фактическом selected remote worker с проверяемым later selected node/control, чтобы unknown действительно останавливал дальнейшую mutation. Negative target injection должен быть достигнут и отмечен; нельзя заменить expected status на любой failed. Gate fixture должна использовать один explicit selected target на publication+helper/readback либо отдельно проверять mismatch refusal, а не silently redirect publication. Остальные final-publication failures пока не классифицированы отдельно от R1: raw показывает, что admission-intent phase не достигнута; их safeguards нельзя удалять/объявлять pass.

## Source inspection: что найдено реализованным, без общего PASS

- :714–864 opaque registry identity/strong reference; exact runtime/release/operation/process PID/start/boot, original-or-shorter deadline; fstat+path inode; two nonblocking locks in common→legacy order без truncation; exit revokes перед close; fork clears registry/closes descriptors без LOCK_UN. Tests O01/reverse/O04–07/11 используют real flock/fork/FS и guarded command fakes. Проверены bounded handshakes, not sleep-only success oracle.
- :865–1010 exclusive intent before mutation, bounded original bytes/base64/hashes and profile links, receipt ownership by inode+bytes, terminal receipt перед last-fallible own intent unlink. Guards не принимают одинаковые fields/UUID вместо live registration; orphan/lookalike/replaced marker controls присутствуют. Crash cuts O08 используют actual publishers и SIGKILL; O09 syscall matrix сохраняет inhibition. Durability не эквивалентна power-loss/native/NFS proof.
- :1367–1507 narrow B binder копирует flat identity в MappingProxyType, проверяет role/actual process boot, фиксирует full-or-None один раз; whole_update и worker update None rejected; provided observer/stopped proof до journal/mask removal; final checks используют snapshot. LI01–10 assertions nonvacuous: no observer for process-only, mismatch pre-journal unchanged bytes, final drift vs caller-dict mutation отдельно, explicit stopped proof до running observer. CLI protected role remains, no new flags; None не переносит CP-OPS.
- Controller callback :2778–2803 использует parent live owner без mutating self SSH/copy; full controller authority rechecks сохранены; workers имеют explicit expected/attempt и fresh remote owner. Candidate capability marker требует new lifecycle protocol, не принимает legacy worker как compatible.
- Worker lifecycle :239–355 common capture/finalize separated by Runner wait под per-node lock; same-node startup uses same lock :404–413, other-node progress + durable inhibit проверяется :130–220 shutdown tests. Startup snapshot reread под common owner, returning intent и independent pre-RESUME marker, owner preserved до terminal cleanup. Poll deadline не renews после preflight.

## Исправление предварительного UID замечания

В раннем сообщении предполагался production runtime0700. Это **неверно для installed namespace**: modules/release.nix:72–73 задаёт root0755 ADMIN_STATE/runtime. Поэтому root→qcl-negf gate publication с callback `_require_owner` не доказана broken по directory traversal; preliminary default-route blocker отозван. Newly-created/custom0700 root-owned runtime + scientific-UID callback имеет иную permission precondition и не проверен native. Root_squash failure в GREEN1 фактически происходит раньше на fake geteuid/stat mismatch (R3). Это различие сохраняется, native readiness не заявлена.

## Limits / решение

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Основные owner/B механизмы представлены | Exact source locators и real control assertions | Не заменяет failed whole positive gate | сохранить |
| 36 failed methods означают 36 production bugs | Raw не поддерживает такую классификацию; inherited/fixture defects выделены | Healthy routing reason неизвестен | данных недостаточно |
| CP-CODE candidate2 готов | GREEN1 exit1, O03/healthy route failed | R1–R5 должны разрешиться без weakening assertions | изменить |
| Native OS/bootstrap/whole-system writer closure достигнута | Нет такого evidence | OPS03-FOLLOWON-PROVISIONING, prepare role gap и CR04 atomic effective admission residual не waived | данных недостаточно |
| Scientific/full CI/release acceptance | Не проверялись | Synthetic local engineering scope только | данных недостаточно |

Reviewer не исполнял tests/helpers/imports/build/native/SSH/Nix/services и не изменял source/Git. Выполнены чтение, SHA inspection, ограниченное чтение root original log/receipt и запись только этого /tmp report. Дальнейший source pass STOP до resolved healthy routing diagnosis и exact reviewed correction.
