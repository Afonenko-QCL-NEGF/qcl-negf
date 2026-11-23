# Fath 54 мВ на период. Ночная проверка устойчивости

```{qstructure} Fathololoumi et al., реконструкция CBO 149 мэВ v1
:id: QS_FATH
:family: Fath
:source: QL_FATHOLOLOUMI_2012

Порядок слоёв, координаты интерфейсов и материалы заданы в паспорте. Период 43,91 нм, донорный интервал 33,41–38,41 нм и листовая концентрация 3,0×10¹⁰ см⁻².
[Паспорт структуры](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/fath-v843/fath-device.toml#L1-L14)
```

```{qpoint} Fath, 54 мВ на период, 10 К, тёмный режим
:id: QP_FATH_54_10_DARK
:family: Fath
:structure: QS_FATH
:bias_kind: per_period
:bias_value: 54
:bias_unit: mV
:temperature: 10 K
:optical: dark
:sign: Электронный наклон −54 мэВ на период; положительный J вдоль +z
:lo_mode: enabled

Ночной вариант реконструкции с фиксированным нулевым Хартри. Работают LO, акустика, примеси, интерфейсная шероховатость и сплав.
[Условия](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/fath54-stability-night/README.md#L7-L17)
```

```{qparam} Радиальная мера и сетка k
:id: QPAM_RADIAL

Радиусы, узлы, ячейки и веса интегрирования по поперечному импульсу. Изменение радиальной меры действует на вход Дайсона и общую квадратуру.
```

```{qobservable} Полный пространственный профиль J(z)
:id: QO_JZ

Ток по физическим сечениям и двум ориентационно согласованным швам. Максимум отклонения, среднее, перепад между фиксированными сечениями и центрированная форма описывают разные свойства профиля.
```

```{qexperiment} Вложенное уточнение K13 → K25 на одной карте
:id: QX_FATH_NIGHT_RADIAL
:family: Fath
:at: QP_FATH_54_10_DARK
:varies: QPAM_RADIAL
:baseline: QR_FATH_NIGHT_K13_48
:variants: QR_FATH_NIGHT_K13_48, QR_FATH_NIGHT_K25_FIRST
:same_input: QE_FATH_MAP48
:observes: QO_JZ
:evidence: QE_FATH_NIGHT_PROFILE
:status: completed
:stationarity: failed
:lo_mode: enabled
:criteria: max(1 А/см², 1% модуля среднего контрольной руки) на общей сетке
:verdict: 15,306 А/см² при допуске 2,672 А/см² на общей K25

Обе руки начинают с одного сырого источника 48-й карты. Энергетическое окно и семь мод сохраняются. Положительные радиальные веса и перенос определены в k².
```

```{qevidence} Ночная радиальная пара, профиль и свежие карты
:id: QE_FATH_NIGHT_PROFILE
:availability: published
:locator: README, одна радиальная пара; profiles.csv, 145 сечений
:role: independent

[Первичный отчёт и метрики](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/fath54-stability-night/README.md#L146-L219) · [Численные профили](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/fath54-stability-night/evidence/profiles.csv)
```

```{needtable}
:filter: id == "QX_FATH_NIGHT_RADIAL"
:columns: ID, TITLE, AT, VARIES, OBSERVES, VERDICT
```

```{needflow} Радиальный опыт и его свидетельство
:filter: id in ["QX_FATH_NIGHT_RADIAL", "QP_FATH_54_10_DARK", "QE_FATH_NIGHT_PROFILE", "QPAM_RADIAL", "QO_JZ"]
:link_types: at, varies, observes, evidence
:show_link_names:
```

## Сравнения на общей карте и траекториях

```{qevidence} Источник ночной карты 48
:id: QE_FATH_MAP48
:availability: compact_only
:locator: measurements.json, coarse_input и input_sha
:role: common_input

Идентичность входа 48-й карты задаёт SHA-256 `326055b8a545b2401bcdebf5115e97817d7c9e3d4f53245303d339feb5c8372f`. Это вход после 47 обновлений F13, отличный по стадии от архивного исходного поля F13. Опубликованы отпечатки и компактные выходы.
[Численные свидетельства](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/fath54-stability-night/evidence/measurements.json#L3994-L3995)
```

```{qrun} K13, семь мод, карта 48
:id: QR_FATH_NIGHT_K13_48
:at: QP_FATH_54_10_DARK
:status: completed
:stationarity: failed
:stage: first_common_map
:evidence: QE_FATH_NIGHT_PROFILE
:verdict: mean J 256,387 А/см²; max отклонение 19,154 А/см²; свежий rK 0,012579

Производственная и независимая квадратуры вычисляют профиль на фиксированных сечениях.
```

