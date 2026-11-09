# Estimación de Costo Mensual de Infraestructura en Google Cloud (Criterio G1)

- **Proyecto:** Sistema de Gestión de Gimnasio en Google Kubernetes Engine (Caso 2)
- **Proyecto de Google Cloud:** `gimnasio-virtual4insanity`
- **Equipo / Identificador:** `virtual4insanity`
- **Clúster declarado:** `gke-virtual4insanity` (Modo Standard, Zonal)
- **Node Pool declarado:** `pool-spot` (2 nodos `e2-small` Spot, discos `pd-balanced` de 30 GB)
- **Namespace:** `virtual4insanity`
- **Región y zona:** `us-central1` / `us-central1-a` (Iowa, EE. UU.)
- **Responsable del documento:** Susana Paola García García (Carné `1224323` · Rol 5: Kubernetes, operación y documentación)
- **Fecha de elaboración inicial:** 2 de noviembre de 2026 *(elaborada antes del despliegue de la infraestructura y verificada contra los archivos definitivos de `terraform/`)*

---

## 1. Propósito y alcance

Este documento presenta la estimación preventiva del costo de la infraestructura en Google Cloud Platform (GCP) para el despliegue del sistema distribuido de gestión de gimnasio, en cumplimiento del **criterio G1** de la rúbrica oficial (*"Presenta la estimación de costo mensual de la infraestructura declarada, elaborada antes del despliegue"*).

El análisis contempla dos escenarios operativos en la región `us-central1`:
1. **Escenario A — Operación continua mensual (730 horas/mes):** Costo proyectado si el clúster y todos sus recursos permanecieran encendidos las 24 horas durante un mes estándar de 730 horas.
2. **Escenario B — Uso temporal del equipo (40 horas totales):** Costo proyectado aplicando la práctica recomendada en el proyecto (*crear la infraestructura con Terraform únicamente durante las sesiones de pruebas y defensa, y destruirla al finalizar*).

---

## 2. Inventario de recursos verificados contra `terraform/` y `k8s/`

De acuerdo con `CONTRATO.md`, los archivos declarativos en `terraform/` ([main.tf](../terraform/main.tf), [variables.tf](../terraform/variables.tf), [outputs.tf](../terraform/outputs.tf)) y los manifiestos en `k8s/`, la infraestructura consta de los siguientes recursos exactos:

| Componente | Especificación declarada en el código | Archivo de referencia |
| :--- | :--- | :--- |
| **Clúster GKE** | Clúster GKE **Standard zonal** `gke-virtual4insanity` en `location = "us-central1-a"` (`remove_default_node_pool = true`, `deletion_protection = false`). | [terraform/main.tf](../terraform/main.tf), [terraform/variables.tf](../terraform/variables.tf) |
| **Node Pool (`pool-spot`)** | **2 nodos `e2-small`** (2 vCPU compartidas = 0.5 núcleo físico, 2 GiB RAM c/u) con aprovisionamiento **Spot** (`spot = true`). | [terraform/main.tf](../terraform/main.tf), [terraform/variables.tf](../terraform/variables.tf) |
| **Discos de arranque (Boot Disks)** | **30 GB por nodo** (`disk_size_gb = 30`) de tipo **`pd-balanced`** (`disk_type = "pd-balanced"`), sumando **60 GB totales** para los 2 nodos. | [terraform/variables.tf](../terraform/variables.tf) |
| **Cuenta de servicio e IAM** | `gke-nodos-virtual4insanity` con roles `artifactregistry.reader`, `logging.logWriter` y `monitoring.metricWriter` (sin costo en GCP). | [terraform/main.tf](../terraform/main.tf) |
| **Volumen persistente de BD (`db-pvc`)** | `PersistentVolumeClaim` de **1 GiB** (`ReadWriteOnce`) para PostgreSQL 16. | [k8s/10-db.yaml](../k8s/10-db.yaml) |
| **Acceso público (`frontend`)** | `Service` tipo **`LoadBalancer`** en el puerto `80` (`targetPort: 80`) con dirección IPv4 pública externa. | [k8s/40-frontend.yaml](../k8s/40-frontend.yaml) |
| **Registro de contenedores** | Repositorio Docker **`gimnasio`** en **Artifact Registry** (`us-central1`) para las 4 imágenes (`frontend:v1`, `api-miembros:v1`, `api-clases:v1`/`v2`, `postgres:16-alpine`). | [terraform/main.tf](../terraform/main.tf) |

