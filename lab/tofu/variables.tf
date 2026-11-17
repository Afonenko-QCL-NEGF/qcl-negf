variable "admin_public_keys" {
  description = "Existing public SSH keys for Ubuntu; private keys stay outside state/config."
  type        = list(string)
  default     = []
}

variable "windows_admin_passwords" {
  description = "Private per-VM Cloudbase-Init bootstrap passwords; protect local state."
  type        = map(string)
  sensitive   = true
  default     = {}
}

variable "workers" {
  description = "Owned VM instances. Template IDs and storage are selected per PVE node."
  type = map(object({
    os                      = string
    node                    = string
    vm_id                   = number
    description             = optional(string, "QCL worker managed by OpenTofu; guest configuration by Ansible")
    tags                    = optional(list(string))
    scsi_hardware           = optional(string, "virtio-scsi-pci")
    operating_system_type   = optional(string)
    serial_devices          = optional(list(string), [])
    configure_admin_account = optional(bool)
    template_id             = optional(number)
    template_node           = optional(string)
    cores                   = optional(number, 4)
    cpu_type                = optional(string, "x86-64-v2-AES")
    memory_mib              = optional(number, 8192)
    root_storage            = string
    root_gib                = optional(number, 64)
    data_storage            = optional(string)
    data_gib                = optional(number)
    data_serial             = optional(string)
    user_data_file_id       = optional(string)
    bridge                  = optional(string, "vmbr0")
    vlan_id                 = optional(number)
    mac_address             = optional(string)
    ipv4                    = optional(string, "dhcp")
    gateway                 = optional(string)
    admin_user              = optional(string, "qcladmin")
  }))
  default = {}
  validation {
    condition     = alltrue([for w in values(var.workers) : contains(["ubuntu", "windows"], w.os)])
    error_message = "Worker OS must be ubuntu or windows."
  }
  validation {
    condition     = alltrue([for w in values(var.workers) : w.data_gib == null || w.data_storage != null])
    error_message = "An extra data disk needs an explicit storage."
  }
}
