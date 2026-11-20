# Static refinement of the compact Fath cell basis

Eight of ten predeclared bases at ranks 9–12 passed the 0.5 meV low-energy criteria at both Nz=144 and Nz=192. Five also passed the earlier 0.10 meV band-study criteria. The tests covered the first four Bloch bands, both central target energies, their splitting, and the principal overlap of the target pair. Every passing basis failed the full-matrix spectral-sum test on the tested energy meshes with 2,401–4,001 nodes.

The unbounded seven-band POD at rank nine passed the bare full-matrix sum on [−400, 4000] meV with 11,001 nodes. At Nk=9, this setup fits the e171 memory preflight for one exploratory transport test. Its top Ritz direction is far outside the energy range of the relevant exact FD bands. Treat this setup as a diagnostic of one numerical representation.

## Comparison criteria

The training uses CBO 149 meV, zero field and zero transverse momentum. Pure POD combines the real and imaginary parts of the lowest selected Bloch states at 24 uniformly spaced phases. Cell augmentation keeps an unbounded POD core and adds the lowest cell-block Ritz vectors in its orthogonal complement. The shifted seam construction retains the lowest fixed-interface states and approximates the remaining seam response at 35 meV. The scan and thresholds were declared in [passport.toml](passport.toml) before the run.

The independent hold-out uses 131 new Bloch phases and a matched seven-period Dirichlet window at 54 mV. The FD target pair has 0<E<20 meV and at least 85% probability in the central cell. The two Ritz partners maximize the smaller squared principal cosine with the target pair. The broader diagnostic uses full FD states in [−100, 80] meV with at least 10% central probability and matches individual eigenvectors by maximum squared overlap.

| Basis | Worst energy criterion across both Nz (meV) | Lowest pair principal cos² | Worst broader-state energy error (meV) | Lowest broader match overlap² |
| --- | ---: | ---: | ---: | ---: |
| POD7, rank 9 | 0.1805 | 0.99955 | 0.283 | 0.989 |
| POD8, rank 10 | 0.0605 | 0.99964 | 0.244 | 0.998 |
| POD5 core 7, cell augmented rank 9 | 0.0575 | 0.99877 | 7.442 | 0.696 |
| POD5 core 8, cell augmented rank 10 | 0.0269 | 0.99897 | 1.627 | 0.480 |
| POD7 core 9, cell augmented rank 12 | 0.1777 | 0.99959 | 0.229 | 0.990 |

At Nz=144, the exact target pair lies at 6.953 and 11.332 meV. The unbounded POD7/rank9 gives 6.992 and 11.406 meV, with a splitting error of 0.0353 meV. Its orthogonality residual stays below 3.6×10⁻¹⁵ on both grids. [All ranks and grids](summary.csv)

## Where the upper pole comes from

For POD7/rank9, the worst ninth Bloch Ritz value at Nz=144 is 2,617 meV where the exact ninth FD band is 267 meV. At Nz=192, the corresponding values are 3,467 and 266 meV. The squared overlap with the strongest exact FD eigenvector is 0.177 and 0.190. Exact FD states within ±20 meV of the Ritz value carry 1.56% and 0% of its weight, respectively. The Ritz energy agrees with the energy expectation of the extended FD decomposition, as it should. The expectation concentrates a dispersed exact spectrum into a single variational pole.

At Nz=144 and k=0.60 nm⁻¹, the two highest nine-cell Ritz poles with at least 10% central weight lie at 2,690 and 2,747 meV. Their strongest exact finite-FD partners lie at 494 and 549 meV (squared overlaps 0.046 and 0.053), and less than 0.4% of either state's overlap is within ±20 meV of its Ritz energy. Above an 860 meV cutoff at that k, the reduced model loses 11.16% of the central trace, while the full FD projected onto the same local directions loses 5.02%. This comparison includes the complete discrete FD eigenbasis in the specified finite window.

The first four exact FD Bloch bands at k=0.60 nm⁻¹ reach about 258 meV. The first nine reach 462 meV. Adding 216 meV for the four-neighbour field span and 260 meV for trust reserve gives energy scales of roughly 0.73 and 0.94 eV. These scales describe the explicitly tracked physical FD bands. They do not certify the full interacting spectral sum or a transport window. The multi-eV Ritz pole grows with axial refinement and has no comparable same-energy exact FD eigenstate. [Selected rank-nine FD and upper-sector diagnostics](results.json)

## Full-basis spectral sum and cost

We integrated the exact finite nine-cell bare cavity measure at each represented k. The full matrix is normalized to the identity across all nine basis directions. The deficit uses the e171 Frobenius norm divided by √Nb and takes the worst k. We computed both the analytic Lorentzian integral with η=0.5 meV and the e171 nodal trapezoid. The current, nonequilibrium occupation and interacting line shapes were outside this static test.