---

## 3. Clasificación de costos (Fijos, Variables por tiempo y Dependientes del consumo)

1. **Costos variables por tiempo de ejecución (por hora/segundo con el clúster activo):**
   - **Administración del plano de control GKE:** Tarifa nominal de **USD 0.10 / hora** por clúster. Google Cloud otorga el crédito **GKE Cluster Management Free Tier** de hasta **USD 74.40 / mes por cuenta de facturación**, el cual cubre el 100 % de la tarifa de administración de **un (1) único clúster Zonal o Autopilot**. Al haberse declarado `location = var.zone` (`us-central1-a`) en [terraform/main.tf](../terraform/main.tf), el cargo neto para un único clúster zonal es **USD 0.00**.
   - **Instancias `e2-small` Spot:** Se facturan por segundo mientras los nodos están en ejecución (**~USD 0.0101 / hora por nodo** en `us-central1`, frente a USD 0.0168 / hora en modalidad *On-Demand*).
   - **Regla de reenvío (*Forwarding Rule*) del Network Load Balancer:** Se factura a **USD 0.025 / hora** por la primera regla activa creada por el `Service` tipo `LoadBalancer` (`frontend`).
   - **Direcciones IPv4 públicas externas en uso:** Se facturan a **USD 0.005 / hora** por cada IPv4 externa asignada a un recurso en ejecución (1 IP del `LoadBalancer` + 2 IPs efímeras de los nodos `e2-small`).
2. **Costos por capacidad aprovisionada (GB-mes prorrateado por tiempo de existencia del disco):**
   - **Discos de arranque de los nodos (`2 × 30 GB = 60 GB pd-balanced`)** y **PVC `db-pvc` (1 GiB):** Se facturan según la capacidad aprovisionada independientemente del porcentaje de ocupación real (`pd-balanced` a **USD 0.10 / GB-mes**). Si no se eliminan al destruir el clúster, continúan generando cargos.
   - **Almacenamiento en Artifact Registry (`gimnasio`):** Los primeros **0.5 GB / mes son gratuitos**; el almacenamiento adicional se factura a **USD 0.10 / GB-mes**.
3. **Costos dependientes del consumo / tráfico de red:**
   - **Procesamiento de datos del Load Balancer:** **USD 0.008 / GiB** procesado en `us-central1`.
   - **Tráfico entrante (*Ingress*) y tráfico interno en la misma zona (`us-central1-a`):** **USD 0.00** (la comunicación por DNS entre `frontend`, `api-miembros`, `api-clases` y `db` dentro de `us-central1-a`, así como la descarga de imágenes desde Artifact Registry en `us-central1`, no generan cargos de transferencia).
   - **Tráfico saliente a Internet (*Internet Egress*):** Alrededor de **USD 0.12 / GiB** (Premium Tier, primeros GiB hacia Internet).

---

## 4. Escenario A: Estimación mensual para operación continua (730 horas/mes)

En esta tabla se detallan los costos proyectados para un mes completo (**730 horas**) en `us-central1` con la configuración exacta de [terraform/variables.tf](../terraform/variables.tf) (`2 × e2-small` Spot y discos `pd-balanced` de 30 GB por nodo):

