/** Estados reutilizables: carga (esqueleto), aviso/error y vacío. */
export function EsqueletoTarjetas({ cantidad = 6 }) {
  return (
    <ul className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3" aria-busy="true" aria-label="Cargando pizzas">
      {Array.from({ length: cantidad }, (_, i) => (
        <li key={i} className="animate-pulse overflow-hidden rounded-2xl border bg-card">
          <div className="h-52 bg-raised" />
          <div className="space-y-3 p-5">
            <div className="h-5 w-2/3 rounded bg-raised" />
            <div className="h-4 w-full rounded bg-raised" />
            <div className="h-4 w-1/2 rounded bg-raised" />
          </div>
        </li>
      ))}
    </ul>
  );
}

export function Aviso({ titulo, children, tono = "danger", accion }) {
  const color = tono === "warn" ? "border-warn/40 bg-warn/10" : "border-danger/40 bg-danger/10";
  const icono = tono === "warn" ? "text-warn" : "text-danger";
  return (
    <div role="alert" className={`flex gap-3 rounded-xl border p-4 ${color}`}>
      <span aria-hidden="true" className={`grid h-6 w-6 shrink-0 place-items-center rounded-full border border-current text-sm font-bold ${icono}`}>!</span>
      <div className="flex-1">
        <p className="font-semibold">{titulo}</p>
        <p className="mt-1 text-sm text-ink-secondary">{children}</p>
        {accion && <div className="mt-3 flex flex-wrap gap-2">{accion}</div>}
      </div>
    </div>
  );
}

export function EstadoVacio({ titulo, children, accion }) {
  return (
    <div className="rounded-2xl border border-dashed px-6 py-14 text-center">
      <h3 className="text-xl">{titulo}</h3>
      <p className="mx-auto mt-2 max-w-md text-ink-secondary">{children}</p>
      {accion && <div className="mt-5">{accion}</div>}
    </div>
  );
}
