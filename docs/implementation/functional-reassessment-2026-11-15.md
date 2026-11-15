# Повторный пересмотр требований, функций и свидетельств QCL-NEGF

15 ноября 2026 года. Карта для подготовки переработки. В этой сессии выполнялись чтение и подготовка документов; solver, tests, builds, установки и операции с сервером не запускались.

**Вывод:** прежний clean-start план неполно описывал научное приложение. Выбор HTCondor/Pkg/Ansible сохраняется; дополнительно требуется привести Core и Runner к согласованному поддерживаемому состоянию, определить судьбу научных форм, справки, исследований и анализа, сохранить несколько эксплуатационных требований. Это не требует возвращать прежнюю платформенную обвязку.

**Уточнение пользователя:** сейчас другая сессия меняет научный код. Описанные ниже ограничения относятся только к прочитанным версиям. Решения «сохранить / довести / удалить / отложить» для конкретного кода принимаются по фактическому состоянию при запуске переработки, с учётом handoff научной кампании. Этот документ не замораживает её исходники и не предписывает удалить функции по сегодняшнему снимку.

## Охват и сила свидетельств

Сопоставлены девять репозиториев: root и восемь компонентов; локальные code/docs/test inventories и история, опубликованные описания PR, исторические требования и весь корпус из 17 документов [PR130](https://github.com/Afonenko-QCL-NEGF/qcl-negf/pull/130). Отдельно прочитаны issues129/131/133, доступные комментарии и текущие правила Java. Существенные поздние возможности проверены адресным чтением source/test/patch на опубликованных refs.

Поиск GitHub вернул **451 уникальное описание PR**: root130, Core28, Runner52, AiiDA37, Contracts30, Platform82, Portal39, Research11, Results42. Root собран из двух перекрывающихся выдач по100, в прямом и обратном порядке; остальные выдачи короче100. Найдены три обычных issue в root; в компонентных выдачах обычных issue не найдено. Это охват доступного поиска, не гарантия полноты удалённой/private истории. В исходном запросе «issue29» публичный root номер29 оказался PR; связанная ретроспектива — issue129.

451 описание не означает semantic review всех PR diffs. Исторический корпус сообщает собственный охват994commit metadata и адресный разбор pivots; мы не выдаём его за повторный независимый review всех994diffs. Старые raw terminal logs, закрытые private packets и большие научные массивы здесь не проверялись. Наличие исходника теста означает найденную проверку, а не новый PASS. PR summary — сообщение о проверке, а не её воспроизведение.

Локальный root: `93880c23bca889ddcb8b98edb995080b332dd99f`; известный dirty overlay сохранён. Локальные Core/Runner/Results/Portal старее некоторых опубликованных ветвей. Поэтому «есть в старом checkout», «есть в поздней ветке», «работает в кампании» и «установлено в кластере» рассматриваются отдельно.

Обозначения в таблицах: **код/тест** — найдены реализация и соответствующие tests, без запуска сейчас; **частично** — отдельные части существуют, соединение или область поддержки ограничены; **идея** — документированный замысел без подтверждённой реализации. «Сохранить» относится к полезному поведению; форму реализации можно заменить.

## Что изменилось в требованиях

| Область | Действующее решение |
| --- | --- |
| Основа | Proxmox сохраняется; первый pool — CachyOS host и Linux guest прежнего Xeon; Windows native позже |
| Старый контур | Старые QCL VM/data/state можно удалить без миграции и старой совместимости; чужие ресурсы и машинные доступы сохраняются |
| Новая наука | Машина, данные, незавершённые изменения и результаты кампании133 вне очистки; передаются также отрицательные результаты и решения |
| Состав | Два репозитория вместо девяти; физика в Core, научное приложение и небольшая lab-конфигурация в root |
| Готовые инструменты | HTCondor, Julia Pkg, системные пакеты и Ansible; редкий ручной ремонт допустим |
| Доступ и UI | GUI запусков и мониторинг обязательны; SSH/RDP/VNC/HTTPS, нативные клиенты пока не выбраны; светлый web UI |
| Ресурсы | Совместное размещение jobs и измерение throughput; сборка на освобождённом выбранном host допустима при работе остальных |
| Обновление | Build и замена общего runtime — разные действия. Новую задачу concurrent/hot update не вводим; общий runtime обновляется в обслуживание после завершения использующих его jobs |
| Процесс | Codex, ограниченные роли по необходимости, независимый review существенного изменения; без Superpowers и собственного orchestration harness |
| Проверки | Поведенческие и научные свойства по риску; обязательные version/module-tree assertions удаляемого продукта не сохраняются |
| Новые результаты | Отмена сохранения старого контура не разрешает терять новые результаты при переустановке или незаметно удалять неуспешные опыты |

Позднее указание от2ноября о maintenance-only подтверждено [ретроспективой10](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/c1fc1b693135a631e58783144c86e2c6d25e74b8/docs/implementation/session-retrospective-2026-11-03/10-requirements-interpretation-and-decisions.md). Оно заменяет прежний сценарий обновления при running jobs. Требование штатного guest agent для PVE guest отражено в [истории13, H07](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/c1fc1b693135a631e58783144c86e2c6d25e74b8/docs/implementation/session-retrospective-2026-11-03/13-whole-history-overview.md); собственный QGA protocol из него не следует.

## Научные возможности, которые нельзя потерять при очистке

Источники **Core0**, **Runner0**, **Research0** и поздние refs раскрыты ниже. Пути в таблицах относительны соответствующему репозиторию.

| Семейство | Свидетельство и граница | Решение для новой версии |
| --- | --- | --- |
| Размерная модель, произвольные слои/материалы/doping, bias/temperature | Core0 `src/domain/types.jl`, `src/domain/scaling.jl`; tests geometry/units. Универсальность всех signed-bias CLI не установлена | Сохранить units, явные физические параметры и ограничения; UI не придумывает material constants |
| Пять каналов рассеяния | Core0 `src/domain/scattering.jl`; Runner0 `test/application/every_scattering_channel_is_isolated_and_configured.jl` | Сохранить выбор и состав модели. Отключение канала — научный вариант, а не невидимое ускорение |
| Дополнительные closures и модели | Core0 `PhysicalModelOptions`, `model_operators.jl`, `electron_electron.jl`, tests model_extensions. Часть возможностей исследовательская/ограниченная | Сохранить полезный код и границы применимости; не включать автоматически в baseline |
| Граничная постановка и представление | Core0 `model_capabilities.jl`, cavity current/spectral tests; некоторые Bloch/Wannier варианты reference-only | Сохранить выбранную постановку и независимые проверки; не обещать законченный contact/device solver |
| SCBA/Poisson, смешивание и inner policy | Core0 `src/domain/research_policy.jl`, tests Anderson/inexact_inner. Приближённый внутренний шаг не равен принятому final | Сохранить нужные алгоритмы и честные residual/status; не спутать inner policy с разрешением voltage seed |
| Эталонные и оптимизированные операторы | Core0 `algorithm_registry.jl`, tests literal six-index contractions, Keldysh/PV/Poisson/current | Сохранить независимые oracles и эквивалентные реализации. Общий ошибочный helper не является независимой проверкой |
| Организация вычислений | Core0 optimized chunking/threading/FFT/factorization. Core28 исправляет создание выбранного Hilbert cache | Сохранить ограниченный набор понятных knobs; chunks/threads не меняют физическую сетку |
| Численные и физические альтернативы | Core0 `algorithm_options.jl`, optimization taxonomy tests | Явно отличать эквивалентную оптимизацию, другую дискретизацию и другую модель; не выбирать скрыто по RAM |
| Адаптация окна | Core0 `domain_adaptation.jl`, tests: расширение энергетического окна с сохранением ΔE и перестроением операторов | Учитывать отдельно от chunking и inner tolerance; применение определяет постановка. Полный nonuniform solver этим не доказан |
| Наблюдаемые и диагностики | Core0 `physics/observables.jl`, acceptance/reference validation: ток, density/populations, spectra, conservation/PSD/window checks | Сохранить units/weights/normalization/applicability и отсутствие данных; не свести к одному PASS |
| Согласованное конечное состояние | Core0 final audit; Core PR8/10/12/13: raw fixed-point, U/G alignment, manufactured/scattering controls | Сохранить численную семантику и независимые тесты; отчётная публикация не равна научной валидации |
| Публичное состояние и восстановление | Поздние Core18–21: detached state, restore, actual checkpoint domain, final observations | На старте выбрать актуальные API; убрать ненужный private-field bridge, сохранив mixer/history/counters и согласованность U/G/Σ |
| Структура/базис до SCBA | Core basis и spectral tests; Runner25/26 и Portal quantum preview | Сохранить явное действие просмотра уровней и wavefunctions с обозначением bare Hamiltonian/κ/Hartree scope |
| Оптический отклик | Core0 `physics/optical_response.jl`, two-level sign tests; Runner optical recompute требует full saved state | Сохранить полезную optional возможность, явно отложенную относительно первого stationary transport. Bare-bubble gain не означает lasing/абсолютно валидированный gain |
| Operator/refinement studies и литература | Research0 `config/operators.yaml`, `spectra.yaml`, `studies/*`, `literature/reference-2019/source.yaml`; поздний researcher guide | Сохранить постановки, источники, неопределённость оцифровки и условия сравнения. План refinement не считать выполненным опытом; литературная расчётная кривая не raw experiment |

## Подготовка, выполнение и работа с результатами

| Семейство | Свидетельство и граница | Минимальная сохраняемая форма |
| --- | --- | --- |
| Входы/defaults/overrides/effective values | Runner configuration_sources; поздний PR29 `resolved_configuration_snapshot/diff` | Один resolver, вход и фактически использованные параметры с units; понятное объяснение отличий |
| Plan и предварительная оценка | Runner0 `cli.jl`, `scientific_plan_dict`, output/memory estimates; поздний estimator уже шире старого Sys.CPU_THREADS пути | Preview без solve и приблизительная заявка ресурсов. Оценка не measured peak и не SHA-допуск |
| Серии, варианты, repeats и continuation | Runner planning/voltage_continuation; Research controlled_paths | Независимые jobs отдельно; последовательная ветвь внутри Runner; explicit repeats и порядок. Не универсальный workflow DSL |
| Прямой локальный запуск | Runner `bin/qcl-negf`; Core27/Runner52 и сообщения133 о standalone Julia/Pkg | Тот же вход/CLI локально и в очереди; отдельные run/analyze/compare действия |
| Resume и seed | Runner persistence и continuation tests | Продолжение текущей точки с историей и потраченными итерациями отдельно от начального приближения новой точки |
| Pause и cancel | Runner pause + Platform lifecycle tests | Запрос, сохранённый checkpoint и остановленный процесс различимы. Native cancel прекращает повторы/исполнение и освобождает ресурсы; не обещает новый checkpoint |
| Научная история и прогресс | Runner progress/scientific_history/physical_markers; Results histories | Лёгкая сохраняемая история iterations/residuals/observables, этап/время/свежесть progress; полный дамп не нужен для каждой строки |
| Final/checkpoint/attempts | Runner state/roundtrip/failure tests | Исходные массивы и отдельные попытки, latest+previous checkpoint, atomic publication; failed и skipped не превращаются в successful final |
| HDF5 и семантические views | Results0 StateReader; Results1 `saved_views.py::AnalysisReader/VIEWS`, Portal1 SavedPlot | Срезы с осями/единицами, density/potential/spectra/levels/wavefunctions/populations. Сохранить знаки, маски, complex selectors; не читать весь файл ради малого среза |
| Научная диагностика сохранённого состояния | Results0 `equilibrium.py`, manufactured tests; Results1 adapter имеет явные ограничения | Сохранить независимую математику и адаптировать к выбранному новому output. Название команды не доказывает рабочий adapter |
| Сравнение без нового transport solve | Runner `compare_saved_results`; Portal/Results history derive/compare | Явно выбрать runs и изменённые параметры; различать несопоставимость, отсутствие данных, descriptive difference и точность |
| Полнота серии | Results1 `brief_result`, Portal exact point/history views | Видны плановые, вычисленные, failed и ещё не исполненные точки; пропуски не интерполируются в успешную I–V |
| Экспорт и анализ без кластера | Results export/archives; Portal Range downloads | Забрать исходные файлы и отчёт обычным средством, докачать после обрыва, анализировать без AiiDA/solver. Science subset не обязательно restorable checkpoint |
| Стоимость анализа и технические измерения | Results limits/performance; Runner phases; Platform monitor sources | Малые selections/output, один analysis process для начала, понятная отмена; per-job elapsed/CPU/memory и существенные solver phases. Host graph не per-job accounting |

## Исследовательский интерфейс и знания

| Семейство | Что реально найдено | Судьба |
| --- | --- | --- |
| GUI очереди и равный кодовый доступ | Portal/AiiDA submit/status/cancel/logs; новые OOD/HTCondor — ещё план замены | Обязательный первый инфраструктурный результат: один input/output/queue для человека и агента |
| Доступ и актуальность GUI | Portal auth-before-dispatch, trusted-group access, tests selection/stale responses и uncertain mutations | Штатная аутентификация и понятная область доступа к jobs/results. Поздний ответ для прежнего run/входа не показывается как результат нового выбора; нужны понятные pending/error/unknown состояния, без нового IAM/actor framework |
| Научный конфигуратор | Portal1 `configurator.tsx`, Runner22/29; template/form/YAML и preview | Сохранить функцию и общий resolver. OOD adapter сам не предоставляет QCL-форму |
| Редактор структуры | Portal1 `structure-editor.tsx`, frontend tests: слои, interfaces, donor mask, явные presets | Сохранить возможность; конкретную первую GUI-форму выбрать на старте. Смена состава не выводит новые constants автоматически |
| Предпросмотр базиса | Portal1 `quantum-preview.tsx`, Runner/Core API; backend tests используют fake process | Сохранить scientific operation; установленный реальный preview потребует проверки выбранного пути |
| Карточка исследования | AiiDA1 research_cards + temporary SQLite/reload tests; Portal1 research-cards | Минимум — вопрос/постановка, заметки, ссылки на runs и отчёт в обычных файлах. Старый DB/version engine не обязателен |
| Отчёты человека/агента | Agent report source/tests, Portal upload и explicit used-run refs | Сохранять авторский вывод и использованные runs; текст рецензии не превращается в машинное scientific acceptance |
| Справка по модели | Portal1 model-help/static reference, исходная теория/Research | Краткий смысл, units, assumptions и источник рядом с параметром; версия справки не подменяет условия старого опыта |
| Used-input help | AiiDA original-input capture и preview есть; Portal1 post-run adapter возвращает unknown/inputs=[] | Сохранить потребность объяснить actual defaults/overrides/origins; наличие отдельных частей не объявлять завершённой функцией |
| Просмотр histories/views | Portal1 saved-results/saved-diagnostics: plots/raw tables/exact selected point/compare | Сохранить полезные представления. Прежнее утверждение «viewer отсутствует» было слишком широким; installed/browser полнота неизвестна |
| Live во время solve | Есть progress/history primitives; поздний Portal legacy live-history adapter явно unavailable | Обязателен лёгкий научный progress. Live многомерные views — отдельная возможность, без full checkpoint на каждый refresh |
| Каталог и поиск | Есть newest-first/paged lists/cards; универсальный scientific full-text/faceted search не подтверждён | Обозримый список и простые фильтры сначала; развитый каталог отложен явно |
| Документация/обучение | Root requirements D09–D11, physics-documentation и Java methodology; offline/search/math реализации и инциденты | Сохранить содержательную теорию, примеры и локально читаемую справку. Учебник и polish поиска — отдельные задачи, без прежней docs factory |

## Эксплуатация и разработка

| Семейство | Свидетельство / сохраняемый смысл | Простое решение |
| --- | --- | --- |
| Машинные доступы и доверие | Private inventory refs, SSH/RDP/VNC/HTTPS; администрирование независимо от приложения | Сохранить credentials/trust, обновлять SSH identity адресно; нативные клиенты выбираются позже |
| Users/permissions | Platform service users/LoadCredential/CI isolation; прежние runtime permission failures | Проверить реальные accounts, запись scratch/depot/results и доступ GUI. Public CI не получает prod credentials; новый IAM/vault не требуется |
| Добавление/замена/вывод worker | Старый onboarding был guest/Nix-specific | Private inventory + Ansible + native queue test; вывод через запрет новых jobs и завершение текущих |
| Сеть и guest agent | Старые network/QGA incidents; human H07 | Обычная сеть и штатный guest agent PVE; без bridge на ноутбуке и собственного QGA/WAL transport |
| CPU/RAM/concurrency | Native facts, Slurm/cgroup history и нынешнее наблюдение30% CPU | HTCondor requests/limits, host reserves и реальный seq/concurrent опыт; без VM memory broker |
| Общий CPU grant и стоимость failed attempts | Исторический R08 отдельно задавал allocated cores × running time; позднее пользователь отменил campaign CPU grants | Общий расходуемый CPU grant удаляется. Штатный учёт стоимости сохраняет неудачные попытки; очередь/wall/CPU time и allocated core-hours различимы. Конечный бюджет отдельной научной кампании не является новым quota engine |
| Build/compute/update | Потребность использовать свободный host и позднее maintenance-only | Build на выбранном освобождённом host; обновление общего runtime после завершения его jobs, фиксированная среда текущего расчёта |
| Отключение клиента/интернета | Исторические LAN/offline требования | Подготовленные inputs/dependencies локальны, submitted job не зависит от браузера/SSH. Работа моделей Codex без связи не обещается |
| Неопределённый исход операции | CR04 и tests timeout-after-mutation | Перед повтором после timeout прочитать native состояние/JobID; ручная сверка достаточна, blind повтор не нужен |
| Диск, spool, новые данные | State/archive/ENOSPC tests и прежние ограничения logical quotas | request_disk/свободное место, видимый failure/hold, сохранение last-good checkpoint; persistent results отдельно от заменяемой ОС |
| Backup будущих данных | Старый archive не был доказанным off-host backup | На целевой машине выбрать обычное сохранение новых inputs/results/config и нужного spool; явно указать, если отдельной копии пока нет |
| Мониторинг | Host/guest/perjob и phase sources, gaps/stale semantics | Один готовый монитор + HTCondor/Runner; пропавшая метрика не ноль, потеря technical telemetry не scientific failure |
| CI/зависимости | Поздние scoped CONTRIBUTING/impact fixes; Java native dependency method | Native managers и проверки затронутого свойства; повтор при новом изменении/сомнении; без root package/release factory |
| Review/автономность | PR132 и Java AGENTS: публичный договор, producer/consumer, отрицательный случай, независимый reviewer | Проверять также необходимость нового слоя для пользовательского сценария. Роли по необходимости; исторические START/расписания не возобновляются |
| Skills/active docs | PR132 меняет11файлов; старые references/CI/entrypoints шире | Короткий AGENTS; каждый skill сохраняется только при самостоятельной пользе. Научные пояснения могут жить в обычных docs |

## Где соединение функций ещё не было доказано

1. **Разные ветви.** [Runner51](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/51) merged в `codex/project-simplification-2026-10-27`, merge `97ab889…`; в прочитанном native5 пути поддержана одна cold stationary point, остальные режимы ограничены. [Runner52](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/52) merged в `main`, merge `18f45ed…`, и используется прямым научным путём. Это разные линии работы, их нельзя механически назвать единым «latest».
2. **Части API и полный сценарий.** В Results1 README268–280 stored equilibrium entrypoints ожидают actual-grid/scales/basis/model adapter. В Portal1 model_help_view и legacy live-history adapter есть явные unknown/unavailable. Рядом существуют полезные math/read/plot/capture части. Правильная задача — согласовать выбранный рабочий путь, затем адресно подключить нужные функции.
3. **Старые диагнозы уже могли быть исправлены.** Поздние Runner39/Platform18/79 сокращали strict policy и уточняли checks; Core27/Runner52 сняли exact Julia patch guard. Старый Sys.CPU_THREADS estimator и старый хрупкий README не характеризуют все поздние refs.
4. **Научные результаты.** [Checkpoint133 от18:38UTC](https://github.com/Afonenko-QCL-NEGF/qcl-negf/issues/133#issuecomment-6899308337) сообщает новые S01 controls без строгой сходимости, исправление Core28 и отрицательный adaptive quadrature outcome. Это состояние продолжающейся кампании, не её окончательный вывод. Raw массивы здесь не читались; переносить нужно её фактический финальный handoff.

## Очистка Core и Runner как самостоятельная часть реализации

На старте определить одну согласованную базу Core/Runner из актуальной научной работы. Не смешивать целиком позднюю инфраструктурную ветку с direct science branch ради возраста commit. Пока научная сессия меняет исходники, готовить инфраструктуру независимо; перенос и cleanup научного кода выполнять после handoff/согласования владения.

Затем по фактическому code path решить судьбу каждого поддерживаемого семейства:

- Оставить один основной вход выполнения, один resolver, один путь записи/чтения нового состояния и публичную границу Core/Runner. Внутренние модули и независимые численные реализации могут оставаться разными.
- Найти дубли execution/persistence/config/diagnostics, deprecated wrappers, private Core imports, stub/capability_unavailable, неиспользуемые branches/exports/options и документированные algorithms без исполняемой реализации. Проверить настоящих callers и тесты, прежде чем удалять.
- Нужную незавершённую функцию довести на выбранном пути. Невостребованную брошенную реализацию удалить. Исследовательскую гипотезу сохранить как заметку или явно отделённый эксперимент, без притворного публичного production API.
- Синхронно исправить CLI/help/docs/examples и релевантные tests: интерфейс сообщает ровно поддерживаемые действия. Пустой stub, скрытый fallback, unknown-as-pass или ослабление физики не являются завершением очистки.
- Сохранить reference/oracle, units/signs/weights, scientific variants, отрицательные результаты и recovery semantics. Численная неопределённость отличается от брошенного инженерного соединения; нерешённая физика не повод удалять проверку.

Примеры нынешних мест проверки — Runner `core_api.jl`, scientific execution/persistence adapters, public Core state/observer boundaries и `algorithm_registry.jl`. Это **кандидаты для свежего анализа**, а не сегодняшнее предписание удалить конкретные символы.

Первый кодовый результат — реально исполняемый согласованный путь input → solver → state/output → independent reader/report. Короткий несошедшийся инженерный пример может проверить соединение и маркировку; он не доказывает научную сходимость. Долгий рабочий режим дополнительно проверяет pause/restart с сохранением состояния и истории. Отдельные многообещающие APIs не заменяют эти сценарии.

## Что явно не возвращаем в обязательный путь

Отменены прежние восемь release lifecycles, отдельные control/storage/CI VM по ролям, AiiDA/Slurm/Nix как обязательная база, custom VM resource grants/qualification, собственные admission/receipts/delivery/reconciliation, mandatory NFS, multipart/legacy migrations и точная общая patch-версия инструментов. Native Pkg hashes и обычная целостность файла сами по себе не запрещены.

Явно отложены GPU/distributed single-solve и прочие algorithm_registry research-only идеи; полный nonuniform solver; lasing/power/dynamics/waveguide; развитый search/catalog; прежнее поручение SSD/root-grow/swap без новой фактической необходимости. Это не потерянные обещания готового продукта. Оптика и существующие научные формы учтены как отдельные возможности; их приоритет в первом научном выпуске определяется при старте.

## Как использовать карту при запуске переработки

Карта — разовая опора для выбора и переноса полезного поведения. Она не становится runtime registry или обязательным повторением всей истории на каждом PR.

1. Снять текущие refs/dirty state и получить handoff научной сессии. При незавершённой кампании отделить независимые инфраструктурные действия от правок её кода.
2. Обновить только изменившиеся участки карты по diff и актуальным публичным entrypoints. Повторить статусный вывод для реально выбранных функций; сегодняшние unavailable/limitations не переносить автоматически.
3. Выбрать поддерживаемые пользовательские сценарии первого научного этапа. Для остальных возможностей явно записать «следующий этап / не нужно / исследовательская идея»; молча терять их при удалении старых репозиториев нельзя.
4. Реализовывать выбранный путь короткими изменениями с содержательными проверками, включая необходимость новых abstractions. Измерять работающий пользовательский результат, а не число PR/тестов/строк документации.

## Проверяемые источники

| Метка | Срез |
| --- | --- |
| Core0 | `3108150dd1b6b1377470b384b15c26e272fe5c5d`, локальный Core |
| Runner0 | `0c53c6d0f68e0b25fce79388db831da6fc3ae856`, локальный Runner |
| Research0 | `5458212063a41051328ef8b5d14d63d5ac7dc781`, локальный Research; поздний guide `46fb51fb…` |
| Results0 / Results1 | `fe27a2a9ed065f9afacecc84113311f30d0c68d6` / `10a32422b90a21ee728e73283217ac6b81bcf760` ([PR42](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/pull/42)) |
| Portal0 / Portal1 | `36837e98a8d1f85820f2807d0212ec92e73c3c7b` / `2c31e5fd597600ac632c292969c02dce0e50d020` ([PR39](https://github.com/Afonenko-QCL-NEGF/qcl-negf-portal/pull/39)) |
| Contracts0 / Contracts1 | `e5c056c47fc3bde3e0ca32866692d740ef9b325c` / `5eb0e61a9fc12fa2215291e47b7cd28888ce64cc` |
| AiiDA0 / AiiDA1 | `53e2a20544a469dd7ee5560243ebe530a6310f0a` / `336358dfd10c698e4b4a71d8c93562aaa8ee7182` ([PR37](https://github.com/Afonenko-QCL-NEGF/qcl-negf-aiida/pull/37)) |
| Platform0 / Platform1 | `6c5b11f3c74d44fed8b2c159f890b83e0b5456b9` / `c47097225a4a798e4124e30245c7b5b2063eb32a` |
| Ретроспектива | Root PR130 head `c1fc1b693135a631e58783144c86e2c6d25e74b8`: требования10, история13, memory14, CD15 и остальные документы корпуса |
| Процесс QCL | [PR132](https://github.com/Afonenko-QCL-NEGF/qcl-negf/pull/132), head `b515c42ef14c1f61151626280da0bcf100d116be`, draft/open на момент чтения |
| Опыт Java | [AGENTS.md](https://github.com/BSU-RFCT-Afonenko-Courses/Java/blob/master/AGENTS.md), прочитан15ноября, content blob `b0bac9188c6578061073b61ff0ee37cc0e5699fc`: native tools, scoped tests, whole-chain cost, без mandatoryTDD/receipts/Superpowers |

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Первоначальная таблица функций была достаточной | Полный охват семейств выявил формы, help, studies, optics и эксплуатационные пропуски | Разные ветви и частичные реализации | изменить план |
| Все старые функции надо переносить как готовые | Найдены реализованные части, stubs и незавершённые соединения | Работоспособность нового пути не проверена | выбрать и согласовать целостный поддерживаемый набор |
| Сегодняшний снимок определяет судьбу Core на будущем старте | Активная133 продолжает менять код и научные выводы | Итоговый handoff ещё формируется | дополнительно проверить актуальное состояние при запуске |
| Cleanup можно ограничить инфраструктурой | Дубли и partial paths существуют также в Core/Runner | Конкретные места могли измениться | включить свежий code audit и cleanup в реализацию |
| Для полноты нужен ещё один постоянный механизм доказательств | Найденные потребности описываются функциями, native tools и короткими operator правилами | Новая реализация ещё впереди | сохранить простоту и проверять выбранные сценарии |
