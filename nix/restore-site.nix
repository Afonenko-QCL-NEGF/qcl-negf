# A caller supplies one already evaluated, reviewed production composition.
# Fetching, resource admission, signatures and provider state remain external.
{
  production,
  platform,
  productionSite,
  target,
  system ? "x86_64-linux",
  stateGiB ? 16,
  prefixLength ? 24,
  initializeBlankStateDisk ? false,
  resourcePrefix ? "qcl-negf-restore",
}:
let
  inventory = production.deploymentInventory;
  controller = production.nixosConfigurations.control;
  original = controller.config;
  imageFields = [ "image_path" "image_file_id" "image_sha256" "image_bytes" ];
  restoredVm = builtins.removeAttrs inventory.vms.control imageFields // {
    vcpus = 2;
    memory_mib = 4096;
    root_gib = 32;
  } // target // {
    address = "${target.address}/${toString prefixLength}";
    started = false;
    on_boot = false;
  };
  restore = controller.extendModules {
    modules = [ ({ config, lib, ... }:
      let
        maskedNames = [
          "qcl-negf-bootstrap"
          "qcl-negf-aiida"
          "qcl-negf-api"
          "slurmctld"
          "slurmd"
          "munged"
          "nginx"
          "site-runtime-secrets"
          "site-ci-registration"
        ] ++ map (lib.removeSuffix ".service") config.qclNegf.runtimeSecretUnits;
      in {
        networking.hostName = lib.mkForce original.networking.hostName;
        networking.interfaces.${original.qclNegf.privateInterface}.ipv4.addresses =
          lib.mkForce [{ address = target.address; inherit prefixLength; }];
        networking.hosts = {
          "${productionSite.addresses.control}" = lib.mkForce [];
          "${target.address}" = lib.mkForce [ original.networking.hostName ];
        };
        services.cloud-init.settings.preserve_hostname = lib.mkForce true;

        # Only an explicitly admitted fresh, blank state disk may be formatted.
        qclNegf.stateDisk.initializeBlankDisk = lib.mkForce initializeBlankStateDisk;
        systemd.services = lib.genAttrs maskedNames (_: {
          enable = lib.mkForce false;
          wantedBy = lib.mkForce [];
          requiredBy = lib.mkForce [];
        });
        fileSystems.${config.qclNegf.cluster.jobDirectory}.options =
          lib.mkForce [ "noauto" "_netdev" ];
        environment.systemPackages = [
          config.qclNegf.application.package
          config.qclNegf.cluster.solverPackage
        ];
        assertions = [
          {
            assertion = config.qclNegf.uid == 3000
              && config.qclNegf.cluster.controller
              && !config.qclNegf.cluster.worker
              && config.qclNegf.application.enable
              && config.qclNegf.application.profile == "qcl-negf"
              && config.qclNegf.stateDisk.enable
              && config.qclNegf.stateArchive.enable
              && config.qclNegf.stateDisk.device == original.qclNegf.stateDisk.device;
            message = "Restore must preserve the UID3000 controller and separate stable state disk.";
          }
          {
            assertion = config.services.postgresql.enable
              && config.services.postgresql.package.psqlSchema == "17"
              && lib.elem "qcl-negf" config.services.postgresql.ensureDatabases;
            message = "Restore requires the owning PostgreSQL17 qcl-negf database; runtime restoration additionally requires an empty database.";
          }
          {
            assertion = config.qclNegf.cluster.solverPackage != null
              && config.qclNegf.release.applicationPackage != null
              && toString config.qclNegf.application.package
                == toString original.qclNegf.application.package
              && toString config.qclNegf.cluster.solverPackage
                == toString original.qclNegf.cluster.solverPackage
              && toString config.qclNegf.release.applicationPackage
                == toString config.qclNegf.application.package;
            message = "Restore must inherit the exact production application and solver closures.";
          }
        ];
      }) ];
  };
  images = platform.lib.mkImages { configurations = { control-restore = restore; }; };
in
assert builtins.all (name: builtins.elem name [
  "vm_id" "address" "mac" "vcpus" "memory_mib" "root_gib" "started" "on_boot"
]) (builtins.attrNames target);
assert builtins.isInt target.vm_id && target.vm_id > 0;
assert builtins.all (vm: target.vm_id != vm.vm_id && target.mac != vm.mac)
  (builtins.attrValues inventory.vms);
assert builtins.all (address: target.address != address)
  (builtins.attrValues productionSite.addresses);
assert builtins.all (vm: !(vm ? address)
  || target.address != builtins.head (builtins.split "/" vm.address))
  (builtins.attrValues inventory.vms);
assert !(target.started or false) && !(target.on_boot or false);
assert stateGiB > 0 && restoredVm.vcpus > 0 && restoredVm.memory_mib > 0
  && restoredVm.root_gib > 0;
assert prefixLength >= 0 && prefixLength <= 32;
{
  nixosConfigurations.control-restore = restore;
  packages.${system}.control-restore-image = images.control-restore;
  deploymentInventory = inventory // {
    build_profile = null;
    resource_prefix = resourcePrefix;
    controller_state_gib = stateGiB;
    vms = { control-restore = restoredVm; };
  };
}
