/** Precio en pesos colombianos: 38900 -> "$ 38.900" */
export const precio = (n) => `$ ${Math.round(Number(n)).toLocaleString("es-CO")}`;

/** Diámetro por tamaño (wireframe T1-02). Si el nombre no está, no se muestra. */
const CM = { pequeña: 25, personal: 25, mediana: 33, grande: 40, familiar: 40 };
export const centimetros = (nombreVariante) => CM[nombreVariante.trim().toLowerCase()] ?? null;

/** Las imágenes de la BD son rutas relativas a /public o URLs absolutas. */
export const urlImagen = (u) => u || null;

/** Mediana es el tamaño por defecto; si no existe, el primero. */
export const variantePorDefecto = (variantes) =>
  variantes.find((v) => v.nombre.toLowerCase() === "mediana") ?? variantes[0] ?? null;
