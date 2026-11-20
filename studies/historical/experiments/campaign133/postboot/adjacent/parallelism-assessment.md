# Native SCBA e171: где используются workers и что измерить дальше

**Решение: следующий долгий запуск пока не переводить сразу на12 workers.**
Код действительно распараллелен; текущий driver одновременно выполняет
существенную последовательную диагностическую работу на каждом map. Сначала
нужен один matched probe4/8 workers с готовой фазовой телеметрией. Ускорение,
его величина и фактическая доля bottleneck здесь **not_measured**.

Source: clean HEAD `e171caa60cce676c6c4238dd671e7c527f2bd977`, tree
`742ed5a6fe82f1e5c63fc1a2290ed77f89ca6da8`; symlink
`../core-accepted-science`. Ни Julia/Pkg/HDF5, ни profiler/attach к текущему
процессу не запускались. Прочитаны только source и малые TOML. Наблюдение
Root0.998CPU за3s и26CPU VM означает3.84% всей VM; даже полностью загруженный
CPUQuota400 процесс занимает максимум15.38% такой VM. Эта нормировка сама
по себе не доказывает ошибку threading; lifetime thread% не измеряет текущую фазу.

**Фазы по source.** Пути в таблице относительно `src/numerics/optimized/`.

| Фаза | Реальное расписание e171 / источник |
|---|---|
| Dyson/Keldysh | Независимые `(E,k)` blocks: `production_state.jl:14–48`; retarded small LU и private workspaces. Number terms параллельны, итоговая упорядоченная сумма последовательна (`production_operators.jl:1346–1373`). |
| Static/LO contractions | Energy chunks распределены по W, каждый worker имеет X/Y и вызывает BLAS1 `mul!`: `production_operators.jl:401–463`; LO shifts/contributions последовательно вызывают эти parallel contractions (`:1036–1091`). Механизмы all5 обходятся последовательно, не пять параллельных solver (`:1196–1262`). |
| Hilbert/PI | Параллельны flattened275 `(k,a,b)` columns, private FFT buffers и FFTW plans num_threads=1: `fft_parallel.jl:50–109,169–225,342–397`. В PI branch создание Γ/ΣR broadcast, doubled-padding subtraction и norms остаются отдельными single-task проходами (`production_operators.jl:1107–1123`; `fft_parallel.jl:392–397`). При direct_green static4 обходят Hilbert, он остаётся для LO (`production_operators.jl:1240–1257`). |
| finite_chain4 embedding | Независимые `(E,k)` и private Nb×Nb workspace; две стороны внутри worker последовательно, затем три global array sums: `production_operators.jl:330–397`. |
| Residuals/PSD/causality | Worker chunks/private eigensolve storage: `residuals.jl:539–750`; scalar arrays затем canonical serial sum (`:495–503,752–755`). Family/component residual calls последовательны (`production_iteration.jl:20–64`). |
| Assembly/linear mixing | Elementwise work через `_production_parallel_linear!`; фазы отмечены `production_solver.jl:560–574,840–881`. Текущий driver использует linear; Anderson не его bottleneck. При Anderson Gram dots в `production_mixing.jl:135–157` не распараллелены этим worker API. |
| Observables | `production_iteration.jl:89–135`: sortperm по энергии, boundary-current accumulation и population sum последовательны. |
| Physical markers | Последовательные full-array component norms, collision integrals, FDT/number/edge scans и bounded sampled eigenmodes: `physics_markers.jl:56–123,131–219,227–394`. |
| Callbacks/I/O | `history_observer` и `iteration_callback` вызываются синхронно (`production_solver.jl:746,761`); произвольная работа driver не получает Julia workers автоматически. |

Worker ceiling задаётся **одновременно** Julia default thread pool, requested
worker_count и jobs (`production_cache.jl:63–79`). Значение worker_count8
при J4 останется≤4. Backend `:blas` принудительно даёт один outer worker
для тяжёлых блоков; текущий `:threads` выбран верно. Для использования8/12 CPU
нужны J8/J12 и соответствующая OS quota; CPUQuota400 не даёт суммарно больше4CPU.

**Именно текущий driver добавляет serial work каждый map.**
`../native-bias1mV-fine48001/run_native.jl` SHA
`75a63edf3e87784862dbeaaef4bf7b77332f52d43acb9f18dc00564d1604eacb`:
lines26–29 задают worker4/hilbert_columns1 и marker cadence1. Это включает
5×2 mixed/fresh collision passes и27 full-field component norm passes
(5channels+embedding±/sum+total, по3components), плюс FDT/quantile/edge work.
Lines109,121–134 запрашивают aligned callback **каждый map**; callback снова
считает два full `(E,k,a,b)` collision passes для embedding± и пишет balance
TOML. Observer113–117 пишет CSV/markers/witness с flush. Это конкретный
кандидат serial cost, а не уже измеренное объяснение всего времени.
`checkpoint_every_scba=0` не отключает explicit checkpoint_request=true.

