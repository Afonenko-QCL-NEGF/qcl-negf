# OPS04 Platform — independent high narrow compatibility CPP

2026-10-20. **PASS_SOURCE / APPROVE exact single-method compatibility delta: блокирующих замечаний не найдено.** Исправление обновляет stale command fixture под существующий whole-update protocol, сохраняя production guards и отдельный frozen-trust oracle. Это не новый runtime результат: correction GREEN не измерен; Root отдельно решает remaining finite Platform invocation.

## Identity и порядок проверки

Сначала прочитаны actual baseline Platform `deliver_cli/_deliver_cli_locked`, capability/attempt/stop/health/registration/admission/provenance paths, baseline old fixture и существующие `NativeUpdateModel/control_response/Commands/install_controller_config_io`; затем candidate method и exact patch; после source assessment — author report и original FIRST-1 raw/receipt. Никакой author diagnosis не заменял первичное сопоставление.

Фактический HEAD `/tmp/qcl-ops04-platform-worktree` — `b067723c82382689bff5cc366981c56e99b926f8`. Status: только `tests/test_application_release.py`, `tests/test_node_enrollment.py`, ранее разрешённые test changes. Submodule status пуст. Production `ops/application_release.py` SHA256 `1d4422bed5986901ddef22890ca16fe600336e6af2bef17d83ae809ebe794df0`, targeted diff к HEAD пуст/exit0. Root gitlink/tree остаются source authority; этот receipt не revision lock.

| Проверенный input | SHA256 |
| --- | --- |
| tests/test_node_enrollment.py candidate | d99c003fccc308c9cffed172f38ec69eeaa744f2753c7a95c28794d07aca305d |
| tests/test_application_release.py unchanged | 3b39987d1a3e1914ba45c8224af6d600dc92cffa6c030a9feaa955dfb0e326d6 |
| /tmp/qcl-ops04-platform-compat-before.py | 27b733487737501880023dc55607b21c357654821da5a65f53940873c0f0cfe5 |
| platform-compat-patch.diff, 8688 bytes | 63e9dd9abee0943bf7f75b0a951fc795f587602e85fc266e8927ad5d6fa0a033 |
| platform-compat-report.md | c7668e069fca4a5b94a876ab82da856acd148531142cc080e62677d1b9376000 |
| platform-compat-identity.json | 0aec03640157b0a3367162dd3aca1e09bfe0a3c4400c52089456f3f0a399e464 |
| accepted platform-red-v2-review.md | ae225ee188ab7f98c647cdecfa32bf4e6a05d7057639a81c771725fc74510120 |
| PLATFORM-FIRST-1/original.log | 898b0da0c1d550e96b6d719f4e21ce32e0cd4c231937429e45511e3f8aabd1e5 |
| PLATFORM-FIRST-1/receipt.json | a9d239bab5f5cb564b450d7168d3ba0262893c952e33bb7f579519efa73727db |

Independent text diff frozen before→candidate с exact patch labels даёт SHA `63e9dd...`, совпадающий с сохранённым compatibility patch. В нём меняется только `EnrollmentTests.test_source_trust_substitution_does_not_change_late_transport_snapshot:691–804`; shared SyntheticCommands, T2/T3 cases и все другие methods неизменны относительно accepted v2. Application test SHA равен v2. Patch применяется поверх v2 tests/equivalent test commit, не отдельно к baseline b067. `git diff --check` выполнен, exit0; это whitespace check, не Python parser.

## Причинность correction

Original complete raw показывает **1 failed / 15 passed**. Отказ идёт из production `_deliver_cli_locked:2669` через `ssh`/dispatch в old SyntheticCommands, который не знает `update-capabilities`. Receipt exit1/wall1.2s, raw5742 bytes, guard_error/stop_reason null. Это observed stale fixture failure, не production defect. Все дальнейшие необходимости (stop/config/profile/health/registration/finish) выведены из actual source, не объявлены дополнительно наблюдёнными failures.

Candidate сохраняет реальный `ops.deliver_cli`, preflight_controller_authority, enrollment validation/binding, capability exact comparison, lifecycle owner/locks/checkpoints, verify_stop_response, node envelope/registration/provenance checks, controller activation и admission publication. В test не патчатся эти high-level функции и не добавляются success-return обходы. Deferred execution-local import test helpers избегает top-level cycle: test_application_release уже импортирует enrollment facts; новые packages/runtime dependencies не появляются. Сам import reviewer не выполнял.

Низкоуровневый transport теперь выдаёт literal capability/stopped/health/finish command responses из существующих model helpers. Проверяет selected SSH target/sudo prefix/action, decoded selected manifest/expected node и nonempty attempt на mutation/update actions. Данные capability и stopped proof не генерируются production validator. Actual verify_stop_response (`2268+`) продолжает проверять schema, exact attempt, enrollment, machine/config, measured stop fields и effective mask ownership. Actual command args содержат enrollment identity и текущий attempt; test не заменяет их заранее готовым deliver result.

