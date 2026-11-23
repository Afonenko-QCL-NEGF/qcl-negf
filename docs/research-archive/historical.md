# Ранние равновесные и native-исследования

Срез источника — `qcl-negf-research` main `76926d0035eeddf7c59a8c4357ab98f4e3bc9eba`. [Исходный набор campaign133](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133) сохраняет входы, программы, малые результаты и обзор ограничений. Завершение программы не означает сходимость. HDF5, полные identity и часть логов остались на VM; их hash не доказывает доступность или повторную проверку. Исходный [исторический перенос](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/08e90bc605f0662f1b5559f4c0f0c5a5655ed691/studies/historical/README.md) прямо называет свою выборку ограниченной.

```{qsource} Статья Bosco и соавт., 2019
:id: QL_BOSCO_2019
:family: Bosco
:role: literature
:locator: DOI 10.1063/1.5110305, рис. 3b

[Паспорт исходника](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/literature/reference-2019/source.yaml); [статья](https://doi.org/10.1063/1.5110305). Оцифрована сплошная чёрная NEGF-кривая рис. 3b при 200 K, в интервале 40–60 мВ/период; неопределённость паспорта касается оцифровки, не модели.
```

```{qstructure} Двухъямная структура reference-2019
:id: QS_BOSCO_2019
:family: Bosco
:source: QL_BOSCO_2019
:locator: literature/reference-2019/structure.csv

[Паспорт и геометрия](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/literature/reference-2019). Структура и легирование взяты из публикации; число периодов устройства прямо не опубликовано. Сравнение проводят по напряжению на период, не по терминальному напряжению.
```

```{qpoint} Равновесный кандидат S01 при 70 K
:id: QP_S01_70K
:family: equilibrium
:structure: QS_BOSCO_2019
:bias_kind: per_period
:bias_value: 0
:bias_unit: mV
:temperature: 70 K
:sign: zero
:optical: unknown

[Вход](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/5458212063a41051328ef8b5d14d63d5ac7dc781/config/studies/equilibrium-0-70.yaml), [описание](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/5458212063a41051328ef8b5d14d63d5ac7dc781/docs/equilibrium-s01.md). Конфигурация не доказывает равновесия. Эта точка отличается от 200 K публикационной кривой.
```

```{qpoint} Reference-2019-derived, 1 мВ на период, 70 K
:id: QP_133_1MV_70K
:structure: QS_BOSCO_2019
:bias_kind: per_period
:bias_value: 1
:bias_unit: mV
:temperature: 70 K
:sign: Положительное смещение на период в сохранённом входе
:optical: unknown

Для postboot и Green AA используется фиксированный нулевой Хартри, пять локальных каналов и Core e171. [Исходный matched-вход](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/postboot/native-bias1mV-postreboot/matched.toml).
```

```{qexperiment} B0 и S01 с фиксированным потенциалом
:id: QX_133_B0_S01
:family: campaign133
:at: QP_S01_70K
:observes: QO_RESIDUAL
:status: completed
:stationarity: unverified
:stage: fixed U, inner SCBA
:evidence: QE_133_B0_S01

B0 и исторический S01 — отдельные серии; в этих запусках Poisson не выполнялся. S01 включает cold fixedU32 и два warm 64-map варианта (unmodified и FD); warm имеет отдельную историю и первую точку повторной оценки границы. Не считать тёплые запуски независимыми холодными репликами.
```

```{qevidence} Идентичности и малые истории B0 и S01
:id: QE_133_B0_S01
:family: campaign133
:availability: public_compact
:locator: provenance/run-identities.toml; evidence/*/history.csv

[Оригинальный набор и описание](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133). Выборка содержит три B0 и три S01 summary, а также CSV трёх S01; полные состояния не включены. График остатка сам по себе не является научной приёмкой.
```

