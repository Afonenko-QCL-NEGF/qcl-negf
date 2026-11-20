# S01: кандидат стационарного теплового равновесия

Статус — ordinary source candidate, не scientific accepted. Вход
[`config/equilibrium.yaml`](../config/equilibrium.yaml) включает только
[`equilibrium-0-70`](../config/studies/equilibrium-0-70.yaml): `operation: stationary`,
`purpose: research`, один independent point **0 mV/period, lattice/LO 70 K**,
одна baseline variant. Он не включён в bundle 48 mV/refinements.
Наличие YAML или successful planning не является выполненным SCBA/Poisson.

## Вопрос и различающее свидетельство

Даёт ли сохранённая модель самосогласованный thermal fixed point при общих
baths, согласованный с одной Fermi–Dirac μ, итоговыми U/G, raw SCBA/Poisson,
нейтральностью и нулевым интегральным током? Достаточность дискретизации
проверяется отдельно после принятого baseline. Это верификация равновесного
предела модели, не validation ненулевого транспорта по эксперименту.

Конкурирующие объяснения — thermal final fixed point; Fermi seed/number
normalization скрывает raw defect; interpolation/window/basis ограничивает
равновесные тождества. Различает raw final map на том же U/G, full-matrix
raw/normalized FDR при одной μ, raw charge/correction и чувствительность
принятого baseline. Сходство двух непринятых candidates не доказывает accuracy.
Локализованные projected populations не автоматически occupations energy
eigenstates. Acoustic elastic/static same-energy и LO energy shifts сами не
обосновывают уникальный возврат из произвольного initial.

## Используемая композиция и происхождение

Источники в порядке merge: reference model, analytical-diagnostic policy,
затем study overrides. Ниже source audit ожидаемых inputs; authoritative used
inputs, assigning leaf histories и point passport хранит Runner frozen plan.
Formula origin (уравнения), value origin (обоснование числа) и assigning origin
(последний override) — разные свидетельства. Generated Runner labels показывают
assignments, не происхождение физических чисел; отсутствие YAML leaf может
означать typed default, а не отсутствие closure.

| Группа | Сохранённые inputs | Value/assigning origin и ограничение |
| --- | --- | --- |
| Структура/doping | Слои 3.26/7.99/1.90/8.40/2.90/5.16 nm; Al fraction0.25; doped segment2.90 nm; sheet4.5e14 m⁻²; ionization1 | Model и structure CSV/passport связывают с Bosco; primary contents/точный locator ещё не проверены |
| Условия | Vperiod0 mV; lattice/LO70 K; spin2 | Новый study выбирает bias, axes задают point; model задаёт T/spin; generated assignments — final assigning owners |
| Материал | Offsets/masses/permittivities; ħωLO36.7 meV; screening0.20 nm⁻¹; IFR0.10 nm/9 nm; acoustic constants без изменения | Явные model assumptions; один DOI о структуре не устанавливает origins всех чисел |
| Рассеяние | LO/acoustic/impurity/IFR/alloy enabled; alloy potential0.60 eV, cell4.5168e−29 m³; e–e none | Первые четыре — model; alloy — policy; e–e none — typed default |
| Closures | Fixed screening, parabolic dispersion, thermal LO; без hot/fixed nonequilibrium phonons | Runner/Core typed defaults; согласованные thermal baths — предпосылка FDR |
| z/basis | Nz96, Nb5, basis periods3 | Nz policy; basis model; projected finite basis остаётся ограничением |
| Energy | NE30721; [−0.30,0.90] eV; trust margin80 meV; seed broadening1.25 meV | Policy/model; Fermi seed не результат solve |
| Momentum | Nk11; kmax0.60 nm⁻¹; angular32; qz81/max10 nm⁻¹ | Policy nodes и model cutoffs; адекватность не установлена |
| Algorithms/boundary | sparse_plan shifts, FFT Hilbert, paired_convex normalization; finite_chain periods4; full self-energy/resolved transverse momentum | Policy/model; embedding — boundary assumption, не автоматически numerical refinement |
| Solver | Existing tolerances/windows/confirmation counts; adaptive_working; SCBA2048/Poisson128; mixing0.2/0.15; checkpoint32 | Model+policy+study; iteration caps не finite compute grant |
| Window adaptation | none | Typed default; окно не меняется ради pass |

Относительно `reference-48` единственное intentional physical изменение —
выбранный bias0; labels/entry identity меняются административно. Full final=true,
projections=true, optical=false, intermediate history64; recovery enabled,
1800 s, 2 generations, 8 GiB byte budget/64 MiB reserve; telemetry enabled/buffer256
сохранены. Recovery bytes не бюджет вычислительного опыта. Raw model preset56 mV
не является effective выбранным bias0; physical override, generated study voltage
и point passport должны согласоваться.

## Oracle, открытые критерии и границы

Общий аналитический oracle — FD/FDR на полном final Green matrix при общих
thermal baths и одной μ. Core владеет уравнениями и научными критериями;
этот brief не добавляет критерии в YAML, schema, UI или scheduler.
Первичные FD/FDR/DOS citations и их formula locators нужно проверить отдельно.
Small scalar/manufactured/LO-only operator anchors полезны в своей области;
их reduced geometry/channels/nodes/toy tolerances не принимают published-structure S01.

До научного опыта нужны обоснованные applicability, weights, units, normalization,
near-zero behavior и tolerances FD/FDR/raw residual/charge/current checks.
Для J=0 требуется абсолютный |J| в A/m² с основанием ошибки; relative division
by zero и universal threshold не вводятся. Existing project tolerances сохранены.
Finite-window tails и projected-basis/local-current sensitivity учитываются
явно. Unmeasured discretization/experimental evidence не становятся pass.

Research passport цитирует Bosco et al., *Thermoelectrically cooled THz quantum
cascade laser operating up to 210 K*, DOI 10.1063/1.5110305. См.
[passport](../literature/reference-2019/source.yaml) и
[literature limits](../literature/README.md). Primary contents с declared hash
и locators геометрии/дозы отсутствуют в предъявленном Git наборе; material/scattering
value origins ещё требуют обоснования как источников или явных assumptions.
Included digitized NEGF curve200 K — иные условия, не S01 equilibrium oracle.

Научный бюджет этой source подготовки: **0 attempts, 0 solver CPU-hours**.
Перед compute нужны fresh runtime/resource/calibration/admission/storage facts,
finite aggregate attempts/CPU-hours, per-job CPU/RAM/wall/output, stop rules и
конкретное различающее свидетельство. Capacity shortage не разрешает уменьшить
модель. После accepted baseline выбираются несколько различающих refinements;
existing48 variants автоматически не запускаются. Embedding — boundary-model
sensitivity; k-cutoff variant одновременно меняет energy window.

## Ожидаемый будущий результат

Exact run/attempt/state/hash, frozen plan/passport, full final GR/GL/GG/A и
U/density/weights/units, raw audit/scalar history, independent FD/FDR/charge/current
таблица и sensitivities. Execution, equation convergence, physical gates,
discretization и experimental validation сохраняются отдельными verdicts.
Сейчас final dataset и numerical S01 evidence не предъявлены; optical gain
не требуется этому рубежу и остаётся отдельным обоснованием.
