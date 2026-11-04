# Требования, трактовки и принятые решения

Пользователь остановил изменения кода и инфраструктуры. Этот документ сохраняет evidence и решения
для последующего анализа; он не возобновляет программу и не предлагает новую реализацию. Предмет —
какие ограничения действительно следовали из поручения, где документы оставляли выбор и как
наблюдаемые решения агента повлияли на путь к установленному продукту.

В рассмотренном наборе нет доказательства, что исходные требования человека были логически
невыполнимы. Есть сложные, но совместимые требования; явно условные альтернативы; последующие
изменения поручения; наконец, решения исполнителя, которым документы не задавали единственную форму.
Наиболее существенная ошибка порядка работ — превращение подробной квалификации dynamic memory в
препятствие первому полезному trial при наличии документированного fixed fallback. Это не
доказывает, что fixed path тогда уже работал или что всю dynamic работу можно было безопасно
удалить.

## 1. Как отделены источники и выводы

Здесь различаются четыре уровня:

1. **Поручение человека.** Прямое сообщение или его проверенная хронологическая запись. Более
   позднее применимое поручение заменяет прежнее в своей области.
2. **Нормативный документ.** План передаёт принятые решения, целевые contracts и авторские
   предложения с разными метками. Даже метка «Р» в опубликованном плане — документальное
   свидетельство решения, а не дословная стенограмма человека.
3. **Трактовка исполнителя.** Восстанавливается из reports, карточек и выбранного порядка работ. Это
   наблюдаемая позиция, а не утверждение о скрытых рассуждениях, сознательном намерении или мотивах
   модели.
4. **Решение в Source или design.** Реализованный символ, опубликованный commit либо frozen
   proposal. Наличие Source не устанавливает Native readiness; proposal не считается реализованным.

Основные публичные первичные источники зафиксированы на **исходной публикации плана** Root
`69d841fdd0fa84f835803560faf80bcfd682679c`, 2026-10-27T21:57:39+03:00. Это отдельная identity от
исходного code baseline `d395044ac09b28c2ff573724f8911d625df43bf5`; план не приписывается baseline,
в котором его ещё не было. Для прочитанных трёх документов Git diff исходной публикации и Root044cbb
не показал изменений.

- **Q01:**
  [project-simplification-2026-10-27.md](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/69d841fdd0fa84f835803560faf80bcfd682679c/docs/implementation/project-simplification-2026-10-27.md).
  Строки31–35 определяют «Ф/Р/К/А»: факт, решение пользователя, целевой contract, авторский выбор
  для review.
- **Q02:**
  [codex-execution-2026-10-27.md](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/69d841fdd0fa84f835803560faf80bcfd682679c/docs/implementation/codex-execution-2026-10-27.md).
  Полномочия, приоритеты и stages; подготовка плана не объявлена исполнением.
- **Q03:**
  [architecture.md](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/69d841fdd0fa84f835803560faf80bcfd682679c/docs/architecture.md).
  Реализованный baseline, границы пакетов и доверия.

