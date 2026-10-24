# DEV08 — propagation of the unchanged PV functional budget into ratios

Статус **DESIGN_CANDIDATE, independent high CP-DESIGN pending**.
Автор `/root/oracle_carrier_design`, D ultra, 2026-10-19. Этот пакет содержит
source/design и docs candidate; ни один Julia import/test/solver, Git command,
fixture/source-code edit или новая попытка исполнения автором не выполнены.
Текущие четыре test files остаются неизменными. Новый design не обнуляет
счётчик DEV08 и не меняет underlying Λ/physical acceptance tolerances.

## Нейтральный вопрос reviewer и первичные inputs

Вывести допустимую ошибку отношения двух center-only PV discretization errors
из существующих scalar functional comparisons, включая Float64 вычитание и
деление. Проверить, сохраняет ли proposed predicate прежний budget самого
функционала и различает ли первый порядок, второй порядок, common multiplier
и знак ровно в заявленной области. Не предполагать ошибку PV implementation.

Inputs: Core `a8d2c0de21dfdce3ed3c7c585c555656443f6d89`, owning
`docs/src/development/review_oracle_contracts.md::O08-06`, неизменённый
`test/numerics/principal_value_independent_oracle.jl` SHA256
`bae8a57957cd9df4da0d7369521a7d7ffa776b4c095859e0d1a9f86a9607eb6e`,
`src/numerics/reference/kernels.jl::direct_hilbert_transform`,
`src/numerics/optimized/production_operators.jl::fft_hilbert_transform`,
Julia 1.13 `base/floatfuncs.jl:222–228::isapprox`, original DEV08 GREEN-1
receipt/log. Первичные locators устанавливаются до чтения диагноза ниже.

Original failed evidence сохраняется без замены:

| Artifact | SHA256 |
| --- | --- |
| `/tmp/qcl-DEV08-GREEN-1/receipt.json` | `e0f7a3b5a8b2afb987232333d04cb3ab6a2600de25dc871f388af5836b8ef775` |
| `/tmp/qcl-DEV08-GREEN-1/original.log` | `495227f26beba7ca0b274de6e8f39bf6ada9e1015afbe21e41a7f000fb250fa7` |

Наблюдение из log: discrete/direct/FFT literal slice 13/13; continuum slice
107 pass/1 fail. Единственный failed predicate при line79 сравнивает
`1.969696969698286` с `65/33 = 1.9696969696969697` при
`ATOL=RTOL=2e-13`. Это exit1 targeted fixture, не fullCI/science. Receipt:
wall6.111s, sampled peak RSS518283264 bytes, original output1799 bytes.
Это чужая сохранённая execution evidence, не выполненный здесь runtime.

## Сохраняемый mathematical/functional contract

При Γ(x)=4+x на [-3,3], ноль снаружи, E=0 и W=3:

```text
L = -3/π,
hN = 2/N, N∈{17,33,65},
ΛN* = L + eN*,
eN* = hN/(2π) = 1/(Nπ) > 0,
eA*/eB* = NB/NA для NB>NA.
```

Сохраняются **все** existing finiteness, absolute center, omitted-cell,
tail/window, zero/discrete/mutation assertions; `ATOL=RTOL=2e-13`
сохраняются без изменения. `errors[i]` — Float64 subtraction именно
`centre - full_continuum`, не погрешность против другого оператора.
Отдельные значения нужны для sign/amplitude; ratio не заменяет их.

В Julia1.13 scalar isapprox criterion —
`abs(x-y) ≤ max(ATOL, RTOL*max(abs(x),abs(y)))`, а не сумма двух budgets.
В рассматриваемой ветви явные guards `0<x<1`, `0<y<1`, `ATOL=RTOL`
дают абсолютный branch `abs(fl(x-y))≤ATOL`. Перед ratio обязательно
проверить **отдельно пересчитанные** три measured errors против independent
`eN=(2/N)/(2π)` тем же строгим scalar isapprox. Старые underlying assertions
не удалять и не заменять одним widened centre/ratio comparison.

## Conditioning proof и outward interval

