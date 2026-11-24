# Fath 54 мВ на период. Вложенные ранги на K31

Рабочая точка, источник F13 и основная радиальная мера связаны с
{need}`QP_FATH_54_10_DARK`, {need}`QE_FATH_MAP48` и {need}`QR_FATH_LOCAL_K31`.

```{qexperiment} Сопоставление вложенных 7/Q21 и 8/Q25 на K31
:id: QX_FATH_K31_RANK
:family: Fath
:at: QP_FATH_54_10_DARK
:varies: QPAM_RANK
:targets: QM_LO, QM_DYSON_NORMALIZATION
:observes: QO_JZ, QO_CHARGE, QO_RESIDUAL, QO_STATIONARITY
:baseline: QR_FATH_K31_Q21
:variants: QR_FATH_K31_Q21, QR_FATH_K31_Q25
:same_input: QE_FATH_MAP48
:status: completed
:stationarity: failed
:stage: matched_fresh_trajectory
:lo_mode: enabled
:criteria: Обе свежие невязки в отношении до 1,25; три последовательные строгие карты для стационарности
:evidence: QE_FATH_K31_RANK_TRAJECTORY, QE_FATH_K31_RANK_BALANCE, QE_FATH_K31_RANK_CONTROL
:verdict: 32 свежие карты на ранг, разность формы 9,216 А/см² на паре GL20

Прямой перенос F13 на K31 общий. Вложение восьмой транспортной моды расширяет координатный кадр Q21 до Q25. Радиусы, веса, границы энергии и физические сечения совпадают.
```

```{qrun} Основная K31, семь мод и Q21
:id: QR_FATH_K31_Q21
:at: QP_FATH_54_10_DARK
:same_input: QE_FATH_MAP48
:status: completed
:stationarity: failed
:evidence: QE_FATH_K31_RANK_TRAJECTORY, QE_FATH_K31_RANK_BALANCE

Источники первой карты совпали побитово. Профиль GL20 совпал по всем сечениям с {need}`QE_FATH_LOCAL_K31`. На карте 32 среднее 245,785 А/см², максимальное отклонение 18,323 А/см².
```

```{qrun} Основная K31, восемь мод и Q25
:id: QR_FATH_K31_Q25
:at: QP_FATH_54_10_DARK
:same_input: QE_FATH_MAP48
:status: completed
:stationarity: failed
:evidence: QE_FATH_K31_RANK_TRAJECTORY, QE_FATH_K31_RANK_BALANCE

Проверены общие моды, подблок гамильтониана, метрика и обратное ограничение источника. На карте 32 среднее 246,262 А/см², максимальное отклонение 15,228 А/см².
```

```{qevidence} Свежие невязки, заряд и полный J(z)
:id: QE_FATH_K31_RANK_TRAJECTORY
:source: QE_FATH_MAP48, QE_FATH_LOCAL_K31
:availability: published
:role: fresh_trajectory
:locator: studies/fath54-k31-rank/evidence/trajectory.jsonl — configuration, map, assessment

Профили включают оба шва и фиксированные физические сечения. Карты измеряются до смешивания. [Итоговый отчёт](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/main/studies/fath54-k31-rank/README.md)
```

```{qevidence} Независимая квадратура и знаковый баланс
:id: QE_FATH_K31_RANK_BALANCE
:source: QE_FATH_K31_RANK_TRAJECTORY
:availability: published
:role: independent
:locator: studies/fath54-k31-rank/evidence/trajectory.jsonl — GL20

На общем наборе сечений измеряются лагированный и синхронный балансы, пять каналов, проекция и разложение гамильтонова тока по связям.
```

```{qclaim} Стационарность пространственного тока на K31
:id: QC_FATH_K31_RANK_STATIONARY
:status: open
:stationarity: failed
:criteria: Три свежие карты с max(rK,rΣ,|λ−1|)<10⁻⁸, спектральным дефектом <10⁻³ и плоскостностью
:evidence: QE_FATH_K31_RANK_TRAJECTORY, QE_FATH_K31_RANK_BALANCE
:limits: QC_FATH_NIGHT_STATIONARY_CURRENT

Ноль строгих подтверждений для обоих рангов. Сопоставимые свежие невязки в последней паре порядка 10⁻². Остаточная неоднородность превышает порог 1% среднего тока.
```

```{needtable}
:filter: id in ["QX_FATH_K31_RANK", "QR_FATH_K31_Q21", "QR_FATH_K31_Q25"]
:columns: ID, TITLE, STATUS, STATIONARITY, VERDICT
```

```{qclaim} Трансляционная связь источников Fath
:id: QC_FATH_K31_SINGLE_PERIOD
:status: supported
:source: QL_KUBIS_PERIODICITY, QE_FATH_MAP48

В девяти копиях цепочки Дайсона общий источник оценивается со сдвигами энергии. Самосогласованное обновление возвращает один пакет центрального периода. Для проверки пространственного чередования населённостей нужна двухпериодная суперячейка с независимыми источниками.
```

