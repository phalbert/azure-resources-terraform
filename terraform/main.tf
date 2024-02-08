# Configure the Azure provider
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0.2"
    }
    port = {
      source  = "port-labs/port-labs"
      version = "~> 1.10.0"
    }
  }

  required_version = ">= 1.1.0"
}

provider "azurerm" {

  features {}
}

provider "port" {
  client_id = var.port_client_id     # or set the env var PORT_CLIENT_ID
  secret    = var.port_client_secret # or set the env var PORT_CLIENT_SECRET
}

# resource "azurerm_storage_account" "storage_account" {
#   name                = var.storage_account_name
#   resource_group_name = var.resource_group_name

#   location                 = var.location
#   account_tier             = "Standard"
#   account_replication_type = "LRS"
#   account_kind             = "StorageV2"
# }

# resource "port_entity" "azure_storage_account" {
#   count      = length(azurerm_storage_account.storage_account) > 0 ? 1 : 0
#   identifier = var.storage_account_name
#   title      = var.storage_account_name
#   blueprint  = "azureStorage"
#   run_id     = var.port_run_id
#   properties = {
#     string_props = {
#       "storage_name"     = var.storage_account_name,
#       "storage_location" = var.location,
#       "endpoint"         = azurerm_storage_account.storage_account.primary_web_endpoint
#     }
#   }

#   depends_on = [azurerm_storage_account.storage_account]
# }


resource "port_action" "sample_action" {
  title      = "Sample Action"
  icon       = "Terraform"
  identifier = "sample-action"
  blueprint  = "service"
  trigger    = "DAY-2"
  webhook_method = {
    type = "WEBHOOK"
    url  = "https://app.getport.io"
  }
  user_properties = {
    string_props = {
      alwaysRequiredInput = {
      }
      inputRequiredBasedOnData = {
        
      }
      "webhook_url" = {
        title       = "Webhook URL"
        description = "Webhook URL to send the request to"
        format      = "url"
        default     = "https://example.com"
        pattern     = "^https://.*"
      }
    }
  }
  required_jq_query = "if .entity.properties.conditionBooleanProperty then [\"alwaysRequiredInput\", \"inputRequiredBasedOnData\"] else [\"alwaysRequiredInput\"] end"
}

resource "port_action" "my_action" {
  title = "My Action"
  identifier = "my-action"
  blueprint = "service"
  trigger = "CREATE"
  kafka_method = {}
  user_properties = {
    "string_props" = {
      "alwaysRequiredInput" = {}
      "inputRequiredBasedOnData" = {}
    }
  }
  required_jq_query = "if .entity.properties.conditionBooleanProperty then [\"alwaysRequiredInput\", \"inputRequiredBasedOnData\"] else [\"alwaysRequiredInput\"] end"
}
