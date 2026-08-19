"""
MiniTienda - Registro y análisis de ventas
============================================
Programa de consola que gestiona un catálogo de productos, registra ventas,
persiste datos en CSV, calcula métricas con NumPy y grafica ingresos por
producto con Matplotlib.

Mapeo de requisitos:
  - Tuplas            -> CATALOGO (lista de tuplas (id, nombre, categoria))
  - Diccionarios      -> PRECIOS, STOCK
  - Listas/arreglos   -> ventas_buffer (buffer de ventas), ids_vendidos (IDs)
  - Funciones         -> todo el programa está modularizado en funciones
  - Errores           -> input inválido, archivo no existe, división por cero
  - Archivos          -> ventas.csv y log.txt
  - Pandas            -> DataFrame, groupby, to_csv/read_csv
  - NumPy             -> mean, std, sum
  - Matplotlib        -> gráfico de barras (pantalla y exportado a PNG)
  - Control de flujo  -> if/elif/else, for, while, break, continue,
                         try/except/else/finally

Retos:
  - Reto A -> agregar_producto_nuevo()
  - Reto B -> opción "6) Exportar gráfico a PNG" -> graficar_ingresos(guardar_png=True)
  - Reto C -> descuento por cantidad >= 10, dentro de registrar_venta()
  - Reto D -> validación de producto_id inexistente + registro en log.txt,
              dentro de registrar_venta()
"""

import sys
from datetime import datetime

try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError as error:
    print(f"Falta instalar una dependencia: {error}")
    print("Instale las librerías necesarias con: pip install numpy pandas matplotlib")
    sys.exit(1)


# --------------------------------------------------------------------------
# Rutas de archivos
# --------------------------------------------------------------------------
RUTA_VENTAS = "ventas.csv"
RUTA_LOG = "log.txt"
RUTA_GRAFICO = "ingresos.png"


# --------------------------------------------------------------------------
# Catálogo de productos (TUPLAS): (id, nombre, categoria)
# --------------------------------------------------------------------------
CATALOGO = [
    (1, "Cuaderno Universitario", "Papeleria"),
    (2, "Lapiz HB", "Papeleria"),
    (3, "Mochila Escolar", "Accesorios"),
    (4, "Audifonos Bluetooth", "Electronica"),
    (5, "Mouse Inalambrico", "Electronica"),
]

# Precios y stock (DICCIONARIOS), llave = id del producto
PRECIOS = {1: 1.50, 2: 0.75, 3: 28.00, 4: 18.50, 5: 12.00}
STOCK = {1: 150, 2: 300, 3: 25, 4: 40, 5: 35}

# Buffer de ventas (LISTA de diccionarios) y lista de IDs de productos vendidos
ventas_buffer = []
ids_vendidos = []
contador_ventas = 0  # se recalcula al cargar el CSV


# --------------------------------------------------------------------------
# Utilidades de archivos: log.txt
# --------------------------------------------------------------------------
def escribir_log(mensaje):
    """Agrega una línea con marca de tiempo a log.txt."""
    marca_tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(RUTA_LOG, "a", encoding="utf-8") as archivo_log:
        archivo_log.write(f"[{marca_tiempo}] {mensaje}\n")


# --------------------------------------------------------------------------
# Catálogo: búsqueda (FOR) y despliegue
# --------------------------------------------------------------------------
def obtener_producto_por_id(producto_id):
    """Busca un producto en el catálogo (tuplas) mediante un for."""
    for producto in CATALOGO:
        if producto[0] == producto_id:
            return producto
    return None


def mostrar_catalogo():
    print("\n{:<5}{:<25}{:<15}{:<10}{:<8}".format(
        "ID", "Nombre", "Categoria", "Precio", "Stock"))
    print("-" * 63)
    for producto_id, nombre, categoria in CATALOGO:
        precio = PRECIOS.get(producto_id, 0)
        stock = STOCK.get(producto_id, 0)
        print("{:<5}{:<25}{:<15}${:<9.2f}{:<8}".format(
            producto_id, nombre, categoria, precio, stock))


