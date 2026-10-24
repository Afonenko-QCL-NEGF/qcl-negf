# OPS03 — frozen GREEN2 candidate, source-only

Baseline Platform: `6c5b11f3c74d44fed8b2c159f890b83e0b5456b9`; component `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/qcl-negf-platform`.

## Точное изменение после DIAG1

Принят independent repair contract `/tmp/qcl-ops03-diag1-review.md`, SHA-256 `4a7786f9a273c9813c95e31bd478ff8e03ab3f8efa87ea76dfe450c79a7878c6`.

От diagnostic candidate изменены ровно три выражения в `application_release.py::deliver_cli`:

1. Local controller `deliver` передаёт в `verify_controller_authority` remote observation как `dict(bindings[name]['identity'])`.
2. Local controller `deliver` передаёт в `check` expected identity как свежую такую же dict value copy.
3. Local controller `admit` передаёт в `fleet_health` expected identity как свежую dict value copy.

`probe` и actual `bind_node_observation` по-прежнему создают immutable canonical bindings. `identity_value` остаётся dict-only schema/wire validator. `_activate_owned` получает исходный immutable binding; once-only immutable binder самостоятельно копирует и проверяет его, как до repair. Нет fallback None, нового observer, policy, trust root или ослабления role/boot checks.

Статически прослежен путь authority → helper/binder → check/assert_expected_node → fleet_health/check → verify_node_envelope. Local check возвращает actual observed dict для envelope; canonical immutable binding служит lookup object. Runtime прохождение этого пути пока не утверждается.

## Сохранённые controls

Тестовые файлы совпадают с frozen diagnostic candidate. Подтверждённые fixture repairs R2–R5 сохранены без изменений. O03 проходит через настоящий probe/bind_node_observation, helper и publishers; assertions сохраняют two flock acquisitions, one helper call, pending local mutation, full identity, Code UUID, оба profile targets, open/completed, cleanup intents и отсутствие self-mutating SSH/copy. Negative forged authority и legacy protocol controls остаются. Диагностика остаётся bounded assertion message, не заменяет oracle.

## Freeze

Полный source-applicable baseline patch: `/tmp/qcl-ops03-green2-candidate.patch`.

| Файл | SHA-256 |
| --- | --- |
| green2-candidate.patch | db537a222ef74b72b49d6521c340445b00465bf2199f38377d29f5865c275498 |
| ops/application_release.py | 1d4422bed5986901ddef22890ca16fe600336e6af2bef17d83ae809ebe794df0 |
| ops/worker_lifecycle.py | b81c722ce9cbca8a5adfed24063de268e39ea0d012ae120bb11d9491ba2a0678 |
| tests/test_application_release.py | f56062eef912a7c63ab9743a24f1db8a5043c2e24620db0732ab516485c0ce21 |
| tests/test_worker_lifecycle.py (unchanged) | 7d8fd49aac1b3eb4527ef185e9bf3a2cfcd7a3265e92a447954ae4e2bef15a2b |
| tests/test_worker_shutdown_intent.py | 53017ecb166b5624dab6fe3d2b57498bdbf37882a83a9be0c9c7668fdc95bfa3 |

`git diff --check` успешен. Автор не исполнял imports, target/helper, tests, native commands, services, SSH или Git mutations. Никакие science/foreign states не изменялись.

## Runtime gate и пределы

Root сохраняет RED1, RED2, GREEN1 (198 passed / 36 failed methods) и DIAG1 (3 failed / 0 errors) вместе с original logs/receipts. Эти исторические четыре calls не сбрасываются. Следующий пакет — ровно один final GREEN, call 5 по отдельному latest human extension, все три selected test files одним процессом, ≤90 s / 1 CPU / 1 GiB RAM / 16 MiB TMP / 2 MiB logs. Исполнение только root; никакого automatic rerun, retry или cancellation. Этот source freeze не утверждает runtime PASS и не создаёт дополнительный бюджет.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 representation mismatch исправлен на трёх согласованных boundaries | Три plain-dict value copies; independent diagnosis hash выше | Final runtime packet ещё не выполнен | изменить |
| Canonical identity и validators сохраняют контракт | Static trace immutable binding → copied strict API inputs; unchanged binder/validator | Это source evidence | сохранить |
| R2–R5 и O03/negative controls сохранены | Совпадающие test source hashes; O03 actual helper/publishers | Не заявляется GREEN | сохранить |
| OPS03 универсально закрыт | Нет такого свидетельства | Provisioning/OS/systemd writer closure, prepare-initial protected-role gap и CR04 atomic effective job admission остаются отдельными blocked residuals; native/scientific/full release/CP-OPS не приняты | данных недостаточно |

STOP перед root final GREEN и independent exact-repair review. Root остаётся sole Git operator.
