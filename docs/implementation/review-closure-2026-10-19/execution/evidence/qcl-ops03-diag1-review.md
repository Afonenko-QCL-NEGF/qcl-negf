# OPS03 DIAG1 — независимый static root-cause review

**Вердикт: причина R1 установлена; narrow repair contract READY. CP-CODE остаётся CHANGES_REQUESTED до exact repair review и final runtime gate.** Reviewer ничего не исполнял и product не менял.

## Binding

Baseline Platform 6c5b11f3c74d44fed8b2c159f890b83e0b5456b9. Самостоятельно пересчитаны:

| Артефакт | SHA-256 |
| --- | --- |
| frozen diagnostic patch | ab8fbf644fa0142f743e5d728e0a841665a817111afa962a20ce82d1604b5f37 |
| diagnostic author report | e4078624e3e341fbdf2645be17a773e28af7bcdeae9dc1ad9365cf080ffcefee |
| application_release.py | 08f67097705f86d2ca842ae373306cb8945f47564c4d2ceb5e00e8272f31831f |
| worker_lifecycle.py | b81c722ce9cbca8a5adfed24063de268e39ea0d012ae120bb11d9491ba2a0678 |
| test_application_release.py | f56062eef912a7c63ab9743a24f1db8a5043c2e24620db0732ab516485c0ce21 |
| /tmp/qcl-OPS03-DIAG-1/receipt.json | 1fe37ad7b16cbdb3ecb98b2e87137426432ff07743fbb7400fd89c28ab66fa87 |
| DIAG1 original.log, 8334 B | 2eeb4fffc01230305a8ac9bfecced48c8915c914852f1066a9e7278e62f6c4ec |

Production совпадает с candidate2, diagnostics/fixture source соответствует declared f560. DIAG1 — root witness трёх selected healthy methods, 3 failed/0 errors, wall1.995s, raw complete. Это диагностика, не GREEN. Original GREEN1 и прежние counters остаются отдельным evidence.

## Точная причина и путь

1. `application_release.py::probe` около :2645–2663 получает JSON `identity_probe` → `bind_node_observation(selected[name], actual, ...)`. Последняя функция :310–318 валидирует observed **dict**, затем возвращает `MappingProxyType({...,'identity':MappingProxyType(actual)})`. Поэтому `bindings[name]['identity']` — canonical immutable full-node mapping, не dict.
2. Новая local-controller ветка `deliver` :2780–2781 вызывает `verify_controller_authority(selected[name], authority['local_identity'], bindings[name]['identity'])`. Его remote_observation теперь внутренний MappingProxyType, тогда как прежняя SSH serialization boundary давала JSON dict.
3. `verify_controller_authority` :320–325 → `bind_node_observation(..., remote_observation, ...)` :311 → `identity_value` :217–219. Последний намеренно требует `isinstance(value,dict)` и выбрасывает **точно** `ValueError('Expected observed node identity')` для proxy. Значения schema/role/boot здесь до проверки не доходят.
4. Этот вызов находится ДО `pending_local_mutation`, owner.local_pending и `_activate_owned` (:2787–2794). Следовательно binder :1367–1390 не является первым виновником и не может исправить входной representation mismatch раньше себя. Ошибка pre-local-mutation объясняет DIAG controller failed, workers verified, requires_reconciliation false: durable whole operation остаётся failed/closed, но controller helper ещё не начал application mutation.

Три DIAG healthy controls независимо показывают одинаковый controller reason; source path обосновывает locator, а не только совпадение строки ошибки. Reviewer не утверждает, что DIAG выполнил оставшиеся нижние stages.

## Все затронутые local strict-observation boundaries

| Boundary | Actual frozen input | Downstream contract / состояние |
| --- | --- | --- |
| `deliver::verify_controller_authority` :2780–2781 | `bindings[name]['identity']` proxy | :320–325→:311→dict-only :217. **First reached failure**, root cause DIAG |
| `deliver::_activate_owned` :2790–2794 | same proxy | `_bind_activation_identity` :1375–1377 явно принимает dict/MappingProxyType и делает `identity_value(dict(...))`; этот seam уже корректен |
| `deliver::check` :2796–2797 | same proxy | `check` :1230→`assert_expected_node` :601→dict-only :217. **Latent deterministic failure** после ремонта первого вызова |
| `admit::fleet_health` :2836–2837 | same proxy | `fleet_health` :2414→dict-only :217; также subsequent expected-node checks требуют dict. **Latent deterministic failure**, DIAG этого stage не достиг |

