# Independent static review: INFO-only benchmark

**GREEN для единственного bounded Root запуска**, без научной приёмки или
обещанного ускорения. Benchmark1c64732edd7f6d23312ccb2c842feee2cc565aa12b00490b2dfa392ac1edae9a,
false input6e1da0aa9253ed7890c8044e31da5582cc129fb129edf7ee79690122f373fcb4.
Reviewer проверил эти SHA, helper SHA и small parent source hashes;
Julia/HDF numeric/new maps не запускал, Core/исходники не менял.

**INFO contract:** Core e171 `optimized/residuals.jl:270,321–352,366–409`:
буфер требуется непустой; код/ccall используют только info[1] как scalar
LAPACK INFO, а не length1-dependent workspace. Vector{BlasInt}(8) с тем же
типом и rooted lifetime совместим. Baseline и padded26 vectors разные,
каждый worker владеет своим; swaps меняют только entries ws.lapack_info.
Положительные части buffers не alias исходных matrices/других workspaces.
Сентинелы[2:8] контролируют лишнюю запись; hardware line/BlasInt size и
actual addresses позволяют проверить расположение, не предполагая, что
length8 на любой ABI обязательно даёт отдельную cache line.

**Входы/контроль:** source state e4fc9b91… и model3de1f7fc… связаны с
complete128maps case0, U0, энергиями/units/schema и parent summary/identity.
Прочитанные типы/axes корректны для GreenState и SelfEnergyFamily constructors.
Whole-file SHA проверяются до HDF; сравнение input fingerprints перед/после
включает все28 retained fields и новый total3fields, energy/h/condition/scale.
GP.array_digest использует SHA над reinterpret(vec), без полного array copy.
Total — намеренный **sum8 surrogate**, который дважды учитывает embedding;
candidate===total, нового Φ нет. Поэтому output rD/rA/rK/PSD/causality —
значения residual kernel на этом surrogate, не новый native residual или
SCBA/convergence доказательство. rΣ family passes/λ/full-phase работы сюда
не входят. Равенство A/B даже при плохом physical residual — не physics pass;
actual rows должны оставаться видимы при дальнейшей интерпретации.

**Сравнение:** одна workspace26/chunk64, same inputs/other buffer addresses;
исключённые A26/A4 warmups, затем A/B/A×2 на W4 и W26:12 timed/14 total.
Все5 metrics и12 actual witness fields сравниваются через isequal с первой
warmup, включая coordinates/kind/tie result. Другие matrix/LAPACK/scalar
buffer addresses и INFO addresses/lengths должны оставаться прежними;
nonmoving layout не принимается лишь на веру в allocator. Concurrent
residual calls отсутствуют; workspace всегда используется последовательно.
Некоторые unused INFO[1] остаются от предыдущего call, но каждая использующая
их LAPACK функция сама обнуляет info[1]; sentinel-tail проверяется у всех26.

**Цена/остановка:**28 source complex fields≈2,957GB +3total≈0,317GB;
read_complex transient около0,211GB на field, явная GC после каждого чтения.
Непредусмотренной копии всех полей в fingerprints/array lists не найдено;
actual RSS/JIT/GC ещё не измерены, поэтому OS6GiB cap остаётся решающим.
Soft admission180s включает warmups/metadata и прекращает новые kernels;
при недопуске следующего case output=`stopped`, не completed subset.
External300s/Swap0/CPU2600/J26/explicitBLAS1/OMP1/file+output32MiB обязательны;
внутренний guard не прерывает уже допущенный kernel. Setter/getter и
Core/env/resource/counter API signatures проверены по исходникам.

При exact output mismatch/tail/address mutation, budget failure или partial
repetitions сравнение не квалифицировано. Стабильный A/B/A эффект может
поддержать INFO-layout hypothesis, но сам по себе не доказывает false sharing
и не переносится на full raw measurement или другой Core/режим. Blockers
в замороженном ограниченном протоколе не найдены; новые features не предлагаются.
