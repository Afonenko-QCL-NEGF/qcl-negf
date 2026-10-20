# DOC06 — narrow lint correction source handoff

2026-10-20. Только source correction по `/tmp/qcl-DOC06-LINT-1/original.log` (15 diagnostics), без lint/fmt/parser/typecheck/test/runtime/import/network/build/commit/CP calls. Sole GREEN принадлежит Root.

Сначала сверены exact managed Root formatted hashes, затем эти два файла скопированы в `/tmp/qcl-doc06-worktree`. Предыдущие v2 sources сохранены `/tmp/qcl-doc06-lint-prior-v2-static-slice.ts` и `/tmp/qcl-doc06-lint-prior-v2-docs_static_slice_test.ts`; formatted inputs сохранены `/tmp/qcl-doc06-lint-base-static-slice.ts` и `/tmp/qcl-doc06-lint-base-docs_static_slice_test.ts`. Managed Root/harness/checkpoints не изменены.

| Artifact | SHA256 |
| --- | --- |
| Formatted adapter base | `f11c439cab0fa3ae4f33d0122f83f118ab90453bddc0e436c73f2e386114fe16` |
| Formatted test base | `0b1cd93487767af0469b4946cd1aa2abb822916577e81ed1cae98909053f06d6` |
| New adapter,43061B | `3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b` |
| New test,30378B | `382a881675093137e5b42563d17851114e4ffbe8217ba3ead4636999e39cc8c4` |
| Minimal portable delta `/tmp/qcl-doc06-lint-fix.patch` | `1492487af611cbba5369bc90d563d7b08ddb0dda2b1f6ee41c552850b250666c` |

Изменены ровно три синтаксические группы:

- У11 outer Deno.test callbacks удалён redundant async. Каждый expression callback по-прежнему возвращает тот же fixture Promise; inner async bodies/awaits/assertions/fixtures/count56 не изменены.
- YAML selected leaf regex использует `^[ ]{2}energy_chunk:` вместо двух literal spaces. Это ровно два ASCII spaces, без разрешения табов/другой indentation.
- `required`, `allowed`, `resolve` внутри schemaProjection try-block стали const function expressions **на прежних местах**. Closures, bodies, guard/call order, hops/seen/root и catch boundary сохранены; все вызовы остаются после инициализации. Переносов между scopes, lint disables/casts/no-check/new dependencies нет.

Minimal diff просмотрен текстом и сопоставлен со всеми15 original diagnostics. Проверок инструментами не выполнялось; formatter/lint/typecheck/GREEN success этим report не заявляются. Independent CPPv2 semantic PASS из parent packet не пересертифицируется и semantic guards не менялись. Original raw сохранён.

Source reads консервативно <1MiB с учётом archive copies/hash/diff; delivered patch/report/identity <16KiB при64KiB output envelope. Physical I/O/CPU/RSS telemetry не измерялись.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Все15 замечаний имеют узкую source correction | Minimal delta:11 async,1 regex,3 expressions | Lint recheck не выполнялся | сохранить |
| Assertions/guards/области видимости сохранены | Прочитанный minimal diff | Runtime не проверялся | дополнительно измерить |
| Lint/fmt/sole GREEN проходят | Новых run receipts нет | Root проверки впереди | данных недостаточно |

STOP для независимого review и Root finite checks.
