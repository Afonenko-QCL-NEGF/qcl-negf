# DEV13 GREEN2 — independent re-review

**Вердикт: CHANGES_REQUESTED, R4.** Прежние R1–R3 исправлены на уровне source; текущий frozen implementation содержит отдельную гонку queued reader operation / reader close. Runtime GREEN2 ещё не представлен. Reviewer не выполнял target imports/tests/build/server/threads/solver и не менял owning source.

## Exact packet и свидетельства

- Portal HEAD `fa80b5b5920dc16dfb911d164939b3d23e6be186`.
- `/tmp/qcl-dev13-green2.diff` SHA256 `a5c983044897460ba614bca6a79356047ff050171617335a47ef1fb1c097b6f0`,94,863B. Независимая реконструкция current tracked diff + untracked test diff byte-equal.
- Сначала прочитаны actual source delta, surrounding lifecycle/dispatch paths и новые assertions; затем author report SHA256 `6b194cc0c5ac14e3c1a69de2cde120132ccdb41d2aef63b297fa1b934cd717d6`.
- `service.py` SHA256 `397e3c4c98136cd34446f38e332bcb088c9cbe360be69bebec5874353b6a6e24`; `test_actor_deadlines.py` `a590bbef178e2ac4fd74c85b2523e15c78bc93c1880ad4429707e80aad4c47fc`. api/exports/settings hashes совпадают с GREEN1 и author report, production delta после RED2 ограничен service.py.
- Root RED2 receipt/raw прочитаны: exit1,9failed/24passed, wall3.189s, sampledRSS72,085,504B, log31,341B, stopnone. Raw summary имеет ровно R1 six/R2 two/R3 one expected failures. Это synthetic semantic RED прежнего implementation; не current GREEN и не native proof. RED2 receipt не содержит source/test hash manifest, поэтому неизменность tests относительно RED2 дополнительно опирается на root witness и author frozen hash; current hashes reviewer проверил самостоятельно.
- `git diff --check` exit0. Все9 original ASGI assertions присутствуют; baseline decorators unchanged, сохраняются4 finite cells. Test-only correction новых2 stalled cells допускает exact ActorDeadline(operation_deadline,unknown) после headers, не fake success/full body. Это соответствует accepted post-header abort boundary.

## R1–R3: ADDRESSED static

1. **Queued mutation fence:** service535–539 проверяет `_mutation_receipt` под тем же metadata lock непосредственно до queued→running. Refused M получает expired/not_started, `mutation_unresolved`, original unresolved operation ID; `_execute` не вызывается, Future сигналится вне lock. Новые tests692–771 подтверждённо queue-ят M2 за started M1 до release,6cells для M3×ValueError/RuntimeError, backendcount0, originalID и healthy read. Это именно прежний пропущенный interleaving.
2. **Reader counts:** `_expire_lease`271–282 сохраняет outstanding для running read/seek; owner570–571 сбрасывает его только после actual backend return/error. Queued expiry продолжает освобождать outstanding. Tests774–827 проверяют read и seek, repeated immediate close counts1/1 при unset Event, actor counts1/1, single exit и completed0/0 после release. Caller abandonment больше не подменяет backend completion в этом пути.
3. **Late report locator:** `_event`224–231 извлекает только canonical UUID из returned report dict, `_flush_events`233–251 логирует этот scalar вместе с original operation/run IDs. Нет filename/report bytes/cause prose; malformed/noncanonical value даёт None через существующий `_uuid`. Completion593–597 записывает returned value до event, late caller error/latch не переписываются. Test830–877 проверяет late report UUID + run + original op в одном returned log, отсутствие report bytes, fence и single store. Readiness wait происходит после flush данного returned event. Existing HTTP safe-cause controls сохраняются. Дополнительный durable/idempotency API не введён.

Эти исправления узкие, source-оснований считать их неправильными не найдено. Current runtime confirmation остаётся pending.

## R4 — P1: close удаляет lease раньше исполнения его queued read/seek