```{qrun} K25, семь мод, первая свежая карта после переноса
:id: QR_FATH_NIGHT_K25_FIRST
:at: QP_FATH_54_10_DARK
:same_input: QR_FATH_NIGHT_K13_48
:status: completed
:stationarity: failed
:stage: first_common_map
:evidence: QE_FATH_NIGHT_PROFILE
:verdict: rK 0,601; rΣ 1,179; сырой входной заряд 3,21712×10¹⁰ см⁻²

Вход повторно решён Дайсоном и нормирован на новой сетке. Замена только квадратуры столкновений при фиксированном продолженном G даёт 0,582 А/см² по профилю. Совместная замена решения Дайсона и нормировки даёт 15,085 А/см². Зависимость этих операций от радиальной меры задана в вычислительной цепочке.
```

```{qexperiment} Исключение одного узла внутри K25
:id: QX_FATH_NIGHT_K24
:family: Fath
:at: QP_FATH_54_10_DARK
:varies: QPAM_RADIAL
:observes: QO_JZ, QO_CHARGE, QO_RESIDUAL
:targets: QM_DYSON_NORMALIZATION
:baseline: QR_FATH_NIGHT_K25_FIRST
:variants: QR_FATH_NIGHT_K25_FIRST, QR_FATH_NIGHT_K24_0175, QR_FATH_NIGHT_K24_0275
:same_input: QE_FATH_MAP48
:evidence: QE_FATH_NIGHT_NODE
:status: completed
:stationarity: failed
:lo_mode: enabled

Общие узлы и подблоки ядер сохранены, веса пересчитаны. Оба сравнения относятся к первой карте после переноса.
```

```{qrun} K24 без кольца 0,175 нм⁻¹
:id: QR_FATH_NIGHT_K24_0175
:status: completed
:stationarity: failed
:evidence: QE_FATH_NIGHT_NODE
:verdict: сырой заряд 2,98797×10¹⁰ см⁻²; max разность профилей с K25 9,225 А/см²
```

```{qrun} K24 без кольца 0,275 нм⁻¹
:id: QR_FATH_NIGHT_K24_0275
:status: completed
:stationarity: failed
:evidence: QE_FATH_NIGHT_NODE
:verdict: сырой заряд 3,21860×10¹⁰ см⁻²; max разность профилей с K25 5,935 А/см²
```

```{qevidence} Побитовый повтор и два измерения K24
:id: QE_FATH_NIGHT_NODE
:availability: published
:locator: README, таблица «Убранное кольцо»; независимый GL20
:supports: QC_FATH_NIGHT_RADIAL_SENSITIVE

GL20 подтвердил штатные профили в пределах 2,25×10⁻⁷ А/см².
[Таблица и исходный протокол](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/fath54-stability-night/README.md#L222-L245)
```

```{qexperiment} Доля свежего источника на общей карте 57
:id: QX_FATH_NIGHT_MIX
:family: Fath
:at: QP_FATH_54_10_DARK
:varies: QPAM_MIX
:observes: QO_JZ, QO_RESIDUAL, QO_STATIONARITY
:status: completed
:stationarity: failed
:lo_mode: enabled
:evidence: QE_FATH_NIGHT_TRAJECTORIES
:verdict: доли 0,35 и 1,0 дали rK 0,008913 и 0,007021; разность формы до 0,201 А/см²

Восемь обновлений каждой руки из одного состояния карты 57. Полная постановка и наблюдатели сохранены. Основная рука затем продолжена с долей 1,0.
```

```{qexperiment} Ранги 7/Q21 и 8/Q25, пространственный баланс
:id: QX_FATH_NIGHT_RANK
:family: Fath
:at: QP_FATH_54_10_DARK
:varies: QPAM_RANK
:targets: QM_LO
:observes: QO_JZ, QO_RESIDUAL, QO_STATIONARITY
:baseline: QR_FATH_NIGHT_K13_48
:variants: QR_FATH_NIGHT_K13_48, QR_FATH_NIGHT_R8_48, QR_FATH_NIGHT_R7_96, QR_FATH_NIGHT_R8_80
:same_input: QE_FATH_MAP48
:status: completed
:stationarity: failed
:lo_mode: enabled
:evidence: QE_FATH_NIGHT_TRAJECTORIES
:verdict: ΔJ на карте 48 меняется с +35,318 до +27,430 А/см²; поднятый LO-член с +35,967 до +22,468 А/см²

Сравнение на карте 48 использует вложенный источник. Поздняя пара карт 64/80 имеет разные длины траекторий и доли смешивания. Почти нулевой наружный поток через два шва характеризует периодический баланс на краях. Пространственное распределение проверено отдельно.
```

