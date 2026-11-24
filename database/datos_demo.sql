-- =====================================================================
-- PizzaSmart · T1-13 · Datos de demostración (HU-01 y HU-02)
-- Responsable: D07 (Backend + recomendador + QA)
--
-- Requisitos: haber ejecutado antes el esquema de T1-09 (las 8 tablas).
-- Es idempotente: se puede ejecutar varias veces (ON CONFLICT DO NOTHING).
--
--   psql "$DATABASE_URL" -f database/datos_demo.sql
--
-- Contenido pensado para probar los casos del sprint:
--   * 4 categorías activas; «Sin gluten» queda vacía a propósito (estado «sin productos»).
--   * 6 pizzas activas + 1 inactiva (Hawaiana): no debe aparecer ni poder comprarse.
--   * Tamaños: Pequeña (x0,8), Mediana (precio base) y Grande (x1,25), redondeados a $100.
--   * 2 pedidos ENTREGADOS para la popularidad del recomendador (HU-09, Sprint 3).
-- Las imágenes viven en frontend/public/img (rutas /img/pizza-N.jpg).
-- =====================================================================

BEGIN;

-- Categorías
INSERT INTO categorias (id, nombre, descripcion, activo) VALUES
  (1, 'Clásicas', 'Las recetas de siempre.', TRUE),
  (2, 'Vegetarianas', 'Sin carne, con mucho sabor.', TRUE),
  (3, 'Picantes', 'Para quienes piden más fuego.', TRUE),
  (4, 'Sin gluten', 'Masa sin gluten (próximamente).', TRUE)
ON CONFLICT (id) DO NOTHING;

-- Ingredientes
INSERT INTO ingredientes (id, nombre, es_vegetariano, calorias_aprox) VALUES
  (1, 'Chorizo pamplonica', FALSE, 230),
  (2, 'Mozzarella', TRUE, 85),
  (3, 'Pimiento del piquillo', TRUE, 20),
  (4, 'Jamón serrano', FALSE, 110),
  (5, 'Espárragos', TRUE, 20),
  (6, 'Rúcula fresca', TRUE, 5),
  (7, 'Parmesano', TRUE, 110),
  (8, 'Champiñones', TRUE, 15),
  (9, 'Pimentón', TRUE, 25),
  (10, 'Cebolla morada', TRUE, 30),
  (11, 'Aceitunas', TRUE, 45),
  (12, 'Tomate San Marzano', TRUE, 25),
  (13, 'Fior di latte', TRUE, 85),
  (14, 'Albahaca fresca', TRUE, 5),
  (15, 'Salami picante', FALSE, 140),
  (16, 'Jalapeño', TRUE, 10),
  (17, 'Miel picante', TRUE, 60),
  (18, 'Gorgonzola', TRUE, 100),
  (19, 'Provolone', TRUE, 95),
  (20, 'Piña', TRUE, 40)
ON CONFLICT (id) DO NOTHING;

-- Productos (precio_base = precio de la Mediana)
INSERT INTO productos (id, categoria_id, nombre, descripcion, precio_base, imagen_url, activo) VALUES
  (1, 1, 'Pamplona', 'Chorizo pamplonica, mozzarella y pimiento del piquillo.', 38900.00, '/img/pizza-1.jpg', TRUE),
  (2, 1, 'Navarra', 'Jamón serrano, espárragos, rúcula fresca y parmesano.', 42900.00, '/img/pizza-2.jpg', TRUE),
  (3, 2, 'Vegetariana', 'Champiñones, pimentón, cebolla morada y aceitunas.', 36900.00, '/img/pizza-3.jpg', TRUE),
  (4, 2, 'Margarita', 'Tomate San Marzano, fior di latte y albahaca fresca.', 32900.00, '/img/pizza-4.jpg', TRUE),
  (5, 3, 'Diablo', 'Salami picante, jalapeño, mozzarella y miel picante.', 40900.00, '/img/pizza-5.jpg', TRUE),
  (6, 2, 'Cuatro quesos', 'Mozzarella, gorgonzola, parmesano y provolone.', 41900.00, '/img/pizza-6.jpg', TRUE),
  (7, 1, 'Hawaiana', 'Jamón serrano, piña y mozzarella. (Inactiva: no debe verse en la carta).', 35900.00, '/img/pizza-1.jpg', FALSE)
