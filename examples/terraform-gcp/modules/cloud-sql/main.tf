resource "google_sql_database_instance" "instance" {
  name             = "mycelium-database-instance"
  database_version = var.database_version
  region           = var.region

  depends_on = [var.vpc_connection]

  settings {
    tier = "db-f1-micro"
    
    ip_configuration {
      ipv4_enabled    = false
      private_network = var.network_id
    }
  }
}

resource "google_sql_database" "database" {
  name     = "mycelium-${var.db_name}"
  instance = google_sql_database_instance.instance.name
}

resource "google_sql_user" "user" {
  name     = var.db_user
  instance = google_sql_database_instance.instance.name
  password = random_password.db_password.result
}

resource "random_password" "db_password" {
  length  = 16
  special = true
} 