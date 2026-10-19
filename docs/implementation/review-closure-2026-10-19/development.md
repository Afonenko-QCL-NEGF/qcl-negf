# Закрытие software findings: план DEV01–DEV25

> **Для будущего исполнителя:** выполнять карточки по одной через
> `superpowers:subagent-driven-development` либо `superpowers:executing-plans`.
> Сейчас разрешено только составление этого плана. Ни одна команда ниже не
> выполнялась при его подготовке и ни один grant этим файлом не активируется.

**Цель:** закрыть адресные software findings RV02–09, RV11–12, RV14–15 и
RV19 с воспроизводимыми source/fixture receipts, сохранив физическую задачу,
сырые данные, exact-attempt identity и независимость научных oracle.

**Архитектура:** формулы и in-memory проверки остаются в Core; файлы,
checkpoint и конфигурационный provenance — в Runner; wire formats — в
Contracts; выбор AiiDA child — в AiiDA; HTTP, временный export и browser
client — в Portal; независимое чтение — в Results. Общий owner и native
lifecycle Platform планируются в [platform-worker.md](platform-worker.md).

**Стек:** Julia с root `julia/Project.toml`/`Manifest.toml`; Python
`>=3.14,<3.15` и единственный root `uv.lock`; Portal Node.js 24 и
`frontend/package-lock.json`. Runtime/build/import identity проверяется
отдельно от совпадения package version.

**Spec:** [master handoff](../review-closure-2026-10-19.md),
[implemented architecture](../../architecture.md), owning component sources
и архивная кампания `2026-10-14-e48e5b2-01`. Архивные ссылки ниже обозначены
`A/RVxx.md` и `A/fixes/...`: `A` — опубликованный repository-relative каталог
`docs/implementation/comprehensive-review/2026-10-14-e48e5b2-01/`.
Original bytes/hashes и historical path map — в его `PORTABILITY.md` и
`publication-receipt.json`; путь компьютера автора не нужен.
Архив source-only; его выводы не являются runtime pass.

## Срез, права и правила карточек

Срез чтения: root `93880c23bca889ddcb8b98edb995080b332dd99f`, восемь
gitlinks соответствуют selected checkouts. Component worktrees были чистыми;
root содержал создаваемый master plan. Проверены `git rev-parse HEAD`,
`git status --short`, `git submodule status --recursive`. Локаторы текущего
Core `3108150…`, Runner `0c53c6d…`, AiiDA `53e2a205…`, Contracts `e5c056c…`,
Portal `36837e9…`, Results `fe27a2a…` служат привязкой наблюдения; состав
релиза каждый раз выводится из Git, отдельный maintained lock не создаётся.

Пятнадцать ошибочно подготовленных ранее candidate files восстановлены.
Остаточные draft patch/tmp не являются принятым кодом, тестом или evidence.
Будущий исполнитель начинает с pristine selected source и повторно сверяет
finding; не переносит ту попытку как «готовую реализацию».

В карточках `C/`, `R/`, `Aii/`, `K/`, `P/`, `B/` означают соответственно
`components/QCLNEGF.jl/`, `components/QCLNEGFRunner.jl/`,
`components/qcl-negf-aiida/`, `components/qcl-negf-contracts/`,
`components/qcl-negf-portal/`, `components/qcl-negf-results/`. Это точные
префиксы permitted paths, а не разрешение менять весь компонент.
`D ultra`, `I medium`, `R high` — отдельные роли с усилием Sol по canonical
policy roadmap. При смене характера работы выделяется следующая карточка.
Не менять модель самостоятельно и не выбирать другой model вследствие
этого плана. После будущего DEV grant D author может завершать локальный
контракт, I — готовую реализацию, R — независимую проверку без обращения к
оператору на каждом шаге.

Общие права, checkpoints и операторские gates определяют master и
[autonomy.md](autonomy.md): `PLAN`, `DEV`, `PUBLISH`, `READ_NATIVE`, `BUILD`,
`OPS`, `SCI`; `CP-DESIGN`, `CP-CODE`, `CP-NATIVE`, `CP-RELEASE` — technical
checkpoints. CP-START/CP-EXCEPTION остаются human gates; approved B/G1/S1 из
[P1](operator-permissions.md) дают CP-OPS/CP-SCI policy approval заранее, с
technical BIND/READY перед действием. G1 merge — отдельное право MERGE_G1.
Сейчас active только PLAN; прочие права **approved_standby**, не EXEC.
Здесь **DEV нужен даже для локальной реализации готовой карточки**;
`source-only` не означает DEV grant. `PUBLISH` нужен для remote push/PR и
root gitlink publication; локальное существование candidate не означает
опубликованный source. READ_NATIVE/BUILD/OPS/SCI не следуют из DEV. Дизайн проходит
CP-DESIGN у независимого reviewer; инвариантно совместимый выбранный
контракт не требует operator approval. Новый physical contract,
деструктивная migration, неизвестный remote outcome или необходимый новый
grant возвращается координатору, не превращается в автономный эксперимент.

Для каждой карточки обязательны immutable input refs, diff/receipt hashes,
фактическая команда, cwd/runtime/import ownership, exit status и размер
вывода, отдельные assertions, исходный failed log и ограничения. Reviewer
получает вопрос, предпосылки и первичные артефакты до диагноза автора.
Receipts оформляются в owning PR или выбранном evidence каталоге root;
сырые scientific arrays, depots, secrets/private inventory туда не попадают.
Согласие двух агентов не заменяет assertions и native measurements.

## Общие ограничения и будущие проверки

- Полностью сохраняются model/SCBA/Poisson, scattering, basis/grid/window,
  tolerances и критерии scientific acceptance. Oracle correction — отдельный
  вопрос от изменения production operator. Дефект физического контракта
  останавливает эту карточку и передаётся научному owner.
- Используются сохранённые frozen plan/model/run/attempt и raw arrays;
  execution, convergence, physics, discretization, experiment имеют отдельные
  статусы. `not_measured`, missing dependency и unknown outcome не равны pass.
- Ни один unit fixture ниже не вызывает новый SCBA/Poisson solve. Использовать
  direct operator/final-audit calls над малыми manufactured states. Если
  existing fixture выполняет больше, чем разрешённый envelope, выделить
  минимальный проверяемый slice до запуска либо запросить иной grant.
- Missing Python 3.14, Julia/depot или locked dependency — blocker execution,
  а не повод использовать Python 3.11, неявный `uv sync`, `Pkg.instantiate`,
  network install, sys.modules stubs или fake package как proof owning import.
  Моки backend допустимы как явно synthetic fault oracle; они не доказывают
  настоящий AiiDA import/runtime, TLS, Slurm, NFS или power-loss durability.
- Все web changes сохраняют фиксированную светлую тему, `color-scheme: light`,
  контраст и безопасное отображение текста; UI не получает scientific formula
  или право менять scientific assessment.
- Готовые existing anchors переиспользуются. Предлагаемые новые имена ниже
  помечены **proposed**; существование test name проверено чтением/`rg`,
  исполнение не выполнялось. Полный test catalogue и coverage не заявляются.
- Prefix `QPY` ниже означает команду из root:
  `uv run --locked --no-sync --package PACKAGE python -m pytest ...`.
  Она не устанавливает окружение. Перед ней проверяется Python 3.14 выбранной
  среды; при несовпадении остановить runtime часть. В командах карточек
  PACKAGE раскрыт полностью. Для Julia working directory также root, include
  содержит полный workspace-relative path; existing support/common импортирует
  owning package из selected root Manifest. Установку/подготовку среды отдельно
  планирует native owner.

Предлагаемые **будущие** envelopes, действующие лишь если их включает DEV
grant: `L-SOURCE` — один source/design packet до 30 min, максимум два review
раунда, без imports/builds/tests; `L-PY` — до четырёх targeted invocations,
каждый до 90 s, 1 CPU/1 GiB, суммарно до 6 min, 16 MiB temporary/2 MiB logs;
`L-JL` — до двух invocations, каждый до 120 s, 1 CPU/2 GiB, суммарно до
4 min, 16 MiB temporary/2 MiB logs. Один общий test slot на всех агентов;
суммарный разрешённый бюджет master/grant всегда сильнее суммы карточек.
Первая неуспешная попытка сохраняется. Повторная invocation допустима после
конкретного изменения или для другого различающего assertion в пределах общего
числа вызовов карточки: максимум четыре L-PY либо два L-JL, включая red/green и
corrections. Review rounds подчиняются autonomy; они не обнуляют этот счётчик.
Превышение лимита,
неподготовленное окружение или необходимость compilation/build за envelope
останавливают runtime проверку, а не запускают скрытый bootstrap.
`timeout --signal=TERM --kill-after=5s 90s` (`120s` для Julia) и доступный
лимит памяти применяет будущий test runner; числа здесь — стоимость проверки,
не scientific tolerances. Полные suites/final CI не входят в эти команды.

