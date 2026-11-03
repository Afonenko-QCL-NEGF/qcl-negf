# Контекст, хронология, Source snapshots и размер

## 1. Область и исходная цель

Исходный запуск этой сессии:27 октября2026,19:03:45UTC. Пользователь поручил исполнить W01/P01–P32,
получить установленный проверенный кластер, первый дополнительный Linux-worker, актуальные русские
руководства; сохранить физическую модель/reference и защитить foreign ресурсы. Начальный
согласованный состав в исполнительном плане — Root `d395044ac09b28c2ff573724f8911d625df43bf5`; это
before для компонентного сравнения. Сам план уже включал много staged возможностей, но seven-day
schedule был ориентиром, а не разрешением подменить полезный результат бесконечными новыми
prerequisites.

Сессия не покрывает всю историю с начала октября. Root Git имеет более ранние commits и большой
объём docs/evidence до27 октября. Ни их сложность, ни все четыре недели нельзя приписать одной этой
сессии. Ниже измеряется конкретный before/after и приводятся вопросы для отдельного более раннего
анализа.

## 2. Хронология прямого steering и фактических стадий

ВремяUTC; для Europe/Minsk добавить3часа. Это отбор существенных событий, не полный рассказ о каждом
tool call.

| Дата       | Поручение / наблюдение                                                                                                                          | Что это меняет                                                                           |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| 27окт19:03 | Начать программу упрощения, сохранить чужие overlays, R00 до interrupt, scoped полномочия и параллельные independent задачи                     | Цель — installed system; Source work само по себе не finish                              |
| 28окт      | Пользователь разрешил удалять прежние тестовые laptop VM; готовил libvirt/root окна; просил не конфликтовать с existing PVE workers             | Portable-worker bootstrap разрешён, foreign VM/LAN защищены                              |
| 29окт      | Запрос общего прогресса без остановки работ; позже sudo временно недоступен                                                                     | Independent Source work должен продолжаться без зависимого root шага                     |
| 30окт      | Несколько проблем сети; пользователь разрешил менять произвольные технические limits по фактам, попросил bridge recovery после reboot/IP change | Actual receipts и network rollback нужны; старые limits не являются физическими законами |
| 30окт      | Поручено сохранить только настоящий финальный результат прежнего исследования перед прерывающим переносом; guest agent обязателен               | Не сохранять history/checkpoint/partial-as-final; обычный QGA diagnosis перед restart    |
| 31окт      | Подтверждено единоличное администрирование PVE; там root, а не laptop sudo                                                                      | Host capacity agreement имеет уточнённую trusted-admin границу                           |
| 1–2ноя     | Повторные вопросы «скоро кластер?»; ряд actual OS/App/resource-install/readback стадий, но backend admission всё ещё закрыт                     | Компоненты/установка продвигались без законченного user path                             |
| 2ноя15:46  | Пользователь убрал update-during-running-job; весь кластер обновлять при stopped jobs                                                           | Этот сценарий должен уйти из критического пути                                           |
| 2ноя15:51  | Явное желание закончить обвязку и вернуться к физике                                                                                            | Высокий уровень scope не оправдывает задержку первого полезного пути                     |
| 3нояутро   | Sockets enabled; серия bridge precondition/profile/L3/STP/route failures и rollback; восстановление после interruption                          | Реальная стоимость неправильных предположений об окружении, не только feature coding     |
| 3ноя15:12  | Laptop sudo недоступен; приоритет main PVE installed cluster/trial, worker готовить до следующего окна                                          | Worker network не должен блокировать main ready задачи                                   |
| 3ноядень   | Genuine tiny producer прошёл; Results/AiiDA consumer упёрлись в metadata allowance; исправления reviewed, whole Results suite завершён          | Настоящий integration gap наконец показан реальными данными; это не scientific trial     |
| 3ноя19:04  | Пользователь запросил самодиагностику полезности недельной работы                                                                               | Выявлен разрыв между объёмом Source/evidence и installed readiness                       |
| 3ноявечер  | Пользователь остановил изменения и поручил Markdown reports→PR+issue; затем попросил помощи в выборе дальнейшего подхода                        | Code/infra остаются; scheduling paused; текущая работа только evidence и предложения     |