```{qexperiment} Preflight native 0/1 мВ: backup PR 13
:id: QX_133_PREFLIGHT
:family: campaign133
:at: QP_S01_70K
:status: planned
:stationarity: not_measured
:stage: preflight
:verdict: not_measured

[Протокол](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/edc7e2d4ed3b2646d89704bf478a14da3a977613/experiments/campaign133/candidates/native-bias1mV/protocol.md), [статус](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/edc7e2d4ed3b2646d89704bf478a14da3a977613/experiments/campaign133/candidates/native-bias1mV/pre-reboot-status.json): начатых больших случаев ноль. Позднейшие postboot имеют другую identity и не делают этот backup выполненным.
```

```{qexperiment} Postboot: native coarse 0 и 1 мВ/период
:id: QX_133_COARSE
:family: campaign133
:at: QP_S01_70K, QP_133_1MV_70K
:status: completed
:stationarity: unverified
:stage: fixed U, native SCBA
:observes: QO_CURRENT, QO_RESIDUAL
:verdict: unresolved

[Протокол, вход и summary](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/postboot/native-bias1mV-postreboot). ALL5 без e–e, фиксированный U; по 32 карты на каждое смещение, оба случая unresolved. Это не принятая ВАХ. Научный Core e171 не следует задним числом заменять более поздним db26.
```

```{qexperiment} Postboot: fine48001
:id: QX_133_FINE
:family: campaign133
:at: QP_S01_70K, QP_133_1MV_70K
:status: aborted
:stationarity: not_measured
:stage: fixed U, native SCBA
:observes: QO_CURRENT, QO_RESIDUAL
:verdict: incomplete

[Протокол и доступные истории](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/postboot/native-bias1mV-fine48001). Остановлен пользователем; принятой согласованной пары нет. Прерывание не является научным отрицательным результатом.
```

```{qexperiment} Postboot: warm128 продолжение coarse
:id: QX_133_WARM128
:family: campaign133
:at: QP_S01_70K, QP_133_1MV_70K
:depends: QX_133_COARSE
:status: completed
:stationarity: unverified
:stage: fixed U, native SCBA
:observes: QO_CURRENT, QO_RESIDUAL
:evidence: QE_133_WARM128
:verdict: unresolved

При 0 и 1 мВ/период по 128 вычислений на случай, первое воспроизводит границу parent32, следовательно не более 127 новых состояний. Тот же bias и исходное состояние своей ветви, без FD-интерполяции; оба `converged=false`, `scientific_acceptance=false`. Отдельный FD-seed warm128 также unresolved; первая λ/J построена инициализацией и не является независимым ответом.
```

```{qevidence} Независимая сверка warm128
:id: QE_133_WARM128
:family: campaign133
:role: independent
:availability: public_compact
:locator: postboot/reviews/native-bias1mV-warm128-max26-result.md; attempt01/summary.toml

[Обзор](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/postboot/reviews/native-bias1mV-warm128-max26-result.md) сверил 256 строк и provenance без повторного чтения больших массивов. Конечные J 115.496 и 17.317 А/см² при 0 и 1 мВ/период несошедшиеся, поэтому не задают проводимость или ВАХ. Порог и фактические residual см. в обзоре и CSV.
```

## Дополнительные ограниченные проверки campaign133

В [описании snapshots и исходных папках](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates) сохранены отдельные входы и сводки серий; наименования ниже служат точными местами доступа к отдельным опытам, а не обобщением одинаковых результатов.

