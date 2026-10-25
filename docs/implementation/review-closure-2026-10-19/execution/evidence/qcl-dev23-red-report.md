# DEV23 tests-first packet — до RED invocation

Этап: реализация tests-first, только source/test authoring. Runtime/import/test invocations автора: 0. Root — единственный исполнитель общего L-PY envelope. Production code и README не изменялись; semantic RED release ещё не получен.

## Immutable inputs и output

Managed root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, observed root HEAD `7d179b28647f0b89347d2d6358f08cf2fe479653`.
AiiDA branch задан координатором `codex/review-closure-cancellation-contract`; HEAD `5579d55684939495230241f446b7ea07c8ae0224`, исходно clean. Root содержит разрешённые изменения других потоков (Runner, Portal, Platform/checkpoint/evidence); они не редактировались. Original `/home/tolya/Загрузки/qcl-negf` не изменялся.

Проверены root AGENTS.md, docs/architecture.md, component CONTRIBUTING.md, DEV23 development card; skills TDD + writing-good-tests и receiving-code-review. Архивы/solver/profile не исполнялись.

| Файл | SHA256 |
| --- | --- |
| AiiDA src/aiida_qcl_negf/service.py (без изменений) | `5cd701303c1c5416c5c593ecc6574e9e2bcdbddc35cca900d001ba06cc835cd5` |
| tests/test_cancellation_contract.py (новый) | `8b276505d190811526bd6d308acb09bf0b00317c36be14a92861236141204809` |
| tests/test_restart.py (candidate) | `eaf3b5e78cce5e8dc1ca7a919b299a76443bb5dab3fed584010b523a65c1ad70` |
| tests/test_submission_identity.py (без изменений) | `2a16bf11fd6f5404897ec367acd72f59ace09ef0597e27e5da5712c635efab5d` |
| /tmp/qcl-dev23-tests.patch (new-file diff) | `bd0394c50974c07cde3f468438c10f41ed84230c4a33e2eae9317f9064ccf16d` |
| /tmp/qcl-dev23-restart.patch | `de774edae6e38f17b30da10dfad889e74f8935c2b9de6490ebcb71e7fa8fa83d` |

`git -C components/qcl-negf-aiida diff --check` выполнен, exit 0, output 0. Untracked cancellation file дополнительно отражён отдельным no-index patch; это статическая проверка, не pytest/RED.

## Отличающие assertions

Настоящий owning `aiida_qcl_negf.service` импортируется тестом; локатор `service.__file__` связывается с selected component. Нет sys.modules/module stubs, нет mock `kill_run` или `_summary`. Подменены только ORM lookup `_node`, daemon client и dispatch `kill_processes`, необходимые для исключения profile/daemon/native процесса. Forbidden sentinels запрещают `submit`, `submit_plan`, `plan_data`; teardown проверяет нулевой count даже на ожидаемой ошибке. Fixture не устанавливает настоящий scheduler-stop и не доказывает native child kill/staging.

- daemon_down: RuntimeError, нет dispatch/refresh, исходный running state сохранён.
- unconfirmed: RuntimeError после единственного dispatch и refresh, terminal/killed state не фабрикуется.
- refresh_confirmed: literal summary относится к новому terminal `finished/301` node с новым mtime, не stale running и не fabricated killed.
- exception redaction: synthetic private broker OSError на daemon/dispatch/refresh; public `str(RuntimeError)` не содержит fake secret/address/vhost, нет второго dispatch/новой работы. Private chained cause не считается public message; полный log sanitization вне scope.
- already_terminal: killed/400, finished/301, finished/0 возвращаются без daemon lookup/kill.
- исходные десять attempt_decision cells полностью сохранены. Дополнительные 301/303/305 cells запрещают инфраструктурную классификацию scientific terminal независимо от отсутствующих stopped/recovery proofs.
- исходный test_submission_identity не менялся: exact descriptor/--no-requeue и immutable executable guards сохранены source-wise; integration runtime не выполнен.

Ожидается 9 cancellation cases + 3 новых retry cells (не фактический collection receipt).

Source-derived RED hypothesis, не observed failure: текущий service.py:556 `get_daemon_client()` и :562 refresh `_node` находятся вне exception handler (:558–561). Поэтому daemon/refresh OSError могут выйти без RuntimeError/redaction; dispatch branch уже корректно wrapped. Root обязан отдельно подтвердить semantic RED с реальным owning import; автор не изменяет production до этого подтверждения. Если результаты расходятся — сначала исправить тестовый/identity/setup дефект, не ослаблять контракт.

## Read-only Runner budget audit

Observed Runner HEAD `2d0190d5573f74d847d92a0dac8dd6ec524d494c`.
`test/infrastructure/production_restart_validates_metadata_and_restores_state.jl`, SHA256 `1c9afcba2c6c0f0cb683230f572974bdbc67b128885f541399e3867bae1d6b9a`: lines145–149 сохраняют history20 и arithmetic remaining60; lines150–169 действительно вызывают solve_scba_production с restored history20, max_scba20 и assert history не растёт/status max_iterations. Это source evidence исчерпанной границы, не измеренный runtime.
`test/application/restored_stage_progress_consumes_the_original_budget.jl`, SHA256 `236dbcae0259c9e6175de49310cf0ac267d34df20b835e803c747380f0a3d23c`: lines11–14 только _begin_solver_stage event20/80 и remaining60. Не выполняется положительный remaining loop.

Новый отдельный Runner D ticket нужен для различающего full-loop assertion: восстановить same-stage history20 при frozen max_scba80, гарантированно не завершить сходимостью преждевременно manufactured oracle, доказать что исполнено максимум60 дополнительных итераций, final logical ν<=80 и history не сброшена к0; отдельно определить outer-loop и final-alignment applicability. Требуется новый конечный runtime budget/SCI scope; эта карточка не добавляет solve. Native all-process stop, Slurm/proctrack и final staged receipt остаются OPS gates.

## Необходимая prose (автор README не пишет)

После отдельного ultra-design README должен сказать: kill_run возвращает observed refreshed terminal parent summary, а ошибки daemon/dispatch/unconfirmed/refresh не подтверждают cancellation. Summary не доказывает native all-process stop либо final staging. Не добавлять auto-retry, second-submit, idempotency store, default retry expansion.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Основные cancellation ветви защищены новым actual-service fixture | new test source + patch hashes | pytest ещё не выполнялся | дополнительно измерить |
| Два backend exception пути могут раскрыть private error | service.py:556,562 и literal OSError tests | source hypothesis; RED отсутствует | дополнительно измерить |
| finite retry и exact submit marker guards сохранены | existing ten cells, immutable submission test hash + new scientific terminal cells | native/integration runtime отсутствует | сохранить |
| remaining60 event доказывает полный numerical cap | событие lines11–14 не выполняет loop; exhausted boundary150–169 уже есть | positive remaining-loop proof отсутствует | данных недостаточно |

STOP: передать root пакет; никакой production repair до semantic RED release, никакого самостоятельного runtime/Git mutation.
