import { Link, Route, Routes } from "react-router-dom";
import Header from "./components/Header.jsx";
import Menu from "./pages/Menu.jsx";
import DetallePizza from "./pages/DetallePizza.jsx";

function PaginaNoEncontrada() {
  return (
    <div className="mx-auto max-w-xl px-6 py-24 text-center">
      <h1 className="text-3xl">Esta página no existe</h1>
      <p className="mt-3 text-ink-secondary">Revisa el enlace o vuelve a la carta.</p>
      <Link to="/" className="btn-secundario mt-6">Ir al menú</Link>
    </div>
  );
}

export default function App() {
  return (
    <>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Menu />} />
          <Route path="/pizza/:id" element={<DetallePizza />} />
          <Route path="*" element={<PaginaNoEncontrada />} />
        </Routes>
      </main>
      <footer className="mt-16 border-t py-8 text-center text-sm text-ink-dim">
        PizzaSmart · Prototipo académico
      </footer>
    </>
  );
}
