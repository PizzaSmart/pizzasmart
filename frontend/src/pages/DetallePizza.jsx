import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { obtenerProducto } from "../api/catalogo.js";
import { useApi } from "../hooks/useApi.js";
import { centimetros, precio, variantePorDefecto } from "../lib/formato.js";
import { ImagenPizza } from "../components/TarjetaPizza.jsx";
import { Aviso } from "../components/Estados.jsx";

function EsqueletoDetalle() {
  return (
    <div className="grid animate-pulse gap-8 md:grid-cols-2" aria-busy="true" aria-label="Cargando pizza">
      <div className="h-72 rounded-2xl bg-raised md:h-[28rem]" />
      <div className="space-y-4">
        <div className="h-4 w-24 rounded bg-raised" />
        <div className="h-9 w-2/3 rounded bg-raised" />
        <div className="h-4 w-full rounded bg-raised" />
        <div className="h-20 rounded bg-raised" />
        <div className="h-16 rounded bg-raised" />
      </div>
    </div>
  );
}

/** HU-02: detalle con ingredientes, tamaños y precios (estados del wireframe T1-02). */
export default function DetallePizza() {
  const { id } = useParams();
  const { datos: p, error, cargando, reintentar } = useApi((signal) => obtenerProducto(id, { signal }), [id]);
  const [varianteId, setVarianteId] = useState(null);
  const [aviso, setAviso] = useState(false);

  useEffect(() => {
    setVarianteId(p ? variantePorDefecto(p.variantes)?.id ?? null : null);
    setAviso(false);
  }, [p]);

  const cuerpo = () => {
    if (cargando) return <EsqueletoDetalle />;

    if (error?.esNoEncontrado) {
      // 404: el producto no existe, está inactivo o su categoría lo está. No se puede comprar.
      return (
        <div className="mx-auto max-w-xl py-10">
          <Aviso tono="warn" titulo="Pizza no disponible por ahora"
            accion={<Link to="/" className="btn-secundario">Elegir otra pizza</Link>}>
            Esta pizza no se puede pedir por ahora. Puedes elegir otra del menú.
          </Aviso>
        </div>
      );
    }
    if (error) {
      return (
        <div className="mx-auto max-w-xl py-10">
          <Aviso titulo="No pudimos cargar la pizza"
            accion={<button className="btn-secundario" onClick={reintentar}>Reintentar</button>}>
            {error.message}
          </Aviso>
        </div>
      );
    }

    const variante = p.variantes.find((v) => v.id === varianteId);

    return (
      <div className="grid gap-8 md:grid-cols-2 md:gap-12">
        <ImagenPizza producto={p} className="h-72 w-full rounded-2xl md:h-[30rem]" />
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-brand">{p.categoria.nombre}</p>
          <h1 className="mt-2 text-4xl sm:text-5xl">{p.nombre}</h1>
          <p className="mt-3 text-ink-secondary">{p.descripcion}</p>

          <h2 className="mt-8 text-xs font-semibold uppercase tracking-[0.14em] text-ink-muted">Ingredientes</h2>
          {p.ingredientes.length === 0 ? (
            <p className="mt-2 text-sm text-ink-muted">Ingredientes no disponibles.</p>
          ) : (
            <ul className="mt-3 flex flex-wrap gap-2">
              {p.ingredientes.map((i) => (
                <li key={i.id} className="rounded-full border bg-surface px-3 py-1.5 text-sm">
                  {i.nombre}{i.es_vegetariano && <span className="sr-only"> (vegetariano)</span>}
                </li>
              ))}
            </ul>
          )}

          <h2 id="tamanos" className="mt-8 text-xs font-semibold uppercase tracking-[0.14em] text-ink-muted">Elige el tamaño</h2>
          {p.variantes.length === 0 ? (
            <div className="mt-3"><Aviso tono="warn" titulo="Sin tamaños disponibles">Esta pizza aún no tiene tamaños configurados.</Aviso></div>
          ) : (
            <div role="radiogroup" aria-labelledby="tamanos" className="mt-3 grid grid-cols-3 gap-3">
              {p.variantes.map((v) => {
                const activa = v.id === varianteId;
                const cm = centimetros(v.nombre);
                return (
                  <button key={v.id} role="radio" aria-checked={activa}
                    onClick={() => { setVarianteId(v.id); setAviso(false); }}
                    className={`rounded-xl border p-3 text-left transition ${activa ? "border-brand bg-brand/10" : "hover:border-strong"}`}>
                    <span className="block font-semibold">{v.nombre}</span>
                    {cm && <span className="block text-xs text-ink-muted">{cm} cm</span>}
                    <span className="mt-1 block text-sm text-ink-secondary">{precio(v.precio_total)}</span>
                  </button>
                );
              })}
            </div>
          )}

          {aviso && (
            <div className="mt-5">
              <Aviso tono="warn" titulo="El carrito llega en el siguiente sprint">
                La selección ya funciona; agregar al carrito se activa en el Sprint 2 (HU-03).
              </Aviso>
            </div>
          )}

          <button className="btn-primario mt-6" disabled={!variante} onClick={() => setAviso(true)}>
            {variante ? `Agregar al carrito · ${precio(variante.precio_total)}` : "Elige un tamaño"}
          </button>
          <p className="mt-3 text-center text-xs text-ink-muted">Máximo 10 unidades por variante en cada pedido.</p>
        </div>
      </div>
    );
  };

  return (
    <div className="mx-auto max-w-6xl px-4 py-8 sm:px-6">
      <Link to="/" className="mb-6 inline-block text-sm text-ink-secondary hover:text-ink">← Volver al menú</Link>
      {cuerpo()}
    </div>
  );
}
