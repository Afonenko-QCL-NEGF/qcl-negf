# Интеграционные отказы, границы тестов и стоимость проверки

Дата среза: 2026-11-03. Статус: **draft для Root/privacy review перед публикацией**. Это
ретроспективный отчёт по сохранённым receipts и Source; при его подготовке не запускались tests,
benchmark, PG, producer или solver. Первичные inputs, идентификаторы узлов, конфигурация хоста и
содержимое научных массивов здесь не публикуются. Evidence IDs T01–T23 ниже связывают выводы с
локальными артефактами и SHA256.

## Что удалось и что остаётся недоказанным

Реальный tiny engineering producer Core/Runner завершил CLI за **305.704с с exit0**. Затем consumers
столкнулись с воспроизводимыми отказами конечного metadata accounting. Results не помещался в
workspace128MiB/retained8MiB; AiiDA selected-access lifetime не помещался в A16 и в единственный
диагностический A32. Это конкретная функциональная блокировка: наличие файлов producer ещё не
означало, что provenance consumer способен принять и опубликовать связанную пару result/binding.
[T01, T03–T07]

Results получил проверенный explicit opt-in160MiB с retained16MiB. Для AiiDA подготовили и
независимо проверили узкое изменение selected lifetime A128MiB и внешнего Source allowance B512MiB.
Независимые43 focused проверки прошли, включая14 дополнительных controls. Это **Source/L одобрение
реализации**, без actual full-route128/512, genuine typed ORM или Native pass. Fresh typed-L driver
сохранили в состоянии **PREPARED, NOT RUN**. [T04–T05, T09, T12–T13]

Полный Results suite в attempt6 завершился с **1604 passed / 49 skipped**. Полный AiiDA package
suite зелёным не объявлялся: broad profile-free проверка имела15 failures, воспроизведённых на
preimplementation baseline. Из этих результатов нельзя выводить сходимость, численную точность,
экспериментальную валидацию или готовность всех service/backend путей. [T10–T12, T19]

Основная польза этой работы — локализация реальных отказов admission и сохранение строгой цепочки
происхождения без ослабления lifecycle. Оптимизация вычислительной физики здесь не доказана.
Стоимость инженерной проверки стала заметной, а полная стоимость недели по времени человека, CPU и
памяти из имеющихся receipts не восстанавливается.

## Source, producer и уровни приёмки

Историческая private coherent composition (не опубликованный Root head) задавалась Root revision
`e37f755c75e1098ae66aca32ef519773d946df34`, Core `01d472141a91c9429f43f7237460a17592d65845` и Runner
`97ab889ff83b73d9fad5d34e278309b2efe3b299`. Базовые published consumer revisions были AiiDA
`336358dfd10c698e4b4a71d8c93562aaa8ee7182` и Results `c50c9ee0cb52a626dfbca0759ce6581c924856e0`.
Фактические consumer overlays фиксировались module SHA и отдельными Source freezes. Published
gitlink и dirty overlay — разные источники; дальнейшая проверка overlay не переименовывает его в
опубликованный commit. [T02, T21, T23]

Producer использовал прежний frozen tiny engineering plan. Receipt T01 подтверждает процесс и время;
сохранённый harness закреплял negative scientific fixture, включая `converged=False`. Ни exit0
producer, ни наличие final declarations не являются научной приёмкой. Здесь различаются четыре
результата:

| Уровень                           | Содержание свидетельства                                                                        | Статус этого среза                                  |
| --------------------------------- | ----------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| Процесс producer                  | CLI завершился, сохранены оригинальные файлы                                                    | Подтверждён receipt                                 |
| Consumer Source/L                 | Конечные allowances, fixtures, refusal/close contracts                                          | Частично подтверждён; scoped implementation одобрен |
| Реальный typed lifecycle / Native | CREATE/readback через текущую composition; установленный actor, privileged boundary и namespace | Full128/512 не выполнялся; Native не подтверждён    |
| Научная приёмка                   | Сходимость, физические тождества, достаточность дискретизации, эксперимент                      | Не следует из этого engineering fixture             |

