# Кампания #133: исходный baseline не сошёлся; проверен отдельный равновесный вариант

**Исходный real-energy SCBA baseline до сходимости не доведён.** Независимо подтверждены inner equations и charge/cutoff checks N512/N1024 **отдельного** all5 Matsubara/reference-tail+M3 finite-N варианта с заданным зарядом. Это численная опора на основе той же QCL-структуры и механизмов рассеяния, а не решение исходной дискретной задачи solver. Результат относится к U=V=0, finite45/hH-all9; он не принимает N→∞, Poisson, finite-bias transport, basis/k convergence или эксперимент.

Ручной старт неизменен: **15 ноября 2026, 16:33:33 UTC**. Плановый checkpoint — 16 ноября06:00UTC/09:00Минск; разрешённый резерв до09:10UTC/12:10Минск пока не активирован. Первый вычислительный этап закрыт03:38:47UTC. По последующему поручению подготовлен опыт1mV на период без e-e; **04:36:59UTC тяжёлые опыты отложены пользователем до перезагрузки**. Полноразмерные 0/1mV cases не запускались. Это промежуточный checkpoint, не завершение нового finite-bias поручения. Подготовка, агенты, вычисления, review, публикация и ожидание входят в одно окно от первоначального старта; автоматического нового 12-часового окна нет. Работа шла только на этой VM, без кластера/Proxmox. Heap hint не заменял hard cap; исходные массивы и неудачные попытки сохранены.

Фактическая VM: **20 logical CPU, 20.6GiB RAM**; ранее предложенные24CPU/25GiB относятся к плану. Native Julia1.13.3; initial dependencies FFTW1.10.0, Unitful1.28.0, HDF5 0.17.4 закреплены Manifest. Поздние Γ/fine/Jv опыты: один heavy Julia4/BLAS1, hard12.125GiB/high11.5GiB/Swap0, без параллельных Julia/Pkg. Исторические baseline сохраняют собственные resource identities. Человеческое участие: ручной старт и steering; активные минуты `not_measured`, не0.

[Итоговый независимый review](issue133-independent-review.md) одобрил научное содержание; окончательные ссылки и source graph сверены отдельно.

## Что именно исследовали

Исторический S01: V=0, фиксированное U=0, TL=TLO=70K, LO/acoustic/impurity/IFR/alloy, Nz96/Nb5/Pbasis3, Nk11, angular32/qz81, finite_chain4 с каждой стороны. Первые baseline использовали NE30721, E∈[−0.3,0.9]eV. Отдельный B0 NE4097 имел alloy OFF: его нельзя считать coarse S01. Fine-grid планы/LO tests уже были в истории; это не выполненные SCBA (`history-science.md`).

Новая equilibrium restriction использует один неизвестный **total local Γ**, все пять механизмов и Hilbert/PI retarded closure, при том же U0. Для commensurate LO выбран m939, NE30704, Emax=0.9000001064962726eV; отличие окна≈0.106496μeV имеет собственную identity. Эта задача отличается от исходного full-Σ baseline, не принимает его задним числом и не включает решение Poisson. Native unconstrained SCBA gates сохраняются как отдельный обязательный выход.

## Основные измеренные результаты

Локальные пути в таблице отсчитываются от `.build/campaign133/`; `reviews/` содержит независимые статические и result reviews. Значения residual безразмерны; weighted нормы используют wE·wk, если явно не оговорено иное.

