"""Módulo de catálogo (HU-01, HU-02).

Aquí van los endpoints públicos de categorías y productos:
- T1-10: GET /categorias y GET /categorias/{id}/productos (solo activos)
- T1-11: GET /productos/{id} con variantes e ingredientes

Para errores de negocio usa las clases de app.core.errores, por ejemplo:
    raise NoEncontrado("La categoría no existe.")
"""
from fastapi import APIRouter

router = APIRouter(tags=["catalogo"])
