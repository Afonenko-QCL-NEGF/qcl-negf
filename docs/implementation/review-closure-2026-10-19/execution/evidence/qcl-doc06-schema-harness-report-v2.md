# DOC06 schema harness v2: source correction R1/R2/R3

2026-10-20. **SOURCE_ONLY_STOP_FOR_SAME_HIGH_REVIEWER**. Созданы отдельные v2 scripts/plan/report/identity; v1 и original helpers сохранены. Никакого import/compile/parser/harness/selftest/tools/product/Git выполнения. Root source AA476/ec4 и CP не менялись.

Previous source review SHA `787e5728d3541584ca91b84be1b76e181863cd83e12233b399e209110d9a3fa3` принят как три обязательные source corrections. Accepted source CPP SHA `2706d0bb54a9e9027ae9cc633bc42fded380501a3ca45bd48400915e35c89be7` и candidate source bindings сохранены.

| Artifact | Bytes | SHA256 |
| --- | --- | --- |
| `/tmp/qcl-doc06-schema-format-run-v2.py` | 24613 | `2daef993d218ac2d4e1cabfc44018725c19a55d60187d43d3d954cef33664aa4` |
| `/tmp/qcl-doc06-schema-lint-run-v2.py` | 24608 | `19ed0f182a51fd5022b0c1068367f92b8019beb74d0e304ee94a744da697a8ee` |
| `/tmp/qcl-doc06-schema-local-unit-run-v2.py` | 31965 | `45e2848cc3cf193c3b9533dcdb518b5daf307da1fbb99546ab619343b1278bef` |
| `/tmp/qcl-doc06-schema-engineering-plan-v2.json` | 4632 | `2206d06e2c072b5132db0a2a89048a7df5ef2602961bd03c19ef916cad5c824c` |

## R1: actual current HEAD

Plan теперь отдельно хранит `author_cpp_base_head=2bb05d3651af4509fe7f02c1253b40f1e5146fec`; это frozen author input, не текущий Root. Fresh READY.head принимает40hex. `actual_head()` выполняет только `/usr/bin/git -C <fixed Root> rev-parse HEAD`, clean env PATH + GIT_OPTIONAL_LOCKS=0, timeout3s. Readiness/prelaunch/terminal observations должны совпасть с fresh READY.head и записываются в receipt. Поэтому Root может указать фактический b079… или более свежий current HEAD после собственного readback; старый HEAD не hardcoded. В этом source этапе Git не запускался; actual Root HEAD здесь не утверждается по новой проверке.

До/после child source/runtime/helper/config/harness/READY/plan bindings сохранены. При невозможном terminal readback gate fails, missing head не заменяется старым known head.

## R2: measured RSS против unknown

`peak=None` до первого полного наблюдения. `rss_tree` требует PPid snapshot и VmRSS выбранных PID; missing/unreadable/malformed fields не становятся0. ENOENT racing unrelated proc допускается; исчезнувший selected PID делает snapshot unknown. Другие snapshot errors сохраняются и дают fail closed. Сразу после Popen до первого poll/capture выполняется postspawn observation; loop observations также учитываются. Возможное live terminal observation участвует в том же RSS cap. Для уже завершившегося процесса terminal sample не выдумывается.

Receipt содержит rss_samples_completed/rss_samples_failed/rss_sample_phases/rss_errors/rss_status. Guarded pass требует completed≥1 и failed=0. Fast-exit без валидного VmRSS получает nullable peak + unknown_NotCapable и failure; retry не разрешается. Каждый измеренный cap breach участвует в stop; наличие раннего measured sample не отменяет позднюю snapshot error. RSS остаётся sampled lower bound, без hard peak/cgroup guarantee. TMP peak тоже nullable до успешной sample.

## R3: failed receipt после reservation

Сразу после exclusive permanent folder mkdir весь остальной code охвачен outer try/except: temporary mkdir, readiness, seed, logOpen, Popen, capture construction/finish, raw summary/hash/readback, terminal source/hash checks, receipt write и console output. Ошибка существующего inner finally тоже попадает во внешний failure path. Он best-effort останавливает child, пытается drain, сохраняет rescue errors и создаёт failed metadata с unknown/null для неустановленного raw capture, hashes, summary, counters и measurements. Source/post hashes не подменяются input hashes. No-child raw capture больше не объявляется complete/0 при отсутствующем log.

