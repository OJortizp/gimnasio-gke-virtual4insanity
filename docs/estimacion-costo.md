# Estimación de Costo Mensual de Infraestructura en Google Cloud (Criterio G1)

- **Proyecto:** Sistema de Gestión de Gimnasio en Google Kubernetes Engine (Caso 2)
- **Equipo / Identificador:** `virtual4insanity`
- **Clúster previsto:** `gke-virtual4insanity` (Modo Standard, Zonal)
- **Namespace:** `virtual4insanity`
- **Región y zona:** `us-central1` / `us-central1-a` (Iowa, EE. UU.)
- **Responsable del documento:** Susana Paola García García (Carné `1224323` · Rol 5: Kubernetes, operación y documentación)
- **Fecha de elaboración:** 2 de noviembre de 2026 *(elaborada antes del despliegue de la infraestructura)*

---

## 1. Propósito y alcance

Este documento presenta la estimación preventiva del costo de la infraestructura en Google Cloud Platform (GCP) para el despliegue del sistema distribuido de gestión de gimnasio, en cumplimiento del **criterio G1** de la rúbrica oficial (*"Presenta la estimación de costo mensual de la infraestructura declarada, elaborada antes del despliegue"*).

El análisis contempla dos escenarios operativos en la región `us-central1`:
1. **Escenario A — Operación continua mensual (730 horas/mes):** Costo proyectado si el clúster y todos sus recursos permanecieran encendidos las 24 horas durante un mes estándar de 730 horas.
2. **Escenario B — Uso temporal del equipo (40 horas totales):** Costo proyectado aplicando la práctica recomendada en la sección 5 del enunciado (*crear la infraestructura con Terraform únicamente durante las sesiones de pruebas y defensa, y destruirla al finalizar*).

---

## 2. Inventario de recursos obligatorios y configuraciones pendientes

De acuerdo con el enunciado del proyecto, `CONTRATO.md` y los manifiestos existentes en `k8s/` (`00-namespace.yaml`, `10-db.yaml` y `20-api-miembros.yaml`), la arquitectura requiere los siguientes recursos de nube:

| Componente | Especificación acordada (`CONTRATO.md` / Enunciado) | Estado de definición en el repositorio (al 2 nov 2026) |
| :--- | :--- | :--- |
| **Clúster GKE** | Clúster GKE **Standard zonal** llamado `gke-virtual4insanity` en `us-central1-a`. | Acordado en `CONTRATO.md`; pendiente archivo `terraform/main.tf` (Rol 1). |
| **Node Pool** | **2 nodos `e2-small`** (2 vCPU compartidas = 0.5 núcleo físico, 2 GiB RAM c/u) con aprovisionamiento **Spot** (`spot = true`). | Acordado en enunciado y `CONTRATO.md`; pendiente archivo `terraform/main.tf` (Rol 1). |
| **Discos de arranque (Boot Disks)** | 1 disco persistente por cada nodo `e2-small` (2 discos en total). | **Pendiente de confirmación en `terraform/main.tf`** (tamaño `disk_size_gb` y tipo `disk_type`). |
| **Volumen persistente de BD (`db-pvc`)** | `PersistentVolumeClaim` de **1 GiB** (`ReadWriteOnce`) para PostgreSQL 16. | Definido en `k8s/10-db.yaml` (líneas 5–17). |
| **Acceso público (`frontend`)** | `Service` tipo **`LoadBalancer`** en el puerto `80` con dirección IPv4 pública externa. | Acordado en `CONTRATO.md` (sección 2); pendiente `k8s/40-frontend.yaml` (Rol 4). |
| **Registro de contenedores** | Repositorio Docker **`gimnasio`** en **Artifact Registry** (`us-central1`) para 4 imágenes (`frontend`, `api-miembros`, `api-clases`, `postgres:16-alpine`). | Acordado en `CONTRATO.md` (secciones 1 y 3); pendiente declaración en `terraform/main.tf` (Rol 1). |

---

## 3. Clasificación de costos (Fijos, Variables por tiempo y Dependientes del consumo)

