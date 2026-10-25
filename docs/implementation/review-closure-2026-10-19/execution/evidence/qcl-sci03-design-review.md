# SCI03 — независимый CP-DESIGN, round R1

2026-10-19. Source-first independent R/high. Это проверка проекта научного
контракта, а не numerical/scientific acceptance и не разрешение submit.
Проверены исходники и литература; Julia, product imports/tests, solver,
benchmarks/install/full CI, Git mutations и server probes не выполнялись.
Старые S01/current-attempt arrays не читались. Author report прочитан **последним**,
после проверки source/norms/формул и определения замечаний.

## Identity и verdict

- Reviewed candidate `/tmp/qcl-sci03-design.md`, 40 020 bytes, SHA256
  `ceffa4f2ca941510451f1d28a9f0cbaff7277e10411230c0b1dc8ab26c649509`.
- Author report `/tmp/qcl-sci03-design-report.md`, SHA256
  `018faf5229df919eb76abb28399758d8da48db0ac9d444645a590c6834ad594a`.
- Review root HEAD `9f8b08bbf8b2f941eaa6426bc07c2b436a2a81d8`.
  `git status --short` при первом чтении: dirty internals AiiDA/Platform;
  позднее concurrent checkpoint change. Эти изменения не приписываются автору
  и не входят в проверенные owning numerical files. Gitlinks прочитаны recursively.
- Core `f5b73369a96d1225bd96fb34f5262c8dcf965f86`, Research
  `b1a3be2b0f4b3adf423cc2a611bcca2b5e0a5ff3`, Results
  `17574ca4c5495f74d86ed9bef51c60dea8265062`: 14 production/doc/config hashes
  совпали с D1. Author root `7d179b28647f0b89347d2d6358f08cf2fe479653`
  отличается от reviewer root; owning bytes совпадают, новый root не наследует
  runtime/native/full release acceptance.
- Дополнительно read-only проверен committed Runner
  `2d0190d5573f74d847d92a0dac8dd6ec524d494c` для выразимости H; это отдельное
  source evidence, не runtime test или утверждение о готовом H plan.

**CP-DESIGN R1: `request_changes`, узкий D2 перед freeze точного контракта.**
Научных противоречий в §5 bounds, S1 scope или политике unknown→blocked не найдено.
Но D1:96 смешивает локальное соглашение `_ratio` с фактическим FDR verdict при
неопределённой μ. Для frozen near-zero semantics требуется явное исправление R1-01.
R1-02 — точный primary locator; R1-03 — устранение неоднозначности scaled
roundoff operands. Изменение physical inputs, допусков или каталога не требуется.
Полная physical/discretization acceptance и pilot launch остаются **blocked**
независимо от этих малых документальных исправлений.

## Замечания с воспроизводимыми локаторами

### R1-01 — explicitly separate ratio helper from complete FDR diagnostic

Категория: наблюдение исходника; приоритет medium для frozen measurement contract.
D1 §3, line96: «denominator0/error0 — measured0 с причиной». Это верно для
Results `_ratio` (equilibrium.py:124–135), но не описывает результат всего
`diagnose_stored_equilibrium` для пустого spectrum. `_fit_mu` возвращает
`status=not_measured, reason=empty_represented_spectrum` при capacity<=0
(equilibrium.py:239–244). Затем `fermi=None` (459–464), и FDR inherits μ status,
reason, value=None (527–531). При negative q/nonbracket/algorithm limit тоже
невозможно подменить этот gate нулём helper.

Контраргумент: D1 уже прямо запрещает принимать пустой spectrum; ложный physical
pass не заявлен. Тем не менее frozen output semantics должны быть однозначны.
Самая дешёвая проверка — прочитанные branches, без runtime. Исправить строку:
ratio zero/zero convention применяется только при defined μ/applicability;
в полном reader unavailable μ сохраняет unavailable FDR, а не measured0.
Решение: **изменить**; D2 — только текст, повторная проверка diff/source hashes.

### R1-02 — acoustic paragraph: printed p.4, not p.3

Категория: наблюдение первичных bytes; low/editorial.
D1:48 P-DOS приписывает small acoustic energy transfers §II.A, printed p.3.
У PDF SHA256 `dfabd791bfb2aa4603233e9b545879e07a3bfc63e8906cbc810760726358ea0c`
указанный абзац находится на **printed p.4**, между Eq.(2) и Eq.(3).
Printed p.3 обсуждает basis states. Воспроизведение: `pdftotext -f 4 -l 4 -layout
/tmp/qcl-dev02-lee-wacker-0212059v1.pdf -`. Присутствие такого же p.3 в milestone
не является независимым подтверждением локатора. B1/B2 на printed p.17 верны.
Физическая оговорка про elastic acoustic остаётся корректной.
Решение: **изменить** primary locator при D2/publication; не менять модель.

### R1-03 — name the operands of roundoff branch