| Recurso | Cantidad / Capacidad | Tarifa unitaria (`us-central1`) | Horas / Periodo | Subtotal 730 h (USD) | Fuente oficial |
| :--- | :--- | :--- | :--- | ---: | :--- |
| **Plano de control GKE Standard Zonal** (`gke-virtual4insanity`) | 1 clúster zonal (`us-central1-a`) | USD 0.10 / h *(Cargo bruto: USD 73.00; exento por crédito mensual de hasta USD 74.40 para 1 clúster zonal)* | 730 h | **0.00** | [GKE Pricing](https://cloud.google.com/kubernetes-engine/pricing) |
| **Nodos de cómputo GKE (`e2-small` Spot)** | 2 nodos (`pool-spot`, 2 vCPU comp., 2 GiB RAM c/u) | USD 0.0101 / nodo-hora | 730 h | **14.75** | [Compute Engine VM Pricing](https://cloud.google.com/compute/vm-instance-pricing) |
| **Discos de arranque de nodos (`Boot Disks`)** | 2 × 30 GB = 60 GB (`pd-balanced`) | USD 0.10 / GB-mes ($\approx$ USD 0.000137 / GB-h) | 730 h (1 mes) | **6.00** | [Compute Engine Disk Pricing](https://cloud.google.com/compute/disks-image-pricing) |
| **Almacenamiento persistente PostgreSQL (`db-pvc`)** | 1 GiB (`standard-rwo` / `pd-balanced`) | USD 0.10 / GB-mes | 730 h (1 mes) | **0.10** | [Compute Engine Disk Pricing](https://cloud.google.com/compute/disks-image-pricing) |
| **Cloud Load Balancing — Regla de reenvío (`frontend`)** | 1 regla de reenvío (puerto 80) | USD 0.025 / h (1 a 5 reglas) | 730 h | **18.25** | [VPC / Cloud Load Balancing Pricing](https://cloud.google.com/vpc/network-pricing) |
| **Cloud Load Balancing — Datos procesados** | ~5 GiB estimados en el mes | USD 0.008 / GiB | Mensual | **0.04** | [VPC / Cloud Load Balancing Pricing](https://cloud.google.com/vpc/network-pricing) |
| **Direcciones IPv4 públicas externas en uso** | 3 IPs (1 `LoadBalancer` + 2 nodos) | USD 0.005 / IP-hora | 730 h | **10.95** | [External IP Addresses Pricing](https://cloud.google.com/vpc/network-pricing#ipaddress) |
| **Artifact Registry (`gimnasio`) — Almacenamiento** | ~1.0 GB total (0.5 GB gratis + 0.5 GB facturables) | Primeros 0.5 GB gratis; luego USD 0.10 / GB-mes | 730 h (1 mes) | **0.05** | [Artifact Registry Pricing](https://cloud.google.com/artifact-registry/pricing) |
| **Transferencia de datos saliente a Internet (*Egress*)** | ~1.0 GiB estimado en el mes | USD 0.12 / GiB (tráfico interno y pull en `us-central1` = USD 0.00) | Mensual | **0.12** | [VPC Network Pricing](https://cloud.google.com/vpc/network-pricing) |
| **TOTAL ESTIMADO MENSUAL (730 HORAS)** | **Con crédito Free Tier GKE Zonal** | | **730 h** | **USD 50.26** | |
| *Total alternativo sin crédito GKE (si hubiera otro clúster)* | *Sumando USD 73.00 de Control Plane* | | *730 h* | *USD 123.26* | |

---

## 5. Escenario B: Uso temporal del equipo (40 horas de trabajo efectivo)

Dado que la infraestructura está declarada como código en Terraform y los manifiestos en YAML, el equipo solo mantiene el clúster encendido durante las sesiones de integración, pruebas y defensa (estimadas en **40 horas acumuladas**), destruyendo los recursos con `terraform destroy` fuera de las sesiones de trabajo:

| Recurso | Cantidad / Capacidad | Tarifa unitaria (`us-central1`) | Horas activas | Subtotal 40 h (USD) | Fuente oficial |
| :--- | :--- | :--- | :--- | ---: | :--- |
| **Plano de control GKE Standard Zonal** (`gke-virtual4insanity`) | 1 clúster zonal (`us-central1-a`) | USD 0.10 / h *(Cargo bruto: USD 4.00; cubierto por crédito mensual GKE Free Tier)* | 40 h | **0.00** | [GKE Pricing](https://cloud.google.com/kubernetes-engine/pricing) |
| **Nodos de cómputo GKE (`e2-small` Spot)** | 2 nodos (`pool-spot`, `e2-small`) | USD 0.0101 / nodo-hora | 40 h | **0.81** | [Compute Engine VM Pricing](https://cloud.google.com/compute/vm-instance-pricing) |
| **Discos de arranque de nodos (`Boot Disks`)** | 60 GB (`pd-balanced`, prorrateado a 40/730 mes) | USD 0.10 / GB-mes | 40 h | **0.33** | [Compute Engine Disk Pricing](https://cloud.google.com/compute/disks-image-pricing) |
| **Almacenamiento persistente PostgreSQL (`db-pvc`)** | 1 GiB (`pd-balanced`, prorrateado a 40/730 mes) | USD 0.10 / GB-mes | 40 h | **0.01** | [Compute Engine Disk Pricing](https://cloud.google.com/compute/disks-image-pricing) |
| **Cloud Load Balancing — Regla de reenvío (`frontend`)** | 1 regla de reenvío | USD 0.025 / h | 40 h | **1.00** | [VPC / Cloud Load Balancing Pricing](https://cloud.google.com/vpc/network-pricing) |
| **Cloud Load Balancing — Datos procesados** | < 1 GiB durante pruebas y defensa | USD 0.008 / GiB | 40 h | **0.01** | [VPC / Cloud Load Balancing Pricing](https://cloud.google.com/vpc/network-pricing) |
| **Direcciones IPv4 públicas externas en uso** | 3 IPs (1 `LoadBalancer` + 2 nodos) | USD 0.005 / IP-hora | 40 h | **0.60** | [External IP Addresses Pricing](https://cloud.google.com/vpc/network-pricing#ipaddress) |
| **Artifact Registry (`gimnasio`) — Almacenamiento** | ~1.0 GB conservado durante la semana del proyecto | Primeros 0.5 GB gratis; luego USD 0.10 / GB-mes | ~1 semana | **0.05** | [Artifact Registry Pricing](https://cloud.google.com/artifact-registry/pricing) |
| **Transferencia de datos saliente a Internet (*Egress*)** | ~0.15 GiB durante pruebas y defensa | USD 0.12 / GiB | 40 h | **0.02** | [VPC Network Pricing](https://cloud.google.com/vpc/network-pricing) |
| **TOTAL ESTIMADO USO TEMPORAL (40 HORAS)** | **Con crédito Free Tier GKE Zonal** | | **40 h** | **USD 2.83** | |

---

## 6. Supuestos verificados en `terraform/` y factores de variación

Al revisar los archivos definitivos entregados por el **Rol 1** en `terraform/` ([main.tf](../terraform/main.tf) y [variables.tf](../terraform/variables.tf)):

1. **Tamaño y tipo del disco de arranque confirmados (`30 GB` `pd-balanced`):**
   - En [terraform/variables.tf](../terraform/variables.tf) se declararon explícitamente `disk_size_gb = 30` y `disk_type = "pd-balanced"`, evitando que GKE asigne el valor por defecto de 100 GB por nodo (lo cual habría elevado el costo de discos de arranque de USD 6.00/mes a USD 20.00/mes en el escenario de 730 h).
2. **Clúster Zonal confirmado (`location = var.zone = "us-central1-a"`):**
   - En [terraform/main.tf](../terraform/main.tf) el recurso `google_container_cluster.gke` utiliza `location = var.zone` (`us-central1-a`), asegurando la aplicación del crédito mensual de administración para un clúster zonal único en la cuenta de facturación.
3. **Restricciones de nodos validadas por código:**
   - [terraform/variables.tf](../terraform/variables.tf) incluye bloques `validation` que impiden configurar más de 2 nodos (`var.node_count <= 2`) o un tipo de máquina distinto de `e2-small`.
4. **Eliminación previa de recursos creados con `kubectl`:**
   - Antes de ejecutar `terraform destroy` se debe eliminar el namespace (`kubectl delete ns virtual4insanity`) para liberar el `Service` `LoadBalancer` y el `PersistentVolumeClaim` `db-pvc`, evitando que la regla de reenvío (USD 0.025/h) o el disco persistente queden huérfanos generando cargos.
5. **Variabilidad de tarifas Spot:**
   - Las tarifas de máquinas virtuales **Spot** en Google Cloud pueden variar dinámicamente según la disponibilidad en `us-central1-a`.

---

## 7. Advertencia sobre los importes estimados

> **Aviso importante:** Todos los valores expresados en este documento están en dólares estadounidenses (**USD**) y constituyen una **estimación técnica preventiva** basada en las listas de precios públicas de Google Cloud para la región `us-central1` vigentes en noviembre de 2026. **No representan importes garantizados ni consumos facturados reales.** El gasto real final se verificará en el panel de Facturación de Google Cloud al cierre del proyecto (**Criterio G3**).

---

## 8. Referencias oficiales consultadas

1. Google Cloud — *Google Kubernetes Engine (GKE) Pricing*: https://cloud.google.com/kubernetes-engine/pricing
2. Google Cloud — *Compute Engine VM Instance Pricing*: https://cloud.google.com/compute/vm-instance-pricing
3. Google Cloud — *Compute Engine Disks and Images Pricing*: https://cloud.google.com/compute/disks-image-pricing
4. Google Cloud — *Virtual Private Cloud (VPC) & Cloud Load Balancing Network Pricing*: https://cloud.google.com/vpc/network-pricing
5. Google Cloud — *Artifact Registry Pricing*: https://cloud.google.com/artifact-registry/pricing
