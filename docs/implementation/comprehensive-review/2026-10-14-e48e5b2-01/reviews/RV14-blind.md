# RV14 · Blind closure review

Candidate RV14/fixes ещё не читались. Denominator задан coordinator: 8 links (Git→selected; source→Julia workspace; standalone→Core; depot→solver build; source/lock→frontend derivation; source→wheels; closures→release manifest; wheel payload→HTTP). S/dirty hashes receipt; static only, no build/import/test/network installation.

## Восемь звеньев

1. Root ops/git.ts::sourceGraph checks exact HEAD gitlinks, child HEAD/clean state, orphan/nested rejection. Git authority separate native dependency locks. Package version0.2.0 insufficient commit proof.
2. Root ops/environment.ts::lock calls Runner tools/prepare_workspace.jl with Core/Runner source paths; tool Pkg.develop relative paths; julia/Manifest.toml binds workspace local source. No Julia execution; lock freshness/derivation receipt not inferred.
3. Runner Project.toml [sources] Core URL rev v0.2.0 and compat =0.2.0 vs workspace local paths. Standalone and workspace can select different Core contents with same package version; exact source/tree resolution must be measured separately.
4. ops/solver.ts::buildSolver requires depot receipt source revision, validates URI/hash, prefetches local file artifact with stable name, builds source Git URI rev through nix/solver.nix→mkPreparedDepot/mkSolver. Native derivation/test contract receipt not regenerated. New root commit cannot inherit old full CI/release acceptance.
5. Portal nix/frontend.nix binds frontend source filtered node_modules/dist, npmDepsHash, nodejs24; Vite output transformed to dist, installed into derivation. Platform nix/application.nix copies frontend result into static. Source/lock declared, bitwise reproducibility unknown.
6. ops/release.ts calls sourceGraph, frontendBuild, locked uv build, four wheels names/sha256 and verifies sourceGraph remains unchanged. Native wheel hook only checks static index file and any assets/*.js presence. Existing stale compiled payload passes this presence check; independent generated-content/source mapping needed for direct wheel build.
7. ops/application_cd.ts::deploymentManifest validates immutable Nix store paths+narHash and records source graph/application/solver closures; producer evidence from nix path-info. Semantic full runtime/installed state not proven by manifest identity alone.
8. Portal pyproject wheel artifacts static/**→api.py conditional StaticFiles mount(root). Existing payload source identity is not established merely by package version, hook pass or mount path. Native import distribution version check does not prove imported source hash.

## Oracle и ограничения

Negative cases: stale static/index.html and assets/stale.js should be refused by a source-binding strengthened hook, but current initialize only presence; 0.2.0 compiled/imported from another commit is possible under version-only checks. Current release frontendBuild reduces stale risk on that route; direct wheel path remains distinct. Need explicit build provenance input or rebuild hook whose imports/effects are bounded, plus canonical checks and returned asset hashes. Two independent builds of same declared derivation and byte diff are separate future scope, M07 not_measured. Runtime consumer self-check/fixtures are future bounded M08; no full release CI rerun implied. Source pipeline/receipt/readability/physics gates separate.
