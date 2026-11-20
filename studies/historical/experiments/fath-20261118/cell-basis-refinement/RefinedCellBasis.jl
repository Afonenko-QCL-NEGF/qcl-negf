module RefinedCellBasis

using SHA
import QCLNEGF as Q

const FROZEN_ADAPTER_SHA256 = "abd4f904012ea0c3c805a594d55b9aba1e77c637cf7087c04aae3bf2744acf6a"
const COMPANION = "CellBlochPOD.jl"
const ADAPTER = let local_copy = joinpath(@__DIR__,COMPANION)
    isfile(local_copy) ? local_copy : joinpath(@__DIR__,"..","cell-basis",COMPANION)
end
bytes2hex(open(sha256,ADAPTER)) == FROZEN_ADAPTER_SHA256 ||
    error("Frozen numerical adapter hash differs")
include(ADAPTER)

"""Build the separate zero-field, unbounded seven-band POD at rank nine."""
function build_problem(;
    physical,numerical,scales,scattering,algorithms,kernel_options,physical_models,
)
    numerical.N_b == 9 && numerical.N_z in (144,192) ||
        throw(ArgumentError("the refined Fath basis is rank nine on Nz=144 or 192"))
    all(name -> getproperty(scattering,name),(:LO,:acoustic,:impurity,:IFR,:alloy)) ||
        throw(ArgumentError("the refined Fath basis requires all five campaign scattering channels"))
    algorithms.kernel_build === :direct &&
        algorithms.embedding === :finite_chain &&
        algorithms.embedding_periods == 4 ||
        throw(ArgumentError("the refined Fath basis requires direct kernels and four cavity neighbours per side"))
    Q.QCLNumerics._scaled_physics(physical,scales).Eᵖ == 0 ||
        throw(ArgumentError("assemble the reference at zero bias, then retarget using e171"))
    result = CellBlochPOD.build_problem(;
        physical,numerical,scales,scattering,algorithms,kernel_options,physical_models,
        train_bands=7,
    )
    result.training.provenance["basis_rank"] = 9
    result.training.provenance["refinement_identity"] = "fath-cbo149-unbounded-pod7-r9-v1"
    result.training.provenance["frozen_adapter_sha256"] = FROZEN_ADAPTER_SHA256
    return result
end

end
