# MiniTienda – Registro y análisis de ventas

Programa de consola en Python para el desafío **MiniTienda**. Gestiona un
catálogo de productos, registra ventas, persiste datos en CSV, calcula
métricas con NumPy y grafica ingresos por producto con Matplotlib.

## Cómo ejecutar

```bash
pip install numpy pandas matplotlib
python main.py
```

Al iniciar, el programa intenta cargar `ventas.csv` (si no existe, arranca
con historial vacío y lo crea al registrar la primera venta).

## Menú

```
1) Ver catálogo de productos
2) Registrar venta
3) Ver historial de ventas
4) Calcular métricas de ventas
5) Graficar ingresos por producto
6) Exportar gráfico a PNG
7) Agregar nuevo producto al catálogo
0) Salir
```

## Estructura de archivos

| Archivo | Descripción |
|---|---|
| `main.py` | Código fuente del programa |
| `ventas.csv` | Historial de ventas (≥10 registros de ejemplo) |
| `log.txt` | Bitácora de eventos (carga, guardado, errores, intentos fallidos) |
| `ingresos.png` | Captura del gráfico de ingresos por producto (Reto B) |

## Mapeo de requisitos

| Requisito | Dónde está |
|---|---|
| Catálogo con tuplas | `CATALOGO` (lista de tuplas `(id, nombre, categoria)`) |
| Precios/stock con diccionarios | `PRECIOS`, `STOCK` |
| Listas / buffer de ventas / IDs | `ventas_buffer`, `ids_vendidos` |
| Funciones (todo modular) | Cada operación está en su propia función |
| Errores controlados | Input inválido (`pedir_entero`, `pedir_flotante_positivo`), archivo no existe (`cargar_ventas_csv`), división por cero (`calcular_metricas`) |
| Archivos | `ventas.csv` (Pandas) + `log.txt` (`escribir_log`) |
| Pandas | `DataFrame`, `groupby` (`obtener_ingresos_por_producto`), `to_csv`/`read_csv` |
| NumPy | `mean`, `std`, `sum` en `calcular_metricas` |
| Matplotlib | `graficar_ingresos` (gráfico de barras, pantalla o PNG) |
| Control de flujo | `if/elif/else`, `for`, `while`, `break`, `continue`, `try/except/else/finally` en todo el código |

## Retos

- **Reto A** — `agregar_producto_nuevo()` (opción 7): agrega un producto
  nuevo al catálogo y crea sus entradas en `PRECIOS`/`STOCK`.
- **Reto B** — opción **"6) Exportar gráfico a PNG"**, usa
  `plt.savefig("ingresos.png")` dentro de `graficar_ingresos(guardar_png=True)`.
- **Reto C** — dentro de `registrar_venta()`: si `cantidad >= 10` se aplica
  un descuento del 5% sobre el subtotal (`if/else`).
- **Reto D** — dentro de `registrar_venta()`: si el `producto_id` no existe
  en el catálogo, se rechaza la venta y el intento fallido queda registrado
  en `log.txt` con marca de tiempo.

## Notas de diseño

- El stock se actualiza en memoria durante la sesión; solo las ventas se
  persisten en CSV (el stock inicial se reinicia a los valores del código
  en cada ejecución, ya que no forma parte del catálogo persistido).
- Los datos de ejemplo en `ventas.csv` y `log.txt` fueron generados
  ejecutando el programa real con una secuencia de operaciones típicas
  (consulta de catálogo, ventas válidas e inválidas, alta de producto,
  cálculo de métricas y exportación del gráfico).
