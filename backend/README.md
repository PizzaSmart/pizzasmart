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

## Pruebas

```bash
pytest
```

## Estructura

```
backend/
├── app/
│   ├── main.py              # crea la app, CORS, errores y monta /api/v1
│   ├── core/
│   │   ├── config.py        # variables de entorno (.env)
│   │   └── errores.py       # formato único de errores
│   └── modules/
│       ├── salud.py         # GET /api/v1/salud
│       └── catalogo/        # HU-01 / HU-02 (T1-10, T1-11)
│           └── router.py
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
| 500 | `ERROR_INTERNO` | Error inesperado (el detalle solo va al log, nunca al cliente) |

Las validaciones se declaran con tipos de Pydantic y `Query`/`Path`, por ejemplo `limite: int = Query(gt=0)`.
