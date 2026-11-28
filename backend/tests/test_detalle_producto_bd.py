"""Prueba de T1-11 contra un PostgreSQL real.

Se salta si no existe la variable TEST_DATABASE_URL. Crea un esquema temporal con
las tablas del catálogo (igual que el modelo del equipo), lo llena y lo borra al final.
"""
import os
import uuid

import psycopg
import pytest
from fastapi.testclient import TestClient
from psycopg.rows import dict_row

from app.core.database import get_conexion
from app.main import PREFIJO_API, crear_app

URL = os.getenv("TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not URL, reason="TEST_DATABASE_URL no definida")

TABLAS = """
CREATE TABLE categorias (id serial PRIMARY KEY, nombre varchar(100) UNIQUE, descripcion text, activo boolean);
CREATE TABLE productos (id serial PRIMARY KEY, categoria_id integer REFERENCES categorias(id),
    nombre varchar(100), descripcion text, precio_base numeric(10,2), imagen_url text, activo boolean);
CREATE TABLE variantes_producto (id serial PRIMARY KEY, producto_id integer REFERENCES productos(id),
    nombre_variante varchar(50), precio_adicional numeric(10,2));
CREATE TABLE ingredientes (id serial PRIMARY KEY, nombre varchar(100) UNIQUE, es_vegetariano boolean,
    calorias_aprox integer);
CREATE TABLE productos_ingredientes (producto_id integer REFERENCES productos(id),
    ingrediente_id integer REFERENCES ingredientes(id), PRIMARY KEY (producto_id, ingrediente_id));

INSERT INTO categorias (id, nombre, activo) VALUES (1, 'Pizzas', true), (2, 'Ocultas', false);
INSERT INTO productos (id, categoria_id, nombre, descripcion, precio_base, activo) VALUES
    (1, 1, 'Hawaiana', 'Jamón y piña', 20000, true),
    (2, 1, 'Retirada', NULL, 15000, false),
    (3, 2, 'De categoría inactiva', NULL, 10000, true);
INSERT INTO variantes_producto (producto_id, nombre_variante, precio_adicional) VALUES
    (1, 'Grande', 12000), (1, 'Personal', 0);
INSERT INTO ingredientes (id, nombre, es_vegetariano, calorias_aprox) VALUES
    (1, 'Piña', true, 40), (2, 'Jamón', false, 120);
INSERT INTO productos_ingredientes VALUES (1, 1), (1, 2);
"""


@pytest.fixture
def cliente():
    esquema = f"prueba_{uuid.uuid4().hex[:8]}"
    with psycopg.connect(URL, autocommit=True) as admin:
        admin.execute(f"CREATE SCHEMA {esquema}")
        try:
            def conexion_de_prueba():
                with psycopg.connect(URL, row_factory=dict_row, options=f"-c search_path={esquema}") as conn:
                    yield conn

            with psycopg.connect(URL, options=f"-c search_path={esquema}") as conn:
                conn.execute(TABLAS)

            app = crear_app()
            app.dependency_overrides[get_conexion] = conexion_de_prueba
            yield TestClient(app)
        finally:
            admin.execute(f"DROP SCHEMA {esquema} CASCADE")


def test_detalle_real(cliente):
    r = cliente.get(f"{PREFIJO_API}/productos/1")
    assert r.status_code == 200
    datos = r.json()
    assert datos["categoria"]["nombre"] == "Pizzas"
    assert [(v["nombre"], v["precio_total"]) for v in datos["variantes"]] == [
        ("Personal", 20000.0),
        ("Grande", 32000.0),
    ]
    assert [i["nombre"] for i in datos["ingredientes"]] == ["Jamón", "Piña"]


@pytest.mark.parametrize("producto_id", [2, 3, 999])
def test_inactivos_o_inexistentes_dan_404(cliente, producto_id):
    r = cliente.get(f"{PREFIJO_API}/productos/{producto_id}")
    assert r.status_code == 404
