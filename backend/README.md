# backend

API REST de PizzaSmart con **FastAPI** (Python 3.11+). Todas las rutas cuelgan de `/api/v1`.

## Instalar y arrancar

Desde la carpeta `backend`:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env        # en Windows: copy .env.example .env
uvicorn app.main:app --reload
```

- API: http://localhost:8000/api/v1/salud
- Documentación interactiva: http://localhost:8000/docs

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/salud` | Comprueba que la API está arriba |
| GET | `/api/v1/categorias` | Categorías activas (T1-10) |
| GET | `/api/v1/categorias/{id}/productos` | Productos activos de una categoría; `[]` si no tiene; 404 si la categoría no existe o está inactiva (T1-10) |
| GET | `/api/v1/productos` | Todos los productos activos de categorías activas (T1-10) |
| GET | `/api/v1/productos/{id}` | Detalle de un producto activo con categoría, variantes (`precio_total` = base + adicional) e ingredientes. 404 si no existe, está inactivo o su categoría está inactiva |

## Pruebas

```bash
pytest
```

Las pruebas de `test_detalle_producto_bd.py` usan un PostgreSQL real y se saltan si no defines
`TEST_DATABASE_URL`. Crean un esquema temporal y lo borran al terminar:

```bash
# Windows PowerShell
$env:TEST_DATABASE_URL="postgresql://usuario:clave@localhost:5432/pizzasmart"
pytest
```

## Estructura

```
backend/
├── app/
│   ├── main.py              # crea la app, CORS, errores y monta /api/v1
│   ├── core/
│   │   ├── config.py        # variables de entorno (.env)
│   │   ├── database.py      # conexión a PostgreSQL (psycopg 3)
│   │   └── errores.py       # formato único de errores
│   └── modules/
│       ├── salud.py         # GET /api/v1/salud
│       └── catalogo/        # HU-01 / HU-02 (T1-10, T1-11)
│           ├── router.py      # endpoints
│           ├── repositorio.py # consultas SQL
│           └── esquemas.py    # forma de las respuestas
└── tests/
```

Para un módulo nuevo: crea `app/modules/<nombre>/router.py` con un `APIRouter` y agrégalo en `main.py` con `api.include_router(...)`.

## Formato de errores

Todos los errores responden igual, para que el frontend los muestre sin casos especiales:

```json
{"error": {"codigo": "NO_ENCONTRADO", "mensaje": "La categoría no existe.", "detalles": []}}
```

| HTTP | codigo | Cuándo |
|------|--------|--------|
| 404 | `NO_ENCONTRADO` | `raise NoEncontrado("...")` o ruta inexistente |
| 409 | `CONFLICTO` | `raise Conflicto("...")` |
| 422 | `DATOS_INVALIDOS` | Parámetros o cuerpo no válidos; `detalles` lista `campo` y `mensaje` |
| 503 | `SERVICIO_NO_DISPONIBLE` | Falta `DATABASE_URL` o PostgreSQL no responde |
| 500 | `ERROR_INTERNO` | Error inesperado (el detalle solo va al log, nunca al cliente) |

Las validaciones se declaran con tipos de Pydantic y `Query`/`Path`, por ejemplo `limite: int = Query(gt=0)`.
