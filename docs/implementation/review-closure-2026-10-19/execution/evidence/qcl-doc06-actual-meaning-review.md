# DOC06 actual-source meaning/coverage: независимый high review

2026-10-20. Verdict: **REQUEST_CHANGES_FOR_FULL_DOC06_FIXED_SLICE**.
Отдельно принимается **REPRODUCIBLE_PARTIAL_SOURCE_ENGINEERING_EVIDENCE**:
selected sources связаны с export, обе завершённые projection дали одинаковые
bytes, provenance/default/example/actual-origin границы в основном сохранены.
Полная semantic/coverage приёмка accepted fixed slice пока не установлена.

Первичный вопрос: точно ли facts выражают selected API/config semantics, все
десять классов, честные status/mode и различие schema/typed/example/actual origin?
Первичные owning sources изучены до comparison summary; равенство output не
использовано как аргумент их смысла.

## Identity, источники и наблюдённое выполнение

Selected Root HEAD по readback:
`2bb05d3651af4509fe7f02c1253b40f1e5146fec`; adapter SHA256
`3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b`
совпадает с reviewed source. `git status --short` сохраняет coordinator dirty/
untracked evidence; это не clean/full release. Восемь submodules совпадают
с selected gitlinks без `+`/`-`. Frozen snapshot authority — committed graph,
не эти working files. Governing design `34b80d4a…fb2e8`, §4–7, в частности
строки182–185 и237 требуют known schema type/direct minimum+required,
schema default-absent и separate typed/example64, с partial для непокрытых
добавочных условий, а не исчезновения прямых деклараций.

Exact nine-source snapshot aggregate245338B. Все девять raw SHA256 независимо
пересчитаны и совпали с input receipt, preparation, R1 readback, A1/A2 receipts
и output source receipt:

| Alias path | Commit owner | Bytes | Raw SHA256 |
| --- | --- | --- | --- |
| runner/src/application/configuration_types.jl | Runner fefaa27f194bfddf85dd51a0e255beef2218c06d | 8663 | 6851ee3d8827912e4542b881ec7014460e5a0f5c83fc4f322b97e1dfce9518f0 |
| runner/src/infrastructure/config/configuration.jl | тот же Runner | 71428 | b07516d1fa1b9f7918efd4fa9096327be45af5ea32233ba15a9e88bf225daebb |
| runner/src/infrastructure/config/configuration_sources.jl | тот же Runner | 3381 | bb08a718dd765a15db2a4fba7de0ff2ea79753f29dc516900f67485331dafbb1 |
| runner/src/application/auto_strategy.jl | тот же Runner | 19019 | 810c72af8e4289c3dd61d4f49549a083568472646fa69eb625f41c5702840326 |
| runner/docs/src/user/configuration.md | тот же Runner | 10648 | 5f1fb2243240a957a1d765af0b8dee4f44a7e105dcea35889c725843bacf4cbf |
| runner/test/fixtures/configurations/base.yaml | тот же Runner | 6973 | 735c0077cc7c64c901829a5a86bd5bab6c9b78e473d469e3240062aa7bc810b2 |
| runner/schema/run.schema.json | тот же Runner | 54815 | 62df4ac2758b40cb78da2f9c5e12e8f8b647d980102f505dfe94bee40fc0e58b |
| contracts/src/qcl_negf_contracts/schemas/run.schema.json | Contracts f4009c933183d8537e289d2fa5fa898defd2d9b5 | 54815 | 62df4ac2758b40cb78da2f9c5e12e8f8b647d980102f505dfe94bee40fc0e58b |
| core/src/numerics/optimized/production_contracts.jl | Core 9f4a96d032ad868ec010ce92d915bb81087c8d92 | 15596 | ebb614494b4e58477231dbaf25a5283e8867e1c612859b2e26690c167b61a019 |

Graph SHA `b7244ee91167b688e598efea33ba9620772c974264920d7e368ec87de4d939e1`;
input receipt SHA `971fc29af70d409e64b37f2e331b03596e92736a2e3a993bad22e9d802bffd1a`;
preparation SHA `03db672d25120747f86469e37a1685f6dfff8bed64199b6a619b5296b8adf5b8`.
Root R1 readback и A1.before=A1.after=A2.before=A2.after содержат эти identities,
все file records и aggregate. Это закрывает требовавшиеся в предыдущем source
review R1/R2 внешние сверки для данных attempts; ограничение самого launcher
не исчезло и не переписывается задним числом.

Существующие A1/A2 receipts содержат complete_partial_projection, exit0,
raw_capture_complete=true, stop_reason/guard/capture_error=null. Wall0.520728/
0.536580s, sampled RSS69402624/71933952B, sampled regular TMP423473B каждый;
prelaunch/loop/terminal/final observations присутствуют. Это инженерные sampled
наблюдения, не hard-quota/transient/native/scientific proof. Original logs26B
каждый содержат только JSON status=partial; SHA обоих
`ff602a8401c76f68f448a0ae58b37281211b6ed20427e1cdbf0603207c92b301`.

