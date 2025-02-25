terraform {
  # State storage configuration
  backend "gcs" {
    bucket = "mycelium-terraform-state"
    prefix = "env/dev"
  }
} 