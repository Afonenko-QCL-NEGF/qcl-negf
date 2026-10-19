# DEV12 independent CP-DESIGN — round1

**Вердикт: CHANGES_REQUESTED; DEV13 implementation NOT_READY до narrow correction R1.** Actor unknown-effect/ownership/admission architecture в целом согласуется с первичными inputs. Единственный blocking gap ниже — bounded ExportStore.close при existing filesystem I/O под store lock. Source-only review; tests/import/build/SSH/solver/product edits отсутствуют.

## Immutable object и независимость

Candidate `/tmp/qcl-dev12-design.md`: SHA256 `b07b0d406a6948da62c7486d0e4138a00bbb910bce6aab4343201be041f3d5b4`,537lines46241B — hash проверен. Author design прочитан после собственного source-first вывода, ранее отправленного coordinator.

Actual Portal `6ff9f6100623c578028506d43a39972dbfbc00dc`, clean; actor-facing source равен ранее reviewed36837e9+DEV11 diff775fd774. AiiDA `5579d55684939495230241f446b7ea07c8ae0224`. Candidate rooteb59809/Portal36837+frozenDEV11 — исторический author observation, не current release freeze; related method bytes совпадают. Прочитаны primary RV05/RV12, exact DEV12/13 task, current service/api/exports/settings и relevant AiiDA submit/store/cancel/artifact source; existing finite disconnect fixture прочитан, не запущен. Не восстанавливались stale drafts и не запускался backend.

## R1 — blocking bounded-close gap

Candidate§10 требует bounded `ExportStore.close(deadline=D)`, сначала устанавливая stopping/cancel **под store lock**, общий lifespan deadline и отсутствие filesystem cleanup в HTTP/lifespan потоке. Но одновременно preservation existing storage/cleanup guards не определяет необходимое изменение этих actual paths:

- `src/qcl_negf_api/exports.py:67–77::_storage`: `with self._lock` включает `shutil.disk_usage(self._root).free` на74;
- `exports.py:50–56::_cleanup`: `shutil.rmtree` на55;
- `_cleanup` вызывается под тем же RLock в `get:79–85` и `create:154–155`.

Reproducible source scenario: worker или другой request удерживает store RLock в stalled disk_usage/rmtree; lifespan вызывает close с конечным D. Простой `with self._lock` для установки stopping блокируется до завершения чужого filesystem I/O. Caller не может вернуть truthful stopping за remaining budget и передать actor.close тот же общийD. Это не arbitrary actor-backend termination problem и не просьба force-kill thread; это фактическое unbounded lock admission перед выбранным close wait. Исключение direct local-file streaming из io bound§9 эту metadata-lock блокировку не закрывает.

**Cheapest design correction:** явно применить short metadata-lock/no-blocking-I/O invariant к ExportStore, а не только actor mailbox. Назвать все three source paths и определить, как filesystem stat/delete/finalization выполняются вне store lock и вне caller/lifespan path при сохранении reservation/readers/TTL/once-only state. Expired entries можно metadata-mark/coalesce и cleanup существующим preparation/finalizer executor; precise seam выбирает author, без unbounded helper queue/new thread-per-cleanup. Альтернатива — finite deadline-aware store-lock admission с exact truthful pending/count semantics и retained finalization. Одного «caller wait timeout» после уже blocking lock недостаточно.

Acceptance дополнить Event-gated filesystem/storage/expiration stall при удерживаемом existing path: caller close возвращает stopping при release unset в shared injectedD; no directory deletion while reader/worker active; release даёт один cleanup и completed, actor close still requested даже при store close error/timeout. Fake FS/Events, no real NFS/server. Implementation разрешать только после того, как author назовёт выбранное поведение, не оставляя medium новый interface/architecture choice.

## Required fixture reconciliation — не второй product blocker

Current `tests/test_stream_disconnect.py:45–57` использует pre-DEV11 SimpleNamespace без `get_export_selection` и `list_execution_artifacts`, а `get_export_plan` не принимает selectors. Export-kind branch на90 теперь вызывает новый consumer create и не дойдёт до actual lease assertions. Это source observation, не выполненный failing test.

