# OPS02 — контракт владения application lifecycle

Статус: **D candidate, CP-DESIGN pending**. Дата: 2026-10-19. Авторская
роль: Sol / ultra по поручению координатора. Это source-only design для OPS03;
product files, checkpoint, services и сервер не изменялись, tests не запускались.
Область — инженерный application lifecycle; физическая модель, критерии,
научные результаты и состав Git не меняются.

## 1. Входы и граница доказательства

Фактически прочитан root
`eb59809a4e601c9bd1d4859228d68502679b6d93` в
`/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
Platform HEAD — `6c5b11f3c74d44fed8b2c159f890b83e0b5456b9`, его
`git status --short` пуст. Root имеет чужие для этой задачи изменения трёх
gitlinks и execution evidence/checkpoint; они сохранены. Полный фактический
`git submodule status --recursive` прочитан, второй lock ревизий не создаётся.

Неизменяемый source packet:

| Platform path | SHA-256 |
| --- | --- |
| `ops/application_release.py` | `6c01e928172d77ccc8eb66678e8ff08a23a2fa1255c819de22eb2e4dfb49fdc8` |
| `ops/worker_lifecycle.py` | `b528eecc5f9842320531028c94dda92a695ff9b95eec7036313aa6e36bf83bd4` |
| `tests/test_application_release.py` | `fe5f2a56b8004778c1d33b576cee613d883e173feb6f153c90e78d816029590a` |
| `tests/test_worker_lifecycle.py` | `7d8fd49aac1b3eb4527ef185e9bf3a2cfcd7a3265e92a447954ae4e2bef15a2b` |
| `tests/test_worker_shutdown_intent.py` | `9426ec41b6b9c89e8004c6b762f8f2b4100e290e94d5eb24cc8ed125bc2ba491` |

Нормативные inputs: root `AGENTS.md`, `docs/architecture.md`, handoff
`README.md`, `autonomy.md`, `operator-permissions.md`, `platform-worker.md`
OPS01–03. Primary review: `RV06.md`,
`fixes/RV06-01-controller-activation-ownership.md`, релевантные RV12 timeout/
unknown и RV15 protected namespace/SSH trust. Старый PLAN/standby в файлах
не отменяет переданную координатором позднюю активацию EXEC B/G1/S1.
Серверные inventory/admission неизвестны и не нужны этому D.

Наблюдения на выбранном Platform source:

* `main` около 2440 использует `activation.lock` для standalone activation и
  initial preparation; `deliver_cli` около 1990 использует `delivery.lock`.
* `activate` около 984 сам owner не приобретает, удаляет ready record, меняет
  application/solver profiles, запускает registration, пишет allowlist/env/ready.
* `_deliver_cli_locked::deliver` около 2242 отправляет controller activation
  через mutating SSH к самому controller при удержании parent `delivery.lock`.
* `worker_lifecycle::_shutdown_owned_poll` уже отделяет capture/finalize под
  common owner от Runner pause/verify-stop под per-node lock; `startup` берёт
  common lock вручную и не берёт тот же per-node normal-lifecycle lock.
* `stop_update`, `repair_stopped_update`, `finish_update` меняют worker-local
  mask/marker без общего с activation node-local owner.

### Непосредственно обнаруженная внешняя граница

`modules/release.nix::qcl-negf-application-profile` непосредственно публикует
application GC root через `nix-env`. `modules/application.nix::qcl-negf-bootstrap`
через `ops/bootstrap.ts` / `bootstrap_profile.py` / `register_aiida.py` пишет
AiiDA config, bootstrap readiness и `code-uuid`. Эти отдельные provisioning/OS
entrypoints не участвуют в Python lifecycle owner и **не входят в edit set
OPS03**. Один `systemctl is-active` до Python mutation не устраняет TOCTOU.

Поэтому CP-CODE OPS03 может подтвердить только сериализацию перечисленных ниже
кооперативных application entrypoints. Universal single-writer PASS для всех
OS/provisioning путей из него не следует. Для native application-only операции
нужны подтверждённое inhibition этих owning publishers на всё окно, отсутствие
concurrent OS activation и конкретный service dependency contract. Fresh
readback должен связывать inhibition с unit/config/boot поколением до mutation
и перед его снятием; один старый receipt или inactive observation недостаточен.
Совместимость inhibition с `Requires`/`RemainAfterExit` и фактическим стартом
API/AiiDA требует native evidence. Здесь конкретный способ masking не
выдумывается и установленным фактом не объявляется.

Для безусловной universal closure требуется отдельная owning D-задача
**OPS03-FOLLOWON-PROVISIONING**: объединить publisher entrypoints
`modules/{application,release}.nix`,
`ops/{bootstrap.ts,bootstrap_profile.py,register_aiida.py}` с lifecycle owner,
сохранив service-account privilege boundary и initial bootstrap ordering.
Не передавать Python capability через env/CLI; не предоставлять `qcl-negf`
право произвольной записи в root admin runtime. Результат должен включать
boot/bootstrap-vs-update contention и start-dependency deadlock control.
Coordinator + independent R решают technical CP-DESIGN scope: принять
ограниченную OPS03 closure с этим обязательным остатком либо сначала выдать
follow-on D. Новый human вопрос для внутреннего выбора не нужен.

## 2. Выбранное решение и альтернативы

Выбран один process-local opaque owner. Controller parent вызывает activation
локально, в том же Python процессе, передавая live object приватному helper.
У каждого worker тот же owner механизм действует в его собственном runtime;
controller object туда не передаётся. Полноценное доверие enrollment/identity/
host keys остаётся независимой предпосылкой, object её не заменяет.

Альтернативы отклонены:

| Альтернатива | Причина |
| --- | --- |
| Только переименовать `activation.lock` в `delivery.lock` | Parent держит lock и ждёт SSH child, который пытается взять тот же lock |
| `--owned`, PID, UUID, JSON/env token от parent | Воспроизводимое caller-controlled значение не доказывает живое владение; PID переиспользуется |
| Новый daemon/lease service или remote capability channel | Новый lifecycle/trust протокол не нужен для локального controller; существенно шире owning scope |

### Инварианты

1. Все mutating application entrypoints в OPS03 приобретают один node-local
   `runtime/delivery.lock`. Lock descriptor никогда не передают внешнему child.
2. Только выданный данным модулем и ещё зарегистрированный live object
   разрешает private owned mutation. Public wrappers не принимают owner.
3. Parent-owned controller activation не делает второй flock и не исполняет
   mutating SSH/Nix copy к controller. Remote identity/SSH trust проверки остаются.
4. Захват lock не примиряет unknown. Durable receipts/intents имеют отдельную
   authority и проверяются после flock; смерть процесса освобождает lock,
   но не их barrier.
5. Успех local activation означает только local ready. Admission может открыть
   исключительно завершённая whole-pool процедура после существующих full
   fleet/cancellation/Slurm/identity predicates. Crash внутри local helper
   сам gate не открывает; отдельная final gate transaction имеет existing
   CR04 closed-or-unknown outcome, уточнённый ниже.
6. Каждый write/command/publication и terminal cleanup проверяет исходный
   monotonic deadline. Child/helper не возобновляет бюджет.
7. Ни один stale/foreign intent, update mask, GC root или receipt не удаляется
   для получения pass. Неизвестное состояние не заменяют нулём/idle/completed.

## 3. Точный API для OPS03

В `ops/application_release.py`:

```python
@contextmanager
def lifecycle_owner(runtime, *, operation, release_id, deadline,
                    release_identity=None):
    # yield LifecycleOwner; no serialized representation
    ...

