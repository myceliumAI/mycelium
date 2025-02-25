# Resource naming and tagging configuration
locals {
  environment = "dev"
  project     = "mycelium"
  
  common_labels = {
    environment = local.environment
    project     = local.project
    managed_by  = "terraform"
  }
  
  name_prefix = "${local.project}-${local.environment}"
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# Network infrastructure
module "vpc" {
  source     = "../../modules/vpc"
  project_id = var.project_id
  region     = var.region
  name       = "${local.name_prefix}-network"
  labels     = local.common_labels
}

# Database infrastructure
module "cloud_sql" {
  source           = "../../modules/cloud-sql"
  project_id       = var.project_id
  region           = var.region
  name             = "${local.name_prefix}-db"
  network_id       = module.vpc.network_id
  database_version = "POSTGRES_17"
  db_name          = "mycelium_db"
  db_user         = "mycelium"
  vpc_connection   = module.vpc.private_vpc_connection
  labels          = local.common_labels
}

# Secret management
resource "random_password" "keycloak_admin_password" {
  length  = 16
  special = true
}

resource "random_password" "postgres_password" {
  length  = 16
  special = true
}

# Service deployments
module "api_service" {
  source     = "../../modules/cloud-run"
  project_id = var.project_id
  region     = var.region
  name       = "mycelium-api-service"
  image      = "myceliumai/api:latest"
  
  # Add Cloud SQL connection
  cloudsql_connections = [module.cloud_sql.connection_name]
  
  environment_variables = {
    # Service configuration
    API_PORT = "8000"
    
    # Database connectivity
    POSTGRES_HOST     = "/cloudsql/${module.cloud_sql.connection_name}"
    POSTGRES_PORT     = "5432"
    POSTGRES_USER     = module.cloud_sql.db_user
    POSTGRES_DB       = "mycelium_db"
    POSTGRES_PASSWORD = random_password.postgres_password.result
    POSTGRES_SOCKET   = "/cloudsql/${module.cloud_sql.connection_name}/.s.PGSQL.5432"
  }
  labels = local.common_labels
}

module "auth_service" {
  source     = "../../modules/cloud-run"
  project_id = var.project_id
  region     = var.region
  name       = "mycelium-auth-service"
  image      = "myceliumai/keycloak:latest"
  
  # Add Cloud SQL connection
  cloudsql_connections = [module.cloud_sql.connection_name]
  
  environment_variables = {
    # Keycloak Server Configuration
    KC_PORT                    = "8081"
    KC_MANAGEMENT_PORT         = "9000"
    KC_REALM                   = "mycelium"
    KC_BOOTSTRAP_ADMIN_USERNAME = "admin"
    KC_BOOTSTRAP_ADMIN_PASSWORD = random_password.keycloak_admin_password.result
    
    # Database Configuration via Cloud SQL Proxy
    POSTGRES_USER              = module.cloud_sql.db_user
    POSTGRES_DB               = "mycelium_db"
    POSTGRES_PORT             = "5432"
    POSTGRES_HOST             = "/cloudsql/${module.cloud_sql.connection_name}"
    
    # Keycloak Client Configuration
    KC_CLIENT_ID              = "mycelium-client"
    KC_DB_PASSWORD           = random_password.postgres_password.result
    
    # Optional Google Authentication
    KC_GOOGLE_CLIENT_ID      = var.google_client_id
    KC_GOOGLE_CLIENT_SECRET  = var.google_client_secret
  }
  labels = local.common_labels
}

module "frontend_service" {
  source     = "../../modules/cloud-run"
  project_id = var.project_id
  region     = var.region
  name       = "mycelium-frontend-service"
  image      = "myceliumai/frontend:latest"
  
  environment_variables = {
    # API Configuration
    API_HOST        = "mycelium-api-service"
    API_PORT        = "8000"
    
    # Keycloak Configuration
    KC_HOST         = "mycelium-auth-service"
    KC_PORT         = "8081"
    KC_REALM        = "mycelium"
    KC_CLIENT_ID    = "mycelium-client"
    
    # Frontend Configuration
    PORT            = "8080"
    FRONTEND_HOST   = "0.0.0.0"
    FRONTEND_PORT   = "8080"
  }
  labels = local.common_labels
} 