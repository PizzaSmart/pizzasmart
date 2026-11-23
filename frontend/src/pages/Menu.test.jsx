import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import Menu from "./Menu.jsx";

const CATEGORIAS = [{ id: 1, nombre: "Clásicas", descripcion: null }, { id: 4, nombre: "Sin gluten", descripcion: null }];
const PIZZA = { id: 1, nombre: "Pamplona", descripcion: "Chorizo", precio_base: 38900, imagen_url: null, categoria_id: 1 };

function simularApi(rutas) {
  globalThis.fetch = vi.fn(async (url) => {
    const ruta = String(url).replace(/^.*\/api\/v1/, "");
    const r = rutas[ruta];
    if (r === "red") throw new TypeError("fail");
    return { ok: r !== undefined, status: r === undefined ? 404 : 200, json: async () => r ?? { error: { mensaje: "no" } } };
  });
}
const abrir = () => render(<MemoryRouter><Menu /></MemoryRouter>);

afterEach(() => vi.restoreAllMocks());

test("muestra las pizzas activas que devuelve la API", async () => {
  simularApi({ "/categorias": CATEGORIAS, "/productos": [PIZZA] });
  abrir();
  expect(await screen.findByText("Pamplona")).toBeInTheDocument();
  expect(screen.getByText("$ 38.900")).toBeInTheDocument();
});

test("catálogo vacío", async () => {
  simularApi({ "/categorias": [], "/productos": [] });
  abrir();
  expect(await screen.findByText("La carta está vacía por ahora")).toBeInTheDocument();
});

test("error de red con botón para reintentar", async () => {
  simularApi({ "/categorias": "red", "/productos": "red" });
  abrir();
  expect(await screen.findByText("No pudimos cargar las pizzas")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Reintentar" })).toBeInTheDocument();
});

test("categoría vacía ofrece «Ver todas»", async () => {
  simularApi({ "/categorias": CATEGORIAS, "/productos": [PIZZA], "/categorias/4/productos": [] });
  abrir();
  await screen.findByText("Pamplona");
  await userEvent.click(screen.getByRole("button", { name: "Sin gluten" }));
  expect(await screen.findByText(/Aún no hay pizzas en Sin gluten/)).toBeInTheDocument();
  await userEvent.click(screen.getByRole("button", { name: "Ver todas" }));
  await waitFor(() => expect(screen.getByText("Pamplona")).toBeInTheDocument());
});
