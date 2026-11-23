import { Link, NavLink } from "react-router-dom";

const enlace = ({ isActive }) =>
  `text-sm transition hover:text-ink ${isActive ? "text-ink" : "text-ink-secondary"}`;

/** Cabecera de la carta. Login y carrito se activan en el Sprint 2 (HU-03, HU-05). */
export default function Header() {
  return (
    <header className="border-b bg-page/80 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center gap-6 px-4 sm:px-6">
        <Link to="/" className="font-titulo text-lg font-extrabold tracking-tight">
          PIZZA<span className="text-brand">SMART</span>
        </Link>
        <nav aria-label="Principal" className="ml-auto flex items-center gap-5">
          <NavLink to="/" end className={enlace}>Menú</NavLink>
          <span className="hidden text-sm text-ink-faint sm:inline" title="Disponible en el Sprint 3">Asistente</span>
          <span className="rounded-xl border px-3 py-1.5 text-sm text-ink-secondary" aria-label="Carrito, 0 productos">
            Carrito · 0
          </span>
        </nav>
      </div>
    </header>
  );
}
