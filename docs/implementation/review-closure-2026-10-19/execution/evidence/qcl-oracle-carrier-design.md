# DEV02 correction: complete manufactured carriers for O08-02/O08-04

Статус: **DESIGN_CANDIDATE; fresh independent CP-DESIGN pending**.
Автор `/root/oracle_carrier_design`, D ultra, 2026-10-19. Единственный
output автора — этот файл. Source edits, imports, Julia execution, tests,
solver, installation, SSH и spawn: **0**. Это correction принятого паспорта,
а не runtime receipt. Implementation ждёт fresh CP-DESIGN этого correction.

## Нейтральный brief первому reviewer

Вопрос: допускают ли реальные публичные конструкторы и builders данные
паспорта O08-02/04? Для каждого public current/Poisson/assessment вызова
проверить минимальные размеры, совпадение всех осей и полной typed assembly,
меру, единицы, независимый численный RHS, near-zero/tolerance и negative
controls. Определить точную границу synthetic routing и scientific state.
Не предполагать заранее наличие или отсутствие дефекта реализации.

Первичные inputs, без ссылки на чужой диагноз:

- Core commit `a8d2c0de21dfdce3ed3c7c585c555656443f6d89`.
- `docs/src/development/review_oracle_contracts.md`, O08-02/04.
- `src/domain/types.jl::NumericalParameters, NEGFProblem, GreenState,
  SelfEnergyFamily, SCBAResult, NEGFSolution`.
- `src/numerics/reference/solver.jl::build_problem`;
  `grids.jl::build_grids, build_profiles`;
  `basis.jl::build_localized_basis, _build_unlocalized_basis`;
  `hamiltonian.jl::build_bdd_hamiltonian`.
- `src/physics/observables.jl::energy_resolved_current, boundary_flux,
  bond_current, _electron_density_bar`;
  `src/numerics/reference/poisson.jl::solve_periodic_poisson`;
  `validation.jl::_validate_solution_metrics, _solution_validation_limits`.
- Root `docs/implementation/review-closure-2026-10-19/development.md`,
  DEV02/04/06 и L-JL envelope.

Reviewer должен самостоятельно раскрыть scalar sums и basis reconstruction
до чтения численных выводов ниже. Accepted/correction/blocked выдать с
локаторами; прежний CP-DESIGN не наследуется автоматически.

## Фактический source и полномочия

Active root `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`,
HEAD `04eecba1ea795a7c8861c4bfd0bb5aa49f093ee6`. Root status при первом чтении:
Core untracked content, Results modified, checkpoint modified, untracked
INT01 summary. Core HEAD указан выше; tracked source чист. При последнем
чтении Core status — два новых test files другого исполнителя:
`test/numerics/keldysh_literal_matrix_oracle.jl` и
`test/numerics/principal_value_independent_oracle.jl`. Они не читались как
источник RHS и не менялись. Gitlinks/root branch не переключались.

Прочитаны architecture, owning CONTRIBUTING, qcl-physics-audit/physics-checks,
handoff DEV02/04/06. Parent уточнил: запрет unchecked constructors означает
запрет обходить доступные проверки и оставлять несогласованные fields.
Required plain `GreenState`/`SelfEnergyFamily` допустимы после полного
test-local checking assembly. Новый production factory ради fixture не нужен.

Важные SHA256 (source files этого commit, не второй lock-файл проекта):

| Path | SHA256 |
| --- | --- |
| `docs/src/development/review_oracle_contracts.md` | `dca2f3c2c94e6a6db983d2d6d4737a08eb240b4181bdfd22fe978e165c059df2` |
| `src/domain/types.jl` | `f428a6c7ce2c7d4796d6be2983decffcdbfc25f21ec400a600038863f673e71b` |
| `src/numerics/reference/solver.jl` | `3a0f68b0a7774bbe363f2aeaef2288b20a5f7b26fa02a1f7a13e5853a5919636` |
| `src/numerics/reference/grids.jl` | `71c4cff98cbefb834eea818067549dc150cb0cd18141854f27dfbd549862d18e` |
| `src/numerics/reference/basis.jl` | `6f58663e6a3276744cd2d0b72edac103f42150b4588468efa4136f5f0685725e` |
| `src/numerics/reference/validation.jl` | `29e1b92daaed51f35d676bab8f70d60836fd0b5dc65c25c38a58646e0395005a` |
| `src/physics/observables.jl` | `b147e41dcb04bb39792a30e0092f9298a64813d87cc5411037c1958bd56b4b9f` |
| `src/numerics/reference/poisson.jl` | `8989ced0c4adc67e5d553b98863cd8ee3584705546ba445565cb5da0e7130645` |
| `src/numerics/reference/hamiltonian.jl` | `7cfea79a21f853754b0edf5cd15922c03457c279b69c6f5a228e2e4c9b6b53a4` |
| `src/domain/scaling.jl` | `2049ea6638da871c406718dad9f1aa4eb5cee68f4ce8941a8270e050dd7eb9f0` |

