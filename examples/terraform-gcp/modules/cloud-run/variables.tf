variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
}

variable "name" {
  description = "The name of the Cloud Run service"
  type        = string
}

variable "image" {
  description = "The Docker image to deploy"
  type        = string
}

variable "environment_variables" {
  description = "Environment variables to set"
  type        = map(string)
  default     = {}
}

variable "cloudsql_connections" {
  description = "Cloud SQL connections to attach to this instance"
  type        = list(string)
  default     = []
} 