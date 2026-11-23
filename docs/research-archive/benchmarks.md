# Сравнения, базис и спектральные контроли

Этот раздел индексирует компактные локальные материалы 18–19 ноября 2026 года. Координаты начинаются от корня исходного рабочего пространства; каталоги `.build` локальны и сами по себе не являются постоянными публичными ссылками. Числа ниже относятся к указанным постановкам, а завершение ограниченной операции не означает сходимости SCBA. Первоисточники публикаций доступны по приведённым ссылкам. Историческая структура Bosco и её 200 K эталон описаны в {need}`QS_BOSCO_2019` и {need}`QL_BOSCO_2019`.

```{qexperiment} Bosco: диагностика смежной пары и границы
:id: QX_BENCH_BOSCO_TRAJECTORY
:family: Bosco
:at: QP_133_1MV_70K
:status: completed
:observes: QO_CURRENT, QO_RESIDUAL
:stage: fixed U, G32→G33
:stationarity: unverified
:evidence: QE_BENCH_BOSCO
:verdict: unresolved

Core e171, 70 K, 1 мВ/период, U=0, пять локальных механизмов без e–e. Цель — различить свежую невязку и последовательное изменение, а также вклад локальных каналов и независимо смешанной границы. ΔG< составляет 2,866·10⁻⁴ в невзвешенной F-норме, но симметричное изменение граничного J равно 2,357·10⁻³, среднего внутренних связей — 1,802·10⁻². Точные коммерческие нормы неизвестны; это не межкодовое доказательство причины несходимости.
```

```{qevidence} Компактные разложения Bosco и повтор траектории
:id: QE_BENCH_BOSCO
:family: Bosco
:availability: local_compact
:locator: .build/negf-comparison-20261118/report.md; numerical.md; numerical-review.md; trajectory/attempt01/diagnostics.toml; embedding/attempt01/decomposition.toml; embedding-channel/attempt01/corner-summary.toml
:supports: QC_BENCH_BOSCO_LIMIT

На G32 разложение границы B(s_f)−B_m = [B(s_f)−B(s_m)]+[B(s_m)−B_m] даёт отношение норм около 18672; обновление локального триплета распространяется через cavity. Два порядка смены каналов распределяют подписанную проекцию 55,46% примесям и 44,54% остальным в штатной норме. Отдельная проекция примесного вклада на кинетический дефект при замороженном GR равна 97,97%; это не доля примесей в токе. Проверка секущей не принята: обе попытки не прошли соответствующую сверку, итоговые коэффициенты исключены. Сохранены `secant/attempt01/status.txt`, `secant/run02.log` и `secant/verified-norms.json`.
```

```{qclaim} Диагностики Bosco не принимают стационарный ток
:id: QC_BENCH_BOSCO_LIMIT
:family: Bosco

Повтор и поканальные проекции относятся к одной сохранённой траектории; они не устанавливают полную производную SCBA, межкодовую эквивалентность или экспериментальную валидацию.
```

```{qexperiment} Fath: ковариантность фиксированного подпространства
:id: QX_BENCH_COVARIANCE
:family: Fath
:at: QP_FATH_54_EARLY
:observes: QO_CURRENT, QO_RESIDUAL
:stage: frozen self-energy and one fresh map
:stationarity: unverified
:evidence: QE_BENCH_COVARIANCE
:verdict: covariance_passed_stationarity_failed

CBO149, 10 K, 54 мВ/период, фиксированный потенциал; Nz32/Nb3/NE17/Nk2. Одна комплексная унитарная матрица поворачивает тот же проектор и все связанные операторы. Успешны 66 сравнений при фиксированной Σ и 83 после одной свежей карты при пороге 5·10⁻¹¹; максимум для J(z) 4,59·10⁻¹⁴ и 4,19·10⁻¹³. Большие невязки и спектральный дефект сохраняются: ковариантность не проверяет достаточность базиса или стационарность.
```

```{qevidence} Исходные и независимые таблицы поворота
:id: QE_BENCH_COVARIANCE
:family: Fath
:availability: local_compact
:locator: .build/session-20261119/basis_covariance/report.md; errors.csv; fresh/errors.csv; fresh/matrix_witness.toml; checksums.sha256; ../science_review/covariance_review.json

Независимое сопоставление 27 сохранённых матриц при E=62,5 мэВ и k=0 дало максимум 8,41·10⁻¹⁵. Диагональные населённости зависят от представления; физические матричные и пространственные величины сравниваются с согласованным поворотом. Вход искусственного резервуара не является принятым транспортным состоянием.
```

