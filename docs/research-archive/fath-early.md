# Ранние кампании: Green AA, Fath и предшественники Dupont

Срез источников — 23 ноября 2026. Завершение программы означает завершение назначенных карт, а не принятую стационарность. Оригинальные отчёты и их числовые приложения сохранены по прежним путям. Обозначения A1328, B164 и #512 — состояния разных историй, а не взаимозаменяемые решения.

## Green AA: метод при 1 мВ

```{qexperiment} Green AA против штатной SCBA
:id: QX_GREEN_AA
:status: completed
:family: Green AA
:at: QP_133_1MV_70K
:lo_mode: enabled
:varies: QPAM_GREEN_METHOD
:observes: QO_RESIDUAL
:evidence: QE_GREEN_AA
:stationarity: failed
:criteria: Совместные строгие проверки на свежих штатных картах
:verdict: Строгих проходов нет; выигрыш по сходимости не установлен

На общем сохранённом состоянии от 16 ноября и Core e171, без e–e, контроль выполнил 32 карты с αΣ=0,2; ветвь по трём полям G — 28 карт и четыре свежие штатные проверки с αΣ=1. Конечные rΣ 0,00328264 и 0,00671730; rK 0,00122467 и 0,00115871 соответственно. На первой штатной проверке ветвь G имела меньшую rΣ, но затем ухудшилась. Время не доказывает ускорение, поскольку проверки делались по-разному; Anderson, возвраты и изменение смешивания не разделены.
```

```{qparam} Переменные итерации Green AA и правило смешивания
:id: QPAM_GREEN_METHOD
```

```{qevidence} Отчёт и агрегаты Green AA
:id: QE_GREEN_AA
:availability: local_compact
:locator: green-aa-20261118/report.md; comparison-summary.json

Локальное компактное свидетельство: `green-aa-20261118/report.md`, таблица конечных невязок и описание 29-й карты; `comparison-summary.json`. Отдельный прямой 18×18 oracle проверяет композицию embedding/Dyson, а не физические модели рассеяния. Публичный адрес этого локального отчёта не установлен.
```

## Fath 18 ноября: транспорт и представление

```{qpoint} Fath: тёмная точка 54 мВ на период, 10 K
:id: QP_FATH_54_EARLY
:family: Fath
:structure: QS_FATH
:bias_kind: per_period
:bias_value: 54
:bias_unit: mV
:sign: электронный наклон −54 мэВ на период
:temperature: 10 K
:optical: dark

Период 43,91 нм соответствует полю 12,2979 кВ/см. В раннем основном транспорте Хартри фиксирован на нуле, e–e выключен; включены LO, acoustic, impurity, IFR и alloy. Основной CBO 149 мэВ; модель IFR гауссова, тогда как в tutorial указана экспоненциальная корреляция.
```

```{qexperiment} Fath native54: продолжение штатной траектории
:id: QX_FATH_NATIVE_18
:supports: QC_FATH_EARLY_UNACCEPTED
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:observes: QO_CURRENT, QO_JZ, QO_RESIDUAL
:evidence: QE_FATH_18, QE_FATH_NATIVE54_SNAPSHOTS
:lo_mode: enabled
:stationarity: failed
:criteria: rΣ, rK, |λ−1| < 1e-8; спектральная сумма < 0,001 и другие проверки
:verdict: 910 различных состояний; строгого принятия нет

Nz144/Nb7, E4801×k25, −400…560 мэВ; 128+16+768−2 повторные карты. На конце rΣ=0,0217016, rK=0,00305935, |λ−1|=2,57422e−5; спектральный максимум 0,0112097. Независимые J₊/J₋ +123,157633/−122,838294 А/см², внутренний J(z) 1,095…196,202 А/см². Близость граничных токов не устанавливает пространственную непрерывность или стационарный ток.
```

```{qexperiment} Fath: спектральный базис и конечное окно
:id: QX_FATH_BASIS_18
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:varies: QPAM_FATH_BASIS
:observes: QO_RESIDUAL, QO_CURRENT
:evidence: QE_FATH_18
:lo_mode: enabled
:stationarity: failed
:verdict: Низкоэнергетическая точность улучшена; транспорт не принят

PzP7 сравнивали с компактными POD9/POD10. На Nz144/192 худший низкоэнергетический критерий для POD9 — 0,1805 мэВ при допуске 0,5 мэВ, для POD10 — 0,0605 мэВ при допуске 0,10 мэВ. Отдельный interacting wide54-pod9 после 96 карт: rΣ=0,06595, rK=0,04300, спектральная сумма 0,009004; статический тест широкого окна не является принятой транспортной точкой. В отдельной паре 64 холодных карт расширение Emax 560→860 мэВ меняет J₊ на 0,059%; независимость от окна не установлена.
```

```{qparam} Базис Fath
:id: QPAM_FATH_BASIS
```

```{qexperiment} Fath: равновесие и перенос в 54 мВ
:id: QX_FATH_EQUIL_TRANSFER
:status: completed
:family: Fath
:observes: QO_RESIDUAL, QO_CURRENT
:evidence: QE_FATH_18
:lo_mode: enabled
:stationarity: failed
:verdict: Полная приёмка равновесия и перенос в 54 мВ не достигнуты

При 0 мВ FDT-старт и продолжение без проекции дали на карте 128 rΣ=1,184e−10 и rK=2,314e−13, но относительное изменение тока 0,0529 превышало 1e−4, независимая спектральная сумма 0,0784 — допуск 0,001. Перенос локальных Σ в 54 мВ с пересборкой G и границ без FDT после 256 карт не улучшил совместный критерий относительно холодного старта. Это разные рабочие точки и истории.
```

