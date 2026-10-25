# DEV05 I — complete final U/G functional oracle, frozen source packet

Дата: 2026-10-19. Статус: **реализация передана CP-CODE; runtime not_measured**.
Owning Core identity из задания координатора:
`f5b73369a96d1225bd96fb34f5262c8dcf965f86`, ветка
`codex/review-closure-final-state-oracle`. Автор не запускал Git; root HEAD,
status и gitlink receipt остаются ответственностью координатора. Свежая
проверка bytes ниже подтвердила 18/18 primary source SHA из D receipt.

## Deliverables и frozen identity

Единственный изменённый owning path:
`test/numerics/final_state_alignment_oracle.jl`.
Managed root: `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.

* Test: 38,711 bytes, 747 lines, SHA256
  `6d0db8b15300dce5350bf1bb282cef008da494be57bd96b23780ab1b314049a9`.
* Full added-file patch: `/tmp/qcl-dev05-final-state.patch`, SHA256
  `27e907a3423dda4b3a4987b1d98c04593fd3d9f4db7f95d44f0b852020675925`.
* Approved D: `/tmp/qcl-final-ug-design.md`, SHA256
  `96c2c50a104b984c72603fa7066986d9bf6c02a8e59ba1ce0df9f06e321da162`.
* Independent CP-DESIGN: `/tmp/qcl-final-ug-design-review.md`, SHA256
  `11900d840a7155ac3a28161f4d0f5f16ac5e3cdb810e37e18c4fc9a5e834c52b`.

Полный patch — source artifact, не runtime receipt. Production, existing
`fresh_candidate_residual.jl`, owning docs, manifests, S1 inputs, model/gates,
SCBA/outer loops/retries/mixers не менялись. Scope-escalated copy разрешил
запись ровно owning test в managed worktree; human permission не запрашивалось.
Original dirty checkout не изменялся.

## Прочитанные инструкции и выбранный этап

Root AGENTS, architecture, implementation entrypoint, DEV05 handoff,
qcl-physics-audit с physics-checks и test-driven-development с
writing-good-tests. Компонентных AGENTS под Core не найдено. Этап — только
новая test-only реализация approved design; не вычислительный эксперимент.
Git/runtime/import/setup/test budget автором использован **0**. Литературные
web reads не нужны для literal source-operator algebra этого контракта.

TDD: production code отсутствует; existing API может оказаться GREEN first.
Намеренные negative inputs и oracle substitutions включены в новый тест,
но их RED/GREEN исходы ещё не наблюдались. Только координатор/назначенный
исполнитель может потратить общий L-JL max2/120s/1CPU/2GiB/16MiB TMP/2MiB logs.
Автор не утверждает, что тест проходит, ловит mutation в runtime или закрывает
CP-CODE. Полный suite запрещён текущим конечным поручением и не выполнялся.

## Материализованный контракт

`manufactured_problem`/`analytic_basis_phase`: адресная копия accepted static
carrier recipe, без include чужого testset. Единственное заранее approved
отличие physical donor target `(1e16/64) m^-2`. Использован checked
`build_problem(...;localization=:none,validate_static=true)`, defaults models
и options. Явно проверяются все carrier grid/profile/basis/kernel/shift/model
поля. Для Poisson literal L3 вводится fatal precondition exact unit wZ и
uniform positive ND, а target/profile/total donors дополнительно ограничены
γ16/γ32 conversion chain. Несовпадение останавливает fixture, а не расширяет
physical tolerance.

`independent_literals`/`literal_state`: literal SI constants и causal quadratic
задают все шесть E/k блоков rank1, φ², nonzero U, n, все Green/Σ families.
Only active support (e2,k1) даёт A/lesser/greater; пять иных retarded узлов
ненулевые и входят в Dyson. PSD/Pauli/causality/partner/family-sum/metadata
assertions не подменяются нулями. Все family/state/variant/candidate/history
arrays проверяются на alias; scoped immutable problem carrier разделяется.

`Ball`/`CBall`: направленное RoundDown/RoundUp каждого scalar operation на
384-bit BigFloat; rational/inactive branch denominator, radicand, normalized
metric denominators и target positivity guards. Actual Float64 g трактуется
как exact input и независимо проверяется polynomial defect. Constants/root
ledger≤16; target complex products γ16, six-entry norm/charge/projection γ32,
Dyson comparison γ64. ηh измеряется только из independently checked static
inputs относительно literal h; T-coefficients дают actual-side exact TGT†
и γ16 implementation error, не fitted final residual. Все metric enclosures
freeze до actual candidate/fresh/final API calls.

`poisson_enclosures`: literal three-row L3/b и exact bordered U/zeta/neutrality
до tiny direct map; actual returned Up independently проверяется backward
residual и forward bound из eigenvalue3 на zero-mean subspace + gauge.
Нет предположения точности LAPACK из одного eps. Fresh validation затем
самостоятельно повторяет map. Source residual floors и norms сохранены.

`manufactured_solution`: complete typed SCBAResult/FixedPointAuditCandidate/
NEGFSolution + SCBA ν1…4/outer μ1…3. Status descriptions явно manufactured.
История — constant algebraic sequence; residual entries являются independent
arithmetic upper bounds, не вымышленными solver measurements. First predecessor
Inf/NaN; дальнейшие differences0 выведены из identical samples. Current J
получен из same-field public flux SI conversion и повторяется, с independent
absolute cancellation bound; population из тех же fields. Empty scattering
roundoff0 означает empty maximum, Hilbert measurement not applicable.

`check_final`: actual public fresh_fixed_point_metrics и validate_solution,
explicit `_validate_solution_metrics`, fixed inventory 41 finite gate metrics,
full fresh subset equality, independently enclosed quantitative rD/rA/rK/rΣ/
charge/Poisson/r_sum и exact message failure names. Empty provisional report
явно unassessed; произвольного dict pass sentinels нет.

| Complete input | Exact expected failed-key set |
| --- | --- |
| Aligned U*,G* | `{r_sum}` |
| N1:2U*,G* | `{r_D,r_D_candidate,r_U,r_sum}` |
| N2:U*,G0 | `{r_D,r_D_candidate,r_sum}` |

N1/N2 сохраняют last stored small rΣ и требуют actual fresh small rΣ.
N2 сохраняет ровно healthy final U; rU обязан проходить. Supplemental controls
на copies metrics отвергают подстановку healthy/old residual values по fixed
negative enclosures; подстановка predicted U отвергается retained-input и
rU checks. Такие copies не подаются production evaluator. Optional N3 не
добавлен: минимальный approved DEV05 контракт содержит N1/N2; existing fresh
pole oracle остаётся независимым отдельным primitive, без дублирования.

## Source-only проверка автора и ограничения

Fresh byte/hash comparison 18/18 D primary paths; test mirrors installed
bytes; newline и trailing whitespace проверены. Получен полный added-file
patch без Git. Julia parser/import/test не запускались; возможные Julia
syntax/dispatch/platform issues должен выявить CP-CODE и bounded executor.
Координатор выполняет Git diff/status и freeze checkpoint, автор их не делал.

Независимая review организуется root на frozen artifact; self-review не
назван независимым evidence. Healthy — только aligned coupled discrete raw
map. Spectral quadrature намеренно неадекватна, global report FAIL только по
r_sum. Ни SCBA iteration runtime, ни discretization adequacy, ни experimental
validation не измерены; S1 0mV/70K/five channels/e–e none не получает приёмки.
Optimized/cavity/five-channel raw map/serialized lineage/audit-error/process0/
alpha-step controls остаются отдельными SCI04 dispositions.

## Узкая correction по independent source review

Полностью прочитан `/tmp/qcl-dev05-code-review.md`, SHA256
`37b6c3a016ff1e4e86bf92760fd995bd3211d54c0f075674f8db0d262b04c95d`;
применён receiving-code-review workflow. Finding проверен по actual
`_solution_validation_limits`: наличие finite metric не гарантировало
сохранение corresponding currently-passing limit.

Добавлено ровно 11 строк в три места единственного owning test:
module-scope literal `CANDIDATE_GATES` (три ключа); once-per-testset comparison
38 unconditional actual limit keys с `setdiff(Set(GATES),Set(CANDIDATE_GATES))`;
для каждого actual healthy/N1/N2 report comparison actual limit keys с literal
`Set(GATES)` из 41 ключа. Expected inventory остаётся independent literal;
empty metrics dictionary используется только для limit inventory query,
никогда для acceptance evaluation.

Narrow delta `/tmp/qcl-dev05-inventory-delta.patch`; previous test сохранён в
`/tmp/qcl-dev05-pre-inventory.jl`, previous report и full patch сохранены с
suffix `-pre-inventory`. Delta содержит только эти 11 additions; исходные
41 metric/failure/enclosure/field/noalias assertions не изменены. Physical
limits/model/D остаются unchanged. Новый freeze требует independent delta
approval до first bounded GREEN; Julia/Git/import/test invocation по-прежнему0.

## Primary bytes receipt (не revision lock)

| Path относительно Core | SHA256 |
| --- | --- |
| src/domain/types.jl | f428a6c7ce2c7d4796d6be2983decffcdbfc25f21ec400a600038863f673e71b |
| src/domain/numerical_convergence.jl | 0a0bd0d1d84b54aac51dd534758240923b19cb701f17f213ac657a4bea2bf053 |
| src/numerics/reference/final_audit.jl | 8384e2022de0c3c912384c15f6e5b3697879dac984d554f38f0d5bc2d916a673 |
| src/numerics/reference/validation.jl | 29e1b92daaed51f35d676bab8f70d60836fd0b5dc65c25c38a58646e0395005a |
| src/numerics/reference/poisson.jl | 8989ced0c4adc67e5d553b98863cd8ee3584705546ba445565cb5da0e7130645 |
| src/numerics/reference/basis.jl | 6f58663e6a3276744cd2d0b72edac103f42150b4588468efa4136f5f0685725e |
| src/numerics/reference/periodicity.jl | b7c3b7098ae1ed79492f6a84ddd1e55ba53e14fa703c264c2c4a8ff0f3864b35 |
| src/numerics/reference/greens.jl | 25f476e3ac4f4c282433f55286ded0893994ac9bb1ce8c0ab17fe1c3b288f5b9 |
| src/numerics/reference/grids.jl | 71c4cff98cbefb834eea818067549dc150cb0cd18141854f27dfbd549862d18e |
| src/numerics/reference/kernels.jl | ad3e5172d80eeaebab496d5e22a82b4db960a66e27ee4bcb3a234b987dbf055d |
| src/physics/observables.jl | b147e41dcb04bb39792a30e0092f9298a64813d87cc5411037c1958bd56b4b9f |
| src/numerics/optimized/production_solver.jl | ae776c29b611a84553116d9b25be8e04e2c16b7ff258c5ca5b11e03f555d8eaa |
| src/numerics/optimized/certification.jl | de2dd971a8d466b53b0b2b4c682e085c743cd789b7e9e0c839f0a9042c5a13e3 |
| docs/src/development/review_oracle_contracts.md | 673bc9641318b01ffe29bcbe6edc6198b5e243a0d246af8072a2190a70e072f2 |
| test/physics/nonzero_public_current_oracle.jl | 17fed2fae5b45549c65cec576cc108f68922a04e3830c0246313ccafd4ee8d01 |
| test/physics/nonneutral_periodic_poisson_assessment.jl | 9aab7a4eea3a7fcb93033d2c9f6f3b420f6b1872843168e0deb98461f2602730 |
| test/numerics/fresh_candidate_residual.jl | 8ab459b5be0c39f96839b862aad38e1dbcd6a8dc633770838fd239c8a871a6a0 |
| test/numerics/independent_nonlinear_and_continuum_anchors.jl | a6a826980fe13de96376383251329da4d3ff6e3225a5b8907b3dc83ed9cdeaec |

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Complete final U/G functional assembly реализована | Новый frozen owning test + literal roots/L3/full fields + exact failed sets | CP-CODE и runtime ещё не выполнены | дополнительно измерить |
| Healthy означает all-gates pass | Независимый r_sum и обязательный exact global FAIL | Finite spectral grid deliberately inadequate | изменить |
| Wrong U/stale G не маскируются small Σ | Full-interface N1/N2 + bounds + retained-small history/fresh assertions | Пока source, не runtime result | дополнительно измерить |
| S1/production physics и thresholds сохранены | Единственный новый test path; 18 primary bytes hashes совпали | Root Git diff выполняет координатор | сохранить |
| Научная приёмка получена | Нет solver/discretization/experimental evidence | Runtime not_measured | данных недостаточно |
