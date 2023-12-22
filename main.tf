# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {
  client_id       =   var.client_id
  client_secret   =   var.client_secret
  subscription_id =   var.subscription_id
  tenant_id       =   var.tenant_id
  
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = "westus2"
}

resource "azurerm_storage_account" "storage_account" {
  name                = var.storage_account_name
  resource_group_name = var.resource_group_name

  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
}