| Серия и исходное место | Фактический предел |
|---|---|
| `pi-frozen-control`, `static-map-control`, `adjacent`, `warm-q-quick`, `warm-q-hermitian-lambda`, `warm-spectral-obstruction` | Замороженные или локальные диагностические контроли; полная SCBA не принята. Некоторые summary — обозначенные проекции без приватных путей. |
| `ifr-benchmark-attempt01`, `ifr-benchmark-protocol.md`, `reviews` | Benchmark и независимые обзоры относятся к оператору IFR; указанное ускорение 2,2 не распространяется на весь SCBA. |
| `equilibrium-gamma-solver`, `equilibrium-gamma-warm`, `equilibrium-gamma-warm-hermitian` | Неисполненные варианты и отказ по памяти не результаты; cold attempt02 ограничен 16 картами без сходимости, native validation не измерялась. Warm Herm16 unresolved. |
| `equilibrium-gamma-hermitian-cont128`, `equilibrium-gamma-affine4096`, `residual-support`, `global-gamma-exact-pd` | Уменьшение reduced residual не доказывает сходимости SCBA; exact-PD относится к сохранённому Γ64. Полная per-energy таблица residual support осталась на VM. |
| `positive-source-preflight`, `equilibrium-gamma-stableA16`, `trial-cone-rayleigh`, `positive-source-selected-big` | Selected-big проверяет 44 выбранных узла, не всю сетку; stableA16 не является опытом ускорения или научной приёмкой. |
| `equilibrium-gamma-stableA-cont64`, `refinement-control`, `fine-mu-decomposition`, `streaming-spectral`, `equilibrium-gamma-projected64` | Cont64 завершён по лимиту, не по сходимости; recovery refinement не добавляет карт. Streaming qualifier проверяет эквивалентность оператора. Projected64 сравнивает 64 начатых Π (62 карты и два отказа); native acceptance и точный PSD не установлены. |
| `equilibrium-gamma-fine2x-m1`, stable-source Jv и Matsubara (`reviews`) | Fine2x-m1: coarse initial, 12 fine и terminal coarse map, не сходимость; Jv ограничен четырьмя проверенными направлениями. Matsubara all5 — конечное N, fixed μ, не предел N→∞; на итерации 2 отрицательная плотность. |
| M3, endpoint и μ-root (`reviews`, postboot/adjacent) | M3 V1 timeout; V2 и endpoint V2 отдельные контроли. μ-root V1 завершился world-age ошибкой до модели и карт; V2 — отдельная identity, N=512/1024, 112 map records. Невыполненные V1 endpoint и старые μ128/256 не результаты. |

См. `COPY-MANIFEST.tsv` и ledger проекций в исходном наборе для точного происхождения, SHA и различия побайтовых копий и очищенных проекций. Планы spectral-edge, fine-grid, mixed-axis и feasibility bond-current не являются выполненными экспериментами. Сохранённый компактный материал не доказывает доступность полных исходных данных.

## Матрица происхождения исторического среза

| Источник | Содержимое и роль | Учёт и границы |
|---|---|---|
| [research main 76926d0](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba) | Campaign133, литература, модель | Канонический опубликованный срез. Ниже отдельные результаты различены по `attempt`. |
| [issue133 artifacts e379bc9](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/e379bc9/experiments/campaign133), [postboot 5318d0e](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/5318d0e/experiments/campaign133/postboot), [postboot final 5703b9e](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/5703b9e/experiments/campaign133/postboot) | Последовательные архивные снимки | Все три коммита — предки main 76926d0; повторно отдельными опытами не считаются. Более ранний срез нужен для истории состава, а не для новой реплики. |
| [preflight edc7e2d](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/edc7e2d/experiments/campaign133/candidates/native-bias1mV) | Backup несостоявшегося preflight | Не предок research main; ссылка на отдельную ветвь. |
| [equilibrium 5458212](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/5458212063a41051328ef8b5d14d63d5ac7dc781) | Исходный S01 паспорт и вход | Не предок research main; исторический формат не проверен на новом runner. |
| [reference-2019](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/literature/reference-2019) | Публикация, геометрия и оцифрованная кривая | Литературный эталон 200 K, отдельный от S01 70 K. Публикация не содержит исходных числовых NEGF-данных. |
| Локальные VM HDF5, identity, сырые журналы | Полные исходные массивы, некоторые повторные проверки | В публичном наборе отсутствуют; записи hash и компактные проекции не доказывают доступность или независимое чтение полных данных. |

## Отдельные ограниченные варианты и записи

