# Pure routing v4 — terminal correction и source supervisors

Подготовлены guard/plan v4 и три отдельных source entry guards. Исполнений0;
STOP до независимого high source review, затем отдельного Root source admission.
Ни один FORMAT1/LINT1/CHECK1/GREEN call не сделан; predecessor/READY отсутствуют.
V3 package и все historical RED artifacts сохранены без изменения.

Основание R1: high review
`/tmp/qcl-docs-routing-pure-harness-v3-review.md`, SHA
`85a8f8930b94824b07e9d46dc66240fc30e98a0e8499fac45cf95a9f928319ec`.
Pinned RawCapture.finish(timeout) может вернуть false с живым non-daemon
thread. V4 после отдельных bounded cleanup/capture/source steps сохраняет
failed consumed receipt, проверяет thread.is_alive и при живом collector
повторно пишет incomplete/collector_not_terminal, затем os._exit(2). Deadline
не отменяется на этом пути. Если receipt write не подтверждён — force exit,
Root обязан reconcile. ITIMER_REAL отменяется только после доказанного
collector terminal. Та же ветка у unit и каждого source stage. Collector не
daemonized; original log не редактируется, missing EOF не считается complete.
Full RawCapture overrun остаётся failure с original bytes; fallback сохраняет
bounded prefix и явно не обещает complete без EOF.120s terminal watchdog и108s
ранний stop сохраняют резерв на bounded terminal steps. Runtime fault injection
не выполнялась; source proof не является измерением termination.

Каждый source wrapper проверяет canonical owned regular shared guard и SHA того
же buffer, который будет compile/exec в fresh non-main ModuleType без pyc/
SourceFileLoader. Entry фиксирует только FORMAT1, LINT1 либо CHECK1; аргументы
не выбирают другой stage. Общий guard затем проверяет wrapper/current guard/
plan hashes из свежего READY. Target Python/TypeScript при этом не импортируется.

Фиксированные stage identities:

| Stage | Attempt | Shared source calls |
| --- | --- | --- |
| FORMAT1 | DOCS-ROUTING-SOURCE-FORMAT-1 |2→3|
| LINT1 | DOCS-ROUTING-SOURCE-LINT-1 |3→4|
| CHECK1 | DOCS-ROUTING-SOURCE-CHECK-1 |4→5|

Source ceiling8 не сбрасывается. Каждый stage требует собственный Root READY,
создаёт exclusive retained folder, initial consumed receipt и делает ровно
один child call. Нет autorun следующего stage, aliases, retries или fallback.
Все stages:≤120s/1CPU/RLIMIT_CPU120s/1GiB sampled RSS/32MiB sampled TMP/2MiB
полного raw envelope. Stage guard не присваивает source acceptance по exit0:
лучший verdict `CAPTURED_REQUIRES_INDEPENDENT_SOURCE_REVIEW`.

FORMAT1 argv использует `fmt --config` exact isolated deno.json, width100;
config SHA `a637ff88ad0e1011480402de58895cb6d178eb1bbe98bdb27ca939b8821f6bce`.
Baseline helper676a…/fixturef02f… обязателен до format. После captured fmt
нужен независимый format-only baseline→final review. LINT1 и CHECK1 требуют
его refs и финальные hashes; LINT1 также проверяет fmt receipt/raw, CHECK1 —
fmt+lint. Предшествующие receipts проверяются прямо: stage/argv/cwd/exact env/
limits/exit/capture/collector terminal/nullable RSS observations/final source,
raw SHA/size. Config и selected source/executable/ref bindings перепроверяются
terminally; lint/check не могут менять source. Форматирование не даёт CPP или
PASS unit, final hashes пока неизвестны и не придуманы.

