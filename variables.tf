variable "resource_group_name" {
  type        = string
  default     = "myTFResourceGroup"
  description = "RG name in Azure"
}

variable "location" {
  type        = string
  default     = "westus2"
  description = "RG location in Azure"
}

variable "storage_account_name" {
  type        = string
  description = "Storage Account name in Azure"
}