Ссылки ведут к конкретным компактным summary на зафиксированной ревизии; расположенные рядом протоколы и независимые обзоры задают полные условия и допуски. «Выполнен» здесь относится только к заявленной ограниченной операции, не к приёмке стационарного решения.

| Вариант и свидетельство | Что проверено и фактический исход |
|---|---|
| [pi-frozen-control/attempt01/public-summary-projection.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/pi-frozen-control/attempt01/public-summary-projection.toml) | Frozen Π: спектральный контроль; не полное решение, исходная сводка очищена от приватных путей. |
| [static-map-control/attempt02/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/static-map-control/attempt02/summary.toml) | Оператор на общем Green; embedding и central Dyson не выполнялись; эквивалентность baseline и SCBA не установлена. |
| [warm-q-quick/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/warm-q-quick/attempt01/summary.toml) | Один finite4 R/K спектральный probe, без fit μ, scattering, Φ или SCBA. |
| [warm-q-hermitian-lambda/attempt02/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/warm-q-hermitian-lambda/attempt02/summary.toml) | Отдельный probe Hermitian λ с теми же ограничениями; это не новая SCBA. |
| [warm-spectral-obstruction/attempt01/public-summary-projection.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/warm-spectral-obstruction/attempt01/public-summary-projection.toml) | Избранные exact-double 45-chain oracle; полный retarded pass, μ, Φ и SCBA не проверены. |
| [raw/S01-FD64-continuation128/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/raw/S01-FD64-continuation128/summary.toml) | 128 вычислений; max_iterations, converged=false, quality=unresolved. |
| [equilibrium-gamma-solver/attempt02/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/equilibrium-gamma-solver/attempt02/summary.toml) | Cold Γ, 16 Π, завершённый ограниченный опыт, scientific_acceptance=false. |
| [equilibrium-gamma-warm-hermitian/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/equilibrium-gamma-warm-hermitian/attempt01/summary.toml) | Warm Herm16, 16 Π; scientific_acceptance=false и unresolved. |
| [equilibrium-gamma-hermitian-cont128/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/equilibrium-gamma-hermitian-cont128/attempt01/summary.toml) | Продолжение Herm16, 128 Π; physical checks перенесены от parent, не повторены; приёмка false. |
| [equilibrium-gamma-affine4096/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/equilibrium-gamma-affine4096/attempt01/summary.toml) | Affine continuation, 32 Π; source checks pass, physical checks заимствованы, научная приёмка false. |
| [residual-support/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/residual-support/attempt01/summary.toml) | Локализация residual на сохранённом snapshot; без вывода о Jacobian, linewidth или сходимости. |
| [adjacent/cauchy-tree-prototype/frozen-attempt01/public-summary-projection.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/adjacent/cauchy-tree-prototype/frozen-attempt01/public-summary-projection.toml) | Frozen Cauchy для k=1,6,11; полная сертификация и экономия density SCBA не измерены. |
| [adjacent/decimation-probe/attempt01/public-summary-projection.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/adjacent/decimation-probe/attempt01/public-summary-projection.toml) | Конечная цепь и поверхность при фиксированных Γ и квадратуре; чувствительность полного sampled A/M не закрыта. |
| [adjacent/contour-oracle/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/adjacent/contour-oracle/attempt01/summary.toml) | Frozen Π off-axis density; формальной полной оценки хвоста нет, сходимость SCBA не измерялась. |
| [ifr-benchmark-attempt01/public-summary-projection.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/ifr-benchmark-attempt01/public-summary-projection.toml) | Сравнение реализаций IFR-оператора; это не ускорение полного SCBA. |
| [positive-source-preflight/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/positive-source-preflight/attempt01/summary.toml) | Три operator-only карты, tiny checks pass; без AA/projector и native acceptance. |
| [equilibrium-gamma-stableA16/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/equilibrium-gamma-stableA16/attempt01/summary.toml) | 16 Π; stable integration checks pass, scientific_acceptance=false; независимая повторная полная физическая проверка не выполнялась. |
| [trial-cone-rayleigh/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/trial-cone-rayleigh/attempt01/summary.toml) | Exact-rational знаки Rayleigh в выбранных направлениях; без Π, solver и acceptance. |
| [positive-source-selected-big/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/positive-source-selected-big/attempt01/summary.toml) | 44 избранных узла certified exact PD; не полная сетка и не приёмка SCBA. |
| [equilibrium-gamma-stableA-cont64/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/equilibrium-gamma-stableA-cont64/attempt01/summary.toml) | 64 Π до cap, scientific_acceptance=false; native exit не установлен. |
| [equilibrium-gamma-projected64/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/equilibrium-gamma-projected64/attempt01/summary.toml) | 64 начатых Π (62 карты и 2 отказа); научная приёмка и точный PSD projected F64 не установлены. |
| [global-gamma-exact-pd/all-attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/global-gamma-exact-pd/all-attempt01/summary.toml) | 337744 блока сохранённого unprojected ΓLast64, exact PD; сходимость и native acceptance не измерялись. |
| [refinement-control/attempt01/public-summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/refinement-control/attempt01/public-summary.toml) | Две Π завершены, затем InexactError; решение SCBA не сошлось. |
| [refinement-control/recovered-postprocess01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/refinement-control/recovered-postprocess01/summary.toml) | Восстановление диагностик после ошибки; 0 новых Π, не новый расчёт. |
| [fine-mu-decomposition/attempt01/public-summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/fine-mu-decomposition/attempt01/public-summary.toml) | Разложение вклада в μ на сохранённых источниках; 0 Π и 0 полных Φ. |
| [streaming-spectral/qualified-attempt01/public-qualifier-summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/streaming-spectral/qualified-attempt01/public-qualifier-summary.toml) | Операторная эквивалентность; zero Φ, mixing и μ fit; разные scope и JIT исключают вывод о скорости. |
| [equilibrium-gamma-fine2x-m1/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/equilibrium-gamma-fine2x-m1/attempt01/summary.toml) | Ограниченный fine-grid контроль: один coarse initial, 12 fine, terminal coarse; SCBA_accepted=false. |
| [adjacent/stable-source-jv/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/adjacent/stable-source-jv/attempt01/summary.toml) | Пять Φ и четыре Jv в выбранных направлениях, без native calls и научной приёмки. |
| [adjacent/gamma-density-hermitian-v4/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/adjacent/gamma-density-hermitian-v4/attempt01/summary.toml) | Frozen Π, hH all9, плотность конечного N; причинность и ошибка полного хвоста не доказаны. |
| [adjacent/matsubara-all5/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/adjacent/matsubara-all5/attempt01/summary.toml) | N128 и N256 завершены по лимиту 32 итераций, native_pass=false. |
| [adjacent/matsubara-moments/attempt02/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/adjacent/matsubara-moments/attempt02/summary.toml) | M3 V2 postprocess; inner maps=0, finite-N tail certificate=false. |
| [adjacent/endpoint-gap-certificate/attempt01/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/adjacent/endpoint-gap-certificate/attempt01/summary.toml) | Endpoint V2: positive gaps для обозначенного конечного scope; не аппаратная формальная верификация и не научная приёмка. |
| [adjacent/matsubara-mu-root-refined/attempt02/summary.toml](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/candidates/adjacent/matsubara-mu-root-refined/attempt02/summary.toml) | V2 finite N=512/1024, 112 map callbacks, научная приёмка false, предел N→∞ не сертифицирован. |

