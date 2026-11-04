# Ресурсная архитектура: исходная цель, доказательства и остановленные решения

По прямому поручению пользователя implementation и инфраструктурные действия остановлены. Код и
инфраструктура оставлены в текущем состоянии; этот документ сохраняет свидетельства, решения и
нерешённые вопросы для последующего анализа. Он не разрешает продолжить реализацию, запустить jobs,
изменить admission, переключить memory policy или выполнить научный расчёт. Состояние «пауза»
относится и к предложенному ниже в историческом контексте порядку продолжения: теперь это
сохранённое решение для будущего рассмотрения, а не действующий план исполнения.

Отчёт составлен по публичному плану, primary Source Platform/Runner и частным review packets.
Сетевые адреса, идентичности хостов и заданий, private policy/configuration, ключи и raw logs сюда
не перенесены. Частные packets указаны относительными локаторами и hashes: они нужны для проверки
происхождения вывода, но не предлагаются к публикации целиком. Номера Source27/28/29 — локальные
имена этапов работы, а не версии публичного API или установленного продукта.

## 1. Что требовалось исходно

Программа упрощения должна была привести к работающей установленной системе, понятному обновлению
компонентов и возвращению к физике. В ресурсной части исходный план требовал сохранить существующие
VM, использовать native backend API, Slurm и cgroups, защищать physical host и чужие ресурсы,
отделять qualification от текущего health. Он не поручал строить самостоятельный scheduler или новую
постоянно работающую orchestration service. Источники: план §§4.3–4.5, 5 и 9 (R01).

Для dynamic memory был принят маршрут
`REQUEST → HOST_GRANT → GROW/readback → GUEST_ADMIT → RUN → SHRINK/readback → RELEASE`. Полный grant
должен быть учтён до роста RAM; configured/requested RAM не равна реально полученной. Неопределённое
изменение остаётся charged до reconciliation. Active grant нельзя отзывать по TTL или уменьшать ниже
живой allocation. После работы release требует подтверждённого cleanup и readback. Это safety
contract, а не необязательная диагностическая детализация (R01, R02).

Одновременно план прямо оставлял conservative/fixed fallback. Если native active-floor механизм или
ballooned Slurm path не обеспечивает требуемого поведения, dynamic mode остаётся unsupported, а
worker использует подтверждённую фиксированную reservation. §9 требовал один bounded engineering
scenario на actual image: заранее известные workload size, output cap, reserves, controlled-pressure
ceiling и stop condition; retained host/guest/job evidence; отсутствие намеренного host OOM. Полный
положительный девятислучайный отчёт не был исходным универсальным prerequisite любого полезного
installed trial (R01).

Здесь важна граница применимости. Fallback не освобождает от проверки actual RAM, Slurm/cgroup
limits, Source, cleanup и host reserves. Он позволяет не доказывать online shrink/balloon semantics
для режима, который этими возможностями не пользуется. Неизмеренный fixed path нельзя объявить
supported одной сменой флага.

## 2. Как устроена реализованная ресурсная граница

В Source Platform ресурсный владелец работает с policy, original operation и durable receipts;
AiiDA/NativeActor/Slurm сохраняют job ownership. Runner владеет scientific execution и публикацией
результата. Platform не выбирает физические допуски, а scheduler не принимает научный результат по
process exit. Эти границы соответствуют архитектуре репозитория и исходному плану (R02, R03).

Host admission использует физический баланс полного объёма grants: host/control/safety reserves,
согласованный foreign maximum, полный guest grant каждой owned VM и overhead. Guest `MemAvailable`
служит дополнительным текущим pressure gate, но не заменяет этот баланс. Нельзя дважды вычитать
resident RSS или считать virtual maximum физической гарантией. Native cgroup `memory.max`
ограничивает task внутри VM; он сам по себе не резервирует память гипервизора (R01, R02).

В рассмотренном calibration пути full-paid baseline сохраняет полную оплату maxima resident VM даже
при исследовании меньшего actual G. Поэтому «paid V» и «actual G» — разные величины. Закрытый
admission и full-paid state защищают состояние, но ещё не дают разрешения запустить body. Нужны
actual guest capacity, source/boot/runtime identity, original job/creator/prolog и действительные
task limits. Повторное использование старой записи или изменение paid bytes ради прохождения
проверки это не заменяет (R02, R04).

