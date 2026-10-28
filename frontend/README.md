# frontend/ · Rol 4

Interfaz web en Vue 3 con Vite, servida por Nginx (puerto 80).

Archivos esperados:

- Proyecto Vue (`package.json`, `src/`, `vite.config.js`).
- `nginx.conf`: sirve `dist/` y reenvía `/api/miembros` a `http://api-miembros:5000` y `/api/clases` a `http://api-clases:5000` (ver CONTRATO.md, sección 5).
- `Dockerfile`: construye Vue y lo copia a una imagen de Nginx. Imagen `frontend`.

Pantallas mínimas: miembros, clases programadas y carnés del equipo.
