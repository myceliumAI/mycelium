variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
}

variable "network_id" {
  description = "The VPC network ID"
  type        = string
}

variable "database_version" {
  description = "The database version"
  type        = string
}

variable "db_name" {
  description = "The name of the database"
  type        = string
}

variable "db_user" {
  description = "The database user"
  type        = string
}

variable "vpc_connection" {
  description = "The VPC connection to depend on"
  type        = any
}

variable "name" {
  description = "Name of the Cloud SQL instance"
  type        = string
}

variable "labels" {
  description = "Labels to apply to resources"
  type        = map(string)
  default     = {}
} 