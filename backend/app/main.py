"""Punto de entrada de la API de PizzaSmart.

Arrancar en desarrollo (desde la carpeta backend):
    uvicorn app.main:app --reload
"""
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.errores import registrar_manejadores
from app.modules import salud
from app.modules.catalogo import router as catalogo

PREFIJO_API = "/api/v1"


def crear_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_nombre, version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.lista_cors,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    registrar_manejadores(app)

    api = APIRouter(prefix=PREFIJO_API)
    api.include_router(salud.router)
    api.include_router(catalogo.router)
    app.include_router(api)
    return app


app = crear_app()
