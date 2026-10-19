# RV08 — finite remaining sections, predeclared properties/caps

Immutable Core S `3108150dd1b6b1377470b384b15c26e272fe5c5d`; root overlay receipt.
Это продолжение source review, не разрешение execute/import/test.
Каждая строка — отдельный atomic packet: denominator=1 symbol/3 properties,
cap≤20 min включая независимый review (author≤12min, review≤8min),
≤1CPU/1GiB; extracts≤96KiB; section≤8KiB. При missing input/cap — partial.
Все properties объявлены до дальнейшего чтения symbols, numerical verdict
`not_measured`. Documentation locators — owning traceability EQ/PROD IDs.

| Section/symbol | Property 1 | Property 2 | Property 3 / applicability |
|---|---|---|---|
| R01 build_bdd_hamiltonian | BDD sign/units | harmonic face normalization | Hermiticity + interface flux, uniform grid |
| R02 build_localized_basis | PzP localization | Löwdin orthonormality | finite subspace/rank gate |
| R03 project_hamiltonians | projected H dimensions | χ/Φ metric normalization | Hermitian U/mass projection |
| R04 build_shift_matrix | energy sign + zero exterior | interpolation moments | fractional/weighted-adjoint limit |
| R05 embedding_self_energy | field-periodic cavity equation | lesser/greater pair | coherent finite-chain limit |
| R06 number_functional | spin/sign/units | energy/k quadrature | real/positive target limit |
| R07 normalize_lesser | λ definition | sheet number target | legacy Pauli failure limit |
| R08 impurity_kernel | Coulomb screened prefactor | donor/angle/qz quadrature | covariance PSD, finite qs |
| R09 interface_roughness_kernel | interface vertex units/sign | correlated covariance norm | sharp-interface limit |
| R10 acoustic_kernel | elastic/high-T prefactor | spatial/basis contraction | PSD + elastic balance |
| R11 alloy_kernel | disorder variance units | well/barrier spatial mask | x=0/1 no disorder |
| R12 _static_contraction | four-index orientation | wk/qK normalization | scalar/literal map |
| R13 _lo_contraction | opposite shifts | Bose/wk/qK normalization | thermal KMS |
| R14 direct_hilbert_transform | PV sign/2π | energy weights/diagonal | finite-window analytic transform |
| R15 retarded_self_energy | Γ identity | Hermitian Λ/anti-Hermitian pair | causal scalar broadening |
| R16 electron_density | χ reconstruction/sign/units | wEwkgs/(2π) | integrated sheet number/coherences |
| R17 sheet_density_matrix | number trace/sign/units | phase-space weights | Hermitian/PSD population |
| R18 effective_levels | static diagnostic eigenproblem | dipole normalization | U=0 no dynamic Σ claim |
| R19 collision_balance | signed integral | absolute event normalization | elastic number/energy vs LO |
| R20 power_balance | work-field sign/units | energy moment normalization | zero-drive thermal limit |
| R21 validate_problem | physical input/shape consistency | kernel/shift normalization | invalid-input negative disposition |
| R22 validate_solution | coupled final algebra | metric/applicability/near-zero | missing measurement fails |
| P01 PROD-SHIFT-001 | same noncyclic shifts | explicit weights/moments | literal integer/fractional pair |
| P02 PROD-CONTRACT-001 | same tensor indices | exact wk/qK factors | independent literal, all backends |
| P03 PROD-HILBERT-001 | same finite PV sum | FFT padding/diagonal/weights | independent analytic window |
| P04 PROD-SEED-001 | Lorentzian/number target | scalar qe/wk units | analytic 2D Fermi density |
| P05 PROD-RESIDUAL-001 | same raw metric definitions | floor/weights | literal negative candidate, deterministic reduction |
| P06 PROD-SCBA-001 | Jacobi raw candidate | stored-state/buffer ownership | independent scalar fixed point |

Source denominator: initial6 + reference22 + production6 =34 packets.
Не объединять counterpart с reference в один pass; общие kernels не oracle.