def _require_owner(owner, *, runtime, operation, release_identity, deadline):
    # validate current registered object; return private live state
    ...

def activate(manifest_value, *, profile=PROFILE, runtime=RUNTIME, role="worker",
             run=command, email=None, allowed_codes_file=..., 
             expected_node_identity=None, update_attempt_id=None,
             gate=GATE, deadline=None, metadata_budget=None):
    # standalone: finite budget -> common owner -> guard -> _activate_owned
    ...

def _activate_owned(manifest_value, *, owner, profile=PROFILE, runtime=RUNTIME,
                    role="worker", run=command, email=None,
                    allowed_codes_file=..., expected_node_identity=None,
                    update_attempt_id=None, gate=GATE, deadline,
                    metadata_budget=None):
    # no acquire/release; requires validated live owner on every boundary
    ...
```

`...` в сигнатурах `allowed_codes_file` выше означает **тот же существующий
default** `Path("/var/lib/qcl-negf/aiida/code-uuid")`, а не новый параметр
реализации. `prepare_initial` сохраняет все existing keywords и получает
необязательный `deadline=None`; как public wrapper он сам берёт owner и
вызывает private `_prepare_initial_owned(..., owner=..., deadline=...)`.
При `deadline=None` public wrappers один раз устанавливают
`time.monotonic() + 1800.0` до preflight; CLI всегда передаёт вычисленный
`action_deadline`. Неявно безграничного mutating helper не остаётся.

`deliver_cli` сохраняет публичную сигнатуру; передаёт owner обязательным
keyword в `_deliver_cli_locked` и `_deliver_pool_owned`. Публичный
`deliver_pool` тоже приобретает common owner, поэтому прямой API не обход.
Mutating worker APIs `stop_update`, `repair_stopped_update`, `finish_update`
также являются wrappers над private owned bodies. Их existing bound-attempt,
enrollment, physical-stop и exact mask-origin checks не ослабляются.
Для owned gate publication и terminal cleanup вводятся private
`_publish_admission_owned(..., owner, deadline)` / `_finish_owned(...)`:
они проверяют owner до каждого write/replace/fsync/unlink. Existing
`publish_admission` получает optional `before` и передаёт его в
`publish_json`, включая temporary UID switch; utility не превращается в
публичный ownership bypass. `close_after_failure` также получает обязательный
internal owner/deadline во всех production mutating call sites. Emergency
close может сохранить already-failed own receipt, но не открыть gate и не
стереть barrier; нужен live owner + exact gate binding, без игнорирования
foreign intent. Generic `publish` остаётся utility; audit проверяет все
конкретные lifecycle callers.

Допустимые operation values: `whole_update`, `activate`, `prepare_initial`,
`shutdown_capture`, `shutdown_finalize`, `startup`, `stop_update`,
`repair_update`, `finish_update`. Operation — closed internal enum, не CLI
authority. `_activate_owned` разрешает только `activate` либо `whole_update`;
`startup` controller owner не даёт права менять controller release.
`release_identity` — точный `manifest(...)` (release id, application store path,
solver executable и schema), обязателен для release-mutating operations.
`release_id` обязан ему соответствовать. Для shutdown capture/finalize,
которые не меняют release, оба могут быть `None`; такой owner activation
helper никогда не принимает. Startup связывает snapshot текущего release до
захвата, а под lock перечитывает и отклоняет его изменение до mutation.

### Как object доказывает владение

`LifecycleOwner` не является dataclass/десериализуемым набором полей.
Private registry хранит **сильную ссылку на сам object** и закрытые данные;
`type(owner) is LifecycleOwner` и `registry.get(id(owner)).object is owner`
обязательны. Публичный конструктор отказывает; `object.__new__`, copy,
deepcopy, pickle и dict с совпадающими полями не создают запись registry.
Python здесь trusted code boundary, а не sandbox против исполнения
злоумышленного Python кода внутри root interpreter.

Private record содержит:

* PID + start ticks текущего процесса + boot ID; получение ограничено
  локальными `/proc` metadata, missing/invalid поколение запрещает mutation;
* canonical runtime pathname, runtime directory `(st_dev, st_ino)`;
* открытый common-lock fd и `(st_dev, st_ino)`, live/closed state;
* closed operation, точную release identity, исходный deadline;
* только свои зарегистрированные intent/receipt paths и текущую attempt
  identity; paths/UUID сами по себе не являются authority;
* inherited command/output accounting и optional parent checkpoint callback.

При каждом `_require_owner`: registry identity, текущие PID/start/boot,
runtime directory и lock pathname/fd inode, fd ещё открыт и deadline не
истёк; release identity и operation соответствуют вызову. Новый owner не
может принять старый object даже при том же pathname/PID. Deadline helper
равен owner deadline либо меньше; `None` и увеличение запрещены.

Context exit отзывает registry **до** освобождения fd. Non-reentrant:
второй public owner в том же процессе на том же runtime отклоняется;
разрешённый parent helper получает тот же object. `O_CLOEXEC` обязателен.
At-fork child очищает registry и закрывает унаследованные owner fds,
**не вызывает `LOCK_UN` на shared open-file-description parent**.
Проверка PID всё равно отвергает inherited object, включая обход at-fork.
Owner нельзя восстановить из receipt и нельзя передать как CLI/env/base64.

### Lock namespace и смешанная миграция

Runtime должен быть private admin namespace без symlink/traversal и чужой
записи. Production route сохраняет existing root-owned protected-directory
policy; temp fixtures моделируют эту policy контролируемыми fakes, не новым
публичным `unsafe` переключателем. Fd-relative open:
`O_RDWR|O_CREAT|O_NOFOLLOW|O_CLOEXEC|O_NONBLOCK`, regular file, single link,
проверка directory/lock inode до mutation. Не использовать `open("w")`, не
усекать содержимое и не unlink/replace lock file. Защита pathname требуется
для отсутствия split-lock при подмене inode; потеря/замена вызывает unknown.

Общий owner сначала берёт `delivery.lock`, затем **неблокирующий legacy
compatibility fence** `activation.lock`, всегда в этом порядке. Это не
второй независимый owner: capability выдаётся только после обоих flock.
Fence оставляется на всём OPS03 rollout, чтобы уже живой старый standalone
процесс не пересекался с новым update. Contention любого lock немедленно
отказывает без application mutation; первый fd освобождается при отказе
второго. Старый parent delivery не может быть принят как новый owner.
Файлы lock пусты/стары/существуют — это не durable receipt и не permission
очистить intents. Удаление fence возможно только отдельным доказанным
rollout contract после исключения всех legacy binaries/processes.

## 4. Матрица entrypoint → owner → guards

| Entry point | Owner | Обязательная граница |
| --- | --- | --- |
| Public CLI/API controller `activate` | Новый common owner `activate` | Common guard, selected closed gate, protected release settings и local bound identity до ready/profile/Code mutations |
| Public CLI/API `prepare-initial` | Новый common owner `prepare_initial` | Common guard; existing cold-controller-only missing gate rule; exact existing bytes/profiles сохраняются |
| Whole update / deliver | Новый controller owner `whole_update` | Existing protected enrollment, complete pool, trust+identity preflight до writes; повторная authority/guard после flock |
| Controller activation внутри update | Тот же object parent | Private helper, точная parent release/boot, local command route; без flock/SSH handoff |
| Remote worker activate/stop/repair/finish | Новый worker-local owner на каждом invocation | Обычный CLI, exact expected node и existing attempt/marker/closed-gate predicates; parent cap не передаётся |
| Controller normal shutdown | Per-node normal lock на весь finite poll; common owner отдельно capture и finalize | `normal_intents=False` лишь для обработки нормальных intents; остальные update/unknown barriers сохраняются |
| Controller normal startup | Тот же per-node normal lock, затем common owner `startup` | Existing authorized startup event, same machine/new boot, safe scope, no unknown; remote worker получает свой local owner |
| `guard`, identity, capabilities, bootstrap selection, check | Без mutating owner | Existing read checks не превращают observation в writer authority |
| `fleet_health` | Observational API с собственным bounded NFS probe | Controller invocation update выполняется локально под parent owner; worker remote result не даёт права открыть gate |

Public `--returning-worker` сохраняется исключительно как existing worker
open-gate policy predicate. Он не обходит lock, unknown/local-update markers,
node identity или controller guards. `--update-attempt-id` остаётся locator
existing защищённого update marker, а не переносимым owner.
Новых `--owned`, `--skip-lock`, `--ignore-intent` нет.
Standalone CLI не получает нового обязательного `--enrollment` аргумента:
protected release config задаёт actual local role; observed local identity
связывает capability с boot. Если existing expected-node identity передана,
она обязательно проверяется до и после. Whole-update routing по-прежнему
требует полного protected enrollment и trusted controller authority.
Direct API сохраняет existing configurable temp profile/runtime/gate для
fixtures; callers должны теперь предоставить selected closed gate, который
раньше проверяла только CLI. Это намеренное устранение API обхода, а не
новое разрешение запускать standalone при неизвестном admission.

Common guard получает optional internal `owner` для проверки своих
публикаций. Без owner поведение fail-closed для всех unknown сохраняется.
С owner разрешено исключить **только exact зарегистрированный current
operation artifact**, когда schema/attempt/release/runtime binding совпали и
live object валиден. Другие файлы той же attempt-подобной формы, orphan
receipt или собственный файл с `requires_reconciliation=True` не исключаются.
Self exclusion не является glob-by-UUID и не принимает caller list.
Worker `update-stop.json` отдельно классифицируется existing protected
marker validators: разрешён лишь переход того же exact attempt/release/
enrollment/machine/boot и exact mask origin, подтверждённый соответствующим
physical-stop/check predicate. Это позволяет stop→activate→health→finish
между разными node-local процессами без переноса capability. Неизвестный,
foreign или mismatched marker блокирует; `--update-attempt-id` без этих
проверок ничего не разрешает. Gate-open допустим для terminal finish и
existing returning-worker policy, но не ослабляет локальный owner/marker.
Внешний `cluster-update.json` остаётся blocker: OPS03 не вводит I14 adapter,
не переименовывает и не удаляет его. Старые failed/running/pending receipts
проверяются existing правилами `unresolved_deliveries` плюс новыми lifecycle
intents. Повреждённый/unknown schema файл в recognised attempt namespace
требует reconciliation, не молчаливого пропуска.

## 5. Controller parent без self-child

`update-capabilities` получает versioned
`schema=qcl-negf-local-update-capability-v2` и literal
`lifecycle_owner=qcl-negf-lifecycle-owner-v1` в дополнение к существующим
stop/health/AiiDA predicates. Новый parent требует exact v2 на всех enrolled
nodes до gate/quiesce mutations. Старый parent, ожидающий exact v1, тоже
откажет на новом ответе; mixed protocol не принимают молчаливо. Это
capability advertisement совместимости установленного command route, не
владеющий object. Existing manifest/Code/attempt schemas сохраняются.

После existing full identity/capability preflight и локального verified
prefetch parent держит owner до последнего terminal cleanup. Для controller:

1. Повторяет `verify_controller_authority` с enrolled binding, local observation
   и trusted remote identity; hostname/target string не выбирает local route.
   Нужен ровно один enrolled controller, совпадающий с owner local machine/boot.
2. Не делает `nix copy --to ssh-ng://controller`: closure уже verified локально.
3. Загружает protected `/etc/qcl-negf/release-config.json` тем же bounded reader,
   что CLI, проверяет controller role/email/allowlist path.