Для workload demand используется различие D и L: D — retained commitment, L — фактический enforced
task limit. Все authorized, pending, unknown и live D остаются учтёнными до полного normal или
abnormal physical closure. Будущий L не выводится из планового D. В рассмотренном body guard
требуется actual finite L каждого участвующего allocation; отсутствие peer allocation приводит к
отказу, а не к предположению о его готовности (R04).

Native memory effect имеет original owner, intent, dispatch и readback. Потерянный ответ не даёт
права повторить эффект по новому идентификатору или признать его завершённым по одному совпадению
target. Это важная защита от двойного dispatch. Но далее вокруг этих исходных инвариантов появился
более подробный private qualification protocol: отдельные roles, immutable permits, mirrors, clock
transcripts, observation slots и deterministic reports. Сам факт роста этого protocol не доказывает
ни его бесполезность, ни его необходимость до первого fixed trial.

## 3. Full-paid, CLOSED и девять dynamic cases

В Platform `c470972…` список REQUIRED_CASES содержит девять случаев: idle shrink, idle grow, restore
full, near floor, active-floor protection, pressure, supported rejection, lost outer response и
closure. `qualification_candidate` заново строит отчёт из original observations и требует PASS всех
случаев. Положительные supplied flags сами по себе не принимаются (R04).

Это содержательная проверка dynamic capability. Например, pressure требует роста actual PSI и
`memory.current`, а active-floor case связывает перекрывающиеся original generations, завершение
одного job и продолжающуюся работу другого. Supported rejection требует отказа ниже aggregate floor
до C dispatch и неизменённого readback. Closure связывает revocation, закрытие jobs, restore и
fence. Exit code управляющего процесса не является эквивалентом этих предикатов.

Однако девять cases являются выбранным подробным contract для положительного dynamic candidate. Их
нельзя автоматически переносить в критерий готовности всех остальных режимов. Существование Source
evaluator ещё не означает, что установленные callers способны произвести все его observations. В
ходе review обнаружилось, что отсутствуют необходимые workload wiring, terminal readers и отдельные
recovery paths. Именно этот разрыв между «предикат существует» и «продукт проходит связный путь»
стал существенной частью дальнейшей работы (R04, R09).

## 4. Source27: полезное исправление actual identity joins

Source27 revision2 исправлял конкретный consumer defect: `_validate_reservation_capacity` терял
часть связи actual native readback с original RuntimeBinding и повторную связь worker identity с
actual accounting identity. Полная оплата и schema-valid worker object не доказывали, что
наблюдалась та же runtime generation. Исправление восстановило сравнение native binding fields и
согласование machine/boot/kernel/image-related facts без подстановки missing данных из plan или paid
V (R05).

Первичные различающие fixtures были сохранены: неизменённый независимый набор сначала давал пять
отказавших assertions и один positive control, после исправления — шесть PASS. Авторский affected
набор сообщал 1056 tests и 561 subtests PASS; отдельный подготовленный App набор — 658 PASS. Эти
числа относятся к адресному Source/L этапу, а не к приёмке VM или запуска на установленном кластере.

Это изменение имело прямую safety-пользу и не сводилось к оформлению отчёта. Его ограничение также
конкретно: оно устраняло ошибку relation checks, но не подключало jobs worker, не давало actual
low-G admission, не закрывало late cleanup/fence и не делало scientific result accepted. Сохранять
это исправление и сохранять его ограниченную область доказательства — совместимые решения.

## 5. Source28: собственный child, полный census и проблема короткой команды

Следующий gap касался privileged processes внутри job census. Нельзя исключить PID только потому,
что он имеет подходящие UID, executable, argv или cgroup. Для исключения собственного readonly
`scontrol listpids` потребовалась связь с единственным process owner, который действительно создал
child; прочий неизвестный Root process должен оставаться в полном raw census и приводить к отказу
classifier (R06).

Source28 добавил optional immutable process observer в существующий command owner и передал его
через NativeSources. Producer сам получал PID от единственного Popen, проверял unreaped direct
child, actual owner/child identity и literal argv. Consumer повторно связывал это с собственным
authenticated root/sudo ancestry и original Source. Full raw stdout/rows/captures сохранялись
отдельно; projection могла исключить только exact own cohort и original observed child, с отдельным
exclusion witness. Default path, один cleanup owner, absolute deadline и existing classifier
сохранялись.