```{qevidence} Публикация кампании 18 ноября
:id: QE_FATH_18
:availability: public
:locator: report.md, таблицы «Нативный транспорт» и «Улучшение базиса»; transport/native54-03/history.csv

[Отчёт и ссылки на исходные паспорта и аудит](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath-20261118/report.md). Внешний MEDIUM-ориентир J≈513,79 А/см² не является тождественным noEE-расчётом: его полный вход и данные недоступны.
```

## 19 ноября: LO, B164 и радиальные контрольные опыты

```{qexperiment} Fath: разрешение продольного интеграла LO
:id: QX_FATH_LO_19
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:varies: QPAM_LO_DISCRETIZATION
:targets: QM_LO
:observes: QO_RESIDUAL
:evidence: QE_FATH_19
:lo_mode: enabled
:stationarity: failed
:verdict: Исходные 81 узел имели большой алиас; B641 остаётся непринятой

На том же пределе qz ±10 нм⁻¹ 81 узел даёт отклонение полного проецированного LO-тензора 0,92218 от независимого интеграла, 641 узел — 8,89e−11. На общих входах A1328 и A1613 сравнивали A81/B641 до смешивания; физический отклик и последующее продолжение не сводятся к различию одних конечных состояний. На B36 фиксированное G при переходе от конечного предела к полной прямой меняет rK на +0,41%.
```

```{qrun} Fath B164
:id: QR_FATH_B164
:supports: QC_FATH_EARLY_UNACCEPTED
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:observes: QO_JZ, QO_RESIDUAL
:evidence: QE_FATH_19
:lo_mode: enabled
:stationarity: failed
:criteria: Три последовательные свежие карты с rΣ, rK, |λ−1| < 1e−8 и спектром < 0,001 на всех k
:verdict: 0 строгих карт из 164

Исправленная B641, PzP7, E4801×25, Nz144: rΣ=0,0256134, rK=0,00140485, |λ−1|=2,96357e−5. Точный межузловой спектральный максимум 0,00992566; не проходит ни одно из 25 колец. J(z) 1,03797…184,58509 А/см². Стационарная величина и её численная неопределённость не определены.
```

```{qexperiment} B36: вложенные радиальные кольца и энергия
:id: QX_FATH_RADIAL_19
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:varies: QPAM_RADIAL
:observes: QO_RESIDUAL
:evidence: QE_FATH_19
:lo_mode: enabled
:stationarity: unverified
:verdict: Сильная чувствительность; сходимость по радиальной сетке не установлена

Вложенная пара 25→33 k на B36: точный максимум спектральной суммы входа/образа 0,009868/0,009876 → 0,042568/0,133107; сырой λ после точного интегрирования 0,99568→1,39873. При 33k сгущение 4801→5539 энергий меняет спектр образа 0,133107→0,046755, rK 153,08→342,17. Это сравнение метрик и заряда; полный J(z) для него в итоговой таблице не указан.
```

```{qevidence} Итог и независимые метрики 19 ноября
:id: QE_FATH_19
:availability: public
:locator: final.md, таблица «Сравнение карт» и раздел «Двенадцать направлений»; evidence/metrics.json

[Итог второй кампании](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath54-20261119-followup/final.md); [метрики](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath54-20261119-followup/evidence/metrics.json). Отдельные опытные строки, в том числе α=0,10/0,20, прямой/PI, LO/LO+примеси и равное время линейного/Anderson, перечислены в исходной таблице с индивидуальными условиями и исходами.
```

## 20 ноября: #512 и первые связанные Fath/Dupont

```{qrun} Причинная траектория Fath до #512
:id: QR_FATH_CAUSAL_512
:supports: QC_FATH_EARLY_UNACCEPTED
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:observes: QO_RESIDUAL, QO_JZ
:evidence: QE_FATH_20
:lo_mode: enabled
:stationarity: failed
:verdict: 384 новых карты; строгих проходов нет

rΣ=0,00401543, rK=0,000694131, |λ−1|=3,28779e−5. Узловой, аффинный и контурный спектральные максимумы свежего образа 0,02703827, 0,01706220 и 0,0006994407: 0/25, 0/25 и 25/25 колец. Среднее J(z) 80,56086 А/см², максимальное отклонение 92,32222 А/см². Контурная проверка не заменяет остальные требования.
```

```{qexperiment} Fath: полные E5658 на 25 и 34 кольцах
:id: QX_FATH_RADIAL_20
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:varies: QPAM_RADIAL
:observes: QO_RESIDUAL, QO_CURRENT
:evidence: QE_FATH_20
:lo_mode: enabled
:stationarity: failed
:verdict: После карты 48 оба плеча вне спектрального допуска

На #48 rK на собственных весах 0,00463936 и 0,02028926, на общих прежних весах 0,00463936 и 0,01388717. Спектр 0/25 и 0/34. Отчёт показывает граничные токи, но не полный сопоставимый J(z) этой пары; не следует засчитывать её как подтверждение сходимости профиля.
```

```{qevidence} Итог 20 ноября
:id: QE_FATH_20
:availability: public
:locator: final.md, разделы «Установленные зависимости» и «Сходимость, ток и модель»

[Отчёт кампании](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath54-20261120/final.md). В таблице отдельно приведены вставки E9133/E9135, разрежение E9135/E8929, полость 4801/4971 и 96 карт, нормировка, замена примесной вершины, шероховатость, два каскада и Хартри. Для каждого указаны исход и предел применимости.
```

