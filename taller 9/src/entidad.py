class pregunta:
    def __init__(self,
                 id = 0,
                 pregunta = "",
                 opcion_a = "",
                 opcion_b = "",
                 opcion_c = "",
                 opcion_d = "",
                 respuesta_correcta = "",
                 dificultad = "",
                 tema = ""):
    
        self.id = id
        self.pregunta = pregunta
        self.opcion_a = opcion_a
        self.opcion_b = opcion_b
        self.opcion_c = opcion_c
        self.opcion_d = opcion_d
        self.respuesta_correcta = respuesta_correcta
        self.dificultad = dificultad
        self.tema = tema   

    def __str__(self):
        return (
        f"Pregunta(id={self.id}, "
        f"pregunta='{self.pregunta}', "
        f"opcion_a='{self.opcion_a}', "
        f"opcion_b='{self.opcion_b}', "
        f"opcion_c='{self.opcion_c}', "
        f"opcion_d='{self.opcion_d}', "
        f"respuesta_correcta='{self.respuesta_correcta}', "
        f"dificultad='{self.dificultad}', "
        f"tema='{self.tema}')"
    )

def to_dict(self):
    return {
        "id": self.id,
        "pregunta": self.pregunta,
        "opcion_a": self.opcion_a,
        "opcion_b": self.opcion_b,
        "opcion_c": self.opcion_c,
        "opcion_d": self.opcion_d,
        "respuesta_correcta": self.respuesta_correcta,
        "dificultad": self.dificultad,
        "tema": self.tema
    }    