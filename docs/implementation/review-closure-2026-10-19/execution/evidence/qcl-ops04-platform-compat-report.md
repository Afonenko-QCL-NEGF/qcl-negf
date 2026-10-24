# OPS04 Platform compatibility fixture — source correction после FIRST-1

2026-10-20. Изменён только `EnrollmentTests.test_source_trust_substitution_does_not_change_late_transport_snapshot` в `/tmp/qcl-ops04-platform-worktree/tests/test_node_enrollment.py`. Это source-only correction перед независимым high CP-CODE; нового runtime результата нет. Shared `SyntheticCommands`, production, T2/T3 fixture bodies, original failed receipts и main не изменены. Root владеет единственным remaining GREEN call; общий Platform counter остаётся **1/2**.

## Наблюдение, причина и гипотеза

Original `/tmp/qcl-OPS04-PLATFORM-FIRST-1/original.log`, SHA256 `898b0da0c1d550e96b6d719f4e21ce32e0cd4c231937429e45511e3f8aabd1e5`,5742 bytes, complete согласно receipt. `/tmp/qcl-OPS04-PLATFORM-FIRST-1/receipt.json` SHA256 `a9d239bab5f5cb564b450d7168d3ba0262893c952e33bb7f579519efa73727db`: exit1, wall1.2s,1failed/15passed; все новые T2/T3 cases прошли. Это engineering subset, не full CI/science/native acceptance.

Stack проходит `deliver_cli`→`_deliver_cli_locked:2669`→`ssh`→локальный `transport`→`SyntheticCommands.__call__`, который выбрасывает `Unexpected synthetic SSH action` для `sudo -n qcl-negf-release update-capabilities`. Shared helper обрабатывает старые identity/activate/check и несколько Nix/service пустых ответов, но не текущий whole-update protocol.

Source-debug по systematic-debugging: прочитаны full failed output/receipt, actual capability/preflight, worker-stop, controller activation, fleet-health, resume/finish и связанные working fixtures в `tests/test_application_release.py`. Единственная observed failure — missing capability fixture. **Вывод по исходникам:** простое добавление одного capability literal недостаточно: далее нужны controller config/profile/Code/selfcheck, cancellation, stopped receipts, scheduler generations и finish responses. Это не наблюдение новых runtime failures и не диагноз production defect.

Гипотеза исправления: локальный callback failing selector должен моделировать текущий command boundary с теми же независимыми фактами, которые используются существующими current-update tests. Production capability/identity/attempt/enrollment/receipt/stop/health/admission guards остаются активными. Проверка гипотезы runtime отложена до high review и Root GREEN.

## Изменение и полный callback inventory

В test method добавлен execution-local import существующих test helpers; imports сейчас **не выполнялись**. Отложенный import избегает module-initialization cycle: application-release tests уже импортируют enrollment facts. Нет нового package/runtime dependency. Используются `NativeUpdateModel`, `control_response`, `Commands`, `clear_aiida`, `controller_stop_state`, `install_controller_config_io`; никакой production acceptance helper не подменён на pass.

| Callback action | Synthetic ответ / побочный эффект | Guard / ограничение |
| --- | --- | --- |
| SSH identity / update-identity | Literal selected CONTROLLER/WORKER/SECOND facts | Target allowlist, exact sudo prefix; snapshot path/strict/global options проверяются на каждом SSH |
| SSH update-capabilities | Existing explicit v2 capability literal из control_response | Actual production exact comparison остаётся |
| SSH stop-update / stopped-identity | Existing full stopped_response с actual command attempt и enrollment, mask/machine/config/window facts | Manifest и expected node из base64 проверяются; actual verify_stop_response работает; all-worker stop barrier перед каждым copy asserted |
| SSH activate | model.activate(worker) продвигает synthetic generation | Exact selected manifest, expected node, nonempty attempt; remote command не исполняется |
| SSH check | Literal bound envelope, ready selected release | Actual verify_node_envelope остаётся; только command response fake |
| SSH health-update | Existing control_response с NativeUpdateModel.health текущего worker generation | Actual current_worker_health/registration/provenance checks остаются |
| SSH finish-update | Existing explicit attempt_id/marker_removed response | Actual production exact terminal comparison остаётся |
| nix path-info | Exact two selected closure hashes | Exact argv store inventory; нет Nix invocation |
| nix copy --to | Empty synthetic response для exact two worker routes/closures | Exact NIX_SSHOPTS frozen path token; обе stop-update actions до copy; два copy подтверждаются в конце |
| UTC/UID/name/squeue | Existing literal timestamp/operator/empty queue facts | Exact argv matching; no shell/process |
| scontrol show/update | Existing independent NativeUpdateModel scheduler state transitions | Model requires explicit UTC/SLURM_CONF argv; records DRAIN/RESUME и generation |
| systemctl show/stop/start/restart/is-active | Existing stopped controller unit facts или synthetic successful command | Known unit allowlist; не native status |
| findmnt | One synthetic NFS4 record selected gate directory+configured source | Actual fleet-health parser и local own probe выполняются при будущем тесте; реального NFS нет |
| runuser AiiDA check | Existing explicit empty-root/CalcJob cancellation proof | Actual two-workflow cancellation validator остаётся |
| nix-env | Existing Commands creates profile symlinks только в owned TemporaryDirectory | Assert profile parent exact temp; реального Nix нет |
| nix-store verify | Empty command response для exact selected two paths | Не доказывает store contents/signatures |
| runuser register / timeout self-check | Existing Commands returns literal Code UUID/solver identity и completed, scientific_accepted:false | Нет AiiDA/Julia execution; production response validators остаются |
| Любой иной command/action | AssertionError | Нет blanket fallback success |

