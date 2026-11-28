import { useCallback, useEffect, useState } from "react";

/** Ejecuta `cargar(signal)` y expone {datos, error, cargando, reintentar}.
 *  Cancela la petición anterior si cambian las dependencias o se desmonta. */
export function useApi(cargar, deps) {
  const [estado, setEstado] = useState({ datos: null, error: null, cargando: true });
  const [intento, setIntento] = useState(0);

  useEffect(() => {
    const control = new AbortController();
    setEstado((e) => ({ ...e, error: null, cargando: true }));
    cargar(control.signal)
      .then((datos) => setEstado({ datos, error: null, cargando: false }))
      .catch((error) => {
        if (error.name !== "AbortError") setEstado({ datos: null, error, cargando: false });
      });
    return () => control.abort();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [...deps, intento]);

  const reintentar = useCallback(() => setIntento((n) => n + 1), []);
  return { ...estado, reintentar };
}
