"""Pruebas de la estructura base de la API (T1-12)."""
from fastapi import Query
from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.core.errores import Conflicto, NoEncontrado
from app.main import PREFIJO_API, crear_app


class Item(BaseModel):
    nombre: str
    precio: float


def app_de_prueba():
    app = crear_app()

    @app.get("/prueba/no-encontrado")
    def _no_encontrado():
        raise NoEncontrado("La categoría no existe.")

    @app.get("/prueba/conflicto")
    def _conflicto():
        raise Conflicto("Estado no permitido.")

    @app.get("/prueba/query")
    def _query(limite: int = Query(gt=0)):
        return {"limite": limite}

    @app.post("/prueba/cuerpo")
    def _cuerpo(item: Item):
        return item

    @app.get("/prueba/explota")
    def _explota():
        raise RuntimeError("detalle interno secreto")

    return TestClient(app, raise_server_exceptions=False)


cliente = app_de_prueba()


def test_salud_responde_ok():
    r = cliente.get(f"{PREFIJO_API}/salud")
    assert r.status_code == 200
    assert r.json()["estado"] == "ok"


def test_ruta_inexistente_da_404_con_formato_comun():
    r = cliente.get(f"{PREFIJO_API}/no-existe")
    assert r.status_code == 404
    assert r.json()["error"]["codigo"] == "NO_ENCONTRADO"
    assert r.json()["error"]["mensaje"] == "El recurso solicitado no existe."


def test_error_de_negocio_no_encontrado():
    r = cliente.get("/prueba/no-encontrado")
    assert r.status_code == 404
    assert r.json() == {
        "error": {"codigo": "NO_ENCONTRADO", "mensaje": "La categoría no existe.", "detalles": []}
    }


def test_error_de_negocio_conflicto():
    r = cliente.get("/prueba/conflicto")
    assert r.status_code == 409
    assert r.json()["error"]["codigo"] == "CONFLICTO"


def test_validacion_de_parametro():
    r = cliente.get("/prueba/query", params={"limite": 0})
    assert r.status_code == 422
    error = r.json()["error"]
    assert error["codigo"] == "DATOS_INVALIDOS"
    assert error["detalles"][0]["campo"] == "query.limite"


def test_validacion_de_cuerpo():
    r = cliente.post("/prueba/cuerpo", json={"nombre": "Hawaiana", "precio": "barata"})
    assert r.status_code == 422
    campos = [d["campo"] for d in r.json()["error"]["detalles"]]
    assert "body.precio" in campos


def test_error_inesperado_no_filtra_detalles():
    r = cliente.get("/prueba/explota")
    assert r.status_code == 500
    assert r.json()["error"]["codigo"] == "ERROR_INTERNO"
    assert "secreto" not in r.text


def test_cors_permite_el_frontend():
    r = cliente.options(
        f"{PREFIJO_API}/salud",
        headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"},
    )
    assert r.headers.get("access-control-allow-origin") == "http://localhost:5173"
