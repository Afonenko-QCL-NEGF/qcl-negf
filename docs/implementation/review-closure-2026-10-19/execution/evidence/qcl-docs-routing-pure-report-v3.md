# Pure routing v3: source-only guard/plan

Подготовлены новый guard и plan для единственного `DOCS-ROUTING-GREEN-1`;
исполнений нет. STOP до отдельного независимого high review и свежего Root
READY. Native I2B остаётся partial/changes-required; эта работа его не завершает.

Исходный cwd `e48e5b2…` с пользовательскими изменениями сохранён. Coordinator
Root отдельно: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`,
наблюдавшийся HEAD `c5ef91f4d11a93bd2cdcc9d0b6b18bba0df80ed0`; там уже есть
изменения CP/evidence другого агента. Product isolated base отдельно:
`/tmp/qcl-docs-test-routing-worktree`, HEAD
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`, dirty I2B overlay и восемь
uninitialized gitlinks. Никакие исходники, CP, indexes, gitlinks не менялись.
Будущий Root HEAD после batch публикации может отличаться от c5ef и обязан
быть заново проверен Root; guard связывает его fresh handoff, не запускает Git.

Состав pure runtime: fixture импортирует только `../ops/docs_tests.ts`; helper
не имеет imports и не использует Deno API. `ops/process.ts`, `environment.ts`,
`git.ts`, CLI/native и native16 не входят в эту closure. Наличие top-level
`Deno.env.get("JULIA")` в environment.ts поэтому не требует `--allow-env`.
Synthetic metadata и fake executor не читают TMP/cache и не запускают real
children. D2 seed неприменим: остаются private empty DENO_DIR/HOME/TMPDIR,
нулевые grants. Любое изменение import closure блокирует текущий plan.
Номинально230 =227 ancestral +3 sourceGraph-failure controls; observed=null.

Исторический RED проверяется отдельно от текущего GREEN. Фиксируются exact v2
H/P, сохранённый historical fixture, receipt2724B, full raw765B, erratum и high
review. Raw обязан совпасть по SHA и полному layout после только ANSI CSI
stripping: TS2307 и зависимый TS7006 с точными URI/координатами/info/hint/LF.
Исходная классификация inconclusive сохраняется. Ни ACCEPTED_RED, ни227
выполненных tests не выдумываются. Новый predecessor record создаётся Root
только после проверки; эта подготовка его не создаёт. Все predecessor checks
предшествуют guard helper imports и permanent GREEN reservation.

Current v3 H/P и final formatted two-file hashes связываются отдельным READY.
Старые v2 H/P никогда не сравниваются с v3 self/plan SHA. Baseline676a…/f02f…
сохранён отдельно. План содержит три будущих отдельных source calls: fmt,
lint, check только двух pure файлов, каждый120s/1CPU/1GiB/32MiB TMP/2MiB raw.
Это не их запуск и не реализация отдельного source tool supervisor. После них
нужны format-only review с baseline→final hashes и тремя receipts, CPP exact
final source и отдельный high guard review. Root обязан проверить смысл этих
review/receipts; произвольный same-user JSON и один SHA authority не создают.

Guard копирует проверенный паттерн SCI08v3: helper SHA проверяет тот же buffer,
который compile/exec будет использовать, без SourceFileLoader/pyc; target при
этом никогда не импортируется Python. Permanent directory exclusive, initial
consumed receipt,120s terminal alarm,108s ранний stop и независимые terminal
steps сохраняют failed receipts. Full RawCapture сохраняет original output;
fallback при отсутствии collector сохраняет bounded prefix и требует EOF для
complete. RSS=null при неизвестном VmRSS/процессе; attempted/valid/unknown
counts отдельны, минимум один valid обязателен. TMP all-entry lstat census и
reviewed regular-payload sampler учитываются отдельно. Нулём отсутствие
измерения не заменяется. Source/H/P/helper/READY/review/predecessor перечитываются
terminally; executable SHA проверяется предварительно, terminal runtime
measurement не заявляется. Sampled limits допускают overshoot и не доказывают
hard filesystem/RAM isolation, production supervision или native admission.

Остался один global engineering call87→88, без alias/retry/RED/C08/CI/science.
Guard verdict при хорошем capture только `CAPTURED_REQUIRES_INDEPENDENT_TAP230_REVIEW`:
independent result review проверяет полные230 names/plan/counters/all-pass и
zero skip/ignore/todo/fail/cancel/only; exit0 сам по себе не даёт pass.

Проверка подготовки: только source reads, read-only Git, textual patch и
SHA/size readback собственных файлов. Guard/plan/target не загружались parser,
не compile/exec/import; Python product/Deno/Julia/tests/formatter/lint/native/
network=0. Начальный metadata discovery был слишком широк и дал усечённый
вывод; значимые named источники затем читались отдельно. Не заявлена полнота
показанных усечённых batch outputs. Conservative logical read reserve4MiB;
CPU/RSS/physical IO не инструментированы. Данные source review не являются
runtime тестом failure handling или гарантий завершения.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Pure230 можно отделить от unfinished native I2B | Two-file closure676a…/f02f…; I2B identity/report | Нужен CPP final formatted source | сохранить |
| Genuine RED ancestry не переписана | Fixed v2/fixture/receipt/raw/erratum/high-review SHAs, full-layout predicate | Original classification inconclusive; assertions не выполнены | сохранить |
| v3 не требует старый H==новый H | Separate ANCESTORS и current READY H/P | Source-only; verifier ещё не исполнялся | изменить |
| Source tools и GREEN готовы к запуску | READY/accepted CPP/format receipts ещё отсутствуют | Требуются независимые gates и отдельный Root handoff | данных недостаточно |
| Pure GREEN доказывает native/full CI/science | Такой evidence отсутствует | Scope только fake pure routing | данных недостаточно |

STOP: отдельный high source review, затем Root решает следующие разрешённые
source tools/late bindings. Эта подготовка не расходует engineering calls.
