# Measured residual cost: уточнение приоритета для Core issue32

**Сейчас нужен узкий разбор residual kernel, а не blanket production refactor.**
На новом J26 запуске residuals уже занимают24.62CPU в среднем: добавление
workers к этой фазе не объяснит её нынешнюю стоимость. Старый
`parallelism-assessment.md` SHAaeb15d4a… сохранён без изменений; его вывод
о serial marker/callback work относился к другому driver с cadence1.

Новый frame: `native-bias1mV-warm128-max26/run_native.jl`
SHA3d83a82205e8dd203f5b89a7ae689821d914d0a07ec5791f0f711e0c78c11935,
**NE24001**, Nk11/Nb5/J26, markers cadence8. Это не fine48001 benchmark.
Core clean e171caa60cce676c6c4238dd671e7c527f2bd977 неизменен.
Прочитаны source, малые JSON и scalar event log; Julia/Pkg/HDF5/profiler и
изменения active kernel отсутствуют.

19 complete iterations2..20, `phase-partial-2-20-withalloc.json`
SHAc1d4f0a9… и независимо разобранные `phase_end` records:

| Фаза | Wall/map,s | CPU/map,s | Allocations/map | GC/map,s |
|---|---:|---:|---:|---:|
| residuals | 3.330353 | 82.007600 | 367920944B | 0.017757 |
| Dyson | 0.471204 | 7.221413 | 2545395392B | 0.089242 |
| scattering | 0.726802 | 9.243188 | 2161340120B | 0.028635 |
| embedding | 0.725595 | 5.872912 | 1423704176B | 0.048836 |
| markers, averaged incl skipped | 0.378441 | 0.395309 | 513259995B | 0.045450 |

Residuals —56.29% суммы записанных phase wall5.916467s/map; это не процент
полного process time с callback/I/O/JIT. Их allocated_bytes одинаковы во всех
19 maps, ≈350.88MiB/map, но это cumulative allocation, **не live RSS**.
GC составляет лишь0.53% residual wall; GC pause не объясняет3.33s. Allocation
и CPU overhead создания объектов всё ещё возможны вне GC. Counters process-
inclusive; текущий single-solver режим облегчает интерпретацию, но это не
sampling attribution к конкретной строке. Immutable19-line residual excerpt
SHAcb4185a5… и `residual-cost-audit.json` SHA fefdf15c… сохранены рядом.

**Что именно проверяется в этих3.33s.** В e171
`src/numerics/optimized/production_iteration.jl:20–64` фаза включает сразу:

- `production_residual_suite` (`residuals.jl:539–771`): rD/rA/rK, PSD и
  causality. На finite штатном пути на каждый из264011 `(E,k)` blocks идут
  **шесть PSD zheev + один causality zheev**:1584066 PSD calls и264011
  causality calls, всего1848077 eigensolves5×5/map. Дополнительный SVD
  причинности нужен только при positive numerator/overflow; causal-zero
  shortcut уже реализован (`:474–490`). Девять small matrix products/block
  проверяют Dyson/spectral/fresh Keldysh/raw products (`:589–729`).
- `production_selfenergy_residual` для8 families: embedding sum/plus/minus и
  all5 scattering. Это24 component scans и48 canonical scalar reductions
  (`production_iteration.jl:34–64`; `residuals.jl:826–864`). Это не24 PSD scans.
- Малые LAPACK matrices/values/work уже private и reused. `zheev` и `zgesvd`
  wrappers используют supplied storage (`residuals.jl:311–411`). Надпись
  allocation-free у них не означает allocation-free всей внешней фазы.

Шесть PSD matrices — A,−iG<,iG>,Γ и два **raw** Dyson/Keldysh products
до occupation redistribution. Их нельзя объявить лишними только потому, что
после redistribution G</G> выглядят допустимыми: защита специально запрещает
normalization скрывать raw defect (`residuals.jl:704–729`). Проверка fresh
candidate Keldysh также не дублирует проверку текущего mixed state. Cost
scientifically required eigensolves пока не отделён от overhead: внутри
residual phase ещё нет measured subphase/attribution.

**Одна рекомендуемая нейтральная оптимизация: lazy PSD-witness materialization.**
Сейчас `_production_negative_part!` после каждого eigensolve вызывает
`_positivity_witness` и создаёт полное12-field summary **до** сравнения с
текущим worst chunk witness (`residuals.jl:435–452`;
`reference/positivity_diagnostics.jl:70–101`). В полном конечном проходе это
1584066 summary evaluations/map, хотя наружу нужны только winners1032 chunks
(default residual_chunk256) и один global winner. Более прямой источник
лишней работы: **Hermitian-defect scan25entries выполняется до winner check**
(`residuals.jl:437–449`), а это поле не входит в ratio/budget
(`positivity_diagnostics.jl:83–99`). Не-победившие diagnostics не используются.
Источник подтверждает эту eager diagnostic work;
**сколько именно из367.9MB выделено здесь, ещё не измерено** — compiler может
устранять часть временных объектов. Это конкретная проверяемая гипотеза,
не утверждение «всё время уходит на boxing».

Production-only helper может вернуть isbits scalar statistics, вычисленные
в том же порядке (λmin, norm, defect, budget, ratio). Только если
`ratio > old_chunk.ratio`, выполнить прежний ordered Hermitian-defect scan
и создать полный `_PositivityWitness`. Сохранить
strict `>`/first-tie policy, nonfinite failure path, все6 PSD+causality
eigensolves, floor/backward-error version3 и полный witness победителя.
Reference implementation и внешние API не менять. Это использует обычные
Julia immutable scalar return/function barriers; новые packages/framework
и другие physical criteria не нужны.

**Один bounded qualification после текущего run:** в изолированном candidate
checkout, сначала warmed allocation microcheck baseline/candidate для этого
helper, затем differential residual check на одном frozen input. Отдельно
измерить suite и family-residual portion; no new SCBA Φ, μ-fit или regrid.
Сравнить все residual scalars и **все поля/координаты witness**, включая
первое tie, tiny negatives внутри/вне backward budget, nonfinite inputs,
raw-only defect и повторное workspace reuse. Existing independent tests
`test/numerics/psd_witness_identifies_full_grid_matrix_and_absolute_scale.jl`
и `psd_backward_error.jl` защищают именно этот контракт; добавить tie case.
Если compiler уже убирает allocations или warmed time не улучшается,
не переносить прототип в production. Никаких обещанных процентов speedup,
снижения PSD cadence или удаления eigensolves из данного предложения.

Это уточнение относится к [Core issue32](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/issues/32).
Фактическая рекомендация — сначала доказать стоимость и эквивалентность
одного witness path; measured CPU-heavy residuals сами по себе не являются
доказательством неудачной архитектуры всего production solver.