## Выбранное изменение паспорта

`NumericalParameters` оба конструктора требуют `Nz≥3, Nb≥1, P≥1,
NE≥3, Nk≥2, Nφ≥4, Nqz≥3` (`types.jl:181–284`). Поэтому прежний O08-04
`NE=2`, а также coherence `NE=Nk=1`, нельзя протащить в public API через
фиктивные numerical metadata. Свободные dyadic weights прежнего паспорта
тоже не являются весами `build_grids`. Production constructor не менять.

Выбор: complete problem через `build_problem(validate_static=true)`;
все actual grids сохраняются. Для O08-04 минимум для two-state example:
`Nz=3,Nb=2,NE=3,Nk=2,P=1,Nφ=4,Nqz=3`, basis `:none`.
Для truncation отдельный такой же builder с `Nb=1`, без нормировки G.
Для O08-02 сохраняется принятый direct N=4 constant-source RHS. Для его
assessment envelope выбран `Nz=Nb=4, localization=:real_space`, поскольку
это даёт прозрачный constant-density complete carrier без ручного BasisData.
Это минимальный full-coordinate carrier на retained four-cell fixture,
не утверждение глобального минимума по всем возможным manufactured bases.

Физический target S1 (0 mV, 70 K, LO/acoustic/impurity/IFR/alloy,
electron–electron=none), tolerances и принятие science не меняются.
Manufactured carriers ниже **не S1 model**. Для current/routing functional
они явно выбирают microscopic `ScatteringOptions(false,false,false,false,false)`.
Это ограничение области fixture, не свидетельство all-five acceptance;
не переносить этот выбор в production/frozen research plan.

## Единственная согласованная процедура physical/numerical construction

Параметризовать helper только `(Nz,Nb,localization)`. Все quantities перед
`PhysicalParameters` уже имеют типы owning fields; нельзя подставлять kwargs,
которых у этого positional checked constructor нет.

```julia
layers = Layer[Layer(d = (Nz*10.0) * u"nm", material = :manufactured_uniform,
    x_Al = 0.0, Eᶜ = 0.0u"eV", mᶻᵣ = 0.067,
    m_parallelᵣ = 0.067, εᵣ = 1.0, doped = true)]
p = PhysicalParameters(layers,
    (Nz*1.0e16) * u"m^-2", 1.0, 0.0u"V/m", 0.0u"m", 0.0u"eV",
    70.0u"K", 70.0u"K", 12.9, 10.89, 0.0367u"eV",
    2.0e8u"m^-1", 2.0e8u"m^-1", 1.0e-10u"m", 9.0e-9u"m",
    7.0u"eV", 5317.0u"kg/m^3", 5240.0u"m/s",
    nothing, nothing, 2, typeof(1.0u"m")[])
n = NumericalParameters(N_z=Nz, N_b=Nb, P_basis=1,
    E_min=-0.1u"eV", E_max=0.1u"eV", N_E=3, M_E=0.05u"eV",
    k_max=1.0e8u"m^-1", N_k=2, N_φ=4,
    qz_max=1.0e8u"m^-1", N_qz=3, η_seed=0.001u"eV")
s = ScaleSystem(E₀=0.1u"eV", L₀=10.0u"nm")
scattering = ScatteringOptions(LO=false, acoustic=false,
    impurity=false, IFR=false, alloy=false)
problem = build_problem(physical=p, numerical=n, scattering=scattering,
    scales=s, localization=localization, validate_static=true,
    physical_models=PhysicalModelOptions())
```

The explicit `* u"..."` products preserve Unitful dimensions. No `NEGFProblem`, `ModelGrids`,
`MaterialProfiles`, `BasisData`, `KernelSet` positional reconstruction.
No `validate_static=false`, no post-builder mutation of their arrays.

