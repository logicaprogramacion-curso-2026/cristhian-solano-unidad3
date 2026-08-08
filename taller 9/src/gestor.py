import pandas as pd
from entidad import pregunta
import json
import os


class Gestor:

    def __init__(self, dao):
        self.dao = dao
        self.preguntas = []


    def validar_datos(self, fila):
    
        campos = [
            "pregunta",
            "opcion_a",
            "opcion_b",
            "opcion_c",
            "opcion_d",
            "respuesta_correcta",
            "dificultad",
            "tema"
        ]

        # Validar campos obligatorios
        for campo in campos:
            if pd.isna(fila[campo]) or fila[campo] == "":
                return False


        # Validar respuesta correcta
        if fila["respuesta_correcta"] not in ["A", "B", "C", "D"]:
            return False


        # Validar dificultad
        if fila["dificultad"] not in ["Fácil", "Media", "Difícil"]:
            return False


        return True



    def convertir_a_objeto(self, fila):
        
        return pregunta(
            id=int(fila["id"]),
            pregunta=fila["pregunta"],
            opcion_a=fila["opcion_a"],
            opcion_b=fila["opcion_b"],
            opcion_c=fila["opcion_c"],
            opcion_d=fila["opcion_d"],
            respuesta_correcta=fila["respuesta_correcta"],
            dificultad=fila["dificultad"],
            tema=fila["tema"]
        )
        
        
    def cargar_desde_csv(self, ruta):
    
        self.preguntas.clear()

        df = pd.read_csv(ruta)

        df = df.rename(columns={
            "ID": "id",
            "Pregunta": "pregunta",
            "OpcionA": "opcion_a",
            "OpcionB": "opcion_b",
            "OpcionC": "opcion_c",
            "OpcionD": "opcion_d",
            "RespuestaCorrecta": "respuesta_correcta",
            "Dificultad": "dificultad",
            "Tema": "tema"
        })

        contador = 0

        for _, fila in df.iterrows():

            if self.validar_datos(fila):

                objeto = self.convertir_a_objeto(fila)
                self.preguntas.append(objeto)
                contador += 1

            else:
                print("Fila rechazada:")
                print(fila.to_dict())
                print("-" * 50)


        print(f"Preguntas cargadas: {contador}")
        
    def cargar_desde_json(self, ruta):
    
        self.preguntas.clear()

        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)


        preguntas = datos["cuestionario"]["preguntas"]

        df = pd.DataFrame(preguntas)


        df["opcion_a"] = df["opciones"].apply(lambda x: x["A"])
        df["opcion_b"] = df["opciones"].apply(lambda x: x["B"])
        df["opcion_c"] = df["opciones"].apply(lambda x: x["C"])
        df["opcion_d"] = df["opciones"].apply(lambda x: x["D"])


        df = df.drop(columns=["opciones"])


        contador = 0


        for _, fila in df.iterrows():

            if self.validar_datos(fila):

                p = pregunta(
                    int(fila["id"]),
                    fila["pregunta"],
                    fila["opcion_a"],
                    fila["opcion_b"],
                    fila["opcion_c"],
                    fila["opcion_d"],
                    fila["respuesta_correcta"],
                    fila["dificultad"],
                    fila["tema"]
                )

                self.preguntas.append(p)
                contador += 1


        print(f"Preguntas cargadas: {contador}")
    
    
    def cargar_desde_txt(self, ruta):
    
        self.preguntas.clear()

        with open(ruta, "r", encoding="utf-8") as f:
            lineas = [l.strip() for l in f.readlines()]


        i = 0


        while i < len(lineas):

            if lineas[i].startswith("ID:"):

                identificador = int(lineas[i].split(":")[1])


                tema = lineas[i+1].split(":",1)[1].strip()

                dificultad = lineas[i+2].split(":",1)[1].strip()

                pregunta_texto = lineas[i+3].split(":",1)[1].strip()


                opcion_a = lineas[i+6][3:].strip()
                opcion_b = lineas[i+7][3:].strip()
                opcion_c = lineas[i+8][3:].strip()
                opcion_d = lineas[i+9][3:].strip()


                respuesta = lineas[i+11].split(":")[1].strip()


                p = pregunta(
                    identificador,
                    pregunta_texto,
                    opcion_a,
                    opcion_b,
                    opcion_c,
                    opcion_d,
                    respuesta,
                    dificultad,
                    tema
                )


                self.preguntas.append(p)


            i += 1


        print(f"Preguntas cargadas: {len(self.preguntas)}")
            
    def guardar_en_base_datos(self):
        """
        Guarda todas las preguntas cargadas en la base de datos.
        """

        contador = 0

        for pregunta in self.preguntas:
            self.dao.insertar(pregunta)
            contador += 1

        print(f"\nSe guardaron {contador} preguntas en la base de datos.")
        
    def exportar_a_txt(self, nombre_archivo):

        os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)

        preguntas = self.dao.obtener_todas()

        with open(nombre_archivo, "w", encoding="utf-8") as archivo:

            for p in preguntas:

                archivo.write(f"{p.id}\n")
                archivo.write(f"{p.pregunta}\n")
                archivo.write(f"{p.opcion_a}\n")
                archivo.write(f"{p.opcion_b}\n")
                archivo.write(f"{p.opcion_c}\n")
                archivo.write(f"{p.opcion_d}\n")
                archivo.write(f"{p.respuesta_correcta}\n")
                archivo.write(f"{p.dificultad}\n")
                archivo.write(f"{p.tema}\n")
                archivo.write("-"*40+"\n")

        print("TXT exportado correctamente.")
        
    def exportar_a_csv(self, nombre_archivo):
    
        os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)

        preguntas = self.dao.obtener_todas()

        datos = []

        for p in preguntas:

            datos.append({
                "ID": p.id,
                "Pregunta": p.pregunta,
                "OpcionA": p.opcion_a,
                "OpcionB": p.opcion_b,
                "OpcionC": p.opcion_c,
                "OpcionD": p.opcion_d,
                "RespuestaCorrecta": p.respuesta_correcta,
                "Dificultad": p.dificultad,
                "Tema": p.tema
            })

        df = pd.DataFrame(datos)

        df.to_csv(nombre_archivo,
                index=False,
                encoding="utf-8-sig")

        print("CSV exportado correctamente.")
        
    
    def exportar_a_json(self, nombre_archivo):
    
        os.makedirs(os.path.dirname(nombre_archivo), exist_ok=True)

        preguntas = self.dao.obtener_todas()

        lista = []

        for p in preguntas:

            lista.append({

                "id": p.id,
                "pregunta": p.pregunta,
                "opciones": {
                    "A": p.opcion_a,
                    "B": p.opcion_b,
                    "C": p.opcion_c,
                    "D": p.opcion_d
                },
                "respuesta_correcta": p.respuesta_correcta,
                "dificultad": p.dificultad,
                "tema": p.tema

            })

        with open(nombre_archivo,
                "w",
                encoding="utf-8") as archivo:

            json.dump(lista,
                    archivo,
                    ensure_ascii=False,
                    indent=4)

        print("JSON exportado correctamente.")
        
        
    def estadisticas_por_tema(self):
    
        preguntas = self.dao.obtener_todas()

        estadisticas = {}

        for p in preguntas:

            if p.tema not in estadisticas:
                estadisticas[p.tema] = 0

            estadisticas[p.tema] += 1

        print("\nPreguntas por tema")

        for tema, cantidad in estadisticas.items():
            print(f"{tema}: {cantidad}")
            
            
    def estadisticas_por_dificultad(self):
    
        preguntas = self.dao.obtener_todas()

        estadisticas = {}

        for p in preguntas:

            if p.dificultad not in estadisticas:
                estadisticas[p.dificultad] = 0

            estadisticas[p.dificultad] += 1

        print("\nPreguntas por dificultad")

        for dificultad, cantidad in estadisticas.items():
            print(f"{dificultad}: {cantidad}")    
            
    