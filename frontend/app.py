import os
import requests
from flask import Flask, render_template

app = Flask(__name__)

# Ajusta estos puertos según el puerto en el que corra cada microservicio de forma predeterminada
MIEMBROS_URL = os.getenv("MIEMBROS_URL", "http://127.0.0.1:5000")
CLASES_URL = os.getenv("CLASES_URL", "http://127.0.0.1:5001")

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "80")), debug=True)