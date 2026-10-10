# R09: conflict-first recovery declarations

Results добавляет preflight prior-final declarations в `verify_recovery_bundle`. Ordered union
охватывает index-only и owner-only paths. До payload SHA/native этой dependency группы отвергаются
contradictory size/SHA и optional semantic claims, противоречащие authoritative final owner.
Optional identity сравнивается рекурсивно с учётом JSON type: `true`/`1.0` не равны integer `1`.
Absent optional claim остаётся допустимым; index labels не создают нового owner. Public API/return,
current-bundle logic, Contracts/schema/Core не менялись.

Это normalization-only изменение. После preflight сохраняется исходный schedule: все index SHA,
затем все owner SHA, включая overlap, затем прежний native loop. Scope не переносится между
finals/calls; новый cache/verified token не введён. Второй SHA сохраняет позднее наблюдение external
mutable bytes. Stat/path/held fd не дают atomic byte snapshot: предложенное hash-elision не принято
без established immutable/captured-byte boundary. SHA-call saving, bytes/RSS/time/speedup не
измерены и не заявлены; performance часть R09 остаётся открытой.

Изменены только `state.py` и `tests/test_state_reader.py`. Runtime preflight: Python3.14.7,
numpy2.5.3, h5py3.16.0, cached locked pytest8.4.2; exact isolated Results/Contracts bindings.
Initial RED7failed/18passed → GREEN25passed; новая selection matrix дала32passed. Проверены
hand-literal verification order, index/owner-only/full closure, metadata после JSON read,
two-final/call isolation, original native/unsafe/duplicate/bool-size rejection. B1 actual same-size
mutation при stale observed stat отвергнута поздним actual SHA; это engineering fixture, не
наблюдённая production corruption/byte snapshot guarantee.

High review обнаружил Python Bool/int equivalence для optional identity. Original source/32-pass
logs сохранены до исправления. Narrow strict comparison прошёл RED4failed/1passed →
GREEN5passed/32deselected: conflicts до SHA/native, correct identity сохраняет5index+3owner SHA
→2native checks. Прежние32 не перезапускались на final fix; это явно ограничивает fresh verification
claim. Production hash/native loops остаются неизменными. Новых scientific/solver/
SCBA/Poisson/operator runs, installs/downloads/server/CI/deploy/merge нет.

Первый tmp budget128MiB не определял sparse accounting: retained fixtures заняли
physical25,985,024B, logical209,478,150B >134,217,728B. Общий temp-budget pass не заявлен; original
fixtures/logs сохранены. Отдельный P2 budget ограничивал новые fixtures32MiB как allocated и
apparent: фактически1,474,560B/1,220,052B. CPU/RAM не capped; peak not_measured. Это ограничение
собственной проверки, не изменение policy scientific storage или повод переписывать failed evidence.

Final two-path diff SHA256: `a6617bb4504fc093f0f9c92e5a3ec44e8a74ff51386fed0792f0e0384ee9224f`.

| Утверждение                                     | Свидетельство                                    | Ограничение                              | Решение             |
| ----------------------------------------------- | ------------------------------------------------ | ---------------------------------------- | ------------------- |
| Conflict отказ предшествует prior payload loops | Literal RED/GREEN и final5 cases                 | Local hand fixtures                      | изменить            |
| Оба SHA/native schedule сохранены               | Unchanged source loops, actual B1/order fixtures | Не atomic external snapshot              | сохранить           |
| Optional identity строго typed                  | Bool/float negative и exact positive5cases       | Final32 не повторялся                    | изменить            |
| Первоначальный tmp cap полностью соблюдён       | Physical26MB/logical209MB                        | Logical выше128MiB; ambiguous accounting | данных недостаточно |
| Ускорение или scientific acceptance установлены | Таких измерений/попыток нет                      | Normalization-only, SCI0                 | данных недостаточно |
