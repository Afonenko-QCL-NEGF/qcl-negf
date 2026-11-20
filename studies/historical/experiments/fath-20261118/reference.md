# Независимая проверка конвенций Fath, 18.11.2026

Аудит конвенций по [Core e171caa60](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/tree/e171caa60cce676c6c4238dd671e7c527f2bd977), [паспорту зон](bands/passport.toml), [транспортной модели](transport/device.toml) и драйверу кампании. Сам аудит не выполняет транспортного расчёта. Локаторы src/ ниже относятся к закреплённому публичному commit ядра.

**Главное:** множитель А/м² → А/см² равен **+10^-4**, он не меняет знак. `J+` — charge-magnitude-weighted *net outward electron flux* в правого соседа, а не автоматически conventional current вдоль +z и не ток определённого внешнего вывода. Отождествлять положительный `J+` с положительной ординатой статьи/tutorial без конвенции внешнего амперметра нельзя. Величина 514 для определения знака не использовалась.

## Геометрия, поле и нуль

[Первичная статья Fathololoumi, DOI 10.1364/OE.20.003866](https://doi.org/10.1364/OE.20.003866), [NRC PDF](https://publications-cnrc.canada.ca/eng/view/accepted/?id=98144fe2-7e95-448c-aa0e-06096537ad2d), §2/Fig.2: от injection barrier B/W=4.3/8.9/2.46/8.15/4.1/16.0 nm, xAl=0.15, Ns=3e10 cm^-2, средние 5 nm phonon well легированы. Карточки это воспроизводят; разбиение последней ямы 5.5/5/5.5 nm не создаёт новых материальных интерфейсов. Lp=43.91 nm, doped interval [33.41,38.41] nm. Статья использует 12.2 kV/cm как design-field magnitude; знак относительно внешних выводов таким числом не задан.

[Официальный historical tutorial rev1521541051](https://nextnano-docu.northeurope.cloudapp.azure.com/dokuwiki/doku.php?id=qcl:tutorials:thz_qcl_-_fathololoumi_2012&rev=1521541051): порядок B/W=4.1/16/4.3/8.9/2.46/8.15 nm; +54 mV/period названо **−12.3 kV/cm**. Это **циклический сдвиг**, а не обращение. В campaign 16-nm яма начинается **27.91 nm**, её центр **35.91 nm**. В tutorial она начинается **4.1 nm**, то есть `z_tutorial=(z_campaign−23.81 nm) mod Lp`; тогда весь период campaign [B4.3,W8.9,B2.46,W8.15,B4.1,W16] становится [B4.1,W16,B4.3,W8.9,B2.46,W8.15]. Doped [33.41,38.41] → **[9.60,14.60] nm**, центр12.10 nm. Итак, **обе геометрии совпадают по циклическому переносу 23.81 nm**, tutorial 12.05 — арифметическая опечатка; напечатанный interval правильный. Циклический перенос с переносом легирования не способен сам превратить направленный период в обратный. Полное обращение потребовало бы обратного порядка слоёв и согласованной смены оси/поля. Кристаллографическая ориентация внешних контактов в карточках не задана.

Код `src/numerics/reference/basis.jl:304,327,380`:

`H = H0 − Fbar (Zbar−z0bar I) + UH + Cbar*kbar²*M_inverse`.

Значит physical electron potential energy `Ue(z)=Ec(z)−e*Fbias*(z−z0)+UH(z)`; так как заряд электрона −e, `phi(z)=Fbias*(z−z0)` и **E_z=−Fbias**. `Fbias=+54mV/Lp` в driver/passport — положительный модуль. Он согласован со знаком tutorial. При переносе начала координат нужен общий сдвиг энергий: в той же бесконечной ячейке смена z0 меняет постоянную, а не силу. `E_ref=0` — произвольный gauge, well Ec=0 до наклона/Poisson; это не измеренный уровень Ферми. [src/numerics/reference/grids.jl:22–23](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/e171caa60cce676c6c4238dd671e7c527f2bd977/src/numerics/reference/grids.jl#L22) и [src/physics/observables.jl:94–95](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/e171caa60cce676c6c4238dd671e7c527f2bd977/src/physics/observables.jl#L94): solver Ebar=(E−Eref)/E0, вывод E=E0*Ebar+Eref. Для сравнения состояний следует выравнивать один и тот же материальный интерфейс и gauge, а не абсолютную высоту картинки.

**Hand check:** 54mV/43.91nm=0.001229788 V/nm=12.29788 kV/cm; за +Lp электронная энергия меняется на **−54 meV**. Ns=3e10 cm^-2=3e14 m^-2; объёмная плотность в 5nm сегменте=6e16 cm^-3. Эти знаки/множители следуют из единиц, без transport результата.

## Что именно означает J и его momentum sum

[src/numerics/reference/basis.jl:132–135](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/e171caa60cce676c6c4238dd671e7c527f2bd977/src/numerics/reference/basis.jl#L132) определяет T+=H[central,right]; [src/numerics/reference/periodicity.jl:225–240](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/e171caa60cce676c6c4238dd671e7c527f2bd977/src/numerics/reference/periodicity.jl#L225) возвращает plus=right embedding, minus=left embedding. Production finite-chain путь сохраняет эту ориентацию; field remap в [src/numerics/optimized/production_operators.jl:158–169](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/e171caa60cce676c6c4238dd671e7c527f2bd977/src/numerics/optimized/production_operators.jl#L158) использует argument E+r*eVp для соседа +r, что соответствует onsite H_r=H_0−r*eVp.

`src/numerics/optimized/production_iteration.jl:76–103,118–126`:

`Jplus_bar = gs/(2π) Σ_e,m wE[e] wk[m] Re Tr(Σplus^> G^< − Σplus^< G^>)`,

`Jplus_SI = J0*Jplus_bar`, `J0=e*E0/(hbar*L0²)>0` ([src/domain/scaling.jl:22](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/e171caa60cce676c6c4238dd671e7c527f2bd977/src/domain/scaling.jl#L22)). E0 и hbar должны быть в согласованных единицах eV и eV*s либо J и J*s, **не добавлять второй e** при использовании eV/eV*s. Если hbar берётся в J*s, E0_eV требует перевода E0_J=e*E0_eV.

Простая независимая проверка знака на одном уровне: Σ^<=iΓ fα, Σ^>=−iΓ(1−fα), G^<=iA f, G^>=−iA(1−f). Тогда скобка=ΓA(f−fα). При f>fα электроны уходят из ячейки к данному резервуару и J_out положителен. Поэтому J+>0 значит электроны выходят вправо; conventional current_z=**−J+**, если +z направлен вправо. Для левого резервуара positive outward означает движение электронов в −z. При стационарном particle balance J++J−≈0; это не равенство двум положительным токам.

Включённый [драйвер, terminal_observables](equilibrium/attempt01/transport-run.jl#L225) умножает обе границы на J0 и делит на **1e4**. Его [write_row](equilibrium/attempt01/transport-run.jl#L263) сохраняет raw `SCBAIteration.J` в **A/m²** без преобразования; печать progress делит на **1e4**. Публичные агрегаты с суффиксом `A_cm2` уже содержат это преобразование. Следовательно нельзя второй раз делить уже названный `J_plus_out_A_cm2`. Название `terminal_current_plus` в summary — локальная граница embedding, не физически смоделированный металлический контакт.

k-resolved summand: `Jplus_m[A/cm²]=1e-4*J0*gs/(2π)*wk[m]*Σ_e wE[e] ReTr(...)`; сумма по m возвращает Jplus. `wk=(κ_right²−κ_left²)/(4π)` ([src/numerics/reference/grids.jl:39](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/e171caa60cce676c6c4238dd671e7c527f2bd977/src/numerics/reference/grids.jl#L39)) уже содержит radial measure k dk/(2π). Повторно умножать на k,2π или degeneracy нельзя. Отдельный summand может менять знак; не брать abs до суммирования. Для `energy_resolved_current` ([src/physics/observables.jl:239–253](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/blob/e171caa60cce676c6c4238dd671e7c527f2bd977/src/physics/observables.jl#L239)) единицы A/m²/eV: дополнительный множитель **1/E0_eV**, и последующее интегрирование физическими dE_eV, в отличие от суммирования безразмерными wE. Отдельный momentum-split файл не требовался и не создавался.

## Различия физики, которые нельзя назвать конвенциями

| Утверждение | Свидетельство | Ограничение / решение |
|---|---|---|
| Активное и клеммное V различаются | Fath §3–4 обсуждает Schottky drop≈0.8V для Au–Au с n+; tutorial задаёт Vperiod | 54mV — падение активного периода, не клеммные 54mV; контактную поправку не переносить на Cu–Cu автоматически. Сохранить. |
| CBO149 выбран осознанно | Tutorial p.3: input120meV, figures149meV; обе карточки transport149 | Не утверждать точное восстановление tutorial input или первичного авторского material database. Сохранить identity reconstruction. |
| IFR отличается | Tutorial p.9: exponential Δ0.1nm,Λ8nm; device: Gaussian; e171 kernels.jl:194–220 S(q)=πΔ²Λ² exp(−q²Λ²/4) | Даже одинаковые0.1/8 не одна корреляционная функция. Изменять модель без решения нельзя. Первичный MC использовал0.12/10nm, тоже иной набор. Сохранить как явно иной benchmark. |
| e–e выключено | [Драйвер модели](equilibrium/attempt01/transport-run.jl#L309): explicit ElectronElectronOptions(mode=:none), assert; CHANNELS только LO/acoustic/impurity/IFR/alloy; device none и bands off | Первичный MC содержит e–e (§4), значит его результаты не идентичная no-e–e модель. Это определяет физическую модель кампании. |
| По знаку J+ установлена полярность внешнего прибора | Формула определяет net electron outflux справа, но контакты/провода отсутствуют | Данных недостаточно. Можно сопоставлять engineering величину при явно принятой конвенции, не выводить полярность из близости к514. |

Численные сходимость и корректность fixed-point не проверялись этой запиской. Геометрическая проверка не доказывает точность finite-basis/current projection.
