# SCI12Math local guard v2 — узкий независимый review B1

2026-10-20. **ACCEPTED_SOURCE_ONLY: B1 закрыт адресной правкой; блокеров в порученном delta scope нет.** Это follow-up frozen v1 review `f85ca6895125a4780ec6eb050a793691a4bb6f216ee1c0e5b7b16b5907944dec`, не новый полный аудит, не execution READY и не scientific/native acceptance.

Сначала прочитан supplied diff SHA `32cb2bcd43d245d53091dc1766964e9fe7fec3c5e3e8649d5b34dfa3b04db7e0`, затем независимо получены текстовые `diff -u` guard v1→v2 и plan v1→v2. Они содержат ровно перенос первого live `observe()` после successful `RawCapture` assignment и identity updates PLAN path/SCOPE v2. Plan меняет только scope. Все прочие строки guard/plan сохранены.

В guard-v2.py:309–313 порядок теперь `Popen` → `collector_attempted=True` → `capture=RawCapture(...)` → `observe()`. Поэтому sampler exception первого live observation входит в finally с уже assigned continuous reader; `finish(2)` :336–338 дренирует его после stop/reap. Прежняя B1 ветвь «child emitted bytes, observation raised, collector ещё не пытались создать, pipe не сохранён» этим переносом устранена на уровне исходника.

Флаг attempted по-прежнему устанавливается **перед** constructor. Если constructor поднимет исключение после native thread start, unchanged :326–334 сохраняет UNKNOWN ownership, incomplete consumed receipt и `os._exit(2)` без competing read/close. Assigned-live-thread guard :398–404 и watchdog остаются неизменными. Никакой fault injection, parse/compile или execution проверки это утверждение не подменяет.

Exact diff подтверждает сохранение caps wall90/early78/affinity1CPU/RLIMIT_CPU90/sampledRSS1GiB/TMP32MiB/raw2MiB, argv, clear environment/PYTHONPATH, frozen F2 и helper/runtime hashes, source closure, RED absence/GREEN exact future product hash, Root meaningful review/predecessor/counter/aggregate handoff и source bindings before/after. Aggregate180s/4MiB и concurrency1 остаются внешней обязанностью Root. Как и в v1, Contracts env binding не доказывает actual imported origin; sampled guards не являются hard quotas/peak proof; guard не выдаёт approvals и не измеряет science. Эти unchanged свойства здесь подтверждены через exact delta, без повторного аудита зависимостей.

| Вход | SHA256 |
| --- | --- |
| guard-v2.py, 21274B | `d5b46ac8eaf1a9b9456b47d90bf5e04ec42ff6859363cf53847c6c1884ef858a` |
| plan-v2.json, 2837B | `968c537b5b3bacf23f288d28254b50670930d27d8ae7e7afeceaba7ba463bf77` |
| report-v2.md, 4760B | `7db537449fa2fbfbda448caad1551be2a6ed3dd7a0a282dcda7efdb574aa5161` |
| identity-v2.json, 2299B | `5db2d50ec51e17c81a8849cbb4974e35f61c3d5de3d8f653c013a61f62cd36c7` |
| v1-to-v2.diff, 2180B | `32cb2bcd43d245d53091dc1766964e9fe7fec3c5e3e8649d5b34dfa3b04db7e0` |

Четыре v1 author artifacts и frozen v1 review/identity SHA повторно совпали; история v1 не переписана. Product88/source8/C088of8 по поручению остаются прежними; Math RED88→89 и GREEN89→90 prospective. Этот reviewer не запускал Math и не резервировал calls; actual current Git/counter в этом узком пакете заново не проверялись. Их fresh проверка остаётся у Root перед конкретным READY, включая exact new guard/plan/source hashes и meaningful reviews.

Учёт узкого v2 review: только wc/SHA, bounded exact-file text reads, два diff и source walkthrough; два новых /tmp review outputs. Scripts/import/parser/compiler/tests/numeric/network/target0, product/source/index/CP/READY/counter writes0, children0. Суммарный логический content-read charge известных входов до создания outputs —161213B (повторные чтения учтены; wc metadata не считается содержимым). С финальной перепроверкой v2 hashes и checksum outputs консервативная верхняя граница этого отдельного пакета230000B<256KiB; output<32KiB. Это учёт файловых байтов, не измерение physical I/O/CPU/RSS; hard isolation не заявляется. Предыдущее отклонение v1 с broad site-packages rg и unknown read volume остаётся действительным; v2 не превращает его в resource PASS задним числом.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| B1 закрыт в source | Exact delta и v2:309–313,336–338 | Runtime fault injection0 | сохранить |
| UNKNOWN-owner/lifecycle контракт сохранён | Exact diff; v2:326–334,398–404 | Только адресный source follow-up | сохранить |
| Caps/env/argv/Root gates не расширены | Exact guard/plan diff | Не новая runtime или semantic CP проверка | сохранить |
| Math outcomes и научная приёмка установлены | Новых Math execution artifacts review не создавал | Execution0 | данных недостаточно |

STOP: B1 принят только на source уровне; Root единолично оформляет meaningful handoff/READY/counters. Автоматического запуска или rerun нет.
