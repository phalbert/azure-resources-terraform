# Configure the providers
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
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  backend "s3" {
    bucket = "cognition-bucket"
    key    = "tfstate"
    region = "eu-west-1"
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

provider "aws" {
  region = "eu-west-1"
}

