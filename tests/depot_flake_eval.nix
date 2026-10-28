# Exact Root flake helpers; synthetic native qualification, no realization.
{ nixpkgs }:
let
  pkgs=import (/. + nixpkgs) {system="x86_64-linux";};
  platform.inputs.nixpkgs.legacyPackages.x86_64-linux=pkgs;
  out=(import ../flake.nix).outputs {inherit platform self;};
  self=out // {rev="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";outPath=../.;lib=out.lib // {
    mkApplication= _: {captureRuntime="/nix/store/11111111111111111111111111111111-capture";};};};
  system="x86_64-linux";
  inputs=self.lib.depotCompatibilityInputs {inherit system;juliaTestWorkerLimit=2;};
  policy=import ../nix/depot-compatibility.nix;
  sha=policy.hash inputs;
  m={format="qcl-negf.julia-depot.v2";sources={format="qcl-negf.git-graph.v1";
    revision="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";components=[{path="components/Core";
      revision="cccccccccccccccccccccccccccccccccccccccc";url="https://github.com/example/core";}];};
    julia="1.13.0";juliaManifest=builtins.hashFile "sha256" ../julia/Manifest.toml;
    url="https://example.invalid/depot.tar";hash="sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
    compatibility={schema="qcl-negf.julia-depot-compatibility.v1";inherit inputs;inputs_sha256=sha;
      native={schema="qcl-negf.julia-depot-native.v1";inputs_sha256=sha;julia_drv=inputs.julia.drv;
        julia_output=inputs.julia.output;observed_platform="x86_64-linux-gnu";
        preferences_sha256=builtins.hashString "sha256" "prefs";
        selector_closure_sha256=builtins.hashString "sha256" "selectors";
        artifact_selection_sha256=builtins.hashString "sha256" "artifacts";
        receipt_sha256=builtins.hashString "sha256" "synthetic receipt";};};};
  a=self.lib.mkPreparedDepot {inherit system;metadata=m;juliaTestWorkerLimit=2;};
  b=self.lib.mkPreparedDepot {inherit system;juliaTestWorkerLimit=2;metadata=m // {
    sources=m.sources // {revision="dddddddddddddddddddddddddddddddddddddddd";};
    compatibility=m.compatibility // {native=m.compatibility.native // {receipt_sha256=builtins.hashString "sha256" "different synthetic evidence";};};};};
  runtime=p: self.lib.mkSolver {inherit system;preparedDepot=p;juliaTestWorkerLimit=2;};
  bad=builtins.tryEval ((self.lib.mkSolver {inherit system;preparedDepot=a;juliaTestWorkerLimit=4;}).drvPath);
in assert a.drvPath==b.drvPath;
assert (runtime a).drvPath==(runtime b).drvPath;
assert !bad.success;
{julia_drv=inputs.julia.drv;depot_drv=a.drvPath;runtime_drv=(runtime a).drvPath;metadata_outside_drv=true;wrong_factory_rejected=true;}
