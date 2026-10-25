# SCI03-5.3 — добавочный контракт измерения absolute represented-current bound

2026-10-19. D / Sol ultra. **CANDIDATE FOR INDEPENDENT R HIGH; STOP DESIGN.**
Единственный этап — source-only scientific design. Ни один новый результат QCL,
scientific acceptance, runtime READY, разрешение I или native admission здесь не
установлены. Product/source/Git не изменены. Единственные выходы этой задачи —
этот файл и `/tmp/qcl-sci03-current-bound-design-identity.json`.

## 1. Вопрос, граница и неизменяемые условия

Вопрос: какие минимальные добавочные скаляры позволяют Results независимо от
Core оценить опубликованный SCI03 §5.3 bound для **каждого** raw/normalized
boundary current из одного immutable stored final? Ответ: шесть абсолютных
state-defect norms и шесть side-coefficient norms; существующие A/correction
accumulators переиспользуются. Дополнительных datasets, HDF passes, matrix
products, μ-fit, public arguments или acceptance evaluator не требуется.

S1 сохраняется: stationary 0 mV/period; lattice/thermal LO 70 K; LO/acoustic/
impurity/IFR/alloy; electron–electron=none; прежние модель, field/window/grid,
finite basis, embedding и все scientific tolerances. Не задаются εJ_abs, другие
accuracy targets, H или новые variants. Formula measurement и его инженерная
регрессия — отдельный предмет от physical acceptance.

Родитель передал конечный envelope: ≤45 min, 1 CPU, 2 GiB, source reads ≤6 MiB,
report ≤96 KiB; без imports/parsers/HDF/Julia/tests/solver/build/install/network/
server/Git mutations/children. C08 использовано **0**; cap8/consumed6 других
writers этой задачей не резервируется. Native admission отсутствует: блокирует
native execution, не данный design. Input arrays/run/attempt/frozen-plan bytes
не предоставлены; никакой coefficient или bound конкретного run не измерен.

## 2. Сначала формулы, предпосылки, единицы и знаки

На одном представленном orthonormal finite basis все матрицы имеют полные
индексы (E,k,a,b), комплексные элементы и persisted dimensionless units `1`.
Пусть положительные persisted E0_eV, L0_m, J0_A_per_m2 проверены, gs — declared
spin degeneracy, wE,wk — сохранённые неотрицательные меры с ненулевой суммой.

```
W_em = gs*wE_e*wk_m/(2*pi)
||X||_W² = sum_em W_em sum_ab ((Re X_emab)^2 + (Im X_emab)^2)
M = sum_em W_em
N = -i G<; P = i G>; A = stored A
S_n,s = -i Sigma<embedding,s; S_p,s = i Sigma>embedding,s
Gamma_s = S_n,s + S_p,s
f_e = FD(E0_eV*energy_e; common fitted mu_relative_eV,T_L_K)
deltaS_s = S_n,s - f_e*Gamma_s
deltaN_v = N_v - f_e*A
deltaP_v = P_v - (1-f_e)*A                  v = raw, normalized
D_v = deltaN_v + deltaP_v
```

`wk` уже содержит annular radial 1/(2π): дополнительный radial/spin factor
запрещён. `A` берётся из exact stored owner, а не подменяется i(GR−GR†).
Одна μ определяется существующим finite-spectrum particle-number construction
и используется для **обеих версий и сторон**. Ни одна сторона/версия не получает
свою μ. E_ref нужен только для existing absolute μ presentation; FD использует
relative energy и relative μ с одной gauge. All-five S1 claim требует отдельно
совпадения frozen model, requested flags, actual stored пяти families и context;
existing reader applicability само по себе не доказывает такой claim.

Для **complex outward electron-flow current**, в принятой положительной J0:

```
J_s,v^c = J0 * sum_em W_em Tr(S_p,s*N_v - S_n,s*P_v)
        = J0 * sum_em W_em Tr(Sigma>_s*G<_v - Sigma<_s*G>_v).
```

Последнее равенство следует из Sigma>=−iS_p, Sigma<=iS_n, G<=iN, G>=−iP;
никакой дополнительный i, minus или electron charge sign не вводится.
Existing outward real field — Re J^c, imaginary field — Im J^c. Для common-z
plus знак тот же, minus меняет знак. Absolute bound одинаков для этих двух
ориентаций. Outward balance не заменяет каждый из двух absolute currents.
Conventional charge-current sign не переносится из статьи в Results молча.

