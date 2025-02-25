output "database_connection" {
  description = "Database connection details"
  sensitive   = true
  value = {
    host     = module.cloud_sql.connection_name
    database = module.cloud_sql.db_name
    username = module.cloud_sql.db_user
  }
}

output "service_urls" {
  description = "URLs of deployed services"
  value = {
    frontend = module.frontend_service.service_url
    api      = module.api_service.service_url
    auth     = module.auth_service.service_url
  }
} 