ON CONFLICT (id) DO NOTHING;

-- Ingredientes de cada producto
INSERT INTO productos_ingredientes (producto_id, ingrediente_id) VALUES
  (1, 1),
  (1, 2),
  (1, 3),
  (2, 4),
  (2, 5),
  (2, 6),
  (2, 7),
  (2, 2),
  (3, 8),
  (3, 9),
  (3, 10),
  (3, 11),
  (3, 2),
  (4, 12),
  (4, 13),
  (4, 14),
  (5, 15),
  (5, 16),
  (5, 2),
  (5, 17),
  (6, 2),
  (6, 18),
  (6, 7),
  (6, 19),
  (7, 4),
  (7, 20),
  (7, 2)
ON CONFLICT DO NOTHING;

-- Tamaños: precio_adicional se suma al precio base (Pequeña es negativo)
INSERT INTO variantes_producto (id, producto_id, nombre_variante, precio_adicional) VALUES
  (1, 1, 'Pequeña', -7800.00),
  (2, 1, 'Mediana', 0.00),
  (3, 1, 'Grande', 9700.00),
  (4, 2, 'Pequeña', -8600.00),
  (5, 2, 'Mediana', 0.00),
  (6, 2, 'Grande', 10700.00),
  (7, 3, 'Pequeña', -7400.00),
  (8, 3, 'Mediana', 0.00),
  (9, 3, 'Grande', 9200.00),
  (10, 4, 'Pequeña', -6600.00),
  (11, 4, 'Mediana', 0.00),
  (12, 4, 'Grande', 8200.00),
  (13, 5, 'Pequeña', -8200.00),
  (14, 5, 'Mediana', 0.00),
  (15, 5, 'Grande', 10200.00),
  (16, 6, 'Pequeña', -8400.00),
  (17, 6, 'Mediana', 0.00),
  (18, 6, 'Grande', 10500.00),
  (19, 7, 'Pequeña', -7200.00),
  (20, 7, 'Mediana', 0.00),
  (21, 7, 'Grande', 9000.00)
ON CONFLICT (id) DO NOTHING;

-- Pedidos entregados (usuario_id NULL: compra como invitado; los usuarios llegan en el Sprint 2)
INSERT INTO pedidos (id, usuario_id, nombre_cliente, telefono_cliente, direccion_envio, estado, total, creado_en) VALUES
  (1, NULL, 'Laura Méndez', '3001112233', 'Cra 27 # 45-10, Bucaramanga', 'ENTREGADO', 104700.00, '2026-11-10 12:40'),
  (2, NULL, 'Diego Peña', '3004445566', 'Calle 36 # 19-20, Bucaramanga', 'ENTREGADO', 124700.00, '2026-11-10 13:05')
ON CONFLICT (id) DO NOTHING;

-- Detalle de los pedidos con precio unitario histórico
INSERT INTO detalle_pedido (id, pedido_id, producto_id, variante_id, cantidad, precio_unitario_historico) VALUES
  (1, 1, 4, 11, 2, 32900.00),
  (2, 1, 1, 2, 1, 38900.00),
  (3, 2, 5, 14, 2, 40900.00),
  (4, 2, 2, 5, 1, 42900.00)
ON CONFLICT (id) DO NOTHING;

-- Reajusta las secuencias (los ids se insertaron de forma explícita)
SELECT setval(pg_get_serial_sequence('categorias', 'id'), (SELECT MAX(id) FROM categorias));
SELECT setval(pg_get_serial_sequence('ingredientes', 'id'), (SELECT MAX(id) FROM ingredientes));
SELECT setval(pg_get_serial_sequence('productos', 'id'), (SELECT MAX(id) FROM productos));
SELECT setval(pg_get_serial_sequence('variantes_producto', 'id'), (SELECT MAX(id) FROM variantes_producto));
SELECT setval(pg_get_serial_sequence('pedidos', 'id'), (SELECT MAX(id) FROM pedidos));
SELECT setval(pg_get_serial_sequence('detalle_pedido', 'id'), (SELECT MAX(id) FROM detalle_pedido));

COMMIT;
