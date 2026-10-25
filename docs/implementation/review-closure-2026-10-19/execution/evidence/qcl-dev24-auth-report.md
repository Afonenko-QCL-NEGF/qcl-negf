# DEV24-AUTH-COUNTERS — I, frozen test-only handoff

Этап: узкое изменение теста по READY контракту из `/tmp/qcl-dev24-first-review.md`
SHA256 `0a1255c3870792a830887e363b9ea514756f24376af593c6f7c0886cd94a2eea`.
Root HEAD `965ebed95d2b627423805d10c46d0ae8dd425e9d`; исходный root status:
` m components/QCLNEGF.jl`, ` M docs/implementation/review-closure-2026-10-19/execution/checkpoint.json`.
Эти файлы не изменены этим автором. Все восемь выбранных gitlinks прочитаны.
Portal HEAD `d28d076c83611278153752d94cc3729d91b32667`, исходно clean detached.
Создана новая ветка `codex/review-closure-rejection-controls`; существующей ветки с таким именем не было.

Изменён только `tests/test_api.py`: добавлены 52 строки, старые функции/fixtures/assertions
не редактировались. Новый nodeid:
`components/qcl-negf-portal/tests/test_api.py::test_rejected_bearer_never_reaches_service_facade`.
Из Portal cwd: `tests/test_api.py::test_rejected_bearer_never_reaches_service_facade`.
Параметры: 7 routes × 2 credentials = 14 cases, каждый содержит healthy control.

| Route | Healthy status | Exact ordered facade calls |
| --- | --- | --- |
| GET /api/v1/runs | 200 | list_runs |
| POST /api/v1/runs | 202 | submit_plan |
| GET /api/v1/runs/{RUN}/artifacts | 200 | list_artifacts |
| GET /api/v1/runs/{RUN}/artifact | 200 | get_artifact_metadata, open_artifact |
| HEAD /api/v1/runs/{RUN}/artifact | 200 | get_artifact_metadata |
| POST /api/v1/runs/{RUN}/artifact/authorize | 200 | get_artifact_metadata |
| POST /api/v1/runs/{RUN}/kill | 200 | kill_run |

Отказ: один запрос missing/wrong bearer, немедленно401 и точный `facade_calls == []`.
До этой проверки счётчик не очищается. После неё отдельный healthy request с AUTH
должен вернуть указанный статус и точный список; каждое релевантное имя ровно один раз.
Все callable public members существующей synthetic fixture обёрнуты, включая payload opener.
Wrapper записывает попытку ДО вызова delegate, поэтому delegate exception не скрывает dispatch.
Существующий synthetic submit/kill не обращается к внешнему процессу/профилю/job.
`create_app` и HTTP маршруты настоящие, service injection synthetic. Это свидетельство
request→facade boundary; реальный AiiDA actor не создаётся и не проверяется.

Статическая mutation-гипотеза: удаление auth/перенос обращения к facade перед auth
нарушит zero-counter assertion даже если backend выбросит исключение; удаление dispatch
у healthy route нарушит ожидаемую последовательность. Runtime mutation checks не выполнялись.

Статические проверки: `git diff --check` exit0; diff единственного файла содержит только
52 добавленные строки; после удаления ровно нового блока `cmp` baseline/stripped exit0.
SHA256 baseline/stripped одинаков:
`55efd325a3a3c97a8799a6eec8341c6eeaf78e8b0c18a3ec740b23ed1c9ebb9e`.
Новый файл: `88d91cb17904398618bc79b92cbae956c91603075ad2cc1cbd5b27893d810c8d`.
Patch `/tmp/qcl-dev24-auth.patch` SHA256:
`abc71cb89bdfff370243b86296d9f2677f879e1f818f1e246a1d2ea1acdf719f`.

Ни runtime/import/test, ни build/solver/server, ни commit/push не выполнялись.
TDD red/green не измерен: по прямому заданию последний DEV24 runtime call зарезервирован
корневому агенту после freeze и независимого CP-CODE review. Full suite, native TLS,
real actor, security/scientific acceptance не заявляются. Product fix/design не потребовался.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Только additive test change | diff52+, cmp baseline/stripped, file hashes | Статическая проверка | сохранить |
| Структура покрывает missing/wrong bearer и healthy dispatch controls | Новый nodeid, 7 route literals, wrappers до delegate | Runtime ещё не выполнен | дополнительно измерить |
| Реальный actor/native/science принят | Таких измерений нет | Synthetic facade scope | данных недостаточно |

Freeze: автор остановлен после этого handoff. Следующий шаг корневого агента:
независимый CP-CODE static review, затем единственный оставшийся targeted DEV24 call
нового nodeid и двух заранее выбранных export cache functions. Повторных запусков
этот автор не выполняет.