## Ранние планы, fixtures и научный контракт

[План fresh fixtures от 3 октября](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/ab2d616/docs/fresh-fixtures-2026-10-03.md) выделяет четыре синтетических операторных вопроса: связность при дробном energy shift (ожидаемые 2 и 1 сектора и проверка collision scale), impurity contraction при 70 K с oracle 2048/4096 углов (допуск oracle < 10⁻⁵ и относительный допуск contraction < 5·10⁻⁵), сохранение подпространства при basis cropping и finite-window PV на аналитических спектрах. Это спецификации и ограничения операторных fixtures, не отдельное свидетельство принятой QCL. Синтетические входы не дают experimental validation, а сам план не запускает большую SCBA/Poisson кампанию.

[SCI03 — контракт измерения равновесия](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/f47b703/docs/equilibrium-measurement-contract.md) имеет статус CP-DESIGN APPROVED только для bounded measurement/pilot design: `run=not_created`, входные fingerprints и идентичности исполнения отсутствуют. Проверяемый вопрос — thermal fixed point при 0 мВ/период и 70 K, с LO/acoustic/impurity/IFR/alloy, без e–e, с finite-chain embedding4. Пороговые условия и предполагаемые модели не являются измеренным исходом; finite accuracy, truncation и nonlinear conditioning оставлены открытыми. Ветви [model-passport 12316a2](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/12316a2) и [recovery-budget 12f8bd3](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/12f8bd3) сохраняют связанные документы и планирование; их отдельное существование не доказывает новый запуск.

