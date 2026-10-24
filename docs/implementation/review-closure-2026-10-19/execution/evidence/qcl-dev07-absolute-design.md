# DEV02 O08-05 / DEV07: четыре absolute kernel oracle passports — D1

Дата: 2026-10-19. Этап: **SOURCE/DESIGN ONLY**. Автор: delegated DEV07,
роль Sol/ultra. Статус: **candidate для независимого CP-DESIGN**; принятие
дизайна и будущий targeted runtime receipt ещё отсутствуют. Четыре паспорта
ниже завершены как проект проверок; объявлять DEV07 implemented/pass нельзя.

Вопрос: обнаруживает ли прямое сравнение ненормированного kernel ошибку
абсолютного множителя, которая сокращается в нормированном LO balance/KMS?
Выход не меняет ни production kernels, ни физическую задачу S1: equilibrium,
0 mV, 70 K, LO+IFR+acoustic+alloy+impurity, electron–electron=none.
Одноуровневая manufactured geometry ниже — отдельная область проверки
дискретных коэффициентов. Она не заменяет frozen S1 model/plan и не
доказывает сходимость, достаточность сетки или валидацию прибора.

Разрешённый implementation path только
`components/QCLNEGF.jl/test/physics/absolute_scattering_kernel_oracles.jl`.
`test/physics/exact_kernel_rescaling.jl` остаётся неизменённым algebraic
control reference. Никаких production edits, fitting prefactors, удаления
scattering, новых SCBA/Poisson или изменения thresholds/models.

## 1. Identity и прочитанный контракт

- Root выбранного immutable source:
  `9d8cf0cad32743791cc3b80ac7c2a948dab02f48`.
- Core выбранного source:
  `f7b108bef206d2b2dc5afe0306b2dff60d27ac59`.
- Фактический Core HEAD при чтении:
  `7324d98c0fccd61b4a1a2756b5cabe2fd0e0e49c`, Core `git status --short`
  пуст. Сравнение выбранного и фактического commit по kernels, constants,
  scaling, grids, basis, Hamiltonian дало пустой diff. Все дальнейшие source
  утверждения привязаны к **selected Git objects**, а не к moving HEAD.
- Root checkout dirty/staged: он принадлежит общей EXEC работе; полный
  captured `git status --short`, submodule status и HEAD gitlinks записаны
  в companion identity JSON. Здесь Git не изменялся; original dirty checkout
  `/home/tolya/Загрузки/qcl-negf` не затрагивался.
- Прочитаны root `AGENTS.md`, `docs/architecture.md`, implementation
  entrypoint и канонический workflow, `development.md` DEV02/DEV07,
  `.agents/skills/qcl-physics-audit/SKILL.md` и памятка, Core
  `CONTRIBUTING.md`. В Core отдельный `AGENTS.md` отсутствует; root применим.
- Предыдущий принятый technical body:
  `/tmp/qcl-dev02-accepted-technical-body.md`, SHA256
  `ca3c12e84ee41bee3f13d1e1294c030197d0f35adca0f2ef61ebb9cd92b1707b`.
  Этот пакет дополняет только его O08-05; остальные oracle не заменяет.

Frozen primary source objects Core:

| Path / symbol | Git blob SHA1 |
| --- | --- |
| `src/numerics/reference/kernels.jl`: `_angular_average_kernel`, `_interface_value`, `_band_jump`, four raw kernels | `bad297072d742f27b2e1eb35eab1fb937d6ae3db` |
| `src/domain/types.jl`: checked physical/numerical constructors, carrier types | `e917407bf93e0ea0224c00d138acd56856caecf0` |
| `src/domain/constants.jl`: frozen constants | `4ec0934fca833b26e541f253c0158110a0407941` |
| `src/domain/scaling.jl`: `ScaleSystem` | `e0c9341fe601cdf0edb1183831f40213c048071f` |
| `src/numerics/reference/grids.jl`: grid/profile builders | `2719dab3b3211f5c361a91ce276f92cc1440cd37` |
| `src/numerics/reference/hamiltonian.jl`: BDD | `52f11f9db2b91bb54b2b608346d4c5cf614ae535` |
| `src/numerics/reference/basis.jl`: `localization=:none` | `85596354002c63d86408909f43968018f741d927` |
| `docs/src/theory/08_kernels.md`: EQ-KLO/KIFR/KAC/KALLOY | `c0d8af179614c20d8291c51f49aec554619384e3` |
| `test/physics/exact_kernel_rescaling.jl` | `cde889a3165411bbb01657729f71f21af265c774` |
| `test/numerics/frozen_scientific_fixtures.jl` | `803ad60a73bdf1240994167a43f8f4add680cb06` |

Git objects служат source receipt этого аудита, не новым lock-файлом состава.

## 2. Primary provenance и границы переноса

