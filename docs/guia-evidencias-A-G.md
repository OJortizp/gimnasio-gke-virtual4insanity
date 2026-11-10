# Guía y Plantilla Maestra del Informe de Evidencias (Secciones A–G)

- **Proyecto:** Despliegue de una aplicación en la nube con Kubernetes e infraestructura como código
- **Caso asignado:** Caso 2 · Gimnasio (`api-miembros` y `api-clases`)
- **Proyecto de Google Cloud:** `gimnasio-virtual4insanity`
- **Identificador del equipo:** `virtual4insanity`
- **Clúster GKE:** `gke-virtual4insanity` (`us-central1-a`, Node Pool `pool-spot`)
- **Namespace:** `virtual4insanity`
- **Coordinadora de documentación y evidencias (Rol 5):** Susana Paola García García (`1224323`)

---

## 0. Reglas obligatorias de admisión para TODAS las capturas

De acuerdo con la sección 6 (*Requisitos de admisión*) del enunciado oficial del curso, **toda captura de pantalla incluida en el informe PDF debe cumplir estrictamente con lo siguiente**:

1. **Reloj del sistema visible:** La barra de tareas del sistema operativo (fecha y hora) debe aparecer completa y legible dentro del encuadre de la captura.
2. **Salida de `gcloud config list` visible:** En toda captura (incluso cuando se muestre el navegador web o un visor de código, colocando una ventana de terminal al lado) debe apreciarse la ejecución de `gcloud config list` mostrando la cuenta activa y el identificador del proyecto (`project = gimnasio-virtual4insanity`).
3. **Comandos y resultados completos y legibles:** Sin recortes que oculten el prompt, el comando ejecutado o el estado de los recursos.
4. **Orden estricto A a G:** El PDF final debe presentar las evidencias exactamente en el orden de los **30 criterios** de la lista de cotejo del Anexo B (100 puntos = 5 puntos grupales).
5. **Política de estados en esta guía:** Ningún criterio se marca como `Verificado` hasta contar con la captura real definitiva en `docs/evidencias/` que incluya `gcloud config list` y reloj del sistema. Los entregables cuyos archivos ya están integrados en `develop` se registran como `Preparado`, y los que requieren ejecución activa en GKE / Google Cloud como `Pendiente`.

---

## 1. Tabla de control general de los 30 criterios (100 puntos)

| Código | Criterio oficial (Anexo B) | Pts. | Rol responsable | Archivo de captura recomendado | Estado actual |
| :---: | :--- | :---: | :--- | :--- | :---: |
| **A1** | Entrega un repositorio Git con código, manifiestos y archivos `.tf`, con al menos 10 commits distribuidos en 3 días distintos. | 4 | Rol 5 · Susana García (`1224323`) | `docs/evidencias/A1-repositorio-commits.png` | `Preparado` |
| **A2** | Incluye un README con el caso asignado, los integrantes con carné y las instrucciones de despliegue. | 3 | Rol 5 · Susana García (`1224323`) | `docs/evidencias/A2-readme.png` | `Preparado` |
| **A3** | Presenta un diagrama de arquitectura propio que identifica frontend, microservicios, base de datos y punto de entrada público. | 3 | Rol 5 · Susana García (`1224323`) | `docs/evidencias/A3-diagrama-arquitectura.png` | `Preparado` |
| **A4** | Muestra el carné de cada integrante registrado en la base de datos y visible en la interfaz. | 2 | Rol 2 · Oscar Ortíz (`1182222`) y Rol 4 · Diego Orellana (`1163722`) | `docs/evidencias/A4-carnes-bd-interfaz.png` | `Pendiente` |
| **A5** | Nombra el clúster y el namespace con el identificador del equipo. | 2 | Rol 5 · Susana García (`1224323`) y Rol 1 · Rochelle Esquivel (`1283220`) | `docs/evidencias/A5-cluster-namespace.png` | `Preparado` *(manifiesto y `.tf` listos; captura en GKE pendiente)* |
| **B1** | Implementa el microservicio A con creación, consulta, actualización y eliminación sobre su entidad. | 5 | Rol 2 · Oscar Ortíz (`1182222`) | `docs/evidencias/B1-crud-miembros.png` | `Preparado` *(código listo; captura en vivo pendiente)* |
| **B2** | Implementa el microservicio B con creación, consulta, actualización y eliminación sobre su entidad. | 5 | Rol 3 · Diego Azurdia (`2528119`) | `docs/evidencias/B2-crud-clases.png` | `Preparado` *(código listo; captura en vivo pendiente)* |
| **B3** | Construye cada microservicio como contenedor independiente con su propio Dockerfile. | 3 | Rol 2 · Oscar Ortíz (`1182222`) y Rol 3 · Diego Azurdia (`2528119`) | `docs/evidencias/B3-dockerfiles-microservicios.png` | `Preparado` |
| **B4** | Opera el frontend contra ambos microservicios y muestra en pantalla los datos devueltos por los dos. | 5 | Rol 4 · Diego Orellana (`1163722`) | `docs/evidencias/B4-frontend-ambos-microservicios.png` | `Pendiente` |
| **C1** | Etiqueta las imágenes de frontend y de ambos microservicios con la ruta completa del repositorio de Artifact Registry. | 4 | Rol 3 · Diego Azurdia (`2528119`) (con Rol 2 y Rol 4) | `docs/evidencias/C1-etiquetado-imagenes.png` | `Pendiente` |
| **C2** | Publica las tres imágenes y demuestra su existencia con el listado del repositorio. | 3 | Rol 3 · Diego Azurdia (`2528119`) | `docs/evidencias/C2-listado-artifact-registry.png` | `Pendiente` *(actualizar `C2-repositorio.png` con las 4 imágenes)* |
| **C3** | Referencia en los manifiestos únicamente imágenes alojadas en Artifact Registry. | 3 | Rol 3 · Diego Azurdia (`2528119`) y Rol 5 · Susana García (`1224323`) | `docs/evidencias/C3-imagenes-manifiestos.png` | `Preparado` *(manifiestos listos; captura en GKE pendiente)* |
| **D1** | Versiona archivos `.tf` que declaran el clúster GKE, el node pool y el repositorio de Artifact Registry. | 5 | Rol 1 · Rochelle Esquivel (`1283220`) | `docs/evidencias/D1-archivos-terraform.png` | `Preparado` |
| **D2** | Parametriza con variables el identificador de proyecto, la zona y el nombre del clúster, sin valores sensibles escritos en el código. | 4 | Rol 1 · Rochelle Esquivel (`1283220`) | `docs/evidencias/D2-variables-terraform.png` | `Preparado` |
| **D3** | Presenta la salida de `terraform plan` previa a la creación de la infraestructura. | 3 | Rol 1 · Rochelle Esquivel (`1283220`) | `docs/evidencias/D3-terraform-plan.png` | `Pendiente` |
| **D4** | Presenta la salida de `terraform apply` con los recursos creados. | 3 | Rol 1 · Rochelle Esquivel (`1283220`) | `docs/evidencias/D4-terraform-apply.png` | `Pendiente` |
| **D5** | Levanta el node pool con nodos de tipo spot según lo declarado en el código. | 3 | Rol 1 · Rochelle Esquivel (`1283220`) | `docs/evidencias/D5-nodos-spot.png` | `Pendiente` |
| **E1** | Ejecuta todos los componentes como Deployments en estado Running, evidenciado con `kubectl get all` en el namespace del equipo. | 5 | Rol 5 · Susana García (`1224323`) | `docs/evidencias/E1-deployments-running.png` | `Pendiente` |
| **E2** | Inyecta configuración no sensible mediante ConfigMap y demuestra su consumo dentro de un pod. | 3 | Rol 4 · Diego Orellana (`1163722`) | `docs/evidencias/E2-configmap-pod.png` | `Pendiente` |
| **E3** | Inyecta credenciales mediante Secret y demuestra su consumo dentro de un pod. | 3 | Rol 2 · Oscar Ortíz (`1182222`) | `docs/evidencias/E3-secret-pod.png` | `Pendiente` |
| **E4** | Monta un PersistentVolumeClaim en la base de datos y conserva los datos tras eliminar el pod. | 5 | Rol 2 · Oscar Ortíz (`1182222`) | `docs/evidencias/E4-pvc-persistencia.png` | `Pendiente` |
| **E5** | Publica la aplicación con una dirección IP pública accesible desde un navegador externo al clúster. | 4 | Rol 4 · Diego Orellana (`1163722`) | `docs/evidencias/E5-ip-publica-navegador.png` | `Pendiente` |
| **E6** | Enruta el tráfico entre frontend y microservicios usando los nombres DNS de los Services. | 2 | Rol 4 · Diego Orellana (`1163722`) | `docs/evidencias/E6-enrutamiento-dns.png` | `Pendiente` |
| **F1** | Escala un microservicio a tres réplicas de forma declarativa y evidencia las réplicas en ejecución. | 3 | Rol 5 · Susana García (`1224323`) | `docs/evidencias/F1-escalado-tres-replicas.png` | `Pendiente` |
| **F2** | Elimina un pod y evidencia que el Deployment lo recrea automáticamente. | 2 | Rol 5 · Susana García (`1224323`) | `docs/evidencias/F2-autorrecuperacion-pod.png` | `Pendiente` |
| **F3** | Ejecuta una actualización de versión de imagen y evidencia el rolling update. | 3 | Rol 3 · Diego Azurdia (`2528119`) | `docs/evidencias/F3-rolling-update.png` | `Pendiente` |
| **F4** | Obtiene y muestra los logs de un pod de la aplicación. | 2 | Rol 3 · Diego Azurdia (`2528119`) | `docs/evidencias/F4-logs-pod.png` | `Pendiente` |
| **G1** | Presenta la estimación de costo mensual de la infraestructura declarada, elaborada antes del despliegue. | 3 | Rol 5 · Susana García (`1224323`) | `docs/evidencias/G1-estimacion-costo.png` | `Preparado` |
| **G2** | Ejecuta `terraform destroy` y presenta la salida con los recursos eliminados. | 3 | Rol 1 · Rochelle Esquivel (`1283220`) | `docs/evidencias/G2-terraform-destroy.png` | `Pendiente` |
| **G3** | Presenta la captura del panel de facturación con el gasto final. | 2 | Rol 1 · Rochelle Esquivel (`1283220`) | `docs/evidencias/G3-panel-facturacion.png` | `Pendiente` |
| **TOTAL** | **30 criterios evaluados** | **100** | **Equipo `virtual4insanity`** | **30 capturas numeradas (A1–G3)** | |

