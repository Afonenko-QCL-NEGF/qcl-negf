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
заменены stdlib `Commands`. В первоначальном targeted бюджете полный suite,
Nix builds/GC, services, SSH, CI, solver и численные scientific checks
не выполнялись. Инфраструктурные credentials при реализации не читались;
сервер не менялся. Draft PR publication не запускает root CI:
workflow имеет только push на `main` и ручной dispatch.

### Расширенные локальные проверки перед публикацией

Пользователь затем явно разрешил GitHub publication при отсутствии секретов
и поручил проводить максимально доступные локальные проверки перед final CI.
Production/bootstrap/solver scope этим не расширен. Выполнен один
`deno task check` без `nix develop`, установки окружения и builds: одна CPU
affinity, 2 GiB sampled aggregate RSS, 120 s wall, 2 MiB вывода. Опциональный
`QCL_TEST_NIXPKGS` удалён из test environment для исключения native Nix eval;
отключён auto-load сторонних pytest plugins.

Формат, lint и typecheck прошли; Deno: **22 passed**. Python:
**248 passed, 5 skipped, 166 subtests passed, 1 failed**. Итого command exit 1,
19.209 s wall, sampled peak RSS 341778432 bytes; лимиты не достигнуты.
Отказ: `tests/ops/test_nix_trust.py::test_public_trust_block_is_idempotent_and_preserves_existing_config`,
Ansible `Local RPC server did not start`. Это не замаскировано как green.
[Полный вывод](evidence/cr05-2026-10-09/local-check.log).
Raw pytest log сохранён byte-for-byte, включая trailing spaces в traceback.
Для нового root evidence `diff --check` применяется к prose/code, исключая
raw `.log`; original failed receipt не нормализуется ради форматирования.

Отдельная дешёвая средовая проба установила: AF_UNIX socket creation разрешён,
bind/listen внутри sandbox даёт `PermissionError`, errno 1. Исходник установленного
Ansible `_internal/_rpc_host.py:LocalManager` использует local RPC listener.
Проверены side effects fixtures: только временные файлы, public dummy key,
local connection, без root/VM configuration. Поэтому выполнен **один**
изолированный запуск `python3 -m pytest -q tests/ops/test_nix_trust.py`
вне sandbox: 1 CPU, 2 GiB sampled RSS, 60 s, 2 MiB вывода. **3 passed**, exit 0,
4.890 s wall, sampled peak RSS 105250816 bytes. Это различающее свидетельство
средового ограничения первоначального отказа, а не повтор полного suite.
[Полный вывод](evidence/cr05-2026-10-09/nix-trust.log).
Пропуски Nix/AiiDA-dependent fixtures не заполнены установкой окружения.

## Независимая проверка и решение

Независимый final code/spec review: **no findings**; сверены frozen diff
SHA256 `ddf6cc84bc578ff1e7b9f288bda669c11b52b3d5326e6b8f3c355a4b2fb968ec`
и фактический component diff. [Полный review](evidence/cr05-2026-10-09/review.md).
Component change зафиксирован в `7eaa515fcf4ad1146d7767b350286814e7c97f70`,
ветка `codex/cr05-solver-profile-recovery`; local root integration candidate
подготовлен в `codex/cr05-platform-integration`.

Первый component push был отклонён automatic approval review: отсутствовало
явное поручение publication во внешний GitHub repository и подтверждение
trusted destination. До явного разрешения пользователя обход/повтор не выполнялся.
После разрешения полный независимый аудит двух commit ranges не обнаружил
секретов и закрытых инфраструктурных адресов.
[Publication audit](evidence/cr05-2026-10-09/publication-audit.md).
Дополнительно pattern scan и сравнение с четырьмя literal sensitive values из
порученного `environment.fish` не нашли совпадений; файл не исполнялся,
значения не выводились и не сохранялись в evidence. Публикуются публичные
GitHub URLs, synthetic example.invalid emails, Nix fixtures и локаторы тестов.
Проверка ограничена новым diff и не даёт абсолютной гарантии для неизвестных
форматов секретов или всей pre-existing Git history.
Owning component опубликован первым:
[Platform draft PR #5](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/pull/5).
Следующий publication step — root gitlink draft PR с этим report/evidence.
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
