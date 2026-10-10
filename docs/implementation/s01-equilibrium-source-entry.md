# S01: ordinary equilibrium candidate source

Owning Research добавляет отдельный meta `config/equilibrium.yaml` и study `equilibrium-0-70`:
research/stationary, одна independent baseline точка, 0 mV/period, lattice/LO temperature 70 K. Это
подготовка входа S01, а не результат решения уравнений.

Ordered model + analytical policy и stationary reference-48 overrides сохранены. Единственное
намеренное физическое изменение относительно этой композиции — bias 0 mV. Все пять scattering
channels, сетки/базис/окно, tolerances, solver policy и archive/recovery settings сохранены; full
final/projections=true, optical=false. Краткий brief различает formula/value/assigning origins,
typed defaults и assumptions с отсутствующими первичными свидетельствами.

## Локальные engineering checks

| Проверка                                   | Фактическое свидетельство                                                    | Ограничение                                                         |
| ------------------------------------------ | ---------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Catalog validator, один вызов              | 16 definitions / 30 configurations / 2 literature files/CSV datasets; exit 0 | Structural validation                                               |
| Existing targeted catalog case, один вызов | 1 passed; exit 0                                                             | System Python 3.14.7/pytest 9.1.1, не locked uv release environment |
| Matching Runner metadata API, один вызов   | 44 assertions; exit 0; 68.495 s                                              | CLI не исполнялся; без operators/SCBA/Poisson                       |

Semantic check сравнил полный point-resolved raw с reference-48, исключив только run name и два
voltage leaves; проверил literal grids/seed, all five channels, typed defaults, output, effective
origins, passport и freeze/load. Получены одна execution/point, independent/cold/no predecessor,
actual 0 V/T70/TLO70. Список sources не выдан за effective leaf owner или formula/value evidence.

Все три проверки выполнены по одному разу: пределы 60/60/180 s, diagnostics 1/1/2 MiB; фактический
суммарный diagnostics 634 bytes. Metadata plan/summary 51735 bytes, меньше 4 MiB. CPU/RAM limits не
вводились; peak RSS/CPU не измерены и не служат scientific admission. Generated plan, локальные
paths и logs сохранены вне Git; scientific arrays не создавались.

SHA256 frozen source diff: `e71d71fd3fda0fd72faa3e828d7bc053155d7d6fc368a7592b2ac5c06035eb6d`.
SHA256 serialized metadata plan: `5cf1cd380f6014f8c665bf0a9256497a4f8b995c066f01ec7b9b01b3089f1d16`.

Scientific budget — 0 attempts. Нет final run/state/attempt, проверки FD/FDR, нулевого тока,
нейтральности или refinement. Primary citation contents, обоснованные FDR/absolute |J| thresholds и
свежие finite compute budget/admission остаются gates до опыта. Toy LO-only operator и digitized 200
K NEGF curve не принимают published-structure S01. CI/deploy/install/full suites не запускались.

| Утверждение                               | Свидетельство                                       | Ограничение                     | Решение                |
| ----------------------------------------- | --------------------------------------------------- | ------------------------------- | ---------------------- |
| Ordinary input 0/70 согласован с plan     | Catalog и metadata assertions                       | Source/planning acceptance      | изменить               |
| Baseline composition кроме bias сохранена | Full raw comparison и literal/default/origin checks | Не solve/state validation       | сохранить              |
| S01 equilibrium научно принят             | Final numerical evidence отсутствуют                | Scientific attempts 0           | данных недостаточно    |
| Дискретизация достаточна                  | Accepted baseline/refinements отсутствуют           | Требуется отдельный finite опыт | дополнительно измерить |