L scaffolding для parents, Code, job state, privileged close reply и read-only namespace помечался
явно. Он позволял проверять consumers на genuine произведённых metadata, но не доказывал эти внешние
полномочия. У исходного failed consumer attempt не достраивали недостающие outputs, не
переименовывали старые bytes под новую birth identity и не удаляли следы отказа. Fresh route
готовили отдельно. [T06–T07, T13]

## Results: почему128/8 оказалось мало, а160/16 имеет свидетельство

Первый actual metadata context при workspace128MiB отказал **до JSON decode checkpoint
declaration**. Arena имела maximum134217728W, а следующий preflight требовал138263196W. В этом числе
присутствовала фиксированная validation reservation117440512W; размер файла сам по себе не описывал
стоимость validation, копий и удерживаемых объектов. Refusal до materialization сохранял конечный
контракт. [T03]

Диагностическое наблюдение позволило увидеть следующий независимый gate: возвращаемый metadata
context весил примерно11.82млн W и превышал retained8MiB. Diagnostic-only расширение не было
production allowance и не доказывало необходимость512MiB для Results. Конечный accepted выбор был
explicit workspace160MiB/retained16MiB; обычные defaults public API остались128MiB и4MiB. [T03, T05]

Два сохранённых genuine metadata случая после160/16 завершились `CLOSED_SUCCESS`. Для одного arena
high-water был152363624W, retained11825264W и IO988614B; для другого —152359976W, retained11822528W
и IO988310B. В обоих `logical_selected_bytes=0`, reader закрыт. Это свидетельство для конкретных
исходных operands, а не достаточность любого будущего архива. [T04–T05]

Последующий отдельно разрешённый public metadata closure на operand для A/B card занял20.941с:
IO988310B, returned forest11822528W, arena high-water150393896W, selected-array guard calls0.
Значения diagnostics/observations declarations позволили заменить неизвестный detached increment
измеренным810006W. Эти данные закрыли конкретную арифметическую неопределённость Source card; они не
измеряли полный AiiDA pipeline, opaque ORM heap или его deadline. Различие arena high-water между
вызовами также не является ускорением: вызовы имеют разные instrumentation/profile circumstances.
[T08]

Owning symbols для проверки смысла чисел: Results
`src/qcl_negf_results/final_observations.py::describe_native_metadata_context`,
`state.py::_MetadataArena`, `_context_decoding`, `_context_weight`. Для этого среза state module SHA
начинается `a2b8f5e9`, API SHA — `05f011a0`; полные hashes находятся в T05/T23. Guard, validation и
close semantics не заменяли более слабым чтением ради прохождения fixture.

## AiiDA: от A16/A32 refusal к конечной Source card

A обозначает lifetime низкоуровневого selected-access adapter; B — внешний shared nonrefundable
ledger consumer pipeline. Это разные владельцы учёта. B предварительно резервирует работу A и
Results, затем оплачивает собственные parser/proof/copy/output/readback операции. Нельзя смешивать
их remaining или складывать вложенные записи как независимые allocations.

В genuine original A16 attempt перед вторым prepay controls оставалось962607W. Следующая запись
требовала4270784W; remaining стал−3308177W и adapter выдал HOLD. Последующий mandatory close также
не мог быть принят на исчерпанном ledger. При этом B320 имел ещё19819608W после reserve A; наличие
этого остатка не означало, что весь downstream route поместится. Science result/binding/selection не
были успешно опубликованы. [T06]

Единственный private A32 diagnostic на тех же сохранённых operands также отказал: перед series JSON
prepayment оставалось9274735W, требовалось25154560W. Nonrefundable debit до отказа составил не
менее49434257W. Results на этом пути ещё не вызывался. Диагностика заняла5.638с, выполнила один
provider iteration; release завершился, исходные file/row hashes сохранились. Исходный отказ не
превращали в успешную запись и не повторяли возрастающие caps до прохождения. [T07]

Source card затем учла полный parser prefix, Results workspace160MiB, retained context slots16MiB,
binder workspace96MiB, immutable aliases, payloads, копии, mandatory close, output constructors и
readback. Для **одного exact unique context и одного RowKey**, при сохранении всех исходных
occurrences, получились bounds:

