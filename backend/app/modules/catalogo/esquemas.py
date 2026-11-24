"""Forma de las respuestas del catálogo."""
from pydantic import BaseModel


class CategoriaResumen(BaseModel):
    id: int
    nombre: str


class Categoria(BaseModel):
    id: int
    nombre: str
    descripcion: str | None


class ProductoResumen(BaseModel):
    """Tarjeta del catálogo (HU-01)."""

    id: int
    nombre: str
    descripcion: str | None
    precio_base: float
    imagen_url: str | None
    categoria_id: int


class Variante(BaseModel):
    id: int
    nombre: str
    precio_adicional: float
    precio_total: float  # precio_base + precio_adicional, calculado en el servidor


class Ingrediente(BaseModel):
    id: int
    nombre: str
    es_vegetariano: bool | None
    calorias_aprox: int | None


class ProductoDetalle(BaseModel):
    id: int
    nombre: str
    descripcion: str | None
    precio_base: float
    imagen_url: str | None
    categoria: CategoriaResumen
    variantes: list[Variante]
    ingredientes: list[Ingrediente]