```{qexperiment} Предшественник связанной модели Fath и Dupont V843
:id: QX_FATH_DUPONT_PRECURSOR
:status: partial
:family: Fath/Dupont
:observes: QO_CURRENT, QO_JZ, QO_RESIDUAL
:evidence: QE_FATH_DUPONT_PRECURSOR
:stationarity: failed
:verdict: Геометрические и спектральные контроли выполнены; стационарные ВАХ не получены

Fath: после четырёх связанных карт на 481×13 сырой λ свежего образа 1,66525, rΣ=1,38112, узловой rK=1,01511. Все 13 колец прошли центральный спектральный порог, но среднее нормированного J(z) 131,20 и максимальное отклонение 23,38 А/см². Dupont: 21,0 и 12,5 кВ/см — отдельные точки другого прибора, а не Fath 54 мВ; в адаптивной связанной паре центральный спектр прошёл, кинетика и пространственный профиль остались вне допуска. Сравнение с литературной ВАХ незавершено.
```

```{qevidence} Промежуточный отчёт Fath/Dupont
:id: QE_FATH_DUPONT_PRECURSOR
:availability: public
:locator: interim-90min.md, разделы «Оператор тока» и «Эталон Dupont V843»

[Опубликованный отчёт](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath-dupont-20261120/interim-90min.md). Компактные локальные протоколы и результаты идентифицируются семейством `fath-dupont-next/work/`: `lead-convergence`, `lead-current-bound`, `lead-ward`, `lead-wannier`, `adaptive-panels`, `impurity` и `lead-discretization`. Они не являются публичными ссылками и отдельные полные поля не переносятся.
```

## Локальные компактные контрольные серии Fath/Dupont

Ниже использованы локальные отчёты `fath-dupont-next/work/` на срезе 23 ноября. Это идентификаторы доступных в данной рабочей среде файлов, не публичные URL; исходные поля и чекпоинты не переносятся. Эти тесты частично раскрывают агрегаты предыдущего опубликованного отчёта. Там, где измерена только замороженная карта, полная новая SCBA не подразумевается.

```{qexperiment} Сохранение частиц при трёх LO-переносах
:id: QX_FATH_LO_CONSERVE
:supports: QC_FATH_LO_CONSERVATION
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:varies: QPAM_LO_DISCRETIZATION
:targets: QM_LO
:observes: QO_RESIDUAL
:evidence: QE_FATH_LOCAL_LO
:lo_mode: enabled
:stationarity: not_measured
:verdict: Сохранение LO улучшено; общая кинетика зависит от выбора пары

На замороженном E5658×34 #48 точечный/объёмный/шляпочный перенос даёт относительный дисбаланс частиц LO −2,6431e−4 / −2,4401e−17 / −2,0303e−17 и общую взвешенную rK 0,02028926 / 0,02053516 / 0,02027039. На E4971×25 #96 соответствующие rK 0,0007538401 / 0,0007538417 / 0,0018019161. Сохранение числа частиц само по себе не квалифицирует перенос для полной карты.
```

```{qevidence} LO-пары на двух сохранённых входах
:id: QE_FATH_LOCAL_LO
:availability: local_compact
:locator: fath-dupont-next/work/lo/report.md, таблица «Два сохранённых входа»
```

```{qexperiment} Примесный угол и радиальное разрешение в двух полосах
:id: QX_FATH_IMPURITY_FROZEN
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:varies: QPAM_RADIAL, QPAM_IMPURITY_ANGLE
:observes: QO_RESIDUAL
:evidence: QE_FATH_LOCAL_IMPURITY
:lo_mode: enabled
:stationarity: not_measured
:verdict: Локальная мера существенно влияет на узкие резонансы

На исходном замороженном причинном операторе в полосах 6,8–7,0 и 25,6–27,0 мэВ изменение с 32 периодических углов на Gauss128 даёт изменение нормы Σ_imp< 0,137% и 3,406%. Замена долей колец положительным интегралом по u=(10k)² изменила сырой заряд в нижней полосе 6,56e8→8,83e8 см⁻², в верхней 1,31e8→6,00e9 см⁻². Интерполяция готового G воспроизводит лишь малую часть добавки. Изменение радиальной и угловой дискретизации — разные тесты, не полный обновлённый транспорт.
```

```{qparam} Угловая квадратура примесной свёртки
:id: QPAM_IMPURITY_ANGLE
```

```{qevidence} Примесная квадратура и локальные прямые тесты
:id: QE_FATH_LOCAL_IMPURITY
:availability: local_compact
:locator: fath-dupont-next/work/impurity/report.md, angular.json, radial.json; impurity-direct-481/report.md; impurity-direct-linked/report.md
```

```{qexperiment} Прямая и PV ретардированная примесная часть
:id: QX_FATH_IMPURITY_DIRECT
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:observes: QO_RESIDUAL, QO_JZ
:evidence: QE_FATH_LOCAL_IMPURITY
:lo_mode: enabled
:stationarity: not_measured
:verdict: Замороженные локальные результаты разнонаправлены; полной новой SCBA нет

В Q21 E121×7 C2 замена только эрмитовой части при тех же прямых L/G и Γ уменьшила локальный примесный источник на выбранных полосах в 57–1115 раз; на отдельном узловом контроле 2,9110→0,06334 А/см². В E481×13 на кольце k=0 и E=60 мэВ абсолютный остаток левой Σ< вырос 0,80949→0,93932 (+16,04%), заранее заданный двукратный порог не достигнут. Разные замороженные входы и наблюдаемые не устанавливают общий эффект на стационарный ток.
```