Независимый review принял exact Source28 как Source/L implementation. Его собственный bounded run
дал 337 tests и 573 subtests PASS, включая восемь дополнительных негативных cases: duplicate child
PID, чужие job/step, unknown/missing terminal, похожий foreign root, deadline до spawn и exec
failure. Frozen source не изменился. Consumer credentials/root/sudo views в части fixtures были
synthetic; настоящими были локальный Popen, PID/PPID/birth, stdout и reap. Это существенное
свидетельство control flow, но не Native root/sudo acceptance (R06).

Одновременно первичные 64 one-shot local measurements выявили availability limit: быстрый `true` не
получал stable live exe/cmdline anchor в 32 из 32 случаев; pinned Python завершался с anchors в 32
из 32. Cleanup оставался подтверждённым во всех 64. Эти измерения не были retries до pass и не
измеряли частоту на actual target `scontrol` (R07).

Здесь нет противоречия между положительным Source review и отрицательным измерением. Source28
безопасно сохранял CLOSED при missing live anchor. Он делал именно то, что требовал тогдашний
contract, но этот contract не обеспечивал универсальную применимость к коротким native commands.
Review не принимал operational scontrol readiness и отдельно оставлял durable delivery наблюдений
зависимым integration gate.

## 6. Source29: предложенная цена устранения proc race

Source29 на момент остановки был frozen design и evidence packet, а не production implementation. Он
предлагал отдельный `completed_owned_exec` variant для ровно fixed readonly scontrol command.
Planned executable/argv должны были оставаться отдельными полями; observed executable у zombie не
выдумывался. Вывод об initial exec строился из trusted pinned CPython fork/exec path, literal
retained normal exit0, повторных zombie metadata samples, original child ownership и успешного
прежнего cleanup (R08).

Первичные local controls были полезны: failed exec давал ошибку, а signalled process показывал,
почему одного Popen return или empty errorpipe недостаточно. Отдельные probes сохраняли retained
zombie с нормальным exit0 при уже недоступном exe. Но диагностический trace сам не считался
admissible production profile. Матрица будущих counterexamples не называлась набором уже пройденных
tests.

Предложенная доверительная база оказалась широкой: pinned interpreter/startup/import chain, closed
environment, source receipts, exact ELF/loader/config, bounded per-call identity checks, original
role/plan/permit/boot и same-call output join. Обсуждался узкий isolated helper startup без `site`;
Root prestaging bytehash receipts должен был отделить дорогой Source hashing от fresh physical-proof
TTL. Это объясняет, как конкретная короткая команда привела к заметному объёму дополнительной
квалификации.

Такой объём не следует оценивать только по названию «observer». Для выбранного strict dynamic census
он закрывает реальный availability gap без generic Root PID filter. Но он не закрывает остальные
workload/report gates и не является безусловным prerequisite работающего fixed-reservation кластера.
Автор Source29 отдельно зафиксировал возможность отложить witness при действительно принятом
existing fixed fallback. Независимый Source28 review и авторская defer-оценка в этом пункте
согласуются; это условное решение по применимости, не отказ от безопасности (R06, R08).

Ни реализация Source29, ни actual worker Source enrollment, ни его положительный Native outcome в
этом отчёте не утверждаются.

## 7. MAIN design: почему это уже отдельный vertical slice

MAIN design пытался связать существующего resource worker, QualificationJobs, NativeActor/Slurm,
actual Source readers и Runner fixture в единый dynamic qualification цикл. Он не предлагал второй
scheduler или новый monitoring stack. Тем не менее по объёму необходимых новых private contracts это
была отдельная разработка, а не простое подключение готовых методов (R09).

Bootstrap dependency была реальной. `capacity_document` требует workload accounting и несколько
genuine mappings, тогда как job stage/admission уже ожидает этот profile. При отсутствии пригодного
same-Source measured input design предлагал exploratory full-max operation B, его physical closure и
mappings, затем новый immutable MAIN operation N. Это означает отдельные genuine births; terminal
jobs B нельзя переименовать или повторно submit как N. Ветка без готового measured input потребовала
бы минимум двух пар jobs, а не одной пары на весь B+N цикл.

