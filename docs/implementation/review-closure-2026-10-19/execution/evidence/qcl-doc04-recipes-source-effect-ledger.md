# DOC04 recipes: frozen source-effect ledger

2026-10-20. Ledger for source-only design, **not an import admission manifest**.
No Julia/Documenter/Deno/package parser/import/build/test was executed.

## Immutable scope

Root observed HEAD `d4113f43cddf02d46025434eb3a9dd8e110e90d6`.
Core selected `e431609f4f5ca6d21225aaf5b18aaf7b50f0c7ee`;
Runner selected `1acc165650fd4f4c2d49605cc679f90e3f6fcdae`.
Root `julia/Project.toml` and `Manifest.toml` resolve those packages by local paths,
Julia1.13.0 and Documenter1.17.0 UUID
`e30172f5-a6a5-5a46-863b-614d45cd2de4`, expected tree
`56e9c37b5e7c3b4f080ab1da18d72d5c290e184a`.
The installed Documenter tree's complete checksum/cache/native identity is unknown.

Pilot plan SHA256
`cde7ee8b4e19878eeda8e92b4cfe6167b105dd3440409da351c0039e600e9e50`.
Operator authored bytes SHA256
`8f05ff4cced8579b09cccd4b4315101e861e1896b87321b42e597374da79de49`.
These hashes are observations of frozen inputs, not a parallel component lock.

## Selected page scope

Core normal navigation,34 Markdown pages:

```text
index.md
user/convergence.md
api/operators.md
api/public.md
theory/01_model.md
theory/02_reference2019.md
theory/03_arrays.md
theory/04_scaling.md
theory/05_basis.md
theory/06_periodicity.md
theory/07_greens.md
theory/08_kernels.md
theory/09_scba.md
theory/10_poisson.md
theory/11_observables.md
theory/12_validation.md
theory/13_visualization.md
theory/14_cost.md
theory/15_limitations.md
theory/16_input_contract.md
theory/17_implementation_plan.md
theory/18_optical_response.md
theory/19_production.md
theory/20_optimization_decision_tree.md
physics/models.md
physics/numerical-policy.md
tutorials/localization.md
tutorials/physical-atlas.md
developer/architecture.md
developer/physics_operators.md
developer/traceability.md
glossary.md
references.md
references_optimization.md
```

Core also has `development/review_oracle_contracts.md` outside that navigation.
Pinned Documenter default `pagesonly=false` means its bytes/directives cannot be
silently excluded from the effect inventory. Keep this extra page in staged input
and inventory it; do not reduce support closure or change existing defaults.
Core docs/src contains35 Markdown files plus static assets/data. Static figures
and CSV are existing authored illustration support, not new measured arrays or
an instruction to regenerate them. Public asset review remains necessary.

Runner navigation,8 Markdown pages:

```text
index.md
user/comparison.md
user/configuration.md
user/plotting.md
user/resources.md
user/results.md
api/public.md
developer/architecture.md
```

Operator has frozen authored chapter mapped byte-exact to staged `recovery.md`,
and a small fixed generated index whose literal text is owned by the root recipe.
Do not copy deployment/execution/private directories into this source tree.

## Directive observations and remaining review

The bounded discovery command was a text grep for triple-backtick directive
starts, `DocTestSetup`, `@meta`, `@docs`, `@autodocs` across selected `docs/src`
and `src`. It returned no fenced `@setup`, `@example`, `@eval`, `@repl` or
`jldoctest`, and no `@autodocs`. This is a negative text observation, not a
complete Markdown/docstring parse or permission to execute changed inputs.

| Class | Exact observed locations | State before render |
| --- | --- | --- |
| Core `@meta` | First line of api/operators,api/public; developer/physics_operators,developer/traceability; glossary,references_optimization; theory01–13 and15–20; tutorials/localization,tutorials/physical-atlas; user/convergence (28 locations) | Bodies must be bound/reviewed individually; do not assume arbitrary assignment is harmless |
| Core `@docs` | api/operators:24,42,71,105; api/public:9,103,132,185 | 8 blocks: enumerate exact expressions/docstrings and signatures before import/render |
| Runner `@meta` | api/public:1 | Body must be hash-bound and reviewed |
| Runner `@docs` | api/public:22,93,191,214,220,229 | 6 blocks: enumerate exact expressions/docstrings before render |
| Operator | One `text` fenced CLI syntax; explicit named headings | Frozen chapter manually reviewed; no executable directive |
| `@setup/@example/@eval/@repl/jldoctest` | No match in the described grep scope | Observed zero; remaining fence forms/nested docstring expansion must be reviewed, not inferred |
| Other executable/embedded forms | `@raw`, tilde/long fences, indented/nested/quoted blocks and dynamically produced docstrings not comprehensively classified by this scan | Unknown; fixed-input review must close or refuse before render |

