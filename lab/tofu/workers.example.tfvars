# Copy to a private *.auto.tfvars; replace node/template/VM IDs after live inventory.
# Templates must have scsi0, VirtIO drivers, QGA and cloud-init/Cloudbase-Init ready.
admin_public_keys = ["ssh-ed25519 REPLACE_WITH_EXISTING_PUBLIC_KEY"]
workers = {
  "qcl-linux-01" = {
    os           = "ubuntu"
    node         = "pve-example"
    vm_id        = 720
    template_id  = 9200
    cores        = 8
    memory_mib   = 16384
    root_storage = "local-lvm"
    data_storage = "data-lvm"
    data_gib     = 128
  }
  "qcl-windows-01" = {
    os           = "windows"
    node         = "pve-example"
    vm_id        = 721
    template_id  = 9201
    cores        = 4
    memory_mib   = 8192
    root_gib     = 80
    root_storage = "local-lvm"
    admin_user   = "qcladmin"
  }
}
# windows_admin_passwords belongs in a private variable file or TF_VAR_*.
