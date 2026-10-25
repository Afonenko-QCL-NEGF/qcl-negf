# OPS04.S Root phase1 correction cycle1 — v3 freeze

Статус: **F1 corrected in source; STOP для narrow independent review до Root RED**. Review `/tmp/qcl-ops04-root-red-v2-review.md` SHA256 `e5b0802310206241992194308e7ac5962483b25c0d7c73cf4e496107c8f17d74` сверён и прочитан. Runtime/observed RED отсутствуют.

Единственная коррекция относительно frozen v2 — expected JSON в `tests/solver_test.ts`, test `OPS04 graph and object order are immaterial while raw duplicate members normalize once`. Прежнее `JSON.stringify(spec)` ошибочно ожидало порядок format…url,hash, хотя raw первые members — hash,url. Теперь expected явно задаёт ordered object `hash,url,format,sources,julia,juliaManifest`, literal source/lock/archive identities и reversed component fixture list. Expected не парсит raw input, не извлекается из outgoing argument и не вызывает production builder. JS duplicate members заменяют значения, сохраняя first-insertion positions. Independent actual outgoing SHA/receipt/graph checks сохранены.

Production, normalization policy, input fixture, `buildSolver` call, application tests и остальной corpus не менялись. Никакой canonical key sorting. Root source authority остаётся `cfc38e1761f24caf436d938f378dbcdbf71a28f0`, isolated `/tmp/qcl-ops04-root-worktree`, branch `codex/review-closure-depot-byte-binding`; protected original не изменялся. Все v1/v2 report/identity/patch/delta сохранены без записи. V3 patch полный от Root base, v3 delta описывает только cycle1 correction.

Final hashes:

| Файл | SHA256 |
| --- | --- |
| tests/solver_test.ts | d2c5da7ad9783bbc65e5e76baef8cb43282eb4388393f8dc130172be74c8b1d5 |
| tests/application_cd_test.ts unchanged | bd92a82d858ea17d1a124f2a9d257a76329f7f1630e423aad5ba1840c1982f85 |
| ops/solver.ts unchanged | bc513f610cce976d108e17902ebd423c434992ba0edb91e2bdc3da2e5f3c247f |
| ops/application_cd.ts unchanged | 91989d0171e011f4518e178e247d4f7a466d08bd02b7931308a202c4354ee9ce |
| nix/solver.nix unchanged | 16c99da166ee2d9afc7d238fa317e43f0bcc71e2eccb8de3ff11e97b70aa858f |
| root-red-v3-patch.diff | f5b8cd3efe2f3e8708cbdfe5b88f979f1f502b85a19daab707635288a64fb7e2 |

`git diff --check` exit0, только whitespace. Target parser/import/tests/typecheck/Deno/Nix/build/network/server/subprocess/children/checkpoint writes — 0. Envelope ≤10min/1CPU/2GiB/read≤1MiB/output≤32KiB; cumulative telemetry не инструментирована, не объявлена измеренной. C08/science не затронуты. Root sole checkpoint/runtime counter writer.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1 wrong key-order oracle исправлен | Explicit independently ordered expected object; source hash above | Только source, narrow review и execution впереди | дополнительно измерить |
| Application/production unchanged | Hashes match v2/baseline | Реализация не начата | сохранить |
| Observed RED/GREEN/native/scientific acceptance установлены | Execution receipts отсутствуют | Source-only correction | данных недостаточно |

**STOP: narrow high review before coordinator RED.**