Пробуются receipt.json и failed-receipt.json. Если I/O не позволяет ни одну запись, stderr fallback явно содержит consumed stage/folder и Root reconciliation requirement. Это **best effort**, не невозможная гарантия сохранности при отказе всех каналов. Permanent identity не удаляется, не repair/reuse; Root обязан сверить внешнюю ошибку, а не повторить call.

Raw metadata: до cap читается streaming64KiB с SHA и summary overlap128B, tail≤4096B; wall guard в readback. Большой original overrun не загружается целиком и не суммируется: metadata status overrun_retained_not_summarized, SHA/summary unknown. Raw оригинал сохраняется без truncation. Summary доступен только при complete capture и успешном bounded readback; иначе unit fails, не PASS. Receipt outcome `guarded_pass` возможен только со всеми guard/capture conditions, а не просто exit0. Finalization failure имеет outer failed outcome.

## Сохранённый finite scope

Идентичные stage ids DOC06-SCHEMA-FORMAT-1 / LINT-1 / E1, по1call; v2 не добавляет calls или retry identity. FORMAT/LINT20s1CPU1GiB32MiBTMP2MiBraw; E1 120s1CPU1GiB8MiBTMP1MiBraw и expected74. Milestone81→87 ceiling, old format3/3 lint3/3 unit2/2 E1 1/1 actual2/2 сохранены. Actual2 future остаются вне packet. CI/science/C08 не открыты.

Все вызовы теперь через `-run-v2.py`; READY fixed `...-format-ready-v2.json`, `...-lint-ready-v2.json`, `...-e1-ready-v2.json`, plan `...-engineering-plan-v2.json`. JSON READY schema string остаётся `qcl-negf.doc06-schema-ready.v1`, остальные поля как v1 contract, но head late-bound и plan/harness SHA должны быть v2. Freshness≤300s. LINT/E1 по-прежнему требуют format receipt и accepted format-only review binding финальных SHA; source CPP bindings точные.

Pinned Deno2.8.3/runtime SHA/config width100 неизменны. Fixed clean child env/no caller inheritance; helper exact-buffer SHA→fresh ModuleType compile/exec без pyc loader; exact2source+ownedTMP read и TMP-only write, no env/run/net/ffi. Эти compile/exec statements только source, здесь не исполнялись.

Seed13nodes и preparation сравнивались как текст с original unit-v2 после удаления единственного outer indentation; equality подтверждена. Изменений seed logic/link targets/backing guards не внесено. Before_seed/prelaunch/loop/terminal TMP thresholds сохранены. RawCapture/drain/fallback original retained. Permissions/finite source paths не расширены новым readonly Git metadata command родительского guard.

## Проверки и границы

Только source reads, textual transformations/comparison, hashes и собственные new `/tmp` artifacts. Нет ast.parse/py_compile/import/compile/harness/selftest/Deno/formatter/linter/test/actual/Git execution. Логический read conservative≤1MiB при cap2MiB; wall<10min;1CPU/1GiB; report<128KiB. CPU/RSS/physical I/O этого I не измерялись. Никакой runtime correctness/acceptance не заявляется.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| R1 hardcoded stale HEAD убран | Late-bound READY40hex + actual Git readback readiness/prelaunch/terminal | Source only; будущий Root READY обязателен | изменить |
| R2 unknown RSS больше не0/pass | Nullable peak, counts/errors/status, immediate sample, any error fails | Нет runtime/fault injection | изменить |
| R3 failure metadata имеет внешний recovery path | Outer envelope, best-effort two receipts+stderr fallback, nullable unknowns | Физический отказ всех I/O нельзя устранить гарантией | изменить |
| Seed/capability/counters сохранены | Exact text comparison + new distinct v2 packet | Tests/tools не запускались | сохранить |
| Engineering/source-tools/unit прошли | Executions0 | Нужен same high source re-review и Root READY | данных недостаточно |

STOP для same high source re-review.
