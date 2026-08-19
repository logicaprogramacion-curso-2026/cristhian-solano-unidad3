"""
TheMarkeT - MiniTienda
Programa de consola para registro y análisis de ventas.

Estructuras usadas:
- Tuplas: cada producto del catálogo es una tupla (id, nombre)
- Diccionarios: precios y stock, indexados por id de producto
- Listas: buffer de ventas (lista de dicts) e IDs de venta
- Pandas: DataFrame de ventas, groupby, lectura/escritura de CSV
- NumPy: mean, std, sum sobre los montos de las ventas
- Matplotlib: gráfico de barras de ingresos por producto
"""

from datetime import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Datos iniciales
# ---------------------------------------------------------------------------

# Catálogo inicial: tupla de tuplas (producto_id, nombre).
# En tiempo de ejecución se trabaja como lista de tuplas para poder
# agregar productos nuevos (Reto A) sin perder la estructura de tupla
# por registro.
CATALOGO_INICIAL = (
    ("P001", "Arroz 1kg"),
    ("P002", "Aceite 1L"),
    ("P003", "Leche 1L"),
    ("P004", "Pan Molde"),
    ("P005", "Huevos x30"),
    ("P006", "Azúcar 1kg"),
    ("P007", "Café 250g"),
    ("P008", "Detergente 1kg"),
)

PRECIOS_INICIALES = {
    "P001": 1.10,
    "P002": 2.35,
    "P003": 0.95,
    "P004": 1.75,
    "P005": 4.20,
    "P006": 1.05,
    "P007": 3.60,
    "P008": 2.90,
}

STOCK_INICIAL = {
    "P001": 150,
    "P002": 120,
    "P003": 200,
    "P004": 80,
    "P005": 60,
    "P006": 140,
    "P007": 90,
    "P008": 75,
}

ARCHIVO_VENTAS = "ventas.csv"
ARCHIVO_LOG = "log.txt"
COLUMNAS_VENTAS = [
    "id_venta", "producto_id", "producto_nombre", "cantidad",
    "precio_unitario", "descuento_pct", "subtotal", "total", "fecha",
]


# ---------------------------------------------------------------------------
# Archivos / logging
# ---------------------------------------------------------------------------

