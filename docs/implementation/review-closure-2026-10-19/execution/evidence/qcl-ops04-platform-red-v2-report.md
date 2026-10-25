# OPS04.S Platform phase1 — correction cycle1, frozen v2

2026-10-20. Только test source, перед отдельным независимым high review. Target runtime/import/parser/test execution: **0**; Platform RED/GREEN counters **0/2**. Production и T2 source не изменены этим correction.

Основание: `/tmp/qcl-ops04-platform-red-review.md`, SHA256 `1f2da5b3154c7a9958a8332a048e113423e3878fccc60ca23b4be60bcf9be791`, полностью прочитан. F1/F2 сверены с actual `protected_directory`/`read_protected_file`, base `b067723c82382689bff5cc366981c56e99b926f8`. Навык receiving-code-review применён для технической проверки замечаний; runtime validation отдельно запрещена поручением этого этапа.

Workspace `/tmp/qcl-ops04-platform-worktree`; branch `codex/review-closure-protected-reader-boundaries`; HEAD неизменён. До/после status — только два modified test paths из phase1; recursive submodule status пуст. Нет Git mutations, stage/commit/push, children, network, server/native/privileged actions, build/install/science/full CI. Original/main и checkpoint не затрагивались.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| F1: readonly-mode mutant теперь различается исходниками assertions | `tests/test_node_enrollment.py::ProtectedInputBoundaryTests.assert_readonly_opens`: каждый recorded successful/failed reader open требует `(flags & os.O_ACCMODE) == os.O_RDONLY`. Helper вызван во всех reader fixtures, включая owner/mode, failed symlink/non-directory opens и semantic enrollment consumer. Writer leaf этим helper не проверяется | Source inspection; runtime/mutation run отсутствует | изменить |
| F2: EOF больше не скрывает over-read | Existing oversize method сохраняет65537 и добавляет65538 bytes, каждый с full/997-fragment returns. Требует ValueError, complete fd closure, actual total ровно65537 и ≤65537; длинный tail остаётся непрочитанным. Каждый recorded requested размер положителен и не превышает независимый remaining budget65537−already_delivered | Expected constants не вычисляются production helper; реальный syscall/native proof отсутствует | изменить |
| Healthy/T2/write-side semantics сохранены | T2 file SHA неизменён; writer fixtures и остальные acceptance predicates не правились; exact-bound65536 healthy остаётся | Нового runtime свидетельства нет | сохранить |
| Production readonly/bounded reader менять не требуется | `ops/application_release.py` SHA неизменён и targeted Git diff пуст | Это source verdict, не native acceptance | сохранить |
| RED/GREEN результат получен | Runtime receipts отсутствуют, counters0/2 | Исполнение отдельно у Root после high review | данных недостаточно |

Read-side helper не моделирует OS access permissions и не вызывает production acceptance logic: он сравнивает observed syscall argument с literal existing readonly contract. Для mutant `n=4096` длинный payload допускает доставку65538, поэтому actual cap assertion различает его; дополнительно last requested размер нарушит independent remaining bound. Это reasoning по исходникам, **не выполненное mutation testing**.

T3 остаётся12 test methods; proposed input combinations увеличены49→52 за счёт oversize1→4. T2 остаётся19 shared negatives+7 retained extras и7 positives. Вложенные assertion subtests не объявляются дополнительной измеренной coverage.

Проверки: просмотр full review, source и complete correction delta; `git diff --check` exit0/пусто; SHA256/размеры и `git diff --numstat`. Cumulative measured CPU/RAM/read не инструментированы; порученный envelope≤10min/1CPU/2GiB/read≤1MiB/output≤48KiB не выдаётся за telemetry.

Frozen v2:

- Full patch `/tmp/qcl-ops04-platform-red-v2-patch.diff`,17249 bytes, SHA256 `ebb800e1cdd95366548f91bcbc86562ecf5ab18e8716e7ec22b47a283a1d610c`.
- Correction-only delta `/tmp/qcl-ops04-platform-red-v2-delta.diff`,4949 bytes, SHA256 `aec8116650eca89efd626c10cc177d4d0598bb998b7c40306845e37787b61e3b`.
- Enrollment tests SHA256 `27b733487737501880023dc55607b21c357654821da5a65f53940873c0f0cfe5`.
- Application tests SHA256 `3b39987d1a3e1914ba45c8224af6d600dc92cffa6c030a9feaa955dfb0e326d6`.
- Production SHA256 `1d4422bed5986901ddef22890ca16fe600336e6af2bef17d83ae809ebe794df0`.

Previous frozen artifacts сохранены и повторно совпали: report `c103de9ae30afb15d38eece1f60d423c5b4821d9f66b96514ab3bdade5d4d252`; identity `ad764c8dc849e046205536936783992fca26d06537ff018704351599b5f3fd31`; patch `b5aa36236fa373c709b6428198afbbf40c54895e2fa2c06fd8dbd365ea3bddef`. Old enrollment source сохранён для reproducible delta в `/tmp/qcl-ops04-platform-red-v1-node-enrollment.py`, SHA256 `68c56e1f6d86966a7e9ad7294bef550f2a74511d131dd067ae11ad1569000a00`.

**STOP** перед отдельным high review. Только Root владеет последующим exact selector/environment/admission/counter и RED invocation. Эта correction не меняет runtime envelope и не расходует слот.
