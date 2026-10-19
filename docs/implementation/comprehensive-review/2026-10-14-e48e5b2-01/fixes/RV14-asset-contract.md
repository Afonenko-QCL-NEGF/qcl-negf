# RV14-1 — standalone Portal asset contract

Disposition: READY discovery/design, implementation not authorized.
Trigger: direct wheel hook verifies presence, source freshness unknown.
Owner Portal; source `10b6c871bb89cce4f2bdc1c4cdaa91e500111ceb`.
Permitted future paths: hatch_build.py, frontend build config, README, selected packaging fixture.
Invariant: same wheel/API/browser compatibility, always light theme; no change physics/contracts.
Minimal design: declare supported source→frontend→wheel workflow, then choose reproducible
source stamp or mandatory generation guard using native locks, not maintained second SHA lock.
Independent oracle/negative: old index.html+JS beside changed frontend input must either cause
explicit rebuild/rejection or be excluded by the documented supported path; fresh output accepted.
Root release.ts and Nix frontend derivation remain separate positive controls.
Checks now: static compare hook, root frontendBuild and Nix cleanSource (performed in RV14).
Future executable check proposal: one fresh and one stale fixture, <=2 attempts, 1CPU/1GiB,
5min aggregate wall, <=4MiB temp output; no dependency install/network. Not a current grant.
If available environment/build cost exceeds envelope stop and redesign budget.
Dependencies: supported packaging route decision; migration/docs owning component PR if authorized.
Closure: owner picks invariant, fixture differentiates stale source, reviewer validates docs/build
semantics. Actual build acceptance remains a separate claim.
