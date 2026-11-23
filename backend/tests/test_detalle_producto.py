"""Pruebas de GET /api/v1/productos/{id} (T1-11, HU-02) sin base de datos."""
from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import PREFIJO_API, crear_app
from app.modules.catalogo.repositorio import get_repositorio

PIZZA = {
    "id": 1,
    "nombre": "Hawaiana",
    "descripcion": "Jamón y piña",
    "precio_base": Decimal("20000.00"),
    "imagen_url": None,
    "categoria_id": 2,
    "categoria_nombre": "Pizzas",
    "variantes": [
        {"id": 10, "nombre_variante": "Personal", "precio_adicional": Decimal("0.00")},
        {"id": 11, "nombre_variante": "Grande", "precio_adicional": Decimal("12500.50")},
    ],
    "ingredientes": [
        {"id": 5, "nombre": "Jamón", "es_vegetariano": False, "calorias_aprox": 120},
        {"id": 6, "nombre": "Piña", "es_vegetariano": True, "calorias_aprox": None},
    ],
}


class RepoFalso:
    def __init__(self, productos):
        self.productos = productos

    def detalle_producto(self, producto_id):
        return self.productos.get(producto_id)


def cliente_con(productos):
    app = crear_app()
    app.dependency_overrides[get_repositorio] = lambda: RepoFalso(productos)
    return TestClient(app)


def test_detalle_devuelve_variantes_e_ingredientes():
    r = cliente_con({1: PIZZA}).get(f"{PREFIJO_API}/productos/1")
    assert r.status_code == 200
    datos = r.json()
    assert datos["nombre"] == "Hawaiana"
    assert datos["categoria"] == {"id": 2, "nombre": "Pizzas"}
    assert [v["nombre"] for v in datos["variantes"]] == ["Personal", "Grande"]
    assert datos["variantes"][1]["precio_total"] == 32500.5
    assert [i["nombre"] for i in datos["ingredientes"]] == ["Jamón", "Piña"]


def test_producto_inexistente_o_inactivo_da_404():
    r = cliente_con({}).get(f"{PREFIJO_API}/productos/99")
    assert r.status_code == 404
    assert r.json()["error"]["codigo"] == "NO_ENCONTRADO"


def test_id_no_valido_da_422():
    cliente = cliente_con({})
    for malo in ("0", "-3", "abc"):
        r = cliente.get(f"{PREFIJO_API}/productos/{malo}")
        assert r.status_code == 422, malo
        assert r.json()["error"]["codigo"] == "DATOS_INVALIDOS"


def test_producto_sin_variantes_ni_ingredientes():
    simple = {**PIZZA, "variantes": [], "ingredientes": []}
    r = cliente_con({1: simple}).get(f"{PREFIJO_API}/productos/1")
    assert r.status_code == 200
    assert r.json()["variantes"] == [] and r.json()["ingredientes"] == []


def test_sin_base_configurada_da_503(monkeypatch):
    from app.core.config import get_settings

    monkeypatch.setattr(get_settings(), "database_url", "")
    r = TestClient(crear_app()).get(f"{PREFIJO_API}/productos/1")
    assert r.status_code == 503
    assert r.json()["error"]["codigo"] == "SERVICIO_NO_DISPONIBLE"