```{qrun} Q25, восемь мод, K13, карта 48
:id: QR_FATH_NIGHT_R8_48
:status: completed
:stationarity: failed
:same_input: QR_FATH_NIGHT_K13_48
:evidence: QE_FATH_NIGHT_TRAJECTORIES
:verdict: mean J 256,929 А/см²; max отклонение 16,155 А/см²; свежий rK 0,012470
```

```{qrun} Q21, семь мод, K13, карта 96
:id: QR_FATH_NIGHT_R7_96
:status: completed
:stationarity: failed
:evidence: QE_FATH_NIGHT_TRAJECTORIES
:verdict: rK 0,003727; max отклонение 18,106 А/см²
```

```{qrun} Q25, восемь мод, K13, карта 80
:id: QR_FATH_NIGHT_R8_80
:status: completed
:stationarity: failed
:evidence: QE_FATH_NIGHT_TRAJECTORIES
:verdict: rK 0,007071; max отклонение 15,595 А/см²
```

```{qexperiment} Продолжение K25 и сопоставление близких невязок с K13
:id: QX_FATH_NIGHT_RADIAL_TRAJECTORIES
:family: Fath
:at: QP_FATH_54_10_DARK
:varies: QPAM_RADIAL
:observes: QO_JZ, QO_RESIDUAL, QO_STATIONARITY
:status: completed
:stationarity: failed
:lo_mode: enabled
:evidence: QE_FATH_NIGHT_TRAJECTORIES
:verdict: max разность 16,382 А/см²; центрированное отличие 3,090 А/см²

Сопоставлены K13 карта 31 и K25 карта 16 после переноса. Отношения свежих невязок 1,028 и 1,025, истории разные. На карте 16 после переноса rK равен 0,01930; строгие критерии не пройдены. Архив F25 на 959 энергиях имеет другую историю.
```

```{qevidence} Свежие и архивные карты, полный профиль и баланс
:id: QE_FATH_NIGHT_TRAJECTORIES
:availability: published
:locator: fresh-maps.csv, profiles.csv и секция «Независимая ранговая проверка»
:role: independent
:limits: QC_FATH_NIGHT_STATIONARY_CURRENT

[Свежие карты](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/fath54-stability-night/evidence/fresh-maps.csv) · [Ранг и баланс](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/fath54-stability-night/README.md#L114-L144) · [Архивные траектории](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/fath54-stability-night/evidence/archive-trajectories.csv)
```

```{qclaim} Чувствительность полной свежей карты к радиальной мере
:id: QC_FATH_NIGHT_RADIAL_SENSITIVE
:status: supported
:evidence: QE_FATH_NIGHT_PROFILE, QE_FATH_NIGHT_NODE
:limits: QC_FATH_NIGHT_STATIONARY_CURRENT

Свидетельства ограничены конкретной общей картой и её радиальными переносами. Разложение выделяет совместный вклад повторного решения Дайсона и нормировки. Для отделения этих операций нужен другой контраст.
```

```{qclaim} Сеточный предел стационарного пространственного тока Fath
:id: QC_FATH_NIGHT_STATIONARY_CURRENT
:status: open
:stationarity: failed
:criteria: Три последовательные свежие карты с max(rK,rΣ,|λ−1|)<1e−8, спектральным дефектом <1e−3 и допуском на плоскостность
:evidence: QE_FATH_NIGHT_TRAJECTORIES

Поздний профиль остаётся пространственно неоднородным одновременно с малыми, но превышающими заданный порог невязками. Архивная сверка и GL20 подтверждают наблюдение промежуточного состояния.
```

## Открытые интерпретации

```{qclaim} Достаточно ли дальнейшего снижения невязки для плоского позднего профиля
:id: QC_FATH_NIGHT_ITERATION_SUFFICES
:status: open
:stationarity: failed
:evidence: QE_FATH_NIGHT_TRAJECTORIES

На основной траектории уменьшение свежего rK в 3,38 раза после карты 48 сопровождалось изменением максимальной неоднородности на 1,048 А/см². Ветвление с карты 57 проверяет только восемь обновлений каждой руки. Поведение предела остаётся открытым.
```

```{qclaim} Поздний перепад сохраняется при снижении невязки в изученном отрезке траектории
:id: QC_FATH_NIGHT_LATE_BALANCE
:status: supported
:evidence: QE_FATH_NIGHT_TRAJECTORIES
:contradicts: QC_FATH_NIGHT_ITERATION_SUFFICES
:limits: QC_FATH_NIGHT_STATIONARY_CURRENT

Лагированный перепад основной руки на карте 96 равен +32,817 А/см², вклад подстановки источника +0,323 А/см². Связь противоречия относится к достаточности наблюдавшегося снижения невязки, а не к неизмеренному стационарному пределу.
```
