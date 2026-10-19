# DEV07 I1 — независимый CP-CODE source review

2026-10-19. **PASS source/math для реализации absolute-amplitude oracle**,
с двумя ограниченными errata ниже. Runtime ещё не запускался этим reviewer;
library certificates и assertions остаются not_measured. S1 science,
continuum/device validation и общая four-index algebra при Nb>1 не приняты.

## Frozen source и фактически выполненная проверка

Worktree `/tmp/qcl-dev07-absolute-worktree`, branch
`codex/review-closure-absolute-kernel-oracles`, base/HEAD
`7324d98c0fccd61b4a1a2756b5cabe2fd0e0e49c`. Status содержит ровно changed docs
и новый test; recursive submodule status пуст. Git не менялся.

Фактически пересчитаны и совпали:

| Артефакт | SHA256 |
| --- | --- |
| `test/physics/absolute_scattering_kernel_oracles.jl` | `b85514cab4c32cb22acef0b0ecd66d070beb0ec6d44949d64a0ca20a171e96af` |
| `docs/src/development/review_oracle_contracts.md` | `4921ce15200998c6af15caf3a606664363bbcc50adc58fe9c37486c028e6cc24` |
| `/tmp/qcl-dev07-absolute-impl-patch.diff` | `561d2a3643ad95be37e50bb76dd9a86e388386e419ced4744427d387c67f7316` |

Сначала проверены test/diff и принятый D1 относительно owning code, затем
прочитаны author identity/report. Первичные формулы уже независимо проверены
в accepted D1 review `caea42e27026e6bee60d1f59988a4f1a927820c503f50b2c07f8a0803ba52687`;
нового network или повторного primary PDF чтения здесь не было. Production
paths не изменены. Прочитаны `test/support/common.jl`, `test/run_group.jl` и
exports: новое имя module отдельно, physics group автоматически обнаруживает
`.jl`, shared suite registration не меняется. Tracked diff и новый файл
прошли whitespace-only `git diff --check`/`--no-index --check`; это не parser.

## Faithfulness accepted D1

Все четыре independent expected coefficients в lines278–295 соответствуют
принятому D1: LO finite qz sum с `169/441`, IFR `2329/3136`, acoustic
`13/(21ell)` и alloy `13/(112ell)`. Raw tensor возвращается с shape
`(2,2,1,1,1,1)`, и проверяются все четыре radial entries. Каждая scale
`.1eV/10nm` и `.2eV/20nm` отдельно сравнивается с literal SI RHS/K0;
отношение16 проверяется только после абсолютных assertions.

`carrier_inputs` использует checked Layer/PhysicalParameters/
NumericalParameters и public builders. Нет unchecked positional
ModelGrids/MaterialProfiles/BasisData, post-builder mutation, NEGFProblem или
solver. Geometry/profile и basis chi защищены literal norm/residual/gap
certificate к независимой A. Дополнительный component-phase alignment
assertion является более сильным precondition, а не actual-product RHS.

Expected constants — decimal strings, rational geometry и interval pi.
Actual CODATA, scale readback, basis/F, `_scaled_physics`, `_K0`, raw kernels,
`build_kernels`, normalized tensors и reducers в expected не входят.
Scale/input readback используется только отдельными certificates. Local
library argument reconstruction использует actual grid/L0, чтобы сравнивать
libm именно на target Float64 аргументе; это не covariance oracle.

Глобальный factor2 отвергается для каждого entry и каждой scale тем же
retained positive predicate; normalize(2K)==normalize(K) остаётся отдельным
algebraic control. Дополнительные prefactor/eps0/2pi/Gaussian/seam/nearest-cell
negatives заданы. Valid screening2/ell, acoustic T35, IFR Delta0, alloy
x0/x1/disabled и constructor failures одного missing alloy parameter сохранены.
Existing impurity/exact rescaling не изменены и не объявляются independent
absolute microscopic oracle. Все пять S1 channels и scientific tolerances
остаются вне изменения.

## Interval arithmetic и library certificates

IV lines44–82 использует outward rounding **каждой primitive**. Сумма/разность
берут правильные endpoints, product — все четыре endpoint products;
reciprocal имеет запрет crossing zero; square отдельно учитывает crossing0;
sqrt/exp монотонны. Negation/sign и endpoint extrema точны. Это настоящее
enclosure, а не две глобальные оценки составной немонотонной функции.

`arithmetic_bounds` переносит D1 g/a/beta/ferr/delta без подбора tolerances.
Expected/channel formulas также вычисляются в IV. Scalar comparisons
используют reference bounds, без normalization на actual K. Positive-case
delta<1/8 отделяет factor2; exact zeros проверяются без SI atol.

`math_certificate` lines246–275 задаёт MPFR down/up enclosure на exact
represented Float64 argument, требует совпадения rounded endpoints и
ограничивает target component одним adjacent Float64 spacing. Проверяются
actual angular cos, real/imag complex LO exp и все actual Gaussian exponent
arguments; qz*x grouping даёт тот же scalar phase, что complex target path.
Extra canonical exp points не заменяют actual-argument checks. Выбор меньшего
из двух соседних spacings консервативен. Correctly-rounded sqrt/normal finite
Float64 arithmetic остаются явными предпосылками, не измеренным результатом.

