# Pure constructor fixtures: no nixpkgs, flake fetching, store queries or builds.
let
  lib = rec {
    mkForce = value: value;
    elem = builtins.elem;
    removeSuffix = suffix: value:
      let n = builtins.stringLength value; m = builtins.stringLength suffix;
      in if n >= m && builtins.substring (n - m) m value == suffix
         then builtins.substring 0 (n - m) value else value;
    genAttrs = names: f: builtins.listToAttrs (map (name: { inherit name; value = f name; }) names);
  };
  config = {
    networking.hostName = "control";
    qclNegf = {
      uid = 3000;
      privateInterface = "cluster0";
      runtimeSecretUnits = [ "custom-secret.service" ];
      application = { enable = true; profile = "qcl-negf"; package = "/immutable/application"; };
      cluster = { controller = true; worker = false; jobDirectory = "/jobs"; solverPackage = "/immutable/solver"; };
      release.applicationPackage = "/immutable/application";
      stateDisk = { enable = true; device = "/dev/disk/by-id/virtio-qcl-state"; };
      stateArchive.enable = true;
    };
    services.postgresql = { enable = true; package.psqlSchema = "17"; ensureDatabases = [ "qcl-negf" ]; };
  };
  makeProduction = cfg: {
    nixosConfigurations.control = {
      config = cfg;
      extendModules = { modules }: { module = (builtins.head modules) { config = cfg; inherit lib; }; };
    };
    deploymentInventory = {
      controller_state_gib = 64;
      vms = {
        control = { vm_id = 112; vcpus = 8; memory_mib = 16000; root_gib = 64; mac = "unused"; address = "192.0.2.12/24"; image_path = "/old/image"; image_sha256 = "old-image"; image_bytes = 1000; };
        compute = { vm_id = 113; mac = "worker-mac"; address = "192.0.2.13/24"; };
      };
    };
  };
  production = makeProduction config;
  platform.lib.mkImages = { configurations }: { control-restore = "image-of-exact-extended-control"; };
  args = {
    inherit production platform;
    productionSite.addresses = { control = "192.0.2.12"; storage = "192.0.2.10"; };
    target = { vm_id = 122; address = "192.0.2.22"; mac = "52:54:00:00:00:22"; };
  };
  constructor = import ../nix/restore-site.nix;
  result = constructor args;
  module = result.nixosConfigurations.control-restore.module;
  formatted = constructor (args // { initializeBlankStateDisk = true; });
  changedSolver = constructor (args // { production = makeProduction (config // {
    qclNegf = config.qclNegf // { cluster = config.qclNegf.cluster // { solverPackage = null; }; };
  }); });
  rejects = value: !(builtins.tryEval (builtins.deepSeq value true)).success;
  allAssertions = m: builtins.all (a: a.assertion) m.assertions;
in
assert allAssertions module;
assert !allAssertions changedSolver.nixosConfigurations.control-restore.module;
assert module.qclNegf.stateDisk.initializeBlankDisk == false;
assert formatted.nixosConfigurations.control-restore.module.qclNegf.stateDisk.initializeBlankDisk == true;
assert module.networking.interfaces.cluster0.ipv4.addresses == [{ address = "192.0.2.22"; prefixLength = 24; }];
assert module.networking.hosts."192.0.2.12" == [];
assert module.systemd.services.custom-secret == { enable = false; wantedBy = []; requiredBy = []; };
assert builtins.length (builtins.attrNames module.systemd.services) == 10;
assert module.fileSystems."/jobs".options == [ "noauto" "_netdev" ];
assert module.environment.systemPackages == [ "/immutable/application" "/immutable/solver" ];
assert result.packages.x86_64-linux.control-restore-image == "image-of-exact-extended-control";
assert result.deploymentInventory.controller_state_gib == 16;
assert builtins.attrNames result.deploymentInventory.vms == [ "control-restore" ];
assert result.deploymentInventory.vms.control-restore.vcpus == 2;
assert result.deploymentInventory.vms.control-restore.memory_mib == 4096;
assert result.deploymentInventory.vms.control-restore.root_gib == 32;
assert result.deploymentInventory.vms.control-restore.started == false;
assert result.deploymentInventory.vms.control-restore.on_boot == false;
assert !(result.deploymentInventory.vms.control-restore ? image_path);
assert !(result.deploymentInventory.vms.control-restore ? image_sha256);
assert !(result.deploymentInventory.vms.control-restore ? image_bytes);
assert rejects (constructor (args // { target = args.target // { vm_id = 112; }; }));
assert rejects (constructor (args // { target = args.target // { vm_id = 113; }; }));
assert rejects (constructor (args // { target = args.target // { mac = "worker-mac"; }; }));
assert rejects (constructor (args // { target = args.target // { address = "192.0.2.12"; }; }));
assert rejects (constructor (args // { target = args.target // { address = "192.0.2.10"; }; }));
assert rejects (constructor (args // { target = args.target // { address = "192.0.2.13"; }; }));
assert rejects (constructor (args // { target = args.target // { image_path = "/unverified"; }; }));
assert rejects (constructor (args // { target = args.target // { started = true; }; }));
assert rejects (constructor (args // { stateGiB = 0; }));
{ passed = true; scope = "pure-injected-constructor; runtime/image/science not measured"; }
