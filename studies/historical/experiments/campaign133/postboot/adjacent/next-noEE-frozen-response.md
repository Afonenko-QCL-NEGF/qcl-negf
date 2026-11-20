# Если cold32 bias1mV stalls: один noEE discriminator

Research-only, 16Nov2026. Это гипотеза/протокол, **не исход текущей пары**
V0/V1. Julia/Pkg/H5/новые расчёты не выполнялись. Старые notes в прежнем
архиве не менялись. Текущий case: Core e171/tree742, all5/noEE/fixedU0,
native full R/L/G, static direct_green + LO PI, NE24001/50µeV/finite_chain4.

Exact ideal graph: static kernels смешивают κ/orbitals при том же E, LO
связывает E±Ω, cavity — E+jEperiod. Поэтому **при frozen всех retarded
propagators**, без paired constraint, raw `n′=Tn n,p′=Tp p` сохраняет energy
components. Ideal734/20 shifts дают parity; при V0 LO734 даёт734 residue
classes. Это не доказательство734/2 нейтральных modes: boundaries/zero
couplings могут дробить graph, а fixed R может быть несовместимо с λ1.
Actual e171 `production_cache.jl:258` и `production_operators.jl:158` не snap
near-integer stencils. Любой ненулевой соседний weight может соединить parity;
нужны exact nonzero graph и отдельно off-parity weight/activity, без threshold
который объявляет малое значение нулём. Малый stencil weight сам не ограничивает
усиление полного T через почти резонансные GR.

Полная SCBA не block-diagonal: `δF=T δx+(δT[δR])x`; LO Γ зависит от n, и
Hilbert связывает R на разных E. Но real-part coupling не добавляет collision
energy transfer. Поэтому ни сохранение sector charges полной dynamics, ни
их уничтожение KK отсюда не доказаны. One global charge не задаёт все sector
occupations; PairedConvex может менять их численно:
`Nnew_s=a Nraw_s+c Praw_s`. Mats global FD выбирает thermal ensemble.

**Выбранный следующий опыт:** один matched frozen-R/full-R **raw response**
на aligned final1mV state, если его raw residual действительно stalls. Не
продолжать SCBA и не строить новый eigen/Newton solver. Из source
`n=−iG<,p=iG>` взять parity0/1 по `(e−1)mod2`, их occupied/empty numbers Ns,Ps
с исходными gs*wE*wk/(2π). Положить
`q=10⁻³ min(P0,N1), u=q/P0, v=q/N1`; при нулевой capacity — unavailable
либо заранее объявленное обратное направление. Создать **одну** Pauli-safe
perturbation: sector0 `n+=u p,p*=(1−u)`; sector1 `p+=v n,n*=(1−v)`
(правые части из исходных arrays). При PSD source convex transfer сохраняет
PSD; δNtotal=0, δcontrast=2q. Float cone witness не strict PSD certificate.
GR не меняется; сохраняется source B=n+p, **не чинится** возможное B−A defect.
Фактический roundoff δN и source cones измеряются, floor/FD/renormalization нет.

Пропустить source и perturbed pair через две arms: (F) fresh </> contractions
и cavity lesser/greater при всех source R/GR frozen; (R) один обычный fresh
full native R/L/G map из каждого input. Максимум **две full maps + две более
дешёвые frozen-L/G applications**, один процесс, прежние memory/output guards;
последовательный reuse, без удержания двух full states. Никаких extra native
iterations. Exact budget/time Root назначает по measured case cost до запуска.

Сохранить raw absolute/weighted response и `||ΔF−δx||/||δx||` для **обоих**
n,p, sector contrast gain, δ(B−A), sector collisions/embedding flux, fresh
LO-R response, source λ и paired sector transfer отдельно. Первичные counts
до paired normalization обязательны (`production_state.jl:52,64`); native λ
на произвольном input — charge ratio, не eigenvalue. Frozen near-unit response
при большом отличии full arm поддержит роль occupation→R feedback; near-unit
в обеих arms — кандидат на медленную phase memory. Один finite response вне
root не доказывает spectral radius, physical conserved charge или причину
старого stall. Если paired transfer доминирует, это самостоятельная algorithmic
составляющая. Physical phonon linewidth — отдельная модельная гипотеза в
`LO-spectral-width-hypothesis.md`; текущий опыт физику не меняет и e–e не добавляет.
