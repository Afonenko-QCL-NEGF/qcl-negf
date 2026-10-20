# DOC06 schema v2: независимый аудит фактического исхода

2026-10-20. Verdict: **SOFTWARE_EVIDENCE_ACCEPTED_WITH_LIMITS_RESOURCE_GATE_UNCLOSED**. Исправленный source и свидетельство успешного выполнения74 software assertions можно принять для узкого code review и честной draft-публикации. **Совокупного PASS нет:** sole DOC06-SCHEMA-E1 остаётся `outcome=failed`, `RSS_observation_unknown_NotCapable`. Resource acceptance, свежая actual projection/meaning acceptance, CI и scientific acceptance этим packet не установлены.

Аудит только читал сохранённые source/log/receipt bytes. Ничего не переигрывалось; guard/Root source/checkpoint/original artifacts не менялись. Attempt E1 потрачен; review не даёт retry, нового E1, CI, solver или других execution grants.

## Точное evidence

| Артефакт | SHA256 |
| --- | --- |
| FORMAT-1 receipt.json | aaaf0be83c834ba83736959d37025113dc067c306ed0dc9ed4b46736d3be3dcc |
| LINT-1 receipt.json | fcab1a950805ae753bf614c18df2c9a39cc9e1112dcc7d79ebfea64a11b8669a |
| E1 receipt.json | 98f6f3d7c6b89c45009a0db1e6066d5583b9758f57e3d41a9e1888347088b313 |
| E1 original.log | a9d789058b4e4bdb84eba977b1d3366f9eb714b96058426acc63e3feac98b9b6 |
| outcome-summary.json | bfd763c78c6dd09ea9b0be798f10f86e3e6b8210abd230132a61600539b301c7 |

Receipt/log paths: `/tmp/DOC06-SCHEMA-{FORMAT-1,LINT-1,E1}/`; summary `/tmp/qcl-doc06-schema-v2-outcome-summary.json`. Все hashes пересчитаны. Все3original logs имеют exact bytes/hash из receipt.raw_metadata и complete capture=true/no capture error. Summary по указанным records согласован с primary receipts; накопленные product_calls82/product_wall_seconds1028.532 не реконструировались по историческому ledger и не используются как отдельное доказательство всей истории.

Frozen execution HEAD по readiness/prelaunch/terminal observations всех3receipts: `b07974b8e46bf8afdf1740947b842669a62a5ccc`. Current owning files независимо перечитаны/хешированы: adapter `a852318af5105aaf224913e2264342c4349cb0ed70991842f00ab78e4d6c4b72`, tests `45febb3ccfdd9d641447d5cec6e26bbfc6c9b97f188c2e9a620142794c1a3b31`; совпадают с LINT/E1 before+after и terminal bindings.

Source CPP SHA `2706d0bb54a9e9027ae9cc633bc42fded380501a3ca45bd48400915e35c89be7` и format-only binding SHA `0130a35e4445fbc73feda5d5ad7e0df20b032b59cc3490abef7409535ce162e3` проверены заново. Accepted candidate→formatter-equivalent final source chain сохранён. Guard source `/tmp/qcl-doc06-schema-local-unit-run-v2.py` SHA `45e2848cc3cf193c3b9533dcdb518b5daf307da1fbb99546ab619343b1278bef` совпал с E1 receipt и source review.

## Наблюдение: source tools прошли свой guard

FORMAT-1: guarded_pass, exit0,0.719s,2valid/0failed RSS samples, raw189B. Output hash adapter/tests соответствует format-only review; форматирование меняло только разрешённые2paths.

LINT-1: guarded_pass, exit0,0.722s,2valid/0failed RSS samples, raw16B `Checked 2 files`; input=output final hashes. Никакой full CI или всего repository lint из этих двух commands не следует. Их resource metrics остаются sampled lower bounds, а не hard transient peak certificates.

## Наблюдение:74 assertions прошли, E1 guard отказал

E1 receipt: child exit0; raw5247B, complete capture=true, raw_metadata.measured и expected_test_summary_observed=true. Полный original log содержит ровно74различных индивидуальных `DOC06 … ... ok (…)` строк и итог `ok | 74 passed | 0 failed (529ms)`. Подсчёт выполнен постобработкой existing log без исполнения tests. Первые56строк соответствуют baseline; последние18 — новым M1/M2/M3 regressions. Это положительное свидетельство выполнения assertions именно на final source hashes, а не вывод по одному exit code.

Одновременно receipt.outcome=`failed`, stop_reason=`RSS_observation_unknown_NotCapable`, wall2.745s;29completed RSS samples,1failed loop sample. Ошибка локализована в guard `rss_tree` при отсутствии VmRSS у выбранного PID2926112 (`:301`), вызывается из `observe_rss():310`; source`:315–318` сохраняет ошибку/reason, terminal gate`:434–435` не снимает её. Семантический test result не отменяет этот отдельный gate.

Valid sampled peak326107136B меньше лимита1073741824B; sampled TMP peak814786B меньше8MiB; raw5247B меньше1MiB. Эти наблюдения не заполняют отсутствующий RSS sample. Ошибка не доказывает превышение памяти и не доказывает соблюдение ресурсного контракта на неизвестном наблюдении.