4. Durable checkpoint записывает `pending_local_mutation` **до** первого
   profile/ready/Code write, затем вызывает `_activate_owned` с тем же owner,
   inherited `dispatch` и одним metadata budget/deadline.
5. Получает local `check(... expected_node_identity=...)` envelope, проверяет
   его existing `verify_node_envelope`. Controller `health-update` из `admit`
   вызывает local `fleet_health`, включая собственный NFS probe. Никакого
   mutating SSH к себе; readonly identity/capabilities SSH сохраняют trust.
6. Только после local/helper postchecks durable checkpoint убирает
   `pending_local_mutation`. Любое отсутствие ответа, crash, write failure
   оставляет pending и/или reconciliation; parent receipt не переносится
   controller child и не создаётся второй admission authority.

Worker copy/activate/check/health/finish остаются SSH через frozen known_hosts
и existing node/attempt identity. Их локальный lock не shared с controller.
Суммарный `used_output` считает controller local commands и remote commands;
исполнитель не создаёт новый `run=command`/budget внутри helper и не
сбрасывает metadata CAP. Local direct helper body входит в parent phase
журнал даже когда между его filesystem writes нет external command.

## 6. State machine и долговечность

Volatile owner и durable operation state разделены:

| До | Условие / действие | После / recovery |
| --- | --- | --- |
| `unowned` | Authority preflight, finite budget, затем оба nonblocking flock | `owned`; contender не меняет profiles/gate/intents |
| `owned` | Common guard + full bindings + expected gate | `validated`; prior unknown → refusal, чужие bytes сохраняются |
| `validated` | Durable exclusive immutable intent, затем running receipt | `mutation_pending`; ошибка durability до mutation запрещает mutation |
| `mutation_pending` | Ready invalidated/false, bounded profile/Code/env/unit actions | `locally_prepared`; любой crash оставляет intent/pending |
| `locally_prepared` | Identity+profiles+self-check+units postchecks | `local_ready`; shared admission всё ещё closed |
| `local_ready` (whole only) | Все node envelopes/fleet/NFS/auth/cancel/Slurm predicates | `admission_pending`, independent CR04 intent persisted |
| `admission_pending` | Gate open publication + terminal receipt | `completed_pending_cleanup`; неоднозначный replace/fsync → unknown + bounded gate close attempt |
| `completed_pending_cleanup` | Own marker cleanup последним, под original deadline | `completed`; сохранившийся после crash marker блокирует retry |
| Любое после mutation intent | Exception/deadline/crash | `reconciliation_required`/running pending; gate closed либо explicitly unknown, никогда fabricated stopped/pass |
| `completed`/refused-before-mutation | Revoke object → close fds | `unowned`; original receipts остаются |

