# Example only: both inputs are already pinned and independently reviewed.
{ qcl, productionSite }:
let
  # The reviewed site's outputs function must accept this exact qcl input.
  production = (import (productionSite + "/flake.nix")).outputs { inherit qcl; };
in
(import (qcl.outPath + "/nix/restore-site.nix")) {
  inherit production;
  platform = qcl.inputs.platform;
  productionSite = import (productionSite + "/site.nix");
  target = {
    vm_id = 122;
    address = "192.0.2.22";
    mac = "52:54:00:00:00:22";
  };
  stateGiB = 16;
  # Enable only for a separately admitted fresh VM and blank state disk.
  initializeBlankStateDisk = false;
}
