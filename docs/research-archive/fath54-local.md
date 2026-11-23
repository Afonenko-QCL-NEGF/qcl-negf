# Fath 54 мВ на период. Локальное сгущение

Кампания 23 ноября проверяет чувствительность к узлам в интервале 0,15–0,20 нм⁻¹. Срез включает компактное локальное состояние до K27. Физическая сессия продолжает работу независимо. За доступностью последующих стадий следите по этой карточке.

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
:status: partial
:stationarity: failed
:stage: single_fresh_map
:lo_mode: enabled
:criteria: Профиль max(1 А/см², 1% модуля среднего контрольной руки); заряд 3×10⁸ см⁻²
:verdict: K25→K27, max разность профилей 4,5700 А/см² при допуске 2,5430; заряд в допуске
:evidence: QE_FATH_LOCAL_K27

Сравнение сохраняет 481 энергию, семь мод, нулевой Хартри, пять каналов и температуру 10 К. K27 добавляет 0,1625 и 0,1875 нм⁻¹ к K25. Консервативный перенос из K13 сделан отдельно на каждую сетку. На новых радиусах заново применяются Дайсон, нормировка и оператор рассеяния. GL20/sub3 проверяет профиль независимо. Порог пространственного отклонения и три последовательные свежие проверки относятся к отдельному критерию стационарности.
```

```{qrun} Опорная K25 в кампании локального сгущения
:id: QR_FATH_LOCAL_K25
:at: QP_FATH_54_10_DARK
:status: completed
:stationarity: failed
:stage: single_fresh_map
:same_input: QE_FATH_MAP48
:evidence: QE_FATH_LOCAL_K27

Контрольная рука сравнения со средним 254,298 А/см².
```

```{qrun} K27 с двумя новыми радиусами
:id: QR_FATH_LOCAL_K27
:at: QP_FATH_54_10_DARK
:status: completed
:stationarity: failed
:stage: single_fresh_map
:same_input: QE_FATH_MAP48
:evidence: QE_FATH_LOCAL_K27
:verdict: среднее +3,0057; центрированное отличие 2,5828; изменение перепада +3,5222 А/см²

Изменение сырого входного заряда −7,6293×10⁷ см⁻² и изменение сырого заряда свежего образа −3,5593×10⁷ см⁻² проходят сеточный допуск. Разность полного профиля превышает допуск с учётом разности независимых наблюдений.
```

```{qrun} K31 и условные контроли
:id: QR_FATH_LOCAL_K31
:at: QP_FATH_54_10_DARK
:status: partial
:stationarity: not_measured
:stage: preflight
:same_input: QE_FATH_MAP48

В срезе доступны предварительные проверки сеток и входов. Итоги полной карты K31, проверки пути переноса, сдвинутых узлов или ранга в архиве пока отсутствуют.
```

```{qevidence} Компактное состояние локального сравнения K25 и K27
:id: QE_FATH_LOCAL_K27
:availability: local
:locator: Fath 54 local radial 2026-11-23 accepted K27; differences.K25_to_K27; metadata.replay
:role: independent
:limits: QC_FATH_NIGHT_STATIONARY_CURRENT

Локальная идентичность `fath54-local-radial/accepted-K27`, поля `differences.K25_to_K27`, `levels.K25`, `levels.K27` и `metadata.replay`. Вход и свежий образ контрольной ночной карты 48 воспроизведены побитово. Компактный срез содержит 145 сечений. Полное вычислительное состояние остаётся в физической сессии.
```
