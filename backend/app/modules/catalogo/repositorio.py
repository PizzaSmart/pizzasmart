"""Consultas SQL del catálogo."""
from fastapi import Depends

from app.core.database import get_conexion


class RepositorioCatalogo:
    def __init__(self, conn):
        self.conn = conn

    def detalle_producto(self, producto_id: int) -> dict | None:
        """Producto activo (de una categoría activa) con sus variantes e ingredientes.

        Devuelve None si no existe o si el producto o su categoría están inactivos.
        """
        producto = self.conn.execute(
            """
            SELECT p.id, p.nombre, p.descripcion, p.precio_base, p.imagen_url,
                   c.id AS categoria_id, c.nombre AS categoria_nombre
            FROM productos p
            JOIN categorias c ON c.id = p.categoria_id
            WHERE p.id = %s AND p.activo AND c.activo
            """,
            (producto_id,),
        ).fetchone()
        if producto is None:
            return None

        producto["variantes"] = self.conn.execute(
            """
            SELECT id, nombre_variante, precio_adicional
            FROM variantes_producto
            WHERE producto_id = %s
            ORDER BY precio_adicional, id
            """,
            (producto_id,),
        ).fetchall()

        producto["ingredientes"] = self.conn.execute(
            """
            SELECT i.id, i.nombre, i.es_vegetariano, i.calorias_aprox
            FROM productos_ingredientes pi
            JOIN ingredientes i ON i.id = pi.ingrediente_id
            WHERE pi.producto_id = %s
            ORDER BY i.nombre
            """,
            (producto_id,),
        ).fetchall()
        return producto


def get_repositorio(conn=Depends(get_conexion)) -> RepositorioCatalogo:
    return RepositorioCatalogo(conn)
