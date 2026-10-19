# OPS03 — уточнение identity прямого `activate`

Статус: **D ruling candidate, требуется independent R high и CP-DESIGN root**.
2026-10-19, source-only. Это ограниченное уточнение accepted OPS02 §§3–4,
а не CP-CODE frozen implementation. Product files, Git, tests/imports,
services/SSH/Nix и follow-on provisioning/admission contracts не изменялись.

## Прочитанные исходные данные

Сначала рассмотрены accepted OPS02 API и authority matrix:
`/tmp/qcl-ops02-design.md`, SHA-256
`26374bcfb194aa5c9701bd00ceaae6016cd535dcc722e8b221719fec72450030`;
independent R `/tmp/qcl-ops02-design-review.md`, SHA-256
`3d5f3c7e33f8c9f1e8a863c73fdefab4969c3af85c737415e294ac366a17a54a`.
Baseline Platform — `6c5b11f3c74d44fed8b2c159f890b83e0b5456b9`.
Baseline `observe_node_identity`, `assert_expected_node`, CLI settings route
сопоставлены с сохранёнными source locators и context frozen patch.

Затем прочитаны actual frozen files в
`/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf/components/qcl-negf-platform`:

| Input | SHA-256 |
| --- | --- |
| `/tmp/qcl-ops03-candidate1.patch` | `8de400d2bae1c39bfbe265d3b8285676b975914d8fefb5fa1a573c108ef74fc1` |
| `/tmp/qcl-ops03-local-identity-question.md` | `ec2b485b779d299cb84f8d996833c442a4d42bffcfdb004407e920461230583d` |
| `ops/application_release.py` | `750198092c6f123b7a8baf2ba82129f6b1b2ee597edce002c327544bd5a09472` |
| `ops/worker_lifecycle.py` | `b81c722ce9cbca8a5adfed24063de268e39ea0d012ae120bb11d9491ba2a0678` |

Actual locators: `observe_node_identity` ~491, `assert_expected_node` ~600,
`_process_generation/_require_owner/lifecycle_owner` ~728–865,
`activate/_activate_owned` ~1343–1475, controller local route ~2740,
CLI activation branch ~2970–2994. Прочитаны также существующие fake seams
в `tests/test_application_release.py`, включая fixture ~272 и OPS03 class
~2885. Они показывают доступный DI маршрут; прежние тесты не являются
основанием этого решения.

## Решение: явный bounded trusted-direct контракт (вариант B)

`activate(..., expected_node_identity=None)` остаётся доверенным прямым
Python API. Он **не вызывает автоматически** `observe_node_identity` и
не читает `/etc/qcl-negf/release-config.json` ради определения full node
identity/роли. `role` задаёт доверенный in-process caller. Это допустимо
только в той же существующей модели доверия, где caller выбирает
`run`, `profile`, `runtime`, `gate`, email и allowlist path и уже исполняет
код с правами данного процесса. API не является RPC/authentication boundary
для непроверенного JSON, сети или пользовательского Python plugin.

Основание — source architecture и уровень authority, а не legacy fixtures.
OPAQUE owner доказывает владение конкретным process/runtime/release/lock,
но не делает произвольный Python caller менее привилегированным, чем
`publish`/`os` в том же interpreter. Автоматический existing full observer
добавил бы новый guest/Slurm precondition: его worker branch требует живого
одиночного slurmd, его unit InvocationID/config и canonical aliases до
activation. Такой probe не следует добавлять скрыто к доверенному API.

`None` означает **отсутствие full node assertion**, а не wildcard, adoption
чужого узла, доказанный enrollment или exemption от ownership. Returned
release для этого режима не получает выдуманный `node_identity`. Реально
наблюдаются actual PID/start ticks/boot посредством существующего
`_process_generation`; capability удерживает common lock/fence и точные
runtime/inode/release/deadline/journal/gate predicates.

Полная identity обязательна для controller whole-update owned helper и
worker update activation с `update_attempt_id`. Для обычного privileged
CLI сохраняются local protected settings role check и все existing
expected-node checks: отсутствие expected identity не может отключить
проверку `settings.role == args.role`. CLI не получает trusted/skip/owned
flag. Этот документ не выдаёт process-only observation за enrolled identity
или native admission evidence.