Другие необходимые изменения включали разделение preliminary preflight и окончательной actor
authorization, workload runtime рядом с unchanged idle lane, Root-only held/release/closure/probe
actions, actual L peer wait, low-G predicate по settled C при full-paid V, abort closure и
role/fence terminal чтение. Предлагались finite plan/worker versions, observation slots и Root-owned
control projection, читаемая Runner в том же процессе. Каждое такое изменение могло быть обосновано
своей зависимостью, но совокупность уже стала новым критическим путём до первой полной dynamic
приёмки.

Runner fixture при этом сохранял honest negative scientific final. Platform `_completed_metadata` и
Runner97ab publication path позволяют genuine failed/invalid/unconverged result при process exit0 и
Slurm COMPLETED/0:0. Это корректно: process завершил publication, а solver science не принималась.
Normal job close требует genuine final и полной absence; abnormal/no-final cleanup должен иметь
отдельный operational outcome и не производить fake final (R03, R09).

Pressure оставался условным результатом. Без actual PSI и memory.current growth case остаётся
NOT_MEASURED; acknowledgement команды не заменяет рост counters. Возможный отдельный memory.high
probe не был частью minimum implementation и требовал своего reviewed effect contract.
Следовательно, design не обещал гарантированного девятислучайного PASS из простого запуска двух
synthetic bodies.

## 8. Два независимых blocker полного design

Независимый Source-only review вернул MAIN design на два конечных уточнения. Product code и
инфраструктура этим review не менялись; никаких новых tests или jobs не запускалось (R10).

**Первый blocker — terminal reader chain шире Jobs.** В design был замечен active fence в Jobs._load
и предложен closed reader. Но source chain для report также проходит через
provider.calibration_observation, parent._catalog, proofs.owner_for и
CalibrationEffectOwner.**init**; последний требует active fence. После успешного fence unlink один
исправленный Jobs reader ещё не позволяет восстановить тот же report по original C
witnesses/readbacks. Аналогично partial role close должен быть читаем после selector unlink и до
общего final fence tombstone. Общая фраза «terminal reader» не определяет достаточный конечный port
для этих стадий.

Review требовал назвать read-only terminal routes для C originals, Jobs, partial role close и
report; mutating owners должны оставаться active-only. Это не предложение ослабить
`repository.active` до любого closed-looking файла. Сохранялось и конкретное различающее требование:
закрытая operation повторно читает тот же report, но не получает stage/case/C capability; crash в
середине selector close продолжает только original reconciliation.

**Второй blocker — publication ACK не равен потреблению шага обоими bodies.** Предложенный
current.json CAS показывал последний coarse step, тогда как Reader должен был отвергать out-of-order
steps. Допустимый schedule: A быстро потребляет pressure step и создаёт измеренный рост суммы
counters; B ещё не прочитал его. Root публикует следующий finish step. B видит скачок ordinal и
обязан отказать. Existing pressure predicate проверяет aggregate growth, а не consumed-step barrier
каждого body, поэтому он не исключает эту гонку.

Review требовал конечную семантику доставки четырёх steps: bounded immutable prefix либо per-member
coarse consumption barrier с original birth/source joins. Такой receipt должен оставаться
nonauthorizing, а actual cgroup/overlap/absence — независимо проверяться. Это сохраняло требование
«никакого дополнительного privileged helper на poll». До остановки ни один из этих вариантов не был
выбран и реализован как новый продуктовый contract.

Разногласие сохранено в точной форме: автор представил проект как готовый к review, reviewer счёл
полный маршрут ещё не замкнутым. Это не finding опасного deployed кода; спор относился к
достаточности ещё не реализованного design. Наличие этих blockers не доказывает неправильности всех
предшествующих Source repairs.

## 9. Что действительно safety, а что стало выбранной сложностью

Независимо от dynamic или fixed режима нельзя отложить known ownership, полный physical reserve
balance, actual guest/task limits, Source identity, original effect owner, no replay, удержание
unknown commitments, whole-subtree cleanup, сохранность результата и честное разделение
process/science. Это необходимая защита кластера, а не избыточное доказательство.

Для положительной dynamic qualification дополнительно нужны low-G mappings, measured R/K,
проверенный grow/shrink, overlapping live jobs, survivor floor, pressure и crash/reconcile evidence.
Детальный nine-case report — один выбранный способ сделать это воспроизводимо. Его разумно сохранять
как отдельный programme debt, но нельзя считать каждую его внутреннюю data structure единственно
возможной архитектурой или обязательным входом любого fixed trial.

