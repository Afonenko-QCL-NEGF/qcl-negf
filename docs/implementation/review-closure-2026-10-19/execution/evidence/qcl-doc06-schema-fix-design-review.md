# DOC06 M1/M2/M3 correction: независимый high D review

2026-10-20. Verdict: **PASS_READY_FOR_I_SOURCE_ONLY**.
Блокирующих замечаний к этому узкому design не найдено. Это готовность к
отдельно порученному I; не приёмка ещё не написанного кода, не разрешение новых
product calls и не semantic/runtime/native/scientific acceptance.

Reviewed design `/tmp/qcl-doc06-schema-fix-design.md` SHA256
`3a655b213799ce5ead32a1acec7aa0f05cd1effb8d2750e76fb10d271fac818b`,16698B;
identity SHA `31e0e2b6cadab37eeb29439380d35ad389247f4ab37e34c4d7fcf05ee29e4eb0`;
readledger SHA `4240320979b74a770f8c25cfb36624dcbcd786741d17decc95d4d6e3fffca254`.
Exact selected Root HEAD `2bb05d3651af4509fe7f02c1253b40f1e5146fec` подтверждён;
adapter SHA `3dde28ca8ab371ba55948ea0b47518d05e4eea6e715c15c310b0678c1538594b`,
canonical tests SHA `e825f6e1e849df0f8c2f6f2453c92f2cf4b39135d76008fb2b78ae557af9be69`
совпали. Git status сохраняет coordinator modified JSON; submodule status
все8 без `+`/`-`. Source edits этим review не выполнялись.

## Первичные проверки

Exact snapshot Contracts schema SHA
`62df4ac2758b40cb78da2f9c5e12e8f8b647d980102f505dfe94bee40fc0e58b`
пересчитан. Region179–423 перечитан: пять root allOf items имеют только if/then;
clauses содержат только properties. Footprints действительно:

| Item | if immediate root property | then immediate root property |
| --- | --- | --- |
| /allOf/0 | run | algorithms |
| /allOf/1 | run | algorithms |
| /allOf/2 | run | run |
| /allOf/3 | execution | algorithms |
| /allOf/4 | scattering | physical |

Ни один footprint не содержит production. Nested if/then (`:224–244`), anyOf
(`:275–339`) находятся под algorithms; refs energyQuantity/volumeQuantity
(`:412–416`) под physical. Они применяют свои schemas к значениям соответствующих
других свойств. Design не выводит из их наличия валидность run и не исполняет
предикаты. Source observations достаточны для узкой классификации области,
но не являются generic JSON Schema evaluator.

Direct production source declarations перечитаны`:1420–1441`: required включает
energy_chunk, leaf integer/minimum1/description и не содержит own default.
Исправление не требует менять schema, physical model, grid, tolerance или loader.
Existing adapter schemaProjection`:497–627` и output branches`:850–958`
подтверждают исходные причины M1/M2/M3. Canonical tests прочитаны по relevant
regions: positive separation/shape/all10, malformed/duplicate/ref/leaf combinator,
escaping pointer, mismatch/default, hop caps и inert-source controls сохраняются.

## Оценка correction contract

**M1.** Две фазы отделяют literal root `/required` от selected-context failure.
Это предотвращает нынешний invented leaf selector для root membership.
Selected schema facts публикуются только после narrow classifier; отдельная
constraint row с partial/authored-context сообщает неполноту conditional/full
validation. Source direct declaration known не становится instance validation.
Schema default-absent ограничен own keyword в recognized leaf; это не claim
про runtime default assignment, effective value или происхождение64.

Предложенный accepted grammar достаточно узок: nonempty allOf array;
ordinary item ровно if+then; ordinary clause ровно properties; nonempty own-key
property dictionary, все immediate names отличаются от production. Неизвестная
ветвь не замалчивается и не становится unrelated автоматически. Root allOf
нельзя просто добавить в generic ignored allowlist. Root anyOf/oneOf/if/not,
item ref/boolean, clause required/additionalProperties/not/ref или else не
проходят эту grammar. Production в if или then также отклоняет selected context.
Предписанный deterministic offending JSON Pointer и reason позволяют отделить
реальную неподдержанную область от отсутствующего leaf.

Значения под unrelated immediate root properties намеренно opaque. Это безопасно
для заявленного source projection: design не интерпретирует nested refs или
combinators, не говорит, что whole schema корректна, и не валидирует configuration.
Если будущая реализация начнёт разрешать nested ссылки ради вывода об общей
валидности или selected default, это выйдет за данный design и не будет покрыто
этим PASS. На selected production/ref/leaf пути старые sibling/ref/cycle/hop/
combinator guards остаются fail closed, как прямо требует design.