Все формулы RHS ниже независимо раскрыты из явно заданных covariance/vertex
предпосылок. Owning docs определяют реализуемую модель; совпадение docs и code
само по себе не является независимым доказательством prefactor.

| Primary source, version, equation | Original PDF SHA256 / bytes | Что действительно используется |
| --- | --- | --- |
| [Lee–Wacker, cond-mat/0212059v1](https://arxiv.org/pdf/cond-mat/0212059v1), B19–B23, PDF p21 | `dfabd791bfb2aa4603233e9b545879e07a3bfc63e8906cbc810760726358ea0c`, 514376 B, ранее сохранённый PDF | Bulk unscreened Fröhlich vertex, абсолютные permittivities и мера `dqz/(2π)` после area/length normalization. B10–B11, PDF pp19–20, поддерживают single-interface band-step vertex; B8 exponential covariance **не** источник Gaussian spectrum. |
| [Huang–Shklovskii–Zudov, 2205.00365v2](https://arxiv.org/pdf/2205.00365v2), Eq8 PDF p2; Eq9 PDF p3 | `00297abb84fdc44fc865461b9ba102dfef7ff7cde2924b2999b0deca054f5f5c`, 301118 B | Gaussian covariance convention `exp(-R²/Λ²)` и её Fourier factor `πΔ²Λ²`; Bernoulli alloy factor `Ωx(1-x)`, `Ω=a³/4`. Paper transport kernels также имеют dielectric screening; этот множитель не приписывается owning IFR/alloy model. |
| [Archetti–Neophytou, 2012.12344v1](https://arxiv.org/pdf/2012.12344v1), Eq20 PDF p9, Appendix “Derivation of Eq.20” PDF p21 | `843184eec1632f8f46fde7e3a2492126763487dc99172f0950761239f9ae046e`, 1641929 B | Primary calculation explicitly combines emission/absorption in the elastic equipartition limit, giving `Ξ² kBT/(ρv_s²)` per normalization volume. Its cylindrical nanowire geometry is **не** геометрия этой fixture; planar four-envelope projection выведена отдельно ниже. |

Авторский review Jirauschek–Kubis 1412.3563v1 прочитан только для source
tracing; его SHA `e2e43e27c96994bfa5aa8750044bef33afe92de1360c0c0c5861bf235d8ff7c8`,
2685475 B. Он не повышается до primary acceptance.

Различия моделей сохраняются явно. Для LO положительный phenomenological
`q_LO,s` добавлен **owning EQ-KLO-001**; Lee–Wacker не доказывает физическую
правильность такой screening model. Для IFR/alloy owning equations задают
bare disorder covariance без последующего carrier dielectric factor. Paper
Eq8/9 используется как независимая проверка microscopic prefactor/volume
convention, а не как утверждение, что screened mobility theory и Core — одна
модель. Derived bare covariance не является предложением убрать screening
из какой-либо production задачи. Текущий S1 ни одним из этих шагов не меняется.

## 3. Общий допустимый carrier, независимый от kernel builders

Expected path использует только literal SI constants и scalar/rational
алгебру; не читает expected из `CODATA`, `s.E₀_J`, `s.L₀_m`, `_scaled_physics`,
`_K₀`, kernel functions, reducers, `build_kernels` или `qᴷ*Khat`.

Константы — frozen input-contract literals, а не оценка их экспериментальной
неопределённости:

```text
e = 1.602176634e-19 C; hbar = 1.054571817e-34 J s
kB = 1.380649e-23 J/K; m0 = 9.1093837139e-31 kg
eps0 = 8.8541878128e-12 F/m
ell = 1e-8 m; mr = .067
tau_J = hbar²/(2*m0*mr*ell²); tau_eV = tau_J/e
```

`ell` — **физическая длина одной spatial cell**, сохраняемая при смене
units. Это не `s.L₀_m` readback. Предлагаются два независимых scale cases:

```text
A: E0=.1 eV, L0=10 nm, lambda=ell/L0=1
B: E0=.2 eV, L0=20 nm, lambda=ell/L0=1/2
K0_ref=(E0_eV*e)²*L0_m² [J² m²]
```

У case B `K0_ref=16*K0_ref(A)`. Оба cases сравниваются с собственным
absolute RHS; затем `Kbar_B=Kbar_A/16` только supplementary unit control.
Физические p/n и cutoffs не меняются; это смена единиц одной fixture.

Checked `PhysicalParameters` полностью задаётся следующими значениями;
dimensioned поля передаются в канонических Unitful field types, для энергий
`tau_eV*u"eV"`, для остальных — явно указанные SI quantities:

| Field | Literal manufactured input |
| --- | --- |
| layers | Три `Layer`, каждая `d=ell m`, `material=:manufactured`, `x_Al=1/4`, `Eᶜ/tau=[2,5/2,1/2]`; обе mass ratios `mr`; `εr=16`; каждая doped=true |
| N_dop²ᴰ, f_ion | `3e16 m^-2`, `1` |
| F_bias, z0, E_ref | `0 V/m`, `0 m`, `0 eV` |
| T_L, T_LO | `70 K`, `70 K` |
| eps_s, eps_inf | `16`, `8`; hence `eps_inf^-1-eps_s^-1=1/16` exactly |
| hbaromega_LO | `.05 eV` |
| q_s, q_LO,s | `1e8 m^-1`, `1e8 m^-1`, оба строго положительны |
| Delta_IFR, Lambda_IFR | `1e-10 m`, `ell m` |
| Xi, rho, v_s | `4 eV`, `4000 kg/m^3`, `4000 m/s` |
| DeltaV_alloy, Omega0 | `.6 eV`, `3.125e-29 m^3`; synthetic site lattice `a=.5 nm`, `Omega0=a³/4` |
| g_s, interfaces | `2`, `[0,ell,2ell] m`; endpoint `3ell` отсутствует |

Это positive synthetic coefficient inputs, не параметры конкретного
материала. В частности `DeltaV_alloy` — контраст site potential и **не**
тождественен малым manufactured layer band jumps `tau`. Они не подгоняются
по полученному kernel. Интерфейсы статистически независимы. Ни один из
четырёх каналов здесь не равен нулю, impurity не отключается каким-либо
`ScatteringOptions`; для вызова этих raw APIs такой объект вообще не нужен.

Checked `NumericalParameters`:

```text
Nz=3, Nb=1, P_basis=1, NE=3, Nk=2, Nphi=4, Nqz=3
Emin=-.1 eV, Emax=.1 eV, M_E=.05 eV, eta_seed=.001 eV
kmax=2/ell m^-1, qzmax=pi/ell m^-1
```

Future construction использует только public checked parameters +
`build_grids(p,n,s)`, `build_profiles(p,n,s,g)`,
`build_localized_basis(p,n,s,g,profiles;localization=:none)`.
Никаких unchecked positional `ModelGrids`/`MaterialProfiles`/`BasisData`,
построения `NEGFProblem`, `validate_static=false` или post-builder mutation.

Независимые geometry assertions до kernel calls:

```text
x=lambda*[1/2,3/2,5/2]; wx=lambda*[1,1,1]
kappa=[0,2/lambda]; wk=[1,3]/(4*pi*lambda²)
qz=[-pi,0,pi]/lambda; wqz=pi*[1/2,1,1/2]/lambda
phi=[0,pi/2,pi,3pi/2]
Ecbar=tau_J/E0_J*[2,5/2,1/2], masses=mr, epsr=16
xAl=[1/4,1/4,1/4], layer_index=[1,2,3], NDbar=lambda^-3*[1,1,1]
energy axes/weights follow the same stated physical .2 eV window;
trusted mask=[false,true,false].
```

Ни `wk`, ни `wE`, ни spin factor не входят в raw covariance amplitude.
Они входят в последующие contractions/observables и здесь не могут
компенсировать missing `2π`.

Независимый spatial Hamiltonian в units `tau_J`:

```text
A=[4 -1 0; -1 9/2 -1; 0 -1 5/2]
spec(A)=[2,7/2,11/2], v=[1,2,4]/sqrt(21), A*v=2v
gap=3/2; Phi=v (up to a scalar phase); chi=v/sqrt(lambda)
```

Это точная eigenpair Dirichlet central block с seam face masses,
используемого `localization=:none`; не ground state бесконечной периодической
структуры. У кода basis общее окно всё равно 9×9, но выбранный `:none`
использует отдельную 3×3 central-cell eigensystem. Доказательство spectrum:
`det(A-zI)=(2-z)(7/2-z)(11/2-z)`, direct multiplication даёт `A*v=2v`.

Для полного объяснения carrier fields:

| Basis field | Independent expectation |
| --- | --- |
| localization | `:none` |
| Phi, chi | scalar-phase `v`, `v/sqrt(lambda)` |
| centres, spreads | `[31lambda/14]`, `[lambda*sqrt(44/147)]` |
| overlap eigenvalues, condition | `[1]`, `1` to arithmetic error |
| H0, Z, M^-1 | `[2tau_J/E0_J]`, `[31lambda/14]`, `[1/mr]` |
| T+, T- | both `[-4tau_J/(21E0_J)]` |
| window_eigenvalues, Egrid0 | `[2tau_J/E0_J]`, `9tau_J/(2E0_J)` |
| r_orth, r_eigen | arithmetic residuals, independently bounded below; not assumed measured zero |
| translation fields | source assigns zero in `:none`; no translation/localization scientific pass is inferred from these bypassed fields |

## 4. Общие absolute assertions и конечный arithmetic budget

Return shapes всех `K`: `(2,2,1,1,1,1)`, units dimensionless;
`K_SI=Kbar*K0_ref` имеет J²m². LO также возвращает `F` shape `(3,1,1)`,
dimensionless. Каждый entry проверяется, включая imaginary component;
все expected `K` strictly positive real.

Для любого scalar function `f(v)`, где `v=q² ell²`, определим буквальную
2×2 таблицу без вызова angular routine:

```text
M[f] = [ f(0)                    f(4);
         f(4)    (f(0)+2*f(8)+f(16))/4 ]
```

Она следует из `[k,k']=[0,2/ell]` и четырёх declared angles: на втором
diagonal `q²ell²=[0,8,16,8]`. Деление на четыре — angular **average**,
не integral. Сравнить raw `K` со `M[f]/K0_ref` отдельно при A и B.
На expected side нет target routines, actual scale readback или target F.
Одно состояние не различает general four-index orientation/adjoints;
этот passport проверяет amplitude, quadrature factors и unit conversion,
а не полноту matrix covariance algebra при `Nb>1`.

Приведённый далее допуск — bound floating evaluation фиксированной малой
fixture. Он не допуск физической приёмки и не оценка continuum quadrature.
Для будущей реализации нужны все предусловия этого раздела; неизвестный
library error или нарушение bound означает stop, а не расширение tolerance.

### 4.1. Preconditions, independent arithmetic and basis certificates

Пусть `u=2^-53`, `gamma(n)=n*u/(1-n*u)`, `g=gamma(32)`, `a=gamma(1024)`.
RHS вычислять в Base BigFloat 256-bit из **decimal strings**/integers,
с направленным округлением; retained interval `[Rlo,Rhi]` охватывает
literal formula. Обычный decimal Float64 input и каждую unit conversion
нужно заключить отдельно; нельзя сначала округлить input в Float64 и
выдать его за exact decimal BigFloat reference. Inverse `K0_ref` входит
в этот interval, а не берётся из target.

Проверить каждый grid/profile scalar независимо с error envelope
`g*max(1,abs(literal))` в нормированных выше coordinates; нули `kappa[1]`
и центральный `qz` отдельно должны быть exact zero. Эти bounds покрывают
не более 32 scalar operations/conversions на узел; числа не «измерены pass»
в этом design. Profile `xAl=1/4` и integer indices должны совпасть exactly.

Для `c=sqrt(lambda)*chi[:,1]` не доверять residual из carrier. Вычислить
независимо literal `||(A-2I)c||2`, `||c||2²` и scalar phase alignment с v
в 256-bit interval arithmetic, используя literal A, не product H.
Требуются:

```text
abs(||c||²-1) <= g
||(A-2I)c||2 <= g*sqrt(29/2)
```

`sqrt(29/2)=||abs(A-2I)||F`. Это equation-level rounding envelope:
каждая трёхчленная complex row и norm имеют менее 32 elementary arithmetic
steps. Проверка требует residual не больше ошибки вычисления точного
eigen-equation в таком envelope; она не утверждает a priori, что любой
LAPACK обязан её пройти. В случае отказа не увеличивать `32`, не подставлять
actual basis в expected RHS: вернуть carrier issue на design.

Спектральный gap даёт явный basis error (после общей фазы):

```text
beta = g/(1+sqrt(1-g))
       + sqrt(2)*g*sqrt(29/2)/((3/2)*sqrt(1-g))
||c-v*phase||2 <= beta.
```

Первый член ограничивает normalization error, второй следует из проекции
residual на complement ground state и gap `3/2`. Поэтому не надо выбирать
произвольный eigensolver tolerance и переносить его на physical amplitude.

Для всех использованных elementary math values (`sin/cos` для LO фаз
и angular nodes, `exp(0),exp(-1),exp(-2),exp(-4)`) независимо проверить
local math evaluation against 256-bit correctly rounded MPFR interval
при **точном представленном Float64 аргументе**: error каждой scalar
component не больше одного Float64 ulp соседнего correctly rounded value.
`sqrt` на положительных normal numbers предполагает IEEE correct rounding.
Это отдельный воспроизводимый library arithmetic contract; отсутствующий
или failed certificate блокирует dependent channel. Оно не получает
`pass` по названию libm. Произвольный ulp запас не добавлять.

### 4.2. Propagation to each amplitude

Операции вне elementary math сертификатов имеют normal-range finite
значения. Консервативный верхний inventory для одного entry, включая
parameters/unit conversion, три z terms, три IFR interfaces и четыре
angular samples: SI scalar operations/known subtraction conditioning ≤128,
three envelope/phase products ≤192, three interface products/interpolation
≤288, four angle blocks/sums ≤256, scale division/output ≤128; всего ≤992
≤1024 real rounded operations. Complex multiplication учитывается как
6 real operations, complex addition как2. Известное худшее conditioning
band-jump subtraction равно9 для `2.5tau-2tau`; оно включено в SI allowance.
Если будущая реализация этого inventory не подтверждает — stop design,
не заменять bound произвольным `rtol`.

Далее все величины — dimensionless positive analytic bounds, не actual
kernel measurements. Они дают непосредственно исполнимый критерий:

```text
h = 2beta + beta²
eQ = g + (1+g)*(2h+3h²)/(13/21)
delta_ac = delta_alloy = (1+a)*(1+eQ)-1

bI = beta + 6g/(1-4g) + g*(1+beta)
hI = 2bI + bI²
eI = (2hI*(207/112) + hI²*(13/2))/(2329/3136)
dq = 128g
dx = dq/4 + 16g
delta_IFR = (1+a)*(1+eI)*exp(dx)*(1+2u)-1

eta_phase = (5pi/2)*(2g+g²) + 2sqrt(2)*u
eW = 3h*(1+g)+g
ferr = eW + (1+eW)*eta_phase + a*(1+eW)*(1+eta_phase)
eF2 = (2ferr+ferr²)/(169/441)
dD = dq + (pi²+1)*(2g+g²) + a
delta_LO = (1+a)*(1+g)*(1+eF2)/(1-dD)-1
```

Обоснования: `|abs(cg)²-vg²|<=h`; quartic sum error не больше `2h+3h²`.
Интерполяция между соседними узлами при `xint=1,2` имеет
`|theta-1/2|<=6g/(1-4g)`; IFR coefficients дают точно
`sum jump²*p=207/112`, `sum jump²=13/2`.
`dq` ограничивает абсолютный error `q²ell²` всех четырёх angles с
certified trig error и normed grid bounds; zero momentum pair не требует
relative division. `dx` ограничивает error Gaussian exponent при
`q²ell²<=16`; один ulp exp даёт relative ≤2u для положительного normal exp.
Для LO `|Fref|²` не меньше `169/441`; denominator ≥1, поэтому ни near-zero
denominator, ни subtractive cancellation сюда не входят.

Для scalar comparison `R>0`, где reference interval `[Rlo,Rhi]` относится
к `M[f]/K0_ref`, assert одновременно finiteness и

```text
real(Kactual) in [Rlo*(1-delta_s), Rhi*(1+delta_s)]
abs(imag(Kactual)) <= Rhi*delta_s
```

То же можно выразить componentwise complex absolute error с суммой
interval width + `delta_s*Rhi`; нельзя использовать норму самого actual K
в denominator. Positive angular average сохраняет max relative bound
слагаемых. Bound обязан удовлетворять `delta_s<1/8`; это только guard
различимости mutant, из приведённых machine-u выражений следует значительно
меньшая величина. Никакой новый научный threshold здесь не вводится.

Expected zero имеет отдельную ветвь: при valid IFR `Delta=0` или alloy
`x=0/1` exact zero получается из algebraic factors, assert exact zero.
Не делить на zero reference и не добавлять фиксированный SI atol,
который мог бы скрыть маленькую физическую амплитуду.

## 5. LO passport

**Exact API:** `lo_phonon_kernel(p::PhysicalParameters,s::ScaleSystem,
grids::ModelGrids,basis::BasisData) -> (K,FLO)`, selected kernels.jl:324.

**Question/assumptions.** Bulk-like Fröhlich interaction, dielectric constants
relative in p, independent 3D phonon normalization, fixed positive
`q_LO,s=1/ell`; temperature occupancies не входят в kernel. Их отдельный
thermal balance не служит absolute oracle. Primary B20 использует absolute
permittivities; `1/eps_abs_inf-1/eps_abs_s = (1/eps_inf-1/eps_s)/eps0`.

Planar states `A^-1/2 exp(ik.r) psi(z)` and phonon volume `A*Lz`:
`|g_Q|²=e² W/(2eps0*A*Lz)*(1/epsinf-1/epss)/Q²`.
Сумма `sum_qz -> Lz*integral dqz/(2π)` и площадь из radial measure удаляют
`A,Lz`; оставляют factor `e²W/(2eps0)` [J²m] и integral [m]. Owning
screened model сохраняет этот prefactor и явно заменяет denominator на
`q²+qz²+q_LO,s²`. Это declared model assumption, не независимое доказательство
screening physics.

**Independent geometry/form factor.** На каждой scale case physical
positions равны `ell*[1/2,3/2,5/2]`, probabilities `[1,4,16]/21`.
Прямое раскрытие roots of unity даёт:

```text
F(-pi/ell)=-13i/21; F(0)=1; F(+pi/ell)=13i/21
I(v)=ell/2 * [1/(v+1) + (169/441)/(v+1+pi²)] [m]
Plo=e²*(.05*e)/(32eps0) [J²m]
f_LO(v)=Plo*I(v) [J²m²]
Kbar_ref=M[f_LO]/K0_ref
```

`I` раскрывает **конкретные три trapezoidal qz nodes** и их weights,
не аналитический infinite-qz integral. Assert all FLO entries against
literal array with absolute envelope `ferr`; raw K против independent
`M[f_LO]`. Никакого actual FLO в RHS.

**Controls.** Все entries nonzero и positive. Multiply raw kernel by2
должно отвергаться той же absolute predicate; normalized shape и normalized
KMS при этом могут быть прежними. Отдельные wrong-operator scalars:
omitted `1/(2π)` даёт `2π*f_LO`; missing dielectric `eps0` меняет units
и amplitude; treating relative eps as absolute должен быть отвергнут.
Вариант `q_LO,s=2/ell` — отдельный valid case с literal replacements
`v+1→v+4`; это дополнительный sentinel declared screening dependence,
не scientific screening selection. `q_LO,s=0` **не** permitted constructor
input и не используется.

**Limits/decision.** Prefactor и finite discrete magnitude имеют полный
candidate passport. Infinite qz window, z quadrature, physical screening
model и phonon occupation balance требуют отдельных свидетельств.
Решение: **изменить** только proposed test; runtime ещё not_run.

## 6. IFR passport

**Exact API:** `interface_roughness_kernel(p,s,grids,basis) -> K`, selected
kernels.jl:201. Independent-interface Gaussian height covariance,
small-displacement first-order band-step vertex; cross-interface covariance
равна нулю как declared assumption.

Из step expansion `deltaV_j=-DeltaEc_j*eta_j(r)*delta(z-zj)` получается
vertex `D_j=DeltaEc_j*psi*(zj)*psi(zj)` [J/m]. При convention
`S(q)=integral d²R exp(-iq.R)<eta(R)eta(0)>` независимый Gaussian integral:

```text
C(R)=Delta² exp(-R²/Lambda²)
S(q)=Delta²*(sqrt(pi)*Lambda)²*exp(-q²Lambda²/4)
    =pi*Delta²*Lambda²*exp(-q²Lambda²/4) [m⁴]
K_SI=sum_j S(q)*|D_j|² [J²m²]
```

Fourier inverse factors `(2π)^-2` принадлежат momentum measure, не `S`.
Gaussian convention подтверждена primary Huang Eq8; exponential B8
Lee–Wacker не подставляется вместо неё. Band-step vertex не берётся из
well-width derivative Huang: он независимо выведен из самого step.

**Literal periodic interface/geometry calculation.** Имеются ровно
`zj=[0,ell,2ell]`; seam end `3ell` не добавляется.

```text
DeltaEc/tau = [3/2, 1/2, -2]
sqrt(ell)*psi_j = [1/sqrt(21), 3/(2sqrt(21)), 3/sqrt(21)]
D_j * ell/tau_J = [1/14, 3/56, -6/7]
sum_j |D_j|² = (tau_J²/ell²)*(2329/3136)
f_IFR(v)=pi*(1e-10)²*ell²*exp(-v/4)
         *tau_J²/ell²*(2329/3136)
Kbar_ref=M[f_IFR]/K0_ref
```

Seam ψ берётся справа как first-cell value — это **документированная
дискретная convention**, не утверждение, что continuum ψ(0)=ψ(ell/2).
Остальные два interface values получены scalar midpoint interpolation
между .5/1.5 и 1.5/2.5, соответственно. Nonconstant v делает ошибку
интерполяции обнаружимой. Endpoint/period seam учитывается один раз;
донорные края отсутствуют, каждый layer edge здесь physical band jump.

**Controls.** Global2 mutant; missing π; wrong Gaussian exponent `-v/2`
вместо `-v/4` меняет offdiagonal и второй diagonal; dropping seam удаляет
`16/3136`, doubling seam добавляет `16/3136` к2329/3136. Wrong nearest-cell
interpolation меняет retained `[3/56,-6/7]` amplitudes. Valid `Delta=0`
даёт exact-zero tensor. Все используют retained absolute RHS, а не
normalized agreement. Нулевая band jump не гарантирует whole-channel zero,
когда остальные два interfaces остаются nonzero.

**Limits/decision.** Discrete seam/interpolation и Gaussian absolute scale
проверяемы. Inter-interface correlations, continuum interpolation error и
small-height approximation на реальном интерфейсе этим не валидированы.
Решение: **изменить** только proposed test; runtime ещё not_run.

## 7. Acoustic passport

**Exact API:** `acoustic_kernel(p,s,grids,basis) -> K`, selected
kernels.jl:240. Longitudinal scalar deformation potential, bulk phonons,
elastic/equipartition approximation; никакого piezoelectric или transverse
coupling без дополнительной модели.

Независимый derivation: quantized longitudinal displacement и
`deltaV=Xi*div(u)` дают
`|g_Q|²=Xi²*hbar*Q/(2rho*V*v_s)`.
В elastic equipartition absorption и emission вместе дают
`2N_Q+1≈2kBT/(hbar*v_s*Q)`, поэтому
`|g_Q|²(2N_Q+1)≈Xi²*kBT/(rho*V*v_s²)`.
Factor2 двух процессов сокращает vertex1/2; двойной учёт этого factor2
изменил бы amplitude. Mixed-space integration `dqz/(2π)` даёт delta(z-z'),
а проекция — integral four envelopes; area normalization удаляется
последующей planar momentum measure. Это planar derivation, отдельно от
primary nanowire geometry; Eq20/Appendix подтверждает microscopic coefficient.

```text
Q4=sum_g ell*|psi_g|^4=(1+16+256)/(441*ell)=13/(21ell) [m^-1]
Cac=(4*e)²*kB*70/(4000*4000²) [J²m³]
f_ac(v)=Cac*13/(21ell) [J²m²], independent of v
Kbar_ref=fill(f_ac/K0_ref,2,2,1,1,1,1)
```

**Controls.** Global2 mutant; spurious single-emission factor1/2; added
spin degeneracy; missing `1/ell` all fail retained magnitude. Дополнительный
valid `T=35 K` case должен дать literal half-amplitude. Это algebraic
coefficient check; применение equipartition для конкретного spectrum при
35/70 K отдельно не доказано. `T=0` API отвергает и как test input не
используется. Отсутствующий zero-reference case для positive parameters
не заменяется выдуманным нулём.

**Limits/decision.** Полный candidate для уже объявленного elastic model;
inelastic thermalization и acoustic q-support applicability — вне вывода.
Решение: **изменить** только proposed test; runtime ещё not_run.

## 8. Alloy passport

**Exact API:** `alloy_kernel(p,s,grids,profiles::MaterialProfiles,basis) -> K`,
selected kernels.jl:280. Independent Bernoulli alloy sites in a virtual
crystal, short-range site potential, explicitly supplied contrast/volume;
no unannounced dielectric screening or empirical prefactor.

Вывод независимо от kernel implementation: пусть site occupation
`eta_j∈{0,1}`, `<eta>=x`, `<(eta_j-x)(eta_l-x)>=x(1-x)*delta_jl`,
`deltaV(r)=Omega*DeltaV*sum_j(eta_j-x)*delta³(r-rj)`.
Continuum site sum имеет density `1/Omega`; следовательно covariance
`<deltaV(r)deltaV(r')>=Omega*(DeltaV)²*x(1-x)*delta³(r-r')`.
Проекция planar states даёт four-envelope integral без дополнительных
spin или `2π` factors. Для zincblende conventional cube содержит четыре
independent substitutional cation sites, потому volume/site=`a³/4`, а не
`a³` или volume per individual atom=`a³/8`. Primary Huang Eq9 проверяет
эту volume convention; его screened transport factor здесь не переносится.

```text
x=1/4; x*(1-x)=3/16
Omega=3.125e-29 m³=(.5e-9)³/4
DeltaV=.6*e J, independent of layer band jumps
Qalloy=(3/16)*13/(21ell)=13/(112ell) [m^-1]
f_alloy(v)=Omega*(.6*e)²*13/(112ell) [J²m²]
Kbar_ref=fill(f_alloy/K0_ref,2,2,1,1,1,1)
```

**Controls.** Global2 mutant; using conventional `a³` volume gives factor4
and fails; using atomic `a³/8` gives factor1/2 and fails; replacing
`x(1-x)` byx gives factor4/3 and fails. Valid all-x0 or all-x1 variant,
constructed through new Layers/profiles with same geometry, даёт exact zero.
Both `DeltaV` and `Omega` missing (`nothing,nothing`) дают raw exact zero
по existing API contract, но это disabled-channel behavior, не positive
absolute oracle; one missing parameter must fail physical constructor.

**Limits/decision.** Model-level absolute disorder magnitude имеет полный
candidate. Значение alloy contrast для реального состава/материала и
корреляции site disorder не доказаны synthetic numbers. Решение:
**изменить** только proposed test; runtime ещё not_run.

## 9. Mutant distinction, reuse, implementation handoff

Каждый channel получает один healthy retained absolute predicate и
`accepts(2*Khealthy,retained_RHS)==false`. Это future negative-control
assertion над immutable RHS; оно не требует изменения production kernel.
Положительный `R` и `delta<1/8` доказывают заранее, что интервалы healthy
и doubled amplitudes не пересекаются. Дополнительно assert на таком mutant
`normalize(2K)==normalize(K)` как scalar algebra demonstrator, не научное
LO balance measurement. Общий multiplier сохраняет homogeneous normalized
KMS/balance identities, но не literal absolute covariance.

Reuse impurity anchor сохраняется дословно по области вывода:
`frozen_scientific_fixtures.jl`, testset “Frozen impurity occupation-weighted
contraction”, selected lines86–121: positive midpoint angles2048/4096,
literal reference `impurity_kernel(...;angular=:legacy_uniform)` и
независимая occupation contraction сравниваются с adaptive optimized result;
пороги `1e-5`/`5e-5` этого fixture не переносятся на четыре новых kernels.
Это независимость angular rule/contraction от optimized path, **не**
полная независимость microscopic impurity prefactor от reference kernel.
Anchor не переписывается и не закрывает LO/IFR/acoustic/alloy denominator.

Proposed single-file implementation sequence:

1. Include existing `test/support/common.jl`; own module name проверить на
   отсутствие collision. Зафиксировать input/constant provenance comments.
2. Construct checked p/n and two ScaleSystem cases; build grids/profiles/
   `:none` basis. Выполнить independent scalar geometry and residual/gap
   preconditions; no solve, no target kernels для их expected values.
3. Implement 256-bit interval literal references, elementary math
   certificates и приведённые analytic error envelopes; freeze values до
   raw calls. Никакого target output в RHS или denominator.
4. Call each of four raw APIs; compare every K entry and LO F, scale A/B
   отдельно; затем supplementary cross-scale relation.
5. Run named global-factor and per-channel negatives, exact-zero cases
   только внутри valid API. Existing rescaling/impurity tests — references,
   не запускаются автоматически этим single-file design.

Будущая команда owning DEV07 (не выполнена здесь):

```console
julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/physics/absolute_scattering_kernel_oracles.jl")'
```

Ей требуется отдельный конечный L-JL envelope/CP-CODE в уже разрешённом
implementation scope. Design review не является receipt выполнения команды.
При выявлении некорректной primary formula, geometry, rounding inventory
или library certificate блокируется только зависимый channel; scientific
model/threshold нельзя подстраивать для прохождения fixture.

## 10. Фактические проверки, стоимость и STOP

Выполнены read-only Git/source inspection, paper equation reading, SHA256
сохранённых primary PDF, ручной analytic derivation. Julia/Python target
imports, tests, parser, solve, profiling, benchmarks, builds и installation
**не выполнялись**. Ни один runtime или scientific gate не объявлен pass.

Первоначальный envelope source/design:60min,1CPU,2GiB,read5MiB,
output128KiB, no children. Parent расширил только engineering primary-source
read/storage до32MiB, max2 logical PDF retrievals,16MiB/file,60s each.
Первый sandbox Huang curl: exit6 DNS,HTTP000,0B; сохранён в identity.
Parent разрешил ровно один escalation fallback той же retrieval; он дал
exit0,HTTP200,301118B. Второй/последний logical retrieval Archetti дал
exit0,HTTP200,1641929B. TLSverification включён, redirects запрещены
(`max-redirs=0`), execute/scripts не применялись. Исходная ошибка не удалена.
Unique local literature bytes touched:514376+2685475+301118+1641929
=5142898 B; это не measured total I/O: hashes/extraction повторно читают
bytes, а hidden web transport total неизвестен. Companion identity содержит
отдельный logical PDF read exposure count; actual disk I/O не измерялся.
Размеры выбранных файлов и их bounded извлечений укладываются в32MiB;
это не утверждение об измеренном объёме всех OS reads. Corpus download
не выполнялся, PDFs не предназначены для Git.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| LO absolute screened-model finite-sum RHS задан независимо | B20–B23 original hash; literal F `[-13i/21,1,13i/21]`; positive qs и explicit finite qz sum; selected EQ-KLO | Screening physics, continuum qz/grid accuracy, runtime не приняты | изменить |
| IFR Gaussian absolute spectrum, seam и interpolation имеют direct RHS | Primary Eq8 convention; independent Fourier transform; jumps `[3/2,1/2,-2]tau`, literal `2329/3136` | Дискретный seam convention не continuum interface validation | изменить |
| Acoustic absolute factor2 установлен | Primary Eq20/Appendix hash; longitudinal-phonon quantization + two processes; literal quartic13/21 | Elastic/equipartition applicability реального spectrum и runtime неизвестны | изменить |
| Alloy site-volume/variance scale установлен | Primary Eq9 hash; независимый Bernoulli covariance derivation; `Omega=a³/4`, Qalloy13/112 | Synthetic DeltaV не material calibration, screening/correlations не валидированы | изменить |
| qK*K и impurity anchor сохраняются | Selected test blobs и явные области их независимости | Не подменяют четыре missing amplitudes | сохранить |
| Все четыре passports accepted, DEV07 tests pass или S1 scientifically accepted | Таких receipts нет | Нужны independent CP-DESIGN, implementation/targeted receipt и отдельные scientific gates | данных недостаточно |

**STOP:** этот D1 frozen для независимого review. Дальнейшая реализация,
новый runtime или scientific experiment этим отчётом не выполняются.