Пусть x,y — measured Float64 errors, a,b — Float64 independent eA,eB.
Строгие functional assertions дают отклонения не более существующего A=ATOL
в floating subtraction. Чтобы учесть его rounding без нового tolerance,
задаём `B=nextfloat(A)`: точная разность двух finite Float64, округлённая
в число ≤A по модулю, лежит строго внутри B. Для близких положительных
errors subtraction также точна по Sterbenz, но этот более сильный факт
для predicate не требуется.

Никакой empirical multiplier не подбирается. Формируем outward bounds:

```text
a_lo=prevfloat(a-B), a_hi=nextfloat(a+B),
b_lo=prevfloat(b-B), b_hi=nextfloat(b+B).
```

При `0<a_lo≤a_hi<1`, `0<b_lo≤b_hi<1` positivity позволяет делить:

```text
r_lo=prevfloat(a_lo/b_hi),
r_hi=nextfloat(a_hi/b_lo).
```

`prevfloat`/`nextfloat` учитывают округление endpoint subtraction/addition
и division; не изменяют input PV budget. Float64 division монотонно на
positive finite intervals, поэтому `fl(x/y)` лежит в [r_lo,r_hi].
Все endpoint/result values должны быть finite. Если lower denominator ≤0,
ratio ill-conditioned/unresolved: **не** подставлять floor, не менять A,
не утверждать ratio/order pass. Для N17/33/65 e65≈.0049≫A, guard имеет
запас и не требует изменения discretization.

Алгебра показывает причину amplification. При exact arithmetic
x=a+δa,y=b+δb, |δa|≤B,|δb|≤B,b>B:

```text
|x/y-a/b| = |b*δa-a*δb| / (b*|b+δb|)
          ≤ (B+(a/b)*B)/(b-B).
```

Для соседних N это около1e-10 как верхняя граница, хотя сами errors имеют
тот же A=2e-13. Это **derived bound**, не выбранный новый ratio tolerance;
точный predicate использует endpoints выше. Поэтому повторное применение
2e-13 непосредственно к ratio не следует из accepted functional budget.
Результат log сам по себе не доказывает ошибку underlying PV map.

Floating RHS `eN=(2/N)/(2π)` отличается от mathematical `1/(Nπ)` только
rounding независимых positive literals. Общий π сокращается в exact ratio;
поэтому retain independent mathematical ratio `ρ=NB/NA` и отдельно проверить
`r_lo≤ρ≤r_hi`. Это проверяет саму construction interval против independent
grid ratio, не читая tested helper. В текущей well-separated fixture width
от propagated A многократно больше elementary rounding RHS; source reviewer
должен подтвердить все endpoints, а не принять observed ratio как expected.

## Frozen future predicates (docs/design only)

Псевдокод использует Julia Base, без BigFloat/interval package/новой среды.
`positive_ratio_interval` — test-local helper, не production API. Он не
вычисляет a,b из actual operator output.

```julia
# Existing ATOL and RTOL remain exactly 2e-13.
nodes = (17, 33, 65)
expected_errors = [(2/N)/(2π) for N in nodes]
for i in eachindex(errors)
    @test isfinite(errors[i]) && 0 < errors[i] < 1
    @test 0 < expected_errors[i] < 1
    @test isapprox(errors[i], expected_errors[i]; atol=ATOL, rtol=RTOL)
end
@test errors[1] > errors[2] > errors[3] > 0 # retained

function positive_ratio_interval(a, b)
    B = nextfloat(ATOL)
    alo, ahi = prevfloat(a-B), nextfloat(a+B)
    blo, bhi = prevfloat(b-B), nextfloat(b+B)
    @test all(isfinite, (alo, ahi, blo, bhi))
    @test 0 < alo <= ahi < 1 && 0 < blo <= bhi < 1
    lo, hi = prevfloat(alo/bhi), nextfloat(ahi/blo)
    @test isfinite(lo) && isfinite(hi) && 0 < lo <= hi
    return (; lo, hi, alo, ahi, blo, bhi)
end
for (i,j) in ((1,2),(2,3))
    box = positive_ratio_interval(expected_errors[i], expected_errors[j])
    @test box.bhi < box.alo # independently separated adjacent error ranges
    rho = nodes[j]/nodes[i] # retained exact grid-ratio intent, rounded once
    @test box.lo <= rho <= box.hi
    measured_ratio = errors[i]/errors[j]
    @test isfinite(measured_ratio)
    @test box.lo <= measured_ratio <= box.hi
end
```