---

## SECCIÓN A. Entregables y trazabilidad (14 puntos)

### Criterio A1
1. **Código y nombre exacto del criterio:** `A1` — Entrega un repositorio Git con código, manifiestos y archivos `.tf`, con al menos 10 commits distribuidos en 3 días distintos.
2. **Puntaje correspondiente:** 4 puntos.
3. **Integrante responsable:** Susana Paola García García (`1224323` · Rol 5).
4. **Objetivo de la evidencia:** Demostrar que el repositorio contiene la totalidad del código fuente (`services/`, `frontend/`, `db/`), manifiestos YAML (`k8s/`) y archivos de Terraform (`terraform/`), y que el historial de commits registra más de 10 commits en al menos 3 fechas distintas.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   git log --oneline --date=short --pretty=format:"%h | %ad | %an | %s" -n 25
   git log --date=short --format="%ad" | sort -u
   ls terraform/ k8s/ db/ services/miembros/ services/clases/ frontend/
   ```
6. **Lugar exacto donde tomar la captura:** Terminal local situada en la raíz del repositorio `gimnasio-gke-virtual4insanity`, mostrando el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/A1-repositorio-commits.png`
8. **Descripción formal para el informe:**
   > **Figura A1.** Verificación del historial de control de versiones del repositorio Git del equipo `virtual4insanity` y estructura de directorios (`terraform/`, `k8s/`, `db/`, `services/` y `frontend/`), evidenciando más de 25 commits distribuidos en 8 días distintos junto con la configuración activa de `gcloud` para el proyecto `gimnasio-virtual4insanity`.
9. **Estado:** `Preparado` (todos los directorios y más de 25 commits en 8 fechas distintas ya están en el repositorio; falta únicamente tomar la captura con `gcloud config list` y reloj).
10. **Dependencias necesarias para completar la prueba:** Tener `gcloud config list` configurado con `project = gimnasio-virtual4insanity`.

---

### Criterio A2
1. **Código y nombre exacto del criterio:** `A2` — Incluye un README con el caso asignado, los integrantes con carné y las instrucciones de despliegue.
2. **Puntaje correspondiente:** 3 puntos.
3. **Integrante responsable:** Susana Paola García García (`1224323` · Rol 5).
4. **Objetivo de la evidencia:** Demostrar que el archivo [README.md](../README.md) principal documenta el Caso 2 (Gimnasio), la tabla de los 5 integrantes con su carné y la guía paso a paso de despliegue.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   head -n 45 README.md
   grep -n "^## " README.md
   ```
6. **Lugar exacto donde tomar la captura:** Pantalla dividida mostrando a la izquierda la vista renderizada de [README.md](../README.md) y a la derecha la terminal con `gcloud config list`, el índice de secciones de `README.md` y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/A2-readme.png`
8. **Descripción formal para el informe:**
   > **Figura A2.** Documento `README.md` principal del repositorio mostrando la descripción del Caso 2 (Sistema de Gestión de Gimnasio), la nómina oficial de los cinco integrantes con su número de carné y el índice completo de instrucciones de despliegue y operación en GKE.
9. **Estado:** `Preparado`.
10. **Dependencias necesarias para completar la prueba:** Tener `gcloud config list` configurado con `project = gimnasio-virtual4insanity`.

---

### Criterio A3
1. **Código y nombre exacto del criterio:** `A3` — Presenta un diagrama de arquitectura propio que identifica frontend, microservicios, base de datos y punto de entrada público.
2. **Puntaje correspondiente:** 3 puntos.
3. **Integrante responsable:** Susana Paola García García (`1224323` · Rol 5).
4. **Objetivo de la evidencia:** Presentar el diagrama de arquitectura propio del equipo ([docs/arquitectura.png](arquitectura.png)) donde se distinguen claramente el `Service` `LoadBalancer` público (puerto 80), el `frontend` (Flask + Gunicorn + Bootstrap 5), los microservicios `api-miembros` y `api-clases` (`ClusterIP`, puerto 5000), la base de datos `db` (PostgreSQL 16, `ClusterIP`, puerto 5432 con `db-pvc`), ConfigMaps (`frontend-config`, `gimnasio-config`, `db-init`), Secret (`gimnasio-secret`) y Artifact Registry.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   ls -lh docs/arquitectura.png docs/arquitectura.mmd
   ```
6. **Lugar exacto donde tomar la captura:** Imagen [docs/arquitectura.png](arquitectura.png) abierta a pantalla completa junto a una ventana de terminal mostrando `gcloud config list` y el reloj del sistema (además de insertar `docs/arquitectura.png` en alta resolución en la sección A3 del PDF).
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/A3-diagrama-arquitectura.png`
8. **Descripción formal para el informe:**
   > **Figura A3.** Diagrama de arquitectura propio del sistema distribuido de gestión de gimnasio en GKE (`gke-virtual4insanity`, namespace `virtual4insanity`), identificando el punto de entrada público (`LoadBalancer` puerto 80), el frontend web en Flask/Gunicorn, los microservicios `api-miembros` y `api-clases` (`ClusterIP` puerto 5000), la base de datos PostgreSQL (`ClusterIP` puerto 5432 con `db-pvc`) y Artifact Registry.
9. **Estado:** `Preparado`.
10. **Dependencias necesarias para completar la prueba:** Tener `gcloud config list` configurado con `project = gimnasio-virtual4insanity` para la captura acompañada del reloj.

---