```{qexperiment} Fath: две нормировки одного оператора
:id: QX_FATH_NORMALIZATION_FROZEN
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:observes: QO_RESIDUAL, QO_JZ
:evidence: QE_FATH_LOCAL_NORMALIZATION
:lo_mode: enabled
:stationarity: not_measured
:verdict: Поправка меняет баланс швов, но не выравнивает J(z)

На фиксированных полях причинного #512 штатная/F(1−F) нормировка меняет добавленную сумму наружных потоков +0,40134097→+0,04005319 А/см² и размах J(z) 171,96557→171,97205 А/см². На B164 соответственно +0,36156588→+0,03615620 и 183,54712→183,55326. Столкновения заморожены; сравнение не является новой полной картой.
```

```{qevidence} Тест нормировки
:id: QE_FATH_LOCAL_NORMALIZATION
:availability: local_compact
:locator: fath-dupont-next/work/lead-normalization/result.md, таблица входов карты 512 и B164
```

```{qexperiment} Узловая и причинная полная карта с общим входом #512
:id: QX_FATH_CAUSAL_PAIR
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:observes: QO_RESIDUAL
:evidence: QE_FATH_CAUSAL_PAIR
:lo_mode: enabled
:stationarity: unverified
:verdict: Совместное изменение нормировки и входа столкновений ухудшило измеренные невязки

Общий запечатанный вход #512, 4801×25; пять каналов и обе полости пересчитаны. Узловой контроль против причинных шляпок: штатная rΣ 0,00390313→0,27610975, штатная rK 0,000689394→0,0655580. В причинном плече одновременно изменены нормировка и представление G для столкновений: отдельный эффект каждого из них этим сравнением не установлен.
```

```{qevidence} Полная пара #512
:id: QE_FATH_CAUSAL_PAIR
:availability: local_compact
:locator: fath-dupont-next/work/lead-map-analysis/result.md, nodal.json, causal_projected.json
```

```{qexperiment} Хвостовые и координатные представления тока
:id: QX_FATH_COORDINATE_CONTROLS
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:varies: QPAM_FATH_BASIS
:observes: QO_JZ
:evidence: QE_FATH_COORDINATE_CONTROLS
:lo_mode: enabled
:stationarity: not_measured
:verdict: Некоторые замороженные профили улучшены; общий компактный ранг не квалифицирован

На 11 замороженных срезах #512 и #128 блочное представление семи хвостовых мод воспроизвело плотные профили и оба шва до 2,26e−11 относительно. Два свежих локальных обновления пяти каналов при Q21 дали отличие не выше 7,61e−13 от полноразмерного хвостового расчёта. Для другой обученной лестницы координатных проекторов только полный ранг 144 выполнил 0,1% на всех отложенных профилях и швах. Два граничных гармонических направления уменьшили ошибку профиля #512 при E=6,8 мэВ с 47,25% до 1,01%, но их энергии выше заранее заданного предела. Эти результаты проверяют разные представления и не доказывают стационарность.
```

```{qevidence} Замороженные координатные и межпериодные срезы
:id: QE_FATH_COORDINATE_CONTROLS
:availability: local_compact
:locator: fath-dupont-next/work/blocks/report.md; coordinate-dimension/report.md; lead-coordinate/result.md; lead-harmonic/result.md
```

```{qexperiment} Положительные плотности и геометрия периодического тока
:id: QX_FATH_GEOMETRIC_CURRENT
:status: completed
:family: Fath/Dupont
:varies: QPAM_FATH_BASIS
:observes: QO_JZ
:evidence: QE_FATH_GEOMETRIC_CURRENT
:stationarity: not_measured
:verdict: Геометрическая представимость не заменяет динамическое решение

Для связанных хвостов Fath при тестовом токе 108,175 А/см² положительные плотности дают максимальное отклонение по 145 связям 0,01457/0,01464 А/см² в двух фазовых выборках при допуске 1,08175. Для Dupont Wannier11±4 при 1500 А/см² — 9,526/7,669 при 21 кВ/см и 9,360/8,807 при 12,5 кВ/см, допуск 15. Независимый сертификат для PzP7 показывает ограничение исходного оператора; эта конструкция не вычисляет физическую стационарную плотность.
```

```{qevidence} Сертификат и положительные плотности
:id: QE_FATH_GEOMETRIC_CURRENT
:availability: local_compact
:locator: fath-dupont-next/work/lead-current-bound/result.md; lead-periodic-current/result.md; witness.json
```

```{qexperiment} Адаптивные панели на независимом окне #512
:id: QX_FATH_ADAPTIVE_PANEL
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:varies: QPAM_RADIAL
:observes: QO_CURRENT, QO_RESIDUAL
:evidence: QE_FATH_ADAPTIVE_PANEL
:lo_mode: enabled
:stationarity: not_measured
:verdict: Условная квадратура точна в проверенном окне; после обновления пик может сместиться

На #512 окно 9,0–11,8 мэВ и 0,075–0,100 нм⁻¹: обе фазы интегрирования u при фиксированном E дают расхождение заряда 0,00176/0,00177% относительно центра двух сгущённых оценок; середины 128×32 — 0,25043%, тензорный Гаусс — 0,50440%. Это вклад отдельного окна, а не полный J(z). После полной карты общая сетка пропустила перемещение узкого пика; две оценки сами по себе не являются строгой границей ошибки.
```

