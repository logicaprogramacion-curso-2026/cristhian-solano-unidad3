"""
Genera datos de ejemplo para TheMarkeT sin necesitar interacción por teclado:
- Al menos 10 ventas (algunas con >=10 unidades para activar el descuento del Reto C)
- Un intento de venta con producto_id inexistente (Reto D) -> queda en log.txt
- Una alta/actualización de producto (Reto A)
- ventas.csv e ingresos.png listos para revisar

Usa backend "Agg" de Matplotlib porque este script corre sin pantalla (headless).
Al ejecutar main.py normalmente (python main.py) en una máquina con entorno gráfico,
Matplotlib usa su backend interactivo por defecto y plt.show() sí abre una ventana.
"""

import os
os.environ.setdefault("MPLBACKEND", "Agg")

from main import (
    CATALOGO_INICIAL, PRECIOS_INICIALES, STOCK_INICIAL,
    ARCHIVO_VENTAS, ARCHIVO_LOG,
    procesar_venta, actualizar_o_agregar_producto,
    guardar_ventas_csv, construir_dataframe,
    calcular_metricas, graficar_ingresos, registrar_log,
)

catalogo = list(CATALOGO_INICIAL)
precios = dict(PRECIOS_INICIALES)
stock = dict(STOCK_INICIAL)
ventas = []
ids_ventas = []

# Reto A: se agrega un producto nuevo y se actualiza precio/stock de uno existente
exito, msg = actualizar_o_agregar_producto(catalogo, precios, stock, "P009", "Papel Higiénico x4", 3.20, 50)
print("Reto A (nuevo producto):", msg)
exito, msg = actualizar_o_agregar_producto(catalogo, precios, stock, "P001", "Arroz 1kg", 1.15, 40)
print("Reto A (actualización):", msg)

# 12 ventas de ejemplo (algunas >=10 unidades -> disparan el 5% de descuento, Reto C)
ventas_demo = [
    ("P001", 5),
    ("P002", 3),
    ("P003", 12),
    ("P004", 8),
    ("P005", 2),
    ("P006", 15),
    ("P007", 4),
    ("P008", 6),
    ("P001", 20),
    ("P002", 7),
    ("P009", 10),
    ("P005", 11),
]

for producto_id, cantidad in ventas_demo:
    exito, resultado = procesar_venta(catalogo, precios, stock, ventas, ids_ventas, producto_id, cantidad)
    if exito:
        v = resultado
        print(f"Venta OK: {v['id_venta']} {v['producto_nombre']} x{v['cantidad']} -> ${v['total']:.2f} "
              f"(desc {v['descuento_pct'] * 100:.0f}%)")
    else:
        print("Venta rechazada:", resultado)

# Reto D: intento de venta con producto_id que NO existe en el catálogo
exito, resultado = procesar_venta(catalogo, precios, stock, ventas, ids_ventas, "P099", 3)
print("Intento con producto inexistente:", resultado, "-> registrado en", ARCHIVO_LOG)

# Guardar CSV (pandas)
df = guardar_ventas_csv(ventas, ARCHIVO_VENTAS)
print(f"\n{len(df)} ventas guardadas en '{ARCHIVO_VENTAS}'.")

# Métricas (NumPy)
calcular_metricas(df)

# Gráfico exportado a PNG (Reto B)
graficar_ingresos(df, mostrar=False, guardar=True, archivo="ingresos.png")

registrar_log("Datos de demostración generados correctamente.", ARCHIVO_LOG)
print("\nListo: ventas.csv, log.txt e ingresos.png generados en este directorio.")
