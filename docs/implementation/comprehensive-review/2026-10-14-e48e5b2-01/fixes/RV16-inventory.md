# RV16-P1 · Статический inventory

Источник: S из `../source-receipt.json`; root Git HEAD плюс frozen overlay. Не второй revision lock. Перечень derived из Git ls-files, root overlay заменяет одноимённые bytes; campaign outputs исключены. Локальные generated outputs учтены отдельно, вне Git denominator.

Markdown включает `.md/.rst/.qmd/.ipynb`; config — `.toml/.yaml/.yml/.json/.jsonc/.nix/.tf/.tfvars`; исключаются filenames с `lock` в имени (case-insensitive), но native `julia/Manifest.toml` и Core `Manifest.toml` сохраняются; fixtures включены отдельным count. Эти lexical counts не означают publicness или semantic coverage. Диаграммы: `.svg/.mmd/.mermaid/.dot`.

| Сегмент | Документы | Diagrams | Config все / test+fixtures | Docs build outputs/bytes |
|---|---:|---:|---:|---:|
| root | 68 | 0 | 18 / 1 | 0 / 0 |
| QCLNEGF.jl | 36 | 14 | 5 / 1 | 0 / 0 |
| QCLNEGFRunner.jl | 11 | 0 | 56 / 43 | 20 / 2591034 |
| qcl-negf-aiida | 5 | 0 | 2 / 1 | 0 / 0 |
| qcl-negf-contracts | 2 | 0 | 19 / 0 | 0 / 0 |
| qcl-negf-platform | 22 | 0 | 60 / 12 | 0 / 0 |
| qcl-negf-portal | 3 | 0 | 6 / 0 | 0 / 0 |
| qcl-negf-research | 6 | 0 | 22 / 0 | 0 / 0 |
| qcl-negf-results | 3 | 0 | 2 / 1 | 0 / 0 |

Повторная проверка component git status выполняется перед freeze candidate. Generated Runner directory: 20 файлов, 8 HTML, `objects.inv`, `search_index.js`, 10 assets; source/build receipt неизвестен. Root/Core/прочие `docs/build` отсутствуют в этих checkout; это не утверждение об отсутствии внешней публикации.

Entry/public surface map и роли находятся в `../RV16.md`; глубина semantic review ограничена выбранным срезом.

## root

Base `./`; source commit root S + receipt overlay.

Docs `.agents/skills/qcl-performance-audit/`: `SKILL.md`.
Docs `.agents/skills/qcl-performance-audit/references/`: `telemetry.md`.
Docs `.agents/skills/qcl-physics-audit/`: `SKILL.md`.
Docs `.agents/skills/qcl-physics-audit/references/`: `physics-checks.md`.
Docs `.agents/skills/qcl-research-framing/`: `SKILL.md`.
Docs `.agents/skills/qcl-research-framing/references/`: `brief.md`.
Docs `.agents/skills/qcl-results-analysis/`: `SKILL.md`.
Docs `.agents/skills/qcl-results-analysis/references/`: `comparison.md`.
Docs `./`: `AGENTS.md`, `CONTRIBUTING.md`, `README.md`, `TODO.md`.
Docs `docs/`: `architecture.md`, `local-lab-packages.md`, `organization-transfer.md`, `publication.md`, `research-workflow.md`, `single-server-deployment.md`, `source-graph-environment.md`.
Docs `docs/implementation/`: `comprehensive-review-source-audit-2026-10-14.md`, `core-scba-optical-scope.md`, `cr01-exact-artifact-locator.md`, `cr02-durable-shutdown-intent.md`, `cr03-enrolled-node-identity.md`, `cr03-root-enrollment-caller.md`, `cr04-bounded-delivery.md`, `cr05-solver-profile-recovery.md`, `cr06-voltage-certificates.md`, `cr07-generated-origins.md`, `d05-native-host-storage-preparation.md`, `gap07-saved-comparison.md`, `local-kvm-lab-validation.md`, `r09-recovery-declaration-conflicts.md`, `recovery-cd-local-validation.md`, `s01-equilibrium-source-entry.md`, `s01-local-operator-oracles.md`, `s01-stored-equilibrium-diagnostics.md`, `s06-bound-branch-reasons.md`, `s09-transport-analysis-defaults.md`, `storage-budget-transition.md`.
Docs `docs/implementation/evidence/cr05-2026-10-09/`: `publication-audit.md`, `review.md`.
Docs `docs/implementation/evidence/recovery-cd-2026-10-03/`: `README.md`.
Docs `docs/superpowers/plans/`: `2026-10-03-local-kvm-lab.md`, `2026-10-03-recovery-cd-implementation.md`, `2026-10-06-overnight-deployment-hardening.md`.
Docs `docs/superpowers/specs/`: `2026-10-03-local-kvm-lab.md`.
Docs `docs/system/`: `README.md`, `agent-review-workflow.md`, `architecture.md`, `autonomous-review-docs-skills.md`, `autonomous-review-engineering.md`, `autonomous-review-formal-science.md`, `autonomous-review-plan.md`, `comprehensive-review.md`, `documentation-methodology.md`, `feasibility.md`, `implementation-entrypoint.md`, `physics-documentation.md`, `rebuild.md`, `release-roadmap.md`, `requirements.md`, `results-and-postprocessing.md`, `review-metrics.md`, `review.md`, `scientific-milestone.md`, `skills-and-instructions-review.md`.
Docs `examples/restore-site/`: `README.md`.
Config denominator list SHA256 `da69ebaed84126e99860aab9e68689d40318171fe833677c172adf30ceb0881b`; N=18. Воспроизводимый список: `git -C BASE ls-files`, suffix/filter выше. Сохраняется source-relative path order sorted; SHA — hash списка, не hash contents.