| Участок                      | Source upper bound | Что это не доказывает                       |
| ---------------------------- | -----------------: | ------------------------------------------- |
| Selected lifetime A          |          67491741W | Actual A128 route и deadline                |
| Полный process B             |         516954064W | Peak RSS или runtime pass                   |
| Offline catalog B            |         297959080W | Универсальность для больших catalog/lineage |
| Запас B512 над process bound |          19916848W | Запас физической RAM хоста                  |

Независимый reviewer нашёл пропущенный offline declared-point projection debit10672W. Card
исправили, исходную revision сохранили; process bound не изменился. Это пример полезного review:
исправлена существенная арифметика конкретного downstream site, а не только формулировка отчёта.
Вариант с двумя действительно разными contexts учитывался отдельно и не выдавался за тот же
one-context fit. [T09]

Реализация меняла finite internal ceilings и их caller, сохраняя legacy/default16 и public
actor/Root MAX16. Первый actor lookup ограничен `min(MAX_METADATA, remaining//4)`; selected A128 не
становится privileged per-call allowance. Unchanged guards включают method metadata8/IO16,
outerIO256, Results160/slot16, binder96, deadline/file/provider limits, nested shared ledger,
terminal failure, no-refund и обязательный final close. Owning symbols: `native_actor.py::_Reads`,
`native_backend.py::_Operation`, `_Packet`, `open_native_selected_sources`;
`saved_sources.py::_native_operation`, `_NativeLedger.reserve`,
`_load_native_binding_inputs_with_ledger`, `_prepare_native_outputs`, `_native_readback`. [T12, T21]

## Что тесты действительно различили

До owning изменения discriminating набор18tests дал11 ожидаемых failures и7 control passes; после
изменения он стал18/18. Позднее focused public/default guards дали29/29. Независимый reviewer
получил43PASS, включая14 дополнительных controls, и одобрил **exact frozen Source/L only**. Он
отдельно зафиксировал `actual128512_pass=false`, `genuine_typed_ORM_pass=false`,
`native_pass=false`, `scientific_accepted=false`. [T10, T12]

Эти проверки защищают содержательные границы: default/explicit16 clamp, finite128 opt-in,
недопустимые ceilings, отсутствие расширения public Root ports/CLI, terminal failed ledger, nested
tightening, no-refund и отсутствие преждевременных outputs. Они полезнее простого наблюдения «новая
константа равна128», потому что ошибочное расширение actor request или свежий ledger после refusal
должны изменить исход проверки. Но mocks и constructors не заменяют реальный полный lifecycle.

Broad profile-free attempt выбрал733 tests:664passed,15failed,54setup errors;654 tests были
deselected. Дополнительно исключали transitive profile dependencies, поскольку один marker
`not integration` не гарантировал отсутствие ORM/profile effects. Exact dependency-path guard
вызвал54setup errors при byte-identical Contracts, импортированном из другой копии. После
исправления invocation path55 соответствующих tests прошли. Source/Contracts под эти errors не
переписывали. [T10]

15 оставшихся failures —14 из saved_sources и один recovery — воспроизвели на saved
preimplementation package с теми же именами и сообщениями. Это сильное свидетельство, что scoped
allowance delta их не внёс. Однако оно **не делает эти failures допустимыми** и не устанавливает,
ошибочен product или устарела fixture. Полный AiiDA suite остаётся незелёным; legacy validation debt
не закрыт ссылкой на29/43 focused passes. [T11–T12]

## Results full-suite: attempts3/4/5/6

Здесь номера full attempts отличаются от номеров targeted environmental probes. Их смешение создаёт
ложную историю успешных повторов. Original logs и receipts сохранены; последующий GREEN не заменяет
исходный failure.

| Full attempt | Установленный результат                                                | Значение и ограничение                                                                                                        |
| ------------ | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 3            | `INCOMPLETE_LOST_TERMINAL`; exit неизвестен, final summary отсутствует | Partial526pass/10skip из1653 — только прогресс. Причина потери завершения не установлена. [T14]                               |
| 4            | 1597passed,3failed,53skipped; supervisor elapsed1567.103с              | Suite завершён, но не GREEN. Один socket fixture и две intentional Contracts tamper fixtures упали из-за окружения. [T15–T16] |
| 5            | 913passed,43failed,61errors,17skipped; прерван, elapsed387.081с        | Неполная проверка; Root сохранил evidence неправильного fixture parent и корректно прервал invalid environment. [T17]         |
| 6            | 1604passed,49skipped; exit0, elapsed1614.693с                          | Завершённая Results проверка exact frozen Source;49 skips ограничивают coverage. [T19, T23]                                   |