CHECK1 вызывает только `deno check` двух pure TS файлов с exact config/offline
flags; компилятор не выполняет модули и не регистрирует tests. В source receipts
test_registration_performed=false, observed_engine_tests=null. Возможное
typecheck или option failure расходует CHECK1 и блокирует продвижение; менять
flags/annotations или повторять автоматически нельзя. Existing local packets
подтверждают fmt/lint --config, offline flags test Deno2.8.3 и обычный check
ops/*.ts. Полная комбинация compiler-only flags новым help/runtime probe не
проверялась; это явный предел source evidence, не утверждение observed support.

Окружение каждого child полностью заменяется тремя private HOME/DENO_DIR/TMPDIR
под stage owned-tmp. Script grants пусты; target pure closure по-прежнему только
fixture→helper, fake executor, без process/environment/git/native16 imports,
seed/cache copy не нужен. RSS nullable, valid≥1 обязателен; attempted/valid/
unknown counts и sampled_with_gaps не превращают пробелы в0. TMP all-entry
lstat census и regular-payload sampler отдельны; initial/final обязательны.
Это sampled env-only guard, не hard RAM/disk/OS isolation/native admission.

CPP4903… (`qcl-docs-routing-impl-i2b-review.md`) целиком CHANGES_REQUIRED.
V4 source READY требует pure_only_slice=true и exact retained ref, а unit
accepted_cpp требует тот же explicit slice плюс отдельный review final
formatted closure. Whole I2B PASS нигде не заявляется. Fresh unit READY также
связывает все3source receipts, format-only review и current H/P/final hashes.
Static230 (227+3) high-confirmed, observed остаётся null до единственного
unit call и независимого полного TAP230 review.

SourceRef issuer — только trusted Root handoff. Source schema SOURCE_HANDOFF
проверяется на точное совпадение Root/global HEAD/isolated base/source/config/
shared source counters с READY. Unit имеет отдельную PURE_HANDOFF schema и
budget87→88. CP file/status не читается как authority marker. Root независимо
проверяет actual HEAD/status/gitlinks/counters непосредственно перед выдачей;
same-user JSON сам по себе не аутентифицирует Root и не доказывает approval.
Наблюдавшийся global Root HEAD
`107bac5697b37cf0e47c3feb44883a907837645c` отличается от fixed isolated base
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`; late READY обязан использовать
свежий global ref после публикации. Защищённый original cwd e48… не менялся.

Historical v2 H/P/04589 fixture/receipt2724B/raw765B/erratum/high-review pins
перенесены без изменения. Validator full raw normalized layout включает
TS2307 и зависимый TS7006, exact URI/координаты/info/hint/finalLF; original
inconclusive classification сохраняется. V4 current H/P/final source не
сравниваются с ancestral v2 H/P. Новый predecessor record path versioned v4,
не создан. Ни новый RED, ни retry, ни другой denominator не разрешён.

Проверка подготовки — только source reads, read-only Git rev-parse, inert
text copying/patching, SHA/size readback. Никакие scripts/guard/parser/compiler/
formatter/linter/tests/Deno/Julia/native/network не исполнялись; product/Root CP/
fixtures/git/index edits0. Авторский readback не заменяет независимый high review.
Grant15min/4MiB reads/1CPU/1GiB/256KiB output; conservative source read reserve
<4MiB, deliverables<128KiB. CPU/RSS/physical IO не инструментированы.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 deadline не снимается при живом collector | Unit/source thread terminal predicates перед alarm cancel, failed receipt+os._exit | Source-only, runtime fault не воспроизведён | изменить |
| Три source calls имеют bounded guards | Distinct wrappers/current guard, exact READY/argv/config/budget/capture | High review/admission/actual calls ещё отсутствуют | изменить |
| Pure scope отделён от incomplete native I2B | Explicit pure_only_slice + retained CPP4903…, two-file closure | Не whole CPP PASS/native readiness | сохранить |
| Historical RED и single230 GREEN budget сохранены | Fixed ancestor chain; unit87→88/ID неизменен | Observed=null; no execution | сохранить |
| Source stages/unit/native/CI/science приняты | Receipts/READY отсутствуют | Только подготовленные исходники | данных недостаточно |

STOP: отдельный high exact v4 review, затем Root source admission. Автоматическое
продолжение, запуск или повторная попытка этим пакетом не разрешаются.