## Карта зависимостей и закрытия

| Поток | Очерёдность | Независимый результат |
| --- | --- | --- |
| Core docs | DEV01 | D08-01/02/03 без изменения numerical code |
| Scientific distinctions | DEV02 → DEV03–08 | Шесть property passports и differentiating fixtures, вход научному плану |
| Composite export | DEV09 → DEV10 → DEV11 | Frozen exact child от selection до cache/bytes/status |
| Actor | DEV12 → DEV13 | Bounded caller response, truthful unknown/close semantics |
| Schema/provenance | DEV14 → DEV15 → DEV16 | Canonical descriptions, published copy/provenance и drift rejection |
| Checkpoint | DEV17 → DEV18 | Явная generic durability scope, independent fault reader |
| Package identity | DEV19 → DEV20; DEV21 → DEV22 | Asset source binding, continued PR6, route-specific import evidence |
| Runtime safety | DEV23 и DEV24 | Retry/cancel semantics и public rejection boundaries |
| Software gate | Всё → DEV25 | Same-source closure, остаток native/science отдельно |

RV00/RV01 и RV10: requirements/passport/scientific wave — master/science
планы; DEV02–08 предоставляют oracle readiness, не объявляют scientific
acceptance. RV03/04: owners/edges и expert API effects сохраняются;
адресные API изменения отражаются в DEV09/12/15/17/19, массовый refactor и
dynamic graph не следуют из review. RV06 и Platform часть RV12/RV15 — OPS
план; DEV не пишет `components/qcl-negf-platform/**`. RV13 restore — OPS.
RV16, RV17 SI01–07, RV18 и общий RV19 docs pilot — отдельный documentation
план; DEV14–16 ограничены owning descriptions/schema boundary. Уже вошедшие
CR05 и single-file CR01 повторно не внедряются.

## DEV01 — Core D08: три authored theory corrections

**Owner / evidence / coverage:** Core; `A/fixes/RV08-doc-and-oracle-handoff.md`,
`A/RV08.md` J2, basis R02 и production-seed passage;
D08-01/02/03, RV08/RV16. **Роль:** D ultra.
**Depends:** актуальный Core gitlink; не зависит от runtime и научных данных.
**Permitted paths:** `C/docs/src/theory/11_observables.md`,
`C/docs/src/theory/19_production.md`, `C/docs/src/theory/05_basis.md`.
**Excluded:** весь `C/src/**`, test/schema/model/acceptance, generated HTML.

**Inputs / interface:** `observables.jl::energy_resolved_current` и
`bond_current`, `optimized/seed.jl::_seed_green_production`,
`reference/basis.jl::build_localized_basis`; theory anchors EQ-CURRENT-001/002.
Выход — owning prose и формула, scientific implementation API не меняется.

- [ ] Сверить energy-current measure с actual `g_s/(2π)` в коде и общей
  `dE/(2π)` convention; внести недостающий factor в EQ-CURRENT-002, сохранить
  units, знак заряда и связь resolved/integrated current.
- [ ] Описать root-search seed без unilateral rescale после bisection;
  не обещать post-root normalization и не менять Pauli policy.
- [ ] Перечислить accepted `pzp`, `none`, `real_space`; явно указать rejection
  `legacy_pzp`, не добавляя compatibility alias в код.
- [ ] Positive: formula и prose согласуются с exact source; negative:
  читатель не может вывести rescale, accepted legacy alias или другую меру.
  Existing anchors: `full_window_basis_preserves_the_spectral_subspace.jl`
  содержит `legacy_pzp` ArgumentError; `production_seed_chemical_potential_trials_are_scalar.jl`
  сохраняется. Численные тесты в этой docs-only карточке не нужны.

**Будущая команда:** `git -C components/QCLNEGF.jl diff --check`;
`rg -n 'EQ-CURRENT-002|legacy_pzp|rescal|normaliz' components/QCLNEGF.jl/docs/src/theory/11_observables.md components/QCLNEGF.jl/docs/src/theory/05_basis.md components/QCLNEGF.jl/docs/src/theory/19_production.md`.
**Receipt / stop:** reviewed three-file diff и таблица source→sentence;
L-SOURCE, CP-DESIGN + docs CP-CODE, без operator при этих инвариантах.
Если обнаружена numerical/formula ambiguity — остановить только спорную
коррекцию, передать DEV02; не менять solver ради совпадения с docs.

## DEV02 — Контракт шести независимых oracle перед fixture implementation

**Owner / evidence / coverage:** Core, научный reviewer; `A/RV08.md`,
`A/RV09.md`, `A/fixes/RV09-oracle-gaps.md`; O08-01…06/RV09 T01–04.
**Роль:** D ultra. **Depends:** immutable Core, theory docs DEV01 как candidate.
**Permitted paths:** **proposed** `C/docs/src/development/review_oracle_contracts.md`.
Это новый authored документ; существование `docs/src/development/` не
предполагается. Подключение к generated navigation — отдельный docs packet.
**Excluded:** production code/test edits, solver, tolerance/model changes.

**Inputs / interface:** produces six passports `O08-01`…`O08-06`: exact
operator/signature, input shape/units, applicability, independent RHS source,
norm/weights/near-zero behavior, tolerance basis, healthy control и deliberate
wrong-operator distinction. Proposed file — самостоятельный output, не runtime.

- [ ] Зафиксировать Keldysh literal noncommuting 2×2 expected matrix;
  wrong sign/adjoint/common multiplier должен нарушать direct assertion.
- [ ] Для Poisson переиспользовать analytic sine RHS Nz32/64/128 из
  `independent_nonlinear_and_continuum_anchors.jl`, отдельно определить fixed
  nonneutral source и expected assessment failure, не solver throw.
- [ ] Для final-state выбрать direct final assembly/audit вызов, где U/G
  одной candidate согласованы, и wrong-U либо stale-G variant различимы;
  existing scalar root/maxiter/fresh residual не объявлять full-state test.
- [ ] Для current определить nonzero wE/wk integral с SI scale и отдельную
  two-state coherence/truncated-basis reconstruction, не universal uniform J.
- [ ] Для LO/IFR/acoustic/alloy выписать absolute prefactor из owning equations
  и primary references с geometry/units; independent RHS не вызывает target
  kernel, `_scaled_physics` или normalized qK×K как собственный oracle.
- [ ] Для PV разделить omitted-diagonal direct sum, FFT implementation той же
  дискретизации и analytic product integration; continuum refinement получает
  свой finite window/tail error и не наследует pass product integration.
- [ ] Для каждого свойства указать существующий anchor и ровно недостающую
  assertion, derives tolerance из roundoff/refinement/equation policy;
  не придумывать численный threshold. При отсутствии derivation статус
  `design_blocked`, а соответствующий I ticket не READY.

**Будущие команды:** `rg -n 'keldysh_green|validate_solution|_validate_solution_metrics|bond_current|direct_hilbert_transform|lo_phonon_kernel|acoustic_kernel|alloy_kernel' components/QCLNEGF.jl/src`;
`git -C components/QCLNEGF.jl diff --check`.
**Receipt / stop:** six complete passports + oracle dependency graph и blind
CP-DESIGN. L-SOURCE; максимум два design rounds. Неразрешённый physical
contract выделяется owner, остальные паспорта продолжаются; никакой SCI grant.

## DEV03 — O08-01: direct noncommuting Keldysh assertion

**Owner / evidence / coverage:** Core; DEV02 O08-01, RV08 K/RV09 T01.3.
**Роль:** I medium. **Depends:** accepted passport O08-01.
**Permitted paths:** **proposed** `C/test/numerics/keldysh_literal_matrix_oracle.jl`;
`C/src/numerics/reference/greens.jl` только если regression доказывает локальный
эквивалентный bugfix; новый physical behavior требует нового D ticket.
**Excluded:** production model/solver, общие test helper rewrites.

**Interface:** existing `keldysh_green(Gᴿ::AbstractArray{<:Number,4}, Σˡ::AbstractArray{<:Number,4})`;
proposed testset `Literal noncommuting Keldysh product`.

- [ ] Ввести small complex 2×2 Gᴿ и anti-Hermitian Σ<, обеспечить
  noncommutativity; literal expected entries считать вне tested helper.
- [ ] Проверить public API на literal matrix, anti-Hermiticity и applicable
  PSD sign по принятой `-iG<` convention. Нулевой downstream current не oracle.
