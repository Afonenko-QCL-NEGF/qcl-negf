# Независимая source-only review v9

Вердикт: **PASS_SOURCE** для неизменяемого пакета ниже. Блокирующих source замечаний к переходу v8→v9 не обнаружено. Это не execution grant, не READY, не успешный CHECK4, не unit/scientific/native acceptance и не доказательство устранения причины CHECK3. Root должен отдельно записать конечное расширение source11→12 до любого исполнения.

Этап: чтение исходников и сохранённых метаданных. Рецензент не исполнял рассматриваемые scripts, parser/import/compiler, tests, Deno, solver или network; дочерних агентов нет. Созданы только этот отчёт и его identity в `/tmp`. Product, CP, READY и Git index не менялись.

## Точная identity

| Артефакт | SHA-256 |
| --- | --- |
| guard-v9.py | e02576c6b421b158a00a570ca729b076737d47c1e79111606d15fb60a2cba01e |
| plan-v9.json | e32f4b534b928cef44cc8e9f35f242e979752b12b70e9eea687c5cca3cc3b2af |
| check-v9.py | 1dd84dcdf977f458b960e6dd78dbb100e4d3c3c83a60e29430d630a455f91f1a |
| report-v9.md | 8a784485090caadb1486ae0b96632c04cf3c2cfc02c0d94dfcbdd1991b72dea7 |
| identity-v9.json | e6b1edbc38286abd1468fd269e0b526c3ba312e9ff0b529f8dd80e4a7873d09f |
| v8-to-v9.diff | d5365c2e1a1cef4db4b2aa3704a46beb6f3d57009c0db9a6077c44e2652e8c16 |

Все пути имеют префикс `/tmp/qcl-docs-routing-pure-`. SHA вычислены чтением файлов. Реальный `diff -u guard-v8.py guard-v9.py | cmp - v8-to-v9.diff` завершился 0 без вывода: сохранённый полный diff соответствует текущим исходникам. Исходный guard-v8 SHA5cecec92f20bed186ab51b08b4b98585dde5452af5e4eef31ad27adbf386763b и plan-v8 SHA813afe65ddf7245eaf2562472398baf8f541463bba0d7022256ebc75f4cdaaa5 также проверены.

## Выводы и воспроизводимые локаторы