Layer mass follows the source well mass; other inactive material constants
follow `reference_parameters` values. εr=1 and whole-cell doping are stated
manufactured choices. `Nsheet*L0²=Nz`, `Lp/L0=Nz`, thus NDbar=1 on every
cell. Empty interface list means a uniform material, not missing data. Alloy
parameters are `nothing` because alloy disabled, not unknown values set zero.

Builder outputs to assert independently (all comparisons scaled/dimensionless):

| Owning fields | Expected / reason |
| --- | --- |
| grids.x,wˣ | `(.5:1:Nz-.5)`, `ones(Nz)`; Δx=1 |
| ε,wᴱ,trusted | `[-1,0,1]`, `[1/2,1,1/2]`, `[false,true,false]` |
| κ,wᵏ | `[0,1]`, `[1,3]/(16π)` from annular edges `[0,1/2,1]` |
| qᶻ,wᑫᶻ,φ | `[-1,0,1]`, `[1/2,1,1/2]`, `[0,π/2,π,3π/2]` |
| profiles | Ec=0, both mass ratios=.067, εr=1, ND=1, xAl=0, layer_index=1 |
| kernels | enabled empty; K/qK empty; FLO shape `(3,Nb,Nb)` zero because LO disabled |
| four shifts | bias pair I3; LO nodal pair below; matrices 3×3 |
| discretization/models | `:nodal_linear`; default fixed/parabolic/thermal/e-e none |
| scales | E0=.1eV, L0=1e-8m, λP/J0 independently checked below |

With δ=0.0367/0.1=.367, retained literals for the LO maps are
`W+=[1-δ δ 0; 0 1-δ δ; 0 0 0]`,
`W-=[0 0 0; δ 1-δ 0; 0 δ 1-δ]`.
Physical-model inactive options are not replacements for missing scientific
inputs. `validate_problem(problem).passed` is a static carrier check only.

## Independent constants, basis and every retained current field

Expected path uses literals, not `CODATA`, `_C̄`, `_scaled_physics`, scale
readback, BDD/Green builders or current helpers:

```text
eSI=1.602176634e-19 C, hbar=1.054571817e-34 J s,
m0=9.1093837139e-31 kg, eps0=8.8541878128e-12 F/m,
E0J=.1*eSI J, E0eV=.1, L0m=1e-8 m, mr=.067,
J0ref=eSI*E0J/(hbar*L0m²),
λref=eSI²/(eps0*E0J*L0m),
t=hbar²/(2*m0*mr*E0J*L0m²).
```

First compare actual scale fields against these independent expressions.
For current normalize actual values with **J0ref**, resolved with
`J0ref/E0eV`, not actual scale fields.

Uniform three-cell Dirichlet H is `t*[2 -1 0; -1 2 -1; 0 -1 2]`.
Its first two eigenpairs are nondegenerate:

```text
φ1=(1/2,1/√2,1/2), E1=(2-√2)t,
φ2=(1/√2,0,-1/√2), E2=2t,
Φ0=[φ1 φ2], χ0=Φ0.
```

Do not assume LAPACK chooses a fixed phase at tied maximum endpoints of φ2.
Let `d[a]=dot(Φ0[:,a],Φactual[:,a])/abs(dot(...))`, `P=Diagonal(d)`.
Assert `|dot|≈1`, `Φactual≈Φ0*P`, χactual≈Φ0*P independently before any
current call. Then transform **every** literal Green/family block as
`Xactual=P' * Xliteral * P`. This uses actual basis only to remove arbitrary
column phases; the expected current RHS remains the retained scalar below.
Do not derive expected RHS by reconstructing with actual Φ or Hgrid.

Full basis inventory from builder, with matrices transformed by P as needed:

| Field | Independent value / provenance |
| --- | --- |
| localization | `:none` |
| Φ,χ | Φ0P, Φ0P |
| centres,spreads | `[3/2,3/2]`, `[1/√2,1]` |
| overlap eigenvalues,κ | ones(2),1 within arithmetic budget |
| H0 | diag((2−√2)t,2t) |
| Z | `P' * [3/2 -1/√2; -1/√2 3/2] * P` |
| M⁻¹ | I2/mr |
| T+ | `-t*P' * [1/4 1/(2√2); -1/(2√2) -1/2] * P` |
| T− | T+' |
| window_eigenvalues,Egrid0 | `[E1,E2]`,2t (the :none builder stores cell eigenvalues) |
| r_orth,r_eigen | builder-computed residuals; require finite and existing static gates, never overwrite with 0 |
| three r_translation fields | builder 0 for :none; excluded from PzP translation gates |

