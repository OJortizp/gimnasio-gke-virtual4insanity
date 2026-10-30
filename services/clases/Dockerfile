# Imagen base oficial y ligera
FROM python:3.12-slim

# Evita que Python escriba archivos .pyc en disco y fuerza stdout/stderr sin buffer (para ver logs al instante en kubectl)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema requeridas si se necesitan herramientas básicas de red o compilación
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Crear un usuario sin privilegios por seguridad
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Exponer el puerto acordado en el CONTRATO.md
EXPOSE 5000

# Arranque en producción con Gunicorn (2 workers para ajustarse a los 100m de CPU de los nodos e2-small)
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "--access-logfile", "-", "--error-logfile", "-", "app:app"]