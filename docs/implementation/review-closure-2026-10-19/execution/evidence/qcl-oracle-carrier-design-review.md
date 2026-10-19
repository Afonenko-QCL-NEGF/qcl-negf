# DEV02 carrier correction — независимый CP-DESIGN

Reviewer `/root/carrier_reviewer`, high, 2026-10-19. Проверен candidate
`/tmp/qcl-oracle-carrier-design.md`, SHA256
`17c6dda56a2223bde9d20e98928e659d9e60fb7d6615b72ff94dcf190b829ea1`.
Source root `04eecba1ea795a7c8861c4bfd0bb5aa49f093ee6`, Core
`a8d2c0de21dfdce3ed3c7c585c555656443f6d89`. Core tracked source чист;
два untracked файла DEV03/08 не использованы как oracle. Root содержит
параллельные изменения других компонентов/receipts. Gitlinks не обновлялись.

**Вердикт:** O08-04 / DEV06 **CP-DESIGN PASS в указанном functional scope**.
O08-02 / DEV04 — **одна обязательная конкретизация near-zero precondition**
перед I-ready; остальной carrier и assessment design согласованы. Общая
six-oracle readiness/scientific acceptance не установлены. Native runtime,
imports, Julia, tests, build, solver, SSH и source writes — 0. Выполнен только
source audit и `git -C components/QCLNEGF.jl diff --check` (exit0).

## Независимость

До чтения candidate самостоятельно установлены constructor lower bounds,
actual-grid measures, public current formula, healthy/nonneutral Poisson
nullspace equations, полный gate inventory assessment. Это передано root
двумя сообщениями до получения candidate. Собственный предложенный путь
`:none` для трёхузельной uniform цепочки совпал с candidate; собственное
первоначальное coherence раскрытие для a=1 затем независимо распространено
на candidate a=[1 2;3 4;5 6]. Чужая готовая рецензия не читалась.
Прочитаны AGENTS, architecture, Core CONTRIBUTING, qcl-physics-audit и
physics-checks, handoff DEV02/04/06, accepted passport и первичные RV08/RV09
source review. Родитель отдельно подтвердил допустимость required plain
GreenState/SelfEnergyFamily после полной локальной проверки полей.

## Единственная correction — здоровый Poisson source должен быть точно нулевым

Локатор candidate: строки142,323,331–345,351,366,384. Owning source:
`reference/grids.jl::build_profiles` вычисляет ND из scaled sheet density и
normalization; `poisson.jl:49–64` задаёт
`b=-λP*(ND-n)` и `rP=norm(LU-b)/(norm(b)+λP*1e-14)`.

Утверждение `ND≈ones(4)` с arithmetic tolerance не обеспечивает healthy
`rP=0`: пусть actual ND=(1+δ)ones, а n=ones. Тогда b константен,
U=0, rP=2|δ|/(2|δ|+1e-14). Уже δ порядка Float64 roundoff может дать
rP порядка 0.01. Поэтому нельзя молча считать literal ones совместимым
source после лишь приблизительной проверки builder output.

Минимальная заморозка, сохраняющая весь literal candidate без изменения RHS:
перед обоими direct Poisson вызовами и synthetic construction обязательно
проверить **точное** `problem.profiles.Nᴰ == ones(4)` (и uniform positive
wX/static assertions candidate). При false остановить DEV04, сохранить лог,
вернуть design; не менять n, допуски или expected values на лету.
Эта precondition честна и проверяема; runtime факт её выполнения здесь
не заявлен. Вписать её явно в frozen owning correction, а не оставить
обычным приблизительным profile assertion.

Равноценная более устойчивая альтернатива требует отдельной заморозки новой
версии: healthy_n=copy(ND), bad_n=healthy_n+ones4; доказать uniform ND=d,
положительность donor sheet, использовать synthetic R=2π²d и n=fill(d,4).
Тогда expected neutrality для bad должна быть
`sum(wX)/dot(wX,ND)` (при uniform d это1/d), а не literal1;
engineered spectral defect=|4πd−1|. При Δx=1 constant excess source по-прежнему
даёт ζ=λP/2 и rP=2/(2+1e-14). Не смешивать эту альтернативу с current
candidate или утверждать, что её implementation уже accepted.

Это замечание о полноте design и около-нулевой нормировке, не доказанный
runtime defect существующего builder. В рамках прежнего checked constructor
и Unitful algebra exact precondition вполне может выполняться; исполнения
для подтверждения не было.

## Проверенные положительные выводы

1. `types.jl:181–284` действительно требует Nz≥3,Nb≥1,P≥1,NE≥3,Nk≥2,
Nφ≥4,Nqz≥3; candidate пользуется checked constructors. `build_problem`
вызывает actual grids/profiles/basis/kernels/shifts и validate_problem.
Нет ручной подмены NEGFProblem/ModelGrids/BasisData, fake dimensions или
validate_static=false. Static validation само по себе не научный pass.

2. `grids.jl::build_grids`: ε=[−1,0,1],wE=[1/2,1,1/2],κ=[0,1],
wk=[1,3]/(16π). M=.05eV покрывает phonon .0367eV; trusted centre nonempty.
Field shift I и LO shift literals candidate корректны. Пустые microscopic
kernels согласованы с явно disabled manufactured options и e-e none.
Их нельзя переносить в неизменённый S1 all-five production model.