## FD-seed: отдельный postboot-вариант

```{qexperiment} Однократная FD-инициализация и native128
:id: QX_133_FDSEED
:family: campaign133
:at: QP_S01_70K, QP_133_1MV_70K
:depends: QX_133_COARSE
:status: completed
:stationarity: unverified
:stage: fixed U, native SCBA
:observes: QO_CURRENT, QO_RESIDUAL
:evidence: QE_133_FDSEED
:verdict: unresolved

При 0 и 1 мВ/период отдельно использованы coarse32 seed той же ветви; исходные L/G однократно заменены глобальным FD, R/GR/A сохранены. Затем выполнено по 128 полных native-карт без повторной FD-проекции. Модель ALL5 без корреляционного e–e, U=0 без Poisson, 70 K; N=24001 в [−0,3; 0,9] эВ, Nk=11, Nb=5, direct-static C, LO PIFFT, finite-chain4. Оба случая имеют max_iterations, converged=false и scientific_acceptance=false. FD при конечном смещении — искусственное начальное приближение, не равновесное условие. Этот опыт отличается от unmodified warm128 и по инициализации, и по политике ресурсов.
```

```{qevidence} Независимая сверка FD-seed native128
:id: QE_133_FDSEED
:family: campaign133
:role: independent
:availability: public_compact
:locator: postboot-final/reviews/native-bias1mV-FDseed128-max26-result.md; native-bias1mV-FDseed128-max26/attempt01/summary.toml

[Обзор результата](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/postboot-final/reviews/native-bias1mV-FDseed128-max26-result.md) и [вход, сводки, отдельные истории](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/postboot-final/native-bias1mV-FDseed128-max26). Проверены 256 строк и compact ledgers без повторного чтения больших HDF5 или собственных eigensolves. Последние J = −0,168491 и 2,605534 А/см² несошедшиеся; constructed первая λ/J не являются независимой физической наблюдаемой. Остатки меньше unmodified128 при одинаковом бюджете карт, но обе ветви не прошли native gates; этот результат не доказывает существование либо отсутствие физического решения.
```

[INFO-padding benchmark](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/blob/76926d0035eeddf7c59a8c4357ab98f4e3bc9eba/experiments/campaign133/postboot-final/reviews/core32-info-padding-result.md) — ограниченный surrogate, не проверка сходимости и не доказательство механизма ускорения. Green-variable map, источники Green AA, PSD/occupation и оценки ширины LO в `postboot-final/adjacent` — анализ или предложения, не исполненная новая физическая приёмка. Численные инициализационные JSON — помеченные проекции, полные массивы исключены.

## Учёт всех доступных research refs

Проверены имена деревьев и ancestry всех 19 именованных ветвей `origin` относительно `origin/main` на ревизии `8aef781`; от `76926d0` её дерево отличается только README-перенаправлением. Эти строки показывают учёт refs, а не утверждают, что каждая строка каждого исходного файла уже сверена.

