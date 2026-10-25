# D4 — focused high re-review R1/R2

**Вердикт: SOURCE PASS для начала I2 по R1/R2.** Новых блокирующих design
замечаний в этом focused scope нет. Это не native-ready, не проверка реализации
и не разрешение DEV/native/final CI запуска.

## Immutable binding

D4 SHA256 `24a7d68b612e7d3dc437404bb805df777ede1f5159c0bff39eca7d693ebe8fc0`;
identity `f1b21f21cc54958c62eed33ac518683d928d3e09a4667c619fc3682b78ea2107`;
delta ledger `0b5a817a42afcdbdb93d1be39cedd32b3506f036901bcc368d95dc6d0f0c9c17`.
Governing D3 и его high review228adacf… сохранены. D4 прочитан целиком;
truncated middle104–125 перечитан отдельно. Selected HEAD повторно прочитан:
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`, прежние4 tracked routing edits и2
untracked helper/fixture. Product/CP/git writes=0. Без parser/compiler/import/
test/probe/network/native/build/solver/CI. Только этот report и identity.

## R1 закрыт на уровне source API

D4:9–38 выбирает один RootDocsSetupV1 и concrete start_docs_setup constructor.
Expected inventory/source/bootstrap и execute_grant поступают из уже trusted
parent до repo execution. Native16/self-hash/record/getuid не объявляются
authority. Неизвестный actual trusted parent/wrapper — явный operator prerequisite;
отсутствие server credentials сейчас не требует придумать новый trust root.

D4:42–52 отменяет ambient Python: exact admitted absolute interpreter,
`-I -S -B`, clear startup env, immutable pre-admitted runtime/stdlib closure и
pre-exec source binding. Это решает замечание о site/PYTHONPATH до self-check.
CPP должен проверить реальные imports/argv и parent prerequisites; isolated flags
сами не доказывают доверие runtime. D2 Python unit argv не меняются.

D4:56–80 задаёт parent pipe ACK/go/EOF, broker peer/subtree checks, single-use
phase records/token lifetime, exact client hello и tasks. Pipe не надо протаскивать
через Deno task; клиенты используют broker с выданным live phase token, который
сам по себе не заменяет peer/source/input/attempt/deadline. Пропагация full через
ops/ci описана; preflight имеет отдельный consumed token. Реализация может иметь
valid route при наличии этих prerequisites, вместо always-blocked stub.

D4:84–104 задаёт exact private tool observation fields, reader/raw/version
predicates и independent parent-populated registration. Нет hidden probes в
preflight; measurement stage требует отдельного scope. Existing records без live
accepted inventory registration не могут авторизовать себя своими booleans.
Фактические tool records/parent wrapper сейчас не доказаны — это сохранённая
runtime/operator граница, а не неопределённый parser/factory для I2.

## R2 закрыт на уровне source API

D4:108–125 вводит injected GitReader во все owning sourceGraph calls; native
driver имеет zero script grants, default git→process.run→output не выбирается.
Allowed root/argv closed, native side запускает exact absolute Git. Это сохраняет
owning graph semantics и переносит process execution в контролируемый native path.

D4:129–152 включает setup/driver/Git в ownership/cgroup/deadline/capture **до**
first repo child, оставляет bounded outer control reserve и durable pre-child
intent. Git имеет finite per-command/snapshot/phase bytes/time/count limits;
complete capture precedes parsing. NUL framing ls-tree не ошибочно трактуется
как invalid descriptor. Driver OOM/EOF и terminal source refusal сохраняют
completed captures и typed missing/unknown outcome. Это устраняет исходный
unbounded binding subprocess gap дизайна.

## Обязательные проверки I2 CPP, без нового design blocker

- Замкнуть actual protocol unions/state machine для `git-read`, включая response
  shape и encoded-frame bound: D3 transport frame limits и D4 raw Git262144B —
  разные ограничения. Реализация обязана bounded-refuse frame, который не
  помещается, либо использовать явно ограниченный reviewed transport; нельзя
  allocate/readAll до проверки и затем объявить его bounded.
- Посчитать actual call/byte schedule initial/per-step/prelaunch/final binding
  целиком в≤512 Git children/8MiB phase raw и shared deadline. Per-snapshot maxima
  не гарантируют, что сумма fits. Повторное чтение, неудачи и cleanup debit не
  обнуляются. Бюджет smaller-than-required даёт blocked, не source acceptance.
- D4:125 требует отсутствия других executable helpers в Git metadata route.
  Проверить local config/attributes/filter paths на actual native branch;
  fsmonitor/hooks flags сами по себе не служат общим доказательством no-exec.
  В текущем uninitialized selected tree rg не нашёл .gitattributes; это не
  свидетельство о final initialized8components/native config.
- Source16 closure должна включать actual imported code и producer/client/driver,
  final committed HEAD и tool/runtime/Git bytes. CPP проверяет zero bypass через
  default git/run/output, no accidental task allow-run expansion и failure
  retention, а не только совпадение имён API.

Эти требования уже следуют D3/D4 и решаются в owning implementation/CPP;
они не требуют свежих measurements или нового архитектурного решения до I2.

## Неизменённые gates

Exact12 descriptor, D2 dedicated maps/argv, D3 fixed13-node seed/TMP debit,
sourceGraph-throw retention, historic RED04589… и отдельный current narrow typing
hash сохраняются. Source PASS не grandfather additional fixture assertions или
registrations под historic227; отдельная reviewed mapping остаётся обязательной.

Два manufactured protocol DEV calls D4:156–163 — **предложение**, не часть
milestone6/slots81→87, не sole pure227 GREEN и не execution authority этого review.
Root должен отдельно заморозить finite plan/attempts/source/runtime/harness/count
bindings и ledger slots перед ними. Fake controls не доказывают live startup,
peer identity, subreaper/pidfd/cgroup/OOM или actual tool report compatibility.

Trusted external job-launch parent, fresh independently admitted runtime/tools,
actual wrapper integration, live delegation/storage/allocation и parent watchdog
остаются обязательными prerequisites. Их отсутствие должно блокировать конкретный
native attempt; нельзя списать source wiring/reader/supervisor stub на отсутствие
сервера. Final CI и scientific acceptance этим review не затронуты.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 позволяет реализовать действующий source route | D4 constructor/startup/registration/broker/tasks | Actual trusted parent ещё prerequisite | сохранить |
| R2 закрывает unbounded native Git path | Injected reader + pre-child guard/caps/retention | Реализация ещё не проверена | сохранить |
| I2 source/API готов к реализации | R1/R2 exact overrides, CPP obligations выше | Source PASS только focused scope | изменить |
| DEV/native/full CI уже разрешены или проверены | Ни запусков, ни нового execution grant нет | Отдельные plans/evidence gates | данных недостаточно |

Reads консервативно<512KiB, wall<10min. CPU/RSS/physical I/O отдельно не измерены.
STOP; production source/CP edits и execution=0.