Для attempt4 дешёвые targeted различения подтвердили две причины. Длинный socket path не позволял
создать fixture; короткий path дал pass. Копия Contracts сохраняла read-only mode исходного package,
поэтому intentional tamper падал на PermissionError до проверяемого поведения; writable owned copy
дала pass. Combined три controls также прошли при unchanged product Source. Это работа с валидностью
теста, а не обнаружение научного дефекта. [T16]

Однако сокращение paths через общий temporary parent в attempt5 вступило в конфликт с настоящим
NativeResultGuard: world-writable ancestor не отвечал его ownership contract. Сохранённая
независимая диагностика воспроизвела failure и positive control с trusted parent; это послужило
основанием interruption. Ослаблять production guard ради suite не стали. [T17]

Для окончательной fixture correction chmod owner-write применялся только к собственной regular
copytree destination непосредственно перед intentional mutation. Оригинальные Contracts и их hashes
оставались неизменны; mechanical review одобрил этот узкий delta. В attempt6 production state/API
hashes совпали с предыдущими, а test/docs Source freeze фиксировал поправку. [T18, T20, T23]

JUnit attempt6 объясняет все49 skips:48 — explicit constructor-only producer fixture root не
supplied, ещё1 — требуется explicit original native5 constructor fixture. Это непроверенные
branches, а не49 дополнительных passes. Четыре Runner paired checks, прежде условно отсутствовавшие,
имели отдельный4PASS receipt и вошли в более полную конфигурацию; итоговое число нельзя переносить
на любую среду. [T16, T19]

История показывает цену поздней диагностики окружения: полные4/5/6 вместе заняли около**3568.9с wall
time, или59.5мин**. Это сумма supervisor elapsed трёх разных попыток, включая одну прерванную; она
не включает unknown attempt3, targeted probes, human review и другие работы. CPU-seconds и
совокупный peak RAM кампании из этих elapsed не выводятся. Дешёвые discriminating checks оказались
полезнее ещё одного немедленного full-suite repeat, но только final full run дал свидетельство
полного выбранного Results набора.

## W, IO, RSS и полезность детализации

W — детерминированный консервативный учёт admissions, копий и удерживаемых metadata. Nonrefundable
ledger может несколько раз списывать обработку одних bytes. B512 **не означает512MiB фактически
занятой RAM** и не является обещанием произвольного входа. Results arena high-water — максимум её
accounting model; A debit — накопленный расход; retained forest — вес возвращаемых объектов. Эти
величины нельзя складывать и называть peak memory.

В A32 diagnostic OS high-water составил184832KiB, то есть180.5MiB, для **всего instrumented Python
процесса**, включая imports и observer. Это не A-only resident peak и не память producer. В explicit
forest удалось получить536 snapshots,88 содержали opaque ORM objects; их missing coverage не
заполняли нулём. True resident peak остался неизвестным. [T07]

В Results original metadata calls process RSS high-water был около80.7–80.9MiB, при accounting
high-water около145.3MiB W; returned forest — около11.3MiB W. Такая разница нормальна для разных
моделей и scope, а не доказательство «лишней» выделенной памяти. IO около0.99MB учитывает
фактическое metadata/verification чтение конкретного API. Ноль selected logical bytes не означает
ноль filesystem reads: public metadata reader читает declarations и metadata из HDF. [T04–T05, T08]

Есть измеренная цена metadata closure:20.9–27.2с в отдельных сохранённых вызовах. Она заметна рядом
с producer305.7с, но эти вызовы различались instrumentation и operands; их нельзя складывать в
полную pipeline latency или объявлять7–9% стабильного overhead. Полный здоровый A128/B512 route пока
не измерен. Причина latency — JSON validation, HDF metadata, imports, provider/ORM либо другая часть
— по этим receipts не разделена.