```{qevidence} Вращение W и Q, проекция LO и два обновления на общем входе
:id: QE_FATH_K31_RANK_CONTROL
:source: QE_FATH_K31_RANK_TRAJECTORY
:availability: published
:role: controlled_comparison
:locator: studies/fath54-k31-rank/evidence/trajectory.jsonl, unitary_control, LO_operator_control, update_control

Полный профиль GL20 при вращении W и Q различается не более чем на 1,90×10⁻¹¹ А/см². Отдельная относительная сверка узлового тока даёт 4,88×10⁻⁶ при пороге 10⁻⁶. При обновлении 1,0 свежие невязки на четвёртой карте контроля ниже на 15–16%, перепады уменьшаются дополнительно на 0,046 и 0,060 А/см² по отношению к 0,35.
```

```{qclaim} Разность формы J(z) сохраняется при понижении двух свежих невязок
:id: QC_FATH_K31_RANK_SHAPE
:status: supported
:evidence: QE_FATH_K31_RANK_TRAJECTORY, QE_FATH_K31_RANK_BALANCE, QE_FATH_K31_RANK_CONTROL
:limits: QC_FATH_K31_RANK_STATIONARY

По GL20 разность центрированной формы равна 10,54 А/см² на первой карте и 9,22 А/см² на карте 32. В синхронном балансе уменьшение LO частично компенсируется проекцией. Результат относится к совместному изменению W и Q при конечных невязках.
```

## Перенос на V843

```{qparam} Представление фиксированного подпространства
:id: QPAM_BASIS_REPRESENTATION

Комплексное унитарное вращение мод W и координат Q при сохранении их размерностей и линейных оболочек.
```

```{qexperiment} Унитарный контроль V843 при 21 кВ/см и 50 К
:id: QX_V843_LOCAL_UNITARY
:family: V843
:at: QP_V843_21
:varies: QPAM_BASIS_REPRESENTATION
:targets: QM_DYSON_NORMALIZATION, QM_LO
:observes: QO_JZ, QO_RESIDUAL, QO_CHARGE, QO_SUBBANDS
:baseline: QR_V843_LOCAL_NATIVE
:variants: QR_V843_LOCAL_NATIVE, QR_V843_LOCAL_ROTATED
:same_input: QE_V843_GRID_INPUT_21
:source: QE_V843_PUBLISHED, QE_V843_FIG1
:evidence: QE_V843_LOCAL_UNITARY
:status: completed
:stationarity: failed
:stage: single_fresh_map
:verdict: Разность GL20 1,08×10⁻¹⁰ А/см², rK 0,18651, rΣ 0,58858
:lo_mode: enabled

Общий ранний архивный вход E239 K5, собственные 11 мод и Q28. Сравнение средних токов с опубликованными NEGF50 и DM50 относится к отдельным результатам. Архивная карта 48 приведена как другой этап этой траектории.
```

```{qrun} V843, исходные W и Q
:id: QR_V843_LOCAL_NATIVE
:at: QP_V843_21
:same_input: QE_V843_GRID_INPUT_21
:evidence: QE_V843_LOCAL_UNITARY
:status: completed
:stationarity: failed
```

```{qrun} V843, повернутые W и Q
:id: QR_V843_LOCAL_ROTATED
:at: QP_V843_21
:same_input: QE_V843_GRID_INPUT_21
:evidence: QE_V843_LOCAL_UNITARY
:status: completed
:stationarity: failed
```

```{qevidence} Узловые и интегральные проверки V843
:id: QE_V843_LOCAL_UNITARY
:availability: published
:source: QE_V843_GRID_INPUT_21, QE_V843_PUBLISHED, QE_V843_FIG1
:role: controlled_comparison
:locator: studies/fath54-k31-rank/evidence/v843/trajectory.jsonl

Причинные компоненты и карта рассеяния сопоставлены в общих координатах. GL20 даёт среднее 1264,136 А/см², e/u = 39,873 и сильную пространственную неоднородность на ранней карте.
```

```{qclaim} Узловая относительная сверка V843 чувствительна к спектральному хвосту
:id: QC_V843_LOCAL_UNITARY
:status: supported
:evidence: QE_V843_LOCAL_UNITARY, QE_FATH_K31_RANK_CONTROL

На −650 мэВ контрольная норма тока составляет 4,33×10⁻¹⁸ в локальных единицах. Абсолютная разность 2,79×10⁻²³ даёт формальное превышение относительного порога. Прямые матрицы сечений ковариантны до 1,48×10⁻¹⁶.
```

## Перенос на LiEL2014

```{qstructure} LiEL2014, Лидс
:id: QS_LIEL2014
:family: LiEL2014
:source: QL_LI_HYBRID, QL_WINGE_TRENDS

Период 61,50 нм. Заключительная инжекторная яма GaAs длиной 17,20 нм легирована Si до 3,0×10¹⁶ см⁻³. Листовая плотность 5,16×10¹⁰ см⁻².
```