Подстановка S_n=fΓ+δS, S_p=(1−f)Γ−δS даёт **matrix identity до trace**:

```
S_p*N - S_n*P = (1-f)*Gamma*deltaN - f*Gamma*deltaP
                - deltaS*(A + deltaN + deltaP).
```

Члены f(1−f)ΓA сокращаются в одном порядке; коммутирование Γ с A/N/P и
spectral identity N+P=A не предполагаются. Hermiticity/PSD тоже не нужны.

Для любых конечных complex matrices X,Y,
`|Tr(XY)|=|sum_ab X_ab Y_ba| <= ||X||F ||Y||F` — обычное scalar complex
Cauchy–Schwarz, поскольку перестановка a,b сохраняет Frobenius norm.
Triangle inequality для суммы em и weighted Cauchy–Schwarz для W≥0 затем дают

```
g_s^- = ||(1-f)*Gamma_s||_W; g_s^+ = ||f*Gamma_s||_W
d_s = ||deltaS_s||_W; a = ||A||_W
n_v = ||deltaN_v||_W; p_v = ||deltaP_v||_W; c_v = ||D_v||_W
B_s,v^repr = J0 * [g_s^-*n_v + g_s^+*p_v + d_s*(a+c_v)]
|J_s,v^c| <= B_s,v^repr.
```

В последнем слагаемом использована ещё одна triangle inequality
`||A+D||_W <= ||A||_W+||D||_W`. `c_v` измеряется **как норма суммы matrices**,
а не `n_v+p_v`; не считается нулём по spectral identity. Все coefficient/defect
norms dimensionless (`units='1'`); три слагаемых после умножения J0 и B имеют
`A/m^2`. Никаких division/J, denominator floors, percent или normalization к
числу доноров/A/J в этом bound нет. Existing normalized FDR остаётся отдельным
отношением и не служит заменой отдельным absolute norms.

Утверждение — algebraic upper bound **представленного exact-arithmetic complex
trace при фиксированном f и stored matrices**. Оно также ограничивает модули
real/imag частей, но не errors истинного physical solution. Float64 output
измеряет RHS этой формулы: округление вычисленных норм, exp, product и sum не
является сертифицированным outward-rounded numerical enclosure. Report обязан
сохранить `arithmetic_error_status='not_measured'`, `arithmetic_error_bound=null`;
не добавлять якобы строгое numerical guarantee из сравнения rounded J и B.
Не охвачены fresh-map/fixed-point defects, μ error из изменения spectrum,
energy/window/k/basis/domain/tails, nonlinear conditioning и эксперимент.
Даже большой измеренный B нельзя объявить приемлемым без отдельно обоснованного
εJ_abs и остальных error contributions.

### Первичные источники и границы attribution

Owning опубликованный Research contract — `docs/equilibrium-measurement-contract.md`
§§2–3,5.3: primary P-FDR Fotso–Freericks, DOI10.3389/fphy.2020.00324, printed p.8
(42), scalar/local lesser FDR; matrix application и greater identity выведены
в самом contract. P-J Wacker arXiv:0706.4202v1, printed p.2 (2)–(6), требует
coherences и оговаривает finite basis/local current; он не является первичным
источником именно adopted outward boundary sign. Homogeneous Keldysh relation
в published source chain: Lee–Wacker cond-mat/0212059v1 (5); initial-correlation
source отдельно не вводится. Owning Core EQ-CURRENT-001 ниже задаёт именно
implemented boundary convention.

Локальные PDF Wacker/Lee–Wacker найдены; SHA256 сверены с опубликованными
receipts: `091a39824c3fb4b5f1f3b0f0659d4a99663b48b6949806aa8586710b6d1d937b`
и `dfabd791bfb2aa4603233e9b545879e07a3bfc63e8906cbc810760726358ea0c`.
Их bytes прочитаны только для SHA (997352 bytes); новый PDF parser/network не
исполнялся, страницы заново не проверялись. Поэтому paper locators здесь —
явная reuse attribution опубликованного SCI03, не новая independent extraction.
Для bound не нужна внешняя приписанная theorem: полный elementary proof дан
выше и не зависит от достоверности библиографической атрибуции. FD/FDR не дают
никакого finite-device scientific tolerance.

## 3. Затем binding к выбранным исходникам

