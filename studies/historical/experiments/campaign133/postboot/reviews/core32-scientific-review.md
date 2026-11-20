# Core #32: independent scientific review of residual cost

**Вывод:** raw gates в `_production_fixed_point_measurement` не являются
checkpoint diagnostics. Их нельзя заменить mixed-step norm, одним residual
суммарной Σ, occupancy-weighted subset или прошлым измерением. Одна узкая
семантически безопасная оптимизация найдена: отложить **только witness-only
Hermiticity scan/materialization** до строгого нового chunk winner. Ни один
sign/eigensolver/raw-equation check это предложение не удаляет. Реализации
и измеренного ускорения нет; Julia/Pkg/HDF/profiler reviewer не запускал.

**Identity.** Новый workspace — каталог артефактов, не Git checkout.
Read-only `core-accepted-science` HEAD e171caa60cce676c6c4238dd671e7c527f2bd977,
tree742ed5a6fe82f1e5c63fc1a2290ed77f89ca6da8, clean. Accepted final Core и
локальный origin/main `core-final-integration` —
db26a0ef49673d8246ae336cbe73bafe6d7482ac, tree073abe5070b6ca60822f5a9b1b139c614ec3e16f,
clean/detached. Live remote ref не обновлялся. Между e171 и db26 побайтно
совпадают **все** `production_iteration.jl`, `residuals.jl`,
`positivity_diagnostics.jl`, `final_audit.jl`; вывод ниже применим к обоим.
Основные SHA: iteration ff466263…, residuals0f95accf…, positivity796cdde4…,
final_audit97736710…. Чужие файлы/active solver не менялись.

## Обязательный научный контракт

Локаторы ниже относительно `src/`. Основной вызов:
`numerics/optimized/production_iteration.jl:2`; измерение **до mixing** и
перед assessment/checkpoint — `optimized/production_solver.jl:577–726`.
G и stored total принадлежат одной итерации; candidate — свежая raw Φ от
этого G. Здесь Σc означает candidate total, Γ=i(Σ>−Σ<) — **stored** total.

| Gate | Точная область/нормировка | Зачем сохранять |
|---|---|---|
| rD | max(E,k) `||D GR−I||F/(||D||F||GR||F+sqrt(Nb))`, D=εI−h−ΣR | Dyson backward residual stored state; не condition estimate |
| rA | `||A−GR Γ GA||F/(||A||F+1e−14)` по всем E,k,a,b | spectral identity с stored Σ; не PSD и не fresh-map convergence |
| rK | `||G<−GR Σc< GA||F/(||G<||F+1e−14)` по всем E,k,a,b | fresh unmixed Keldysh equation; candidate product НЕ делится на λ |
| rΣ | max каждого R/< /> residual **каждой** enabled scattering и embedding/plus/minus family; denominator fresh component norm+1e−14 | total Σ допускает cancellation отдельных механизмов и не эквивалентна этому максимуму |
| rλ | `abs(Nraw/ND−1)` | независимый charge constraint; normalized published density не доказывает λ≈1 |
| rPSD | max по A,−iG<,+iG>,Γ,−iGRΣ<GA,+iGRΣ>GA и всем E,k | проверяются normalized **и raw** occupation/hole; перераспределение числа не должно скрывать плохой raw input |
| rcaus | max(E,k) `max(0,eigmax(ImΣR))/(||ΣR||2+1e−14)` | полный generally nonnormal ΣR в denominator; norm(ImΣR) его не заменяет |

Все F-нормы rA/rK/rΣ **без** wE/wk: это unweighted algebraic full-domain
contract (`optimized/residuals.jl:589–767,804–868`). Взвешивание добавляет
другой критерий. Число N использует исходные wE·wk и gs/(2π). D/Σ заданы
в scaled E0, G/A — inverse E0; additive floors относятся к этим solver
units. Возле нуля rA/rK/rΣ используют именно +1e−14: zero/zero fields→0,
nonzero difference при нулевой candidate norm НЕ исчезает. rD denominator
имеет sqrt(Nb). NaN/Inf/overflow/eig failure дают Inf, не pass.

