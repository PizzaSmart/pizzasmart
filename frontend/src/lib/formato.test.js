import { centimetros, precio, variantePorDefecto } from "./formato.js";

test("formatea pesos colombianos", () => {
  expect(precio(38900)).toBe("$ 38.900");
  expect(precio("32900.00")).toBe("$ 32.900");
});

test("centímetros por tamaño", () => {
  expect(centimetros("Mediana")).toBe(33);
  expect(centimetros("Pequeña")).toBe(25);
  expect(centimetros("XL")).toBeNull();
});

test("Mediana es el tamaño por defecto", () => {
  const v = [{ id: 1, nombre: "Pequeña" }, { id: 2, nombre: "Mediana" }, { id: 3, nombre: "Grande" }];
  expect(variantePorDefecto(v).id).toBe(2);
  expect(variantePorDefecto([{ id: 9, nombre: "Única" }]).id).toBe(9);
  expect(variantePorDefecto([])).toBeNull();
});