Workspace `/home/tolya/.codex/worktrees/review-closure-exec/qcl-negf`.
Root фактически `cfc38e1761f24caf436d938f378dbcdbf71a28f0`; root tracked dirty:
Results gitlink и `execution/checkpoint.json`, плюс coordination/evidence
untracked files соседних writers. Это не изменялось этой задачей.
Gitlinks — composition authority, этот snapshot не новый maintained lock.

| Owner | Root gitlink | Фактический selected HEAD/status |
| --- | --- | --- |
| Core | 7324d98c0fccd61b4a1a2756b5cabe2fd0e0e49c | совпал, чистый |
| Contracts | 12fc26462bbab3df76904c6deb01f8c6596de7be | совпал, чистый |
| Research | 1eacefcd81a50e245ea9da74a0b717b33818c61e | совпал, чистый |
| Results | e2fdeda29ab4064fb92626f4e98c3d39aac2e4ae | 33b1a39eab62b0c00532c4d6b30fa3279c06a5d3, чистый |

Equilibrium source/test hashes совпадают с SCI06; StateReader отличается
после отдельного SCI05 format work. Старые line numbers SCI06 для StateReader
не переносятся на новый selected HEAD. Protected original checkout
`/home/tolya/Загрузки/qcl-negf` не читался и не изменялся этой задачей.

| Formula/свойство | Selected source locator | Наблюдение |
| --- | --- | --- |
| gs,wE,wk,W | Core `src/numerics/reference/grids.jl:22–39`; Results `equilibrium.py:425–433` | Trapezoid energy, annular wk; reducer W=gs/(2π)*wE*wk |
| J0 scale | Core `src/domain/scaling.jl:10–23`; Results `equilibrium.py:318–321` | Persisted positive scale, не guessed constants |
| Boundary trace/sign | Core `docs/src/theory/11_observables.md::EQ-CURRENT-001`; `src/physics/observables.jl::_current_trace`, `_boundary_flux_complex` (175–205); Results `equilibrium.py:494–526` | Full ordered matrix products, signed integral before abs; outward/common-z fields |
| Weighted norm | Results `equilibrium.py::_Norm` (83–121) | Full complex real+imag LASSQ with W, no diagonal fallback |
| μ gates | Results `_applicability` (177–203), `_fit_mu` (227–285), main 459–464,527–531 | Missing/unsupported context, finite drive, unavailable μ stay unavailable |
| Raw reconstruction | Results `equilibrium.py:470–478` | GA=GR†; sum actual enabled scattering + embedding_total exactly once; Nraw=−iGRΣLtotalGA, Praw=iGRΣGtotalGA |
| Existing norms/reports | Results `equilibrium.py:465–493,527–547` | A/correction available internally; aggregate FDR combines δN and δP, side coefficients/sum defect absent |
| Provenance/budget | Results `state.py::StateReader` (372–449), `read` (514–581) | Full owner SHA+receipt, exact provided identity keys, native/schema/units/axes reads, physical I/O guard |

Read root AGENTS, architecture, agent-review-workflow, P1 science C07/C08,
SCI03/SCI06, Research+Results CONTRIBUTING, qcl-physics-audit. Dispatched-subagent
exception in using-superpowers applies. SCI06 audit input SHA exactly
`4c5a8160abadb2f011950a19379fd3b103354716aef8306a1f2ff163bc88e73f`.

## 4. Точные consumed inputs; ни одного нового dataset

Reuse existing immutable physics.full native-v4 StateReader; require valid
commit/receipt/source owner and C07 **полный** expected identity:
execution_id, point_id, attempt, plan_fingerprint, state_id, state_sequence.
Это caller precondition для данного exact-final measurement. Существующий
partial-selector public StateReader API в этом ticket не сужается. Pending
format/native-final improvements других tasks не переопределяются.

