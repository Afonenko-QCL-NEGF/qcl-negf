# Независимый финальный review CR05

Вердикт: **no findings**. Frozen diff соответствует первому bounded ticket CR05;
препятствий к дальнейшему оформлению owning Platform change по результатам этого
review не выявлено. Это не production или scientific acceptance.

## Исходники и границы проверки

- Root HEAD: `bce0aee088313fd28b2440f55350980e21ed46bd`.
- Platform source HEAD: `cc910b6f13a474423fe06126b65d2fb59341e8aa`.
- Frozen diff: `/tmp/qcl-cr05-final.patch`, SHA256
  `ddf6cc84bc578ff1e7b9f288bda669c11b52b3d5326e6b8f3c355a4b2fb968ec`.
  SHA256 текущего `git diff --binary` Platform совпадает с frozen diff.
- Component имеет ровно три modified paths: `ops/application_release.py`,
  `tests/test_application_release.py`, `docs/application-cd.md`;
  HEAD и root gitlink совпадают с выданным source.
- Root status содержит заранее существующие правки AGENTS.md, README.md, TODO.md,
  docs/architecture.md, docs/single-server-deployment.md, untracked docs/system/.
  Они не входят в рассматриваемый diff. Recursive submodule status прочитан.
- Прочитаны ticket, architecture, contributing, canonical role policy,
  CR05/I10–I12, весь diff трёх файлов, окружающий activate/check и исходный
  `ops/register_aiida.py:reconcile` вместе с `tests/test_registration.py`.
- Read-only review: команды Nix/SSH/systemctl/AiiDA, тесты, solver, builds и
  subagents не запускались. Создан только этот отчёт в `/tmp`.

## Сопоставление контракта и реализации

1. `ops/application_release.py:activate` (строки 298–306 в frozen diff)
   сверяет application и solver profiles независимо. Missing/wrong solver при
   correct app и ready record приводит только к solver setter. Повреждённый
   app при здоровом solver приводит только к app setter; исправные profiles
   не получают дополнительных setters. Выбранные immutable paths берутся
   из валидированного manifest, а не из повреждённого profile.
2. После каждого setter повторно проверяется resolved profile identity.
   Исключение setter либо неправильный результат останавливает выполнение
   до Code registration, environment publication и service/health commands.
   Прежний ready record удаляется перед command boundary (строка 295),
   поэтому эти отказы не сохраняют старое `ready:true`.
3. `check` (строки 206–208) отклоняет missing/wrong solver profile до
   `nix-store --verify-path`, service health и solver self-check. Существующая
   проверка app/record identity сохранена.
4. `same` и выбор `systemctl start/restart` не изменены. Для correct app +
   ready record ремонт solver сохраняет identical-retry service policy;
   при повреждённом app остаётся прежнее поведение restart. Release/executable
   и release-specific Code label также не изменены. Prepare/bootstrap,
   delivery/admission и прочие lifecycle entry points diff не меняет.
5. Документация описывает внедрённую раздельную reconciliation и fail-closed
   поведение, а также прямо ограничивает доказательность fake boundary.

## Качество и независимость проверок

Новые тесты вызывают реальные `activate`/`check`, создают реальные временные
symlinks и runtime records. Ожидаемые `/nix/store/application`,
`/nix/store/solver`, executable и label заданы вручную, не вычисляются через
production helpers. Проверка точного списка `nix-env` calls ловит как отсутствие
repair, так и лишнее переключение здорового profile. Guard test требует пустой
command trace, а failure/wrong-result matrix проверяет отсутствие ready и
service/health commands для worker/controller и обоих profiles.

Healthy retry уже покрыт существующими worker/controller cases. Исправленный
app-mismatch fixture теперь содержит `ready:true` и здоровый solver profile:
он проверяет именно app mismatch, а не раньше срабатывавший ready guard.

Сопоставление before/after UUID в activation tests само по себе ограничено:
`Commands.registered` — постоянный fake UUID. Поэтому отдельно рассмотрен
исходный `cc910b6:ops/register_aiida.py:reconcile`: строки 45–56 выбирают
существующий Code по неизменному label, проверяют computer/executable/plugin/MPI,
возвращают его UUID и создают Code только при отсутствии. Прочитанный existing
`tests/test_registration.py:test_retry_after_auth_failure_reuses_both_uuid_and_completes_configuration`
проверяет reuse на stateful in-memory ORM. Эти исходники дают основание считать
register path совместимым с CR05; реальный AiiDA/database в этом ticket не проверен.

Первичный лог независимого targeted запуска `/tmp/qcl-cr05-final.log` содержит
40 tests, OK, suite exit 0, 1 CPU affinity, RLIMIT_AS 2 GiB, timeout 60 s.
Повторного запуска рецензент не делал. RED/GREEN executor report прочитан;
совокупный бюджет по выданным сведениям использован 3/4.

## Что рассмотрено и оставлено вне вердикта CR05

- CR02–CR04: lifecycle serialization, maintenance/admission и remote timeout
  recovery — отдельные tickets; изменения этих механизмов здесь отсутствуют.
- Конкурентная внешняя mutation profile после проверки — требует отдельного
  lifecycle/операторского контракта; diff не вводит или не доказывает его.
- Реальная регистрация GC roots и устойчивость closures к Nix GC — native
  integration evidence не получено; fake symlinks доказывают identity logic.
- Реальные services, AiiDA/PostgreSQL и UUID reuse на deployed host — команды
  не запускались; existing register path рассмотрен только по исходникам.
- Полные I10–I12/bootstrap, science acceptance и production readiness —
  объём шире этого первого bounded CR05 ticket.

## Решение

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Раздельный missing/wrong profile repair реализован | Source `cc910b6` + frozen diff SHA256; `ops/application_release.py:activate`; exact setter assertions | Native Nix boundary fake | изменить |
| Solver identity обязателен для успешного check | `ops/application_release.py:check`; missing/wrong matrix с пустым command trace | Real services не запускались | сохранить |
| Setter failure/wrong result не публикует ready | Удаление record до setters и post-set identity guard; failure matrix | Внешние concurrent mutations вне bounded scope | сохранить |
| Release/executable/label identity сохраняются | Before/after assertions; unchanged registration args; `ops/register_aiida.py:reconcile` | UUID fake в activation; stateful ORM test прочитан, не запущен | сохранить |
| Реальные GC/AiiDA/services и полный релиз приняты | Таких первичных runtime свидетельств нет | Только targeted fake-boundary лог и static review | данных недостаточно |

Actionable Critical/Important/Minor findings в пределах рассматриваемого diff:
**нет**. Дополнительный targeted rerun для этого review не требуется.
