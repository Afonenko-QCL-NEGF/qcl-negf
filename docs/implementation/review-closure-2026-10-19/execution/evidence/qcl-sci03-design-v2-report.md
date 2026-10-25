# SCI03 — узкий D2 после independent R1

2026-10-19. D / Sol ultra, второй и последний initial design round. Прочитан
полностью `/tmp/qcl-sci03-design-review.md`, SHA256
`f917b3b6fab356dd1972aece21b34f1b4ba967e53303d613c373262b6bd96822`,
verdict `request_changes`. Подготовлен новый candidate; самостоятельного
CP-DESIGN PASS или scientific/native READY автор не объявляет.

## Immutable inputs/outputs

| Артефакт | Bytes / SHA256 |
| --- | --- |
| Сохранённый D1 `/tmp/qcl-sci03-design.md` | 40 020 / `ceffa4f2ca941510451f1d28a9f0cbaff7277e10411230c0b1dc8ab26c649509` |
| Новый `/tmp/qcl-sci03-design-v2.md` | 40 812 / `788ab058f1c52520d79aa621dcecd0d525f2562b7fcf2ea10da2c664989c8018` |
| Узкий `/tmp/qcl-sci03-design-v2.diff` | 6 680 / `3011ef89c2618d68145b537869d2a59ec6e670b2793fcc5ccf9d4faa6ccbe104` |

`v2` обозначает corrective author round; внутреннее имя SCI03-D1 и исходный
source snapshot намеренно сохранены: diff содержит **ровно три замены строк**
описания, отвечающие R1-01–03. Нет новой acceptance version, новых формул,
thresholds, scientific inputs, slots или source/runtime identity.

## Выполненные исправления

| Review finding | Узкое изменение | Первичное/owning evidence |
| --- | --- | --- |
| R1-02, P-DOS locator | Inelastic acoustic paragraph: printed p.3 → **printed p.4**; B1/B2 p.17 без изменения | Из уже существующего Lee–Wacker PDF с SHA256 `dfabd791bfb2aa4603233e9b545879e07a3bfc63e8906cbc810760726358ea0c` прочитана p.4, paragraph между Eq.2 и Eq.3 |
| R1-01, near-zero FDR | Локальный `_ratio(0,0)` не равен полному FDR verdict. Сохранён applicability gate; unavailable μ передаёт status/reason/value=None. При applicable context, nonnegative spectral-number weights и capacity≤0 — `not_measured/empty_represented_spectrum`; negative-weight/прочие причины не перезаписываются | Results `equilibrium.py::_fit_mu`239–244, fitted μ/fermi459–463, full FDR branch528–531 прочитаны; numeric/helper expression и FDR formula не менялись |
| R1-03, roundoff operands | Явно зафиксированы FJ=Φ± с gs/(2π), FC=unprefactored signed collision integral, FP=prefactored dimensionless channel power. Сохранены switch1e−12, multiplier100 и strict1e−10 | Core `observables.jl::collision_balance`314–321, `power_balance`391–397, `validation.jl`current-roundoff616–628; max по sides для J, по internal channels для P; C отдельно по channel |

В частности, relative branch не оправдывает игнорировать prefactor у switch и
absolute branch. Это уточнение буквального measurement descriptor, не найденное
изменение evaluator и не запрос новых runtime tests.

## Проверки и границы

- Сравнение D1→v2: ровно3 removed и3 added lines, три diff hunks; обратное
  восстановление permitted replacements даёт исходные D1 bytes. D1 hash сохранён.
- Повторно проверены14 owning source hashes из таблицы design и hash primary
  Lee–Wacker PDF; inputs совпадают с D1/R1. Git-команды/изменения не выполнялись.
- Восемь Markdown tables имеют прежнее число columns, fences сбалансированы,
  trailing whitespace отсутствует, newline в конце сохранена.
- Остальные bytes, включая reviewed derived μ/density/current bounds, strict
  policy, unknown εQ/tail/conditioning/truncation blockers и H+ΔE/4 protocol,
  не изменились. Algebra/product checks D1 повторно не запускались без причины.

Проверки использовали файловое чтение/сравнение и Python standard library для
hash/Markdown/diff; продуктовые imports, Julia, solver, native probes, benchmark,
install, builds, fullCI и numerical data не выполнялись. **0 scientific attempts,
0 solver CPU-hours**; новых primary downloads нет. CPU/RSS не инструментировались
и не объявляются measured profile. Старые S01 arrays/run/protected checkout
не читались. Component code/docs и root/checkpoint не редактировались.

## Состояние после D2

Нужна независимая адресная re-review exact v2 hash и узкого diff по R1-01–03.
Физическая/discretization accuracy остаётся blocked: finite accuracy basis,
tail/conditioning/truncation bounds не появились из редакционных исправлений.
H source-expressible в already approved phase slot согласно R1, однако exact
resolved plan/guards/fresh admission отсутствуют; runtime READY не заявляется.
Здесь работа остановлена, без третьего autonomous design round или implementation.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Три замечания R1 отражены в D2 | Exact3-line diff и адресные primary/source branches | Independent R2 ещё нужен | изменить |
| Derived bounds, strict policy, physics/S1/H сохранены | Остальные bytes совпадают с D1;14 hashes | Runtime/scientific evidence не добавлено | сохранить |
| Acceptance/native READY достигнуты | Те же unknown accuracy/bounds/admission | Source corrections не расчёт | данных недостаточно |
