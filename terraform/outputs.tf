# outputs.tf · Rol 1
# Datos útiles después del apply.

output "cluster_name" {
  description = "Nombre del clúster GKE."
  value       = google_container_cluster.gke.name
}

output "cluster_location" {
  description = "Zona del clúster."
  value       = google_container_cluster.gke.location
}

output "node_machine_type" {
  description = "Tipo de máquina de los nodos."
  value       = google_container_node_pool.spot.node_config[0].machine_type
}

output "nodes_are_spot" {
  description = "Confirma que los nodos son Spot."
  value       = google_container_node_pool.spot.node_config[0].spot
}

output "registry_path" {
  description = "Ruta base para etiquetar y subir las imágenes."
  value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.gimnasio.repository_id}"
}

output "get_credentials_command" {
  description = "Comando para conectar kubectl al clúster."
  value       = "gcloud container clusters get-credentials ${google_container_cluster.gke.name} --zone ${var.zone} --project ${var.project_id}"
}
