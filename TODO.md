# Задачи развития

Здесь находятся межкомпонентные задачи общего проекта. Запись в TODO не
означает, что возможность реализована или разрешены новые вычисления.

## results-ro-crate

- [ ] **Упаковывать исследовательские результаты в RO-Crate для автономного анализа.**

Цель: связать научный вопрос, гипотезы, план, критерии, фактические runs,
исходники и HDF5 с выводами. RO-Crate дополняет текущий native export и receipts;
не заменяет HDF5, scientific contracts, AiiDA provenance или физическую приёмку.

Владелец реализации — `qcl-negf-results`; profile/форматы — `qcl-negf-contracts`;
постановки — `qcl-negf-research`; emitters — runner и AiiDA. Ядро не должно
зависеть от RO-Crate. Superproject интегрирует опубликованные изменения gitlinks.

### Версии и семантика

На 2026-09-28 опубликованы [RO-Crate 1.3, Recommendation](https://www.researchobject.org/ro-crate/specification/1.3/index.html)
и [Workflow Run RO-Crate 0.6](https://www.researchobject.org/workflow-run-crate/profiles/changelog),
совместимый с Workflow RO-Crate 1.1. При реализации повторно проверить
совместимость инструментов и выбрать точные версии; не смешивать JSON-LD
contexts разных поколений. Это целевой профиль, не декларация текущего экспорта.

Начать с Process Run Crate для фактически выполненных инструментов. Заявлять
Workflow Run Crate, когда представлен реальный `ComputationalWorkflow` и его
исполнение; подробные шаги при необходимости описывать Provenance Run Crate.
Не выдумывать workflow ради заполнения графа.

`ro-crate-metadata.json` описывает root `./`; descriptor `conformsTo` относится
к базовой RO-Crate, root `conformsTo` — к профилям. В 1.3 сущности профилей
должны иметь тип `Profile` (допустимо вместе с `CreativeWork`).
`hasPart` задаёт состав, включая допустимые внешние data entities;
`mentions` помогает найти действия, но не обозначает причинность.
`CreateAction` связывает фактические `object` (входы), `instrument` и `result`.
План и реально исполненное действие — разные сущности.

### Объём и критерии приёмки будущей реализации

- [ ] Определить логическую единицу: crate исследования/run и общий каталог.
  Отличать 5–7 самостоятельных исследовательских архивов от транспортных частей
  одного export. Сохранить действующий предел **200 000 000 байт на часть**;
  не исключать доказательства ради размера. Указать, автономна часть, crate
  или только полный комплект. Приёмку проводить именно на заявленном комплекте.
- [ ] Включать локальные brief, гипотезы, область применимости, версии плана и
  критериев, отклонения от плана, отрицательные выводы. Связать
  `criterion → run/attempt → artifact/dataset → metric/figure → verdict`.
  Ретроспективную постановку явно отличать от заранее зафиксированной.
- [ ] Сохранять frozen plan/model identity, точные commits и gitlinks,
  dirty patch/свидетельство чистоты, нужный source snapshot, dependency locks,
  существенные build flags, Julia/BLAS/HDF5 и analysis environment, seeds,
  hardware/threads/SMT/affinity. Не поддерживать отдельный ручной список ревизий.
- [ ] Описывать HDF5 paths, dtype/shape, оси/координаты/веса, units, conventions,
  complex representation и missing values; проверять соответствие словаря
  фактическим данным. External links, VDS и compression filters учитывать
  в offline-зависимостях, а не оставлять скрытыми.
- [ ] Связать QCL run/attempt с AiiDA UUID и Slurm cluster/job/array/step, где
  применимо; сохранить нужные provenance/attributes, logs и accounting локально.
  Не требовать живой AiiDA DB/Slurm для понимания связи.
- [ ] Различать исполнение, snapshot consistency, convergence, scientific
  acceptance и вывод о гипотезе. Сохранять failures/restarts/непринятые попытки.
  Для QCL требовать явный `actionStatus`; completed не означает физический успех.
- [ ] Включить полный manifest с размерами и SHA-256 и внешние checksums финальных
  архивов/частей; определить покрытие metadata/manifest без self-hash цикла.
  Проверять пропущенные, повреждённые, неожиданные файлы и неполный multipart set.
  Использовать существующие receipts, не создавать конфликтующие истины.
- [ ] Реализовать QCL profile с документированными собственными полями и JSON-LD
  mappings. Проверять отдельно graph/profile, целостность файлов, HDF5 semantics
  и научную прослеживаемость. Отчёт содержит validator/version и scope проверки.
- [ ] Проверить автономную постобработку в чистом каталоге без сети, исходного
  checkout, AiiDA и Slurm: из включённых HDF5 восстановить заявленные метрики,
  таблицы и графики с оговорёнными допусками. Включить analysis scripts,
  локально доступные зависимости для заявленной платформы, schema/context
  resolver и инструкции. Не обещать полноту offline только по lock-файлу или URL.
  Полный повтор NEGF — отдельная возможность и отдельный бюджет.
- [ ] Предусмотреть fixtures: успешный и failed run, отсутствующая метрика,
  несколько attempts, внешняя зависимость, damaged/missing part, неверная единица,
  смена criteria после run, недоступный AiiDA. Не запускать новые production runs
  ради разработки упаковки; начать с малых явно синтетических fixtures.

RO-Crate повышает связность и проверяемость происхождения. Сохранность байтов и
валидный граф не доказывают физическую правильность; автономность требует
наличия всех заявленных данных/зависимостей и выполненного offline-теста.

### Официальные источники

- [Structure и целостность](https://www.researchobject.org/ro-crate/specification/1.3/structure.html)
  — базовая RO-Crate не требует полного inventory; это дополнительное требование QCL.
- [Data Entities](https://www.researchobject.org/ro-crate/specification/1.3/data-entities.html)
  — локальные и внешние данные.
- [Profiles](https://www.researchobject.org/ro-crate/specification/1.3/profiles.html)
  — `conformsTo` и тип профиля.
- [Process Run](https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/),
  [Workflow Run](https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/),
  [Provenance Run](https://www.researchobject.org/workflow-run-crate/profiles/provenance_run_crate/)
  — последовательные уровни описания выполненной работы.
