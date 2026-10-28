# db/ · Rol 2

Script de inicio de la base de datos `gimnasio`.

Archivo esperado:

- `init.sql`: crea las tablas `integrantes`, `miembros` y `clases` (ver CONTRATO.md, sección 6) e inserta los carnés del equipo.

El script se monta en el contenedor de PostgreSQL en `/docker-entrypoint-initdb.d/` y solo corre cuando el volumen está vacío.