Independent `NativeUpdateModel` моделирует DRAIN/RESUME и daemon generation; activate изменяет model generation до последующих health responses. Controller/current-worker registration, retained DRAIN reason/generation и owned-resume validators остаются actual production code. Existing helper моделирует scheduler command responses, а не вызывает acceptance helper для создания ожидаемого ответа. Его reuse допустим для этой compatibility correction; он не становится вторым независимым oracle update protocol.

В native route сохраняется условие `run is command`: в scope `ops.command` patched ровно на передаваемый transport. Поэтому actual production dispatch строит NIX_SSHOPTS, а test наблюдает именно этот env. Наличие native dispatch branch здесь означает командный fake, не выполнение Nix/SSH.

## Frozen-trust oracle и barriers сохранены

До delivery actual protected reader и freeze выполняются над FakeProtectedFS: independent original bytes → actual frozen path+SHA. При **каждом** последующем callback original source заменяется, frozen bytes остаются original и frozen SHA сверяется с независимым hashlib(original). Actual SSH argv обязаны содержать frozen UserKnownHostsFile/strict checking/no-global file; actual Nix copy env проверяется по exact parsed UserKnownHostsFile token. Последующий read_protected_file запрещён fail-fast trap; final original source-open count не увеличен и original source действительно изменён.

Старые load_enrollment/local-identity/freeze substitutions сохранены. Новый `_process_generation` меняет только boot UUID для synthetic controller consistency, сохраняя реальные PID/start ticks; lifecycle owner не подменён. Existing config-I/O helper перенаправляет только `/etc/qcl-negf/release-config.json` и PROFILE к owned temporary fixture и возвращает cleanup через ExitStack. Профильные symlink/receipt/gate/probe writes остаются actual local code. Это synthetic metadata boundary, не proof root namespace/OS identity.

Command fallback теперь fail-closed: unknown local command/action даёт AssertionError. Перед каждым worker copy assert требует обе stop-update actions; actual production дополнительно требует verified all-worker stop receipts. Full terminal assertions требуют completed/open/no reconciliation, actual receipt trust_snapshot, полный worker_stop/fleet_health inventory, прохождение capability/stop/stopped/activate/check/health/finish для обоих workers, matching receipt attempt и ровно два worker copy. Это отличает завершённый current protocol от раннего capability-only ответа или удаления failing selector.

Эти healthy fixture assertions не являются mutation coverage каждого lifecycle guard. Например, presence/order of command и response, смоделированные общим helper, не доказывают независимо реальный remote stop или native barrier. Здесь source подтверждает, что production validators остаются активны, а отдельный различающий oracle — frozen bytes/SHA/no-reread/transport binding. Author limitation сформулирована явно и сохранена.

## Границы результата

Никакой correction runtime/Python/parser/import/test не выполнялся reviewer. Уже accepted T2/T3 R2 source pass не пересматривается и не расширяется; unchanged hashes/exact single-method delta сохраняют его область. Original failed log/receipt не менялись. Correction не меняет tolerance/physics/model, trust policy, capability или admission schema.

Envelope ≤20min/1CPU/2GiB/read≤4MiB/report≤96KiB. Cumulative CPU/RAM/read/tool-output telemetry не инструментировалась; это порученные пределы. Только text/Git/SHA reads, whitespace diff check и запись review artifacts в `/tmp`. Source edits, target imports/parsers/Python/tests, Nix/build/network/server, children, Git mutations и checkpoint writes — **0**. Platform counter по inputs **1/2**, reviewer slots0; C08 **8/8**, science/fullCI0 — coordinator-owned границы, не новые разрешения. Sole remaining GREEN решает Root после source binding.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| FIRST-1 failure — stale fixture response | Original full raw+receipt; baseline SyntheticCommands vs actual update-capabilities | Дальнейшие runtime outcomes не наблюдались | изменить |
| Correction сохраняет production guards и test scope | Exact single-method delta; unchanged production/T2/T3/shared helper hashes | Source-only assessment | сохранить |
| Snapshot substitution oracle различает late trust reread | Actual initial freeze; per-callback bytes/SHA, SSH/NIX_SSHOPTS token и no-reread trap | Synthetic namespace/model; не real remote/native evidence | сохранить |
| Current protocol имеет meaningful healthy reachability | Actual deliver path, verified barrier code, terminal receipt/action/copy assertions | Reused model не второй независимый protocol oracle | сохранить |
| Correction GREEN/native/science acceptance получены | Новых execution receipts нет | Remaining coordinator gate впереди | дополнительно измерить |

**STOP. PASS_SOURCE exact compatibility correction. Root separately binds source and decides sole remaining finite Platform GREEN; reviewer не запускает проверки.**