- [ ] Negative inputs/operator variants из паспорта должны давать отличную
  matrix/assertion: reversed order, missing adjoint, wrong multiplier/sign.
  Не менять expected RHS вместе с deliberate mutation.
- [ ] Сохранить existing `analytic_equilibrium_sum_rule_lo_balance_and_zero_current_anchors.jl`;
  не копировать его как второй zero-current test.

**Будущая команда:** `julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/numerics/keldysh_literal_matrix_oracle.jl")'`.
**Receipt / stop:** direct expected/actual matrix assertions и negative
distinction, L-JL; CP-CODE на том же source. Необходимость large solve либо
необоснованный tolerance → replan; accepted local contract исполняется по DEV.

## DEV04 — O08-02: incompatible Poisson source fails assessment

**Owner / evidence / coverage:** Core; RV08 P, RV09 T03; DEV02 O08-02.
**Роль:** I medium. **Depends:** accepted O08-02 passport.
**Permitted paths:** `C/test/numerics/independent_nonlinear_and_continuum_anchors.jl`,
**proposed** `C/test/physics/nonneutral_periodic_poisson_assessment.jl`.
**Excluded:** Poisson stencil/source subtraction, acceptance thresholds и grids.
**Interface:** `solve_periodic_poisson`; direct
`QCLNEGF._validate_solution_metrics` как existing assessment seam, точные
arguments копировать из selected implementation, не предполагать scalar API.

- [ ] Сохранить existing independent sine derivative RHS и existing ratios;
  не использовать `build_poisson_matrix * expected_U` как continuum oracle.
- [ ] Создать constant nonzero mean charge в fixed periodic fixture;
  проверить gauge и сохраняемые ζ/r_neutral/r_P diagnostics согласно паспорту.
- [ ] Передать actual metrics в existing assessment; проверить
  `ConvergenceReport.passed == false` на relevant declared limits, healthy
  compatible case имеет соответствующие passing gates.
- [ ] Negative: forced removal of mean charge или dropped neutrality gate
  должна нарушить independent expected diagnostic/assertion, не требовать throw.

**Будущие команды:** `julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/physics/nonneutral_periodic_poisson_assessment.jl")'`;
second invocation, если бюджет допускает: `julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/numerics/independent_nonlinear_and_continuum_anchors.jl")'`.
**Receipt / stop:** metric→criterion table с units/normalization/near-zero;
L-JL, CP-CODE. Если existing anchor cost выше лимита, не запускать его скрыто:
сохранить source reuse, запросить bounded runtime stage отдельно.

## DEV05 — O08-03: final state U/G freshness

**Owner / evidence / coverage:** Core; RV08 S, RV09 T02; DEV02 O08-03.
**Роль:** I medium. **Depends:** approved direct final-state seam/passport.
**Permitted paths:** **proposed** `C/test/numerics/final_state_alignment_oracle.jl`;
`C/test/numerics/fresh_candidate_residual.jl` лишь для общего control без дубля.
**Excluded:** solver loops/mixers, retries, criteria weakening, нового solve нет.
**Interface:** existing `fresh_fixed_point_metrics(problem::NEGFProblem,
scba::SCBAResult, U::AbstractVector{<:Real}, candidate::FixedPointAuditCandidate)`
в `reference/final_audit.jl` и `_validate_solution_metrics(solution::NEGFSolution,
metrics; accept_approximate_scba=false)` в `validation.jl`.
DEV02 выбирает complete fixture assembly и не подменяет её arbitrary partial
state. Proposed testset `Final state U G alignment`.

- [ ] Собрать самый малый complete manufactured state с independent literal
  Dyson/Poisson relation; inventory обязательных fields не заменять unrelated zeros.
- [ ] Проверить aligned U/G final audit; затем сохранить U и подать stale G,
  либо изменить U при retained G — designated fresh residual/gate fails.
- [ ] Убедиться, что stored small Σ-step/residual сам не маскирует final failure;
  oldΣ/predicted-U подмена не может пройти fixed expected oracle.
- [ ] Переиспользовать existing fresh pole literal oracle и existing causal
  quadratic root/maxiter-negative, явно ограничить их primitive scope.

**Будущие команды:** `julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/numerics/final_state_alignment_oracle.jl")'`;
`julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/numerics/fresh_candidate_residual.jl")'`.
**Receipt / stop:** field-level state passport и gate assertions, L-JL;
CP-CODE. Нет complete direct seam без полноценного SCBA — вернуть DEV02,
не объявлять synthetic primitive доказательством полной assembly.

## DEV06 — O08-04: nonzero public current и basis coherence

**Owner / evidence / coverage:** Core; RV08 J, RV09 T01/T05; DEV01/02.
**Роль:** I medium. **Depends:** O08-04 accepted measure/unit passport.
**Permitted paths:** **proposed** `C/test/physics/nonzero_public_current_oracle.jl`;
`C/test/physics/cavity_current_and_spectral_oracles.jl` только existing control.
**Excluded:** навязывание constant local J, boundary/bias symmetry, model changes.
**Interface:** existing `energy_resolved_current`, `bond_current(problem, Gˡ)`;
proposed testset `Nonzero current measure and basis coherence`.

- [ ] Small literal offdiagonal G< с ненулевым signed current, неодинаковыми
  wE/wk и explicit scale; API result сравнить с независимой component sum.
- [ ] Проверить отдельно resolved и integrated current, factor 2π и SI output;
  omission/change sign/weight должен отличаться при retained expected value.
- [ ] Two-state ΦGΦ† reconstruction сохраняет coherence; diagonal-only и
  truncated-basis controls имеют именно derived expected profiles из паспорта.
- [ ] Сохранить finite-chain cavity oracle как embedding control; не называть
  его проверкой bond_current, если соответствующий API там не вызывается.

**Будущая команда:** `julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/physics/nonzero_public_current_oracle.jl")'`.
**Receipt / stop:** signed literal sum, units/weights, coherence negative;
L-JL/CP-CODE. Если для truncation не выведен expected effect, оставить эту
подчасть design_blocked и не заменять физический вывод uniform profile.

## DEV07 — O08-05: absolute kernel amplitude

**Owner / evidence / coverage:** Core; RV08 L/R09–R11, R08 reuse,
RV09 T04, O08-05.
**Роль:** I medium. **Depends:** все четыре accepted absolute passports DEV02;
если принят только один, выполнять только его отдельным child packet.
**Permitted paths:** **proposed** `C/test/physics/absolute_scattering_kernel_oracles.jl`;
existing `C/test/physics/exact_kernel_rescaling.jl` только control reference.
**Excluded:** renormalization K, отключение scattering, fitting prefactors,
исправление модели без scientific decision.

**Interface:** existing `lo_phonon_kernel`, `interface_roughness_kernel`,
`acoustic_kernel`, `alloy_kernel`; четыре имени проверены в
`src/numerics/reference/kernels.jl` на selected source.

- [ ] Для каждого accepted channel использовать independent one-state
  geometry/SI constants и literal form factor, сохраняя scale conversion.
- [ ] Direct unnormalized kernel magnitude сверить с derived RHS; отдельно
  existing qK×normalized-K equality оставить algebraic control.
- [ ] Wrong global multiplicative factor должен нарушать absolute assertion,
  даже если normalized thermal LO/KMS/balance сохраняется.
- [ ] Переиспользовать existing impurity midpoint-angle oracle из
  `C/test/numerics/frozen_scientific_fixtures.jl`; impurity не подменяет четыре
  missing channel cases.

**Будущая команда:** `julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/physics/absolute_scattering_kernel_oracles.jl")'`.
**Receipt / stop:** четыре independent RHS provenance/units и magnitude
assertions, L-JL/CP-CODE. Unknown prefactor/reference/geometry — stop того
channel; no invented thresholds и no normalized test as substitute.

## DEV08 — O08-06: direct/FFT PV отдельно от product integration

**Owner / evidence / coverage:** Core; RV08 R14, RV09 T04, O08-06.
**Роль:** I medium. **Depends:** O08-06 accepted discrete/continuum passports.
**Permitted paths:** `C/test/numerics/direct_principal_value_transform.jl`,
`C/test/numerics/fft_linear_hilbert_map_equals_direct_principal_value.jl`,
**proposed** `C/test/numerics/principal_value_independent_oracle.jl`.
**Excluded:** discrete operator/window changes ради совпадения; не менять
`analytic_product_integration.jl` для получения чужого pass.

**Interface:** `direct_hilbert_transform`, `QCLNEGF.fft_hilbert_transform`;
existing analytic-product-integration test остаётся другим contract.