Standalone activation/initial preparation создаёт в existing
`runtime/delivery-attempts` отдельный immutable
`<uuid>.lifecycle-intent.json` (`schema=qcl-negf-lifecycle-intent-v1`) через
exclusive nofollow mode0600 create, file fsync, directory fsync **до**
первой mutation. Поля: attempt id, operation, exact release, node/runtime
binding, started time, marker purpose. Это durable inhibition, не capability.
Рядом `<uuid>.json` — phase receipt с предшествующими bounded snapshots/
hashes, attempted/completed boundary, outcome и reconciliation. Любое
присутствие lifecycle intent блокирует другие operations; своего marker
может не бояться только зарегистрированный live owner.
При успешном standalone завершении terminal receipt fsync предшествует
own intent unlink; unlink — последний fallible success step. Ошибка после
mutation оставляет immutable intent, даже если report записать не удалось.
Ошибку самого intent fsync трактуют консервативно: mutation не начинается,
оставшийся файл не стирают автоматически. Failed-known до mutation может
быть terminal без marker; после первого persistent изменения не делают
автоматическую классификацию retryable по exception/exit code.
Original `release.json`, `service.env` и allowlist bytes сохраняются bounded
base64 snapshot (≤64 KiB каждый), profile symlink targets — как строки;
hash без original bytes не является обещанным сохранением исходного
состояния. Protected settings/secrets в public report не копируются.

