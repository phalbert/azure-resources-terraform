# Makefile for Pulumi Commands

# Set your Pulumi stack name
PULUMI_STACK=arete

# Set the Pulumi project directory
PULUMI_PROJECT_DIR=./ts

.PHONY: init
init:
	@echo "Initializing Pulumi project..."
	pulumi stack init $(PULUMI_STACK) --cwd $(PULUMI_PROJECT_DIR)

.PHONY: set-stack
set-stack:
	@read -p "Enter the stack name: " STACK_NAME; \
	pulumi stack select phalbert/port-resources/$$STACK_NAME --cwd $(PULUMI_PROJECT_DIR)

.PHONY: preview
preview:
	@echo "preview Pulumi stack..."
	pulumi preview --cwd $(PULUMI_PROJECT_DIR)

.PHONY: up
up:
	@echo "Deploying Pulumi stack..."
	pulumi up --cwd $(PULUMI_PROJECT_DIR)

.PHONY: destroy
destroy:
	@echo "Destroying Pulumi stack..."
	pulumi destroy --cwd $(PULUMI_PROJECT_DIR)

.PHONY: stack-output
stack-output:
	@echo "Fetching stack outputs..."
	pulumi stack output --json --cwd $(PULUMI_PROJECT_DIR)

.PHONY: destroy-and-clean
destroy-and-clean: destroy
	@echo "Cleaning up Pulumi stack files..."
	rm -rf $(PULUMI_PROJECT_DIR)/.pulumi

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  init            - Initialize Pulumi project"
	@echo "  up              - Deploy Pulumi stack"
	@echo "  destroy         - Destroy Pulumi stack"
	@echo "  stack-output    - Fetch stack outputs"
	@echo "  destroy-and-clean - Destroy stack and clean up Pulumi files"
