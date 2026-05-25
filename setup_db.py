"""
Script para crear la base de datos SQLite y poblarla con preguntas iniciales
Ejecutar: python setup_db.py
No requiere instalar nada - SQLite está incluido en Python
"""

import sqlite3
import os
from datetime import datetime

# Configuración de la base de datos SQLite
DB_FILE = 'quiz_sevilla.db'

PREGUNTAS_SEVILLA = [
    {
        'pregunta': '¿Cuál es la capital de España?',
        'opcion_a': 'Sevilla',
        'opcion_b': 'Madrid',
        'opcion_c': 'Barcelona',
        'opcion_d': 'Valencia',
        'respuesta_correcta': 'B',
        'categoria': 'geografía'
    },
    {
        'pregunta': '¿En qué año se realizó la Exposición Iberoamericana en Sevilla?',
        'opcion_a': '1920',
        'opcion_b': '1929',
        'opcion_c': '1950',
        'opcion_d': '1992',
        'respuesta_correcta': 'B',
        'categoria': 'historia'
    },
    {
        'pregunta': '¿Cuál es el monumento más emblemático de Sevilla?',
        'opcion_a': 'La Sagrada Familia',
        'opcion_b': 'La Catedral de Sevilla',
        'opcion_c': 'La Torre de Hércules',
        'opcion_d': 'El Acueducto de Segovia',
        'respuesta_correcta': 'B',
        'categoria': 'monumentos'
    },
    {
        'pregunta': '¿Qué ríos atraviesan Sevilla?',
        'opcion_a': 'El Tajo y el Duero',
        'opcion_b': 'El Guadalquivir',
        'opcion_c': 'El Ebro y el Júcar',
        'opcion_d': 'El Genil',
        'respuesta_correcta': 'B',
        'categoria': 'geografía'
    },
    {
        'pregunta': '¿De cuántas naves consta la Catedral de Sevilla?',
        'opcion_a': 'Tres',
        'opcion_b': 'Cuatro',
        'opcion_c': 'Cinco',
        'opcion_d': 'Seis',
        'respuesta_correcta': 'C',
        'categoria': 'monumentos'
    },
    {
        'pregunta': '¿En qué barrio se encuentra el Real Alcázar de Sevilla?',
        'opcion_a': 'Triana',
        'opcion_b': 'Santa Cruz',
        'opcion_c': 'Macarena',
        'opcion_d': 'Arenal',
        'respuesta_correcta': 'B',
        'categoria': 'monumentos'
    },
    {
        'pregunta': '¿Cuándo se celebra la Feria de Sevilla?',
        'opcion_a': 'En diciembre',
        'opcion_b': 'En enero',
        'opcion_c': 'En abril/mayo',
        'opcion_d': 'En agosto',
        'respuesta_correcta': 'C',
        'categoria': 'tradiciones'
    },
    {
        'pregunta': '¿Quién diseñó la Torre del Oro?',
        'opcion_a': 'Los almohades',
        'opcion_b': 'Los cristianos en la Reconquista',
        'opcion_c': 'El Renacimiento español',
        'opcion_d': 'Los borbones',
        'respuesta_correcta': 'A',
        'categoria': 'historia'
    },
    {
        'pregunta': '¿Cuál es la altura aproximada de la Giralda?',
        'opcion_a': '97 metros',
        'opcion_b': '105 metros',
        'opcion_c': '120 metros',
        'opcion_d': '150 metros',
        'respuesta_correcta': 'A',
        'categoria': 'monumentos'
    },
    {
        'pregunta': '¿Qué tipo de arte es característico de Sevilla en sus azulejos?',
        'opcion_a': 'Gótico',
        'opcion_b': 'Barroco',
        'opcion_c': 'Azulejos mudéjar',
        'opcion_d': 'Neoclásico',
        'respuesta_correcta': 'C',
        'categoria': 'cultura'
    },
    {
        'pregunta': 'María Jiménez fue una famosa cantante sevillana de:',
        'opcion_a': 'Flamenco',
        'opcion_b': 'Copla',
        'opcion_c': 'Zarzuela',
        'opcion_d': 'Ópera',
        'respuesta_correcta': 'B',
        'categoria': 'cultura'
    },
    {
        'pregunta': '¿En qué siglo fue construida la Casa de Pilatos?',
        'opcion_a': 'Siglo XIV',
        'opcion_b': 'Siglo XV',
        'opcion_c': 'Siglo XVI',
        'opcion_d': 'Siglo XVII',
        'respuesta_correcta': 'C',
        'categoria': 'monumentos'
    },
    {
        'pregunta': '¿Cuántas plazas principales tiene el Barrio de Santa Cruz?',
        'opcion_a': '2',
        'opcion_b': '3',
        'opcion_c': '4',
        'opcion_d': '5',
        'respuesta_correcta': 'B',
        'categoria': 'geografía'
    },
    {
        'pregunta': '¿Qué famoso artista sevillano pintó cuadros sobre las corridas de toros?',
        'opcion_a': 'Diego Velázquez',
        'opcion_b': 'Francisco Goya',
        'opcion_c': 'Bartolomé Murillo',
        'opcion_d': 'Alejo Fernández',
        'respuesta_correcta': 'A',
        'categoria': 'cultura'
    },
    {
        'pregunta': '¿Cuándo fue proclamada Sevilla como Patrimonio de la Humanidad la zona de Santa Cruz?',
        'opcion_a': '1970',
        'opcion_b': '1987',
        'opcion_c': '2000',
        'opcion_d': '2010',
        'respuesta_correcta': 'B',
        'categoria': 'historia'
    },
    {
        'pregunta': '¿En qué siglo llegó Cristóbal Colón a Sevilla?',
        'opcion_a': 'Siglo XIV',
        'opcion_b': 'Siglo XV',
        'opcion_c': 'Siglo XVI',
        'opcion_d': 'Siglo XVII',
        'respuesta_correcta': 'B',
        'categoria': 'historia'
    },
    {
        'pregunta': '¿Qué festival internacional es muy importante en Sevilla?',
        'opcion_a': 'Festival de Cine de San Sebastián',
        'opcion_b': 'Festival de Flamenco de Jerez',
        'opcion_c': 'Bienal de Sevilla',
        'opcion_d': 'Festival de Danza de Cannes',
        'respuesta_correcta': 'C',
        'categoria': 'cultura'
    },
    {
        'pregunta': '¿Cuántas iglesias tiene aproximadamente el barrio de la Macarena?',
        'opcion_a': '5',
        'opcion_b': '8',
        'opcion_c': '12',
        'opcion_d': '15',
        'respuesta_correcta': 'C',
        'categoria': 'monumentos'
    },
    {
        'pregunta': '¿Qué famoso toreo sevillano fue banderillero en los años 60?',
        'opcion_a': 'Vaquero',
        'opcion_b': 'Chicuelina',
        'opcion_c': 'Costillares',
        'opcion_d': 'Pedro Romero',
        'respuesta_correcta': 'A',
        'categoria': 'tradiciones'
    },
    {
        'pregunta': '¿En qué año se celebraron los Juegos Olímpicos en Barcelona, donde muchos sevillanos participaron?',
        'opcion_a': '1980',
        'opcion_b': '1988',
        'opcion_c': '1992',
        'opcion_d': '2000',
        'respuesta_correcta': 'C',
        'categoria': 'historia'
    },
    {
        'pregunta': '¿Cuál es la característica más distintiva del barrio de Triana?',
        'opcion_a': 'Ser un barrio de pescadores',
        'opcion_b': 'Ser conocido por sus alfareros y ceramistas',
        'opcion_c': 'Ser el barrio judío medieval',
        'opcion_d': 'Ser la zona de palacios renacentistas',
        'respuesta_correcta': 'B',
        'categoria': 'geografía'
    }
]


