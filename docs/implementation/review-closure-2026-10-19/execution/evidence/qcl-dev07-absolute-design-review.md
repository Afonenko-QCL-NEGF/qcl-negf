# DEV02 O08-05 / DEV07 D1 — независимый CP-DESIGN review

Дата: 2026-10-19. Этап: source/math review, без исполнения target-кода.
Вердикт: **PASS для четырёх absolute-amplitude design passports** в явно
ограниченной области ниже. Блокирующей неизвестности физического prefactor,
неверной конечной суммы или product-as-oracle не найдено. Это не runtime PASS,
не scientific acceptance S1 и не проверка применимости приближений к прибору.

## Identity, независимость и фактически прочитанные материалы

- Root: `9d8cf0cad32743791cc3b80ac7c2a948dab02f48`; selected Core gitlink:
  `f7b108bef206d2b2dc5afe0306b2dff60d27ac59`; actual Core:
  `7324d98c0fccd61b4a1a2756b5cabe2fd0e0e49c`, status пуст.
- Фактические root `git status --short` и recursive submodule status прочитаны;
  root имеет unrelated staged/dirty/untracked работу. Ничего в Git не менялось.
- `git diff selected actual` пуст по kernels/constants/scaling/types/grids/
  basis/Hamiltonian. Все десять selected blob IDs таблицы D1 проверены через
  `git ls-tree` и совпадают. Изменения G1 вне этих путей не получают приёмку
  от данного review. Это не утверждение об отсутствии других source changes.
- D1: `/tmp/qcl-dev07-absolute-design.md`, SHA256
  `1d74158042e305c37875ceef25589b08f6ca9256fdd7f65993ee6825c165a07e`.
  Companion identity SHA256
  `3ec116f268114be68de41e25360f165ea016ef00fff467930bb456b2a46f1cc5`.
  Эти два digest пересчитаны reviewer.
- Прочитаны root AGENTS, architecture, entrypoint, DEV02/DEV07 development,
  Core CONTRIBUTING, qcl-physics-audit и памятка. Отдельного Core AGENTS нет.
- Сначала прочитаны owning kernels/scaling/basis/grid/constructors и первичные
  уравнения; затем candidate derivation и его заключения. Предыдущие author
  reviews и согласие других агентов не использованы как доказательство.
- Локально прочитаны Lee–Wacker v1 PDF pp19–22 (B8/B10/B11/B19–B23), Huang v2
  PDF pp2–3 (Eq8/9), Archetti v1 PDF pp8–9/21 (Eq20 и Appendix). Версии и
  primary PDF SHA256 даны frozen identity; reviewer не выполнял повторный
  полный hash PDF. Старый обзор Jirauschek–Kubis не нужен для данного вывода.
  Нового web/download не было.

## Независимая проверка модели и геометрии

Owning источник: selected Core, `src/numerics/reference/kernels.jl`, blob
`bad297072d742f27b2e1eb35eab1fb937d6ae3db`. Raw kernel — covariance с
единицей J²m²; нормировка `K0=E0_J² L0_m²`. Occupancies, spin, radial и energy
weights не принадлежат этому raw coefficient.

Manufactured one-state fixture не является изменённым S1. Все positive inputs
допустимы проверяемыми `PhysicalParameters`, `NumericalParameters`, `Layer`.
`Nz=3`, `Nk=2`, `Nphi=4`, `Nqz=3` удовлетворяют нижним границам, margin
удовлетворяет `2 M_E < Emax-Emin`. Положительный LO screening обязателен;
`q_LO,s=0` нельзя незаметно вводить ради unscreened limit. Carrier строится
через builders, без unchecked positional types или отключения validation.

Для `ell=1e-8 m` и `tau=hbar²/(2 m0 mr ell²)` BDD central block равен
`tau/E0 * A`, где `A=[4 -1 0; -1 9/2 -1; 0 -1 5/2]`. Независимое умножение
даёт `A*[1,2,4]=2*[1,2,4]`; characteristic factors дают spectrum
`[2,7/2,11/2]` и gap `3/2`. Нормированный `v=[1,2,4]/sqrt(21)` поэтому
независим от результата eigensolver. Проверены также `sum |v|^4=13/21`,
centre `31/14`, spread² `44/147` в cell-length units, coupling `-4tau/21`.
`:none` выбирает именно эту central-cell eigensystem; zero translation fields
не объявляются успешной PzP/translation validation.