| Ветви и зафиксированные tips | Состав и решение по переносу |
|---|---|
| [campaign/fath-20261118 `38c86c2`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/38c86c2), [fath54-20261119-followup `f42cb0f`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/f42cb0f), [fath54-20261120 `824fd9a`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/824fd9a), [fath-dupont-20261120 `d2868af`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/d2868af) | Четыре отдельные от main ветви научных отчётов и свидетельств Fath и Dupont; охвачены отдельными страницами Fath и V843. При деревесном сравнении с общим предком — соответственно 277, 9, 3 и 2 добавленных пути; число путей не равно числу опытов. |
| [issue133-experiment-artifacts `e379bc9`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/e379bc9), [postboot-native-evidence `5318d0e`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/5318d0e), [postboot-final-evidence `5703b9e`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/5703b9e) | Предки main, сохранены как исторические срезы единого campaign133; не считать их копии независимыми запусками. |
| [native-bias-preflight-backup `edc7e2d`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/edc7e2d) | Не предок main, 15 изменённых или добавленных путей. Содержит незапущенный preflight, отдельный resource-v1 и adjacent-анализ; нет результата запуска. |
| [fresh-fixture-plan `ab2d616`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/ab2d616), [s01-equilibrium-source-entry `981c260`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/981c260), [review-closure-model-passport `12316a2`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/12316a2), [review-closure-equilibrium-criteria `f47b703`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/f47b703), [equilibrium-recovery-budget `12f8bd3`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/12f8bd3) | Исторические fixtures, S01, паспорт и SCI03/ресурсные рамки; не предки main. Паспорт и SCI03 отражены выше; фиксация плана и бюджета не является исполнением. |
| [review-closure-contribution-routing `f8bd6f9`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/f8bd6f9), [gui-configurator-catalog `6221198`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/6221198), [review-closure-current-bound-contract-integration `408ca41`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/408ca41), [p26-researcher-guide-20261029 `627c334`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/627c334), [project-simplification-2026-10-27 `46fb51f`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/46fb51f) | Интеграция существующего S01, маршрутов документации и configurator catalog. Прямое сравнение промежуточных деревьев показывает добавление catalog и researcher guide и уточнение существующих документов; эти изменения не дают автоматически новые численные опыты. Не предки main. |
| [feat/russian-policy-20261010 `4c3d754`](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/4c3d754) | Правила языка и шаблон PR; две добавленные служебные записи, не научная кампания. Не предок main. |

Вышеприведённая проверка деревьев выявляет научные семейства по путям и истории, но не заменяет сверку каждого содержимого, reviewer notes и имеющихся локальных данных; полный охват всех экспериментов ещё не установлен.

## Принятая конечночастотная равновесная опора M3

```{qexperiment} Fixed-charge Matsubara N512 и независимый N1024
:id: QX_133_MATSUBARA_M3
:family: campaign133
:at: QP_S01_70K
:observes: QO_RESIDUAL, QO_CHARGE, QO_STATIONARITY
:status: completed
:stationarity: passed
:stage: finite_N_equilibrium
:criteria: Три последние сырые невязки REL≤1e−9 и ABS≤1e−12 на каждый вызов; заряд и сравнение частотных отсечек
:verdict: Последние три прошли во всех семи вызовах; max REL 1,59634e−18, ABS 1,58311e−19
:variants: QR_133_MATSUBARA_N512, QR_133_MATSUBARA_N1024
:evidence: QE_133_MATSUBARA_M3
:supports: QC_133_MATSUBARA_M3

U=V=0, 70 K, finite45/hH-all9, один центральный источник повторяется в девяти ячейках, direct-static, full-line LO и reference-tail+M3. Шесть внешних вызовов N512 и один независимый N1024 начинались от Σ=0; доля свежего источника 1, по 16 карт. Подтверждена стационарность этой конечной карты и её заряд. Сходимость исходного native real-energy baseline, предел N→∞ и транспорт при ненулевом смещении оставались открыты.
```