| Опыт / отдельная identity | Измерено | Обоснованный вывод и ограничение |
|---|---|---|
| Итог: fixed-charge all5 Mats/M3, N512/N1024 | N512 error−2.30581e−11target; N1024−2.23776e−10; cross−2.00718e−10 | 112/≤144 maps; независимые equation/value audits PASS, finite-N numerical variant. |
| S01 unmodified warm64, Core f50 | rK=0.0535285, rΣ=0.151063, rλ=0.00787353 | Не сошёлся; `raw/S01-warm-unmodified64/summary.toml`. |
| Однократная FD initialization64, тот же source retarded state | rK=0.00200042, rΣ=0.00304599; rsum=0.00492212 | Initial-condition control улучшил конечные невязки, но rsum выше0.001. FD projection впоследствии не повторялась. |
| Продолжение FD64 ещё128 native maps | rK=8.23882e−5, rΣ=1.31884e−4, rλ=1.59154e−6 | `max_iterations`, не convergence; первая boundary строка повторяет source. |
| Frozen Γ: nodal-Hilbert → existing PI | rsum 0.00492212→0.000406478, ≈12.11× | При том же Γ и fresh cavity; изменение retarded operator, не SCBA solve (`reviews/pi-frozen-control-result.md`). |
| Stable covariance Γ-cont64 | raw final/best4.12558e−6; 64 entered Π, 62 completed | Два finite negative-q отказа и один precone reject сохранены; native0, reduced trigger1e−9×3 не достигнут. |
| Selected split-input Big oracle | 44 blocks: max relative Acov error6.83682e−15, GR3.45425e−15 | Intended hH/ΛH/Γ full45 model; independent exact PD/Big witness, не full-grid accuracy certificate. |
| Exact PD всего stored unprojected Γlast64 | **337744/337744** exact Hermitian и strictly PD | Gaussian-integer Bareiss/Sylvester, 20,264,640 exact divrem; сертификат сохранённых binary inputs, не решения. |
| Streaming spectral qualifier на том же Γ64 | Все GR/A/q/κ/scale и10 selected quantities — **bitwise equal** | Две R/A responses, Φ0/μ-fit0; `reviews/streaming-qualifier-result.md`. |
| Frozen Γ128 uniform2x:30704→61407 | ‖D‖w/‖PΦc‖w=0.0026539831; **99.99999105% weighted D² на новых midpoints** | Существенная collocation sensitivity одного frozen Γ; не доказательство будущей fine convergence. |
| Exact μ-attribution на том же fine A | Held-μ full defect0.00265398096; midpoint F/D=0.9999992366 | μ-shift объясняет old-node D, практически не объясняет dominant midpoint D. |
| PSD projection только AA trial,64 calls | raw final2.47801699e−6, ≈39.94% ниже matched control; native0 | Raw Φ не clipping; критерии прежние. Это улучшение траектории, **не convergence**. |
| Новый Matsubara all5, fixed-μ, N128/N256 | 32/32 maps; raw Σ−Φ **Float64 exact0 с i11 поi16**, обаN | Independent result review принят; конечная карта решена, плотность/cutoff ещё не квалифицированы. |
| Frozen Γ64 density-functional V4 | Mats M3 N1024 против real-grid: +9.33768e−5target | Fixed-source witness; N512→1024 изменение−4.4242e−8target — не rigorous tail bound. |
| Stable Γ64 → fine2x NE61407, AA history1 | raw0.00262528169→0.0003221790743; weighted0.00266090→0.0002872985082 | Все14 responses завершены:1coarse+12fine+1restriction; domain0/streak0/native0. Independent result review завершается. |
| Frozen Γ64 Jacobian/Jv | 5Φ+4Jv, Γ updates0; halving-ε consistency≈4× | Локальная derivative/Krylov диагностика; не full spectral radius или доказательство stall. Independent result review завершается. |

Frozen refinement/μ-control использует прежний HermΛ/raw-central-h Γ128; это **другой input**, чем unprojected stable-A Γ64 для PD/streaming qualifier и нового fine2x pilot. Первый refinement postprocessing завершился `Int64(1.2)` после двух законченных Π. Отдельный recovery исправил только диагностику, newΠ=0; failure не удалён. CSV покрывает лишь5.19% weighted D², не весь defect.

## Главный результат: finite-N fixed-charge M3

В `adjacent/matsubara-mu-root-refined/attempt02` выполнены6 outer N512 calls+1 independent N1024 witness, каждый отΣ0, α1×16:112maps. Все7 last-three raw residual maxima REL1.59634e−18/ABS1.58311e−19 прошли неизменные1e−9/1e−12×3; финальные N512/N1024 Σ/Φ binary identical. μ=0.08458841693811386native=8.458841693811387meV, без rescale плотности.

