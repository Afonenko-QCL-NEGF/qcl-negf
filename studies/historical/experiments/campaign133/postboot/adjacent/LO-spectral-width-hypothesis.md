# Может ли physical LO linewidth смешать phase sectors без e–e?

**Структурно да; это ещё не диагноз нашей SCBA.** Research-only: модель не
изменялась, реализация/Julia/Pkg/H5/новые опыты не выполнялись. В нынешнем
native model electronic broadening Γ и retarded KK не меняют разрешённые
collision transfers ±Ω. Конечная **phonon** spectral width — другой объект.

Пусть ε>0 — энергия phonon transfer, b(ε)≥0 — coupling spectral measure
causal phonon propagator, Nε=[exp(βε)−1]⁻¹. Dispersionless model соответствует
δ(ε−Ω). Born lesser functional становится

`Σ<(E)=i∫₀∞ dε b(ε) Kε[(Nε+1)n(E+ε)+Nε n(E−ε)]`.

Greater использует p=iG> и противоположные emission/absorption shifts.
Continuous positive support b даёт transfers помимо ±Ω и в общем разрушает
идеальные E modΩ/parity sectors. На discrete grid это требует actual
off-sector quadrature support: broadening, представленная только even shifts,
может сохранить parity. Width существенно меньше ΔE может быть не разрешена;
width нельзя выбирать равной grid step просто для ускорения.

Физически согласованный вариант использует один causal D^R, его signed odd
boson spectral function, **связанные с ним** D</> через bath FDT и те же vertex
weights в electron ΣR/L/G. Для каждого ε требуется `(Nε+1)/Nε=exp(βε)`.
Тогда equilibrium electron FD detailed balance выполняется termwise и после
интегрирования. Сглаживание energy shifts при неизменном N_B(Ω) обычно это
нарушает. Добавление η только в **electron GR**, smoothing готовой ΣR/Γ или
rounding stencil weights физическую phonon spectrum не заменяет. Это отличает
новую физическую approximation от numerical regularization старой identity.

Primary motivation: [Vallée–Bogani, PRB43,12049(1991)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.43.12049)
измеряли temperature-dependent LO **dephasing** в GaAs. Это свидетельство
конечного phonon coherence time, не калибровка width нашего doped heterostructure
при70K. Population lifetime T1, coherence T2, HWHM/FWHM нельзя смешивать:
при exponential coherence energy HWHM=ℏ/T2, FWHM=2ℏ/T2; равенство T2=2T1
требует отсутствия pure dephasing. Здесь никакое численное γ не выбрано.
Полная nonequilibrium SCBA постановка electron-phonon self-energies для QCL
имеет primary precedent [Lee–Wacker, PRB66,245314(2002)](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.66.245314);
это не утверждение, что данный paper уже использует нужную broadened bath.
Проверены primary abstracts; модельное integral statement выше — независимый
вывод из Born energy convolution, не цитата из измерения.

Это смелая **последующая физическая гипотеза**: spectral bath width может
снять некоторые kinetic degeneracies, но не гарантирует uniqueness,
contractivity или convergence полной R/L/G SCBA. Перед ней выбран более
различающий no-model-change frozen/full raw-response control из соседней
записки. При будущем отдельном physical variant нужны источник/uncertainty
phonon spectrum, новый input identity, zero-width limit и fixed-bath KMS
check. Никаких e–e добавлений пользователь не разрешал; здесь они не предлагаются.
