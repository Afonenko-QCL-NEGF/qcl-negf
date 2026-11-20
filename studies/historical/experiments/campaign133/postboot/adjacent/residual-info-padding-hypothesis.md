# lapack_info padding: допустимый изолированный опыт, не диагноз

**Стоит проверить: length1→8 научно нейтрален для residual вычислений e171.**
False sharing, фактическое размещение buffers/cache lines и ускорение пока
**not_measured**. Этот вывод не объясняет82CPU/3.33wall сам по себе;1.85млн
малых eigensolves/map остаются физически предусмотренной работой.
Никаких Julia/Pkg/HDF5/profiler или изменений active Core не выполнялось.

На clean e171caa60cce676c6c4238dd671e7c527f2bd977 полный поиск usages даёт:

- `src/numerics/optimized/residuals.jl:39,78,100`: field —
  Vector{Vector{BlasInt}}, отдельный zeros(BlasInt,1) каждому logical worker.
- Lines248–271 проверяют число buffers и **nonempty**, не length==1.
- Lines321/352 и366/409: единственные Julia data reads/writes — info[1].
  zheev/zgesvd принимают Ptr{BlasInt} для scalar INFO (lines335/348 и387/405),
  длина info в LAPACK не передаётся. `lwork` берётся из другого work buffer,
  не из info. Увеличение vector сохраняет первый scalar и native ABI.
- Line571 выбирает ws.lapack_info[worker] внутри worker task; других
  consumers полного payload в Core source нет. Extra slots не участвуют
  в eigensolve, norms, PSD/backward budget, criteria, reductions или witness.
  Это не сокращение числа проверок и не изменение floating arithmetic.

**Самый чистый benchmark возможен вообще без Core edit.** На приватном
ProductionResidualWorkspace сохранить ссылки на первоначальные info vectors,
подготовить padded vectors и перед запуском заменить только элементы
`ws.lapack_info[w]`. Struct immutable, но его vector field mutable; остальные
H/values/work/rwork, scalar partial arrays и scientific input сохраняют те же
объекты/адреса. Function specialization Vector{BlasInt} также та же. Это лучше
изолирует info layout, чем две полные allocations всех workspaces подряд.

Причина гипотезы: info[1] пишется Julia и LAPACK при каждом eigensolve. Worker
ownership исключает data race, но не исключает соседство разных info[1] на
одной cache line. **Source не задаёт allocator layout/alignment/line size.**
Нельзя вывести такое соседство из того, что objects маленькие. Length8 даёт
64payload bytes лишь при sizeof(BlasInt)==8; на32-bit integer ABI это32bytes.
Это также не гарантирует64-byte alignment и ничего не доказывает о прочих
buffers или внутренней BLAS/LAPACK contention.

После завершения sole active run: один отдельный warmed A/B/A layout probe
на4 и26 workers, BLAS1/OMP1, одинаковый frozen residual input. Сначала
записать sizeof(BlasInt), фактический hardware coherency line size и
pointer(info[w])/line grouping **для baseline и padded**, затем callbacks,
phase wall/CPU/alloc/GC и raw repeated samples (не только minimum). Проверить
padding tail sentinels после native calls. Сравнить все residual outputs и
полный worst-witness payload/coordinates/first-tie policy; NaN/Inf/failure
paths включить в маленькую отдельную qualification. Никаких новых SCBA maps.
Root отдельно назначает cap и repetition budget; этот документ опыта не запускает.

Если baseline first scalars уже на разных lines, именно эта false-sharing
гипотеза не подтверждается размещением. Если padded case не даёт устойчивого
выигрыша, не делать production change ради padding. Положительный timing
без адресов/повторов не отличает locality от прогрева/частоты/шумов. Даже
отрицательный результат не исключает другую LAPACK concurrency overhead.

Поздний constructor patch потребовал бы отдельно согласовать видимую длину
internal workspace field и обновить memory estimator
`production_cache.jl:497–504`: +7*sizeof(BlasInt) на worker (1456raw bytes
при26workers/BlasInt8, без изменения числа arrays/headers). Сейчас достаточно
изолированного workspace-layout probe; production source остаётся неизменным.
