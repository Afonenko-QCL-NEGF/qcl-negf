# Fath 54 мВ на период. Локальное сгущение

Кампания 23 ноября 2026 года проверила интервал 0,15–0,20 нм⁻¹
на одном побитово восстановленном входе 48-й карты F13. Все численные
сведения относятся к новым свежим картам до смешивания.
[Итоговый отчёт и данные](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/main/studies/fath54-local-radial/README.md)

```{qexperiment} Вложенное сгущение K25, K27, K31
:id: QX_FATH_LOCAL_RADIAL
:family: Fath
:at: QP_FATH_54_10_DARK
:varies: QPAM_RADIAL
:targets: QM_DYSON_NORMALIZATION
:observes: QO_JZ, QO_CHARGE, QO_RESIDUAL
:baseline: QR_FATH_LOCAL_K25
:variants: QR_FATH_LOCAL_K25, QR_FATH_LOCAL_K27, QR_FATH_LOCAL_K31
:same_input: QE_FATH_MAP48
:status: completed
:stationarity: failed
:stage: single_fresh_map
:lo_mode: enabled
:criteria: Профиль max(1 А/см², 1% модуля среднего контрольной руки); заряд 3×10⁸ см⁻²
:verdict: Профиль 4,5700 и 0,3894 А/см² на двух шагах; сырой заряд в допуске
:evidence: QE_FATH_LOCAL_K27, QE_FATH_LOCAL_K31

Сравнение сохраняет E481, семь мод, Q21, нулевой Хартри, пять каналов
и 10 К. K27 добавляет 0,1625 и 0,1875 нм⁻¹. K31 ещё раз делит
промежутки внутри окна пополам. Каждая рука получает прямой
консервативный перенос F13. На новых радиусах пересчитаны физические
парные ядра. Независимый GL20/sub3 измеряет 145 физических сечений.
```

```{qrun} K25, полный
:id: QR_FATH_LOCAL_K25
:at: QP_FATH_54_10_DARK
:status: completed
:stationarity: failed
:stage: single_fresh_map
:same_input: QE_FATH_MAP48
:evidence: QE_FATH_LOCAL_K27
:verdict: Среднее 254,298; макс. отклонение 17,763 А/см²

Полная исходная сетка с узлом 0,175 нм⁻¹. Архивный профиль повторён.
```

```{qrun} K27
:id: QR_FATH_LOCAL_K27
:at: QP_FATH_54_10_DARK
:status: completed
:stationarity: failed
:stage: single_fresh_map
:same_input: QE_FATH_MAP48
:evidence: QE_FATH_LOCAL_K27
:verdict: Среднее 257,304; макс. отклонение 19,008 А/см²

Новые радиусы 0,1625 и 0,1875 нм⁻¹. Вход перенесён напрямую с F13.
```

```{qrun} K31
:id: QR_FATH_LOCAL_K31
:at: QP_FATH_54_10_DARK
:status: completed
:stationarity: failed
:stage: single_fresh_map
:same_input: QE_FATH_MAP48
:evidence: QE_FATH_LOCAL_K31
:verdict: Среднее 257,172; макс. отклонение 18,943 А/см²

Ещё четыре радиуса внутри окна 0,15–0,20 нм⁻¹. Вход перенесён напрямую с F13.
```

```{qevidence} Компактные свидетельства K25 и K27
:id: QE_FATH_LOCAL_K27
:availability: published
:locator: studies/fath54-local-radial/evidence/measurements.json, levels.K25, levels.K27, differences.K25_to_K27
:role: independent
:supports: QC_FATH_LOCAL_CHARGE, QC_FATH_LOCAL_PROFILE
:limits: QC_FATH_NIGHT_STATIONARY_CURRENT

Сырой заряд на входе изменился на −7,6293×10⁷ см⁻². Разность полного
профиля 4,5700 А/см² превышает допуск 2,5430 А/см². Отдельно
зарегистрированы сдвиг среднего, центрированная форма и перепад
на 33,8473–39,6410 нм.
```

```{qevidence} Компактные свидетельства K31 и сверка независимого наблюдателя
:id: QE_FATH_LOCAL_K31
:availability: published
:locator: studies/fath54-local-radial/evidence/measurements.json, levels.K31, differences.K27_to_K31, metadata
:role: independent
:supports: QC_FATH_LOCAL_CHARGE, QC_FATH_LOCAL_PROFILE
:limits: QC_FATH_NIGHT_STATIONARY_CURRENT

Второй уровень меняет полный профиль на 0,3894 А/см² при допуске 2,5730 А/см². Профили на общих сечениях и заряд по ячейкам доступны в
{download}`CSV профилей <../../studies/fath54-local-radial/evidence/profiles.csv>`
и {download}`CSV радиального заряда <../../studies/fath54-local-radial/evidence/radial-charge.csv>`.
```

```{qparam} Путь консервативного переноса в радиальной мере
:id: QPAM_RADIAL_TRANSFER

Выбор между прямым переносом на целевую сетку и композицией консервативных переносов через промежуточную сетку.
```

