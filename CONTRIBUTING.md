# Contributing

Use one developer loop: edit the owning component, select checks from the actual impact, review and
publish its PR, then update its published gitlink here and run the integration or native checks
needed for that composition. Gitlinks record source revisions; do not maintain another manual source
lock. Keep formulas and scientific acceptance in their owners, independent of orchestration and UI.

| Class | Purpose               | Typical evidence                                                                                                                                         |
| ----- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D     | Documentation         | Changed text, formatting, links and anchors; no Julia, install or docs build for docs-only changes.                                                      |
| L     | Local behaviour       | Relevant contract fixtures and failure cases in the available environment.                                                                               |
| N     | Native integration    | Actual package, service or backend checks for affected composition.                                                                                      |
| S     | Scientific experiment | Separately commissioned experiment with frozen model, plan and criteria; report process, convergence, physics, discretization and validation separately. |

Choose checks for changed paths and dependencies; unknown impact requires the corresponding full
check. Existing commands and their prerequisites are documented by their owners. Do not bootstrap
implicitly as part of a cheap check. Full CI checks release composition or broad changes; repeat
when source or a failure warrants it, not for every PR by default. A source audit alone does not
establish runtime behaviour. The latest applicable user instruction and explicit scope govern
authorized checks; do not ask again for actions already authorized. Explicit task limits remain in
force.

Use a feature branch in each modified submodule and publish its commits before updating gitlinks.
Keep unrelated changes and foreign resources intact; do not commit VM images, environments, depots,
credentials, private inventories or scientific output. Cite literature at source and retain units
and uncertainty. Review contributed code before executing it on infrastructure-connected self-hosted
runners.
