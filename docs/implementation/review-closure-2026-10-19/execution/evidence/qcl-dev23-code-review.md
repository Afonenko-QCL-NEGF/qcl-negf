# DEV23 — независимый CP-CODE и README review

Вердикт: **CP-CODE spec/quality PASS** для указанного AiiDA candidate и README. Блокирующих замечаний нет. Это source/fixture review, не native-stop, staging, full-release или scientific acceptance.

Reviewer `/root/dev23_reviewer`, 2026-10-19. Этап: независимый анализ, только чтение; единственная запись — этот отчёт. Project execution/import/tests, Git, daemon/profile, solver, Slurm, network и изменения owning source не выполнялись. Component baseline `5579d55684939495230241f446b7ea07c8ae0224`, branch `codex/review-closure-cancellation-contract` предоставлены координатором, не выдаются за самостоятельно снятый Git receipt. Root HEAD/status/gitlinks остаются у root executor.

## Порядок и immutable inputs

Сначала прочитаны root AGENTS/architecture, component CONTRIBUTING, handoff/development DEV23, существующие service API/README и actual service/workflow/tests; затем primary patch и RED/GREEN receipts/raw. Отчёты авторов прочитаны после собственного source анализа. Исходники не импортировались. Исходные и конечные SHA256 service/README/cancellation fixture совпали.

| Артефакт | Проверенный SHA256 |
| --- | --- |
| `src/aiida_qcl_negf/service.py` | `5f7e9b28f9007255e3de319fff43e48143d4c23a9c9487164ecda92ebac8c762` |
| `tests/test_cancellation_contract.py` | `8b276505d190811526bd6d308acb09bf0b00317c36be14a92861236141204809` |
| `tests/test_restart.py` | `eaf3b5e78cce5e8dc1ca7a919b299a76443bb5dab3fed584010b523a65c1ad70` |
| `tests/test_submission_identity.py` | `2a16bf11fd6f5404897ec367acd72f59ace09ef0597e27e5da5712c635efab5d` |
| `README.md` | `490e49b686047d45d64b20f61984506bd3d48dd8c8f1227d6477a4b7f6ab96fb` |
| `/tmp/qcl-dev23-full.patch` | `dd30d5e29b648ee122d035ef75f2a09cb3a7351db53c6b6cb07cd4d1945c61a3` |
| `/tmp/qcl-dev23-docs.patch` | `bdc75ea725e966f8e82c3ce4f8c45f4598cbe70adee1b25f2ce9be8f46335c6f` |

## Независимые выводы

1. `service.py::_node` (строки 45–56) и initial admission в `kill_run` (553) не меняются: invalid UUID остаётся ValueError, absent/foreign workflow — LookupError. Already-terminal fast path (554–555) не обращается к daemon. `kill_run` сохраняет сигнатуру и summary schema.
2. В `kill_run` (556–570) daemon client/property failure теперь получает generic cancellation RuntimeError; dispatch и единственный post-dispatch `_node` refresh входят в тот же safe exception boundary. Daemon-down остаётся отдельной ошибкой. Timeout10, один dispatch, отсутствие retry/submit и nonterminal refusal сохранены. Единственная success ветвь после dispatch требует `refreshed.is_terminated` и возвращает настоящий `_summary(refreshed)`. Finished/301 сохраняется finished/301, killed status не фабрикуется. Возврат `kill_processes` сам по себе не принимается за подтверждение: прочитанный установленный `aiida/engine/processes/control.py::_resolve_futures` допускает логирование неуспеха без raise, что делает terminal re-read необходимым.
3. Девять cancellation cells вызывают actual owning `service.kill_run` и `_summary`; path assertion исключает другой checkout/wheel. Подменены `_node`, daemon client и dispatch, не проверяемая функция или summary. Literal finished/301 summary содержит новый mtime и отличает refreshed от stale running node. Event sequences различают no-dispatch/down, single-dispatch/unconfirmed и refresh-before-return. Fault matrix daemon/dispatch/refresh проверяет публичный `str(RuntimeError)` на synthetic secret/address/vhost; forbidden submit/submit_plan/plan_data sentinels проверяются и в teardown. Это содержательные assertions, не mock-call-only pass.
4. `test_restart.py` сохраняет исходные десять eligibility cells и добавляет 301/303/305 без stopped/recovery proof. `workflow.py::attempt_decision`, finite defaults/validators/max_iterations, `submit_plan` и `calculation.py` не входят в production diff. Неизменённый `test_submission_identity.py` проверяет exact descriptor, `--no-requeue`, immutable executable и ordering release guard до solver. Presubmit создаёт scripts, не исполняет их. Selected fixtures не запускают synthetic solver/daemon/Slurm.
5. Cancellation не вводит second submit или idempotency store. Lost-ack fence остаётся owning Portal DEV12/13: source `qcl_negf_api/service.py` MUTATIONS/admission/dispatch fences и `test_actor_deadlines.py::test_blocked_call_returns_unknown_without_duplicate_submit` сохраняют один backend submit. Этот Portal packet не выполнялся reviewer и не входит в DEV23 GREEN; отдельная DEV13 приёмка не наследуется.
6. README `Cancel a run` (159–179) точно описывает observed terminal parent, already-terminal path, unknown errors, initial lookup semantics и отсутствие автоматического повторного submit после lost acknowledgement. Ссылки на `docs/service.md`, `service.py`, `workflow.py` разрешаются в прочитанные файлы. Явно разделены parent terminal, native all-process/Slurm proctrack stop и final staging/recovery receipt; claims об измеренной native отмене отсутствуют. Документация соответствует узкому diff.