| Native path | Storage/units и назначение |
| --- | --- |
| `/state_dimensionless/{GR,GL,GG,A}/{real,imag}` | binary64 shape (NE,Nk,Nb,Nb), axes E,k,a,b, units `1`; GR только existing raw reconstruction, A spectral reference, GL/GG normalized N/P |
| `/selfenergy_dimensionless/{LO,acoustic,impurity,IFR,alloy,embedding_total}/{SL,SG}/{real,imag}` | Те же complete matrices; actual enabled dictionary + embedding_total ровно один раз формирует raw |
| `/selfenergy_dimensionless/{embedding_plus,embedding_minus}/{SL,SG}/{real,imag}` | Те же complete matrices; **только соответствующая сторона** даёт Γs,δSs и side current; total+plus+minus не суммируются в raw |
| `/grids_dimensionless/{energy,wE,k,wk,state_index}` | binary64 vectors/zero-based int64 state_index, units `1`; coordinate links всех matrices точно energy,k,state_index,state_index |
| `/numerical_inputs/{NE,Nk,Nb,scattering_LO,scattering_acoustic,scattering_impurity,scattering_IFR,scattering_alloy}` | Existing exact dimensions/flags, units `1`; не defaults |
| `/inputs/{spin_degeneracy,F_bias_V_per_m,V_period_V,T_L_K,T_LO_K,E_ref_eV,N_dop_2D_per_m2,f_ion}` | Existing units `1,V/m,V,K,K,eV,m^-2,1`; μ target/gates/context |
| `/scales/{E0_eV,L0_m,J0_A_per_m2}` | Existing `eV,m,A/m^2`; finite positive; J0 only physical multiplier RHS |
| commit `stationary_assessment.model_context` + native/commit identity/receipt | Existing applicability, requested/stored inventory, declared orthonormal basis, thermal LO/e–e none; не доказательство truthful physical provenance |

Все existing invalid_data/unsupported_layout/unsupported_context/budget guards
сохраняются, включая nonfinite, axes/transposition labels, negative weights,
unknown/missing families, uncompressed chunk cap и complete basis plane.
Missing stored family не становится zero kernel. Нет дополнительных physical
assumptions про e–e, conserving SCBA, flat energy current или FD attraction.

## 5. Минимальный additive report contract и статусы

Public signature и existing keys/values/schema остаются. Один **новый optional
additive top-level namespace** `represented_current_bound`; namespace version
`contract='SCI03-5.3-represented-current-v1'` документируется в owning Results
README со ссылкой на Research §5.3. Strict native/portable format и contract_set
не меняются: новых persisted datasets/commit fields нет. Если найден внешний
consumer с запретом unknown report keys, compatibility надо проверить до I;
в просмотренных owning source/tests отдельная strict shared schema этого report
не найдена. Не открывать новый CLI/public helper/Core evaluator.

Exact scalar rows ниже имеют `status`, `reason`, `units`, `value`; как existing
API, value — finite float либо null, без NaN/Inf. Dependency groups могут иметь
общий status/reason, сохраняя те же semantics для всех трёх значений.

```
represented_current_bound = {
  contract: 'SCI03-5.3-represented-current-v1',
  norm: 'absolute weighted full complex Frobenius',
  weight: 'gs*wE*wk/(2*pi)',
  normalization: 'none',
  reference_mu: 'mu.value_relative_eV',
  spectral_norm: row(a, units='1'),
  normalization_correction_norms: {
    occupied: row(||Nnormalized-Nraw||_W, units='1'),
    empty: row(||Pnormalized-Praw||_W, units='1')
  },
  state_defects: {
    raw: {status, reason, units:'1', occupied_norm:n_raw,
          empty_norm:p_raw, sum_norm:c_raw},
    normalized: {status, reason, units:'1', occupied_norm:n_normalized,
                 empty_norm:p_normalized, sum_norm:c_normalized}
  },
  boundary_coefficients: {
    plus: {status, reason, units:'1', one_minus_f_gamma_norm:g_plus^-,
           f_gamma_norm:g_plus^+, sigma_fdr_defect_norm:d_plus},
    minus: {status, reason, units:'1', one_minus_f_gamma_norm:g_minus^-,
            f_gamma_norm:g_minus^+, sigma_fdr_defect_norm:d_minus}
  },
  bounds: {
    plus: {raw: boundrow, normalized: boundrow},
    minus: {raw: boundrow, normalized: boundrow}
  },
  arithmetic_error_status:'not_measured', arithmetic_error_bound:null,
  scope:'represented exact-arithmetic complex trace; no acceptance'
}
boundrow = {status, reason, units:'A/m^2', value:B_s,v,
            occupied_term:J0*g_s^-*n_v, empty_term:J0*g_s^+*p_v,
            selfenergy_term:J0*d_s*(a+c_v)}
```

Имена g_plus^± в псевдокоде — mathematical placeholders, не JSON keys. Все JSON
keys выше literal ASCII. Общая μ и complete source/domain/scales уже сохранены
в existing report; копии arrays, собственного source manifest или μ-fit нет.
Внешний snapshot identity в companion — audit evidence, не composition lock.

