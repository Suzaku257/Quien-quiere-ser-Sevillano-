"""
Módulo de gestión de base de datos para la aplicación de quiz
Utiliza SQLite para máxima portabilidad sin dependencias externas
Thread-safe usando threading.local() para conexiones por thread
"""

import sqlite3
import hashlib
import os
import threading
from datetime import datetime


class DatabaseManager:
    """Gestor thread-safe de conexiones y operaciones con SQLite"""
    
    def __init__(self, database='quiz_sevilla.db'):
        self.database = database
        # Threading.local() almacena una conexión diferente por cada thread
        self._local = threading.local()
    
    def _get_connection(self):
        """Obtiene o crea una conexión para el thread actual"""
        if not hasattr(self._local, 'connection') or self._local.connection is None:
            # Cada thread crea su propia conexión
            self._local.connection = sqlite3.connect(
                self.database, 
                timeout=10.0,
                check_same_thread=True  # Seguro porque cada thread tiene su conexión
            )
            self._local.connection.row_factory = sqlite3.Row
        return self._local.connection
    
    def connect(self):
        """Establece conexión con la base de datos SQLite"""
        try:
            conn = self._get_connection()
            print(f"Conectado a {self.database}")
            return True
        except Exception as e:
            print(f"Error de conexión: {e}")
            return False
    
    @property
    def connection(self):
        """Propiedad para acceso a la conexión de este thread"""
        return self._get_connection()
    
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if hasattr(self._local, 'connection') and self._local.connection:
            self._local.connection.close()
            self._local.connection = None
            print("Desconectado de la base de datos")
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta que no retorna datos (INSERT, UPDATE, DELETE)"""
        cursor = None
        try:
            conn = self.connection
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return True, cursor.rowcount
        except Exception as e:
            conn.rollback()
            print(f"Error ejecutando query: {e}")
            return False, str(e)
        finally:
            if cursor:
                cursor.close()
    
    def fetch_query(self, query, params=None):
        """Ejecuta una consulta que retorna datos (SELECT)"""
        cursor = None
        try:
            conn = self.connection
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            # Convertir rows a diccionarios
            columns = [description[0] for description in cursor.description] if cursor.description else []
            result = []
            for row in cursor.fetchall():
                result.append(dict(zip(columns, row)))
            return result
        except Exception as e:
            print(f"Error en consulta: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    def hash_password(self, password):
        """Genera hash seguro de contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    # ============ OPERACIONES DE USUARIOS ============
    
    def register_user(self, nombre, email, password):
        """Registra un nuevo usuario"""
        password_hash = self.hash_password(password)
        query = "INSERT INTO usuarios (nombre, email, contraseña, fecha_registro) VALUES (?, ?, ?, ?)"
        success, result = self.execute_query(query, (nombre, email, password_hash, datetime.now()))
        return success, result
    
    def get_user_by_email(self, email):
        """Obtiene usuario por email"""
        query = "SELECT * FROM usuarios WHERE email = ?"
        return self.fetch_query(query, (email,))
    
    def get_user_by_id(self, user_id):
        """Obtiene usuario por ID"""
        query = "SELECT * FROM usuarios WHERE id = ?"
        result = self.fetch_query(query, (user_id,))
        return result[0] if result else None
    
    def verify_password(self, stored_hash, provided_password):
        """Verifica contraseña"""
        return stored_hash == self.hash_password(provided_password)
    
    # ============ OPERACIONES DE PREGUNTAS ============
    
    def get_all_questions(self):
        """Obtiene todas las preguntas"""
        query = """
        SELECT id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, categoria
        FROM preguntas
        ORDER BY id
        """
        return self.fetch_query(query)
    
    def get_question_by_id(self, question_id):
        """Obtiene una pregunta por ID"""
        query = """
        SELECT id, pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, categoria
        FROM preguntas
        WHERE id = ?
        """
        result = self.fetch_query(query, (question_id,))
        return result[0] if result else None
    
    def verify_answer(self, question_id, answer):
        """Verifica si la respuesta es correcta"""
        query = "SELECT respuesta_correcta FROM preguntas WHERE id = ?"
        result = self.fetch_query(query, (question_id,))
        if result:
            return result[0]['respuesta_correcta'] == answer
        return False
    
    # ============ OPERACIONES DE PUNTUACIONES ============
    
    def save_score(self, user_id, puntuacion_total, respuestas_correctas, respuestas_totales):
        """Guarda la puntuación del quiz"""
        query = """
        INSERT INTO puntuaciones (usuario_id, puntuacion_total, respuestas_correctas, respuestas_totales, fecha_intento)
        VALUES (?, ?, ?, ?, ?)
        """
        success, result = self.execute_query(
            query, 
            (user_id, puntuacion_total, respuestas_correctas, respuestas_totales, datetime.now())
        )
        return success, result
    
    def get_user_scores(self, user_id):
        """Obtiene el historial de puntuaciones de un usuario"""
        query = """
        SELECT * FROM puntuaciones
        WHERE usuario_id = ?
        ORDER BY fecha_intento DESC
        """
        scores = self.fetch_query(query, (user_id,))
        # Convertir strings de fecha a datetime para compatibilidad
        if scores:
            for score in scores:
                if isinstance(score['fecha_intento'], str):
                    score['fecha_intento'] = datetime.fromisoformat(score['fecha_intento'])
        return scores
    
    def get_user_stats(self, user_id):
        """Obtiene estadísticas generales del usuario"""
        query = """
        SELECT 
            COUNT(*) as total_intentos,
            MAX(puntuacion_total) as puntuacion_maxima,
            AVG(puntuacion_total) as puntuacion_promedio,
            SUM(respuestas_correctas) as total_respuestas_correctas
        FROM puntuaciones
        WHERE usuario_id = ?
        """
        result = self.fetch_query(query, (user_id,))
        return result[0] if result else None

    def get_global_stats(self):
        """Obtiene estadísticas globales de toda la aplicación"""
        query = """
        SELECT 
            COUNT(*) as total_intentos,
            COUNT(DISTINCT u.id) as total_usuarios,
            AVG(p.puntuacion_total) as puntuacion_promedio,
            MAX(p.puntuacion_total) as puntuacion_maxima,
            SUM(p.respuestas_correctas) as total_respuestas_correctas
        FROM puntuaciones p
        INNER JOIN usuarios u ON u.id = p.usuario_id
        """
        result = self.fetch_query(query)
        return result[0] if result else None

    def get_all_scores(self):
        """Obtiene todos los resultados con información del usuario"""
        query = """
        SELECT 
            p.id,
            p.fecha_intento,
            p.puntuacion_total,
            p.respuestas_correctas,
            p.respuestas_totales,
            u.id as usuario_id,
            u.nombre as usuario_nombre,
            u.email as usuario_email
        FROM puntuaciones p
        INNER JOIN usuarios u ON u.id = p.usuario_id
        ORDER BY p.fecha_intento DESC
        """
        scores = self.fetch_query(query)
        if scores:
            for score in scores:
                if isinstance(score['fecha_intento'], str):
                    try:
                        score['fecha_intento'] = datetime.fromisoformat(score['fecha_intento'])
                    except ValueError:
                        pass
        return scores or []

    def get_leaderboard(self):
        """Obtiene un ranking global de usuarios"""
        query = """
        SELECT 
            u.id as usuario_id,
            u.nombre,
            u.email,
            COUNT(p.id) as intentos,
            MAX(p.puntuacion_total) as puntuacion_maxima,
            AVG(p.puntuacion_total) as puntuacion_promedio,
            SUM(p.respuestas_correctas) as respuestas_correctas_totales
        FROM usuarios u
        LEFT JOIN puntuaciones p ON p.usuario_id = u.id
        GROUP BY u.id, u.nombre, u.email
        HAVING COUNT(p.id) > 0
        ORDER BY puntuacion_maxima DESC, puntuacion_promedio DESC, intentos DESC, u.nombre ASC
        """
        return self.fetch_query(query) or []

