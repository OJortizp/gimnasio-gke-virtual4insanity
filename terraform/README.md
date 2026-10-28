# terraform/ · Rol 1

Infraestructura declarada como código.

Archivos esperados:

- `main.tf`: clúster GKE Standard zonal, node pool de 2 nodos e2-small spot y repositorio de Artifact Registry.
- `variables.tf`: proyecto, zona y nombre del clúster.
- `outputs.tf`: datos útiles después del apply (nombre del clúster, ruta del repositorio).
- `terraform.tfvars.example`: valores de ejemplo. El `terraform.tfvars` real no se sube.

El estado (`*.tfstate`) tampoco se sube al repo.