Детализация была продуктивна, когда открывала новый различающий факт: predecode refusal, retained
overflow, actor envelope leak risk, omitted offline debit, invalid fixture environment, incomplete
suite receipt. Её польза падает, когда повторный список charge sites лишь пересказывает уже принятую
card. Работа дала функциональные contracts и обнаружила gaps; она ещё не доказала пользовательский
выигрыш полного выбранного pipeline. Это ограничивает положительную оценку недельного прогресса.

## Незавершённый driver и вопросы независимому анализу

Fresh driver закрепляет новые birth/UUID, прежний frozen plan и отдельно pinned consumer overlays.
Он предусматривает один tight-cap terminal negative, late-close failure до science outputs,
настоящий process parse/update/readback и отдельные offline point/catalog обращения.
Parent/Code/job/privileged close/namespace остаются L stubs. Supervisor configuration имеет
`execute=false`, attempt отсутствует. Подготовительные AST/pin/copy checks — свидетельство
reviewable подготовки, не исполнения. Никакого нового runtime поручения этот отчёт не создаёт. [T13,
T22]

Будущему независимому разбору полезны следующие вопросы; перечисленные материалы уже сохранены,
новые benchmark или implementation здесь не предлагаются:

- **Какую пользовательскую возможность восстановило изменение?** Сопоставить original refusal
  T06/T07 с Source changes T21 и явно отсутствующим full-route result T12/T13. Сейчас доказаны
  причина блокировки и конечная реализация; завершённый typed acceptance остаётся gap.
- **Насколько allowance соответствует объёму полезной работы?** Разделить fixed Results/binder
  reservations, A lifetime и повторные copy/readback debits в T06/T09. Число512 само по себе не
  отвечает ни на вопрос RSS, ни на вопрос latency.
- **Где тест находил product defect, а где проверял не то окружение?** Сопоставить первый traceback
  с targeted counterexample T16/T18 и unchanged module hashes T23. Это дешевле и содержательнее
  подсчёта общего числа запусков.
- **Что означают оставшиеся15 failures и49 skips?** T11 позволяет отделить regression attribution от
  legacy correctness; T19 уже даёт точные skip reasons. Для оценки общей готовности недостаточно
  focused43PASS.
- **Не превращены ли Source или L evidence в Native/scientific verdict?** Проверить scope полей
  T05/T09/T12/T13. Ни один из этих packets не даёт требуемых физических критериев, а prepared driver
  не создаёт нового доказательства.
- **Можно ли оценить стоимость недели?** Есть несколько wall/RSS/IO observations, но нет полного
  campaign accounting и human effort ledger. Приписывать всю работу одной цене или делать вывод об
  экономической эффективности — данных недостаточно.

## Решения по имеющимся свидетельствам

| Утверждение                                                         | Свидетельство                                        | Ограничение                                   | Решение               |
| ------------------------------------------------------------------- | ---------------------------------------------------- | --------------------------------------------- | --------------------- |
| Genuine producer работал, consumers блокировались                   | T01, T03, T06–T07                                    | Tiny engineering fixture, без научной приёмки | сохранить             |
| Explicit Results160/16 принимает эти metadata и закрывает reader    | T04–T05, T08                                         | Defaults128/4; не произвольный архив          | сохранить             |
| Scoped A128/B512 имеет конечную проверенную Source реализацию       | T09–T12, T21                                         | Actual full route не выполнен                 | сохранить             |
| Все тесты всех компонентов GREEN                                    | T10–T12, T19                                         | AiiDA15 failures, Results49 skips             | данных недостаточно   |
| Environmental failures объяснены без ослабления guards              | T15–T20                                              | Не объясняют всякий иной failure              | сохранить             |
| 512MiB — реальное RAM потребление                                   | T07–T09                                              | W, RSS и IO имеют разные scope                | изменить формулировку |
| Полезность новой детализации подтверждена сама числом packets/tests | Сохранённые receipts различают реальные отказы и шум | Нет полной стоимости недели                   | данных недостаточно   |
| Fresh typed chain или Native уже проверены                          | T12–T13, T22                                         | PREPARED NOT RUN                              | данных недостаточно   |

## Реестр источников