- [ ] Few-node asymmetric array с nonunit quadrature weights: literal
  omitted-diagonal sum зафиксирован вне target helper; сверить all entries.
- [ ] FFT сравнить с тем же independently specified discrete map, включая
  zero-padding/boundary condition; общий direct helper не единственный oracle.
- [ ] Отдельный finite-window analytic continuum case и refinement trend
  проверить только по DEV02 derivation; tail/window error сохранить явно.
- [ ] Wrong denominator sign, inserted diagonal term или periodic wrap
  нарушает designated assertion; RHS при mutation остаётся фиксированной.

**Будущие команды:** `julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/numerics/principal_value_independent_oracle.jl")'`;
`julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/numerics/fft_linear_hilbert_map_equals_direct_principal_value.jl")'`.
**Receipt / stop:** два разных claims discrete/continuum и retained product
scope, L-JL/CP-CODE; не принять прямое agreement двух shared implementations
как independent continuum evidence.

## DEV09 — Exact-child selection contract для composite export

**Owner / evidence / coverage:** AiiDA service с Portal consumer; RV07 F07.1,
`A/fixes/RV07-attempt-export.md`. **Роль:** D ultra.
**Depends:** current `_select_child`/single-file contract сохраняется.
**Permitted paths:** **proposed** `Aii/docs/export-selection.md` и только
ссылка из `Aii/README.md`. Portal reviewer read-only, consumer code не менять.
**Excluded:** новую scientific selection policy, latest-time heuristic,
publication switch mutation, native daemon.

**Inputs / proposed interface для CP-DESIGN:**
`get_export_selection(identifier: str, execution_id: str, *, attempt=None,
calcjob_uuid=None) -> dict[str, Any]` возвращает ровно selected
`execution_id`, positive `attempt`, canonical `calcjob_uuid` и scientific
`status` либо explicit unknown; `list_execution_artifacts(identifier,
execution_id, *, attempt=None, calcjob_uuid=None)` возвращает inventory только
того же child. Это **proposed** additions; existing `get_export_plan` и
`open_artifact` уже принимают оба selectors. Existing `list_artifacts(run)`
all-attempt listing остаётся совместимым, Portal не строит из него snapshot.

- [ ] Описать omitted-selector shortcut через существующий published
  selection/legacy single child; ambiguous/conflicting/foreign selection
  rejects до payload, Bool attempt rejects, new export resolve выполняется один раз.
- [ ] Зафиксировать one immutable child binding для inventory/plan/bytes/status;
  selectors обоих значений передаются в каждый subsequent call; status0 process
  не становится scientific completed.
- [ ] Задать cache identity `(run, execution, attempt, calcjob_uuid, profile)`;
  stale legacy cache после process restart отсутствует, silent reuse не допускается.
- [ ] Contract fixtures: two attempts equal-size/different bytes+plans,
  same/disjoint paths, selected2, selection change after resolve; one-attempt
  compatibility и explicit errors. Decide exact response fields/error mapping
  в документе до READY DEV10/11, не оставлять значения «TBD».

**Будущие команды:** `rg -n '^def (_select_child|get_export_plan|list_artifacts|get_artifact_metadata|open_artifact)' components/qcl-negf-aiida/src/aiida_qcl_negf/service.py`;
`git -C components/qcl-negf-aiida diff --check`.
**Receipt / stop:** versioned proposed service/API contract, migration/error
table и CP-DESIGN; L-SOURCE. Если нужно менять scientific selection authority,
сохранить existing behavior и вернуть scoped question владельцу.

## DEV10 — AiiDA exact export selection producer

**Owner / evidence / coverage:** AiiDA, RV07, DEV09 accepted contract.
**Роль:** I medium. **Depends:** DEV09 CP-DESIGN.
**Permitted paths:** `Aii/src/aiida_qcl_negf/service.py`,
`Aii/tests/test_artifact_locator.py`, `Aii/tests/test_export_plan.py`,
**proposed** `Aii/tests/test_export_selection.py`, `Aii/README.md` API examples.
**Excluded:** workflows/CalcJob/scientific arrays, Portal, all-attempt API removal.

**Interface:** implement exactly accepted DEV09 additions and reuse
`_select_child`; `get_export_plan(..., attempt=, calcjob_uuid=)` remains exact.

- [ ] Реализовать resolve-once selection и exact inventory без payload reads;
  если child lacks complete inventory — explicit reject.
- [ ] Two equal-size attempts с различными raw bytes и source-plan origins:
  assert selection2 UUID/attempt/status/inventory; stale published selection
  не меняет explicit subsequent calls.
- [ ] Same/disjoint paths и legacy one-attempt positive; foreign UUID,
  mismatch pair, missing child, Bool/zero attempt, ambiguity reject до payload.
- [ ] Reuse existing `test_equal_size_content_oracle_and_selection_pin`,
  `test_metadata_fail_closed_without_payload`,
  `test_retrieved_frozen_plan_preserves_exact_bytes_and_closes_reader`;
  новые names в new file — **proposed** `test_export_selection_pins_child`
  и `test_export_inventory_rejects_foreign_or_incomplete_child`.

**Будущая команда:** `uv run --locked --no-sync --package aiida-qcl-negf python -m pytest components/qcl-negf-aiida/tests/test_export_selection.py components/qcl-negf-aiida/tests/test_artifact_locator.py components/qcl-negf-aiida/tests/test_export_plan.py -q`.
**Receipt / stop:** actual imported service path/version+source, all selected
assertions, L-PY/CP-CODE. Mock repositories явно synthetic; missing actual
AiiDA dependency не обходить import stubs. Owning publication по PUBLISH
раньше смены consumer/root gitlink.

## DEV11 — Portal composite export consumer, API и cache

**Owner / evidence / coverage:** Portal; RV07 F07.1/RV15 locator boundary.
**Роль:** I medium. **Depends:** accepted DEV09, DEV10 source/contract available;
production consumer upgrade после публикации producer.
**Permitted paths:** `P/src/qcl_negf_api/{service.py,exports.py,api.py}`,
`P/frontend/src/api.ts`, `P/frontend/src/main.tsx`, `P/tests/test_exports.py`,
`P/tests/test_api.py`, `P/tests/test_service.py`, `P/README.md`,
**proposed** `P/frontend/tests/export-selection.test.ts`.
**Excluded:** formulas/scientific acceptance, arbitrary inventory filtering,
Bearer/capability redesign, unrelated UI.

**Interface:** `ExportStore.create(run, execution_id, profile, *, attempt=None,
calcjob_uuid=None)` — **proposed** compatible signature, resolves DEV09 once;
ExportRequest strict optional positive attempt/UUID; status/cache include
exact selected identity; frontend types/request propagate selected fields.

- [ ] Registered actor operations получают additions DEV10; metadata/plan/
  copy/status всегда используют frozen selectors, не default latest.
- [ ] Cache reused только для exact key; selection switch mid-prepare не
  меняет ready archive. Unselected same-path entry не вызывает duplicate.
- [ ] Test bytes2 equality, exact frozen-plan bytes/source2 и status2;
  equal lengths не являются достаточной assertion. Existing
  `test_export_forwards_exact_frozen_plan_bytes_and_source` сохраняется.
- [ ] Negative invalid/mismatched selectors 422 до preparation/payload;
  unknown child404, ambiguity/incomplete422 по accepted contract; old one-child
  body остаётся compatible. Cache never shares attempt1 and attempt2.
- [ ] Existing spool/reserve/receipt-tail checks и error cleanup сохраняются;
  browser отображает exact attempt, фиксированную light theme и native
  download без complete-file Blob. Add proposed tests
  `test_export_pins_inventory_plan_payload_status_and_cache` и
  `test_export_selection_changes_do_not_mix_snapshot`.

**Будущие команды:** `uv run --locked --no-sync --package qcl-negf-api python -m pytest components/qcl-negf-portal/tests/test_exports.py components/qcl-negf-portal/tests/test_api.py -q`;
`node --experimental-strip-types --test components/qcl-negf-portal/frontend/tests/export-selection.test.ts`.
**Receipt / stop:** API/error/cache matrix+bytes oracle, L-PY; frontend source
checks максимум один дополнительный 90 s call в общем slot. Build не входит.
CP-CODE; отсутствующий producer operation — blocker, не dynamic fallback.

## DEV12 — Actor bounded response / unknown outcome / close: отдельный design

**Owner / evidence / coverage:** Portal с AiiDA semantics; RV05, RV12 lost-submit.
**Роль:** D ultra. **Depends:** existing one-thread/loop/handle ownership.
**Permitted paths:** **proposed** `P/docs/actor-lifecycle.md`, `P/README.md`
только ссылка/согласованная формулировка. **Excluded:** actor/API code и tests,
process isolation внедрение, kill thread/process, реальный submit.

