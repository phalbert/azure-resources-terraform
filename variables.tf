# Service Principal Variables

variable "client_id" {
    description =   "Client ID (APP ID) of the application"
    default     = "XXXXXX-1111-2222-3333-YYYYYYYYYY"
    type        =   string
}

variable "client_secret" {
    description =   "Client Secret (Password) of the application"
    default     = "XXXXXX-1111-2222-3333-YYYYYYYYYY"
    type        =   string
}

variable "subscription_id" {
    description =   "Subscription ID"
    default     = "XXXXXX-1111-2222-3333-YYYYYYYYYY"
    type        =   string
}

variable "tenant_id" {
    description =   "Tenant ID"
    default     = "XXXXXX-1111-2222-3333-YYYYYYYYYY"
    type        =   string
}

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
