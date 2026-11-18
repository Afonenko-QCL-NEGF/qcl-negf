# Сквозной диагностический запуск QCL-NEGF, 18 ноября 2026

В рамках [#135](https://github.com/Afonenko-QCL-NEGF/qcl-negf/issues/135)
проведена одна stationary-точка из публичной постановки при 70 K и 48 мВ
на период. Runner заморозил разрешённую конфигурацию, выполнил две итерации SCBA
на Core, записал HDF5 и историю. Независимый Results проверил содержимое и
подготовил отчётные графики. Статус серии `completed_with_warnings`, статус точки
`completed / unconverged`. Внешних итераций Poisson не было. Итерационная
сходимость и физические проверки дали `false`, дискретизация `not_measured`,
научная приёмка `false`.

## Исходники и воспроизведение

- Исходный root main `2b30eb9bd730fd76a53d6ae9dd52bf503df78ef5`, Core
  `db26a0ef49673d8246ae336cbe73bafe6d7482ac`, Runner до изменения
  `53b3a280109228a980df7ddea59e4f1b75b836be`, независимый Results
  `8fadceebe819e94b95310767f463c1b0f0ffc7b1`.
- Julia 1.13.4 фактически импортировала Core `e171caa60cce676c6c4238dd671e7c527f2bd977`
  со старым Pkg source и `db26a0ef49673d8246ae336cbe73bafe6d7482ac` с новым.
  Контрольный запуск использовал дерево Runner `72d1936e24baef1ac14e4861b1bd5004b2833ddd`.
  Локальный checkout `03c5f6f7bb5b59b85217e7b681b27e14022aa0f8` и опубликованный
  merge `48f31e95d550f0aaeaece6cddf1267810ea4715c` имеют это же дерево.
  В отдельной Pkg integration-среде с двумя gitlinks импорт подтвердил оба
  checkout, а CLI сформировал побайтно тот же frozen plan.
  [Runner PR #54](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/54).
- Сохранённый Pkg Manifest имеет SHA-256
  `a98031f511386ad7eb7a03ff96abd9e7524d4cd0ffb15a9714d52cb0f92ca361`.
  Тот же хеш записан в `metadata/toolchain_json` нативных файлов.
  Хеш и пути загрузки служат provenance расчёта.

В checkout Runner с системной Julia и подготовленным Pkg Manifest:

```sh
export JULIA_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
julia --startup-file=no --project=. -e 'using Pkg; Pkg.instantiate()'
bin/qcl-negf plan examples/config/stationary-smoke.yaml --max-runs 1 > plan.json
bin/qcl-negf run-plan plan.json stationary-result
bin/qcl-negf analyze stationary-result stationary-report
```

`plan.json` содержит `resolved_configuration`, `effective_inputs` и
`estimated_peak_bytes` в `resources` и в записи execution. У принятого плана
fingerprint `a307c75e19a61b9da3683772374eb366802a18d307c4719bd00046e6174056c4`.
Выбрана опубликованная малая инженерная сетка из Runner
`test/integration/fixed_work_production_calibration.jl`.
Вычисление использует 48 пространственных и 49 энергетических узлов, пять
радиальных импульсов, три состояния, один период. Включены LO, акустические
фононы, примеси и шероховатость интерфейсов. Унаследованы допуски и схемы
взвешивания публичного паспорта. Явные пределы SCBA и Poisson равны 2.

На точке `representation_preflight.json` дал `covered:false`. Для заданных
48 мВ оценка покрытия требует диапазон примерно от −0,15656 до 0,30122 эВ
при рабочем окне от −0,10 до 0,28 эВ. Режим `diagnostic` сохраняет этот
результат preflight и допускает продолжение. В
`history.h5:/scba/r_K` итог 1,52929, в `history.h5:/scba/r_Σ` итог 1,63657.
Это безразмерные сырые невязки перед смешиванием. Core использует невзвешенную
норму Фробениуса с добавкой `1e-14` в знаменателе. Для Keldysh знаменатель
нормирует по сохранённой `G<`, для Σ по свежему кандидату с максимумом по
компонентам и семействам. Финальный допуск `1e-8` взят из публичной
постановки. Унаследованное требование трёх последовательных проходов SCBA
превышает бюджет примера. Точку используют для проверки работы интерфейсов и
хранилища.

## Нативные артефакты и проверки

- Локальный commit артефактов
  `d4f4d1d58bebe0b72cff723a038b0593d350c488eed00cdab71911e5f51788dc`
  связывает `physics.h5`, `analysis.h5`, `history.h5`, `recovery.json` и
  `resolved_configuration.json`. Исходный неудачный прогон сохранил историю
  и отказ `MANDATORY_STORAGE_FAILED` из-за вызова отсутствующего
  private helper occupied spectral quantiles. Исправление
  сохраняет этой метрике `not_measured` и публикует остальные данные.
- `qcl-negf-results render POINT/artifacts OUTPUT` независимо проверил хеш
  `analysis.h5` и построил шесть графиков. `POINT` указывает на
  `points[].data.artifact_root` относительно корня серии. Экспорт
  `qcl-negf-results export stationary-result exports --profile full-state --status completed_with_warnings`
  проверил согласованность полного набора. SHA-256 части архива
  `4b7eb8fec892ff4cfbe8109c0bb17710aaec2426afb2327e00da59d9cd24f0b2`.
- Подменённый fingerprint, неизвестный execution ID и повреждённая копия
  `analysis.h5` отклонены с exit 2. Повтор исходного плана на копии результата
  переиспользовал attempt 1 и тот же commit. Целевые Julia проверки прошли
  86/86, включая историю попыток, несовместимые checkpoint и чтение
  исторического Hilbert checkpoint. Пройден Deno type check и сборка
  Documenter с doctests. Восстановление прерванного solve на этой
  диагностической точке отдельно не измерялось.
- Независимое ревью GPT‑6.2 Sol проверило дерево Runner, вызовы, нативные
  артефакты и отчёт до merge. Старое поле `scientific_accepted` в
  commit/Results отражает `solution.converged`. Отчёт берёт научную оценку из
  Core `scientific_assessment`, где для неё требуется независимая проверка
  дискретизации.

## Ресурсы и очередь

Локальный холодный CLI-прогон занял 136,9 с, из них 44,4 с по таймеру вызова
solver, peak RSS 1 734 460 KiB и примерно 3 MiB записанных файлов. Ограничения
проверки — один CPU, один поток Julia и BLAS, 300 с, 8 GiB виртуального
адресного пространства и 16 MiB на файл. Frozen plan оценил собственно
численные массивы и рабочие области в 3 352 664 B. Для выбора RAM требуются
измеренный стартовый расход Julia/компиляции и запас Runner в cgroup.

Задание HTCondor 26.0.1 `20.0` на Ubuntu worker завершилось с native exit 0
и событиями передачи входа и результата. От подачи до возврата прошло
158 с, из них `TimeExecute=115` с. Запрос составил 1 CPU,
5 GiB RAM и 256 MiB диска, время payload ограничено 300 с. Scheduler сообщил
`MemoryUsage=977` MiB, это наблюдаемое значение ClassAd. Вернулись те же
байты frozen plan и Manifest hash. Независимо проверены пять хешей артефактов
в commit `b5f8fb6044d33b9a2dbde33806bea9ef2d22279890c552519a777043741b748a`
и full-state export. Статусы и счётчики совпали с локальными. Максимальные
расхождения двух записанных SCBA строк по `r_K` и `r_Σ` соответственно
`1,60e-14` и `5,55e-15`. Для диагностики записанный электронный ток
в направлении +z составил около `4,01114e7 A/m²`, абсолютное расхождение
между запусками `3,0e-6 A/m²`. Расчёт содержит одну несошедшуюся точку.

Сохранены два ранних задания. `18.0` вернуло exit 127 из-за поиска Julia
через `prlimit`. Обёртка теперь передаёт полный executable path.
`19.0` вернуло exit 0 и серию `failed / PREPARATION_FAILED` при 3 GiB.
Проверка Runner обнаружила, что располагаемая cgroup память после вычета
штатного резерва 2 GiB недостаточна. При повторе менялся только запрос RAM.

Для этой точки исходный default на Linux составляет 1 поток Julia, 1 BLAS
и проверенный запрос 5 GiB. Измерение 5 GiB устанавливает рабочий запрос
для этого окружения, нижняя граница не измерена. Для обычной подачи Pkg
среду нужно штатно подготовить на всех подходящих workers. HTCondor тогда
выбирает worker по запросу CPU/RAM/disk. Для расчёта запроса Runner требуется
добавить к оценке рабочего набора зафиксированную стоимость Julia/JIT,
сохранения и запас cgroup. 5 GiB применялись к этому примеру, автоматическая
оценка общего случая остаётся отдельной задачей.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Pkg выбирает согласованный Core | Нативный импорт и Manifest `db26a0e`, идентичные деревья локального и merged Runner | Julia 1.13.4, Linux | сохранить |
| Один публичный stationary input проходит до независимого отчёта | Нативный commit, две SCBA строки, Results render и full-state export | Одна диагностическая точка | сохранить |
| Постановка достигла сходимости или физической приёмки | `scientific_assessment`, невязки и preflight выше | Неполное окно, две SCBA, ноль внешних итераций, дискретизация не измерена | сохранить статус unconverged |
| Штатная очередь исполняет тот же plan и возвращает состояние | HTCondor `20.0`, native transfer и независимая проверка commit | Один подготовленный Ubuntu worker, измеренная память зависит от cgroup и старта | сохранить проверенный default для примера |
| Сохранённые данные безопасно переиспользуются | Повтор attempt 1, отрицательные проверки и целевые тесты restart | Restart из прерванной точки не измерен для этого примера | дополнительно измерить |

Локально сохранены оба результата CLI, возвращённые результаты и журналы
очереди, frozen plan, Pkg Manifest, история и full-state экспорт.
Кампания [#133](https://github.com/Afonenko-QCL-NEGF/qcl-negf/issues/133)
остаётся в состоянии опубликованного handoff. Новые опыты на её VM не выполнялись.

**Следующий шаг.** Проверить штатное pause/resume этой точки через HTCondor
self-checkpointing с сохранением исходного бюджета итераций и непрерывности
истории.