```{qrun} N512, шесть вызовов для подбора химпотенциала
:id: QR_133_MATSUBARA_N512
:status: completed
:stationarity: passed
:stage: finite_N_equilibrium
:evidence: QE_133_MATSUBARA_M3
:verdict: относительная ошибка целевого заряда −2,30581e−11
```

```{qrun} N1024, независимая проверка на выбранном μ
:id: QR_133_MATSUBARA_N1024
:status: completed
:stationarity: passed
:stage: finite_N_equilibrium
:role: independent
:evidence: QE_133_MATSUBARA_M3
:verdict: относительная ошибка целевого заряда −2,23776e−10; разность N1024−N512 −2,00718e−10
```

```{qevidence} Сводка и независимая проверка finite-N M3
:id: QE_133_MATSUBARA_M3
:availability: public_compact
:role: independent
:locator: issue133-report, § Главный результат; independent-review, строки 5–13
:supports: QC_133_MATSUBARA_M3

[Отчёт со значениями](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/e74aef3b0520da80ad56d36643e58599707abe97/docs/campaigns/issue133-report.md#L44-L50) · [Независимая сверка уравнений и чисел](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/e74aef3b0520da80ad56d36643e58599707abe97/docs/campaigns/issue133-independent-review.md#L5-L13)
```

```{qclaim} Конечночастотная карта M3 при фиксированном заряде прошла проверку
:id: QC_133_MATSUBARA_M3
:status: supported
:evidence: QE_133_MATSUBARA_M3

Это численная равновесная опора для определённых граничного замыкания и отсечек. Без M3 ошибка заряда меняется до −4,6958e−7 и −5,8919e−8 от цели на соответствующих отсечках.
```

## Сквозная диагностическая точка 48 мВ

```{qpoint} Reference-2019-derived, 48 мВ на период, 70 K
:id: QP_SMOKE_48_70K
:structure: QS_BOSCO_2019
:bias_kind: per_period
:bias_value: 48
:bias_unit: mV
:temperature: 70 K
:sign: Положительный записанный электронный ток направлен вдоль +z
:optical: unknown

[Конфигурация stationary-smoke](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/runner/examples/config/stationary-smoke.yaml)
```

```{qexperiment} Сопоставление локального и HTCondor исполнения одного frozen plan
:id: QX_SMOKE_48
:family: integration_diagnostic
:at: QP_SMOKE_48_70K
:status: completed
:stationarity: failed
:lo_mode: enabled
:observes: QO_CURRENT, QO_RESIDUAL
:stage: two_SCBA_maps
:criteria: Три последовательные карты SCBA при допуске 1e−8
:verdict: rK 1,52929; rΣ 1,63657; обе среды завершили точку unconverged
:evidence: QE_SMOKE_48

48 пространственных и 49 энергетических узлов, пять радиальных импульсов, три состояния и один период. Доступное окно −0,10…0,28 эВ при требуемом покрытии примерно −0,15656…0,30122 эВ. Успешный перенос замороженного плана и независимое чтение показали эквивалентность инженерного тракта на этой малой точке.
```

```{qevidence} История smoke 48 мВ, повтор чтения и отказы
:id: QE_SMOKE_48
:availability: public_report_local_arrays
:locator: stationary-checkpoint, history.h5:/scba/r_K и /scba/r_Σ, задания 18.0–20.0

В отчёте приведены отказ обязательной записи, задача 18.0 с exit 127, 19.0 с недостатком памяти и успешная 20.0. Расхождения двух SCBA строк между локальным и принятым удалённым запуском не превышали 1,60e−14 и 5,55e−15 для rK и rΣ соответственно. Полные исходные выходы локальны.
[Исходный отчёт](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/docs/implementation/stationary-checkpoint-2026-11-18.md#L41-L114)
```