## Runtime evidence и ограничения

Прочитаны сохранённые root receipts, повторных запусков нет:

- RED-1: **7 passed / 2 failed**, semantic failures daemon/refresh OSError, raw 3494 bytes complete; receipt SHA256 `065d0af00b389f782242cf2a103469cd466348e80f96b344b7e2315b03158dd3`, raw `01195ffe706ed1c7f612961a2cba4daffe09c6cb23e0c9942bec19e93feada99`.
- GREEN-1: **29 passed / 10 warnings**, exit0, wall4.698s, sampled tree RSS163184640 bytes, sampled TMP736459 bytes, raw3475 bytes complete, no guard/overrun/stop. Receipt SHA256 `b5f8f6bac2946f35aebea77ef4c4d86e366e8eb183d474409a84af66841d0f1c`, raw `8d9150b6be7f9883db58db9c503227702e57e77c48361d792e590274fdf191b0`.

GREEN fixture hashes совпадают с reviewed candidates. Runtime identity/import ownership и отсутствие изменения service между root invocation и snapshot опираются на packet координатора; GREEN receipt сам перечисляет fixture hashes, не service hash. Sampling50ms не доказывает transient peaks или hard quotas. Warnings относятся к временной AiiDA configuration и SQLAlchemy bookkeeping, не scientific outcomes. Reviewer не повторял runtime и не объявляет full suite pass.

Public-safe scope — exception type и публичный `str`, не полная цепочка traceback/log sanitization: private cause намеренно сохранён через `from exception`. Initial backend lookup и summary storage failure не получили нового глобального redaction contract. Native daemon timing, ORM refresh semantics на целевом deployment, descendants/proctrack stop и staging требуют отдельных OPS receipts.

Runner read-only follow-on подтверждён независимо: `production_restart_validates_metadata_and_restores_state.jl` SHA256 `1c9afcba2c6c0f0cb683230f572974bdbc67b128885f541399e3867bae1d6b9a`, строки145–169 — history20/remaining60 arithmetic плюс exhausted max_scba20 solve source. `restored_stage_progress_consumes_the_original_budget.jl` SHA256 `236dbcae0259c9e6175de49310cf0ac267d34df20b835e803c747380f0a3d23c`, строки11–14 — event20/80/remaining60, без positive remaining loop. Full-loop cap не доказан и не входит в PASS: нужен отдельный Runner D контракт/конечный бюджет для history20→не более60 новых итераций при frozen max80, с outer/final-alignment applicability. Julia не запускалась.

Author reports прочитаны последними и совпадают с наблюдениями: implementation `16248556c3ee07ee67a0e39514b86a5086adf4ddbd43b53c10dd43591c8d2f18`; docs `277a65208321e5f935bceecbd6dea18b31ac2ecb865af3f11e228a762911996e`; tests-first `14ff3ee24516bac4e600c8236e491a9219c61d38f37abd90dc8cd2981fd25a88`.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Truthful cancellation и public-safe known fault paths закрыты | Reviewed exact service/test hashes, semantic RED и GREEN29 | Synthetic ORM/daemon/dispatch; public str scope | сохранить |
| Finite retry, immutable submit markers, no-second-submit не расширены | Narrow diff; old10+new3 retry cells; unchanged submission tests; Portal fence source | Portal runtime gate отдельный | сохранить |
| README честно описывает текущую поддержку | Exact README hash и строки159–179 vs actual service | Native-stop/staging receipts отсутствуют | сохранить |
| Native all-process stop/final staging приняты | В этом packet нет таких receipts | OPS gates остаются открытыми | данных недостаточно |
| Positive remaining-loop numerical budget доказан | Только arithmetic/event60 и exhausted-boundary source | Нужен отдельный Runner D/finite runtime scope | дополнительно измерить |

STOP: source и README review завершён; publication/Git/PR и дальнейший runtime — у координатора в его grants.