**Output contract:** полная state/operation table для initialize/read/seek/
call/submit/cancel/close, queue admission и response deadline source. Exact
timeout values author выводит из existing policy либо документирует как
новое operational решение с основанием; не выдаёт придуманные значения за
существующие. Test injected clock/deadline не scientific threshold.

- [ ] Развести deadline caller response и завершение backend effect; running
  Future timeout не отменяет ORM/submit. Unknown mutation outcome не допускает
  auto retry/новый provenance submit; reconcile через exact known run/CalcJob.
- [ ] Сохранить один profile/thread/loop owner и exactly-once handle exit;
  close result truthful: completed только после unload/handle close, timeout
  остаётся unknown/stopping, не successful close.
- [ ] Выбрать минимальную architecture: bounded caller wait + controlled
  admission/stopping достаточна, если hard backend termination не требуется.
  Process isolation рассматривается отдельным D output, если нужна гарантия
  process exit; нельзя обещать её поверх ThreadPoolExecutor wait.
- [ ] Определить exact exception/result types, HTTP mapping, unknown mutation
  response/reconnect workflow, limits pending calls, export lease lifecycle;
  показать compatibility для healthy finite calls.
- [ ] Test design: Event-gated fake backend starts before disconnect/close,
  independent monotonic clock/order witness, Event always released in finally;
  healthy control, queued-before-start timeout, in-flight submit timeout,
  late completion, repeated close, no double handle close/no second submit.

**Будущие команды:** `rg -n 'result\(|shutdown\(|def close|def _call|open_artifact' components/qcl-negf-portal/src/qcl_negf_api/service.py components/qcl-negf-portal/src/qcl_negf_api/exports.py`;
`git -C components/qcl-negf-portal diff --check`.
**Receipt / stop:** CP-DESIGN accepts precise states/types/settings/source,
L-SOURCE; DEV13 stays blocked until no unspecified operation/error behavior.
New irreversible recovery policy или need process supervisor — отдельный D,
не blanket implementation и не operator gate для уже определённого local contract.

## DEV13 — Реализация actor contract и fault fixtures

**Owner / evidence / coverage:** Portal; RV05/RV12; accepted DEV12.
**Роль:** I medium. **Depends:** CP-DESIGN DEV12.
**Permitted paths:** `P/src/qcl_negf_api/{service.py,api.py,exports.py,settings.py}`,
`P/tests/test_service.py`, `P/tests/test_stream_disconnect.py`,
`P/tests/test_exports.py`, `P/tests/test_api.py`,
**proposed** `P/tests/test_actor_deadlines.py`, `P/docs/actor-lifecycle.md`.
**Excluded:** AiiDA ORM ownership migration/real daemon, automatic resubmit,
thread kill, claiming bounded process exit without selected design proof.

**Interface:** exact DEV12 accepted types/settings/state machine; no new
unreviewed names or arbitrary hardcoded deadline. Proposed tests
`test_blocked_call_returns_unknown_without_duplicate_submit`,
`test_close_does_not_claim_backend_completion`,
`test_disconnect_releases_handle_exactly_once_after_backend_returns`.

- [ ] Implement bounded caller waits and queue/stopping admission per design;
  preserve one owner, no ORM/handle action in HTTP threads.
- [ ] Event-gated backend asserts actual owner order and caller response
  within injected design bound; no time.sleep race as sole witness.
- [ ] Running submit timeout gives unknown; assert submit_count==1 even
  reconnect/status read, no success response before known acceptance.
- [ ] Close timeout remains truthful; finite late completion closes/unloads
  once; repeated close idempotent. Always release Event in test finally.
- [ ] Preserve existing `test_aiida_profile_operations_and_artifact_handles_have_one_thread_owner`,
  `test_asgi_disconnect_closes_reader_and_releases_export_lease`,
  `test_shutdown_cancels_preparation_at_the_next_progress_callback`.

**Будущая команда:** `uv run --locked --no-sync --package qcl-negf-api python -m pytest components/qcl-negf-portal/tests/test_actor_deadlines.py components/qcl-negf-portal/tests/test_service.py components/qcl-negf-portal/tests/test_stream_disconnect.py components/qcl-negf-portal/tests/test_exports.py -q`.
**Receipt / stop:** Event/owner/known-vs-unknown evidence, L-PY/CP-CODE.
Hung test обязан выйти по cap, failed log сохраняется; необходимость настоящего
backend process kill не решается скрытым supervisor в этой карточке.

## DEV14 — Canonical Contracts descriptions и legacy size scope

**Owner / evidence / coverage:** Contracts; RV07 F07.3, RV19 P19A.
**Роль:** D ultra. **Depends:** current schema semantics; D01 historical report
не нужен как substitute current source, его отсутствие сохранить.
**Permitted paths:** `K/README.md`,
`K/src/qcl_negf_contracts/schemas/run.schema.json` только
`$defs.production.properties.energy_chunk.description`.
**Excluded:** required/type/minimum/default constraints, values, validator,
new size ceiling, Runner vendored copy в этой карточке.

**Interface:** authored description — positive integer execution chunk count,
required merged input без schema-assigned default; Core typed default не
assigning provenance; chunk не energy-grid step. README200MB относится
legacy multipart, new single-archive receipt имеет nonnegative bytes без ceiling.

- [ ] Внести только описания и legacy-only wording; existing300000000-byte
  receipt остаётся valid, Bool/-1/path/parts invalid.
- [ ] Сравнить parsed old/new schemas, разрешён только exact description leaf;
  не сортировать/переформатировать весь JSON и не менять defaults.
- [ ] Назвать existing `test_single_archive_receipt_validates_unbounded_size_and_confined_filename`
  как regression anchor; это prose-only correction не требует numerical env.
- [ ] Output documented canonical change/source hash передать DEV15/16;
  не редактировать обе копии independently.

**Будущие команды:** `git -C components/qcl-negf-contracts diff --check`;
при DEV cheap-check scope `uv run --locked --no-sync --package qcl-negf-contracts python -m pytest components/qcl-negf-contracts/tests/test_contracts.py::test_single_archive_receipt_validates_unbounded_size_and_confined_filename -q`.
**Receipt / stop:** description-only semantic diff и legacy scope source map,
L-SOURCE + максимум один L-PY invocation если runtime готов. CP-DESIGN/CP-CODE;
publication canonical Contracts перед Runner copy; никакой schema relaxation.

## DEV15 — Runner assigning-source prose и schema drift contract

**Owner / evidence / coverage:** Runner; RV07 F07.2/RV19; current copies equality
не ongoing guard. **Роль:** D ultra. **Depends:** DEV14 reviewed canonical diff.
**Permitted paths:** `R/src/application/configuration_types.jl` только docstring
`configuration_source`, `R/docs/src/user/configuration.md`,
**proposed** `R/docs/schema-provenance.md`.
**Excluded:** code behavior, schema bytes/provenance hashes (DEV16), full origin
inference; Portal/Platform generators не входят.

**Interface:** `configuration_source(configuration::ResolvedRunConfiguration,
dotted_path::AbstractString)` возвращает last explicit source filename либо
`nothing` при missing/empty provenance, не schema default/effective origin.
Schema drift contract отдельно определяет canonical inputs + packaged check.

- [ ] Исправить docstring и guide на explicit assignment meaning; existing
  merge-order base→17→23 выбирает23/last filename, reverse выбирает17.
  Absence history не выдумывает assigning source от typed default64.
- [ ] Найти existing owning drift guard во всех tracked Runner integration
  paths, не объявлять отсутствие по одному search. Если guard есть — specify
  reuse, не заводить второй framework.
- [ ] Если отсутствует: describe **proposed** `tools/verify_schema_provenance.jl`
  check: parse existing `schema/PROVENANCE.json`, verify each declared packaged
  file bytes/hash; workspace mode additionally compares canonical Contracts
  path from selected root, no remote latest resolution. Standalone mode does
  not require sibling checkout, validates bundled declared hashes.
- [ ] Определить exact invocation and failure boundary: verification before
  schema-dependent configuration use в agreed supported entrypoints; one-byte
  vendored change, stale PROVENANCE и changed canonical copy fail closed.
  New hash tracks bytes, not научную adequacy. Записать integration seam
  до READY DEV16, не прятать runtime cost/behavior в docs-only change.

**Будущие команды:** `rg -n 'PROVENANCE.json|configuration_source|schema.*hash|verify.*schema' components/QCLNEGFRunner.jl`;
`git -C components/QCLNEGFRunner.jl diff --check`.
**Receipt / stop:** prose diff + accepted drift seam/CLI/mode/error contract,
L-SOURCE/CP-DESIGN. Нужен root integration edit — отдельная root owner task,
а не расширение permitted paths этого Runner writer.

