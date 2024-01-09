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
  default     = "demo"
}

variable "port_run_id" {
  type        = string
  description = "The runID of the action run that created the entity"
}

variable "port_client_id" {
  type        = string
  description = "The Port client ID"
}

variable "port_client_secret" {
  type        = string
  description = "The Port client secret"
}

variable "az_subscription_id" {
  type        = string
  description = "The Azure subscription ID"
}

variable "az_client_id" {
  type        = string
  description = "The Azure client Id"
}

variable "az_client_secret" {
  type        = string
  description = "The Azure client Secret"
}

variable "az_tenant_id" {
  type        = string
  description = "The Azure tenant id"
}