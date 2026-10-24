# DOC06: независимая семантическая проверка actual static-source → facts, v2

**Вывод:** существенных семантических несоответствий, блокирующих именно узкий source-only `fixed-slice` со статусом `partial`, не обнаружено. Десять fact classes представлены у обоих subjects. Декларации, текстовые пояснения, явный fixture и неизвестное effective origin разделены. Это не приёмка полного schema validator, Julia dispatch/runtime, научной модели или приложения. Есть два неблокирующих уточнения к представлению отсутствия и locator (ниже).

Проверяющий начал с зафиксированных исходников и полученного output, затем прочитал contract DOC06 и только после первичного сопоставления — фрагменты `ops/docs/static-slice.ts` из указанного Root. Старые reviews и авторские диагнозы не использованы. Код источников не исполнялся; product/guards не перезапускались.

## Идентичность и граница

- Root задания: `c5ef91f4d11a93bd2cdcc9d0b6b18bba0df80ed0`.
- Evidence namespace: `/tmp/qcl-DOC06-ACTUAL-c5ef91f-schemafix-v2`; source — его `snapshot/`, ровно 9 файлов, 245338 B.
- Самостоятельно пересчитаны все 9 SHA-256/bytes; они совпадают с `input-receipt.json` и identity входа в `source-receipt.json`.
- Runner `fefaa27f194bfddf85dd51a0e255beef2218c06d`; Contracts `f4009c933183d8537e289d2fa5fa898defd2d9b5`; Core `9f4a96d032ad868ec010ce92d915bb81087c8d92`.
- `facts.json` A1=A2: 20951 B, SHA-256 `577f43c0653e7394355dda4df58a6e9d299589941c59d7ccbb2395824df2550e`.
- `source-receipt.json` A1=A2: 17056 B, SHA-256 `30e3824f61194d24918fbaea6f8c9802fb40c2bf7cd4f57f4f6d7b690b6ac60e`.
- Обычный cwd сейчас иной: HEAD `e48e5b2ef16d3e6f1d633dd29c95f94d60ca8cc1`, имеются изменённые/неотслеживаемые документы; текущие gitlinks отличаются от selected Root. Их состояние записано read-only и не использовано вместо snapshot.
- Проверка byte hashes здесь подтверждает supplied bytes. Commit→bytes/R1 binding и guards остаются отдельными свидетельствами Root/другого reviewer; совпадение A1/A2 не доказывает смысл.

Обозначения далее: `F0.n` = JSON pointer `/subjects/0/facts/n` в A1 `facts.json` (`configuration_source`); `F1.n` = `/subjects/1/facts/n` (`production.energy_chunk`). Пути source ниже относительны `snapshot/`; commit определяется таблицей owners выше. SourceRef пути корректно убирают только snapshot-prefix (`runner/`, `core/`, `contracts/`). Все их owner/path/SHA соответствуют входным bytes.

## Первичное сопоставление

