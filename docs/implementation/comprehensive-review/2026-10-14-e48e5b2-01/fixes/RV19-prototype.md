# RV19 — future bounded static prototype

Status needs_version_and_authorization. Owner Portal/docs + Root dependencies; inputs S Portal source and revised docstrings if chosen. Current REVIEW executes nothing.

Candidate: Griffe static AST, inspection disabled, no extensions/external alias resolution. Read-only prerequisites: installed executable/Python/version/hash/lock and generator config; selected uv.lock lookup does not establish Griffe pin. Missing runtime → needs_environment, no install fallback.

Conditional exact command after pinned version/cap accepted:

```text
python3 -m griffe dump qcl_negf_api --search /home/tolya/Загрузки/qcl-negf/components/qcl-negf-portal/src --no-inspection --no-resolve-external --output /tmp/qcl-rv19-prototype/api.json
```

Official [CLI](https://mkdocstrings.github.io/griffe/reference/cli/) supports flags today; chosen version must support them before READY. Generator own imports/AST processing are future bounded action; target package never imported/inspected. No lifespan/app creation/network/private settings/server/solver/tests. Preserve raw JSON/errors and environment receipt.

Proposed future envelope, not grant: 1 invocation, <=1 CPU/1 GiB, <=5 min wall, <=8 MiB JSON, <=32 KiB shown log; stop missing source/pin, inspection fallback, cap/unauthorized effect, preserve partial. Oracle: source signatures/docstrings/create_app/raw route decorators. Route effects remain authored, AST does not prove OpenAPI/dynamic runtime aliases.

Separate existing Julia candidate: Julia1.13.0/Documenter1.17.0 selected sources, `julia --project=julia components/QCLNEGFRunner.jl/docs/make.jl`. It imports/compiles/runs doctests/examples: separate docs-build stage/finite budget/effect inventory, not static prototype. Never reuse old HTML as source-build receipt.

Acceptance: facts conserved, assigning/default distinction visible, no target imports, stable source links/hash. Renderer/version/offline/light passed to RV18; runtime/source compatibility remains separate.
