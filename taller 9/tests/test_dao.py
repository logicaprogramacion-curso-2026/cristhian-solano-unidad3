import unittest

from src.database import Database
from src.dao import preguntaDAO
from src.entidad import pregunta


class TestDAO(unittest.TestCase):


    def setUp(self):

        self.db = Database()

        self.dao = preguntaDAO(
            self.db
        )

        self.dao.crear_tabla()



    def test_insertar_pregunta(self):

        obj_pregunta = pregunta(

            1,
            "Capital de Ecuador",
            "Quito",
            "Lima",
            "Bogotá",
            "Caracas",
            "A",
            "Fácil",
            "Geografía"
        )


        resultado = self.dao.insertar(
            obj_pregunta
        )


        self.assertTrue(
            resultado
        )



    def test_consultar_preguntas(self):

        preguntas = self.dao.obtener_todas()


        self.assertIsNotNone(
            preguntas
        )


if __name__ == "__main__":
    unittest.main()