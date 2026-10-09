# S01: independent diagnostics of saved equilibrium artifacts

The Results component adds `diagnose_stored_equilibrium` with explicit identity,
I/O, numeric workspace and report limits. Mandatory commit SHA and native-state
verification remain in place. The diagnostic measures a common Fermi–Dirac
chemical potential, weighted charge, Green-state FDR, stored Keldysh residuals,
separate occupied/empty correction norms and outward boundary currents.

Results owns these independent observations of saved arrays. It does not rerun
the Core nonlinear map or select scientific tolerances. Empty charge remains a
measured quantity; donor-target residuals apply only to occupied charge. Undefined
ratios and unavailable measurements have explicit statuses and JSON null values.

The selected source is the published Results gitlink. Owning source PR:
[Results #4](https://github.com/Afonenko-QCL-NEGF/qcl-negf-results/pull/4).
Independent source review identified an empty-charge residual applicability
error; its repair was reviewed on the final source.

| Claim | Evidence | Limitation | Decision |
| --- | --- | --- | --- |
| Diagnostic algebra and guards have bounded regression coverage | Final 36 manufactured cases pass, including independent matrix and weighted oracles | Synthetic finite-domain arrays | Keep for saved-data analysis |
| Existing StateReader behavior remains compatible | All 37 cases in the existing StateReader test file pass on the selected source | Synthetic fixtures; not a whole repository suite | Keep |
| Execution stayed within finite local packets | Four diagnostic calls and one compatibility call; failed attempts retained | These packets do not cover deployment or native solver execution | Keep evidence separate |
| S01 scientific acceptance is established | No production equilibrium artifact was generated in these packets | SCBA/Poisson attempts: zero | Insufficient data; execute the separate accepted scientific plan |

Publication checks covered the four owning changed paths: `git diff --check`,
independent review, and a scan of 1,432 added lines for credential patterns,
network addresses and four sensitive literals from the external configuration.
The scan found no matches; it cannot prove absence of unknown secrets by itself.
