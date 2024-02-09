variable "resource_group_name" {
  type        = string
  default     = "arete-resources"
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
  default     = "fortizo"
}

variable "port_run_id" {
  type        = string
  description = "The runID of the action run that created the entity"
  default     = ""
}

variable "port_client_id" {
  type        = string
  description = "The Port client ID"
}

variable "port_client_secret" {
  type        = string
  description = "The Port client secret"
}

variable "conditional_property" {
  type        = string
  description = "A conditional property"
  default     = ""
}

variable "resource_tags" {
  type = any
  default = {
    Environment = "Production"
    Department  = "Finance"
  }
}