Воспроизводимые source locators: `service.py::_release`409–415; `_owner_main`518–560,569–571; `_execute`457–468; `_exit`487–490; `_expire_lease`274. Contract owning `docs/actor-lifecycle.md:307–326`: metadata-only close, одна outstanding read/seek, once-only owner cleanup, closing reader не выполняет backend read; owner остаётся для других independent leases/reads. Capacity/queue contract209–216 запрещает orphan pending Futures.

Interleaving без backend timeout:

1. Artifact lease открыт. Другой healthy metadata R начинает работать на owner и держит Event; actor state ready.
2. Caller ставит `reader.read` либо `reader.seek` в очередь; lease.outstanding=True. Тест должен подтвердить queued message под actor condition.
3. Другой caller выполняет reader.close с коротким/immediate deadline. `_release` выставляет lease.closing, но не отзывает queued reader message.
4. Release первого metadata R до deadlines. Owner выбирает closing lease **до mailbox**, вызывает `_exit` и удаляет его из `_leases`490.
5. Старое queued reader message остаётся. Если ещё не expired, `_execute` получает lease=None и падает на `.handle`; completion570 затем делает `_leases[id]` и получает **KeyError вне catch `_execute`**. Если message уже expired, `_expire_lease`274 получает тот же KeyError ещё до dispatch. Owner аварийно выходит в finally/profile unload. Caller Future не имеет предусмотренного typed completion и при собственном deadline тоже может упасть на missing lease. Owner callback отдаёт failed и удерживает global guard.

Это не допустимое bounded caller timeout и не просто closed-reader ValueError до admission: сообщение уже admitted и потеряло свой lifecycle record. При других открытых leases unexpected owner exit также обходит их normal exit path перед unload. Running read/close путь R2 не покрывает queued variant; новые R1 tests относятся к M, не lease queue.

Самый дешёвый различающий control: fake artifact открыт, independent R signals started и удерживает Event; reader read/seek queued и подтверждён; reader.close metadata отмечает closing и возвращает stopping; release R до call/io deadlines. Assert: queued reader backend_count0, predictable typed not-started/closed outcome без KeyError/orphan Future; exit ровно1 на owner; actor продолжает healthy independent read, unload не случился до actor.close; затем clean completed. Read и seek можно параметризовать. Если проверяется дополнительный open lease, его handle нельзя потерять при close первого. Все threads/events fixture должны быть конечно завершены и original failing evidence сохранены. Исправление должно атомарно разрешить queued lease work vs cleanup/tombstone перед освобождением registry; просто catch KeyError после unload не восстанавливает ownership contract.

Решение: сохранить текущий frozen candidate; добавить различающий negative fixture и узко исправить lifecycle, затем новый source packet и ограниченный централизованный GREEN. Не выполнять reviewer runtime.

## Остальные границы

Accepted exit/unload failure controls по-прежнему явно не найдены в actor_deadlines/service assertions; source этих путей прочитан, но happy close не является runtime failure-path evidence. Это остаётся отдельно указанным acceptance coverage gap исходного report, не объявляется PASS по зелёному exit code. Lifecycle/source safety шире трёх уже устранённых defects; GREEN2 существующего набора не опровергнет R4, которого в нём нет.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Рецензируется exact frozen GREEN2 | package byte equality, source/report hashes | текущие перечисленные owning files | сохранить |
| R1–R3 source причины устранены | dispatch/count/event delta и9 distinct regression cells | current GREEN ещё не получен | дополнительно измерить |
| Queued lease close не ломает owner | R4 interleaving и missing registry accesses | source proof, reviewer не исполнял fixture | изменить |
| Original finite ASGI assertions сохранены |9 assertions + decorators unchanged | stalled cells отдельно ожидают abort | сохранить |
| Полный CP-CODE/runtime/native acceptance | R4 и pendingGREEN/coverage gaps | synthetic tests не native/science acceptance | данных недостаточно |