- Если μ.value_relative_eV определена existing applicable path: новые dependent
  groups и four boundrows имеют `status='measured',reason=null`. Это статус
  измерения формулы, не pass/equilibrium. Каждый finite product/sum и J0
  conversion проверяется existing `_finite`/finite scalar guard; overflow →
  invalid_data, никакого Inf/null с measured status. Coefficients не делятся на A.
- Если μ unavailable: **сначала наследовать** её exact status/reason, затем
  n,p,c,g^±,d,B и term values=null. Нельзя заменить missing μ нулём даже при
  всех boundary matrices=0. Existing A/correction rows могут быть measured,
  поскольку μ не требуют; existing numbers/currents сохраняют своё поведение.
- При defined μ и literal zero factor(s) соответствующий product равен
  absolute0; bound0 measured только если все три finite terms действительно0.
  Никакого 0/0, relative-current field или stabilizing floor. Nonzero defect
  при A=0 не получает FDR pass; unavailable μ/empty spectrum имеет приоритет.
- Rounding underflow/exact factor distinguishability этой Float64 метрикой не
  сертифицируются; это часть explicit missing arithmetic enclosure. Нулевой
  rounded norm не доказывает отсутствия exact-arithmetic/scientific error.
- Сохранить existing corrections relative ratio, numerator_squared,
  denominator_squared и их zero-denominator conventions. Новые absolute
  correction rows лишь публикуют существующие `_Norm.magnitude()`, не меняют
  normalization algorithm и не выдаются за δN/δP FDR.
- Нет `pass`, `accepted`, tolerance/criteria registry, claimed target accuracy
  или comparison-vs-target поля. `not_measured` нигде не преобразуется в pass0.

## 6. Приватная реализация и конечная стоимость будущего measurement

Это **контракт будущего I после R**, не выполненные изменения.
Allowed owner: Results `src/qcl_negf_results/equilibrium.py`, focused existing
`tests/test_equilibrium_diagnostics.py`, небольшой README additive description.
Core/Runner/Contracts/Research equations и UI/scheduler не редактируются.

Pass two уже держит A, raw/normalized N/P и читает обе side ΣL/ΣG. Добавить
ровно 12 streaming `_Norm`: по δN,δP,D для двух версий (6); по (1−f)Γ,fΓ,δS
для двух сторон (6). Existing A/corr_n/corr_p и aggregate FDR сохраняются.
Не вычислять n,p из одного aggregate FDR ratio. D складывать из полных двух
matrix defects; не навязывать closure. При μ undefined accumulators dependent
пусты, но report null-gated; отсутствие samples не означает measured zero.

Compute state norms до side loop, затем освобождать временные defects; для
side сформировать S_n,Γ и последовательно подать (1−f)Γ,fΓ,δS в `_Norm`,
освобождая temporaries до перехода к следующей стороне. Existing flux ordered
matrix products и signed compensated sums сохраняются. Не перезаписывать GL/GG,
Σ или A alias/in-place; no diagonal fallback. Можно private helper для сборки
finite report scalars, но не public API или duplicate acceptance authority.

Числовой scratch forecast должен **предварять чтение** и покрывать новые
arrays. Простой консервативный вариант: existing per-energy allowance
`24*16*Nb²` увеличить до `32*16*Nb²`, при документированном scheduling с максимум
8 добавочных complex tile buffers и O(tile) f-weights. При этом существующий
fixed forecast `10*8*NE + 4096 + 32*Nk +16*Nb +512*len(descriptions)` сохраняется;
если реальные O(tile) vectors не укладываются в восемь slots, учитывать их
отдельно, не объявлять cap доказанным. Full-plane minimum/tile adaptation
пересчитать существующим механизмом; maximum_workspace_bytes, single read и
chunk caps не увеличивать. 12 scalar accumulators и bounded report metadata
добавить в documented fixed scratch allowance (например reserve4096 bytes —
engineering accounting, не claim process RSS). Ни один cap не разрешает full
array loading. Точная implementation allocation census — обязательный пункт R.

При N=NE*Nk*Nb² новые norms дают O(12N) complex-entry visits (24N real/imag
component visits), ещё O(N) scalar multiplications/subtractions. **Новых
O(Nb³) matrix products нет**, но Python `_Norm` loops могут быть существенны:
без benchmark их wall-time стоимость неизвестна, слово negligible запрещено.
Нет новых scientific runs или profiling/benchmark в этом design.

