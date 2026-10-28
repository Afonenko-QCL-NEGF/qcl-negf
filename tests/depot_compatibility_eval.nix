# Source-only: mock Julia store identity, actual checked-out native metadata.
let
  helper = import ../nix/depot-compatibility.nix;
  julia = { drvPath = "/nix/store/11111111111111111111111111111111-julia.drv";
            outPath = "/nix/store/22222222222222222222222222222222-julia"; };
  inputs = helper.inputs { root = ../.; inherit julia; system = "x86_64-linux";
    juliaTestProfile = "production-build"; juliaTestWorkerLimit = 2; };
  sha = builtins.hashString "sha256" (builtins.toJSON inputs);
  m = {format="qcl-negf.julia-depot.v2";sources={format="qcl-negf.git-graph.v1";revision="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";components=[{path="components/Core";revision="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb";url="https://github.com/example/core";}];};julia="1.13.0";
    juliaManifest=builtins.hashFile "sha256" ../julia/Manifest.toml;
    url="https://example.invalid/depot.tar";hash="sha256-AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=";
    compatibility={schema="qcl-negf.julia-depot-compatibility.v1"; inherit inputs;
      inputs_sha256=sha;native={schema="qcl-negf.julia-depot-native.v1";inputs_sha256=sha;
        julia_drv=julia.drvPath;julia_output=julia.outPath;observed_platform="x86_64-linux-gnu";
        preferences_sha256=builtins.hashString "sha256" "prefs";
        selector_closure_sha256=builtins.hashString "sha256" "selectors";
        artifact_selection_sha256=builtins.hashString "sha256" "artifacts";
        receipt_sha256=builtins.hashString "sha256" "receipt";};};};
in assert inputs.julia.test_workers == 2;
assert helper.valid {metadata=m;expected=inputs;manifest=m.juliaManifest;};
assert !helper.valid {metadata=m // {compatibility=m.compatibility // {extra=true;};};expected=inputs;manifest=m.juliaManifest;};
assert !helper.valid {metadata=m;expected=inputs // {system="other";};manifest=m.juliaManifest;};
{ inherit inputs sha; }
