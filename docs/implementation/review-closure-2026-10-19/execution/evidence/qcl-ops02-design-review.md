# OPS02 independent CP-DESIGN

**Вердикт: PASS для ограниченной OPS03 implementation перечисленных cooperative application entrypoints.** API, state machine и routing достаточно определены для medium writer. Universal OS/provisioning single-writer acceptance и effective-closed job admission при каждом final-gate crash этим PASS не установлены. Два остатка сохранены ниже.

Candidate `/tmp/qcl-ops02-design.md`: SHA256 `26374bcfb194aa5c9701bd00ceaae6016cd535dcc722e8b221719fec72450030`,565 lines — проверен и прочитан полностью. Собственный source-first вывод отправлен root до получения candidate. Platform `6c5b11f3c74d44fed8b2c159f890b83e0b5456b9`, clean; все пять source/test hashes автора совпали с actual bytes. Root eb59809 у автора — историческое наблюдение; current04eecba не меняет owning Platform packet.

Прочитаны root AGENTS/architecture, Platform README/CONTRIBUTING (component AGENTS отсутствует), OPS02/03/P1, original RV06/fixcard/RV12/RV15, actual release/worker lifecycle, relevant tests и Nix/bootstrap publishers. Imports/tests/SSH/Nix/server/native/solver/product edits:0.

## Source-first basis

Actual `application_release.py:682–708` guard/delivery.lock, `deliver_cli:1971–2000`, final branch `main` с activation.lock и `_deliver_cli_locked::deliver` с controller SSH подтверждают competing route и self-deadlock риск. Public prepare_initial918/activate984 сами common owner не приобретали. Shutdown232–309 отделяет capture/finalize от Runner wait; startup373–529 держит common lock, но не тот же per-node lock. Их durable intent нельзя заменить освобождённым flock.

Activation пишет app/solver profiles, registration/Code allowlist, service.env, release ready:false/true и управляет units. `publish:781–814` делает file/dir fsync, но общей multi-file transaction нет. `guard:1071–1083` читает ready+shared gate, а не controller intent. Existing gate-open fsync/terminal failure fixture508 допускает raw open при failed close. Nix initial-profile service и bootstrap/register_aiida publishers находятся вне Python lifecycle routing. Согласие с author observations не является native или научным доказательством.

## Принятый контракт

1. **Opaque capability.** Private registry держит strong object identity; проверяются exact type, PID/start ticks/boot, runtime/lock fd и pathname dev/inode, full manifest identity, closed operation и original deadline. Copy/pickle/dict/UUID/PID не создают authority. Trusted Python boundary явно не является sandbox против malicious code в root interpreter.
2. **Lifetime/namespace.** No-follow/nonblocking/CLOEXEC fd-relative lock, regular single-link file, без truncate/unlink/replace; inode recheck перед mutation. Revocation до fd close. Fork child очищает registry и закрывает inherited fd без LOCK_UN shared open-file-description parent. PID check остаётся дополнительным барьером.
3. **Routing.** Owner берёт delivery.lock, затем nonblocking activation.lock fence. При contention второго первый освобождается без application mutation. Controller parent вызывает private `_activate_owned` с тем же object, без второго flock, mutating self SSH и self Nix copy. Enrollment и local/remote identity проверки сохраняются. Worker получает собственный local owner; attempt locator не переносит capability.
4. **Public boundary.** Existing CLI/API names и keywords сохраняются; public wrappers получают finite deadline и сами acquire/guard. Direct API теперь требует selected closed gate, как ранее CLI. Returning-worker не bypass. Stop/repair/finish входят в node-local serialization без ослабления enrollment, physical-stop и mask-origin checks. Read-only calls не дают writer authority.
5. **Migration.** Dual-lock fence защищает от старого standalone CLI и delivery writer; старый lock не очищает unknown. Exact capabilities v2 на всех nodes проверяются до gate/quiesce. Старый v1 parent тоже отвергает новый ответ. Это coordinated rollout dependency, а не transparent mixed-version compatibility; fence снимается только по отдельному доказанному rollout contract.
6. **Unknown/journal.** Self-exclusion разрешено только для exact registered own current artifact при совпадении schema/inode/attempt/release/runtime. Foreign, orphan, malformed, requires_reconciliation, cluster-update и mismatched normal/update markers остаются блокирующими. Standalone durable exclusive intent0600 с file/dir fsync предшествует первой application mutation. Original bounded bytes сохраняются, а не только hashes. Public deliver_pool без внешнего checkpoint сам создаёт journal. Pending local mutation охватывает filesystem writes helper, не только external commands.
7. **Publishers/deadlines.** Таблица§6 охватывает ready invalidation, оба GC roots, registration/allowlist, env с переданным gate, unit start, ready:true, shared gate и own terminal cleanup. Callback проверяет owner/deadline до write/replace/fsync/unlink, включая UID-switch route. Generic publish не объявлен universal writer guard. Потеря ответа child остаётся unknown; retained pending блокирует следующую mutation. Identical completed release ремонтирует только повреждённый GC root с сохранением Code UUID; orphan требует reconciliation.
8. **Normal lifecycle.** Fixed order per-node→common для startup/shutdown; capture/finalize краткие, Runner pause/verify идут вне common owner при durable intent. Startup сохраняет common owner между health и RESUME, независимый marker появляется до RESUME. Vanished job без verify-stop, legacy incomplete boot или unknown event не становятся safe/resumed. Per-poll deadline не сбрасывается вложенными helper.

