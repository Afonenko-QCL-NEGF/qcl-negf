# DOC04 recipes D2 — независимый source-only review

Вердикт: **REQUEST_CHANGES — два узких дефекта контракта API**. Реализация medium I по замороженному тексту ещё не однозначна: для operator указан нетипизированный пустой `modules`, а обязательный `sitename` отсутствует в точном наборе pilot kwargs. Оба исправления технические, в пределах принятого DOC04; нового решения о физике, доверии или разрешения BUILD они не требуют.

Это проверка исходников и проектного контракта. Julia, импорты, Documenter, тесты, сборки, solver, сеть и парсеры не запускались. Изменены только этот отчёт и его identity в `/tmp`. Продуктовые исходники и checkpoint не изменялись.

## Неизменяемые входы

Рабочий root: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`, HEAD `514cd9707a32cde60c630d60986973a898d35b18`; selected Core `e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee`, Runner `1acc165650fd4f4c2d49605cc679f90e3f6fcdae`. Проверенные owner docs paths не имели локальных изменений. Gitlinks HEAD задают состав; новый lock-файл не создавался.

| Вход | SHA-256 |
| --- | --- |
| `/tmp/qcl-doc04-design.md` — принятый первичный D | `77ee8593655f98b2e66d762620279ba6ac7ec7da126c62a2ccbd56a0262bf12b` |
| `/tmp/qcl-doc04-design-review.md` — первичный R | `6caa4f15035e6a9f564d1ec86f14ecd64bbd31d73457556327e090e9d6628164` |
| `/tmp/qcl-doc04-recipes-design.md` — D1, сохраняемый D2 | `008650e7c9ff98bdaf38a3450d2b3b13818409795c92738d0a9dbddaba2c2505` |
| `/tmp/qcl-doc04-recipes-design-v2.md` — предмет review | `ce582cc394d7dd70971c2a25929bf9362aad7d829403f1e2e0fba68a8ff65610` |
| `/tmp/qcl-doc04-recipes-source-effect-ledger-v2.md` | `39eb90584c32d883e2db0bab32a500a31f7a6427eb0260c54b22315741fe77a4` |
| `/tmp/qcl-doc04-recipes-identity.json` | `5938cc4edbd0f34f8911ed73bff72ccfbe0ba697c38f862251faa43eb02b3d1e` |
| `/tmp/qcl-doc04-recipes-continuation-witnesses.txt` | `38d6cc0f65c9b44eea7322a71d55bc04bff8ae2e84202726184b2f96c2a3c2c8` |
| `components/Core/docs/make.jl` (далее Core make) | `edafb4e03b0fd9982039267dc24ba7c6332551f7e3770fca20b35fc8dae9380f` |
| `components/Runner/docs/make.jl` (далее Runner make) | `0749b9989ce07c34034dddac2fe8127a9ecca72d43105425928f7468dae16cbc` |
| pinned `Documenter/AXNMp/src/documents.jl` | `67ded455a9d8881b6fe3cf4a4cfbc97a992e27cd8e31ad3d28de23cbc3578e06` |
| pinned `Documenter/AXNMp/src/html/HTMLWriter.jl` | `72b261cbef5e06e9edc4159c038d740b5f5372134f9d75db06eeb35b894b29dd` |
| pinned `Documenter/AXNMp/src/expander_pipeline.jl` | `601553820653a52b8c851fdc2355c04a8c5350e70aeeb62dac8e92a2a84664ab` |

Pinned Documenter находится в root `.build/local-julia-int01/depot-1/packages/Documenter/AXNMp`. Его наличие — свидетельство прочитанного API, не признание полной toolchain/cache identity для BUILD.

## Блокирующие замечания

### R1. Literal `modules=[]` несовместим с pinned keyword type

Локаторы: D2 строки 46–50; D1 строки 90–100; pinned `src/documents.jl:420`.

D2 явно закрепляет для operator `modules=[]`, а D1 повторяет это в описании и точном наборе kwargs. В выбранном Documenter объявлено:

```julia
modules::Union{Module, Vector{Module}} = Module[]
```

Julia literal `[]` имеет тип `Vector{Any}` и не удовлетворяет этому keyword type. Даже с оговоркой D1:108 о нерunnable шаблоне записи две явные инструкции оставляют implementer неверный конкретный аргумент. Такая ошибка может остановить operator recipe до HTML render; это дефект источника контракта, а не доказанный runtime failure.

Минимальная коррекция: закрепить **`modules=Module[]`** во всех operator упоминаниях; `checkdocs=:none` и граф из двух страниц сохранить. Можно было бы опустить keyword и использовать типизированный default, но для независимого medium I предпочтителен один явно зафиксированный вариант `Module[]`. Никакого импорта owner module это не добавляет.

### R2. Точный pilot contract не задаёт обязательный `sitename`

Локаторы: D1 строки 96–105, D2 строки 46–51, pinned `src/documents.jl:427`, `src/html/HTMLWriter.jl:823–825`; существующие Core/Runner `docs/make.jl`, вызовы `makedocs`.

В точном наборе pilot kwargs нет `sitename`. Document constructor по умолчанию устанавливает пустую строку; HTML renderer явно требует непустую строку:

```julia
!isempty(doc.user.sitename) || error("HTML output requires `sitename`.")
```

Новый operator recipe не может унаследовать это поле из существующего owner make. Для Core/Runner сохранение существующих значений возможно, но также должно быть явно совместимо с названным «exact public kwargs» списком. Это нельзя оставлять необъявленным выбором medium I.

Минимальная коррекция: добавить `sitename` в точный контракт: Core **`"QCLNEGF"`**, Runner **`"QCLNEGFRunner"`** (оба уже стоят в выбранных make); operator **`"Документация оператора"`**, совпадающий с уже замороженным заголовком generated index. Непустое имя — презентационное поле, не новый scientific/model/trust contract. Зафиксировать один literal для operator в узкой авторской коррекции; не начинать BUILD для проверки этого дефекта.

## Остальные существенные границы

**Default и pilot.** Исходные Core/Runner recipes действительно импортируют owner и Documenter, задают DocMeta setup с owner/Unitful/LinearAlgebra, используют doctest=true, checkdocs=:exports, warnonly=false и имеющиеся page vectors. D1/D2 сохраняют эту ветку при unset/empty profile, вводят отказ неизвестного profile до импортов и отдельный pilot-v1 с doctest=false. Сохранение default doctests не означает их разрешённый запуск в этом review или pilot.

**Namespace и страницы.** Сохранение owner modules и целых Core/Runner pages vectors совместимо с CurrentModule и `@docs`. `pagesonly=false` сохраняет scope unlisted Markdown. Typed `scattering_options(::ResolvedRunConfiguration)` в Runner `docs/src/api/public.md:224` требует существующий module context; D не предлагает переносить owner API в Root. Operator имеет свой `Module[]` после R1 и checkdocs=:none. Это достаточное разделение source namespace.

**Отсутствие скрытого numerical execution.** По фиксированным Markdown подтверждён ограниченный отрицательный scan executable fences; обнаружены `@meta` и `@docs`, включая typed expression. Это не доказывает безопасность docstrings/imports. В pinned expander pipeline `EvalBlocks`, `ExampleBlocks`, `REPLBlocks`, `SetupBlocks` входят в nested pipeline, а `DocsBlocks` получает docstrings выбранных modules. D2 правильно снимает более сильное предположение D1 и оставляет неизвестную вложенную/динамическую документацию и import/include/extension/cache closure hard BUILD blocker. Прочитанные owner imports и Core precompile workload дополнительно объясняют, почему нельзя запускать import как дешёвый «probe»: workload включает численные операции; отсутствующий cache может изменить фактические эффекты. Здесь не утверждается запуск SCBA/Poisson или отсутствие всех прочих эффектов.

**Root gate и процессы.** Абсолютные ROOT/SOURCE/BUILD и проверка VERSION/active project до owner imports конкретны; make guards не подменяют внешний admission. Root preflight должен проверить source graph, toolchain/cache/effect identity, assets и admission до Julia spawn. Caller boolean/наличие receipt не даёт права импортировать. План задаёт прямой argv с startup/history disabled, bounded concurrent drains stdout/stderr и конечные terminal receipts. Он явно исключает существующий unbounded-buffer process helper и не выдаёт kill непосредственного child за доказанное завершение descendants: последнее остаётся обязанностью admitted внешнего job/cgroup. Offline environment flags сами по себе не изоляция сети. Эти границы согласованы и не требуют новой trust registry.

**Operator и fixed light.** Byte-exact staging замороженного recovery source, literal index, два navigation targets, prettyurls=false и существующие anchor routes конкретны. Light CSS, отсутствие OS-dark alternative, отключённый runtime math и последующая контролируемая обработка pinned dependencies согласуются с принятым D; `mathengine=nothing` не выдаётся за доказательство отсутствия всех CDN/head ссылок. Это контракт будущей реализации, не проверка собранной страницы или браузера.

**BUILD prerequisites.** Final adapter API CPP2, точные assets/fonts/OFL/license/CSS bindings, полная Documenter/toolchain/cache/effect identity и свежие inventory/admission остаются обязательными. Их отсутствие не позволяет запускать Julia/render/assembly. Medium I может реализовать fail-closed scaffolding после R1/R2; зависимая интеграция и BUILD должны оставаться blocked до получения собственных свидетельств. Не нужно придумывать значения вместо unknown, расширять чтение/import scan автоматически, ослаблять checkdocs/warnonly, stripping/draft или создавать status=reviewed по заверению автора. Candidate/blocked/failed отделены от native/browser/scientific acceptance; публикация/release pointer не разрешены.

## Ресурсы и полнота свидетельств

Первоначальный author scan 5,523,762 B при cap 4,194,304 B сохраняется как **FAILED_RESOURCE_CAP**. Его нельзя исправить задним числом совпадением результатов. Отдельная continuation имеет отдельное разрешение 2 MiB и заявленный logical read 1,142,390 B: 43 Markdown файла, два прохода по 508,210 B, три чтения expander по 41,990 B. Это другой этап. В этом review сверены frozen hashes, выбранные API/owner sources и один узкий scan фактического owner Markdown; полной независимой перепроверки всех docstrings/import effects нет.

Собственные чтения ограничивались перечисленными артефактами и выбранными owner/Documenter source paths; широкого поиска по execution tree, imports, parsers и исполнения не было. Оценка прочитанного payload около 1.8–1.9 MiB с учётом повторных чтений; точный единый byte ledger на каждый shell read не сохранён, поэтому формальный metered PASS ресурсного лимита не заявляется. Physical I/O/RSS не измерены. Вывод существенно меньше 64 KiB. Эти ограничения не уменьшают воспроизводимость двух API-локаторов и не превращаются в разрешение BUILD.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Operator должен передать typed empty modules | D2:48; D1:94,100; AXNMp documents.jl:420 | Source type analysis; без Julia execution | изменить |
| HTML recipes нуждаются в непустом sitename | D1:99–105; documents.jl:427; HTMLWriter.jl:825; existing owner make | Render не запускался | изменить |
| Default recipe/doctest и owner namespace сохранены в проекте | Existing Core/Runner make, D1/D2 profile/page clauses | Продуктовая реализация ещё не выполнена | сохранить |
| Root admission/process/fixed-light границы достаточно конкретны для source I | Принятый D; D1/D2 argv, drain, staging и fail-closed clauses | Зависимые adapter/assets/toolchain evidence отсутствуют | сохранить |
| Нет основания запускать BUILD или заявлять scientific acceptance | D2 nested-docstring gate; selected expander/import/precompile sources; отсутствующие prerequisites | Полная effect closure не установлена | данных недостаточно |
| Original resource overrun не превращается в PASS | Исходный ledger и отдельная continuation identity | Собственный точный aggregate read ledger отсутствует | сохранить |

Следующее необходимое действие — узкая авторская коррекция R1/R2 с новыми hashes. Этот review не реализует её и не разрешает последующее исполнение. STOP.
