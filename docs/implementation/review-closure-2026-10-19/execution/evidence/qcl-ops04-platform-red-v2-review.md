# OPS04 Platform RED v2 — узкая независимая corrective source review

2026-10-20. **PASS_SOURCE: оба предыдущих замечания R1/F1 и R2/F2 закрыты.** Новых замечаний в corrective delta не найдено. Это eligible source для отдельно bound coordinator unit invocation, не syntax/runtime/RED/GREEN/native acceptance. Reviewer imports/parsers/Python/tests/network/build/Git mutations/source edits/children=0; runtime calls=0.

## Identity / scope

Actual HEAD `/tmp/qcl-ops04-platform-worktree`: `b067723c82382689bff5cc366981c56e99b926f8`; status — только два modified test paths из phase1. Прочитаны correction-only delta и actual source, сопоставлены original/v2 full patches и мой original review; авторский report прочитан после source assessment. Accepted D2 и production semantics не пересматриваются.

| Вход | SHA256 |
| --- | --- |
| `tests/test_node_enrollment.py` | `27b733487737501880023dc55607b21c357654821da5a65f53940873c0f0cfe5` |
| `tests/test_application_release.py` | `3b39987d1a3e1914ba45c8224af6d600dc92cffa6c030a9feaa955dfb0e326d6` |
| `ops/application_release.py` | `1d4422bed5986901ddef22890ca16fe600336e6af2bef17d83ae809ebe794df0` |
| `/tmp/qcl-ops04-platform-red-v2-patch.diff` | `ebb800e1cdd95366548f91bcbc86562ecf5ab18e8716e7ec22b47a283a1d610c` |
| `/tmp/qcl-ops04-platform-red-v2-delta.diff` | `aec8116650eca89efd626c10cc177d4d0598bb998b7c40306845e37787b61e3b` |
| `/tmp/qcl-ops04-platform-red-v2-identity.json` | `89fb707baa45571901d1e285ebcce0f74f181d7340307196619d617ecd5adaf7` |
| `/tmp/qcl-ops04-platform-red-v2-report.md` | `4339bfc67ecb6a584254fa51fc126944edb53f922f59b0d2e64e3f766395e069` |
| Original independent review | `1f2da5b3154c7a9958a8332a048e113423e3878fccc60ca23b4be60bcf9be791` |

Original author report/identity/patch повторно хешированы и сохранены соответственно `c103de9ae30afb15d38eece1f60d423c5b4821d9f66b96514ab3bdade5d4d252`, `ad764c8dc849e046205536936783992fca26d06537ff018704351599b5f3fd31`, `b5aa36236fa373c709b6428198afbbf40c54895e2fa2c06fd8dbd365ea3bddef`. Source hashes T2 и production byte-identical предыдущему reviewed candidate. Full patch comparison ограничен добавлением readonly observer/calls и заменой oversize block; writer/остальные controls не менялись.

## Закрытие замечаний

**R1/F1 CLOSED — tests/test_node_enrollment.py:206–210,230,250,264,279,296,311,321,332.** Новый test-side helper наблюдает каждый recorded reader open, в том числе failed attempted syscall, и требует literal `(flags & os.O_ACCMODE) == os.O_RDONLY`. Это правильное сравнение для нулевого O_RDONLY. Helper вызывается во всех новых reader fixture paths: healthy, oversize, leaf type, owner/mode, symlink, non-directory, invalid path и semantic consumer. Invalid path case отдельно требует no opens, поэтому vacuous readonly loop не заменяет его прежний guard. O_RDONLY→O_RDWR mutant нарушает наблюдаемый syscall argument даже при неизменных fake returned bytes. Writer fixtures335+ этот helper не вызывают; O_WRONLY snapshot leaf не объявлен ошибочным. Это наблюдение existing source contract, не новая permission policy или product acceptance helper.

**R2/F2 CLOSED — tests/test_node_enrollment.py:233–251.** Сохранён size65537 и добавлен независимый tail size65538; оба проверяются с normal full reads и fragmented997. Expected65537 literal не получается через production helper. Для actual recorded reads требуют requested>0, requested≤65537−already_delivered, actual total ровно65537 и≤65537. Для longer input actual<size доказывает, что tail не исчерпан fixture EOF. После rejection сохраняются readonly и complete descriptor closure assertions.

Конкретный прежний mutant constant n=4096 нарушит last requested remaining budget; на longer input способен доставить65538 и нарушить actual cap/tail assertions. Correct source с final bounded request остаётся согласован с literals и full/fragmented positives. Это reasoning по source, не выполненный mutation test. Bound не увеличен; extra bytes остаются private synthetic input, новый scientific/native run не добавлен.

## Отсутствие регрессий и ограничения

Actual numstat от base: Application+57/-3, Enrollment+224/-0; относительно reviewed v1 Enrollment delta net+25 lines. T2 source неизменён, включая exact parity/username-only/local argv и old no-callback/no-quiesce controls. Writer full/progressing short success, zero/prefix exception, fsync1/2/3 failures, original failed-prefix retention и fd-close controls не изменены. Healthy exact-limit65536/full/fragmented, nofollow/nonblock/type/owner/mode/semantic-empty checks сохранены. Production byte-identical; исправлять уже корректный reader для этих test gaps не требуется.

Наблюдения source не доказывают actual root permissions, FIFO/socket hang avoidance, native fsync durability, SSH/Nix/signatures или trusted-root post-freeze integrity. OPS04.N остаётся unknown. Original review wider limits/OPS03/CR04 residuals сохраняются. Exact runtime/environment/selector/source binding и coordinator intent/counter admission ещё отдельный шаг. Поручение сообщает used0/2; reviewer не измерял и не расходовал эти calls, не выдаёт новый budget. Именование RED не требует искусственного failure Platform guards, уже корректных по source.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 readonly-mode mutant различается | Observer206–210 и reader-only calls | Runtime mutation test отсутствует | сохранить |
| R2 EOF больше не скрывает read budget | Sizes65537/65538 × full/997, actual/request/tail assertions233–251 | Source reasoning, не native I/O proof | сохранить |
| T2/write/old guards сохранены | Exact hashes и full patch delta | Ни один тест не исполнялся | сохранить |
| Unit/native/fullrelease/science acceptance получены | Receipts отсутствуют | Exact bind и конечный coordinator run ещё впереди | дополнительно измерить |

**STOP. PASS_SOURCE R1/R2 closure; executions=0.**