Pinned Documenter `src/expander_pipeline.jl` witnesses:
selectors280–290 separate Meta/Docs/Eval/Example/REPL/Setup;
Meta338–352 evaluates assignment RHS with `Core.eval(Main,...)`;
Docs460 evaluates signature expressions;
Eval713–734, Example837–879, REPL946–978 and Setup1024–1038
execute independently of doctest and are only skipped by draft branches.
Pilot remains `draft=false`; do not substitute draft placeholders for content.
`doctest=false` is insufficient to authorize these effects.

## Package/import edges

| Edge | Observed effect / source witness | Admission state |
| --- | --- | --- |
| Existing Core recipe | `using QCLNEGF, Documenter`; recursive DocMeta DocTestSetup; makedocs(doctest=true,checkdocs=:exports,warnonly=false) | Default stays unchanged; pilot has separate branch |
| Existing Runner recipe | Same pattern for QCLNEGFRunner | Same; standalone docs/Project pins old Corev0.2.0 and must not select pilot environment |
| Core module entry | Exact Julia version guard; using LinearAlgebra,Logging,SHA,FFTW,Unitful,Roots; includes domain/reference/optimized/composition files | Entry/include list observed, complete top-level evaluation closure not reviewed |
| Core precompile include | `src/QCLNEGF.jl:1182` includes composition/precompile_workload.jl | Included edge confirmed |
| Core workload | PrecompileTools @setup_workload/@compile_workload constructs tutorial no-scattering problem, Hamiltonian, small retarded Green and spectral function; no explicit SCBA/Poisson solve call in this file | Package-image work is not free; matching prepared cache/admission needed; dependency effects unknown |
| Runner module entry | imports Core API, FFTW,Unitful,YAML; persistence/HDF5,telemetry,presentation/configuration/composition includes; scratch_execution and cli included | Complete top-level/transitive closure not reviewed |
| Runner `__init__` | Lines884–887 assigns DEFAULT_CONFIGURATION_SCHEMA via default_configuration_schema() | Resource path initialization known; called accessor/transitive effects need binding |
| Runner workload file | Same named source file exists; selected entrypoint has no include of it | Not an observed import edge; never count existence as execution |
| Documenter | Dependency list includes Downloads,Git,Pkg,PrecompileTools,CodecZlib, etc.; @meta/@docs evaluation paths above | No install/deploydocs/prerender/linkcheck requested; complete dependency/cache effects still unknown |
| Native/transitive libraries | HDF5/FFTW/Unitful/Roots/PrecompileTools/Documenter closure and package extensions | Unknown until reviewed manifest + admitted matching cache/toolchain evidence |

Do not describe a partial include/import audit as `reviewed`. Each include/init/
workload/docstring edge needs exact owner/revision/path/hash/effect/reason/evidence.
Missing or changed edge blocks its corresponding render, before the owning
package is imported by the pilot process. Runtime isolation and caps add evidence;
they do not turn an unknown effect into a reviewed one.

## Budget/discovery limitation

A late `git ls-tree -rl` census found Core `src`+`docs/src` totals4,431,653 bytes
and112 files; Runner totals1,092,109 bytes and67 files. The earlier grep scope
included static docs assets/data and was broader than the required Markdown scan.
Its conservative logical scan breadth therefore exceeds the4MiB source-read
envelope; this was reported to coordinator and all further target-source reads
stopped. Git's actual decompressed/physical reads were not instrumented.
This limitation is preserved instead of claiming a completed full effect audit.
The medium I source stage must finish the precise Markdown/docstring ledger in
its own granted budget; no BUILD readiness follows from this packet.

STOP: ledger is factual observations + explicit unknown gates, no import approval.