Ниже `source` — локатор сохранённого первичного receipt или Source freeze относительно корня
repository, затем SHA256 файла. Каталоги с inputs/arrays не являются приложением к публикации.
Полные receipts могут содержать непубличные operational поля; отчёт переносит только приведённые
выше агрегаты. Проверка hashes устанавливает точность локатора, а не научную истинность содержимого.

Префиксы локаторов (каждый раскрывается относительно корня repository):

- `P` =
  `.build/P04-P05-Root127-AiiDA-actual-final-allowance-20261103/interop/actual-capture-attempt1`
- `G` = `.build/Root-actual-stationary-consumer-composition-20261103`
- `R` = `.build/P04-P05-Root127-actual-final-Results-arena-20261103`
- `RI` = `.build/P04-P05-Root127-actual-final-Results-arena-independent-review-20261103`
- `A` = `.build/P07-Root127-selected-access-actual-lifetime-measurement-20261103`
- `C` = `.build/P07-Root127-selected-access-allowance-card-20261103`
- `CI` = `.build/P07-Root127-selected-access-allowance-card-independent-review-20261103`
- `I` = `.build/P07-Root127-selected-access-scoped-allowance-implementation-20261103`
- `II` = `.build/P07-Root127-selected-access-scoped-allowance-independent-review-20261103`
- `D` = `.build/P07-Root127-A128-B512-fresh-typed-chain-20261103`
- `E` = `.build/P07-Root127-Results-fullsuite-environment-20261103`
- `F4` = `.build/P04-P05-Root127-Results-full-durable-20261103-attempt4`
- `F5` = `.build/P04-P05-Root127-Results-full-durable-20261103-attempt5`
- `F6` = `.build/P04-P05-Root127-Results-full-durable-20261103-attempt6`
- `RF` = `.build/P07-Root127-Results-fixture-Root-integration-20261103`

