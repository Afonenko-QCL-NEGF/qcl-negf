# julia --project=runner check_balance.jl /path/to/studies/fath-v843
using LinearAlgebra, Random, Test
include(joinpath(abspath(only(ARGS)), "test_spatial_balance.jl"))
include("observe_balance.jl")

BLAS.set_num_threads(1)
Random.seed!(54)
random_frame = randn(ComplexF64,14,9)
dual = Matrix(inv(Hermitian(random_frame' * random_frame)))
random_hermitian() = Matrix(Hermitian(randn(ComplexF64,9,9)))
lift(op) = random_frame * op * random_frame'
lift_sigma(op) = lift(dual * op * dual)

h = random_hermitian()
g_h, lesser, greater = random_hermitian(), im*random_hermitian(), -im*random_hermitian()
s_h, sigma_l, sigma_g = random_hermitian(), im*random_hermitian(), -im*random_hermitian()
retarded, sigma_r = g_h + (greater-lesser)/2, s_h + (sigma_g-sigma_l)/2
coordinate_h, coordinate_lesser = lift_sigma(h), lift(lesser)
monitor = 4:11
direct = vec(sum(projected_crossings(random_frame,dual*h*dual,lesser,monitor,4); dims=2))
rectangles = [2sum(real(coordinate_h[i,j]*coordinate_lesser[j,i])
    for i in 1:a, j in a+1:size(random_frame,1)) for a in 4:10]
@test direct ≈ rectangles
@test diff(direct) ≈ 2real.(diag(lift(dual*h*lesser))[5:10])

combined, kinetic, dispersive, scratch, lh, sh = (zero(dual) for _ in 1:6)
lo_split_terms!(combined,kinetic,dispersive,scratch,lh,sh,
    retarded,lesser,greater,sigma_r,sigma_l,sigma_g,dual)
anticommutator(a,b) = a*b+b*a
commutator(a,b) = a*b-b*a
@test lift(kinetic+kinetic') ≈
    (anticommutator(lift(greater),lift_sigma(sigma_l)) -
     anticommutator(lift_sigma(sigma_g),lift(lesser)))/2
@test lift(dispersive+dispersive') ≈
    commutator(lift(g_h),lift_sigma(sigma_l))-commutator(lift_sigma(s_h),lift(lesser))
@test combined+combined' ≈ kinetic+kinetic'+dispersive+dispersive'

p0 = test_problem(modal_change)
p = LT.LinkedProblem(p0.en,p0.we,p0.wk,p0.geo.modes,p0.nb,p0.geo.offsets,p0.geo.voltage,
    p0.geo.reach,p0.h,p0.hops,p0.const_by_channel,p0.v; spin_degeneracy=p0.spin_degeneracy,
    current_scale=1e6,density_scale=p0.density_scale,target_dimless=p0.target_dimless)
z = [FATH_LATE7_CUTS_NM...,43.91]
linked_metrics(_,_) = (;fermionic_pair=(a=1.0,c=0.0),current_profile_A_cm2=original.current_A_cm2)
probe = observe_balance(p,fields,(;source=lagged,summary=nothing),z,1;
    energy_rule=nothing,fresh_profile=false)
@test probe.lagged.current_A_cm2 ≈ 1e6 .* original.current_A_cm2 atol=1e-8
@test probe.lagged.projected_current_A_cm2 ≈ probe.lagged.current_A_cm2 atol=1e-8
@test probe.lagged.kinetic_remainder_A_cm2 ≈ 1e6 .* inconsistent.kinetic_remainder_A_cm2 atol=1e-8
@test probe.lagged.maximum_closure_error_A_cm2 < 1e-8
@test probe.lo_localization.triggered
@test only(probe.lo_localization.selected).ring == 1
@test probe.lo_localization.selected_lo_fraction ≈ 1.0
@test abs(probe.lo_localization.selected_reconstruction_error_A_cm2) < 1e-8
@test abs(probe.lo_localization.native_ring_sum_error_A_cm2) < 1e-8
@test only(probe.lo_localization.split.rings).maximum_closure_error_A_cm2 < 1e-8
println("Direct projected crossings and conditional LO decomposition passed.")
