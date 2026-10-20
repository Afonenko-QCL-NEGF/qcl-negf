# I2C — independent high source CPP

**CHANGES REQUIRED; native source candidate не READY.** Конкретные дефекты
queued phase-ready, KaTeX self-SHA, irreversible full-cap debit, cumulative512
и always-failed setup исправлены в исходниках. Полные группы C3/C4/C6/C7/C8
ещё не закрыты; в частности, source failure ошибочно становится `measured`
при наличии rejected validation receipt. Следующий шаг — узкие code/fixture
исправления в тех же owning files, без нового design-only цикла.

Это source review: ни actual wire/syscall execution, ни pass восьми методов/
восьми registrations, ни source build/compiler/native acceptance не заявлены.
Неизменённый pure676a…/current230f02f… остаётся независимым later gate.

## Frozen packet и owning manifest

| Артефакт | SHA256 |
| --- | --- |
| I2C report | `56a4dc2179353ad20a4a40879a4e5f9aabd74871d0b82c6081156fc92d632bac` |
| I2C identity | `398e5004484dd86b93f5f2cc701b8f1cd77b96d120ae43a05c86d180bd00b9e9` |
| complete237096B patch | `7fd92c7f21bcc63e16872fc7ea0f25b6267324e1277f2fa5a3c221a2ab61c13e` |
| Prior I2B high CPP, неизменён | `4903c3d64d8254a7b4ac89fcc08efed049485a21b1a1c155922b515b6118c4ea` |