| Fact locator | Исходник и наблюдение | Оценка смысла |
| --- | --- | --- |
| F0.0–1 | Runner `src/application/configuration_types.jl:208–227`: doc signature и typed header `ResolvedRunConfiguration`, `AbstractString` | Точные декларации; typed inventory честно partial. `:L208` указывает начало docstring delimiter, `:L224` — function header. |
| F0.2–4 | Там же header, без argument defaults | Авторский `not_applicable` для единиц и узкое `not_assigned` только для распознанного header корректны; полный dispatch не обещан. |
| F0.5–6 | Там же `:208–223`, а тело `:228–229` получает history и возвращает `nothing` либо `last(history)` | Docstring воспроизведён; `known` относится к документированному описанию, а не runtime inventory. `errors:partial` не объявляет отсутствие ошибок. |
| F0.7–8 | Lookup provenance, а не численная физическая формула/величина | N/A явно авторское; фактический returned identifier не придуман. |
| F0.9–10 | Docstring `:211–220`; ни run instance, ни его history не входят в 9 входов | Assigning rule частичен; effective origin правильно unknown. Формулировку unavailable history следует уточнить, см. C2. |
| F1.0–2 | Contracts `src/qcl_negf_contracts/schemas/run.schema.json`, `/$defs/production/properties/energy_chunk/{type,description}` (`:1437–1441`); Core `src/numerics/optimized/production_contracts.jl:92` | `integer`, `Int` и owning description точны. Текст описания назван source declaration. Переклассификация ранее обсуждённого units/resource вопроса в этот review не входит. |
| F1.3 | Тот же Contracts leaf содержит `type`, `minimum`, `description` и не содержит `default` | Отсутствие schema default правильно как `not_assigned`; `null` не должен означать literal default. Locator/mode caveat C1. |
| F1.4 | Core `ProductionOptions` `:88–109`, `energy_chunk::Int = 64` на `:92` | Текстовый default 64 верен; не выдан за происхождение значения declarative input. |
| F1.5 | Runner `test/fixtures/configurations/base.yaml:162–163` | Явный illustrative fixture 64 верен; хотя class `default`, текст явно говорит «не default», receipt context — `example-explicit`. Это сохраняет distinction. |
| F1.6–7 | Contracts leaf `type:integer`, `minimum:1`; `/$defs/production/required` содержит energy_chunk (`:1423–1435`); `/required` содержит production (`:15`) | Все три ограничения и root membership верны. `/properties/production/$ref` действительно ведёт к `#/$defs/production` (`:43–45`). Нет подмены requirement constructor default. |
| F1.8 | Contracts `/allOf`: 5 immediate pairs scopes: run→algorithms, run→algorithms, run→run, execution→algorithms, scattering→physical | Footprint точен. Ни один selected pair не накладывает immediate production branch. Предикаты не вычислены; text/status явно partial. Это не полная оценка schema и не доказательство валидности instance. |
| F1.9–11 | Owning description; Core doc `:69–86`; Core guard `:395–413` (energy_chunk positivity на `:399`) | Scheduling interpretation поддержана исходником. Полные effects/errors не заявлены; отсутствие генерируемой физической формулы для scheduling leaf обосновано. Текст честно говорит, что guard/body adapter не интерпретирует. |
| F1.12 | Schema/Core/fixture — три distinct contexts; нет actual instance | `partial`, unknown actual numeric origin корректны. Равенство 64 не объявлено provenance. |
| F1.13 | Runner docs `docs/src/user/configuration.md:17–23`; API body `configuration_types.jl:228–229` | Точная цитата recorded-history rule; никаких load/validation effects самому lookup не приписано. Caveat C2 касается слова «отсутствует». |
| F1.14 | Runner docs `configuration.md:25–29` | Цитата 17→23 и reverse точна; она явно fixture expectation, не наблюдение запуска. Сама linked fixture не входит в 9 source files и здесь не выполнена. |
| F1.15 | Runner docs `configuration.md:72–80`; независимо сопоставлено с `src/application/auto_strategy.jl:39–67,453–523` | `application:auto_exact` добавляется для requested `auto_exact` + production backend; history append избегает duplicate-last marker. Plan supplies typed/raw chunk на `:475,483`. Текст не универсализирует marker на другие paths и не выдаёт marker за full origin/measurement. |
| F1.16 | Ни effective run configuration, ни retained ExecutionPlan instance не поданы | `unknown` корректен. Определения типов/алгоритмов в исходниках не заменяют instance provenance. |

Дополнительная поддержка distinction исходниками, не новый runtime вывод: `configuration.jl:214–237` записывает assigning filename при merge; `configuration_sources.jl` сначала собирает/сливает/валидирует документ и только затем передаёт его на typed resolution; `_parse_production` в `configuration.jl:914–975` требует и явно передаёт energy_chunk. Core positivity guard и Runner `_integer` `configuration.jl:84–98` доступны статически, но отсутствуют как исчерпывающий errors inventory. Их omission допустим при `partial`; факт не утверждает, что эта информация отсутствует в исходниках.

## Неблокирующие замечания

**C1 — absence locator и extraction mode.** В F1.3 `sources[0].selector` равен `/$defs/production/properties/energy_chunk/default`, но такого члена у verified leaf нет. Единственный неразрешимый schema pointer среди фактов — этот. В `source-receipt.json:/extractions/14` при этом стоят `mode:literal-extraction`, `context:schema-default`, `value:null`. Правильное factual содержание — «own default keyword отсутствует», и это уже отражено статусом `not_assigned` и текстом. Однако машинный consumer не должен воспринимать receipt null как извлечённый literal null или требовать разрешения этого selector как существующего JSON value. Рекомендуется сослаться на существующий parent leaf и отдельно обозначить absent key/absence observation; либо явно документировать selector как координату проверки отсутствия. Это замечание о точности source locator/режима, а не обнаруженный default null в schema и не ложное утверждение full validation.

