using LinearAlgebra
using Test
using QCLNEGF
include("spatial_balance.jl")
import QCLNEGF.LinkedTransport as LT
using .SpatialBalance

energy = [-2.0, -0.5, 0.5, 2.0]
we = [0.75, 1.25, 1.25, 0.75]
wk = [1.0]
nz = 2
rank = 2
q = Matrix{ComplexF64}(I, nz, rank)
frame = Matrix{ComplexF64}(I, 3nz, 3nz)
# A nonunit change of mode normalization leaves the physical chain invariant.
modal_change = Diagonal(ComplexF64[0.9, 1.4, 1.2, 0.8, 1.35, 1.1])
h0 = Matrix(SymTridiagonal(fill(0.0, 3nz), fill(-0.15, 3nz-1)))
shift = Matrix{Float64}(I, length(energy), length(energy))
kernels = LT.LocalCollisionKernels(q, wk, zeros(nz), zeros(nz), zeros(0,nz),
    ones(1,1), zeros(ComplexF64,nz,nz,1,1), zeros(nz,nz,1,1), shift, shift, 0.0)
anchor = zeros(ComplexF64,rank,rank,1,5)
function test_problem(change)
    return LT.LinkedProblem(energy,we,wk,frame*change,rank,[-1,0,1],
        0.15,1,reshape(change'*h0*change,3nz,3nz,1),fill(-0.15,nz+1,1),
        anchor,kernels;spin_degeneracy=2,current_scale=1.0,density_scale=1.0,
        target_dimless=0.1)
end
fields = zeros(rank^2, 2, length(energy), 1, 5)
fields[1:rank,1,:,1,1] .= [0.07,0.12]
fields[1:rank,2,:,1,1] .= [0.05,0.08]
fields[1:rank,1,:,1,2] .= 0.01
fields[1:rank,2,:,1,2] .= 0.02
cuts = [0.0,1.0,2.0]
rotated = spatial_balance(test_problem(modal_change),fields,[1.0];current_cuts=cuts)
original = spatial_balance(test_problem(I),fields,[1.0];current_cuts=cuts)
@test original.maximum_exact_dyson_residual < 1e-12
@test rotated.maximum_exact_dyson_residual < 1e-12
@test maximum(abs.(original.spatial_projection_gap_A_cm2)) < 1e-12
@test original.current_A_cm2 ≈ rotated.current_A_cm2 atol=1e-12
@test original.collision_cumulative_A_cm2["LO"] ≈ rotated.collision_cumulative_A_cm2["LO"] atol=1e-12
@test original.maximum_closure_error_A_cm2 < 1e-12
@test original.central_bands.fraction ≈ rotated.central_bands.fraction atol=1e-12
@test original.central_bands.total_sheet_over_physical_sheet ≈ 1.0 atol=1e-12
budget = original.spectral_energy_budget
@test budget.absolute_outward_W_m2 ≈ rotated.spectral_energy_budget.absolute_outward_W_m2 atol=1e-12
@test budget.maximum_closure_error_W_m2 < 1e-10
@test abs(budget.relative_to_local_potential.net_relative_energy_minus_absolute_flux_and_work_W_m2) < 1e-10
lagged = copy(fields)
lagged[1, 1, :, :, 1] .*= 2
inconsistent = spatial_balance(test_problem(I),fields,[1.0]; collision_sources=lagged)
@test original.current_A_cm2 == inconsistent.current_A_cm2
@test maximum(abs.(inconsistent.kinetic_remainder_A_cm2)) > 1e-6
@test inconsistent.maximum_closure_error_A_cm2 < 1e-12
println("Manufactured linked current, nonorthogonal lift and lagged remainder passed.")
