variable "project_id" {
  description = "The GCP project ID"
  type        = string
  
  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{4,28}[a-z0-9]$", var.project_id))
    error_message = "Project ID must be between 6 and 30 characters, start with a letter, and contain only lowercase letters, numbers, and hyphens."
  }
}

variable "region" {
  description = "The GCP region where resources will be created"
  type        = string
  
  validation {
    condition     = can(regex("^[a-z]+-[a-z]+-[0-9]$", var.region))
    error_message = "Region must be in the format: xxxxx-xxxxx-#, like europe-west1."
  }
}

variable "google_client_id" {
  description = "Google OAuth client ID for Keycloak"
  type        = string
  default     = ""
}

variable "google_client_secret" {
  description = "Google OAuth client secret for Keycloak"
  type        = string
  default     = ""
} 