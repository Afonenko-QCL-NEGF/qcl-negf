# Four manufactured Core oracles — independent CP-CODE

Вердикт по frozen files: **DEV03 и DEV08 CHANGES_REQUESTED для fixture arithmetic; DEV04/DEV06 source READY, runtime not_measured**. Production defect этими данными не установлен. Ни thresholds модели, ни operator/physics менять оснований нет. Reviewer не выполнял Julia, imports, tests, solver или numerical script; прочитаны source, frozen tests, затем accepted passports/correction/review, author reports и сохранённые root runtime receipts.

## Immutable scope

Root observation `cbb24a61344a947761b6c049a6bb6687e14cff04`; Core HEAD `a8d2c0de21dfdce3ed3c7c585c555656443f6d89`. Root parallel dirty state не входил в owning review. Core tracked diff empty; ровно четыре новых untracked files. Source/Project/Manifest diff против HEAD empty. Прочитаны root architecture/AGENTS, Core CONTRIBUTING/architecture, qcl-physics-audit/physics-checks, handoff DEV03/04/06/08 и actual owning operators/builders/assessment.

| Card | Frozen file | SHA256 |
| --- | --- | --- |
| DEV03 | test/numerics/keldysh_literal_matrix_oracle.jl | `9a22526d104dc15e25b203a52631687819999ea1c84872627199c00062373d42` |
| DEV08 | test/numerics/principal_value_independent_oracle.jl | `bae8a57957cd9df4da0d7369521a7d7ffa776b4c095859e0d1a9f86a9607eb6e` |
| DEV04 | test/physics/nonneutral_periodic_poisson_assessment.jl | `3cd3ef409e82e790bfe1581c392cf1d3209900d4c753e419564d5f583518beaa` |
| DEV06 | test/physics/nonzero_public_current_oracle.jl | `17fed2fae5b45549c65cec576cc108f68922a04e3830c0246313ccafd4ee8d01` |

Accepted owning `docs/src/development/review_oracle_contracts.md` плюс carrier correction `/tmp/qcl-oracle-carrier-design.md` SHA256 `17c6dda56a2223bde9d20e98928e659d9e60fb7d6615b72ff94dcf190b829ea1`, independent design review `b5b3f58eb879272ed4be2081f36fa5c21c9f3733e961951d4649b6feb2edc348`. Root selected exact ND precondition. Author reports прочитаны после собственного source/arithmetic вывода: numerical report `c895e43ca99a2da2813435c99aeb8cf14179d5df8e35d46e34f462ec23d13339`, carrier report `4b813b86955105ce075d65340f2417cbb132d80ee30cab464016b6333250a1ff`. Reports не заменяют assertions/runtime. `git diff --check` exit0; не выполнялись full CONTRIBUTING suite/docs commands из-за explicit bounded read-only scope.

## F03 — P2: exact determinant использует rounded LU helper

Локатор: DEV03 file21; actual Julia1.13 LinearAlgebra `src/generic.jl:1838–1845`, `lu.jl:587–599`.

Независимое scalar раскрытие даёт GR*C=[[2−3i,2+i],[−1−2i,2−i]], B=GR*C*GR†=[[7,3+4i],[3−4i,5]], G<=iB. Точные Gaussian-integer entries, anti-Hermitian relation и positive principal minors корректны: detC=2−1=1, detB=35−25=10; first minors2/7>0. Literal expected RHS не обращается к target/helper, noncommutativity и четыре fixed-RHS wrong variants различимы.

Однако `det(B)==10` не является исключительно Gaussian-integer computation: generic det nontriangular ComplexF64 matrix вызывает LU; det(LU) перемножает rounded pivots. Elimination содержит division by7, которая не exact binary64. Exact equality поэтому необоснованно распространена с проверяемого matrix product на отдельный library factorization.

Root `/tmp/qcl-DEV03-GREEN-1/{receipt.json,original.log}` относится к exact frozen hash: 15pass/1fail/0error, единственный fail — composite predicate file21; all-entry actual/expected, anti-Hermitian/norm и остальные controls прошли. Exit1/wall4.710s/complete raw1429B/stopnone; sampledRSS506,245,120B, не hard-cgroup proof. Raw не печатает фактическое det value; конкретная причина `det(B)==10` выводится из independently exact known B/trace и actual stdlib path, а не из выдуманного printed number.

Минимальная correction: retain literal RHS и exact entry product assertions; principal minor раскрыть непосредственно `B11*B22−B12*B21 == 10` (аналогично C для прозрачности). Здесь все operations малы Gaussian integers и exact. Это сохраняет PSD certificate без arbitrary tolerance и не меняет production. После нового frozen hash нужен bounded current fixture result; исходный failed receipt сохранить.

