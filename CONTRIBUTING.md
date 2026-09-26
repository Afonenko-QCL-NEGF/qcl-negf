# Contributing

Change the component that owns the behavior. Keep numerical formulas and scientific acceptance
criteria reviewable independently of orchestration and deployment. Add tests for a changed contract
or failure mode; do not copy the implementation into its tests.

Use a feature branch in each modified submodule. Publish those commits before updating their
gitlinks in this superproject. Native package managers generate environment locks; source revisions
are already recorded by Git. Run `deno task prepare`, `deno task check` and the relevant
`deno task test` group, followed by the full integration pipeline before a release.

Do not commit VM images, Python environments, Julia depots, credentials, private inventories or
scientific output. Cite literature data at its source and retain physical units and uncertainty.
Review contributed code before executing it on an infrastructure-connected self-hosted runner.
