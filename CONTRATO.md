# Contrato del equipo

Estos son los acuerdos técnicos que todos respetamos para poder trabajar en paralelo. Si alguien necesita cambiar algo de aquí, lo propone en el grupo y se actualiza este archivo por Pull Request antes de cambiar el código.

## 1. Nombres generales

| Elemento | Valor |
| --- | --- |
| Identificador del equipo | `virtual4insanity` |
| Región / zona de Google Cloud | `us-central1` / `us-central1-a` |
| Nombre del clúster | `gke-virtual4insanity` |
| Namespace | `virtual4insanity` |
| Repositorio de Artifact Registry | `gimnasio` (formato Docker, región `us-central1`) |
| Base de datos | PostgreSQL 16, una base llamada `gimnasio` |

## 2. Componentes y nombres en Kubernetes

El Deployment, el Service y la etiqueta `app` de cada componente llevan el mismo nombre. Así el nombre DNS interno siempre es el nombre del Service.

| Componente | Nombre (Deployment, Service, `app`) | Puerto del contenedor | Tipo de Service | Dueño |
| --- | --- | --- | --- | --- |
| Base de datos | `db` | 5432 | ClusterIP | Rol 2 |
| Microservicio Miembros | `api-miembros` | 5000 | ClusterIP | Rol 2 |
| Microservicio Clases | `api-clases` | 5000 | ClusterIP | Rol 3 |
| Frontend | `frontend` | 80 | LoadBalancer (puerto 80) | Rol 4 |

Dentro del clúster los componentes se llaman así:

- `db:5432`
- `http://api-miembros:5000`
- `http://api-clases:5000`

Nunca se usa la IP de un pod, porque cambia cada vez que el pod se recrea.

## 3. Imágenes

| Imagen | Ruta completa | Dueño |
| --- | --- | --- |
| Frontend | `us-central1-docker.pkg.dev/<PROJECT_ID>/gimnasio/frontend:<tag>` | Rol 4 |
| Miembros | `us-central1-docker.pkg.dev/<PROJECT_ID>/gimnasio/api-miembros:<tag>` | Rol 2 |
| Clases | `us-central1-docker.pkg.dev/<PROJECT_ID>/gimnasio/api-clases:<tag>` | Rol 3 |
| Base de datos | `us-central1-docker.pkg.dev/<PROJECT_ID>/gimnasio/postgres:16-alpine` | Rol 3 |

- `<PROJECT_ID>` es el ID del proyecto de Google Cloud que crea el Rol 1.
- La primera versión de nuestras imágenes es `v1`. Para el rolling update se publica `v2`.
- Nunca se usa el tag `latest`.
- La base usa la imagen oficial `postgres:16-alpine`, pero el Rol 3 la copia a nuestro repositorio de Artifact Registry. El criterio C3 pide que los manifiestos solo usen imágenes de Artifact Registry, y eso incluye la de la base.

## 4. Tecnologías

| Parte | Tecnología |
| --- | --- |
| Microservicios | Python 3.12, Flask, Gunicorn y psycopg2 |
| Frontend | Vue 3 con Vite, servido por Nginx |
| Base de datos | PostgreSQL 16 |
| Infraestructura | Terraform y Google Cloud (GKE, Artifact Registry) |

Todo el código se escribe desde cero. No se copia nada de los Proyectos 1 y 2.

## 5. Cómo llega el navegador a los microservicios

El navegador solo conoce la IP pública del frontend. Nginx, dentro del contenedor del frontend, reenvía las llamadas a los microservicios por su nombre DNS:

| El navegador pide | Nginx lo envía a |
| --- | --- |
| `/` | Archivos de Vue (carpeta `dist`) |
| `/api/miembros...` | `http://api-miembros:5000` |
| `/api/clases...` | `http://api-clases:5000` |

Por eso **las rutas de cada microservicio ya empiezan con `/api/<servicio>`** y Nginx no tiene que cambiar la ruta. En Vue, Axios usa la base `/api`, nunca `localhost` ni una IP.

## 6. Base de datos

Una sola base `gimnasio` con tres tablas. Cada microservicio solo toca su propia tabla:

