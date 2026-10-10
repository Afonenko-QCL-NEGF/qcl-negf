# Физическая документация рядом с исследованием

Статус: требования пользователя и предлагаемый способ реализации, 2026-10-09.
Аудит относится к root `bce0aee` и его gitlinks. Сайт и Julia HTML docs
сейчас не изменены/не собраны; новые расчёты не выполнялись.

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
