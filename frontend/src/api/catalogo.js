import { pedirJson } from "./cliente.js";

export const obtenerCategorias = (opts) => pedirJson("/categorias", opts);
/** Sin categoriaId devuelve todos los productos activos («Todas»). */
export const obtenerProductos = (categoriaId, opts) =>
  pedirJson(categoriaId ? `/categorias/${categoriaId}/productos` : "/productos", opts);
export const obtenerProducto = (id, opts) => pedirJson(`/productos/${id}`, opts);