### Criterio A4
1. **Código y nombre exacto del criterio:** `A4` — Muestra el carné de cada integrante registrado en la base de datos y visible en la interfaz.
2. **Puntaje correspondiente:** 2 puntos.
3. **Integrante responsable:** Oscar Javier Ortíz Pocón (`1182222` · Rol 2) y Diego Oswaldo Orellana Morales (`1163722` · Rol 4).
4. **Objetivo de la evidencia:** Demostrar que los 5 carnés del equipo (`1283220`, `1182222`, `2528119`, `1163722`, `1224323`) están almacenados en la tabla `integrantes` de PostgreSQL y son consultados y mostrados en la sección superior (*Integrantes del Equipo y Carnés*) de la interfaz web del frontend.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   kubectl exec -n virtual4insanity deploy/db -- psql -U gimnasio_user -d gimnasio -c "SELECT carne, nombre, rol FROM integrantes ORDER BY carne;"
   curl -s http://<EXTERNAL_IP>/api/miembros/integrantes
   ```
6. **Lugar exacto donde tomar la captura:** Pantalla dividida mostrando: (1) el navegador web en `http://<EXTERNAL_IP>` con las 5 tarjetas de integrantes y carnés visibles, y (2) la terminal con la consulta SQL directa en el pod `db`, `gcloud config list` y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/A4-carnes-bd-interfaz.png`
8. **Descripción formal para el informe:**
   > **Figura A4.** Comprobación de honestidad académica: registros de la tabla `integrantes` en PostgreSQL (`db`) con los números de carné de los cinco integrantes del equipo y su visualización simultánea en la interfaz web pública del sistema.
9. **Estado:** `Pendiente`.
10. **Dependencias necesarias para completar la prueba:** Clúster GKE en ejecución y componentes `db`, `api-miembros` y `frontend` desplegados.

---

### Criterio A5
1. **Código y nombre exacto del criterio:** `A5` — Nombra el clúster y el namespace con el identificador del equipo.
2. **Puntaje correspondiente:** 2 puntos.
3. **Integrante responsable:** Susana Paola García García (`1224323` · Rol 5) y Rochelle Giulianne Esquivel Vargas (`1283220` · Rol 1).
4. **Objetivo de la evidencia:** Evidenciar que el clúster de GKE se llama `gke-virtual4insanity` y que el namespace activo en Kubernetes se llama `virtual4insanity`.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   gcloud container clusters list
   cat k8s/00-namespace.yaml
   kubectl get namespace virtual4insanity --show-labels
   ```
6. **Lugar exacto donde tomar la captura:** Terminal ejecutando `gcloud config list`, `gcloud container clusters list` y `kubectl get namespace virtual4insanity --show-labels`, con el reloj del sistema visible.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/A5-cluster-namespace.png`
8. **Descripción formal para el informe:**
   > **Figura A5.** Verificación en Google Cloud y Kubernetes del clúster `gke-virtual4insanity` y del namespace `virtual4insanity`, ambos nombrados con el identificador oficial del equipo.
9. **Estado:** `Preparado` (manifiesto [k8s/00-namespace.yaml](../k8s/00-namespace.yaml) y [terraform/variables.tf](../terraform/variables.tf) listos; falta captura contra el clúster activo en GKE).
10. **Dependencias necesarias para completar la prueba:** Clúster `gke-virtual4insanity` activo en GKE y aplicación de `kubectl apply -f k8s/00-namespace.yaml`.

---

## SECCIÓN B. Aplicación construida desde cero (18 puntos)

### Criterio B1
1. **Código y nombre exacto del criterio:** `B1` — Implementa el microservicio A con creación, consulta, actualización y eliminación sobre su entidad.
2. **Puntaje correspondiente:** 5 puntos.
3. **Integrante responsable:** Oscar Javier Ortíz Pocón (`1182222` · Rol 2).
4. **Objetivo de la evidencia:** Demostrar las 4 operaciones CRUD (`POST`, `GET`, `PUT`, `DELETE`) del microservicio `api-miembros` sobre la entidad `miembros`.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   # Crear miembro (POST -> 201)
   curl -i -X POST http://<EXTERNAL_IP>/api/miembros -H "Content-Type: application/json" -d '{"nombre":"Pedro Alvarado","correo":"pedro@correo.com","telefono":"5555-1111","membresia":"Mensual","carne_registro":"1182222"}'
   # Consultar miembros (GET -> 200)
   curl -s http://<EXTERNAL_IP>/api/miembros
   # Actualizar miembro (PUT -> 200)
   curl -i -X PUT http://<EXTERNAL_IP>/api/miembros/4 -H "Content-Type: application/json" -d '{"nombre":"Pedro Alvarado","correo":"pedro@correo.com","telefono":"5555-2222","membresia":"Anual","carne_registro":"1182222"}'
   # Eliminar miembro (DELETE -> 200)
   curl -i -X DELETE http://<EXTERNAL_IP>/api/miembros/4
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando la ejecución secuencial de creación, consulta, actualización y eliminación de un miembro en `api-miembros` a través de `http://<EXTERNAL_IP>/api/miembros`, junto con `gcloud config list` y reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/B1-crud-miembros.png`
8. **Descripción formal para el informe:**
   > **Figura B1.** Prueba funcional de las operaciones de creación (`POST`), consulta (`GET`), actualización (`PUT`) y eliminación (`DELETE`) en el microservicio A (`api-miembros`) sobre la entidad `miembros`.
9. **Estado:** `Preparado` (código implementado en [services/miembros/app.py](../services/miembros/app.py); pendiente captura con el servicio desplegado en GKE).
10. **Dependencias necesarias para completar la prueba:** `db`, `api-miembros` y `frontend` en ejecución en GKE.

---

### Criterio B2
1. **Código y nombre exacto del criterio:** `B2` — Implementa el microservicio B con creación, consulta, actualización y eliminación sobre su entidad.
2. **Puntaje correspondiente:** 5 puntos.
3. **Integrante responsable:** Diego Andrés Azurdia Ortíz (`2528119` · Rol 3).
4. **Objetivo de la evidencia:** Demostrar las 4 operaciones CRUD (`POST`, `GET`, `PUT`, `DELETE`) del microservicio `api-clases` sobre la entidad `clases`, incluyendo la validación de `miembro_id` contra `api-miembros`.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   # Crear clase (POST -> 201)
   curl -i -X POST http://<EXTERNAL_IP>/api/clases -H "Content-Type: application/json" -d '{"nombre":"Boxeo","instructor":"Mario Estrada","fecha":"2026-11-11","hora":"19:00","cupo":15,"miembro_id":1,"carne_registro":"2528119"}'
   # Consultar clases (GET -> 200)
   curl -s http://<EXTERNAL_IP>/api/clases
   # Actualizar clase (PUT -> 200)
   curl -i -X PUT http://<EXTERNAL_IP>/api/clases/4 -H "Content-Type: application/json" -d '{"nombre":"Boxeo Avanzado","instructor":"Mario Estrada","fecha":"2026-11-11","hora":"20:00","cupo":12,"miembro_id":1,"carne_registro":"2528119"}'
   # Eliminar clase (DELETE -> 200)
   curl -i -X DELETE http://<EXTERNAL_IP>/api/clases/4
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando la ejecución de creación, consulta, actualización y eliminación sobre `api-clases`, junto con `gcloud config list` y reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/B2-crud-clases.png`
8. **Descripción formal para el informe:**
   > **Figura B2.** Prueba funcional de las operaciones de creación (`POST`), consulta (`GET`), actualización (`PUT`) y eliminación (`DELETE`) en el microservicio B (`api-clases`) sobre la entidad `clases`, verificando la existencia del miembro asociado en `api-miembros`.
9. **Estado:** `Preparado` (código implementado en [services/clases/app.py](../services/clases/app.py); pendiente captura en ejecución en GKE).
10. **Dependencias necesarias para completar la prueba:** `db`, `api-miembros`, `api-clases` y `frontend` desplegados en GKE.

---

