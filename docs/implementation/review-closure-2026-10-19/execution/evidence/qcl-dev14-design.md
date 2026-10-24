# DEV14 — design handoff: canonical Contracts descriptions

Дата: 2026-10-19. Автор: `/root/dev14_design`, роль design `ultra`, выбранная Sol сохранена. Статус: **DESIGN_CANDIDATE; CP-DESIGN pending independent reviewer high**. Этот документ не является разрешением реализации и не утверждает CP-CODE. Единственный записанный автором файл — `/tmp/qcl-dev14-design.md`; product files, Git index/refs и coordination checkpoint автор не менял.

## Задача и полномочия

Проверяемый результат DEV14: убрать неоднозначность размера legacy export part в Contracts README и добавить canonical описание `production.energy_chunk`, сохранив все принимаемые/отклоняемые документы и numerical behavior. Покрытие: RV07 F07.3, RV19 P19A. Классификация: bounded authored-description change в существующем контракте; отдельного subsystem/генератора не требуется.

Direct EXEC B/G1/S1 и последующее разрешение использовать доступные engineering resources сообщены координатором и отражены в execution checkpoint. Старые PLAN/approved_standby passage в исходном handoff — исторический контекст, не актуальный запрет уже активированного scope. В этом назначении разрешено только чтение и design handoff; tests/import/install/build/SSH/solver не выполняются. Broad engineering resource grant сохраняет finite packets/accounting, physics/S1 без e–e и единственную final full CI. DEV14 не расходует scientific/build/final-CI counters.

После независимого CP-DESIGN совместимый внутренний контракт может передаваться исполнителю `medium` координатором без нового вопроса оператору — `autonomy.md`, §4. До этого gate implementation **not ready**. Смена constraint/default/validator либо физического смысла требует остановки этой карточки и нового design, а не скрытой правки.

## Immutable inputs и фактический checkout