# --------------------------------------------------------------------------
# Entradas validadas (manejo de INPUT INVÁLIDO)
# --------------------------------------------------------------------------
def pedir_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
        except ValueError:
            print("Entrada inválida. Debe ingresar un número entero.")
            continue
        else:
            return valor


def pedir_entero_positivo(mensaje):
    while True:
        valor = pedir_entero(mensaje)
        if valor <= 0:
            print("El valor debe ser mayor a 0.")
            continue
        return valor


def pedir_flotante_positivo(mensaje):
    while True:
        try:
            valor = float(input(mensaje))
        except ValueError:
            print("Entrada inválida. Debe ingresar un número (use punto decimal).")
            continue
        if valor <= 0:
            print("El valor debe ser mayor a 0.")
            continue
        return valor


# --------------------------------------------------------------------------
# Persistencia: CSV con Pandas (try/except/else/finally)
# --------------------------------------------------------------------------
def cargar_ventas_csv():
    """Carga ventas.csv al iniciar. Maneja el caso de ARCHIVO NO EXISTENTE."""
    global ventas_buffer, ids_vendidos, contador_ventas
    try:
        df = pd.read_csv(RUTA_VENTAS)
    except FileNotFoundError:
        print(f"No se encontró '{RUTA_VENTAS}'. Se iniciará con historial vacío.")
        escribir_log(f"'{RUTA_VENTAS}' no encontrado. Historial inicializado vacío.")
        ventas_buffer = []
    else:
        ventas_buffer = df.to_dict("records")
        ids_vendidos = [venta["producto_id"] for venta in ventas_buffer]
        print(f"Se cargaron {len(ventas_buffer)} ventas previas desde '{RUTA_VENTAS}'.")
        escribir_log(f"Se cargaron {len(ventas_buffer)} ventas desde '{RUTA_VENTAS}'.")
    finally:
        contador_ventas = max((v["id_venta"] for v in ventas_buffer), default=0)
        print("Proceso de carga de datos finalizado.\n")


def guardar_ventas_csv():
    """Guarda el buffer de ventas en ventas.csv usando Pandas."""
    try:
        df = pd.DataFrame(ventas_buffer)
        df.to_csv(RUTA_VENTAS, index=False)
    except Exception as error:
        print(f"Error al guardar el archivo CSV: {error}")
        escribir_log(f"ERROR al guardar '{RUTA_VENTAS}': {error}")
    else:
        print(f"Datos guardados correctamente en '{RUTA_VENTAS}' "
              f"({len(ventas_buffer)} ventas en total).")
    finally:
        escribir_log(f"Operación de guardado en '{RUTA_VENTAS}' finalizada.")