```{qpoint} LiEL2014, 50 мВ на период, 77 К, тёмный режим
:id: QP_LIEL2014_DARK50
:family: LiEL2014
:structure: QS_LIEL2014
:bias_kind: per_period
:bias_value: 50
:bias_unit: mV
:temperature: 77 K
:optical: dark
:sign: Электронный потенциал падает на 50 мэВ вдоль +z
:lo_mode: enabled
:source: QL_WINGE_TRENDS
```

```{qobservable} Пространственно-энергетическая плотность носителей
:id: QO_SPATIAL_ENERGY_DENSITY

Карта n(z,E), интегральный заряд и локализация заселённости. Сравнение с опубликованной картой требует общей оси z и единого начала энергии.
```

```{qobservable} Инверсия населённостей
:id: QO_POPULATION_INVERSION

Разность заселённостей верхнего и нижнего лазерных состояний при зафиксированных метках. Однозначность знака оценивается по сопоставимым кандидатам.
```

```{qparam} Физические приближения тёмного переноса LiEL2014
:id: QPAM_LIEL_TRANSPORT_MODEL

Продольный гамильтониан, поперечная мера, электростатика и столкновительные модели при фиксированной точке.
```

```{qexperiment} Тёмная карта n(z,E) LiEL2014 и знак инверсии
:id: QX_LIEL2014_DARK_DENSITY
:family: LiEL2014
:at: QP_LIEL2014_DARK50
:varies: QPAM_LIEL_TRANSPORT_MODEL
:targets: QM_DYSON_NORMALIZATION
:observes: QO_SPATIAL_ENERGY_DENSITY, QO_POPULATION_INVERSION, QO_RESIDUAL, QO_STATIONARITY
:baseline: QR_LIEL2014_WINGE
:variants: QR_LIEL2014_WINGE, QR_LIEL2014_LOCAL
:source: QL_WINGE_TRENDS, QL_LI_HYBRID
:evidence: QE_LIEL2014_LOCAL_DENSITY
:status: completed
:stationarity: failed
:lo_mode: enabled
:verdict: Инверсия +9,62×10⁸ см⁻² на последней карте, rK 0,02238, rΣ 0,01579

Сопоставляется результат штатного локального Runner с качественной картой Winge. Сравнение учитывает разницу продольной модели, поперечного импульса, электростатики и столкновений.
```

```{qrun} LiEL2014, расчёт Winge на рис. 3
:id: QR_LIEL2014_WINGE
:at: QP_LIEL2014_DARK50
:source: QL_WINGE_TRENDS
:status: published
:stationarity: unknown
:verdict: Положительная инверсия и заполнение инжектора и верхнего уровня
```

```{qrun} LiEL2014, локальный Runner
:id: QR_LIEL2014_LOCAL
:at: QP_LIEL2014_DARK50
:source: QL_LI_HYBRID, QL_WINGE_TRENDS
:evidence: QE_LIEL2014_LOCAL_DENSITY
:status: completed
:stationarity: failed
```

```{qevidence} Локальная карта n(z,E), невязки и заселённости LiEL2014
:id: QE_LIEL2014_LOCAL_DENSITY
:availability: published
:source: QL_WINGE_TRENDS, QL_LI_HYBRID
:role: computed
:locator: studies/fath54-k31-rank/evidence/liel/

Два блока по 96 карт SCBA. Локальная карта сохраняет интегральный заряд 5,16×10¹⁰ см⁻². Пара 4→3 даёт положительную инверсию на двух наблюдавшихся состояниях. Стационарность ограничивают в том числе спектральная сумма и непрерывность тока.
```

```{qclaim} Положительная инверсия и заполнение инжекторной ямы LiEL2014
:id: QC_LIEL2014_LOCAL_INVERSION
:status: supported
:stationarity: failed
:evidence: QE_LIEL2014_LOCAL_DENSITY
:source: QL_WINGE_TRENDS

Качественный знак и локализация согласуются с рис. 3 Winge в наблюдавшихся состояниях шестимодового расчёта. Амплитуды и стационарная инверсия остаются открытыми.
```

```{needflow} Три рабочие точки и источники сравнения
:filter: id in ["QX_FATH_K31_RANK", "QP_FATH_54_10_DARK", "QE_FATH_K31_RANK_CONTROL", "QC_FATH_K31_SINGLE_PERIOD", "QL_KUBIS_PERIODICITY", "QX_V843_LOCAL_UNITARY", "QP_V843_21", "QE_V843_PUBLISHED", "QX_LIEL2014_DARK_DENSITY", "QP_LIEL2014_DARK50", "QL_WINGE_TRENDS", "QL_LI_HYBRID"]
:link_types: at, evidence, source
:show_link_names:
```