For POD7/rank9, the minimum upper cutoff for an analytic full-matrix deficit below 10⁻³ is 2.898 eV at Nz=144 and 3.732 eV at Nz=192. The upper-cutoff scan on 2,401–4,001 nodes hit either this truncation error or large trapezoidal sampling errors. For example, [−400, 3000] meV with 4,001 nodes at Nz=144 gives analytic 4.03×10⁻⁴ and nodal 3.40×10⁻². Widening at fixed node count raises ΔE and can increase aliasing.

For [−400, 4000] meV and ΔE=0.4 meV, η/ΔE=1.25. The worst infinite uniform-grid Lorentzian comb error is 7.77×10⁻⁴ in a single line. The lower cutoff alone contributes 3.29×10⁻⁴ (Nz=144) and 3.28×10⁻⁴ (Nz=192) to the worst-k continuous Frobenius deficit. The upper cutoff alone contributes 5.39×10⁻⁵ and 9.41×10⁻⁵, respectively. The combined nodal result is measured below. The e171 iteration uses working η=0 with its self-energy. A converged transport result needs a fresh spectral-sum check.

| Nk | Nodal r_sum, Nz=144 | Nodal r_sum, Nz=192 | Nz=144 e171 peak GiB, 8 workers | Nz=144 e171 peak GiB, 12 workers | Dense contraction FLOP factor vs original native grid |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 9 | 7.92×10⁻⁴ | 6.54×10⁻⁴ | 11.480 | 11.492 | 0.816 |
| 13 | 8.78×10⁻⁴ | 7.38×10⁻⁴ | 16.620 | 16.634 | 1.697 |
| 17 | 7.92×10⁻⁴ | 7.53×10⁻⁴ | 21.790 | 21.807 | 2.898 |

With a 3 GiB reserve below an 18 GiB peak allowance, only Nk=9 fits the stated estimate. The dense contraction estimate for Nk=9 is 3.525 times the compact PzP7 pair. The estimate does not give wall time, and momentum convergence with nine nodes is untested. The rank-ten variant that passes the 0.10 meV target and the broader active test requires about 4.8 eV and 13,001 nodes at the same energy step on Nz=192. Its conservative estimate is 24.26 GiB at Nk=13. [Resolved spectral grid](resolved_grid.json) · [Native resource estimates](preflight.toml)

## Implementation and reproduction

`RefinedCellBasis.jl` binds the frozen companion `CellBlochPOD.jl` by SHA-256 and calls its unbounded seven-band calculation at rank nine. It uses the alternate numerical identity `fath-cbo149-unbounded-pod7-r9-v1`. The native e171 assembler generates all five kernels from the actual final basis. The small e171 fixture passed its structural checks at 0 and 54 mV. Matrix projection differences were at most 1.81×10⁻¹⁶ relative, and the optimized and literal kernels agreed within 5.88×10⁻¹⁶. The production cache and zero-iteration seed consume the new basis and kernels. The actual Julia and independent NumPy projectors agree within 4.50×10⁻¹⁰ in operator norm. Store both adapter digests and the provenance in any transport run. The frozen bounded rank-seven model is a separate prior variant.

Use Python 3.11+ with NumPy, the pinned Julia 1.13.4 e171 environment, and one CPU and BLAS thread. Generate the sibling `bands/native.toml` with `bands/native.jl` as in the original [cell-basis reproduction](../cell-basis/README.md). The refinement's Julia verifier reads the sibling `transport/device.toml` and records the scalar checks without wavefunctions in its compact output. All commands are relative to the campaign directory.

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
python cell-basis-refinement/refine.py
python cell-basis-refinement/resolved_grid.py
julia --startup-file=no --threads=1 --heap-size-hint=280M --project=/path/to/pinned-environment cell-basis-refinement/preflight.jl
julia --startup-file=no --threads=1 --heap-size-hint=280M --project=/path/to/pinned-environment cell-basis-refinement/verify.jl
python cell-basis-refinement/verify_adapter.py
```

The static scan took 23 s and peaked at 291 MiB RSS. The e171 constructor check took 19 s and peaked at 464 MiB RSS. Both were pinned to one CPU. [Native verification](verification-summary.toml) · [Implementation hold-out](adapter_holdout.json)

[Core e171](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/tree/e171caa60cce676c6c4238dd671e7c527f2bd977)

The published `results.json` is a selected scalar projection for POD7/rank9 on both spatial grids, with representative coarse-window cases and aggregate counts. `refine.py` regenerates the complete original scan. `verification.toml` contains basis columns and is regenerated locally; only its scalar summary and digest are distributed.
