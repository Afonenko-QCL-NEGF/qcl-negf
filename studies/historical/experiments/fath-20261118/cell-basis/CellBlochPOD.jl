module CellBlochPOD

using LinearAlgebra
import QCLNEGF

const Q = QCLNEGF
const N = Q.QCLNumerics
const METHOD = :bloch_snapshot_pod
const BOUNDED_METHOD = :bounded_bloch_snapshot_pod
const TRAIN_PHASE_COUNT = 24

"""Use one real orthonormal cell basis from a zero-field Bloch snapshot SVD."""
function train_basis(n, scales, grids, profiles; train_bands::Int, max_principal_angle=nothing)
    1 <= train_bands <= n.N_z || throw(ArgumentError("invalid snapshot band count"))
    1 <= n.N_b <= n.N_z || throw(ArgumentError("invalid POD rank"))
    dx = only(unique(grids.wˣ))
    Hcell = Q.build_bdd_hamiltonian(profiles, grids, scales; boundary=:periodic)
    T = zeros(n.N_z, n.N_z)
    T[end,1] = Hcell[end,1]
    Hcell[1,end] = Hcell[end,1] = 0
    Egrid = maximum(abs, diag(Hcell))
    snapshots = Matrix{ComplexF64}(undef, n.N_z, train_bands * TRAIN_PHASE_COUNT)
    training_residual = 0.0
    for j in 0:TRAIN_PHASE_COUNT-1
        phase_factor = cispi(2j/TRAIN_PHASE_COUNT)
        Hphase = Hermitian(Hcell + phase_factor*T + conj(phase_factor)*T')
        solved = eigen(Hphase/Egrid, 1:train_bands)
        columns = (j*train_bands+1):((j+1)*train_bands)
        snapshots[:,columns] = solved.vectors
        residual = (Hphase/Egrid)*solved.vectors - solved.vectors*Diagonal(solved.values)
        training_residual = max(training_residual, maximum(norm, eachcol(residual)))
    end
    # Re/Im stacking preserves the complex projector density for a real subspace.
    frame = svd(hcat(real(snapshots), imag(snapshots))/sqrt(TRAIN_PHASE_COUNT))
    n.N_b <= length(frame.S) && frame.S[n.N_b] >= 100eps(Float64)*frame.S[1] ||
        throw(ArgumentError("insufficient numerical snapshot rank"))
    phi_real = frame.U[:,1:n.N_b]
    if max_principal_angle !== nothing
        0 < max_principal_angle <= pi/2 || throw(ArgumentError("principal angle cap must lie in (0,π/2]"))
        anchor = eigen(Symmetric(Hcell/Egrid), 1:n.N_b).vectors
        alignment = svd(anchor'*phi_real)
        reference = anchor*alignment.U
        phi_real = phi_real*alignment.V
        for j in axes(phi_real, 2)
            cosine = clamp(alignment.S[j], 0, 1)
            angle = acos(cosine)
            if angle > max_principal_angle
                scale = sin(max_principal_angle)/sin(angle)
                phi_real[:,j] .= (cos(max_principal_angle)-scale*cosine).*reference[:,j] .+
                    scale.*phi_real[:,j]
            end
        end
        phi_real = Matrix(qr(phi_real).Q)[:,1:n.N_b]
    end
    for column in eachcol(phi_real)
        column .*= sign(column[argmax(abs.(column))])
    end
    Phi = ComplexF64.(phi_real)
    H0 = Phi'*Hcell*Phi
    Tplus = Phi'*T*Phi
    Z = Phi'*Diagonal(grids.x)*Phi
    M = Phi'*Diagonal(1 ./ profiles.m_parallelᵣ)*Phi
    centres = real.(diag(Z))
    second = real.(diag(Phi'*Diagonal(grids.x.^2)*Phi))
    spreads = sqrt.(max.(second-centres.^2, 0))
    overlap = Phi'*Phi
    method = max_principal_angle === nothing ? METHOD : BOUNDED_METHOD
    basis = Q.BasisData(
        method, Phi, Phi/sqrt(dx), centres, spreads, eigvals(Hermitian(overlap)),
        cond(overlap), H0, Z, M, Tplus, Matrix(Tplus'), eigvals(Hermitian(H0)), Egrid,
        norm(overlap-I), training_residual, NaN, NaN, NaN,
    )
    provenance = Dict("basis_method"=>string(method), "train_bands"=>train_bands,
        "train_phase_count"=>TRAIN_PHASE_COUNT, "train_voltage_mv"=>0,
        "pzp_translation_diagnostics"=>"inapplicable",
        "max_principal_angle_rad"=>something(max_principal_angle,"unbounded"))
    return (; basis, singular_values=frame.S, train_bands, phase_count=TRAIN_PHASE_COUNT, provenance)
end

"""
Build a Fath production problem with native e171 scattering and nodal shift plans.
All five vertices consume the final POD basis via the stock assembly context.
Metadata identifies the alternate basis separately from native algorithm options.
"""
function build_problem(;
    physical, numerical, scales, scattering, algorithms, kernel_options, physical_models,
    train_bands::Int, max_principal_angle=nothing,
)
    algorithms.solver_backend === :production && algorithms.energy_shift === :sparse_plan ||
        throw(ArgumentError("this campaign constructor requires production sparse shift plans"))
    physical_models.electron_electron.mode === :none ||
        throw(ArgumentError("this campaign constructor requires electron-electron scattering off"))
    physical = Q.resolve_physical_models(physical, physical_models)
    grids = Q.build_grids(physical, numerical, scales)
    profiles = Q.build_profiles(physical, numerical, scales, grids)
    training = train_basis(numerical, scales, grids, profiles; train_bands, max_principal_angle)
    context = Q.ScatteringAssemblyContext(physical, numerical, scales, grids, profiles, training.basis)
    models = Q.scattering_models(physical, scattering)
    plan = Q.scattering_numerical_plan(algorithms, kernel_options)
    assembled = Q.assemble_scattering_kernels(context, models, plan)
    sp = N._scaled_physics(physical, scales)
    shifts = map(shift -> Q.build_shift_plan(grids.ε, shift),
        (+sp.Eᵖ, -sp.Eᵖ, +sp.ħωᴸᴼ, -sp.ħωᴸᴼ))
    problem = Q.NEGFProblem(
        physical, numerical, scattering, scales, grids, profiles, training.basis,
        assembled.kernels, shifts..., :nodal_linear, physical_models,
    )
    report = Q.validate_problem(problem)
    report.passed || throw(ArgumentError("static POD model validation failed: " * join(report.messages, "; ")))
    return (; problem, training, static_report=report, kernel_diagnostics=assembled.diagnostics,
        scattering_evidence_class=assembled.evidence_class)
end

end
