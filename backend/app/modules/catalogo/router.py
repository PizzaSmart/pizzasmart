"""Módulo de catálogo (HU-01, HU-02).

Endpoints públicos de categorías y productos:
- T1-10: GET /categorias y GET /categorias/{id}/productos (solo activos)
- T1-11: GET /productos/{id} con variantes e ingredientes

Para errores de negocio usa las clases de app.core.errores, por ejemplo:
    raise NoEncontrado("La categoría no existe.")
"""
from decimal import Decimal

from fastapi import APIRouter, Depends, Path

from app.core.errores import NoEncontrado
from app.modules.catalogo.esquemas import ProductoDetalle
from app.modules.catalogo.repositorio import RepositorioCatalogo, get_repositorio

router = APIRouter(tags=["catalogo"])


@router.get("/productos/{producto_id}", response_model=ProductoDetalle)
def detalle_producto(
    producto_id: int = Path(gt=0, description="Id del producto"),
    repo: RepositorioCatalogo = Depends(get_repositorio),
):
    """Detalle de un producto activo con sus variantes (tamaños) e ingredientes."""
    fila = repo.detalle_producto(producto_id)
    if fila is None:
        raise NoEncontrado("El producto no existe o no está disponible.")

    precio_base = Decimal(fila["precio_base"])
    return {
        "id": fila["id"],
        "nombre": fila["nombre"],
        "descripcion": fila["descripcion"],
        "precio_base": precio_base,
        "imagen_url": fila["imagen_url"],
        "categoria": {"id": fila["categoria_id"], "nombre": fila["categoria_nombre"]},
        "variantes": [
            {
                "id": v["id"],
                "nombre": v["nombre_variante"],
                "precio_adicional": v["precio_adicional"] or 0,
                "precio_total": precio_base + Decimal(v["precio_adicional"] or 0),
            }
            for v in fila["variantes"]
        ],
        "ingredientes": fila["ingredientes"],
    }
