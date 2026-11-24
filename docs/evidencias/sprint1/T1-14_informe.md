# T1-14 · Prueba de integración del Sprint 1

Fecha: 23/11/2026  ·  Responsable: chaparr005

## Entorno
Node 26.13.1 · Python 3.11.9 · PostgreSQL 18.6

## Resultados
- [x] esquema.sql y datos_demo.sql corren sin errores (también repetidos)
- [x] 6 pizzas activas y 21 variantes (`01-base-de-datos.png`)
- [x] pytest: 23 passed (`02-pytest-23-passed.png`)
- [x] GET /categorias, /productos y /productos/1 responden 200 (`03`, `04`, `05`)
- [x] /productos/7 (Hawaiana inactiva) responde 404 (`06-api-inactivo-404.png`)
- [x] La carta muestra 6 pizzas y los filtros funcionan (`07`, `08`: Vegetarianas, 3 pizzas)
- [x] «Sin gluten» muestra el estado vacío (`09-categoria-vacia.png`)
- [x] El detalle muestra ingredientes, tamaños y precios (`10`: Pamplona, Mediana $38.900; `11`: Grande $48.600)
- [x] /pizza/7 muestra «Pizza no disponible por ahora» (`12-pizza-no-disponible.png`)
- [x] Error de conexión con botón «Reintentar» (`14-error-con-reintentar.png`, backend detenido)
- [x] Vista móvil correcta (`13-movil.png`, 390 × 844)
- [x] Extra (opcional): `npm test` (Vitest) 7 passed, 2 archivos de prueba (ejecutado; sin captura)

## Problemas encontrados
Ninguno bloqueante. Notas:
- Al repetir `esquema.sql` salen dos avisos (NOTICE) de que los índices `idx_detalle_pedido` e
  `idx_detalle_producto` ya existen; se omiten y no son errores.
- Las capturas 03 a 14 se tomaron con Chrome en modo automático, por eso no se ve la barra de
  direcciones. La dirección de cada una está en la tabla de abajo.

| Captura | Dirección |
|---|---|
| 03 | http://localhost:8000/api/v1/categorias |
| 04 | http://localhost:8000/api/v1/productos |
| 05 | http://localhost:8000/api/v1/productos/1 |
| 06 | http://localhost:8000/api/v1/productos/7 |
| 07 | http://localhost:5173/ |
| 08 | http://localhost:5173/?categoria=2 |
| 09 | http://localhost:5173/?categoria=4 |
| 10, 11 | http://localhost:5173/pizza/1 |
| 12 | http://localhost:5173/pizza/7 |
| 13 | http://localhost:5173/ (vista móvil) |
| 14 | http://localhost:5173/ (backend apagado) |