| Evidence ID | source                                                 | SHA256                                                             |
| ----------- | ------------------------------------------------------ | ------------------------------------------------------------------ |
| T01         | `P/producer-receipt.json`                              | `01a727c843e18c4a8196cd9335c0f492529cb37e3b2956735a1a54fd4fc1552d` |
| T01 (прод.) | `P/harness.py`                                         | `f6286b7741ad2cdbb6a9e8a9ba792d606953963ac0fca4674faa7fce44da41a7` |
| T02         | `G/graph.stdout`                                       | `5040fb9275a9d8c4bac8963972dd6972249f7726931c1dd8db9ee1676784d0d6` |
| T03         | `R/red-actual-final-attempt1.json`                     | `dc81e5abc71749699c68d63ab127e0535dc329d647118c1296f61350dd636a85` |
| T03 (прод.) | `R/diagnostic512-exact-debits-attempt1.json`           | `e790531c95ae340b507bfaa4fa9e938e55f7f0717e955445c74ea5588750210d` |
| T04         | `R/green-native-orm-final-attempt1.json`               | `a11dd4dbbf325db30c7615c36f5764c6d7114160914b46cf0b33e7663d0640c3` |
| T04 (прод.) | `R/green-actual-final-attempt1.json`                   | `36535636b0862f19fb724418eb3cd17c0e85dd7236c5d6d3f45306268ab0f5b5` |
| T05         | `RI/verification.json`                                 | `f06c3b4501eeb019990840efc0852dc0cc93fed54c669c1cf707a95e3a992e00` |
| T06         | `P/accounting.json`                                    | `80164f64bf04988cbefffeddfede54cc4c7d36684c3d15a8b261bf7dc6c1ef89` |
| T06 (прод.) | `P/failure.txt`                                        | `e25ae7b9cd6cdf06e6bc01f425a503f1ec48fd63b6a975442ebc1cfad8cb70f6` |
| T07         | `A/analysis.json`                                      | `12dd1de00c8e54984e53c8c48c975b79f44b86681c6ba33097465b17be4a74c9` |
| T07 (прод.) | `A/report.json`                                        | `d7390b664d7111dd1cfb63e9376ae083b904b4ea7381644f10cdc337bacebd70` |
| T08         | `C/detached-metadata-weights.json`                     | `fc1411f6b967798d8b2773116f9e1386b045d0fe8e4d052f535718b41e3f8e63` |
| T09         | `CI/decision.json`                                     | `50d395edf55e9f4674734ce293c1b587b99fc14994ce8c83b3a752cbff6699d7` |
| T10         | `I/test-counts.json`                                   | `d7829b84680c933bad6f81b1dd7de4818da64ef36c623fb1c77b209c3c9836ae` |
| T10 (прод.) | `I/REPORT.ru.md`                                       | `4fec3ca4fd47c335d4d2fe60d642ff4e2484807b05fa955f41b8936420130879` |
| T11         | `I/legacy-failure-comparison.json`                     | `52ffbf9b8a6934a0593ecc11154d8c03de1cf7912adc01a44b6002891c516b30` |
| T12         | `II/decision.json`                                     | `3d5d2d9689b1572b94f88eac9020f5686144cfd273531c555e5e23dbce93c4e4` |
| T13         | `D/manifest.json`                                      | `4464844ecb2607c6ef9d506de28d0d4cf38c939de73da35360f7970b7daf82bd` |
| T14         | `R/reconciliation.json`                                | `e4cd9acd47112079f5fc4e8b15db0e1a9b0c0ef6065f9ed77d46e469ff28e343` |
| T15         | `F4/receipt.json`                                      | `6d92b49c09238f697a2ca1133a5a43dfc132498723feb8e82231f59bba1833d2` |
| T15 (прод.) | `F4/stdout`                                            | `12a932ca0f67afd3c658c20debfe0c62a538de59c2996e30716328df36f2031e` |
| T16         | `E/attempt1/receipt.json`                              | `5687bc6cb4d91d9b69813ee7ecfeb6f5af5e79a3f5e2cfa7d7db3930bd8a318b` |
| T16 (прод.) | `E/attempt2/receipt.json`                              | `d7e468feab93e0f7a049ab9abef6c1fb38d2055d22eaba5d2ae9f1104d7a6eea` |
| T17         | `F5/receipt.json`                                      | `4682bc46174833ba1a50a7cdd728bd473a9c95206251a2738828e87ad30c7944` |
| T17 (прод.) | `F5/stdout`                                            | `13c35e3f5b7c51f52fe3e64601bbb6596bc2b611c34f0947dda95cebaf72cc65` |
| T17 (прод.) | `F5/interrupt-authorized-on-environment-evidence.json` | `f825a3cb0bcdbcf20780fefe91a23acfa60ce9365ba38b155867fcb0f6971acb` |
| T18         | `E/attempt5/receipt.json`                              | `64c7790286e5a796e9315dde2652ac5e1f583b7ff52a1aaef28bb8ce9d614a9b` |
| T19         | `F6/receipt.json`                                      | `7fe4a48e5a829db185edbac48b29a171d4d292868dafca06f22c8825e406ac86` |
| T19 (прод.) | `F6/tests.xml`                                         | `d929b1eaa88df7d58b49b951c8c836ba4c3cf8732f64370932482528a25f628d` |
| T19 (прод.) | `F6/stdout`                                            | `d8c1d54da8ee5c709a26402c5211d9f02ed70bb80bbd0ae0db7dca7d40c1dea0` |
| T20         | `RF/review.json`                                       | `cfae3c7349c4a5ecc208cfd0ae77a39bb1d99e11e226833131fbf4e69fdb9c8e` |
| T21         | `I/source-freeze.json`                                 | `061dd7cf4c6fd053f11328ad942d07660dbcad33e68ac465961a68585a7f5bf4` |
| T22         | `D/preparation-checks.json`                            | `184986a84a0c2ebfd623139d16976b78b4546fd3f181334eb6b91220403c17b5` |
| T22 (прод.) | `D/README.ru.md`                                       | `2ab1f5cea34b8fb967b4866d100e8dfc39ab199409a0272c1b463efaa049c9a3` |
| T23         | `RF/source-freeze.json`                                | `bf139af6127dbb2553619cb492e16437b208ac1d37df8262a9a51b7fd540aa7b` |

Проверка самого draft: operational UUID, абсолютные host paths, LAN/PG configuration и array values
в текст не перенесены. Окончательное разрешение публикации и privacy review принадлежат Root; этот
draft не является PR или issue.