## O08-04 literal current, actual 3×2 measure

All arrays have full shape `(3,2,2,2)`. In literal analytic basis, for each
`(e,m)`, `a=[1 2;3 4;5 6]`:

```text
Q=[2 i;-i 1], B=[1 i;-i 2], F=I2/2, D=I2,
G< = i*a*Q; G> = -i*I2;
GR = -i*(a*Q+I2)/2; A=a*Q+I2;
Σ< = i*I2/2; Σ> = -i*B; ΣR=-i*(B+I2/2)/2.
```

Both sets obey their stated Keldysh identities; `-iG<`, `iG>`, A and the
correlation matrices are PSD. This family is a **manufactured current
functional input**, not the self-energy produced by problem.kernels or an
embedding solve. It is not Dyson/SCBA/Poisson solution evidence.

To fill `GreenState.condition_number` and `dyson_scale` without unrelated
ones/zeros, use the actual declared D for this problem/family, not a fake
Dyson inverse of literal GR. h is independently diagonal in the analytic
basis: `h_jm=E_j+t*κ_m²`, and `ξ_j=ε_e-h_jm`:

```text
D_em=[ξ1+3i/4 -1/2; +1/2 ξ2+5i/4],
τ=ξ1²+ξ2²+21/8,
d2=(ξ1*ξ2-11/16)² + ((5ξ1+3ξ2)/4)²,
q=sqrt(max(0,τ²-4*d2)),
condition_number[e,m]=sqrt((τ+q)/(τ-q)),
dyson_scale[e,m]=max(sqrt(ξ1²+9/16)+1/2,
                       sqrt(ξ2²+25/16)+1/2).
```

The max(0,...) only protects analytic singular-value discriminant arithmetic,
not a scientific PSD repair; reject negative discriminant beyond the stated
arithmetic budget. D is nonsingular because its positive-definite imaginary
Hermitian part is `(B+F)/2`. Assert all six metadata entries finite/positive,
matching shape. No assertion of small Dyson residual for this fixture.

Before positional `GreenState(GR,Gl,Gg,A,κD,sD)` and
`SelfEnergyFamily(SR,Sl,Sg)`, test-local checking helper verifies:
all arrays exactly full shape/ComplexF64; matrices metadata shape `(3,2)`;
all finite; no aliasing between fields; all basis phase mappings; Hermitian A;
Green/family Keldysh identities; stated PSD signs; analytic κD/scaleD fields.
This checks all plain-container fields; it does not upgrade the input to a
Dyson solution. Use independently expanded matrix entries; don't call target
Green/self-energy helpers to produce expected arrays.

Independent scalar trace expansion gives
`tr(B*aQ−F*I)=a*(2+1+1+2)−(1/2+1/2)=6a−1`, so

```text
S=[5 11;17 23;29 35],
Σ_m wk[m]*S[e,m]=[38,86,134]/(16π)=[19,43,67]/(8π),
jE_expected=[19,43,67]/(8π²) * J0ref/E0eV,
Σ_e (E0eV*wE[e])*jE_expected[e]=43/(4π²)*J0ref,
eSI*boundary_flux_expected=43/(4π²)*J0ref.
```

Each public API gets its own assertion against these retained literals.
Also assert Unitful dimensions/convertibility in A/m²/eV, m⁻²s⁻¹, A/m².
Physical energy weights are `[.05,.1,.05] eV`, not just wE.

## O08-04 coherence and genuine truncated carrier

Reuse the same `Gl=i*aQ` and actual 3×2 axes; no NE=Nk=1 shortcut.
With analytic Φ0:

```text
Re[(Φ0*(iQ)*Φ0')[2,1]]=-1/2,
Re[(Φ0*(iQ)*Φ0')[3,2]]=-1/2,
Σ_em wE[e] wk[m] a[e,m]
  =((1+6)/2+(3+12)+(5+18)/2)/(16π)=15/(8π),
bond_expected=[1,1] * 15t/(8π²) * J0ref.
```

Both bonds happen to agree for these two sine columns and this manufactured
field. This is a derived fact here, not an acceptance condition of spatially
uniform J in a finite basis. No periodic seam returned or invented.

