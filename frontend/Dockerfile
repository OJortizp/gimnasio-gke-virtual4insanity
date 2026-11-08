# Frontend · imagen frontend
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates/ templates/

EXPOSE 80

# Gunicorn en vez del servidor de desarrollo de Flask
CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:80", "--access-logfile", "-", "app:app"]
