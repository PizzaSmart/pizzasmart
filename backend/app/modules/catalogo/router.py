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
from app.modules.catalogo.esquemas import Categoria, ProductoDetalle, ProductoResumen
from app.modules.catalogo.repositorio import RepositorioCatalogo, get_repositorio

router = APIRouter(tags=["catalogo"])


@router.get("/categorias", response_model=list[Categoria])
def listar_categorias(repo: RepositorioCatalogo = Depends(get_repositorio)):
    """Categorías activas."""
    return repo.listar_categorias()


@router.get("/categorias/{categoria_id}/productos", response_model=list[ProductoResumen])
def productos_de_categoria(
    categoria_id: int = Path(gt=0, description="Id de la categoría"),
    repo: RepositorioCatalogo = Depends(get_repositorio),
):
    """Productos activos de una categoría. Una categoría activa sin productos devuelve []."""
    if not repo.categoria_activa(categoria_id):
        raise NoEncontrado("La categoría no existe o no está disponible.")
    return repo.listar_productos(categoria_id)


@router.get("/productos", response_model=list[ProductoResumen])
def listar_productos(repo: RepositorioCatalogo = Depends(get_repositorio)):
    """Todos los productos activos (filtro «Todas» de la carta)."""
    return repo.listar_productos()


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