Прямые пользовательские события проверены в локальном JSONL session, созданном27окт; первые и
последние локаторы в evidence08. Heartbeat payload не считался новым человеческим разрешением или
самостоятельным подтверждением пользы.

## 3. Точный размер: что измерено

Считались tracked Git blobs выбранных refs, а не весь рабочий каталог, Nix store, submodule
duplicates, build caches или научные результаты. Gitlinks не разворачивались рекурсивно внутри Root;
каждый из8 компонентов посчитан один раз. UTF-8 text безNUL, строка=LF плюс последняя непустая
незавершённая строка; blank/comments тоже строки. Binary считается по files/bytes отдельно, но не по
lines. Ни одного blob>10MiB в этих snapshots не встретилось.

Это **physical text lines**, не language-aware SLOC, не complexity score, не число вручную
написанных строк и не developer-hours. Категории определены pathname/extension. Code
вsrc/ops/nix/modules/scripts/.github относится к source/build; tests/fixtures отдельно;
docs/implementation отдельно как plans/evidence; documentation assets включаютSVG/CSV и не равны
прозе. Method script выполнялся только как чтение Git objects. Детальная локальная таблица/count
script сохранены как evidence; содержимое blobs в публикацию не копировалось.

### Восемь компонентов

| Категория                         |      Before |       After |          Net |
| --------------------------------- | ----------: | ----------: | -----------: |
| Конфигурация, lock, прочие assets |      22,977 |      23,950 |         +973 |
| Документация и её assets/data     |      81,064 |      89,366 |       +8,302 |
| Прочий текст                      |       2,192 |       2,621 |         +429 |
| Исходники и сборочные скрипты     |      92,866 |     135,240 |      +42,374 |
| Тесты и fixtures                  |      78,004 |     145,206 |      +67,202 |
| JSON/YAML schemas                 |       8,550 |      34,895 |      +26,345 |
| **Все текстовые строки**          | **285,653** | **431,278** | **+145,625** |

Ранее сообщённый directory-based ростsrc/ops/nix/modules +56625 включал всё содержимое этих
каталогов, в том числеJSONschemas; refined source/build category выросла **+42374**. Это два разных
определения. Предыдущее число не означает столько же новых строк executable logic. Тесты/fixtures
дали+67202, schemas+26345; они составляют большую часть недельного роста.

| Компонент          | Before text lines | After text lines |     Net | After source/build lines |
| ------------------ | ----------------: | ---------------: | ------: | -----------------------: |
| QCLNEGF.jl         |           100,032 |          106,808 |  +6,776 |                   24,529 |
| QCLNEGFRunner.jl   |            62,530 |           75,657 | +13,127 |                   37,627 |
| qcl-negf-contracts |            12,287 |           41,329 | +29,042 |                    6,447 |
| qcl-negf-results   |            19,800 |           34,674 | +14,874 |                   14,790 |
| qcl-negf-aiida     |            10,780 |           33,835 | +23,055 |                    9,571 |
| qcl-negf-platform  |            53,624 |          107,429 | +53,805 |                   30,405 |
| qcl-negf-portal    |            23,204 |           28,062 |  +4,858 |                   11,713 |
| qcl-negf-research  |             3,396 |            3,484 |     +88 |                      158 |

### Root отдельно и общий каталог

Root без component gitlinks:220464→223255 text lines. В before уже было185908
строкdocs/implementation plans/evidence; after187197. Это преимущественно ранее накопленные планы,
reports, JSON receipts, patch/log copies, а не вычислительный код. Например, одна pre-existing
tracked execution/checkpoint.json имела12881строку. Root docs/assets не смешивались с component
science.

Если механически сложить Root и8 selected component snapshots, получается506117→654533 text lines;
source/build category102469→144681. Это не утверждение «у solver654тысячи строк».
Вafter156475строкtests/fixtures,34895schemas,187197implementation plans/evidence и101526docs/assets.
Поэтому вопрос «проект200к?» без указания состава/категории не имеет одного честного ответа. Даже
отдельно~145тысяч source/build lines — большой объём для одного владельца; точная классификация не
отменяет пользовательской проблемы проверяемости.

