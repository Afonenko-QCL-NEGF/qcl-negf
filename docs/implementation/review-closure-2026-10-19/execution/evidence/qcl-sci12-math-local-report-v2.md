# SCI12-MATH local guard v2 — только B1 source correction

По frozen high review `/tmp/qcl-sci12-math-local-guard-v1-review.md` SHA `f85ca6895125a4780ec6eb050a793691a4bb6f216ee1c0e5b7b16b5907944dec` и identity SHA `20260a676ac16fa71a70ee0d8c25003ce86fcece6acdeceb2326b5457801da7f` исправлен только порядок установки reader. Это source candidate для свежего независимого high review, не execution READY.

Теперь после успешного `Popen` идут `collector_attempted=True`, успешное присваивание `capture=RawCapture(...)` и только затем первый live `observe()`. Потенциальный OSError sampler после запуска процесса попадает в cleanup с назначенным continuous reader, который дренирует pipe. Если constructor поднял исключение после старта native thread, прежняя UNKNOWN branch сохраняется: incomplete consumed receipt и force exit без competing read/close. Если assigned thread остаётся жив после finish timeout, прежний watchdog/forceexit также сохранён. Source reasoning не является runtime fault injection.

Единственные дополнительные изменения идентичности — `PLAN` указывает v2 path и `SCOPE` изменён на `SCI12-MATH-local-v2` одновременно в guard и plan. Полный `v1-to-v2.diff` содержит все изменения executable guard/plan. Локальный v2 scope не расширяет Root grant. Четыре v1 файла сохранены с прежними SHA. Report/identity v2 созданы как новые описания correction; прежний report/identity не переписывались.

Нет drift в argv, environment, frozen F2, helper/runtime hashes, source closure, модельных предпосылках, попытках, счетчиках или caps. Root finite plan `/tmp/qcl-sci12-math-engineering-plan-Root-v1.json` SHA `ad4ee176fac13463a701bf97d35275c4bcb3e9f7501a64a69ca64413bf482e62` остаётся внешней authority: только prospective RED88→89/GREEN89→90, ceiling90, concurrency1, wall90s/CPU1/RSS1GiB/TMP32MiB/raw2MiB каждый; aggregate180s/4MiB. Product88/source8/C088of8 не менялись. Historical81→88 и Routing failed/caps сохраняются. Новый product hash не придуман, module не создавался; никаких CP/READY/index/component files не записано.

Все ограничения v1 сохраняются: sampled RSS/TMP/raw stop не дают hard peak/OS quota, guard не устанавливает actual Contracts import ownership, source HEAD и meaningful review/predecessor/counter/aggregate проверяет Root перед fresh READY, numerical/native/scientific outcomes не измерены. Report v1 остаётся полным описанием остального контракта.

Проверка correction — точный текстовый diff и SHA256/size. Compiler/parser/import/scripts/tests/runtime/network0; детей0; продуктовых изменений0. Вся работа ограничена пятью новыми `/tmp` outputs. Source-content reads консервативно <256KiB из 1MiB, total output <64KiB, deliverables <40KiB. CPU/RSS/physical IO не измерялись; жёсткое resource enforcement не заявлено. Никакого execution authorization этот отчёт не выдаёт.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| B1 адресно исправлен на уровне source | v1→v2 diff: observe перенесён после assigned reader | Без runtime fault injection; нужен high review | дополнительно измерить |
| Остальной guard/plan сохранён | Полный diff: только порядок и v2 PLAN/scope identity | Авторская текстовая сверка | сохранить |
| V1 история сохранена | Четыре исходных SHA совпали после correction | Без перезаписи v1 | сохранить |
| RED/GREEN/scientific acceptance получены | Новых execution artifacts нет | Исполнение0, counter не менялся | данных недостаточно |

STOP: fresh independent high review до Root READY; автоматического запуска/rerun нет.