Остальные просмотренные границы: `probe`/remote identity получают dict из JSON; authority.local_identity/remote_identity нормализованы dict при preflight :568–571; `recheck_controller_authority` использует их и fresh observed dict. `verify_node_envelope` принимает immutable binding как lookup object, но envelope.node_identity должен быть observed dict; local check возвращает fresh observed dict, wire worker — JSON dict. Receipt node_bindings :2672 и remote base64 flags :2700/:2803 уже явно делают dict копию. Поэтому не нужен global schema/authority relaxation.

## Минимальный correction contract

- На трёх названных strict observation API boundaries передать fresh plain-dict value copy canonical flat identity; можно иметь явно scoped local snapshot, но не менять/размораживать canonical bindings.
- Сохранить `identity_value` dict-only wire/schema validation; не ловить ValueError с fallback None, не пропускать verify_controller_authority/check/fleet_health и не создавать новый observer/trust root.
- `_bind_activation_identity` остаётся once-only immutable role/full-or-None, actual process boot, whole/update full required. Local helper не reacquire flock, mutating self SSH/copy не возвращается.
- Existing O03/healthy whole controls должны пройти **через actual `bind_node_observation`**, а не подменить canonical source на handwritten dict-only bindings. Сохранить real helper/publishers, full node envelope, no self-SSH, acquisition count, selected gate, immutable Code/profile assertions. Test diagnostics остаются failure messages, не oracle replacement.
- После source repair заново проследить local authority→helper→check→fleet health→terminal gates. Final GREEN проверяет прежние negative/unknown/terminal controls; DIAG3fail не выдаётся за proof всех remaining stages.

Это исправление value representation между уже проверенными internal bindings и existing observation functions; authority/role/node selection и accepted B semantics не меняются.

## Fixture corrections R2–R5 — source review

Прочитаны actual corrected tests до author report. Подтверждены без runtime claim:

- **R2** :2385–2395, :2720: CAP-derived exhaustion вместо hardcoded32MiB; no actual access/sentinel assertions сохранены. Production64MiB не изменён. Dependent inherited cases не удалены.
- **R3** :772–805: fake root st_uid только для dev/inode controlled runtime + двух lock entries; прочие stat fields и real flock сохраняются. Native reads по-прежнему требуют synthetic UID/GID3000, restoration UID0/GID42; добавлен count≥4 для intended gate reads. Не ослаблен product owner predicate. Ранее отозванный default-runtime UID finding остаётся отозванным: installed modules/release.nix задаёт root0755.
- **R4** :1244–1280: failed operation сохраняет blocker bytes/closed gate; same-runtime retry требует refusal до callback; fresh runtime/gate positive независим, old bytes unchanged. :1319–1327 malformed None/[] subcases имеют independent runtime. Unknown adoption/intent deletion не добавлены.
- **R5** :482–512 malformed remote fault адресован real worker, complete three-node context; ровно один fired injection; controller verified/worker failed/later second not_attempted; запрещены later copy/activate/finish/RESUME. Эти assertions пока зависят от R1 repair и не считаются executed pass. :1038–1055 cache/hash fixture использует один selected gate/runtime вместо перенаправления publisher. Missing-target refusal не заменён success.
- `delivery_diagnostic` :92–115 ограничивает receipt source selected runtime/delivery-attempts, read65537/64KiB rejection, selected fields/last8 commands и output6000 chars; completed/open assertions не заменены. Root final-publication controls/LI/O checks не удалены для apparent green.

DIAG1 выполнял только три healthy selections. R2–R5 source corrections не имеют отдельного runtime PASS в этом отчёте.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| First controller failure вызван proxy→dict-only boundary | :310–325/:217 и :2780–2781; exact root DIAG reason | Runtime traceback внутри caught ValueError отсутствует, но source type path однозначен | изменить |
| Один repair binder устранит всё | Binder уже конвертирует proxy; ещё две strict boundaries ниже | Latent check/fleet-health failures не выполнены DIAG | изменить все три boundary copies |
| Negative fixture contracts сохранены | R2–R5 actual assertions перечислены выше | Эти corrections source-only до final packet | сохранить |
| CP-CODE/native/scientific/full CI готовы | Нет такого evidence | Repair/review/final GREEN ещё нужны; provisioning/prepare role gap/CR04 residual retained | данных недостаточно |

Reviewer не запускал target/helper/tests/imports, не менял product/tests/Git/native state; только source/hash/log inspection и этот /tmp report. STOP после frozen diagnosis. Никакого automatic rerun или нового budget этим review не создаётся; root отдельно сохраняет исторические четыре calls и authorizes ровно один final GREEN по переданному grant.