Исторические `/proc/<pid>/status` State, полный status snapshot и timestamp отдельной ошибки не сохранены. Поэтому причина отсутствия VmRSS **не установлена**. PID нельзя ретроспективно объявить zombie/завершившимся, а ошибку нельзя понизить до harmless race. Current state PID не воспроизвёл бы историческое наблюдение. Никаких таких probes или replays не выполнялось. Existing guard и failed receipt должны сохраниться без переклассификации.

## Что покрывает software evidence

Baseline56 сохраняет положительную проекцию и10fact classes, missing/hash/allowlist/owner/symlink/fresh-output controls, bounded JSON/ref/lexical caps, YAML/Julia dynamic-unknown, inert sentinels и source provenance controls. Exact baseline test prefix был сохранён в CPP/format-only review; raw log теперь подтверждает выполнение этих56assertion cases.

Новые18 source registrations повторно сверены в final `tests/docs_static_slice_test.ts` по `assertSchemaUnknown`, `rootConditional` и M1/M2/M3 block:

| Cases | Count | Отличающее software evidence |
| --- | --- | --- |
| Unrelated root conditional positive | 1 | Direct declarations/default-absence,2constraint locators, partial coverage/footprint, modes/status и10classes/null identities, determinism |
| Selected production в if/then | 2 | Обе стороны fail closed; independent root required остаётся literal |
| Unknown item keys | 2 | else и escaped extra key не игнорируются |
| Root-wide clause keys | 5 | required/additionalProperties/not/ref/escaped key отказывают с locator |
| Root anyOf | 1 | Selected context unknown; direct required independent |
| Selected production/leaf combinator | 2 | Failure locator/reason-aware unknown, без fabricated description/effects |
| Escaped required pointer | 1 | Leaf и required source pointers сохраняют escape |
| Direct root membership false | 1 | false остаётся literal при отдельном unsupported context |
| Description absent/source missing | 2 | Reasons, units text, effects/formula-origin modes/status различаются |
| No composition | 1 | Полная instance validation по-прежнему не заявляется |

Positive cases требуют known facts и не проходят при тотальном unknown; negative cases требуют partial projection и независимые surviving facts, а не общего refusal. Поэтому результат поддерживает исправление M1/M2/M3 на этих fixtures. Он не доказывает arbitrary-schema correctness, full JSON Schema validation, полноту всех malformed shapes или смысл fresh actual output на canonical nine-source snapshot. Fixture software evidence и actual/source/physics acceptance остаются разными.

## Решение о публикации и открытом gate

Узкий исправленный code diff годится для draft-публикации с приложенными CPP, format-only review, exact final hashes, raw74-assertion log и явным E1 guard failure. Оснований блокировать само представление source на review из-за недоказанного RSS sample нет: это не выявленный отказ assertions/модели. Но draft не должен иметь текст «все проверки прошли», «E1 guarded GREEN», «ресурсный бюджет подтверждён» или «DOC06 полностью принят». Merge/deploy/release/CI/scientific acceptance этот review не разрешает.

Корректная validation запись для draft: «Targeted formatter и linter: guarded_pass. Единственный Deno E1:74passed/0failed, child exit0; общий guard outcome failed из-за1неизмеренного VmRSS sample,29успешных наблюдений. Повтор не запускался; ресурсный gate и fresh actual meaning acceptance не закрыты».

Resource gate остаётся **незакрытым**; это не право запускать следующий этап. Разрешение причины потребовало бы отдельно принятой политики/телеметрии исторического состояния и нового конечного поручения, если оно вообще нужно. В текущем scope guard unchanged, никаких новых calls; прежние actual A1/A2 не переименовываются в success исправленного source. Заявленные source-tool/sole-unit caps и finite counters не сбрасываются.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Reviewed M1/M2/M3 source пригоден для draft review | CPP2706… + format equivalence0130… + final hashes | Не merge/deploy/actual/science gate | сохранить |
| Targeted format/lint прошли | Exact receipts: guarded_pass; raw hashes/capture valid | Ровно2paths, не repository CI | сохранить |
|74software assertions выполнены успешно | Exact E1 raw74distinct OK + summary74/0 + exit0 + bindings | Ограниченное fixture coverage | сохранить |
| E1 resource guard принят | Receipt.failed, RSS unknown29+1, no historical State | Причина и неизвестный interval не восстановимы из данных | данных недостаточно |
| Нужно изменить guard/повторить E1 сейчас | Такого execution scope нет; sole attempt consumed | Приёмка не достигается ослаблением после результата | сохранить |
| Fresh actual meaning/CI/scientific acceptance достигнуты | В packet отсутствуют | Source/tests не заменяют эти gates | данных недостаточно |

Audit limits: conservative logical reads≤1MiB при cap4MiB, wall<600s, report+identity<128KiB;1CPU/1GiB request. Physical CPU/RSS/I/O review не измерялись. Записаны только отдельные outcome review/identity; executions0, replay0, guard modifications0, Root/CP writes0.
