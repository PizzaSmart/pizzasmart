"""Manejo de errores: toda respuesta de error tiene la misma forma.

    {"error": {"codigo": "NO_ENCONTRADO", "mensaje": "...", "detalles": [...]}}

Los módulos lanzan ErrorApp (o sus subclases) y este archivo los convierte en JSON.
"""
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

log = logging.getLogger("pizzasmart")


class ErrorApp(Exception):
    """Error de negocio con código HTTP y código legible para el frontend."""

    status = 400
    codigo = "SOLICITUD_INVALIDA"

    def __init__(self, mensaje: str, detalles: list | None = None):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.detalles = detalles or []


class NoEncontrado(ErrorApp):
    status = 404
    codigo = "NO_ENCONTRADO"


class Conflicto(ErrorApp):
    status = 409
    codigo = "CONFLICTO"


def respuesta_error(status: int, codigo: str, mensaje: str, detalles: list | None = None) -> JSONResponse:
    return JSONResponse(
        status_code=status,
        content={"error": {"codigo": codigo, "mensaje": mensaje, "detalles": detalles or []}},
    )


CODIGOS_HTTP = {
    400: "SOLICITUD_INVALIDA",
    401: "NO_AUTENTICADO",
    403: "SIN_PERMISO",
    404: "NO_ENCONTRADO",
    405: "METODO_NO_PERMITIDO",
    409: "CONFLICTO",
}

# Mensajes por defecto de Starlette que se traducen.
MENSAJES_EN_ESPANOL = {
    "Not Found": "El recurso solicitado no existe.",
    "Method Not Allowed": "Método no permitido para esta ruta.",
}


def registrar_manejadores(app: FastAPI) -> None:
    @app.exception_handler(ErrorApp)
    async def _error_app(_: Request, exc: ErrorApp):
        return respuesta_error(exc.status, exc.codigo, exc.mensaje, exc.detalles)

    @app.exception_handler(RequestValidationError)
    async def _validacion(_: Request, exc: RequestValidationError):
        detalles = [
            {"campo": ".".join(str(p) for p in e["loc"]), "mensaje": e["msg"]}
            for e in exc.errors()
        ]
        return respuesta_error(422, "DATOS_INVALIDOS", "Los datos enviados no son válidos.", detalles)

    @app.exception_handler(StarletteHTTPException)
    async def _http(_: Request, exc: StarletteHTTPException):
        mensaje = exc.detail if isinstance(exc.detail, str) else "Error en la solicitud."
        mensaje = MENSAJES_EN_ESPANOL.get(mensaje, mensaje)
        return respuesta_error(exc.status_code, CODIGOS_HTTP.get(exc.status_code, "ERROR_HTTP"), mensaje)

    @app.exception_handler(Exception)
    async def _inesperado(_: Request, exc: Exception):
        log.exception("Error no controlado", exc_info=exc)
        # No se expone el detalle interno al cliente.
        return respuesta_error(500, "ERROR_INTERNO", "Ocurrió un error inesperado. Intenta de nuevo.")
