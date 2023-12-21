variable "subscription_id" {
  type        = string
  default     = "XXXXXX-1111-2222-3333-YYYYYYYYYY"
  description = "Subscription ID in Azure"
}

variable "tenant_id" {
  type        = string
  default     = "XXXXXXX-1111-2222-3333-YYYYYYYYY"
  description = "Tenant ID in Azure"
}

variable "resource_group_name" {
  type        = string
  default     = "DefaultResources"
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
