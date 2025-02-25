# Primary database instance
resource "google_sql_database_instance" "instance" {
  name             = var.name
  database_version = var.database_version
  region           = var.region

  depends_on = [var.vpc_connection]  # Ensure network is ready

  settings {
    tier = "db-custom-1-3840"
    
    # Network configuration
    ip_configuration {
      ipv4_enabled    = false
      private_network = var.network_id
    }

    # Apply labels
    user_labels = var.labels
  }

  # Operation timeouts
  timeouts {
    create = "30m"
    update = "30m"
    delete = "30m"
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