3. Полная analytic :none basis: Hcell=t tridiag(−1,2,−1),
φ1=(1/2,1/√2,1/2),φ2=(1/√2,0,−1/√2), E1=(2−√2)t,E2=2t.
Z12=−1/√2, spreads=(1/√2,1), T+=−t φ(last)'φ(first) совпадают с таблицей.
Фаза P определяется после independent basis assertion; Xactual=P'XliteralP
во всех Green/family блоках делает ΦXΦ† и traces invariant. Колонки
недегенеративны, фиксировать ненадёжный tie-phase LAPACK не требуется.

4. Кандидатные literal constants совпадают с source constants.jl:42–54
(это именно зафиксированный набор проекта, а не неявный внешний CODATA).
Независимая RHS не читает scale.J0/CODATA/helper. Поэтому regression budget
2e-14+2e-13 на scaled currents/ratios не должен поглотить ошибку единиц,
2π или общего multiplier. Этот budget — inherited policy, не uncertainty
фундаментальных констант и не экспериментальная точность.

5. При Q=[2 i;−i 1],B=[1 i;−i 2],F=I/2,D=I ручная trace даёт 6a−1.
S=[5 11;17 23;29 35], weighted rows=[38,86,134]/(16π).
Следовательно jE=[19,43,67]J0ref/(8π²E0eV), integral=43J0ref/(4π²).
Boundary flux отдельно сравнивается с тем же literal engineering electron
flow eΦ; conventional electrical-charge direction имеет противоположный
знак. Physical dE=[.05,.1,.05]eV обязательно.

6. Full literal Green/family identities и PSD корректны, но GR намеренно
не решение заданного D. Metadata всё же относятся к actual declared D:
D=[[ξ1+3i/4,−1/2],[1/2,ξ2+5i/4]],
tr(D†D)=ξ1²+ξ2²+21/8, |detD|²=(ξ1ξ2−11/16)²+
((5ξ1+3ξ2)/4)²; candidate κD и row-sum scale следуют отсюда.
Эти диагностические поля не объявлены малыми Dyson residuals. Полные
shape/finite/identity/phase/PSD/no-alias checks перед plain construction
соответствуют реальной границе unchecked internal containers.

7. Re Ggrid21=Re Ggrid32=−a/2. Weighted a sum=30/(16π)=15/(8π),
H12=H23=−t, gs/(2π)=1/π, поэтому bonds=[1,1]15tJ0ref/(8π²).
Diagonal-only и genuine Nb1 checked rebuild дают0 без renormalization.
Это derived finite fixture effect; spatially uniform J не становится
универсальным physical gate. Seam у bond_current отсутствует.

8. Для exact ND=n=ones4 direct Poisson healthy U=ζ=rP=rneutral=0.
Для n=2ones4 L cyclic, sP4,v=ones/2; incompatible b=λP ones даёт
U0,ζ=λP/2,rP=2/(2+1e-14),rneutral1. ζ sign/scaled bordered meaning верны.
rP без spatial weights, neutrality использует wX и положительный donor
denominator, gauge mean zero. Значения превосходят существующие declared
t.rP/t.rneutral/t.rζ; их нельзя заменить лишь surrogate rP>1/2.

9. Routing carrier с real_space Nb=Nz4 полный: R=2π²d,
GR=−iRI,G<=iRI,G>=−iRI,A=2RI,
ΣR=εI−hm−iI/R,Σ<=iI/R,Σ>=−iI/R. D=iI/R,κ1,scale1/R,
Dyson/Keldysh/Pauli identities и density d действительно получаются.
Equal split всех трёх Σ components согласует total/plus/minus. Empty
histories честны; converged SCBA tuple является явно synthetic branch
input, outer solution остаётся manufactured/nonaccepted. Нет claims
actual embedding/fixed-point solution. Spectral sum defect при d1=4π−1
явно показывает предел полного scientific pass.

10. `_validate_solution_metrics` missing base key→Inf; frozen полный
sentinel key list candidate соответствует `_solution_validation_limits`.
Полный fail с тремя bad diagnostics и три isolated single-gate fail tests
обязательны: один dropped gate иначе маскировался бы двумя оставшимися.
Synthetic zero sentinels не измерения; explicit marking и запрет scientific
assessment/persistence существенны. Optional consistent false classification
tuple отдельно различает quality branch.

## Controls и пределы приёмки

Sign/2π/wk/wE/physical dE mutations математически различимы при retained RHS.
Diagonal family trace4a−1 отличается от6a−1. Mean removal уничтожает fixed
nonneutral Poisson RHS. В runtime надо вызвать actual APIs/seam; повторение
formula в mock не закрывает gap. Это predicted distinguishing effect,
не выполненные mutation tests.

Нет полномочий или свидетельства SCBA/Poisson loops, solver convergence,
достаточности сетки/базиса, S1 all-five or experimental validation. O08-03/05,
DEV05/07 остаются blocked. Proposed tiny builder/direct5×5 operations
укладываются в конечный будущий packet; runtime/import admission и enforcement
остаются отдельными prerequisites и не исполнялись этим review.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| O08-04 carrier и literal functional RHS согласованы | Checked builder, exact sums, analytic eigenbasis/phase/D metadata | Source/design, runtime0, не Dyson solution | сохранить |
| O08-02 healthy near-zero branch полностью frozen | Candidate пока допускает обычный приблизительный profile check | ND≈1 не гарантирует b=0/rP=0 | изменить |
| O08-02 nonneutral и isolated assessment gates различимы | Nullspace equations + full synthetic gate list | После exact healthy precondition или separately frozen robust alternative | сохранить |
| Routing pass означает scientific acceptance | Engineered spectral defect4π−1, synthetic classification/sentinels | Full coupled equations/history не measured | данных недостаточно |
| O08-03/05 и S1 закрыты | Нужных independent RHS/measurements нет | Не область данного correction | данных недостаточно |