Два existing passes и dataset selection unchanged. Для C stored scattering
families existing scalar real/imag matrix components суммарно `2*(11+2C)`:
A два раза, остальные required matrices один. При tile length t и одном k
logical forecast contribution `2*(11+2C)*8*(t*Nb²+2t+2+2Nb)`; vector/scalar
reads отдельно. Instrumentation **не добавляет** этих payload/coordinate reads
или third pass. Actual mandatory full owner SHA + HDF delivery + metadata/
receipt/sidecar reads остаются под existing total physical I/O callback budget;
logical forecast не заменяет actual I/O admission. Chunk decompression guarded
existing cap. Axis limits сами по себе не дают I/O/CPU grant.

Новый namespace — конечное число скаляров, engineering incremental JSON reserve
≤8 KiB; existing maximum_report_bytes (default64 KiB) **не увеличивается**.
Если final encoded report не помещается — budget_exceeded, не обрезать rows и
не скрывать missing measurements. Workspace scope остаётся numeric arrays+
scratch, не total RSS/HDF cache/OS I/O. Actual time/RSS/I/O могут быть оценены
только на future admitted immutable final; сейчас datasets/input bytes missing.

## 7. Независимый literal positive/negative fixture contract

Все ниже — **manufactured measurement/oracle inputs**, не новая S1 grid,
physical model или proposal solver run. No product imports/helpers в expected
arithmetic: использовать выписанные 2×2 entries, scalar products, `math.fsum`,
scalar sqrt/exp; `_Norm`, `_fd`, `_fit_mu`, product bound builder не oracle.
Transport не вызывается. Existing HDF fixture encoder разрешён только для
format plumbing после отдельного I grant; provenance/helper sharing явно
ограничивает независимость encoding, не literal arithmetic.

### 7.1 Positive nonzero-defect control

Минимальный reader fixture: один manufactured E=0, два distinct k labels,
Nb=2, wE=3/8, wk=[1/4,3/4], gs=2, T=70 K, μ*=0, E_ref=0, E0=0.1 eV,
J0=13 A/m², positive L0 как existing fixture. Это reader diagnostic plane,
не допустимый production build_grids NE=1. Пять scattering families actual,
requested и context present; thermal LO/e–e none/zero drive. Все native units,
axis links, exact six identity fields/owner SHA/local receipt корректны.

Пусть ε=1/128, ε_k=[ε,2ε], I=identity2:

```
X = [0  1; 1  0]           Y = [0  i; -i 0]
A = 2 I; GR = -i I; GA = i I
Gamma_plus  = [1/2   i/8;             -i/8           1/4]
Gamma_minus = [1/4   1/16+i/16;       1/16-i/16      1/2]
Gamma_internal = 2I - Gamma_plus - Gamma_minus
DeltaS_plus,k  = epsilon_k * X
DeltaS_minus,k = epsilon_k * Y
S_n,s,k = Gamma_s/2 + DeltaS_s,k
S_p,s,k = Gamma_s/2 - DeltaS_s,k
SigmaL_s = i*S_n,s; SigmaG_s = -i*S_p,s
```

`embedding_total` — буквальная сумма plus/minus. Internal Γ делится на пять
families с **dyadic** fractions [1/8,1/8,1/8,1/8,1/2], для каждой Sn=Sp=Γ/2.
Следовательно totalΓ=2I, Nraw=I+εk(X+Y), Praw=I−εk(X+Y) (поскольку GR=−iI),
A=i(GR−GA)=2I. Side Γs PSD; Γs и X/Y не коммутируют. N/P synthetic defects
измеряются, scientific fixed point не утверждается. Stored normalized:

```
Nnorm,k = I + epsilon_k*(2X+Y)
Pnorm,k = I + epsilon_k*(-X+2Y)
GLnorm=i*Nnorm; GGnorm=-i*Pnorm
```

Норма суммы normalized намеренно ненулевая; это positive control способности
измерить defect, не физический healthy equilibrium. Target ionized dimensionless
number=2M, где `M=sum_k W_k=3/(8*pi)`, задаёт μ*=0 по **stored A**, не по
raw/normalized numbers. Ни один fit другой μ не разрешён.

Сначала literal table для f=1/2, `L=sum W εk=(7/4)Mε`,
`R=sum W εk²=(13/4)Mε²`:

