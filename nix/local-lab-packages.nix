# Local development build API. Input JSON is derived from lab:snapshot evidence.
# Production ops/git.ts and ops/solver.ts keep their GitHub-only source guard.
{ inputFile, package ? "solver" }:
let
  input = builtins.fromJSON (builtins.readFile inputFile);
  project = builtins.getFlake input.source;
  application = project.lib.mkApplication { system = "x86_64-linux"; };
  metadata = builtins.fromJSON (builtins.readFile input.depotManifest);
  manifestHash = builtins.hashFile "sha256" (project.outPath + "/julia/Manifest.toml");
  preparedDepot = project.lib.mkPreparedDepot { system = "x86_64-linux"; inherit metadata; juliaTestProfile = "local-debug"; };
in
assert builtins.elem package [ "application" "solver" ];
assert project.rev == input.snapshotRevision;
assert input.sourceGraph.revision == project.rev;
if package == "application" then
  application
else
  assert metadata.format == "qcl-negf.julia-depot.v2" || metadata.sources == input.sourceGraph;
  assert metadata.juliaManifest == manifestHash;
  assert input.preparedManifestSha256 == manifestHash;
  project.lib.mkSolver {
    system = "x86_64-linux";
    inherit preparedDepot;
    juliaTestProfile = "local-debug";
  }
