/** Cliente HTTP mínimo. Convierte los errores de la API en ErrorApi.
 *  Formato de error del backend: {"error": {"codigo", "mensaje", "detalles"}} (backend/README.md) */
const BASE = (import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1").replace(/\/$/, "");

export class ErrorApi extends Error {
  constructor(mensaje, { status = 0, codigo = "SIN_CONEXION", detalles = [] } = {}) {
    super(mensaje);
    this.status = status;
    this.codigo = codigo;
    this.detalles = detalles;
  }
  get esNoEncontrado() { return this.status === 404; }
  get esRed() { return this.codigo === "SIN_CONEXION"; }
}

export async function pedirJson(ruta, { signal } = {}) {
  let resp;
  try {
    resp = await fetch(`${BASE}${ruta}`, { signal, headers: { Accept: "application/json" } });
  } catch (e) {
    if (e.name === "AbortError") throw e;
    throw new ErrorApi("No pudimos conectar con el servidor. Revisa tu conexión e intenta de nuevo.");
  }
  if (!resp.ok) {
    let cuerpo = null;
    try { cuerpo = (await resp.json()).error; } catch { /* respuesta sin JSON */ }
    throw new ErrorApi(cuerpo?.mensaje ?? "Ocurrió un error inesperado. Intenta de nuevo.", {
      status: resp.status,
      codigo: cuerpo?.codigo ?? "ERROR_HTTP",
      detalles: cuerpo?.detalles ?? [],
    });
  }
  return resp.json();
}