| Измерение | Independent exact-arithmetic expectation |
| --- | --- |
| a² | 8M |
| g_plus^-² = g_plus^+² | (11/128)M; ||Γplus||F²=11/32 |
| g_minus^-² = g_minus^+² | (21/256)M; ||Γminus||F²=21/64 |
| d_plus² = d_minus² | 2R |
| n_raw² = p_raw² | 4R |
| c_raw² | 0 |
| n_normalized² = p_normalized² | 10R |
| c_normalized² | 20R |
| occupied/empty absolute correction norms² | 2R / 18R |
| raw complex currents both sides | J0*L/4 = J0*M*7/2048, imaginary0 |
| normalized plus outward | J0*(-L/8-2R) = -J0*M*69/32768 |
| normalized minus outward | J0*(L/8-6R) = J0*M*17/32768 |
| minus common-z | negative of corresponding outward |

Для каждого side/variant expected B вычисляется из **этих отдельных literal
norms**, все три expected term values сверяются отдельно, затем total. Из
f=1/2 таблицы дополнительно Braw/J0=(2√g+4)√(MR),
Bnorm/J0=√(10gMR)+4√(MR)+√40 R, где g=||Γs||F². Bound-only inequality не
достаточна: завышенный ошибочный B тоже может покрыть J.

Finite API μ-fit обычно даёт μhat≈0, но не точно0. **Не ослаблять μ algorithm
или oracle под это.** Проверить independently, что bracket включает0, и взять
в expected **один** scalar `t=1/(1+exp(-muhat/kBT))-1/2`, используя public report
μ и самостоятельный scalar FD. Это тест arithmetic при выбранной μ; отдельная
known-μ/bracket проверка защищает construction. Точные поправки таблицы:

```
a²=8M; c_raw²=0; c_norm²=20R; corrections²=(2R,18R)
g_s^-²=(1/2-t)²*g*M; g_s^+²=(1/2+t)²*g*M
n_raw²=p_raw²=4R+8t²M
n_norm²=p_norm²=10R+8t²M
d_plus²=2R+t²*(11/32)*M
d_minus²=2R - t*L/4 + t²*(21/64)*M
```

J и normalization corrections не зависят от construction t. Эти формулы
следуют orthogonality I,X,Y в Frobenius inner product и literal Tr(YΓminus)=1/8;
product norm/reducer oracle не вызывается. Assert и table при f0, и finite-t
API expectations (первые можно проверить чистой scalar arithmetic seam).
Engineering regression budget после π/exp/sqrt — например
`512*u*max(1,abs(expected))`, u=2^-53, отдельно для каждого dimensionless/SI
scalar при фиксированных scales13 и малом fixture. Это conservative policy
для ≤512 scalar rounding operations на одну row при обычных libm exp/sqrt;
не rigorous libm certificate и не device tolerance. Dyadic matrix identities,
нулевые literal terms и exact sign expectations проверяются отдельно; если
implementation меняет цепочку/число операций, reviewer обязан заново проверить
это обоснование, а не расширять допуск для падения. μ bracket uncertainty не
прячется в этот budget: finite-t formula учитывает её явно.

### 7.2 Required negative/control matrix

| Control/mutation | Обязательное различающее assertion |
| --- | --- |
| Все boundary Σ действительно stored zero; internals сохраняют defined μ | g^±=d=0, four B=0 measured, arbitrary finite state defect не вызывает division/J; absence datasets вместо zero отвергается existing inventory guard |
| Missing context, finite drive, unequal LO T, e–e mode≠none, empty spectrum или μ iteration limit | Exact inherited μ status/reason; all μ-dependent new values/terms null, даже если boundary zero; A/correction absolute rows independently measured где входы валидны |
| Diagonal-only / discard Im / trace-only defects | Literal off-diagonal n,p,c,d nonzero/table нарушается; raw current остаётся nonzero; mask нельзя компенсировать setting0 |
| Drop δS term или assume Σ FDR | d²=2R и expected selfenergy term требуют nonzero; **exact coefficient/term** assertion, не только |J|≤B |
| Replace c by n+p либо assume N+P=A | c_raw=0 при n_raw,p_raw>0 и c_norm²=20R отдельно различают обе ошибки |
| fΓ/(1−f)Γ swapped | Дополнительный off-centered common μ fixture: target=M (четверть capacity4M), μ*=−kBT ln3, f*=1/4, t*=−1/4 при E=0. Поэтому g^-=(3/4)√(gM), g^+=(1/4)√(gM); compare literal finite-t norms при same public μ. Основной f0/t≈0 control один swap не различает |
| Wrong gs/2π/radial factor or linear вместо squared f weighting | Все coefficient/defect absolute norms и expected SI terms сверяются отдельно с literal W; не только согласованное rescaling J/B |
| Both k planes accidentally identical / wrong wk | εk различны, R/M=13ε²/4 и L/M=7ε/4 должны сохраниться; replace с unweighted mean нарушает oracle |
| Transpose/order/sign of side Σ или plus/minus reused | Γplus/minus norms различны; side signed raw/normalized currents literal выше; transposed Γplus flips its Y contribution, sign error не скрывается absolute B |
| Embedding_total + plus + minus double counted in raw | Nraw/Praw literal entries и correction norms нарушаются; side Γ определяется только side datasets, не total |
| Only real-current magnitude checked | Добавить Nnorm→Nnorm+iρI, ρ=1/32; Pnorm unchanged: Im J_s=J0*(3ρM/8) на каждой стороне. Expected full complex norm² включает +2ρ²M в n_norm² и c_norm². Проверить `hypot(ReJ,ImJ) <= B + engineering roundoff budget`, не только |ReJ| |
| Negative weights/nonfinite input/wrong axis/attempt/receipt | Existing healthy+rejected cases retain errors; новый namespace не обходной path |
| Product/sum overflows although all inputs finite | invalid_data, никогда measured Inf; report encoding allow_nan=False и cap enforced |
| Too-small workspace/I/O/report cap | budget_exceeded с сохранением guards; new fields не вызывают full-plane fallback/third pass/truncated success |