## F08 — P2: ratio assertion не наследует error budget функционала без propagation

Локаторы: DEV08 file69–79, особенно79. Root `/tmp/qcl-DEV08-GREEN-1` exact frozen hash: discrete literal13/13pass; continuum107pass/1fail/0error. Только `errors[2]/errors[3]≈65/33` при atol=rtol=2e−13 не прошёл: actual1.969696969698286, expected1.9696969696969697. All direct functional/finite-window/omitted-cell/tail/positivity checks прошли. Receipt exit1/wall6.111s/complete raw1799B/stopnone, sampledRSS518,283,264B; не scientific failure и не full test PASS.

Source `_direct_hilbert_ordered` использует wjΓj/[2π(Ei−Ej)] без diagonal, FFT zero-padded linear counterpart извлекает тот же discrete map. Independent rows для [-1,0,1],w=[1/4,1/2,3/4],Γ=[1,2,4]: two-term sums −5/(4π),−11/(8π),9/(16π). Оба APIs проверяются против этих литералов отдельно, не только друг против друга. Wrong sign/finite diagonal/cyclic endpoint controls сохраняют RHS.

Continuum: при E0=0 integrand=−(4/x+1)/(2π), odd term cancels; compact support/window даёт −min(W,3)/π. На odd cell-centred grid omitted central cell даёт **+h/(2π)**, missing W1 tail добавляет error2/π; W3/W5 имеют одинаковый support. Refinement error ratio в точной арифметике33/17 и65/33 выведен верно. Это center-only omitted-diagonal operator, не product integration, не general physical tail bound.

Но errors получаются вычитанием O(1) continuum из computed centre, затем делятся на O(h) error. Тот же2e−13 budget ratio не следует из base functional2e−13: cancellation/division усиливают propagated absolute errors. Если e_i=a_i+δ_i, |δ_i|≤B_i и a_j>B_j, то

`|e_i/e_j−a_i/a_j| ≤ (B_i+(a_i/a_j)*B_j)/(a_j−B_j)`.

B_i должны быть заранее выведены из **неизменённых** base-functional budgets с rounding subtraction/literal assumptions, не подогнаны к observed ratio. Равно допустим заранее derived cross-product comparison с соответствующей propagation. Новый generic tolerance/production change не обоснован. Parent сообщил отдельный ultra D packet для этой конкретизации; он данным review не принят автоматически. Current DEV08 остаётся CHANGES_REQUESTED до frozen derivation/source correction и bounded rerun по отдельному счётчику.

## DEV04 — source READY в direct Poisson + synthetic routing scope

Carrier build_problem использует checked constructors: Nz=Nb4,:real_space,NE3,Nk2,P1,Nφ4,Nqz3; actual grids/profiles/basis/shifts и static gates сохраняются. Нет unchecked NEGFProblem/ModelGrids/BasisData reconstruction. Manufactured disabled microscopic scattering явно отделено от protected all-five S1. Все mutable plain Green/self-energy fields имеют shape/finite/no-alias/identity/PSD checks перед сборкой.

Прямое independent решение: wX1,εr1, cyclic L diag2/offdiag−1, sP4,v=ones/2. Для exact ND=n=ones RHS0→U=ζ=rP=rneutral0. При n=2ones b=λones и projection на nullspace даёт U0,ζ=λ/2; norm(b)=2λ, поэтому rP=2/(2+1e−14), neutrality1, mean-zero gauge. Own code poisson.jl49–65 соответствует этим sign/scaled conventions. Existing declared t.rP/t.rneutral/t.rζ проверяются отдельно, margin rP>1/2 их не заменяет.

**Mandatory near-zero guard реализован:** file173–175 exact ND==ones4 @test AND fatal error до solves177–178 и до synthetic construction198. Если Float64 builder не даёт exact1, card должна stop/replan, не подставлять actual ND в expected RHS и не ослаблять tolerances. Это runtime precondition, пока not_measured.

Real-space basis H0=t tridiag(−1,2,−1),T+=−t e4e1†,Φ=χ=I,spreads0,all-four eigenvalues2t[1−cos(jπ/5)] согласованы с actual builder. R=2π² synthetic family даёт D=iI/R,GR=−iRI,Gl=iRI,Gg=−iRI,A=2RI; Keldysh/Dyson algebra, densityR/(2π²)=1, condition1/scale1/R верны. Equal plus/minus split всех трёх Σ, empty iteration histories и explicit synthetic classification согласованы. Spectral residual4π−1 проверяется явно — полного scientific pass нет.

