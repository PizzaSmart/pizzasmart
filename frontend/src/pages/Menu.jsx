import { useSearchParams } from "react-router-dom";
import { obtenerCategorias, obtenerProductos } from "../api/catalogo.js";
import { useApi } from "../hooks/useApi.js";
import TarjetaPizza from "../components/TarjetaPizza.jsx";
import { Aviso, EsqueletoTarjetas, EstadoVacio } from "../components/Estados.jsx";

/** HU-01: carta con categorías. Abre en «Todas»; la categoría activa vive en ?categoria=ID. */
export default function Menu() {
  const [params, setParams] = useSearchParams();
  const categoriaId = Number(params.get("categoria")) || null;

  const categorias = useApi((signal) => obtenerCategorias({ signal }), []);
  const productos = useApi((signal) => obtenerProductos(categoriaId, { signal }), [categoriaId]);

  const elegir = (id) => setParams(id ? { categoria: String(id) } : {});
  const lista = categorias.datos ?? [];
  const categoriaActual = lista.find((c) => c.id === categoriaId) ?? null;
  // La API responde 404 si la categoría de la URL no existe o está inactiva.
  const categoriaInvalida = Boolean(categoriaId) && productos.error?.esNoEncontrado;
  const botonVerTodas = <button className="btn-secundario" onClick={() => elegir(null)}>Ver todas</button>;

  const contenido = () => {
    if (productos.cargando) return <EsqueletoTarjetas />;
    if (categoriaInvalida)
      return <EstadoVacio titulo="Esa categoría ya no está disponible" accion={botonVerTodas}>Mira el resto de la carta.</EstadoVacio>;
    if (productos.error)
      return (
        <Aviso titulo="No pudimos cargar las pizzas"
          accion={<button className="btn-secundario" onClick={productos.reintentar}>Reintentar</button>}>
          {productos.error.message}
        </Aviso>
      );
    if (productos.datos.length === 0)
      return categoriaActual ? (
        <EstadoVacio titulo={`Aún no hay pizzas en ${categoriaActual.nombre}`} accion={botonVerTodas}>
          Estamos preparando nuevas recetas. Mientras tanto, mira el resto de la carta.
        </EstadoVacio>
      ) : (
        <EstadoVacio titulo="La carta está vacía por ahora">Vuelve en un rato: estamos actualizando el menú.</EstadoVacio>
      );
    return (
      <>
        <h2 className="mb-5 text-lg text-ink-secondary">
          {productos.datos.length} {productos.datos.length === 1 ? "pizza" : "pizzas"}
          {categoriaActual ? ` · ${categoriaActual.nombre}` : ""}
        </h2>
        <ul className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {productos.datos.map((p) => <TarjetaPizza key={p.id} producto={p} />)}
        </ul>
      </>
    );
  };

  return (
    <div className="mx-auto max-w-6xl px-4 pb-8 pt-10 sm:px-6">
      <section className="mb-10">
        <h1 className="text-4xl leading-tight sm:text-6xl">
          Pizza artesanal, hecha <span className="font-serif font-medium italic text-brand">al momento.</span>
        </h1>
        <p className="mt-4 max-w-xl text-ink-secondary">Elige una categoría y mira ingredientes, tamaños y precios.</p>
      </section>

      <nav aria-label="Categorías" className="mb-8 flex flex-wrap gap-2">
        {[{ id: null, nombre: "Todas" }, ...lista].map((c) => {
          const activa = c.id === (categoriaActual?.id ?? null);
          return (
            <button key={c.id ?? "todas"} onClick={() => elegir(c.id)} aria-pressed={activa}
              className={`rounded-full border px-4 py-2 text-sm transition ${
                activa ? "border-ink bg-ink font-semibold text-[#161616]" : "text-ink-secondary hover:border-strong hover:text-ink"
              }`}>
              {c.nombre}
            </button>
          );
        })}
        {categorias.error && (
          <button onClick={categorias.reintentar} className="rounded-full border border-danger/40 px-4 py-2 text-sm text-danger">
            No se cargaron las categorías · Reintentar
          </button>
        )}
      </nav>

      <section aria-live="polite">{contenido()}</section>
    </div>
  );
}
