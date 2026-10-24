# DEV13 author receipt — frozen GREEN-1, runtime pending

Этап: реализация принятого DEV12v2 software lifecycle. Medium implementer,
отдельный ultra author владел docs/actor-lifecycle.md и README. Я эти docs не
менял. Root — единственный Git operator; stage/commit/push/branchswitch = 0.

## Source и frozen inputs

Рабочий checkout `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
При начале root HEAD `04eecba1ea795a7c8861c4bfd0bb5aa49f093ee6`, Portal
`6ff9f6100623c578028506d43a39972dbfbc00dc`. Root git status/recursive gitlinks
прочитаны; Results independently advanced, Core untracked prep и checkpoint
не затрагивались. До GREEN root опубликовал только independently approved docs:
Portal теперь `fa80b5b5920dc16dfb911d164939b3d23e6be186`.

Accepted design `/tmp/qcl-dev12-design-v2.md` SHA256
`fa3ca630f7b44ef9d72582ff91ced2e0c671f0986cecb4e20cddf5b294255712`;
independent v2 review SHA256
`e55a503c0a01bbfdd171d6681ff0299c614ea554bcb3c93e317b08fe273c3da5`.
Прочитаны AGENTS/architecture/Portal contributor docs, handoff README/autonomy/P1,
DEV12/DEV13, RV05/RV12 и actual AiiDA service mutation/selection boundaries.

RED snapshot `/tmp/qcl-dev13-red.diff` SHA256
`6f1a99f6462c47cf7406daefb4de30952db431a19e0c791eade61cbab516a67e`.
Root reported RED-1: 11 missing-interface Settings TypeError failures,
47 passed, включая все4 reconciled ASGI finite cells. Raw original
`/tmp/qcl-DEV13-RED-1/original.log`; wall4.965s RSS164093952/log15808B.
Это RED отсутствующего interface; не observed behavior failure нового actor.
После root explicit release начаты product edits.

Frozen CODE/TEST packet `/tmp/qcl-dev13-green1.diff` SHA256
`7ace94cc51e485340e8812f9cca2ba02eb7d2c6735a94660b6bce67bf14fecc3`.
Green selection: tests/test_actor_deadlines.py, tests/test_service.py,
tests/test_stream_disconnect.py, tests/test_exports.py, tests/test_api.py.
Root centrally owns runtime slot/budget; результат GREEN-1 на момент receipt
не получен. Никаких project imports/pytest/build/install/SSH/solver самостоятельно.

## Implementation / accepted contract mapping

| Contract | Source locator | Prepared fixture evidence (not runtime pass) |
| --- | --- | --- |
| Exact result/errors/settings/defaults, no credentials placeholder | service.py types63–134; settings.py ACTOR_DEFAULTS/__post_init__/from_environment | six direct invalid domain cells |
| One owner/loop/profile, bounded deque, atomic queued→running deadline | AiidaService::_admit/_wait/_owner_main, process OWNER_GUARD | existing one-owner control retained; queued expiry/no replay; cap1 refuses next operation and accepts close; init deadline retains owner guard |
| Unknown mutation and sticky first-receipt fence | _wait, _owner_main mutation exception wrapper, _receipt | submit deadline no duplicate; backend ValueError/RuntimeError categories; late return restores GET but kill remains fenced |
| Bounded lease wait, late-open cleanup, once-only owner exit | _ArtifactReader/_release/_execute/_exit | blocked read while release unset; late open never publishes proxy; repeated close; owner exit count |
| Truthful stopping/actual cleanup terminal, no wait=True | close/_owner_main/_owner_returned | close while backend stalled; existing unload/loop close owner assertion retained |
| Store independent lifecycle latch, timed optional snapshot | ExportStore::close/_request_maintenance | separate _storage and create disk_usage Event stalls prove old store lock occupied, stopping/None counts/root retained |
| Coalesced existing worker, TTL marks/accounting, FS outside store lock | _cleanup/_maintain/_remove_directory/_finish | TTL-rmtree Event stall, one maintenance submit, old lock available, held local download file retained, directory/root once claims; cleanup failure retained reservation/no retry |
| No ready after stopping, cooperative preparation cancellation | _prepare/_progress | existing shutdown progress callback retained; worker root cleanup deferred |
| Shared lifespan absoluteD, actor closes in finally | api.py::lifespan | export close stopping/failed/raised cells, sameD + actor called |
| Safe HTTP categories/detail-string/unknown headers | api.py::actor_error/export_call/invoke/invoke_agent_report; exports::_selection_call | report unknown404/422/503 redaction, no auto retry header, new refusal ID vs original unresolved ID |
| Existing finite disconnect and exact producer binding | test_stream_disconnect.py selection/inventory/plan fake | all4 existing ASGI2.3/2.4×artifact/export bodies65536/retainedresponse/actual closed/readers0 assertions preserved |
| Stalled cancellation cleanup | test_actor_deadlines.py::test_disconnect_releases_handle_exactly_once_after_backend_returns | both spec versions retain ClosingStreamingResponse; external task cancellation after backend-start, in-flight next wait finite, backend exit deferred |

Existing expiry-directory `not exists` assertion preserved, with FIFO worker
barrier establishing actual deletion before assertion. No test assertion removed.
Stalled ASGI control exercises caller task cancellation while backend read is
running; finite full app controls remain the original four protocol cells.
It is not an OS network disconnect, real NFS/AiiDA latency or backend termination
measurement.

## Source checks and limits

AST parsing all Portal source/tests passed without importing project code;
`git diff --check` passed. Source Ruff service.py/settings.py/exports.py/new
actor fixture passed. Initial broad selected lint additionally found 3 inherited
E501 in api.py lines407/414/441; these untouched lines remain and a broad lint
pass is not claimed. Formatter applied only new service.py/new actor fixture;
Ruff import fixes only service/settings/newfixture. These source checks are not
pytest packets; root records their resource scope separately.

No mutation of AiiDA source/frontend/docs/locks/scientific contracts. No thread
kill, process supervisor, automatic submit/kill/reset/retry, hard process-exit
claim, protected S01 or server state operation. Operational diagnostics use
bounded scalar metadata; known mutation original exception retained as cause,
HTTP error details use generic validation text and uncertainty suffix/headers.
Native backend/process may continue after CloseResult(stopping).

## Frozen per-file hashes

| Portal path | SHA256 |
| --- | --- |
| src/qcl_negf_api/service.py | 528b4676ae711aa3b041b4fb3f05f3851b02d0d01cfd9fd8fb5463772aa1a692 |
| src/qcl_negf_api/api.py | d324a9188d8b4f0b3a8bea5de38a0aa3891949a8f0b924c12790711496ea5e63 |
| src/qcl_negf_api/exports.py | 1116d3717b8cafdd51278a60b0eff5887d49e66609a5086ade535848250351a8 |
| src/qcl_negf_api/settings.py | fc8986ec7d06a25b261517d458162438eba9096a6f2f1d8d3f04f71b10c3897c |
| tests/test_actor_deadlines.py | 4c95b540aae3d000b9d321ebbd3cc0f2a8ea1510a2e57dd40d44052da148d3a2 |
| tests/test_api.py | 55efd325a3a3c97a8799a6eec8341c6eeaf78e8b0c18a3ec740b23ed1c9ebb9e |
| tests/test_exports.py | d5bc95bd27346030cab6f60681fd21580b8ea2d70abb3757562e4bd1ed40ac8a |
| tests/test_stream_disconnect.py | 356a5dd71638b0207f9fcd4ab995b587ef7a3c0338706d9ea1ae023133b109b0 |

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Owning implementation frozen for review | GREEN1 diff/hash + accepted design mapping | Авторский source report; independent CP-CODE ещё нет | дополнительно измерить |
| Initial RED established missing interface | root RED1 11failed/47passed receipt | Не поведенческая проверка новой реализации | сохранить |
| All finite compatibility/fault cases pass | Runtime receipt отсутствует | GREEN pending centrally bound slot | данных недостаточно |
| Actual backend/process completion bounded | Такого свидетельства нет; stopping explicitly returned | Thread architecture/OS I/O может удерживать процесс | данных недостаточно |
| Scientific/CI/release acceptance achieved | Не выполнялось | Эта карточка только Portal software lifecycle | данных недостаточно |
