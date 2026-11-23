-- =====================================================================
-- PizzaSmart · T1-09 · Esquema PostgreSQL (8 tablas, PK/FK e índices)
-- Reconstruido a partir del diagrama ER (pgAdmin) del equipo de BD (D05).
--
-- Es idempotente: se puede ejecutar varias veces (IF NOT EXISTS).
--
--   psql "$DATABASE_URL" -f database/esquema.sql
--   psql "$DATABASE_URL" -f database/datos_demo.sql
--
-- Decisiones (a confirmar con D05 / PO1):
--   * precio_adicional puede ser negativo: el precio base es el de la
--     Mediana y la Pequeña resta (regla del flujo de catálogo).
--   * cantidad entre 1 y 10: máximo 10 unidades por pizza y tamaño.
--   * estado de pedido: PENDIENTE, EN_PREPARACION, ENTREGADO (mockup).
--   * usuario_id es opcional: permite pedidos de invitado.
--   * No se borran categorías con productos ni productos/variantes con
--     pedidos (RESTRICT); lo normal es desactivar (activo = FALSE).
--   * rol sin CHECK: definir los valores definitivos en el Sprint 2 (HU-05).
-- =====================================================================

BEGIN;

CREATE TABLE IF NOT EXISTS usuarios (
    id            SERIAL PRIMARY KEY,
    nombre        VARCHAR(100) NOT NULL,
    email         VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    rol           VARCHAR(30)  NOT NULL,
    activo        BOOLEAN      NOT NULL DEFAULT TRUE,
    creado_en     TIMESTAMP    NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS categorias (
    id          SERIAL PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    activo      BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS ingredientes (
    id             SERIAL PRIMARY KEY,
    nombre         VARCHAR(100) NOT NULL UNIQUE,
    es_vegetariano BOOLEAN NOT NULL DEFAULT FALSE,
    calorias_aprox INTEGER CHECK (calorias_aprox IS NULL OR calorias_aprox >= 0)
);

CREATE TABLE IF NOT EXISTS productos (
    id           SERIAL PRIMARY KEY,
    categoria_id INTEGER NOT NULL REFERENCES categorias (id) ON DELETE RESTRICT,
    nombre       VARCHAR(100) NOT NULL,
    descripcion  TEXT,
    precio_base  NUMERIC(10, 2) NOT NULL CHECK (precio_base >= 0),
    imagen_url   TEXT,
    activo       BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS productos_ingredientes (
    producto_id    INTEGER NOT NULL REFERENCES productos (id) ON DELETE CASCADE,
    ingrediente_id INTEGER NOT NULL REFERENCES ingredientes (id) ON DELETE RESTRICT,
    PRIMARY KEY (producto_id, ingrediente_id)
);

CREATE TABLE IF NOT EXISTS variantes_producto (
    id               SERIAL PRIMARY KEY,
    producto_id      INTEGER NOT NULL REFERENCES productos (id) ON DELETE CASCADE,
    nombre_variante  VARCHAR(50) NOT NULL,
    precio_adicional NUMERIC(10, 2) NOT NULL DEFAULT 0,
    UNIQUE (producto_id, nombre_variante)
);

CREATE TABLE IF NOT EXISTS pedidos (
    id               SERIAL PRIMARY KEY,
    usuario_id       INTEGER REFERENCES usuarios (id) ON DELETE SET NULL,
    nombre_cliente   VARCHAR(100) NOT NULL,
    telefono_cliente VARCHAR(30),
    direccion_envio  TEXT,
    estado           VARCHAR(30) NOT NULL DEFAULT 'PENDIENTE'
                     CHECK (estado IN ('PENDIENTE', 'EN_PREPARACION', 'ENTREGADO')),
    total            NUMERIC(10, 2) NOT NULL CHECK (total >= 0),
    creado_en        TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS detalle_pedido (
    id                        SERIAL PRIMARY KEY,
    pedido_id                 INTEGER NOT NULL REFERENCES pedidos (id) ON DELETE CASCADE,
    producto_id               INTEGER NOT NULL REFERENCES productos (id) ON DELETE RESTRICT,
    variante_id               INTEGER NOT NULL REFERENCES variantes_producto (id) ON DELETE RESTRICT,
    cantidad                  INTEGER NOT NULL CHECK (cantidad BETWEEN 1 AND 10),
    precio_unitario_historico NUMERIC(10, 2) NOT NULL CHECK (precio_unitario_historico >= 0)
);

-- Índices iniciales (las PK y los UNIQUE ya crean los suyos)
CREATE INDEX IF NOT EXISTS idx_productos_categoria_activo ON productos (categoria_id, activo);
CREATE INDEX IF NOT EXISTS idx_prod_ingredientes_ingrediente ON productos_ingredientes (ingrediente_id);
CREATE INDEX IF NOT EXISTS idx_pedidos_usuario ON pedidos (usuario_id);
CREATE INDEX IF NOT EXISTS idx_pedidos_estado_fecha ON pedidos (estado, creado_en);
CREATE INDEX IF NOT EXISTS idx_detalle_pedido ON detalle_pedido (pedido_id);
CREATE INDEX IF NOT EXISTS idx_detalle_producto ON detalle_pedido (producto_id);

COMMIT;
