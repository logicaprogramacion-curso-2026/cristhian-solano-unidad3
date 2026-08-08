from entidad import pregunta  
import sqlite3

class preguntaDAO:
    
    def __init__(self, db):
        self.db = db

    def crear_tabla(self):
        self.db.cursor.execute('''
            CREATE TABLE IF NOT EXISTS preguntas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pregunta TEXT NOT NULL,
                opcion_a TEXT NOT NULL,
                opcion_b TEXT NOT NULL,
                opcion_c TEXT NOT NULL,
                opcion_d TEXT NOT NULL,
                respuesta_correcta TEXT NOT NULL CHECK (respuesta_correcta IN ('A', 'B', 'C', 'D')),
                dificultad TEXT NOT NULL CHECK (dificultad IN ('Fácil', 'Media', 'Difícil')),
                tema TEXT NOT NULL
            )
        ''')

    def insertar(self, pregunta):
       
        self.db.cursor.execute('''
            INSERT INTO preguntas (
                pregunta,
                opcion_a,
                opcion_b,
                opcion_c,
                opcion_d,
                respuesta_correcta,
                dificultad,
                tema
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            pregunta.pregunta,
            pregunta.opcion_a,
            pregunta.opcion_b,
            pregunta.opcion_c,
            pregunta.opcion_d,
            pregunta.respuesta_correcta,
            pregunta.dificultad,
            pregunta.tema
        ))

        self.db.conn.commit()
        return self.db.cursor.lastrowid
    
    def obtener_todas(self):
        self.db.cursor.execute("SELECT * FROM preguntas")

        registros = self.db.cursor.fetchall()

        preguntas = []

        for fila in registros:
            preguntas.append(
                pregunta(
                    fila[0],
                    fila[1],
                    fila[2],
                    fila[3],
                    fila[4],
                    fila[5],
                    fila[6],
                    fila[7],
                    fila[8]
                )
            )

        return preguntas

    def obtener_por_id(self, id):
        self.db.cursor.execute('''SELECT * FROM preguntas WHERE id = ?''', (id,))
        return self.db.cursor.fetchone()
    
        
    def limpiar_tabla(self):
        self.db.cursor.execute("DELETE FROM preguntas")
        self.db.cursor.execute("DELETE FROM sqlite_sequence WHERE name='preguntas'")
        self.db.conn.commit()