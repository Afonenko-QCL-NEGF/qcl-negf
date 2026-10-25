# DEV08 ratio budget и owning carrier consolidation — independent high review

Reviewer `/root/carrier_reviewer`, high, 2026-10-19.

Проверены два отдельно зафиксированных объекта:

- PV candidate `/tmp/qcl-pv-ratio-budget-design.md`, SHA256
  `cdbed6971dce106613face5c1235f7ab914a49ba1fdadf8c1987a37002d4b17c`.
- Owning Core `docs/src/development/review_oracle_contracts.md`, SHA256
  `61508afc44b57954b2d1c5d843c333aa8fb4a14fb9a1b1ffa811afc0798fece3`,805 lines.

Source identity предоставлена coordinator: root04eecba1ea795a7c8861c4bfd0bb5aa49f093ee6,
Corea8d2c0de21dfdce3ed3c7c585c555656443f6d89. Новый Git command не выполнялся.
Файлы читались в active review-closure-exec workspace. Product/test/source
writes, imports, Julia/native execution, solver, installs, benchmarks, SSH,
subagent spawn — 0. Единственная запись reviewer — этот /tmp receipt.

**PV CP-DESIGN: PASS** для proposed interval propagation при сохранении
всех strict per-error и underlying Λ assertions. Нет concrete scientific
или arithmetic blocker. **Owning consolidation: PASS TEXT/DESIGN**:
accepted carrier17c6…/reviewb5b3… перенесены полностью, exact-ND fatal
condition включена, ratio candidate self-contained и честно pending.
Native acceptance нового ratio predicate и DEV04 donor guard этим review
не установлена. DEV05/07 остаются blocked.

## Независимость и источник semantics

Непосредственно прочитан actual bundled Julia1.13 Base:
`components/QCLNEGFRunner.jl/.build/julia/share/julia/base/floatfuncs.jl:222–228`.
Формула Number isapprox действительно:
`x==y || (isfinite(x)&&isfinite(y)&&norm(x-y)<=max(atol,rtol*max(norm(x'),norm(y'))))`
с default norm=abs. Это max, не сумма absolute/relative budgets.
Actual fixture, operators и original log/receipt прочитаны до основного
/tmp PV candidate. Ограничение строгой blind source-first процедуры:
первое чтение owning документа уже вывело pending ratio text до прямого
чтения Base source. Root уведомлён. Поэтому этот отчёт — самостоятельная
проверка algebra/source без диагноза другого reviewer, но не утверждение
идеально blind порядка показа всех candidate материалов.

Raw evidence соответствует заявленным hashes:
GREEN1 log495227f26beba7ca0b274de6e8f39bf6ada9e1015afbe21e41a7f000fb250fa7;
receipt e0f7a3b5a8b2afb987232333d04cb3ab6a2600de25dc871f388af5836b8ef775;
actual unchanged fixture bae8a57957cd9df4da0d7369521a7d7ffa776b4c095859e0d1a9f86a9607eb6e.
Log: discrete13/13, continuum107 pass/1fail, exit1. Failed line79:
1.969696969698286 versus65/33=1.9696969696969697 at ATOL=RTOL2e-13.
Receipt wall6.111s, sampled peak RSS518283264bytes, output1799bytes.
Это сохранённое исполнение другого агента; reviewer не запускал тест.
Ни raw log, ни receipt не переписаны.

## Собственный вывод propagation

Owning old O08-06/direct operator определяет omitted-diagonal map
Σ(j≠i)wjΓj/[2π(εi−εj)]. Для Γ=4+x, target0, symmetric compact support
[-3,3] constant symmetric terms отменяются, каждый ненулевой linear cell
даёт−h/(2π). При W3 число contributing cells3N−1, h=2/N:
ΛN*=−3/π+1/(Nπ), eN*=1/(Nπ)>0. Поэтому exact adjacent error ratio
ρ=NB/NA. Это center-only manufactured discretization, не all-energy PV
error theorem и не SCBA/physical spectrum.

1. Пусть measured x и independent expected a — finite Float64,0<x,a<1,
A=ATOL=RTOL=2e-13. Relative branch≤A, поэтому actual scalar gate равносилен
`abs(fl(x−a))≤A` (с отдельной equality branch, также покрытой).
Guard0<x<1 проверяется для заново вычисленного error-loop значения;
ранний отдельный W3 вызов не заменяет этот gate.