`install_controller_config_io` перенаправляет только `/etc/qcl-negf/release-config.json` к owned temporary fixture и PROFILE к temporary path; cleanup ограничен ExitStack. Это существующий metadata boundary pattern, не root namespace/permission proof. `_process_generation` сохраняет реальные process PID/start facts, заменяя лишь boot UUID на synthetic controller UUID, как existing current-update tests; lifecycle owner/locks/receipts не отключаются. Ранее подменяемые load_enrollment/local identity/freeze сохраняются.

## Сохранённый и усиленный oracle

Сохранены initial actual protected-reader/snapshot calls под FakeProtectedFS; original snapshot bytes/SHA проверяются на **каждом** callback после source substitution; unchanged source-open count и substituted original source проверяются в конце. Поздний `read_protected_file` теперь fail-fast trap, чтобы ни один protected source не перечитывался после freeze. Проверки обоих SSH и NIX_SSHOPTS сохранены, Nix option проверяется точным parsed token.

Добавлены terminal completed/open/no-reconciliation, actual receipt trust snapshot binding, полный worker-stop/fleet-health inventory, per-worker capability/stop/stopped/activate/check/health/finish reachability, stop attempt identity и ровно два native-model copy. Эти assertions требуют пройти current protocol, а не удалить failing selector или ограничить его ранним capability ответом.

Ограничение независимости: control_response и NativeUpdateModel повторно используются с другими operational tests; compatibility fixture не является вторым независимым oracle этих protocol responses. Его отдельный oracle — frozen bytes/SHA/no reread/transport binding. Реальная OS identity/Slurm/systemd/NFS/Nix/AiiDA/Julia/remote behavior не проверяется этим source delta.

## Source identity и проверка

Owning isolated HEAD/base неизменён `b067723c82382689bff5cc366981c56e99b926f8`. Coordinator main test commit `cb0e7be` — контекст; main не читался/менялся этим исправлением. Start/end status содержит только прежние два modified test paths; recursive submodule status пуст. Exact delta получен относительно frozen v2 enrollment bytes, SHA256 `27b733487737501880023dc55607b21c357654821da5a65f53940873c0f0cfe5`, сохранённых в `/tmp/qcl-ops04-platform-compat-before.py`.

- `/tmp/qcl-ops04-platform-compat-patch.diff`:8688 bytes, SHA256 `63e9dd9abee0943bf7f75b0a951fc795f587602e85fc266e8927ad5d6fa0a033`; это **только compatibility delta**, применять поверх v2/его main test commit, не base b067 отдельно.
- Candidate `tests/test_node_enrollment.py`: SHA256 `d99c003fccc308c9cffed172f38ec69eeaa744f2753c7a95c28794d07aca305d`.
- Unchanged application tests SHA256 `3b39987d1a3e1914ba45c8224af6d600dc92cffa6c030a9feaa955dfb0e326d6`.
- Unchanged production SHA256 `1d4422bed5986901ddef22890ca16fe600336e6af2bef17d83ae809ebe794df0`.

Выполнены text/Git reads, полный просмотр exact correction diff, `git diff --check` exit0/пусто, hashes/размеры. Новые executions/imports/parsers/Python/tests/network/native/children/Git mutations:0. Resource envelope≤15min/1CPU/2GiB/read≤3MiB/output≤96KiB; cumulative resource telemetry не измерена.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| FIRST-1 отказал на stale capability fixture | Original full log+receipt SHA выше | Не доказывает дальнейшие runtime outcomes | изменить |
| Snapshot oracle сохранён при current delivery protocol | Exact single-method delta и callback inventory | Source-only, reused test model | сохранить |
| Исправление прошло GREEN | Receipt отсутствует | Platform использован1/2; Root исполнит remaining call после high CP | данных недостаточно |
| Production/new T2/T3 менять требуется | Нового production failure не выявлено; targeted source unchanged | Ограниченный engineering subset | сохранить |

**STOP** перед независимым high CP-CODE. Original failed artifacts неизменны, новый runtime slot не расходован.
