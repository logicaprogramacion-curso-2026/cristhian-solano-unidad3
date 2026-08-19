"""
Sistema de Evaluación Formativa de Competencias Digitales Asistida por IA
Implementa el siguiente flujo:

1. El docente describe una actividad que va a realizar.
2. La IA analiza qué tan completa está la actividad respecto a los
   resultados que se buscan.
3. La IA evalúa la eficiencia de la actividad aunque no cuente con
   muchos parámetros (funciona con información parcial).
4. La IA detecta las deficiencias en la propuesta del docente.
5. La IA estima el posible enfoque que tomará el estudiante.
"""

from dataclasses import dataclass
from typing import Dict, List




@dataclass
class ActividadDocente:
    descripcion: str
    objetivo: str = ""
    competencia_digital: str = ""
    instrumento_evaluacion: str = ""
    tiempo_estimado: str = ""
    recursos: str = ""

    def parametros_completados(self) -> Dict[str, bool]:
        """Indica qué parámetros fueron proporcionados por el docente."""
        return {
            "descripcion": bool(self.descripcion.strip()),
            "objetivo": bool(self.objetivo.strip()),
            "competencia_digital": bool(self.competencia_digital.strip()),
            "instrumento_evaluacion": bool(self.instrumento_evaluacion.strip()),
            "tiempo_estimado": bool(self.tiempo_estimado.strip()),
            "recursos": bool(self.recursos.strip()),
        }


class EvaluadorIA:
    PALABRAS_CLAVE_COMPETENCIAS = [
        "búsqueda de información", "seguridad digital", "comunicación digital",
        "colaboración en línea", "creación de contenido", "pensamiento crítico",
        "alfabetización digital", "ciudadanía digital", "resolución de problemas",
    ]

    PESOS_PARAMETROS = {
        "descripcion": 0.30,
        "objetivo": 0.20,
        "competencia_digital": 0.20,
        "instrumento_evaluacion": 0.15,
        "tiempo_estimado": 0.075,
        "recursos": 0.075,
    }

    def __init__(self, actividad: ActividadDocente):
        self.actividad = actividad

    def evaluar_completitud(self) -> float:
        params = self.actividad.parametros_completados()
        completitud = sum(
            self.PESOS_PARAMETROS[p] for p, presente in params.items() if presente
        )
        return round(completitud * 100, 1)

    def evaluar_eficiencia(self) -> Dict[str, float]:
        params = self.actividad.parametros_completados()
        n_presentes = sum(params.values())
        n_total = len(params)
        confianza = round((n_presentes / n_total) * 100, 1)

        texto = self.actividad.descripcion.lower()
        senales_positivas = sum(
            1 for palabra in self.PALABRAS_CLAVE_COMPETENCIAS if palabra in texto
        )
        puntaje_base = min(100, 40 + senales_positivas * 15)


        eficiencia = round(puntaje_base * (0.5 + 0.5 * (confianza / 100)), 1)

        return {"eficiencia_estimada": eficiencia, "confianza": confianza}

    def detectar_deficiencias(self) -> List[str]:
        deficiencias = []
        params = self.actividad.parametros_completados()

        if not params["objetivo"]:
            deficiencias.append("No se especificó un objetivo de aprendizaje claro.")
        if not params["competencia_digital"]:
            deficiencias.append("No se indicó qué competencia digital se trabaja.")
        if not params["instrumento_evaluacion"]:
            deficiencias.append("Falta un instrumento o rúbrica de evaluación.")
        if not params["tiempo_estimado"]:
            deficiencias.append("No se definió el tiempo estimado de la actividad.")
        if not params["recursos"]:
            deficiencias.append("No se detallaron los recursos o herramientas digitales requeridas.")

        texto = self.actividad.descripcion.lower()
        if not any(p in texto for p in self.PALABRAS_CLAVE_COMPETENCIAS):
            deficiencias.append(
                "La descripción no menciona explícitamente ninguna competencia digital reconocible."
            )

        if not deficiencias:
            deficiencias.append("No se detectaron deficiencias relevantes en la actividad descrita.")

        return deficiencias

    def estimar_enfoque_estudiante(self) -> str:
        texto = self.actividad.descripcion.lower()

        if "colabora" in texto or "grupo" in texto or "equipo" in texto:
            return ("El estudiante probablemente abordará la actividad de forma "
                    "colaborativa, priorizando la coordinación con sus compañeros.")
        elif "individual" in texto:
            return ("El estudiante probablemente resolverá la actividad de forma "
                    "autónoma, enfocándose en su propio desempeño.")
        elif "investiga" in texto or "búsqueda" in texto:
            return ("El estudiante probablemente centrará su esfuerzo en la búsqueda "
                    "y verificación de información.")
        elif "crea" in texto or "diseñ" in texto or "produc" in texto:
            return ("El estudiante probablemente se enfocará en el proceso creativo "
                    "y la calidad del producto final.")
        else:
            return ("El enfoque del estudiante es incierto; se recomienda especificar "
                    "mejor la modalidad de trabajo (individual/grupal) y el tipo de tarea.")



class SimuladorEvaluacionFormativa:
    def __init__(self, actividad: ActividadDocente):
        self.actividad = actividad
        self.evaluador = EvaluadorIA(actividad)

    def ejecutar(self) -> Dict:
        eficiencia = self.evaluador.evaluar_eficiencia()
        return {
            "completitud_%": self.evaluador.evaluar_completitud(),
            "eficiencia_estimada_%": eficiencia["eficiencia_estimada"],
            "confianza_%": eficiencia["confianza"],
            "deficiencias_docente": self.evaluador.detectar_deficiencias(),
            "enfoque_probable_estudiante": self.evaluador.estimar_enfoque_estudiante(),
        }

    def imprimir_reporte(self):
        r = self.ejecutar()
        print("=" * 62)
        print("REPORTE DE EVALUACIÓN FORMATIVA ASISTIDA POR IA")
        print("=" * 62)
        print(f"Completitud de la actividad:  {r['completitud_%']}%")
        print(f"Eficiencia estimada:           {r['eficiencia_estimada_%']}%")
        print(f"Confianza del análisis:        {r['confianza_%']}%")
        print("\nDeficiencias detectadas en el docente:")
        for d in r["deficiencias_docente"]:
            print(f"  - {d}")
        print(f"\nEnfoque probable del estudiante:\n  {r['enfoque_probable_estudiante']}")
        print("=" * 62)



if __name__ == "__main__":
    actividad = ActividadDocente(
        descripcion=(
            "Los estudiantes trabajarán en grupo para investigar sobre seguridad "
            "digital y crear una infografía colaborativa usando herramientas en línea."
        ),
        objetivo="Fomentar el pensamiento crítico frente a riesgos digitales.",
        competencia_digital="Seguridad digital y creación de contenido",
        instrumento_evaluacion="",  # parámetro faltante a propósito
        tiempo_estimado="2 semanas",
        recursos="Canva, computadoras con acceso a internet",
    )

    SimuladorEvaluacionFormativa(actividad).imprimir_reporte()