| Tabla | La usa |
| --- | --- |
| `integrantes` | api-miembros (solo lectura) |
| `miembros` | api-miembros |
| `clases` | api-clases |

### integrantes

Guarda los carnés del equipo (criterio A4). Se llena con el script de inicio.

| Columna | Tipo | Regla |
| --- | --- | --- |
| `carne` | VARCHAR(10) | Llave primaria |
| `nombre` | VARCHAR(100) | Obligatorio |
| `rol` | VARCHAR(60) | Obligatorio |

### miembros

| Columna | Tipo | Regla |
| --- | --- | --- |
| `id` | SERIAL | Llave primaria |
| `nombre` | VARCHAR(100) | Obligatorio |
| `correo` | VARCHAR(100) | Obligatorio y único |
| `telefono` | VARCHAR(20) | Opcional |
| `membresia` | VARCHAR(20) | `Mensual`, `Trimestral` o `Anual` |
| `fecha_inscripcion` | DATE | Por defecto, la fecha de hoy |
| `carne_registro` | VARCHAR(10) | Carné del integrante que creó el registro; debe existir en `integrantes` |

### clases

| Columna | Tipo | Regla |
| --- | --- | --- |
| `id` | SERIAL | Llave primaria |
| `nombre` | VARCHAR(100) | Obligatorio (por ejemplo Spinning, Yoga) |
| `instructor` | VARCHAR(100) | Obligatorio |
| `fecha` | DATE | Obligatorio |
| `hora` | TIME | Obligatorio |
| `cupo` | INTEGER | Mayor que 0 |
| `miembro_id` | INTEGER | Obligatorio; id del miembro que reservó la clase |
| `carne_registro` | VARCHAR(10) | Carné del integrante que creó el registro |

`clases.miembro_id` no tiene llave foránea hacia `miembros`, porque cada microservicio es dueño de su tabla. Quien valida que el miembro exista es **api-clases**, preguntándole a api-miembros (ver sección 7).

Si se elimina un miembro, sus clases no se borran; el frontend muestra "Miembro no encontrado" en esas filas.

## 7. API

Todas las respuestas son JSON. Las fechas van como `"2026-11-05"` y las horas como `"18:30"`.

### api-miembros (puerto 5000)

| Método | Ruta | Qué hace | Respuestas |
| --- | --- | --- | --- |
| GET | `/api/miembros/health` | Revisa que el servicio y la base respondan | 200 |
| GET | `/api/miembros` | Lista todos los miembros | 200 |
| GET | `/api/miembros/<id>` | Devuelve un miembro | 200, 404 |
| POST | `/api/miembros` | Crea un miembro | 201, 400, 409 |
| PUT | `/api/miembros/<id>` | Actualiza un miembro | 200, 400, 404, 409 |
| DELETE | `/api/miembros/<id>` | Elimina un miembro | 200, 404 |
| GET | `/api/miembros/integrantes` | Lista los carnés del equipo | 200 |

Ejemplo de miembro:

```json
{
  "id": 1,
  "nombre": "Ana López",
  "correo": "ana@correo.com",
  "telefono": "5555-1234",
  "membresia": "Mensual",
  "fecha_inscripcion": "2026-11-02",
  "carne_registro": "1182222"
}
```

Para crear o actualizar se envían los mismos campos sin `id` ni `fecha_inscripcion`.

### api-clases (puerto 5000)

| Método | Ruta | Qué hace | Respuestas |
| --- | --- | --- | --- |
| GET | `/api/clases/health` | Revisa que el servicio y la base respondan | 200 |
| GET | `/api/clases` | Lista todas las clases (acepta `?miembro_id=1`) | 200 |
| GET | `/api/clases/<id>` | Devuelve una clase | 200, 404 |
| POST | `/api/clases` | Crea una clase | 201, 400 |
| PUT | `/api/clases/<id>` | Actualiza una clase | 200, 400, 404 |
| DELETE | `/api/clases/<id>` | Elimina una clase | 200, 404 |

Ejemplo de clase:

