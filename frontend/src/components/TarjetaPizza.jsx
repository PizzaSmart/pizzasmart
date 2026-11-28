import { Link } from "react-router-dom";
import { precio, urlImagen } from "../lib/formato.js";

export function ImagenPizza({ producto, className = "" }) {
  const src = urlImagen(producto.imagen_url);
  if (!src) {
    return (
      <div aria-hidden="true" className={`grid place-items-center bg-raised font-titulo text-5xl font-extrabold text-brand ${className}`}>
        {producto.nombre.charAt(0)}
      </div>
    );
  }
  return <img src={src} alt={`Pizza ${producto.nombre}`} loading="lazy" className={`object-cover ${className}`} />;
}

export default function TarjetaPizza({ producto }) {
  return (
    <li className="group overflow-hidden rounded-2xl border bg-card transition hover:border-strong">
      <Link to={`/pizza/${producto.id}`} className="block" aria-label={`Ver detalle de ${producto.nombre}`}>
        <ImagenPizza producto={producto} className="h-52 w-full" />
        <div className="p-5">
          <div className="flex items-baseline justify-between gap-3">
            <h3 className="text-xl">{producto.nombre}</h3>
            <span className="whitespace-nowrap font-semibold text-brand">{precio(producto.precio_base)}</span>
          </div>
          <p className="mt-2 min-h-[2.5rem] text-sm text-ink-muted">{producto.descripcion}</p>
          <p className="mt-4 border-t pt-4 text-xs font-semibold text-ink-secondary group-hover:text-ink">Ver ingredientes y tamaños →</p>
        </div>
      </Link>
    </li>
  );
}
