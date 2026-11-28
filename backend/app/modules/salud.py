from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(tags=["salud"])


@router.get("/salud")
def salud():
    """Comprueba que la API está arriba."""
    return {"estado": "ok", "entorno": get_settings().app_entorno}