1. **Costos variables por tiempo de ejecución (por hora/segundo con el clúster activo):**
   - **Administración del plano de control GKE:** Tarifa nominal de **USD 0.10 / hora** por clúster. Google Cloud otorga el crédito **GKE Cluster Management Free Tier** de hasta **USD 74.40 / mes por cuenta de facturación**, el cual cubre el 100 % de la tarifa de administración de **un (1) único clúster Zonal o Autopilot**. Si la cuenta de facturación no tiene otros clústeres activos, el cargo neto es **USD 0.00**.
   - **Instancias `e2-small` Spot:** Se facturan por segundo mientras los nodos están en ejecución (**~USD 0.0101 / hora por nodo** en `us-central1`, frente a USD 0.0168 / hora en modalidad *On-Demand*).
   - **Regla de reenvío (*Forwarding Rule*) del Network Load Balancer:** Se factura a **USD 0.025 / hora** por la primera regla activa creada por el `Service` tipo `LoadBalancer`.
   - **Direcciones IPv4 públicas externas en uso:** Se facturan a **USD 0.005 / hora** por cada IPv4 externa asignada a un recurso en ejecución (1 IP del `LoadBalancer` + 2 IPs efímeras de los nodos `e2-small` si el clúster utiliza nodos públicos).
2. **Costos por capacidad aprovisionada (GiB-mes prorrateado por tiempo de existencia del disco):**
   - **Discos de arranque de los nodos (Boot Disks)** y **PVC `db-pvc` (1 GiB):** Se facturan según la capacidad aprovisionada independientemente del porcentaje de ocupación real (`pd-balanced` a **USD 0.10 / GiB-mes** o `pd-standard` a **USD 0.04 / GiB-mes**). Si no se eliminan al destruir el clúster, continúan generando cargos.
   - **Almacenamiento en Artifact Registry:** Los primeros **0.5 GiB / mes son gratuitos**; el almacenamiento adicional se factura a **USD 0.10 / GiB-mes**.
3. **Costos dependientes del consumo / tráfico de red:**
   - **Procesamiento de datos del Load Balancer:** **USD 0.008 / GiB** procesado en `us-central1`.
   - **Tráfico entrante (*Ingress*) y tráfico interno en la misma zona (`us-central1-a`):** **USD 0.00** (la comunicación por DNS entre `frontend`, `api-miembros`, `api-clases` y `db` dentro de `us-central1-a`, así como la descarga de imágenes desde Artifact Registry en `us-central1`, no generan cargos de transferencia).
   - **Tráfico saliente a Internet (*Internet Egress*):** Alrededor de **USD 0.12 / GiB** (Premium Tier, primeros GiB hacia Internet).

---

## 4. Escenario A: Estimación mensual para operación continua (730 horas/mes)

En esta tabla se detallan los costos proyectados para un mes completo (**730 horas**) en `us-central1`, asumiendo discos de arranque `pd-balanced` de 30 GiB por nodo:

