# Local development build API. Input JSON is derived from lab:snapshot evidence.
# Production ops/git.ts and ops/solver.ts keep their GitHub-only source guard.
{ inputFile, package ? "solver" }:
let
  input = builtins.fromJSON (builtins.readFile inputFile);
  project = builtins.getFlake input.source;
  pkgs = project.inputs.platform.inputs.nixpkgs.legacyPackages.x86_64-linux;
  application = project.lib.mkApplication { system = "x86_64-linux"; };
  fixture = project.outPath + "/components/qcl-negf-aiida/tests/transport_fixture.py";
  synthetic = pkgs.writeShellScriptBin "qcl-negf-synthetic-transport-1" ''
    # SYNTHETIC transport fixture only; this is not a physical solver.
    exec ${application}/bin/python ${fixture} "$@"
  '';
  metadata = builtins.fromJSON (builtins.readFile input.depotManifest);
  manifestHash = builtins.hashFile "sha256" (project.outPath + "/julia/Manifest.toml");
  preparedDepot = project.lib.mkPreparedDepot { system = "x86_64-linux"; inherit metadata; };
in
assert builtins.elem package [ "application" "solver" "synthetic" ];
assert project.rev == input.snapshotRevision;
assert input.sourceGraph.revision == project.rev;
if package == "application" then
  application
else if package == "synthetic" then
  assert builtins.pathExists fixture;
  synthetic
else
  assert metadata.sources == input.sourceGraph;
  assert metadata.juliaManifest == manifestHash;
  assert input.preparedManifestSha256 == manifestHash;
  project.lib.mkSolver {
    system = "x86_64-linux";
    inherit preparedDepot;
    juliaTestProfile = "local-debug";
  }
