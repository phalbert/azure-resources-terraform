resource "azurerm_storage_account" "storage_account" {
  name                = "{{ storage_name }}"
  resource_group_name = var.resource_group_name

  location                 = "{{ storage_location }}"
  account_tier             = "Standard"
  account_replication_type = "LRS"
  account_kind             = "StorageV2"
}