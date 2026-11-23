"""Conexión a PostgreSQL (psycopg 3). Cada petición abre y cierra su conexión."""
import logging

import psycopg
from psycopg.rows import dict_row

from app.core.config import get_settings
from app.core.errores import ServicioNoDisponible

log = logging.getLogger("pizzasmart")


def get_conexion():
    """Dependencia de FastAPI: entrega una conexión que devuelve filas como dict."""
    url = get_settings().database_url
    if not url:
        raise ServicioNoDisponible("La base de datos no está configurada (DATABASE_URL).")
    try:
        conn = psycopg.connect(url, row_factory=dict_row)
    except psycopg.OperationalError as exc:
        log.error("No se pudo conectar a PostgreSQL: %s", exc)
        raise ServicioNoDisponible("No se pudo conectar con la base de datos.") from exc
    with conn:
        yield conn