Для четырёх углов `q²ell²` у pair `(k,k')=(2/ell,2/ell)` равны
`[0,8,16,8]`. Весь radial tensor должен проверяться по буквальной таблице
`[f(0) f(4); f(4) (f(0)+2 f(8)+f(16))/4]`, с четырьмя ненулевыми entries.
Здесь «2×2» — radial axes; basis axes имеют размер 1. Порядок/adjoint общей
четырёхиндексной covariance при `Nb>1` этим не проверяется; D1 это прямо
ограничивает (lines204–223), что соответствует one-state scope DEV07.

## Проверка каждого канала

**LO — PASS design.** Lee–Wacker B20 использует абсолютные permittivities.
Из `|g_Q|²=e² W (eps_inf^-1-eps_s^-1)/(2 eps0 A Lz Q²)` и
`sum_qz -> Lz integral dqz/(2pi)` получается owning prefactor
`e² W (eps_inf^-1-eps_s^-1)/(2eps0)` [J²m]. Замена `Q²` на
`Q²+q_LO,s²` — явно отдельное owning screened-model assumption, не формула
экранирования, доказанная этой статьёй.

На трёх физических точках probabilities `[1,4,16]/21` дают напрямую
`F(-pi/ell)=-13i/21`, `F(0)=1`, `F(pi/ell)=13i/21`. Трапеция с weights
`pi*[1/2,1,1/2]/ell` после деления на `2pi` даёт
`I(v)=ell/2 * (1/(v+1)+(169/441)/(v+1+pi²))` [m]. Следовательно
`f_LO=e²*(.05e)/(32eps0)*I(v)` [J²m²] верен. Это точный finite discrete
RHS, не бесконечный qz integral. Actual F не входит в expected kernel.

**IFR — PASS design.** Lee–Wacker B10/B11 даёт full band-step vertex без
diagonal-only сокращения, а Huang Eq8 задаёт Gaussian correlation convention.
Прямое двумерное Gaussian transform даёт `pi Delta² Lambda² exp(-q²Lambda²/4)`
[m⁴]. Huang screening factor не переносится в owning bare IFR модель;
exponential Lee–Wacker B8 не используется вместо Gaussian.

Из right seam и midpoint interpolation следуют interface amplitudes
`sqrt(ell)*psi=[1,3/2,3]/sqrt(21)` и jumps `[3/2,1/2,-2]tau`.
Отсюда `D*ell/tau=[1/14,3/56,-6/7]`, квадратная сумма
`(16+9+2304)/3136=2329/3136`. Полученный D1 `f_IFR` [J²m²] верен.
Drop/double seam меняет сумму на `16/3136`, что намного больше arithmetic
envelope. Дискретное right-seam значение не выдаётся за continuum psi(0).

**Acoustic — PASS design.** Longitudinal displacement vertex даёт
`|g_Q|²=Xi² hbar Q/(2rho V vs)`. В elastic equipartition сумма emission и
absorption даёт `2kBT/(hbar vs Q)` и ровно сокращает vertex factor 1/2.
Archetti Eq20/Appendix подтверждает coefficient `Xi²kBT/(rho vs²)`;
nanowire geometry статьи не переносится в planar projection. Mixed-space
Fourier completeness даёт four-envelope integral [m^-1]. Literal spatial
sum равен `13/(21ell)`, поэтому D1 coefficient имеет J²m² и верен.
Это проверка уже объявленного elastic coefficient, а не доказательство
equipartition applicability для реального спектра при 70 K или 35 K.

**Alloy — PASS design.** Независимый Bernoulli-site covariance при site
density `1/Omega` даёт `Omega DeltaV² x(1-x) delta³(r-r')`. Huang Eq9
подтверждает variance/volume convention `Omega=a³/4`; его carrier screening
не переносится в owning bare disorder. При `x=1/4` интеграл равен
`(3/16)*13/(21ell)=13/(112ell)` [m^-1]. `Omega DeltaV²` [J²m³] и итоговый
J²m² RHS верны. Site volume и potential contrast — synthetic inputs,
отдельные от manufactured band jumps; material calibration не утверждается.

## Arithmetic criterion и выявляемость wrong global factor

