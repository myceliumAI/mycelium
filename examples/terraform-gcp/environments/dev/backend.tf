terraform {
  required_version = ">= 1.0.0"
  
  # State storage configuration
  backend "gcs" {
    bucket = "mycelium-terraform-state"
    prefix = "env/dev"
    workspace_prefix = "mycelium-"
  }

  # Provider requirements
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
} 