DEV13 permitted paths включают этот fixture. Design/implementation должны явно обновить fake producer interfaces по accepted DEV09 exact-child contract, сохранить ASGI2.3/2.4×artifact/export denominator, retained response против GC, actual closed/readers0 assertions и добавить stalled-owner case. Нельзя просто исключить export cells, заменить create stubbed-ready entry без проверки тех же lifecycle invariants или объявить старый control passed по прежнему runtime receipt. DEV11 scoped CP-CODE не заявлял full suite/этот stream packet executed.

## Принятые части и implementation guardrails

- Single owner `_owner_main`/one executor, bounded mailbox, atomic queued→running boundary, no backend calls under actor metadata lock — подходящий минимальный design. Deadline — caller response, не backend cancellation. Queued/not_started и running/unknown различены; late completion не переписывает response. Pending expiration drain и cleanup flags не создают скрытую unbounded executor queue.
- All3mutation operations перечислены верно: submit_plan AiiDA407 может создать workflow до return, save_agent_report490 stores до receipt, kill_run559 теряет confirmation. Conservative unknown при любом dispatched mutation exception обоснован: exception class не доказывает effect-phase. HTTP-side validation остаётся known before actor. Read errors сохраняют existing category.
- Persistent process-local mutation fence, no auto retry/reset endpoint/TTL; late returned exactUUID фиксируется, но latch автоматически не снимается. Нет durable cross-crash idempotency; restart не substitute reconciliation. Lost response без operationUUID/runUUID остаётся unknown, hash/label/list absence не proof. Новая скрытая scheduler/SCI recovery не разрешена.
- Exact operation/type/code/settings tables достаточно конкретны. Новые30/30/15/10s defaults/capacity16/8 и upper guards явно operational decisions, не измеренный SLO/physics thresholds. Queue budget не reset при dequeue; scheduling caveat честный. Existing AiiDA kill10s не трактуется как native stop witness.
- Owner-only context enter/read/seek/exit, reservation before enter, late-open registry-before-publication, poisoned reader after unknown offset, idempotent cleanup admitted независимо от mailbox capacity и single exit **attempt** — соответствуют source risks. Failed exit не handle-closed; owner guard нельзя освободить после merely timed-out init/cleanup.
- Actor close completed требует actual lease exits/unload/asyncgen/loop cleanup; repeatedclose idempotent; no bounded process-exit claim поверх ThreadPoolExecutor. Shared lifespanD/export then actor finally — принят после исправления R1.
- HTTP scalar string detail+fixed diagnostic headers сохраняют frontend compatibility; actor-specific mapper перед genericRuntimeError обязателен также для export selection/agent-report paths. Unknown suffix/headers не удалять sanitizer; streaming after sent headers abort/log, не synthetic JSON/полный download. Process/scientific state не переопределяется.
- Diagnostic event logging не должно добавлять unbounded caller I/O на пути finite response; сохранить short metadata critical sections и выполнять потенциально blocking logging вне response-critical wait/admission либо через already bounded owner path. Это implementation guardrail, не требование нового logger subsystem.
- Full guard/source acceptance остаётся отдельным DEV13 CP-CODE с Event/real-monotonic/order witnesses и finally release/bounded joins. Fake clock alone, sleep-only order или hung fixture без external cap не proof responsiveness.

## Проверочный итог

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Actor caller deadline/effect certainty различены | Candidate§3–8, current Future/backend mutation boundaries | Source/design, no runtime | сохранить |
| Owner/late handle cleanup truthful | Candidate§6/9/10 и current single-owner paths | Backend может остаться blocked; no process-exit guarantee | сохранить |
| Export close всегда имеет finite caller wait | Candidate§10 vs current lock-protected disk_usage/rmtree | R1 leaves initial lock wait unbounded | изменить |
| Existing disconnect controls можно считать сохранёнными | Current fixture source45–57 | Old fake incompatible с DEV11; не запускался | изменить fixture в DEV13 |
| DEV13 medium готов без нового design выбора | Почти полный contract, one missing store-lock seam | CP-DESIGN CHANGES_REQUESTED | данных недостаточно |
| Native/scientific/full release приёмка установлена | Соответствующих receipts нет | Software design-only | данных недостаточно |
