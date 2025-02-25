# Cloud Run service deployment
resource "google_cloud_run_service" "service" {
  name     = var.name
  location = var.region

  template {
    metadata {
      annotations = {
        # Cloud SQL instance connection
        "run.googleapis.com/cloudsql-instances" = join(",", var.cloudsql_connections)
      }
    }

    spec {
      containers {
        image = var.image
        
        ports {
          container_port = 8080
        }

        dynamic "env" {
          for_each = var.environment_variables
          content {
            name  = env.key
            value = env.value
          }
        }
      }
    }
  }
}

# Public access configuration
resource "google_cloud_run_service_iam_member" "public" {
  location = google_cloud_run_service.service.location
  project  = google_cloud_run_service.service.project
  service  = google_cloud_run_service.service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
} 