Whole update сохраняет existing CR04 receipt/admission intent protocol;
`unresolved_deliveries` дополнительно проверяет `pending_local_mutation`.
Перед любой самостоятельной whole mutation нужен уже durable pending marker
или persisted pending command; bare callback без journaling запрещён.
Public `deliver_pool` с optional external `checkpoint=None` обязан сам
создать lifecycle intent/receipt, чтобы direct API не обходил crash barrier.

**Граница final admission:** текущий `guard` около 1071 проверяет только
worker `release.json` и shared gate, а не controller-local CR04 intent.
Crash строго после authorized open replace, но до terminal receipt/fsync
может оставить raw gate open. Owner и сохранённый intent блокируют blind
повтор update, но этого недостаточно для доказательства, что все job readers
видят effective closed admission. OPS02 не заявляет более сильное свойство.
Для требования «каждая crash оставляет effective job admission closed»
нужен отдельный owning D на atomic admission-commit/read protocol со всеми
consumers, а не удаление intent или новое поле, которое читает только writer.
O08 проверяет local activation cuts до разрешённой gate-open phase; O09
измеряет existing final-publication closed/unknown outcomes. Если R считает
сильное effective-admission свойство обязательным для CP-DESIGN этой
карточки, это явный отдельный dependency, не pass по согласованию агентов.

