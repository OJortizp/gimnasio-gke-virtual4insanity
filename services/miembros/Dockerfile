# Microservicio Miembros · imagen api-miembros
FROM python:3.12-slim

# Sin archivos .pyc y con logs inmediatos (se ven al momento con kubectl logs)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Primero las dependencias, para que Docker las reutilice si solo cambia el código
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# El contenedor no corre como root
RUN useradd --create-home appuser
USER appuser

EXPOSE 5000

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "--access-logfile", "-", "app:app"]