M3 numbers N512=.04499999999896239, N1024=.044999999989930074; relative target errors−2.30581e−11/−2.23776e−10, cross−2.00718e−10. НезависимаяρcrossFrob3.129419477e−12; final correctedρ Pauli min7.15117e−8/max.21749887177, Herm defect≤2.5e−17. Rawρ **безM3** имеет charge errors−4.6958e−7/−5.8919e−8target: существенна asymptotic tail closure, не нормировка результата.

Actual85.33sprocess/84.953sscript/952148KiB/Swap0, J1/BLASgetter1, data635703192B<1GiB. Refined ecf7 module отличается от1434 только именем/doc/допустимымиN, sourceCoree171 не менялся. Equation/value audits приняты: `reviews/matsubara-mu-root-refined-result.md` (53f0b1de…), `…-value.md` (ee0f9940…); summarySHA`e041cca82a7e…`. Metadata scientific/native/infinite flags **false** сохранены: принято именно новое finite-N fixed-charge numerical equilibrium, не rigorous infinite-N remainder/uniqueness или original baseline.

## Предшествующий fixed-μ N128/N256 результат

Вариант **direct-static-C/full-line-LO/reference-tail/finite45 central-repeat/hH-all9**, V0/70K/Nb5/Nk11, решает Σs=Ks[G] для complex Matsubara G. Те же пять raw kernels/qK/wk, но closure отличается от finite-energy HilbertPI; старые Γ/Φ не импортируются. Одна central-driven Σ повторяется в девяти ячейках, не девять independent cellwise SCBA. Фиксирована μ=8.459614262982019meV, без density fit. LO использует положительный bosonic kernel `2Ω/[β(ν²+Ω²)]`, packing `G(-n-1)=G(n)†`, exact bare45 pole reference и конечную convolution толькоΔG. Density:

\[
\rho_N=\rho_{ref}+\frac2\beta\sum_{n=0}^{N-1}\operatorname{Herm}\Delta G_n,\qquad
\mathcal N_N=g_s\sum_k w_k\operatorname{tr}\rho_{N,k}.
\]

Прежние32maps дали binaryΣ=Φ, raw0 i11..16 и30 independent successor replays; `iteration_budget` сохранён. Цена25.12s/888616KiB,17 slice-контракций≤1.44e−15. При CP kernels q≈0.305293 относится и к finite-N/reference map, но не является Float64 CP/forward-error certificate или infinite-cutoff bound.

Finalρ обоихN удовлетворяет measured Pauli0..1, но сохранён transient N128-i02 minρ=−3.19e−9: positivity всех iterations не заявляется, repair отсутствовал. Shared low32 Grelative1.52e−13/Srelative8.05e−11 не контролирует integrated tail. N128=.04500368792, N256=.04500486199; ΔN=1.17407e−6≈2.61e−5target. Cutoff/density constraint остаются unresolved. Первичные данные: `adjacent/matsubara-all5/attempt01`, summarySHA`b9397bf71b7e…`; scope принят в `reviews/matsubara-all5-result.md`.

Отдельный frozen-Γ V4 не решает новуюΣ: при certified Γ64 и fixedμ сопоставляет density functional с real-grid integral. Actual28.54s/917176KiB; небольшой N512→1024 witness относительно +9.33768e−5target discrepancy не доказывает continuum-tail/ghost/atom error bound (`reviews/gamma-density-hermitian-v4-result.md`).

Старый fixed-μ M3 V2 postprocess уменьшил N128→256 number-cutoff difference в128.0055×, до2.03823e−7target, всё ещё выше1e−8: **charge pass нет**. Actual16.56s/722136KiB, BLAS getter1. V1 timeout120s сохранил partialN128; setter был пропущен. Отдельная диагностика показала ENV1/getter128→explicit setter/getter1; actualV1 getter не записан, BLAS1 ему не приписывается (`adjacent/matsubara-moments/attempt02`, `reviews/matsubara-m3-result-audit.json`).

