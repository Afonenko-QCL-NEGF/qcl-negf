# DEV13 — независимый CP-CODE, frozen GREEN1 candidate

Вердикт: **CHANGES_REQUESTED**. Source-first проверка до получения GREEN receipt. Reviewer не запускал target imports, тесты, build, backend, threads, сервер или solver; проверены исходный текст, assertions, hashes и diff. Это не runtime/scientific acceptance.

## Привязка

- Portal HEAD `fa80b5b5920dc16dfb911d164939b3d23e6be186`, branch `codex/review-closure-actor-lifecycle`.
- Frozen `/tmp/qcl-dev13-green1.diff`: SHA256 `7ace94cc51e485340e8812f9cca2ba02eb7d2c6735a94660b6bce67bf14fecc3`, 85,832 bytes. Независимая реконструкция `git diff --binary` + new-file diff `tests/test_actor_deadlines.py` равна пакету byte-for-byte.
- Accepted `/tmp/qcl-dev12-design-v2.md`: SHA256 `fa3ca630f7b44ef9d72582ff91ced2e0c671f0986cecb4e20cddf5b294255712`; owning `docs/actor-lifecycle.md`: `d824d97a1f6bdd99e7c6cce321e11b9773467242e5c7c359440e8eb8689b2376`.
- Scope: четыре owning Python files, три existing test files, один новый test file. Изменения вне этого пакета не оценивались. AiiDA `5579d55684939495230241f446b7ea07c8ae0224` использован только для проверки формы возвращаемого report receipt.
- Current hashes: `service.py` `528b4676ae711aa3b041b4fb3f05f3851b02d0d01cfd9fd8fb5463772aa1a692`; `exports.py` `1116d3717b8cafdd51278a60b0eff5887d49e66609a5086ade535848250351a8`; `api.py` `d324a9188d8b4f0b3a8bea5de38a0aa3891949a8f0b924c12790711496ea5e63`; `settings.py` `fc8986ec7d06a25b261517d458162438eba9096a6f2f1d8d3f04f71b10c3897c`; new test `4c95b540aae3d000b9d321ebbd3cc0f2a8ea1510a2e57dd40d44052da148d3a2`.

## Findings

### R1 — P1: queued mutation обходит fence после backend exception

Locators: `src/qcl_negf_api/service.py::_owner_main`, 522–533 и 562–583; `_admit`, 294–295. Contract: owning docs 241–243, 271–277; никаких submit/kill/report writes после unknown mutation.

Если M1 уже выполняется, M2 может быть admitted и находиться в mailbox. При конечном exception M1 owner ставит `_mutation_receipt`, но не отзывает queued M и не проверяет fence при dequeue: единственный барьер там — deadline. Поэтому после unknown store/submit M1 ещё не просроченный M2 выполняет backend mutation. Проверка `_admit` защищает только запросы, пришедшие после latch. Running-timeout путь отдельно drain-ит очередь, exception путь этого не делает.

Дешёвый различающий control: fake M1 сигналит started/stored и ждёт Event; M2 подтверждённо стоит в очереди; до истечения обоих deadlines release M1 с ValueError либо RuntimeError. После этого M2 backend count должен остаться 0, его outcome — not_started с original unresolved operation ID; reads должны оставаться работоспособными. Проверить одну и ту же гарантию для всей M group. Existing `test_started_mutation_exception_latches_original_receipt` (93–115) вызывает M2 только после exception и пропускает этот interleaving. Сохранить frozen пакет перед исправлением.

Решение: изменить до CP-CODE PASS.

### R2 — P2: reader close сообщает ноль при незавершённом read/seek

Locators: `service.py::_expire_lease`, 265–274; `_wait`, 339–350; `_release`, 407–412. Contract: owning docs 130–132 — actor/reader close counts exact, unknown nullable counts допустимы лишь ExportStore.

При timeout выполняющегося reader read/seek `_expire_lease` сразу сбрасывает `lease.outstanding=False`, хотя owner ещё находится внутри backend read/seek. Последующий reader.close deadline возвращает `CloseResult(stopping, 0, 1, ...)`. Это ложный pending_operations=0 при фактически незавершённой операции; state stopping и pending lease спасают cleanup, но не достоверность счётчика. Actor.close отдельно смотрит `_running` и считает иначе.

