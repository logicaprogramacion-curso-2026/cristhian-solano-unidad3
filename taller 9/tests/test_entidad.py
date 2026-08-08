import unittest
from src.entidad import pregunta


class TestPregunta(unittest.TestCase):


    def test_crear_pregunta(self):

        obj_pregunta = pregunta(
            1,
            "¿Qué lenguaje se usa en este proyecto?",
            "Java",
            "Python",
            "C++",
            "PHP",
            "B",
            "Fácil",
            "Programación"
        )


        self.assertEqual(
            obj_pregunta.pregunta,
            "¿Qué lenguaje se usa en este proyecto?"
        )


        self.assertEqual(
            obj_pregunta.respuesta_correcta,
            "B"
        )



    def test_respuesta_correcta(self):

        obj_pregunta = pregunta(
            1,
            "2+2=?",
            "3",
            "4",
            "5",
            "6",
            "B",
            "Fácil",
            "Matemática"
        )


        self.assertEqual(
            obj_pregunta.respuesta_correcta,
            "B"
        )


if __name__ == "__main__":
    unittest.main()