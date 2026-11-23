# Библиотека QCL-NEGF

Основной обзор охватывает академическую литературу до 18 ноября 2026 года. Дополнение от 20 ноября связывает четыре первоисточника с результатами Fath и V843. [Сверка наблюдаемых и операторов](audit-preparation/evidence-index.md#fath54-v843) · [Задание по библиотеке](https://github.com/Afonenko-QCL-NEGF/qcl-negf/issues/141) · [Задание по базису](https://github.com/Afonenko-QCL-NEGF/qcl-negf/issues/140)

- [Карта от математических уравнений к Core](mappings/model-to-sources.md) охватывает PzP/Bloch/Wannier, пять scattering vertices, ретардированное замыкание, boundary/continuity, нормировку и самосогласование. [Навигация по темам](topics/README.md).
- [Матрица методов](mappings/methods-matrix.csv) сравнивает постановки. [Трассировка Core](mappings/code-traceability.csv) связывает функции на db26 с проверенными исходными местами и конкретным тестом. Исторические опыты маркируются идентификатором расчётного Core.
- [Поисковый журнал](audit-preparation/search-log.md) содержит даты, выборочные цепочки цитирования, критерии включения, реальные ограничения охвата и недочитанные материалы.
- [Индекс архивных свидетельств](audit-preparation/evidence-index.md) и [гипотезы, результаты, пять различающих проверок](audit-preparation/candidate-contradictions.md) включают Campaign 133, Fath, Green AA, Bosco и nextnano. Данные измерений Bosco и рассчитанная авторами кривая имеют разное происхождение.
- [Дополнение от 23 ноября](../../../docs/research-archive/literature.md#перенос-проверок-между-методами-и-приборами) связывает проверку базиса Fath с выводами Lee и с документацией nextnano. Сопоставлены NEGF и Монте-Карло для ККЛ, условия независимых сравнений V843 и LiEL2014, а также модели транзисторного транспорта NESS, QuaTrEx и QTCAD.

[Канонический каталог JSONL](catalog.jsonl) хранит устойчивый ID, авторов, версии, права, фактический доступ, координаты чтения и собственную аннотацию. [BibTeX](catalog.bib) генерируется из JSONL. Команда `python3 literature/build_catalog.py --write` обновляет BibTeX, команда без аргументов сверяет BibTeX, уникальность DOI/arXiv и ссылки в таблицах. В определении `read_full` доступен полный текст и проверены явно перечисленные места. `abstract_only` означает проверенную аннотацию, `metadata_only` — идентификатор или библиографическую запись, `unavailable` — не удалось получить требуемый источник. Внешний private manifest существует вне research. Публичный пакет состоит из ссылок и собственных аннотаций.

## Bosco et al. (2019) comparison data

`reference-2019` identifies the publication **Thermoelectrically cooled THz
quantum cascade laser operating up to 210 K**, Applied Physics Letters 115,
010601 (2019), [DOI 10.1063/1.5110305](https://doi.org/10.1063/1.5110305).
The label names a reference dataset, not an original experiment performed by
this software project.

| File | Content |
| --- | --- |
| `reference-2019/source.yaml` | Publication identity, digitization method, source artifact hashes, comparison limits and local data hashes |
| `reference-2019/structure.csv` | Published dimensions, doping and device characteristics with units and source descriptions |
| `reference-2019/negf_iv_digitized.csv` | Six digitized samples of the publication's calculated NEGF current curve, with digitization uncertainties |

The CSV current curve is a digitization of a **calculated NEGF curve**, not raw
experimental observations. Its active-region temperature is 200 K. The horizontal
calibration uses the publication's 56 mV-per-period peak statement. Quoted
uncertainties describe digitization only; they are not estimates of model error.
Do not extrapolate this curve to score points outside 40–60 mV per period.

Compare current density against voltage **per period**. Terminal voltage/current,
threshold current, optical output power, maximum operating temperature and
absolute gain require additional device physics and cannot be inferred from
agreement with these data. The 405-period geometry value in the example model is
not directly established by the publication and must not become a terminal
voltage validation target.

The source PDFs are not bundled. Their recorded hashes identify the source
artifacts used for digitization; local CSV hashes allow accidental data changes
to be detected without downloading those PDFs. When replacing or extending a
digitization, document the source curve, units, method and uncertainty, then
update its hash deliberately.
