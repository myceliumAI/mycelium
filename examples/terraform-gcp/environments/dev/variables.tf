variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
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