Diagonal-only array keeps `G11=2ia,G22=ia`, zeros just the originally nonzero
coherences, and gives both bonds zero. This is a deliberate input control,
not an optimization proposal. For truncation construct a **new checked**
`build_problem(Nz=3,Nb=1,localization=:none)` with the same physical/numerical
axes; prove its sole eigenvector equals φ1 up to phase. Supply full array
shape `(3,2,1,1)`, `Gtrunc=2ia`. Both bonds are zero because the reconstructed
coordinate entries are purely imaginary. Do not keep Nb=2 numerical metadata,
mutate basis fields, renormalize charge, or call it the same finite-basis
physical state. This tests exactly the derived loss of this coherence.

Comparison budget inherited from current passport/finite-chain regression:
`atol=2e-14,rtol=2e-13` on **scaled** currents, not SI amperes. Use the same
small arithmetic budget on phase-aligned analytic basis entries (dimensionless)
and scalar scale ratios; existing validate_problem gates remain authoritative
for static reports. This is a regression policy, not new physical tolerance
or a proven LAPACK-specific forward bound. Near zero use absolute branch.

Required retained-RHS negative distinctions:

| Deliberate wrong operator/input | Difference independently forced |
| --- | --- |
| reverse current sign | all nonzero resolved/integrated coefficients change sign |
| omit 1/(2π) with gs=2 | actual result multiplied by 2π |
| omit wk[1] | resolved coefficient loses `[5,17,29]/(16π²)` |
| omit wk[2] | loses `3*[11,23,35]/(16π²)` |
| omit wE in energy integration | total `129/(8π²)` instead of `86/(8π²)`, ratio3/2 |
| use dimensionless weights as physical dE | total divided by E0eV, ratio10 |
| diagonal-only reconstruction | bonds zero instead of positive `15t/(8π²)` |
| true Nb1 truncation | same zero bonds, derived above |

Negative tests retain expected RHS; do not replace expected array when mutating
the tested expression. A current-family diagonal-only mutation also changes
trace `6a−1` to `4a−1`, so offdiagonal errors are not invisible in the
resolved current slice.

## O08-02 direct Poisson and complete routing envelope

Build `(Nz=4,Nb=4,localization=:real_space)` with the checked helper above.
Public builder generates Φ=χ=I4, profilesND=1, εr=1, x/w as accepted O08-02.
No manual grids/profiles. Static H0 is the four-cell Dirichlet tridiagonal
with 2t/−t; T+=−t e4e1', T−=T+', Z=diag(.5,1.5,2.5,3.5),
M−1=I4/mr. Real-space basis centres=x, spreads=0, overlap eigenvalues=1,
κ=1, window_eigenvalues are all eigenvalues of that H0,
Egrid0=2t; basis residual zeros follow exact identity construction in builder.
Grids and four 3×3 shifts match the current carrier's actual E/k axes.

Run only direct bounded Poisson operator, once healthy n=ones4 and once
nonneutral n=2ones4. Analytic bordered equations remain accepted:

```text
L=cyclic(2,-1,-1), sP=4, v=ones4/2;
healthy U=0,ζ=rP=rneutral=0;
nonneutral U=0,ζ=λref/2,
rP=2/(2+1e-14), rneutral=1.
```

Assert gauge, each diagnostic, healthy declared t.rP/t.rneutral/t.rζ gates;
nonneutral all three fail. `ζ` comparison retains accepted absolute `1e-10`
diagnostic budget; `rP` literal comparison can use current arithmetic budget,
and `rP>1/2` is a margin assertion, not a replacement threshold. `rU=0`
is valid because solved U and published manufactured U are both zero.
The existing analytic sine derivative/refinement anchor is source reuse;
do not copy/reexecute it silently within this packet.

For **synthetic routing only**, assemble a fully inventoried NEGFSolution.
This part is deliberately not a final-state physical oracle. One density
parameter d=1 suffices for common envelope; diagnostics are separately
supplied metric inputs to `_validate_solution_metrics`.

```text
c=2π², R=c*d;
for all e,m: GR=−iR I4, G<=iR I4, G>=−iR I4, A=2R I4;
hm=t*tridiag4(−1,2,−1)+t*κm² I4;
ΣR=εe I4−hm−i/R I4, Σ<=i/R I4, Σ>=−i/R I4;
D=εe I4−hm−ΣR=i/R I4;
condition_number=ones(3,2), dyson_scale=fill(1/R,3,2).
```