def create_database():
    """Crea la base de datos SQLite si no existe"""
    try:
        # SQLite crea el archivo automáticamente
        conn = sqlite3.connect(DB_FILE)
        conn.close()
        print(f"✓ Base de datos {DB_FILE} lista")
        return True
    except Exception as e:
        print(f"✗ Error creando BD: {e}")
        return False


def create_tables():
    """Crea las tablas de la base de datos"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL,
            fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            activo INTEGER DEFAULT 1
        )
        """)
        print("✓ Tabla usuarios creada")
        
        # Tabla de preguntas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS preguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pregunta TEXT NOT NULL,
            opcion_a TEXT NOT NULL,
            opcion_b TEXT NOT NULL,
            opcion_c TEXT NOT NULL,
            opcion_d TEXT NOT NULL,
            respuesta_correcta TEXT NOT NULL,
            categoria TEXT,
            dificultad TEXT DEFAULT 'media'
        )
        """)
        print("✓ Tabla preguntas creada")
        
        # Tabla de puntuaciones
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS puntuaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            puntuacion_total INTEGER NOT NULL,
            respuestas_correctas INTEGER NOT NULL,
            respuestas_totales INTEGER NOT NULL,
            fecha_intento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
        )
        """)
        print("✓ Tabla puntuaciones creada")
        
        # Crear índices
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON usuarios(email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuario ON puntuaciones(usuario_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fecha ON puntuaciones(fecha_intento)")
        
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"✗ Error creando tablas: {e}")
        return False
    return True


def populate_questions():
    """Puebla la tabla de preguntas con datos iniciales"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        query = """
        INSERT INTO preguntas (pregunta, opcion_a, opcion_b, opcion_c, opcion_d, respuesta_correcta, categoria)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        for q in PREGUNTAS_SEVILLA:
            cursor.execute(query, (
                q['pregunta'],
                q['opcion_a'],
                q['opcion_b'],
                q['opcion_c'],
                q['opcion_d'],
                q['respuesta_correcta'],
                q['categoria']
            ))
        
        conn.commit()
        print(f"✓ {len(PREGUNTAS_SEVILLA)} preguntas insertadas")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"✗ Error insertando preguntas: {e}")
        return False
    return True


def main():
    """Ejecuta el setup completo"""
    print("=== SETUP BASE DE DATOS QUIZ SEVILLA ===\n")
    
    print("[1/3] Creando base de datos...")
    if not create_database():
        return
    
    print("[2/3] Creando tablas...")
    if not create_tables():
        return
    
    print("[3/3] Poblando preguntas...")
    if not populate_questions():
        return
    
    print("\n✓ Setup completado exitosamente")
    print("Puede ejecutar: python app.py")


if __name__ == '__main__':
    main()
