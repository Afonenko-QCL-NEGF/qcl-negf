# Local build entry point; all data is parsed as JSON, never interpolated Nix code.
{ source, depotManifestJson, depotManifestSha256, system ? "x86_64-linux",
  juliaTestProfile ? "production-build", juliaTestWorkerLimit ? null }:
assert builtins.isString depotManifestJson && builtins.isString depotManifestSha256;
assert builtins.hashString "sha256" depotManifestJson == depotManifestSha256;
let
  project = builtins.getFlake source;
  metadata = builtins.fromJSON depotManifestJson;
  preparedDepot = project.lib.mkPreparedDepot { inherit system metadata juliaTestProfile juliaTestWorkerLimit; };
in
project.lib.mkSolver { inherit system preparedDepot juliaTestProfile juliaTestWorkerLimit; }
