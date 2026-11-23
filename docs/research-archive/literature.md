# Литература, карты уравнений и свидетельств

Ключи ниже воспроизводят идентификаторы существующего каталога. Полнота доступа и проверенные места каждого первоисточника хранятся в его канонической записи. В этой сборке доступны {download}`каталог с аннотациями <../../studies/historical/literature/catalog.jsonl>` и {download}`BibTeX <../../studies/historical/literature/catalog.bib>`.

- [Тематический указатель и исходные аннотации](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/literature/topics/README.md)
- [Формулы и соответствующие функции Core](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/literature/mappings/model-to-sources.md)
- [Матрица методов](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/literature/mappings/methods-matrix.csv) · [Карта кода](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/literature/mappings/code-traceability.csv)
- [Индекс исходных свидетельств](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/literature/audit-preparation/evidence-index.md) · [Кандидатные противоречия и независимые проверки](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/literature/audit-preparation/candidate-contradictions.md) · [Поисковый журнал](https://github.com/Afonenko-QCL-NEGF/qcl-negf/blob/1815bf37cb978777f1cf8df69cba9b6af52e2e2a/studies/historical/literature/audit-preparation/search-log.md)

```{qsource} Fathololoumi et al. (2012)
:id: QL_FATHOLOLOUMI_2012
:locator: fathololoumi2012; Fig. 1 и описание активной области
:role: literature

{cite:p}`fathololoumi2012` задаёт литературную геометрию, энергетические уровни и уровни связи. Реконструкция CBO 149 мэВ фиксируется отдельным паспортом. Режимы максимальной температуры и мощности требуют отдельного сопоставления.
```

```{qsource} Lee et al. (2006), пространственный ток
:id: QL_LEE_LOCAL_CURRENT
:locator: lee2006-local-current
:role: literature

{cite:p}`lee2006-local-current` используется в карте пространственного тока. Совместимость наблюдаемых требует проверки разрезов, нормировки, базиса и ориентации тока.
```

## Перенос проверок между методами и приборами

```{qsource} Kubis и Vogl (2009), период распределения носителей
:id: QL_KUBIS_PERIODICITY
:role: literature
:locator: kubis-vogl2009-periodicity, §§ 2–4, рис. 1–3

{cite:p}`kubis-vogl2009-periodicity` сравнивают одно- и двухпериодную активную область между контактами. В их резонансно-фононной структуре при 52 мВ/период и 40 К ВАХ почти совпадают, хотя населенность и спектр тока в соседних каскадах различаются. Энергия теряется через один и два LO-фонона в последовательных каскадах, в модели уменьшается усиление второго каскада. Экстраполяцию на длинную цепь авторы делают по двум активным периодам. Для сравнения на Fath нужны независимо изменяемые распределения соседних периодов и общая энергетическая шкала с учётом падения напряжения.
```

В закреплённом Core для Fath связанные периоды используют общий источник, вычисленный на энергиях со сдвигом по номеру периода. Девять связанных периодов дают пространственный диапазон пропагатора. Чтобы проверить чередование заселённостей, нужно освободить хотя бы два источника для независимого самосогласования. Для паспорта Fath 2 × 54 = 108 мэВ и 3 × 36,7 = 110,1 мэВ. Близость энергий мотивирует опыт. При стационарности полный ток должен сохраняться и при чередовании спектров. [Сборка источника в Core](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/c2f45cae21c3e2e4257805ea9c30f9c1d80a7515/src/numerics/linked/selected_rows.jl#L16-L32) · [Построение энергетических сдвигов](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/c2f45cae21c3e2e4257805ea9c30f9c1d80a7515/src/numerics/linked/causal.jl#L200-L207).

```{qsource} Mátyás et al. (2009), два метода на одной структуре
:id: QL_MATYAS_EMC
:role: literature
:locator: matyas2009-emc-negf, §§ 1–3, рис. 1–4

{cite:p}`matyas2009-emc-negf` сопоставляют ансамблевый Монте-Карло и NEGF. Согласие около порога в исследованной структуре сменяется расхождением в подпороговой области когерентного туннелирования. Электрон-электронные столкновения включены в EMC. Для проверки общего матричного элемента LO можно выбрать пару подзон с узкими спектральными линиями и сравнить отдельно испускание и поглощение, уравняв населённости, экран, сдвиги энергии и меру интегрирования. Это предложенная проверка нашего оператора.
```

```{qsource} Li et al. (2014), эксперимент Лидса
:id: QL_LI_HYBRID
:role: literature
:locator: li2014-hybrid, Experimental details и рис. 1–3

{cite:p}`li2014-hybrid` задают геометрию, легирование и экспериментальные оптические характеристики гибридной структуры. Тёмное распределение в следующей работе рассчитано другой группой.
```

```{qsource} Winge, Franckié и Wacker (2016), единые параметры для серии ККЛ
:id: QL_WINGE_TRENDS
:role: literature
:locator: winge2016-trends, §§ II, IV–VI, табл. I, рис. 1, 3–6
:source: QL_LI_HYBRID

{cite:p}`winge2016-trends` задают для LiEL2014 наблюдаемую в одной рабочей точке — распределение плотности по энергии и координате при 50 мВ на период, 77 К, в темноте (рис. 3). Видны инверсия и скопление электронов в инжекторе и на верхнем уровне. Пики 500, 1100 и 1240 А/см² относятся ко всей кривой в трёх разных физических режимах. Для Dupont имеется также независимая матричная кинетика при 50 К, см. {need}`QL_V843_LITERATURE`. Во всех приведённых авторами расчётах используется приближение представительных передач импульса.
```

```{qsource} nextnano.NEGF, остаточная неоднородность и стоимость расчёта Fath
:id: QL_NEXTNANO_MODAL_CURRENT
:role: literature
:locator: nextnano-negf, FAQ и Getting Started

В {cite:p}`nextnano-negf` раздел [FAQ](https://www.nextnano.com/docu/nextnano.NEGF/faq/index.html) связывает неоднородность реконструированного тока у высоких барьеров с усечением мод. В [примерах Fath](https://www.nextnano.com/docu/nextnano.NEGF/getting_started/index.html) указаны типичные 5 минут и 2 часа на ВАХ, второй вариант включает высокие подзоны. Размеры матриц и фактический пик RAM для этих двух запусков в руководстве не приведены.

Для другого прибора доступен [оригинальный журнал теста Adams](https://github.com/nextnano-GmbH/nextnanopy/blob/f3eae6bcf2b7c15369d360d925643d29d9d314a1/tests/datafiles/nextnano.NEGF/example.log). Строки 43, 81, 85–89 дают 6 минизон, 22 поперечных состояния и 131 энергетический узел с шагом 2 мэВ для точки 4 мВ/период. Строка 1514 фиксирует неполную сходимость. Этот пример позволяет установить размеры по первичным данным для конкретной ревизии и рабочей точки.
```

```{qclaim} Вклад конечного подпространства в перепад тока Fath
:id: QC_FATH_PROJECTED_BARRIER_HYP
:status: open
:source: QL_LEE_LOCAL_CURRENT, QL_NEXTNANO_MODAL_CURRENT
:evidence: QE_FATH_LOCAL_K31

Проверяем, меняется ли профиль вблизи барьера при расширении подпространства и сопоставимых свежих невязках. Предсказание для того же подпространства сильнее: согласованная унитарная замена всех матриц, полной карты столкновений и наблюдателей должна сохранить полный наблюдаемый ток с точностью численных операций. Это разные опыты. Знак изменения при добавлении одной моды заранее неизвестен.
```

Среди открытых транзисторных решателей NESS описывает переход от баллистического случая к электрон-фононным самоэнергиям в модовом пространстве {cite:p}`berrada2020-ness`. Публикации QuaTrEx документируют самосогласованный GW в нанопроволоке и дальнейший переход к наноленте с пространственной декомпозицией {cite:p}`quatrex2024-gw,quatrex2025-gw`. В коммерческом примере QTCAD адаптивное интегрирование по энергии применяется к плотности и резонансному току в FET {cite:p}`qtcad-fdsoi-negf`. Эти источники описывают проверки и реализацию. Для сравнения токов между приборами требуются совпадающие физические условия.

## Доступ к публикациям

DOI остаётся идентификатором из исходного каталога. Издательские сайты Wiley, APS и AIP возвращали HTTP 403 при автоматической проверке, Optica перенаправляла на проверку браузера, а сервер IOP вернул HTTP 500 для одной статьи. Эти ответы характеризуют доступ в момент проверки. Дополнительные адреса для ключевых сравнений:

- Fathololoumi et al. (2012), [принятая версия в архиве NRC](https://publications-cnrc.canada.ca/eng/view/accepted/?id=98144fe2-7e95-448c-aa0e-06096537ad2d).
- Dupont et al. (2012), [авторская версия](https://arxiv.org/abs/1201.4189).
- Bosco et al. (2019), [авторская версия](https://arxiv.org/abs/1911.06582).
- Han et al. (2016), [архив публикации](https://eprints.whiterose.ac.uk/id/eprint/106583/) и [набор измерений и модельных кривых](https://archive.researchdata.leeds.ac.uk/99/).

## Библиография

```{bibliography}
:all:
```
