"""Microservicio Miembros · Gimnasio · Virtual Insanity (ver CONTRATO.md, sección 7)."""
import os
import re
from contextlib import contextmanager

import psycopg2
from psycopg2 import errors
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from werkzeug.exceptions import HTTPException

load_dotenv()  # Solo para pruebas locales: busca el .env en esta carpeta o en las de arriba

app = Flask(__name__)
app.json.ensure_ascii = False  # Devuelve "López" y no "L\u00f3pez"
app.json.mimetype = "application/json; charset=utf-8"  # Avisa al cliente que el texto viene en UTF-8

MEMBRESIAS = ("Mensual", "Trimestral", "Anual")
CAMPOS = ("nombre", "correo", "telefono", "membresia", "carne_registro")
CORREO_VALIDO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@contextmanager
def db():
    """Abre la conexión, entrega un cursor y siempre la cierra (con commit si todo salió bien)."""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "gimnasio"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5,
    )
    try:
        with conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur
    finally:
        conn.close()


def error(mensaje, codigo):
    return jsonify({"error": mensaje}), codigo


def formato(fila):
    """Convierte la fecha a texto AAAA-MM-DD."""
    fila = dict(fila)
    fila["fecha_inscripcion"] = fila["fecha_inscripcion"].isoformat()
    return fila


def validar(data):
    """Devuelve un mensaje de error si los datos no cumplen el contrato, o None si están bien."""
    for campo in ("nombre", "correo", "membresia", "carne_registro"):
        if not str(data.get(campo) or "").strip():
            return f"El campo '{campo}' es obligatorio"
    if not CORREO_VALIDO.match(str(data["correo"]).strip()):
        return "El correo no es válido"
    if data["membresia"] not in MEMBRESIAS:
        return "La membresía debe ser Mensual, Trimestral o Anual"
    return None


def valores(data):
    """Limpia los datos en el orden de CAMPOS; el teléfono vacío se guarda como NULL."""
    limpio = {c: (str(data.get(c)).strip() if data.get(c) is not None else None) for c in CAMPOS}
    limpio["telefono"] = limpio["telefono"] or None
    return tuple(limpio[c] for c in CAMPOS)


@app.errorhandler(errors.UniqueViolation)
def correo_repetido(e):
    return error("Ese correo ya está registrado", 409)


@app.errorhandler(errors.ForeignKeyViolation)
def carne_ajeno(e):
    return error("El carné de registro no pertenece al equipo", 400)


@app.errorhandler(psycopg2.DataError)
def dato_invalido(e):
    return error("Algún dato no tiene el formato correcto", 400)


@app.errorhandler(psycopg2.OperationalError)
def base_caida(e):
    app.logger.error("Sin conexión a la base: %s", e)
    return error("La base de datos no responde", 500)


@app.errorhandler(HTTPException)
def error_http(e):
    """Rutas inexistentes, métodos no permitidos, etc.: también en JSON."""
    mensajes = {404: "La ruta no existe", 405: "Método no permitido en esta ruta"}
    return error(mensajes.get(e.code, e.description), e.code)


@app.errorhandler(Exception)
def error_inesperado(e):
    app.logger.exception("Error inesperado")
    return error("Error inesperado en el servidor", 500)


@app.get("/api/miembros/health")
def health():
    with db() as cur:
        cur.execute("SELECT 1")
    return jsonify({"status": "ok", "service": "api-miembros"})


@app.get("/api/miembros/integrantes")
def listar_integrantes():
    with db() as cur:
        cur.execute("SELECT carne, nombre, rol FROM integrantes ORDER BY nombre")
        return jsonify(cur.fetchall())


@app.get("/api/miembros")
def listar_miembros():
    with db() as cur:
        cur.execute("SELECT * FROM miembros ORDER BY id")
        return jsonify([formato(f) for f in cur.fetchall()])


@app.get("/api/miembros/<int:id>")
def obtener_miembro(id):
    with db() as cur:
        cur.execute("SELECT * FROM miembros WHERE id = %s", (id,))
        fila = cur.fetchone()
    return jsonify(formato(fila)) if fila else error(f"El miembro {id} no existe", 404)


@app.post("/api/miembros")
def crear_miembro():
    data = request.get_json(silent=True) or {}
    if mensaje := validar(data):
        return error(mensaje, 400)
    with db() as cur:
        cur.execute(
            "INSERT INTO miembros (nombre, correo, telefono, membresia, carne_registro) "
            "VALUES (%s, %s, %s, %s, %s) RETURNING *",
            valores(data),
        )
        return jsonify(formato(cur.fetchone())), 201


@app.put("/api/miembros/<int:id>")
def actualizar_miembro(id):
    data = request.get_json(silent=True) or {}
    if mensaje := validar(data):
        return error(mensaje, 400)
    with db() as cur:
        cur.execute(
            "UPDATE miembros SET nombre = %s, correo = %s, telefono = %s, membresia = %s, "
            "carne_registro = %s WHERE id = %s RETURNING *",
            (*valores(data), id),
        )
        fila = cur.fetchone()
    return jsonify(formato(fila)) if fila else error(f"El miembro {id} no existe", 404)


@app.delete("/api/miembros/<int:id>")
def eliminar_miembro(id):
    with db() as cur:
        cur.execute("DELETE FROM miembros WHERE id = %s RETURNING id", (id,))
        borrado = cur.fetchone()
    if not borrado:
        return error(f"El miembro {id} no existe", 404)
    return jsonify({"mensaje": f"Miembro {id} eliminado"})


if __name__ == "__main__":
    # Solo para pruebas locales. En el contenedor arranca Gunicorn en el puerto 5000.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
