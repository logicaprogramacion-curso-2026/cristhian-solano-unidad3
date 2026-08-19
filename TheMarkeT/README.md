# TheMarkeT — MiniTienda

Programa de consola en Python para registro y análisis de ventas.

## Archivos

- `main.py` — programa principal (menú interactivo).
- `demo_generar_datos.py` — genera datos de ejemplo sin usar `input()` (12 ventas, un intento fallido y un alta de producto), para tener `ventas.csv`, `log.txt` e `ingresos.png` listos de entrega.
- `ventas.csv` — historial de ventas generado por la demo.
- `log.txt` — log de eventos e intentos fallidos.
- `ingresos.png` — gráfico de ingresos por producto (Reto B).

## Cómo ejecutar

```bash
pip install pandas numpy matplotlib
python main.py
```

Al ejecutarlo en una máquina con entorno gráfico, la opción **5) Graficar ingresos por producto**
abre una ventana con `plt.show()`. La opción **6) Exportar gráfico a PNG** guarda `ingresos.png`
con `plt.savefig()` sin necesidad de pantalla.

Para regenerar los datos de ejemplo sin usar el menú:

```bash
python demo_generar_datos.py
```

## Cobertura de requisitos

| Requisito | Dónde |
|---|---|
| Tuplas (catálogo) | `CATALOGO_INICIAL`, cada producto es `(id, nombre)` |
| Diccionarios (precio/stock) | `PRECIOS_INICIALES`, `STOCK_INICIAL` |
| Listas (buffer de ventas / IDs) | `ventas`, `ids_ventas` en `main()` |
| Funciones modulares | todo el programa está dividido en funciones de un solo propósito |
| Errores controlados | `try/except` en menú, cantidad, precio/stock (Reto A) y `ZeroDivisionError` en métricas |
| Archivo no existe | `cargar_ventas_csv()` (try/except/else/finally) |
| ventas.csv + log.txt | `guardar_ventas_csv()`, `registrar_log()` |
| Pandas: DataFrame + groupby + CSV | `construir_dataframe()`, `ingresos_por_producto()`, `guardar_ventas_csv()` |
| NumPy: mean/std/sum | `calcular_metricas()` |
| Matplotlib: gráfico de barras | `graficar_ingresos()` |
| Menú con while + control de flujo | `main()`: `if/elif/else`, `for`, `while`, `break`, `continue`, `try/except/else/finally` |
| Reto A (agregar/actualizar producto) | `actualizar_o_agregar_producto()`, opción 7 del menú |
| Reto B (exportar PNG) | opción 6 del menú, `plt.savefig("ingresos.png")` |
| Reto C (descuento 5% si cantidad ≥ 10) | `calcular_descuento()` |
| Reto D (validar producto inexistente + log) | `procesar_venta()` |