## QCLNEGF.jl

Base `components/QCLNEGF.jl/`; source commit 3108150dd1b6b1377470b384b15c26e272fe5c5d.

Docs `./`: `CONTRIBUTING.md`, `README.md`.
Docs `docs/src/api/`: `operators.md`, `public.md`.
Docs `docs/src/developer/`: `architecture.md`, `physics_operators.md`, `traceability.md`.
Docs `docs/src/`: `glossary.md`, `index.md`, `references.md`, `references_optimization.md`.
Docs `docs/src/physics/`: `models.md`, `numerical-policy.md`.
Docs `docs/src/theory/`: `01_model.md`, `02_reference2019.md`, `03_arrays.md`, `04_scaling.md`, `05_basis.md`, `06_periodicity.md`, `07_greens.md`, `08_kernels.md`, `09_scba.md`, `10_poisson.md`, `11_observables.md`, `12_validation.md`, `13_visualization.md`, `14_cost.md`, `15_limitations.md`, `16_input_contract.md`, `17_implementation_plan.md`, `18_optical_response.md`, `19_production.md`, `20_optimization_decision_tree.md`.
Docs `docs/src/tutorials/`: `localization.md`, `physical-atlas.md`.
Docs `docs/src/user/`: `convergence.md`.
Diagrams `docs/src/assets/diagrams/`: `nested_solver.svg`, `production_parallelism.svg`.
Diagrams `docs/src/assets/physics/`: `band_dispersion.svg`, `basis_localization.svg`, `basis_operators.svg`, `coherence_current.svg`, `hartree_response.svg`, `localization_metrics.svg`, `optical_response.svg`, `reference2019_structure.svg`, `scattering_factors.svg`, `scba_fixed_point.svg`, `spectral_population.svg`.
Diagrams `docs/src/assets/`: `scba_flow.svg`.
Config denominator list SHA256 `6ba0efdc5f0b62c4b2da93dd1bd4d4dca0005de9ac28035ca2a07dd886c82334`; N=5. Воспроизводимый список: `git -C BASE ls-files`, suffix/filter выше. Сохраняется source-relative path order sorted; SHA — hash списка, не hash contents.

## QCLNEGFRunner.jl

Base `components/QCLNEGFRunner.jl/`; source commit 0c53c6d0f68e0b25fce79388db831da6fc3ae856.

Docs `./`: `CONTRIBUTING.md`, `README.md`.
Docs `docs/`: `local-lab-acceptance.md`.
Docs `docs/src/api/`: `public.md`.
Docs `docs/src/developer/`: `architecture.md`.
Docs `docs/src/`: `index.md`.
Docs `docs/src/user/`: `comparison.md`, `configuration.md`, `plotting.md`, `resources.md`, `results.md`.
Config denominator list SHA256 `5c57b840e2e459a9d49aac618dd6fb83a2176edfd5ee1375acff2d236a3f1401`; N=56. Воспроизводимый список: `git -C BASE ls-files`, suffix/filter выше. Сохраняется source-relative path order sorted; SHA — hash списка, не hash contents.

