# Сопоставимость и доказательства

| Группа | Что извлечь из каждого запуска |
| --- | --- |
| Identity | Commit общего репозитория и компонентов, dirty diff при наличии, frozen plan fingerprint, schema, run/attempt |
| Физика | Геометрия/материалы, T, bias и единицы, density, boundaries, scattering, broadening, seed/continuation |
| Дискретизация | E step/window/phase, k density/cutoff, z/interfaces, basis/periods, embedding, quadratures |
| Метод | Алгоритм/mixing, raw residual definitions, inner/outer tolerances, strict final checks, iteration limits |
| Результат | Наблюдаемые, статусы/пороги/применимость, фактические итерации, stop reason, missing data |
| Стоимость | Hardware/SMT/affinity, Julia/BLAS threads, RAM, wall/CPU time, JIT/GC/I/O, attempts и accounting scope |

Для каждой строки обозначить: совпадает, контролируемое отличие, несопоставимо,
неизвестно. Отсутствующая величина не равна нулю. Отсутствие дискретизационных
свидетельств не устраняется малым SCBA residual.

Пути от корня общего репозитория, проверены для
`efb68778a9267cb11c6e9f49701ea2c247c35645`:

- `components/qcl-negf-results/README.md` — profiles `science`/`full-state`,
  multipart receipts; части ≤200 000 000 десятичных байт. Указанное здесь —
  транспортное ограничение проекта, не лимит загрузки ChatGPT.
- `components/qcl-negf-results/src/qcl_negf_results/model.py` — проверка model
  configuration hash; `native.py` — native payload; `history.py` — история;
  `multipart.py` — целостность набора; `witnesses.py` — выбранные свидетельства.
- `components/qcl-negf-contracts/src/qcl_negf_contracts/schemas/` — контракты.
- `components/QCLNEGFRunner.jl/docs/src/user/results.md` — restart/quality;
  analysis result не обязательно пригоден для восстановления состояния.

Текущий README results заявляет `qcl-negf.results.v1` и native HDF5 `4.0`.
При ином архиве сначала найти соответствующую версию reader. В отдельной
установке навыка запросить доступ к исходникам, если их нет; не угадывать схему.

Шаблон утверждения: «Для run R, attempt A, artifact SHA256 H, dataset D, slice S,
при предпосылках P наблюдается X; это поддерживает Y в пределах Z. Не проверено W».
Заявление о производительности передавать в qcl-performance-audit вместе
с этой матрицей, а не только с итоговыми временами.
