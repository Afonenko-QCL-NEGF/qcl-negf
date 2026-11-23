include("radial_control.jl")
const T = FathRadialControl
using LinearAlgebra
BLAS.set_num_threads(1)
coarse, fine, output = ARGS
input = T.Runner._read_linked_checkpoint(coarse)
pair = T.radial_setup(input.problem,input.current_midpoints,coarse,fine)
prolonged = T.apply_radial(pair.p_to_f,input.seed)
input_checks = T.input_transfer_checks(pair,input.seed,prolonged)
T.radial_write(output,(;coarse=pair.p.nk,fine=pair.f.nk,pair.kernel_common_relative,
    pair.kernel_reciprocity_coarse_and_fine,input_checks,coarse_identity=input.identity,pair.fine_identity,
    protocol_sha256=T.file_sha(joinpath(@__DIR__,"protocol.md"))))