2. В стандартной Float64 RoundNearest точная разность δ, округлённая в
Float64 с |flδ|≤A, удовлетворяет |δ|<nextfloat(A)=B. Соседний Float64 B
лежит дальше верхней середины rounding cell A. Здесь subtraction близких
положительных x,a дополнительно точна по Sterbenz, но это не нужно для
безопасности bound. B — enclosure existing scalar predicate, не новый
PV tolerance. Отсутствующий/nonfinite/negative error не подменяется нулём.

3. Для независимо вычисленных Float64 a,b интервалы
alo=prevfloat(fl(a−B)),ahi=nextfloat(fl(a+B)),
blo=prevfloat(fl(b−B)),bhi=nextfloat(fl(b+B))
содержат x,y, прошедшие указанные строгие gates. Каждое расширение на
соседний representable value ограждает округление одной endpoint operation.
При проверенных finite positive endpoints quotient монотонен по numerator
и антимонотонен по denominator. Поэтому
lo=prevfloat(fl(alo/bhi)),hi=nextfloat(fl(ahi/blo))
содержит и exact x/y, и округлённый measured Float64 quotient. Для
последнего достаточно monotonicity correctly rounded positive division;
дополнительный outward step сохраняет enclosure. Ни floor, ни empirical
multiplier не нужен. Nonpositive lower denominator — unresolved/stop.

4. Exact perturbation identity независимо даёт
|x/y−a/b|=|bδa−aδb|/(b|b+δb|)
≤B(1+a/b)/(b−B).
Для17/33 первая asymptotic half-width≈6.10e-11, для33/65≈1.21e-10.
Это conditioning, а не новое произвольно выбранное rtol. Endpoint predicate
лучше fixed decimal ratio budget и сохраняет exact underlying A.

5. Endpoint safety проверена аналитически без численного исполнения:
e17 между.0187,.0188; e33 между.00964,.00965; e65 между.00489,.00490.
Все четыре endpoints finite,positive,<1 и adjacent boxes строго разделены:
минимальный gap между error levels больше.0047, тогда как расширение
каждого≈2e-13. Простые консервативные quotient enclosures находятся в
ρ±6.2e-11 иρ±1.3e-10 соответственно (с запасом на endpoint/division ulps).
Величины2/N,2π и final division имеют rounding порядка few ulps от
mathematical1/(Nπ), намного меньше A. Exact true errors также внутри boxes;
округлённый once ρ=NB/NA лежит глубоко внутри quotient interval.
Предложенный runtime assertion lo≤ρ≤hi независимо удерживает эту связь.
Эти оценки проверяют наличие и размер интервала; точные endpoint bits и
actual future errors не заявляются исполненными/измеренными.

6. Observed ratio discrepancy≈1.3163e-12 существенно меньше conditioning
bound, но этим фактом нельзя автоматически объявить будущий тест прошедшим:
обязательные per-error gates заново пересчитанного error-loop и implementation
guards ещё должны исполниться. GREEN1 failure не устанавливает operator bug.

## Distinguishing controls и обязательные implementation условия

Healthy a,b и independent allowed perturbation a+A/2,b−A/2 проходят тот же
strict input gate; quotient содержится в box по доказательству. Округление
этих additions много меньше A/2 и не меняет acceptance утверждения.
Ratio1 расположен на расстоянии более.94 от обоих first-orderρ, аρ²
отличается отρ более1.8: интервалы ширины≈1e-10 исключают оба. Это
negative order controls, не выполненные operator mutations.

Common multiplier2 сохраняет quotient (для normal Float64 scaling на2
точен), но нарушает retained eN amplitude gates на величину eN≫A.
Common negative sign сохраняет quotient, но нарушает positivity и amplitude
gates. Следовательно ratio не доказывает ни знак, ни абсолютную амплитуду;
эти отдельные checks обязательны. Candidate и owning text это сохраняют.

Содержательный contract готов к bounded implementation:

- Сохранить ATOL=RTOL2e-13, все underlying discrete/center/window/tail/zero
  comparisons и wrong-sign/diagonal/cyclic controls без изменения.
- Только два старых direct ratio isapprox заменяются derived interval;
  добавить три strict same-budget per-error comparisons для actual error-loop,
  positivity/finiteness/order и дешёвые scalar controls из candidate.
- Endpoint tests должны **останавливать** dependent division при invalid
  precondition. @test сам продолжает execution; prose candidate159–163 и
  owning741–744 явно требует real guard/throw/return. Псевдокод не выдаётся
  за готовую безопасную реализацию без этого guard.
- Expected errors, endpoints и ρ не вычислять из operator output. Подстановка
  observed failed ratio как RHS/tolerance недопустима.
- GREEN1 original artifacts и invocation count сохраняются. Новая попытка
  потребляет оставшуюся DEV08 invocation; нет нового бюджета/retry/reset.

