# Independent result: native warm128 max26, 0/1mV per period

**Выполнение и provenance подтверждены; обе ветви остаются UNRESOLVED.** Summary `../native-bias1mV-warm128-max26/attempt01/summary.toml` SHA256 `adae7807439307a7ff42af8c7fc92c667713b796006835204c795e95f6fd4fdb`: по128completed fresh native map evaluations при0/1mV/PERIOD, exit0, обе status=max_iterations, quality=unresolved, converged=false, scientific_acceptance=false. First map повторяет parent32boundary: максимум127новых post-parent Green states/case, nominal terminal159, не160. Это не принятые стационарные токи и не I–V.

Frozen driver `3d83a82205e8dd203f5b89a7ae689821d914d0a07ec5791f0f711e0c78c11935`, loader `fecbab99e7cee48fefd6c59865db180aa3e346dbdf14782ebd90ba14b1802719`, actual input `c62fde3d99f3963d54e36bc6b8caeb9c056320983246e6add15383e749261919`. Same-voltage private unmodified28fields из cold32, consume_initial=true/resume_iterations=false/emptyhistory, безFD/interpolation/repair. Научный вариант прежний: all5/no correlation e–e, fixedU0/noPoisson, real-energy fullR/L/G/N24001[−0.3,0.9]eV/50μeV, direct-static C/LO PIFFT/finite-chain4/70K/αΣ0.2. Julia1.13.4/J26/worker26/BLAS1 — исполнение, не новая физика и не Mats/M3 functional.

## Независимый малый audit

`native-bias1mV-warm128-max26-result-audit.py/.json`: Python stdlib AS≤128MiB, все256CSV rows, summaries/identities/sourcecopies/Manifest,34marker+balance TOML, оба boundary/warm-initialization reports и4.4MiB phase log. Новых Julia/Pkg/maps, декодирования HDF5 или чтения больших state.h5 **нет**. Full-array bitwise replay ниже — свидетельство исполнившегося pinned source; reviewer независимо проверил его provenance, zeros/flags и raw scalar equality, не повторял array comparison.

Проверены ν1..128 обеих histories, summarycounts/lastrows/source+loader SHA иactualinput; parent_completed32/parent_convergedfalse/reset/consume flags. Обе saved boundary reports показывают GR/GL/GG/A bitwise equality и нулевые weighted/unweighted differences при freshrow1; все13 raw scalar fields точно совпали с parent lastrow и текущей первой CSV-строкой. Это подтверждает перенос и первый replay приJ4→J26, а не сходимость parent.

Все256 rows воспроизводят λ=rawN/target, rλ=|λ−1| и pairedN=target. Markers/balances присутствуют **ровно** на1,8,…,128:17/case. Для каждого marker independently replayed rΣ=max raw per-channel/component norms, отличие≤5.8e−13; подтверждены ΔE/LO734/field0или20steps, particle sums и power ratios. Все256 event progress имеют fixed_point_passed=false/convergence_streak0. Минимальный joint max(rK,rΣ,rλ) за128calls:0.0815687/0.0251792; final значения выше, поэтому даже монотонное приближение к решению не установлено.

| Финальная raw метрика |0mV/period|1mV/period|
|---|---:|---:|
| rK |0.02395989924|0.01212425826|
| rΣ |0.1229881809|0.05077529349|
| rλ |0.002910427958|0.001174955690|
| Raw number |0.04486903074|0.04505287301|
| Paired number |0.04500000000|0.04500000000|
| Particle relative diagnostic |0.00778621|0.000617914|
| Power relative diagnostic |1.0|0.0995799|
| J, A/cm², **UNCONVERGED** |115.4960341|17.3171379|

Малые rD/rA и reported cone/causality defects около roundoff не заменяют raw fixed-point/charge gates. Pairedtarget — действие встроенного iteration constraint. Ненулевой0V current, finite-bias current и их разность не пригодны для conductance, отрицательной проводимости, power prediction или сравнения с экспериментом. Приведённые collision/power ratios — диагностика на сохранённом несошедшемся Green, не самостоятельная приёмка conservation. Равновесная FDR под1mV неприменима.

## Фактические ресурсы и phase scope

Root execution:1587.40s/process,1587.11s/script, case830.90/749.07s, данные6847873652B≤8GiBpair. cgroup peak17083142144B=15.91GiB приhard21.5/high21GiB/swap0; memory.high/max/oom/oomkill events0. cgroupCPU28325.98s: среднее17.8443CPU cores,68.63% квоты26; это не процентbusy time отдельного потока и не доказательство ускорения26×. Admission был записан до запуска; per-run/output/cutoff budgets соблюдены.

Phase log проверен regex-парсером безeval: только2SCBAcasebegins/max128 и256progress rows, безtiny-contamination; все phasebegin/end согласованы, statuscompleted, counter_scope=process. Суммарные неперекрывающиеся phasewall1492.018s≤wholeprocess1587.397s; phaseCPU28218.023s≤cgroupCPU28325.981s. Residuals:857.350s wall/21217.593s processCPU (54.0% wholewall,74.9% wholeCPU); candidate scattering182.938s, embedding169.044s, Dyson124.742s, marker phase85.570s. Marker wrapper имеет256events, фактически measured payload34; эти величины нельзя путать. Это измеренная стоимость данной траектории, не отдельный benchmark или доказательство эквивалентности будущей оптимизации. Phase log внеpair data counter учтён отдельно по scope; root разделилtiny/actuallogs.

## Provenance и предел

Declared final stateSHA:0V `e4fc9b91fe33e65d71a3475898efc615a554efa88c3ccca9c63e819da448fcc6`;1mV `c66dbab35e2659b07ec7f783e8aff0020df880d1d3a4c7817bb537ecef112fce`. В этом bounded review они не rehashed; новые model/fullstate arrays не проверялись независимо. Loader runtime whole-source/model checks и raw-frame digests сохраняются в initialization reports; иное wholemodel HDF hash само по себе не означает смены физических матриц.

Подтверждён конечный **несошедшийся** full-nonequilibrium опыт на большей продолжительности. Не доказаны существование/единственность steady state, достаточность energy/window/basis/k/cavity discretization, causal real-axis accuracy, Poisson, finite-device physics или experimental validation. Отменённый fine48001 опыт не становится ни pass, ни научным отрицательным результатом этой coarse continuation. Продолжение/оптимизация требует новой отдельной identity и полномочий; этот report новых solver runs не разрешает.