PSD version3 (`reference/positivity_diagnostics.jl:75`): для Herm(X)
`s=maxabs(eigenvalues)`, `b=64 Nb eps max(s,1)`,
`ratio=max(0,−λmin−b)/max(s,floatmin)`. Это declared scaled backward budget,
не clipping и не доказательство exact PD. Hermiticity defect — отдельное
witness field, **не вход этого ratio/приёмки**. Causality уже имеет safe
fast path: при exact numerator0 и конечном Frobenius bound полного ΣR SVD
не вычисляется (`residuals.jl:464`); нельзя обещать ещё одно такое сокращение.

Default tolerances (`domain/types.jl:296`): rD1e−11,rA1e−9,rK/rΣ/rλ1e−8,
rPSD/rcaus1e−10. Полный SCBA gate также включает rroundoff и rJ/rpopulation
stability (`domain/numerical_convergence.jl:108`), минимум итераций/streak.
Они не заменяют fresh raw gates. Physics markers имеют собственную cadence,
checkpoint request лишь публикует aligned state; это отдельные фазы.
`_production_positivity_witness` уже читает готовые chunk summaries **без**
нового eigenscan. Финальный independent fresh audit не дубликат старой row:
`reference/final_audit.jl:33–95` повторно проверяет опубликованный last-source
state/candidate, включая candidate Dyson/spectral/charge. Его нельзя удалить
на основании совпадения checkpoint history.

## Одна узкая оптимизация и её границы

`optimized/residuals.jl:414–451`: после обязательных finite/Herm/eig checks
helper безусловно считает 25-entry Hermiticity norm, создаёт witness, затем
сравнивает `witness.ratio > sink[c].ratio`. По прямому чтению
`positivity_diagnostics.jl:75–104` ratio/budget не зависят от Hermiticity.
Для **отбрасываемого** witness этот scan/payload не влияет ни на rPSD,
ни на winner, ни на acceptance; даже его overflow сейчас лишь discarded
diagnostic, а не отдельный gate. Поэтому допустима lazy winner construction:
все eigenvalues/scalar ratio/finite checks остаются; full Hermiticity field
вычисляется только при том же строгом `>`.

Сохранять одну реализацию scalar formula, budget version, empty ratio−1,
первый tie, chunk/global canonical winner, все coordinates/kind/fields.
Winner Hermiticity следует вычислить **сразу**, пока Γ/temporary2 ещё
принадлежит данному блоку: отложенный scan по reused scratch даст другой
source. При отсутствии sink возвращаемый scalar также не меняется.
Это не разрешение пропускать шесть PSD checks или причинность. Heap-allocation
выигрыш не доказан: immutable witness может оптимизироваться компилятором.

Workspace уже сохраняет per-worker матрицы/LAPACK и per-block norm terms.
Не запускать family residuals одновременно с одним workspace: scratch
векторы переиспользуются и это создаст races. Fusing norm loops допустимо
лишь с раздельными R/< />/family accumulators и тем же inner/canonical
sum order; оно не уменьшает научную область проверки. Parallel tree
reductions, fastmath или иной denominator меняют arithmetic contract и
near-threshold решения — научной эквивалентности здесь не установлено.
Не ослаблять SolverTolerances для сокрытия таких отличий.

Для будущей реализации нужны existing deterministic/reference/nonfinite/
storage checks плюс winner/tie/raw-vs-normalized/near-zero witnesses;
это требования проверки новой дельты, здесь тесты не запускались.

**Цена/лимит вывода.** Только готовый
`native-bias1mV-warm128-max26/phase-partial-2-20-withalloc.json`:
residual3,33035wall/82,0076CPU≈24,62 core-equivalents, allocated367920944B,
GC0,01776s≈0,53% phase wall. Значит фаза уже параллельна; телеметрия не
локализует allocation и не доказывает, что предлагаемый witness scan
объясняет основной wall cost. Свежие кандидаты и шесть знаковых условий
реально стоят вычислений. По этим данным нельзя обещать speedup, объявить
остаток последовательным bottleneck или принять новую физическую модель.
