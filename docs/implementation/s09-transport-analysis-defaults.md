# S09: transport-only default analysis

Runner `postprocess_series` по умолчанию выбирает только `iv`, `populations`, `density_map`,
`potential_map`, `energy_density_map`. Existing CLI `analyze` наследует этот default без новых
flags. Прежние default `gain_voltage` и `optical_map` теперь требуют явного выбора existing expert
keyword API; supported helpers/schema/quality handling и `optical_recompute` не изменены. Сохранение
expert API не доказывает количественную точность gain.

Genuine RED: 24 pass / 8 fail / 32 total / 0 errors; GREEN: 32/32, 14.439 s. Два вызова ограничены
60 s/128 KiB каждый; исходный RED log сохранён. Fixture исполняет actual producer/helpers и
unchanged CLI с hand-literal transport data и synthetic saved I/O; expected five operations
независимы от production defaults. Проверены отсутствие optical reads в default, готовые/
отсутствующие expert gain/map, missing-photon guard и сохранение unconverged quality и
converged/figure accepted=false. Completed derivation не означает принятого состояния.

Fixture evaluates parsed actual source, исключая только whole `_recompute_optics` definition из-за
Unitful macros; count этого исключения проверяется. Его native mathematics не тестировались.
Core/Runner/HDF5/Unitful не импортировались; saved toy bytes не native HDF5 archive.
Canonical/native archive integrity, whole-package integration и scientific validation не проверены.
Stdlib warnings в original logs сохранены.

Три source files: producer default/docstring, narrow user docs, standalone contract fixture.
Model/scattering/grids/tolerances/evaluators и solver inputs сохранены. Scientific attempts 0; новых
installs/full suites/CI/deploy нет. Source diff check прошёл.

SHA256 frozen source diff: `e8222eea0ca8fc95a5fe706beaf4352bf45e5672ea7f2302ebb61234bab82405`.

| Утверждение                                      | Свидетельство                                      | Ограничение                                 | Решение             |
| ------------------------------------------------ | -------------------------------------------------- | ------------------------------------------- | ------------------- |
| Daily API/CLI default transport-only             | Genuine RED и actual routing GREEN                 | Synthetic saved I/O                         | изменить            |
| Explicit expert optics сохранены                 | Ready/missing assertions и unchanged helper source | Native recompute mathematics не выполнялись | сохранить           |
| Unconverged/false metadata не повышены           | Literal metadata и figure assertions               | Не scientific dataset                       | сохранить           |
| Scientific/native archive acceptance установлены | Таких свидетельств нет                             | Отдельные numerical/integration gates       | данных недостаточно |
