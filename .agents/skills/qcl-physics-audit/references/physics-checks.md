# Применимость проверок QCL-NEGF

Это карта вопросов к [physics audit](../SKILL.md), не источник формул, схем
или численных порогов. Формулу, нормировку, веса, units, near-zero behavior,
допуск и его основание брать из owning contract соответствующей версии.
Source/static, metadata, runtime и scientific evidence принимать раздельно.

## Три маршрута

| Маршрут | Исходные материалы | Допустимый вывод |
| --- | --- | --- |
| Текущий source-only | Проверяемое физическое/численное утверждение, selected source commit/gitlinks и dirty overlays, owning equations/docs и path/symbol | Архивный run не обязателен. Сопоставить предпосылки, дискретизацию и реализацию; отсутствие raw ограничивает только result-specific вывод. Ни тестовый source, ни совпадение двух реализаций не доказывают runtime correctness. |
| Неизменяемый архив | Его archived source/model identity, frozen plan/criteria, run/attempt, hashes, native metadata/доступные arrays | Читать формулы/acceptance metadata и reader, совместимые именно с этим архивом. Текущие docs/defaults не подставлять вместо архивных; current code audit вести отдельно. Missing source/raw/compatibility остаётся точным gap. |
| Standalone | Запрос, поставляемые paper/source fragments/данные с refs и hashes, [SKILL.md](../SKILL.md) | Без root можно провести ограниченный разбор предоставленного. Назвать нужный owning path/symbol и версию, если он недоступен; не угадывать содержание и не устанавливать окружение ради аудита. |

Для standalone достаточно вопроса/owner, доступных неизменяемых inputs,
разрешённого этапа/границ, сохраняемой модели/units/tolerances, oracle и уровня
вывода, протокола чтения, зависимостей, конечного общего бюджета/stop и выхода
с evidence/limits/resume. При доступном root это поля канонического контракта
`docs/system/agent-review-workflow.md`, «Разбиение до READY», а не новая форма.
Уже разрешённую работу не пересогласовывать; missing блокирует только dependents.
Навык не создаёт полномочий на изменение модели или новый расчёт.

## Вопросы применимости

| Проверка | Что установить в owning постановке |
| --- | --- |
| Единицы и конвенции | Energy/length, sheet/volume density, spin, мера k, знак заряда, направление тока и bias per period |
| Green functions | Принятая adjoint/anti-Hermitian конвенция; матричная PSD, а не знак off-diagonal |
| Спектральная сумма | Метрика базиса, retarded/advanced и spectral definitions; конечный хвост и квадратура различаются; формулу брать из owning validation |
| Сохранение частиц | Стационарность, контакты/источники, полная интеграционная мера и порядок интегрирования/модуля |
| Локальный ток | Восстановление из усечённого базиса; применимость локального баланса и неупругие переходы; не требовать постоянства энергоразрешённого тока без вывода |
| Энергия | Работа поля, контакты, LO/baths и все активные каналы; электронный поток отдельно не обязан сохраняться |
| Равновесие | Согласованные chemical potential/temperature/baths и отсутствие drive; owning FDR/current oracle. Один нулевой bias не достаточен |
| Конечные окна | Граничные хвосты, дробные сдвиги, веса/сопряжённость; перенормировка density не исправляет неверное распределение |
| Наблюдаемые | Gain, порог и мощность различаются; circuit/thermal/optical assumptions должны быть явны |

Raw fixed-point residual, смешанный шаг, SCBA и Poisson не взаимозаменяемы.
Final U/G должны относиться к одному состоянию; fresh-map свидетельство не
подменяется history. Не менять модель/channels/grid/basis/window/tolerances
ради pass или стоимости. Независимый analytic/physical oracle нужен помимо
общих reference/optimized kernels. Calibration не является independent validation.

## Owning locators для выбранного source

Пути от root; проверены чтением 2026-10-19. Это search entrypoints, не lock
версий и не доказательство pass. Для нового задания найти символ через `rg`
в фактически выбранном source и привязать вывод к commit + path/symbol.
Documenter `@id` ниже — owning anchor, не обычный file fragment skill package.

| Предмет | Owning locator |
| --- | --- |
| Невязки, независимые эталоны, представление | `components/QCLNEGF.jl/docs/src/physics/numerical-policy.md` |
| Формула → функция | `components/QCLNEGF.jl/docs/src/developer/traceability.md`, `@id traceability` |
| Определения acceptance | `components/QCLNEGF.jl/src/numerics/reference/acceptance_metadata.jl`, `_acceptance_metric_metadata`; `components/QCLNEGF.jl/docs/src/theory/12_validation.md`, `@id acceptance-metadata-registry`, `@id eq-validation-residuals` |
| Спектральная проверка | Та же глава `12_validation.md`, `@id validation-spectral-sum`; не копировать её формулу/thresholds в skill |
| Пределы модели | `components/QCLNEGF.jl/docs/src/theory/15_limitations.md`, `@id theory-limitations` |
| Геометрия и controlled studies | `components/qcl-negf-research/docs/scientific-inputs.md` |

Если нужный archived contract или owning документ недоступен, записать точный
commit/path и влияние на конкретный claim. Не требовать полного checkout для
доступного source-only вопроса и не заменять missing документацию текущим README.
Историческая карта была прочитана на root
`efb68778a9267cb11c6e9f49701ea2c247c35645`; этот snapshot не источник нового run.

## Датированные первоисточники

Следующие ссылки и пределы чтения сохранены из прохода 2026-09-28; новой
проверки публикаций этим обновлением нет. Для конкретной формулы сверить статью
и её применимость, не считать bibliography сертификацией solver.

- [Wacker, 2007](https://arxiv.org/pdf/0706.4202), Eqs. 2–3, Fig. 1:
  определение тока и влияние конечного базиса на пространственный профиль.
- [Baym, 1962](https://doi.org/10.1103/PhysRev.127.1391): условия conserving
  approximations; был проверен abstract, не полный закрытый текст. Название SCBA
  не доказывает выполнение этих условий конкретной реализацией.
- [Hałdaś, 2019](https://doi.org/10.1007/s10825-019-01386-4): grid/interfaces;
  refinement не должен незаметно менять геометрию.
- [Oberkampf & Trucano, 2007](https://www.sandia.gov/research/publications/details/verification-and-validation-benchmarks-2007-02-01/):
  code/solution verification, validation и независимые benchmarks.