## Точная сигнатура и binding seam

Публичная сигнатура **не меняется**:

```python
def activate(manifest_value, *, profile=PROFILE, runtime=RUNTIME,
             role="worker", run=command, email=None,
             allowed_codes_file=Path("/var/lib/qcl-negf/aiida/code-uuid"),
             expected_node_identity=None, update_attempt_id=None,
             gate=GATE, deadline=None, metadata_budget=None):
```

Не добавлять `trusted=True`, observer callback, ownership flags или
переключатель по `run is command`, temp path, UID либо наличию config file.
Ни DI fake, ни native route не выбирают authority semantics косвенно.

Разрешён один private seam в `ops/application_release.py`:

```python
def _bind_activation_identity(owner, *, role, expected_node_identity):
    # Pure validation + once-only immutable binding in private owner registry.
    # Return (role, normalized_expected_or_None), never a new capability.
```

Этот helper вызывается в начале `_activate_owned`, после `_require_owner`,
до `_begin_local_mutation`, удаления update mask, record unlink, profile/
Code/env/service действий. Он:

1. Разрешает ровно `role in {"controller", "worker"}`. Неверная роль —
   `ValueError` до journal/application mutation.
2. Копирует provided identity через existing `identity_value`; сравнивает
   её role с `role`. Несовпадение/invalid schema — `ValueError`.
3. Для `state.operation == "whole_update"` запрещает `None`
   (`PermissionError`). Worker `update_attempt_id != None` также требует
   provided full identity (`ValueError`), до `_begin_local_mutation`.
   Последняя проверка находится рядом с binding в `_activate_owned`,
   поскольку update id не является аргументом pure seam.
4. Запоминает immutable snapshot `(role, normalized identity or None)`
   в private registry owner. Первый binding допускается только однажды;
   следующий вызов должен быть exact-equal. Смена role, expected identity
   или переход full↔None на том же owner — `PermissionError` до mutation.
5. При provided identity сравнивает её boot с actual owner process boot
   из уже захваченного `state.generation`; несовпадение — `ValueError`.
   Caller не может передать другой boot вместо текущего process generation.

Normalized identity — новая immutable/защищённая копия flat identity values.
Все дальнейшие checks и final publication используют snapshot, а не
ссылку на mutable caller dict. Нормализованный None никогда не подставляет
`role`/boot в поля несуществующего node observation.

Provided full identity дополнительно проходит **существующий** наблюдающий
validator до journal/application mutation:

* ordinary controller/worker: `assert_expected_node(snapshot, role=role,
  run=bounded_run, metadata_budget=owner_budget)`;
* stopped worker update: existing `observe_stopped_update` и
  `bind_node_observation(snapshot, observation, prior_boot=snapshot["boot_id"])`.
  Не вызывать running-daemon observer до снятия owned stop mask вместо
  существующего stopped proof; это сломало бы legitimate stopped-worker route.

После activation, непосредственно перед ready:true, provided identity
перепроверяется existing `assert_expected_node` и exact before/after
comparison. Process-only route перепроверяет `_owner_before` и тот же
bound role/None snapshot; full observer в него не добавляется. Actual
process generation/inode/deadline проверки на каждом mutation boundary
остаются обязательны в обоих режимах.

Ошибка schema/role/boot/expected observation до первого persistent действия
не создаёт lifecycle intent и не удаляет ready record. Ошибка actual
observation после mutations оставляет existing journal inhibition и
запрещает ready:true/terminal cleanup; unknown не называется mismatch-free
success. Deadline/IO exceptions не преобразуются в `None`.

## Callers и совместимость

