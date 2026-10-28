# services/clases/ · Rol 3

Microservicio Clases programadas (Flask, puerto 5000).

Archivos esperados:

- `app.py`: rutas `/api/clases...` (ver CONTRATO.md, sección 7).
- `requirements.txt`
- `Dockerfile`: imagen `api-clases`.

Lee la conexión a la base desde `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER` y `DB_PASSWORD`, y la dirección de Miembros desde `MIEMBROS_URL`. Antes de guardar una clase valida que el miembro exista.
