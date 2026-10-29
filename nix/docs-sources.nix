# Documentation adds owning recipes/pages to the unchanged runtime projections.
{ lib, root }:
let
  select = base: names: lib.fileset.toSource {
    root = base;
    fileset = lib.fileset.unions (map (name: base + "/${name}") names);
  };
in {
  runtime = import ./runtime-sources.nix { inherit lib root; };
  core = select (root + "/components/QCLNEGF.jl") [ "docs/make.jl" "docs/Project.toml" "docs/src" ];
  runner = select (root + "/components/QCLNEGFRunner.jl") [ "docs/make.jl" "docs/Project.toml" "docs/src" ];
  contracts = select (root + "/components/qcl-negf-contracts") [ "src" "pyproject.toml" "LICENSE" ];
  presentation = select root [
    "ops/docs/produce.py" "ops/docs/assemble.py" "ops/docs/runtime-assets.py"
    "ops/docs/math-render.mjs" "ops/docs/assets.lock.json" "ops/docs/pilot-plan.json"
    "docs/public/make.jl" "docs/public/operator-recovery.md"
    "docs/capture-runtime-delivery.md" "docs/solver-build-receipt.md"
  ];
}