| Caller | Snapshot / authority |
| --- | --- |
| Public trusted `activate`, expected omitted | Declared valid role + `None`; actual process owner/common gate/journal contract; full node not asserted |
| Public trusted `activate`, expected supplied | Normalized full identity; same role/actual process boot; existing pre/post observation |
| CLI standalone activate | Settings-derived role check обязателен независимо от expected; helper получает None либо explicit snapshot; ownership flags отсутствуют |
| Controller `_deliver_cli_locked::deliver` | Enrolled local+remote controller authority уже установлена; explicit full binding обязателен, helper не понижает его до None |
| Worker remote update | Expected identity и protected stopped attempt/mask proof обязательны; отдельный worker-local owner |
| Returning-worker CLI | Existing guarded open-gate predicate; role settings и any provided identity checks сохраняются; None не снимает local intent/unknown/update-marker checks |

Configurable profile/runtime/gate и service email/allowlist path прямого
Python API сохраняются. Выбранный closed gate обязателен, как уже решено
OPS02; валидные controller/worker roles не заменяются role из случайного
локального файла ноутбука. `prepare_initial`, provisioning writers,
CR04 shared gate protocol и other APIs этим уточнением не меняются.

### Полный source audit production call sites

Выполнен read-only `rg` по root и Platform code, включая root `.github`,
Platform `ops/modules/windows/ansible`, прямые imports и строки privileged
CLI. Platform `.github` отсутствует; это отсутствие учтено, а не принято
за проверенную runtime поверхность. Ниже перечислены все найденные native
cooperative activation/preparation call sites frozen candidate; test calls
в эту native таблицу не включены.

| Call site | Что передаёт фактически | Authority / ограничение |
| --- | --- | --- |
| `application_release.py::activate` ~1358 → `_activate_owned` | Caller role; expected optional; configurable profile/runtime/gate/run | Единственный public direct wrapper. Production native repository callers самого wrapper не обнаружены; Python tests вызывают его напрямую. None — process-only, не measured node authority |
| `_deliver_cli_locked::deliver` ~2756 → `_activate_owned` | Literal controller role; explicit `bindings[name]["identity"]`; live whole-update owner | Enrolled local+remote protected authority до helper; None после этого решения запрещён |
| `_deliver_cli_locked::deliver` ~2774 → remote CLI activate | Selected worker role; explicit base64 observed binding; own update attempt id | Existing enrollment/trust/physical-stop flow; remote fresh node-local owner; не process-only native shortcut |
| `worker_lifecycle.py::startup` ~526 → remote CLI activate | Literal worker role; explicit expected identity из bound observation ~492; returning-worker predicate | Existing startup event/new boot/complete stop scope + controller authority. Отсутствующая expected identity здесь contract violation |
| `application_release.py::main` ~2991 → `_activate_owned` | `args.role`, optional expected; settings email/allowlist | Перед helper settings.role exact-check ~2988 независимо от expected. User CLI role сам authority не является; forged role fails. Provided expected проходит existing validation |
| `application_release.py::prepare_initial` ~1261 → `_prepare_initial_owned` | Caller role; owner; no expected parameter by existing API | Cold preparation, closed gate и ready:false/exact-byte contract; full identity не объявляется |
| `application_release.py::main` ~2972 → `prepare_initial` | CLI requested role; no expected identity | Existing initial-provisioning route; protected-settings role check **в этом branch отсутствует**. Этот note его не выдумывает и не переносит в обычную full-node activation |
| `modules/release.nix::releaseCommand` ~18 | `exec python3 ... application_release.py "$@"` | Wrapper не даёт отдельного role/owner bypass; authority проверяется выбранным CLI branch |

Других direct calls/imported aliases `activate`, `prepare_initial`,
`_activate_owned`, `_prepare_initial_owned` в native code root/eight-component
workspace поиском не найдено. Root `ops/application_cd.ts` собирает manifest,
но activation не вызывает. AiiDA `calculation.py` вызывает только job
`guard`; `modules/release.nix` ExecStartPre вызывает `node-check`;
`modules/application.nix` вызывает только `bootstrap-identity` перед
отдельной bootstrap chain. Эти readers не являются None activation
callers. Независимые Nix/bootstrap publishers остаются уже сохранённым
OPS02 follow-on, без нового waiver.

