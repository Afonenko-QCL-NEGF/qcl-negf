# Public role-closure API for a captured local development snapshot.
# Site JSON contains public configuration only; runtime secrets stay outside Nix.
{ inputFile, siteFile }:
let
  input = builtins.fromJSON (builtins.readFile inputFile);
  project = builtins.getFlake input.source;
  site = builtins.fromJSON (builtins.readFile siteFile);
  application = import ./local-lab-packages.nix { inherit inputFile; package = "application"; };
  solver = import ./local-lab-packages.nix { inherit inputFile; package = "solver"; };
  lab = project.inputs.platform.lib.mkLocalLab {
    site = site // { inherit application solver; };
  };
in
# Validate both packages even when a caller selects only the storage role.
builtins.seq application.drvPath (builtins.seq solver.drvPath {
  inherit (lab) systems;
  inherit application solver;
})