Категория: вывод из owning evaluator; low, но нужен перед буквальным freeze.
D1:140 даёт одну формулу с F для rroundJ/rroundC/rroundP без указания prefactor.
Owning metadata acceptance_metadata.jl:248–264 поясняет отличие; actual
observables.jl:314–321 использует для rroundC **unprefactored** signed integral,
а validation.jl:616–628 — prefactored scaled boundary flux для rroundJ;
observables.jl:391–397 — prefactored dimensionless channel power для rroundP.
Relative branch scale cancels, но 1e-12 switch и absolute100*error branch scale
не cancels. Зафиксировать FJ=Φ± с gs/(2π), FC=signed из `_collision_sum` без
prefactor, FP=`_collision_power_bar` с gs/(2π); max по sides/channels. Floor и
порог не менять. Existing owning code не содержит обнаруженного здесь defect.
Решение: **изменить** описание; новых tests/runtime не требуется.

## Независимая проверка физики и bounds

FD formula/particle-number constraint независимо прочитаны на первичной
[странице Smirnov, (2.30)–(2.31)](https://www.iue.tuwien.ac.at/phd/smirnov/node25.html).
Lesser relation независимо прочитана в
[Fotso–Freericks, printed p.8, Eq.(42)](https://www.acsu.buffalo.edu/~hffotso/MyPapers/FrontiersPhys_FDT.pdf).
Scalar/local scope источника не объявляется прямым QCL matrix proof; в общем
orthonormal basis и global μ/T matrix equilibrium identity используется как
явная теоретическая предпосылка. Greater form следует из Keldysh identity.
Web retrieval позволяет проверить формулы/локаторы, но reviewer не получил
independent raw HTTP body hashes для этих двух источников: их D1 hashes остаются
receipt автора, а не моим independently hashed byte evidence.

Уже существующие три local primary PDF hashes проверены непосредственно:
Lee–Wacker `dfabd791bfb2aa4603233e9b545879e07a3bfc63e8906cbc810760726358ea0c`;
Wacker `091a39824c3fb4b5f1f3b0f0659d4a99663b48b6949806aa8586710b6d1d937b`;
Bosco `b103b3da9fa977d1dc682d1e2caf96d74b5f081731e4db0da944af675a58dc70`.
Lee–Wacker B2 density of states и Wacker printed p.2 Eqs.(2)–(6)/finite-basis
paragraph прочитаны адресно из этих bytes. Bosco physical units/source caveat
взяты из опубликованного SCI02 passport; повторная визуальная проверка Fig.3
в данном R1 не выполнялась, новой experimental validation не заявляется.

Для фиксированного A и nonzero ||A||W выполняется reverse triangle inequality
для объединённого occupied/empty residual vector. FD derivative
|df/dμ|<=1/(4kBT) даёт |Δη|<=sqrt(2)*uμ/(4kBT). Независимая SI арифметика:
kBT70K=0.006032133283501625 eV; coefficient=58.61166754393028 eV^-1.
Это только μ construction при фиксированном spectrum; finite-precision number
bracketing uncertainty и model/window changes не превращены в total μ bound.

Sheet bound следует из |Tr X|<=sqrt(Nb)||X||F и Cauchy–Schwarz по положительным W.
Density bound следует из |χᵀXχ*|<=||χ||²||X||F, затем той же Cauchy–Schwarz.
Размерности /L0² и /L0³ и coherence projection совпадают с actual observables.

Current identity проверена независимо раскрытием скобок:
Sp=(1-f)Γ−δS, Sn=fΓ+δS, N=fA+δN, P=(1-f)A+δP. Члены f(1-f)ΓA сокращаются
без commutation; остаются именно три члена §5.3. Trace Frobenius inequality и
weighted Cauchy дают приведённый bound для complex per-side represented trace.
W уже содержит gs/(2π), повторный prefactor не нужен; J0 положителен в owning
ScaleSystem. Bounds conditional exact-arithmetic, не новый product oracle,
не continuum/roundoff/nonlinear certificate. Такого полного reducer ещё нет.

Backward Dyson→forward bound требует ||D^-1||, а coupled raw residual→solution
bound требует доказанной conditioning/contraction на области. Исторический
residual ratio, малый mixed step и normalized charge этого не дают. D1 правильно
оставляет q/LQ/inverse Jacobian/tail/truncation/cross-axis remainder unknown.
Additive coefficients1 соответствуют triangle inequality только при отдельно
доказанных component upper bounds/remainder; D1 не выдаёт sensitivities за них.

## Strict policy, slots и готовность

Actual acceptance_metadata, validation, final_audit, poisson, grids, observables,
Results reader, typed defaults и Research tolerances прочитаны. Проверены особо:
rD stored1e-11/rA1e-9 versus candidate rK1e-8; candidate λ без fitted normalization;
unweighted spectral/Keldysh versus weighted FDR; rJ floor в **scaled flux** versus
rJchange floor1e-12 **A/m²**; signed channel integral; pointwise imaginary branch;
PSD64Nb eps construction allowance; worst-k spectral sum; edge/tail heuristics
не outside-domain bound; explicit not_measured error_budget. R1-01/R1-03 выше
уточняют descriptor, не предлагают менять evaluator или scientific tolerances.

P1/science catalog допускает ровно13 attempts/936 execution node-hours:
B0/E1/P1/K1, W/Z/B/A/Q, C, R×2, H×1; каждый<=72h, concurrency<=2 и все existing
per-attempt/shared byte caps. D1 распределяет измерения только по этим slots,
B0 first и relevant strict closure before routine accuracy refinement. W и C
имеют разные окна; D1 правильно запрещает называть C−W pure k-cutoff error.

H +ΔE/4 сохраняет шаг и ширину окна chosen single approved final variant;
это разрешённый заранее H phase protocol, без нового solver/model/mixing.
Committed Runner ScientificVariant.overrides→`_deep_merge!` и numerical parser
поддерживают energy_min/max/nodes; Core build_grids принимает конечные ordered
endpoints с тем же trust margin. Поэтому предложение source-expressible.
Это **не** проверка resolved plan или native execution. SCI09/12 должны сохранить
exact numeric endpoints/units/NE/ΔE/identity/hash до submit, post-H raw не доступен
для выбора A1 criteria/candidate. H не доказывает missing tails/conditioning.

Source/design tickets SCI04/O08-03, SCI06 reducer design+literal oracle contract,
SCI12 mappings/tail/H и SCI03-ACC derivation basis **готовы к поручению** после
узкого D2 CP-DESIGN. Actual reducer implementation требует собственного D→I→R.
Physical accuracy acceptance **blocked**: finite εQ/coefficients/bounds отсутствуют.
Pilot runtime **blocked**: SCI07/08 enforceable guards/fresh admission и SCI09
exact plans не установлены. Missing native evidence не блокирует source review
и не является основанием повторять уже утверждённое B/G1/S1 permission request.

## Fourteen owning SHA256, independently checked

| Locator | SHA256 |
| --- | --- |
| Core src/numerics/reference/acceptance_metadata.jl | `4d1880b7d6e475534d0bbfa229ced25dd40b062f674ec8a2ea86b45e0db1dd86` |
| Core src/numerics/reference/validation.jl | `29e1b92daaed51f35d676bab8f70d60836fd0b5dc65c25c38a58646e0395005a` |
| Core src/numerics/reference/final_audit.jl | `8384e2022de0c3c912384c15f6e5b3697879dac984d554f38f0d5bc2d916a673` |
| Core src/numerics/reference/poisson.jl | `8989ced0c4adc67e5d553b98863cd8ee3584705546ba445565cb5da0e7130645` |
| Core src/numerics/reference/grids.jl | `71c4cff98cbefb834eea818067549dc150cb0cd18141854f27dfbd549862d18e` |
| Core src/numerics/reference/positivity_diagnostics.jl | `796cdde49e736245bbd3cf53aab96b33368560e7c1518e27e96ba2d0d67d8039` |
| Core src/physics/observables.jl | `b147e41dcb04bb39792a30e0092f9298a64813d87cc5411037c1958bd56b4b9f` |
| Core src/domain/types.jl | `f428a6c7ce2c7d4796d6be2983decffcdbfc25f21ec400a600038863f673e71b` |
| Core src/domain/scaling.jl | `2049ea6638da871c406718dad9f1aa4eb5cee68f4ce8941a8270e050dd7eb9f0` |
| Results src/qcl_negf_results/equilibrium.py | `3f8ee56390741e15bc2c709de67d4b0c80260733c99752d8fbbb4f538e3042e6` |
| Research docs/reference-2019-model-passport.md | `653dc08a55575043b3b95ee43c0ff5413914f39ae6b554c9993345514d5f8f3c` |
| Research config/model/reference-2019-70k.yaml | `78444c7a358fabef315e07e028d3d65f65fec07efd119ac9ca238cc25c110829` |
| Research config/policies/analytical-diagnostic.yaml | `fbbb2b4afe9eac694e71b29c77883930072416250f0f75e86d8ffaf3821c49b0` |
| Research config/studies/equilibrium-0-70.yaml | `2fde52250d6ab85240d556f8c59b70ce1a065e04800d531dea95d9a2f3a8c0e9` |

## Итог

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| D1 точно freezes actual near-zero FDR status | _ratio vs diagnose/_fit_mu branches | Empty spectrum описан двусмысленно | изменить |
| Local μ/density/current bounds mathematically valid | Independent algebra, source measures/scales, SI arithmetic | Fixed represented state, not total forward accuracy | сохранить |
| Strict policy/physics/S1 caps preserved | 14 hashes + actual evaluator/P1 catalog | Actual runtime/resolved plan не создан | сохранить |
| H+ΔE/4 source-expressible within approved H | Committed Runner override/parser + Core grid + P1 H phase | SCI09/12 exact plan/admission ещё нужны | сохранить |
| Полная scientific/discretization acceptance получена | Missing εQ/conditioning/tail/truncation evidence | Source design не численное решение | данных недостаточно |
| Pilot submit уже READY | Missing guards/fresh admission/exact plan | Runtime gates отдельные | данных недостаточно |
| Bounded source/design handoff полезен | Concrete SCI03/04/06/12 tickets | Узкий D2 по R1-01–03 до freeze | изменить |
