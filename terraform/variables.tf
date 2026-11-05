# variables.tf · Rol 1
# Ningún valor sensible va en el código: el proyecto se pasa por terraform.tfvars
# (que está en .gitignore) y el resto tiene los valores acordados en CONTRATO.md.

variable "project_id" {
  description = "ID del proyecto de Google Cloud (no el nombre ni el número)."
  type        = string
}

variable "zone" {
  description = "Zona del clúster. Zonal = control plane en una sola zona (cubierto por el crédito de GKE)."
  type        = string
  default     = "us-central1-a"
}

variable "region" {
  description = "Región del repositorio de Artifact Registry. Debe coincidir con la zona."
  type        = string
  default     = "us-central1"
}

variable "cluster_name" {
  description = "Nombre del clúster GKE (lleva el identificador del equipo)."
  type        = string
  default     = "gke-virtual4insanity"
}

variable "repository_id" {
  description = "Nombre del repositorio Docker en Artifact Registry."
  type        = string
  default     = "gimnasio"
}

variable "node_count" {
  description = "Cantidad de nodos del node pool. El enunciado prohíbe más de 2."
  type        = number
  default     = 2

  validation {
    condition     = var.node_count >= 1 && var.node_count <= 2
    error_message = "El enunciado no permite más de 2 nodos."
  }
}

variable "machine_type" {
  description = "Tipo de máquina de los nodos. El enunciado no permite nada mayor a e2-small."
  type        = string
  default     = "e2-small"

  validation {
    condition     = var.machine_type == "e2-small"
    error_message = "El enunciado solo permite e2-small."
  }
}

variable "disk_size_gb" {
  description = "Tamaño del disco de arranque por nodo (GB). Si no se declara, GKE pone 100 y sube el costo."
  type        = number
  default     = 30
}

variable "disk_type" {
  description = "Tipo de disco de arranque de los nodos."
  type        = string
  default     = "pd-balanced"
}

variable "team_id" {
  description = "Identificador del equipo, usado como etiqueta."
  type        = string
  default     = "virtual4insanity"
}