These fields obey Dyson/Keldysh/Pauli algebra, but Σ is an explicitly
engineered energy-dependent counterterm, **not** actual embedding kernel.
Density is independently constant: `gs/(2π) * (ΣwE=2) *
(Σwk=1/(4π)) * R = R/(2π²)=d`. Thus U=zeros4 and n=ones4 are explained
and same-state; no unrelated n=zeros. Optionally d=2 creates a second
equally inventoried carrier for nonneutral metrics; don't double Gl alone
while leaving its GR/Gg/A and Σ fields inconsistent. It is not necessary
for routing, which accepts metric input separately.

Complete field inventory for the synthetic envelope:

| Container / fields | Value and limitation |
| --- | --- |
| GreenState six fields | all 4 arrays `(3,2,4,4)` and metadata above, checked finite/algebra/density before construction |
| SelfEnergyFamily | Σ above; split **all three components** equally between plus/minus; embedding is their exact sum |
| SCBAResult.scattering | empty dict agrees with disabled microscopic carrier options; not S1 evidence |
| SCBAResult.green/embedding/plus/minus | complete fields above, no aliasing of mutable families |
| SCBAResult.history | empty because no iterations executed; no fake measured SCBAIteration |
| converged/status/quality | `(true,:converged,:strictly_converged)` is explicit synthetic classification input to routing; constructor validates this tuple, not science |
| restart_contract/mixer_state | `nothing`, default linear empty state, because no iteration/restart performed |
| NEGFSolution.problem/options | complete checked builder and `SolverOptions()` with unmodified tolerances |
| U,n | zeros4/ones4, justified by direct compatible U and reconstructed density |
| outer_history | empty, no outer-loop measurements manufactured |
| observables | only explicit synthetic label, e.g. `:fixture_kind=>"synthetic_acceptance_routing"`; do not add scientific quality metadata |
| report | initial `ConvergenceReport(false, empty Dict{Symbol,Float64}(), String[])`, a nonaccepted placeholder; assessment seam uses supplied metrics |
| converged/status | outer false, `:manufactured_routing`; never publish/save as scientific solution |

The positive routing input is an explicit table of **synthetic pass sentinels**,
not values measured from this Green state. Use zero for each required base
metric, with actual healthy/nonneutral Poisson entries overriding only
`:r_P,:r_neutral,:r_ζ`; `:r_U=0` has the direct same-U explanation.
Zero in this table means an intentional branch input, not `not_measured=pass`.
No call to solution_scientific_assessment/validate_solution or persistence
may treat these sentinels as measurement. Testset names/assertion labels
must say synthetic routing. There is a concrete guard against an overclaim:
this engineered Green has spectral sum residual `4π−1`, not zero; the
complete scientific validation is therefore not claimed to pass.

Freeze the input metric keys explicitly, so dropping a gate in production
cannot drop it from the expected input by sharing `_solution_validation_limits`:

```text
r_D,r_A,r_K,r_Σ,r_λ,r_roundoff,r_Jchange_scba,r_population_scba,
r_PSD,r_caus,r_caus_sc,r_caus_embedding,
r_selfenergy_identity,r_selfenergy_identity_sc,r_selfenergy_identity_embedding,
r_antihermitian_G,r_antihermitian_Σ,r_antihermitian_Σsc,r_antihermitian_Σembedding,
r_sum,r_J,r_ImJ,r_roundJ,r_power,r_ImP,r_roundP,
r_P,r_U,r_n,r_neutral,r_ζ,r_Jchange,r_population,
r_tail_low,r_tail_high,r_tail_k,r_edge_gamma,r_edge_spectral
```

No optional channel/candidate/hot-LO/e-e metric keys are added for this empty
microscopic carrier. Required assertions:

1. All healthy routing sentinels + actual healthy Poisson values → report
   passed, no messages, **only as a routing assertion**. The direct compatible
   control claims only the three relevant measured Poisson gates; it does not
   establish a genuine full coupled physical pass.
2. Actual nonneutral three metrics inserted → not passed, exactly the three
   named `r_P`, `r_neutral`, `r_ζ` failures, no unrelated failure.
3. Three isolated cases: only one actual bad diagnostic retained, other two
   actual healthy diagnostics. Each must fail its one expected named gate.
   This catches dropped gate independent of another failing gate.