### Criterio B3
1. **Código y nombre exacto del criterio:** `B3` — Construye cada microservicio como contenedor independiente con su propio Dockerfile.
2. **Puntaje correspondiente:** 3 puntos.
3. **Integrante responsable:** Oscar Javier Ortíz Pocón (`1182222` · Rol 2) y Diego Andrés Azurdia Ortíz (`2528119` · Rol 3).
4. **Objetivo de la evidencia:** Demostrar que [services/miembros/Dockerfile](../services/miembros/Dockerfile) y [services/clases/Dockerfile](../services/clases/Dockerfile) existen por separado y construyen contenedores independientes para cada microservicio.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   cat services/miembros/Dockerfile
   cat services/clases/Dockerfile
   docker build -t us-central1-docker.pkg.dev/gimnasio-virtual4insanity/gimnasio/api-miembros:v1 ./services/miembros
   docker build -t us-central1-docker.pkg.dev/gimnasio-virtual4insanity/gimnasio/api-clases:v1 ./services/clases
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando el contenido de ambos `Dockerfile` y la salida exitosa de `docker build` para cada microservicio independiente, con `gcloud config list` y reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/B3-dockerfiles-microservicios.png`
8. **Descripción formal para el informe:**
   > **Figura B3.** Archivos `Dockerfile` independientes de `services/miembros/` y `services/clases/` basados en `python:3.12-slim` y Gunicorn, junto con la construcción exitosa de ambos contenedores de forma aislada.
9. **Estado:** `Preparado`.
10. **Dependencias necesarias para completar la prueba:** Tomar la captura de construcción con `gcloud config list` activo.

---

### Criterio B4
1. **Código y nombre exacto del criterio:** `B4` — Opera el frontend contra ambos microservicios y muestra en pantalla los datos devueltos por los dos.
2. **Puntaje correspondiente:** 5 puntos.
3. **Integrante responsable:** Diego Oswaldo Orellana Morales (`1163722` · Rol 4).
4. **Objetivo de la evidencia:** Demostrar que el frontend web ([frontend/app.py](../frontend/app.py) + [frontend/templates/index.html](../frontend/templates/index.html)) consume tanto `api-miembros` como `api-clases` y renderiza en pantalla las tablas de *Miembros Registrados* y *Clases Programadas*.
5. **Comandos o procedimiento para verificar el requisito:**
   - Abrir en un navegador `http://<EXTERNAL_IP>` mostrando simultáneamente las tablas de *Miembros Registrados* y *Clases Programadas* pobladas con los datos devueltos por ambos microservicios.
   - En una ventana lateral de terminal, mostrar `gcloud config list` y `kubectl logs -l app=frontend -n virtual4insanity --tail=10`.
6. **Lugar exacto donde tomar la captura:** Navegador web en `http://<EXTERNAL_IP>` junto con la terminal mostrando `gcloud config list` y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/B4-frontend-ambos-microservicios.png`
8. **Descripción formal para el informe:**
   > **Figura B4.** Interfaz web del frontend operando en vivo contra los microservicios `api-miembros` y `api-clases`, mostrando en pantalla los registros de miembros inscritos y clases programadas devueltos por ambos servicios.
9. **Estado:** `Pendiente`.
10. **Dependencias necesarias para completar la prueba:** Despliegue de `db`, `api-miembros`, `api-clases` y `frontend` en GKE.

---

## SECCIÓN C. Publicación de imágenes (10 puntos)

### Criterio C1
1. **Código y nombre exacto del criterio:** `C1` — Etiqueta las imágenes de frontend y de ambos microservicios con la ruta completa del repositorio de Artifact Registry.
2. **Puntaje correspondiente:** 4 puntos.
3. **Integrante responsable:** Diego Andrés Azurdia Ortíz (`2528119` · Rol 3), en coordinación con Rol 2 y Rol 4.
4. **Objetivo de la evidencia:** Demostrar que las imágenes fueron etiquetadas con el prefijo completo `us-central1-docker.pkg.dev/gimnasio-virtual4insanity/gimnasio/<imagen>:v1` (sin usar `latest`).
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   docker images --filter=reference="us-central1-docker.pkg.dev/gimnasio-virtual4insanity/gimnasio/*"
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando `gcloud config list`, los comandos `docker build -t` / `docker tag` y la tabla de `docker images` con las rutas completas de Artifact Registry y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/C1-etiquetado-imagenes.png`
8. **Descripción formal para el informe:**
   > **Figura C1.** Etiquetado de las imágenes de contenedores (`frontend:v1`, `api-miembros:v1`, `api-clases:v1` y `postgres:16-alpine`) utilizando la ruta completa del repositorio `gimnasio` en Google Artifact Registry (`us-central1-docker.pkg.dev/gimnasio-virtual4insanity/gimnasio`).
9. **Estado:** `Pendiente`.
10. **Dependencias necesarias para completar la prueba:** Imágenes construidas localmente y `gcloud config list` activo.

---

