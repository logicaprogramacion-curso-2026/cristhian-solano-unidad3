import sqlite3
import os


class Database:

    def __init__(self):

        # Sale de src y entra al proyecto
        ruta_proyecto = os.path.dirname(os.path.dirname(__file__))

        # Entra a la carpeta database
        carpeta_database = os.path.join(
            ruta_proyecto,
            "database"
        )

        # Si no existe la carpeta, la crea
        os.makedirs(carpeta_database, exist_ok=True)

        # Archivo SQLite
        ruta_db = os.path.join(
            carpeta_database,
            "preguntas.db"
        )

        self.conn = sqlite3.connect(ruta_db)
        self.cursor = self.conn.cursor()

        print("BD ubicada en:", ruta_db)


    def cerrar(self):
        self.conn.close()