# --------------------------------------------------------------------------
# Registrar venta (Reto C: descuento, Reto D: validación + log)
# --------------------------------------------------------------------------
def registrar_venta():
    global contador_ventas
    print("\n--- Registrar venta ---")
    items_vendidos = 0

    while True:
        producto_id = pedir_entero("ID del producto a vender: ")
        producto = obtener_producto_por_id(producto_id)

        # Reto D: producto_id que no está en el catálogo -> log del intento fallido
        if producto is None:
            print(f"El producto con ID {producto_id} no existe en el catálogo.")
            escribir_log(
                f"INTENTO FALLIDO de venta: producto_id {producto_id} "
                f"no existe en el catálogo."
            )
            continue

        cantidad = pedir_entero_positivo(f"Cantidad de '{producto[1]}' a vender: ")

        stock_disponible = STOCK.get(producto_id, 0)
        if cantidad > stock_disponible:
            print(f"Stock insuficiente. Stock disponible: {stock_disponible}.")
            escribir_log(
                f"INTENTO FALLIDO de venta: stock insuficiente para producto_id "
                f"{producto_id} (solicitado {cantidad}, disponible {stock_disponible})."
            )
            continue

        precio_unitario = PRECIOS[producto_id]
        subtotal_bruto = precio_unitario * cantidad

        # Reto C: descuento del 5% si la cantidad vendida es >= 10 unidades
        if cantidad >= 10:
            descuento_pct = 5.0
        else:
            descuento_pct = 0.0
        subtotal = round(subtotal_bruto * (1 - descuento_pct / 100), 2)

        STOCK[producto_id] = stock_disponible - cantidad
        contador_ventas += 1

        venta = {
            "id_venta": contador_ventas,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "producto_id": producto_id,
            "producto": producto[1],
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "descuento_pct": descuento_pct,
            "subtotal": subtotal,
        }
        ventas_buffer.append(venta)
        ids_vendidos.append(producto_id)
        items_vendidos += 1

        detalle_descuento = f" (descuento {descuento_pct:.0f}% aplicado)" if descuento_pct else ""
        print(f"Venta registrada: {cantidad} x {producto[1]} = ${subtotal:.2f}{detalle_descuento}")

        continuar = input("¿Agregar otro producto a esta venta? (s/n): ").strip().lower()
        if continuar != "s":
            break

    if items_vendidos > 0:
        guardar_ventas_csv()
    else:
        print("No se registró ningún producto en esta venta.")


# --------------------------------------------------------------------------
# Historial (Pandas DataFrame)
# --------------------------------------------------------------------------
def mostrar_historial():
    if not ventas_buffer:
        print("Aún no hay ventas registradas.")
        return
    df = pd.DataFrame(ventas_buffer)
    print("\n--- Historial de ventas ---")
    print(df.to_string(index=False))


# --------------------------------------------------------------------------
# Métricas con NumPy + ingresos por producto con Pandas groupby
# (división por cero controlada)
# --------------------------------------------------------------------------
def obtener_ingresos_por_producto():
    if not ventas_buffer:
        return None
    df = pd.DataFrame(ventas_buffer)
    return df.groupby("producto")["subtotal"].sum().sort_values(ascending=False)


def calcular_metricas():
    print("\n--- Métricas de ventas ---")
    total_ventas = len(ventas_buffer)
    total_ingresos = sum(venta["subtotal"] for venta in ventas_buffer)

    # División por cero controlada con try/except/else/finally
    try:
        promedio_por_venta = total_ingresos / total_ventas
    except ZeroDivisionError:
        print("Aún no hay ventas registradas; no se puede calcular el promedio.")
        escribir_log("Cálculo de métricas sin ventas registradas (división por cero controlada).")
    else:
        print(f"Ingreso promedio por venta: ${promedio_por_venta:.2f}")
    finally:
        print("(cálculo de promedio finalizado)")

    if total_ventas == 0:
        return

    cantidades = np.array([venta["cantidad"] for venta in ventas_buffer], dtype=float)
    subtotales = np.array([venta["subtotal"] for venta in ventas_buffer], dtype=float)

    print(f"Unidades vendidas -> media: {cantidades.mean():.2f} | "
          f"desv. estándar: {cantidades.std():.2f} | total: {cantidades.sum():.0f}")
    print(f"Ingresos ($)      -> media: {subtotales.mean():.2f} | "
          f"desv. estándar: {subtotales.std():.2f} | total: {subtotales.sum():.2f}")
    print(f"Productos distintos vendidos (histórico): {len(set(ids_vendidos))}")

    ingresos_producto = obtener_ingresos_por_producto()
    print("\nIngresos totales por producto (pandas groupby):")
    for producto, ingreso in ingresos_producto.items():
        print(f"  {producto}: ${ingreso:.2f}")