Combined constraint получает свидетельство leaf и production required либо
отдельную literal membership row. Это исправляет нынешний locator, где один leaf
pointer использован как единственная опора required. Unknown composition не
стирает independently read rootRequired или независимые Core/example/API facts.

**M2.** Branch по description_absent отделён от source_missing/unsupported/
malformed failure. Это устраняет ложное утверждение «description отсутствует».
Обещание quoted description и authored scheduling sentence теперь допускаются
только после успешного literal extraction; failure получает unknown и не
подтверждает отсутствующую цитату. Это сильнее исправления одного текста на
конкретном actual fixture, поскольку сохраняет честность failure branches.

**M3.** Условная пара description success→not_applicable/authored-context и
failure→unknown/dynamic-unknown согласовывает status, text и provenance mode.
Exact description selector поддерживает authored interpretation; это не
literal physical equation extraction. Отказ от нового route parser и скрытого
fallback сохраняет fixed scope и простую проверяемость.

Публичный API generateStaticSlice, Fact `{name,status,text,sources}` и extraction
shape не расширяются. Partial coverage/application_release=null/run=null,
all10 names, typed/example distinction, source bytes/hash/symlink protections,
caps, fresh output, no target evaluation и scoped permissions остаются.

## Source-review gates для I

Это не дополнительные этапы или product calls: следующие assertions входят
в уже предусмотренные design controls и независимый source review.

1. Отрицательная пара должна закрывать **обе** стороны selected footprint:
   production в if.properties и production в then.properties. Exact item keys
   исключают else; отдельный fixture с else полезен, чтобы implementation
   случайно не проверял только наличие if/then, игнорируя extras.
2. Для nested unrelated refs/combinators сохранить scoped opacity и partial
   full-validation text; не запускать ref resolution или условие. Для selected
   production/leaf refs/combinators сохранить прежний отказ. Условия в other
   root property не следует выдавать за вычисленные true/false.
3. Offending pointer должен использовать escaped JSON Pointer segments и
   source location, а production required locator — фактически resolved
   production.location+`/required`, а не hardcoded `/$defs/production/required`.
   Existing escaped-ref fixture p/~q должен сохранить правильную ссылку.
4. Сохранить existing56 control meanings: no constant64/backfill, malformed и
   duplicate guards, local-only refs/cycle/hop caps, canonical schema independent
   от packaged mismatch, typed79/example31, unknown actual/effective origins,
   sentinel inertness, source identity/symlink/caps. Новые rows не должны ломать
   fact_index→receipt mapping; использовать context для поиска, не старые offsets.
5. Required literal membership false означает отсутствие именно этого прямого
   membership declaration, не доказательство optional instance semantics при
   неизвестной composition. Missing source/malformed input не обозначать false.
6. Coverage footprint/диагностики/дополнительные sources подчиняются тем же
   fact/output caps. Determinism проверяется для facts **и** receipt; одинаковые
   bytes не заменяют independent primary-source meaning review.

Design содержит разумный paired positive/negative oracle. Предложенная
последовательность I limited2 source rounds, compiler/source review до product
calls и отдельный Root READY сохраняет finite scope. Упоминание1 GREEN+2actual
в D является предложением, не новым grant. Old unit2/2, E1 1/1 и actual2/2
остаются исчерпанными; originals/failed artifacts сохраняются. Этот review
не проверял и не активировал executable paths/harness/command budgets нового
milestone — это отдельная обязанность Root при dispatch/readiness.

## Граница и STOP

Выполнены только inert source/metadata reads, SHA и Git readback; собственные
report/identity writes. Code/parser/target/test/harness/Deno/compiler/native/
network/science execution0; product/checkpoint/Git/original artifacts не менялись.
Conservative logical source read upper bound768KiB≤1MiB; wall<10min;
CPU/RSS/physical I/O не измерялись. Report<96KiB. Подагенты не использованы.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Actual5 root allOf branches имеют unrelated footprint | Exact schema:179–423, таблица выше | Предикаты и whole schema не evaluated | сохранить |
| Design способен исправить M1 без общего validator | Узкая grammar, independent /required, direct facts+partial coverage | Реализация и executable controls ещё отсутствуют | изменить |
| M2/M3 исправлены в correction contract | Reason-aware text и conditional status/mode/source rules | Пока design, не output evidence | изменить |
| Design готов для отдельного I | Exact baseline/hash, finite scope, paired controls, preserved guards | Source review final implementation ещё обязателен | сохранить |
| Новые runtime/DOC03/render/native/science gates пройдены | D/R выполнения0 | Этот PASS не разрешает и не принимает эти gates | данных недостаточно |

STOP: READY_FOR_I_SOURCE_ONLY; report/identity только, без execution grants.
