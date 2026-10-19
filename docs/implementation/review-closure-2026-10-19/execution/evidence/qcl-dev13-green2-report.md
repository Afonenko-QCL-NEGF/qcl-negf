# DEV13 correction R1/R2/R3 — frozen GREEN-2

Portal base `fa80b5b5920dc16dfb911d164939b3d23e6be186`.
Independent review SHA256 `e749318061cdaaf4fd224750c94ddbdb9833574118ebaed358078cf22b593d2b`.
Root witnessed RED-2:9failed/24passed, exact R1six/R2two/R3one assertions;
ASGI corrected post-header abort expectation passed. Raw/receipt сохранены root
в `/tmp/qcl-DEV13-RED-2`; wall3.189s/RSS72085504/log31341B/stopnone.
После semantic RED и explicit root release production исправлен только в
`src/qcl_negf_api/service.py`; остальные product files и все RED-2 tests unchanged.

## Narrow correction

- **R1:** `_owner_main` под существующим metadata lock непосредственно перед
  queued→running повторно проверяет mutation fence. Любое из M3, admitted до
  post-dispatch exception предыдущего M, получает `mutation_unresolved`,
  not_started и original unresolvedID; backend dispatch не происходит. Read
  queue остаётся доступна. Существующие Future signals остаются вне lock.
- **R2:** `_expire_lease` больше не сбрасывает outstanding для running read/seek.
  Этот флаг теперь снимается owner только после actual backend return/error.
  Для queued/not-started expiry он снимается сразу. Поэтому stopping readerclose
  имеет pending_operations1 до actualreturn; repeated release не меняет счётчик.
- **R3:** bounded `_event` metadata дополнена одним `report_uuid` scalar, который
  извлекается только из canonical UUID поля returned save_agent_report receipt.
  `_flush_events` на owner добавляет report locator в ту же diagnostic logrecord,
  где original operationUUID/anchorUUID. ActorReceipt/publicAPI shape не менялся.
  No report bytes, report prose, filename, raw exception или private URL берутся
  в event/logger. Malformed/noncanonical UUID становится None, не guessedlocator.
  Mutation latch не сбрасывается поздним returned receipt.

Все9 differentiated Event/Condition/caplog regression cells сохранены без
изменений. Сохранены corrected stalled ASGI2cells и все4 original finite cells.
Новый дизайн, deadlines, physics, scientific status, ownership model, automatic
retry/reconciliation/store или process supervisor не добавлялись.

## Frozen packet/checks

`/tmp/qcl-dev13-green2.diff` SHA256
`a5c983044897460ba614bca6a79356047ff050171617335a47ef1fb1c097b6f0`.
Source service SHA256
`397e3c4c98136cd34446f38e332bcb088c9cbe360be69bebec5874353b6a6e24`.
Tests actor SHA256 unchanged from RED2
`a590bbef178e2ac4fd74c85b2523e15c78bc93c1880ad4429707e80aad4c47fc`.
Other product hashes unchanged:
api`d324a9188d8b4f0b3a8bea5de38a0aa3891949a8f0b924c12790711496ea5e63`;
exports`1116d3717b8cafdd51278a60b0eff5887d49e66609a5086ade535848250351a8`;
settings`fc8986ec7d06a25b261517d458162438eba9096a6f2f1d8d3f04f71b10c3897c`.

Source-only Ruff service/newactorfixture PASS, format unchanged; gitdiffcheckPASS.
Никаких tests/project imports/install/build/server/solver этим автором не
выполнено. Branch/stage/commit/push =0. Expected runtime не назван observedpass.
Root GREEN-2 selection: five testfiles actor_deadlines,service,stream_disconnect,
exports,api — прежний finite shared envelope; independent re-review требуется.
Остальные inherited api.py E501 и native/process-exit limits из первого report
не изменялись и не названы проверенными/исправленными.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1–R3 различаются tests до fix | Root RED2 exact9 failures | Synthetic backend, не native | сохранить |
| Source устраняет три причины | Narrow service dispatch/count/log changes + frozenhash | GREEN2/independent re-review pending | дополнительно измерить |
| Report operational correlation безопасна | CanonicalUUID-only bounded event, fixed logger format | Durable/cross-crash logging не доказано | сохранить |
| Runtime/CP-CODE accepted | Нового receipt ещё нет | CHANGES_REQUESTED снимает independent reviewer | данных недостаточно |
