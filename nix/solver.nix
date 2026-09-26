# Local build entry point; all data is parsed as JSON, never interpolated Nix code.
{ source, depotManifest, system ? "x86_64-linux" }:
let
  project = builtins.getFlake source;
  metadata = builtins.fromJSON (builtins.readFile depotManifest);
  preparedDepot = project.lib.mkPreparedDepot { inherit system metadata; };
in
project.lib.mkSolver { inherit system preparedDepot; }