Рабочая копия: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`. Защищённая original copy `/home/tolya/Загрузки/qcl-negf` не читалась для вычислительного анализа и не изменялась.

- Root `HEAD=e0f244d075dd49874ba4f3847f4efa693f3b3622`; `git status --short` прочитан. Root dirty из-за параллельных owning packets/receipts: `MM components/QCLNEGF.jl`, изменённые AiiDA/Portal/Research, staged/unstaged root docs/evidence. Это не clean release candidate и не diff DEV14. Автор не stage/reset/checkout никакие из этих путей.
- `git submodule status --recursive` прочитан; current Core `a8d2c0de21dfdce3ed3c7c585c555656443f6d89` и AiiDA `5579d55684939495230241f446b7ea07c8ae0224` отличаются от root gitlinks. Portal DEV11 — другой writer; его файлы не входят в source conclusion DEV14 и не изменялись.
- Нужные authority gitlinks прочитаны через `git ls-tree HEAD`: Contracts `e5c056c47fc3bde3e0ca32866692d740ef9b325c`, Runner `0c53c6d0f68e0b25fce79388db831da6fc3ae856`, baseline Core `3108150dd1b6b1377470b384b15c26e272fe5c5d`. Contracts/Runner actual `HEAD` совпадают с этими gitlinks; обе component worktrees чисты.
- Это локаторы наблюдения, не второй поддерживаемый revision lock. Перед implementation/publication состав снова извлекается из Git. Никакие submodules latest не выбирались.

Handoff `development.md` при чтении: SHA256 `494b1c487183ca02e6d19f8c571e3aeba77e0e49e467aa7655dc68eff711ad13`. Прочитаны карточки DEV14–16, README/autonomy/operator-permissions, AGENTS, implemented architecture, implementation-entrypoint и canonical role policy. Для выбранных handoff/review файлов `git diff -- ...` пуст; primary historical review читается из root source, не выдаётся за новый runtime receipt.

Primary review locators:

| Вход | Immutable locator / существенный факт |
| --- | --- |
| `docs/implementation/comprehensive-review/2026-10-14-e48e5b2-01/RV07.md`, F07.3 | SHA256 `a626bc666fae77e984ab886eb9f1e8c052f1b138c23a29f60400cf828c0fcd4c`; legacy-only README ambiguity и 300 MB regression anchor |
| `.../RV19.md`, P19A | SHA256 `cabb6a151e30b2f9d0142744678bf7598d0cdbe73e1b5db815d27bb5e077db4a`; required integer count/no schema default и distinction typed default/assignment |
| `.../fixes/RV19-source-meaning.md` | SHA256 `ddae24cb3a2335a92b77d0b3f0cd52344963e60fb66bf7de1bcdbbe35e499a2e`; prior additive description proposal |
| `.../fixes/RV07-legacy-doc-scope.md`, `.../fixes/RV07-schema-drift.md`, RV07 blind/review | Historical source Contracts `923e0c6…`; limitations и canonical→copy order. Historical source не подменяет current Contracts `e5c056c…` |

Упомянутый исторический D01 report не найден среди published selected bundle paths; он не восстановлен и не использован как обязательный источник. Current validator/schema/assertions достаточны для этого design, но не для утверждения, что D01 выполнен или принят.

## Наблюдаемые source interfaces

Все Contracts локаторы ниже относятся к `e5c056c47fc3bde3e0ca32866692d740ef9b325c`:

1. `README.md:44` пока говорит о maximum independently readable export part 200,000,000 decimal bytes без локального legacy qualifier. `README.md:67` уже правильно ограничивает этот размер archived `qcl-negf.export-parts.v1` и отдельно называет single archive без fixed size upper bound. Исправляется только первое противоречивое предложение; правильный Export transport passage сохраняется.
2. `src/qcl_negf_contracts/schemas/run.schema.json:1420` — `$defs.production.required` содержит `energy_chunk`; `properties.energy_chunk` на строке 1437 имеет только `type: integer` и `minimum: 1`. `description` и `default` отсутствуют.
3. `artifacts.py::validate_export_receipt` (`:69`) принимает Python `int` bytes ≥0, исключает `bool`, не вводит ceiling; confined `.tar.xz` names, SHA256/profile/snapshot checks и запрет `parts/multipart/part_count/maximum_part_bytes` сохраняются.
4. `schemas/export-receipt.schema.json` — `properties.bytes={type:integer, minimum:0}`, без maximum; multipart keys отклоняются через `not/anyOf`. Registry legacy size сохраняется в `results-contract-set.json::legacy_maximum_export_part_bytes=200000000`.
5. `tests/test_contracts.py::test_single_archive_receipt_validates_unbounded_size_and_confined_filename` (`:42`) проверяет literal `300_000_000` через validator function и bundled JSON Schema, затем True/-1/bad hash/parent path/nested path/parts/missing snapshot. Новое physical/transport ограничение из этих примеров не выводится.

Runner `0c53c6d…` read-only interfaces: `_parse_production` в `src/infrastructure/config/configuration.jl:914–935` требует `energy_chunk` в merged mapping и передаёт его в typed constructor. `configuration_source` в `src/application/configuration_types.jl:209–222` возвращает last explicit provenance filename либо `nothing` при absent/empty history. Это не механизм присвоения default. Его prose correction — DEV15.

Core baseline `3108150…`: `src/numerics/optimized/production_contracts.jl::ProductionOptions.energy_chunk` имеет typed default 64. `_production_static_contraction!` в `production_operators.jl:401–434` формирует `first_energies=1:energy_chunk:NE`, `chunk_capacity=min(energy_chunk,NE)` и `last_energy=min(first_energy+energy_chunk-1,NE)`. Поэтому count относится к energy points, помещаемым в chunk; это не число chunks и не grid spacing. Baseline/current Core Git blob identities этих двух файлов совпали: contracts `506792ca13984911444974800fd53b06476fe321`, operators `db3ae118a1b5c018b57e3320b7e4675dd8e4877d`. Так source observation не наследует чужой общий Core acceptance.

Current byte hashes, снятые read-only `sha256sum`:

| Contracts input | SHA256 |
| --- | --- |
| `README.md` | `5902f67e6c36321cacf4eeef70074f73d564fdd99b68519fb4556371cec05451` |
| `schemas/run.schema.json` | `01ebc5aa635ae98d864fda23606d3228efc6020c68066496539227002ada6390` |
| `schemas/export-receipt.schema.json` | `b773dde7e07ab64255faf053eab31569bf1c9b33739ce9fd8a3a99d25b875bdb` |
| `artifacts.py` | `639ebd85f0a1612d2c036d11d8926f7c4bdd04778d5690a8778eb03e8cb6ccaa` |
| `tests/test_contracts.py` | `0231b4d437ed3086a2cb365a0ce2a3926da93008d67e99df598e8aced6f63fd7` |

Runner schema bytes currently hash to the same `01ebc5aa…`; `schema/PROVENANCE.json` SHA256 `dd7f1256d4f994cc554f53288a63ad299baba3866d465625876f0737fd43ea28` declares this hash. Equality today does not establish future enforcement. Description addition intentionally changes canonical bytes; DEV14 leaves Runner copy/provenance untouched until DEV16.

## Alternatives и выбранное решение

| Вариант | Последствие | Решение |
| --- | --- | --- |
| A. Минимально уточнить README44 и один canonical description leaf | Совместимость validator/schema сохраняется; canonical byte hash меняется; straightforward owning publication | **Рекомендуется** |
| B. Перестроить README в общий transport tutorial либо добавить descriptions для всех production options | Расширяет review denominator и авторство без нужды для F07.3/P19A | Не входит в DEV14 |
| C. Добавить schema default64, export maximum либо редактировать Runner copy одновременно | Меняет contract/ownership, создаёт ложный default origin или новый размерный ceiling | Запрещено карточкой |

Выбран A. Предложение historical fixcard «execution chunk count» уточняется до максимального числа energy points в chunk по current operator, без изменения поведения. Это точность описания существующего параметра; reviewer должен подтвердить формулировку в CP-DESIGN.

## Точный implementation contract

Один writer `medium` получает ровно два permitted product paths внутри `components/qcl-negf-contracts`:

- `README.md`: заменить только текущий paragraph в Contract ownership, содержащий unscoped maximum part clause, на текст ниже. Остальной README, включая Export transport, сохраняется.
- `src/qcl_negf_contracts/schemas/run.schema.json`: добавить только JSON Pointer `/$defs/production/properties/energy_chunk/description`. Формат/порядок всех остальных bytes сохраняются; local JSON hunk включает необходимую запятую после `minimum: 1`.

Точный новый README paragraph:

> The result contract is `qcl-negf.results.v1`, and native HDF5 layout is `4.0`. The maximum independently readable part in legacy archived `qcl-negf.export-parts.v1` sets is 200,000,000 decimal bytes. Current single-archive export receipts have no fixed byte ceiling. Readers reject missing or different contract sets. A successful transport or export does not establish scientific acceptance.

Точное proposed значение description — одна JSON string, английский язык owning schema сохранён:

> Positive integer maximum number of energy points per execution chunk for work scheduling. Required in the merged declarative configuration; no schema default is assigned here. The Core typed constructor has its own default, which must not be inferred as configuration-source provenance. This option does not define energy-grid spacing.

README сохраняет decimal bytes 200000000 для legacy parts, `qcl-negf.results.v1` и HDF5 `4.0`; слово «maximum» не относится к current receipt. Description сохраняет dimensionless integer count, required merged declarative input, absence of schema assignment и distinction Core typed default/assigning provenance. No default64 добавляется в schema или README как effective origin. Никаких новых refs/URLs/dependencies/version bumps.

**Excluded writes:** все validator/test/registry/export schema files, constraints `required/type/minimum/default`, другие descriptions, Runner vendored schema/PROVENANCE/docs/source, root gitlinks/locks, Core/Portal/AiiDA/Research/Platform, generated docs/assets. Source behavior, scientific parameters, grid/basis/window/scattering/criteria не меняются. Найденный unrelated defect передаётся координатору отдельной карточкой.

## Acceptance и cheapest checks

Denominator: два authored изменения и сохранение целого parsed canonical schema вне одного description leaf. Ни одно свойство scientific accuracy не заявляется.

| Свойство / control | Проверяемое свидетельство | Критерий |
| --- | --- | --- |
| Только разрешённые paths | `git -C components/qcl-negf-contracts diff --name-only e5c056c47fc3bde3e0ca32866692d740ef9b325c` и reviewed diff | Ровно README + canonical run schema; нет file-wide JSON rewrite |
| Единственный semantic schema change | stdlib JSON old/new comparison, old bytes из `git show e5c056c…:src/.../run.schema.json`; удалить только exact new description leaf из candidate и сравнить со всем old parsed document | Exact equality, description baseline отсутствует, candidate equals agreed string; `required/type/minimum` неизменны, default по-прежнему отсутствует |
| README legacy/current distinction | Literal proposed paragraph и existing Export transport source; validator/registry read-only comparison | 200000000 остаётся только legacy maximum; current bytes ≥0 без introduced ceiling; scientific-acceptance caveat сохранён |
| Invariant files | Owning `git diff --name-only` плюс old/new hashes при receipt | `artifacts.py`, export schema, registry, tests unchanged |
| Existing transport regression, optional one invocation | Exact existing test below, prepared Python3.14 owning import route | 300000000 valid both validators; seven invalid updates rejected; process exit alone не receipt без assertions mapping |
| Formatting | `git -C components/qcl-negf-contracts diff --check` | Exit0; final newline/whitespace correct |

Semantic comparison — временная standard-library postprocessing existing/candidate JSON без project imports, не новый product test/helper и не env setup. Будущий исполнитель вправе создать temporary check script под `/tmp`; exact assertions above являются его полным контрактом. Использовать old bytes из Git object, не независимо набранную копию old schema. Parsed equality намеренно проверяет constraint preservation независимо от формы patch; отдельный reviewed textual diff ловит ненужное переформатирование.

Optional existing regression command, cwd selected root, только после централизованного test-slot grant и проверки готового Python3.14 owning import receipt:

```sh
timeout --signal=TERM --kill-after=5s 90s uv run --locked --no-sync --package qcl-negf-contracts python -m pytest components/qcl-negf-contracts/tests/test_contracts.py::test_single_archive_receipt_validates_unbounded_size_and_confined_filename -q
```

Это maximum **один** L-PY invocation для DEV14, 1 CPU/1 GiB, wall≤90 s, temporary≤16 MiB, logs≤2 MiB; счётчик общий для автора/reviewer. Actual executable/version/module path+distribution/lock route, command/cwd, exit, original output/hash/bytes/wall/RSS записываются координаторским runner. Max ресурсный grant не требует занимать лишние CPU для prose-only check. При missing dependency/Python mismatch/environment failure сохранить receipt и обозначить runtime `not_measured`; не устанавливать окружение и не повторять без нового finite diagnostic packet. Для docs-only exact semantic preservation достаточно source/static checks; optional regression не превращается в numerical requirement. Tests/fixtures новые не добавлять.

Near-zero/units/tolerance: integer/byte boundaries exact, floating tolerance неприменим. Current validator source допускает `bytes=0`; `True` и `-1` запрещены. Existing named regression не содержит zero positive assertion, поэтому его исполнение не выдавать за проверку zero branch. Semantic unchanged proof и прямое чтение validator/schema подтверждают сохранение branch source-wise. Операционная size quota и ресурсы consumers могут быть конечными; phrase no fixed byte ceiling относится к format validator, не unlimited allocation.

### Ограничения oracle

Рецензент независимо читает current validator/schema/required mapping и diff. Сопоставление parsed schemas доказывает отсутствие schema validation drift при этой правке; оно не доказывает корректность baseline. Existing test имеет literal expected outcomes и две реализации validation, но Python validator и JSON Schema могут разделять одну ошибку дизайна. Нет независимого scientific oracle, transport durability/NFS/native reader evidence, numerical solve/discretization/experiment validation. README/source consistency не закрывает эти gates. D01 absence и границы исторического review остаются явными.

## Failure/unknown semantics и stop

В продукте новые exceptions/statuses/I/O не возникают: только descriptions. Для handoff состояния конечны:

- `CP-DESIGN pending`: этот design представлен, implementation не стартует до независимого решения.
- `ready_implementation`: reviewer принимает exact wording/path scope, invariants и checks; координатор назначает writer.
- Source поменялся: re-read affected immutable paths и bounded rebase/re-review; прежний receipt не переносится автоматически.
- Parsed diff затрагивает любой иной leaf, README начинает ограничивать single archive, numerical/default change требуется для prose: stop/replan.
- Optional check не выполнен/окружение отсутствует: `not_measured`, никогда fabricated pass/skip-as-success.
- Review disagreement о «points per chunk»: сохранить два source locators (partition loop и schema) и самую дешёвую проверку — повторное чтение точного Git blob; solver не нужен.

Design envelope: один L-SOURCE packet ≤30 min, максимум два review rounds для этого design без tests/import/build; broader до5 corrective author/review cycles не обнуляют counters. В этой работе выполнены только чтение/поиск Git+source, вычисление file hashes и запись design. Runtime targeted invocations 0, installs/builds/SSH/solver/final CI 0. Shared test slot не занимался. Полные suites и Julia environment не нужны.

## CP-DESIGN вопросы независимому reviewer

Дать reviewer нейтральный вопрос и immutable первичные inputs до авторского объяснения: «Какой контракт задают current schema/validator для energy_chunk и export bytes, и какие минимальные authored corrections нужны при сохранении поведения?» Сначала Contracts/Runner/Core refs+paths и RV07/RV19 original artifacts; затем этот candidate.

1. Верно ли source-grounded «maximum number of energy points per execution chunk», включая shorter final chunk, и устраняет ли это неоднозначность historical «chunk count» без смены семантики?
2. Достаточно ли README paragraph вместе с existing Export transport для однозначного legacy-only 200000000 и current single-archive format, без обещания unlimited operational resources?
3. Сохраняет ли description required merged input/no schema default и разграничение typed default/assigning source, не беря на себя DEV15 full origins?
4. Достаточны ли exact one-leaf semantic diff и reviewed textual diff для prose-only CP-CODE, а optional regression сформулирован честно по реальному assertion denominator/zero limitation?
5. Корректны ли source publication dependency и отсутствие Runner edits в DEV14?

Результат reviewer: accepted / scoped corrections / blocked c воспроизводимыми locators, не общий pass. Технический CP-DESIGN в утверждённом scope закрывают author+reviewer/coordinator; повторный human grant этому документу не предполагается. Этот автор не принимает собственный design.

## Передача DEV15/16 и publication

После CP-DESIGN реализация `medium` делает только два описания, source/static checks и optional one existing regression. После CP-CODE owning Contracts commit/PR публикуется в active PUBLISH; G1 merge имеет собственный exact-reviewed-head/protections gate. Этот design автора не публикует и не merge ничего.

Для DEV15/16 передать: immutable reviewed canonical Contracts commit, exact diff/hash; base canonical schema hash `01ebc5aa…`, новый SHA256 и size canonical schema после реализации; точный JSON Pointer/description; README diff; CP-DESIGN/CP-CODE receipts и runtime limitations. Не вычислять заранее вымышленный новый hash и не обновлять PROVENANCE вручную в DEV14.

DEV15 design может готовиться на reviewed canonical diff. **DEV16 implementation/publication ждёт canonical Contracts source published** и accepted DEV15 drift seam. Runner затем копирует published canonical bytes целиком и обновляет существующий provenance owning workflow, а не повторяет ручной description patch. Root gitlink выбирает опубликованный owning ref отдельным INT02. Перед этой операцией source recheck обязателен; equality старых copies не ongoing guard. Новый root candidate получает своё release evidence, sole final CI остаётся будущим OPS16.

## Фактическое завершение design

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Неоднозначность legacy maximum остаётся в current README | Contracts e5c056c README44 vs67, validator/schema/registry | Product correction ещё не реализована | изменить |
| energy_chunk required positive dimensionless count без schema default | Canonical production required/type/minimum; Runner _parse_production; Core chunk partition | Description отсутствует; runtime не выполнялся | изменить |
| Typed default64 не даёт assigning provenance | Core ProductionOptions + Runner configuration_source sources/last | Full origin model не входит в DEV14 | сохранить |
| Format receipt допускает 300000000 и сохраняет hostile-input rejection | Current artifacts.py/schema + literal existing test assertions | Anchor прочитан, тест не запускался; zero positive assertion отсутствует | сохранить |
| Разрешён exact minimal implementation packet | Proposed two-path wording, one-leaf equality contract, finite optional test, publication order | CP-DESIGN независимым reviewer pending | дополнительно измерить |
| Native/scientific/release acceptance установлен этим design | Нет соответствующих запусков или receipts | Source/design-only; S1/final-CI counters не затронуты | данных недостаточно |
