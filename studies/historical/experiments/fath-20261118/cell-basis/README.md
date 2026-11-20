# Compact cell basis for the Fath 54 mV reconstruction

The bounded rank-seven Bloch snapshot basis improves several low-energy static diagnostics on the CBO 149 meV, 144-node device. It supports a same-grid exploratory comparison with native PzP7. The result covers one-particle spectra and scattering assembly.

## Method

At zero field and transverse momentum, solve the five lowest eigenvectors of the native cell BDD operator at 24 uniformly spaced Bloch phases. Stack the real and imaginary parts of those eigenvectors and retain the seven leading left singular vectors. This uses the same real cell subspace for every period and every momentum. To control the high-energy Ritz directions, align this subspace with the seven lowest eigenvectors of the isolated diagonal block and cap each principal rotation at 0.25 radian. The diagonal block keeps the same seam contribution as the full BDD operator.

The scan included unconstrained snapshot spaces trained on 3–9 bands at ranks 5, 7 and 9, along with a two-mode seam attachment construction. The bounded candidate was chosen after inspecting static spectra and spectral-window coverage. Training used zero-field eigenvectors only. No current, transport solution or experimental target entered the selection.

The final orthonormal columns project H₀, T₊, T₋, Z and M⁻¹. The e171 scattering assembler computes all five enabled channels from their envelopes before creating a `NEGFProblem`. Retargeting retains the basis, kernel tensors and LO form factor. The separate method identity is `bounded_bloch_snapshot_pod`. The inherited PzP translation fields are inapplicable. The legacy `window_eigenvalues` field holds the cell Ritz energies, as for e171's isolated-cell basis.

## Static hold-out

The independent NumPy BDD implementation uses 211 shifted phases disjoint from the training samples. Both full FD and projected tilted spectra use the same seven-cell Dirichlet window, bias origin and end diagonals. A central candidate has at least 10% probability in the central cell. At 54 mV the seven candidates in [−100, 80] meV in the primary geometry each have a distinct dominant match in both arms. The last column is the minimum squared overlap over those matches.

| CBO 149 meV, Nz=144 | Max error in Bloch bands 1–4 (meV) | Min squared principal overlap, bands 1–4 | Max error of 7 central matches at 54 mV (meV) | Min squared state overlap |
| --- | ---: | ---: | ---: | ---: |
| Native PzP7 | 18.762 | 0.739 | 20.033 | 0.443 |
| Unbounded POD, 6 bands, rank 7 | 0.519 | 0.994 | 4.815 | 0.658 |
| Unbounded POD, 7 bands, rank 9 | 0.172 | 0.999 | 0.283 | 0.990 |
| Bounded POD, 5 bands, rank 7 | 11.222 | 0.871 | 8.777 | 0.604 |

At zero field, the maximum ranked error across the lowest 28 finite-window states was 18.698 meV for PzP7 and 11.109 meV for bounded POD7. At 54 mV, their ranked errors were 44.157 and 33.877 meV over the same state count. Over the wider central selection [−100, 170] meV, minimum squared match overlaps are 0.018 and 0.037. These wider matches have too little overlap to identify corresponding levels. Individual bounded errors in the first seven Bloch bands are 3.219, 0.232, 0.597, 11.222, 7.222, 7.671 and 205.095 meV. Bands 2, 3, 5 and 7 each have a larger maximum error than PzP7 in this geometry.

The bounded rank-seven active-window result is similar at CBO 149 meV and Nz=192 (8.804 meV, 0.587). At Nz=96 the dominant energy match is unreliable even in the narrow selection. The 120 meV cases show stronger grid sensitivity. The rank-five and rank-nine bounded variants have weak or duplicate active matches on the primary geometry.

## Spectral window and implementation

For the separate window check, the exact one-particle nine-cell cavity uses 17 momentum nodes through 0.60 nm⁻¹ and 0.5 meV constant Lorentzian broadening. The central spectral trace and a projection weighted by the seven active full-FD states quantify spectral weight above a given cutoff. The percentages integrate the normalized spectral measure over momentum.

| Diagnostic | Native PzP7 | Bounded POD7 | Unbounded POD7, 6 bands |
| --- | ---: | ---: | ---: |
| Highest local pole (meV) | 484.77 | 433.64 | 1383.83 |
| Coupling norm (meV) | 56.63 | 109.36 | 502.83 |
| Exact highest finite-cavity pole (meV) | 715.86 | 699.45 | 1844.33 |
| Central trace above sampled +560 meV | 0.05594% | 0.08474% | 14.316% |
| Active-weighted trace above sampled +560 meV | 0.04531% | 0.04023% | 2.611% |
| Worst single orbital above sampled +560 meV | 0.1261% | 0.3352% | 82.832% |
| Central trace above trusted +300 meV | 15.107% | 14.764% | 14.731% |
| Active-weighted trace above trusted +300 meV | 10.315% | 4.798% | 2.681% |

The bounded arm retains 98.78% of the spatial active weight at k=0. Both rank-seven arms place some poles above the trusted window. A 10 K Fermi occupation of the discrete cavity poles, normalized to the donor sheet, gives negligible occupation above +560 meV. That equilibrium reference gives no bound on nonequilibrium occupations or interacting spectral tails. The high Ritz direction rules out pure POD as a same-window arm.

On e171, an independent seven-cell FD reconstruction agrees with every projected matrix within 3.3×10⁻¹⁸ in maximum relative difference. The original literal and optimized production generators agree within 4.5×10⁻¹⁶ for all five dimensionless raw kernels and the LO form factor. The basis has Frobenius orthogonality residual 1.3×10⁻¹⁵. Independent Julia and Python projectors differ by 4.2×10⁻¹⁰ in operator norm. A small actual-device fixture exercised runtime retargeting, the production cache, and the donor-normalized production seed with zero SCBA iterations.

## Reproduce

Use Julia 1.13.4, the pinned Core environment, Python 3.11 or newer, and NumPy. From the campaign directory, generate `bands/native.toml` via `bands/native.jl`, and keep `bands/passport.toml` and `transport/device.toml` at their sibling paths. Substitute the environment path that resolves the pinned Core checkout. [e171 Core tree](https://github.com/Afonenko-QCL-NEGF/QCLNEGF.jl/tree/e171caa60cce676c6c4238dd671e7c527f2bd977)

```sh
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
julia --startup-file=no --threads=1 --heap-size-hint=280M --project=/path/to/pinned-environment bands/native.jl
julia --startup-file=no --threads=1 --heap-size-hint=280M --project=/path/to/pinned-environment cell-basis/verify.jl
python cell-basis/holdout.py
python cell-basis/window_weight.py
```

`summary.csv` covers the scanned ranks and geometries. `holdout.json`, generated by the scripts and excluded from this compact package, records the individual energies and overlaps. `window_weight.json` records the upper and lower spectral tails. `verification.toml`, also regenerated locally and excluded here, records the Julia checks and the basis columns consumed by the independent Python implementation hold-out. The scalar-only `verification-summary.toml` has a digest of that complete evidence. For an exploratory transport build, call `CellBlochPOD.build_problem` with `train_bands=5, max_principal_angle=0.25`, and record `built.training.provenance` with the model fingerprint. Native solver options retain their existing registry values. The actual basis identity comes from the constructed model.