The helper tests must stop dependent interval assertions if finite/positive
preconditions fail; `@test` alone records failure but does not short-circuit.
Implementation should use a guard returning `nothing`/throwing a clearly
labelled fixture-precondition error after the failed assertion, not continue
division through invalid endpoint. No operator retry is implied.

For the separately recomputed errors add same-budget assertions as above;
do not assume the earlier W3 invocation's result is an assertion on a later
call. Do not edit the captured original test/receipt/log. Medium implements
only after high CP-DESIGN; the present task writes no test file.

## Cheap distinguishing controls, no extra operator evaluations

Use the same independent a,b and interval for each adjacent node pair;
test-local predicates check synthetic scalar numbers, not mock PV output.

| Case | Frozen predicate / purpose |
| --- | --- |
| Healthy errors a,b | strict scalar gates and finite ratio interval accept |
| Allowed independent perturbation x=a+A/2,y=b−A/2 | both strict scalar gates accept and propagated ratio interval accepts; no ad hoc ratio rtol |
| Constant refinement x=b,y=b | ratio1 lies outside interval; error-order claim rejected |
| Second-order ratio x=(NB/NA)^2*b,y=b | ratioρ² lies outside interval; retained first-order ratio rejected |
| Common multiplier x=2a,y=2b | ratio remainsρ, so ratio alone may pass; strict functional assertions reject both amplitudes |
| Common sign reversal x=−a,y=−b | ratio remainsρ, so ratio alone may pass; positivity and strict functional assertions reject |

Explicitly assert the stated accept/reject conditions. Common scale/sign
cases explain why ratio/order evidence cannot replace signed functional
evidence. They do not trigger additional direct/FFT operations or a new
scientific solve. Keep existing literal wrong-sign/diagonal/cyclic controls.

## Portable contract, implementation/runtime handoff and limits

Owning Core document receives this derivation under O08-06 as **pending
clarification**, while its original functional formulas/2e-13 budget remain
unchanged. That document also consolidates the separately accepted O08-02/04
complete carrier, reviewer b5b3f58… and root's exact-ND precondition. It
must contain sufficient formulas/predicates to stand alone, not require /tmp.
Root coordinator copies this design and review/failed-attempt references to
`docs/implementation/review-closure-2026-10-19/execution/evidence/`; this
author does not edit root evidence/checkpoint. Historical design status is
not rewritten as execution success.

After fresh high CP-DESIGN, medium may change only the two ratio comparisons,
add the same-budget per-error guards and these cheap synthetic controls in
the existing DEV08 test file. No production change or tolerance update.
New native attempt identity preserves GREEN-1 failure and original bytes;
it consumes the remaining invocation of the existing two-invocation DEV08
L-JL allowance. Future execution, if root binds it: one invocation ≤120s,
1 CPU/2GiB, ≤16MiB temporary/2MiB logs, shared native slot; no imports/setup
hidden outside existing ready environment. Timeout/OOM/source discrepancy →
preserve evidence and stop; no autonomous rerun. Runtime here remains0.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Targeted DEV08 GREEN-1 прошёл | Original log: 13/13 then107/108, exit1 | ratio failed, не fullCI/science | изменить |
| Ratio должен наследовать 2e-13 напрямую | Division identity has1/(e65−B) conditioning | input errors около.005, budget абсолютный | изменить |
| Underlying PV budget можно сохранить | Same isapprox gates + outward propagation, retained independent h/(2π) | Это regression policy, не FFTW forward-error theorem | сохранить |
| Ratio доказывает знак/амплитуду | Common scale/sign cancel from quotient | Separate functional and positivity checks mandatory | сохранить |
| Новый ratio predicate принят/проверен runtime | Только candidate derivation/docs | fresh high CP-DESIGN и medium/native впереди | данных недостаточно |