Deadline checks ограничивают progression между syscalls. Они не прерывают
уже выполняющийся filesystem/NFS fsync атомарно; истёкший deadline после
replace означает unknown publication и сохранение blocker, а не отсутствие
произошедшего write. Cleanup использует только оставшийся исходный budget;
по истечении нельзя удалять intent, объявлять closed или начинать новый
recovery budget. Native syscall stalls/power-loss отдельно не измерены.

### Publishers: обязательный before / after

| Publisher / boundary | До | После / failure |
| --- | --- | --- |
| `release.json` invalidation | Live owner, original bytes/hash captured, durable pending, exact selected gate | Missing либо ready:false не выдаётся за ready; original evidence в receipt; unlink durability неоднозначна → marker остаётся |
| application profile `nix-env` | Owner/deadline, selected immutable contents verified, own pending | Resolve exact selected store path; каждый profile — отдельный GC root |
| solver profile `nix-env` | Те же checks независимо от app profile | Resolve solver closure; отсутствие root не прикрывается совпадением app/release id |
| AiiDA registration subprocess | Owner+durable pending, protected email/solver/label, Code invariants | Exact returned immutable executable/UUID; subprocess пишет bootstrap/code-uuid под lifetime parent, без переноса cap |
| configured Code allowlist | Повтор owner/deadline после subprocess; old bytes/hash retained | Atomic publish+file/dir fsync, exact UUID; при unknown нет services/ready progression |
| `service.env` | Owner, exact release/executable/**переданный `gate`** | Verify expected bytes; использовать `str(gate)`, а не захардкоженный `str(GATE)` |
| ready:false record | Owner/pending; bound node identity | Complete atomic record перед service start; readiness не наследуется от old record |
| start/restart units | Profiles/Code/env complete, deadline, bound machine, existing worker stop/mask proof | All required units active + solver self-check + bound identity recheck; timeout не remote-stop proof |
| ready:true record | Повтор owner/deadline и profile/identity health | Atomic publish/fsync; только local readiness, gate не открывает |
| gate close/open / failure recovery | Common controller owner, prior/current gate binding, durable parent intent | Existing CR04 semantics; unknown recorded; чужой mismatched release gate не перезаписывается для apparent repair |
| intent/receipt finalization | Live owner, matching own inode/schema/attempt, original deadline | Удаляется только own marker последним; write/cleanup failure сохраняет inhibition |

Registration child после смерти parent теоретически может ещё завершать
local mutation; flock сам по себе это не устраняет. Durable pending запрещает
следующему owner mutating progression до trusted reconciliation. Не заявлять
kill SSH или освобождённый flock доказательством остановки remote/child effect.
Безопасный recovery выполняет existing trusted operator owner, устанавливает
actual process/profile/Code/env/gate state и сохраняет original attempt.
Новый `--force`/auto-reconcile API в OPS03 не вводится.

Identical **успешно завершённый** release с повреждённым app или solver GC
root допускает новую standalone attempt при closed exact gate и отсутствии
unknown. Ремонтируется только несовпадающий root; `register_aiida` обязан
возвратить сохранённый immutable Code UUID, несовпадение не принимается.
Повтор с тем же release после orphan/pending marker сначала требует trusted
reconciliation; identical release не является способом сбросить unknown.
`prepare-initial` сохраняет exact existing record/env/Code/provenance bytes;
не превращает уже существующую установку в cold ради missing gate.

## 7. Normal worker lifecycle: порядок и ожидание

Оба controller entrypoints `shutdown_step(node)` и `startup(node)` берут
один existing `runtime/shutdown-<node>.lock` nonblocking на весь finite
invocation. Порядок всегда **per-node normal lock → common owner**.
Whole update per-node normal lock не ждёт: под common owner он видит durable
normal intent и отказывает. Обратного порядка locks не вводить.

Capture: fresh authority/binding → common owner `shutdown_capture` → guards
→ durable capture_pending до DRAIN → merged complete scope → awaiting_jobs
durable → common owner release. Runner pause/verify-stop выполняются вне
common owner, под тем же per-node normal lock; каждый poll имеет исходный
finite deadline, даже если внешний операторский цикл ждёт неограниченно.
Другой node может выполнить capture/finalize. Тот же node startup/shutdown
получает contention до mutation.

Finalize: новый short common owner `shutdown_finalize` с тем же исходным
poll deadline → authority recheck → exact shutdown id/boot/phase → final
queue + verified scoped stop reread → safe_to_power_off только при полном
scope. Dead capture/incomplete/orphan либо vanished job без stop receipt не
становятся safe на пустой очереди. Прежняя legacy-v1 migration сохраняет
original raw и reconciliation, без изобретённого boot proof.

Startup: per-node lock → common `startup` → existing safe/new-boot/event
checks → durable returning intent → worker remote local activation/check →
identity+guard → independent admission intent до RESUME → resumed receipt →
own marker removal последним. Common owner не отпускается между health и
RESUME. Startup event, normal intent, update receipt и lifecycle owner —
разные сущности. Отказ/чужой marker не разрешает обычному startup clearing.

## 8. OPS03: конечный implementation packet

Допустимые source edits: только
`ops/application_release.py`, `ops/worker_lifecycle.py`,
`tests/test_application_release.py`, `tests/test_worker_lifecycle.py`,
`tests/test_worker_shutdown_intent.py`; accepted документ позже публикуется
как предложенный `docs/lifecycle-ownership.md` owning Platform. Один writer.
Не менять Nix modules/bootstrap scripts в этом packet. Никаких SSH/Nix/
services в checks, новых dependencies/installs/full builds или solver.

Порядок после CP-DESIGN:

1. Добавить independent recording oracle и regressions ниже. Positive local
   parent scenario выполняет реальный `_activate_owned` и real temp file
   publishers с fake external commands, а не mock всего helper.
2. Ввести opaque capability, fixed lock order/fence, revocation и journal
   helpers, затем owner wrappers и local controller routing. Guard routing
   предшествует first mutation; сохранить existing enrollment/trust/pin gates.
3. Перевести normal lifecycle на accepted node/common lock order. Добавить
   bounded crash cuts и legacy/foreign controls; обновить старый тест,
   который утверждает именно старый `activation.lock`, на общий owner contract.
4. Independent R рассматривает exact diff, control assertions, command output
   и final source hashes; coordinator закрывает CP-CODE в пределах grants.

### Обязательные fake сценарии и oracle

Каждый child имеет wall-clock watchdog ≤5 s, в multiprocessing используется
explicit pipe/event handshake; отсутствие сообщения/таймаут — failure,
а не sleep-based доказательство. Все внешние argv должны отклоняться, если
fake boundary их не распознал. Independent mutation ledger отдельно
регистрирует profile symlink writes, record/env/allowlist/gate bytes и
mutating command calls. Ожидаемые значения — literals fixture, не output
production validator.

| ID | Setup / действие | Обязательный отрицательный или положительный результат |
| --- | --- | --- |
| O01 | Process A holds whole-update owner после validated pre-mutation handshake; process B invokes real public controller `activate`/CLI с matching closed gate | B fail-fast contention; ноль application/Code/env/ready/gate mutations; прежние bytes hashes равны |
| O02 | Reverse: A standalone activate owner, B whole update | B не достигает quiesce/DRAIN/copy/gate publication; per-process preflight reads допустимы |
| O03 | Parent update real local helper при уже held owner; instrument flock call count | Один acquisition common + один fence на owner, controller helper ноль; update доходит до envelopes; no mutating self SSH или self nix copy |
| O04 | Arbitrary object, dict, `object.__new__`, copied/pickled token, caller UUID/PID | `_activate_owned` отказывает до first filesystem/command mutation |
| O05 | Real token: wrong runtime/release/operation/deadline, expired context, closed fd, changed lock/runtime inode | Каждый case отказывает до mutation; marker/foreign files не удаляются |
| O06 | Fork child inherits real object; parent ещё holds lock; затем parent exits | Child cannot use token; child cleanup не unlock parent; после parent exit новый owner берёт flock, но orphan journal blocks mutation |
| O07 | Deadline expires после profile/registration response, до allowlist replace, до ready publish и до intent unlink | Нет следующей mutation/start/open; no new budget; marker сохраняется; original failure outcome |
| O08 | Standalone/local-helper crash cuts до authorized whole gate-open: after pending durable; app profile; solver profile; registration/Code allowlist; service.env; ready:false; unit start; ready:true; before local terminal publication | Kill child на pipe handshake; next standalone/update не mutates, local activation никогда не открывает gate; исходный marker/receipt/snapshots retained |
| O09 | Inject write/replace/file-fsync/dir-fsync failures в intent, ready record, terminal receipt и gate open/close | До durable intent — no mutation; после — blocked/unknown; close failure не становится closed; original failed receipt retained |
| O10 | Prior CR04 intent, running mutating receipt, pending_local_mutation, cluster-update marker; также чужой exact-looking same UUID файл | Guard refuses; собственный cap не исключает foreign/unknown; zero clearing/overwrite |
| O11 | Legacy process holds только activation.lock; new update/activate; отдельно legacy delivery.lock | New owner fail-fast на соответствующем fence/common lock; не deadlocks; files/intents unchanged |
| O12 | Completed same release; повреждён только solver GC root (и отдельно app root) | Только один соответствующий nix-env; оба exact roots после; Code UUID тот же; gate closed; при orphan marker тот же retry refuses |
| O13 | Cold initial controller и existing exact installation | Только cold controller может создать missing closed gate; worker/missing gate/existing runtime refuses; exact existing bytes preserved |
| O14 | Controller forged expected identity / enrollment / trust snapshot / local-vs-remote controller mismatch | Reject before application mutation; local routing не превращает target name в authority |
| O15 | Shutdown node A waits Runner; node B captures; update/activate и same-node startup contend | Common flock доступен node B; update/activate blocks на durable A intent; same-node startup blocks на node lock; no RESUME |
| O16 | Startup/capture/finalize vs update interleavings, vanished job, orphan capture, terminal replace failure после RESUME | Existing independent markers retain inhibition; no invented safe/resumed outcome, no duplicate recovery submission |
| O17 | Worker-local stop/activate/finish race при разных remote parent attempt IDs | Node-local owner serializes finite invocation; exact marker/identity guard rejects foreign attempt; no mask removal by lookalike |
| O18 | Controlled expired/no owner call to gate/open/final cleanup helper | No admission publish/unlink; lower-level generic publish primitive остаётся utility, production mutating call sites audited |

O08 — конечная параметризация перечисленных cuts, один child на cut, один
контролируемый повтор для проверки blocker; не random chaos loop.
Никакой synthetic pass не заменяет native power-loss/NFS/Slurm receipt.
Provisioning/OS writer controls являются отдельным follow-on/native residual,
не спрятанным skipped success.

### Команды и бюджет будущего OPS03

Из component directory максимум **4 Python invocations вместе** по L:
1 CPU / 2 GiB / 60 s / 1 MiB на invocation, без install/full suite.
Первый — regression selection (red), затем три named test files (green):

```text
python3 -m unittest discover -s tests -p test_application_release.py
python3 -m unittest discover -s tests -p test_worker_lifecycle.py
python3 -m unittest discover -s tests -p test_worker_shutdown_intent.py
```

Координатор выбирает точную red selection из добавленных tests, в receipt
фиксирует command/attempt/start/end/resource cap/output bytes/final source
hashes и counts. При невозможности вместить red+green+review repair в четыре
invocations нельзя сбросить счётчик; technical coordinator решает перераспределение
внутри активного общего DEV envelope. Этот D не тратит ни одну invocation.
Один implementation pass, один reviewed repair; same unexplained failure/
deadlock или contract ambiguity возвращается D, без blind rerun.

## 9. Review packet и утверждения

Первому fresh R переданы первичные source и вопрос без авторского диагноза:
проверить один controller writer для standalone/whole/normal worker lifecycle,
отсутствие self-deadlock/переносимой authority, определить needed publishers,
unknown/migration/crash barriers и минимальные controls. Затем R получает
этот exact artifact hash. Review отдельно оценивает provisioning residual:
OPS03 bounded closure либо обязательная prior follow-on D.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Текущие standalone/whole routes используют разные locks | Platform `6c5b11f` `main` / `deliver_cli` / `_deliver_cli_locked::deliver`, hashes §1 | Source counterexample, не native incident | изменить |
| Local opaque owner и local controller helper устраняют конкретный bypass/self-child cycle | API/lock/guard/route contract §§3–5, future O01–O07/O11 | Дизайн; checks не исполнены | изменить |
| Common owner не заменяет unknown/recovery authority | Existing `lifecycle_guard`, CR04, normal intents + §§6–7 | Crash/fsync/native outcomes не измерены | сохранить |
| Independent app и solver GC roots/Code identity сохраняются | Existing `activate` profile loop / `register_aiida.reconcile`, §6/O12 | После orphan сначала reconciliation; native GC не проверялся | сохранить |
| Все OS/provisioning publishers уже покрыты OPS03 | Противосвидетельство `modules/{application,release}.nix`, bootstrap chain §1 | Вне accepted OPS03 edit set | данных недостаточно |
| Native application-only deployment безопасен при verified phase exclusion | Required inhibition+exclusive-window predicates §1; future native receipts | Fresh inventory/admission и mechanism proof отсутствуют | дополнительно измерить |
| CR04 intent гарантирует effective closed job admission на каждом final-publication crash | `guard` читает ready+gate, не controller-local intent; §6 | Separate admission commit/read contract не спроектирован этим D | данных недостаточно |
| Scientific/native acceptance выполнена | Отсутствует; этот D использует только чтение | Tests/services/SSH/Nix/solver не запускались | данных недостаточно |
