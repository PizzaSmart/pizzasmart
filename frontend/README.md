# frontend

Cliente web de PizzaSmart: **React 18 + Vite + Tailwind CSS 3**. Sprint 1: carta con categorías (HU-01) y detalle de pizza (HU-02).

## Arrancar

Desde la carpeta `frontend` (con el backend corriendo en `:8000`):

```bash
npm install
cp .env.example .env     # Windows: copy .env.example .env
npm run dev              # http://localhost:5173
```

`VITE_API_URL` apunta a la API (por defecto `http://localhost:8000/api/v1`). El puerto 5173 ya está permitido por CORS en el backend.

```bash
npm test                 # vitest: formato de precios y estados de la carta
npm run build
```

## Pantallas y estados

| Ruta | Pantalla | Estados cubiertos |
|------|----------|-------------------|
| `/` (`?categoria=ID`) | Carta (UI-01, T1-05/T1-06) | cargando (esqueleto), error de red + «Reintentar», carta vacía, categoría vacía + «Ver todas», categoría inexistente |
| `/pizza/:id` | Detalle (UI-02, T1-07/T1-08) | cargando, normal, **no disponible** (404: inexistente o inactiva), error + «Reintentar», sin tamaños, sin ingredientes. Móvil: una columna bajo `md` |

El botón «Agregar al carrito» ya elige tamaño (Mediana por defecto) y calcula el precio, pero el carrito real llega en el Sprint 2 (T2-05): por ahora muestra un aviso.

## Endpoints que consume

| Uso | Endpoint |
|-----|----------|
| Chips de categorías | `GET /categorias` |
| «Todas» | `GET /productos` |
| Una categoría | `GET /categorias/{id}/productos` |
| Detalle | `GET /productos/{id}` |

## Estructura

```
src/
├── api/          # cliente.js (fetch + errores del backend) y catalogo.js
├── hooks/        # useApi: carga con cancelación y reintento
├── lib/          # formato de precios, tamaños en cm
├── components/   # Header, TarjetaPizza, Estados (esqueleto, aviso, vacío)
└── pages/        # Menu, DetallePizza
```

Colores y tipografías salen de `tailwind.config.js` (tokens de `diseno/carpeta_administrativo`, T1-03): Manrope (títulos), DM Sans (cuerpo), Playfair Display (palabra resaltada).
Las imágenes de ejemplo están en `public/img` y las referencia `database/datos_demo.sql`.
