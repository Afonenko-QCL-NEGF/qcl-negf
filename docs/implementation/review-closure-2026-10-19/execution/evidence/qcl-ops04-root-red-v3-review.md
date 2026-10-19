# OPS04.S Root v3 — narrow F1 source review

2026-10-20. **APPROVE test-source v3: F1 закрыт на уровне source, новых блокирующих замечаний в единственном correction delta нет.** Полный review v2 `/tmp/qcl-ops04-root-red-v2-review.md`, SHA256 `e5b0802310206241992194308e7ac5962483b25c0d7c73cf4e496107c8f17d74`, сохраняется для остального неизменённого corpus. Это ready source для решения координатора о finite RED; observed RED/GREEN, typecheck или native acceptance не установлены.

## F1 и отсутствие ослабления

`tests/solver_test.ts:171–188` заменяет неверный `JSON.stringify(spec)` на независимый явный expected object. Его первые properties — `hash,url,format,sources,julia,juliaManifest`, как требует first-insertion order raw duplicate members. Значения `hash/url` — окончательные корректные значения, а не discarded prefix. Вложенный graph сохраняет literal format/root и reversed components Runner→Core, соответствующие input fixture; Manifest/Julia identities точны.

Expected не парсит raw, не извлекается из outgoing JSON, не вызывается production builder/validator. Сравнение actual outgoing string с точным expected сохранено, canonical sorting не введён. Предшествующие command-count и `bound(...)` assertions сохранены, включая независимый SHA actual outgoing argument, full graph/archive, raw/consumed hashes и byte counts. Это исправление ошибочного oracle, а не ослабление проверки.

Проверена **единственность delta**: текстовый stream `tests/solver_test.ts` с заменой только строк 171–188 обратно на прежний assertion имеет SHA256 `d26512392d63eaccf44ab7711ea07b1b6c8a15a3fb3108afd47c1ccacbf9d542`, точно frozen v2. Stream не записывался в source file и не исполнялся. Application test SHA не изменился. Full actual `git diff -- tests/solver_test.ts tests/application_cd_test.ts` SHA совпадает с v3 patch `f5b8cd3efe2f3e8708cbdfe5b88f979f1f502b85a19daab707635288a64fb7e2`. Более шумный diff двух baseline patches объясняется переназначением context lines Git, а не дополнительным source delta.

## Identity и ограничения

Checkout `/tmp/qcl-ops04-root-worktree`, фактический HEAD `cfc38e1761f24caf436d938f378dbcdbf71a28f0`; status содержит только два modified test files. Восемь selected gitlinks не инициализированы и не менялись. Targeted product diff `ops/solver.ts ops/application_cd.ts nix/solver.nix` пуст, exit 0; их SHA совпадают с v2/baseline.

| Frozen input | Проверенный SHA256 |
| --- | --- |
| tests/solver_test.ts | d2c5da7ad9783bbc65e5e76baef8cb43282eb4388393f8dc130172be74c8b1d5 |
| tests/application_cd_test.ts | bd92a82d858ea17d1a124f2a9d257a76329f7f1630e423aad5ba1840c1982f85 |
| root-red-v3-report.md | b22a0f1b690c3f4443a16e1965f2df528cd594c13fabcb68a79ceaa6b411057c |
| root-red-v3-identity.json | 1b3e92192fcbff17a55a2fcd7278b64dcee9c84a87f5ef78ceb190a9515977ae |
| root-red-v3-patch.diff | f5b8cd3efe2f3e8708cbdfe5b88f979f1f502b85a19daab707635288a64fb7e2 |
| root-red-v3-delta.json | 26c598cf000c80d7653463fbca4b97f4b647f2c39728aceeaca838e1bbbb7845 |

Envelope ≤10min/1CPU/2GiB/read≤1MiB/report≤32KiB. Cumulative read/CPU/RAM/tool-output telemetry не инструментирована. Выполнены только текстовые/Git/SHA чтения и запись review/identity в `/tmp`; imports/parsers/typecheck/Deno/Nix/tests/build/network, source writes, children и checkpoint writes — **0**. Runtime slots не расходованы. Проверка source не заменяет будущий execution gate и не расширяет coordinator-owned budget.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1 исправлен без нового production normalization | Literal ordered expected object; exact-string и SHA/full-graph assertions сохранены | Только source, runtime впереди | сохранить |
| Остальной corpus равен reviewed v2 | Reverse-text SHA равен v2; application SHA неизменён | Предыдущие source-review ограничения сохраняются | сохранить |
| Observed RED/GREEN установлен | Execution receipts отсутствуют | Никаких запусков reviewer | дополнительно измерить |
| Native/scientific acceptance установлена | Данных нет | Source-only review | данных недостаточно |

**STOP. APPROVE narrow source correction; coordinator отдельно решает запуск finite RED.**
