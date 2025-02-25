terraform {
  required_version = ">= 1.0.0"
  
  backend "gcs" {
    bucket = "mycelium-terraform-state"
    prefix = "dev"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
} 