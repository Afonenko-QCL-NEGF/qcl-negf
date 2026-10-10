# CR01: точный locator артефакта

Изменение размера, Range и содержимого между разными attempts устранено в owning AiiDA и Portal.
Источник baseline — gitlinks root `24b6dc1`; состав результата определяется gitlinks интеграционного
commit, без отдельного lock-файла ревизий.

Owning draft PR: [AiiDA #3](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/pull/3),
[Portal #5](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/pull/5).

AiiDA `service.py:get_artifact_metadata` выбирает один retrieved CalcJob и читает его complete
cached inventory без payload/repository I/O. Portal разрешает shortcut один раз, возвращает URL с
attempt и CalcJob UUID и связывает с ним scoped cookie. GET/HEAD/Range и opener используют тот же
child даже после изменения published selection. Browser передаёт оба selectors и использует
возвращённый native URL; список показывает attempt. Светлая тема сохранена.

Новый Portal требует coordinated AiiDA operation. Bearer shortcut и legacy single attempt
поддержаны; download cookie требует точного возвращённого URL. Потерянный или изменённый selector
отклоняется до metadata/payload access.

## Проверки и ограничение свидетельств

Проверки выполнены локально с existing native Python и cached test dependencies по owning `uv.lock`;
установка окружения, сервер, CI и scientific solver не запускались. Для async fixtures явно загружен
`anyio.pytest_plugin`.

| Проверка                                        | Результат                                                                                     |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------- |
| AiiDA targeted locator                          | 20 passed                                                                                     |
| AiiDA full pytest                               | 128 passed, 193 warnings, 31.29 s                                                             |
| Portal full pytest                              | 57 passed, 3.14 s; включая 10 export и 4 disconnect cases                                     |
| Frontend existing Node 24 dependencies          | 5 passed; TS без diagnostics; Vite build успешен                                              |
| Независимое чтение frozen diff, fixtures и logs | actionable findings отсутствуют                                                               |
| Diff/secret audit                               | формат корректен; known patterns/configured sensitive literals и private endpoints не найдены |

Original logs сохранены локально. SHA256 full logs:

- AiiDA: `62c40856a45435eec36189e7627b31453708b4c54e770a7d947bc90dd56c6a82`.
- Portal: `c94fe04f46db5a415f834f9134a1f7f40d751f8c17b79632d7bfe9601475bc98`.
- Frontend: `9f048b450ce5aa67b56c7b32c5ae04bd76b2117bc6ca2a77689db63582eff922`.

Исходные failed attempts сохранены: AiiDA два ошибочных CWD/edit вызова и meaningful RED; Portal
sandbox TestClient stall, несовместимый Node 26 и meaningful RED. Один промежуточный backend GREEN
имел два ошибочных shared export-fixture assertions; исправлен guard только для raw artifact, затем
единственный full Portal прошёл. Async plugin configuration исправила четыре environmental errors в
RED. Эти попытки не считаются pass. AiiDA использовал 4 targeted + 1 full; Portal после явного
budget ruling — 6 targeted + 1 full; frontend полный existing-dependencies check выполнен один раз.

AiiDA warnings о temporary profile и SQLAlchemy session сохранены и не подавлены. Frontend log
содержит aggregate success, без отдельного persisted TS exit receipt. Live DOM duplicate-row test и
combined real actor disconnect integration не выполнялись; actor ownership и ASGI closure проверены
отдельно. Cached inventory доверяется parser; payload integrity scan не выполнялся. Неизвестные
secret formats не исключаются одним pattern scan.

| Утверждение                                          | Свидетельство                                                                    | Ограничение                          | Решение             |
| ---------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------ | ------------------- |
| Metadata, HTTP size и bytes относятся к одному child | Real selector fixtures: два размера, equal-size A/B, selection race; full suites | Synthetic local provenance/backend   | изменить            |
| Capability не допускает selector substitution        | HMAC canonical URL и 401 с пустым I/O trace                                      | Existing key lifetime policy         | сохранить           |
| Metadata и HEAD не читают payload                    | Repository spies и HEAD opener counters                                          | Production backend не измерен        | сохранить           |
| Exports и actor ownership сохранены                  | Полные Portal fixtures                                                           | Combined actor disconnect не измерен | сохранить           |
| Production/scientific acceptance достигнута          | Такие проверки не выполнялись                                                    | Engineering identity scope           | данных недостаточно |