Альтернативы не были взаимозаменяемыми по смыслу. Slurm уже владеет allocation и очередью; cgroup
ограничивает task, но не host reservation; static full allocation сокращает online state space, но
требует действительного physical fit; native PVE memory API умеет resource mutation/readback, но не
обеспечивает atomic transaction с guest readiness, job cleanup и application output. Existing
systemd/Slurm/backend owners полезны именно потому, что не нужно создавать им параллельных
владельцев. Отказ от отдельного proof framework не означает отказа от их реальных safety guarantees
(R01, R02, R11).

Full-paid/CLOSED state также не является fixed acceptance. Source уже содержит
`_fixed_qualification`, проверяющий actual fixed native configuration, Source, boot/runtime
generation, guest capacity, reserve и Slurm reporting. На PVE этот путь требует actual disabled
balloon и full maximum. Применимость установленной версии не была проверена данным reviewer. Если
current policy/configuration отличается, нужен owning transition с original provenance; стирание
paid journal, подмена digest или открытие admission по предположению недопустимы (R11).

Таким образом, «проверить existing conservative/fixed suitability» было конечной альтернативой
дальнейшему расширению dynamic design. Это не было утверждением, что fixed path уже работает, и не
поручало переключить систему во время аудита.

## 10. Что известно о результате и как оценивать стоимость

Наблюдаемый результат ресурсной части неоднороден: есть опубликованный Source, реальные fixes,
distinguishing tests, genuine local process measurements и independent reviews. Есть также private
proposals, ещё не реализованные ports, неизвестная installed applicability и незавершённый whole
workflow. Перенос всех этих состояний в одну цифру «готовность» скрывал бы практическую границу
прогресса.

Программный аудит отдельно отметил большой рост Source при незавершённом installed end-to-end
результате. Для опубликованного Platform tree он привёл восемнадцать host-resource/native-attempt
файлов суммарно около четырнадцати тысяч строк; это счётчик текста, а не доказательство ненужности
каждой строки. Тот же аудит признал перекос от работающей системы к инфраструктуре её доказательства
и снял прежние субъективные проценты/ETA. Эти выводы — аудит приоритизации координатора, не measured
attribution стоимости каждому модулю и не диагностика дефекта skills (R12).

В ресурсной ветви стоимость расширения видна и без денежных оценок: identity repair привёл к
own-child observer, fast-process race — к отдельной CPython/ELF/startup trust proposal, а девять
predicates — к bootstrap, probe choreography и terminal reader contracts. Каждый локальный шаг имел
объяснимую причину; их совокупность всё дальше отодвигала полезную installed проверку. Именно этот
совокупный trade-off требуется оценивать, а не только число PASS.

**Гипотеза, а не измеренный факт:** более ранняя фиксация fixed lane как первого эксплуатационного
результата могла сократить critical path и раньше обнаружить реальные integration failures. Отчёт не
доказывает, сколько часов или средств было бы сэкономлено; полного сопоставимого activity/cost
accounting нет.

**Сохранённое решение до пользовательского STOP:** dynamic-only implementation, включая Source29 и
MAIN nine-case expansion, отложить; следующим объектом пользы считать actual conservative/fixed
suitability, один свежий малый полный AiiDA lifecycle и coherent installed composition. Полный
scientific run остаётся отдельным опытом с frozen model/criteria и достаточной памятью. После STOP и
эти действия не выполняются: сохранено только их объяснение для будущего решения.

**Предлагаемый урок для последующего анализа:** завершать следующий конкретный эксплуатационный
milestone и заранее называть режим, к которому относится qualification. Source-only safety repair
сохранять вместе с его ограничениями. Если проверка относится только к dynamic feature, не
превращать её молча в prerequisite fixed mode. Эти уроки не являются новым design, новым test plan
или поручением продолжить работу.

## 11. Локаторы свидетельств

Частные hashes ниже идентифицируют evidence packets, а не текущую authority или установленную
готовность. Raw packets могут содержать private operational metadata и не должны автоматически
становиться приложениями public PR.

**R01 — исходный scope.** Root `044cbb420e66078207b77eadd7f54c1324b884b0`,
[project-simplification-2026-10-27.md](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/044cbb420e66078207b77eadd7f54c1324b884b0/docs/implementation/project-simplification-2026-10-27.md),
§§4.3–4.5, 5.1–5.4, 9;
[codex-execution-2026-10-27.md](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/044cbb420e66078207b77eadd7f54c1324b884b0/docs/implementation/codex-execution-2026-10-27.md),
цель и раздельные gates.