def registrar_log(mensaje, archivo_log=ARCHIVO_LOG):
    """Escribe un mensaje con marca de tiempo en el archivo de log."""
    with open(archivo_log, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {mensaje}\n")


def cargar_ventas_csv(archivo=ARCHIVO_VENTAS):
    """Lee el historial de ventas desde CSV. Maneja el caso de archivo inexistente
    con try/except/else/finally."""
    df = None
    try:
        df = pd.read_csv(archivo)
    except FileNotFoundError:
        print(f"No se encontró '{archivo}'; se iniciará con un historial vacío.")
        df = pd.DataFrame(columns=COLUMNAS_VENTAS)
    else:
        print(f"Se cargaron {len(df)} ventas desde '{archivo}'.")
    finally:
        registrar_log(f"Intento de carga de '{archivo}' finalizado.")
    return df


def guardar_ventas_csv(ventas, archivo=ARCHIVO_VENTAS):
    """Guarda el buffer de ventas (lista de dicts) como CSV vía pandas."""
    df = construir_dataframe(ventas)
    df.to_csv(archivo, index=False)
    return df


# ---------------------------------------------------------------------------
# Catálogo / productos
# ---------------------------------------------------------------------------

def obtener_nombre_producto(catalogo, producto_id):
    for pid, nombre in catalogo:  # recorrido con for
        if pid == producto_id:
            return nombre
    return None


def producto_existe(catalogo, producto_id):
    return obtener_nombre_producto(catalogo, producto_id) is not None


def mostrar_catalogo(catalogo, precios, stock):
    print("\n--- Catálogo TheMarkeT ---")
    for producto_id, nombre in catalogo:
        precio = precios.get(producto_id, 0.0)
        disponible = stock.get(producto_id, 0)
        print(f"{producto_id:<6} {nombre:<20} ${precio:>6.2f}   Stock: {disponible}")


def actualizar_o_agregar_producto(catalogo, precios, stock, producto_id, nombre, precio, cantidad_stock):
    """Reto A: agrega un producto nuevo o actualiza precio/stock de uno existente.
    Lógica pura (sin input) para poder probarla también desde un script/demo."""
    if precio < 0 or cantidad_stock < 0:
        return False, "Precio y stock deben ser valores no negativos."

    if producto_existe(catalogo, producto_id):
        precios[producto_id] = precio
        stock[producto_id] = stock.get(producto_id, 0) + cantidad_stock
        return True, f"Producto '{producto_id}' actualizado (precio y stock)."
    else:
        catalogo.append((producto_id, nombre))
        precios[producto_id] = precio
        stock[producto_id] = cantidad_stock
        return True, f"Producto '{nombre}' agregado al catálogo con ID '{producto_id}'."


def agregar_producto(catalogo, precios, stock):
    """Wrapper interactivo de actualizar_o_agregar_producto (Reto A)."""
    producto_id = input("ID del producto (nuevo o existente): ").strip().upper()
    nombre = input("Nombre del producto: ").strip()
    try:
        precio = float(input("Precio unitario: $"))
        cantidad_stock = int(input("Stock inicial/adicional: "))
    except ValueError:
        print("Entrada inválida: precio y stock deben ser numéricos.")
        return

    exito, mensaje = actualizar_o_agregar_producto(
        catalogo, precios, stock, producto_id, nombre, precio, cantidad_stock
    )
    print(mensaje)


# ---------------------------------------------------------------------------
# Ventas
# ---------------------------------------------------------------------------

def calcular_descuento(cantidad, porcentaje=0.05, umbral=10):
    """Reto C: 5% de descuento si la cantidad vendida es >= 10 unidades."""
    if cantidad >= umbral:
        return porcentaje
    return 0.0


def procesar_venta(catalogo, precios, stock, ventas, ids_ventas, producto_id, cantidad, archivo_log=ARCHIVO_LOG):
    """Núcleo de la lógica de venta. Devuelve (True, venta_dict) o (False, motivo).
    Reutilizable desde el menú interactivo o desde un script de demo."""

    # Reto D: valida producto_id inexistente y registra el intento fallido en log.txt
    if not producto_existe(catalogo, producto_id):
        registrar_log(
            f"Intento fallido de venta: producto_id '{producto_id}' no existe en el catálogo.",
            archivo_log,
        )
        return False, "producto no encontrado en el catálogo"

    if cantidad <= 0:
        registrar_log(
            f"Intento fallido de venta: cantidad inválida ({cantidad}) para '{producto_id}'.",
            archivo_log,
        )
        return False, "la cantidad debe ser mayor que cero"

    if stock.get(producto_id, 0) < cantidad:
        registrar_log(
            f"Intento fallido de venta: stock insuficiente para '{producto_id}' "
            f"(solicitado {cantidad}, disponible {stock.get(producto_id, 0)}).",
            archivo_log,
        )
        return False, "stock insuficiente"

    precio_unitario = precios[producto_id]
    descuento_pct = calcular_descuento(cantidad)
    subtotal = precio_unitario * cantidad
    total = subtotal * (1 - descuento_pct)

    stock[producto_id] -= cantidad

    id_venta = f"V{len(ids_ventas) + 1:04d}"
    ids_ventas.append(id_venta)  # lista de IDs de venta

    venta = {
        "id_venta": id_venta,
        "producto_id": producto_id,
        "producto_nombre": obtener_nombre_producto(catalogo, producto_id),
        "cantidad": cantidad,
        "precio_unitario": precio_unitario,
        "descuento_pct": descuento_pct,
        "subtotal": round(subtotal, 2),
        "total": round(total, 2),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    ventas.append(venta)  # buffer de ventas (lista)
    return True, venta


def input_registrar_venta(catalogo, precios, stock, ventas, ids_ventas):
    """Wrapper interactivo de procesar_venta, con validación de entrada."""
    mostrar_catalogo(catalogo, precios, stock)

    while True:
        producto_id = input("ID del producto a vender (o 'cancelar'): ").strip().upper()
        if producto_id.lower() == "cancelar":
            print("Venta cancelada.")
            return
        if not producto_existe(catalogo, producto_id):
            registrar_log(f"Intento fallido de venta: producto_id '{producto_id}' no existe en el catálogo.")
            print("Ese producto no existe en el catálogo. Intente nuevamente.")
            continue
        break

    while True:
        entrada = input("Cantidad a vender: ").strip()
        try:
            cantidad = int(entrada)
        except ValueError:
            print("Entrada inválida: debe ser un número entero.")
            continue
        if cantidad <= 0:
            print("La cantidad debe ser mayor que cero.")
            continue
        break

    exito, resultado = procesar_venta(catalogo, precios, stock, ventas, ids_ventas, producto_id, cantidad)
    if exito:
        venta = resultado
        print(
            f"Venta registrada: {venta['id_venta']} | {venta['producto_nombre']} x{venta['cantidad']} "
            f"-> ${venta['total']:.2f} (descuento {venta['descuento_pct'] * 100:.0f}%)"
        )
    else:
        print(f"No se pudo registrar la venta: {resultado}")


# ---------------------------------------------------------------------------
# Análisis: pandas / numpy / matplotlib
# ---------------------------------------------------------------------------

def construir_dataframe(ventas):
    if not ventas:
        return pd.DataFrame(columns=COLUMNAS_VENTAS)
    return pd.DataFrame(ventas)


def mostrar_historial(df):
    if df.empty:
        print("Todavía no hay ventas registradas.")
        return
    print(df.to_string(index=False))


def ingresos_por_producto(df):
    """Ingresos totales agrupados por producto (pandas groupby)."""
    if df.empty:
        return pd.Series(dtype=float)
    return df.groupby("producto_nombre")["total"].sum().sort_values(ascending=False)


def calcular_metricas(df):
    """Métricas con NumPy: mean, std, sum sobre los montos de venta."""
    if df.empty:
        print("No hay ventas registradas todavía.")
        return

    totales = df["total"].to_numpy()
    cantidades = df["cantidad"].to_numpy()

    suma_total = float(np.sum(totales))
    promedio = float(np.mean(totales))
    desviacion = float(np.std(totales))
    unidades_totales = int(np.sum(cantidades))

    # División por cero controlada (precio promedio por unidad vendida)
    try:
        precio_promedio_unidad = suma_total / unidades_totales
    except ZeroDivisionError:
        precio_promedio_unidad = 0.0

    print("\n--- Métricas (NumPy) ---")
    print(f"Ingresos totales:                 ${suma_total:.2f}")
    print(f"Ingreso promedio por venta:        ${promedio:.2f}")
    print(f"Desviación estándar de ventas:      ${desviacion:.2f}")
    print(f"Unidades totales vendidas:          {unidades_totales}")
    print(f"Precio promedio por unidad vendida: ${precio_promedio_unidad:.2f}")


def graficar_ingresos(df, mostrar=True, guardar=False, archivo="ingresos.png"):
    """Gráfico de barras de ingresos por producto. mostrar=True hace plt.show();
    guardar=True exporta con plt.savefig (Reto B)."""
    ingresos = ingresos_por_producto(df)
    if ingresos.empty:
        print("No hay datos suficientes para graficar todavía.")
        return

    plt.figure(figsize=(8, 5))
    plt.bar(ingresos.index, ingresos.values, color="#4C72B0")
    plt.title("Ingresos por producto - TheMarkeT")
    plt.xlabel("Producto")
    plt.ylabel("Ingresos ($)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    if guardar:
        plt.savefig(archivo)
        print(f"Gráfico exportado como '{archivo}'.")
    if mostrar:
        plt.show()
    plt.close()


# ---------------------------------------------------------------------------
# Menú principal
# ---------------------------------------------------------------------------

def mostrar_menu():
    print("\n===== TheMarkeT - MiniTienda =====")
    print("1) Ver catálogo")
    print("2) Registrar venta")
    print("3) Ver historial de ventas")
    print("4) Calcular métricas (NumPy)")
    print("5) Graficar ingresos por producto")
    print("6) Exportar gráfico a PNG")
    print("7) Agregar/actualizar producto")
    print("8) Guardar y salir")
    print("===================================")


def main():
    catalogo = list(CATALOGO_INICIAL)
    precios = dict(PRECIOS_INICIALES)
    stock = dict(STOCK_INICIAL)

    df_previo = cargar_ventas_csv(ARCHIVO_VENTAS)
    ventas = df_previo.to_dict("records") if not df_previo.empty else []
    ids_ventas = [v["id_venta"] for v in ventas]

    registrar_log("Inicio de sesión de TheMarkeT.")

    while True:
        mostrar_menu()
        opcion_raw = input("Seleccione una opción: ").strip()

        try:
            opcion = int(opcion_raw)
        except ValueError:
            print("Opción inválida: ingrese un número del menú.")
            continue

        if opcion == 1:
            mostrar_catalogo(catalogo, precios, stock)
        elif opcion == 2:
            input_registrar_venta(catalogo, precios, stock, ventas, ids_ventas)
        elif opcion == 3:
            mostrar_historial(construir_dataframe(ventas))
        elif opcion == 4:
            calcular_metricas(construir_dataframe(ventas))
        elif opcion == 5:
            graficar_ingresos(construir_dataframe(ventas), mostrar=True, guardar=False)
        elif opcion == 6:
            graficar_ingresos(construir_dataframe(ventas), mostrar=False, guardar=True, archivo="ingresos.png")
        elif opcion == 7:
            agregar_producto(catalogo, precios, stock)
        elif opcion == 8:
            guardar_ventas_csv(ventas, ARCHIVO_VENTAS)
            registrar_log("Cierre de sesión: ventas guardadas en CSV.")
            print(f"Datos guardados en '{ARCHIVO_VENTAS}'. ¡Hasta la próxima!")
            break
        else:
            print("Opción fuera de rango (1-8). Intente de nuevo.")
            continue


if __name__ == "__main__":
    main()