Существующие R01 known μ/nonunit weights, R02 normalized coherence, R03/R04
stored Σ mutation, zero/missing context, IO guards и source-ownership assertions
сохраняются. Их historical executed/pass status не присваивается новым cases.
Expected module не импортирует проверяемые arithmetic helpers; source-bound
fixture encoder/source identity remain separately checked. Для R high дать
исходные formulas и fixture entries без требуемого verdict; author не закрывает
собственный design или code review. Все исправления/retests вписываются только
в уже выделенный aggregate C08 budget; дополнительный process здесь не разрешён.

## 8. Приёмка implementation, что осталось неизвестным, STOP

Independent D review должен проверить: algebra/signs/units, missing-μ inheritance,
full-complex measure, literal finite-t expectations, side distinction, scratch
allocation census и strictly additive compatibility. Только после его approval
coordinator может выдать отдельный owning I medium. Review обязан сохранить
доказанное disagreement и cheapest resolving source/oracle question. Последующий
R source/code + выбранные admitted synthetic checks доказывают instrumentation
properties; они не дают native/scientific acceptance. Native arrays, admission,
εJ_abs/H и остальные error bounds здесь отсутствуют — их не изобретать.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| SCI03 §5.3 даёт отдельный absolute bound complex boundary current | Полный algebra+Cauchy proof §2; опубликованный Research §5.3 | Fixed represented exact arithmetic/f, не forward physical accuracy | сохранить |
| Existing aggregate FDR достаточно для восстановления RHS | Selected Results equilibrium.py:465–493,527–547 не сохраняет separate components/side norms | Concrete source gap, не измерение actual run | изменить |
| Gap закрывается без новых native inputs/read pass/fresh map | Все matrices уже читаются pass2; 12 streaming norms и reuse A/corrections §6 | Allocation census/code/runtime ещё не проверены | изменить |
| Literal fixture отличает основные norm/sign/side/weight mistakes | Независимые entries, rational norm/current table и finite-t formulas §7 | Design only; synthetic helper graph/encoding и libm scope явно ограничены | дополнительно измерить |
| Current source proves exact-final data/run bound | Ни одного immutable final array/run/attempt/frozen plan не дано | Metadata/current source не numerical evidence | данных недостаточно |
| Measured B означает scientific/current acceptance | Unknown εJ_abs, roundoff/domain/fixed-point/nonlinear contributions | Большой B может быть бесполезен; missing не0 | данных недостаточно |
| Native execution READY | Fresh admission/runtime binding отсутствуют | Design не создаёт execution grant | данных недостаточно |

Выполнено только чтение source/metadata, elementary ручной вывод и запись двух
/tmp документов. Read accounting не является telemetry каждого filesystem byte:
997352 PDF SHA bytes известны; выбранные text ranges/search corpus малы и без
scientific arrays/archives, общий source envelope≤6 MiB использован как предел
scope, а не заявленный измеренный I/O receipt. Полного native/test environment,
imports/parsers, HDF reads, Julia, solver, tests, benchmark, network, install,
build, Git mutation, children и server actions не было. C08 consumption=0.
STOP DESIGN; independent review ещё не выполнен.
