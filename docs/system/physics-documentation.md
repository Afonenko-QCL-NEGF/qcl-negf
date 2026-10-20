# Физическая документация рядом с исследованием

Статус: требования пользователя и предлагаемый способ реализации, 2026-10-09.
Аудит относится к root `bce0aee` и его gitlinks. Сайт и Julia HTML docs
сейчас не изменены/не собраны; новые расчёты не выполнялись.

Уточнение 2026-10-19: [контракт реализации DOC03](#model-source-help-contract)
ниже принят после independent CP-DESIGN. Исторический аудит и примеры этого
документа сохраняют прежнюю source/date identity; reference parameter set
не подменяет used inputs конкретного S1 run. Принятый контракт не означает
готовность schemas, runtime help, HTML serving или научную приёмку.

## Назначение

Исследователь должен понимать, **какую модель использует и почему выбран
параметр**, непосредственно при постановке задачи и чтении результатов.
DOI без объяснения недостаточен. Первый путь чтения — учебный, для человека,
знакомого с квантовой механикой и полупроводниками, но изучающего NEGF.
Полная формальная и программная справка остаётся доступной.

Это не новый physics engine в UI. Математика и её семантика принадлежат
Core; материальные наборы, источники конкретных значений и постановки —
Research; resolution и effective values — Runner; Portal показывает их.

## Три разных происхождения

1. **Модель/формула.** Что описывает взаимодействие, из каких предпосылок
   выведено и какая именно версия реализована. Например, гауссовый коррелятор
   IFR и независимые интерфейсы.
2. **Численное значение.** Где получены Δ/Λ, массы, permittivity и т. п.:
   измерение, таблица/формула статьи, material interpolation, fit, явное
   допущение исследователя. Статья о геометрии не автоматически задаёт их.
3. **Effective input.** Что фактически принято в данной задаче: preset,
   явный override, derived value или выбранное правило. Путь YAML файла
   объясняет composition, но не является физическим первоисточником.

Физические константы, material parameters, model assumptions, derived
quantities и numerical tolerances различаются. Не требуется DOI для каждого
π или списка индексов; требуется объяснить роль и основание любого значимого
числа. Неизвестное происхождение показывается как неизвестное, а не заменяется
выдуманной ссылкой или нулём.

Пользователь согласовал: явные исследовательские значения с неизвестным
источником допустимы для запуска помеченного варианта. Они не получают
статус published/measured, а научное принятие требует обоснования. Нельзя
создать бесконечный gate «найти все источники» перед любым exploratory solve.

## Карточка модели под рукой

В конфигураторе у механизма/параметра есть краткое пояснение и кнопка
«Модель и источник», открывающая светлую боковую панель без потери формы.
На странице run та же карточка показывает **использованное** значение и
модель этого run, а не текущий default другого релиза. Отдельная вкладка
«Физика и модели» даёт учебное чтение и полную справку.

| Содержание карточки | Что видит исследователь |
| --- | --- |
| Название и status | Реализовано в baseline / доступно как вариант / отдельный оператор / вне scope этого исследования |
| Интуиция | Что делает механизм, почему важен для QCL и каких наблюдаемых касается |
| Предпосылки | Размерность, equilibrium/nonequilibrium, elastic/inelastic, независимость/correlations, boundary assumptions |
| Формула | Canonical equation ID, конвенции, определения символов и единицы; переход к выводу |
| Значение в задаче | Effective value/units, preset или override, условия T/composition/doping где применимо |
| Источник модели и значения | Раздельные source locators: статья+раздел/формула/таблица либо явное исследовательское допущение |
| Ограничения | Где модель неприменима, что исключено, какие uncertainties/fit assumptions известны |
| Реализация | Публичный Julia symbol и документация; степень включения в полный solver |
| Проверка | Применимые identities/нормировки и ссылка на их определение; наличие operator test не называется transport validation |
| Продолжение чтения | Связанные главы учебника, glossary и полная API/формальная справка |

Не все поля должны быть развёрнуты сразу. Первое представление — несколько
объясняющих предложений и used values; затем предпосылки/формула/источники;
полный вывод и API по ссылке. Это progressive disclosure содержания,
а не сокращённая физическая модель.

### Пример: шероховатость интерфейсов

Текущий passport задаёт Δ = 0.10 nm и Λ = 9.0 nm. Короткое объяснение:
«Небольшие случайные смещения границ меняют край зоны и рассеивают электроны.
Δ — среднеквадратичная высота, Λ — пространственный масштаб корреляции».
Подробный слой показывает Gaussian spatial correlation, независимость
разных интерфейсов, canonical `EQ-KIFR-001`, `interface_roughness_kernel`
и область применимости. Значения связываются с **их собственным** источником;
наличие DOI Bosco рядом с толщинами не устанавливает источник этих двух чисел.
Если источник пока не подтверждён, это прямо написано в value origin.

Другой пример — `q_s = 0.20 nm⁻¹`: нужно показать, фиксировано ли screening
или вычислено по density/temperature, какую потенциальную форму/размерность
оно задаёт. Равное численное κ в двух моделях не делает модели одинаковыми.

## Учебный маршрут и полная справка

Предлагаемый первый маршрут:

1. Задача QCL: период, quantum wells, bias per period, ток и scope модели.
2. От профилей материалов к basis/subbands: что проектируется и что теряется
   при конечном подпространстве; границы легирования и материалов различны.
3. Почему одного Schrödinger spectrum недостаточно: доступные и занятые
   состояния, смысл Gᴿ/Gˡ/Gᵍ, spectral function и conventions.
4. Рассеяние: от физического механизма к self-energy, параметры и исходные
   assumptions; различие coherent transport и отдельной rate picture.
5. Самосогласование SCBA/Poisson: что меняется на итерации и как читать
   raw residual; смешанный шаг не равен fixed-point residual.
6. Наблюдаемые: J, populations и spatial-energy maps; units, energy zero,
   integration и ограничения. Existing optical response описан отдельно
   в expert reference; его включение в релиз отложено по S09.
7. Когда результату можно доверять: разные уровни convergence, physics,
   discretization и validation; один разбор ошибки/отрицательного результата.
8. Работа через Julia/API, конфигуратор и independent/continuation sweep.

Каждая глава: физический вопрос → интуиция/схема → assumptions → формула и
вывод → маленький явно обозначенный пример → связь с implemented symbol →
проверки/ограничения → полная справка. Не начинать с deployment или перечня
всех полей YAML. Воспроизводимые examples используют малые bounded задачи;
самосогласованный production solve не запускается при открытии страницы.

Рядом, без обязательного линейного чтения: полный каталог моделей/параметров,
формулы/конвенции, discretizations, API/экспертные операторы, словарь,
источники и численные протоколы. Учебные chapters и reference не копируют
одни и те же canonical formulas. Такой способ различать учебник, пояснение,
рецепты работы и справку соответствует [Diátaxis](https://www.diataxis.fr/start-here/);
он не требует второго documentation framework или четырёх копий текста.

Полная справка сохраняет описание уже существующих экспертных операторов,
включая находящиеся вне области текущего релиза. Такие страницы явно
помечаются как отдельный оператор/иллюстрация либо вне scope; их наличие
не обещает расчёт мощности лазера, временной динамики или волновода.
Учебный маршрут первого релиза остаётся стационарным.
Оптические gain/absorption спектры не предлагаются как принятая функция
этого релиза до отдельного обоснования количественного отклика. Это не
исключает уровни энергии структуры и spectral transport maps из учебника.

## Согласование с Julia docs

Core уже содержит `docs/src/theory`, `physics/models.md`, physical atlas,
glossary, docstrings и equation→symbol traceability. Сохраняем их и улучшаем
порядок/связи. Julia `?symbol` получает краткий API contract, units и ссылку
на canonical модель/вывод; Documenter объединяет docstrings и Markdown.
[Julia documentation](https://docs.julialang.org/en/v1/manual/documentation/),
[Documenter makedocs](https://documenter.juliadocs.org/stable/lib/public/).

Длинные физические explanations находятся в owning Markdown chapters,
а не целиком внутри docstrings. Research владеет sourced parameter sets
с условиями/происхождением; Core chapter ссылается на них, не объявляет все
constants материалом из одного design paper. Одному source fragment/model ID
соответствуют полный HTML и короткая карточка. Короткий текст задаётся в
том же owning source/выделенном фрагменте; build генерирует представление
для Portal. Ручная копия формулы или ещё один независимо редактируемый
справочник в React не допускаются.

Формат небольшой карточки/связи parameter→model/document fragment —
межкомпонентный contract. Его schema принадлежит Contracts, содержание —
Core/Research, effective origin — Runner. Static catalog — presentation
artifact, не global research cache и не новый evidence ledger. Не надо
пересчитывать SHA каждого HDF5 для показа help или ссылок на статьи.

## Материализация рядом с Portal

Предпочтительно сохранить Documenter и выпускать **статический documentation
artifact** из выбранных gitlinks/locked workspace, совместимый с release.
Serving — тот же локальный HTTP origin, отдельный prefix `/docs/` и ссылки
из Portal. Core, Runner и research help имеют различимые sections/versions;
не нужен live Julia service, новый CMS или отдельная docs VM.

Пример URL layout — предложение, не существующий route:
`/docs/<release-source-id>/core/theory/08_kernels.html#eq-ifr-kernel`.
Человек получает HTML/search/формулы, агент — bounded текст карточки и
canonical refs через тот же API/static catalog. Run использует свой model/
release locator; документация текущего релиза не выдаётся за описание
несовместимого старого run. Source-id берётся из существующего release
composition, отдельного ручного revision lock нет.

Full docs лучше открывать самостоятельной страницей с прямой ссылкой, а
краткую карточку — внутри configurator. Iframe не является обязательным:
он осложняет navigation/focus, theme и nested scrolling. Альтернатива —
полный Markdown renderer в Portal, но он требует заново поддерживать
Documenter `@ref/@docs`, math/search и source links; сейчас не оправдан.

Обязательные условия материала на локальном сайте:

- Все JS/CSS/fonts/math/search assets доступны локально; внешние articles
  остаются ссылками, но отсутствие интернета не ломает explanations/формулы.
- Весь HTML, включая Documenter pages, фиксированно светлый. Наличие светлого
  Portal не гарантирует отсутствие theme switcher/OS auto-dark в docs.
- Готовый artifact строится в build/CI фазе, затем только раздаётся. Просмотр
  help не запускает Julia, compilation, docs build или solver.
- Public/reference names, anchors и help bindings проверяются; текущий
  `checkdocs=:exports` не доказывает полноту любой внутренней/expert справки.
- Doctests и illustrative examples отделены от scientific acceptance;
  полные SCBA/Poisson не добавляются скрыто в docs build.
- Documentation build и source binding имеют свои checks. Их pass не
  превращается в pass физических уравнений.

<a id="model-source-help-contract"></a>

## Принятый контракт реализации model/source help

Статус на 2026-10-19: technical contract DOC03 принят для owning implementation
после независимого CP-DESIGN. Это спецификация будущих schemas, adapters и
публикации, а не утверждение, что они уже реализованы или проверены runtime.
Source facts ниже относятся к root
`9d8cf0cad32743791cc3b80ac7c2a948dab02f48` и его gitlinks; эта запись не
заменяет Git как authority состава. Existing audit выше и ниже сохраняет
датированный контекст `bce0aee`.

Минимальный route — existing Documenter + static hub/catalog. Человек и агент
получают один canonical fragment; numeric reference origin, assigning source
и фактически переданный solver input различаются. При отсутствии retained
origin proof либо execution snapshot соответствующее поле остаётся unknown.
Новый solver, model registry, capture ingress или field configurator этим
контрактом не вводятся. Полное оформление docs не становится prerequisite S01.

Полный научный scope сохраняется: 0 mV/period, lattice/LO 70 K, LO/acoustic/
impurity/IFR/alloy, electron–electron=none. Fixed-light/offline publication,
реализация контрактов, browser/native и научная приёмка имеют отдельные checks.
Приведённые ниже negatives и controls запланированы; их исполнение здесь не
утверждается.

<a id="model-help-source-facts"></a>

### Source facts выбранной композиции

1. Root `ops/git.ts:sourceGraph` уже получает `qcl-negf.git-graph.v1` из Git
   gitlinks, проверяет checked-out revisions и clean source. `ops/release.ts`
   вкладывает этот graph в `qcl-negf.release.v2`; application release directory
   именуется SHA256 точных bytes `release.json`. Root commit, application
   release digest и documentation bundle digest — разные идентичности.
2. Root `julia/Manifest.toml` выбирает Julia `1.13.0` и Documenter `1.17.0`,
   package UUID `e30172f5-a6a5-5a46-863b-614d45cd2de4`, tree
   `56e9c37b5e7c3b4f080ab1da18d72d5c290e184a`. Root `julia/Project.toml`
   выбирает Core/Runner через workspace paths. Standalone Runner docs имеют
   другую source selection (`Core v0.2.0`); она не подходит для release pilot.
3. Selected Core/Runner `docs/make.jl` используют Documenter, `prettyurls=false`,
   `doctest=true`, `checkdocs=:exports`, `warnonly=false` и импортируют пакеты.
   Root `ops/ci.ts` уже передаёт `QCL_NEGF_PROJECT=<root>/julia` в owning docs
   tasks. Build может импортировать/precompile и выполнять executable examples;
   это отдельный BUILD stage, не source-only extraction и не просмотр страницы.
4. Runner `src/application/configuration_types.jl:configuration_source` возвращает
   последнюю запись истории или `nothing`. `_deep_merge!` хранит absolute source
   filenames. Generated assignment markers и `application:auto_exact` объясняют
   назначение, не научный источник и не весь effective causal chain.
5. Contracts `run.schema.json` ссылается из `/properties/production/$ref` на
   `#/$defs/production`; точный leaf — `/$defs/production/properties/energy_chunk`.
   Он требует integer>=1 и явно не назначает schema default. Core
   `src/numerics/optimized/production_contracts.jl:ProductionOptions` отдельно
   задаёт typed default 64. Равные числа не устанавливают одинаковое происхождение.
6. Scientific plan имеет `model_revision=transport-contract-v2`, fingerprints,
   execution `resolved_configuration`/`provenance.sources` и point passports.
   Runner `_point_resolved_raw` применяет оси отдельно. Один `model_revision`
   не доказывает root release/source identity; planned value не доказывает used
   value после runtime planning. Missing execution snapshot остаётся unknown.
7. Research `config/model/reference-2019-70k.yaml` хранит Δ=0.10 nm, Λ=9.0 nm,
   fixed screening 0.20 nm^-1 и **56 mV**, а не принятый S1 0 mV. DOI в run
   description относится к геометрии/легированию, не подтверждает автоматически
   все material/scattering values. Это reference fragment, не паспорт S1 attempt.
8. Portal `api.py:create_app` ставит authenticated `/api/v1/…` routes и затем
   `app.mount('/', StaticFiles(..., html=True))`. Platform
   `modules/application.nix` проксирует `/` к API. Документационного mount нет.
   CSP — same-origin без внешних scripts/styles. Frontend `main.tsx` загружает
   frozen JSON plan; физического field configurator в selected source нет.
9. AiiDA service уже читает bounded frozen input/retrieved plan в actor
   (`get_export_plan`) и хранит optional WorkChain `release_id` при submission.
   Этот portable label сам по себе не равен Git SHA. Нужен сохранённый release
   manifest/receipt, который связывает именно этот label с graph; current
   deployment defaults для historical run не подходят.

Это source observations, не native/import/browser/scientific доказательства.

<a id="model-help-publication-route"></a>

### Минимальный путь публикации

| Вариант | Три journeys DOC02 | Стоимость/ограничения | Решение |
| --- | --- | --- | --- |
| Static hub с тремя входами + existing Documenter search по каждому разделу + bounded JSON fragments | Исследователь идёт к SCBA/final assessment; разработчик к configuration_source/energy_chunk; оператор к recovery/runbook. Один hub связывает главы и reference | Нет общего cross-corpus ранжирования; три осмысленных входа и прямые anchors уже достаточны для pilot | **Выбрать** |
| Единый search adapter поверх inventories/search indexes всех generators | Полезен, когда reader question нельзя разрешить по разделу; мог бы объединить symbol/config/operator lookup | Ещё один index compatibility layer; нужно version isolation, ranking, snippets, offline/cold-cache controls. `objects.inv` не содержит value origin | Отложить до наблюдаемого gap DOC05 |
| Markdown/math renderer и поиск внутри React либо новый docs framework | Единая оболочка | Повторная реализация @ref/@docs/math/source links/theme и второй independently edited corpus | Не выбирать |

Выбранные URLs — proposed, сегодня не реализованы:

```text
/docs/<source_revision>/index.html
/docs/<source_revision>/core/theory/09_scba.html#researcher-scba-route
/docs/<source_revision>/core/theory/12_validation.html#researcher-final-route
/docs/<source_revision>/runner/user/configuration.html#developer-configuration-route
/docs/<source_revision>/runner/user/results.html#operator-recovery-route
/docs/<source_revision>/operator/recovery.html
/docs/<source_revision>/help/fragments/<fragment_id>.json
/docs/<source_revision>/bundle.json
```

`source_revision` — полный 40-hex root commit из existing graph. Это source URL,
не application release digest. Run разрешает его только через его retained
binding. Hub имеет три task links и обычные links на model/API/config references;
разделы сохраняют собственный offline search. Нового live Julia service, docs
VM, CMS, workflow DSL, общего model registry или research cache нет.

<a id="model-help-canonical-sources"></a>

### Canonical source для каждого факта

«Один source» означает единственное owning место для каждого атомарного факта,
а не вручную поддерживаемую универсальную таблицу вместо владельцев.

| Факт | Canonical owner/source | Что материализуется |
| --- | --- | --- |
| Julia documented signature, units, effects/errors | Core/Runner docstring + typed declaration и проверки соответствующего symbol | Documenter @docs; fragment с source refs и extraction status. Documented signature не выдаётся за runtime method inventory |
| Declarative type/required/default/constraint | Contracts owning JSON Schema, `description` и существующие validation rules | Field reference по JSON Pointer. Schema default отсутствует — `not_assigned`; typed default хранится отдельным fact |
| Модель, assumptions, conventions, formula IDs, applicability/ограничения | Existing Core Markdown chapters/models/traceability | Full HTML; короткое authored пояснение в **одном** owning `docs/help/fragments.json` с refs в эти главы. Формулы не копируются в JSON/React |
| Источник конкретного material/model value, условия/uncertainty | Research `docs/help/value-origins.json` и выбранный parameter-set YAML | Value-origin annotation с public source refs; численные значения читаются из owning YAML, повторного набора чисел в help нет |
| Последний assigning source | Runner recorded provenance того же plan/execution/leaf | Sanitized structured assignment. `configuration_source` — один из inputs адаптера, не вывод scientific origin |
| Planned/used inputs, point axes, runtime resource override | Runner frozen point passport + retained execution input/strategy snapshot | Bounded projection. Plan и used snapshot различаются. Отсутствующие части не реконструируются по default или совпадению числа |
| Presentation и serving | Portal/Platform | Чтение этих bytes, ссылки и unknown/error states; никаких физических формул или новых критериев в UI/scheduler |

Proposed authoring files содержат только короткий текст/семантические refs и
provenance annotations. Это не model registry: нет API выбора модели, вычисления
derived input или live resolution. Если fact уже имеет canonical текст, annotation
ссылается на него. Изменение поведения сопровождается owning docstring/schema.

Первый help slice: IFR, fixed screening, LO и masses/band offsets выбранного
reference parameter set; DOC06 fixed API/config slice — `configuration_source`
и `production.energy_chunk`. Наличие этого slice не означает coverage всех
активных leaves. Unknown mapping виден явно, а не молча связывается по имени.

<a id="model-help-formats"></a>

### Формат bundle, fragment и run view

Contracts владеет одним schema resource `model-help.schema.json` (Draft 2020-12)
с `$defs` для bundle, fragment и view. Все описанные objects имеют
`additionalProperties:false`; версия `v1` принимает только перечисленные поля.
Это принятый implementation contract; существующим Contracts API он не объявляется.

Общие типы:

- `Sha1` — `[0-9a-f]{40}`, `Sha256` — `[0-9a-f]{64}`.
- `Id` — `[a-z][a-z0-9._-]{0,127}`; один fragment на URL/response.
- `PublicRef` = `{component, revision, path, selector, sha256}`. Component — один
  из source graph paths или `root`; revision ровно выбранный commit владельца;
  path — нормальный repo-relative POSIX file из input allowlist; selector —
  `{kind: 'symbol'|'anchor'|'json_pointer'|'file', value: string}`; file selector
  имеет пустое value. SHA256 относится к полным source bytes, не к вырезке.
- `DocRef` = `{section, path, anchor}`: section=`core|runner|research|operator`,
  path — allowlisted relative `.html`, anchor — существующий ID либо `null`.
  URL строится только относительно exact `/docs/<source_revision>/`.
- `Origin` = `{status, kind, locators, note}`. status=`known|unknown|not_applicable`;
  kind=`publication|measurement|interpolation|fit|research_assumption|code_policy|unknown|not_applicable`;
  locators — массив `{title, uri, location}`. URI только `https:`/`doi:` без
  credentials/query secrets; location — точная формула/таблица/раздел/страница.
  Для unknown: kind=unknown, locators=[], note обязателен. Known исследовательское
  допущение допускает locators=[], но note называет явное owning assumption;
  наличие DOI не превращает kind в measurement. `note` — plain text.
- `Atom` = `{kind, value, unit}`. kind=`quantity|integer|number|boolean|enum|null`;
  value — scalar JSON соответствующего типа, finite numbers only; unit —
  canonical строка единицы, `1` для dimensionless, `null` при неприменимости.
  Никаких массивов, объектов, NaN/Inf. Known-null отличается от отсутствия.
- `Fact` = `{name, status, text, sources}`. name — один из десяти классов:
  `signature`, `units`, `default`, `constraint`, `effects`, `errors`,
  `formula_origin`, `value_origin`, `assigning_origin`, `effective_origin`.
  status=`known|partial|unknown|not_assigned|not_applicable`; text — plain text
  или null; sources — PublicRef[]. Unknown/partial не считается extraction pass.
  Default facts явно называют контекст schema/typed constructor/example; known
  dynamic/default невозможно получить по одному имени/пустой history.

<a id="model-help-bundle"></a>

#### `bundle.json`: output build, input static server/help resolver

| Поле | Тип/точное содержание |
| --- | --- |
| `format` | const `qcl-negf.docs-bundle.v1` |
| `sources` | existing `qcl-negf.git-graph.v1` object из `sourceGraph`: format, revision, sorted components[{path,revision,url}]; generated, не новая таблица pins |
| `schema` | PublicRef на Contracts `model-help.schema.json`, selector file |
| `generator` | `{name:'Documenter', version:'1.17.0', uuid, git_tree_sha1, julia_version:'1.13.0', project_sha256, manifest_sha256, recipes:PublicRef[], toolchain_lock:PublicRef}`; uuid/tree как в [source facts](#model-help-source-facts) |
| `fragments` | descriptors `[{id, file, sha256}]`, unique id/file; file ровно `help/fragments/<id>.json` |
| `files` | `[{path, media_type, bytes, sha256}]` всего публичного payload, включая HTML/CSS/JS/fonts/math/search/JSON; unique normalized paths; `bundle.json` исключён из self-hash списка |
| `aliases` | `[{from, to}]` version-local DocRef; aliases должны иметь реальную сохранённую HTML page/anchor, не только запись в index |

Идентичность manifest — SHA256 exact UTF-8 bytes `bundle.json`; хранится во внешнем
build/publication receipt, не рекурсивно внутри самого manifest. Application
`release.json` не редактируется задним числом ради добавления docs digest.
Production publication receipt связывает existing `release_id`/retained release
manifest SHA256, sources.revision и bundle SHA256. Для standalone source docs
application binding может отсутствовать; тогда UI не заявляет installed release.

<a id="model-help-fragment"></a>

#### Static fragment: output Core/Research + bounded extraction

| Поле | Тип/содержание |
| --- | --- |
| `format` | const `qcl-negf.model-help-fragment.v1` |
| `id` | Id: например `model.ifr` или `config.production.energy_chunk` |
| `source_revision` | root Sha1, равен bundle.sources.revision |
| `title`, `summary` | plain text, max 160 / 1600 Unicode characters; summary authored один раз в owning source |
| `scope` | `baseline|variant|operator_only|outside_study`; scope привязан к documented model context, не выводится из feature наличия |
| `meaning_source` | PublicRef owning Core/Runner scientific/API explanation |
| `full` | DocRef полного owning объяснения |
| `related` | DocRef[] учебных/формальных/API продолжений, максимум 12 |
| `equations` | `[{id, doc}]`, id существующего equation ID (например EQ-KIFR-001), doc=DocRef; формулы здесь не повторяются |
| `inputs` | `[{path, schema_source, facts, reference_value_origin}]`; path — whitelisted dotted config leaf, schema_source=PublicRef с JSON Pointer, facts=Fact[]; reference_value_origin — ReferenceValueOrigin ниже, всегда reference-only |
| `api` | `[{symbol, source, doc, facts}]`; public symbol, PublicRef, DocRef, Fact[] |
| `assumptions`, `limitations` | массивы короткого plain text, по максимум 12×400 chars; длинный вывод остаётся в full |

`facts` покрывают все десять классов для fixed slice; неприменимое явно
not_applicable, отсутствие annotation/extraction явно unknown/partial. В
static fragment `assigning_origin`/`effective_origin` описывают **семантику** и
source функции, без частных значений или истории конкретного run. Для numeric
leaf нет автоматического DOI или pseudo-formula из его имени.

<a id="model-help-value-origin"></a>

#### Reference origin и источник конкретного значения

`ReferenceValueOrigin` имеет ровно `{id, parameter, atom, applicability, origin}`:

- id=Id, parameter=PublicRef точного public parameter-set file + JSON Pointer;
  atom=Atom, **сгенерирован** из этих bytes, не второй вручную редактируемый набор
  чисел. Revision/hash parameter обязаны совпасть с bundle graph.
- applicability=`{status, conditions, note}`; status=`specified|unknown`.
  conditions — максимум 12 `{id,path,relation:'equal',atom,source}`; path —
  публичный scalar context/physical leaf, source=PublicRef scientific statement
  об условиях источника. Это authored applicability источника, не автоматически
  весь YAML. Unknown требует note и не допускает run-origin bound.
- origin=Origin. Карточка всегда подписывает его «Источник reference-набора»;
  static known publication остаётся known **только в этом reference context**.

Динамический InputView получает отдельное обязательное `value_origin`:
`{declared:ValueOriginView, used:ValueOriginView}`. ValueOriginView имеет ровно
`{status, origin, binding, reason}`; status=`bound|unknown|not_applicable`;
origin=Origin; binding=`ValueOriginBinding|null`; reason=
`ok|origin_not_recorded|override_unbound|conditions_unbound|source_unbound|value_unavailable|not_applicable`.
Unknown имеет origin.status=unknown, origin.kind=unknown, locators=[], binding=null
и явный reason. Число и assigning provenance могут быть known независимо от него.

`ValueOriginBinding` — `{reference_id, annotation, parameter, phase, value,
assignment, conditions, receipt}`. Reference_id=ReferenceValueOrigin.id;
annotation=PublicRef authored Research annotation; parameter — exact PublicRef
parameter-set leaf; phase=`declared|used`; value=Evidence нужного scalar;
assignment=Evidence **retained source-binding receipt**, не только pathname;
conditions=Evidence[] для всех applicability conditions; receipt=Evidence
retained origin claim. Evidence.container дополнен `value_origin_receipt`.

Retained origin claim — scalar object в selected snapshot `origin_bindings[]`:
`{reference_id, annotation, parameter, phase, assignment_receipt, conditions}`.
Assignment_receipt имеет `{source, source_sha256, leaf_pointer, capture,
plan_fingerprint, execution_id, point_id, attempt}`: source=PublicRef,
source_sha256 равен его content hash, leaf_pointer — JSON Pointer assignment
в этом frozen plan, capture const `retained_public_source_binding`. Conditions —
`[{id,input_path,phase}]`, они адресуют scalar input **этого** snapshot/context;
для declared можно адресовать exact frozen point passport. В claim нет DOI-копий,
private pathname или самостоятельно назначенных AiiDA UUID. Origin берётся из
annotation, не из свободного текста claim.

Validator связывает record только если одновременно:
1. static annotation/parameter bytes и source graph соответствуют выбранному
   bundle, scientific applicability status=specified;
2. retained receipt связывает **именно последний assigning source** данного
   leaf с этим public file/leaf, включая hash и local context; source filename
   из history без capture receipt недостаточен;
3. target declared/used Atom совпадает с leaf binding и все applicability
   conditions совпадают с retained context evidence по phase; numeric equality
   сама по себе никогда не устанавливает пункты 1–2;
4. receipt/claim относится к этому plan/execution/point/attempt и exact phase,
   available snapshot hash проверен. Declared origin не переносится в used,
   если после него есть unbound runtime override/derived step.

**Producer boundary:** Research авторствует annotation; Runner source adapter
проверяет/переносит только уже retained public source-binding receipt в
origin_bindings. Selected source сегодня такого receipt не сохраняет. Поэтому
первый DOC07 для этих existing plans возвращает actual value_origin=unknown,
даже когда static reference известен. Он не пытается создать receipt задним
числом из equality, current checkout или source filename. Для новых snapshots
без входного capture receipt origin_bindings=[]. Production known-origin
capture не заявлен существующим или обязательным для завершения этого scope;
если нет готового retained receipt, неизвестное остаётся неизвестным. Формат
и positive fixture позволяют проверить bound branch без фиктивной production
атрибуции. Новый capture ingress/CLI/API этим контрактом не вводится.

Reference A=0.10 nm, override B=0.15 nm без origin -> reference-only origin A
сохраняется, declared/used origin B=unknown/override_unbound. Override B=0.10 nm
с другой assignment либо иными T/composition также unknown. Positive control
использует explicit retained binding exact A/context/phase: только тогда bound.
Отсутствие физического первоисточника не запрещает exploratory solve.

<a id="model-help-run-view"></a>

#### Run view: output read adapter, input человек/агент/Portal

Новый proposed authenticated endpoint:
`GET /api/v1/runs/{run_uuid}/model-help?fragment_id=…&execution_id=…&point_id=…&attempt=…&calcjob_uuid=…`.
Все selectors bound к одному существующему run; execution/point обязательны;
attempt и calcjob_uuid выбираются по уже действующим правилам AiiDA selection.
Неоднозначность не разрешается выбором первого result. Нет path/query URL от
пользователя, batch всех leaves или обхода actor ownership.
UUID канонический полный; execution/point имеют existing scientific identifier
grammar, fragment_id — Id, attempt — положительный integer. HTTP 401 сохраняет
existing auth; malformed selectors — 422, absent run/execution/point — 404,
ambiguous/conflicting attempt selection — 409, actor unavailable — existing 503.
Для существующего context unknown/incompatible/unavailable binding возвращается
HTTP 200 с typed status/reason и fragment=null: это metadata о недоступности,
а не successful scientific/help binding. Неизвестный syntactically valid fragment
даёт unavailable/fragment_missing; static JSON URL для него отвечает 404.

| Поле | Тип/содержание |
| --- | --- |
| `format` | const `qcl-negf.model-help-view.v1` |
| `context` | `{run_uuid, execution_id, point_id, attempt, calcjob_uuid, plan_fingerprint, scientific_fingerprint, configuration_hash, model_revision}`; trusted actor UUID/attempt обязательны после selected-child enrichment; fingerprints от exact frozen plan; configuration_hash — declared point passport, nullable только при отсутствии |
| `binding` | `{status, release_id, release_manifest_sha256, source_revision, bundle_sha256, reason}`; status=`bound|unknown|incompatible|unavailable`; unknown scalar fields=null; reason — enum ниже |
| `fragment` | `{id, url, sha256}` либо null; url только allowlisted static JSON того же exact source revision; содержимое не переписывается в API |
| `inputs` | bounded `InputView[]` только paths из fragment.inputs; максимум 32 |
| `input_status` | `{status,reason}` exact enums [контракте retrieval](#model-help-retrieval); availability input metadata отдельно от documentation binding/scientific status |

`InputView` имеет **ровно** `{path, declared, used, assigning, effective_origin, value_origin}`; value_origin определён в [контракте value origin](#model-help-value-origin):

- `declared` и `used` = `{status:'known'|'unknown', atom:Atom|null,
  evidence:Evidence|null}`. Known требует atom и evidence. Unknown требует оба
  null. `declared` читается из retained frozen point-resolved configuration;
  `used` — только из retained execution input/strategy snapshot того же attempt.
  Plan или current default не заполняет missing used. Point axes читаются из
  point passport/explicit axis mapping Runner, не из template первой точки.
- `assigning` = `{status:'known'|'unknown'|'redacted', kind, source, rule, evidence}`.
  kind=`config_file|generated_assignment|typed_constructor|execution_strategy|point_axis|unknown`;
  source=PublicRef|null; rule=allowlisted producer rule ID|null;
  evidence=Evidence|null. Known должен иметь source или rule и evidence;
  unknown имеет kind=unknown и null поля. Private source path означает redacted,
  source=null; его basename/absolute path не возвращаются. Presence of a scalar
  не разрешает kind=typed_constructor. Последняя recorded assignment не заменяет
  историю полного effective origin.
- `effective_origin` = `{status:'known'|'partial'|'unknown', evidence:Evidence[]}`.
  Полное known требует всех применимых retained planning/runtime steps; missing
  chain даёт partial/unknown, даже если assigning известен.
- `Evidence` = `{container, sha256, selector}`. container —
  `frozen_plan|execution_input|execution_strategy|release_receipt|value_origin_receipt`; sha256 — exact
  bounded metadata bytes, selector — allowlisted JSON Pointer внутри них.
  Raw file paths, handles/ORM objects и свободные server URLs не возвращаются.

Причины binding: `ok|source_binding_missing|wrong_release|bundle_missing|unsupported_version|fragment_missing`.
`fragment=null` при unknown/incompatible/unavailable: нельзя показывать current
карточку как помощь этого run. Отдельная явная ссылка «Справка текущего релиза»
возможна вне run-bound карточки с соответствующей подписью.

<a id="model-help-local-snapshot"></a>

#### Runner-local snapshot, placement и capture

Выбран только stationary snapshot output:
`<output>/executions/<execution_id>/<point_id>/attempt-<local_attempt>/model-help-inputs.json`.
При CalcJob output=`result`, retrieved logical path —
`result/executions/<execution_id>/<point_id>/attempt-<attempt>/model-help-inputs.json`.
File не находится в scientific archive commit/recovery closure и не меняет их
identity. Aggregate help payload на execution/attempt <=8 MiB: writer проверяет cumulative bytes до publish; overrun сохраняет прошлые files и даёт missing snapshot/diagnostic, без остановки physics ради help. Directory — существующий actual `_scientific_attempt_directory`;
используется реально выделенный attempt, без переименования/перезаписи старого.
Для двух точек два files; retry пишет новый attempt directory. Phase не обновляется
в одном file: один закрытый immutable JSON на actual solver-entry, atomic publish
без replace существующего файла. Missing/failed serialization -> used unknown
и help diagnostic; scientific checks/status и arrays не меняются.

Snapshot имеет ровно `{format, context, phase, inputs, origin_bindings}`:

- format const `qcl-negf.model-help-inputs.v1`, phase const `solver_input`;
- context=`{plan_fingerprint, scientific_fingerprint, model_revision, execution_id,
  point_id, attempt, configuration_hash}`. Fingerprints/model_revision — из
  exact frozen plan; execution/point — actual selected loop variables; attempt —
  actual allocated local attempt. Configuration_hash — **declared point passport**
  hash `_point_passport`, не hash actual runtime options; missing -> null;
- inputs — raw InputView без Evidence и без API value_origin. Ровно
  `{path,declared,used,assigning,effective_origin}`; declared/used={status,atom},
  assigning={status,kind,source,rule}, effective_origin={status,steps};
  steps=`[{kind,source,rule}]`, kind=
  `configuration_merge|point_axis|execution_strategy|checkpoint_restore`.
  Применяются общие type/status/unknown invariants этого контракта;
- origin_bindings — claims [контракте value origin](#model-help-value-origin), [] если retained proof отсутствует.

**Не входят** run_uuid, calcjob_uuid, release_id, root source_revision или
bundle identity: standalone Runner не имеет их authority/input. Это не nullable
фиктивные UUID, а отсутствующие поля local contract. API обогащает их ниже.

Capture site — selected Runner `scientific_execution.jl` после применения
`resolve_execution_strategy`, actual point retarget, checkpoint restore (который
может заменить problem) и окончательного `runtime_options`, непосредственно
перед `solution=if … solve_adaptive_production(...)`. Это не snapshot до restore.
Он фиксирует переданные входы; adaptive values после входа в solve не заявляются.
Skipped/preparation-failed и operator-only points не имеют solver-entry snapshot.

Fixed exact mapping для I (names проверены по selected Core f7/Runner238):

| Help leaf | Declared из frozen plan | Used на capture site |
| --- | --- | --- |
| production.energy_chunk | execution.resolved_configuration.production.energy_chunk | runtime_options.energy_chunk, unit 1 |
| physical.lattice_temperature | selected point.temperature_K, unit K | problem.physical.Tᴸ, convert K |
| physical.lo_temperature | selected point.temperature_K, unit K | problem.physical.Tᴸᴼ, convert K |
| physical.interface_roughness_height | execution.resolved_configuration.physical.interface_roughness_height | problem.physical.Δᴵᶠᴿ, convert nm |
| physical.interface_correlation_length | corresponding resolved_configuration leaf | problem.physical.Λᴵᶠᴿ, convert nm |
| physical.impurity_screening_wavenumber | corresponding resolved_configuration leaf | problem.physical.q_s, convert nm^-1 |
| physical.lo_screening_wavenumber | corresponding resolved_configuration leaf | problem.physical.qᴸᴼ_s, convert nm^-1 |
| physical.lo_phonon_energy | corresponding resolved_configuration leaf | problem.physical.ħωᴸᴼ, convert meV |

Other material leaves получают unknown used до отдельного source-verified mapping,
а не universal reflection/name-based conversion. Эти conversions принадлежат
Runner dimensional adapter, не Portal. Fixed screening относится к passed fixed
parameter; density-dependent derived closure без retained evidence остаётся
partial/unknown. Assignment history читается из frozen provenance; restored typed
config с пустой history не восстанавливает её из constructor defaults.

<a id="model-help-retrieval"></a>

#### Retrieval, parser inventory и selected-child enrichment

AiiDA owner changes обязательны в DOC07 coordination, не optional handoff.
Existing CalcJob retrieve tuple для `result/executions` сохраняет этот subtree;
добавлять отменённый root `model_help_inputs.json` в retrieve_list не нужно.
Existing Runner scratch/staging переносит closed result tree целиком; новый file
учитывается в existing tree byte accounting, size guards и file inventory.
На нового scientific-plan или result schema fields не опираемся.

AiiDA parser добавляет отдельный optional output `model_help_index: orm.Dict`
(объявлен в QCLExecutionCalculation spec, exposed существующим RestartWorkChain).
Полный scientific result/selection contract и exit codes сохраняются. Index
строится после initial inventory, **до** ранних scientific result/recovery exits,
чтобы failed/paused attempt мог сохранить help metadata независимо от science.
Его exact detached object:
`{format:'qcl-negf.model-help-index.v1', complete, entries}`;
entries=`[{path,bytes,sha256,execution_id,point_id,attempt,status,reason}]`.
Status=`valid|invalid`; reason=
`ok|malformed|identity_mismatch|too_large|unsupported_version`.
Index не является scientific pass. До payload reads parser проверяет sum inventory sizes matching help files <=8 MiB; превышение даёт complete=false, entries=[], reason передаётся как inventory_incomplete, без чтения payload. Missing file — отсутствующая запись;
invalid file — typed invalid entry без guessed context из payload. Identity
entry для malformed берётся из validated logical path/child, а не мусорного JSON.
Если path не проходит grammar, он остаётся в generic inventory, не help index.

Parser проверяет exact path grammar, <=64 KiB/file, UTF-8/JSON/schema, unique path,
hash/size, local plan fingerprints/model_revision, point membership execution,
attempt равный child.inputs.attempt.value и path attempt, configuration_hash
против frozen point passport. Число entries <=min(plan point count,10000),
index bytes <=2 MiB; incomplete generic inventory/превышение caps -> complete=false,
без доверия частичному help index. Каждый file читается максимум один раз с
size+1 guard, без HDF5/arrays. Invalid optional help не изменяет scientific exit;
service выдаёт used unknown со snapshot_invalid. Parser сохраняет raw retrieved
file для diagnosis и index; исходные scientific arrays/receipts не удаляются.

Для endpoint используется один новый **read-only** actor operation
`get_model_help_input(run_uuid,execution_id,point_id,attempt,calcjob_uuid)` в AiiDA
service и Portal OPERATIONS allowlist. Он внутри одного actor-owned call:

1. `_node(run_uuid)` и existing `_export_child` выбирают exact child **один раз**;
   затем все reads используют возвращённые explicit attempt+child UUID. Не
   перечитывать mutable published selection между metadata и payload read.
2. Читает bounded original frozen input plan; validates point membership и
   local configuration passport. Get-export-plan semantics для retrieved plan:
   corrupt/different существующий snapshot не заменяется original/current.
3. Находит ровно одну valid help-index entry exact child/execution/point/attempt;
   сверяет generic inventory path/size, читает только этот retrieved object,
   проверяет raw SHA256/size и local context повторно. Metadata не открывает
   arbitrary filesystem path. Handle закрывается в actor до возврата bytes.
4. API context.run_uuid=node.uuid, calcjob_uuid=child.uuid, attempt=child input;
   execution/point из validated plan/request; остальные local fields совпадают
   со snapshot. Никакой UUID из Runner file не принимается.
5. Release_id только child/owning workflow immutable inputs; graph/bundle binding
   только retained release receipt этого selected execution. Отсутствие ->
   source_binding_missing, даже если current deployment знает другой release.
6. Portal получает detached scalar projection+hashes, генерирует Evidence по
   closed snapshot bytes/JSON Pointers; validator [контракте value origin](#model-help-value-origin) формирует actual
   value_origin либо unknown. Static reference source остаётся reference-only.

Run API context attempt/calcjob_uuid теперь **обязательны после успешного child
selection**. Nullable остаются только missing configuration_hash и binding
identity fields. Невозможность выбрать child — existing 404/409, не fabricated
context. No-snapshot/invalid snapshot для уже выбранного child -> HTTP200,
inputs.used unknown, typed `input_status` ниже; existing actor outage ->503.

Run view получает ещё одно обязательное поле
`input_status={status,reason}`: status=`available|unavailable|invalid`, reason=
`ok|snapshot_missing|snapshot_invalid|point_not_executed_by_selected_child|inventory_unavailable|inventory_incomplete`.
Это отделено от documentation binding и scientific status. Existing historical
plan даёт declared при available frozen input; отсутствие used snapshot не
ломает run/submit. Origin without proof остаётся unknown независимо от snapshot
presence. На client user-provided path нет.

Retention: snapshot живёт в original CalcJob retrieved repository вместе с его
inventory/index и не удаляется checkpoint prune. Retry child имеет собственный
retrieved namespace. Completed point, импортированный из prior archive в retry,
не получает новый snapshot с новой attempt identity. Для point row с
record.attempt<selected child attempt endpoint возвращает
point_not_executed_by_selected_child; пользователь может явно выбрать original
child/attempt для его used help. Автоматического обхода других children и
приписывания старого input retry child нет. Старые snapshot/plan bytes не меняются.

Standalone Runner produces тот же local file с allocated attempt; он читаем
без AiiDA, но не превращается в run-bound API context без trusted selected child.
Никакого нового UUID CLI input или authority registry не требуется. Если future
capture/source receipt отсутствует, это локальный unknown, не основание придумывать
AiiDA identity или scientific result.

<a id="model-help-compatibility"></a>

#### Unknown example и совместимость

Пример — короткая иллюстрация Origin части authored **reference help**, не полный schema-valid fragment и не observed S1 run:

```json
{
  "path": "physical.interface_roughness_height",
  "reference_value_origin": {
    "origin": {"status": "unknown", "kind": "unknown", "locators": [],
    "note": "Источник конкретного Δ=0.10 nm в reference parameter set не подтверждён; DOI геометрии его не устанавливает."}
  }
}
```

При известной assignment к public Research YAML можно показать этот source
отдельно. Если есть только frozen plan, `declared` содержит 0.10 nm с evidence,
`used` остаётся `{status:'unknown',atom:null,evidence:null}`. Unknown не блокирует
сам по себе exploratory вариант, не становится published/measured и не доказывает
scientific acceptance. У typed energy_chunk=64 отдельно видны constructor
default и `schema default: not_assigned`; отсутствующая history не выбирает первый.

v1 consumer принимает только известные const format и проверенные bytes/hash;
unknown major/неподдерживаемый format -> incompatible, без best-effort reinterpretation.
Никакой совместимости по package `0.2.0`, `transport-contract-v2`, одинаковому
fragment ID или числу. Default rule — exact graph equality. Старый run с известным
graph использует его retained bundle; если bundle отсутствует — unavailable.
Future explicit compatibility mapping потребует отдельного reviewed contract;
сегодня его нет. Unknown source run остаётся unbound, даже если release_id совпал
по тексту с current label. Redirect на latest не исправляет несовместимость.

<a id="model-help-build"></a>

### Allowlist, пределы и сборка

Input allowlist build: selected component `docs/src/**`, explicit docstring/type
source paths для fixed slice, Contracts schema resources, explicit Research
public configuration + `docs/help/value-origins.json`, reviewed Root operator
chapter. Path list точная и versioned в recipe; glob всего worktree/archives нет.
Наличие private path в source metadata не разрешает публикацию его basename.

Public output allowlist: перечисленные manifest HTML/CSS/JS/fonts/math/search,
images SVG/PNG/WebP, approved JSON fragments/catalog и optional inventory.
Запрещены symlinks, абсолютные paths, `..`, backslash, NUL/control chars,
URL-decoding traversal, dotfile directories, private inventory, .git, .aws,
logs/receipts с private targets, arrays/HDF5, depots, source maps с machine paths,
credential/query/token bytes. SVG/HTML/JS только из selected reviewed recipes и
public authored source; нет dynamic user HTML. Статическая карточка plain text,
React не рендерит arbitrary HTML. Links на первоисточники не загружаются автоматически.

Пределы proposed публичного catalog: manifest<=2 MiB, fragment<=32 KiB,
<=256 fragments/пилот, max help response<=64 KiB. Files listing содержит byte counts;
любой overrun — replan соответствующего artifact, не truncation посреди JSON.
Runtime reads используют меньший из этих пределов и existing actor/API limits.
Actual HTML/assets budget DOC04 задаётся по measured BUILD admission и manifest;
этот design не утверждает размер или скорость ещё не собранного corpus.

Выбран **existing Documenter 1.17.0** с root Julia 1.13.0 manifest. Hub/catalog
collector — небольшой source-only adapter на existing locked Deno toolchain из
root/platform flake, без нового generator dependency или network access. JSON
Schema extraction использует normal JSON, remote `$ref` не fetch. Для Julia
fixed slice DOC06 распознаёт лишь заявленные source constructs; unsupported
dynamic expression возвращает partial/unknown и source locator. Target modules,
extensions/plugins/config evaluation не импортируются. `objects.inv` и готовый
Documenter search index допускаются как generated link/index inputs после
проверки их version/schema в DOC04, не как provenance чисел.

Prerequisites DOC04 (проверить, не запускать здесь):

1. Новый published clean root с DOC02/Contracts/help source gitlinks и locked
   workspace; `sourceGraph()` до/после build совпадает. Recipe/source hashes и
   Project/Manifest hashes входят в receipt.
2. Проверенный existing Julia executable/depot matching manifest; exact installed
   version/tree Documenter и package import effects. Deno executable/version/store
   identity сверяются с selected root/platform flake lock. Сейчас installed paths
   и binary versions **не измерены**, нельзя назначить найденный PATH `deno` pin.
3. Прочитать source/API **pinned** Documenter для local math/fonts/search и theme;
   сохранить fixed-light без switcher/OS auto-dark, local assets. Не выдумывать
   HTML kwargs по документации latest. Required CDN/font/math downloads должны
   быть закрыты локальными pinned assets в recipe; отсутствие pin блокирует
   этот render, не ведёт к установке latest.
4. Импортирующий render выполняется только в DOC04 BUILD envelope на fresh
   builder admission. Existing docs command с QCL_NEGF_PROJECT использует root
   workspace. Без него standalone task может instantiate другую композицию.
   Не использовать full `deno task test` или CI как обёртку pilot.
5. Проверить все executable jldoctest/@example/import/precompile effects до
   render. Обычные fenced snippets — текст. Solver/SCBA/Poisson в build/view
   запрещены; executable examples, если нужны, получают отдельный bounded
   contract. Нет изменения scientific gates ради успешной сборки.
6. Three pilot slices: Core физическая глава/SCBA route, Runner API/config route,
   Root operator recovery chapter. Небольшой reviewed operator HTML создаётся
   existing Documenter из authored public chapter; весь исторический deployment
   runbook или execution receipts автоматически в public docs не копируются.

<a id="model-help-serving"></a>

### Serving, anchors, offline и UI

Owning Platform передаёт immutable documentation bundle path; Portal монтирует
его **на `/docs` до последнего `/` static mount**. Nginx может продолжать
существующий `/` proxy: отдельный nginx alias в pilot не нужен. Это сохраняет
same-origin headers/CSP и не добавляет альтернативный auth/serving путь.
Нет serving arbitrary filesystem root или user-controlled directory.

Public docs содержат только public allowlist source; auth API остаётся protected.
Request `/docs/<rev>/missing.html` -> docs 404, не Portal index; `/api/v1/…`
не попадает в docs. Даже при отсутствующем documentation directory prefix
резервируется и возвращает docs unavailable/404 до Portal catch-all. Startup
binding проверяет manifest/hash/schema once без Julia; ошибочный docs bundle
не должен выключать unrelated API или давать ложный help pass.

`/docs/<rev>/…` immutable URL получает immutable cache/ETag по payload hash;
API view сохраняет existing no-store. `/docs/current` — необязательный explicit
deployment redirect к конкретному source revision, отдельно опубликованный с
activation receipt. Run-bound ссылки его не используют. Не менять pointer
самовольно после preview acceptance.

Existing headings/explicit @id сохраняются; DOC02 anchors проверяются только
после выбора соответствующих gitlinks. Fragment anchors не передаются серверу:
old `#anchor` сохраняется реальным alias element в owning HTML. File aliases
также реальные pages/redirects; их targets остаются в той же версии, если
явная migration не заявлена. Retained old bundles обслуживаются по exact URL;
удалённая неизвестная версия -> явный 404/unavailable, без перенаправления на
current. Source links могут идти на exact public commit и требовать интернет;
чтение главы, math/fonts/search/direct anchors от него не зависит.

Offline означает cold-cache browser с заблокированной **внешней** сетью при
доступном локальном origin; при копировании bundle поддерживается локальный
HTTP static preview. `file://` не обещается: search/fetch может иметь другие
ограничения. Все internal links и assets relative к version prefix; без CDN,
external fonts/search analytics или service worker, подмешивающего другую версию.
CSP не ослабляется глобально ради docs. Если pinned math renderer конфликтует
с existing CSP, DOC04 подбирает source/asset recipe; новая trust/CSP exception
возвращается на review до publication.

DOC07 UI: светлая «Модель и источники» рядом с существующей submit form и на
странице selected run/point. Статический reference доступен без запуска plan;
used карточка требует точных retained selectors/binding. Сохраняются введённые
plan bytes и submission behavior. Панель показывает summary, declared/used,
assignment/value origin и full link; full docs открываются отдельной страницей,
iframe и новый field configurator не нужны. Keyboard focus, close/return,
contrast/loading/error/unknown states проверяет DOC05. Простой просмотр не
вызывает resolve, derive, hash full result, Julia или solve.

<a id="model-help-negative-controls"></a>

### Приёмка: пять обязательных отрицательных случаев

Ниже **будущие** проверки/controls, сегодня они не исполнялись.

| Случай | Инъекция/вход | Требуемое наблюдение | Positive control / evidence |
| --- | --- | --- | --- |
| Wrong release | Run receipt связан с graph A, установлен bundle B с тем же fragment ID | binding incompatible/wrong_release; used help B не показан и не fallback current. Если retained A есть, разрешён exact A | Совпадающие receipt/graph/manifest/fragment SHA дают bound; сохранить JSON/network/UI receipts |
| Missing source | Manifest/fragment обещает known PublicRef, но выбранный Git blob/selector отсутствует или hash иной | Build binding validation отказывает этому required fragment/bundle; не создаёт ссылку якобы known. Historical run без source receipt возвращает source_binding_missing | Существующий exact blob + selector проходит source check; fake missing source control не смешивать с допустимым unknown value origin |
| Private path | История assignment `/private/site/…`, traversal/symlink либо source-map с machine path в output | Публичный build исключает/отклоняет unsafe payload; dynamic assignment redacted без absolute path/basename. API selector не допускает file path | Public Research repo-relative source разрешён; проверить exact response bytes и output manifest, без вывода secret contents |
| Unknown origin | Reference A=0.10 nm имеет known publication; run override B=0.15 nm без origin, либо равное 0.10 с другой assignment/T/composition | Static origin подписан reference-only; actual declared/used value_origin unknown/override_unbound или conditions_unbound. Equality не переносит origin | Exact A/context/phase с retained public source-binding receipt -> bound; missing receipt -> unknown даже при равном числе; пустая history energy_chunk=64 остаётся unknown assignment |
| Catch-all routing | Direct `/docs/<rev>/…#anchor`, missing docs asset/page, docs directory absent, API URL и root UI | Valid direct page/anchor работает; docs misses дают docs 404, не Portal HTML200; API auth и existing root UI сохранены | Cold-cache direct known page + asset, authenticated API и root navigation; route tests + browser offline/light receipts |

Дополнительные bounded controls: unsupported format/version, wrong manifest hash,
nonexistent fragment, malformed schema, no/multiple selected point, generated
axis override, auto_exact strategy, historical run, unavailable bundle, target
module sentinel без side effect при DOC06 source-only extraction. Request/load
help не увеличивает счётчик запуска solver/build. Никаких numerical accuracy
claims из этих tests. DOC05 отдельно проверяет cold cache, offline math/fonts/
search, dark/light OS + saved preference при неизменно светлом сайте, focus и
потребление exact bundle. DOC04 build exit не заменяет эти observations.

<a id="model-help-point-retry-controls"></a>

#### Запланированные controls: origins, точки и retry

| Case | Exact input и ожидание |
| --- | --- |
| R1 override/context negative | Known reference A=0.10 nm; used B=0.15 nm без receipt -> actual origin unknown, static reference-only. Повтор с B=0.10 nm, но другой assignment или T/composition -> также unknown. |
| R1 positive | Frozen synthetic snapshot содержит exact A/context, phase и retained binding claim с verified public source hash/last-assignment capture; все conditions имеют evidence -> bound. Удаление любого proof/condition или used override после declared -> unknown. Fixture не объявляется production run/science evidence. |
| R2 two points | Один frozen execution E, P1/P2 с разными axes; child C1 attempt1. Два logical paths P1/attempt-1 и P2/attempt-1, distinct hash/used values, local contexts без UUID. Selected actor enriches обе записи run R/C1/1; запрос P2 не получает P1. |
| R2 retry | C1/1 сохраняет P1 и interrupted P2 input; C2/2 восстанавливает P2, completed P1 imported. P2/C2 -> его attempt2 snapshot; P1/C1 -> исходный attempt1; P1/C2 -> point_not_executed_by_selected_child, used unknown. C1 raw/index остаются доступны. |
| R2 identity/tamper | Snapshot P1 либо local attempt1 под path P2/attempt2, UUID injected additional property, wrong plan SHA или payload hash -> invalid; actor UUID не берётся из payload; scientific result не повышается и raw сохраняется. |
| R2 partial/missing | Killed/skipped point без snapshot, missing/incomplete index, malformed >64 KiB snapshot -> unknown used с typed reason. Correct generic inventory/valid sibling остаётся доступным, если complete; не сканировать HDF5/другие children. |
| Standalone | Runner получает только plan/execution/attempt, produces local file без AiiDA UUID/release identity; local metadata valid, run-bound API невозможен без actor child. |


## Приёмка и ближайшие работы

### Что обнаружено в текущей физической документации

Это целевой static audit активных параметров, нескольких моделей/статусов и
публикационного пути, не повторная проверка всех уравнений solver. Независимые
агенты читали один неизменяемый source набор. Ниже не установлена неверность
материальных чисел и не доказана применимость всей модели к 70 K.

| Наблюдение | Source locator | Решение и ограничение |
| --- | --- | --- |
| Модель ядра рассеяния объяснена, но источники выбранного material набора не связаны с отдельными значениями | Core `src/domain/presets.jl:46–79`; `theory/02_reference2019.md:48–51`; research passport `physical` | Паспорта ΔEc, m, ε, LO/acoustic inputs; условия/материальная аппроксимация. Не объявлять данные неверными или fitted по одному отсутствию citation |
| Gaussian IFR имеет формулу и смысл, но Δ=0.10 nm и Λ=9 nm не имеют value-level primary locator | Core `presets.jl:23–24`; `theory/08_kernels.md:47–61`; research `reference-2019-70k.yaml:75–76` | Сохранить объяснение; добавить origin значений и convention корреляционной длины. RMS/Λ другой статьи нельзя переносить без её определения коррелятора |
| Fixed κ=0.20 nm⁻¹ не является derived Debye/TF result | Core `presets.jl:25–26`; `physics/models.md:23–46,248–251`; `model_operators.jl:7` | Различить fixed/derived screening, 2D/3D, electron/bath T и density. Формулы известных closures не доказывают выбор fixed числа |
| Alloy включается другим config source с ΔV=0.60 eV и Ω₀=4.5168×10⁻²⁹ m³ | Research `config/policies/analytical-diagnostic.yaml:22–26`; Core `theory/08_kernels.md:80–95` | Нужны source/convention elementary volume и контраста; это model change. Историю Ω₀ нельзя реконструировать догадкой по похожему lattice volume |
| **P2 docs/code:** описание approximate return опускает необходимый режим | Core `theory/09_scba.md:84–91`; `src/domain/numerical_convergence.jl:383–384` | Указать `adaptive_working` **и** enabled diagnostic quality, дальнейшие gates. Сценарий `research_continue+enabled` не даёт описанного early return; это mismatch документации, не новый numerical verdict |
| **P2 docs scope:** оптика универсально заявляет отсутствие e–e, хотя SCBA допускает SPPA | Core `theory/18_optical_response.md:85`; `src/numerics/reference/kernels.jl:628–631`; `src/physics/optical_response.jl:494–498` | Ограничить e–e утверждение выбранным baseline; отдельно оставить отсутствие δΣ/vertex. Это не доказанная ошибка gain |
| Optical background εb по default берётся из static εs | Core `src/physics/optical_response.jl:306` | Объяснить frequency-independent background и область применимости; не подставлять новый ε автоматически ради улучшения совпадения |
| Core reference defaults 200 K/56 mV и selected study 70 K — разные контексты | Core `presets.jl:20–22`, `theory/02_reference2019.md:43–45`; research passport `68–69` | Показывать контекст preset/example/used point; не менять независимый Core default только ради совпадения страницы текущего исследования |
| Origin winning YAML не даёт научное происхождение свойства, generated axis assignment может обходить history | Runner `configuration.jl:214`, `infrastructure/scientific/definitions.jl:410–421`, `application/scientific/planning.jl:65` | Сохранить file origin отдельно; карточка T/V берёт actual point/axis. Исправление связано с CR07 основного review |

Положительная основа: `08_kernels.md` объясняет случайный potential→covariance
kernel, `models.md` — assumptions/размерность и пределы расширений,
`developer/traceability.md` — stable equation→symbol links. `physical-atlas.md:20–26`
честно отличает отдельные иллюстрации от рабочего самосогласованного состояния;
это различие переносится в UI. `constants.jl:42–61` отделяет размерные
константы и производный масштаб: их нельзя превращать в fitting controls.

Связанные файлы:
[kernels](../../components/QCLNEGF.jl/docs/src/theory/08_kernels.md),
[models](../../components/QCLNEGF.jl/docs/src/physics/models.md),
[SCBA](../../components/QCLNEGF.jl/docs/src/theory/09_scba.md),
[optical response](../../components/QCLNEGF.jl/docs/src/theory/18_optical_response.md),
[presets](../../components/QCLNEGF.jl/src/domain/presets.jl),
[research inputs](../../components/qcl-negf-research/config/model/reference-2019-70k.yaml).

### Что уже есть для локального HTML и что отсутствует

Root `ops/ci.ts:70–75` уже собирает оба Documenter сайта с общим locked
Julia workspace; `julia/Manifest.toml:138` выбирает Documenter 1.17.0.
Поэтому новый documentation toolchain не нужен. Standalone Runner docs
`Project.toml:9` выбирает Core `v0.2.0`; для release использовать root
workspace/gitlinks, иначе документация может описывать другой composition.

В прочитанном publication пути HTML docs не включены: portal
`api.py:449–451` раздаёт React assets, platform `application.nix:114`
проксирует `/`. Нужен static artifact + отдельный prefix до catch-all route.
`objects.inv` Documenter может использоваться для generated anchor/link
index; он не содержит готовой научной атрибуции чисел.
[Documenter inventory](https://documenter.juliadocs.org/stable/lib/internals/writers/#Inventory).

Doc build импортирует Julia-пакеты, может компилировать/precompile workload
и исполнять doctests/examples. Текущее `doctest=true` не доказывает исполнение
обычных fenced `julia` snippets: в просмотренных источниках executable
`jldoctest/@example` blocks не обнаружены. Примеры должны получить отдельную
проверку с конечным бюджетом; не включать expensive solver runs скрытно.
[Documenter doctests](https://documenter.juliadocs.org/stable/man/doctests/).

Default HTML требует отдельной проверки local assets и theme behavior;
`prettyurls=false` не делает offline closure или fixed light автоматически.
На собранном output надо проверить math/search/fonts и прямые anchors при
запрещённой внешней сети и тёмной настройке ОС. Сегодня эта сборка/проверка
не выполнялась.

### Поэтапная реализация

Первый небольшой срез: IFR, fixed screening, LO phonons и material masses/
band offsets для выбранной 70 K постановки. Для каждого показать formula
origin, value origin, effective input и implementational scope. Затем
распространить контракт на все активные свойства, scientific criteria и
advanced variants; отсутствие mapping должно явно обнаруживаться.

Приёмка: из поля формы за два действия доступно полное объяснение; override
виден; неизвестный источник честно показан; direct Julia/API и UI одинаково
интерпретируют модель; offline HTML/search/math работают; light theme
сохраняется при dark OS; статьи/формулы/числа не ошибочно смешаны.

Научный аудит проводится по активным model choices, а не только по names:
formula/assumptions → dimensional inputs/normalization → code → observable →
criterion → ограниченное свидетельство. Для численного default нужны роль
и основание, но не выдуманная научная статья.

S01 при 0 mV/period и 70 K остаётся первым научным рубежом. Полное оформление учебника и
hosting всех docs не должно стать его prerequisite: достаточно объяснимой
постановки и источников используемой модели. Расширение help идёт поэтапно.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Учебная основа и полная физическая справка уже существенны | Core theory/models/atlas/traceability и Documenter build | Полнота каждой derivation/API не доказана | Сохранить |
| Требуется связать значения с их научным происхождением и overrides | Приведённые presets/passports/resolver locators | Неверность чисел и история calibration не установлены | Изменить |
| Два описания расходятся с текущими code conditions/scope | SCBA approximate gate и optical e–e scope | Runtime и numerical correctness не проверены | Изменить |
| Локальная HTML публикация реализуема без нового live service | Existing build, static HTML, serving boundary | Offline/light behavior и стоимость сборки не измерены | Дополнительно измерить |
| Равновесный рубеж 0 V / 70 K пока не следует из документации | Разделённые source/check/illustration статусы | Нет научных runs в этой задаче | Данных недостаточно |

<a id="model-help-doc07-v1-clarifications"></a>

### Уточнения DOC07 v1: matrices и retained projection

Это уточнение закрывает технические branches принятого model/source help
contract. Пять форматов и перечисленные поля, owning boundaries, scientific
model/criteria и полномочия не меняются. Schema-valid object сам по себе не
доказывает source/release/origin binding.

В каждом `facts` fixed slice присутствуют все десять классов. Несколько facts
одного класса допустимы для разных authored contexts, в частности schema,
typed constructor и example defaults; ограничения «ровно десять» и uniqueness
по name нет.

Все поля Origin обязательны. Для status=known kind — один из publication,
measurement, interpolation, fit, research_assumption, code_policy. Schema не
вводит обязательный DOI или обязательный locator для каждого kind; known
research_assumption с locators=[] требует непустую note, называющую owning
assumption. Для unknown: kind=unknown, locators=[], непустая note. Для
not_applicable: kind=not_applicable, locators=[]; note остаётся plain-text
string. Unknown не заменяется not_applicable из-за отсутствия данных.

Atom quantity имеет numeric value и непустую строку canonical unit. Integer,
number, boolean, enum и null имеют соответственно JSON integer, number,
boolean, string и null value; boolean не numeric/integer. Их unit по форме
string|null; каноничность и применимость единицы доказывает owning dimensional
mapping, без нового unit registry. Для dimensionless canonical unit — `1`.
Finite JSON boundary отклоняет NaN/Inf и другие nonfinite values до schema;
known-null отличается от unknown/missing.

| ValueOriginView.status | origin | binding | reason |
| --- | --- | --- | --- |
| bound | Origin known | Nonnull ValueOriginBinding | ok |
| unknown | Origin unknown/kindunknown/[]/непустая note | null | origin_not_recorded, override_unbound, conditions_unbound, source_unbound или value_unavailable |
| not_applicable | Origin not_applicable/kindnot_applicable/[] | null | not_applicable |

Branch bound дополнительно требует всех четырёх retained-proof условий
контракта value origin. Missing proof даёт accepted unknown reason или отказ
проверки attempted bound record; corrupt/contradictory identity/hash/context
claim не сохраняется как bound. Scientific value/context mismatch с reference
может быть законным override и даёт unknown, а не фиктивную атрибуцию.
Никакого backfill из equality, filename history или current defaults нет.

| binding.status | Допустимые reason | fragment |
| --- | --- | --- |
| bound | ok | Nonnull exact descriptor id/url/sha256 |
| unknown | source_binding_missing | null |
| incompatible | wrong_release или unsupported_version | null |
| unavailable | bundle_missing или fragment_missing | null |

Bound требует nonnull retained release_id, release_manifest_sha256,
source_revision и bundle_sha256, а также проверенную цепочку selected release
receipt → exact graph → bundle → fragment bytes. На unbound branches каждый
неизвестный identity scalar равен null; уже известные verified retained scalars
не обнуляются только из-за статуса. Trusted actor run_uuid/calcjob_uuid/attempt
обязательны после child selection независимо от availability docs/snapshot.
Configuration_hash nullable только при отсутствии declared point passport.

| input_status.status | Допустимые reason |
| --- | --- |
| available | ok |
| invalid | snapshot_invalid |
| unavailable | snapshot_missing, point_not_executed_by_selected_child, inventory_unavailable или inventory_incomplete |

Input metadata availability, documentation binding, value_origin и scientific
status независимы. Invalid/unavailable snapshot не заполняет used из plan или
current defaults. Available означает проверенную metadata выбранного child;
это не обещание полноты каждого scalar mapping или scientific pass.

Публичный input path slice берётся только из inputs[].path exact requested
Fragment v1 того же retained selected source context. Для этого owning adapter
проверяет exact fragment и Bundle manifest bytes, descriptor id/file/hash,
manifest digest и graph, привязанные retained source/release receipt именно к
выбранному run/execution. Это existing bundle/fragment artifacts, а не новый
mapping registry или sidecar format. Detached internal validation inputs
содержат эти bytes/selection evidence, не unverified status booleans.

Если exact retained fragment/manifest/mapping proof отсутствует, inputs=[].
Context и input_status сохраняют доказанные selected-child факты. Current
fragment, global leaf list, first fragment, имя поля или весь plan не заменяют
missing mapping. Отсутствие source binding само по себе не даёт права выбрать
source context по текущему deployment.

Если mapping доказана, declared и used оцениваются независимо по своим retained
evidence. Fragment descriptor остаётся null на unbound documentation branch.
Unserved/missing public bundle assets не обнуляют verified used metadata из
snapshot этого child, когда exact retained fragment/manifest доступны для
mapping. Missing used snapshot оставляет used unknown; declared при этом может
быть known из exact frozen point configuration. Available/ok с inputs=[]
допустим, когда snapshot valid, а безопасной path mapping нет. Reference origin
остаётся reference-only; actual origin по-прежнему требует отдельного proof.

Для public emission этого pilot выбран query-free locator subset. URI parser
допускает только schemes https/doi, запрещает userinfo/credentials и control
characters; https должен быть корректным absolute URI. Presence query delimiter
или query component, включая пустой `?`, блокирует emission affected artifact.
Query не вырезается, locator не переписывается и не fetch. Одного format:uri
недостаточно; arbitrary secret scanner или новый trusted URI registry не нужен.

Источник locator — authored annotation/owning public source exact revision/hash
из versioned input allowlist уже reviewed recipe. Evidence этого public-content
review сохраняется в owning source/build review receipt. Query-free URI сама по
себе не доказывает отсутствие private token в path, scientific attribution или
measurement: public source review и output guards остаются обязательны. Без
такого review evidence artifact остаётся unverified/rejected для publication.
Query-bearing locator не публикуется в pilot; дальнейшее harmless-query support
требует отдельного reviewed technical recipe contract, а не выбора текущего
исполнителя или скрытой эвристики. Это ограничение публичного payload не меняет
scientific model или numeric value.

Contracts использует private pure binding validation над finite schema-valid
objects и bounded detached retained evidence. Она не выбирает actor child,
не выполняет filesystem/network/ORM/Julia/derive, не вводит новый serialized
receipt/capture API и не требует __init__ re-export. Existing loader/schema API
остаётся достаточным для shape validation; source/release/origin/full-chain
claims требуют отдельного proof, а не evidence.length>0.