```{qevidence} Перенос адаптивной квадратуры
:id: QE_FATH_ADAPTIVE_PANEL
:availability: local_compact
:locator: fath-dupont-next/work/adaptive-panels/report.md, таблица «Независимое окно на №512»; drift.json
```

```{qexperiment} Аналитические радиальные моменты замороженного связанного оператора
:id: QX_FATH_RADIAL_PENCILS
:status: completed
:family: Fath/Dupont
:varies: QPAM_RADIAL
:observes: QO_CURRENT
:evidence: QE_FATH_RADIAL_PENCILS
:stationarity: not_measured
:verdict: Проверена квадратура фиксированной аффинной реконструкции

На фиксированном E и аффинных Σ ошибки матричных моментов к прямой квадратуре: Fath Q21 p0/p4 4,00e−13/1,02e−13; V843 Q28 при 21/12,5 кВ/см 6,44e−14/8,15e−14. Это не измерение ошибки модели радиальной физики или стационарной карты; RMS кинетического остатка нельзя заменить линейными моментами G.
```

```{qevidence} Радиальные пучки
:id: QE_FATH_RADIAL_PENCILS
:availability: local_compact
:locator: fath-dupont-next/work/lead-radial-pencils/result.md, p0-radial-pencils.json, p4-radial-pencils.json, transfer-v843.md
```

```{qexperiment} Fath и V843: статические функции Ванье
:id: QX_FATH_V843_WANNIER
:status: completed
:family: Fath/Dupont
:varies: QPAM_FATH_BASIS
:observes: QO_RESIDUAL
:evidence: QE_FATH_V843_WANNIER
:stationarity: not_measured
:verdict: Полевая конструкция V843 прошла заявленные одночастичные тесты; Fath rank11 нет

У Fath rank11/±4 при 54 мВ максимальная ошибка смещённого уровня 0,734 мэВ и потеря нормы 0,183; две полевые поправки также не проходят. У V843 rank11/±4 при 21 кВ/см исходная/первый порядок/конечный поворот дают ошибки 0,37195/0,15984/0,17146 мэВ; при 12,5 кВ/см 0,007333/0,009942/0,007308 мэВ. Две полевые конструкции V843 прошли объявленные статические условия; это ещё не ВАХ.
```

```{qevidence} Статический тест Ванье
:id: QE_FATH_V843_WANNIER
:availability: local_compact
:locator: fath-dupont-next/work/lead-wannier/result.md, fath-field.json, dupont-field.json, dupont-coupled.json
```