Selected `/tmp/qcl-docs-test-routing-worktree`: actual HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`,5tracked+6untracked source files,
8uninitialized прежних gitlinks. Review locators относятся к actual frozen
overlay, не к committed содержимому HEAD. Packet hashes и actual четыре
changed paths сверены; original I2B report/identity/patch повторно совпали.

| Только четыре I2C owning paths | Actual SHA256 | Bytes |
| --- | --- | ---: |
| `ops/docs_tests_native.py` | `5b43a26b416d127cfb606898bd617145af8df7e50ee7001c4228aa3d61ca4adb` |126239|
| `ops/docs_tests_cli.ts` | `b89aa1da8cdebf3544212f19ac2454671478819d382082f2be5b8444b6889d3f` |15121|
| `tests/test_docs_test_native.py` | `29fd56b6882b81e915cd46464614245b3b6a2bf1361441aa9f0d2467e3a6ba2b` |10567|
| `tests/docs_test_native_protocol_test.ts` | `48628f79ef3b4ffde506f90be81577834c3a422543fd26e19405b2523326721b` |5056|

Pure helper SHA `676a3db1a4de455bbd73a46e57f316b4ae7721e631aa3b7d81a2da8564340d8c`,
fixture SHA `f02f541d633c56280077701ba9fbee3928ae7c2e055cae8b2e78d759bd3a9761`
перепроверены: byte-identical. Complete patch headers — те же11overlay paths;
его применение/исполнение не выполнялось. Native16 working sizes из packet
не объявлены committed clean binding. D4/D5/D6 сохраняют authority.

Сначала actual parent/reader/schedule/cleanup/protocol source, затем авторский
report; narrative candidate не принят как доказательство. Обрезанные tool
outputs не считаются полностью прочитанными; relevant sections перечитаны.
Лимит reads8MiB соблюдён: conservative content upper bound<3MiB. Review wall
<15min, output<48KiB (<192KiB); CPU/RSS/physical I/O не измерены. Нет target
imports/parser/compiler/tests/runtime/network/native/source/CP/index writes.

## Диспозиция восьми I2B findings

| Группа | Что действительно исправлено в source | Что не закрыто |
| --- | --- | --- |
| C1 parent | `1555–1649` общий dispatcher/pump, await_phase, gated launch; `1678–1716` actual producer/participant refs, original guard, conditional complete вместо always failed | C3 exact terminal scalars/attachments, C4 error closure, C8 complete two-phase controls; external trusted lease остаётся runtime prerequisite |
| C2 retained | `1036–1043` persisted KaTeX без self-ref, external ref только projection; `1046–1052` exact unit record; `494–526` runtime manifest bytes/files/hash/size/unique entries | C3 all producer/scalar/ref validation; actual admitted records не созданы этим review |
| C3 union/intents | `130–137` D5 AuditIntent fields; `1060–1103` request keys; `1768–1780` full runtime/capsule ACK comparison; `1848` phase intent до driver | Nested scalar/authority/ref schemas не closed; tiny task durable intent и several unvalidated labels остаются |
| C4 cleanup | pre-child command ledger; reaped exception fallback; `run_phase` prebinding внутри try; DriverPipe object удержан до init; real stderr pipe/EOF; inherited close попытка | First-FD failures, remaining FD≥4096, cleanup exception/final publication, source/retention statuses и failed I/O ownership transfer не замкнуты |
| C5 debit | `388–402` outstanding reservation отделён от actual committed bytes; raw full-cap больше не списывается как actual; handoff/final writes charged | Полный executed write/failure trace отсутствует; некоторые writes/unknown fallback/transport paths не tied к одному durable ledger |
| C6 budgets | `1472` phase counters reset; `1106–1143`100/444+families admission; binary blobs; snapshots/tickets имеют guards; noexec scan добавлен | Exact ordinal root/argv/state, source-observation truth, terminal/failure reserve и metadata race coverage недостаточны |
| C7 protocol | Depth/finite numbers, before-atob chunk cap, per-op bounds, rejected finish ACK, raw report-summary comparison | Closed response/refusal/terminal schemas и finite scalar types остаются неполными; cap mismatch для refusal; actual state transitions не controls-tested |
| C8 fixtures |8Python+8Deno сохранены; добавлены isolated dispatcher/KaTeX/terminal/ledger/codec cases | Нет полного healthy fake parent→kernel→broker→driver→executor→whole-empty route и paired failure matrix |

Узкие concrete fixes C1 queued/C2 self-ref/C5 full-cap/C6 cumulative counter
можно сохранить и не реализовывать заново. Их source closure не превращает
полные C1–C8 в acceptance PASS. Остаточные обязанности нужно проверять там,
где они исполняются, а не ссылкой на количество добавленных subcases.

## P1-A: source/retention labels не выводятся из наблюдений

`native.py:1528–1535`: `bind_native_context` может бросить на финальном Git/
blob/source read. Catch устанавливает failed, но затем создаёт **rejected**
validation receipt. `:1550` выбирает
`source_observation='measured' if validation_ref else 'not_measured'`.
Следовательно неизвестное source observation объявляется измеренным лишь из-за
успешной записи документа об отказе. Это нарушает D3/D4 pure/native boundary;
process failure остаётся failed, но evidence status неверен.

Там же `retention_status='complete' if terminal else 'partial'` зависит только
от driver terminal. Native command index мог не сохраниться (`:1547–1549`),
prefix/ref мог остаться unknown, а driver всё-таки корректно вышел. Его EOF/reap
не удостоверяет retention предыдущих command artifacts.

Нужно хранить independent typed source observation state и retention ledger;
measured появляется только после полного binding, not_measured при read/parse/
transport refusal; failed mutation и unknown — разные outcomes. Complete
retention только по actual required raw/receipt/index refs. Первичный failure
сохраняется при финализационных ошибках. Добавить source-final-throw после
completed captures и missing-index controls с проверкой exact status/ref set.

## P1-B: первая ошибка FD/fork/cleanup всё ещё вне полного guarded owner

`execute_bounded :738–752`: socketpair, pipe2, fork и первые closes находятся
до try. При pipe2/fork failure часть FDs остаётся открытой, command pending
есть, но cleanup owner ещё не установлен. `Active.command :966–973` резервирует
raw, затем metadata и пишет pending до своего try: failure второго reserve/
pending write не закрывает первый reservation как known unused.

`DriverPipe :1235–1246` создаёт owner/reserve/file/несколько pipes до guarded
fork. `close(pid is None) :1325–1332` закрывает лишь subset names, не все
возможные read/write gate/pipe FDs и не settle stderr reservation. Worker
prctl/owner initialization остаются до try (`:638–639`); native final fallback
лучше прежнего, но не заменяет bookkeeping каждого first-FD outcome.

`:1256` закрывает только3…4095. У bootstrap control_fd нет upper bound4095,
поэтому inherited control FD≥4096 переживёт exec. Закрыть actual inherited
FD set/пометить единственный passed control FD noninheritable до создания
driver, не предполагать маленькие FD numbers. Paired control должен дать
parent FD выше4095 и проверить отсутствие его в exec-visible whitelist.

`DriverPipe.close :1341–1375` может выйти на stderr write/drain error раньше
TERM→KILL/owner close; в finally fsync/stat/commit могут снова бросить и
пропустить последующие close. `run_phase :1543–1550` ловит close failure,
но не исполняет отдельную независимую bounded cleanup для сохранившегося
driver. Source contract требует explicit unknown+outer escalation, actual
partial evidence и release accounting, не надежду на удачный finally.

Нужен один owner от первой allocation, idempotent close для каждого созданного
handle, nested error-preserving finalization и fake first-socket/pipe/fork,
stderr short-write/fsync/stat/commit/TERM/KILL/deadline controls. No foreign
signals, no premature kill единственного subreaper сохраняются.

## P1-C: публикация receipt пока не соответствует durable terminal claim

`retain_record :824–835` пишет непосредственно окончательное имя и fsync-ит
file; parent directory не fsync-ится, отдельного atomic complete publication
нет. После partial write окончательное имя уже занято, а после crash нельзя
считать filename durable только по file fsync. D3/D4 требуют durable original
intent/terminal publication и no overwrite.

Реализовать exclusive pending→no-replace final publication с directory durability
и actual SHA, сохранив partial files при отказе. Либо exact equivalent owning
filesystem primitive с теми же гарантиями. Тестовые injected handles должны
различать partial file, complete data, published name и directory sync failure;
никакой rejected/unknown publication не получает complete durable ref.
Это implementation correction принятого контракта, новый design документ не нужен.

## P1-D: exact source/Git state и budgets ещё не полная acceptance proof

Из source арифметика исправлена:

- Graph36, native16 binding32; preflight100, full444Git +4units; phase counters
  reset в1472, global storage/deadline остаются прежними.
- Family-derived raw bound проверяется как7graph+6native для full плюс256KiB;
  calls+16≤512, raw+reserve≤8MiB; native blob family требует bytes/SHA.
- Metadata formula2026496B<2097152B в `1138–1139`; ранее111MiB/62.4375MiB
  искусственного committed debit больше нет. Это условный analytical cap, а
  не actual frozen inventory или trace writes.

Однако `run_phase :1494–1501` считает любые36permitted Git calls snapshot,
не сравнивает exact ordinal owning root/argv sequence. prepare/execute
проверяют plan/index, но не требуют полного завершённого source slot, и любой
не-finish op может предшествовать положенному preflight. `bind_native_context`
не отмечает snapshot ledger для своих32reads. Failure raw/time дебиты в
`git_read :1012–1017` происходят только после возвращения command; throwing
capture оставляет соответствующий Git budget вне этого counter, хотя native
raw storage debit уже состоялся. Следующие finalization bindings не должны
терять этот расход.

`noexec_git_metadata :1146–1186` — полезная защита от filter/include indirection,
но это отдельный pre-read без retained config/attributes identity recheck на
actual dispatch. Не считать mere successful scan общим доказательством stable
no-exec source closure. `.gitmodules` section regexp `1074` также уже owning
`sourceGraph`: он отвергает допустимые owning section spellings вне
`[A-Za-z0-9_.-]`, вместо exact bounded string из bound `.gitmodules`.

Нужно exact native operation/source-slot ledger derived from owning graph order,
phase/snapshot counters charge in finally для failures, final/cleanup reserve
до unit dispatch и config/attributes byte/stat identity binding. Никаких новых
Git probes или default git/run/output bypass. Unit physics/public model/caps
не меняются. Parent-controlled family inventory нельзя выдумать из удобных
нулей: отсутствие actual final source freeze блокирует конкретный attempt,
а отсутствие этих guards — source completion.

## P1-E: nested schemas/scalars и terminal/refusal wire ещё открыты

`validate_request :1060–1103` существенно улучшен, но например Git family
проверяет неотрицательность **суммы**, а не каждого stdout/stderr upper bound;
components revision/url, limits/pids, every storage limit/control_dir, tool
version/hash, registration binary_cap/reserve/delegation fields не имеют полного
finite exact typed contract. `record.tool` и `duration_ns` в tool reader не
проверяются (`494–538`); observation UTC сравнивается строками без полного
calendar/type validation обоих timestamps. Terminal validator `1723–1729`
не ограничивает exit/signal/identity scalar types/ranges/ref shape целиком.
JSON bool не должен проходить как integer через равенство0/1.

`launch_phase :1649` передаёт tiny `{phase,binding_digest}` как durable_intent,
тогда как D5 задаёт exact bootstrap/phase union. Уже сохранённый producer
phase-intent полезен, но parent launch adapter должен связывать тот actual
intent/ref либо передавать нормативный redacted projection; не заводить третий
неописанный audit format. Никаких raw capsule/env/nonce dumps.

TS `runDriver :99–105` принимает metadata без exact full response validation;
other response/terminal/refusal branches также не имеют единого exact union
reader. `transport` caps для git-read4096/prepare16384 в `186` не учитывают
допустимый D5 typed refusal≤16384 для любой операции: корректный larger refusal
при git-read превращается в generic frame error, теряя typed refusal context.
Native generic frame buffer bounded, но per-op bound применяется уже после
decode (`1309–1314`), без exact active slot-based reader bound.

Нужны closed schemas всех существующих unions, finite integers/ranges/enums/
refs и per-state reader bound. Rejected finish теперь существует и сохраняет
validation receipt — это исправление; его source/retention labels и all-error
delivery cleanup должны удовлетворять P1-A/B. Не менять chunk/Capture contracts.

## P1-F:8+8 controls остаются isolated seam coverage

Все Python methods и Deno registrations прочитаны. Новые Python cases
(`73–103`, `119–145`) напрямую вызывают dispatcher/terminal/ledger/KaTeX
readers через mocks; это meaningful source subcases, но не fake-process lifecycle.
Control с queued phase-ready не запускает `_pump→bind_phase_leader` для второй
фазы. Terminal proof case не вызывает `_await_terminal` positive/negative
predicate и whole-empty. Deno healthy graph tests вызывают injected sourceGraph,
а healthy runDriver→prepare→capture chunks→finish lifecycle отсутствует.

Нет fake before-exec gating, fakeproc/pidfd/cgroup ownership, first-FD failure,
partial drains/storage-full, driver/producer loss, parent EOF/cancel, two phases
и final setup proof. Поэтому C8 сохраняется P1 до native source acceptance и
DEV readiness. Добавить source controls **самих owning paths**, а не ещё
booleans equal true в helper doubles. У каждого негативного case — exact
forbidden dispatch count и original/partial refs/status evidence. Nominal8+8
можно сохранить, но расширение denominator требует отдельной frozen mapping.

## Минимальные следующие code/fixture acceptance boundaries

Governing D4/D5/D6 уже задали нужные schemas/state/closure. Один finite
source-only corrective pass в тех же4files; pure/helper/current230/owning
gitlink/public inputs/source16 paths/scientific code/server/CP не менять.
Рекомендуемые последовательно завершённые boundaries:

1. **Truthful terminal evidence:** P1-A и normative scalar/schema validators;
   measured/retention complete выводятся из actual source/raw/index ledger,
   rejected ACK ничего не удостоверяет своим наличием. Actual producer/job
   proof проверяется existing trusted lease adapter, не новым trust registry.
2. **Total owner cleanup/publication:** P1-B/C с first-FD ownership, full inherited
   FD rule, safe error-preserving drain/escalation/partial-index/fallback и
   durable publish. Positive phase/setup недостижимы при unknown ownership,
   drain, receipt publication или retention.
3. **Exact schedule/ledger:** P1-D/E, unique family bounds, native ordinal graph
   slots, every failed-call debit и all writes/transport/fallback/domain handoffs.
   До dispatch привести одну replayable analytic schedule+cost table для
  100/444 routes с metadata≤2MiB, Git≤512/8MiB/60s per phase и global storage/
   deadline. Actual source freeze отдельный prerequisite, не повод пропустить code.
4. **Full manufactured route:** Python fake existing lease+clock+handles+
   fakeproc/pidfd/cgroup вызывает actual factory/broker/driver/executor/finalizer
   через injected adapters, healthy preflight→check и direct docs доходят до
   fake execute и final setup complete. Paired P1-A–E failures запрещают pass/
   next phase и сохраняют evidence. Deno fixture упражняет actual runDriver
   healthy+failed capture/terminal source throw/full maximum chunks/finish.
   Никакого real Git/version probe/process/cgroup mutation при будущих DEV calls.

Output: immutable report/identity/complete patch с actual hashes и table
«закрытый поддефект→owning guard→paired fixture→remaining runtime gate», затем
STOP для независимого CPP. Отсутствие implementation seam для injected test
не заменять неисполняемым giant mock: узко refactor-owning adapters в native16
files без роста production import closure. Новый broad D-only этап не требуется.

Дальше отдельно Root finite compiler/DEV plans; данный review их не запускает.
Pure helper/fixture import closure прежняя: fixture→pure helper без native/git/
process/env calls; native driver CLI guarded by import.meta.main, native Python
main by __name__. Current230 nominal, observed неизвестен. Native gaps не
расходуют/не блокируют независимый уже source-reviewed pure later GREEN.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Queued phase, self-SHA, always-failed/cumulative/full-cap defects исправлены | Dispatcher/KaTeX/reservation/reset/positive predicate source locators | Не полная native acceptance | сохранить |
| Unknown source честно маркирован в final phase | Rejected validation_ref→measured в1550 | Ложный evidence status | изменить |
| Cleanup/retention покрывают каждый error | First-FD/range4096/finally/durability gaps | No execution, но source paths воспроизводимы | изменить |
| Budget proof полон и replayable | Conditional100/444/2026496 table; missing exact slots/failure ledger | Actual family freeze отсутствует отдельно | изменить |
|8+8 подтверждают full native READY | Isolated source controls; no full fake route | Observed=null | данных недостаточно |
| Pure230 изменён native continuation | SHA676a…/f02f… неизменны | Отдельный later finite plan | сохранить |

STOP. Original artifacts сохранены; target execution/source/CP/index edits=0.