Это сохраняет physical criteria и regression gate самого Λ. Сравнение
quotient логически слабее исходного произвольно строгого quotient2e-13,
но заменяется обоснованным следствием исходных неизменённых functional
предпосылок; signed/amplitude operator evidence не ослабляется.

## Owning document consolidation — отдельная проверка

Сопоставлены carrier candidate17c6… и reviewerb5b3… с current owning61508…,
не только между собой, но и с ранее прочитанными actual constructors,
grids/basis/observables/Poisson/validation seams. Перенос не потерял:

- Проверенные минимальные NE3,Nk2,Nφ4,Nqz3,Nz3,Nb2,P1,checked builder,
  :none/:real_space choices, actual trapezoid/annular weights, trust margin,
  qz/angular grids, all profile/kernel/shift/models fields.
- Полные analytic basis Φ/χ, centres/spreads,overlap,H0/Z/M−1/T±,energies,
  Egrid0 и measured static residual inventory. Phase P transport применяется
  ко всем literal Green/family matrices; genuine Nb1 rebuild без renormalization.
- Независимые SI constants,J0ref/λref/t и units; current literal trace6a−1,
  resolved[19,43,67]/(8π²), integrated43/(4π²), bonds15t/(8π²), scaled
  atol2e-14/rtol2e-13, zero branch и retained-measure mutations.
- Все plain Green/family fields включая analytic D condition/scale metadata,
  finite/shape/identity/PSD/no-alias checks; functional current GR не выдан
  за Dyson/SCBA solution.
- O08-02 **fatal exact** `ND==ones(4)` перед любым Poisson и synthetic
  construction, stop+preserve failure приfalse; нет скрытого перехода к
  альтернативе n=ND/изменённой neutrality. Healthy U0 и incompatible
  ζλ/2,rP2/(2+1e-14),neutral1, gauge/weights/near-zero смысл сохранены.
- Полную real_space engineered routing assemblyR2π², same-state density1,
  explained U/metadata/plus-minus splitting, synthetic classification tuple,
  пустые настоящие истории, полного explicit base gate key list и three
  isolated gate-drop controls. Sentinel zeros явно routing inputs, не
  measured scientific values. Spectral defect4π−1 и запрет scientific
  assessment/persistence не потеряны.
- DEV05/O08-03 и DEV07/O08-05 blocked, неизменный S1 all-five/e-e-none,
  functional scope и научные ограничения, finite future packet/shared counter.

Owning O08-06 содержит весь смысл propagation, endpoint equations,
independent expected-errors/grid ratios, precondition stopping rule,
scalar controls и сохранение original failure; нормативная реализация
не зависит от /tmp candidate. Hashes/raw receipts — provenance, не замена
формул. Заголовок различает historical functional acceptance и pending ratio
clarification; нет claiming нового runtime pass. Review root receipt path
для carrier существует в integration workspace. Полные docs build/link crawl
не выполнялись и не разрешались.

Проверенные чужие runtime сведения строго ограничены: DEV06 original log
содержит248/248 passed. Это supplement, не основание design verdict и не
повторное исполнение reviewer. DEV04 GREEN1 original log содержит parse
error при `κ[m]^2.*I4` до assertions. Отсюда **не следует**, что exact donor
guard прошёл; corrected whitespace и pending repeat не являются witness
его исполнения. Owning exact-ND condition — contract, не runtime promise.

| Утверждение | Свидетельство | Ограничение | Решение |
| --- | --- | --- | --- |
| Ratio interval следует из неизменённого A | Actual Base isapprox, positive endpoint enclosure и division identity | Для strict guarded Float64 inputs, не general FFTW error theorem | сохранить |
| PV operator/test полностью прошёл | GREEN1 13 discrete+107/108 continuum, exit1 | Новый predicate не исполнялся | данных недостаточно |
| Ratio различает order | 1 иρ² отделены отρ более.94/1.8 против widths≈1e-10 | Scalar controls должны быть исполнены | сохранить |
| Ratio различает sign/common amplitude | Оба сокращаются в quotient | Нужны сохранённые positivity/amplitude gates | сохранить |
| Owning61508… переносит accepted carrier без /tmp-only contract | Complete formulas/fields/phase/SI/exactND/routing/predicates сопоставлены | Docs TEXT/DESIGN, no native/docs build | сохранить |
| DEV04 donor guard уже имеет runtime witness | GREEN1 остановился parseerror до assertions | Corrected repeat pending | данных недостаточно |
| DEV05/07 либо S1 science закрыты | Coupled/absolute/scientific evidence отсутствует | Не область данного review | данных недостаточно |
