terraform {
  backend "local" {}
  required_providers {
    proxmox = { source = "bpg/proxmox" }
  }
}

# Endpoint and credentials use the provider's native PROXMOX_VE_* environment.
provider "proxmox" {}

# Templates contain only the OS, guest agent and initial administrative access.
# Linux: cloud-init. Windows: sysprep + Cloudbase-Init (configdrive2).
resource "proxmox_virtual_environment_vm" "worker" {
  for_each = var.workers

  node_name     = each.value.node
  vm_id         = each.value.vm_id
  name          = each.key
  description   = each.value.description
  tags          = each.value.tags == null ? ["qcl", "tofu", each.value.os] : each.value.tags
  on_boot       = true
  started       = true
  scsi_hardware = each.value.scsi_hardware

  dynamic "clone" {
    for_each = each.value.template_id == null ? [] : [each.value.template_id]
    content {
      vm_id        = clone.value
      node_name    = each.value.template_node
      datastore_id = each.value.root_storage
      full         = true
    }
  }
  agent { enabled = true }
  cpu {
    cores = each.value.cores
    type  = each.value.cpu_type
  }
  memory {
    dedicated = each.value.memory_mib
    floating  = 0
  }
  network_device {
    bridge      = each.value.bridge
    model       = "virtio"
    mac_address = each.value.mac_address
    vlan_id     = each.value.vlan_id
  }
  disk {
    datastore_id = each.value.root_storage
    interface    = "scsi0"
    size         = each.value.root_gib
  }
  dynamic "disk" {
    for_each = each.value.data_gib == null ? [] : [each.value.data_gib]
    content {
      datastore_id = each.value.data_storage
      interface    = "scsi1"
      size         = disk.value
      serial       = coalesce(each.value.data_serial, "qcl-data-${each.value.vm_id}")
    }
  }

  operating_system {
    type = each.value.operating_system_type == null ? (each.value.os == "windows" ? "win11" : "l26") : each.value.operating_system_type
  }
  dynamic "serial_device" {
    for_each = each.value.serial_devices
    content {
      device = serial_device.value
    }
  }
  initialization {
    datastore_id = each.value.root_storage
    ip_config {
      ipv4 {
        address = each.value.ipv4
        gateway = each.value.gateway
      }
    }
    user_data_file_id = each.value.user_data_file_id
    dynamic "user_account" {
      for_each = (each.value.configure_admin_account == null ? each.value.user_data_file_id == null : each.value.configure_admin_account) ? [each.value.admin_user] : []
      content {
        username = user_account.value
        keys     = each.value.os == "ubuntu" ? var.admin_public_keys : null
        password = each.value.os == "windows" ? var.windows_admin_passwords[each.key] : null
      }
    }
  }
}

output "workers" {
  value = {
    for name, worker in proxmox_virtual_environment_vm.worker : name => {
      vm_id = worker.vm_id
      node  = worker.node_name
      os    = var.workers[name].os
      ipv4  = worker.ipv4_addresses
    }
  }
}