## DEV16 — Runner packaged schema update и enforcing drift guard

**Owner / evidence / coverage:** Runner; RV07/RV19. **Роль:** I medium.
**Depends:** DEV14 canonical source published, DEV15 CP-DESIGN.
**Permitted paths:** `R/schema/run.schema.json`, `R/schema/PROVENANCE.json`,
**proposed** `R/tools/verify_schema_provenance.jl`,
`R/src/infrastructure/config/configuration_contract.jl` только approved seam,
**proposed** `R/test/contracts/schema_copy_provenance.jl`,
`R/test/application/configuration_merge_order_and_fail_closed_validation.jl`.
**Excluded:** independent schema constraints, schema defaults, full Origin model,
root locks/manual component lock, scientific config.

**Interface:** DEV15 exact drift seam; canonical source selected by published
Contracts gitlink, hashes regenerated through owning workflow. Proposed
testset `Packaged schema provenance rejects drift before resolution`.

- [ ] Copy canonical DEV14 schema byte-for-byte, update existing provenance
  metadata; no individually edited second description/constraint.
- [ ] Implement/reuse declared guard in both supported workspace/standalone
  modes; existing schema validation still runs before Unitful semantics.
- [ ] Positive exact source/file hashes; negatives one-byte packaged change,
  stale hash, mismatching canonical workspace copy, missing file all reject
  before configuration-dependent mutation/execution. Corrupt temporary copies
  only, никогда original selected schemas.
- [ ] Preserve assigning merge17/23/empty history assertions. Existing
  `configuration_merge_order_and_fail_closed_validation.jl` and
  `configuration_schema_scattering_domain.jl` remain source anchors; no full suite.

**Будущие команды:** `julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGFRunner.jl/test/contracts/schema_copy_provenance.jl")'`;
`julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGFRunner.jl/test/application/configuration_merge_order_and_fail_closed_validation.jl")'`.
**Receipt / stop:** canonical/copy/provenance byte hashes + reject-before-use
assertions, L-JL/CP-CODE. Publication ordering mismatch blocks consumer publish;
do not mark guard passed solely because copies currently equal.

## DEV17 — Generic runtime checkpoint durability: contract first

**Owner / evidence / coverage:** Runner; RV11 F11.1,
`A/fixes/RV11-runtime-durability.md`. **Роль:** D ultra.
**Depends:** generic publication trace, не наследовать scientific commit protocol.
**Permitted paths:** **proposed** `R/docs/runtime-checkpoint-durability.md`.
**Excluded:** production helpers/checkpoint writes, scientific generation/schema,
NFS/power-loss experiment и automatic migration.

**Inputs / interface:** `src/infrastructure/runtime/filesystem_repository.jl`
`save_runtime_checkpoint!`, `load_latest_checkpoint`, `_immutable_yaml`,
atomic YAML helper; сравнить read-only с `persistence/point_artifacts.jl`
closed payload→publish→verify→receipt→pointer barriers.

- [ ] Trace complete call chain, файл/директория и parent fsync, error
  propagation, lock scope и reader acknowledgement. Если enclosing barrier
  уже достаточен — exact proof и keep, не duplicate fsync patch.
- [ ] Определить supported filesystem/durability level: atomic namespace
  replacement отдельно от acknowledged persistence; local POSIX и NFS unknown
  не смешиваются. Crash before successful return не обещает latest generation.
- [ ] Выбрать exact sequencing/error result так, чтобы acknowledged reader
  принимает только old/new complete verified generation; no partial payload,
  missing metadata и hash mismatch fail closed; raw identity preserved.
- [ ] Define fault cuts after payload close/hash/publish, metadata write/
  publish и pointer update; proposed injectable seam имена/signature определить
  здесь. Independent reader не вызывает writer validation helper.
- [ ] Совместимость старых checkpoint и cleanup rules явны; неизвестную
  migration не выполнять автоматически. Output contract делает DEV18 READY
  только после точного sequencing и fault assertions.

**Будущие команды:** `rg -n 'save_runtime_checkpoint!|load_latest_checkpoint|_immutable_yaml|_atomic_replace_file|fsync' components/QCLNEGFRunner.jl/src/infrastructure/runtime/filesystem_repository.jl components/QCLNEGFRunner.jl/src`;
`git -C components/QCLNEGFRunner.jl diff --check`.
**Receipt / stop:** CP-DESIGN sequence diagram/table+support scope, L-SOURCE.
Live medium/NFS behavior — OPS gate. Barrier ownership ambiguity сохраняется
как blocked design, не «добавим fsync всюду».

## DEV18 — Generic checkpoint barriers и independent fault reader

**Owner / evidence / coverage:** Runner, RV11; accepted DEV17.
**Роль:** I medium. **Depends:** exact barrier/fault contract DEV17.
**Permitted paths:** `R/src/infrastructure/runtime/filesystem_repository.jl`,
`R/src/infrastructure/persistence/atomic_files.jl` только accepted DEV17 seam;
`R/test/infrastructure/yaml_repository_provenance_spans_and_checkpoint_integrity.jl`,
**proposed** `R/test/infrastructure/runtime_checkpoint_durability_faults.jl`,
`R/docs/runtime-checkpoint-durability.md` фактические implementation locators.
**Excluded:** scientific point commit redesign, native NFS claim, solver/restart.

**Interface:** existing save/load signatures unchanged либо exact versioned
compatibility decision DEV17; proposed testset `Runtime checkpoint publication faults`.

- [ ] Implement only missing accepted barrier; propagate write/fsync/rename
  errors, no copy/delete fallback weakening immutable publication.
- [ ] At each approved cut inject deterministic failure; independent byte/hash
  reader sees old/new complete state or explicit unavailable, never partial
  acknowledged generation. Post-return success requires complete new state.
- [ ] ENOSPC metadata tail, payload hash mismatch, wrong run/point/attempt and
  missing file reject. Temporary test roots preserve original checkpoints.
- [ ] Healthy save/load and existing YAML integrity fixture remain compatible;
  failed attempt original logs preserved, no deleting blocker to pass.

**Будущие команды:** `julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGFRunner.jl/test/infrastructure/runtime_checkpoint_durability_faults.jl")'`;
`julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGFRunner.jl/test/infrastructure/yaml_repository_provenance_spans_and_checkpoint_integrity.jl")'`.
**Receipt / stop:** fault-cut matrix+independent observed bytes, L-JL/CP-CODE.
Large existing HDF5/Julia compilation beyond cap stops verification; native
crash durability remains unmeasured even при всех synthetic passes.

## DEV19 — Standalone assets и import routes: supported workflow design

**Owner / evidence / coverage:** Portal package owner, Runner/Results reviewers;
RV14 F14.1/F14.2, RV02 M06. **Роль:** D ultra.
**Depends:** current root release.ts / Portal Nix frontend path source-read.
**Permitted paths:** **proposed** `P/docs/package-identity.md`, `P/README.md`
supported build section. **Excluded:** hook/config implementation, deps install,
wheel build, extra maintained revision lock, change root release workflow.

**Inputs / interface:** `P/hatch_build.py::CustomBuildHook.initialize` checks
only existence; Vite config writes static tree, package-lock owns JS deps;
root `ops/release.ts` and `P/nix/frontend.nix` build source separately.

- [ ] Choose supported direct wheel workflow and source-freshness contract:
  generated build receipt binds exact frontend input set/package-lock/build
  recipe/content hashes; wheel hook rejects missing/stale receipt+payload.
  Receipt is derived output, ignored generated artifact, not a maintained lock.
- [ ] Exact input enumeration, exclusion of node_modules/dist/generated output,
  output asset hash list, atomic receipt publish и build-hook error behavior
  specify before READY. If mandatory clean-generation route selected instead,
  define how direct wheel cannot accept stale payload through that route.
- [ ] Healthy compiled assets accepted; old index/JS beside changed TS input,
  changed lock, missing asset, altered output bytes and incomplete receipt
  explicitly fail. Editable route remains declared bypass of browser build,
  не accepted release wheel.
- [ ] Define route matrix: workspace editable, standalone wheel/editable,
  Runner standalone Core tag vs workspace post-tag, Nix release closure.
  Same0.2.0 label never transfers import receipt; module/distribution/source
  location and build identity fields exact.
- [ ] Keep light/offline source rules; remote CDN/theme injection cannot
  become freshness fix. Build receipt contains no private environment/secrets.

