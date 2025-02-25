output "service_url" {
  description = "The URL of the deployed service"
  value       = google_cloud_run_service.service.status[0].url
}

output "service_name" {
  description = "The name of the Cloud Run service"
  value       = google_cloud_run_service.service.name
} 