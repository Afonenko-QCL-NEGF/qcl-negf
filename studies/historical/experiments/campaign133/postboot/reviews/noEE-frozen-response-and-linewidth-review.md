# Независимая review: noEE frozen/full response и LO linewidth

**Вывод: выбранный no-model-change discriminator математически пригоден; перед actual требуется уточнить frozen anchor и доступ к raw до normalization.** Physical LO width остаётся отдельной гипотезой, не диагнозом stall. Исходные notes не редактировались; Julia/Pkg/HDF/numeric maps reviewer не запускал. Текущая fine48001 пара не оценивалась этим review.

Проверены новые notes exactSHA: `next-noEE-frozen-response.md` **68bf83f816bae77ff02a8b9ce4d5793a3067b49a7da3fba93298e8185252c56b**, `LO-spectral-width-hypothesis.md` **f13c0d4b3b3f6212dc1baa2d49d0c955a3c55dd8c65b5036721d242a52a7f403**. Read-only code binding: accepted Core **e171caa60cce676c6c4238dd671e7c527f2bd977**, tracked clean. Новый cwd — artifact directory, не Git checkout; код сопоставлен с прежним accepted source tree, а не выдан за новую ревизию.

## Perturbation и graph

При N1,P0>0 имеем0<u=q/P0≤10⁻³ и0<v=q/N1≤10⁻³. Sector0: n′=n+up,p′=(1−u)p; sector1: n′=(1−v)n,p′=p+vn. При исходных PSD n,p обе пары PSD и n′+p′=n+p **в каждой точке**. С исходными gs·wE·wk/(2π) δN0=q,δN1=−q,δNtotal=0,δ(N0−N1)=2q. Это Pauli-safe относительно **source B=n+p**, не исправление исходного B−A. Source B=A не следует из малого N residual. На Float source нужны исходные/perturbed cone witnesses и actual δN/contrast/B defect; если capacity или representable perturbation равны0 — unavailable, не hidden renormalization. Strict PSD из machine cone не доказана — note это корректно оговаривает.

Идеальные734/20 shifts дают parity, V0 ideal734 —734 energy residue classes, но не такое число нейтральных eigenmodes. Core `production_cache.jl:258–287` действительно вычисляет fractional weight без near-integer snap; `production_operators.jl:158–193` аналогично строит cavity remaps. Поэтому actual graph должен учитывать **все ненулевые** веса/active channels/zero extension; activity и общий response gain отдельно от graph connectivity. Выключать tiny weight threshold нельзя. Полная LO retarded/PV feedback связывает R глобально, но не становится новым collision energy transfer. Static direct_green читает входной GR (`production_operators.jl:1240–1245`); при неизменном inputGR его local staticR не меняется, LO/cavity R могут меняться.

Если source позже выбирается из fine48001/25µeV, нужен новый source bind/graph: ideal shifts1468/40 имеютgcd4; parity — допустимый **coarse contrast**, не заявление о ровно двух components. Notes сейчас явно относятся к24001/50µeV, переносить их source identity молча нельзя.

## Один valid next discriminator и execution blockers

После фактически установленного stall выбранного aligned1mV state — одна N-neutral perturbation выше и две matched arms, **≤2 full maps+2 frozen-L/G applications**, без дополнительных iterations/Γ repair/μ fit:

1. Один fresh full **unperturbed** map фиксирует R*: local scatteringR, все side-cavity retarded inverses/embeddings и output centralGR. Этими же R* пользоваться в обоих frozen applications. Frozen-base raw L/G обязаны воспроизвести fresh-full-base raw L/G в объявленном arithmetic допуске. Простое удержание stored **input** GR/R может смешать occupation→R feedback с обычным base-cycle drift: тогда это иной control, не чистая partial response.
2. Fresh full perturbed map пересчитывает всеR; frozen perturbed application пересчитывает только </> источники и cavity </> при R*. Сравнить Δraw обеих arms с тем же δ(n,p), включая sector contrast gain, both n/p norms, δ(B−A), LOδR и boundary flux. Frozen near-unit/full materially different — evidence retarded feedback в этом response; near-unit в обеих — кандидат slow memory, не доказанная conserved charge/причина stall/spectral radius.
3. **Raw-before-paired обязателен.** `_current_green_production` (`production_state.jl:52–75`) считает λ=Nraw/Ntarget, затем меняет пару; обычный возвращаемый Green уже normalized. Нельзя выдать его за raw map. Сохранить raw N_s/P_s и response до `_paired_number_coefficients`, затем отдельно a,c и Nnew_s=aNraw_s+cPraw_s. λ произвольного input — charge ratio, не измеренный eigenvalue. Потребуются конкретный raw-capture adapter/source hashes и ресурсное admission Root по measured cost; их ещё нет в исследовательской note. Это blockers реализации, а не математики perturbation.

## Physical linewidth: KMS и цитаты

С note-конвенциями n=−iG<,p=iG> greater должен быть
`Σ>(E)=−i∫b(ε)Kε[(Nε+1)p(E−ε)+Nεp(E+ε)]dε`.
При p(E±ε)=exp[β(E±ε−μ)]n(E±ε) и Nεexp(βε)=Nε+1 получаем **покомпонентно как matrix identity** Σ>(E)=−exp[β(E−μ)]Σ<(E). Поэтому note's energy-dependent Bose factor и одинаковые emission/absorption vertex maps дают правильный bath KMS. Fixed NB(Ω) при распределённыхε этого обычно не даёт. Для PSD источников нужен положительный spectral measure и vertex contraction, сохраняющий PSD, а не только entrywise-positive scalar kernel.

Будущая model identity должна обеспечить Γ=i(Σ>−Σ<), ΣR−ΣA=Σ>−Σ< и retarded dispersive part от того же causal bath/vertices с теми же static terms; независимое smoothingΣR или electronη этого не заменяет. Кроме causal odd phonon spectral function нужны finite thermal-weighted integrals, например `∫b(ε)(2Nε+1)||Kε||dε<∞`, и корректные normalization/zero-width limit. У произвольной positive-half Lorentzian с b(0)>0 Bose∼1/ε может дать infrared divergence; odd causal alone не является готовым finite bath specification. Численное γ/калибровка/новая implementation пока отсутствуют — actual linewidth experiment этим review не одобрен.

Primary abstracts перепроверены напрямую. [Vallée–Bogani PRB43,12049](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.43.12049) поддерживает temperature-dependent coherent LO dephasing в GaAs, **не** width нашей doped heterostructure при70K. Lorentzian HWHM=ℏ/T2/FWHM=2ℏ/T2 требует exponential coherence; T2=2T1 — отсутствие pure dephasing. [Lee–Wacker PRB66,245314](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.66.245314) подтверждает QCL electron-phonon/impurity/IFR SCBA precedent (с mean-field electron-electron частью), не нужный broadened fixed bath и не разрешение добавлять e–e. Осторожный citation scope обеих notes корректен.

Итоговое решение: далее полезен именно matched frozen/full **raw** finite response с fresh-base anchor и отдельным paired-transfer ledger. Он может различить механизмы локального response, но пока ни одна note не доказывает причину нашего stall. Linewidth — последующий отдельный физический вариант только после spectral/KMS/RLG/low-energy specification и отдельного разрешённого resource/input scope.
