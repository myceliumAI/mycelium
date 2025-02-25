# Create VPC
resource "google_compute_network" "vpc" {
  name                    = var.name
  auto_create_subnetworks = false
}

# Create Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "${var.name}-subnet"
  ip_cidr_range = "10.0.0.0/24"
  network       = google_compute_network.vpc.id
  region        = var.region

  # Enable private Google Access
  private_ip_google_access = true
}

# Allocate IP range for VPC peering
resource "google_compute_global_address" "private_ip_address" {
  name          = "${var.name}-private-ip"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.vpc.id
}

# Create VPC peering connection
resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]

  depends_on = [google_compute_global_address.private_ip_address]
}

# Create VPC connector
resource "google_vpc_access_connector" "connector" {
  name          = "${replace(var.name, "-", "")}-con"
  ip_cidr_range = "10.8.0.0/28"
  network       = google_compute_network.vpc.name
  region        = var.region

  depends_on = [google_compute_network.vpc]
} 