Проверены связи D1 lines230–350: независимые literal constants/scale,
направленные 256-bit reference intervals, scalar grid/profile certificates,
независимый eigen residual к literal A и gap bound на basis error. Frobenius
norm `||abs(A-2I)||F=sqrt(29/2)` и используемый gap `3/2` верны.
Precondition не предполагает заранее, что LAPACK обязан его пройти.

Propagation имеет положительные конечные нормировки: quartic `13/21`, IFR
`2329/3136`, LO `|F|²>=169/441`, denominator>=1 в физических cell units.
Проверены IFR sums `sum jump² p=207/112` и `sum jump²=13/2`, а также
quartic perturbation `2h+3h²`. Positive angular average сохраняет максимальную
relative error bound. Нули выделены в точные algebraic cases (Delta=0,
x=0/1), без artificial absolute SI tolerance. Scale B даёт тот же physical
SI coefficient при `K0_B=16 K0_A`; каждая scale сравнивается с собственным
RHS до supplementary A/B equality.

**Обязательные условия implementation, ещё не измеренные:** actual operation
inventory должен укладываться в gamma(1024); local trig/exp на фактически
представленных Float64 аргументах должны получить заявленный MPFR certificate;
interval evaluation должно быть настоящим enclosure всех выражений и
conversion inputs, а не просто двумя global-rounding evaluations произвольной
составной функции. Это прямые требования D1, не разрешение увеличить допуск.
Если certificate или inventory не подтверждается, зависимый channel остаётся
blocked до исправления arithmetic design. Настоящий review не превращает эти
будущие measurements в pass. Bessel из nanowire derivation не вычисляется в
новом oracle и не требует libm certificate в его runtime path.

Expected не вызывает raw kernels, reducers, `_scaled_physics`, `_K0`,
`build_kernels`, actual CODATA/readback scales, actual F или qK*Khat.
Общий basis builder защищён независимым literal residual/gap precondition.
При `R>0` и `delta<1/8` retained interval для healthy amplitude и doubled
amplitude не пересекается: direct raw assertion отличает глобальный factor2,
хотя нормированная форма остаётся той же. Width reference interval отдельно
входит в enclosure; она при 256 bits не заменяет machine error envelope.

Existing exact_kernel_rescaling остаётся algebraic control. Прочитанный
impurity anchor использует reference impurity kernel с midpoint2048/4096 и
literal contraction против adaptive optimized path. Это независимость angular
rule/contraction, а не независимый microscopic impurity-prefactor oracle.
D1 lines549–557 корректно сохраняет эту границу; общая ошибка prefactor в
impurity не считается закрытой четырьмя новыми паспортами.

## Решения и STOP

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Четыре absolute prefactor/discrete RHS допускают implementation | Primary equations и независимые вычисления выше; selected kernel blob | Runtime и arithmetic certificates ещё отсутствуют | сохранить |
| Global2 различим без normalized/product oracle | Positive full radial table, independent RHS и delta<1/8 | Только указанная amplitude fixture, Nb=1 | сохранить |
| LO screening / bare IFR-alloy / elastic acoustic явно разделены с primary model | D1 per-channel assumptions и прочитанные первичные уравнения | Применимость реальному S1/device не проверена | сохранить |
| Test plan меняет S1 physics или ослабляет science tolerances | Такого изменения в D1 нет; raw synthetic API tests отдельны | Будущий code diff должен сохранить эту границу | сохранить |
| Certificates library/operation inventory фактически выполнены | Свидетельств runtime нет | Требуется отдельный bounded targeted receipt | дополнительно измерить |
| SCBA/Poisson convergence, physical gates, discretization sufficiency, experiment пройдены | В этом review нет таких данных | Source/math PASS этого не доказывает | данных недостаточно |

Выполнены только bounded document/source reading и Git/hash inspection.
Ни target imports, Julia/Python parser/tests, SCBA/Poisson, benchmarks,
install/build/server actions, Git mutations, source edits, ни дочерние агенты
не выполнялись. Документы извлекались стандартным pdftotext без запуска
вложенных скриптов. Уникальный набор трёх primary PDFs имеет 2457423 B;
выводы основаны на указанных страницах. Повторные document reads были, точный
OS disk I/O не измерен; unique bytes не выдаются за измеренный I/O.

**STOP:** четыре D1 design passports приняты только для stated absolute
amplitude scope. Реализация/targeted runtime, scientific acceptance и
production/model changes данным review не выполняются и не принимаются.