**R02 — native operation ownership.** Platform `c47097225a4a798e4124e30245c7b5b2063eb32a`,
[ops/host_resource_qualification.py](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_qualification.py):
`check_baseline`, `CalibrationRepository`, `CalibrationEffectOwner`, `NativeQualificationService`;
[ops/host_resource_qualification_gate.py](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_qualification_gate.py):
`QualificationJobs`, `validate_closure`.

**R03 — genuine negative fixture.** Runner `97ab889ff83b73d9fad5d34e278309b2efe3b299`,
[src/cli.jl](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/97ab889ff83b73d9fad5d34e278309b2efe3b299/src/cli.jl):
`_cli_native_publication_fixture`;
[src/composition/scientific_execution.jl](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/blob/97ab889ff83b73d9fad5d34e278309b2efe3b299/src/composition/scientific_execution.jl):
`_native_publication_fixture_resources`, `_execute_native_publication_fixture`. Platform c470,
[ops/native_attempt.py](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/native_attempt.py):
`_completed_metadata`, `NativeSources.preflight`.

**R04 — dynamic predicates и actual evidence.** Platform c470,
[ops/host_resource_qualification_observations.py](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_qualification_observations.py):
`REQUIRED_CASES`, `capacity_document`, `observed_pressure`, `evaluate_case`,
`qualification_candidate`;
[ops/host_resource_qualification_sources.py](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_qualification_sources.py):
`_validate_reservation_capacity`, `_validate_guest_actual_body`,
`ControllerQualificationView.submit_permit`;
[ops/host_resource_facts.py](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_facts.py):
`calibration_observation`.

**R05 — Source27 repair.** Private
`.build/P20-Root127-task3-actual-sources-implementation-20261103-revision2/REPORT.ru.md`,
`FREEZE.json`; freeze SHA256 `4167c22d8d8aa0360c7badcd651653967cf084bbdfc6019fbd8c948b8f38a3ce`.
Published base Platform `e3861b2c103a67bd33b1f864ee04c4c4404924b9`; revised
`_validate_reservation_capacity` и unchanged independent controls. Его final-source baseline
отдельно сверялся при независимом Source28 review.

**R06 — Source28 implementation/review.** Private
`.build/P20-Root127-task3-process-observer-20261103/FREEZE.json`, SHA256
`4874b73cbcd6c5564a6d47d37c51b0f5605efb9c593bda670c2682b105e0d3a5`; patch SHA256
`90d68b3b746fe94736565d5316c22ed4d98dcf378efe2d5242deebc1c8e75bfe`. Independent
`.build/P20-Root127-Source28-independent-review-20261103/decision.json`, `REVIEW.ru.md`,
`own-checks.json`; review SHA256 `3a473ce144a80dace44a29721f3a3119ebb3b2e1a613aa0b924ce3d204bbc512`.

**R07 — short-command primary.** Private
`.build/P20-Root127-task3-process-observer-20261103/logs/FAST-READONLY-L.json`, SHA256
`a3c7140a499003098996187cb0ae08df06b3407ab4b259617f8f4802d1fb0097`. Independent recount сохранён в
R06 packet. Числа относятся только к local one-shot operands; target scontrol frequency неизвестна.

**R08 — Source29 proposal и defer decision.** Private
`.build/P20-Root127-short-command-witness-design-20261103/CONTRACT.ru.md`, `REPORT.ru.md`,
`REVIEW-CARD.ru.md`, `WHY-NOW-AND-DEFER.ru.md`; `FREEZE.json` называет status design-only/no
implementation и primary design SHA256
`2786bb39a105195eced5d58caf1ec390acbe46b8edaa606b9926f260a21e51a6`. Авторские probes и будущие
controls в packet разделены; новый producer здесь не принят.

**R09 — полный MAIN proposal.** Private
`.build/P20-Root127-main-workload-qualification-design-20261103/DESIGN.ru.md`, SHA256
`54960a193c245cf8b1ef4fbae65baf42d7293774fbaaf4b41d849cf5bfb1564a`; `PLAN.ru.md`, SHA256
`01c31c6f7814040aee3239a494ead82986a424e05365515468b5faf20fa05c30`. Эти документы — предложения, не
implemented/installed API.

