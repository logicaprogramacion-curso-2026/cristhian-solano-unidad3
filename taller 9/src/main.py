from database import Database
from dao import preguntaDAO
from gestor import Gestor
from simulador import Simulador
import os


# ============================
# CONFIGURACIÓN
# ============================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

RUTA_DATOS = os.path.join(
    BASE_DIR,
    "datos"
)

RUTA_RESULTADOS = os.path.join(
    BASE_DIR,
    "resultados"
)

os.makedirs(
    RUTA_RESULTADOS,
    exist_ok=True
)


# ============================
# BASE DE DATOS
# ============================

db = Database()

dao = preguntaDAO(db)

gestor = Gestor(dao)

dao.crear_tabla()



# ============================
# MENÚS
# ============================

def menu_principal():

    print("\n==============================")
    print(" BANCO DE PREGUNTAS PYTHON")
    print("==============================")

    print("1. Cargar preguntas desde archivo")
    print("2. Ver todas las preguntas")
    print("3. Ver estadísticas")
    print("4. Iniciar simulación")
    print("5. Exportar datos")
    print("6. Ver reportes")
    print("7. Salir")



def menu_carga():

    print("\nSeleccione archivo:")

    print("1. TXT")
    print("2. CSV")
    print("3. JSON")



def menu_exportar():

    print("\nExportar datos:")

    print("1. TXT")
    print("2. CSV")
    print("3. JSON")
    print("4. Todos")



def menu_estadisticas():

    print("\nEstadísticas:")

    print("1. Por tema")
    print("2. Por dificultad")
    print("3. Ambas")



# ============================
# PROGRAMA PRINCIPAL
# ============================

while True:

    menu_principal()

    opcion = input(
        "Seleccione una opción: "
    )


    try:


        # ====================
        # CARGAR
        # ====================

        if opcion == "1":

            menu_carga()

            archivo = input(
                "Seleccione: "
            )


            if archivo == "1":

                gestor.cargar_desde_txt(
                    os.path.join(
                        RUTA_DATOS,
                        "PREGUNTAS_PYTHON.txt"
                    )
                )


            elif archivo == "2":

                gestor.cargar_desde_csv(
                    os.path.join(
                        RUTA_DATOS,
                        "PREGUNTAS_PYTHON.csv"
                    )
                )


            elif archivo == "3":

                gestor.cargar_desde_json(
                    os.path.join(
                        RUTA_DATOS,
                        "PREGUNTAS_PYTHON.json"
                    )
                )


            else:

                print("Opción inválida.")
                continue


            print(
                f"\nPreguntas cargadas: {len(gestor.preguntas)}"
            )



        # ====================
        # VER PREGUNTAS
        # ====================

        elif opcion == "2":

            if not gestor.preguntas:

                print(
                    "No existen preguntas cargadas."
                )

            else:

                for i, pregunta in enumerate(
                    gestor.preguntas,
                    1
                ):

                    print(
                        f"\n{i}. {pregunta.pregunta}"
                    )



        # ====================
        # ESTADÍSTICAS
        # ====================

        elif opcion == "3":

            menu_estadisticas()

            op = input(
                "Seleccione: "
            )


            if op == "1":

                gestor.estadisticas_por_tema()


            elif op == "2":

                gestor.estadisticas_por_dificultad()


            elif op == "3":

                gestor.estadisticas_por_tema()

                gestor.estadisticas_por_dificultad()


            else:

                print("Opción inválida.")



        # ====================
        # SIMULACIÓN
        # ====================

        elif opcion == "4":

            if not gestor.preguntas:

                print(
                    "Primero debe cargar preguntas."
                )

                continue


            cantidad = int(
                input(
                    "Cantidad de preguntas: "
                )
            )


            simulador = Simulador(
                gestor.preguntas
            )


            simulador.iniciar_simulacion(
                cantidad
            )


            simulador.reporte_txt()

            simulador.reporte_csv()

            simulador.reporte_json()



        # ====================
        # EXPORTAR
        # ====================

        elif opcion == "5":

            menu_exportar()

            op = input(
                "Seleccione: "
            )


            if op == "1":

                gestor.exportar_a_txt(
                    os.path.join(
                        RUTA_RESULTADOS,
                        "preguntas_exportadas.txt"
                    )
                )


            elif op == "2":

                gestor.exportar_a_csv(
                    os.path.join(
                        RUTA_RESULTADOS,
                        "preguntas_exportadas.csv"
                    )
                )


            elif op == "3":

                gestor.exportar_a_json(
                    os.path.join(
                        RUTA_RESULTADOS,
                        "preguntas_exportadas.json"
                    )
                )


            elif op == "4":

                gestor.exportar_a_txt(
                    os.path.join(
                        RUTA_RESULTADOS,
                        "preguntas_exportadas.txt"
                    )
                )

                gestor.exportar_a_csv(
                    os.path.join(
                        RUTA_RESULTADOS,
                        "preguntas_exportadas.csv"
                    )
                )

                gestor.exportar_a_json(
                    os.path.join(
                        RUTA_RESULTADOS,
                        "preguntas_exportadas.json"
                    )
                )


            else:

                print("Opción inválida.")



        # ====================
        # REPORTES
        # ====================

        elif opcion == "6":

            print("\nReportes disponibles:")

            print(
                " - resultados/respuestas_usuario.txt"
            )

            print(
                " - resultados/estadisticas.csv"
            )

            print(
                " - resultados/reporte.json"
            )



        # ====================
        # SALIR
        # ====================

        elif opcion == "7":

            db.cerrar()

            print(
                "\nPrograma finalizado."
            )

            break


        else:

            print(
                "Opción inválida."
            )


    except Exception as error:

        print(
            "\nError:",
            error
        )