# DEV13 RED-2 tests-only freeze

Baseline GREEN-1 packet `7ace94cc51e485340e8812f9cca2ba02eb7d2c6735a94660b6bce67bf14fecc3`.
Independent review `/tmp/qcl-dev13-code-review.md`, SHA256
`e749318061cdaaf4fd224750c94ddbdb9833574118ebaed358078cf22b593d2b`.
Root GREEN-1 receipt:2failed/156passed; raw `/tmp/qcl-DEV13-GREEN-1/original.log`.
Применён receiving-code-review; R1–R3 проверены по фактическому owning source.

Root explicit release tests-only. Product files НЕ менялись; hashes остаются:
service528b4676ae711aa3b041b4fb3f05f3851b02d0d01cfd9fd8fb5463772aa1a692;
api d324a9188d8b4f0b3a8bea5de38a0aa3891949a8f0b924c12790711496ea5e63;
exports1116d3717b8cafdd51278a60b0eff5887d49e66609a5086ade535848250351a8;
settingsfc8986ec7d06a25b261517d458162438eba9096a6f2f1d8d3f04f71b10c3897c.

Единственный изменённый testfile `tests/test_actor_deadlines.py`, SHA256
`a590bbef178e2ac4fd74c85b2523e15c78bc93c1880ad4429707e80aad4c47fc`.
Incremental tests-only diff `/tmp/qcl-dev13-red2-tests.diff`, SHA256
`f3bb4e586291dc1cb8bfaca80df6c8cfb421e725202172d974c50aef03c084c4`.
Сохранён baseline testfile `/tmp/qcl-dev13-green1-actor-tests.py`.

## Дифференцирующие регрессии

- R1: `test_queued_mutation_is_refused_when_earlier_dispatched_mutation_becomes_unknown`,
  3queued operations(submit_plan/kill_run/save_agent_report)×2first exception
  types(ValueError/RuntimeError). First store-start Event держит owner; under actor
  Condition observer подтверждает уже admitted queued M2; release до1s deadline
  вызывает post-store exception M1. Assertion M2 backendcount0, not_started и
  original unresolvedID, GET remains usable. Ожидаемый semantic RED: queued M2
  сейчас исполняется. Все helper threads finally released/bounded joined.
- R2: `test_reader_close_counts_include_timed_out_backend_operation_until_actual_return`,
  read/seek. После bounded response deadline backend Event всё ещё held;
  repeated reader.close требует exact(operations1,leases1), actor counts same;
  actual return даёт completed0/0 и single exit. Ожидаемый RED: readeroperations0.
- R3: `test_late_report_uuid_is_logged_with_original_operation_without_report_bytes`.
  Report store held за callerdeadline, then returns exact new reportUUID. After
  owner ready barrier caplog требует returned record с original operationUUID,
  anchorUUID и reportUUID вместе, без raw report; fence stays/no secondwrite.
  Ожидаемый RED: reportUUID отсутствует в logger diagnostics.

## GREEN-1 ASGI failures: source/log diagnosis и tests-only correction

Оба observed failures — `ActorDeadline(operation_deadline)` из reader.read,
доставленный Starlette/AnyIO через non-abandoning worker next() после уже
посланных headers. Caller cancellation не превращает exception из in-flight
next() в successful stream. Product contract §9 прямо требует abort/log после
headers и запрещает новый JSON/успешное полное тело. Исходный test предполагал
silent coroutine return и не перехватывал ожидаемый stream abort.

В `serving` добавлен catch ТОЛЬКО ActorDeadline, затем assertions exactly1,
operation_deadline/unknown. Все прежние bound/releaseunset/zero-body/deferredexit/
actual single exit assertions сохранены; timeout не повышен. This does not catch
arbitrary exceptions/cleanup errors. Existing four full-app finite ASGI cells и
их assertions не менялись.

## Проверки и ожидаемый packet

Source-only Ruff format/check нового testfile PASS; git diff--check PASS.
Tests/imports/build/install/server/solver этим implementer не запускались.
Root RED-2 selection: только components/qcl-negf-portal/tests/test_actor_deadlines.py.
Ожидаются9 differentiated failures(R1 six,R2 two,R3 one), а correctedASGI cells
должны пройти с прежним bound. Это ожидаемый результат, runtime ещё не получен.
До root semantic RED-2 release production исправления не выполняются.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1–R3 выделены отдельными негативными controls | Event/Condition/caplog assertions | Пока source-only, root runtime pending | дополнительно измерить |
| Product frozen при RED-2 | Four unchanged hashes | Исправления ещё не внесены | сохранить |
| ASGI failure вызван silent-return expectation | Original GREEN1 stack to reader.read ActorDeadline | Corrected abort expectation ещё не executed | изменить |
| Full CP-CODE/runtime achieved | Receipt отсутствует | Independent CHANGES_REQUESTED действует | данных недостаточно |