Остальные локальные технические серии имеют собственные точные места: `lead-ward/result.md` (локальный баланс пяти каналов, включая прямую упругую R), `lead-convergence/result.md` (секущие и смешивание), `lead-phase-cost/result.md` (стоимость физической энергетической меры), `lead-observed-solve/result.md` (частичные обращения и полный контроль), `lead-causal-evaluation/result.md` (дальние шляпки PV), `solver/report.md` (хвосты исходных #512/#768), `ab-fixed/report.md` и `ab-autonomous/report.md` (две версии квадратуры). Они являются отдельными техническими или замороженными контролями, не подтверждениями стационарности.

| Дополнительная локальная серия и точное место | Условие и исход | Граница |
| --- | --- | --- |
| `ab-fixed/report.md`, `ab-autonomous/report.md`, `verifier/result.md` | Общий #128 для разработки; закрытый E9135 #4 после фиксации. База 32×16: ошибка заряда 7,3331%; фиксированный финал 0,14575%, но провал защиты rK; автономный финал 0,03709%, защиты пройдены. | Менялись свобода планирования и правило узлов совместно; один отложенный вход, локальная полоса. |
| `lead-convergence/result.md`, таблица первых остатков | На Q21 481×13 при α=0,2 остатки пяти каналов 0,09154494→0,06813197; косинус 0,97178, линейный минимум секущей α=0,5153. | Локальная линейная модель не гарантирует итог полного нелинейного продолжения. |
| `lead-ward/result.md`, таблица p0/p4 | Локальный источник примесей Q21 с PV 27,424/23,595 А/см², с прямой упругой R 0,0554/0,0573; вклад LO и IFR остаётся. | Один исходный G, без обновления полостей. |
| `lead-phase-cost/result.md`, таблица колец | GL9/13/18 на тех же панелях Fath k=0 сократил узлы 19530→13546 при max ΔJ(z)=3,70e−10 А/см²; грубое разбиение ранее отклонено. | Замороженное поле и выбранные кольца; не проверка полной SCBA. |
| `lead-observed-solve/result.md` | На 1198 Fath и 1107 V843 точках выбранные строки согласованы с полной инверсией до 6,88e−11 и 1,68e−11 соответственно. | Точность выбранных точек и стоимость одного окружения. |
| `lead-causal-evaluation/result.md` | Дальний PV-ряд согласован с 256-битным расчётом до 5,16e−17 на 576 примерах; слабый шов V843 требует дополнительного контроля. | Оценивает построение источника, не полный интеграл. |
| `solver/report.md` | Доли внешнего окна в квадрате взвешенной невязки левой Σ< 95,61% на причинной #512 и 95,88% на исходной #768. | Разные истории; это диагностика уже сохранённых состояний. |

```{qclaim} Ранний ток Fath при 54 мВ не имеет принятой стационарной оценки
:id: QC_FATH_EARLY_UNACCEPTED
:status: open
:family: Fath
:at: QP_FATH_54_EARLY
:evidence: QE_FATH_18, QE_FATH_19, QE_FATH_20
:stationarity: failed

Для описанных историй и допусков ни сближение граничных потоков, ни отдельное прохождение контурного спектра не закрывает невязки и пространственную непрерывность. Это ограничение вычисленных состояний, а не оценка погрешности относительно MEDIUM.
```

```{qclaim} Точная локальная LO-консервация не гарантирует общую сходимость
:id: QC_FATH_LO_CONSERVATION
:status: open
:family: Fath
:at: QP_FATH_54_EARLY
:evidence: QE_FATH_LOCAL_LO
:stationarity: not_measured

На двух сохранённых входах парные переносы подавляют интегральный источник частиц LO, но шляпочная пара на E4971×25 увеличивает общую rK. Это утверждение ограничено замороженными полями и не предсказывает результат полной карты.
```

## Дополнительные отдельные серии 18 ноября

```{qexperiment} Одночастичные зоны и скан 60 представлений
:id: QX_FATH_BANDS_18
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:varies: QPAM_FATH_BASIS
:evidence: QE_FATH_BANDS_18
:stationarity: not_measured
:verdict: Ни одна из 60 комбинаций при Nz144 не выдержала проектный спектральный допуск

Без столкновений и Хартри исследованы CBO 149 и 120 мэВ отдельно. При CBO149 ошибка первых четырёх минизон от пространственной сетки достигает 0,611 мэВ, а от проекции PzP7 — 18,762 мэВ. Граница применимости — одночастичный спектр, не стационарный ток. Паспорт задаёт положение легирования и различает геометрические сегменты и реальные IFR-интерфейсы.
```

```{qevidence} Паспорт и скан зон
:id: QE_FATH_BANDS_18
:availability: public
:locator: bands/report.md, basis_scan.csv, passport.toml

[Отчёт зон](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath-20261118/bands/report.md) · [Результаты скана](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath-20261118/bands/basis_scan.csv).
```

```{qexperiment} Компактный базис: статическое обучение и уточнение ранга
:id: QX_FATH_COMPACT_REFINEMENT
:status: completed
:family: Fath
:varies: QPAM_FATH_BASIS
:evidence: QE_FATH_COMPACT_REFINEMENT
:stationarity: not_measured
:verdict: Низкоэнергетические и полные спектральные критерии расходятся

Ограниченный POD7 выбран по статике без подгонки тока; обучен на 24 фазах при нулевом поле. Для десяти объявленных базисов rank9–12 восемь проходят 0,5 мэВ и пять 0,10 мэВ на Nz144/192; все кандидаты нарушили полную матричную сумму на коротких энергетических сетках. POD9 прошёл голую сумму в широком окне, но его верхнее Ritz-направление далеко от точных FD-состояний. Отложенная проверка использовала 131 новую фазу и семипериодное окно при 54 мВ.
```

```{qevidence} Компактный базис и уточняющая таблица
:id: QE_FATH_COMPACT_REFINEMENT
:availability: public
:locator: cell-basis/README.md; cell-basis-refinement/README.md, summary.csv, passport.toml

[Первый базис](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath-20261118/cell-basis/README.md) · [Уточнение](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath-20261118/cell-basis-refinement/README.md).
```

```{qexperiment} Парные ранние транспортные контроли базиса и окна
:id: QX_FATH_TRANSPORT_PAIRS_18
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:varies: QPAM_FATH_BASIS
:observes: QO_JZ, QO_CURRENT, QO_RESIDUAL
:evidence: QE_FATH_TRANSPORT_PAIRS_18
:lo_mode: enabled
:stationarity: failed
:verdict: Парные результаты разнонаправлены; строгого принятия нет

После 64 карт компактные PzP7/Bloch7 дают rK 0,059270/0,082709, граничный небаланс 11,691%/2,541%, внутренний J(z) 1,119…201,272/−109,965…296,474 А/см². В отдельной паре одинаковых 64 холодных карт расширяли только верхний энергетический край 560→860 мэВ, а не базис; J₊ изменился на 0,059%. Малая разность в одной паре не доказывает сходимость по окну.
```

```{qevidence} Сводки ранних пар транспорта
:id: QE_FATH_TRANSPORT_PAIRS_18
:availability: public
:locator: transport/report.md, разделы парного базиса и верхнего края; compact-basis-comparison.json; compact-window-comparison.json

[Парные данные](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath-20261118/transport/report.md).
```

```{qexperiment} Однократный Пуассон на сохранённых плотностях
:id: QX_FATH_POISSON_ONCE
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:evidence: QE_FATH_POISSON_ONCE
:stationarity: not_measured
:verdict: Электростатический отклик измерен без обратной связи

На шести незавершённых плотностях, полученных при Uᴴ=0, размах Uᴴ=1,82–2,09 мэВ. Для native карты 128 — 2,09319 мэВ. Обратной подстановки в Dyson или SCBA не было и новый ток не измерялся.
```

```{qevidence} Сохранённые профили отклика Пуассона
:id: QE_FATH_POISSON_ONCE
:availability: public
:locator: poisson-response/README.md, таблица «Профили»

[Однократный отклик](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath-20261118/poisson-response/README.md).
```

```{qexperiment} Спектральная постобработка двух сохранённых состояний
:id: QX_FATH_SPECTRAL_18
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:observes: QO_RESIDUAL
:evidence: QE_FATH_SPECTRAL_18
:lo_mode: enabled
:stationarity: not_measured
:criteria: Спектральная сумма ниже 0,001
:verdict: Точный интеграл выбранного интерполянта остаётся вне допуска

Для native54-03 карты 128 и checkpoint256 при k=0,375 нм⁻¹ точный интеграл интерполированного Dyson даёт дефект 0,00562/0,00561. Независимая 24-точечная квадратура согласована до 6,6e−12 по норме суммы. Постобработка фиксированной Σ не является полной SCBA на более тонкой сетке.
```

```{qevidence} Анализ спектра и крайних весов
:id: QE_FATH_SPECTRAL_18
:availability: public
:locator: spectral54/README.md, diagnostics.json; balance/report.md, edge_weights.csv

[Спектральный разбор](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath-20261118/spectral54/README.md) · [Заряд и энергетические границы](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath-20261118/balance/report.md).
```

```{qexperiment} Ускорители и кинетические предикторы компактной точки
:id: QX_FATH_ITERATORS_18
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:observes: QO_RESIDUAL
:evidence: QE_FATH_ITERATORS_18
:lo_mode: enabled
:stationarity: failed
:verdict: Ни один из перечисленных вариантов не прошёл совместный критерий переноса

На общем пилотном входе к карте 7 Anderson d2 увеличил rΣ и rK в 2,62 и 4,22 раза к линейному контролю. Скалярный Aitken снизил поздние медианы, но при одинаковом бюджете его конечные rΣ/rK выше линейного в 1,426/1,521 раза. Замороженный нейтральный lesser-дефект имел усиление 1,00895: это не спектр полной SCBA. Pauli-проекция GMRES вернула допустимость заполнений, но полный свежий остаток вырос на 24,6%, дефект числа — с 2,26e−5 до 1,78e−2. Разные опыты имеют отдельные входы и бюджеты.
```

```{qevidence} Исходные протоколы методов
:id: QE_FATH_ITERATORS_18
:availability: public
:locator: method/report.md; method/adaptive-scalar/report.md; method/frozen-kinetic/report.md; method/pauli-predictor/report.md

[Anderson и смешивание](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath-20261118/method/report.md) · [Aitken](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath-20261118/method/adaptive-scalar/report.md) · [Замороженная кинетика](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath-20261118/method/frozen-kinetic/report.md) · [Pauli](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/experiments/fath-20261118/method/pauli-predictor/report.md).
```

## Вложенные локальные проверки дискретизации и тока

```{qexperiment} Разрешение входного примесного кольца Fath E959×25
:id: QX_FATH_INCOMING_ANNULUS
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:varies: QPAM_RADIAL
:observes: QO_RESIDUAL
:evidence: QE_FATH_DISCRETIZATION_LOCAL
:stationarity: not_measured
:verdict: Точечные изменения неодинаковы по энергии; обновлённой SCBA нет

Для E=−24,023115 мэВ, k выхода 0,125 нм⁻¹ и входной ячейки 0,1125…0,1375 нм⁻¹ узловая ширина старой моды 5,65860 мэВ, разрешённая полная ковариация порядка 12 даёт 0,254745 мэВ. В соседней точке −25,213177 мэВ ширина меняется в противоположную сторону 0,009591→0,241358 мэВ. На окне −26…−23 мэВ два порядка E дают локальную rK узловая/разрешённая 94,0376/8,37998 и 94,0659/8,38153. Пересчитывался только вход выбранной ячейки при замороженном старом операторе; это не глобальная rK и не полный ток. Парный двухсторонний протокол и отдельный JSON на −24,023115 существуют, но его глобального исхода здесь не устанавливаем.
```

```{qexperiment} Кинетическая температура сохранённых образов Fath и V843
:id: QX_FATH_V843_KINETIC_TEMPERATURE
:status: completed
:family: Fath/Dupont
:evidence: QE_FATH_DISCRETIZATION_LOCAL
:stationarity: failed
:verdict: Моментные температуры относятся к несошедшимся образам и различным сеткам

Fath 54 мВ: E481×13, E481×25, E959×25 дают 44,0862, 78,5582 и 77,7797 K. V843 при 21 кВ/см с фиксированным H и с Хартри — 72,1879 и 72,1057 K; при 12,5 кВ/см с фиксированным H — 82,2087 K. Каждое значение вычислено на собственной энерго-проекционной мере свежего нестационарного образа, а не измерено как температура решётки или сравнимая равновесная температура.
```

```{qevidence} Файлы дискретизации и моментных температур
:id: QE_FATH_DISCRETIZATION_LOCAL
:availability: local_compact
:locator: fath-dupont-next/work/lead-discretization/incoming-annulus.md; incoming-annulus*.json; fath-incoming-window-order6.json; fath-incoming-window-order10.json; paired-impurity.md; paired-impurity-E24p023.json; temperature-*.json; spatial-mesh.json
```

```{qexperiment} Сырые профили причинной и штатной линий
:id: QX_FATH_RAW_CURRENT_512_768
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:observes: QO_JZ, QO_CURRENT
:evidence: QE_FATH_CURRENT_LOCAL
:lo_mode: enabled
:stationarity: failed
:verdict: Почти сбалансированные сырые швы сосуществуют с большим внутренним размахом

Для свежих сырых образов причинного #512 и штатного #768, 4801×25, наружные швы соответственно −108,174773/+108,174727 и −105,998115/+105,998052 А/см²; 143 внутренних связи дают 0,980042…172,883077 и 0,955859…169,168981 А/см². Образы имеют разные истории; сравнение само по себе не является парным изменением одного фактора.
```

```{qexperiment} Связанный Q21: профили и локальный баланс
:id: QX_FATH_Q21_CURRENT
:status: completed
:family: Fath
:at: QP_FATH_54_EARLY
:observes: QO_JZ, QO_CURRENT
:evidence: QE_FATH_CURRENT_LOCAL
:lo_mode: enabled
:stationarity: failed
:verdict: Независимый пересчёт воспроизводит профиль; пространственный допуск остаётся открытым

Два грубых обновления Q21 сверены плотным решением на 145 связях, включая оба шва, до 1,02e−8 А/см². На собственных сетках p0/p4 среднее J(z) 301,938/711,573 А/см², максимальное отклонение 276,690/818,325. Отдельные свежие связанные шаги 6/7/8 при α=0,5 дают средние 97,48159/88,78883/83,21303 и худшие подписанные отклонения +11,21318/−10,75221/−12,09800 А/см². Рост отклонения 7→8 главным образом связан с потерей вклада 16…22 мэВ при k=0,15; кинетический остаток локализован в другом окне. Другой замороженный контроль Q21/W против полного координатного H на резонансе C2 даёт различие профиля 15,2%; это не новая самосогласованная координатная история.
```

```{qevidence} Независимые профили и балансы
:id: QE_FATH_CURRENT_LOCAL
:availability: local_compact
:locator: fath-dupont-next/work/current/continuity-report.md; q21-continuity-report.md; linked-collision-report.md; linked-step678-current-report.md; соответствующие JSON и linked-step678-hats-profiles.csv
```

## Сохранённые срезы и локальные операторы

```{qevidence} Промежуточные точки длинной native54
:id: QE_FATH_NATIVE54_SNAPSHOTS
:availability: public_compact
:locator: checkpoint-0128, checkpoint-0256, checkpoint-0512; summary.toml last_row
:limits: QC_FATH_EARLY_UNACCEPTED

Все три точки принадлежат одной траектории `native54-long-alpha02`, одной модели и 54 мВ. В новом дереве этих сводок нет; исходные адреса сохранены ниже.

| Свежих карт | rK | rΣ | Исходная сводка |
| ---: | ---: | ---: | --- |
| 128 | 0,0074231 | 0,0451239 | [Checkpoint 128](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/38c86c218ebaa1f546bdfe8ad4497552099ea3d3/experiments/fath-20261118/transport/native54-long-alpha02/checkpoint-0128/summary.toml#L1-L28) |
| 256 | 0,0052050 | 0,0278393 | [Checkpoint 256](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/38c86c218ebaa1f546bdfe8ad4497552099ea3d3/experiments/fath-20261118/transport/native54-long-alpha02/checkpoint-0256/summary.toml#L1-L28) |
| 512 | 0,0039148 | 0,0220877 | [Checkpoint 512](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/38c86c218ebaa1f546bdfe8ad4497552099ea3d3/experiments/fath-20261118/transport/native54-long-alpha02/checkpoint-0512/summary.toml#L1-L28) |

Принятие всех трёх ложно по исходным summary. Эти срезы дополняют опубликованный поздний профиль и историю.
```

```{qexperiment} Парная примесная свёртка на одной энергии
:id: QX_FATH_PAIRED_IMPURITY_POINT
:family: Fath
:at: QP_FATH_54_EARLY
:varies: QPAM_RADIAL
:status: completed
:stationarity: not_measured
:stage: frozen_single_energy
:evidence: QE_FATH_LOCAL_POINT_CONTROLS

Три положительные меры на −24,023115 мэВ имеют 25, 78 и 112 узлов. Абсолютный дефект следа заряда в координатном представлении составляет соответственно 1,58×10⁻¹⁷, 1,26×10⁻²¹ и 1,78×10⁻²¹. Кумулятивный Ward-профиль имеет нормы 2,31×10⁻¹⁷, 1,67×10⁻²⁰ и 2,13×10⁻²⁰. Сравнение ограничено одним энергетическим срезом; протокол отдельно требует интегралов на основном и отложенном окнах.
```

```{qexperiment} Координатная сетка с узлами на интерфейсах
:id: QX_FATH_DUPONT_SPATIAL_MESH
:status: completed
:stationarity: not_measured
:stage: coherent_levels
:evidence: QE_FATH_LOCAL_POINT_CONTROLS

Для каждого устройства сохранены 24 условия: две фазы Блоха, два k, три номинальных размера и два размещения узлов. На 576 номинальных узлах максимальная абсолютная ошибка уровней Fath меняется с 0,21847 до 0,02129 мэВ при согласовании интерфейсов, Dupont — с 0,42686 до 0,02759 мэВ. Исходные поля `reference_meV`, `levels_meV` и `charge_continuity_defect` позволяют воспроизвести сравнение по каждому условию. Проверка относится к когерентному спектру.
```

```{qevidence} Локальные срезы примесной пары и пространственной сетки
:id: QE_FATH_LOCAL_POINT_CONTROLS
:availability: local_compact
:locator: fath-dupont-next/work/lead-discretization/paired-impurity-E24p023.json rules; spatial-mesh.json fath.checks и dupont.checks

Точечная примесная проверка и когерентная проверка интерфейсов имеют отдельные входы. Протокол парной свёртки описан в `paired-impurity.md` той же серии.
```
