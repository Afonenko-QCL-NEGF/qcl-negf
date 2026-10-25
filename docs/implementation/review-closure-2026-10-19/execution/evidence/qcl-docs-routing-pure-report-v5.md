# Pure routing v5 — узкие R1b/R2 source corrections

Подготовлен отдельный v5 пакет: unit guard/plan и FORMAT1/LINT1/CHECK1 entry
guards. Никаких scripts/parser/compiler/runtime/tests/network запусков нет;
product/Root CP/fixtures не менялись. STOP до свежего независимого high review.
Все v3/v4 artifacts сохранены. Основание — high v4 review
`/tmp/qcl-docs-routing-pure-harness-v4-review.md`, SHA
`206731b357638ae735a0b33019108725f4cbe8d329b2009c2f35dce6633791bb`.

R1b исправлен одинаково в unit и common source lifecycle. Boolean
collector_construction_attempted устанавливается **до** RawCapture constructor
call. Если constructor не вернул capture, ownership неизвестен, поскольку
thread.start мог запустить native thread до исключения. После отдельного
bounded stop_owned сохраняется failed consumed receipt: complete=false,
collector_terminal=null, raw SHA/count=null и только best-effort фактически
прочитанный prefix size (nullable). Fallback не читает тот же pipe и не
закрывает stream при неизвестном competing reader. Затем os._exit(2), alarm
остаётся активным. Terminal-alarm receipt также записывает attempted/ownership.
Если capture был присвоен, v4 finish/is_alive/failed-receipt/force-exit safety
сохранена. capture=None больше не трактуется как terminal после attempted
construction; shared helper bytes/hash не менялись. Original raw не обрезается
и не выдаётся за complete. Runtime fault injection не выполнялась.

R2 исправлен как acceptance predicate, а не переименование gaps. Перед каждым
RSS attempt вызывается Popen.poll(). Только уже полученный terminal returncode
разрешает **не предпринимать** RSS attempt: отдельные N/A-after-reap count и
proof содержат PID, returncode и elapsed time. RSS не измерялся в этом событии,
peak не становится0 и valid count не увеличивается. Для live/unreconciled child
rss_tree(None/malformed/read failure) увеличивает attempted/unknown и сразу
устанавливает failure reason. Если child исчез во время attempted RSS, это
остаётся unknown и не отменяется последующим reap. Final good явно требует
unknown=0 и по-прежнему valid≥1. Final observe после доказанного wait/reap
пишет N/A proof, не искусственный unknown и не retrospective waiver.

Source predecessor gate требует unknown=0, attempted=valid+unknown, valid≥1,
exact N/A count/proof shape/PID/exit-code/time и прежние complete capture/
collector/argv/env/limits/raw/source predicates. Теперь unit тоже пропускает
все3source receipt_refs через этот прямой gate, в порядке FORMAT1/LINT1/CHECK1.
Форматирование остаётся под Root: эта работа не меняет owning files и не
выдумывает final SHA или format-only approval. Whole I2B CPP4903… по-прежнему
CHANGES_REQUIRED, positive slice явно pure_only; final formatted closure CPP
и substantive Root acceptance остаются отдельными обязательствами.

Сохранено без расширения: unconsumed DOCS-ROUTING-GREEN-1 с230 static
registrations/observed=null/global87→88; source FORMAT1/LINT1/CHECK1 с2→3→4→5
при ceiling8; runtime Deno2.8.3 cdd88…; config a637…/width100; only pure
fixture→helper closure; пустые script grants/private empty env roots/no seed;
120s/1CPU/1GiB sampled RSS/2MiB raw, unit16MiB/source32MiB sampled TMP;
108s early stop+120s terminal watchdog. No aliases, retry, RED, native16,
C08/full-CI/science. Exact-buffer wrappers и helper loading без pyc сохранены.

Исторический RED не переоценивался: fixed v2 H/P/04589 fixture/receipt2724B/
raw765B/erratum/high-review, exact normalized TS2307+TS7006 layout и original
inconclusive classification неизменны. Fixed historical identities отдельно
от v5 current H/P/final source. DOC06 E1 unknownFAILED также не переименован.
Versioned predecessor-v5 record/READY не созданы. Isolated base2bb05… отдельно
от global Root late READY, source authority только trusted Root SourceRef;
CP file/status не превращается в admission authority.

Проверка автора: reads high review/current source, inert copies и patches,
textual named-section readback, SHA/size checks. Prepared code/parser/compile/
import/formatter/lint/check/tests/Deno/Julia/native/network0. Фактическая
runtime correctness и fault handling этим source pass не доказаны. Conservative
logical read reserve<4MiB, grant12min/1CPU/1GiB/128KiB output; physical CPU/RSS/
IO не инструментированы. Первичный combined output был truncated; необходимые
изменённые sections перечитаны отдельно, полнота скрытого остатка не заявлена.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Constructor unknown не теряет finite terminal path | attempted-before-call; failed incomplete receipt и force exit без competing fallback | Source-only, fault injection0 | изменить |
| Live RSS unknown блокирует результат и следующий stage | immediate reason + final unknown=0 + direct predecessor predicates | Sampled caps не hard peak/quota proof | изменить |
| N/A относится только к pre-proven terminal | poll proof до attempted RSS, отдельные counters/PID/returncode/time | Нет retrospective отмены live unknown | сохранить |
| Scope, ids,230 и historical RED сохранены | V3/v4 immutable package; v5 plan frozen/current separation | Observed=null, calls0 | сохранить |
| V5 admitted/принят runtime | READY/actual receipts отсутствуют | Требуется fresh independent high review и Root admission | данных недостаточно |

STOP перед fresh high review. Никакого исполнения или automatic continuation.