**C2 — unavailable input versus empty actual history.** В F0.9 «фактическая history отсутствует» и F1.13 «actual assigning history отсутствует» допустимо понять как доказанную пустую/отсутствующую provenance конкретного run. Из 9 входов следует более узкое: run history **не предоставлена**. В F0.10/F1.16 origin уже правильно `unknown`; ни один факт не сообщает runtime `nothing`. Рекомендуемая локальная формулировка: «История конкретного run не предоставлена в selected input; её наличие/содержимое неизвестны». Разница существенна для дальнейшего UI: `configuration_source` вернёт `nothing` при действительно пустой history, но unavailable history не является таким наблюдением.

## Полнота узкого среза и modes

Получены 28 facts: 11 API + 17 config. У каждого subject все 10 class names; receipt содержит ровно одну extraction запись на каждый fact. 11 записей помечены `literal-extraction`, 17 — `authored-context`; C1 — конкретное уточнение внутри literal группы. Owner distinction держится на Contracts sourceRefs для declarative schema, Core для typed field/default и Runner для lookup/docs/example. Schema copies совпадают byte-for-byte, но факт о semantic ownership следует из selected owning path, не из этого равенства.

Override example и planner policy действительно взяты из owning docs, и их текст согласуется с selected implementation. Их `authored-context` + `partial` не должен быть представлен как выполненный fixture или наблюдённый plan. Неизвестные error/effects/effective-chain детали явно ограничены. Пропуск полного Julia body interpretation, всех schema predicates и внешних linked fixtures не является критическим пропуском заявленного source-only prototype; он запрещает более сильное обещание API/schema/runtime coverage.

`coverage.status=partial`, `coverage.scope=fixed-slice`, `binding.status=source-prototype`, null application_release/run и receipt `result=partial` согласованы. В output нет claim, что JSON Schema полностью валидирована, что arbitrary instance принят, что runtime dispatch установлен, что scientific acceptance выполнена или что positive/negative controls были здесь заново запущены. Contract DOC06 требует отдельные controls; их reported guards не заменены этим семантическим review.

## Утверждение / свидетельство / ограничение / решение

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Selected declarations верно отражены в facts | Перечисленные F0/F1 pointers и exact source locators; 9 SHA совпали | Не полная Julia/schema семантика | сохранить |
| Schema default не назначен; Core default и fixture — отдельные 64 | Contracts leaf; Core :92; Runner base.yaml :163; F1.3–5 | Receipt mode/absent pointer нуждаются в явном толковании C1 | изменить |
| Lookup показывает последний assigning identifier | Runner API :208–230, merge :214–237; F0.5/F1.13 | Не full causal chain; actual run history не подана | сохранить |
| Отсутствие входного run context позволяет unknown origin | F0.10/F1.16; в inputs только source files | Не доказывает empty history; C2 | изменить |
| Fixed slice покрыт достаточно для bounded partial prototype | Все 10 classes у двух subjects, explicit contexts/modes/limits | Не вся DOC06 controls acceptance и не scientific acceptance | сохранить |
| Полный validator/runtime/error inventory подтверждён | Такого claim в output нет; partial disclaimers | Запуски и полная семантика не проверены | данных недостаточно |
| Равные A1/A2 дают семантическую/научную корректность | Только byte equality/hash | Равенство не независимый oracle | данных недостаточно |

**Disposition:** для указанного exact-output fixed slice — сохранить узкое `partial/source-prototype`; C1/C2 передать как неблокирующие исправления точности. Не расширять вывод до full validation, run provenance или общей научной приёмки. Никаких source edits, CP, runtime/parser/compiler/test/Deno/Julia/science/native/network запусков в этом review не сделано. Разрешённая stdlib обработка ограничилась JSON/bytes/hash/metadata и записью этого отчёта/identity.
