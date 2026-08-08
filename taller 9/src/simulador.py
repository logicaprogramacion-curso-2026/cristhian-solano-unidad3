import random
import json
import os
import csv
from datetime import datetime


class Simulador:

    def __init__(self, preguntas):

        self.preguntas = preguntas
        self.respuestas_usuario = []
        self.puntaje = 0
        self.total = 0
        self.fecha_simulacion = datetime.now()


    def obtener_ruta_resultados(self):

        BASE_DIR = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        ruta_resultados = os.path.join(
            BASE_DIR,
            "resultados"
        )

        os.makedirs(
            ruta_resultados,
            exist_ok=True
        )

        return ruta_resultados


    def iniciar_simulacion(self, cantidad):

        if cantidad > len(self.preguntas):
            cantidad = len(self.preguntas)

        preguntas_seleccionadas = random.sample(
            self.preguntas,
            cantidad
        )

        self.total = cantidad

        print("\n===== SIMULADOR DE PREGUNTAS =====")


        for pregunta in preguntas_seleccionadas:

            self.mostrar_pregunta(pregunta)


        print("\nSimulación finalizada")
        print(
            f"Puntaje obtenido: {self.puntaje}/{self.total}"
        )


    def mostrar_pregunta(self, pregunta):

        print("\n--------------------------------")
        print(pregunta.pregunta)

        print(f"A) {pregunta.opcion_a}")
        print(f"B) {pregunta.opcion_b}")
        print(f"C) {pregunta.opcion_c}")
        print(f"D) {pregunta.opcion_d}")


        respuesta = input(
            "Seleccione una respuesta (A-D): "
        ).upper()


        correcta = self.validar_respuesta(
            respuesta,
            pregunta.respuesta_correcta
        )


        if correcta:

            print("✓ Respuesta correcta")
            self.puntaje += 1

        else:

            print(
                f"✗ Respuesta incorrecta. "
                f"La respuesta era {pregunta.respuesta_correcta}"
            )


        self.respuestas_usuario.append(
            {
                "pregunta": pregunta.pregunta,
                "respuesta_usuario": respuesta,
                "respuesta_correcta": pregunta.respuesta_correcta,
                "resultado": correcta
            }
        )


    def validar_respuesta(self, respuesta, correcta):

        opciones_validas = [
            "A",
            "B",
            "C",
            "D"
        ]

        return respuesta in opciones_validas and respuesta == correcta



    def obtener_estadisticas_tema(self):

        temas = {}


        for respuesta in self.respuestas_usuario:

            tema = respuesta.get(
                "tema",
                "Sin tema"
            )


            temas[tema] = temas.get(
                tema,
                0
            ) + 1


        return temas



    def obtener_estadisticas_dificultad(self):

        dificultades = {}


        for respuesta in self.respuestas_usuario:

            dificultad = respuesta.get(
                "dificultad",
                "Sin dificultad"
            )


            dificultades[dificultad] = dificultades.get(
                dificultad,
                0
            ) + 1


        return dificultades



    def reporte_txt(self):

        ruta = os.path.join(
            self.obtener_ruta_resultados(),
            "respuestas_usuario.txt"
        )


        with open(
            ruta,
            "w",
            encoding="utf-8"
        ) as archivo:


            archivo.write(
                "===== REPORTE DE SIMULACIÓN =====\n\n"
            )


            archivo.write(
                f"Fecha y hora: {self.fecha_simulacion}\n"
            )


            archivo.write(
                f"Puntaje obtenido: {self.puntaje}/{self.total}\n\n"
            )


            archivo.write(
                "PREGUNTAS Y RESPUESTAS:\n"
            )


            for r in self.respuestas_usuario:

                archivo.write(
                    "\nPregunta: "
                    + r["pregunta"]
                )

                archivo.write(
                    "\nRespuesta usuario: "
                    + r["respuesta_usuario"]
                )

                archivo.write(
                    "\nRespuesta correcta: "
                    + r["respuesta_correcta"]
                )

                archivo.write(
                    "\nResultado: "
                    + str(r["resultado"])
                )

                archivo.write(
                    "\n----------------------------\n"
                )


            archivo.write(
                "\nEstadísticas por tema:\n"
            )

            archivo.write(
                str(
                    self.obtener_estadisticas_tema()
                )
            )


            archivo.write(
                "\n\nEstadísticas por dificultad:\n"
            )


            archivo.write(
                str(
                    self.obtener_estadisticas_dificultad()
                )
            )


        print("TXT generado correctamente")



    def reporte_csv(self):

        ruta = os.path.join(
            self.obtener_ruta_resultados(),
            "estadisticas.csv"
        )


        with open(
            ruta,
            "w",
            newline="",
            encoding="utf-8"
        ) as archivo:


            escritor = csv.writer(archivo)


            escritor.writerow(
                [
                    "Fecha",
                    "Pregunta",
                    "Respuesta Usuario",
                    "Respuesta Correcta",
                    "Resultado"
                ]
            )


            for r in self.respuestas_usuario:

                escritor.writerow(
                    [
                        self.fecha_simulacion,
                        r["pregunta"],
                        r["respuesta_usuario"],
                        r["respuesta_correcta"],
                        r["resultado"]
                    ]
                )


        print("CSV generado correctamente")



    def reporte_json(self):

        reporte = {

            "fecha_simulacion":
                str(self.fecha_simulacion),

            "total_preguntas":
                self.total,

            "puntaje":
                self.puntaje,

            "respuestas_correctas":
                self.puntaje,

            "respuestas_incorrectas":
                self.total - self.puntaje,

            "preguntas":
                self.respuestas_usuario,

            "estadisticas_tema":
                self.obtener_estadisticas_tema(),

            "estadisticas_dificultad":
                self.obtener_estadisticas_dificultad()
        }


        ruta = os.path.join(
            self.obtener_ruta_resultados(),
            "reporte.json"
        )


        with open(
            ruta,
            "w",
            encoding="utf-8"
        ) as archivo:


            json.dump(
                reporte,
                archivo,
                indent=4,
                ensure_ascii=False
            )


        print("JSON generado correctamente")