Независимые sha256sum и cmp подтвердили полное равенство A1/A2:

| Output | Bytes | SHA256 |
| --- | --- | --- |
| facts.json | 19556 | ead7c19658478682d9da3b966f5aaec2e0ec9a180a27b7c62442f5796b63e041 |
| source-receipt.json | 15444 | 7bd0d68220ec0d37972b2cb25ad20b5f3b99078f95e06f64327727b446f7bd92 |

A1 receipt SHA `d525dd33a202c17436e85280187d692ff4297da7ab3c11ff96ed96a854fbd19f`;
A2 receipt SHA `6af221c17e590bc24352a016cec9da71204adf8720c76dd3a9dc1bb0710a0755`.
Comparison SHA `28029ded29e20b1d08198604b09729e5ddfc43536f4472bc47e74cecea498fc3`.
Этот review не создавал calls: actual2/2 исчерпаны; unit2/2 и separate E1 1/1
не переоткрываются. Оригинальные raw/facts/receipts следует сохранить как
положительное engineering и отрицательное coverage evidence.

## Findings, блокирующие полную fixed-slice приёмку

### M1 — реальные schema facts не извлечены из-за root allOf

Primary locator: selected Contracts schema (raw SHA62df4ac2…e58b)
`:179–423` содержит root `allOf`, тогда как `Root@2bb05d3:
ops/docs/static-slice.ts:518–550` не включает его в objectKeys и вызывает
unsupported_schema_keyword до `rootRequired` и локального `$ref` traversal.
Тот же schema raw hash существовал в accepted D; это не новая физическая модель
или случайное изменение исходников между A1/A2.

Reproduction без запуска: A1/A2 `owned-tmp/out/facts.json`, subject
production.energy_chunk, fact indices0/3/6/7 содержат соответственно
schema-type/schema-default/schema-constraint/root-required как partial;
source-receipt `extractions` indices для этого subject с fact_index0/3/6 дают
null+unsupported_schema_keyword, fact_index7 — null+unsupported_syntax.
В facts это строки139–150,181–192,223–248; в source receipt строки189–197,
215–223,240–257. Required root fact ещё и указывает selector leaf вместо
`/required`; фактический failure root `/allOf` в diagnostic не локализован.

Непосредственно присутствуют и проверены текстом:

- root required включает production (`schema:8–20`, точнее15);
- `/properties/production/$ref` = `#/$defs/production` (`:41–43`);
- `/$defs/production/required` включает energy_chunk (`:1423–1435`);
- leaf type=integer, minimum=1, description literal и отсутствие default
  (`:1437–1441`), с pointer исправленным accepted erratum;
- owning route`:82–87` повторяет отсутствие schema default и count meaning.

Непокрытые composition conditions оправдывают partial **полноты validation**,
но accepted positive slice ожидает эти прямые source declarations. Сейчас all10
class names присутствуют, а требуемое schema содержание отсутствует. Это честное
refusal-like degradation, но не PASS полного fixed-slice positive gate.

Самое дешёвое source исправление — отделить literal declaration projection и
её source selectors от утверждения о полноте условий schema. Сохранить explicit
partial/unsupported diagnostic для root composition и не применять schema к
instance. Для данного fixed profile можно отдельно проверить reviewed root
allOf region: его conditions/consequents касаются run, algorithms, execution,
scattering/physical, а не production; это наблюдение из`:179–423`, не общий
JSON Schema oracle. Нельзя просто добавить allOf в ignored allowlist и объявить
все схемы validated. Новые execution checks требуют отдельного finite grant;
этот review такой grant не даёт.

### M2 — отказ извлечения ошибочно назван отсутствием source description

Primary locators: A1/A2 facts production.energy_chunk.fact[2], строка169:
«Owning description отсутствует». Однако exact schema leaf`:1440` содержит
полное описание positive integer maximum number of energy points per chunk,
work scheduling, no schema default, separate Core default и no energy spacing.
Output source receipt fact_index2 указывает `reason=unsupported_schema_keyword`,
а не description_absent. Причина source failure подменена утверждением о данных.
Root adapter`:880–889` использует одну absent формулировку для любого reason.

Связанное противоречие: facts.fact[8] effects, строка253, говорит «Owning
description приведено отдельно», но units fact description не приводит.
Root adapter`:932–940` печатает эту фразу независимо от успешного extraction.
Статус unknown полезен, но не исправляет ложные утвердительные предложения.

Самое дешёвое исправление: reason-aware text «описание не извлечено
(unsupported_schema_keyword)», отдельно от настоящего description_absent,
и условное обещание quoted description только при наличии цитаты. M1 может
восстановить literal description здесь; failure branch всё равно нуждается
в честном различении absence и unsupported.

### M3 — небольшая несогласованность mode/source в formula_origin