**Будущие команды:** `rg -n 'CustomBuildHook|frontendBuild|cleanSource|npmDepsHash|outDir|static' components/qcl-negf-portal/hatch_build.py components/qcl-negf-portal/frontend components/qcl-negf-portal/nix/frontend.nix ops/release.ts`;
`git -C components/qcl-negf-portal diff --check`.
**Receipt / stop:** exact derived-receipt schema/mode/CLI/signatures in design,
CP-DESIGN/L-SOURCE. Actual frontend/wheel/Nix build требует BUILD, DEV20
не получает право installing/building dependency graph вследствие документа.

## DEV20 — Portal stale-assets rejection implementation

**Owner / evidence / coverage:** Portal; RV14 F14.1. **Роль:** I medium.
**Depends:** DEV19 accepted source-binding design.
**Permitted paths:** `P/hatch_build.py`, `P/frontend/vite.config.ts`,
`P/frontend/package.json` только script hook without dependency additions,
**proposed** `P/frontend/tools/asset-receipt.mjs`,
**proposed** `P/tests/test_build_assets.py`, `P/.gitignore`,
`P/docs/package-identity.md` exact workflow references.
**Excluded:** generated static/assets/dependency dirs committed, lock refresh,
Nix hash edits, backend API, full build в DEV envelope.

**Interface:** exact DEV19 receipt filename/JSON fields/input hashing and
hook mode; no new undocumented second source stamp. Proposed tests
`test_wheel_rejects_stale_frontend_inputs`,
`test_wheel_rejects_changed_asset_bytes`,
`test_editable_route_does_not_claim_release_asset_identity`.

- [ ] Add derived receipt generation and verification without target import
  side effects/network; hook verifies both inputs and emitted bytes.
- [ ] Tiny synthetic public directories exercise fresh/stale/missing/changed
  inputs/output/malformed receipt, no actual npm install/build needed.
- [ ] Positive root/Nix workflow compatibility verified source-wise; actual
  wheel payload/browser acceptance deferred to CP-NATIVE route receipt DEV22.
- [ ] Existing `test_ci_environment.py` command contract stays unchanged;
  full `deno task test:frontend` includes npm ci and is not cheap DEV check.

**Будущие команды:** `uv run --locked --no-sync --package qcl-negf-api python -m pytest components/qcl-negf-portal/tests/test_build_assets.py -q`;
`python3.14 -m unittest discover -s components/qcl-negf-portal/tests -p test_ci_environment.py`.
**Receipt / stop:** stale/fresh differentiating results и generated-receipt
contract, L-PY/CP-CODE. Если hatchling absent — no stubs as native hook proof;
preserve source diff и runtime blocker, среду готовит отдельный BUILD stage.

## DEV21 — Продолжить Results PR6: owning imports, portability и oracle guards

**Owner / evidence / coverage:** Results; RV02/RV09 T05, existing
[PR6](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/pull/6).
**Роль:** I medium. **Depends:** read-only exact PR base/head metadata;
archived base `fe27a2a…`, candidate `a1492b7…` — historical locators,
не обещание current PR head. **Permitted paths:** existing PR6 touched files
`B/README.md`, `B/tests/test_equilibrium_diagnostics.py`,
**PR6 existing, absent at selected base** `B/tests/test_source_ownership.py`,
`B/tests/source_ownership.py`; exact four-file list подтвердить current PR
diff перед READY. Если differs — scoped replan, не guessing file names.
**Excluded:** новый duplicate PR, removing ownership guard ради pass,
numerical production changes, reverting independent arithmetic.

**Interface:** retain PR6 selected-source guard, no personal hardcoded paths,
owning `qcl_negf_results`/`qcl_negf_contracts` imports and actual distribution
identity; preserve 36 numerical properties and whole existing assertion sets.

- [ ] Attach existing PR6 to future task; inspect exact published head/raw
  diff before writing. Source review archive keep не runtime acceptance.
- [ ] Compare current base/candidate and resolve only remaining portability
  gap. Preserve literal inverse2/math.fsum/weights oracle, R02 offdiagonal,
  R04 transpose/R06 changed weights-retained target, R35 attempt mismatch.
- [ ] Reuse existing PR6 positive selected source and negative copied Results,
  shadow Contracts/conflicting workspace override; do not accept unknown modules.
- [ ] Add only missing standalone wheel/editable or wrong distribution-version
  branch with **proposed** names `test_standalone_distribution_ownership` and
  `test_wrong_distribution_version_is_rejected`; actual wheel execution
  depends prepared trusted wheel artifacts from BUILD, source fixtures alone
  labelled synthetic.
- [ ] Run targeted existing PR6 ownership+numerical fixtures under Python3.14
  lock; if actual imports unavailable, preserve blocker, not fake stubs/skip-pass.

**Будущие команды:** `gh pr view 6 --repo Afonenko-QCL-NEGF/qcl-negf-results --json url,baseRefOid,headRefOid,files,state`;
`uv run --locked --no-sync --package qcl-negf-results python -m pytest components/qcl-negf-results/tests/test_source_ownership.py components/qcl-negf-results/tests/test_equilibrium_diagnostics.py -q`.
**Receipt / stop:** exact PR head+import ownership+positive/negative assertions,
L-PY/CP-CODE. No permission for posting comments/messages from this plan;
updates/push under PUBLISH. Candidate object absent → metadata/raw source
recovery first, не сравнивать текущий base с imagined PR implementation.

## DEV22 — Независимая проверка source/build/import identity по маршрутам

**Owner / evidence / coverage:** package integration reviewer; RV02 M06,
RV14 eight selected links. **Роль:** R high. **Depends:** DEV19/20/21;
для build/wheel/closure маршрутов — exact BUILD receipts и CP-NATIVE OPS owner.
**Permitted paths:** **proposed** root evidence file
`docs/implementation/evidence/review-closure-2026-10-19/package-identity.md`
после DEV grant; owning PR review receipts. **Excluded:** code/settings/locks,
installation/build/SSH, global env mutation, production runtime access.

**Interface:** matrix root/gitlink→distribution→actual module path/version→
assets→derivation/output; upstream producer refs опубликованы до release claim.
Reviewer читает immutable candidate без подсказанного «pass» результата.

- [ ] Workspace imports map to selected B/K/Aii/P src paths; check
  `sys.executable`, `sys.version`, module `__file__`, importlib.metadata version
  и direct_url если существует. Missing metadata не заменять версией0.2.0.
- [ ] Standalone wheel и editable пути проверяются отдельными receipts из
  подготовленной изолированной Python3.14 среды; portable foreign user/source
  path не содержит developer personal absolute constants.
- [ ] Julia workspace `pathof(QCLNEGF)`/`pathof(QCLNEGFRunner)` и standalone
  tag route сравниваются отдельно; post-tag Core3108150 и v0.2.0 string не
  объявляются one source. Native sysimage/solver receipt отдельно от import.
- [ ] Match Portal receipt inputs/assets hash с built wheel contents; root
  frontendBuild/Nix cleanSource path controls не inherited full-release CI.
- [ ] Новый root HEAD всегда получает new release evidence scope; native
  output reuse только derivation+contents+test-contract match. Two rebuild
  reproducibility пока не измерена, не делать её из hashes alone.

**Будущие команды:**
`uv run --locked --no-sync --package qcl-negf-results python -c 'import sys, importlib.metadata as m, qcl_negf_results, qcl_negf_contracts; print(sys.executable, sys.version); print(qcl_negf_results.__file__, m.version("qcl-negf-results")); print(qcl_negf_contracts.__file__, m.version("qcl-negf-contracts"))'`;
`julia --startup-file=no --project=julia --threads=1 -e 'using QCLNEGF, QCLNEGFRunner; println(VERSION); println(pathof(QCLNEGF)); println(pathof(QCLNEGFRunner))'`.
Standalone command uses exact prepared interpreter path from BUILD receipt,
никогда invented universal path; binding вписывается reviewer до invocation.
**Receipt / stop:** route-specific matrix и limitations; максимум по одному
bounded L-PY/L-JL invocation, imports требуют готовой среды. CP-CODE;
missing native artifact оставляет соответствующую cell not_measured и не
блокирует source/doc review остальных маршрутов.

## DEV23 — AiiDA retry/cancel/submit uncertainty: сохранить code boundaries

**Owner / evidence / coverage:** AiiDA, Runner budget reviewer; RV12/RV09 T06.
**Роль:** I medium. **Depends:** existing `attempt_decision`, exact submit marker,
DEV12 unknown-mutation contract при Portal integration.
**Permitted paths:** `Aii/tests/test_restart.py`,
`Aii/tests/test_submission_identity.py`, **proposed** `Aii/tests/test_cancellation_contract.py`,
`Aii/src/aiida_qcl_negf/service.py` только truthful kill result/errors,
`Aii/README.md` cancellation semantics; Runner read-only fixtures below.
**Excluded:** default retry expansion/auto resubmit/idempotency store, Slurm job
operations, native owner proof, runner solve/budget redesign без нового D.

