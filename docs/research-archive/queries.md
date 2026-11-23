# Контрольные выборки

## Fath, 54 мВ на период, радиальная мера и полный профиль

Выборка требует совпадения точки, изменённой радиальной меры и наблюдаемого полного профиля. Переход на основании только граничного тока сюда не попадает. В колонке «Общий вход» видна идентичность источника, если её проверили. Сравнение траекторий с разными историями сохраняет собственную запись.

```{needtable}
:filter: type == "qexperiment" and family == "Fath" and ("QP_FATH_54_10_DARK" in at or "QP_FATH_54_EARLY" in at) and "QPAM_RADIAL" in varies and "QO_JZ" in observes
:columns: ID, TITLE as "Опыт или вариант", SAME_INPUT as "Общий вход", STATUS as "Исполнение", STATIONARITY as "Стационарность", VERDICT as "Исход"
:colwidths: 17, 18, 14, 11, 14, 26
:style: TABLE
:sort: id
```

### Три строгих подтверждения

Не обнаружено опубликованных подтверждений стационарности в этой выборке. Критерий требует три последовательные свежие карты с прохождением допусков по невязкам, заряду, спектру и плоскостности. Независимое совпадение двух наблюдателей проверяет измерение профиля. [Замороженные условия](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/fath-v843/method-freeze.toml#L13-L18)

```{needtable}
:filter: type == "qexperiment" and family == "Fath" and ("QP_FATH_54_10_DARK" in at or "QP_FATH_54_EARLY" in at) and "QPAM_RADIAL" in varies and "QO_JZ" in observes and stationarity == "passed"
:columns: ID, TITLE as "Опыт или вариант", CRITERIA as "Критерий", VERDICT as "Исход"
:style: TABLE
:filter_warning: В этом срезе нет вариантов с тремя строгими подтверждениями.
```

В отдельной конечночастотной равновесной задаче {need}`QX_133_MATSUBARA_M3` три проверки прошли. Она имеет другие уравнения, смещение и наблюдаемые.

## Роль LO

### LO включён в постановку

```{needtable}
:filter: type == "qexperiment" and lo_mode == "enabled" and "QM_LO" not in targets and "QPAM_LO_DISCRETIZATION" not in varies
:columns: ID, TITLE as "Опыт или вариант", AT as "Рабочая точка", VARIES as "Изменённый фактор", OBSERVES as "Наблюдаемые"
:style: TABLE
:sort: id
```

### Проверяется LO-механизм

```{needtable}
:filter: type == "qexperiment" and "QM_LO" in targets
:columns: ID, TITLE as "Опыт или вариант", AT as "Рабочая точка", VARIES as "Изменённый фактор", VERDICT as "Исход"
:style: TABLE
:sort: id
```

### Меняется дискретизация LO

```{needtable}
:filter: type == "qexperiment" and "QPAM_LO_DISCRETIZATION" in varies
:columns: ID, TITLE as "Опыт или вариант", BASELINE as "База", VARIANTS as "Варианты", VERDICT as "Исход"
:style: TABLE
:sort: id
```

## V843 на общих входах

Строки сгруппированы по идентичности входа. Одно поле или одни параметры сами по себе не устанавливают общий источник.

```{needtable}
:filter: type == "qrun" and ("QP_V843_21" in at or "QP_V843_125" in at) and same_input
:columns: ID, TITLE as "Опыт или вариант", AT as "Рабочая точка", SAME_INPUT as "Общий вход", STATIONARITY as "Стационарность", VERDICT as "Исход"
:style: TABLE
:sort: id
```

## Непроверенная стационарность и открытые утверждения

```{needtable}
:filter: type in ["qexperiment", "qrun"] and stationarity in ["unverified", "not_measured"]
:columns: ID, TITLE as "Опыт или вариант", STATUS as "Исполнение", STATIONARITY as "Стационарность", STAGE as "Стадия", VERDICT as "Исход"
:style: TABLE
:sort: id
```

```{needtable}
:filter: type == "qclaim" and status == "open"
:columns: ID, TITLE as "Опыт или вариант", SUPPORTS_BACK as "Поддержано", LIMITS_BACK as "Ограничено", CONTRADICTS_BACK as "Возражения", EVIDENCE as "Свидетельства"
:style: TABLE
:sort: id
```

## Графы связей

```{needflow} Три варианта V843 на одном источнике
:filter: id in ["QX_V843_RADIAL_17", "QE_V843_COMMON_INPUT", "QR_V843_K5", "QR_V843_K9", "QR_V843_K17"]
:link_types: variants, same_input
:show_link_names:
```

```{needflow} Свидетельства и пределы интерпретации ночного Fath
:filter: id in ["QE_FATH_NIGHT_PROFILE", "QE_FATH_NIGHT_NODE", "QE_FATH_NIGHT_TRAJECTORIES", "QC_FATH_NIGHT_RADIAL_SENSITIVE", "QC_FATH_NIGHT_STATIONARY_CURRENT", "QC_FATH_NIGHT_LATE_BALANCE", "QC_FATH_NIGHT_ITERATION_SUFFICES"]
:link_types: evidence, supports, limits, contradicts
:show_link_names:
```

## Итоги контрольных выборок

В таблице радиального Fath пять опытов. Два локальных опыта охватывают вложенные сетки K25/K27/K31 и сдвиг новых узлов K31. Три ночных записи охватывают первую карту на K13/K25, исключение одного кольца и поздние траектории с разными историями. Строгих подтверждений в этой выборке ноль. Профили F13/F25 с одновременным изменением энергии, радиальной сетки и истории приведены в {need}`QX_FATH_F13_F25_PROFILE` как отдельная проверка переносимости.

Девять строк V843 распределены по трём общим источникам: по три сеточных варианта на каждом поле исходной кампании и отдельная тройка K5/K9/K17 на 21 кВ/см. Связи в таблице ведут к соответствующим идентичностям входов.