Julia `@test` сохраняет failed preconditions в общем failed testset, хотя
может продолжить последующие assertions. В runtime receipt при любом failed
certificate нельзя отдельно повышать dependent amplitude до accepted PASS.
Код не ловит такой failure с расширением delta и не подменяет RHS actual basis.

## Inventory: независимый потолок и мелкое уточнение

Универсальный `gamma(1024)` имеет достаточный запас. Независимый заведомо
консервативный счёт по исходному kernel, в real rounded operations на entry:

| Канал | Независимый ceiling | Разложение |
| --- | --- | --- |
| LO | 744 | SI128 +9 envelope/phase terms×24 +4 angles×(q12 +3 qz blocks×24 +scale12) +accumulation16 |
| IFR | 544 | SI128 +3 interfaces×32 +4 angles×(q12 +spectrum16 +3 vertex contractions×12 +scale12) +accumulation16 |
| acoustic | 268 | SI128 +3 quartic terms×32 +prefactor16 +scale12 +extra accumulation16 |
| alloy | 280 | SI128 +3 variance/quartic terms×36 +prefactor16 +scale12 +extra accumulation16 |

SI128 — принятый D1 allowance для canonical conversions/literal inputs и
conditioned jumps; grid/basis errors отдельно ограничены certificates.
Complex multiply6/add2 и real×complex2 учтены. Например LO qz block имеет
три squares, два adds, четыре factor operations, complex products/accumulation
10: всего19<24. LO envelope term ≤24 включает phase argument, три products и
complex accumulation. Все новые ceilings <992<1024; никакой смены tolerance
или gamma_n не нужно. Это статическое считывание, не профилирование.

**E1 — accounting erratum, low, nonblocking для functional source.**
Test comments lines28–32 называют LO denominator4 и total584 точными
conservative source ceilings. Буквальный `qbar^2+qz[h]^2+qscreen^2` содержит
5 operations. Можно либо явно отнести qscreen² в SI allowance/предполагаемое
повторное использование, либо считать5 в каждом блоке (584→596 до других
перегруппировок). Universal1024 не нарушен, но 584 как отдельный доказанный
ceiling без такого пояснения не следует из описанного accounting. Дешёвое
решение — поправить source comment, author identity/report inventory и
соответствующий docs текст, не меняя исполняемых assertions или tolerance.
Первоначальный I1 freeze сохранить. Independent ceiling744 выше устраняет
неопределённость именно для source acceptance универсального бюджета.

## Provenance erratum

**E2 — root identity, nonblocking для owning math, требуется перед publication
как fresh context.** I1 identity содержит `frozen_at_utc=2026-10-19T18:20:02Z`
и `root_head_observed=9d8cf0c...` без timestamp отдельного root наблюдения.
Фактически прочитанный reviewer root HEAD:
`cfc38e1761f24caf436d938f378dbcdbf71a28f0`, commit time
`2026-10-19T21:15:49+03:00` (=18:15:49Z), selected Core gitlink ровно7324d98.
9d8cf — корректный historical D1 source context; из I1 identity нельзя
выводить, что это fresh root readback на момент freeze18:20. Невозможно
восстановить время старого авторского наблюдения по одному этому полю.

Дешёвое решение: сохранить original I1 identity/report/patch и добавить
отдельный erratum с historical label для9d8cf, actual cfc38e1 + readback time,
same Core7324 и unchanged file hashes. Не переписывать raw history и не
делать из исправления метаданных новый runtime/scientific receipt.

## Решение

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Четыре amplitude tests faithfully реализуют D1 | Frozen source hash, independent expected formulas, checked carrier, two scales/full radial table | Source-only, Nb1 | сохранить |
| Reference endpoints являются outward enclosures | Прочитанные IV primitives и directed MPFR use | Julia исполнение ещё not_run | сохранить |
| Universal1024 достаточен | Независимые ceilings744/544/268/280 | 584 accounting comment требует E1 уточнения | изменить |
| Owning source верен, root context нуждается в historical label | Actual7324, same gitlink на cfc38e1, I1 identity9d8cf | Старое время root readback неизвестно | изменить |
| Certificate/assertion/runtime pass установлен | Свидетельств исполнения нет | Отдельный bounded DEV07 L-JL | дополнительно измерить |
| S1 science/model acceptance установлен | Таких данных нет | Fixture не solver/device validation | данных недостаточно |

**STOP.** Source/math PASS относится к указанным байтам и универсальному
arithmetic bound. E1/E2 — ограниченные отчётные исправления; functional
production/test-model defect не найден. Reviewer не исполнял imports,
parsers/tests/Julia, solver/build/network/server tooling, не менял Git/source,
не создавал детей. Raw C08/SCI05 и DEV07 runtime attempt counter не затронуты.