After здесь — каталог последних опубликованных heads компонентов, а не один уже установленный
coherent release: Root selected composition может отставать. Это важно и для количественных выводов,
и для reproduction.

## 4. Source snapshots

| Компонент          | Before изRootd395                          | Последний опубликованный head при остановке |
| ------------------ | ------------------------------------------ | ------------------------------------------- |
| QCLNEGF.jl         | `0df7dd5a481c2c339e8520d2291c035253e7c0e2` | `01d472141a91c9429f43f7237460a17592d65845`  |
| QCLNEGFRunner.jl   | `8264f48c01ccc524548036d4b3f44552a76f19b5` | `97ab889ff83b73d9fad5d34e278309b2efe3b299`  |
| qcl-negf-contracts | `41209389109d387912b0410a5244dbc29ff1ff42` | `5eb0e61a9fc12fa2215291e47b7cd28888ce64cc`  |
| qcl-negf-results   | `f811d7c43bef8a70eb79ef74d554f08496a9af1c` | `10a32422b90a21ee728e73283217ac6b81bcf760`  |
| qcl-negf-aiida     | `7f4223eaff86b3a6104743098162ffa3fc4e0334` | `336358dfd10c698e4b4a71d8c93562aaa8ee7182`  |
| qcl-negf-platform  | `1b1370d2b8e83a267a97c8d49df14db220123478` | `c47097225a4a798e4124e30245c7b5b2063eb32a`  |
| qcl-negf-portal    | `104481fdce8e11c9734b8b5b0f2743c9e5760151` | `2c31e5fd597600ac632c292969c02dce0e50d020`  |
| qcl-negf-research  | `408ca413a8df865110edfb480db2c8544452b8d0` | `46fb51fbd594be80127cf543c7160fc69d8e3b2d`  |

Root public programme head:`a29fe2fb19aba0bab216c520653627316f099cce`. Private coherent
candidate:`e37f755c75e1098ae66aca32ef519773d946df34`, ещё не опубликован; он отстаёт по части latest
component refs. Installed runtime build source:`f2db3115b423c8508d65fa4422441918806d92c6`. Existing
main checkout:`044cbb420e66078207b77eadd7f54c1324b884b0` с6 сохранёнными unrelated component
overlays. Ни один из этих refs не подставляется вместо source другого run. Docs-only evidence branch
не меняет component gitlinks.

## 5. Количество публикаций не равно готовности

В selected before→after Git ranges найдено250 merge commits:92Root и158компонентных. Это
воспроизводимая характеристика истории, не250независимых готовых возможностей и не доказательство
авторства каждого изменения этой сессией. МногиеRoot merges лишь обновляли gitlink после owning PR.
Полный индекс в07 позволяет отобрать конкретные изменения для review.

## 6. Чего эти числа не устанавливают

Не устанавливаются scientific speedup, качество сходимости, время до accepted science, heap/RSS,
число полезных tests, процент бессмысленных строк, деньги или часы активной разработки. Не выполнен
semantic review всех597 changed component paths. Рост Source — основание исследовать
scope/ownership, а не автоматически удалить код. Current user просит оставить всё как есть.

| Утверждение                            | Свидетельство                                             | Ограничение                                 | Решение                              |
| -------------------------------------- | --------------------------------------------------------- | ------------------------------------------- | ------------------------------------ |
| За неделю произошло большое расширение | Exact refs/count method; net145625 component text lines   | LOC включает разные категории               | сохранить раздельные числа           |
| Весь проект имеет200к executable code  | Ни одного такого измерения нет                            | Total text иsource/build различаются        | исправить формулировку               |
| Результат отстаёт от публикаций        | Source/private/installed matrix; runtime gaps             | Нет trustworthy % functional readiness      | измерять конкретный user path        |
| Вся история с начала октября разобрана | Этот пакет касается27окт–3ноя и named earlier public docs | Другие сессии/ранние решения не аттестованы | дополнительно анализировать отдельно |