**Interface:** existing `kill_run(identifier)->dict` returns refreshed state
only if terminated, daemon-down/exception/unconfirmed cancellation raises
RuntimeError; this means parent state, not native all-process stop/staging.
Existing submission marker+`--no-requeue` and finite max_attempts preserved.

- [ ] Reuse ten `test_attempt_decision_requires_stopped_owner_and_verified_state`
  cells: infrastructure eligible only with stopped owner+verified recovery;
  scientific301/303/305 terminal, status0 не external physics oracle.
- [ ] Preserve `test_slurm_script_binds_attempt_and_disables_independent_requeue`
  exact frozen bytes/attempt descriptor and immutable executable guards.
- [ ] Add actual-service fault fixtures, no daemon/profile: proposed
  `test_kill_run_daemon_down_has_no_success`,
  `test_kill_run_unconfirmed_state_remains_unknown`,
  `test_kill_run_refreshes_before_confirmed_summary`; verify no fabricated killed
  status, no retry/submit calls on cancellation ambiguity, exception redaction.
- [ ] Lost submit acknowledgement uses DEV12 no-second-submit assertion;
  do not add duplicate submission workaround. Full restart budget inspected
  with existing `production_restart_validates_metadata_and_restores_state.jl`
  and `restored_stage_progress_consumes_the_original_budget.jl`; event remaining60
  alone not full-loop proof. If missing full numerical cap assertion remains,
  exact new Runner D ticket (not hidden solver run) goes coordinator/science plan.

**Будущая команда:** `uv run --locked --no-sync --package aiida-qcl-negf python -m pytest components/qcl-negf-aiida/tests/test_cancellation_contract.py components/qcl-negf-aiida/tests/test_restart.py components/qcl-negf-aiida/tests/test_submission_identity.py -q`.
**Receipt / stop:** retry status matrix, cancellation known/unknown and no
duplicate evidence, L-PY/CP-CODE. Native Slurm/proctrack/final staged receipt
остаётся OPS evidence; source response не закрывает remote-stop gate.

## DEV24 — Независимые public trust/rejection controls

**Owner / evidence / coverage:** Portal/AiiDA/Contracts reviewer; RV15,
RV07 selector negative и RV09 T06. **Роль:** R high.
**Depends:** DEV10/11/13/16/23 candidate refs; Platform public/private checks OPS.
**Permitted paths:** review receipt в owning PR либо **proposed**
`docs/implementation/evidence/review-closure-2026-10-19/software-rejections.md`.
**Excluded:** product edits/security framework expansion, real credentials,
native TLS/private file ownership, privileged test fixtures.

**Interface:** reject-before-payload/submit oracle; public synthetic input
corpus → observed status + zero protected-operation counters. Actual owning
module imports distinguish from backend synthetic mocks.

- [ ] Reuse `test_authentication_and_private_schema`,
  `test_submission_rejections_do_not_start_work`,
  `test_native_artifact_capability_cannot_open_other_artifacts`,
  `test_locator_selection_race_capability_and_range`,
  `test_exact_locator_errors_have_no_payload`,
  `test_broker_unavailable_is_not_reported_as_success`.
- [ ] Independently check missing/wrong token401 before actor, wrong path/
  selector before payload, wrong capability before metadata, invalid resources
  before submit. Exact-attempt export invalid inputs cannot share old cache.
- [ ] Reuse AiiDA `test_invalid_paths_before_selection` and
  `test_metadata_fail_closed_without_payload`; Contracts finite JSON/bool
  rejection `test_json_boundary_rejects_ambiguous_or_invalid_inputs`.
- [ ] Selected public errors hide private fake broker address; log access/
  sanitization and full security audit remain unmeasured. Findings need exact
  assertion+source locator; small corrective implementation gets new I ticket,
  reviewer не меняет код незаметно под видом R.

**Будущие команды:** `uv run --locked --no-sync --package qcl-negf-api python -m pytest components/qcl-negf-portal/tests/test_api.py -q -k 'authentication_and_private_schema or submission_rejections_do_not_start_work or native_artifact_capability_cannot_open_other_artifacts or locator_selection_race_capability_and_range or exact_locator_errors_have_no_payload or broker_unavailable_is_not_reported_as_success'`;
`uv run --locked --no-sync --package aiida-qcl-negf python -m pytest components/qcl-negf-aiida/tests/test_artifact_locator.py -q`;
`uv run --locked --no-sync --package qcl-negf-contracts python -m pytest components/qcl-negf-contracts/tests/test_contracts.py -q -k json_boundary`.
**Receipt / stop:** property×negative/control matrix, L-PY/CP-CODE; no repeated
suite without change. All asserts passing не production TLS/security acceptance.

## DEV25 — Same-source software closure и передача release/native/science

**Owner / evidence / coverage:** независимый coordinator/reviewer всех DEV;
RV02–09, RV11–12, RV14–15, owning RV19 descriptions.
**Роль:** R high. **Depends:** готовые DEV packets и preserved open cells.
**Permitted paths:** closure receipt **proposed**
`docs/implementation/evidence/review-closure-2026-10-19/software-closure.md`;
review comments в agreed artifact, не отправка сообщений людям.
**Excluded:** код, root gitlinks/locks/settings, remote PR publication/merge,
CI reruns, deploy/scientific acceptance.

- [ ] Снять immutable root/component candidate graph, all diffs/source refs;
  обеспечить один writer/path и пересмотреть source changes с момента каждого
  receipt. Старый accepted receipt нельзя переносить на изменённый candidate.
- [ ] Blind reviewer повторно проверяет source contracts, exact test assertions,
  imports и соблюдение envelopes; где reviewer делит fixture helper с author,
  независимость ограничена явно. Disagreement сохраняется с cheapest check.
- [ ] Mapping каждого DEV/RV finding имеет keep/change/measure/insufficient
  disposition, full publication order и отдельные pending native gates.
- [ ] Повторять runtime checks только по new changes/failures; `git diff --check`
  и links/path validation не являются solver test. Уже source-positive
  single-fileCR01/CR05 не переоткрывать из-за старого report.
- [ ] Проверить publication order каждого готового owning packet: собственный
  CP-CODE + active PUBLISH → owning I/INT02 публикует component PR refs → root
  gitlinks/INT02 → повторный CP-SOURCE → CP-NATIVE. Reviewer DEV25 сам ничего
  не публикует и не задерживает независимые publications. Software closure
  receipt передать в будущий final CP-RELEASE dossier; final CI один раз на final ready source,
  никаких automatic reruns. SCI получает oracle passports/limitations, не
  готовый вывод «физика принята».

**Будущие команды:** `git diff --check`; `git status --short`;
`git submodule status --recursive` — каждая отдельно из selected root;
адресное `git -C COMPONENT diff --check` для каждого изменённого component.
**Receipt / stop:** final table ниже заполняется фактическими locators;
L-SOURCE, CP-CODE. Незакрытый blocker не маскируется merge/deploy/общим pass.
Готовые независимые packets допускаются к publication по их собственному
grant, без ожидания недоступного сервера для docs/source результатов.

## Обязательный формат фактического завершения

Это шаблон полей результата, а не заполненный pass. Для каждого task/finding
добавляется строка; текущие статусы всех будущих runtime действий — not_measured.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| D08/source descriptions согласованы с owning implementation | Commit+path/symbol, reviewed exact diff | План; после принятия docs-only diff numerical checks не подразумеваются | изменить |
| O08 property различает healthy и ошибочный оператор | Passport+literal RHS+test assertion+actual log hash | Manufactured scope; не model/experiment validation | сохранить / дополнительно измерить |
| Composite archive принадлежит одному child | Exact UUID/attempt, inventory/plan/bytes/status/cache assertions | Synthetic repositories; native delivery отдельно | изменить / дополнительно измерить |
| Actor timeout/close передаёт truthful known/unknown | Event/order/count assertions и accepted lifecycle contract | Hard blocked backend exit не доказан thread fixture | сохранить / данных недостаточно |
| Schema/checkpoint/package identity guard действует | Exact producer/copy/provenance/import/fault receipt | Не scientific accuracy/NFS durability/full-release acceptance | изменить / дополнительно измерить |
| Release/scientific stage готов к своему gate | Опубликованные owning refs, fresh native inputs, oracle readiness | Pending operator inventory/runtime/science нельзя считать done | дополнительно измерить / данных недостаточно |
