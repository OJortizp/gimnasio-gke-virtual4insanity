import os
import requests
from flask import Flask, Response, jsonify, render_template, request

app = Flask(__name__)

# En Kubernetes llegan por ConfigMap con los nombres DNS de los Services (http://api-miembros:5000, http://api-clases:5000).
# Los valores por defecto son para pruebas locales.
MIEMBROS_URL = os.getenv("MIEMBROS_URL", "http://127.0.0.1:5001")
CLASES_URL = os.getenv("CLASES_URL", "http://127.0.0.1:5002")

@app.route("/")
def index():
    miembros = []
    clases = []
    integrantes = []
    error_msg = None

    # 1. Consultar microservicio de Miembros
    try:
        res_miembros = requests.get(f"{MIEMBROS_URL}/api/miembros", timeout=3.0)
        if res_miembros.status_code == 200:
            miembros = res_miembros.json()
    except Exception as e:
        error_msg = f"No se pudo conectar al microservicio de miembros: {str(e)}"

    # 2. Consultar integrantes del equipo desde el backend (Criterio A4)
    try:
        res_integrantes = requests.get(f"{MIEMBROS_URL}/api/miembros/integrantes", timeout=3.0)
        if res_integrantes.status_code == 200:
            integrantes = res_integrantes.json()
    except Exception as e:
        pass

    # 3. Consultar microservicio de Clases
    try:
        res_clases = requests.get(f"{CLASES_URL}/api/clases", timeout=3.0)
        if res_clases.status_code == 200:
            clases = res_clases.json()
    except Exception as e:
        if not error_msg:
            error_msg = f"No se pudo conectar al microservicio de clases: {str(e)}"

    return render_template(
        "index.html", 
        miembros=miembros, 
        clases=clases, 
        integrantes=integrantes, 
        error=error_msg
    )


# Reenvía /api/miembros/... y /api/clases/... al microservicio correspondiente por su nombre DNS.
# Así el navegador solo conoce la IP pública del frontend (CONTRATO.md, sección 5).
SERVICIOS = {"miembros": MIEMBROS_URL, "clases": CLASES_URL}


@app.route("/api/<servicio>", defaults={"resto": ""}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/api/<servicio>/<path:resto>", methods=["GET", "POST", "PUT", "DELETE"])
def reenviar_api(servicio, resto):
    base = SERVICIOS.get(servicio)
    if not base:
        return jsonify({"error": "La ruta no existe"}), 404
    url = f"{base}/api/{servicio}" + (f"/{resto}" if resto else "")
    try:
        r = requests.request(
            request.method,
            url,
            params=request.args,
            data=request.get_data(),
            headers={"Content-Type": request.headers.get("Content-Type", "application/json")},
            timeout=5,
        )
    except requests.RequestException:
        return jsonify({"error": f"No se pudo contactar a api-{servicio}"}), 502
    return Response(r.content, status=r.status_code, content_type=r.headers.get("Content-Type"))


if __name__ == "__main__":
    # Solo para pruebas locales. En el contenedor arranca Gunicorn en el puerto 80.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))