# Gimnasio en GKE · Virtual Insanity

Proyecto Final del curso Virtualización (Universidad Rafael Landívar, segundo semestre 2026). Aplicación web para un gimnasio, construida desde cero y desplegada en Google Kubernetes Engine con la infraestructura declarada en Terraform.

## Caso asignado

**Caso 2 · Gimnasio.** El sistema maneja dos entidades:

- **Miembros** (microservicio A): las personas inscritas en el gimnasio.
- **Clases programadas** (microservicio B): cada clase referencia a un miembro.

## Integrantes

| Integrante | Carné | Rol |
| --- | --- | --- |
| Rochelle Giulianne Esquivel Vargas | 1283220 | Rol 1 · Infraestructura como código |
| Oscar Javier Ortíz Pocón | 1182222 | Rol 2 · Base de datos y Miembros |
| Diego Andrés Azurdia Ortíz | 2528119 | Rol 3 · Clases programadas e imágenes |
| Diego Oswaldo Orellana Morales | 1163722 | Rol 4 · Frontend y acceso público |
| Susana Paola García García | 1224323 | Rol 5 · Kubernetes, operación y documentación |

## Estructura del repositorio

| Carpeta | Contenido | Responsable |
| --- | --- | --- |
| `terraform/` | Clúster GKE, node pool spot y Artifact Registry | Rol 1 |
| `db/` | Script de creación de tablas y carnés del equipo | Rol 2 |
| `services/miembros/` | Microservicio Miembros y su Dockerfile | Rol 2 |
| `services/clases/` | Microservicio Clases programadas y su Dockerfile | Rol 3 |
| `frontend/` | Interfaz web y su Dockerfile | Rol 4 |
| `k8s/` | Manifiestos de Kubernetes | Rol 5 (cada dueño escribe los de su parte) |
| `docs/` | Diagrama, estimación de costo y evidencias | Rol 5 |

Los acuerdos técnicos del equipo (nombres, rutas, campos y variables) están en [CONTRATO.md](CONTRATO.md).

## Arquitectura

Pendiente: aquí va el diagrama de arquitectura (Rol 5).

## Cómo trabajamos

- `main` solo recibe código probado, por Pull Request.
- `develop` es la rama donde se junta el trabajo de todos.
- Cada quien trabaja en su rama, por ejemplo `feature/terraform` o `feature/api-clases`, y abre un Pull Request hacia `develop`.
- Commits pequeños y con un título claro, por ejemplo `feat(miembros): crear endpoint para listar miembros`.

## Despliegue

Pendiente: instrucciones paso a paso para crear la infraestructura, publicar las imágenes y aplicar los manifiestos.