```{qexperiment} Fath: отбор мод, ранг и проекция
:id: QX_BENCH_RANK
:family: Fath
:at: QP_FATH_54_EARLY
:varies: QPAM_RANK
:stage: coherent BDD and fixed self-energy controls
:stationarity: not_measured
:evidence: QE_BENCH_RANK
:verdict: low_energy_and_spectral_gates_distinct

На общих Nz=96/144/192 сетках сравнивали отбор и ранг отдельно; когерентные FD и Ritz сравнения не включают SCBA или Poisson. Из 114 вариантов POD восьми Bloch-зон рангов 10 и 12 прошли низкоэнергетические ворота на всех сетках, но нарушили спектральный допуск прежнего окна. Поворот внутри фиксированного пространства и обрезка хвостов — разные операции. Малый NEGF-контроль с фиксированной модельной Σ отдельно сравнивает PzP, :none и real_space; он не является сходимостью рабочего прибора.
```

```{qevidence} Данные ранга и независимая проверка
:id: QE_BENCH_RANK
:family: Fath
:availability: local_compact
:locator: .build/session-20261119/basis_rank/report.md; summary.csv; results.json; small-negf/*/result.toml; REPRODUCE.md; ../science_review/rank_review.json; ../science_review/small_rank_review.toml

При Nz144 POD8/10 даёт максимальную ошибку четырёх нижних Bloch-уровней 0,060225 мэВ, но нормированный спектральный дефицит 0,26555 в окне [−400,560] мэВ. Независимый контроль для одного пробного пространства показывает, что прохождение Ritz-порога совместимо с потерей спектрального веса полной FD-задачи в конечном окне.
```

```{qparam} Шаг энергетической сетки и квадратура
:id: QPAM_BENCH_ENERGY

Шаг энергии и соответствующая квадратура; отдельно фиксируются окно, перенос исходной Σ, сетка k и число свежих карт.
```

```{qexperiment} Fath: замороженный спектр и пара энергетических сеток
:id: QX_BENCH_SPECTRAL
:family: Fath
:at: QP_FATH_54_EARLY
:varies: QPAM_BENCH_ENERGY
:observes: QO_RESIDUAL, QO_CHARGE, QO_CURRENT
:stage: frozen Sigma and one fresh map per arm
:stationarity: failed
:evidence: QE_BENCH_SPECTRAL
:verdict: diagnostic_not_converged

Terminal910: фиксированная Σᴿ, 25 значений k и конечное окно [−400,560] мэВ. Точный интеграл линейного интерполянта дал r_sum≤10⁻³ только для одного среза; 18 срезов улучшились и семь ухудшились относительно трапеции. Отдельная пара Nk5 на шагах 0,10/0,05 мэВ использовала перенесённый seed и по одной свежей карте без смешивания и Poisson. Сырой заряд seed/цель = 1,7172/1,7154; rΣ = 1,0929/1,0738 и rK = 19,915/19,804. Различия квадратуры и образов измерены, но стационарность не достигнута, а перенос на Nk25 не установлен.
```

```{qevidence} Спектральные матрицы, пары и PV-аудит
:id: QE_BENCH_SPECTRAL
:family: Fath
:availability: local_compact_partial_fields
:locator: .build/session-20261119/spectral_convergence/spectral-convergence.md; frozen_signed_by_k.csv; frozen_verification.json; pair_verification.json; arm-9601/map_residual.toml; arm-19201/map_residual.toml; pv_diagnostics.json; ../science_review/pair_review.toml

Независимая квадратура согласована со всеми 25 интегральными матрицами до 6,48·10⁻¹⁵ в норме ||ΔW||F/√7. Независимый LO PV на трёх срезах воспроизвёл сохранённую эрмитову часть с относительной ошибкой около 2,2·10⁻¹⁵; физические хвосты вне окна и причинность полной Σ не определены. Полные поля образа мелкой сетки для независимого восстановления не сохранены.
```

## Ориентиры опубликованных сравнений

```{qexperiment} Отбор внешнего benchmark без новых запусков
:id: QX_BENCH_SELECTION
:family: benchmark_selection
:stage: literature and published data
:stationarity: not_measured
:evidence: QE_BENCH_SELECTION
:verdict: candidate_selection_only

Fath MEDIUM — модельный ориентир nextnano около 514 А/см² при 10 K и 54 мВ/период, точный вход недоступен, а текст и рисунки tutorial указывают CBO 120 и 149 мэВ соответственно. Han D2 — отдельная измеренная точка 10 K, 4,7903 кВ/см и 298,792 А/см² после авторской контактной поправки. Li при 77 K: модельные максимумы 500 А/см² dark без e–e, 1240 с GW без поля и 1100 с генерацией без e–e; это разные модели, а не общая кривая. Планы новых расчётов здесь не выполнены.
```