**hilbert_columns1 не означает один FFT worker.** Это ширина batch на каждый
worker; все W получают непересекающиеся column ranges. Здесь L=131072,
275columns; W4/8/12 получают примерно69/35/23columns. Chunk1 делает отдельные
FFTs по колонкам, уменьшая buffer и потенциально увеличивая call overhead.
Замена на32 меняет throughput/workspace, но не дискретный PI оператор; её
не следует смешивать с первым worker A/B. При W8 chunk32 только FFT workspace
primary+verification≈1542MiB вместо54MiB при chunk1 — это уже существенный
новый memory admission. PI выполняет double-padding witness по своему пути;
нельзя обещать устранить его работу одним verify_fft_roundoff=false.

**8/12 workers: растёт scratch, а не копия всего физического состояния.**
Для NE48001/Nk11/Nb5 один complex field=211204400bytes. При energy_chunk64,
hilbert_columns1, linear mixing из формул `production_cache.jl:479–568`
дополнительный worker требует около6.553MiB: FFT6MiB, X/Y0.537MiB и малые
Dyson/cavity/residual workspaces. Это статическая dimensional estimate
(BlasInt8), без FFTW opaque metadata, stacks/JIT/GC и пользовательских копий.

| W | Δ peak к W4 | Формула peak bytes | Запас до native budget20543700992bytes |
|---|---:|---:|---:|
| 4 | 0 | 20224379456 | 304.53MiB |
| 8 | +26.21MiB | 20251865376 | 278.32MiB |
| 12 | +52.43MiB | 20279351296 | 252.10MiB |

База peak взята из `../native-bias1mV-fine48001/attempt01/case0/identity.toml`,
не из измеренного RSS. OS cap22011707392bytes дополнительно оставляет driver
reserve1468006400bytes; это не разрешение держать дополнительные полные
solutions. Public `estimate_production_memory(problem; options=po,
worker_capacity=8/12)` использует реальные enabled kernels/energy nodes
(`production_cache.jl:671–697`); его следует повторить для frozen warm input
и фактического retention до admission. Статический delta не является гарантией
безопасного RSS на новой VM. Смена8→12 не требует автоматически больше29GB,
но и свободная host RAM сама по себе не даёт ускорения memory-bound фаз.

**Готовый API измерения, без Core edit.** `ProductionOptions.phase_timing`
и `event_sink` публичны (`production_contracts.jl:88–108`, API public docs).
`with_production_options` сохраняет остальные поля (`:117–153`):

```julia
sink = event -> begin
    if event.action in (:phase_begin, :phase_end)
        # Buffer only event.stage/label/iteration/status and scalar metrics.
        push!(phase_rows, event)
    end
    false
end
po = QCLNEGF.QCLNumerics.with_production_options(po;
    worker_count=W, phase_timing=true, event_sink=sink)
```

В `production_telemetry.jl:119–273` доступны duration_seconds, cpu_seconds,
allocated_bytes, gc_seconds/count, task_width, process-scope counters.
CPU/wall по фазе показывает среднее занятых CPU, не thread attribution;
вложенные этапы не суммировать дважды. `event_sink` синхронный: buffer small
scalars и одна запись после solve, без flush/матриц на каждое событие.
`phase_request` — resource-width callback, а не profiler: для чистого A/B
оставить nothing. Отдельно обернуть timing вокруг external observer и
iteration_callback: непосредственный solve_scba callback в core не обрамлён
отдельным checkpoint_publish, в отличие от top-level solve wrapper
(`production_solver.jl:996–1036`).

**Один различающий опыт перед128 maps:** после текущего sole heavy process,
последовательно два новых bounded процесса с одним и тем же frozen checkpoint
и exact physics/Core/input, одинаковой marker cadence1 и callbacks: A=J4/W4/
CPU400, B=J8/W8/CPU800, BLAS1/OMP1, hilbert_columns1, memory22GB/swap0.
Каждый ровно4ordinary maps; первый отдельно считать JIT/resume, средние2/3 —
steady сравнение, последний terminal не смешивать с ordinary mixing timing.
Cap≤600s на процесс, суммарно≤8maps/1200s, small output≤32MiB на вариант;
исходный checkpoint остаётся неизменным. Сохранить phase events, callback
wall/CPU, cgroup usage/throttling и maxRSS, raw gate/scalar history, выбранные
малые witness blocks и потоковые logical digests финальных S/G массивов
(без второго full-state output; digest cost отдельно от solver time).
Для equivalent path предпочесть exact digest match; несовпадение не скрывать
новой tolerance. Выбирать8 только при меньшем measured steady wall без потери
identity/guards и без memory/throttle проблемы. Если markers/callbacks или
PI serial проходы доминируют, сначала оптимизировать именно их: immutable
block partials + canonical final reductions/reuse measured traces, отдельным
Core change и equivalence review. Снижение scientific marker cadence ради
speedup — отдельное изменение наблюдения; оно не входит в этот A/B.
