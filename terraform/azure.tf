resource "azurerm_storage_account" "storage_account" {
  name                = var.storage_account_name
  resource_group_name = var.resource_group_name

  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
  tags                     = var.resource_tags
}


resource "port_entity" "azure_storage_account" {
  count      = length(azurerm_storage_account.storage_account) > 0 ? 1 : 0
  identifier = var.storage_account_name
  title      = var.storage_account_name
  blueprint  = "azureStorage"
  run_id     = var.port_run_id
  properties = {
    string_props = {
      "storage_name"     = var.storage_account_name,
      "storage_location" = var.location,
      "endpoint"         = azurerm_storage_account.storage_account.primary_web_endpoint
    }
  }

  depends_on = [azurerm_storage_account.storage_account]
}
