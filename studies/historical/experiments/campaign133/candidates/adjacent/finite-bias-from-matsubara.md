# 1mV/period без e–e: что переносится из thermal Mats root

Research-only; Julia/Pkg/H5/новые опыты не выполнялись. **Быстрый V0 Mats
root не обещает быстрый biased SCBA.** Переносятся physical model, проверенные
kernel conventions, equilibrium density/μ как seed/reference. Imaginary-axis
G не является real-axis GR; FD `G<=ifA` и общий thermal μ не задают biased
distribution. Basis/H/T/kernels/cache/shiftplans требуется rebuild либо
проверяемое равенство: при bias cavity использует E+jEperiod, а не одну
Σ(E) во всех9 cells. Из thermal root можно сделать warm guess только после
согласованного real-axis materialization; это отдельная identity, не принятие
исходного unresolved baseline. Fixed-Hartree вопрос отделён от Poisson.

На accepted Core e171/tree742, `production_operators.jl:1240` реализует
distribution-independent static `ΣsR=Ks[GR]`; это допустимо и вне equilibrium
для energy-local Born kernels, без e–e. Но LO retarded часть зависит от
occupation. При n=−iG<, p=iG>, n+p=A, S₊[X](E)=X(E+Ω),
S₋[X](E)=X(E−Ω), fixed Bose NB:

`ΣLO<=iKLO[(NB+1)S₊[n]+NB S₋[n]]`,
`ΣLO>=−iKLO[(NB+1)S₋[p]+NB S₊[p]]`,
`ΓLO=KLO[(NB+1)S₋[A]+NB S₊[A]+S₊[n]−S₋[n]]`.

Это algebra actual `_production_lo_contraction` (`production_operators.jl:974`),
а R восстанавливается из свежих </> в scattering candidate: **e–e0 не
устраняет nonlinear R↔occupation feedback**. Малый NB не разрешает выкинуть
absorption;1meV drop также не гарантирует linear regime относительно узких
linewidths/resonances. Finite-chain/window/interpolation biases остаются.

Полезный будущий discriminator при kinetic plateau: заморозить **все** local
и side/cavity retarded propagators первого согласованного biased state.
Без paired normalization raw updates тогда линейны:
`n′=Tn n`, `p′=Tp p`. Ks, LO shifts и cavity lesser propagation linear
(`production_operators.jl:158,235`); density задаёт scale. Nonzero stationary
solution требует eigenvalue1, **обоих** equations, n,p⪰0 и n+p=A. Для одного
lesser eigenvector недостаточно нормировать N: frozen R может вообще не
допускать согласованной pair. Измерять raw absolute/weighted vector residual,
eigenvalue defect, Pauli/pair defect, collisions/window leakage и fresh LO-R
mismatch; near-null modes/неединственность при e–e0 не исключены.
`production_state.jl:52` native λ=Nraw/Ntarget — на произвольном iterate лишь
number ratio, не eigenvalue. `:paired_convex` далее переносит holes↔occupied;
его normalized output не заменяет этот linear diagnostic или raw acceptance.
Новый inner solver сейчас не предлагается: сначала существующий bounded
native full-R/L/G1mV control и его свежие rK/rΣ/λ свидетельства.

Из imaginary axis **в принципе** доступен infinitesimal Kubo response, но
нужен two-particle vertex: contour Dyson variation
`δG=G(δU+δΣ)G`, `δΣ=(δΣ/δG)δG`. Born disorder/LO vertex не исчезает вместе
с e–e; continuation external bosonic frequency и DC limit также нужны.
Тепловой Γ-only Jacobian исключает occupation modes и этим vertex не является.
Связь conserving response с consistent self-energy derivative обоснована в
[Baym–Kadanoff1961](https://journals.aps.org/pr/abstract/10.1103/PhysRev.124.287);
необходимость self-energy variation для gauge-independent QC response — в
[Wacker2002](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.66.085326).
Primary abstracts проверены; формулы выше выведены из actual code. Для нашей
finite-window/central-driven closure conserving/Ward property отдельно
проверяется, не наследуется по названию SCBA. Такой Kubo путь не готовый
дешёвый1mV solve и не доказывает finite-bias linearity. Успех Mats equilibrium
и старые frozen-Γ certificates остаются научно отдельными результатами.