### Criterio C2
1. **Código y nombre exacto del criterio:** `C2` — Publica las tres imágenes y demuestra su existencia con el listado del repositorio.
2. **Puntaje correspondiente:** 3 puntos.
3. **Integrante responsable:** Diego Andrés Azurdia Ortíz (`2528119` · Rol 3).
4. **Objetivo de la evidencia:** Demostrar mediante `gcloud artifacts docker images list` que las imágenes de `frontend`, `api-miembros`, `api-clases` y `postgres` están publicadas en el repositorio `gimnasio` de Artifact Registry. *(Nota: reemplazar o complementar `docs/evidencias/C2-repositorio.png` para que aparezcan las 4 imágenes con `--include-tags`).*
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   gcloud artifacts docker images list us-central1-docker.pkg.dev/gimnasio-virtual4insanity/gimnasio --include-tags
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando la salida de `gcloud artifacts docker images list ... --include-tags` con las 4 imágenes (`frontend:v1`, `api-miembros:v1`, `api-clases:v1`/`v2`, `postgres:16-alpine`), junto con `gcloud config list` y reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/C2-listado-artifact-registry.png`
8. **Descripción formal para el informe:**
   > **Figura C2.** Listado oficial del repositorio `gimnasio` en Google Artifact Registry (`us-central1`) obtenido con `gcloud artifacts docker images list`, confirmando la publicación de las imágenes del sistema (`frontend`, `api-miembros`, `api-clases` y `postgres`).
9. **Estado:** `Pendiente` (la captura actual [docs/evidencias/C2-repositorio.png](evidencias/C2-repositorio.png) solo muestra `api-clases` y `postgres`; debe actualizarse cuando estén subidas también `api-miembros:v1` y `frontend:v1`).
10. **Dependencias necesarias para completar la prueba:** `docker push` ejecutado para las 4 imágenes en `us-central1-docker.pkg.dev/gimnasio-virtual4insanity/gimnasio`.

---

### Criterio C3
1. **Código y nombre exacto del criterio:** `C3` — Referencia en los manifiestos únicamente imágenes alojadas en Artifact Registry.
2. **Puntaje correspondiente:** 3 puntos.
3. **Integrante responsable:** Diego Andrés Azurdia Ortíz (`2528119` · Rol 3) y Susana Paola García García (`1224323` · Rol 5).
4. **Objetivo de la evidencia:** Demostrar que todos los campos `image:` dentro de `k8s/*.yaml` apuntan exclusivamente a `us-central1-docker.pkg.dev/gimnasio-virtual4insanity/gimnasio/...` (incluyendo PostgreSQL).
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   grep -rn "image:" k8s/
   kubectl get pods -n virtual4insanity -o custom-columns="POD:.metadata.name,IMAGE:.spec.containers[*].image"
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando el resultado de `grep -rn "image:" k8s/` y las imágenes en uso por los pods en el clúster, junto con `gcloud config list` y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/C3-imagenes-manifiestos.png`
8. **Descripción formal para el informe:**
   > **Figura C3.** Verificación de los manifiestos YAML en `k8s/` y de los pods en ejecución, comprobando que la totalidad de los contenedores (`db`, `api-miembros`, `api-clases` y `frontend`) utilizan únicamente imágenes alojadas en Artifact Registry con versiones explícitas.
9. **Estado:** `Preparado` (los 4 manifiestos `10-db.yaml`, `20-api-miembros.yaml`, `30-api-clases.yaml` y `40-frontend.yaml` ya tienen configurada la ruta de Artifact Registry; falta la captura en GKE).
10. **Dependencias necesarias para completar la prueba:** Pods desplegados en el clúster GKE.

---

## SECCIÓN D. Infraestructura como código (18 puntos)

### Criterio D1
1. **Código y nombre exacto del criterio:** `D1` — Versiona archivos `.tf` que declaran el clúster GKE, el node pool y el repositorio de Artifact Registry.
2. **Puntaje correspondiente:** 5 puntos.
3. **Integrante responsable:** Rochelle Giulianne Esquivel Vargas (`1283220` · Rol 1).
4. **Objetivo de la evidencia:** Mostrar los archivos versionados en `terraform/` ([main.tf](../terraform/main.tf), [outputs.tf](../terraform/outputs.tf)) donde se declaran `google_container_cluster.gke`, `google_container_node_pool.spot` (`pool-spot`) y `google_artifact_registry_repository.gimnasio`.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   git ls-files terraform/
   cat terraform/main.tf
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando `gcloud config list`, los archivos `.tf` versionados en Git y los bloques `resource` en [terraform/main.tf](../terraform/main.tf), con el reloj del sistema visible.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/D1-archivos-terraform.png`
8. **Descripción formal para el informe:**
   > **Figura D1.** Archivos de Terraform versionados en el directorio `terraform/`, declarando el clúster GKE Standard zonal (`gke-virtual4insanity`), el node pool `pool-spot` administrado por separado y el repositorio Docker `gimnasio` en Artifact Registry.
9. **Estado:** `Preparado` (archivos `.tf` ya integrados en el repositorio; falta captura con `gcloud config list`).
10. **Dependencias necesarias para completar la prueba:** Tomar la captura con `gcloud config list` y reloj del sistema.

---

### Criterio D2
1. **Código y nombre exacto del criterio:** `D2` — Parametriza con variables el identificador de proyecto, la zona y el nombre del clúster, sin valores sensibles escritos en el código.
2. **Puntaje correspondiente:** 4 puntos.
3. **Integrante responsable:** Rochelle Giulianne Esquivel Vargas (`1283220` · Rol 1).
4. **Objetivo de la evidencia:** Demostrar en [terraform/variables.tf](../terraform/variables.tf) y [terraform/terraform.tfvars.example](../terraform/terraform.tfvars.example) la parametrización de `project_id`, `region`, `zone` y `cluster_name`, y que [.gitignore](../.gitignore) excluye `*.tfvars` y credenciales JSON.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   cat terraform/variables.tf
   cat terraform/terraform.tfvars.example
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando el contenido de [terraform/variables.tf](../terraform/variables.tf) y [terraform/terraform.tfvars.example](../terraform/terraform.tfvars.example), junto con `gcloud config list` y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/D2-variables-terraform.png`
8. **Descripción formal para el informe:**
   > **Figura D2.** Parametrización mediante variables en `terraform/variables.tf` para el identificador del proyecto (`project_id`), la región/zona (`us-central1` / `us-central1-a`) y el nombre del clúster (`gke-virtual4insanity`), verificando la ausencia de credenciales o datos sensibles en el código versionado.
9. **Estado:** `Preparado` (archivos ya integrados en el repositorio; falta captura con `gcloud config list`).
10. **Dependencias necesarias para completar la prueba:** Tomar la captura con `gcloud config list` y reloj del sistema.

---

### Criterio D3
1. **Código y nombre exacto del criterio:** `D3` — Presenta la salida de `terraform plan` previa a la creación de la infraestructura.
2. **Puntaje correspondiente:** 3 puntos.
3. **Integrante responsable:** Rochelle Giulianne Esquivel Vargas (`1283220` · Rol 1).
4. **Objetivo de la evidencia:** Mostrar la ejecución de `terraform plan` donde Terraform proyecta la creación de los recursos antes de ejecutar el `apply`.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   cd terraform && terraform plan
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando la salida de `terraform plan` (con el resumen `Plan: ... to add, 0 to change, 0 to destroy`), `gcloud config list` y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/D3-terraform-plan.png`
8. **Descripción formal para el informe:**
   > **Figura D3.** Salida de `terraform plan` ejecutada antes del aprovisionamiento en Google Cloud, detallando los recursos programados para creación (clúster GKE `gke-virtual4insanity`, node pool `pool-spot` y repositorio `gimnasio` en Artifact Registry).
9. **Estado:** `Pendiente`.
10. **Dependencias necesarias para completar la prueba:** Captura tomada por Rochelle (Rol 1) durante la ejecución de Terraform en el proyecto `gimnasio-virtual4insanity`.

---

### Criterio D4
1. **Código y nombre exacto del criterio:** `D4` — Presenta la salida de `terraform apply` con los recursos creados.
2. **Puntaje correspondiente:** 3 puntos.
3. **Integrante responsable:** Rochelle Giulianne Esquivel Vargas (`1283220` · Rol 1).
4. **Objetivo de la evidencia:** Mostrar la finalización exitosa de `terraform apply` (`Apply complete!`) y los outputs definidos en [terraform/outputs.tf](../terraform/outputs.tf) (`cluster_name`, `cluster_location`, `node_machine_type`, `nodes_are_spot`, `registry_path`, `get_credentials_command`).
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   cd terraform && terraform apply
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando la salida de `terraform apply` con el mensaje `Apply complete!` y los outputs generados, junto con `gcloud config list` y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/D4-terraform-apply.png`
8. **Descripción formal para el informe:**
   > **Figura D4.** Ejecución exitosa de `terraform apply` confirmando la creación en Google Cloud del clúster `gke-virtual4insanity`, el node pool `pool-spot` de 2 nodos `e2-small` y el repositorio `gimnasio` en Artifact Registry.
9. **Estado:** `Pendiente`.
10. **Dependencias necesarias para completar la prueba:** Captura tomada por Rochelle (Rol 1) al completar `terraform apply`.

---

### Criterio D5
1. **Código y nombre exacto del criterio:** `D5` — Levanta el node pool con nodos de tipo spot según lo declarado en el código.
2. **Puntaje correspondiente:** 3 puntos.
3. **Integrante responsable:** Rochelle Giulianne Esquivel Vargas (`1283220` · Rol 1).
4. **Objetivo de la evidencia:** Demostrar que el node pool `pool-spot` activo en GKE cuenta con 2 nodos de tipo de máquina `e2-small` y aprovisionamiento `Spot` (`spot: true` / `cloud.google.com/gke-spot=true`).
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   gcloud container node-pools describe pool-spot --cluster gke-virtual4insanity --zone us-central1-a --format="yaml(name,initialNodeCount,config.machineType,config.spot,config.diskSizeGb,config.diskType)"
   kubectl get nodes -L cloud.google.com/gke-spot,node.kubernetes.io/instance-type -o wide
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando la salida de `gcloud container node-pools describe pool-spot` y `kubectl get nodes -L ...` confirmando 2 nodos `e2-small` con `spot: true`, junto con `gcloud config list` y reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/D5-nodos-spot.png`
8. **Descripción formal para el informe:**
   > **Figura D5.** Verificación técnica del node pool `pool-spot` en GKE mediante `gcloud` y `kubectl`, confirmando la ejecución de 2 nodos con tipo de máquina `e2-small` y modelo de aprovisionamiento `Spot`.
9. **Estado:** `Pendiente`.
10. **Dependencias necesarias para completar la prueba:** Clúster `gke-virtual4insanity` en ejecución (Rol 1).

---

## SECCIÓN E. Despliegue en GKE (22 puntos)

### Criterio E1
1. **Código y nombre exacto del criterio:** `E1` — Ejecuta todos los componentes como Deployments en estado Running, evidenciado con `kubectl get all` en el namespace del equipo.
2. **Puntaje correspondiente:** 5 puntos.
3. **Integrante responsable:** Susana Paola García García (`1224323` · Rol 5) *(ejecución en GKE coordinada con Rochelle, Rol 1)*.
4. **Objetivo de la evidencia:** Aplicar los manifiestos de `k8s/` en orden y demostrar con `kubectl get all -n virtual4insanity` que los 4 Deployments (`db`, `api-miembros`, `api-clases` y `frontend`) tienen sus pods en estado `Running` (`1/1`), sus ReplicaSets listos y sus Services activos (con `EXTERNAL-IP` asignada en `service/frontend`).
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   kubectl apply -f k8s/00-namespace.yaml
   kubectl apply -f k8s/01-configmap.yaml
   kubectl apply -f k8s/secret.yaml
   kubectl apply -f k8s/10-db.yaml
   kubectl apply -f k8s/20-api-miembros.yaml
   kubectl apply -f k8s/30-api-clases.yaml
   kubectl apply -f k8s/40-frontend.yaml
   kubectl get all -n virtual4insanity
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando `gcloud config list` y la salida íntegra de `kubectl get all -n virtual4insanity` (con los 4 pods en `1/1 Running`, los 4 Services, los 4 Deployments y los 4 ReplicaSets), junto con el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/E1-deployments-running.png`
8. **Descripción formal para el informe:**
   > **Figura E1.** Salida del comando `kubectl get all -n virtual4insanity` evidenciando que todos los componentes del sistema (`db`, `api-miembros`, `api-clases` y `frontend`) se ejecutan como Deployments con sus pods en estado `Running` (`1/1`).
9. **Estado:** `Pendiente`.
10. **Dependencias necesarias para completar la prueba:** Clúster GKE activo y las 4 imágenes publicadas en Artifact Registry.

---

### Criterio E2
1. **Código y nombre exacto del criterio:** `E2` — Inyecta configuración no sensible mediante ConfigMap y demuestra su consumo dentro de un pod.
2. **Puntaje correspondiente:** 3 puntos.
3. **Integrante responsable:** Diego Oswaldo Orellana Morales (`1163722` · Rol 4).
4. **Objetivo de la evidencia:** Demostrar la existencia de los `ConfigMap` `gimnasio-config` y `frontend-config` en el namespace `virtual4insanity` y verificar dentro de los pods en ejecución que las variables no sensibles (`DB_HOST`, `DB_PORT`, `DB_NAME`, `MIEMBROS_URL`, `CLASES_URL`, `EQUIPO`) fueron inyectadas en su entorno.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   kubectl describe configmap gimnasio-config frontend-config -n virtual4insanity
   kubectl exec -n virtual4insanity deploy/api-miembros -- printenv DB_HOST DB_PORT DB_NAME MIEMBROS_URL EQUIPO
   kubectl exec -n virtual4insanity deploy/frontend -- printenv MIEMBROS_URL CLASES_URL
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando `kubectl describe configmap` y la salida de `kubectl exec ... printenv` dentro de los pods, con `gcloud config list` y reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/E2-configmap-pod.png`
8. **Descripción formal para el informe:**
   > **Figura E2.** Inspección de los `ConfigMap` `gimnasio-config` y `frontend-config` en el namespace `virtual4insanity` y comprobación de su consumo efectivo como variables de entorno dentro de los pods en ejecución.
9. **Estado:** `Pendiente`.
10. **Dependencias necesarias para completar la prueba:** Pods `api-miembros` y `frontend` en ejecución en GKE.

---

### Criterio E3
1. **Código y nombre exacto del criterio:** `E3` — Inyecta credenciales mediante Secret y demuestra su consumo dentro de un pod.
2. **Puntaje correspondiente:** 3 puntos.
3. **Integrante responsable:** Oscar Javier Ortíz Pocón (`1182222` · Rol 2).
4. **Objetivo de la evidencia:** Demostrar la existencia del `Secret` `gimnasio-secret` (`Opaque`) en el namespace `virtual4insanity` y comprobar dentro de un pod en ejecución que las credenciales (`DB_USER`, `DB_PASSWORD`) están inyectadas y permiten autenticar contra PostgreSQL.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   kubectl get secret gimnasio-secret -n virtual4insanity
   kubectl describe secret gimnasio-secret -n virtual4insanity
   kubectl exec -n virtual4insanity deploy/api-miembros -- sh -c 'echo "DB_USER=$DB_USER | DB_PASSWORD_LEN=${#DB_PASSWORD}"'
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando `kubectl describe secret gimnasio-secret` y la comprobación de las variables inyectadas dentro del pod, con `gcloud config list` y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/E3-secret-pod.png`
8. **Descripción formal para el informe:**
   > **Figura E3.** Verificación del objeto `Secret` `gimnasio-secret` en el namespace `virtual4insanity` y demostración de su inyección segura en el entorno de ejecución de los pods para la autenticación ante PostgreSQL.
9. **Estado:** `Pendiente`.
10. **Dependencias necesarias para completar la prueba:** `k8s/secret.yaml` aplicado en el clúster GKE y pods en ejecución.

---

### Criterio E4
1. **Código y nombre exacto del criterio:** `E4` — Monta un PersistentVolumeClaim en la base de datos y conserva los datos tras eliminar el pod.
2. **Puntaje correspondiente:** 5 puntos.
3. **Integrante responsable:** Oscar Javier Ortíz Pocón (`1182222` · Rol 2).
4. **Objetivo de la evidencia:** Demostrar que `db-pvc` está en estado `Bound` montado en `/var/lib/postgresql/data`, que al insertar un miembro nuevo, eliminar el pod `db` (`kubectl delete pod -l app=db`) y esperar a que el nuevo pod `db` arranque, el registro insertado permanece intacto.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   kubectl get pvc db-pvc -n virtual4insanity
   # 1. Insertar o verificar registro en miembros antes de borrar el pod db
   curl -s http://<EXTERNAL_IP>/api/miembros
   # 2. Eliminar el pod de la base de datos
   kubectl get pods -l app=db -n virtual4insanity
   kubectl delete pod -l app=db -n virtual4insanity
   kubectl wait --for=condition=ready pod -l app=db -n virtual4insanity --timeout=90s
   kubectl get pods -l app=db -n virtual4insanity
   # 3. Consultar nuevamente y comprobar que los datos persisten en el nuevo pod
   curl -s http://<EXTERNAL_IP>/api/miembros
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando el PVC en `Bound`, los datos antes de borrar el pod `db`, la eliminación y recreación del pod `db` (con nuevo nombre y `AGE` reciente) y la consulta posterior confirmando que los datos se conservaron, con `gcloud config list` y reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/E4-pvc-persistencia.png`
8. **Descripción formal para el informe:**
   > **Figura E4.** Prueba de persistencia de datos en PostgreSQL mediante el `PersistentVolumeClaim` `db-pvc` (`1Gi`, `Bound`): se verifica la conservación íntegra de los registros tras eliminar el pod de base de datos y esperar su recreación automática.
9. **Estado:** `Pendiente`.
10. **Dependencias necesarias para completar la prueba:** `k8s/10-db.yaml` y `k8s/20-api-miembros.yaml` desplegados en el clúster GKE.

---

### Criterio E5
1. **Código y nombre exacto del criterio:** `E5` — Publica la aplicación con una dirección IP pública accesible desde un navegador externo al clúster.
2. **Puntaje correspondiente:** 4 puntos.
3. **Integrante responsable:** Diego Oswaldo Orellana Morales (`1163722` · Rol 4).
4. **Objetivo de la evidencia:** Mostrar el `Service` `frontend` de tipo `LoadBalancer` con su `EXTERNAL-IP` pública asignada y el navegador web externo cargando la aplicación en `http://<EXTERNAL_IP>`.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   kubectl get service frontend -n virtual4insanity -o wide
   ```
6. **Lugar exacto donde tomar la captura:** Pantalla mostrando en paralelo la terminal con `kubectl get service frontend -n virtual4insanity` (evidenciando la `EXTERNAL-IP` pública) y el navegador web abierto exactamente en `http://<EXTERNAL_IP>` (barra de direcciones visible), junto con `gcloud config list` y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/E5-ip-publica-navegador.png`
8. **Descripción formal para el informe:**
   > **Figura E5.** Exposición pública del sistema a través del `Service` `frontend` (`type: LoadBalancer`) con dirección IPv4 pública externa asignada en GKE y acceso verificado desde un navegador web externo.
9. **Estado:** `Pendiente`.
10. **Dependencias necesarias para completar la prueba:** Manifiesto [k8s/40-frontend.yaml](../k8s/40-frontend.yaml) e imagen `frontend:v1` desplegados en GKE.

---

### Criterio E6
1. **Código y nombre exacto del criterio:** `E6` — Enruta el tráfico entre frontend y microservicios usando los nombres DNS de los Services.
2. **Puntaje correspondiente:** 2 puntos.
3. **Integrante responsable:** Diego Oswaldo Orellana Morales (`1163722` · Rol 4).
4. **Objetivo de la evidencia:** Demostrar que el contenedor `frontend` ([frontend/app.py](../frontend/app.py)) se comunica con los microservicios exclusivamente mediante los nombres DNS de sus Services (`http://api-miembros:5000` y `http://api-clases:5000`) inyectados desde el `ConfigMap` `frontend-config`, y nunca mediante direcciones IP de pods.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   kubectl get svc -n virtual4insanity
   kubectl exec -n virtual4insanity deploy/frontend -- printenv MIEMBROS_URL CLASES_URL
   curl -i http://<EXTERNAL_IP>/api/miembros/health
   curl -i http://<EXTERNAL_IP>/api/clases/health
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando los `Services` en el namespace `virtual4insanity`, las variables `MIEMBROS_URL=http://api-miembros:5000` y `CLASES_URL=http://api-clases:5000` dentro del pod `frontend` y las respuestas HTTP 200 de `/api/miembros/health` y `/api/clases/health` a través del frontend, junto con `gcloud config list` y reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/E6-enrutamiento-dns.png`
8. **Descripción formal para el informe:**
   > **Figura E6.** Verificación del enrutamiento interno entre el contenedor `frontend` y los microservicios empleando exclusivamente los nombres DNS de los Services de Kubernetes (`http://api-miembros:5000` y `http://api-clases:5000`).
9. **Estado:** `Pendiente`.
10. **Dependencias necesarias para completar la prueba:** `frontend`, `api-miembros` y `api-clases` desplegados en GKE.

---

## SECCIÓN F. Operación (10 puntos)

### Criterio F1
1. **Código y nombre exacto del criterio:** `F1` — Escala un microservicio a tres réplicas de forma declarativa y evidencia las réplicas en ejecución.
2. **Puntaje correspondiente:** 3 puntos.
3. **Integrante responsable:** Susana Paola García García (`1224323` · Rol 5) *(ejecución en GKE coordinada con Rochelle, Rol 1)*.
4. **Objetivo de la evidencia:** Demostrar el cambio declarativo `replicas: 3` en el manifiesto YAML del microservicio ([k8s/20-api-miembros.yaml](../k8s/20-api-miembros.yaml)), la ejecución de `kubectl apply -f k8s/20-api-miembros.yaml` y la comprobación de las 3 réplicas en estado `Running` (`3/3`).
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   # tras cambiar spec.replicas: 3 en k8s/20-api-miembros.yaml
   grep -n -C 3 "replicas:" k8s/20-api-miembros.yaml
   kubectl apply -f k8s/20-api-miembros.yaml
   kubectl rollout status deployment/api-miembros -n virtual4insanity
   kubectl get deployment api-miembros -n virtual4insanity
   kubectl get pods -l app=api-miembros -n virtual4insanity -o wide
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando la línea `replicas: 3` en `k8s/20-api-miembros.yaml`, el comando `kubectl apply -f k8s/20-api-miembros.yaml`, el Deployment con `READY 3/3` y los 3 pods en estado `Running` (`1/1`), junto con `gcloud config list` y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/F1-escalado-tres-replicas.png`
8. **Descripción formal para el informe:**
   > **Figura F1.** Escalado horizontal declarativo del microservicio `api-miembros` a 3 réplicas mediante la modificación de `spec.replicas: 3` en `k8s/20-api-miembros.yaml` y aplicación con `kubectl apply`, evidenciando las tres instancias en estado `Running`.
9. **Estado:** `Pendiente` (requiere clúster GKE en ejecución).
10. **Dependencias necesarias para completar la prueba:** Clúster GKE activo e imagen `api-miembros:v1` desplegada.

---

### Criterio F2
1. **Código y nombre exacto del criterio:** `F2` — Elimina un pod y evidencia que el Deployment lo recrea automáticamente.
2. **Puntaje correspondiente:** 2 puntos.
3. **Integrante responsable:** Susana Paola García García (`1224323` · Rol 5) *(ejecución en GKE coordinada con Rochelle, Rol 1)*.
4. **Objetivo de la evidencia:** Demostrar la capacidad de autorrecuperación (*self-healing*) de Kubernetes eliminando manualmente un pod con `kubectl delete pod` y mostrando que el controlador del Deployment crea de inmediato un nuevo pod de reemplazo en estado `Running`.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   kubectl get pods -l app=api-miembros -n virtual4insanity -o wide
   kubectl delete pod <NOMBRE_POD_A_ELIMINAR> -n virtual4insanity
   kubectl get pods -l app=api-miembros -n virtual4insanity -o wide
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando en una sola secuencia: el listado de pods previo, el comando `kubectl delete pod <nombre>` y el listado posterior donde aparece el nuevo pod con un sufijo aleatorio distinto y `AGE` de pocos segundos en estado `Running`, junto con `gcloud config list` y reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/F2-autorrecuperacion-pod.png`
8. **Descripción formal para el informe:**
   > **Figura F2.** Prueba de autorrecuperación (*self-healing*): tras eliminar manualmente un pod del microservicio con `kubectl delete pod`, el ReplicaSet controlado por el Deployment instancia automáticamente un nuevo pod hasta restablecer las réplicas declaradas en estado `Running`.
9. **Estado:** `Pendiente` (requiere clúster GKE en ejecución).
10. **Dependencias necesarias para completar la prueba:** Clúster GKE activo y Deployment en ejecución.

---

### Criterio F3
1. **Código y nombre exacto del criterio:** `F3` — Ejecuta una actualización de versión de imagen y evidencia el rolling update.
2. **Puntaje correspondiente:** 3 puntos.
3. **Integrante responsable:** Diego Andrés Azurdia Ortíz (`2528119` · Rol 3).
4. **Objetivo de la evidencia:** Demostrar la actualización sin tiempo de inactividad (*rolling update*) cambiando la versión de la imagen en [k8s/30-api-clases.yaml](../k8s/30-api-clases.yaml) de `api-clases:v1` a `api-clases:v2`, aplicando el manifiesto y verificando el progreso del rollout y la nueva imagen activa en los pods.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   kubectl apply -f k8s/30-api-clases.yaml
   kubectl rollout status deployment/api-clases -n virtual4insanity
   kubectl describe deployment api-clases -n virtual4insanity | grep -E "Image:|Events:" -A 10
   kubectl get pods -l app=api-clases -n virtual4insanity -o custom-columns="POD:.metadata.name,STATUS:.status.phase,IMAGE:.spec.containers[*].image"
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando `kubectl rollout status`, los eventos de escalado gradual de ReplicaSets en `kubectl describe deployment` y el pod corriendo con la imagen `:v2`, junto con `gcloud config list` y reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/F3-rolling-update.png`
8. **Descripción formal para el informe:**
   > **Figura F3.** Ejecución de actualización progresiva (*rolling update*) del microservicio `api-clases` desde la versión `v1` hacia `v2` alojada en Artifact Registry, verificando el reemplazo ordenado de pods sin interrupción del servicio.
9. **Estado:** `Pendiente`.
10. **Dependencias necesarias para completar la prueba:** Imagen `api-clases:v2` publicada en Artifact Registry y manifiesto [k8s/30-api-clases.yaml](../k8s/30-api-clases.yaml) aplicado en GKE.

---

### Criterio F4
1. **Código y nombre exacto del criterio:** `F4` — Obtiene y muestra los logs de un pod de la aplicación.
2. **Puntaje correspondiente:** 2 puntos.
3. **Integrante responsable:** Diego Andrés Azurdia Ortíz (`2528119` · Rol 3).
4. **Objetivo de la evidencia:** Mostrar la salida de `kubectl logs` de un pod en ejecución (`api-miembros`, `api-clases` o `frontend`) evidenciando el arranque de Gunicorn y el registro de peticiones HTTP procesadas.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   kubectl logs -l app=api-miembros -n virtual4insanity --tail=30
   kubectl logs -l app=api-clases -n virtual4insanity --tail=30
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando la salida de `kubectl logs` con las líneas de Gunicorn y las peticiones HTTP atendidas por el pod, junto con `gcloud config list` y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/F4-logs-pod.png`
8. **Descripción formal para el informe:**
   > **Figura F4.** Extracción de registros de ejecución (*logs*) de los pods de la aplicación en el namespace `virtual4insanity` mediante `kubectl logs`, mostrando la actividad de los workers de Gunicorn y las peticiones HTTP procesadas.
9. **Estado:** `Pendiente`.
10. **Dependencias necesarias para completar la prueba:** Pods en ejecución dentro de GKE.

---

## SECCIÓN G. Costos y cierre responsable (8 puntos)

### Criterio G1
1. **Código y nombre exacto del criterio:** `G1` — Presenta la estimación de costo mensual de la infraestructura declarada, elaborada antes del despliegue.
2. **Puntaje correspondiente:** 3 puntos.
3. **Integrante responsable:** Susana Paola García García (`1224323` · Rol 5).
4. **Objetivo de la evidencia:** Presentar la estimación formal de costos mensuales en `us-central1` ([docs/estimacion-costo.md](estimacion-costo.md)) elaborada y versionada en Git antes del despliegue de la infraestructura.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   git log --follow --date=short --pretty=format:"%h | %ad | %an | %s" -- docs/estimacion-costo.md
   cat docs/estimacion-costo.md
   ```
6. **Lugar exacto donde tomar la captura:** Vista de la tabla de costos de [docs/estimacion-costo.md](estimacion-costo.md) junto a la terminal mostrando el commit de creación previo al despliegue (`2026-11-02`), `gcloud config list` y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/G1-estimacion-costo.png`
8. **Descripción formal para el informe:**
   > **Figura G1.** Estimación preventiva del costo mensual de la infraestructura declarada en la región `us-central1` (`docs/estimacion-costo.md`), elaborada y versionada antes del despliegue (USD 50.26/mes para 730 horas continuas y USD 2.83 para 40 horas de operación efectiva).
9. **Estado:** `Preparado`.
10. **Dependencias necesarias para completar la prueba:** Tener `gcloud config list` configurado con `project = gimnasio-virtual4insanity`.

---

### Criterio G2
1. **Código y nombre exacto del criterio:** `G2` — Ejecuta `terraform destroy` y presenta la salida con los recursos eliminados.
2. **Puntaje correspondiente:** 3 puntos.
3. **Integrante responsable:** Rochelle Giulianne Esquivel Vargas (`1283220` · Rol 1).
4. **Objetivo de la evidencia:** Demostrar que, una vez concluida la defensa en vivo, el equipo eliminó el namespace de Kubernetes y ejecutó `terraform destroy`, obteniendo `Destroy complete! Resources: X destroyed`.
5. **Comandos o procedimiento para verificar el requisito:**
   ```bash
   gcloud config list
   kubectl delete namespace virtual4insanity
   cd terraform && terraform destroy
   gcloud container clusters list
   ```
6. **Lugar exacto donde tomar la captura:** Terminal mostrando la salida final de `terraform destroy` (`Destroy complete!`) y `gcloud container clusters list` vacío (0 clústeres activos), junto con `gcloud config list` y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/G2-terraform-destroy.png`
8. **Descripción formal para el informe:**
   > **Figura G2.** Cierre responsable de la infraestructura: salida de `terraform destroy` y verificación con `gcloud container clusters list` confirmando la eliminación completa de los recursos aprovisionados después de la defensa.
9. **Estado:** `Pendiente` (se ejecuta inmediatamente después de la defensa del martes 10 o jueves 12 de noviembre, con fecha límite viernes 13 de noviembre a las 23:59).
10. **Dependencias necesarias para completar la prueba:** Haber finalizado la defensa en vivo ante el docente.

---

### Criterio G3
1. **Código y nombre exacto del criterio:** `G3` — Presenta la captura del panel de facturación con el gasto final.
2. **Puntaje correspondiente:** 2 puntos.
3. **Integrante responsable:** Rochelle Giulianne Esquivel Vargas (`1283220` · Rol 1).
4. **Objetivo de la evidencia:** Mostrar el panel de Facturación (*Billing*) de Google Cloud Console correspondiente al proyecto `gimnasio-virtual4insanity` con el desglose del gasto final incurrido.
5. **Comandos o procedimiento para verificar el requisito:**
   - Abrir en Google Cloud Console la sección **Facturación > Informes (Billing > Reports)** filtrada por el proyecto `gimnasio-virtual4insanity`.
   - Colocar al lado una ventana de terminal con la salida de `gcloud config list`.
6. **Lugar exacto donde tomar la captura:** Pantalla mostrando el panel de facturación de Google Cloud Console con el costo total acumulado del proyecto, junto con la ventana de terminal mostrando `gcloud config list` y el reloj del sistema.
7. **Nombre recomendado para guardar la imagen:** `docs/evidencias/G3-panel-facturacion.png`
8. **Descripción formal para el informe:**
   > **Figura G3.** Captura del panel oficial de Facturación de Google Cloud Platform mostrando el reporte de gasto final acumulado por el proyecto `gimnasio-virtual4insanity` tras la destrucción de la infraestructura.
9. **Estado:** `Pendiente` (se toma al concluir la defensa y destruir la infraestructura).
10. **Dependencias necesarias para completar la prueba:** Destrucción completa de la infraestructura (`G2`) y acceso al panel de Billing de la cuenta de Google Cloud (Rol 1).

---

## 2. Lista de comprobación final antes de exportar el PDF de evidencias

Antes de generar el archivo PDF definitivo para el portal (fecha límite de entrega inicial: **martes 10 de noviembre a las 17:59**; evidencia de destrucción: **viernes 13 de noviembre a las 23:59**), verifique uno por uno los siguientes puntos:

- [ ] **1. Secuencia completa A–G:** El documento contiene exactamente las secciones **A (A1–A5), B (B1–B4), C (C1–C3), D (D1–D5), E (E1–E6), F (F1–F4) y G (G1–G3)** en orden estricto sin saltar ningún código.
- [ ] **2. Reloj del sistema en el 100 % de las capturas:** Todas y cada una de las imágenes muestran claramente la fecha y hora del sistema operativo.
- [ ] **3. Salida de `gcloud config list` en el 100 % de las capturas:** En todas las capturas es legible la salida de `gcloud config list` con `project = gimnasio-virtual4insanity`.
- [ ] **4. Diagrama de arquitectura incluido:** El diagrama [docs/arquitectura.png](arquitectura.png) está integrado tanto en el [README.md](../README.md) del repositorio como en la sección **A3** del PDF de evidencias en alta resolución.
- [ ] **5. Los 5 carnés visibles en BD e interfaz (A4):** En la captura de **A4** se distinguen claramente los carnés `1283220`, `1182222`, `2528119`, `1163722` y `1224323`.
- [ ] **6. Nombres oficiales exactos (A5, E1–E6):** Todas las salidas de terminal muestran el clúster `gke-virtual4insanity`, el namespace `virtual4insanity`, los Services `db`, `api-miembros`, `api-clases` y `frontend`, los ConfigMaps `gimnasio-config` y `frontend-config`, el Secret `gimnasio-secret` y el PVC `db-pvc`.
- [ ] **7. Cero uso del tag `latest` (C1–C3):** Ningún manifiesto ni imagen en las capturas utiliza `:latest`; todas provienen de `us-central1-docker.pkg.dev/gimnasio-virtual4insanity/gimnasio/...`.
- [ ] **8. Estimación de costos previa al despliegue (G1):** La sección **G1** incluye la tabla de costos de [docs/estimacion-costo.md](estimacion-costo.md) con fecha anterior al `terraform apply`.
- [ ] **9. Legibilidad del PDF exportado:** Al abrir el PDF al 100 % de zoom, ningún texto de consola o navegador aparece pixelado o cortado.