Поздние указания ниже привязаны к
[хронологии01](01-context-timeline-and-size.md#2-хронология-прямого-steering-и-фактических-стадий) и
её локальному первичному session evidence, описанному в [08](08-evidence-and-preservation.md). Для
нового разбора Root адресно извлёк human records в private
`.build/session-evidence-followup-20261104/verified-human-steering-locators.json`; этот автор
прочитал extract, но не повторял полный разбор raw JSONL. Далее — парафразы, **не дословные цитаты
пользователя**. Session record line — локатор исходной сессии, не строка этого PR.

| Human evidence | UTC timestamp / session record line | Что меняет                                                                                                                                  |
| -------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| H01            | 2026-10-30T14:03:09.672Z /49466     | Разрешено самостоятельно корректировать технические limits по собранным фактам; это не новая научная модель и не blanket снятие всех guards |
| H02            | 2026-10-30T17:27:20.989Z /53258     | Перед переносом сохранить только genuine final старого исследования, без history; позднее исключение к первоначальному no-export            |
| H03            | 2026-10-31T17:55:39.032Z /72526     | Human question-reply подтверждает sole administration; вопрос был в72277,17:42:56.996Z; locator независимо найден reviewer11                |
| H04            | 2026-10-31T17:57:19.547Z /72550     | PVE администрируется root и не требует laptop sudo; это само по себе не доказательство sole administration                                  |
| H05            | 2026-11-02T15:46:53.204Z /104921    | Не рассматривать и не испытывать application update при running job; whole cluster update после stopped jobs                                |
| H06            | 2026-11-03T15:12:53.926Z /118007    | При недоступном laptop sudo приоритет main cluster/trial; worker готовить в доступном scope до следующего окна                              |

**Q04 — оформленное supersession.** Commit
[2ff7baa92ad3b4886646e825d54b61fe4f95339a](https://github.com/Afonenko-QCL-NEGF/qcl-negf/commit/2ff7baa92ad3b4886646e825d54b61fe4f95339a),
2026-11-02T19:07:55+03:00, изменил project-simplification после H05:
[L612–619](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/2ff7baa92ad3b4886646e825d54b61fe4f95339a/docs/implementation/project-simplification-2026-10-27.md#L612-L619)
явно запрещают update и его acceptance при работающей job. Соответственно изменены P23/P27 и дневные
gates. Это не следует читать как исходное правило27окт. Execution plan в этом изменении не
переписан; позднее direct steering и адресная нормативная правка имеют приоритет над его старой
общей формулировкой scoped rollout.

Использованы также опубликованные summaries [03](03-resource-architecture-and-decisions.md) и
[05](05-process-findings-and-analysis-questions.md), их named original Source/review packets.
Private `.build/...` locators и hashes ниже — указатели на локальные артефакты, **не файлы этого PR
и не общедоступные приложения**. Их raw содержимое может требовать редакции перед передачей.
Signing-key directory не читался. Новые tests, probes, PG/VM operations или scientific runs ради
этого документа не выполнялись.

## 2. Матрица требований и наблюдаемых решений

Классификация: **противоречие** — одновременно применимые требования нельзя выполнить вместе;
**напряжение** — совместимы, но требуют компромисса или порядка; **неоднозначность** — документ не
определяет существенную границу; **выбор агента** — конкретная конструкция не была единственно
предписана. Отдельно отмечено **замещение во времени**: прежнее правило отменено новым; это не
нерешённое одновременное противоречие. Уверенность высокая в прочитанном Source/документе, средняя в
причинной атрибуции; точная доля потраченного времени не вычислялась.

| ID, точное требование и локатор                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Класс                                                                                                                                          | Документированная трактовка и выбранное действие                                                                                                                                                                                                                                                                                                                                           | Эффект; невыбранная альтернатива                                                                                                                                                                                                                                                                                                           | Уверенность / недостающее                                                                                                                                     |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **M01.** «все VM постоянно resident»; «Нельзя уменьшать RAM ниже active job/build grant»; полный grant оплачивается до growth. Q01 [L478–502](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/69d841fdd0fa84f835803560faf80bcfd682679c/docs/implementation/project-simplification-2026-10-27.md#L478-L502). При неподдержанном active-floor — «проверенный conservative reservation», L540–545; при проблемах Slurm — fixed reservation, L589–596.                                                                                                                               | Разрешимое напряжение, условные ветви. Resident не означает, что сумма maxima может превысить physical capacity; dynamic return не безусловен. | Platform выбрал per-host paid state, quarantine/fence и dynamic qualification. В c470 `check_baseline` требует full-paid maxima и `running_quarantined`; `_validate_reservation_capacity` требует полный resident set. Далее nine-case design стал крупным следующим этапом.                                                                                                               | Conservatism защищал capacity, но CLOSED/full-paid не давали работающего body. Альтернатива уже была в плане: отдельно установить пригодность existing fixed path, не требуя dynamic-only completion. Это могло изменить critical path, но не даёт права объявить unknown fixed PASS.                                                      | Высокая: условный fallback и Source. Средняя: насколько раньше он был practically доступен; actual fixed trial отсутствует в данном evidence.                 |
| **M02.** «existing project primitive → native Nix/systemd/Slurm/backend API → готовая library → свой узкий adapter». Q01 [L328–340](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/69d841fdd0fa84f835803560faf80bcfd682679c/docs/implementation/project-simplification-2026-10-27.md#L328-L340). Одновременно сохранить8repos, L64;32review units названы авторским разбиением, L664–674.                                                                                                                                                                                       | Напряжение и выбор реализации; восемь ownership boundaries не противоречат reuse.                                                              | Сохранены Slurm, AiiDA, Nix, HDF5 и native APIs. Одновременно добавлены custom identity/receipt/schema/readback/proof layers. После поручения исполнить W01/P01–P32 этот scope стал заданием; авторская метка сама по себе не делала units необязательными. Split отдельных contracts разрешался L724–729; в selected Git ranges получилось250merge records, не32пользовательские функции. | Разбиение сохранило ownership и reviewability. Оно не задавало число циклов и не доказывало необходимость каждого layer до installed trial. Невыбранная последовательность — раньше замкнуть одну реальную цепочку, оставив необязательные capabilities явно pending. Это не требование объединить repositories или удалить все tests.     | Высокая: наличие reuse и расширения. Данных недостаточно: какая часть custom кода действительно повторяет native tools и сколько часов можно было сэкономить. |
| **M03.** «Нет искусственного общего лимита времени/CPU/RAM/числа попыток»; обычные timeouts и bounded buffers сохраняются. Q02 [L53–57](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/69d841fdd0fa84f835803560faf80bcfd682679c/docs/implementation/codex-execution-2026-10-27.md#L53-L57); campaign CPU grants удалить, Q01 L85–89.                                                                                                                                                                                                                                            | Разные области, не противоречие. Запрет campaign quota не равен безграничному command/API payload.                                             | Незавершённый `campaign_strict` удалён; ordinary admission/cgroups остались. В metadata consumers реализованы finite lifetime/workspace ledgers. Точные nonrefundable charge formulas,16/128/512MiB и копии — конкретный engineering contract, не цифры, заданные человеком.                                                                                                               | Finite limits ловили реальные overruns; actualA16/A32 отказал до завершённого consumer route. Дальнейший accounting стал самостоятельным design/review циклом. Альтернатива для анализа — сопоставить более простой payload/process bound с тем же threat model; cgroup сам по себе не заменяет host reservation или provenance integrity. | Высокая: различие quota/bound и observed refusal. Не установлено, какая минимальная модель достаточна; нынешний отчёт не разрешает менять caps.               |
| **M04.** Новая система автоматически продолжает exact checkpoint после fault, Q01 L74–75 и [L644–648](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/69d841fdd0fa84f835803560faf80bcfd682679c/docs/implementation/project-simplification-2026-10-27.md#L644-L648). Но старый run не экспортировать, restart полностью на новой версии, Q02 [L71–74](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/69d841fdd0fa84f835803560faf80bcfd682679c/docs/implementation/codex-execution-2026-10-27.md#L71-L74). Позднее30окт — сохранить только genuine final старого исследования. | Разные run/format scopes плюс позднее уточнение сохранности. Не конфликт exact resume и engineering cutover.                                   | Новый exact state/history contract разрабатывался отдельно. Старый checkpoint не обязан мигрировать; later final-only не разрешал partial-as-final. В опубликованном AiiDA336 native `QCLExecutionRestartWorkChain.setup` пока требует `max_iterations=1` и отвергает recovery/prior archive.                                                                                              | Старый run не должен был стать препятствием из-за отсутствия checkpoint copy. Но новый native exact recovery остаётся незавершённой target capability: Source state support не доказывает linked fault→resume. Альтернатива — явно staged native recovery, а не обещание готовности из constructor checks.                                 | Высокая: планы, Source restriction и адресный H02. Фактическое исполнение каждого старого data-retention действия здесь не расследовано.                      |
| **M05.** «Разрешено без повторного запроса внутри программы»: fixes/builds/deploy/PR/merge с review; Q02 [L32–51](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/69d841fdd0fa84f835803560faf80bcfd682679c/docs/implementation/codex-execution-2026-10-27.md#L32-L51). Авторский design проходит review, Q01 L31–35; routine API coordination не новый вопрос человеку, Q02 L385–389.                                                                                                                                                                                            | Автономность совместима с review; неоднозначна граница накопленного architecture expansion.                                                    | Исполнитель правомерно не спрашивал разрешение на каждый scoped fix и применял independent Source review. Наблюдаемая ошибка — необходимость нового subsystem часто уступала вопросу корректности exact patch. Main necessity review явно поставлен после запроса самодиагностики.                                                                                                         | Review нашёл реальные defects и предотвратил false PASS. Но chain локальных approvals не подтверждает ценность расширенного critical path. Альтернатива — раньше предъявить понятный operational choice и его цену; не новая обязательная процедура approval каждого файла.                                                                | Высокая: grants и два разных review-вопроса. Нет evidence, что каждое расширение было непорученным; blanket «агент вообще не имел разрешения» неверен.        |
| **M06.** Изначально compatible web/docs обновляются без остановки science; Q01 L71, [L611–635](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/69d841fdd0fa84f835803560faf80bcfd682679c/docs/implementation/project-simplification-2026-10-27.md#L611-L635). 2ноя15:46 — update-during-running-job убрать, весь кластер обновлять при stopped jobs.                                                                                                                                                                                                                              | Замещение во времени. Если удерживать обе версии как текущие, получится прямой конфликт acceptance сценария; latest instruction его снимает.   | Retrospective фиксирует maintenance-only supersession. Изначальный scoped-update design был обоснован прежним требованием, но после2ноя concurrent-update acceptance должен был исчезнуть из обязательного пути.                                                                                                                                                                           | Не следует продолжать решать отменённый scenario ради старого checklist. При этом необходимы unknown-outcome handling, state preservation и health/readback даже при stopped jobs. Альтернатива — сузить активный gate, сохранив старые designs как историю.                                                                               | Высокая: H05 и Q04. Полного аудита удаления всех stale gate/callsites нет.                                                                                    |
| **M07.** Initial API — «single trusted team's interface, not a multitenant security boundary», Q03 [L64–67](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/69d841fdd0fa84f835803560faf80bcfd682679c/docs/architecture.md#L64-L67). Защита foreign VM/shared storage сохраняется; Q01 L491–495 признаёт предел cooperating lock. 31окт уточнено sole PVE admin.                                                                                                                                                                                                                  | Разные trust boundaries и требующая решения неоднозначность. Trusted HTTP team не превращает любой root/process claim в достоверный.           | Source28 связывает конкретный собственный child с raw process census; неизвестный privileged process не исключается только по UID. Это разумный safety отказ при неизвестном ownership. Но цель защиты от произвольного враждебного администратора не следует из trusted-team baseline; original plan прямо признаёт предел local lock.                                                    | Нельзя честно обещать абсолютную host protection от другого root. Не следует и выбрасывать PID reuse/provenance checks: они защищают от обычных races и ошибок того же администратора. Альтернатива — явно ограниченный trusted-admin operational contract; его достаточность и минимальный proof пока не доказаны.                        | Высокая: Source28 invariant, исходный предел гарантии и раздельные H03/H04. Причинность «вся сложность из неверного hostile threat model» не установлена.     |
| **M08.** Все3backend обязательны в программе, но Linux first; дополнительные PVE/Hyper-V после Linux gate и человеческой подготовки. Q01 [L733–755](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/69d841fdd0fa84f835803560faf80bcfd682679c/docs/implementation/project-simplification-2026-10-27.md#L733-L755); Q02 L430–433.                                                                                                                                                                                                                                                  | Стадийность, не противоречие. Общий конечный scope не равен prerequisite каждой стадии.                                                        | В Source поддерживались backend-independent contracts и отдельные adapters. 3ноя laptop sudo недоступен; latest приоритет — main PVE installed trial, worker готовить до окна.                                                                                                                                                                                                             | Нельзя объявлять absent backend PASS или исключить его из полного scope. Нельзя и делать недоступный Hyper-V host причиной остановить independent main work. Альтернатива — separate readiness по backend/стадии, существующая в плане.                                                                                                    | Высокая: staged normative text и H06. Actual readiness каждого backend требует его receipts.                                                                  |
| **M09.** «Resident memory принимается одним ограниченным engineering scenario» на actual image, без provoked host OOM, Q01 [L784–789](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/69d841fdd0fa84f835803560faf80bcfd682679c/docs/implementation/project-simplification-2026-10-27.md#L784-L789).                                                                                                                                                                                                                                                                              | Выбор детализации. Один связный scenario может содержать несколько checks, поэтому сам счёт9 не доказывает нарушения.                          | Реализованы nine required predicates; MAIN proposal добавил bootstrap/main phases, two-body observations и closure/report chain. Независимый Source review нашёл terminal-reader и step-consumption blockers.                                                                                                                                                                              | Нужны physical reserves, actual limits, cleanup и fail-closed unknown. Но конкретные9cases и bootstrap mechanics — не единственная форма любой qualification, тем более fixed. Альтернатива — отдельно аттестовать конкретный first-use mode; нынешний документ не заменяет его новым design.                                              | Высокая: первоначальный текст и frozen proposal/review. Не измерена стоимость возможного более узкого accepted route.                                         |
| **M10.** Семь дней — ориентир, не автоматический timeout; продукт готов при установленном working path, Q02 L53–57 и [L438–439](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/69d841fdd0fa84f835803560faf80bcfd682679c/docs/implementation/codex-execution-2026-10-27.md#L438-L439).                                                                                                                                                                                                                                                                                           | Напряжение цели/оценки и выбор приоритета. Нет глобального budget не означает отсутствие обязанности объяснять пользу/остаток.                 | Публикации и PASS множились, но whole user path оставался незамкнутым; прогнозы65%/48–96ч позднее отозваны как неподтверждённые.                                                                                                                                                                                                                                                           | Длительная работа не нарушала искусственный deadline, которого не было, но это не оправдывает неподтверждённый прогноз и потерю фокуса. Альтернатива — отчёт о конкретном работающем/неработающем пути вместо процента по объёму артефактов.                                                                                               | Высокая по нормативной цели и отозванным forecasts; недостаточно activity/cost данных для точной доли waste.                                                  |

## 3. Что связывает трактовки с настоящим design

Усложнение не было только словарём отчётов. В Platform `c47097225a4a798e4124e30245c7b5b2063eb32a`
существуют
[CalibrationRepository/check_baseline/CalibrationEffectOwner](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_qualification.py#L206-L254),
immutable records, owner references и baseline checks. Это реализованные способы закрыть
crash/partial-action ambiguity. `check_baseline` L206–218 действительно требует unchanged paid state
и quarantine. Таким образом, «только thin wrapper native API» уже не описывает результат, но «всё
написано заново без reuse» также неверно.

Независимые reviews различили реальные ошибки. Source27 исправил потерю reservation identity joins.
Source28 добавил наблюдение уже принадлежащего command owner child, сохранив original raw census;
local negatives проверяли foreign/reuse/unknown и cleanup. Это защищало правильную границу, а не
просто увеличивало test count. Вместе с тем быстрый operand в32/32local one-shot observations не
давал live executable anchor. Значит, положительный Source/L verdict не был достаточным
доказательством operational пригодности observer для любой короткой команды; actual target frequency
неизвестна.

Source29 был proposed completed-exec witness, не production extension. MAIN был frozen proposal
полноценного dynamic vertical slice. Два независимых blockers относились к terminal reader chain за
пределами Jobs и к ошибочному равенству publication ACK с потреблением шага обоими bodies. Эти
находки нужно сохранить: они показывают, почему нельзя было просто запустить design как принятый.
Они не доказывают, что надо сначала реализовать весь design для fixed trial.

Связь с M01 и M09 наблюдаема прямо в Source:
[open_native_jobs](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_qualification_sources.py#L364-L365)
всё ещё возвращает `qualification_worker_phase_required`. Одновременно
[NativeFactsProvider._fixed_qualification](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_facts.py#L646-L710)
существует отдельно: для PVE требует actual disabled balloon/full maximum, exact runtime/Source,
fresh guest, registration и reserve. Его наличие подтверждает альтернативную ветвь design, но **не
actual пригодность установленного fixed пути**. Открывать admission по одному этому факту нельзя.

Для M03 настоящая польза finite accounting — обнаруженные consumer refusals, aliases/copies и
omitted offline debit, исправленный независимым review. Его цена — additional Source card и
несколько циклов контрактной проверки при ещё не выполненном full A128/B512 lifecycle. Отсюда
следует вопрос о достаточности выбранной модели и её эксплуатационной цене; не следует доказанная
ненужность всех guards. Для M04 опубликованный
[workflow.py:setup](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/blob/336358dfd10c698e4b4a71d8c93562aaa8ee7182/src/aiida_qcl_negf/workflow.py#L50-L65)
позволяет точнее назвать пробел: новый native automatic recovery ещё не поддержан этой ветвью, даже
при наличии общего retry framework.

Локальные первичные packets к этим claims перечислены подробно в03 R05–R11 и04 T06–T13. Существенные
frozen identities: Source28 `FREEZE.json` SHA256
`4874b73cbcd6c5564a6d47d37c51b0f5605efb9c593bda670c2682b105e0d3a5`; private MAIN `DESIGN.ru.md` —
`54960a193c245cf8b1ef4fbae65baf42d7293774fbaaf4b41d849cf5bfb1564a`; private independent MAIN
`REVIEW.ru.md` — `2ef3981232e839c5fe391226b191ebee25935682b8924137e0e679a2b30cad44`. Они фиксируют
точные объекты анализа; не являются публичным runtime certificate.

## 4. Граница причинного вывода

Подтверждённая причинная цепочка узкая: условный fallback присутствовал в нормативном плане; dynamic
route оставался закрыт; выбранное дальнейшее развитие требовало новых concrete contracts и
исправлений; necessity review позднее признал, что этот объём не универсальный prerequisite fixed
эксплуатации. Поэтому справедливо говорить об ошибке формирования critical path и позднем
предъявлении альтернативы. Несправедливо утверждать, что fixed вариант гарантированно дал бы готовый
кластер в конкретный день: actual configuration, переход, consumer lifecycle и coherent install всё
ещё могли требовать работы.

Аналогично, trusted-team baseline ограничивает заявляемую security guarantee, но не отменяет защиту
от случайного PID reuse, чужих процессов, stale identity или partial mutation. Missing
ownership/readback должен оставаться unknown/HOLD. Пересмотр угроз и необходимого объёма proofs —
отдельный аналитический вопрос, а не вывод «администратор один, значит проверки не нужны».

Смена требований во времени не оправдывает одновременное исполнение обеих версий. Final-only старого
run не отменяет full compact history новой системы; maintenance-only отменяет прежний
concurrent-update scenario, но не integrity при обычном update. Код, оставшийся от старого
требования, может быть полезен либо избыточен; это устанавливается по current call graph и scope, а
не по возрасту.

Положительный evidence работы — публичные interfaces, удалённый strict branch, независимые readers,
реальные найденные identity/lifetime bugs и сохранённые failures. Отрицательный evidence результата
— незавершённый installed user path и превращение опциональных стадий в последовательные
prerequisites. Ни один из них не даёт численного процента бесполезной работы, обвинения пользователя
или достоверного рассказа о внутренних мотивах агента. Текущий вывод — сохранить эти различия для
внешнего review в существующем evidence PR/issue, оставив code/infra остановленными.

| Утверждение                                                                     | Свидетельство                                                   | Ограничение                                                       | Решение                                                            |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------ |
| Исходные требования в этом наборе логически несовместимы                        | M01–M10: условные branches, разные scopes и supersession        | Это не аудит всех сообщений месяца                                | данных недостаточно для такого обвинения; не утверждать            |
| Dynamic proof был единственным разрешённым путём                                | Q01 L540–545,589–596; distinct fixed Source branch              | Actual fixed readiness неизвестна                                 | сохранить fallback как реально разрешённую альтернативу            |
| Запрет campaign quota отменял finite safety bounds                              | Q02 L53–57 прямо сохраняет bounded operations                   | Точные ledgers/caps не предписаны этим текстом                    | сохранить различие, отдельно анализировать цену выбранной модели   |
| Все последующие design choices были прямо требованиями человека                 | «А/К/Р» в плане; concrete Source/proposals и M02/M05/M09        | Широкое scoped execution было разрешено                           | изменить атрибуцию: требование отдельно, выбор реализации отдельно |
| Actual design был только бесполезным scaffolding                                | Source27/28 fixes, custody/lifecycle checks, original negatives | Whole installed usefulness и стоимость не доказаны                | сохранить положительное evidence и limits                          |
| Maintenance-only и final-only оставляют старые противоположные правила текущими | H02/H05 с timestamps/record lines, нормативный Q04              | Raw session не публикуется; full stale-callsite audit не выполнен | сохранить supersession; не исполнять исторические gates по инерции |
| Этот документ разрешает новый design/runtime                                    | Явный current user STOP                                         | Текущий scope — evidence и публикационная подготовка              | сохранить остановку                                                |
