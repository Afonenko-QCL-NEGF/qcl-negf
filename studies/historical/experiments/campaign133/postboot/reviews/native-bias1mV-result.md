# Независимый результат native matched0/1mV, N24001

**Выполнение подтверждено; обе ветви не сошлись.** `native-bias1mV-postreboot/attempt01/summary.toml` SHA256 `76bba8e87123f04a0298087b20a979e3ff23f3c1d921ea5eae91cf38a121d59b`: exit0, по32 completed SCBA iterations на0 и1mV/period; обе status=max_iterations, quality=unresolved, converged=false/scientific_acceptance=false. Это завершённый finite-budget опыт, не time-stop и не физически принятый I–V.

Метод/source: новый real-energy full R/L/G fixed-U0/noPoisson all5/no correlation e–e вариант N24001[−0.3,0.9]eV, direct-static C+LO PIFFT/finite-chain4,70K/J4/BLAS1. Driver `1a25007ef353aabb7ee41de1474bf9043be45f0302eea6609943de42c6068726`; actual matched input `34d184c9543a5cdd097efba89dc64dffbf265835dedb2029c55516ef891767d0`. Cold FD только initialization; native paired number constraint далее сохраняется вместе с rawλ gate. Это не прежний30704/30721 Hilbert baseline и не Mats/M3 functional.

Независимый audit `native-bias1mV-result-audit.py/.json`: Python stdlib AS≤128MiB,64CSV rows,64marker/balance TOML, summaries/identities/sourcecopies/Manifest hashes, byteSHA двух **малых**7.5MiB model.h5. Никаких Julia/maps, декодирования HDF5 arrays или чтения больших state.h5. Полные stateSHA ниже остаются declared, а не независимо rehashed; алгебра full arrays не перепроверялась.

Проверены ν1..32, совпадение последних rows с обоими summary, inputvoltage иsourcehash, marker ΔE50μeV/LO734steps/field0или20steps; finite-bias FDR корректно not_applicable. Для всех64 rows независимо воспроизведены rΣ=max component/channel norms (расхождение≤9.3e−13), λ=rawN/target иrλ=|λ−1|, pairedN=target, signed particle balance и power ratio из saved scalar terms. Это replay первичных scalar witnesses, не новый независимый SCBA solve.

| Последний показатель |0mV/period|1mV/period|
|---|---:|---:|
| rK |0.5317105319|0.5031378394|
| rΣ |0.3160538648|0.2125673616|
| rλ |0.0392018494|0.0251051307|
| Raw number |0.04676408322|0.04612973088|
| Paired number |0.04500000000|0.04500000000|
| Particle relative diagnostic |0.0194334|0.0124857|
| Power relative diagnostic |0.601537|0.533661|
| J, A/cm², **UNCONVERGED** |−614.983858|2.959779|

Малые rD/rA≈roundoff и сохранённые rPSD/rcaus=0 не компенсируют большие raw Keldysh/selfenergy/charge defects. Равенство нормированной плотности target — действие iteration constraint. В частности, большой ненулевой0V current и изменяющийся1mV current не пригодны для conductance, gain, power prediction или утверждения об отрицательной проводимости. Нельзя относить raw defects только к недостаточной сетке: finite32steps и nonlinear transient также не разрешены.

ModelSHA независимо сверены: V0 `91c53995b6b3ff51387de23e97fe50676fa829066072545759f28a1c36cf9e21`, V1 `ecb2b0dc93f6b44543a19f8be55302a7130aebb79fe4ab7a04cf981751284a94`. Declared stateSHA: V0 `3caddc855578b8af691e105a1b871239bdd96e443a560472aa68e1408d46fae8`, V1 `0a9d838adeb6b93a8d953167e273f91fe5b263c8f85fcaeb6cfbb85c4f5adbe6`. Current Manifest matches both identities (`da0780fb…`). Сохранённые shapes/alignment обоснованы frozen source/tiny, не full-state array audit данного review.

Ресурсы Root actual-execution:535.51s/process,535.37s/script, data6840148013B, cgrouppeak12352028672B приhard12616466432B/high12348030976B/swap0; memory.high1539events, max/oom/oomkill0. Exact native estimate10118450072B; измеренный peak выше него на2233578600B≈2.08GiB. Доhard оставалось264437760B≈252MiB. Поэтому native guardPASS не является фактическим RSS upper bound: fine-план требует свежей resource/data admission с учётом **измеренной** разницы, а не одного reserve1400MiB. Причина overhead этим scalar audit не установлена. Никаких дополнительных запусков не разрешено данным report.

Пределы: grid/window/basis/k/finite-chain convergence, Poisson, causal retarded accuracy и experimental validation не приняты. Сравнение с future N48001 — только finite cold trajectories при одинаковых definitions; до сходимости/независимых проверок fine−coarse не errorbar.
