output "connection_name" {
  description = "The connection name of the instance to be used in connection strings"
  value       = google_sql_database_instance.instance.connection_name
}

output "db_user" {
  description = "The database user"
  value       = google_sql_user.user.name
}

output "db_name" {
  description = "The name of the database"
  value       = google_sql_database.database.name
} 