import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from database import get_db_connection, check_db_health

load_dotenv()

app = Flask(__name__)

# URL base interna acordada en el contrato
MIEMBROS_URL = os.getenv("MIEMBROS_URL", "http://localhost:5001")


def validar_miembro_existe(miembro_id):
    """
    Consulta al microservicio api-miembros para verificar si el ID existe.
    Retorna True si existe (200), False si no existe (404).
    Lanza excepción si api-miembros está caído o da error 500.
    """
    url = f"{MIEMBROS_URL}/api/miembros/{miembro_id}"
    try:
        response = requests.get(url, timeout=3.0)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        else:
            raise Exception(f"api-miembros devolvió status {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"No se pudo contactar a api-miembros: {str(e)}")


def formatear_registro(registro):
    """Convierte tipos DATE y TIME a strings según el contrato (YYYY-MM-DD y HH:MM)"""
    if not registro:
        return None
    data = dict(registro)
    if "fecha" in data and data["fecha"]:
        data["fecha"] = data["fecha"].strftime("%Y-%m-%d")
    if "hora" in data and data["hora"]:
        data["hora"] = data["hora"].strftime("%H:%M")
    return data


# --- 1. Health check ---
@app.route("/api/clases/health", methods=["GET"])
def health():
    db_ok = check_db_health()
    if db_ok:
        return jsonify({"status": "ok", "service": "api-clases", "database": "connected"}), 200
    return jsonify({"error": "Base de datos no disponible"}), 500


# --- 2. Listar clases (con soporte opcional ?miembro_id=X) ---
@app.route("/api/clases", methods=["GET"])
def listar_clases():
    miembro_id = request.args.get("miembro_id")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if miembro_id:
            cur.execute("SELECT * FROM clases WHERE miembro_id = %s ORDER BY id ASC;", (miembro_id,))
        else:
            cur.execute("SELECT * FROM clases ORDER BY id ASC;")
        filas = cur.fetchall()
        cur.close()
        conn.close()

        resultado = [formatear_registro(f) for f in filas]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": f"Error al consultar clases: {str(e)}"}), 500


# --- 3. Obtener detalle de una clase ---
@app.route("/api/clases/<int:id>", methods=["GET"])
def obtener_clase(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM clases WHERE id = %s;", (id,))
        clase = cur.fetchone()
        cur.close()
        conn.close()

        if not clase:
            return jsonify({"error": f"La clase {id} no existe"}), 404

        return jsonify(formatear_registro(clase)), 200
    except Exception as e:
        return jsonify({"error": f"Error inesperado: {str(e)}"}), 500


# --- 4. Crear clase ---
@app.route("/api/clases", methods=["POST"])
def crear_clase():
    data = request.get_json() or {}
    campos_obligatorios = ["nombre", "instructor", "fecha", "hora", "cupo", "miembro_id", "carne_registro"]

    # Validación de campos presentes
    for campo in campos_obligatorios:
        if campo not in data or data[campo] is None or str(data[campo]).strip() == "":
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

    # Validación de cupo > 0
    try:
        cupo = int(data["cupo"])
        if cupo <= 0:
            return jsonify({"error": "El cupo debe ser mayor que 0"}), 400
    except ValueError:
        return jsonify({"error": "El cupo debe ser un número entero"}), 400

    miembro_id = data["miembro_id"]

    # Validación de existencia del miembro contra api-miembros
    try:
        existe = validar_miembro_existe(miembro_id)
        if not existe:
            return jsonify({"error": f"El miembro {miembro_id} no existe"}), 400
    except Exception as e:
        return jsonify({"error": f"Error validando miembro: {str(e)}"}), 500

    # Inserción en la base de datos
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            INSERT INTO clases (nombre, instructor, fecha, hora, cupo, miembro_id, carne_registro)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *;
        """
        cur.execute(query, (
            data["nombre"],
            data["instructor"],
            data["fecha"],
            data["hora"],
            cupo,
            miembro_id,
            data["carne_registro"]
        ))
        nueva_clase = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return jsonify(formatear_registro(nueva_clase)), 201
    except Exception as e:
        return jsonify({"error": f"Error al guardar la clase: {str(e)}"}), 500


# --- 5. Actualizar clase ---
@app.route("/api/clases/<int:id>", methods=["PUT"])
def actualizar_clase(id):
    data = request.get_json() or {}
    campos_obligatorios = ["nombre", "instructor", "fecha", "hora", "cupo", "miembro_id", "carne_registro"]

    for campo in campos_obligatorios:
        if campo not in data or data[campo] is None or str(data[campo]).strip() == "":
            return jsonify({"error": f"El campo '{campo}' es obligatorio"}), 400

    try:
        cupo = int(data["cupo"])
        if cupo <= 0:
            return jsonify({"error": "El cupo debe ser mayor que 0"}), 400
    except ValueError:
        return jsonify({"error": "El cupo debe ser un número entero"}), 400

    miembro_id = data["miembro_id"]

    try:
        existe = validar_miembro_existe(miembro_id)
        if not existe:
            return jsonify({"error": f"El miembro {miembro_id} no existe"}), 400
    except Exception as e:
        return jsonify({"error": f"Error validando miembro: {str(e)}"}), 500

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Verificar que la clase exista antes de actualizar
        cur.execute("SELECT id FROM clases WHERE id = %s;", (id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": f"La clase {id} no existe"}), 404

        query = """
            UPDATE clases
            SET nombre = %s, instructor = %s, fecha = %s, hora = %s, cupo = %s, miembro_id = %s, carne_registro = %s
            WHERE id = %s
            RETURNING *;
        """
        cur.execute(query, (
            data["nombre"],
            data["instructor"],
            data["fecha"],
            data["hora"],
            cupo,
            miembro_id,
            data["carne_registro"],
            id
        ))
        clase_actualizada = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return jsonify(formatear_registro(clase_actualizada)), 200
    except Exception as e:
        return jsonify({"error": f"Error al actualizar la clase: {str(e)}"}), 500


# --- 6. Eliminar clase ---
@app.route("/api/clases/<int:id>", methods=["DELETE"])
def eliminar_clase(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id FROM clases WHERE id = %s;", (id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"error": f"La clase {id} no existe"}), 404

        cur.execute("DELETE FROM clases WHERE id = %s;", (id,))
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"mensaje": f"Clase {id} eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": f"Error al eliminar la clase: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)