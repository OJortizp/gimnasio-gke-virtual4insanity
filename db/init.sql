-- Base de datos del gimnasio · Proyecto Final Virtualización · Virtual Insanity
-- Corre solo la primera vez que el volumen de PostgreSQL está vacío.

-- ---------- Integrantes del equipo (criterio A4) ----------
CREATE TABLE integrantes (
    carne   VARCHAR(10)  PRIMARY KEY,
    nombre  VARCHAR(100) NOT NULL,
    rol     VARCHAR(60)  NOT NULL
);

INSERT INTO integrantes (carne, nombre, rol) VALUES
    ('1283220', 'Rochelle Giulianne Esquivel Vargas', 'Infraestructura como código'),
    ('1182222', 'Oscar Javier Ortíz Pocón',           'Base de datos y Miembros'),
    ('2528119', 'Diego Andrés Azurdia Ortíz',         'Clases programadas e imágenes'),
    ('1163722', 'Diego Oswaldo Orellana Morales',     'Frontend y acceso público'),
    ('1224323', 'Susana Paola García García',         'Kubernetes, operación y documentación');

-- ---------- Miembros (microservicio api-miembros) ----------
CREATE TABLE miembros (
    id                 SERIAL       PRIMARY KEY,
    nombre             VARCHAR(100) NOT NULL,
    correo             VARCHAR(100) NOT NULL UNIQUE,
    telefono           VARCHAR(20),
    membresia          VARCHAR(20)  NOT NULL
                       CHECK (membresia IN ('Mensual', 'Trimestral', 'Anual')),
    fecha_inscripcion  DATE         NOT NULL DEFAULT CURRENT_DATE,
    carne_registro     VARCHAR(10)  NOT NULL REFERENCES integrantes (carne)
);

-- ---------- Clases programadas (microservicio api-clases) ----------
-- miembro_id no tiene llave foránea: api-clases valida el miembro con api-miembros.
CREATE TABLE clases (
    id              SERIAL       PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    instructor      VARCHAR(100) NOT NULL,
    fecha           DATE         NOT NULL,
    hora            TIME         NOT NULL,
    cupo            INTEGER      NOT NULL CHECK (cupo > 0),
    miembro_id      INTEGER      NOT NULL,
    carne_registro  VARCHAR(10)  NOT NULL REFERENCES integrantes (carne)
);

-- ---------- Datos de ejemplo ----------
INSERT INTO miembros (nombre, correo, telefono, membresia, carne_registro) VALUES
    ('Ana López',     'ana.lopez@correo.com',   '5555-1234', 'Mensual',    '1182222'),
    ('Luis Méndez',   'luis.mendez@correo.com', '5555-5678', 'Anual',      '1182222'),
    ('María Castillo','maria.castillo@correo.com', NULL,     'Trimestral', '1182222');

INSERT INTO clases (nombre, instructor, fecha, hora, cupo, miembro_id, carne_registro) VALUES
    ('Spinning', 'Carlos Pérez',  '2026-11-05', '18:30', 15, 1, '2528119'),
    ('Yoga',     'Lucía Ramírez', '2026-11-06', '07:00', 20, 2, '2528119'),
    ('CrossFit', 'Jorge Aguilar', '2026-11-07', '17:00', 12, 3, '2528119');