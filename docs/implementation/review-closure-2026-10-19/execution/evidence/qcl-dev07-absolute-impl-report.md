# DEV07 O08-05 — source implementation I1

Дата: 2026-10-19. Этап: **изменение source без исполнения target-кода**.
Кандидат frozen в `/tmp/qcl-dev07-absolute-worktree`, branch
`codex/review-closure-absolute-kernel-oracles`, base Core
`7324d98c0fccd61b4a1a2756b5cabe2fd0e0e49c`. Независимый CP-CODE и targeted
runtime отсутствуют; implementation PASS и scientific PASS не заявляются.

Пакет: `/tmp/qcl-dev07-absolute-impl-identity.json`,
`/tmp/qcl-dev07-absolute-impl-patch.diff`. Хеши source и patch — в identity.
Принятый D1 и независимый CP-DESIGN пересчитаны и совпали с поручением.
Позднее уточнение координатора подтвердило accepted owning path
`test/physics/absolute_scattering_kernel_oracles.jl`; слово numerics в brief
не означало изменения accepted path. Existing physics group обнаруживает
файл автоматически; registration/runner не менялись.

## Реализованный контракт

Новый отдельный module сохраняет existing suites и production source.
Checked Layer/PhysicalParameters/NumericalParameters и публичные builders
создают Nb1 manufactured geometry: три cells ell=1e-8m, central A spectrum
[2,7/2,11/2], exact eigenvector [1,2,4]/sqrt21. Expected carrier не подменён
прочитанным target Hamiltonian. Нормировка, literal eigen residual и phase
alignment с eigenvector проверяются независимыми interval operations.

Для LO/IFR/acoustic/alloy каждый full radial2×2 entry проверяется отдельно
по absolute covariance RHS и literal K0 при обеих scales .1eV/10nm и
.2eV/20nm. LO F проверяется против literal [-13i/21,1,13i/21]. Expected
использует decimal-string SI constants, rational geometry и finite sums;
не использует actual F, CODATA, target scale readback, _scaled_physics, _K0,
reducers или product qK*Khat.

Написаны global2 negatives для каждого entry, normalized-shape algebraic
control, отдельные prefactor/dielectric/2pi/IFR Gaussian/seam/nearest-cell
mutants, positive screening2/ell и acoustic T35 sentinels, exact-zero IFR
height0 и alloy x0/x1/disabled cases, constructor rejection одного missing
alloy параметра. Existing impurity midpoint anchor и exact rescaling
сохранены. Nb1 scope не проверяет общую four-index orientation/adjoints.

## Арифметические предпосылки и inventory

Все reference endpoints вычисляются при 256 bits с **per-operation**
направленным округлением: +/- используют соответствующие endpoints,
умножение — четыре пары, reciprocal требует interval без нуля, sq учитывает
crossing0, sqrt/exp используют monotonicity. Это не два global-rounding
вычисления составной немонотонной функции. Literal decimal constants не
проходят через Float64 до построения RHS interval. Отдельные input/unit
certificates проверяют относительную ошибку нормированных SI inputs;
нулевые inputs проверяются точно. Grid/profile scalars используют D1 g.

u=2^-53, g=gamma32, a=gamma1024; beta/ferr/delta перенесены из D1 §4 без
подбора epsilon. IEEE Float64 normal arithmetic и correctly rounded sqrt
являются предпосылками. Остальные elementary functions должны пройти
написанные MPFR sin/cos/exp certificates на точных представленных Float64
аргументах, включая scalar components фактического complex LO exp.
Library certificates ещё **не измерены**. На runtime failure нельзя
увеличивать delta или подставлять actual basis/F в RHS.

Source-local real-op inventory (complex multiply6, add2) дан в test lines:
SI/conversions allowance128; LO162 envelope operations +4*(9 q +54 qz
contraction +8 scaling)+10 averaging =584; IFR72 interfaces +4*(9 q +10
spectrum +30 interface contractions +4 scaling)+10 averaging +128 =422;
acoustic128+72+8+8=216; alloy128+84+4+8=224. Это conservative static ceilings,
а не profiling receipt. SI128 раскрыт на literal roundings16, conversions32,
conditioned material energy/contrast32 (condition9), prefactor32 и
conversion factors16. Все <1024; shared eigensolver не включается фиктивно
в этот count — он защищён отдельным literal residual/gap certificate.
Принятый universal ceiling D1 992 сохранён. Reviewer должен независимо
проверить counts и arithmetic propagation до runtime.

## Фактически выполненные проверки и границы

Прочитаны AGENTS/architecture/entrypoint/DEV02/DEV07, Core CONTRIBUTING,
qcl-physics-audit и памятка; owning kernels/grids/basis/scaling/types/constants,
existing rescaling test и auto-discovery. Выполнены Git HEAD/status/submodules,
создание изолированного worktree через разрешённую escalation, manual source
readback, SHA256, tracked `git diff --check` и whitespace check нового файла
через `git diff --no-index --check`. Оба whitespace checks прошли.

Julia, imports, parser, tests, solver, builds, setup, network, server, Git
stage/commit/push не выполнялись. Runtime DEV07 L-JL consumed0; дальнейшее
исполнение принадлежит координатору в его отдельном envelope. Прямых детей0.
Исходный protected checkout и shared SCI05 C08 не менялись. Root dirty
EXEC work лишь прочитана; Core source checkout до worktree был clean.

Wall/CPU/RAM/read/output caps поручения не расширялись. Exact OS I/O и
суммарный отображённый output не измерялись; повторные ограниченные source
reads были. Нельзя выдавать отсутствие instrumentation за measured budget
receipt. Данных производительности этот source-only этап не создаёт.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Четыре raw amplitude oracle написаны независимо от target amplitudes | Frozen test hash, D1 scalar finite RHS, two scale cases | Нет runtime verdict; Nb1 только | изменить |
| Outward interval и represented-argument MPFR certificates заданы | IV primitives и library_certificates source | Реальное выполнение не измерено | дополнительно измерить |
| Static operation ceilings укладываются в gamma1024 | 584/422/216/224 и раскрытый inventory | Требуется independent CP-CODE; не profiler | сохранить |
| Production/model/scientific tolerances сохранены | Только new test и appended docs subsection | Source review не scientific validation | сохранить |
| Test/runtime/science acceptance пройдены | Таких receipts нет | Отдельные gates | данных недостаточно |

**STOP:** source frozen для независимого review. Автор не исполняет Julia
и не публикует/не переносит diff в общий Core checkout.