| Recurso | Cantidad / Capacidad | Tarifa unitaria (`us-central1`) | Horas / Periodo | Subtotal 730 h (USD) | Fuente oficial |
| :--- | :--- | :--- | :--- | ---: | :--- |
| **Plano de control GKE Standard Zonal** (`gke-virtual4insanity`) | 1 clúster zonal | USD 0.10 / h *(Cargo bruto: USD 73.00; exento por crédito mensual de hasta USD 74.40 para 1 clúster zonal)* | 730 h | **0.00** | [GKE Pricing](https://cloud.google.com/kubernetes-engine/pricing) |
| **Nodos de cómputo GKE (`e2-small` Spot)** | 2 nodos (2 vCPU comp., 2 GiB RAM c/u) | USD 0.0101 / nodo-hora | 730 h | **14.75** | [Compute Engine VM Pricing](https://cloud.google.com/compute/vm-instance-pricing) |
| **Discos de arranque de nodos (`Boot Disks`)** | 2 × 30 GiB = 60 GiB (`pd-balanced`) | USD 0.10 / GiB-mes ($\approx$ USD 0.000137 / GiB-h) | 730 h (1 mes) | **6.00** | [Compute Engine Disk Pricing](https://cloud.google.com/compute/disks-image-pricing) |
| **Almacenamiento persistente PostgreSQL (`db-pvc`)** | 1 GiB (`standard-rwo` / `pd-balanced`) | USD 0.10 / GiB-mes | 730 h (1 mes) | **0.10** | [Compute Engine Disk Pricing](https://cloud.google.com/compute/disks-image-pricing) |
| **Cloud Load Balancing — Regla de reenvío (`frontend`)** | 1 regla de reenvío (puerto 80) | USD 0.025 / h (1 a 5 reglas) | 730 h | **18.25** | [VPC / Cloud Load Balancing Pricing](https://cloud.google.com/vpc/network-pricing) |
| **Cloud Load Balancing — Datos procesados** | ~5 GiB estimados en el mes | USD 0.008 / GiB | Mensual | **0.04** | [VPC / Cloud Load Balancing Pricing](https://cloud.google.com/vpc/network-pricing) |
| **Direcciones IPv4 públicas externas en uso** | 3 IPs (1 `LoadBalancer` + 2 nodos) | USD 0.005 / IP-hora | 730 h | **10.95** | [External IP Addresses Pricing](https://cloud.google.com/vpc/network-pricing#ipaddress) |
| **Artifact Registry (`gimnasio`) — Almacenamiento** | ~1.0 GiB total (0.5 GiB gratis + 0.5 GiB facturables) | Primeros 0.5 GiB gratis; luego USD 0.10 / GiB-mes | 730 h (1 mes) | **0.05** | [Artifact Registry Pricing](https://cloud.google.com/artifact-registry/pricing) |
| **Transferencia de datos saliente a Internet (*Egress*)** | ~1.0 GiB estimado en el mes | USD 0.12 / GiB (tráfico interno y pull en `us-central1` = USD 0.00) | Mensual | **0.12** | [VPC Network Pricing](https://cloud.google.com/vpc/network-pricing) |
| **TOTAL ESTIMADO MENSUAL (730 HORAS)** | **Con crédito Free Tier GKE Zonal** | | **730 h** | **USD 50.26** | |
| *Total alternativo sin crédito GKE (si hubiera otro clúster)* | *Sumando USD 73.00 de Control Plane* | | *730 h* | *USD 123.26* | |

---

## 5. Escenario B: Uso temporal del equipo (40 horas de trabajo efectivo)

Dado que la infraestructura está declarada como código en Terraform y los manifiestos en YAML, el equipo solo mantendrá el clúster encendido durante las sesiones de integración, pruebas y defensa (estimadas en **40 horas acumuladas**), destruyendo los recursos con `terraform destroy` fuera de las sesiones de trabajo:

| Recurso | Cantidad / Capacidad | Tarifa unitaria (`us-central1`) | Horas activas | Subtotal 40 h (USD) | Fuente oficial |
| :--- | :--- | :--- | :--- | ---: | :--- |
| **Plano de control GKE Standard Zonal** (`gke-virtual4insanity`) | 1 clúster zonal | USD 0.10 / h *(Cargo bruto: USD 4.00; cubierto por crédito mensual GKE Free Tier)* | 40 h | **0.00** | [GKE Pricing](https://cloud.google.com/kubernetes-engine/pricing) |
| **Nodos de cómputo GKE (`e2-small` Spot)** | 2 nodos (`e2-small`) | USD 0.0101 / nodo-hora | 40 h | **0.81** | [Compute Engine VM Pricing](https://cloud.google.com/compute/vm-instance-pricing) |
| **Discos de arranque de nodos (`Boot Disks`)** | 60 GiB (`pd-balanced`, prorrateado a 40/730 mes) | USD 0.10 / GiB-mes | 40 h | **0.33** | [Compute Engine Disk Pricing](https://cloud.google.com/compute/disks-image-pricing) |
| **Almacenamiento persistente PostgreSQL (`db-pvc`)** | 1 GiB (`pd-balanced`, prorrateado a 40/730 mes) | USD 0.10 / GiB-mes | 40 h | **0.01** | [Compute Engine Disk Pricing](https://cloud.google.com/compute/disks-image-pricing) |
| **Cloud Load Balancing — Regla de reenvío (`frontend`)** | 1 regla de reenvío | USD 0.025 / h | 40 h | **1.00** | [VPC / Cloud Load Balancing Pricing](https://cloud.google.com/vpc/network-pricing) |
| **Cloud Load Balancing — Datos procesados** | < 1 GiB durante pruebas y defensa | USD 0.008 / GiB | 40 h | **0.01** | [VPC / Cloud Load Balancing Pricing](https://cloud.google.com/vpc/network-pricing) |
| **Direcciones IPv4 públicas externas en uso** | 3 IPs (1 `LoadBalancer` + 2 nodos) | USD 0.005 / IP-hora | 40 h | **0.60** | [External IP Addresses Pricing](https://cloud.google.com/vpc/network-pricing#ipaddress) |
| **Artifact Registry (`gimnasio`) — Almacenamiento** | ~1.0 GiB conservado durante la semana del proyecto | Primeros 0.5 GiB gratis; luego USD 0.10 / GiB-mes | ~1 semana | **0.05** | [Artifact Registry Pricing](https://cloud.google.com/artifact-registry/pricing) |
| **Transferencia de datos saliente a Internet (*Egress*)** | ~0.15 GiB durante pruebas y defensa | USD 0.12 / GiB | 40 h | **0.02** | [VPC Network Pricing](https://cloud.google.com/vpc/network-pricing) |
| **TOTAL ESTIMADO USO TEMPORAL (40 HORAS)** | **Con crédito Free Tier GKE Zonal** | | **40 h** | **USD 2.83** | |

---

## 6. Supuestos utilizados y variaciones posibles al recibir los archivos de Terraform (Rol 1)

Dado que a la fecha de esta estimación (2 de noviembre de 2026) los archivos definitivos en `terraform/` (`main.tf`, `variables.tf`, `outputs.tf`) están pendientes de entrega por parte de **Rochelle Esquivel (Rol 1)**, los siguientes parámetros podrían modificar el costo final:

1. **Tamaño y tipo del disco de arranque del Node Pool (`disk_size_gb` y `disk_type`):**
   - *Supuesto utilizado:* 30 GiB por nodo de tipo `pd-balanced` (60 GiB totales = **USD 6.00/mes** en 730 h o **USD 0.33** en 40 h).
   - *Qué cambia si varía en `terraform/main.tf`:*
     - Si no se especifica `disk_size_gb` en Terraform, GKE asigna por defecto **100 GiB por nodo** (200 GiB totales). Con `pd-balanced` esto elevaría el costo de discos de arranque a **USD 20.00/mes** en 730 h (total mensual de **USD 64.26**) o **USD 1.10** en 40 h (total de **USD 3.60**).
     - Si se configura `disk_type = "pd-standard"` (HDD, USD 0.04/GiB-mes) con 30 GiB por nodo, el costo de discos de arranque bajaría a **USD 2.40/mes** en 730 h (total mensual de **USD 46.66**) o **USD 0.13** en 40 h (total de **USD 2.63**).
2. **Condición del crédito del plano de control de GKE:**
   - La tarifa de administración de GKE (USD 0.10/hora) solo es USD 0.00 si el clúster es **Zonal** (`location = "us-central1-a"`) y es el **único clúster** activo en la cuenta de facturación del proyecto. Si por error se declarase `location = "us-central1"` (clúster Regional), el crédito gratuito no aplica y se cobrarían USD 0.10/hora desde el primer minuto.
3. **Eliminación de recursos creados fuera de Terraform (`kubectl`):**
   - Como advierte la sección 12 (pregunta frecuente #7) del enunciado, antes de ejecutar `terraform destroy` se debe eliminar el namespace o el Service `LoadBalancer` y el `PersistentVolumeClaim` (`kubectl delete ns virtual4insanity`) para evitar que la regla de reenvío (USD 0.025/h) o el disco persistente queden huérfanos generando cargos.
4. **Variabilidad de precios Spot:**
   - Las tarifas de máquinas virtuales **Spot** en Google Cloud fluctúan según la oferta y demanda de capacidad en `us-central1-a` (con descuentos de entre el 60 % y el 91 % respecto a la tarifa bajo demanda).

---

## 7. Advertencia sobre los importes estimados

> **Aviso importante:**Todos los valores expresados en este documento están en dólares estadounidenses (**USD**) y constituyen una **estimación técnica preliminar** basada en las listas de precios públicas de Google Cloud para la región `us-central1` vigentes en noviembre de 2026. **No representan importes garantizados ni una cotización vinculante.** La facturación real dependerá del tiempo exacto de ejecución en segundos, la variación dinámica de las tarifas Spot, las cuotas del nivel gratuito disponibles en la cuenta de facturación vinculada y la correcta destrucción de los recursos al concluir la defensa.

---

## 8. Referencias oficiales consultadas

1. Google Cloud — *Google Kubernetes Engine (GKE) Pricing*: https://cloud.google.com/kubernetes-engine/pricing
2. Google Cloud — *Compute Engine VM Instance Pricing*: https://cloud.google.com/compute/vm-instance-pricing
3. Google Cloud — *Compute Engine Disks and Images Pricing*: https://cloud.google.com/compute/disks-image-pricing
4. Google Cloud — *Virtual Private Cloud (VPC) & Cloud Load Balancing Network Pricing*: https://cloud.google.com/vpc/network-pricing
5. Google Cloud — *Artifact Registry Pricing*: https://cloud.google.com/artifact-registry/pricing