# --------------------------------------------------------------------------
# Matplotlib: gráfico de barras (Reto B: exportar a PNG)
# --------------------------------------------------------------------------
def graficar_ingresos(guardar_png=False):
    ingresos = obtener_ingresos_por_producto()
    if ingresos is None or ingresos.empty:
        print("No hay datos de ventas para graficar todavía.")
        return

    productos = ingresos.index.tolist()
    valores = ingresos.values

    plt.figure(figsize=(8, 5))
    plt.bar(productos, valores, color="#4C72B0")
    plt.title("Ingresos por producto - MiniTienda")
    plt.xlabel("Producto")
    plt.ylabel("Ingresos ($)")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()

    if guardar_png:
        plt.savefig(RUTA_GRAFICO)  # Reto B
        print(f"Gráfico exportado como '{RUTA_GRAFICO}'.")
        escribir_log(f"Gráfico de ingresos exportado a '{RUTA_GRAFICO}'.")
    else:
        plt.show()
    plt.close()


# --------------------------------------------------------------------------
# Reto A: agregar producto nuevo y actualizar precios/stock
# --------------------------------------------------------------------------
def agregar_producto_nuevo():
    print("\n--- Agregar nuevo producto al catálogo ---")

    nuevo_id = pedir_entero("ID del nuevo producto: ")
    if obtener_producto_por_id(nuevo_id) is not None:
        print("Ya existe un producto con ese ID. Operación cancelada.")
        return

    nombre = input("Nombre del producto: ").strip()
    categoria = input("Categoría: ").strip()
    precio = pedir_flotante_positivo("Precio unitario: ")
    stock_inicial = pedir_entero("Stock inicial: ")

    if stock_inicial < 0:
        print("El stock no puede ser negativo. Operación cancelada.")
        return

    CATALOGO.append((nuevo_id, nombre, categoria))
    PRECIOS[nuevo_id] = precio
    STOCK[nuevo_id] = stock_inicial

    print(f"Producto '{nombre}' agregado correctamente con ID {nuevo_id}.")
    escribir_log(
        f"Nuevo producto agregado: ID {nuevo_id}, {nombre}, "
        f"precio ${precio:.2f}, stock inicial {stock_inicial}."
    )


# --------------------------------------------------------------------------
# Menú principal (WHILE, IF/ELIF/ELSE, BREAK, CONTINUE)
# --------------------------------------------------------------------------
def mostrar_menu():
    print("\n" + "=" * 42)
    print("           MENU - MINITIENDA")
    print("=" * 42)
    print("1) Ver catálogo de productos")
    print("2) Registrar venta")
    print("3) Ver historial de ventas")
    print("4) Calcular métricas de ventas")
    print("5) Graficar ingresos por producto")
    print("6) Exportar gráfico a PNG")
    print("7) Agregar nuevo producto al catálogo")
    print("0) Salir")
    print("=" * 42)


def main():
    print("Bienvenido a MiniTienda\n")
    cargar_ventas_csv()
    escribir_log("Inicio de sesión de MiniTienda.")

    intentos_invalidos = 0
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            mostrar_catalogo()
        elif opcion == "2":
            registrar_venta()
        elif opcion == "3":
            mostrar_historial()
        elif opcion == "4":
            calcular_metricas()
        elif opcion == "5":
            graficar_ingresos(guardar_png=False)
        elif opcion == "6":
            graficar_ingresos(guardar_png=True)
        elif opcion == "7":
            agregar_producto_nuevo()
        elif opcion == "0":
            print("Guardando datos antes de salir...")
            guardar_ventas_csv()
            escribir_log("Cierre de sesión de MiniTienda.")
            print("¡Hasta pronto!")
            break
        else:
            intentos_invalidos += 1
            print("Opción no válida. Intente nuevamente.")
            if intentos_invalidos >= 5:
                print("Demasiados intentos inválidos. Cerrando el programa.")
                escribir_log("Cierre forzado por demasiadas opciones inválidas.")
                break
            continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
        escribir_log("Programa interrumpido con Ctrl+C.")
    except Exception as error:
        print(f"Ocurrió un error inesperado: {error}")
        escribir_log(f"ERROR inesperado: {error}")