§4 protected-role policy соблюдается существующими native normal activation
entrypoints: whole controller и returning/update workers передают явную
identity, standalone CLI дополнительно сопоставляет protected configured
role независимо от optional expected. Direct Python API отделён как
доверенный программный primitive, а не объявлен более слабым equivalent
authenticated CLI. При появлении нового native direct caller required
call-site review должен определить его external role/target authority;
наличие Python/root permissions не означает безопасность любого target.

**Source/G1 pass не даёт native operational permission.** None invocation
не наследует fresh CP-OPS BIND/readiness от source closure, owning merge,
закрытого gate или прав процесса. Для реальной maintenance operation
по-прежнему нужны bound approved target set/role, release/source,
window/inhibition, protected ownership, storage/backup/rollback и fresh
admission по существующим grants. Ни один такого рода факт API None не
проверяет и не заменяет. В текущей кампании использовать существующие
CLI/whole/native lifecycle entrypoints; появление нового production direct
None route требует explicit technical D/R call-site admission в пределах
active grant, а не молчаливого выбора удобного API. Foreign/unknown targets
и credentials/trust boundaries не становятся разрешёнными от этого note.

## DI и минимальные discriminating controls

DI только средствами теста `patch.object` существующих module seams
`observe_node_identity`, `_process_generation`, command boundary и metadata
reader. Public API не получает тестового переключателя. В identity tests
синтетический observed boot обязан совпадать с boot fake process-generation
source; PID/start-generation cases остаются отдельными реальными owner
controls. Нельзя глобально возвращать controller fixture для worker case
и затем игнорировать mismatch. Pure binder и validators не mock-ятся в
проверяемом positive path.

| ID | Действие | Oracle |
| --- | --- | --- |
| LI01 | Trusted direct expected=None, valid controller и worker roles по отдельности; observer fake raises if called | Real owner/files/fake commands complete; observer call count 0; returned record не содержит invented node_identity |
| LI02 | None + invalid role; worker update id + None | ValueError до intent/profile/Code/env/ready/mask mutation; старые bytes равны |
| LI03 | Explicit expected wrong role / invalid schema / boot ≠ actual capability boot | ValueError до journal/mutation, no fallback to process-only |
| LI04 | Explicit expected correct role/boot, observer returns wrong machine/role/boot | Existing validator rejects до mutation; direct wrapper не пропускает provided check |
| LI05 | Explicit expected changes at final observer; separately input dict mutated by command fake | Snapshot неизменен; actual drift blocks ready:true and keeps intent; caller dict mutation не меняет pinned expected identity |
| LI06 | Whole-update live owner private helper with None | PermissionError до mutation; process-only direct policy не переносится в whole-update |
| LI07 | Reuse same owner: full→None, None→full, changed role/identity | PermissionError before second mutation; exact-repeat binder допустим |
| LI08 | CLI expected omitted + settings.role mismatch | ValueError before application mutation; None не обходит privileged local role check |
| LI09 | Explicit stopped worker update, supported owned stop marker, daemon ещё stopped | Existing stopped observation accepted до mask removal; running observer не вызывается преждевременно; final full observation обязателен |
| LI10 | Process-only route wrong runtime/release/lock inode/process generation/deadline, foreign durable intent либо open gate | Existing O-controls refuse; None не обходной ownership режим |

Controls входят в уже централизованный OPS03 allowance; этот D не расходует
test invocations и не разрешает дополнительные reruns. Medium остаётся
STOP на этой границе до exact independent R + root CP-DESIGN. После принятия
он выполняет только согласованное уточнение в existing OPS03 edit set.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Trusted direct None не требует скрытого guest probe | Existing configurable Python API / trusted interpreter boundary; решение выше | Не устанавливает enrolled/local full node identity | сохранить |
| Full expected identity нельзя потерять на owned route | Once-only snapshot seam, explicit whole/update requirements, LI03–07/09 | Пока design; candidate нуждается в указанном binding/ordering | изменить |
| CLI None не разрешает role bypass | Actual `main` settings.role check ~2988; LI08 | Native protected-config evidence отдельно | сохранить |
| Narrow boundary готова для independent CP-DESIGN | Точные signature/seam/callers/errors/controls | Tests0, CP-CODE и follow-on gates не закрыты | дополнительно измерить |
