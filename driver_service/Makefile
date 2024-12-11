# Variables
APP_NAME := driver-service
SRC_DIR := ./cmd
SWAGGER_DIR := ./api

# Commands
GO := go
SWAGGER := swag

# Targets
.PHONY: all build run swagger-init swagger-gen swagger-serve clean

# Default target
all: build

# Build the application
build:
	@echo "Building $(APP_NAME)..."
	$(GO) build -o $(APP_NAME) $(SRC_DIR)/main.go

# Run the application
run: build
	@echo "Running $(APP_NAME)..."
	./$(APP_NAME)

# Initialize Swagger setup
swagger-init:
	@echo "Initializing Swagger..."
	$(SWAGGER) init -o $(SWAGGER_DIR) -g $(SRC_DIR)/main.go --parseDependency
	$(SWAGGER) fmt