**R10 — два independent blockers и necessity review.** Private
`.build/P20-Root127-main-workload-qualification-independent-review-20261103/REVIEW.ru.md`, SHA256
`2ef3981232e839c5fe391226b191ebee25935682b8924137e0e679a2b30cad44`; `decision.json`, `sources.json`.
Решение: return for two finite design revisions; tests/product/infra/native execution не
выполнялись.

**R11 — существующий fixed path.** Platform c470,
[ops/host_resource_facts.py](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_facts.py):
`NativeFactsProvider._fixed_qualification`;
[ops/host_resource_service.py](https://github.com/Afonenko-QCL-NEGF/qcl-negf-platform/blob/c47097225a4a798e4124e30245c7b5b2063eb32a/ops/host_resource_service.py):
выбор fixed/dynamic readback contract. Наличие Source path не доказывает применимость установленной
конфигурации.

**R12 — bounded programme audit.** Private `.build/program-audit-20261103/REPORT.ru.md`, разделы
«Количественный признак чрезмерного расширения», «Полезность по группам», «Динамическая память была
ошибочно поднята в обязательный вход первого trial», «Коррекция исполнения». Его оценки объёма и
приоритетов не являются измерением scientific speedup, оплаченных часов или диагностикой skills.

## 12. Сводка утверждений и решений

| Утверждение                                                                          | Свидетельство                                            | Ограничение                                                                   | Решение                                                 |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------- |
| Host ownership, reserves, grants, actual limits и cleanup обязательны в любом режиме | R01, R02, R04, R11                                       | Full-paid/CLOSED сами не дают body authority                                  | Сохранить safety contract                               |
| Source27 исправил реальные identity joins                                            | R05, unchanged RED→GREEN controls                        | Source/L repair, не Native acceptance                                         | Сохранить исправление и ограничения                     |
| Source28 безопасно связывает собственный child и raw census                          | R06, independent337 tests/573 subtests                   | Synthetic credential views; target runtime не принят                          | Сохранить Source result                                 |
| Source28 пригоден для любой короткой команды                                         | R07: missing live anchor32/32 у быстрого operand         | Actual scontrol rate неизвестна                                               | Не заявлять operational readiness                       |
| Source29 уже реализован и закрывает Task3                                            | R08 прямо design-only; остаются другие gates             | Есть local probes, нет нового production producer/Native pass                 | Сохранить proposal, оставить implementation на паузе    |
| MAIN dynamic design готов без уточнений                                              | R09 и два independent findings R10                       | Terminal C/role read chain и step-consumption race не закрыты                 | Сохранить blockers для будущего анализа                 |
| Полный nine-case framework обязателен до первого fixed trial                         | R01 допускает conservative/fixed fallback                | Сам fixed path требует actual proof; нельзя менять admission по предположению | Не делать dynamic-only scope универсальным prerequisite |
| Fixed fallback уже подтверждён installed evidence                                    | R11 показывает Source route; R10 сохраняет unknown       | Live configuration/transition/readiness этим review не проверены              | Данных недостаточно                                     |
| Весь рост proof infrastructure уже окупился                                          | R12 фиксирует рост Source и незавершённый installed путь | Нет сопоставимого accepted-solution/cost before-after                         | Не выводить пользу из PASS/LOC; сохранить вопрос        |
| Сейчас разрешено продолжить trial или dynamic implementation                         | Прямое пользовательское STOP                             | Отчёт — сохранение свидетельств, не запуск работ                              | Оставить code/infra без изменений                       |

## Уточнение scope CD после исторического разбора4ноября

Отсутствие требования нового самостоятельного scheduler не означает запрета на отдельную service
обновлений. Initial plan `69d841fdd0fa84f835803560faf80bcfd682679c`,
`project-simplification-2026-10-27.md` lines619–624, прямо предусматривает controller systemd
service, durable request/attempt identity, переживание отключения клиента и reconciliation при
restart. Следовательно, само появление delivery service нельзя называть внезапным непорученным
daemon. Предмет оценки — выбранная полнота coordination/proof, стоимость и дублирование native
функций; поздняя maintenance-only правка не отменила автоматически требования durability. Подробная
хронология в[15](15-artifact-delivery-and-cd-history.md).