```{qexperiment} Контроль переноса F13 → K25 → K31
:id: QX_FATH_LOCAL_RADIAL_PATH
:family: Fath
:at: QP_FATH_54_10_DARK
:varies: QPAM_RADIAL_TRANSFER
:targets: QM_DYSON_NORMALIZATION
:observes: QO_JZ, QO_CHARGE, QO_RESIDUAL
:baseline: QR_FATH_LOCAL_K31
:variants: QR_FATH_LOCAL_K31, QR_FATH_LOCAL_K31_PATH
:same_input: QE_FATH_MAP48
:status: completed
:stationarity: failed
:stage: single_fresh_map
:lo_mode: enabled
:criteria: Профиль max(1 А/см², 1% модуля среднего контрольной руки); заряд 3×10⁸ см⁻²
:verdict: Макс. разность профилей 0,132 А/см²
:evidence: QE_FATH_LOCAL_K31_PATH

Целевая сетка и физика одинаковы. Последовательный перенос вводит промежуточную сетку K25.
```

```{qrun} K31 после последовательного переноса
:id: QR_FATH_LOCAL_K31_PATH
:at: QP_FATH_54_10_DARK
:status: completed
:stationarity: failed
:stage: single_fresh_map
:same_input: QE_FATH_MAP48
:evidence: QE_FATH_LOCAL_K31_PATH
:verdict: Среднее 257,114; макс. отклонение 18,910 А/см²

Контроль выполняет полный оператор рассеяния и независимое наблюдение.
```

```{qevidence} Прямой и последовательный перенос на K31
:id: QE_FATH_LOCAL_K31_PATH
:availability: published
:locator: studies/fath54-local-radial/evidence/measurements.json, followup.path и followup.path_difference
:role: independent
:limits: QC_FATH_LOCAL_PROFILE, QC_FATH_NIGHT_STATIONARY_CURRENT

Разность входного сырого заряда 1,62×10⁷ см⁻². Изменение среднего −0,0575 А/см².
```

```{qexperiment} Радиальный контроль со сдвигом новых узлов K31
:id: QX_FATH_LOCAL_RADIAL_SHIFT
:family: Fath
:at: QP_FATH_54_10_DARK
:varies: QPAM_RADIAL
:targets: QM_DYSON_NORMALIZATION
:observes: QO_JZ, QO_CHARGE, QO_RESIDUAL
:baseline: QR_FATH_LOCAL_K31
:variants: QR_FATH_LOCAL_K31, QR_FATH_LOCAL_K31_SHIFT
:same_input: QE_FATH_MAP48
:status: completed
:stationarity: failed
:stage: single_fresh_map
:lo_mode: enabled
:criteria: Профиль max(1 А/см², 1% модуля среднего контрольной руки); заряд 3×10⁸ см⁻²
:verdict: Макс. разность профилей 0,251 А/см²
:evidence: QE_FATH_LOCAL_K31_SHIFT

Шесть новых узлов сдвинуты внутри двух промежутков K25. Исходные узлы K25 сохранены. Пересчитаны веса, ядра и полный профиль.
```

```{qrun} K31 со сдвигом новых радиусов
:id: QR_FATH_LOCAL_K31_SHIFT
:at: QP_FATH_54_10_DARK
:status: completed
:stationarity: failed
:stage: single_fresh_map
:same_input: QE_FATH_MAP48
:evidence: QE_FATH_LOCAL_K31_SHIFT
:verdict: Среднее 257,229; макс. отклонение 19,016 А/см²

Прямой перенос F13 и положительные веса ячеек в k².
```

```{qevidence} Профиль, сырой заряд и энергетический контроль сдвига
:id: QE_FATH_LOCAL_K31_SHIFT
:availability: published
:locator: studies/fath54-local-radial/evidence/measurements.json, differences.K31_to_shift и followup.localization_shifted
:role: independent
:supports: QC_FATH_LOCAL_PROFILE
:limits: QC_FATH_NIGHT_STATIONARY_CURRENT

GL20 измеряет все сечения. На выбранных кольцах проверена чувствительность наблюдаемых к порядку энергетического интеграла. {download}`Энергетические данные сдвинутой сетки <../../studies/fath54-local-radial/evidence/localization-shifted.json>`.
```

```{qclaim} Сырой заряд на этой карте устойчив по инженерному допуску
:id: QC_FATH_LOCAL_CHARGE
:status: supported
:evidence: QE_FATH_LOCAL_K27, QE_FATH_LOCAL_K31
:limits: QC_FATH_NIGHT_STATIONARY_CURRENT

На обоих вложенных шагах изменение сырого заряда укладывается в 3×10⁸ см⁻². На втором шаге вклад свежего заряда внутри окна почти компенсируется вкладом остальной области.
```

```{qclaim} Локальная радиальная мера влияет на форму и средний ток свежей карты
:id: QC_FATH_LOCAL_PROFILE
:status: supported
:evidence: QE_FATH_LOCAL_K27, QE_FATH_LOCAL_K31
:limits: QC_FATH_NIGHT_STATIONARY_CURRENT

На первом шаге превышен допуск по полному и центрированному профилю. На втором шаге обе разности укладываются в допуск. Пространственная неоднородность на K31 сохраняется при больших свежих невязках.
```