4. Force neutralized mean source for the nonneutral operator variant and
   retain original nonzero expected ζ/rP/rneutral: direct RHS assertion fails.
5. Optional classification control uses consistent constructor tuple
   `(false,:max_iterations,:unresolved)` and healthy metric sentinels, and
   fails the SCBA classification branch separately. Never invalid tuple.

Do not test a mock implementation of `_validate_solution_metrics`; call the
actual seam with the typed envelope. No new public factory or solver call.

## Independence, remaining gap and finite future L-JL packet

All numerical expected current values use literal component sums, SI constants,
analytic sine columns, independently derived FD offdiagonal −t and actual-grid
quadrature formulas. Builder creates the input carrier only; it does not
create expected current. Actual basis used for phase transport is constrained
by independent analytic-basis assertions first. Poisson expected U/ζ/residuals
come from nullspace/bordered equations, not L*expected_U. Assessment sentinel
table is intentionally policy-routing input, not a physical oracle.

Unresolved: no complete independently derived all-five coupled final-state
O08-03 assembly, no absolute four-channel O08-05 prefactors, no S1 convergence,
discretization or experimental acceptance. This correction closes only carrier
design gaps of DEV04/06 after reviewer acceptance; DEV05/07 stay blocked.

Future implementation changes **only** owning passport correction and two
new test files already allowed by DEV04/06. Coordinate source writer and
do not touch imports, Julia locks/depot, project manifests or source APIs.
Before running confirm INT01 native import readiness and immutable reviewed
Core snapshot; if tracked operator sources changed, recheck this design's
locators/hash rather than silently accepting a different implementation.

Bounded runtime packet: one invocation of each new test file, sequential,
threads=1, **each ≤120s, 1 CPU, 2GiB RAM**, combined ≤240s and 4MiB output,
≤16MiB new logs/artifacts. At most the existing two-invocation L-JL allowance
per card; counts include red/green/reviewer runs, shared across agents. This
proposed reduced packet uses one per card, leaves no implicit retry authority.
Public build_problem here is explicitly permitted only as no-solve tiny
static assembly: three constructions for current (`Nb2`, `Nb1`) and Poisson
(`Nz=Nb4`), no microscopic kernel tensors, maximum Hwin12×12, Green block
array96 complex entries. One healthy and one nonneutral **direct** bordered
Poisson5×5 solve; no SCBA/outer Poisson loop/profiling/benchmark.

Commands, root cwd, only after CP-DESIGN + import readiness:

```sh
julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/physics/nonneutral_periodic_poisson_assessment.jl")'
julia --startup-file=no --project=julia --threads=1 --check-bounds=yes -e 'include("components/QCLNEGF.jl/test/physics/nonzero_public_current_oracle.jl")'
```

A runner must enforce memory/wall/output limits externally using its existing
L-JL mechanism. Any import/build/setup attempt is charged to INT01, not hidden
inside this test packet. Timeout/OOM/nonfinite/basis or static failure means
preserve log + stop that card; source diagnosis, no solve-to-success loop.
Candidate source/format checks are read-only `git diff --check`, exact diff,
targeted links. No full suite/docs build or repeated sine anchor implied.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Старые размеры current carrier подходят public constructors | `types.jl:181–284` contradicts NE2/Nk1 | source-only, runtime0 | изменить |
| Полный public current carrier выведен | checked builder, actual3×2 weights, analytic Nb2 basis, full Green/family/metadata inventory | manufactured functional, CP-DESIGN pending | изменить |
| Nonzero RHS различает measure/sign/units/coherence | retained `[19,43,67]/(8π²)`; `43/(4π²)`; bonds `15t/(8π²)` | regression arithmetic policy, no solution validation | сохранить |
| O08-02 constant-source diagnostics независимы | bordered nullspace: ζ=λ/2, rP=2/(2+floor), rneutral=1 | four-cell direct operator only | сохранить |
| Typed assessment route возможен без solver | real-space builder + all fields explained + frozen synthetic metric table | classification/other gates deliberately synthetic, not measurements | изменить |
| Полный all-five final-state/scientific pass доказан | такого RHS/измерений нет; engineered spectral residual4π−1 | O08-03/05 и science остаются незакрыты | данных недостаточно |
| Native/tests выполнены | imports/tests/solver0 | будущий finite L-JL packet только предложен | данных недостаточно |