## qcl-negf-aiida

Base `components/qcl-negf-aiida/`; source commit 69aa1309c8465a838e4778b9dff464a306229f01.

Docs `./`: `CONTRIBUTING.md`, `README.md`.
Docs `docs/`: `deployment.md`, `service.md`.
Docs `tests/`: `TRANSPORT_ACCEPTANCE.md`.
Config denominator list SHA256 `2eee1c7c26e1821eeb5f5af966f2577e15124744ab0e0ea7be7669c8e4d63049`; N=2. Воспроизводимый список: `git -C BASE ls-files`, suffix/filter выше. Сохраняется source-relative path order sorted; SHA — hash списка, не hash contents.

## qcl-negf-contracts

Base `components/qcl-negf-contracts/`; source commit 923e0c6cd9cbbe63bd1fb9c77892ef171385ed76.

Docs `./`: `CONTRIBUTING.md`, `README.md`.
Config denominator list SHA256 `7ab3eb11063fc6b20a5129ee126333ceec40f4e4f81076281871c88721a0ffc2`; N=19. Воспроизводимый список: `git -C BASE ls-files`, suffix/filter выше. Сохраняется source-relative path order sorted; SHA — hash списка, не hash contents.

## qcl-negf-platform

Base `components/qcl-negf-platform/`; source commit 4ce214e29b72276157b10a9267e2f30fef4ac66f.

Docs `./`: `CONTRIBUTING.md`, `README.md`.
Docs `docs/`: `application-cd.md`, `application.md`, `bootstrap.md`, `build-admission.md`, `github-registration.md`, `host-network.md`, `host-storage.md`, `image-transfer.md`, `infrastructure.md`, `local-lab-orchestration.md`, `local-lab.md`, `monitoring.md`, `nginx-preflight.md`, `operations.md`, `runner-routing.md`, `slurm-maintenance.md`, `staged-python.md`, `state-archive.md`, `status-journal.md`, `windows-workers.md`.
Config denominator list SHA256 `ef56318435ac74666cb2c3794acb524c5a4e06625d4018e3c76ffd8ce7943519`; N=60. Воспроизводимый список: `git -C BASE ls-files`, suffix/filter выше. Сохраняется source-relative path order sorted; SHA — hash списка, не hash contents.

## qcl-negf-portal

Base `components/qcl-negf-portal/`; source commit 10b6c871bb89cce4f2bdc1c4cdaa91e500111ceb.

Docs `./`: `AGENTS.md`, `CONTRIBUTING.md`, `README.md`.
Config denominator list SHA256 `9604018566b5821188aa85f592ecbce9fa7dce5039fc96125b53194c9dd40ddf`; N=6. Воспроизводимый список: `git -C BASE ls-files`, suffix/filter выше. Сохраняется source-relative path order sorted; SHA — hash списка, не hash contents.

## qcl-negf-research

Base `components/qcl-negf-research/`; source commit 5458212063a41051328ef8b5d14d63d5ac7dc781.

Docs `./`: `CONTRIBUTING.md`, `README.md`.
Docs `docs/`: `equilibrium-s01.md`, `fresh-fixtures-2026-10-03.md`, `scientific-inputs.md`.
Docs `literature/`: `README.md`.
Config denominator list SHA256 `811280310fbde2244335bdacdd66f1e8f0e6fed5ab795171cb9e32fa476b7457`; N=22. Воспроизводимый список: `git -C BASE ls-files`, suffix/filter выше. Сохраняется source-relative path order sorted; SHA — hash списка, не hash contents.

## qcl-negf-results

Base `components/qcl-negf-results/`; source commit fe27a2a9ed065f9afacecc84113311f30d0c68d6.

Docs `./`: `CONTRIBUTING.md`, `README.md`.
Docs `docs/`: `export-budget.md`.
Config denominator list SHA256 `41a77b29ff3fc88b18d495d810c354e59c3559521632ec5e6d22d7f5f7d1e07f`; N=2. Воспроизводимый список: `git -C BASE ls-files`, suffix/filter выше. Сохраняется source-relative path order sorted; SHA — hash списка, не hash contents.