```{qevidence} Паспорта и опубликованные данные кандидатов
:id: QE_BENCH_SELECTION
:family: benchmark_selection
:availability: local_compact_and_public_sources
:locator: .build/negf-benchmark-selection-20261118/report.md; implementation.md; han-figure.md; mit.md; open-solvers.md; sources.md; evidence/provenance.json

Источники: [Fathololoumi 2012](https://doi.org/10.1364/OE.20.003866), [Han 2016](https://doi.org/10.1364/OE.24.028583), [числовые данные Han](https://doi.org/10.5518/107), [Li 2014](https://doi.org/10.1049/el.2013.4035), [Winge и соавт., Table I и Fig. 1–2](https://arxiv.org/pdf/1607.02374). Han Figure-04-data01, строка 24 без заголовка: 15,7534 кВ/см и 1254,768 А/см² — модель со стимулированным излучением, не измеренный тёмный ток. Единицы CSV идентифицированы по шкале и форме, не по метаданным столбцов. Полный открытый комплект solver, точного input и авторского output для кандидатов не установлен.
```

## Учёт остальных компактных материалов

| Группа и точное место | Статус и границы |
|---|---|
| `.build/negf-comparison-20261118/bands/report.md`, `energies.csv`, `basis_bloch_check.json`, `audit_transfer.json` | Измерены четыре последовательных приближения одночастичного оператора Bosco при нулевых F, U и Σ. Сдвиг от профиля к проекции не является оценкой ошибки рабочего тока. |
| `.build/negf-comparison-20261118/bosco2019/figure-summary.json`, `measured-curve-samples.csv`, `model-curve.csv`, `digit-review.md`, `verify_bosco_digitization.py` | Оцифровка опубликованной Fig. 3b 200 K и независимая сверка; модельная и измеренная кривые разные, публикационные сырые NEGF-данные не получены. [Статья](https://doi.org/10.1063/1.5110305). |
| `.build/negf-comparison-20261118/nextnano.md`, `nextnano-evidence/` | Архив официальных описаний, входов и журнала: Minimal 300 K/58 мВ не запускался, журнал Adams PARTIAL и завершился исключением; точные параметры MEDIUM и коммерческая норма GF неизвестны. |
| `.build/negf-comparison-20261118/impurity/impurity_check.json`, `trajectory/impurity-direction/results.json`, `embedding/profile-verification.json`, `audit_rows.json` | Проверены отдельные свёртки, одно направление и восстановление профиля на сохранённых состояниях; это не полный Jacobian и не приёмка стационарности. |
| `.build/negf-comparison-20261118/experiment.md`, `models.md`, `external-data/`, `figures/` | Сопоставление публикаций, операторов, открытых данных Han и иллюстрации. Формулы и геометрии разных устройств сохраняют собственные условия, числовые архивы не заменены. |
| `.build/negf-benchmark-selection-20261118/mit.md`, `evidence/` | Проверены публикации и доступность MIT, Adams, открытых схем и решателей. Полный воспроизводимый transport-комплект не установлен, новые solver-запуски не выполнялись. |
| `.build/session-20261119/science_review/review.md`, `baseline_review.toml`, `frozen_review.toml`, `pair_review.toml`, `rank_review.json`, `covariance_review.json` | Независимые проверки baseline, спектра, ранга, ковариантности и пары. Различаются повтор сохранённых данных, ограничения конечного окна и отсутствие полного fine-grid output. |
| `.build/session-20261119/evidence_index/source-verification.md` | Учёт доступности и прав источников: на этой стадии в основном проверены аннотации и метаданные; последующий `science_review/review.md` отдельно описывает более глубокую сверку отдельных уравнений. Доступная авторская версия не означает права на перераспространение. |

Архив включает и технические неудачи: `basis_covariance/prior-attempt/` остановлен до результата из-за ссылки на модуль; `spectral_convergence/attempt-9601-charge-diagnostic-pre-map/` остановлен до свежей карты; у Bosco направленного прохода `trajectory/impurity-direction/failed-virtual-address-limit.json` фиксирует неудачное выделение памяти. Они не учитываются как научные отрицательные результаты.