Минимальный control уже почти есть: в `test_close_does_not_claim_backend_completion` (118–158) Event остаётся unset после read timeout. Проверить оба counts у reader.close до release, повторный close, затем нули completed после actual owner return; распространить на seek. Учитывать фактическую queued/running lease operation под metadata lock, не caller abandonment.

Решение: изменить и подтвердить truthful counts.

### R3 — P2: late report UUID не сохраняется под operation UUID

Locators: `service.py::_receipt`, 207–221; `_flush_events`, 228–245; owner completion 577–581. Contract: owning docs 262–269 и required fixture 584.

Для `save_agent_report` `_receipt` берёт только args[0] — anchor run UUID. Возвращаемый `value['uuid']` нового report нигде не включается в bounded event. Logger печатает run/child/attempt, report locator отсутствует. После timeout поздний successful report receipt тем самым не коррелируется в retained operational diagnostics с original operation UUID. AiiDA owning source `src/aiida_qcl_negf/service.py:442–445,448–491` возвращает именно отдельный новый report UUID; anchor run не заменяет этот locator. Локальная переменная завершённого сообщения не является предусмотренным диагностическим интерфейсом. Submit UUID путь реализован, report путь пропущен.

Дешёвый control: fake save signals stored, выдерживает caller deadline и затем возвращает canonical report UUID + known anchor. После release bounded log/event должен содержать exact report UUID и original operation UUID, без report bytes/raw exception; latch остаётся и повторная M не выполняется. Existing late-return fixture 412–441 проверяет submit, не report и не diagnostic correlation. Исправление не требует нового durable idempotency API.

Решение: изменить до принятия полного D12 diagnostic contract.

## Что source check подтверждает и где остаются границы

- Один executor owner и bounded mailbox; Future signal/cancel callbacks вынесены из metadata locks. Queue expiry не исполняет истёкшее сообщение. Owner priority cleanup, open reservation, late-enter cleanup и once-only exit присутствуют. Их runtime корректность данным чтением не доказана.
- Export stop latch имеет отдельный lifecycle lock, timed store-lock acquisition и nullable counts. Caller TTL path помечает metadata, deletion идёт на один coalesced worker; reader lease удерживает archive. Failed delete сохраняет reservation и не выдаёт cleanup completed. Синхронный arbitrary filesystem read не получил выдуманный deadline.
- Общий lifespan deadline передаётся exports и actor; actor close вызывается в finally. Close bounded wait не означает остановку backend/thread/process; этого implementation и review не утверждают.
- ActorUnavailable обрабатывается до generic RuntimeError; diagnostic headers/unknown suffix сохраняются при agent-report sanitization. HTTP-side schema/admission отказ до actor отличен от dispatched backend exception. Для backend422 используется консервативное safe сообщение; raw cause не раскрывается.
- Existing ASGI control сохраняет все 9 прежних assertions (AST membership independently checked), оба ASGI versions × artifact/export decorators сохранены; добавлены только 4 fake selection/inventory/plan assertions и новый producer seam. Новые stalled actor tests — отдельно. Fixture compatibility не равна ASGI runtime PASS.
- Набор новых assertions не покрывает R1–R3. Отдельные accepted exit/unload failure и seek timeout controls в новом файле не найдены; их отсутствие не заменяется проверкой happy read/close.
- `git diff --check` exit0. Product/source tests не выполнялись reviewer. GREEN receipt на момент этого report не представлен; даже GREEN существующих assertions не устраняет source findings. После исправления нужны новый exact package/hash и целевые различающие assertions с централизованным ограниченным запуском.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Рецензировался frozen candidate | byte equality reconstruct, hashes, Portal HEAD | только перечисленные файлы | сохранить |
| Unknown mutation fence закрывает все последующие backend writes | R1: queued M проходит dequeue без fence | source interleaving, не executed fixture | изменить |
| Reader close counts truthful | R2: outstanding сброшен до backend return | state stopping сохранён | изменить |
| Late report effect имеет exact same-op locator | R3: возвращённый report UUID не логируется | run anchor есть, report locator потерян | изменить |
| Основные ownership/stop/deferred-FS механизмы присутствуют | owning source и preserved controls | runtime ещё не подтверждён; edge cases выше | дополнительно измерить |
| Full CP-CODE/runtime/native/scientific acceptance | отсутствует current GREEN receipt; три source gaps | не выводится из diff check | данных недостаточно |