Endpoint certificate:44 positive Gershgorin lower gaps, minimum1.7752291; independent15checks. При declaredIEEE/exact-input premises ghost/target≤2.32360237e−30, exterior/endpoint atoms исключены **только для старой frozenΓ64 dyadic-hat/hH модели**. Это не новая Matsall5 closure, не tail/idealFFT/quadrature certificate (`reviews/endpoint-gap-certificate-result.md`).

## Почему изменили вычисление A

В слабых хвостах возможны raw-h anti-Hermitian contamination, потеря малогоΓ при Λ/R assembly, cavity/inverse roundoff и cancellation в Asub. Но diagonal q использует `−2ImGR` без финального вычитания больших величин: единственная причина не установлена. Qualified путь сохраняет раздельныеΓ/ΛH, exact native plan.hlocal во всех9cells и переносит источник через прежнюю cavity recursion:

\[
K_{phys}=\Gamma-i(\Sigma^<_{+,probe}+\Sigma^<_{-,probe}),\qquad
A_{cov}=G^R K_{phys}G^A,
\]

где probe local Σ<=iΓ, Σ>=0. Native retarded cavity при этом не меняет Schur-оператор; generic Float64 congruence не объявляется строго положительным Gram-фактором. Никаких скрытого η, clipping, floor или нормировки A нет. Тот же A должен питать q, μ, FD lesser/greater и все каналы Φ; positive q при другом A в Φ не определял бы единой карты.

Big192 full45 oracle поддерживает Acov для split hH/ΛH/Γ; LDL44 blocks/384bit repeat независимы от native recursion, но не изолируют единственную причину ошибки. Asub error6.57e10 relative относится к ||A||≈1.16e−28, absolute≈7.59e−18, не к большой density error. ALL Γ64 PD установлен отдельным full traversal; reviewer проверил proof и два Fraction witnesses, не второй full scan.

Высокоуровневый шаг в Julia выглядит так; это схема исследовательского map, не новый публичный solver API:

```julia
state = StreamingSpectral.stream_spectrum(GP, context, Γ)
μ = GP.fit_mu(ε, state.q, target, kBT).mu
Gfd, _ = GP.fd_green(state.GR, state.A, state.condition,
                     state.scale, ε, μ, kBT)
Φraw, _, _ = GP.phi(context, Gfd)       # все пять каналов, один A
raw_residual = Φraw - Γ              # критерий исходных уравнений
working = Herm(Φraw) - Γ             # отдельно: representation ledger
trial = propose_AAII(Γ, working)      # working history; raw Φ не clipping
# Domain checks, затем отдельный следующий map; raw Φ не исправляется.
```

Julia dispatch, concrete Context/function barriers, worker-owned Nb×Nb buffers и `mul!` позволяют менять представление без переноса физики в runner. Streaming helper118строк переиспользует owning `_cavity_side!` и central inverse, сохраняя `S+(plusR+minusR)` и `Γ−i*(plusL+minusL)`. Его spectral sweep держит4F, F=16NE·Nk·Nb²; qualifier честно удерживал old GR/A и поэтому6F, плюс cache/PI/model/scalars/JIT/RSS. Mixed process peak≈2.94GiB не является isolated stream bound/speed benchmark.

## Что установил контроль сетки и μ

Определено D=Φf(PΓc,μf)−PΦc(Γc,μc), где P — interpolation на **действительных координатах**. Static Γ_s=K_s[A] не зависит от μ. Поэтому два native LO-вызова при одном fine R/A дают точное finite-operator разложение

\[
M=\Gamma_{LO,f}(\mu_f)-\Gamma_{LO,f}(\mu_c),\qquad F=D-M.
\]

Один R и два LO, без full Φ/Pi и refit, воспроизвели saved N при обеих μ и fine LO norm с нулевой replay error. Δμ≈−0.494641μeV; fixed-μ Nfine/target−1≈7.11110e−5. Old-node held-μ defect упал до weighted relative8.15e−15, но midpoint F остался0.0037536598. Это исключает μ-refit как объяснение **измеренного dominant defect**, не доказывая единственную причину nonlinear plateau. Refinement меняет endpoint ghost hats; маленькая source delta отдельно оценена, resolvent amplification не сертифицирован.