## Controls и scope

O01–O18 дают нужный denominator: два процесса и reverse contention; actual local helper/temp publishers с независимым mutation ledger; отсутствие reacquire/self SSH; forged/stale/fork/inode/deadline rejection до mutation; phase/final-publication cuts; legacy fences/protocol; GC-root/Code repair; cold gate; forged authority; concurrent normal wait/update; exact worker attempt/mask race. Для child заданы Event/pipe handshake, watchdog≤5s и cleanup; sleep-only absence не считается доказательством. Fake commands закрыты allowlist.

OPS03 меняет только два ops-файла, три test-файла и accepted owning document. Modules/bootstrap не входят. Максимум четыре будущих Python invocations в централизованном L envelope, без installs/full build/native. Counters при repair не сбрасываются; unexplained deadlock возвращается D. Tests здесь не запускались; synthetic evidence позже не заменяет NFS/power-loss/Slurm/native или scientific acceptance.

## Два остатка — не waiver

**1. OS/provisioning writers.** Принимаю scoped OPS03 с обязательным residual `OPS03-FOLLOWON-PROVISIONING` из§1. `modules/release.nix` initial-profile service и `modules/application.nix` bootstrap/register routes не охвачены. До native application-only mutation нужны phase-long inhibition/exclusive OS window и bound unit/config/boot/service-dependency proof; одного is-active snapshot недостаточно. Unconditional source single-writer claim требует owning follow-on D с privilege/Requires/RemainAfterExit/bootstrap ordering и contention/deadlock controls. Внутренний compatible D не требует повторного human grant, но исходное требование пока не закрыто. Full release не наследует universal PASS от OPS03.

**2. Final admission commit/read.** После authorized open replace crash до terminal fsync/close может оставить raw gate open. CR04 intent блокирует blind writer retry, однако job guard этого intent не читает. Поэтому effective job admission closed не доказано. O08 проверяет local activation cuts до authorized open; O09 — existing closed/unknown outcomes. Сильное «crash never opens» свойство требует отдельного owning atomic admission commit/read D со всеми consumers и native failure proof. Сохранить unresolved dependency в coverage/final gates; не переименовывать unknown в pass и не вводить неявно distributed protocol в OPS03.

Это границы результата, будущие owning задачи и phase predicates, а не operator waiver, hidden workaround или отказ от required criteria/backend. Поддержанный routing можно реализовать сейчас; production readiness и full source/native release acceptance требуют остальных обязательных gates.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Scoped entrypoints имеют один owner без self-deadlock | Capability/dual-lock/private-helper contract; future O01–O07/O11/O17 | Design-only, tests0 | изменить |
| Unknown/dead parent не становятся authority | Durable intent/receipt и migration rules | Flock не доказывает stop remote effect | сохранить |
| Runner wait не удерживает common owner | Short capture/finalize и per-node order; O15–16 | Native Runner/Slurm не исполнялись | сохранить |
| OPS03 medium implementation ready | Exact API/state/publisher/failure contract принят | Narrow closure; CP-CODE впереди | сохранить |
| Universal OS writer closure/final crash-closed admission доказаны | Source counterexamples и explicit residual D | Required follow-on gates остаются unknown | данных недостаточно |
| Native/scientific/full release приняты | Соответствующих receipts нет | Source/design-only | данных недостаточно |