```json
{
  "id": 1,
  "nombre": "Spinning",
  "instructor": "Carlos Pérez",
  "fecha": "2026-11-05",
  "hora": "18:30",
  "cupo": 15,
  "miembro_id": 1,
  "carne_registro": "2528119"
}
```

Al crear o actualizar una clase, api-clases llama a `GET http://api-miembros:5000/api/miembros/<miembro_id>`. Si responde 404, la clase no se guarda y se devuelve 400.

### Errores

Todos los errores tienen la misma forma:

```json
{ "error": "El miembro 7 no existe" }
```

| Código | Cuándo |
| --- | --- |
| 400 | Faltan campos, un dato no es válido, el carné no es del equipo o el miembro no existe |
| 404 | El registro pedido no existe |
| 409 | El correo del miembro ya está registrado |
| 500 | Error inesperado o la base no responde |

## 8. Configuración (ConfigMap y Secret)

Los microservicios leen todo de variables de entorno. Nada de contraseñas en el código.

**ConfigMap `gimnasio-config`** (datos no sensibles):

| Clave | Valor |
| --- | --- |
| `DB_HOST` | `db` |
| `DB_PORT` | `5432` |
| `DB_NAME` | `gimnasio` |
| `MIEMBROS_URL` | `http://api-miembros:5000` |
| `EQUIPO` | `virtual4insanity` |

**Secret `gimnasio-secret`** (credenciales):

| Clave | Uso |
| --- | --- |
| `DB_USER` | Usuario de PostgreSQL |
| `DB_PASSWORD` | Contraseña de PostgreSQL |

- El Deployment de `db` pasa estos valores al contenedor de PostgreSQL como `POSTGRES_DB`, `POSTGRES_USER` y `POSTGRES_PASSWORD`.
- En el repo solo se sube `k8s/secret.example.yaml` con valores de ejemplo. El `k8s/secret.yaml` real está en `.gitignore`.
- Para pruebas locales se usa un `.env` copiado de `.env.example`.

## 9. Persistencia

- La base usa un PersistentVolumeClaim llamado `db-pvc` de 1 Gi.
- Se monta en `/var/lib/postgresql/data` y se define `PGDATA=/var/lib/postgresql/data/pgdata`. Sin ese subdirectorio PostgreSQL no arranca en GKE, porque el disco trae una carpeta `lost+found`.
- El script `db/init.sql` se monta en `/docker-entrypoint-initdb.d/` y solo corre la primera vez que el volumen está vacío.

## 10. Manifiestos

Todos los manifiestos van en `k8s/` y todos llevan `namespace: virtual4insanity`.

| Archivo | Contenido | Dueño |
| --- | --- | --- |
| `00-namespace.yaml` | Namespace | Rol 5 |
| `01-configmap.yaml` | ConfigMap `gimnasio-config` | Rol 4 |
| `secret.example.yaml` | Plantilla del Secret | Rol 2 |
| `10-db.yaml` | PVC, ConfigMap del init.sql, Deployment y Service de `db` | Rol 2 |
| `20-api-miembros.yaml` | Deployment y Service de `api-miembros` | Rol 2 |
| `30-api-clases.yaml` | Deployment y Service de `api-clases` | Rol 3 |
| `40-frontend.yaml` | Deployment y Service LoadBalancer de `frontend` | Rol 4 |

Cada Deployment de la aplicación pide como máximo `cpu: 100m` y `memory: 128Mi`, porque los nodos e2-small son pequeños.

## 11. Ramas y commits

| Rama | Dueño |
| --- | --- |
| `feature/terraform` | Rol 1 |
| `feature/db-miembros` | Rol 2 |
| `feature/api-clases` | Rol 3 |
| `feature/frontend` | Rol 4 |
| `feature/k8s-docs` | Rol 5 |

- Cada quien sale de `develop` y vuelve a `develop` por Pull Request, con al menos una revisión.
- `main` recibe `develop` solo cuando todo está probado.
- Formato de commit: `tipo(parte): descripción`, por ejemplo `feat(clases): validar miembro al crear clase` o `fix(frontend): corregir ruta de la API`.
