# Первый научный рубеж и метод работы

Статус: выбранная цель, проект проверки перед запуском. Новые вычисления
этот документ не разрешает. Связанные требования: S01–S09, C01–C06, R07–R09.

## Проверяемое утверждение

Первый рубеж по уточнению пользователя: самосогласованное стационарное
**тепловое равновесие при 0 mV/period и 70 K** опубликованной GaAs/AlGaAs
структуры. Проверяются населённости, итоговое U/G, нейтральность, нулевой
ток и чувствительность к дискретизации. Это верификация равновесного
предела модели/реализации. Совпадение с аналитическим равновесием само не
доказывает экспериментальную точность транспорта при ненулевом bias.

Основной кандидат источника — Bosco et al., DOI
[10.1063/1.5110305](https://doi.org/10.1063/1.5110305),
[полный текст](https://arxiv.org/pdf/1911.06582).
Именно к нему уже привязаны геометрия и sheet doping каталога research.
Нужно фиксировать конкретную геометрию/дозу по тексту и явно объявить
остальные material/model assumptions; равновесный oracle не берётся из
экспериментальной ВАХ этой статьи.

Существующий `reference-48` — 48 mV/period, 70 K — теперь кандидат
**следующего ненулевого** transport рубежа, а не первой точки. Включённая
digitized curve — опубликованный NEGF расчёт (solid black) при 200 K, не
экспериментальный набор и не oracle S01. Research model
`reference-2019-70k.yaml:64` сам содержит 56 mV; frozen plan должен явно
разрешиться в 0 mV. `operator-lo-equilibrium.yaml:22–25` содержит ось 0 mV,
но запускает operator check, а не полный stationary SCBA/Poisson.

Температуру нельзя повышать до 200 K ради удобного reference и называть
это той же задачей. Источник расхождения уже документирован в
[scientific inputs](../../components/qcl-negf-research/docs/scientific-inputs.md).

## Что означает ожидаемое равновесие

Для электронов общий эталон — Fermi–Dirac:

\[
f(E;\mu,T)=\frac{1}{1+\exp[(E-\mu)/(k_BT)]}.
\]

Классическая экспонента Boltzmann допустима только при
\(\exp[(\mu-E)/(k_BT)]\ll1\) в существенной части спектра. Температура
70 K и отсутствие напряжения сами не доказывают этот предел. μ определяется
числом электронов и спектром, а не независимо подгоняется для каждой
населённости. [Smirnov, (2.30)–(2.31)](https://www.iue.tuwien.ac.at/phd/smirnov/node25.html).

В конвенции ядра \(A=i(G^R-G^A)\) равновесное FDR:

\[
G^<=ifA,\qquad G^>=-i(1-f)A.
\]

Проверка относится ко всей матрице итогового Green state, а не только её
диагонали или графику population. Она сопоставляет доступный спектральный
вес с занятым/пустым при одной температуре и μ.
[Fotso–Freericks, (42)](https://www.acsu.buffalo.edu/~hffotso/MyPapers/FrontiersPhys_FDT.pdf).

Для независимого малого anchor идеальных параболических 2D-подзон можно
интегрировать их DOS:

\[
n_i=\frac{g_i m_i k_BT}{2\pi\hbar^2}
\ln\!\left[1+e^{(\mu-E_i)/(k_BT)}\right].
\]

Здесь \(n_i\) — sheet population (m⁻²), \(m_i\) — in-plane mass,
\(g_i\) — объявленное вырождение, включая spin без двойного учёта.
Для полного broadened NEGF используется интеграл fA с фактическими weights;
населённости локализованного базиса не автоматически являются occupations
энергетических eigenstates. DOS anchor: [Lee–Wacker, Appendix B, (B2)](https://arxiv.org/pdf/cond-mat/0212059).

Предпосылки: общий thermal bath 70 K, thermal LO Bose occupation, отсутствие
hot/fixed nonequilibrium phonons и внешней инжекции; при e–e closure —
согласованная температура. Для periodic Poisson проверяется
\(\int(N_D^+-n)dz=0\) и выбранный gauge Hartree. При 0 V геометрия и
легирование всё равно дают неоднородные potential/n(z); нулевая разность
потенциалов не требует плоских зон или одинаковых population.

### Что можно проверить существующим кодом

- Core `src/numerics/reference/scba.jl:59–78` задаёт seed через ifA и μ из
  number target. Совпадение seed с Fermi не является результатом solve.
  Последующая SCBA использует Dyson/Keldysh (`189–201`): проверять её
  итоговый raw map и согласованное U/G.
- `greens.jl:141` корректирует number через occupied/empty spectral weight;
  `final_audit.jl:48` хранит raw charge, λ и raw Keldysh residual. Нормированное
  число частиц само не доказывает raw conservation; коррекция должна быть
  объяснима и исчезать в принятом fixed point в пределах обоснованной ошибки.
- `src/numerics/optimized/physics_markers.jl:273–329` уже сравнивает raw и
  normalized occupied/empty weights с fA. Эти markers diagnostic-only
  (`1–2`); их наличие/available не означает принятую проверку S01.
- `test/physics/production_lo_equilibrium_discretization.jl:104–119`
  различает integer/fractional LO energy shifts; интерполяционный KMS error
  убывает при refinement. Это существующий operator fixture, не предъявленный
  полный расчёт опубликованной структуры; тест сейчас не выполнялся.

Важно ограничить обещание о начальном состоянии. Acoustic канал сейчас
elastic equipartition (`kernels.jl:233–252`), другие static channels не
переносят энергию (`415–438`), LO связывает E±ħω (`447–457`). Поэтому
нельзя заранее требовать уникального возврата к одной FD форме из любого
произвольного initial: модель не обязана смешивать все энергетические
секторы. Lee–Wacker обсуждают роль малого inelastic acoustic transfer при
low bias (§II.A, p.3). Это гипотеза по структуре операторов, не наблюдённый
failure. Первым проверяется сохранение/самосогласованность thermal fixed
point; ограниченное возмущение initial — отдельная robustness проверка.

Для нулевого ожидаемого тока используется абсолютная ошибка в A/m² с
обоснованным масштабом, а не относительная ошибка с делением на J=0.
Допуски FDR/raw residuals, weighting, хвосты спектра и критерии чувствительности
обосновываются до finite опыта; универсальный числовой порог здесь не задан.

## Уровни свидетельств

| Уровень | Что должно быть проверено | Что не следует из успеха |
| --- | --- | --- |
| Выполнение | Точный plan, finite run, сохранённый final state, читаемый результат | Сходимость |
| Итерации | Raw SCBA fixed-point residual, outer Poisson residual, финальные U/G одного состояния, причины stopping | Правильность физических уравнений и достаточность сетки |
| Физические проверки | Применимые spectral/charge/current/equilibrium checks с конвенциями, нормировками и допусками | Экспериментальная точность или полнота basis |
| Дискретизация | Чувствительность наблюдаемой и состояния к обоснованным grid/window/basis refinements при той же физической модели | Независимость от всех возможных discretizations; смена boundary model не считается автоматически refinement |
| Validation | Сопоставимые эксперимент/публикация, условия и uncertainties; различены calibration и проверка | Мощность/динамика, иная температура/структура или универсальность solver |

Критерии живут в owning scientific component. Не назначать универсальные
`1e-6`, монотонную I–V, positive gain или zero local-current variation без
вывода применимости. Core уже не заявляет campaign scientific acceptance
после одного solve; это сохранить.

## Минимальный различающий цикл

1. Research готовит короткий brief: вопрос, структура/условия, наблюдаемые,
   исключённые механизмы, analytical equilibrium oracle, критерии и ожидаемый различающий
   результат. Отсутствующие material parameters явно отмечены.
2. Из code/theory audit выбираются применимые независимые operator oracles.
   Shared reference/optimized kernel не считается независимым oracle.
   Уже существующие fixtures повторно используются только в своей области.
3. Runner разрешает небольшой вход в точный plan и прогноз CPU/RAM. До
   compute устанавливается конечный совокупный бюджет: attempts, CPU-hours,
   per-job wall time/RAM/output, stop rules. Он включает failures и refinements.
4. Выполняется baseline одной физической точки. Если candidate не принят,
   refinements не считаются исследованием точности; сначала причина failure.
5. Выбираются несколько **различающих**, а не автоматически все девять,
   refinements. Каждое меняет известное направление ошибки и сохраняет модель.
   Энергетический шаг/окно, k grid/cutoff, spatial grid, basis/period embedding
   рассматриваются отдельно; достаточность покрытия обосновывается audit.
   Изменение embedding/boundary относится к model sensitivity, если не доказано,
   что оно уточняет одну заранее фиксированную целевую boundary model.
   Текущий research embedding variant помечен `boundary_model`; его нельзя
   автоматически включить в discretization pass.
6. Results независимо читает final states, строит таблицу чувствительности и
   заключение. Недостаточный бюджет может дать обоснованное «не установлено»,
   но не scientific pass. Отрицательный результат полезен, однако не заменяет
   выбранную пользователем приёмку S01.

После S01 — обоснованная отдельная ненулевая transport point, затем ВАХ
и transport maps. Zero-bias pass не переносится автоматически на finite bias.
Оптические gain/absorption
спектры пользователь отложил до отдельного обоснования количественного
отклика; existing expert API и его ограничения сохраняются в справке.
До S01 инфраструктурная работа допустима,
если устраняет конкретный blocker запуска/чтения/доверия, а не расширяет
универсальную платформу. Неразрешённый physical defect не лечится новым UI.

## Цель → предпочтительный рисунок

| Цель | Рисунок и подписи | Основание / ограничение |
| --- | --- | --- |
| Транспорт / ВАХ | J(V) с отмеченными непринятыми точками; T, V на период, units A/cm² или kA/cm² | Bosco Fig. 3(b); device voltage нельзя получить без period count/contact assumptions |
| Стационарная структура | Band profile + spatial-energy electron density, при нужде selected states | Bosco Fig. 3(a); объявить energy zero, momentum integration, normalization |
| Материальный отклик — отложено по S09 | Signed gain/absorption против photon energy, T и bias | Будущий шаблон: Bosco Fig. 1(b). Current bare-bubble model не даёт основания принять абсолютный gain по этой статье; это не мощность/эмиссионный спектр |
| Населённости | Relative state populations с правилами tracking basis states | Bosco Fig. 1(a); label state без mapping между вариантами может вводить в заблуждение |
| Спектральный транспорт | A(z,E), n(z,E), J(z,E) с единицами и integration conventions | Jirauschek/Kubis Figs. 32–34; A при k=0 не равна momentum-integrated density |
| Numerical reliability | Raw residuals vs iteration, final checks и observables vs refinement | Наша diagnostic recommendation; не выдаётся за экспериментальный QCL график |

Второй основной источник:
[Jirauschek & Kubis, Modeling techniques for quantum cascade lasers](https://arxiv.org/abs/1412.3563),
DOI [10.1063/1.4863665](https://doi.org/10.1063/1.4863665).
UI template должен хранить область применимости рисунка; высокий красивый
gain не заменяет сходимость или корректность модели.

## Как сократить цикл разработки

Рабочая единица — научный вопрос или конкретный failure contract, а не
«ещё один полный проход по инфраструктуре». До изменения формулируются
ожидаемый эффект, отличающий check и стоимость. После — проверяется ровно
это свойство и необходимые integration boundaries.

- Operator fixtures: analytic/manufactured/independent matrix oracle.
- Solver: малые nonlinear anchors и проверка final-state consistency.
- Runner/contracts/results: formats, statuses, attempt locators и bounded I/O.
- Platform: interruption/idempotence/identity, затем VM acceptance.
- S01: физическая точка и обоснованная discretization sensitivity.

Full CI, successful boot, content integrity и научная приёмка записываются
раздельно. Не суммировать счётчики перекрывающихся test suites и не
переносить старое acceptance на новый HEAD. Для обычных docs edits научное
окружение не требуется. В следующем запуске дорогие checks имеют общий
конечный бюджет; бесконечных автоматических reruns нет.

## Ожидаемый результат рубежа

Короткий brief + точные использованные inputs + final observables/state по
профилю вывода + таблица проверки и чувствительности + несколько рисунков
с units + заключение и границы применимости. Scalar iteration diagnostics
сохраняются для выбранного опыта; большие промежуточные matrices не
становятся обязательным evidence лишь ради отчёта.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Геометрия каталога имеет опубликованный источник | Research passport, Bosco paper | Совпадение полной model/temperature ещё надо установить | Сохранить источник, уточнить постановку |
| Одиночный candidate не доказывает discretization | Core final audit и независимые направления ошибки | Нужны finite variants, не новый framework | Дополнительно измерить |
| Existing operator tests полезны | Source fixtures и исторические журналы | Не являются предъявленным production QCL result | Сохранить |
| Срок настройки инфраструктуры не определяет время сходимости | Budget и нелинейная задача различны | Свежие measurements отсутствуют | Данных недостаточно |