Fine2x от stableΓ64/history1: coarse wholeΦ exact0;213.21s/6581748KiB/Swap0. Terminal cross-grid Φ discrepancy0.002520039/weighted0.002516081 включает собственныеμ/ghost variants, не error bound. Native full-grid admission остаётся отказом (`equilibrium-gamma-fine2x-m1/attempt01/summary.toml`).

Frozen Jv:5Φ/4Jv, Γupdates0,82.72s/3444604KiB. FD-error при ε1e−3→5e−4:4.70096e−6→1.17525e−6; normalizedδN≤1.362e−14. Arnoldi3 Ritz1.000148 имеет residual.116849 (остальные≈.78/.76); restrictedGMRES предсказывает1.59% снижения, не full spectral-radius/stall proof (`adjacent/stable-source-jv/attempt01`).

## Принятый код и научные источники

Приняты Core [#27](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/pull/27) compatibility, [#28](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/pull/28) selected cache, [#29](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/pull/29) exact uniformPIFFT/conservative planning, [#30](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/pull/30) direct-static variant, [#31](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/pull/31) exact IFR. [Runner#52](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/52)/[#53](https://github.com/Afonenko-QCL-NEGF/QCLNEGFRunner.jl/pull/53) приняли совместимость/restart и source selection. Nonuniform PI сохраняет dense fallback; полного nonuniform production acceptance нет. Direct-static closure научно отдельна, не подменяла Hilbert Γ-pilots.

Exact IFR использует Dⱼ=dⱼuⱼuⱼ†: q=u†Gu, radial mixing, суммаd²q·uu†; source guard/dense fallback и qK/wk однократно сохранены. На FD64 GR:2.196× median, error5.53e−16 **IFR-only**, не end-to-end speedup.

Поздние Γ/Mats/fine/Jv опыты относятся к Core **e171caa6**; прежние native baselines — к **f50**, строго по attempt identity. Финальная пара — Core **db26a0ef**/Runner **53b3a280**. Её45.86s integration smoke: совместный import, две acoustic-only fixed-U итерации и direct HDF5 GR/GL roundtrip. Не Runner checkpoint/restart, не IFR benchmark, не native SCBA acceptance. Standalone Runner53b всё ещё pin-selects Coree171; path-developed финальная пара — другая source identity.

Физическая опора direct static covariance: [Kalvová–Velický, PRB65,155329, Eqs.63/66/68](https://doi.org/10.1103/PhysRevB.65.155329). Matrix-Dyson stability/edge результаты [Ajanki–Erdős–Krüger](https://doi.org/10.1007/s00440-018-0835-z) имеют дополнительные предпосылки и не доказывают convergence нашего LO mixer. Открытые solver-подходы не портировались: [NESSi paper](https://doi.org/10.1016/j.cpc.2020.107484), source6bb4c832/MPL2 и применимость — `adjacent/nessi-analysis.md`.

## Provenance, воспроизведение и незавершённое

Provenance anchors: FD64 H5 `e6fffb997f…`; unprojected Γ64 H5 `cab81029eff5…`, model `700ae17684d9…`; full-PD summary `a703ec4c3e2f…`; Big44 summary `e0f462249519…`; streaming summary `c48d6e4ff1d1…`; coarse/fine H5 `27cefe8bed43…`/`87ad129508f6…`. Полные SHA, exact inputs/Manifest/source graph, datasets и команды находятся в соответствующих immutable attempt и review; сокращённые значения здесь — locators, не замена hash verification. Arrays не коммитились. [Research bundle](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/tree/801d613cee4f73e11d3ee093b1d2045532f70b92/experiments/campaign133) содержит frozen scripts/small evidence; финальный snapshot8 принят через [Research PR #12](https://github.com/Afonenko-QCL-NEGF/qcl-negf-research/pull/12):1593entries, manifest SHA256 `6e221f32f7c2dd65927d61b9969d2052dfb1a9cbe89cbd27c4b65202a4a249e9`. Все3186source/publicSHA проверены, private-path данные исключены. Большие исходные массивы остаются на ВМ.

Actual replay требует исходных H5, whole SHA до/после чтения, exact e171/Julia1.13.3/Manifest и реального внешнего resource scope; copied input с `runtime_authorized=false` запуск не разрешает.

Итоговый refined replay: CLI без `--tiny`, отдельный2GiB/J1/BLAS1/1200s/data1GiB/file32MiB scope и новый bound input/output:

```sh
julia --startup-file=no --threads=1 --project=NEW_BOUND_ENV \
  .build/campaign133/adjacent/matsubara-mu-root-refined/run_mu_root.jl \
  NEW_AUTHORIZED_INPUT NEW_OUTPUT
```

**История/ограничения:** old μ128/256 UNRUN из-за cutoff; refined attempt01 world-age failure1.82s до model/maps/пустойoutput сохранён отдельно от successfulV2. Bond-current NOTRUN: algebraic zero для любой localΣ, не независимая physical validation (`reviews/matsubara-bond-current-feasibility.md`).

## Конечное напряжение: подготовлено, запуск отложен

Пользователь подтвердил **1mV на период и отсутствие e-e рассеяния**. Подготовлен matched cold pilot0/1mV: полный native Dyson/Keldysh и ΣR/L/G, all5, fixed HartreeU0,32 maps/case; FD используется только для начального seed. Новая сетка N24001/50µeV и direct-static+PI closure обозначены отдельно; их сходимость не установлена. Малый native API/HDF-контроль дал14/14 assertions; это не полноразмерный физический результат.

Первый resource admission отказал до запуска. Подготовлен только resource-only вариант с hard11.75GiB; повторный plan/actual не выполнялся после просьбы отложить тяжёлую работу. После перезагрузки нужны свежий ресурсный preflight и согласование абсолютного cutoff с уже разрешённым резервом; старый UTC05 guard нельзя молча обходить. E-e mode:none не равнозначен отключению Hartree: здесь U0 — явное дополнительное условие. Равновесное Mats/FD предположение при напряжении не используется.

**Ближайший согласованный опыт:** выполнить этот bounded0/1mV контроль, проверить исходные raw residuals, λ, число, ток и collisional balances. До этого finite-bias convergence/current остаются `not_measured`.

**Методический кандидат для последующего сравнения:** mixed-axis LO ladder через midpoint469.820607meV с Mats anchor (`adjacent/mixed-axis-LO-continuation.md`,736aca…). [Margine–Giustino2013](https://arxiv.org/html/1211.3345), Eqs.26–27 используют FS/constant-DOS: статья поддерживает framework, **наша full-matrix формула имеет самостоятельный spectral-measure/scalar proof**, без переносаiπ/NF. Sign review `reviews/mixed-axis-LO-static.md`: complex f обязателен, 0<η≤ω₀/2; приη>0 нельзя Herm(C). Малый Mats contraction bound q не доказывает real-axis contraction; однаphase не даёт density. Cutoff/ladder length/η контролируются отдельно. В этой кампании реализация/новый run исключены.

| Утверждение / процесс | Свидетельство | Ограничение | Решение |
|---|---|---|---|
| Finite-N M3 fixed-charge equilibrium установлен | Equation/value audits N512/N1024 | Не rigorousN∞/Poisson/transport | **Сохранить результат** |
| Raw residual, domain guards и immutable lineage полезны | Отказы q/cone, preserved baseline, independent audits | μ-fit/mixing/exit0 не заменяют уравнения | **Сохранить** |
| Asub-путь неточен в проверенных слабых хвостах | Split Big44, exact source PD и covariance comparison | Не универсальная forward-error bound | **Изменить** construction с отдельной identity |
| Новые midpoints различают сеточную ошибку лучше old-node replay | Frozen2x D и exact μ decomposition | Будущий fine nonlinear solve ещё не принят | **Сохранить** comparator для mixed-axis |
| Повтор coarse/mixing без нового witness | История и frozen-grid controls | Raw artifacts/tests сохраняются | **Убрать**, выбрать mixed-axis опыт |