Facts leaf.fact[10] not_applicable и текст «Авторский контекст» по смыслу
поддерживаются owning route`:67` и schema`:1440`. Но output receipt fact_index10
(`:275–283`) помечен dynamic-unknown с null+unsupported_schema_keyword и ссылается
на неизвлечённый schema description. Root adapter`:950–958` не передаёт явный
authored-context mode, поэтому reason description меняет mode автоматически.
Это не ложная физическая формула, но режим доказательства не соответствует тексту.
Дешёвое исправление — явный authored-context с exact owning-route selector
для этого вывода либо согласованный unknown text/status при отсутствии evidence.
Не блокирует отдельно M1/M2, но нужно исправить в том же ограниченном source patch.

## Что meaning review подтверждает

API facts subject configuration_source имеет11 rows и все10 имён. Known только
documented signature/effects, typed header partial; аргументные defaults
not_assigned, errors/dispatch/history полнота partial, effective origin unknown.
Selected `configuration_types.jl:208–230` подтверждает docstring и literal
implementation: get(history), absent/empty→nothing, иначе last(history).
Lookup не загружает source, не валидирует и не назначает defaults. Он не
обещает восстановить причинную цепь или runtime method inventory.
Authored units/formula/value-origin not_applicable для такого identifier разумны.

Leaf имеет16 rows, все10 имён. Core typed default64 и fixture explicit64
действительно разные literal-extraction contexts (`Core:88–109`, fixture`:162–163`).
Schema default не выведен из64; status partial честно сообщает failure, хотя
для positive slice должен быть восстановлен как not_assigned по direct source.
No actual value64/17/23 или default origin выдуман: assigning origin partial,
effective origin unknown, application_release/run=null и coverage partial.

Quoted17/23 override example точно совпадает с owning route`:25–29`, помечен
synthetic authored-context и не предъявлен как произведённый merge/run.
`configuration.jl:_deep_merge!:214–238` действительно заменяет leaves по порядку
и записывает abspath(source_file). `configuration_sources.jl:39–52` последовательно
merges files, затем validate; `configuration.jl:914–975` требует explicit chunk
и передаёт его в ProductionOptions, а не присваивает schema default.

Quoted planner paragraph route`:72–80` соответствует selected
`auto_strategy.jl:_execution_plan_provenance:39–67`: marker добавляется для
auto_exact+production; `:453–488` использует plan.energy_chunk и обновляет raw.
Marker не становится hardware measurement или полным effective origin.
Core `_check_production_options:395–413` требует chunk>0; output честно не выдаёт
это за полный error inventory. Scheduling, а не energy-grid spacing/model
parameter, также подтверждено Core docstring`:72–82` и auto_strategy`:430–434`.

Public structured refs содержат selected full revisions, repo-relative owner
paths, правильные raw hashes и локаторы. Части с direct text имеют точные
строчные selectors; exceptions M1 rootRequired и M3 описаны выше. Копированные
authored paragraphs содержат публичные historical GitHub links и @ref markup;
их содержание принято только как literal owning-doc quotation, не как
проверенные внешние ссылки или render result. Absolute private assigning paths,
credentials, run identity или actual history в facts не наблюдаются.

## Граница приёмки и действия reviewer

Приняты export/readback source identity, existing complete raw capture,
воспроизводимость обоих bounded output artifacts, API semantics и корректное
разделение default/example/actual origin. Полный DOC06 fixed slice нельзя
закрыть одним all10 presence, exit0 или identical SHA при M1/M2. DOC03 shared
Fragment/Bundle/schema compatibility, documentation rendering/link validation,
native target behavior, scientific convergence/physics/discretization/experiment
этим packet не принимаются.

Этот review выполнил только inert source/metadata reads, sha256sum/cmp,
Git readback и запись собственных report/identity. Не запускал target, exporter,
harness, parser, tests, Deno/native/network/SCI; не менял source/product/CP/Git
или original artifacts. Девять файлов целиком прочитаны для raw hashing;
semantic reading — необходимые docstring/merge/loader/planner/schema/fixture
regions, не весь scientific solver. Conservative logical source read upper
bound1.5MiB≤2MiB; wall<10min; CPU/RSS/physical I/O reviewer не измерялись.
Report<96KiB. Подагенты не использованы. Root сохраняет durable raw backup.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Exact actual sources и A1/A2 outputs связаны и воспроизводимы |9raw SHA, R1/R2 records, receipts, cmp/full output SHA |Только эти source/profile bytes и два attempts |сохранить |
| API lookup и происхождение defaults/examples выражены верно |Owning types:208–230, Core:92, fixture:163, route:17–29/72–87 |Нет target runtime method/call evidence |сохранить |
| Все10 классов означают выполненную fixed-slice coverage |Формально11+16rows; schema rows null+unsupported при реальных declarations |M1 нарушает positive schema-content requirement |изменить |
| Owning description отсутствует |Facts:169 против schema:1440 и receipt reason |Failure extraction не равен absent data |изменить |
| Formula-origin mode согласован |Facts not_applicable/authored против receipt dynamic-unknown |M3 provenance-mode mismatch |изменить |
| DOC03/render/native/science acceptance установлена |Таких gates/evidence нет |Source prototype и partial engineering output |данных недостаточно |

STOP: report/identity только. Actual budget2/2 exhausted; source patch и новые
checks не выполнены и этим review не разрешаются.