1. `guard-v9.py:344–440` (`RSS_FAILURE_DIAGNOSTICS`, `rss_failure`, `rss_tree`): status и children читаются по одному разу через read_bytes/decode вместо read_text; дополнительных `/proc` probes нет. Сохраняются только доступные уже прочитанные префиксы и census. Birth identity явно null/not_read. Все старые failure возвраты остаются None; диагностическое событие не является RSS sample или доказательством известной причины.
2. `guard-v9.py:348–376,458–472`: максимум4 события; обычный compact event проверяется против16000B, oversized payload заменяется коротким маркером с ограниченными kernel PID/path полями. Capture failure и dropped отмечаются явно. Четыре события плюс state укладываются в64KiB; compact ASCII receipt ограничен262144B. Сериализация receipt отделена от child `original.log`; raw collector не изменён. Envelope/запись receipt при ошибке не дают успешного возврата.
3. `guard-v9.py:556–580,693–710,898–923,1038–1051`: live None немедленно увеличивает unknown и устанавливает failure; финальный unknown!=0 запрещает good, valid>=1 обязателен. Предварительно доказанный poll/reaped N/A сохраняется отдельно; новых N/A оснований нет. Startup без измеримого RSS сохраняет `RSS_not_measured`/exception/unknown и не получает pass. Диагностика rss_tree не обещает измерить ошибку до входа в sampler или birth identity: при таком сбое event может отсутствовать, а причина остаётся неизвестной. Изменения watchdog/R1b/collector lifecycle в полном diff отсутствуют.
4. `guard-v9.py:739–853` (`SOURCE_STAGES`, `source_receipt_ref`, `source_main`): исполняем только CHECK4, counter11→12 cap12. FORMAT3/LINT3 остаются точными retained v8 receipt/wrapper/H/P/env/raw/counter identities8→9 и9→10cap11. New CHECK4 требует собственные currentv9 H/P/wrapper, counter11→12 и фактический future receipt. Приравнивания oldH/P к newH/P нет. Source tools по-прежнему не регистрируют unit tests.
5. `guard-v9.py:279–308`: consumed CHECK3 receipt a399281f3159ffd88cc014a5fd8504110fb8c272e21472cab5404e3ff67eb05a сохраняется как FAILED с32valid1unknown, child0 и stop attempted_live_RSS_unknown. Этот receipt прочитан непосредственно: он не объясняет причину. Race/zombie не подтверждены. Good prerequisites теперь FORMAT3(v8),LINT3(v8),CHECK4(v9); failed CHECK3 не переиспользуется как successful check.
6. `guard-v9.py:285–318,480–511,806–853`, `plan-v9.json:5–16`: сохраняются unique E1 product90→91, expected232, fresh Root READY, отдельный SourceRef handoff, exact known format+pure review и formatted sources. Реально вычисленные helper12fbb1d8c754536135e7b919ca14a465532bd3910bdff7f68ef6fdb129376bab и fixturea629e366cdebacc9d6ffbef1458990cf00232d99ca3cb1668696c169fc4a1164 совпадают. SHA принятого CPP8ac8702532f17c9fc43149578cfa64bc477bd69679bf5b403d7174b1c615c3b3 проверен. Механизм same-user JSON не доказывает полномочия: содержательное принятие source outcome и проверка counters/admission остаются обязанностью Root.
7. `plan-v9.json:8–14`: только prospective append1call120s/1CPU/1GiBRSS/16MiBTMP/2MiBraw, aggregate5calls600s10MiB включая unused E1; consumed failures не сбрасываются. До Root extension source остаётся11/11EXHAUSTED. Sampled guards не доказывают hard quotas, peak RSS или native isolation.

## Checkout и границы проверки

В review checkout `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf` фактический HEAD107bac5697b37cf0e47c3feb44883a907837645c. Status: изменён execution/checkpoint.json; untracked i2b-review.md, i2b-review-identity.json, root-batch15-publication.json, root-progress-batch15-manifest.json. Все8 recursive submodule statuses прочитаны; ведущих `+`, `-`, `U` нет. Это наблюдение checkout, а не fresh admission будущего CHECK4.

Синтаксическая/runtime корректность, startup resource peak и способность будущего запуска дать различающее свидетельство не измерены. Прочитаны применимые AGENTS.md и architecture; using-superpowers явно исключает dispatched subagent. Проверка последовательная, без детей. Один агрегированный tool response сообщил truncation; полный diff после этого прочитан отдельно и сверён с реальными файлами. Соблюдение total tool-output ceiling64KiB не доказано и не заявляется; это ограничение процесса данного рецензента, не изменение проверяемого пакета. Лимит чтения2MiB не исчерпан по объёму выбранных файлов/повторных чтений; физические CPU/RSS/I/O не измерены.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Диагностика не ослабляет acceptance | полный exact diff; rss_tree/observe/final gates | source-only | сохранить |
| CHECK3 остаётся consumed failed | actual receipt a399281f и pinned history | причина UNKNOWN | сохранить |
| Один CHECK4 использует отдельную identity | source_main/source_receipt_ref/plan | Root extension ещё отсутствует | дополнительно измерить |
| Startup без RSS не даёт pass | valid>=1/final unknown/error gates | startup failure не измерен и может не дать RSS event | данных недостаточно |
| Mixed prerequisites сохраняют provenance | exact retained hashes и newCHECK4 map | future CHECK4 outcome неизвестен | сохранить |
| Причина CHECK3 устранена | свидетельства нет | diagnostics ещё не исполнялись | данных недостаточно |

STOP после source review. Пакет можно передать trusted Root для решения о единственном конечном диагностическом CHECK4; этот отчёт сам не расширяет бюджет и не разрешает исполнение.
