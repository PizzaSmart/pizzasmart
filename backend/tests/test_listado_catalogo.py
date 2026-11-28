"""Pruebas de GET /categorias, /categorias/{id}/productos y /productos (T1-10, HU-01) sin base de datos."""
from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import PREFIJO_API, crear_app
from app.modules.catalogo.repositorio import get_repositorio

CATEGORIAS = [
    {"id": 1, "nombre": "Clásicas", "descripcion": None},
    {"id": 4, "nombre": "Sin gluten", "descripcion": "Masa sin gluten"},
]
PRODUCTOS = [
    {"id": 1, "nombre": "Pamplona", "descripcion": "Chorizo", "precio_base": Decimal("38900.00"),
     "imagen_url": "/img/pizza-1.jpg", "categoria_id": 1},
    {"id": 2, "nombre": "Navarra", "descripcion": None, "precio_base": Decimal("42900.00"),
     "imagen_url": None, "categoria_id": 1},
]


class RepoFalso:
    def listar_categorias(self):
        return CATEGORIAS

    def categoria_activa(self, categoria_id):
        return categoria_id in {c["id"] for c in CATEGORIAS}

    def listar_productos(self, categoria_id=None):
        if categoria_id is None:
            return PRODUCTOS
        return [p for p in PRODUCTOS if p["categoria_id"] == categoria_id]


def cliente():
    app = crear_app()
    app.dependency_overrides[get_repositorio] = lambda: RepoFalso()
    return TestClient(app)


def test_lista_categorias():
    r = cliente().get(f"{PREFIJO_API}/categorias")
    assert r.status_code == 200
    assert [c["nombre"] for c in r.json()] == ["Clásicas", "Sin gluten"]


def test_lista_todos_los_productos():
    r = cliente().get(f"{PREFIJO_API}/productos")
    assert r.status_code == 200
    assert [p["nombre"] for p in r.json()] == ["Pamplona", "Navarra"]
    assert r.json()[0]["precio_base"] == 38900.0


def test_productos_de_una_categoria():
    r = cliente().get(f"{PREFIJO_API}/categorias/1/productos")
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_categoria_activa_sin_productos_devuelve_lista_vacia():
    r = cliente().get(f"{PREFIJO_API}/categorias/4/productos")
    assert r.status_code == 200
    assert r.json() == []


def test_categoria_inexistente_da_404():
    r = cliente().get(f"{PREFIJO_API}/categorias/99/productos")
    assert r.status_code == 404
    assert r.json()["error"]["codigo"] == "NO_ENCONTRADO"


def test_id_invalido_da_422():
    r = cliente().get(f"{PREFIJO_API}/categorias/0/productos")
    assert r.status_code == 422
