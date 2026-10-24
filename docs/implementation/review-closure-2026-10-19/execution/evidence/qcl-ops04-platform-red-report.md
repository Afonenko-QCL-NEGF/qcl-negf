# OPS04.S Platform T2/T3 — исходники fixtures, перед независимым review

2026-10-19. Этап: phase 1, tests first, **runtime not_measured**. Это не результат RED/green и не scientific/native acceptance. После записи артефактов работа остановлена до независимого high review и отдельного bounded RED dispatch coordinator.

## Identity и область

- Owning Platform base/HEAD: `b067723c82382689bff5cc366981c56e99b926f8`.
- Изоляция: local clone `--no-hardlinks --no-checkout` из `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/qcl-negf-platform`, затем checkout exact base в ветку `codex/review-closure-protected-reader-boundaries`, путь `/tmp/qcl-ops04-platform-worktree`. Network и submodule init отсутствовали.
- Начальные `git status --short` и `git submodule status --recursive` пусты. Финальный status: только два изменённых Python test paths. Нет stage/commit/push, production changes, docs changes или Root TS changes.
- Accepted D2: `/tmp/qcl-ops04-source-design-v2.md`, SHA256 `19d56005eacf80aae3164291728530fe9b78eb9f43948f306e67c73d34c99147`.
- Independent design review: `/tmp/qcl-ops04-source-design-v2-review.md`, SHA256 `12e811ec56093734fdeb7fd6aac370f312ef880c2b7a64edd9689c8bca26ec42`.
- Неизменённый production locator: `ops/application_release.py`, SHA256 `1d4422bed5986901ddef22890ca16fe600336e6af2bef17d83ae809ebe794df0`.

Прочитаны primary root AGENTS/architecture, Platform CONTRIBUTING и D2 T2/T3, source readers/snapshot/prefetch, существующие fixtures и Root T2 literal table. Работа не меняет resource ownership, trust roots, signatures, enrollment authority или физическую модель. Используется synthetic inode/syscall model; настоящий FIFO, privileged namespace и root permission mutation не создаются.

## Предлагаемое покрытие исходниками

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| T2 password/argument negatives до callbacks | `tests/test_application_release.py:1096`, existing rejection test расширен до exact Root table: named/explicit-empty/encoded passwords, HTTPS/SSH/ssh-ng, malformed authority, whitespace/controls/DEL/leading dash/nonstring. 19 общих literals плюс 7 прежних regressions; no commands и unchanged gate | Тесты не запускались; Python guard уже проверяет `password is not None`. Произвольные secrets в username/query не распознаются | сохранить |
| T2 username-only и local routes сохраняются | `tests/test_application_release.py:1136`: 7 exact Root positives, включая encoded colon in username; callback argv точный, URI один элемент, copy перед path-info, две hashes и исходный manifest неизменны | Python consumer не вычисляет release digest; Root проверяет mirror identity отдельно | сохранить |
| T3 0/1/65536 bytes и fragmented reads | `tests/test_node_enrollment.py:211`; 6 positive subcases, exact bytes, actual read sum, O_NOFOLLOW всех opens, leaf O_NONBLOCK, fd closure | Synthetic source fixture, не native syscall evidence | дополнительно измерить |
| T3 oversize 65537 | `:226`, fragmented chunks, exact actual sum 65537, ValueError и fd closure | Нет утверждения о kernel-blocked I/O | дополнительно измерить |
| T3 FIFO/socket/directory leaf до read | `:234`, 3 types, no reads, обязательные O_NONBLOCK/O_NOFOLLOW, fd closure | Нет native FIFO и реального hang | дополнительно измерить |
| T3 owner/mode/root/ancestor/leaf | `:247`, 9 uid/group-write/other-write negatives; `:261`, 3 symlink negatives с независимым asserted O_NOFOLLOW; `:276`, 6 root/ancestor non-directory cases | Fake OS boundary, не реальная защита от trusted root mutation | дополнительно измерить |
| T3 invalid paths и semantic emptiness | `:290`, 6 path negatives до open; `:299`, empty enrollment и empty known_hosts consumer negatives | Raw reader вправе вернуть empty bytes | сохранить |
| T3 healthy full и progressing short writes | `:310`, full write и positive counts 1/2/3/4/remaining; exact bytes/hash/0600/0700, file→directory→parent fsync, complete fd closure | Existing write-all loop не изменён | сохранить |
| T3 incomplete write не выдаёт trusted reference | `:327`, initial zero, prefix+zero, prefix+exception; assertRaises, exact original failed prefix retained, no fsync, fd closure | Никакого cleanup/retry; original failed attempt остаётся | сохранить |
| T3 fsync failure не выдаёт trusted reference | `:341`, failures file/directory/parent, ordered fsync prefix, complete original bytes retained, fd closure | Не доказывает persistence на native filesystem | дополнительно измерить |
| T3 invalid frozen input до namespace mutation | `:356`, empty/65537/nonbytes/bytearray/None, unchanged synthetic nodes, no opens | Source-only | сохранить |
| Late SSH и NIX_SSHOPTS snapshot binding | Existing `EnrollmentTests.test_source_trust_substitution_does_not_change_late_transport_snapshot` сохранён без изменений | В phase1 не выполнен; реальная transport compatibility отдельно | сохранить |

T3 добавляет 12 test methods с 49 proposed subcases. T2 изменяет один existing test method и добавляет один positive method. Это source inventory, **не измеренная test coverage**. Ожидаемые Python guards уже выглядят корректными; phase name RED не требует искусственно ломать production или ожидать непременно failing Platform cases.

## Проверка и стоп

Выполнены text/Git reads, создание local clone/branch, изменение только test sources, `git diff --check` (exit 0, пустой вывод), просмотр полного изменённого fixture section и T2 diff, hashes/размеры. Import/parser/Python/test runtime invocations: **0**. Nix/Deno/Julia/build/install/network/server/native/science/full CI: **0**. Дочерние агенты не создавались. Checkpoint не правился.

Порученный envelope ≤25min/1CPU/2GiB/read≤4MiB/output≤96KiB. Фактические cumulative CPU/RAM/read не инструментировались; лимиты не представлены как measured telemetry. Дорогих subprocess runtime не было. Один ошибочный ранний `cat` несуществующего skill path дал exit 1 без чтения данных, после чего прочитан реальный using-superpowers с явным SUBAGENT-STOP; это не target runtime check.

Frozen patch `/tmp/qcl-ops04-platform-red-patch.diff`, 15923 bytes, SHA256 `b5aa36236fa373c709b6428198afbbf40c54895e2fa2c06fd8dbd365ea3bddef`.

- `tests/test_node_enrollment.py`: SHA256 `68c56e1f6d86966a7e9ad7294bef550f2a74511d131dd067ae11ad1569000a00`.
- `tests/test_application_release.py`: SHA256 `3b39987d1a3e1914ba45c8224af6d600dc92cffa6c030a9feaa955dfb0e326d6`.

Только coordinator определяет remaining shared runtime slot и точный harness. Возможный будущий subset: `ProtectedInputBoundaryTests` + два T2 methods + preserved existing cache/hash/no-cache/late-transport controls, **один** Python invocation ≤60s/1CPU/2GiB/output≤1MiB, после независимого high review. Эта запись не выдаёт разрешение на исполнение и не расходует runtime slot.
