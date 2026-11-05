# main.tf · Rol 1
# Clúster GKE Standard zonal + node pool de 2 nodos e2-small Spot
# + repositorio de Artifact Registry. Los objetos de Kubernetes
# (Deployments, Services, etc.) NO se gestionan aquí: se aplican con kubectl.

terraform {
  required_version = ">= 1.5"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

# ---------------------------------------------------------------------------
# APIs necesarias (FAQ 4 del enunciado: si no están habilitadas, el apply falla).
# disable_on_destroy = false evita que el destroy apague APIs que otros usan.
# ---------------------------------------------------------------------------
locals {
  apis = [
    "container.googleapis.com",        # Kubernetes Engine
    "artifactregistry.googleapis.com", # Artifact Registry
    "compute.googleapis.com",          # Compute Engine (nodos, discos, balanceador)
    "iam.googleapis.com",              # Cuentas de servicio
  ]
}

resource "google_project_service" "apis" {
  for_each = toset(local.apis)

  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}

# ---------------------------------------------------------------------------
# Repositorio de Artifact Registry (formato Docker)
# ---------------------------------------------------------------------------
resource "google_artifact_registry_repository" "gimnasio" {
  project       = var.project_id
  location      = var.region
  repository_id = var.repository_id
  format        = "DOCKER"
  description   = "Imágenes del proyecto final (frontend, api-miembros, api-clases, postgres)."

  labels = {
    equipo = var.team_id
  }

  depends_on = [google_project_service.apis]
}

# ---------------------------------------------------------------------------
# Cuenta de servicio de los nodos (FAQ 3: ImagePullBackOff si no puede leer
# Artifact Registry). Es la identidad con la que los nodos bajan las imágenes,
# sin contraseñas ni imagePullSecret.
# ---------------------------------------------------------------------------
resource "google_service_account" "nodos" {
  project      = var.project_id
  account_id   = "gke-nodos-${var.team_id}"
  display_name = "Nodos GKE ${var.team_id}"

  depends_on = [google_project_service.apis]
}

resource "google_project_iam_member" "nodos_registry_reader" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = "serviceAccount:${google_service_account.nodos.email}"
}

resource "google_project_iam_member" "nodos_log_writer" {
  project = var.project_id
  role    = "roles/logging.logWriter"
  member  = "serviceAccount:${google_service_account.nodos.email}"
}

resource "google_project_iam_member" "nodos_metric_writer" {
  project = var.project_id
  role    = "roles/monitoring.metricWriter"
  member  = "serviceAccount:${google_service_account.nodos.email}"
}

# ---------------------------------------------------------------------------
# Clúster GKE Standard zonal.
# location = zona (NO región): un clúster regional cobraría USD 0.10/h sin crédito.
# El node pool por defecto se elimina y se declara uno propio aparte.
# ---------------------------------------------------------------------------
resource "google_container_cluster" "gke" {
  name     = var.cluster_name
  project  = var.project_id
  location = var.zone

  remove_default_node_pool = true
  initial_node_count       = 1

  # Permite que "terraform destroy" borre el clúster (en el provider 6.x
  # el valor por defecto es true y bloquearía el destroy).
  deletion_protection = false

  resource_labels = {
    equipo = var.team_id
  }

  depends_on = [google_project_service.apis]
}

# ---------------------------------------------------------------------------
# Node pool: 2 nodos e2-small de tipo Spot, disco de 30 GB pd-balanced.
# ---------------------------------------------------------------------------
resource "google_container_node_pool" "spot" {
  name       = "pool-spot"
  project    = var.project_id
  location   = var.zone
  cluster    = google_container_cluster.gke.name
  node_count = var.node_count

  node_config {
    machine_type = var.machine_type
    spot         = true
    disk_size_gb = var.disk_size_gb
    disk_type    = var.disk_type

    service_account = google_service_account.nodos.email
    oauth_scopes    = ["https://www.googleapis.com/auth/cloud-platform"]

    labels = {
      equipo = var.team_id
    }
  }

  depends_on = [
    google_project_iam_member.nodos_registry_reader,
    google_project_iam_member.nodos_log_writer,
    google_project_iam_member.nodos_metric_writer,
  ]
}
