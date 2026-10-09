# CR05: независимое восстановление application и solver profiles

Статус: свидетельства bounded реализации первого ticket этапа 1, 2026-10-09.
Это инженерная проверка activation/check; приёмка runtime и научной модели
остаётся отдельной. Задание дано по локальному `docs/system/implementation-entrypoint.md`;
корпус `docs/system/` при начале работы ещё не опубликован.

## Исходный набор и перепроверка

Фактический root HEAD: `bce0aee088313fd28b2440f55350980e21ed46bd`.
Gitlink Platform: `cc910b6f13a474423fe06126b65d2fb59341e8aa`;
component checkout был чистым. `git rev-parse HEAD`, `git status --short`
и `git submodule status --recursive` сняты до изменения. Другие gitlinks
не обновлялись; источник состава — Git tree, а не отдельный revision lock.

До изменения root содержал локальные правки `AGENTS.md`, `README.md`, `TODO.md`,
`docs/architecture.md`, `docs/single-server-deployment.md` и untracked `docs/system/`.
Они сохранены и не включены в integration commit этого ticket.
GitHub API подтвердил совпадение исходного HEAD с
[root PR #6](https://github.com/Afonenko-QCL-NEGF/qcl-negf/pull/6) и выбранного
component commit с
[Platform PR #4](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/4),
а также доступность обоих commit через Git commit endpoint.

CR05 подтверждён чтением исходного `ops/application_release.py:activate/check`
и независимым read-only аудитом того же commit, без передачи готового диагноза.
Контрпример: matching ready record и application profile, но удалённый либо
неверный solver profile. `same` пропускал оба setters; `check` проверял solver
closure напрямую и не выявлял отсутствие отдельного solver GC root.
Это не доказывает фактическое удаление closure GC: другие roots могли его удерживать.

## Изменение и совместимость

Owner — Platform; исполнитель с effort `medium`, независимые reviews — `high`.
Model не менялась. Один executor менял три component файла:
[activation](../../components/qcl-negf-platform/ops/application_release.py),
[fixtures](../../components/qcl-negf-platform/tests/test_application_release.py),
[owning documentation](../../components/qcl-negf-platform/docs/application-cd.md).

Application и solver profiles теперь восстанавливаются раздельно по resolved
closure identity. Здоровому profile не назначается новая generation только
из-за повреждения второго. Каждый setter сопровождается проверкой конечного
target; отказ или неверный результат не публикует `ready:true`.
`check` отклоняет missing/wrong solver profile до service health/self-check.

Manifest/API, immutable solver path, Code label и схема runtime не изменены.
Условия `systemctl start/restart` и Code registration сохранены.
Существующий `register_aiida.py:reconcile` переиспользует Code по label и
проверяет его computer/executable/plugin/with_mpi; регрессии activation
проверяют неизменность UUID, executable и label на command boundary.
Реальный AiiDA profile/ORM этой проверкой не исследован.

## Проверки и бюджет

Разрешено максимум четыре targeted suite вызова, каждый: одна CPU affinity,
`RLIMIT_AS=2147483648` (2 GiB), timeout 60 s. Использованы три вызова;
нет автоматического повторения до успеха. Из component directory:

```console
python3 -m unittest discover -s tests -p test_application_release.py
```

| Проверка | Результат | Свидетельство |
| --- | --- | --- |
| RED до product fix | 40 tests; 18 ожидаемых subtest failures; suite exit 1 | [Полный RED](evidence/cr05-2026-10-09/red.log) |
| GREEN после fix | 40 tests, OK; exit 0 | [Полный GREEN](evidence/cr05-2026-10-09/green.log) |
| Окончательная проверка координатором | 40 tests, OK; exit 0; wall 0.167 s | [Полный final](evidence/cr05-2026-10-09/final.log) |
| Формат и scope | `git diff --check` exit 0; только три component файла | Component diff |

RED отказы: solver guard — 4; независимый repair — 8; setter failure/wrong-result
без ready — 6. Остальные tests не падали. Shell wrapper RED успешно сохранил
лог; это не меняет suite exit 1.
Новые fixtures охватывают worker/controller, missing/wrong application и solver,
здоровый peer profile, ошибки setters и неверный target после success.
Исправлен прежний app mismatch fixture: matching ready и здоровый solver
исключают отказ по другой причине.

Тесты вызывают реальный Python activation/check и пишут реальные временные
symlinks/runtime records; внешние Nix/systemd/registration/self-check команды
заменены stdlib `Commands`. Полный suite, Nix builds/GC, services, SSH, CI,
solver и численные scientific checks не выполнялись. Инфраструктурные credentials
не читались и сервер не менялся. Draft PR publication не запускает root CI:
workflow имеет только push на `main` и ручной dispatch.

## Независимая проверка и решение

Независимый final code/spec review: **no findings**; сверены frozen diff
SHA256 `ddf6cc84bc578ff1e7b9f288bda669c11b52b3d5326e6b8f3c355a4b2fb968ec`
и фактический component diff. [Полный review](evidence/cr05-2026-10-09/review.md).
Component change зафиксирован в `7eaa515fcf4ad1146d7767b350286814e7c97f70`,
ветка `codex/cr05-solver-profile-recovery`; local root integration candidate
подготовлен в `codex/cr05-platform-integration`.

Публикация не выполнена: automatic approval review отклонил component `git push`,
указав отсутствие явного поручения публикации во внешний GitHub repository
и подтверждения trusted destination. Обход или повтор push не выполнялись.
Для двух draft PR требуется подтверждение пользователя. Порядок после
подтверждения: опубликовать component/owning PR, затем root gitlink candidate.
Root HEAD этого кандидата выбирает component через Git tree; полный релиз
и production runtime не наследуют приёмку исходного root.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| CR05 актуален на исходном source | Commit + `activate/check`; независимый аудит; RED | Исходный контрпример инженерный | изменить |
| Missing/wrong solver profile восстанавливается независимо | `activate`; GREEN/final repair fixtures | Fake Nix boundary; real GC не измерен | изменить |
| Здоровые profiles идемпотентны | Existing retry fixtures; точные setter traces | Допускаются health checks и runtime publication | сохранить |
| Недоказанный profile не получает ready | Post-set identity guard; failure/wrong-result fixtures | Внешние конкурентные mutations не исследованы | сохранить |
| Release и immutable Code selection сохраняются | Before/after identity, UUID/executable/label fixtures; unchanged reconcile source | Реальный AiiDA не проверялся | дополнительно измерить |
| Production/runtime и S01 приняты | Таких свидетельств нет | В этот этап не входят | данных недостаточно |