Frozen SYNTHETIC_GATE_KEYS160–167 не выводится из target limits. Healthy synthetic sentinels + measured healthy3 pass только policy routing; actual incompatible3 дают ровно именованные3fail; три isolated gates213–218 отличают drop каждого релевантного gate от маскировки двумя другими. Target `_validate_solution_metrics` вызывается непосредственно. Outer solution остаётся !converged,reportfalse,statusmanufactured_routing. Synthetic zeros не представлены measured physical diagnostics; no solution_scientific_assessment/persistence call. Sine refinement anchor reused as unchanged source, не скрыто reexecuted.

## DEV06 — source READY в public current functional scope

Независимые SI literals совпадают с **зафиксированным source constants.jl42–54**, а не с неявным более точным внешним CODATA. J0ref=e E0J/(ħ L0²),λref=e²/(ε0 E0J L0),t=ħ²/(2m0 mr E0J L0²). Expected current не читает target scales/CODATA/helpers; actual SI scale ratios отдельно asserted. Это regression fixed-constant code verification, не uncertainty fundamental constants.

Actual checked3×2 measure: ε=[−1,0,1],wE=[.5,1,.5],κ=[0,1],wk=[1,3]/(16π). Analytic three-cell eigenvectors φ1=(.5,1/√2,.5),φ2=(1/√2,0,−1/√2), E1=(2−√2)t,E2=2t; spreads1/√2,1; Z12=−1/√2; seam matrix file102 правильна. Basis readback используется только для phase transport после independent analytic overlap/Φ assertions; every Green/family block X=P†XliteralP. Это не построение expected RHS из actual basis.

For Q=[[2,i],[−i,1]],B=[[1,i],[−i,2]], trace BQ=6; trace Σg Gl−Σl Gg=6a−1. For amplitudes rows[1,2],[3,4],[5,6] weighted traces дают [19,43,67]/(8π²). Physical dE=E0eV[.5,1,.5], integral43/(4π²); e*boundary_flux отдельно получает тот же SI coefficient. Dimensions проверяются `ustrip` в A/m²/eV,m−2s−1,A/m². Retained wrong sign/2π/wk/wE/physical dE distinctions ненулевые и не поглощаются budget2e−14+2e−13 scaled units.

Coordinate coherences дают Re G21=Re G32=−a/2; H12=H23=−t, weighted Σa=15/(8π),gs/(2π)=1/π, hence both bonds15t/(8π²). Diagonal-only даёт0; genuine checked Nb1 rebuild и full (3,2,1,1) Gl=2ia даёт0. Нет charge renormalization, seam/current conservation или universal uniform-J acceptance claim.

Green/family PSD/anti-Hermitian/Keldysh identities проверены, но manufactured GR не объявлен Dyson solution. Metadata имеет independent actual declared D=[[x+3i/4,−1/2],[1/2,y+5i/4]],traceD†D=x²+y²+21/8,|detD|²=(xy−11/16)²+((5x+3y)/4)² и row-sum scales; condition derivation согласована. All-zero/unchecked metadata или false SCBA acceptance не вводятся.

## Evidence levels и решения

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| DEV03 Keldysh matrix functional literal верен | independent component expansion; saved15pass incl exact output | exact LU det auxiliary fails; current file notgreen | изменить fixture arithmetic |
| DEV08 discrete/center formulas верны | independent scalar/PV derivation;13+107 passing assertions | ratio budget lacks propagation,1fail | изменить derived ratio contract |
| DEV04 source implements fixed Poisson/gate distinctions | exact donor fatalguard, independent bordered RHS,3isolated actual gates | runtime not_measured; routing не science | сохранить; дополнительно измерить |
| DEV06 source implements signed public current/coherence | SI/constants/phase/weights/component sums and negative distinctions | runtime not_measured; functional GR notcoupledsolution | сохранить; дополнительно измерить |
| Production changed/bug established | tracked source unchanged; saved failures localise auxiliary arithmetic | no production defect proof | сохранить production |
| Iterative convergence | новые SCBA/outer loops отсутствуют | none measured | данных недостаточно |
| Physical solution gates/discretization | manufactured code assertions; finite center PV error only | no S1/all-five/final-state or general domain proof | данных недостаточно |
| Experimental validation/full release | evidence отсутствует в scope | unit/code fixtures не experiment/CI | данных недостаточно |

DEV05/full-U-G oracle и DEV07/scattering absolute prefactors остаются blocked. Original failed logs/receipts и frozen hashes сохраняются; исправления не дают права на автоматические дополнительные runs или scientific parameter/tolerance change.
