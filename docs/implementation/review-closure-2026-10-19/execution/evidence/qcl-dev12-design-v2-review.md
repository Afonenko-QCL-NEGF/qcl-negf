# DEV12 independent CP-DESIGN — round2 narrow re-review

**Вердикт: PASS / ready_implementation exact v2 contract. R1 ADDRESSED на уровне design.** Это не runtime fix/DEV13 CP-CODE. Новых blocking gaps в R1 correction и fixture reconciliation не обнаружено; ранее принятые actor state/settings/HTTP/unknown/fence/owner rules сохраняются.

Candidate `/tmp/qcl-dev12-design-v2.md` SHA256 `fa3ca630f7b44ef9d72582ff91ced2e0c671f0986cecb4e20cddf5b294255712`,739lines64164B — hash проверен. Полный old→v2 textual diff прочитан;207 added lines, основной новый §10.1 и acceptance controls. Original candidate и saved round1 оба по-прежнему SHA256 `b07b0d406a6948da62c7486d0e4138a00bbb910bce6aab4343201be041f3d5b4`; original reviewer CHANGES_REQUESTED receipt сохранён SHA256 `325eb95b13fe77c2b8bba37ee49965dfd6b9b4750731f53810aea11eb625e9a3`. Portal current `6ff9f6100623c578028506d43a39972dbfbc00dc`, clean. Source/operation boundaries round1 применимы. Reviewer не выполнял imports/tests/build/solver/SSH/source edits.

## Blocking R1 closure

Выбран exact deadline-aware admission вариант, не подразумеваемый prompt store-lock acquisition:

- §10/10.1 independent short lifecycle lock/Condition и stop latch устанавливаются до store RLock. Локальные lifecycle critical sections не включают store acquire/filesystem/backend/logger/Future wait/shutdown. Порядок двух lock только store→lifecycle; close lifecycle отпускает до timed store acquire. Это устраняет actual storage-disk_usage lock wait на пути установки stopping.
- Close algorithm0–5 чётко делит latch/cancel/coalesced request, timed optional snapshot и remainingD wait. При занятом store lock оба counts=None с store_metadata_pending; None не ноль. Actor/reader counts остаются exact integers, только export snapshot nullable. Completed требует worker-confirmed cleanup и0/0. Исчерпанный D всё равно ставит stop/request, actor.close получает тот жеD через lifespan finally.
- Existing disk_usage может оставаться под store RLock для storage serialization; ordinary filesystem caller responsiveness не обещается. Именно lifecycle response обходит эту блокировку. Не заявлен hard OS I/O/thread/process termination.
- TTL `_cleanup` становится metadata-only delete_pending marking, without rmtree/stat/disk_usage. Post-lock scheduling в finally get/create сохраняет requests при404/cachehit/refusal. Reservations/128-limit удерживаются до verified deletion; internalflags не public. Новые leases после stop/claim запрещаются atomically; late create повторно проверяет latch/maintenance перед publication.
- Maintenance максимум1scheduled/running Future на existing single preparation executor, плюс максимум1prep; repeated requests coalesce dirty flag, без нового thread/task-per-entry или unbounded helperqueue. Race close-before-prep-submit явно разобран через зарегистрированную preparation Future под store lock и maintenance cancellation этого unstarted Future. Required maintenance не попадает под cancel_futures.
- Worker claims directory под store lock после readers0/no writer, releases locks до rmtree. Cleanup failures не ignore_errors-success: reservation retained, terminalfailed, no identical automatic retry или косвенный root deletion того же failedclaim. Root cleanup once после worker/readers completion, retained object/root и clear-before-check/set-after-decrement Event предотвращают lost wakeup. Filesystem cleanup больше не HTTP/lifespan operation.
- Diagnostics finite-response path не делает synchronous logging I/O; это закрывает прежний implementation guardrail. Any Future.cancel/done callbacks в DEV13 также обязаны соблюдать тот же explicit no reverse-lock/no I/O lifecycle invariant; eager callbacks нельзя выполнять под lock, если они могут получить store lock.

Эта correction достаточно конкретна для medium implementation: новая seam/result-nullability/maintenance bounds и error behavior выбраны author, не оставлены implementer для нового architecture выбора.

## Acceptance и finite controls

§12 теперь содержит отдельные Event-gated stalls `_storage` и create admission с independently witnessed occupied old store lock; close возвращает stopping/None при release unset, reservations/files retained. TTL-rmtree stall подтверждает worker/no-lock execution и coalescedFuture<=1; separate readerrelease, single directory/root claims, cleanup-error failed/no retry и lifespan actor-close sameD проверяются отдельно. Real monotonic/order witnesses, finally release и bounded helperjoins сохранены. Это proposed tests, runtime0.

Current test_stream_disconnect.py45–57 incompatibility с DEV11 явно зафиксирована. New fake должен предоставить exact4field selection, exact selected inventory rows, plan selector kwargs и existing selected opens. Real create→prepare synthetic-exporter lifecycle сохраняется, ready entry вручную не подменяется. **Все4 ASGI2.3/2.4×artifact/export cells** сохраняют retainedresponse/nonempty65536chunk/one-response/readerclosed-or-readers0 assertions; stalled actor case добавляется, не заменяет controls. Source-only finding не назван observed runtime failure.

## Boundaries и remaining gates

Actor mutation unknown/fence, not_started lock/start boundary, owner-only cleanup/init guard, exact types/settings/HTTP mapping и no cross-crash exactly-once claim из accepted portions round1 не изменены. Per-operation caller deadline не становится научным threshold или full HTTP/filesystem/process-exit SLO. `CloseResult` nullable counts — авторизованное v2 interface change, не скрытая implementation relaxation.

Следующий writer обязан сохранить exact DEV11 child/cache/status/bytes/native capabilities, admission/spool/reserve/tail checks и retained original failure receipts. DEV12 owning doc/README delta затем проходит CP-CODE; DEV13 code/fault fixtures — отдельная task с finite centrally bound runtime budget. Source design success не означает load-bearing fault tests прошли или что любой native AiiDA/NFS/backend завершится вD. Нет разрешения на force owner/thread kill, scheduler cancellation, service restart как reconciliation substitute, solver/fullCI.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Initial store-lock wait больше не разрушает close callerD | §10.1 separate latch/timed snapshot/nullablecounts/remainingbudget | Actual implementation ещё нет | сохранить |
| Retained writer/reader files/accounting и once-only cleanup определены | Coalesced existing-worker seam, lockorder/claim/error rules | OS I/O может остаться blocked | сохранить |
| Existing ASGI fixture reconciliation определено полностью | Exact producer fake +all4cells+independent stalledcase | Tests не запускались | сохранить |
| DEV12 design готов medium implementation | Independent R1 re-review без blocking gaps | CP-CODE/DEV13 fault execution впереди | сохранить |
| Runtime/native/scientific/fullrelease accepted | Соответствующих receipts нет | Design-only | данных недостаточно |
